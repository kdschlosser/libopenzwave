import os

base_path = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(base_path, '..'))


class RST:
    file_count = 0
    line_count = 0


class PY:
    file_count = 0
    line_count = 0
    comment_count = 0


class CPP:
    file_count = 0
    line_count = 0


class H:
    file_count = 0
    line_count = 0


class PYX:
    file_count = 0
    line_count = 0


class PXD:
    file_count = 0
    line_count = 0


class C:
    file_count = 0
    line_count = 0


extensions = [
    RST,
    PY,
    CPP,
    H,
    C,
    PXD,
    PYX
]


def iter_path(p):

    for f in os.listdir(p):
        d = os.path.join(p, f)
        if os.path.isdir(d):
            iter_path(d)
        else:
            for c in extensions:
                ext = '.' + c.__name__.lower()
                if f.endswith(ext):
                    break
            else:
                continue

            try:
                with open(d, 'r') as fle:
                    c.line_count += len(fle.readlines())

            except UnicodeDecodeError:
                with open(d, 'r', encoding='utf-8') as fle:
                    c.line_count += len(fle.readlines())

            cls.file_count += 1


iter_path(path)

file_count = 0
line_count = 0

for cls in extensions:
    print('.' + cls.__name__.lower() + ' Files')
    print('file count:', cls.file_count)
    print('line count:', cls.line_count)
    file_count += cls.file_count
    line_count += cls.line_count
    print()

print('totals')
print('file count:', file_count)
print('line count:', line_count)
