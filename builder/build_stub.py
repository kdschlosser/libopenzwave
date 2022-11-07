# -*- coding: utf-8 -*-

import os
import sys
import inspect
from setuptools import Command
from distutils import log as LOG


HEADER = '''\
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
:synopsis: loader for libopenzwave

.. moduleauthor:: Kevin G Schlosser
.. moduleauthor:: This file is automatically generated 
"""

from typing import List, Union, Optional
import logging

'''


CLASS_TEMPLATE = '''
{indent}class {class_name}({parent_classes}):
{indent}    """
{class_doc}
{indent}    """
{class_attributes}{class_methods}{class_properties}{class_classes}
'''

FUNC_TEMPLATE = '''
{indent}def {func_name}({func_args}){rtype}:
{indent}    """
{func_doc}
{indent}    """
{indent}    ...
'''

METH_TEMPLATE = '''
{indent}    def {meth_name}({meth_args}){rtype}:
{indent}        """
{meth_doc}
{indent}        """
{indent}        ...
'''

PROPGET_TEMPLATE = '''
{indent}@property
{indent}def {prop_name}(self){rtype}:
{indent}    """
{prop_doc}
{indent}    """
{indent}    ...
'''


PROPSET_TEMPLATE = '''
{indent}@{prop_name}.setter
{indent}def {prop_name}(self, {param}):
{indent}    ...
'''

':py:class:`openzwave.network.ZWaveNetwork` instance'


def _is_in_base(bases, item):
    for base in bases:
        if item in base.__dict__.values():
            return True
    return False


def _iter_bases(parent, bases):
    for parent_base in inspect.getmro(parent):
        if parent_base == parent:
            continue

        if parent_base in bases:
            bases.remove(parent_base)

        _iter_bases(parent_base, bases)


def _build_class(class_name, cls, indent):
    if not cls.__module__.startswith('_libopenzwave'):
        return ''

    if class_name.startswith('_'):
        return ''

    class_doc = inspect.getdoc(cls)

    if class_doc in (None, 'None'):
        class_doc = indent + '    NO DOC'
    else:
        class_doc = '\n'.join(
            indent + '    ' + line for line in class_doc.split('\n')
        )

    class_attributes = []
    class_methods = []
    class_properties = []
    class_classes = []
    bases = list(b for b in inspect.getmro(cls) if b != cls)

    for parent_class in bases[:]:
        if parent_class != cls:
            _iter_bases(parent_class, bases)

    parent_classes = list(p.__name__ for p in bases)

    if not parent_classes:
        parent_classes = ['object']

    bases = list(b for b in inspect.getmro(cls) if b != cls)

    used_items = []

    for item_name, item in cls.__dict__.items():
        if item_name in used_items:
            continue

        if item_name in (
            '__dict__',
            '__weakref__',
            '__setstate__',
            '__reduce__'
        ):
            continue

        if _is_in_base(bases, item):
            continue

        if item_name.startswith('_') and not item_name.endswith('_'):
            continue

        if inspect.isclass(item):
            class_classes += [_build_class(item_name, item, indent + '    ')]
        elif isinstance(item, classmethod):
            class_methods += [
                indent + '\n    @classmethod',
                _build_meth(item_name, item.__func__, indent).replace(
                    'self',
                    'cls, *args, **kwargs'
                )
            ]
        elif isinstance(item, staticmethod):
            class_methods += [
                indent + '\n    @staticmethod',
                _build_meth(item_name, item.__func__, indent).replace(
                    'self, ',
                    ''
                ).replace('self', '')
            ]
        elif inspect.isgetsetdescriptor(item) or isinstance(item, property):
            class_properties += [_build_prop(item_name, item, indent)]
        elif inspect.ismethod(item) or inspect.ismethoddescriptor(item):
            class_methods += [_build_meth(item_name, item, indent)]
        elif inspect.isfunction(item):
            class_methods += [_build_meth(item_name, item, indent)]
        elif not item_name.startswith('_'):
            item_value = str(type(item)).split("'")[1].split('.')[-1]
            if item_value in (
                'module',
                'property',
                'builtin_function_or_method'
            ):
                continue

            if isinstance(item, list):
                item_value = ': List[' + str(
                    type(item[0])
                ).split("'")[1].split('.')[-1] + ']'

            elif item is None:
                item_value = ' = None'

            else:
                item_value = ': ' + item_value

            class_attributes += [
                indent + '    ' + item_name + '{0}\n'.format(item_value)
            ]

        used_items.append(item_name)

    output = CLASS_TEMPLATE.format(
        class_name=class_name,
        parent_classes=', '.join(parent_classes),
        class_doc=class_doc,
        class_attributes=''.join(class_attributes),
        class_methods=''.join(class_methods),
        class_properties=''.join(class_properties),
        class_classes=''.join(class_classes),
        indent=indent
    )
    output = ''.join(output)

    for item in (
        class_attributes,
        class_methods,
        class_properties,
        class_classes
    ):
        if item:
            break

    else:
        output += indent + '    ...'

    return output


