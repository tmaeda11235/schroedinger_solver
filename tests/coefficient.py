from sympy import *
from operator import *
from functools import *
dx = symbols("dx1:7")
x = symbols("x")
xi = symbols("x:7")
yi = symbols("y:7")
h = symbols('h')

p = lambda i: reduce(mul, [x - j for j in xi if not j == xi[i]])
p_ = lambda i: reduce(mul, [xi[i] - j for j in xi if not j == xi[i]])
P = lambda i: p(i)/p_(i) * yi[i]
F = sum([P(i) for i in range(7)])

g = [h if j <= i else h * 1.1 **  (j - i) for i in range(6) for j in range(6)]
G = list(reversed([g[6 * i:6 * i+6] for i in range(6)]))

O = []
[ O.append(a) for GG in G for a in zip(dx , GG)]
o = [O[6 * i:6 * i+6] for i in range(6)]

xii = [xi[0]]
for i, DX in enumerate(dx):
    xii.append(xii[i] + DX)
print(xii)
sxi = []
[sxi.append(a) for a in zip(xi, xii)]

for oo in o:
    B = simplify(expand(diff(F, x, 2).subs(x,xii[3]).subs(sxi).subs(oo)))
    print(latex((B * 360 * h ** 2).evalf()),"\n\n\n\n")