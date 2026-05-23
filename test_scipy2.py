import scipy.optimize
from mpmath import mp
x0 = [mp.mpf('1.705'), mp.mpf('0.500'), mp.mpf('5')/mp.mpf('12')]
def f(x):
    return [x[0]-1, x[1]-1, x[2]-1]
res = scipy.optimize.root(f, x0, method='hybr', tol=1e-15)
print(res.x)