def _build_prop(prop_name, prop, indent):
    indent += '    '
    prop_doc = inspect.getdoc(prop)
    if prop_doc in (None, 'None'):
        prop_doc = indent + '    NO DOC'
    else:
        prop_doc = '\n'.join(
            indent + '     ' + line for line in prop_doc.split('\n')
        )
    # :rtype: NodeStats
    # :type node_id: int

    if ':type ' in prop_doc:
        param_name = prop_doc.split(':type ')[-1]
        param_name, param_type = param_name.split('\n')[0].split(': ')
        param_type = list(
            item.strip() for item in param_type.strip().split(',')
            if item.strip()
        )
        if len(param_type) > 1:
            param = param_name + ': Union[' + ', '.join(param_type) + ']'
        else:
            param = param_name + ': ' + param_type[0]
    else:
        param = 'value'

    if ':rtype:' in prop_doc:
        rtype = prop_doc.split(':rtype:')[-1].split('\n')[0].strip()
        rtype = list(item.strip() for item in rtype.split(',') if item.strip())
        if len(rtype) > 1:
            rtype = ' -> Union[' + ', '.join(rtype) + ']'
        else:
            rtype = ' -> ' + rtype[0]
    else:
        rtype = ''

    output = PROPGET_TEMPLATE.format(
        prop_name=prop_name,
        prop_doc=prop_doc,
        indent=indent,
        rtype=rtype
    )

    try:
        if prop.fset:
            output += PROPSET_TEMPLATE.format(
                prop_name=prop_name,
                indent=indent,
                param=param
            )
    except AttributeError:
        output += PROPSET_TEMPLATE.format(
            prop_name=prop_name,
            indent=indent,
            param=param
        )

    return output


def _parse_args(func_args, func_doc):

    func_args = func_args.split(', ')
    if len(func_args) > 1 or (len(func_args) == 1 and 'self' not in func_args):
        # :rtype: NodeStats
        # :type node_id: int

        for i, func_arg in enumerate(func_args):
            func_arg = func_arg.split('=')

            if ':type ' + func_arg[0] in func_doc:
                param_type = func_doc.split(
                    ':type ' + func_arg[0] + ': '
                )[-1].split('\n')[0]

                param_type = list(
                    item.strip() for item in param_type.strip().split(',') if
                    item.strip())

                if 'optional' in param_type:
                    has_optional = True
                    param_type.remove('optional')

                elif 'Optional' in param_type:
                    has_optional = True
                    param_type.remove('Optional')

                else:
                    has_optional = False

                if len(param_type) > 1:
                    param_type = 'Union[' + ', '.join(param_type) + ']'
                else:
                    param_type = param_type[0]

                if has_optional:
                    func_arg[0] += ': Optional[' + param_type + ']'
                else:
                    func_arg[0] += ': ' + param_type

            func_arg = '='.join(func_arg)

            func_args[i] = func_arg

    func_args = ', '.join(func_args)

    if ':rtype:' in func_doc:
        rtype = func_doc.split(':rtype:')[-1].split('\n')[0].strip()
        rtype = list(item.strip() for item in rtype.split(',') if item.strip())

        if 'optional' in rtype:
            optional = True
            rtype.remove('optional')
        elif 'Optional' in rtype:
            optional = True
            rtype.remove('Optional')
        else:
            optional = False

        if len(rtype) > 1:
            rtype = 'Union[' + ', '.join(rtype) + ']'
        else:
            rtype = rtype[0]

        if optional:
            rtype = ' -> Optional[' + rtype + ']'
        else:
            rtype = ' -> ' + rtype
    else:
        rtype = ''

    return func_args, rtype


