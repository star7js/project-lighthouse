#!/usr/bin/env python3
"""
L-039: Gauss, Cod. Ms. Gauss Math. 48 Cim. (the Tagebuch booklet), fol. 11r, pencil table.
Scan: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3382323:00000023/full/1600,/0/default.jpg

Heading on the scan:  a = 4n+1:  A = [] - a x []      a = 4n-1:  A = [] + a x []
Rows on the scan (coefficient lists, written under "1 + x +"):
   5 :  1+3+1                       |  1+1
  13 :  1+7+15+19+15+7+1            |  1+3+5+5+3+1
  17 :  1+9+11 -5 +15+5+11+9+1      |  1+3+1+3+3+1+3+1     (only one minus sign is clearly visible)

Checked here, with A = 1 + x + ... + x^(a-1):
  (1) rows 5 and 13 satisfy A = C^2 - a x D^2 exactly as written;
  (2) row 17 with all signs plus does not; exactly which sign patterns of the written magnitudes do;
  (3) these C, D are not the Y, Z of Disquisitiones art. 357 (4A = Y^2 - aZ^2) divided by 2;
  (4) the heading for a = 4n-1, tested on a = 3, 7, 11 (no rows for these on the page).
Run:  python3 -I verify/gm48_11r_cyclotomic_square_forms.py
"""
import itertools
import sympy as sp

x = sp.symbols("x")


def poly(coeffs):
    return sum(c * x**k for k, c in enumerate(coeffs))


def A(a):
    return sum(x**k for k in range(a))


ok = True
rows = {5: ([1, 3, 1], [1, 1]), 13: ([1, 7, 15, 19, 15, 7, 1], [1, 3, 5, 5, 3, 1])}
for a, (C, D) in rows.items():
    r = sp.expand(poly(C) ** 2 - a * x * poly(D) ** 2 - A(a)) == 0
    print(f"a = {a}: A = C^2 - a x D^2 as written: {r}")
    ok &= r

Cm, Dm = [1, 9, 11, 5, 15, 5, 11, 9, 1], [1, 3, 1, 3, 3, 1, 3, 1]
allplus = sp.expand(poly(Cm) ** 2 - 17 * x * poly(Dm) ** 2 - A(17)) == 0
print(f"a = 17, all signs plus: {allplus}  (expected False)")
ok &= not allplus
good = []
for sc in itertools.product([1, -1], repeat=len(Cm) - 1):
    C = [Cm[0]] + [s * c for s, c in zip(sc, Cm[1:])]
    for sd in itertools.product([1, -1], repeat=len(Dm) - 1):
        D = [Dm[0]] + [s * d for s, d in zip(sd, Dm[1:])]
        if sp.expand(poly(C) ** 2 - 17 * x * poly(D) ** 2 - A(17)) == 0:
            good.append((C, D))
print(f"a = 17: sign patterns of the written magnitudes that satisfy the identity: {len(good)}")
for C, D in good:
    print("   C =", C, " D =", D)
ok &= len(good) >= 1 and any(C[3:6] == [-5, -15, -5] for C, _ in good)

# (3) Disquisitiones art. 357 for a = 5: 4A = Y^2 - 5 Z^2 with Y = 2x^2 + x + 2, Z = x
Y, Z = 2 * x**2 + x + 2, x
da = sp.expand(Y**2 - 5 * Z**2 - 4 * A(5)) == 0
differs = sp.expand(2 * poly(rows[5][0]) - Y) != 0
print(f"art. 357 form for a = 5 holds: {da}; the page's C differs from Y/2: {differs}")
ok &= da and differs

# (4) heading for a = 4n-1: A = C^2 + a x D^2 has a solution with integer C, D
for a, C, D in [(3, [1, -1], [1]), (7, [1, -3, 3, -1], [1, -1, 1]), (11, [1, -5, -1, 1, 5, -1], [1, -1, -1, -1, 1])]:
    r = sp.expand(poly(C) ** 2 + a * x * poly(D) ** 2 - A(a)) == 0
    print(f"a = {a}: A = C^2 + a x D^2 with C = {C}, D = {D}: {r}")
    ok &= r

print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
