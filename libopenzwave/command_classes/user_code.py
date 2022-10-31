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
:synopsis: COMMAND_CLASS_USER_CODE

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# User Code Command Class - Active
# Application
COMMAND_CLASS_USER_CODE = 0x63


class Code(object):
    """
    This class represents a user code.
    """

    def __init__(self, node, index):
        self._node = node
        self._index = index

    @property
    def node(self):
        """
        Node that contains this user code.

        :rtype: :py:class:`libopenzwave.node.ZWaveNode`
        """
        return self._node

    @property
    def id(self):
        """
        User Code Id

        :rtype: int
        """
        return self._index

    @property
    def _value(self):
        return getattr(self._node.values, 'user_code_' + str(self._index))

    def get(self):
        """
        Get the User Code.

        :rtype: str
        """
        return self._value.data

    def set(self, code):
        """
        Set the User Code.

        :param code: new code.
        :type code: str

        :rtype: None
        """
        self._value.data = code

    @property
    def name(self):
        """
        Get/Set the Name of the User Code.

        Using this you will be able to allow for easy identification of
        the different codes. Most would probably designate a code to a
        family member. A user can use the name of the family member as an
        easy way to identify a code.

        :param value: new name
        :type value: str

        :rtype: str
        """
        return self._value.label

    @name.setter
    def name(self, value):
        self._value.label = value

    def remove(self):
        """
        Remove this User Code from use.

        :rtype: None
        """
        self._node.user_code_remove(self)


