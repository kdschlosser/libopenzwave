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
:synopsis: COMMAND_CLASS_SENSOR_ALARM

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Alarm Sensor Command Class - Depreciated
# Application
COMMAND_CLASS_SENSOR_ALARM = 0x9C


class SensorAlarmSensor(object):

    def __init__(self, value):
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
        return self.__value.units


# noinspection PyAbstractClass
class SensorAlarm(zwave_cmd_class.ZWaveCommandClass):
    """
    Sensor Alarm Command Class

    symbol: `COMMAND_CLASS_SENSOR_ALARM`
    """

    class_id = COMMAND_CLASS_SENSOR_ALARM
    class_desc = 'COMMAND_CLASS_SENSOR_ALARM'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        sensor_alarm_1 = 0
        sensor_alarm_2 = 1
        sensor_alarm_3 = 2
        sensor_alarm_4 = 3
        sensor_alarm_5 = 4
        sensor_alarm_6 = 5
        sensor_alarm_7 = 6
        sensor_alarm_8 = 7
        sensor_alarm_9 = 8
        sensor_alarm_10 = 9
        sensor_alarm_11 = 10
        sensor_alarm_12 = 11
        sensor_alarm_13 = 12
        sensor_alarm_14 = 13
        sensor_alarm_15 = 14
        sensor_alarm_16 = 15
        sensor_alarm_17 = 16
        sensor_alarm_18 = 17
        sensor_alarm_19 = 18
        sensor_alarm_20 = 19
        sensor_alarm_21 = 20
        sensor_alarm_22 = 21
        sensor_alarm_23 = 22
        sensor_alarm_24 = 23
        sensor_alarm_25 = 24
        sensor_alarm_26 = 25
        sensor_alarm_27 = 26
        sensor_alarm_28 = 27
        sensor_alarm_29 = 28
        sensor_alarm_30 = 29
        sensor_alarm_31 = 30
        sensor_alarm_32 = 31
        sensor_alarm_33 = 32
        sensor_alarm_34 = 33
        sensor_alarm_35 = 34
        sensor_alarm_36 = 35
        sensor_alarm_37 = 36
        sensor_alarm_38 = 37
        sensor_alarm_39 = 38
        sensor_alarm_40 = 39
        sensor_alarm_41 = 40
        sensor_alarm_42 = 41
        sensor_alarm_43 = 42
        sensor_alarm_44 = 43
        sensor_alarm_45 = 44
        sensor_alarm_46 = 45
        sensor_alarm_47 = 46
        sensor_alarm_48 = 47
        sensor_alarm_49 = 48
        sensor_alarm_50 = 49
        sensor_alarm_51 = 50
        sensor_alarm_52 = 51
        sensor_alarm_53 = 52
        sensor_alarm_54 = 53
        sensor_alarm_55 = 54
        sensor_alarm_56 = 55
        sensor_alarm_57 = 56
        sensor_alarm_58 = 57
        sensor_alarm_59 = 58
        sensor_alarm_60 = 59
        sensor_alarm_61 = 60
        sensor_alarm_62 = 61
        sensor_alarm_63 = 62
        sensor_alarm_64 = 63
        sensor_alarm_65 = 64
        sensor_alarm_66 = 65
        sensor_alarm_67 = 66
        sensor_alarm_68 = 67
        sensor_alarm_69 = 68
        sensor_alarm_70 = 69
        sensor_alarm_71 = 70
        sensor_alarm_72 = 71
        sensor_alarm_73 = 72
        sensor_alarm_74 = 73
        sensor_alarm_75 = 74
        sensor_alarm_76 = 75
        sensor_alarm_77 = 76
        sensor_alarm_78 = 77
        sensor_alarm_79 = 78
        sensor_alarm_80 = 79
        sensor_alarm_81 = 80
        sensor_alarm_82 = 81
        sensor_alarm_83 = 82
        sensor_alarm_84 = 83
        sensor_alarm_85 = 84
        sensor_alarm_86 = 85
        sensor_alarm_87 = 86
        sensor_alarm_88 = 87
        sensor_alarm_89 = 88
        sensor_alarm_90 = 89
        sensor_alarm_91 = 90
        sensor_alarm_92 = 91
        sensor_alarm_93 = 92
        sensor_alarm_94 = 93
        sensor_alarm_95 = 94
        sensor_alarm_96 = 95
        sensor_alarm_97 = 96
        sensor_alarm_98 = 97
        sensor_alarm_99 = 98
        sensor_alarm_100 = 99
        sensor_alarm_101 = 100
        sensor_alarm_102 = 101
        sensor_alarm_103 = 102
        sensor_alarm_104 = 103
        sensor_alarm_105 = 104
        sensor_alarm_106 = 105
        sensor_alarm_107 = 106
        sensor_alarm_108 = 107
        sensor_alarm_109 = 108
        sensor_alarm_110 = 109
        sensor_alarm_111 = 110
        sensor_alarm_112 = 111
        sensor_alarm_113 = 112
        sensor_alarm_114 = 113
        sensor_alarm_115 = 114
        sensor_alarm_116 = 115
        sensor_alarm_117 = 116
        sensor_alarm_118 = 117
        sensor_alarm_119 = 118
        sensor_alarm_120 = 119
        sensor_alarm_121 = 120
        sensor_alarm_122 = 121
        sensor_alarm_123 = 122
        sensor_alarm_124 = 123
        sensor_alarm_125 = 124
        sensor_alarm_126 = 125
        sensor_alarm_127 = 126
        sensor_alarm_128 = 127
        sensor_alarm_129 = 128
        sensor_alarm_130 = 129
        sensor_alarm_131 = 130
        sensor_alarm_132 = 131
        sensor_alarm_133 = 132
        sensor_alarm_134 = 133
        sensor_alarm_135 = 134
        sensor_alarm_136 = 135
        sensor_alarm_137 = 136
        sensor_alarm_138 = 137
        sensor_alarm_139 = 138
        sensor_alarm_140 = 139
        sensor_alarm_141 = 140
        sensor_alarm_142 = 141
        sensor_alarm_143 = 142
        sensor_alarm_144 = 143
        sensor_alarm_145 = 144
        sensor_alarm_146 = 145
        sensor_alarm_147 = 146
        sensor_alarm_148 = 147
        sensor_alarm_149 = 148
        sensor_alarm_150 = 149
        sensor_alarm_151 = 150
        sensor_alarm_152 = 151
        sensor_alarm_153 = 152
        sensor_alarm_154 = 153
        sensor_alarm_155 = 154
        sensor_alarm_156 = 155
        sensor_alarm_157 = 156
        sensor_alarm_158 = 157
        sensor_alarm_159 = 158
        sensor_alarm_160 = 159
        sensor_alarm_161 = 160
        sensor_alarm_162 = 161
        sensor_alarm_163 = 162
        sensor_alarm_164 = 163
        sensor_alarm_165 = 164
        sensor_alarm_166 = 165
        sensor_alarm_167 = 166
        sensor_alarm_168 = 167
        sensor_alarm_169 = 168
        sensor_alarm_170 = 169
        sensor_alarm_171 = 170
        sensor_alarm_172 = 171
        sensor_alarm_173 = 172
        sensor_alarm_174 = 173
        sensor_alarm_175 = 174
        sensor_alarm_176 = 175
        sensor_alarm_177 = 176
        sensor_alarm_178 = 177
        sensor_alarm_179 = 178
        sensor_alarm_180 = 179
        sensor_alarm_181 = 180
        sensor_alarm_182 = 181
        sensor_alarm_183 = 182
        sensor_alarm_184 = 183
        sensor_alarm_185 = 184
        sensor_alarm_186 = 185
        sensor_alarm_187 = 186
        sensor_alarm_188 = 187
        sensor_alarm_189 = 188
        sensor_alarm_190 = 189
        sensor_alarm_191 = 190
        sensor_alarm_192 = 191
        sensor_alarm_193 = 192
        sensor_alarm_194 = 193
        sensor_alarm_195 = 194
        sensor_alarm_196 = 195
        sensor_alarm_197 = 196
        sensor_alarm_198 = 197
        sensor_alarm_199 = 198
        sensor_alarm_200 = 199
        sensor_alarm_201 = 200
        sensor_alarm_202 = 201
        sensor_alarm_203 = 202
        sensor_alarm_204 = 203
        sensor_alarm_205 = 204
        sensor_alarm_206 = 205
        sensor_alarm_207 = 206
        sensor_alarm_208 = 207
        sensor_alarm_209 = 208
        sensor_alarm_210 = 209
        sensor_alarm_211 = 210
        sensor_alarm_212 = 211
        sensor_alarm_213 = 212
        sensor_alarm_214 = 213
        sensor_alarm_215 = 214
        sensor_alarm_216 = 215
        sensor_alarm_217 = 216
        sensor_alarm_218 = 217
        sensor_alarm_219 = 218
        sensor_alarm_220 = 219
        sensor_alarm_221 = 220
        sensor_alarm_222 = 221
        sensor_alarm_223 = 222
        sensor_alarm_224 = 223
        sensor_alarm_225 = 224
        sensor_alarm_226 = 225
        sensor_alarm_227 = 226
        sensor_alarm_228 = 227
        sensor_alarm_229 = 228
        sensor_alarm_230 = 229
        sensor_alarm_231 = 230
        sensor_alarm_232 = 231
        sensor_alarm_233 = 232
        sensor_alarm_234 = 233
        sensor_alarm_235 = 234
        sensor_alarm_236 = 235
        sensor_alarm_237 = 236
        sensor_alarm_238 = 237
        sensor_alarm_239 = 238
        sensor_alarm_240 = 239
        sensor_alarm_241 = 240
        sensor_alarm_242 = 241
        sensor_alarm_243 = 242
        sensor_alarm_244 = 243
        sensor_alarm_245 = 244
        sensor_alarm_246 = 245
        sensor_alarm_247 = 246
        sensor_alarm_248 = 247
        sensor_alarm_249 = 248
        sensor_alarm_250 = 249
        sensor_alarm_251 = 250
        sensor_alarm_252 = 251
        sensor_alarm_253 = 252
        sensor_alarm_254 = 253
        sensor_alarm_255 = 254

    @property
    def sensor_alarms(self):
        """
        Alarm sensors.

        :return: list of
            :py:class:`libopenzwave.command_classes.sensor_alarm.SensorAlarmSensor`
            instances

        :rtype: List[SensorAlarmSensor]
        """
        res = []
        for i in range(1, 256):
            for key, value in SensorAlarm.ValueIndexes.__dict__.items():
                if value == i:
                    value = getattr(self.values, key)
                    if value.data is not None:
                        res += [SensorAlarmSensor(value)]
        return res
