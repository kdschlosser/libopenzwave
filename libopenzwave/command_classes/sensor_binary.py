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
:synopsis: COMMAND_CLASS_SENSOR_BINARY

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Binary Sensor Command Class - Depreciated
# Application
COMMAND_CLASS_SENSOR_BINARY = 0x30


class SensorBinarySensor(object):

    def __init__(self, value):
        self._value = value

    @property
    def type(self):
        """
        Alarm type

        :rtype: str
        """
        return self._value.label

    @property
    def reading(self):
        """
        Sensor Reading

        :rtype: Any
        """
        return self._value.data

    @property
    def units(self):
        """
        Sensor Unit of Measure

        :rtype: str
        """
        return self._value.units


# noinspection PyAbstractClass
class SensorBinary(zwave_cmd_class.ZWaveCommandClass):
    """
    Sensor Binary Command Class

    symbol: `COMMAND_CLASS_SENSOR_BINARY`
    """

    class_id = COMMAND_CLASS_SENSOR_BINARY
    class_desc = 'COMMAND_CLASS_SENSOR_BINARY'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        sensor_binary_1 = 0
        sensor_binary_2 = 1
        sensor_binary_3 = 2
        sensor_binary_4 = 3
        sensor_binary_5 = 4
        sensor_binary_6 = 5
        sensor_binary_7 = 6
        sensor_binary_8 = 7
        sensor_binary_9 = 8
        sensor_binary_10 = 9
        sensor_binary_11 = 10
        sensor_binary_12 = 11
        sensor_binary_13 = 12
        sensor_binary_14 = 13
        sensor_binary_15 = 14
        sensor_binary_16 = 15
        sensor_binary_17 = 16
        sensor_binary_18 = 17
        sensor_binary_19 = 18
        sensor_binary_20 = 19
        sensor_binary_21 = 20
        sensor_binary_22 = 21
        sensor_binary_23 = 22
        sensor_binary_24 = 23
        sensor_binary_25 = 24
        sensor_binary_26 = 25
        sensor_binary_27 = 26
        sensor_binary_28 = 27
        sensor_binary_29 = 28
        sensor_binary_30 = 29
        sensor_binary_31 = 30
        sensor_binary_32 = 31
        sensor_binary_33 = 32
        sensor_binary_34 = 33
        sensor_binary_35 = 34
        sensor_binary_36 = 35
        sensor_binary_37 = 36
        sensor_binary_38 = 37
        sensor_binary_39 = 38
        sensor_binary_40 = 39
        sensor_binary_41 = 40
        sensor_binary_42 = 41
        sensor_binary_43 = 42
        sensor_binary_44 = 43
        sensor_binary_45 = 44
        sensor_binary_46 = 45
        sensor_binary_47 = 46
        sensor_binary_48 = 47
        sensor_binary_49 = 48
        sensor_binary_50 = 49
        sensor_binary_51 = 50
        sensor_binary_52 = 51
        sensor_binary_53 = 52
        sensor_binary_54 = 53
        sensor_binary_55 = 54
        sensor_binary_56 = 55
        sensor_binary_57 = 56
        sensor_binary_58 = 57
        sensor_binary_59 = 58
        sensor_binary_60 = 59
        sensor_binary_61 = 60
        sensor_binary_62 = 61
        sensor_binary_63 = 62
        sensor_binary_64 = 63
        sensor_binary_65 = 64
        sensor_binary_66 = 65
        sensor_binary_67 = 66
        sensor_binary_68 = 67
        sensor_binary_69 = 68
        sensor_binary_70 = 69
        sensor_binary_71 = 70
        sensor_binary_72 = 71
        sensor_binary_73 = 72
        sensor_binary_74 = 73
        sensor_binary_75 = 74
        sensor_binary_76 = 75
        sensor_binary_77 = 76
        sensor_binary_78 = 77
        sensor_binary_79 = 78
        sensor_binary_80 = 79
        sensor_binary_81 = 80
        sensor_binary_82 = 81
        sensor_binary_83 = 82
        sensor_binary_84 = 83
        sensor_binary_85 = 84
        sensor_binary_86 = 85
        sensor_binary_87 = 86
        sensor_binary_88 = 87
        sensor_binary_89 = 88
        sensor_binary_90 = 89
        sensor_binary_91 = 90
        sensor_binary_92 = 91
        sensor_binary_93 = 92
        sensor_binary_94 = 93
        sensor_binary_95 = 94
        sensor_binary_96 = 95
        sensor_binary_97 = 96
        sensor_binary_98 = 97
        sensor_binary_99 = 98
        sensor_binary_100 = 99
        sensor_binary_101 = 100
        sensor_binary_102 = 101
        sensor_binary_103 = 102
        sensor_binary_104 = 103
        sensor_binary_105 = 104
        sensor_binary_106 = 105
        sensor_binary_107 = 106
        sensor_binary_108 = 107
        sensor_binary_109 = 108
        sensor_binary_110 = 109
        sensor_binary_111 = 110
        sensor_binary_112 = 111
        sensor_binary_113 = 112
        sensor_binary_114 = 113
        sensor_binary_115 = 114
        sensor_binary_116 = 115
        sensor_binary_117 = 116
        sensor_binary_118 = 117
        sensor_binary_119 = 118
        sensor_binary_120 = 119
        sensor_binary_121 = 120
        sensor_binary_122 = 121
        sensor_binary_123 = 122
        sensor_binary_124 = 123
        sensor_binary_125 = 124
        sensor_binary_126 = 125
        sensor_binary_127 = 126
        sensor_binary_128 = 127
        sensor_binary_129 = 128
        sensor_binary_130 = 129
        sensor_binary_131 = 130
        sensor_binary_132 = 131
        sensor_binary_133 = 132
        sensor_binary_134 = 133
        sensor_binary_135 = 134
        sensor_binary_136 = 135
        sensor_binary_137 = 136
        sensor_binary_138 = 137
        sensor_binary_139 = 138
        sensor_binary_140 = 139
        sensor_binary_141 = 140
        sensor_binary_142 = 141
        sensor_binary_143 = 142
        sensor_binary_144 = 143
        sensor_binary_145 = 144
        sensor_binary_146 = 145
        sensor_binary_147 = 146
        sensor_binary_148 = 147
        sensor_binary_149 = 148
        sensor_binary_150 = 149
        sensor_binary_151 = 150
        sensor_binary_152 = 151
        sensor_binary_153 = 152
        sensor_binary_154 = 153
        sensor_binary_155 = 154
        sensor_binary_156 = 155
        sensor_binary_157 = 156
        sensor_binary_158 = 157
        sensor_binary_159 = 158
        sensor_binary_160 = 159
        sensor_binary_161 = 160
        sensor_binary_162 = 161
        sensor_binary_163 = 162
        sensor_binary_164 = 163
        sensor_binary_165 = 164
        sensor_binary_166 = 165
        sensor_binary_167 = 166
        sensor_binary_168 = 167
        sensor_binary_169 = 168
        sensor_binary_170 = 169
        sensor_binary_171 = 170
        sensor_binary_172 = 171
        sensor_binary_173 = 172
        sensor_binary_174 = 173
        sensor_binary_175 = 174
        sensor_binary_176 = 175
        sensor_binary_177 = 176
        sensor_binary_178 = 177
        sensor_binary_179 = 178
        sensor_binary_180 = 179
        sensor_binary_181 = 180
        sensor_binary_182 = 181
        sensor_binary_183 = 182
        sensor_binary_184 = 183
        sensor_binary_185 = 184
        sensor_binary_186 = 185
        sensor_binary_187 = 186
        sensor_binary_188 = 187
        sensor_binary_189 = 188
        sensor_binary_190 = 189
        sensor_binary_191 = 190
        sensor_binary_192 = 191
        sensor_binary_193 = 192
        sensor_binary_194 = 193
        sensor_binary_195 = 194
        sensor_binary_196 = 195
        sensor_binary_197 = 196
        sensor_binary_198 = 197
        sensor_binary_199 = 198
        sensor_binary_200 = 199
        sensor_binary_201 = 200
        sensor_binary_202 = 201
        sensor_binary_203 = 202
        sensor_binary_204 = 203
        sensor_binary_205 = 204
        sensor_binary_206 = 205
        sensor_binary_207 = 206
        sensor_binary_208 = 207
        sensor_binary_209 = 208
        sensor_binary_210 = 209
        sensor_binary_211 = 210
        sensor_binary_212 = 211
        sensor_binary_213 = 212
        sensor_binary_214 = 213
        sensor_binary_215 = 214
        sensor_binary_216 = 215
        sensor_binary_217 = 216
        sensor_binary_218 = 217
        sensor_binary_219 = 218
        sensor_binary_220 = 219
        sensor_binary_221 = 220
        sensor_binary_222 = 221
        sensor_binary_223 = 222
        sensor_binary_224 = 223
        sensor_binary_225 = 224
        sensor_binary_226 = 225
        sensor_binary_227 = 226
        sensor_binary_228 = 227
        sensor_binary_229 = 228
        sensor_binary_230 = 229
        sensor_binary_231 = 230
        sensor_binary_232 = 231
        sensor_binary_233 = 232
        sensor_binary_234 = 233
        sensor_binary_235 = 234
        sensor_binary_236 = 235
        sensor_binary_237 = 236
        sensor_binary_238 = 237
        sensor_binary_239 = 238
        sensor_binary_240 = 239
        sensor_binary_241 = 240
        sensor_binary_242 = 241
        sensor_binary_243 = 242
        sensor_binary_244 = 243
        sensor_binary_245 = 244
        sensor_binary_246 = 245
        sensor_binary_247 = 246
        sensor_binary_248 = 247
        sensor_binary_249 = 248
        sensor_binary_250 = 249
        sensor_binary_251 = 250
        sensor_binary_252 = 251
        sensor_binary_253 = 252
        sensor_binary_254 = 253
        sensor_binary_255 = 254

    @property
    def sensors_binary(self):
        """
        Binary sensors.

        :return: list of
            :py:class:`libopenzwave.command_classes.sensor_binary.SensorBinarySensor`
            instances

        :rtype: List[SensorBinarySensor]
        """
        res = []
        for i in range(1, 256):
            for key, value in SensorBinary.ValueIndexes.__dict__.items():
                if value == i:
                    value = getattr(self.values, key)
                    if value.data.data is not None:
                        res += [SensorBinarySensor(value)]
        return res