# noinspection PyAbstractClass
class UserCode(zwave_cmd_class.ZWaveCommandClass):
    """
    User Code Command Class

    symbol: `COMMAND_CLASS_USER_CODE`
    """

    class_id = COMMAND_CLASS_USER_CODE
    class_desc = 'COMMAND_CLASS_USER_CODE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        user_code_enrollment_code = 0
        user_code_1 = 1
        user_code_2 = 2
        user_code_3 = 3
        user_code_4 = 4
        user_code_5 = 5
        user_code_6 = 6
        user_code_7 = 7
        user_code_8 = 8
        user_code_9 = 9
        user_code_10 = 10
        user_code_11 = 11
        user_code_12 = 12
        user_code_13 = 13
        user_code_14 = 14
        user_code_15 = 15
        user_code_16 = 16
        user_code_17 = 17
        user_code_18 = 18
        user_code_19 = 19
        user_code_20 = 20
        user_code_21 = 21
        user_code_22 = 22
        user_code_23 = 23
        user_code_24 = 24
        user_code_25 = 25
        user_code_26 = 26
        user_code_27 = 27
        user_code_28 = 28
        user_code_29 = 29
        user_code_30 = 30
        user_code_31 = 31
        user_code_32 = 32
        user_code_33 = 33
        user_code_34 = 34
        user_code_35 = 35
        user_code_36 = 36
        user_code_37 = 37
        user_code_38 = 38
        user_code_39 = 39
        user_code_40 = 40
        user_code_41 = 41
        user_code_42 = 42
        user_code_43 = 43
        user_code_44 = 44
        user_code_45 = 45
        user_code_46 = 46
        user_code_47 = 47
        user_code_48 = 48
        user_code_49 = 49
        user_code_50 = 50
        user_code_51 = 51
        user_code_52 = 52
        user_code_53 = 53
        user_code_54 = 54
        user_code_55 = 55
        user_code_56 = 56
        user_code_57 = 57
        user_code_58 = 58
        user_code_59 = 59
        user_code_60 = 60
        user_code_61 = 61
        user_code_62 = 62
        user_code_63 = 63
        user_code_64 = 64
        user_code_65 = 65
        user_code_66 = 66
        user_code_67 = 67
        user_code_68 = 68
        user_code_69 = 69
        user_code_70 = 70
        user_code_71 = 71
        user_code_72 = 72
        user_code_73 = 73
        user_code_74 = 74
        user_code_75 = 75
        user_code_76 = 76
        user_code_77 = 77
        user_code_78 = 78
        user_code_79 = 79
        user_code_80 = 80
        user_code_81 = 81
        user_code_82 = 82
        user_code_83 = 83
        user_code_84 = 84
        user_code_85 = 85
        user_code_86 = 86
        user_code_87 = 87
        user_code_88 = 88
        user_code_89 = 89
        user_code_90 = 90
        user_code_91 = 91
        user_code_92 = 92
        user_code_93 = 93
        user_code_94 = 94
        user_code_95 = 95
        user_code_96 = 96
        user_code_97 = 97
        user_code_98 = 98
        user_code_99 = 99
        user_code_100 = 100
        user_code_101 = 101
        user_code_102 = 102
        user_code_103 = 103
        user_code_104 = 104
        user_code_105 = 105
        user_code_106 = 106
        user_code_107 = 107
        user_code_108 = 108
        user_code_109 = 109
        user_code_110 = 110
        user_code_111 = 111
        user_code_112 = 112
        user_code_113 = 113
        user_code_114 = 114
        user_code_115 = 115
        user_code_116 = 116
        user_code_117 = 117
        user_code_118 = 118
        user_code_119 = 119
        user_code_120 = 120
        user_code_121 = 121
        user_code_122 = 122
        user_code_123 = 123
        user_code_124 = 124
        user_code_125 = 125
        user_code_126 = 126
        user_code_127 = 127
        user_code_128 = 128
        user_code_129 = 129
        user_code_130 = 130
        user_code_131 = 131
        user_code_132 = 132
        user_code_133 = 133
        user_code_134 = 134
        user_code_135 = 135
        user_code_136 = 136
        user_code_137 = 137
        user_code_138 = 138
        user_code_139 = 139
        user_code_140 = 140
        user_code_141 = 141
        user_code_142 = 142
        user_code_143 = 143
        user_code_144 = 144
        user_code_145 = 145
        user_code_146 = 146
        user_code_147 = 147
        user_code_148 = 148
        user_code_149 = 149
        user_code_150 = 150
        user_code_151 = 151
        user_code_152 = 152
        user_code_153 = 153
        user_code_154 = 154
        user_code_155 = 155
        user_code_156 = 156
        user_code_157 = 157
        user_code_158 = 158
        user_code_159 = 159
        user_code_160 = 160
        user_code_161 = 161
        user_code_162 = 162
        user_code_163 = 163
        user_code_164 = 164
        user_code_165 = 165
        user_code_166 = 166
        user_code_167 = 167
        user_code_168 = 168
        user_code_169 = 169
        user_code_170 = 170
        user_code_171 = 171
        user_code_172 = 172
        user_code_173 = 173
        user_code_174 = 174
        user_code_175 = 175
        user_code_176 = 176
        user_code_177 = 177
        user_code_178 = 178
        user_code_179 = 179
        user_code_180 = 180
        user_code_181 = 181
        user_code_182 = 182
        user_code_183 = 183
        user_code_184 = 184
        user_code_185 = 185
        user_code_186 = 186
        user_code_187 = 187
        user_code_188 = 188
        user_code_189 = 189
        user_code_190 = 190
        user_code_191 = 191
        user_code_192 = 192
        user_code_193 = 193
        user_code_194 = 194
        user_code_195 = 195
        user_code_196 = 196
        user_code_197 = 197
        user_code_198 = 198
        user_code_199 = 199
        user_code_200 = 200
        user_code_201 = 201
        user_code_202 = 202
        user_code_203 = 203
        user_code_204 = 204
        user_code_205 = 205
        user_code_206 = 206
        user_code_207 = 207
        user_code_208 = 208
        user_code_209 = 209
        user_code_210 = 210
        user_code_211 = 211
        user_code_212 = 212
        user_code_213 = 213
        user_code_214 = 214
        user_code_215 = 215
        user_code_216 = 216
        user_code_217 = 217
        user_code_218 = 218
        user_code_219 = 219
        user_code_220 = 220
        user_code_221 = 221
        user_code_222 = 222
        user_code_223 = 223
        user_code_224 = 224
        user_code_225 = 225
        user_code_226 = 226
        user_code_227 = 227
        user_code_228 = 228
        user_code_229 = 229
        user_code_230 = 230
        user_code_231 = 231
        user_code_232 = 232
        user_code_233 = 233
        user_code_234 = 234
        user_code_235 = 235
        user_code_236 = 236
        user_code_237 = 237
        user_code_238 = 238
        user_code_239 = 239
        user_code_240 = 240
        user_code_241 = 241
        user_code_242 = 242
        user_code_243 = 243
        user_code_244 = 244
        user_code_245 = 245
        user_code_246 = 246
        user_code_247 = 247
        user_code_248 = 248
        user_code_249 = 249
        user_code_250 = 250
        user_code_251 = 251
        user_code_252 = 252
        user_code_253 = 253
        user_code_refresh = 255
        user_code_remove_code = 256
        user_code_count = 257
        user_code_raw_value = 258
        user_code_raw_value_index = 259

    @property
    def user_code_count(self):
        """
        Number of User Codes

        :rtype: int
        """
        return self.values.user_code_count.data

    def user_code_refresh_all(self):
        """
        Refresh User Codes

        :rtype: None
        """
        self.values.user_code_refresh.data = True

    @property
    def user_code_enrollment_code(self):
        """
        Enrollment Code

        :rtype: str
        """
        return self.values.user_code_enrollment_code.data

    def user_code_remove(self, id_):
        """
        Removes a User Code from Use

        :param id_: the id of the user code
        :type id_: int

        :rtype: None
        """
        if not isinstance(id_, int):
            id_ = id_.id  # NOQA

        self.values.user_code_remove_code.data = id_

    @property
    def user_codes(self):
        """
        Gets the User Codes

        :return: list of
            :py:class:`libopenzwave.command_classes.user_code.Code`
            instances
            
        :rtype: List[Code]
        """
        res = [None]

        for i in range(1, self.user_code_count):
            res += [Code(self, i)]

        return res

