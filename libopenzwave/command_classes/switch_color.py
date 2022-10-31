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
:synopsis: COMMAND_CLASS_SWITCH_COLOR

.. moduleauthor:: Kevin G Schlosser
"""

# #RRGGBBWWCWAMCYPR
# [RR][GG][BB][WW][CW][AM][CY][PR]
# [RR] = Red
# [GG] = Green
# [BB] = Blue
# [WW] = Warm White
# [CW] = Cold White
# [AM] = Amber
# [CY] = Cyan
# [PR] = Magenta

from . import zwave_cmd_class

# Color Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_COLOR = 0x33


def _clamp(x):
    return max(0, min(x, 255))


def _hex2(x):
    return hex(_clamp(x))[2:]


# noinspection PyAbstractClass
class SwitchColor(zwave_cmd_class.ZWaveCommandClass):
    """
    Switch Color Command Class

    symbol: `COMMAND_CLASS_SWITCH_COLOR`
    """

    class_id = COMMAND_CLASS_SWITCH_COLOR
    class_desc = 'COMMAND_CLASS_SWITCH_COLOR'

    COLORIDX_WARMWHITE = 0
    COLORIDX_COLDWHITE = 1
    COLORIDX_RED = 2
    COLORIDX_GREEN = 3
    COLORIDX_BLUE = 4
    COLORIDX_AMBER = 5
    COLORIDX_CYAN = 6
    COLORIDX_PURPLE = 7
    COLORIDX_INDEXCOLOR = 8

    PRESET_COLORS = [
        "Off",
        "Cool White",
        "Warm White",
        "Red",
        "Lime",
        "Blue",
        "Yellow",
        "Cyan",
        "Magenta",
        "Silver",
        "Gray",
        "Maroon",
        "Olive",
        "Green",
        "Purple",
        "Teal",
        "Navy",
        "Custom"
    ]

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        color = 0
        switch_color_index = 1
        switch_color_channels = 2
        switch_color_fade_duration = 4

    @staticmethod
    def __normalize_value(value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        return value

    @property
    def switch_color_preset(self):
        """
        Get/Set a preset color

        :param value: one of PRESET_COLORS
        :type value: str

        :return: The color, one of PRESET_COLORS
        :rtype: str
        """
        return self.values.switch_color_index.data

    @switch_color_preset.setter
    def switch_color_preset(self, value):
        self.values.switch_color_index.data = value

    @property
    def switch_color_preset_items(self):
        """
        Get the supported preset colors

        :return: list of supported colors
        :rtype: List[str]
        """
        return self.values.switch_color_index.data_list

    def __get_color(self, color_code):
        supported_colors = self.values.switch_color.units

        if color_code in supported_colors:
            start = supported_colors.find(color_code)
            color = self.values.switch_color.data
            return int(color[start:][:2], 16)

    def __set_color(self, color_code, value):
        supported_colors = self.values.switch_color.units

        if color_code in supported_colors:
            value = self.__normalize_value(value)

            start = supported_colors.find(color_code)
            color = self.values.switch_color.data
            self.values.switch_color.data = (
                color[:start] + hex(value)[2:] + color[start + 2:]
            )
            return True

        return False

    @property
    def switch_color_warm_white(self):
        """
        Get/Set the warm white

        :type value: int

        :rtype: int
        """
        return self.__get_color('WW')

    @switch_color_warm_white.setter
    def switch_color_warm_white(self, value):
        self.__set_color('WW', value)

    @property
    def switch_color_cold_white(self):
        """
        Get/Set the cold white

        :type value: int

        :rtype: int
        """
        return self.__get_color('CW')

    @switch_color_cold_white.setter
    def switch_color_cold_white(self, value):
        self.__set_color('CW', value)

    @property
    def switch_color_red(self):
        """
        Get/Set the red color

        :type value: int

        :rtype: int
        """
        color = self.__get_color('RR')

        if color is None:
            color = self._cmy_to_rgb(*self.switch_color_cmy)[0]

        return color

    @switch_color_red.setter
    def switch_color_red(self, value):
        if not self.__set_color('RR', value):
            _, g, b = self._cmy_to_rgb(*self.switch_color_cmy)
            self.switch_color_cmy = self._rgb_to_cmy(value, g, b)

    @property
    def switch_color_green(self):
        """
        Get/Set the green color

        :type value: int

        :rtype: int
        """
        color = self.__get_color('GG')

        if color is None:
            color = self._cmy_to_rgb(*self.switch_color_cmy)[1]

        return color

    @switch_color_green.setter
    def switch_color_green(self, value):
        if not self.__set_color('GG', value):
            r, _, b = self._cmy_to_rgb(*self.switch_color_cmy)
            self.switch_color_cmy = self._rgb_to_cmy(r, value, b)

    @property
    def switch_color_blue(self):
        """
        Get/Set the blue color

        :type value: int

        :rtype: int
        """
        color = self.__get_color('BB')

        if color is None:
            color = self._cmy_to_rgb(*self.switch_color_cmy)[2]

        return color

    @switch_color_blue.setter
    def switch_color_blue(self, value):
        if not self.__set_color('BB', value):
            r, g, _ = self._cmy_to_rgb(*self.switch_color_cmy)
            self.switch_color_cmy = self._rgb_to_cmy(r, g, value)

    @property
    def switch_color_amber(self):
        """
        Get/Set the amber color (yellow)

        :type value: int

        :rtype: int
        """
        color = self.__get_color('AM')

        if color is None:
            color = self._rgb_to_cmy(*self.switch_color_rgb)[2]

        return color

    @switch_color_amber.setter
    def switch_color_amber(self, value):
        if not self.__set_color('AM', value):
            c, m, _ = self._rgb_to_cmy(*self.switch_color_rgb)
            self.switch_color_rgb = self._cmy_to_rgb(c, m, value)

    @property
    def switch_color_cyan(self):
        """
        Get/Set the cyan color

        :type value: int

        :rtype: int
        """
        color = self.__get_color('CY')

        if color is None:
            color = self._rgb_to_cmy(*self.switch_color_rgb)[0]

        return color

    @switch_color_cyan.setter
    def switch_color_cyan(self, value):
        if not self.__set_color('CY', value):
            _, m, y = self._rgb_to_cmy(*self.switch_color_rgb)
            self.switch_color_rgb = self._cmy_to_rgb(value, m, y)

    @property
    def switch_color_magenta(self):
        """
        Get/Set the magenta color

        :type value: int

        :rtype: int
        """
        color = self.__get_color('PR')

        if color is None:
            color = self._rgb_to_cmy(*self.switch_color_rgb)[1]

        return color

    @switch_color_magenta.setter
    def switch_color_magenta(self, value):
        if not self.__set_color('PR', value):
            c, _, y = self._rgb_to_cmy(*self.switch_color_rgb)
            self.switch_color_rgb = self._cmy_to_rgb(c, value, y)

    @property
    def switch_color_fade_duration(self):
        """
        Get/Set the fading duration

        :type value: int

        :rtype: int
        """
        return self.values.switch_color_fade_duration.data

    @switch_color_fade_duration.setter
    def switch_color_fade_duration(self, value):
        self.values.switch_color_fade_duration.data = value

    @property
    def switch_color_rgb(self):
        """
        Get/Set the color using RGB color code

        (Red, Green, Blue)

        :type value: Tuple[int, int, int]

        :rtype: Tuple[int, int, int]
        """
        supported_colors = self.values.switch_color.units
        color = self.values.switch_color.data

        for code in ('RR', 'GG', 'BB'):
            if code not in supported_colors:
                break
        else:
            red_start = supported_colors.find('RR')
            green_start = supported_colors.find('GG')
            blue_start = supported_colors.find('BB')

            red = color[red_start:][:2]
            green = color[green_start:][:2]
            blue = color[blue_start:][:2]

            red = int(red, 16)
            green = int(green, 16)
            blue = int(blue, 16)
            return red, green, blue

        cyan_start = supported_colors.find('CY')
        magenta_start = supported_colors.find('PR')
        amber_start = supported_colors.find('AM')

        cyan = color[cyan_start:][:2]
        magenta = color[magenta_start:][:2]
        amber = color[amber_start:][:2]

        cyan = int(cyan, 16)

        magenta = int(magenta, 16)
        amber = int(amber, 16)
        return self._cmy_to_rgb(cyan, magenta, amber)

    @switch_color_rgb.setter
    def switch_color_rgb(self, value):
        red, green, blue = value

        supported_colors = self.values.switch_color.units
        color = self.values.switch_color.data

        for code in ('RR', 'GG', 'BB'):
            if code not in supported_colors:
                cyan_start = supported_colors.find('CY')
                magenta_start = supported_colors.find('PR')
                amber_start = supported_colors.find('AM')

                cyan, magenta, amber = self._rgb_to_cmy(
                    _clamp(red),
                    _clamp(green),
                    _clamp(blue)
                )

                cyan = _hex2(cyan)
                magenta = _hex2(magenta)
                amber = _hex2(amber)

                color = (
                    color[:cyan_start - 1] +
                    cyan +
                    color[:cyan_start + 1]
                )
                color = (
                    color[:magenta_start - 1] +
                    magenta +
                    color[:magenta_start + 1]
                )
                color = (
                    color[:amber_start - 1] +
                    amber +
                    color[:amber_start + 1]
                )
                break
        else:
            red_start = supported_colors.find('RR')
            green_start = supported_colors.find('GG')
            blue_start = supported_colors.find('BB')

            red = _hex2(red)
            green = _hex2(green)
            blue = _hex2(blue)

            color = (
                color[:red_start - 1] +
                red +
                color[:red_start + 1]
            )
            color = (
                color[:green_start - 1] +
                green +
                color[:green_start + 1]
            )
            color = (
                color[:blue_start - 1] +
                blue +
                color[:blue_start + 1]
            )

        self.values.switch_color.data = color

    @property
    def switch_color_cmy(self):
        """
        Get/Set color using CMY color code

        (Cyan, Magenta, Yellow)

        :type value: Tuple[int, int, int]

        :rtype: Tuple[int, int, int]
        """
        supported_colors = self.values.switch_color.units
        color = self.values.switch_color.data

        for code in ('PR', 'CY', 'AM'):
            if code not in supported_colors:
                break
        else:
            cyan_start = supported_colors.find('CY')
            magenta_start = supported_colors.find('PR')
            amber_start = supported_colors.find('AM')

            cyan = color[cyan_start:][:2]
            magenta = color[magenta_start:][:2]
            amber = color[amber_start:][:2]

            cyan = int(cyan, 16)
            magenta = int(magenta, 16)
            amber = int(amber, 16)

            return cyan, magenta, amber

        red_start = supported_colors.find('RR')
        green_start = supported_colors.find('GG')
        blue_start = supported_colors.find('BB')

        red = color[red_start:][:2]
        green = color[green_start:][:2]
        blue = color[blue_start:][:2]

        red = int(red, 16)
        green = int(green, 16)
        blue = int(blue, 16)

        return self._rgb_to_cmy(red, green, blue)

    @switch_color_cmy.setter
    def switch_color_cmy(self, value):

        cyan, magenta, amber = value

        supported_colors = self.values.switch_color.units
        color = self.values.switch_color.data

        for code in ('CY', 'PR', 'AM'):
            if code not in supported_colors:
                red_start = supported_colors.find('RR')
                green_start = supported_colors.find('GG')
                blue_start = supported_colors.find('BB')

                red, green, blue = self._cmy_to_rgb(
                    _clamp(cyan),
                    _clamp(magenta),
                    _clamp(amber)
                )

                red = _hex2(red)
                green = _hex2(green)
                blue = _hex2(blue)

                color = (
                    color[:red_start - 1] +
                    red +
                    color[:red_start + 1]
                )
                color = (
                    color[:green_start - 1] +
                    green +
                    color[:green_start + 1]
                )
                color = (
                    color[:blue_start - 1] +
                    blue +
                    color[:blue_start + 1]
                )
                break
        else:
            cyan_start = supported_colors.find('CY')
            magenta_start = supported_colors.find('PR')
            amber_start = supported_colors.find('AM')

            cyan = _hex2(cyan)
            magenta = _hex2(magenta)
            amber = _hex2(amber)

            color = (
                color[:cyan_start - 1] +
                cyan +
                color[:cyan_start + 1]
            )
            color = (
                color[:magenta_start - 1] +
                magenta +
                color[:magenta_start + 1]
            )
            color = (
                color[:amber_start - 1] +
                amber +
                color[:amber_start + 1]
            )

        self.values.switch_color.data = color

    @property
    def switch_color_html(self):
        """
        Get/Set the color using HTML color code

        #RRGGBB

        :type value: str

        :rtype: str
        """
        red, green, blue = self.switch_color_rgb
        color = _hex2(red) + _hex2(green) + _hex2(blue)
        color = '#' + color.upper()
        return color

    @switch_color_html.setter
    def switch_color_html(self, value):
        value = value.lstrip('#')

        red = value[:2]
        green = value[2:4]
        blue = value[4:]

        red = int(red, 16)
        green = int(green, 16)
        blue = int(blue, 16)

        self.switch_color_rgb = (red, green, blue)

    @property
    def switch_color_hsv(self):
        """
        Get/Set the color using HSV color code

        (Hue, Saturation, Value)

        :type value: Tuple[int, int, int]

        :rtype: Tuple[int, int, int]
        """
        import colorsys

        r, g, b = self.switch_color_rgb
        return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    @switch_color_hsv.setter
    def switch_color_hsv(self, value):
        import colorsys

        self.switch_color_rgb = tuple(
            int(round(i * 255.0)) for i in colorsys.hsv_to_rgb(*value)
        )

    @staticmethod
    def _rgb_to_cmy(r, g, b):
        if (r, g, b) == (0, 0, 0):
            return r, g, b

        c = 1.0 - r / 255.0
        m = 1.0 - g / 255.0
        y = 1.0 - b / 255.0

        k = min(c, m, y)
        c = ((c - k) / (1.0 - k)) * 255.0
        m = ((m - k) / (1.0 - k)) * 255.0
        y = ((y - k) / (1.0 - k)) * 255.0

        return int(round(c)), int(round(m)), int(round(y))

    @staticmethod
    def _cmy_to_rgb(c, m, y):

        r = 255.0 * (1.0 - c / 255.0)
        g = 255.0 * (1.0 - m / 255.0)
        b = 255.0 * (1.0 - y / 255.0)

        k = max(r, g, b)
        r *= 1.0 - k / 255.0
        g *= 1.0 - k / 255.0
        b *= 1.0 - k / 255.0

        return int(round(r)), int(round(g)), int(round(b))