def _build_func(func_name, func, indent):
    func_doc = inspect.getdoc(func)

    if func_doc in (None, 'None'):
        func_doc = indent + '        NO DOC'
    else:
        func_doc = '\n'.join(
            indent + '        ' + line for line in func_doc.split('\n')
        )

    func_args = inspect.formatargspec(inspect.getargspec(func))  # NOQA
    func_args, rtype = _parse_args(func_args, func_doc)

    output = FUNC_TEMPLATE.format(
        func_name=func_name,
        func_args=func_args,
        func_doc=func_doc,
        indent=indent,
        rtype=rtype
    )
    return output


def _build_meth(meth_name, meth, indent):
    meth_doc = inspect.getdoc(meth)

    if meth_doc in (None, 'None'):
        meth_doc = indent + '        NO DOC'
    else:
        meth_doc = '\n'.join(
            indent + '        ' + line for line in meth_doc.split('\n')
        )

    try:
        meth_args = inspect.formatargspec(inspect.getargspec(meth))  # NOQA
    except TypeError:
        meth_args = ['self']

        if meth_name in (
                '__rand__',
                '__ror__',
                '__or__',
                '__and__',
                '__rxor__',
                '__xor__',
                '__ne__',
                '__eq__'
        ):
            meth_args += ['other']

        elif meth_name == '__getattr__':
            meth_args += ['key']

        elif meth_name == '__getitem__':
            meth_args += ['item']
        elif meth_name in ('__setattr__', '__setitem__'):
            meth_args += ['key', 'value']

        else:
            for param_name in meth_doc.split(':'):
                if param_name.startswith('param '):
                    param_name = param_name.split(' ')[-1]
                    meth_args += [param_name]

        meth_args = ', '.join(arg.strip() for arg in meth_args if arg.strip())

    meth_args, rtype = _parse_args(meth_args, meth_doc)

    output = METH_TEMPLATE.format(
        meth_name=meth_name,
        meth_args=meth_args,
        meth_doc=meth_doc,
        indent=indent,
        rtype=rtype
    )
    return output


ENUM_ITEM_TEMPLATE = '''
    class {p_name}({cls_name}):
        doc = {doc}
        index = {index}
{addl_params}

    {p_name} = {p_name}({doc})
'''

ADDL_PARAMS_TEMPLATE = '''        {param_name} = {param_value}'''


ENUM_CLASS_TEMPLATE = '''
class {name}({cls_name}):
{classes}


{name} = {name}()

'''


