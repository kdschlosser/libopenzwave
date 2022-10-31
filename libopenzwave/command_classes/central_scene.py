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
:synopsis: COMMAND_CLASS_CENTRAL_SCENE

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Central Scene Command Class - Active
# Application
COMMAND_CLASS_CENTRAL_SCENE = 0x5B


# noinspection PyAbstractClass
class CentralScene(zwave_cmd_class.ZWaveCommandClass):
    """
    Central Scene Command Class

    symbol: `COMMAND_CLASS_CENTRAL_SCENE`
    """
    class_id = COMMAND_CLASS_CENTRAL_SCENE
    class_desc = 'COMMAND_CLASS_CENTRAL_SCENE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        scene_1 = 1
        scene_2 = 2
        scene_3 = 3
        scene_4 = 4
        scene_5 = 5
        scene_6 = 6
        scene_7 = 7
        scene_8 = 8
        scene_9 = 9
        scene_10 = 10
        scene_11 = 11
        scene_12 = 12
        scene_13 = 13
        scene_14 = 14
        scene_15 = 15
        scene_16 = 16
        scene_17 = 17
        scene_18 = 18
        scene_19 = 19
        scene_20 = 20
        scene_21 = 21
        scene_22 = 22
        scene_23 = 23
        scene_24 = 24
        scene_25 = 25
        scene_26 = 26
        scene_27 = 27
        scene_28 = 28
        scene_29 = 29
        scene_30 = 30
        scene_31 = 31
        scene_32 = 32
        scene_33 = 33
        scene_34 = 34
        scene_35 = 35
        scene_36 = 36
        scene_37 = 37
        scene_38 = 38
        scene_39 = 39
        scene_40 = 40
        scene_41 = 41
        scene_42 = 42
        scene_43 = 43
        scene_44 = 44
        scene_45 = 45
        scene_46 = 46
        scene_47 = 47
        scene_48 = 48
        scene_49 = 49
        scene_50 = 50
        scene_51 = 51
        scene_52 = 52
        scene_53 = 53
        scene_54 = 54
        scene_55 = 55
        scene_56 = 56
        scene_57 = 57
        scene_58 = 58
        scene_59 = 59
        scene_60 = 60
        scene_61 = 61
        scene_62 = 62
        scene_63 = 63
        scene_64 = 64
        scene_65 = 65
        scene_66 = 66
        scene_67 = 67
        scene_68 = 68
        scene_69 = 69
        scene_70 = 70
        scene_71 = 71
        scene_72 = 72
        scene_73 = 73
        scene_74 = 74
        scene_75 = 75
        scene_76 = 76
        scene_77 = 77
        scene_78 = 78
        scene_79 = 79
        scene_80 = 80
        scene_81 = 81
        scene_82 = 82
        scene_83 = 83
        scene_84 = 84
        scene_85 = 85
        scene_86 = 86
        scene_87 = 87
        scene_88 = 88
        scene_89 = 89
        scene_90 = 90
        scene_91 = 91
        scene_92 = 92
        scene_93 = 93
        scene_94 = 94
        scene_95 = 95
        scene_96 = 96
        scene_97 = 97
        scene_98 = 98
        scene_99 = 99
        scene_100 = 100
        scene_101 = 101
        scene_102 = 102
        scene_103 = 103
        scene_104 = 104
        scene_105 = 105
        scene_106 = 106
        scene_107 = 107
        scene_108 = 108
        scene_109 = 109
        scene_110 = 110
        scene_111 = 111
        scene_112 = 112
        scene_113 = 113
        scene_114 = 114
        scene_115 = 115
        scene_116 = 116
        scene_117 = 117
        scene_118 = 118
        scene_119 = 119
        scene_120 = 120
        scene_121 = 121
        scene_122 = 122
        scene_123 = 123
        scene_124 = 124
        scene_125 = 125
        scene_126 = 126
        scene_127 = 127
        scene_128 = 128
        scene_129 = 129
        scene_130 = 130
        scene_131 = 131
        scene_132 = 132
        scene_133 = 133
        scene_134 = 134
        scene_135 = 135
        scene_136 = 136
        scene_137 = 137
        scene_138 = 138
        scene_139 = 139
        scene_140 = 140
        scene_141 = 141
        scene_142 = 142
        scene_143 = 143
        scene_144 = 144
        scene_145 = 145
        scene_146 = 146
        scene_147 = 147
        scene_148 = 148
        scene_149 = 149
        scene_150 = 150
        scene_151 = 151
        scene_152 = 152
        scene_153 = 153
        scene_154 = 154
        scene_155 = 155
        scene_156 = 156
        scene_157 = 157
        scene_158 = 158
        scene_159 = 159
        scene_160 = 160
        scene_161 = 161
        scene_162 = 162
        scene_163 = 163
        scene_164 = 164
        scene_165 = 165
        scene_166 = 166
        scene_167 = 167
        scene_168 = 168
        scene_169 = 169
        scene_170 = 170
        scene_171 = 171
        scene_172 = 172
        scene_173 = 173
        scene_174 = 174
        scene_175 = 175
        scene_176 = 176
        scene_177 = 177
        scene_178 = 178
        scene_179 = 179
        scene_180 = 180
        scene_181 = 181
        scene_182 = 182
        scene_183 = 183
        scene_184 = 184
        scene_185 = 185
        scene_186 = 186
        scene_187 = 187
        scene_188 = 188
        scene_189 = 189
        scene_190 = 190
        scene_191 = 191
        scene_192 = 192
        scene_193 = 193
        scene_194 = 194
        scene_195 = 195
        scene_196 = 196
        scene_197 = 197
        scene_198 = 198
        scene_199 = 199
        scene_200 = 200
        scene_201 = 201
        scene_202 = 202
        scene_203 = 203
        scene_204 = 204
        scene_205 = 205
        scene_206 = 206
        scene_207 = 207
        scene_208 = 208
        scene_209 = 209
        scene_210 = 210
        scene_211 = 211
        scene_212 = 212
        scene_213 = 213
        scene_214 = 214
        scene_215 = 215
        scene_216 = 216
        scene_217 = 217
        scene_218 = 218
        scene_219 = 219
        scene_220 = 220
        scene_221 = 221
        scene_222 = 222
        scene_223 = 223
        scene_224 = 224
        scene_225 = 225
        scene_226 = 226
        scene_227 = 227
        scene_228 = 228
        scene_229 = 229
        scene_230 = 230
        scene_231 = 231
        scene_232 = 232
        scene_233 = 233
        scene_234 = 234
        scene_235 = 235
        scene_236 = 236
        scene_237 = 237
        scene_238 = 238
        scene_239 = 239
        scene_240 = 240
        scene_241 = 241
        scene_242 = 242
        scene_243 = 243
        scene_244 = 244
        scene_245 = 245
        scene_246 = 246
        scene_247 = 247
        scene_248 = 248
        scene_249 = 249
        scene_250 = 250
        scene_251 = 251
        scene_252 = 252
        scene_253 = 253
        scene_254 = 254
        scene_255 = 255
        scene_count = 256
        scene_clear_timeout = 257

    def get_scene(self, scene_index):
        """
        :type scene_index: int
        """
        for key, value in CentralScene.ValueIndexes.__dict__.items():
            if value == scene_index:
                return getattr(self.values, key)

    def scene_clear_timeout(self):
        """
        :rtype: None
        """
        self.values.scene_clear_timeout.data = True

    @property
    def scene_count(self):
        """
        Number of Scenes

        Retrieves the number of scenes.

        :return: number of scenes
        :rtype: int
        """

        return self.values.scene_count.data
