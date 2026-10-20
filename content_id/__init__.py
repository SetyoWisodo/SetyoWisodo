# -*- coding: utf-8 -*-
"""Registry konten bab dalam (deep) edisi Indonesia."""

from .ch01 import CH as _ch01
from .ch02 import CH as _ch02
from .ch03 import CH as _ch03
from .ch04 import CH as _ch04
from .ch05 import CH as _ch05
from .ch06 import CH as _ch06
from .ch07 import CH as _ch07
from .ch08 import CH as _ch08
from .ch09 import CH as _ch09
from .ch10 import CH as _ch10
from .ch11 import CH as _ch11
from .ch12 import CH as _ch12

DEEP_ID = {
    1: _ch01,
    2: _ch02,
    3: _ch03,
    4: _ch04,
    5: _ch05,
    6: _ch06,
    7: _ch07,
    8: _ch08,
    9: _ch09,
    10: _ch10,
    11: _ch11,
    12: _ch12,
}
