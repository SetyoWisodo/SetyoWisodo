# -*- coding: utf-8 -*-
"""Registry konten bab dalam (deep) edisi Indonesia."""

from .ch01 import CH as _ch01
from .ch02 import CH as _ch02
from .ch03 import CH as _ch03
from .ch04 import CH as _ch04
from .ch05 import CH as _ch05

DEEP_ID = {
    1: _ch01,
    2: _ch02,
    3: _ch03,
    4: _ch04,
    5: _ch05,
}
