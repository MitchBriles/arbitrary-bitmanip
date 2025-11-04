"""
Bit manipulation instructions not found in Z3
"""

from z3 import *

def orcb_32(a):
    """
    RISC-V's orc.b: "Bitwise OR-Combine, byte granule."
    32-bit input
    """
    def byte(x):
        return If (x == BitVecVal(0, 8),
                BitVecVal(0x00, 32),
                BitVecVal(0xff, 32));
    b0 = byte(Extract(7, 0, a))
    b1 = byte(Extract(15, 8, a))
    b2 = byte(Extract(23, 16, a))
    b3 = byte(Extract(31, 24, a))
    return \
        b0 | \
        (b1 << BitVecVal(8, 32)) | \
        (b2 << BitVecVal(16, 32)) | \
        (b3 << BitVecVal(24, 32))

def orcb_16(a):
    """
    RISC-V's orc.b: "Bitwise OR-Combine, byte granule."
    16-bit input
    """
    def byte(x):
        return If (x == BitVecVal(0, 8),
                BitVecVal(0x00, 16),
                BitVecVal(0xff, 16));
    b0 = byte(Extract(7, 0, a))
    b1 = byte(Extract(15, 8, a))
    return \
        b0 | \
        (b1 << BitVecVal(8, 16))

def orc2_8(a):
    """
    Inspired by RISC-V's orc.b: "Bitwise OR-Combine, byte granule."
    Instead operates on 8 bits, with crumb granule.
    """
    def byte(x):
        return If (x == BitVecVal(0, 2),
                BitVecVal(0b00, 8),
                BitVecVal(0b11, 8));
    b0 = byte(Extract(1, 0, a))
    b1 = byte(Extract(3, 2, a))
    b2 = byte(Extract(5, 4, a))
    b3 = byte(Extract(7, 6, a))
    return \
        b0 | \
        (b1 << BitVecVal(2, 8)) | \
        (b2 << BitVecVal(4, 8)) | \
        (b3 << BitVecVal(6, 8))

def bit_reverse(x):
    """
    Returns a bit vector with the bits of `x` reversed
    """
    n = x.size()
    return Concat(*[Extract(i, i, x) for i in range(n)])

def fill_with_edge_xor(x):
    """
    Returns a bit vector with all bits set to (msb ^ lsb)
    """
    n = x.size()
    lsb = Extract(0, 0, x)
    msb = Extract(n - 1, n - 1, x)
    b = lsb ^ msb
    return Concat(*[b for _ in range(n)])
