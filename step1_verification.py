import mpmath as mp
mp.dps = 80

# Exact rational values only
kappa = mp.mpf('1') / mp.mpf('2')
lambda_S = mp.mpf('5') / mp.mpf('12')

lhs = 5 * kappa**2        # must equal 5/4
rhs = 3 * lambda_S        # must equal 5/4

residual = abs(lhs - rhs)

assert residual < mp.mpf('1e-14'), f"[RG_CONSTRAINT_FAIL] residual={residual}"
print(f"LHS = {mp.nstr(lhs, 30)}")
print(f"RHS = {mp.nstr(rhs, 30)}")
print(f"Residual = {mp.nstr(residual, 10)}")  # expect 0.0 or < 1e-80
