import logging
import math
import random
import time

from SimConnect import *


class SimconnectForceCalculator:
    def __init__(self):
        self.simConnect = SimConnect(auto_connect=False)
        self.aircraftRequests = AircraftRequests(self.simConnect, _time=0)
        self.last_connection_attempt = 0
        self.typical_wingspan = 35
        self.last_stall_update_time = 0
        self.last_overspeed_update_time = 0
        self.stall_direction = 0
        self.overspeed_direction = 0
        self.shaker_direction = 0
        self.gear_change_start_time = None
        self.last_shaker_update_time = 0
        self.update_frequency_ms = 10
        self.previous_gear_position = 0.0
        self.max_aoa = 25
        self.coefficients = {
            'rotation_velocity_body_x': 0.2,
            'rotation_velocity_body_y': 0.2,
            'elevator_position': 0.2,
            'aileron_position': 0.2,
            'aoa': 0.2,
            'gear': 0.0,
            'elevator_trim_position': 0.1,
            'stick_shaker': 0.5,
            'stall_severity': 0.3,
            'overspeed_severity': 0.3,
            'weight_ratio': 0.2,
        }

    def linear_interpolate(self, envelope: any, value: float):
        """
        Return the interpolated value based on the envelope.
        The envelope must be sorted eg:
            [
                (0.0, 0.2), # magnitude, coefficient
                (0.5, 0.3),
                (1.0, 0.4),
            ]
        """
        if type(envelope) != list:
            return envelope
        if len(envelope) == 1:
            return envelope[0][1]

        if value <= envelope[0][0]:
            return envelope[0][1]
        elif value >= envelope[-1][0]:
            return envelope[-1][1]

        # Loop through the points to find the correct interval
        for i in range(len(envelope) - 1):
            x0, y0 = envelope[i]
            x1, y1 = envelope[i + 1]

            if x0 <= value <= x1:
                # Linear interpolation formula: y = y0 + (y1 - y0) * (value - x0) / (x1 - x0)
                return y0 + (y1 - y0) * (value - x0) / (x1 - x0)

    def apply_force(self, magnitude, direction):
        return magnitude * math.cos(math.radians(direction)), magnitude * math.sin(math.radians(direction))

    def calculate_force(self):
        x_force, y_force = 0, 0
        now = int(round(time.time() * 1000))

        if not self.simConnect.ok:
            if now - self.last_connection_attempt > 1000:
                try:
                    self.last_connection_attempt = now
                    self.simConnect.connect()
                except ConnectionError as e:
                    logging.error(e)
            return x_force, y_force

        if self.simConnect.paused:
            return x_force, y_force

        # Get data from SimConnect
        # May need to normalize the inputs
        elevator_trim_position = self.aircraftRequests.get("ELEVATOR_TRIM_POSITION")
        elevator_position = self.aircraftRequests.get("ELEVATOR_POSITION")
        aileron_position = self.aircraftRequests.get("AILERON_POSITION")
        airspeed = self.aircraftRequests.get("AIRSPEED_INDICATED")
        aoa = self.aircraftRequests.get("ANGLE_OF_ATTACK_INDICATOR")
        gear_position = self.aircraftRequests.get("GEAR_HANDLE_POSITION")
        current_weight = self.aircraftRequests.get("TOTAL_WEIGHT")
        reference_weight = self.aircraftRequests.get("MAX_GROSS_WEIGHT")
        weight_ratio = current_weight / reference_weight
        weight_ratio_coefficient = self.linear_interpolate(self.coefficients['weight_ratio'], weight_ratio)
        stick_shaker = self.aircraftRequests.get("STICK_SHAKER")  # Returns 1 if active, 0 if not
        airspeed_barber_pole = self.aircraftRequests.get("AIRSPEED_BARBER_POLE")
        rotation_velocity_body_x = self.aircraftRequests.get(
            "ROTATION_VELOCITY_BODY_X")  # Rotation relative to aircraft axis, Feet per second
        rotation_velocity_body_y = self.aircraftRequests.get(
            "ROTATION_VELOCITY_BODY_Y")  # Rotation relative to aircraft axis, Feet per second

        # Rotation velocity effects on control surfaces
        rotation_velocity_body_x_coefficient = (
            self.linear_interpolate(self.coefficients['rotation_velocity_body_x'], rotation_velocity_body_x))
        rotation_velocity_body_x_magnitude = abs(rotation_velocity_body_x) * rotation_velocity_body_x_coefficient
        rotation_velocity_body_x_direction = 0 if rotation_velocity_body_x > 0 else 180
        x, y = self.apply_force(rotation_velocity_body_x_magnitude, rotation_velocity_body_x_direction)
        x_force += x
        y_force += y

        rotation_velocity_body_y_coefficient = (
            self.linear_interpolate(self.coefficients['rotation_velocity_body_y'], rotation_velocity_body_y))
        rotation_velocity_body_y_magnitude = abs(rotation_velocity_body_y) * rotation_velocity_body_y_coefficient
        rotation_velocity_body_y_direction = 0 if rotation_velocity_body_y > 0 else 180
        x, y = self.apply_force(rotation_velocity_body_y_magnitude, rotation_velocity_body_y_direction)
        x_force += x
        y_force += y

        # Airspeed effects on control surfaces
        elevator_coefficient = self.linear_interpolate(self.coefficients['elevator_position'], abs(elevator_position))
        elevator_magnitude = ((airspeed / airspeed_barber_pole) * weight_ratio_coefficient * abs(
            elevator_position)) * elevator_coefficient
        elevator_direction = 0 if elevator_position > 0 else 180
        x, y = self.apply_force(elevator_magnitude, elevator_direction)  # Assuming a forward force for elevator
        x_force += x
        y_force += y

        aileron_coefficient = self.linear_interpolate(self.coefficients['aileron_position'], abs(aileron_position))
        aileron_magnitude = ((airspeed / airspeed_barber_pole) * weight_ratio_coefficient * abs(
            aileron_position)) * aileron_coefficient
        aileron_direction = 90 if aileron_position > 0 else 270
        x, y = self.apply_force(aileron_magnitude, aileron_direction)
        x_force += x
        y_force += y

        # AoA effects
        aoa_coefficient = self.linear_interpolate(self.coefficients['aoa'], aoa)
        aoa_magnitude = (aoa / self.max_aoa) * aoa_coefficient
        x, y = self.apply_force(aoa_magnitude, 0)
        x_force += x
        y_force += y

        # Gear effects
        if gear_position != self.previous_gear_position:
            # Check if this is the start of the gear change
            if self.gear_change_start_time is None:
                self.gear_change_start_time = now
            time_since_gear_change = now - self.gear_change_start_time

            # Only apply the effect if it's within the desired duration (e.g., 3000 ms or 3 seconds)
            if time_since_gear_change < 3000:
                gear_coefficient = self.linear_interpolate(self.coefficients['gear'], gear_position)
                gear_magnitude = 1 * gear_coefficient
                x, y = self.apply_force(gear_magnitude, 0)
                x_force += x
                y_force += y

            # If gear has completed its transition, reset the start time
            if gear_position in [0, 1]:  # assuming 0 is fully retracted and 1 is fully extended
                self.gear_change_start_time = None
            self.previous_gear_position = gear_position

        # Trim Effects
        # Assuming trim value is in the range [-1, 1]
        # A positive trim value indicates nose down, while negative indicates nose up.
        # this is wrong, trim should remove force
        elevator_trim_coefficient = self.linear_interpolate(self.coefficients['elevator_trim_position'],
                                                            abs(elevator_trim_position))
        elevator_trim_force = abs(elevator_trim_position) * elevator_trim_coefficient
        direction_trim = 0 if elevator_trim_position > 0 else 180
        x, y = self.apply_force(elevator_trim_force, direction_trim)
        x_force += x
        y_force += y

        # Stick Shaker effect
        if stick_shaker == 1:
            stick_shaker_coefficient = self.linear_interpolate(self.coefficients['stick_shaker'], stick_shaker)
            magnitude_shaker = 1 * stick_shaker_coefficient
            if now - self.last_shaker_update_time > self.update_frequency_ms:
                self.shaker_direction = random.uniform(0, 360)
                self.last_shaker_update_time = now
            x, y = self.apply_force(magnitude_shaker, self.shaker_direction)
            x_force += x
            y_force += y

        # Stall Buffet based on aoa
        if aoa > 20:
            stall_severity = (aoa - 20) / 5
            stall_severity_coefficient = self.linear_interpolate(self.coefficients['stall_severity'], stall_severity)
            magnitude_stall = stall_severity * stall_severity_coefficient
            if now - self.last_stall_update_time > self.update_frequency_ms:
                self.stall_direction = random.uniform(0, 360)
                self.last_stall_update_time = now
            x, y = self.apply_force(magnitude_stall, self.stall_direction)
            x_force += x
            y_force += y

        # Overspeed Shake based on speed
        if airspeed > airspeed_barber_pole:
            overspeed_severity = (airspeed - airspeed_barber_pole) / 10
            overspeed_severity_coefficient = self.linear_interpolate(
                self.coefficients['overspeed_severity'], overspeed_severity)
            magnitude_overspeed = overspeed_severity * overspeed_severity_coefficient
            if now - self.last_overspeed_update_time > self.update_frequency_ms:
                self.overspeed_direction = random.uniform(0, 360)
                self.last_overspeed_update_time = now
            x, y = self.apply_force(magnitude_overspeed, self.overspeed_direction)
            x_force += x
            y_force += y

        # Convert back to magnitude and direction for the resultant force
        resultant_magnitude = math.sqrt(x_force ** 2 + y_force ** 2)
        resultant_direction = math.degrees(math.atan2(y_force, x_force)) % 360

        # Normalize magnitude
        resultant_magnitude = min(max(resultant_magnitude, 0.0), 1.0)

        return resultant_magnitude, resultant_direction
