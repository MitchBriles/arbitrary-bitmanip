from z3 import *
from fns import *

N = 32

def bitmanip(x, M, mask, exclusive):
    bits = []
    for i in range(N):
        acc = BitVecVal(0, 1)
        for j in range(N):
            idx = i * N + j
            mbit = Extract(idx, idx, M)
            xbit = Extract(j, j, x)
            acc = If(exclusive, acc ^ (mbit & xbit), acc | (mbit & xbit)) 
        bits.append(acc)

    y = Concat(*reversed(bits))
    return y ^ mask

if __name__ == "__main__":
    x = BitVec('x', N)
    M = BitVec('M', N*N)
    mask = BitVec('b', N)
    exclusive = Bool('exclusive')

    constr = orcb_32(x) == bitmanip(x, M, mask, exclusive)

    s = Solver()

    s.add(exclusive == False)
    s.add(ForAll(x, constr))

    # print(s.to_smt2())

    if s.check() == sat:
        m = s.model()
        print("sound optimization for:")
        resM = int(str(m.eval(M, model_completion=True)))
        print("M =")
        [print(*f"{resM:0{N*N}b}"[i:i+N]) for i in range(0, N*N, N)]
        print("mask = " + str(m.eval(mask, model_completion=True)))
        print("exclusive = " + str(m.eval(exclusive, model_completion=True)))
    else:
        print("unsound optimization")