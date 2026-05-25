import mpmath as mp

def ghost_prop(k, E_geo):
    mp.dps = 80
    return 1 / (k**2 + E_geo**2)

def gluon_prop(k, E_geo):
    mp.dps = 80
    return 1 / (k**2 + E_geo**2)

def integrand(k, E_geo):
    mp.dps = 80
    return k**3 * ghost_prop(k, E_geo) * gluon_prop(k, E_geo)

if __name__ == '__main__':
    mp.dps = 80
    delta_star = mp.mpf('1.710')
    gamma = mp.mpf('16.339')
    E_geo = delta_star / gamma

    k_max = 20 * E_geo

    # wrap integrand
    def wrapped_integrand(k):
        return integrand(k, E_geo)

    result = mp.quad(wrapped_integrand, [0, k_max])
    f1_dummy = result / (2 * mp.pi**2 * E_geo**2)

    print('E_geo        =', mp.nstr(E_geo, 20))
    print('Integral     =', mp.nstr(result, 20))
    print('f1_dummy     =', mp.nstr(f1_dummy, 20))
