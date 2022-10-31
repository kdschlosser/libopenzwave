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
:synopsis: COMMAND_CLASS_CONFIGURATION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Configuration Command Class - Active
# Application
COMMAND_CLASS_CONFIGURATION = 0x70


# noinspection PyAbstractClass
class Configuration(zwave_cmd_class.ZWaveCommandClass):
    """
    Configuration Command Class

    symbol: `COMMAND_CLASS_CONFIGURATION`
    """

    class_id = COMMAND_CLASS_CONFIGURATION
    class_desc = 'COMMAND_CLASS_CONFIGURATION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        parameter_1 = 1
        parameter_2 = 2
        parameter_3 = 3
        parameter_4 = 4
        parameter_5 = 5
        parameter_6 = 6
        parameter_7 = 7
        parameter_8 = 8
        parameter_9 = 9
        parameter_10 = 10
        parameter_11 = 11
        parameter_12 = 12
        parameter_13 = 13
        parameter_14 = 14
        parameter_15 = 15
        parameter_16 = 16
        parameter_17 = 17
        parameter_18 = 18
        parameter_19 = 19
        parameter_20 = 20
        parameter_21 = 21
        parameter_22 = 22
        parameter_23 = 23
        parameter_24 = 24
        parameter_25 = 25
        parameter_26 = 26
        parameter_27 = 27
        parameter_28 = 28
        parameter_29 = 29
        parameter_30 = 30
        parameter_31 = 31
        parameter_32 = 32
        parameter_33 = 33
        parameter_34 = 34
        parameter_35 = 35
        parameter_36 = 36
        parameter_37 = 37
        parameter_38 = 38
        parameter_39 = 39
        parameter_40 = 40
        parameter_41 = 41
        parameter_42 = 42
        parameter_43 = 43
        parameter_44 = 44
        parameter_45 = 45
        parameter_46 = 46
        parameter_47 = 47
        parameter_48 = 48
        parameter_49 = 49
        parameter_50 = 50
        parameter_51 = 51
        parameter_52 = 52
        parameter_53 = 53
        parameter_54 = 54
        parameter_55 = 55
        parameter_56 = 56
        parameter_57 = 57
        parameter_58 = 58
        parameter_59 = 59
        parameter_60 = 60
        parameter_61 = 61
        parameter_62 = 62
        parameter_63 = 63
        parameter_64 = 64
        parameter_65 = 65
        parameter_66 = 66
        parameter_67 = 67
        parameter_68 = 68
        parameter_69 = 69
        parameter_70 = 70
        parameter_71 = 71
        parameter_72 = 72
        parameter_73 = 73
        parameter_74 = 74
        parameter_75 = 75
        parameter_76 = 76
        parameter_77 = 77
        parameter_78 = 78
        parameter_79 = 79
        parameter_80 = 80
        parameter_81 = 81
        parameter_82 = 82
        parameter_83 = 83
        parameter_84 = 84
        parameter_85 = 85
        parameter_86 = 86
        parameter_87 = 87
        parameter_88 = 88
        parameter_89 = 89
        parameter_90 = 90
        parameter_91 = 91
        parameter_92 = 92
        parameter_93 = 93
        parameter_94 = 94
        parameter_95 = 95
        parameter_96 = 96
        parameter_97 = 97
        parameter_98 = 98
        parameter_99 = 99
        parameter_100 = 100
        parameter_101 = 101
        parameter_102 = 102
        parameter_103 = 103
        parameter_104 = 104
        parameter_105 = 105
        parameter_106 = 106
        parameter_107 = 107
        parameter_108 = 108
        parameter_109 = 109
        parameter_110 = 110
        parameter_111 = 111
        parameter_112 = 112
        parameter_113 = 113
        parameter_114 = 114
        parameter_115 = 115
        parameter_116 = 116
        parameter_117 = 117
        parameter_118 = 118
        parameter_119 = 119
        parameter_120 = 120
        parameter_121 = 121
        parameter_122 = 122
        parameter_123 = 123
        parameter_124 = 124
        parameter_125 = 125
        parameter_126 = 126
        parameter_127 = 127
        parameter_128 = 128
        parameter_129 = 129
        parameter_130 = 130
        parameter_131 = 131
        parameter_132 = 132
        parameter_133 = 133
        parameter_134 = 134
        parameter_135 = 135
        parameter_136 = 136
        parameter_137 = 137
        parameter_138 = 138
        parameter_139 = 139
        parameter_140 = 140
        parameter_141 = 141
        parameter_142 = 142
        parameter_143 = 143
        parameter_144 = 144
        parameter_145 = 145
        parameter_146 = 146
        parameter_147 = 147
        parameter_148 = 148
        parameter_149 = 149
        parameter_150 = 150
        parameter_151 = 151
        parameter_152 = 152
        parameter_153 = 153
        parameter_154 = 154
        parameter_155 = 155
        parameter_156 = 156
        parameter_157 = 157
        parameter_158 = 158
        parameter_159 = 159
        parameter_160 = 160
        parameter_161 = 161
        parameter_162 = 162
        parameter_163 = 163
        parameter_164 = 164
        parameter_165 = 165
        parameter_166 = 166
        parameter_167 = 167
        parameter_168 = 168
        parameter_169 = 169
        parameter_170 = 170
        parameter_171 = 171
        parameter_172 = 172
        parameter_173 = 173
        parameter_174 = 174
        parameter_175 = 175
        parameter_176 = 176
        parameter_177 = 177
        parameter_178 = 178
        parameter_179 = 179
        parameter_180 = 180
        parameter_181 = 181
        parameter_182 = 182
        parameter_183 = 183
        parameter_184 = 184
        parameter_185 = 185
        parameter_186 = 186
        parameter_187 = 187
        parameter_188 = 188
        parameter_189 = 189
        parameter_190 = 190
        parameter_191 = 191
        parameter_192 = 192
        parameter_193 = 193
        parameter_194 = 194
        parameter_195 = 195
        parameter_196 = 196
        parameter_197 = 197
        parameter_198 = 198
        parameter_199 = 199
        parameter_200 = 200
        parameter_201 = 201
        parameter_202 = 202
        parameter_203 = 203
        parameter_204 = 204
        parameter_205 = 205
        parameter_206 = 206
        parameter_207 = 207
        parameter_208 = 208
        parameter_209 = 209
        parameter_210 = 210
        parameter_211 = 211
        parameter_212 = 212
        parameter_213 = 213
        parameter_214 = 214
        parameter_215 = 215
        parameter_216 = 216
        parameter_217 = 217
        parameter_218 = 218
        parameter_219 = 219
        parameter_220 = 220
        parameter_221 = 221
        parameter_222 = 222
        parameter_223 = 223
        parameter_224 = 224
        parameter_225 = 225
        parameter_226 = 226
        parameter_227 = 227
        parameter_228 = 228
        parameter_229 = 229
        parameter_230 = 230
        parameter_231 = 231
        parameter_232 = 232
        parameter_233 = 233
        parameter_234 = 234
        parameter_235 = 235
        parameter_236 = 236
        parameter_237 = 237
        parameter_238 = 238
        parameter_239 = 239
        parameter_240 = 240
        parameter_241 = 241
        parameter_242 = 242
        parameter_243 = 243
        parameter_244 = 244
        parameter_245 = 245
        parameter_246 = 246
        parameter_247 = 247
        parameter_248 = 248
        parameter_249 = 249
        parameter_250 = 250
        parameter_251 = 251
        parameter_252 = 252
        parameter_253 = 253
        parameter_254 = 254
        parameter_255 = 255

    def get_config(self, config_index):
        """
        :param config_index:  int
        :rtype: Any
        """

        for key, value in Configuration.ValueIndexes.__dict__.items():
            if value == config_index:
                return getattr(self.values, key)