class build_stub(Command):
    description = 'stub builder'

    user_options = [
        (
            'run-build',
            None,
            'internal use'
        ),
    ]

    boolean_options = ['run-build']

    def finalize_options(self):
        build = self.distribution.get_command_obj('build')  # NOQA
        build.ensure_finalized()

    def initialize_options(self):
        self.run_build = False  # NOQA

    def run(self):
        build = self.distribution.get_command_obj('build')  # NOQA

        import subprocess

        if not sys.platform.startswith('win') and not self.run_build:
            p = subprocess.Popen(
                'bash',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )

            cmd = sys.executable + ' setup.py build_stub --run-build'

            _, err = p.communicate(cmd.encode('utf-8'))

            if b'Traceback' in err:
                LOG.error('\n\n' + err + '\n')
                sys.exit(1)

            # p.stdin.write(cmd.encode('utf-8'))
            # p.stdin.close()
            #
            # while p.poll() is None:
            #     pass
            #
            # if not p.stdout.closed:
            #     p.stdout.close()
            #
            # if not p.stderr.closed:
            #     p.stderr.close()

            return

        sys.path.insert(0, build.build_lib)

        # build_ext = self.distribution.get_command_obj('build_ext')

        def _get_module_names(pth, name=''):
            mod_names = []
            for fle in os.listdir(pth):
                file = os.path.join(pth, fle)

                if fle.endswith('pyd'):
                    if name:
                        nme = name + '.' + os.path.splitext(fle)[0]
                    else:
                        nme = os.path.splitext(fle)[0]

                    mod_names.append([nme, file.replace('.pyd', '.pyi')])
                elif os.path.isdir(file):
                    if name:
                        nme = name + '.' + fle
                    else:
                        nme = fle

                    mod_names.extend(_get_module_names(file, nme))

            return mod_names

        mod = __import__('_libopenzwave')
        mod_name = '_libopenzwave'

        output = []
        end_output = ['\n']

        for key in dir(mod):
            if (
                key.startswith('__') or
                key in ('copyfile', 'get_distribution')
            ):
                continue

            value = getattr(mod, key)

            if inspect.isclass(value) and value.__name__ == key:
                output += [_build_class(key, value, '')]
            elif inspect.isfunction(value):
                output += [_build_func(key, value, '')]
            elif not key.startswith('_'):
                val = str(type(value)).split("'")[1]

                if mod_name in val:
                    val = val.replace(mod_name + '.', '')

                if val in (
                        'module',
                        'property',
                        'builtin_function_or_method'
                ):
                    continue

                if val in ('Enum', 'NotificationEnum'):
                    params = {}

                    for p_name in sorted(list(value.keys())):
                        addl_params = []
                        p_value = value[p_name]
                        idx = int(p_value)
                        doc = repr(p_value.doc)
                        if p_value.type is not None:
                            addl_params.append(
                                ADDL_PARAMS_TEMPLATE.format(
                                    param_name='type',
                                    param_value=repr(p_value.type)
                                )
                            )

                        if p_value._value is not None:  # NOQA
                            addl_params.append(
                                ADDL_PARAMS_TEMPLATE.format(
                                    param_name='value',
                                    param_value=repr(p_value._value)  # NOQA
                                )
                            )

                        params[idx] = ENUM_ITEM_TEMPLATE.format(
                            p_name=p_name,
                            cls_name=p_value.__class__.__name__,
                            doc=doc,
                            index=idx,
                            addl_params='\n'.join(addl_params)
                        )

                    classes = []
                    for idx in sorted(list(params.keys())):
                        classes.append(params[idx])

                    end_output += [ENUM_CLASS_TEMPLATE.format(
                        name=key,
                        cls_name=val,
                        classes=''.join(classes)
                    )]

                else:
                    if value is None:
                        val = ' = None'
                    else:
                        val = ': ' + val

                    end_output += [key + '{0}\n'.format(val)]

        output = ''.join(output + end_output)

        # imports, deletes = build_imports(mod_name)

        with open(os.path.join(build.build_lib, '_libopenzwave.pyi'), 'w') as f:
            f.write(HEADER)
            # f.write('\n' + imports + '\n')
            f.write(output)
            # f.write('\n\n' + deletes + '\n')

#
# def build_imports(name):
#     if name == '_libopenzwave':
#         return '', ''
#
#     res1 = []
#     res2 = []
#     if 'value' not in name:
#         res1.append('from .value import ZWaveValues, ZWaveValue')
#         res2.extend(['del ZWaveValues', 'del ZWaveValue'])
#     if 'state' not in name:
#         res1.append('from .state import StateItem, State')
#         res2.extend(['del StateItem', 'del State'])
#     if 'option' not in name:
#         res1.append('from .option import ZWaveOption')
#         res2.extend(['del ZWaveOption'])
#     if 'object' not in name:
#         res1.append('from .object import ZWaveObject')
#         res2.extend(['del ZWaveObject'])
#     if 'node_types' not in name:
#         res1.append('from .node_types import DeviceType, SpecificType,
#         GenericType, RoleType, BasicType, NodeType, Types')
#         res2.extend(['del DeviceType', 'del SpecificType', 'del GenericType',
#         'del RoleType', 'del BasicType', 'del NodeType', 'del Types'])
#     if 'node_types' in name or 'node' not in name:
#         res1.append('from .node import ZWaveNodes,
#         ZWaveNode, NodeId, URLs, Help')
#         res2.extend(['del ZWaveNodes', 'del ZWaveNode',
#         'del NodeId', 'del URLs', 'del Help'])
#     if 'network' not in name:
#         res1.append('from .network import ZWaveNetwork')
#         res2.extend(['del ZWaveNetwork'])
#     if 'manager' not in name:
#         res1.append('from .manager import ZWaveManager')
#         res2.extend(['del ZWaveManager'])
#     if 'location' not in name:
#         res1.append('from .location import ZWaveLocation')
#         res2.extend(['del ZWaveLocation'])
#     if 'controller' not in name:
#         res1.append('from .controller import ZWaveController')
#         res2.extend(['del ZWaveController'])
#     if 'association_group' not in name:
#         res1.append('from .association_group import ZWaveAssociationGroup')
#         res2.extend(['del ZWaveAssociationGroup'])
#
#     return '\n'.join(res1), '\n'.join(res2)
