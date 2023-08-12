import logging
import signal
import sys
import time
from ctypes import c_long, c_ushort, c_short

import sdl2
import sdl2.ext

joystick = None
haptic = None
spring_effect_id = 0
spring_effect = None


def stop_sdl_joysitck_haptics():
    global haptic
    global joystick
    global spring_effect_id

    if haptic:
        sdl2.SDL_HapticStopAll(haptic)
        if spring_effect_id >= 0:
            sdl2.SDL_HapticDestroyEffect(haptic, spring_effect_id)
            spring_effect = None
        sdl2.SDL_HapticClose(haptic)
    if joystick:
        sdl2.SDL_JoystickClose(joystick)


def signal_handler(sig, frame):
    stop_sdl_joysitck_haptics()
    sys.exit(0)


def run():
    global haptic
    global joystick
    global spring_effect_id

    start = time.time()

    joystick_index = None

    num_joysticks = sdl2.SDL_NumJoysticks()
    for i in range(num_joysticks):
        joystick_name = sdl2.SDL_JoystickNameForIndex(i).decode('utf-8')
        logging.info(f"Found joystick {joystick_name}")
        if joystick_name == 'TinyUSB Device':
            joystick_index = i

    if joystick_index is None:
        logging.error("No joystick index set.")
        return

    joystick = sdl2.SDL_JoystickOpen(joystick_index)
    if not joystick:
        logging.error("Failed to open the joystick!")
        stop_sdl_joysitck_haptics()
        return

    joystick_name = sdl2.SDL_JoystickName(joystick).decode('utf-8')
    logging.info(f"Device {joystick_index}: {joystick_name}")

    haptic = sdl2.SDL_HapticOpenFromJoystick(joystick)
    if not haptic:
        logging.warning("Joystick does not support haptics!")
        sdl2.SDL_JoystickClose(joystick)
        return

    if haptic:
        logging.info(
            f"Supports {sdl2.haptic.SDL_HapticNumEffects(haptic)} simultaneous effects.")
        effects_supported = sdl2.haptic.SDL_HapticQuery(haptic)
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

    if haptic:
        spring_effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SPRING)
        spring_effect.condition.direction.type = sdl2.SDL_HAPTIC_POLAR
        spring_effect.condition.direction.dir = (c_long * 3)(0, 0, 0)
        spring_effect.condition.length = sdl2.SDL_HAPTIC_INFINITY

        satd = 1
        coeffd = 12
        deadbandd = 0

        sat = (c_ushort * 3)(int(65535 / satd), int(65535 / satd), int(65535 / satd))  # 0..65535
        coeff = (c_short * 3)(int(32767 / coeffd), int(32767 / coeffd), int(32767 / coeffd))  # -32768..32767

        spring_effect.condition.right_sat = sat
        spring_effect.condition.left_sat = sat
        spring_effect.condition.right_coeff = coeff
        spring_effect.condition.left_coeff = coeff
        spring_effect.condition.length = sdl2.SDL_HAPTIC_INFINITY
        spring_effect.condition.deadband = (c_ushort * 3)(int(deadbandd), int(deadbandd), int(deadbandd))
        spring_effect_id = sdl2.SDL_HapticNewEffect(haptic, spring_effect)
        if spring_effect_id < 0:
            logging.info("Failed to create the spring haptic effect!")
            stop_sdl_joysitck_haptics()
            return
        sdl2.SDL_HapticRunEffect(haptic, spring_effect_id, 1)

    while True:
        if time.time() - start > 5000:
            print('!!BREAK!!')


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    logging.basicConfig(level=logging.INFO)
    sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_HAPTIC)
    run()
    sdl2.SDL_Quit()
