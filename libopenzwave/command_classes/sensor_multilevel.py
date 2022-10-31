# -*- coding: utf-8 -*-

# **libopenzwave** is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# **libopenzwave** is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""

This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)
:synopsis: COMMAND_CLASS_SENSOR_MULTILEVEL

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Multilevel Sensor Command Class - Active
# Application
COMMAND_CLASS_SENSOR_MULTILEVEL = 0x31


class SensorMultilevelSensor(object):

    def __init__(self, node, value):
        self._node = node
        self.__value = value

    @property
    def type(self):
        """
        Alarm type

        :rtype: str
        """
        return self.__value.label

    @property
    def reading(self):
        """
        Sensor Reading

        :rtype: Any
        """
        return self.__value.data

    @property
    def units(self):
        """
        Sensor Unit of Measure

        :rtype: str
        """

        unit_index = self.__value.index + 255

        for value in self._node.values:
            if value.index == unit_index:
                return value.data

        return ''


# noinspection PyAbstractClass
class SensorMultilevel(zwave_cmd_class.ZWaveCommandClass):
    """
    Sensor Multilevel Command Class

    symbol: `COMMAND_CLASS_SENSOR_MULTILEVEL`
    """

    class_id = COMMAND_CLASS_SENSOR_MULTILEVEL
    class_desc = 'COMMAND_CLASS_SENSOR_MULTILEVEL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        sensor_air_temperature = 1
        sensor_general_purpose = 2
        sensor_luminance = 3
        sensor_power = 4
        sensor_humidity = 5
        sensor_velocity = 6
        sensor_direction = 7
        sensor_atmospheric_pressure = 8
        sensor_barometric_pressure = 9
        sensor_solar_radiation = 10
        sensor_dew_point = 11
        sensor_rain_rate = 12
        sensor_tide_level = 13
        sensor_weight = 14
        sensor_voltage = 15
        sensor_current = 16
        sensor_carbon_dioxide = 17
        sensor_air_flow = 18
        sensor_tank_capacity = 19
        sensor_distance = 20
        sensor_angle_position = 21
        sensor_rotation = 22
        sensor_water_temperature = 23
        sensor_soil_temperature = 24
        sensor_seismic_intensity = 25
        sensor_seismic_magnitude = 26
        sensor_ultraviolet = 27
        sensor_electrical_resistivity = 28
        sensor_electrical_conductivity = 29
        sensor_loudness = 30
        sensor_moisture = 31
        sensor_frequency = 32
        sensor_time = 33
        sensor_target_temperature = 34
        sensor_particulate_mater_2_5 = 35
        sensor_formaldehyde_ch20_level = 36
        sensor_radon_concentration = 37
        sensor_methane_density = 38
        sensor_volatile_organic_compound = 39
        sensor_carbon_monoxide = 40
        sensor_soil_humidity = 41
        sensor_soil_reactivity = 42
        sensor_soil_salinity = 43
        sensor_heart_beat = 44
        sensor_blood_pressure = 45
        sensor_muscle_mass = 46
        sensor_fat_mass = 47
        sensor_bone_mass = 48
        sensor_total_body_water = 49
        sensor_basic_metabolic_rate = 50
        sensor_body_mass_index = 51
        sensor_x_axis_acceleration = 52
        sensor_y_axis_acceleration = 53
        sensor_z_axis_acceleration = 54
        sensor_smoke_density = 55
        sensor_water_flow = 56
        sensor_water_pressure = 57
        sensor_rf_signal_strength = 58
        sensor_particulate_matter = 59
        sensor_respiratory_rate = 60
        sensor_relative_modulation = 61
        sensor_boiler_water_temperature = 62
        sensor_domestic_hot_water_temperature = 63
        sensor_outside_temperature = 64
        sensor_exhaust_temperature = 65
        sensor_water_chlorine = 66
        sensor_water_acidity = 67
        sensor_water_oxidation_reduction_potential = 68
        sensor_heart_rate_lf_hf_ratio = 69
        sensor_motion_direction = 70
        sensor_applied_force = 71
        sensor_return_air_temperature = 72
        sensor_supply_air_temperature = 73
        sensor_condenser_coil_temperature = 74
        sensor_evaporator_coil_temperature = 75
        sensor_liquid_line_temperature = 76
        sensor_discharge_line_temperature = 77
        sensor_suction = 78
        sensor_discharge = 79
        sensor_defrost_temperature = 80
        sensor_ozone = 81
        sensor_sulfur_dioxide = 82
        sensor_nitrogen_dioxide = 83
        sensor_ammonia = 84
        sensor_lead = 85
        sensor_particulate_matter_v2 = 86
        sensor_air_temperature_units = 256
        sensor_general_purpose_units = 257
        sensor_luminance_units = 258
        sensor_power_units = 259
        sensor_humidity_units = 260
        sensor_velocity_units = 261
        sensor_direction_units = 262
        sensor_atmospheric_pressure_units = 263
        sensor_barometric_pressure_units = 264
        sensor_solar_radiation_units = 265
        sensor_dew_point_units = 266
        sensor_rain_rate_units = 267
        sensor_tide_level_units = 268
        sensor_weight_units = 269
        sensor_voltage_units = 270
        sensor_current_units = 271
        sensor_carbon_dioxide_units = 272
        sensor_air_flow_units = 273
        sensor_tank_capacity_units = 274
        sensor_distance_units = 275
        sensor_angle_position_units = 276
        sensor_rotation_units = 277
        sensor_water_temperature_units = 278
        sensor_soil_temperature_units = 279
        sensor_seismic_intensity_units = 280
        sensor_seismic_magnitude_units = 281
        sensor_ultraviolet_units = 282
        sensor_electrical_resistivity_units = 283
        sensor_electrical_conductivity_units = 284
        sensor_loudness_units = 285
        sensor_moisture_units = 286
        sensor_frequency_units = 287
        sensor_time_units = 288
        sensor_target_temperature_units = 289
        sensor_particulate_mater_2_5_units = 290
        sensor_formaldehyde_ch20_level_units = 291
        sensor_radon_concentration_units = 292
        sensor_methane_density_units = 293
        sensor_volatile_organic_compound_units = 294
        sensor_carbon_monoxide_units = 295
        sensor_soil_humidity_units = 296
        sensor_soil_reactivity_units = 297
        sensor_soil_salinity_units = 298
        sensor_heart_beat_units = 299
        sensor_blood_pressure_units = 300
        sensor_muscle_mass_units = 301
        sensor_fat_mass_units = 302
        sensor_bone_mass_units = 303
        sensor_total_body_water_units = 304
        sensor_basic_metabolic_rate_units = 305
        sensor_body_mass_index_units = 306
        sensor_x_axis_acceleration_units = 307
        sensor_y_axis_acceleration_units = 308
        sensor_z_axis_acceleration_units = 309
        sensor_smoke_density_units = 310
        sensor_water_flow_units = 311
        sensor_water_pressure_units = 312
        sensor_rf_signal_strength_units = 313
        sensor_particulate_matter_units = 314
        sensor_respiratory_rate_units = 315
        sensor_relative_modulation_units = 316
        sensor_boiler_water_temperature_units = 317
        sensor_domestic_hot_water_temperature_units = 318
        sensor_outside_temperature_units = 319
        sensor_exhaust_temperature_units = 320
        sensor_water_chlorine_units = 321
        sensor_water_acidity_units = 322
        sensor_water_oxidation_reduction_potential_units = 323
        sensor_heart_rate_lf_hf_ratio_units = 324
        sensor_motion_direction_units = 325
        sensor_applied_force_units = 326
        sensor_return_air_temperature_units = 327
        sensor_supply_air_temperature_units = 328
        sensor_condenser_coil_temperature_units = 329
        sensor_evaporator_coil_temperature_units = 330
        sensor_liquid_line_temperature_units = 331
        sensor_discharge_line_temperature_units = 332
        sensor_suction_units = 333
        sensor_discharge_units = 334
        sensor_defrost_temperature_units = 335
        sensor_ozone_units = 336
        sensor_sulfur_dioxide_units = 337
        sensor_nitrogen_dioxide_units = 338
        sensor_ammonia_units = 339
        sensor_lead_units = 340
        sensor_particulate_matter_v2_units = 341

    @property
    def sensors_multilevel(self):
        """
        Multilevel Sensors.

        :return: list of :py:class:`SensorMultilevel.SensorMultilevelSensor`
                 instances
        :rtype: List[SensorMultilevelSensor]
        """
        res = []
        for i in range(1, 87):
            for key, value in SensorMultilevel.ValueIndexes.__dict__.items():
                if value == i:
                    value = getattr(self.values, key)
                    if value.data is not None:
                        res += [SensorMultilevelSensor(self, value)]
        return res
