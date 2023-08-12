import logging
import time
from ctypes import c_long, c_ushort, c_short

import sdl2
import sdl2.ext
from PySide6 import QtCore

from simconnect_force_calculator import SimconnectForceCalculator


class SimConnectWorkerSignals(QtCore.QObject):
    stopped = QtCore.Signal()
    started = QtCore.Signal()
    force_updated = QtCore.Signal(float, float)


class SimConnectWorker(QtCore.QRunnable):
    def __init__(self, simconnect_force_calculator: SimconnectForceCalculator, joystick_index=None):
        super(SimConnectWorker, self).__init__()
        self.signals = SimConnectWorkerSignals()
        self.running = False
        self.simconnect_force_calculator = simconnect_force_calculator
        self.last_update_time = 0
        self.update_frequency_ms = 10
        self.joystick_index = joystick_index
        self.joystick = None
        self.haptic = None
        self.constant_effect = None
        self.constant_effect_id = None
        self.spring_effect = None
        self.spring_effect_id = None
        self.simconnect_force_calculator.update_frequency_ms = self.update_frequency_ms

    @QtCore.Slot()
    def run(self):
        if self.joystick_index == None:
            logging.error("No joystick index set.")
            self.running = False
            return

        self.joystick = sdl2.SDL_JoystickOpen(self.joystick_index)
        if not self.joystick:
            logging.error("Failed to open the joystick!")
            self.stop_sdl_joysitck_haptics()
            self.running = False
            return

        joystick_name = sdl2.SDL_JoystickName(self.joystick).decode('utf-8')
        logging.info(f"Device {self.joystick_index}: {joystick_name}")

        self.haptic = sdl2.SDL_HapticOpenFromJoystick(self.joystick)
        if not self.haptic:
            logging.warning("Joystick does not support haptics!")
            sdl2.SDL_JoystickClose(self.joystick)
            return

        if self.haptic:
            logging.info(
                f"Supports {sdl2.haptic.SDL_HapticNumEffects(self.haptic)} simultaneous effects.")
            effects_supported = sdl2.haptic.SDL_HapticQuery(self.haptic)
            logging.info("Supported Effects:")
            if effects_supported & sdl2.SDL_HAPTIC_SPRING:
                logging.info("- SDL_HAPTIC_SPRING")
            if effects_supported & sdl2.SDL_HAPTIC_LEFTRIGHT:
                logging.info("- SDL_HAPTIC_LEFTRIGHT")
            if effects_supported & sdl2.SDL_HAPTIC_TRIANGLE:
                logging.info("- SDL_HAPTIC_TRIANGLE")
            if effects_supported & sdl2.SDL_HAPTIC_SAWTOOTHUP:
                logging.info("- SDL_HAPTIC_SAWTOOTHUP")
            if effects_supported & sdl2.SDL_HAPTIC_SAWTOOTHDOWN:
                logging.info("- SDL_HAPTIC_SAWTOOTHDOWN")
            if effects_supported & sdl2.SDL_HAPTIC_RAMP:
                logging.info("- SDL_HAPTIC_RAMP")
            if effects_supported & sdl2.SDL_HAPTIC_SPRING:
                logging.info("- SDL_HAPTIC_SPRING")
            if effects_supported & sdl2.SDL_HAPTIC_DAMPER:
                logging.info("- SDL_HAPTIC_DAMPER")
            if effects_supported & sdl2.SDL_HAPTIC_INERTIA:
                logging.info("- SDL_HAPTIC_INERTIA")
            if effects_supported & sdl2.SDL_HAPTIC_FRICTION:
                logging.info("- SDL_HAPTIC_FRICTION")
            if effects_supported & sdl2.SDL_HAPTIC_CUSTOM:
                logging.info("- SDL_HAPTIC_CUSTOM")

        if self.haptic:
            self.spring_effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SPRING)
            self.spring_effect.condition.direction.type = sdl2.SDL_HAPTIC_POLAR
            self.spring_effect.condition.direction.dir = (c_long * 3)(0, 0, 0)
            self.spring_effect.condition.length = sdl2.SDL_HAPTIC_INFINITY
            self.spring_effect.condition.right_sat = (c_ushort * 3)(65535, 65535, 65535)  # 0..65535
            self.spring_effect.condition.left_sat = (c_ushort * 3)(65535, 65535, 65535)
            self.spring_effect.condition.right_coeff = (c_short * 3)(32767, 32767, 32767)  # -32768..32767
            self.spring_effect.condition.left_coeff = (c_short * 3)(32767, 32767, 32767)
            self.spring_effect.condition.length = sdl2.SDL_HAPTIC_INFINITY
            self.spring_effect_id = sdl2.SDL_HapticNewEffect(self.haptic, self.spring_effect)
            if self.spring_effect_id < 0:
                logging.info("Failed to create the spring haptic effect!")
                self.stop_sdl_joysitck_haptics()
                self.running = False
                return
            sdl2.SDL_HapticRunEffect(self.haptic, self.spring_effect_id, 1)

            self.constant_effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_CONSTANT)
            self.constant_effect.constant.direction.type = sdl2.SDL_HAPTIC_POLAR
            self.constant_effect.constant.direction.dir = (c_long * 3)(0, 0, 0)
            self.constant_effect.constant.length = sdl2.SDL_HAPTIC_INFINITY
            self.constant_effect.constant.level = 0

            self.constant_effect_id = sdl2.SDL_HapticNewEffect(self.haptic, self.constant_effect)
            if self.constant_effect_id < 0:
                logging.info("Failed to create the constant haptic effect!")
                self.stop_sdl_joysitck_haptics()
                self.running = False
                return

            sdl2.SDL_HapticRunEffect(self.haptic, self.constant_effect_id, 1)

        self.running = True
        self.signals.started.emit()
        while self.running:
            if int(round(time.time() * 1000)) - self.last_update_time > self.update_frequency_ms:
                magnitude, direction = self.simconnect_force_calculator.calculate_force()
                self.apply_haptic_effect(magnitude, direction)
                self.signals.force_updated.emit(magnitude, direction)
            QtCore.QThread.yieldCurrentThread()
        self.stop_sdl_joysitck_haptics()
        self.signals.stopped.emit()

    @QtCore.Slot()
    def stop(self):
        self.running = False

    def apply_haptic_effect(self, magnitude, force_direction):
        self.constant_effect.constant.level = int(32767 * magnitude)
        self.constant_effect.constant.direction.dir = (c_long * 3)(int(force_direction), 0, 0)
        sdl2.SDL_HapticUpdateEffect(self.haptic, self.constant_effect_id, self.constant_effect)

    def stop_sdl_joysitck_haptics(self):
        if self.haptic:
            sdl2.SDL_HapticStopAll(self.haptic)
            if self.constant_effect_id >= 0:
                sdl2.SDL_HapticDestroyEffect(self.haptic, self.constant_effect_id)
                self.constant_effect = None
            if self.spring_effect_id >= 0:
                sdl2.SDL_HapticDestroyEffect(self.haptic, self.spring_effect_id)
                self.spring_effect = None
            sdl2.SDL_HapticClose(self.haptic)
        if self.joystick:
            sdl2.SDL_JoystickClose(self.joystick)
