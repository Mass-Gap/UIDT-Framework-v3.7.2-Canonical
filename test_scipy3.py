import scipy.optimize
x0 = [1.705, 0.500, 5.0/12.0]
def f(x):
    return [x[0]-1, x[1]-1, x[2]-1]
res = scipy.optimize.root(f, x0, method='hybr', tol=1e-15)
print(res.x)
