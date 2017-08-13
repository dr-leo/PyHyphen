import sys

__all__ = ['TextWrapper', 'wrap', 'fill']


if sys.version[0] == '2':
    from .python2 import TextWrapper
else:
    from .python3 import TextWrapper

def wrap(text, width=70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)

def fill(text, width=70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.fill(text)
