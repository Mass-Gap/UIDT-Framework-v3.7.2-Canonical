import mpmath as mp
mp.dps = 80
x0 = [1.705, 0.500, float(5)/12] # This is exactly what the code reviewer complained about, I need to use `5/12` but I need to make sure I don't use `float(5)/12` or `5/12` if `scipy` complains. Wait, `scipy.optimize.root` requires floats. Let's see what the reviewer said.
