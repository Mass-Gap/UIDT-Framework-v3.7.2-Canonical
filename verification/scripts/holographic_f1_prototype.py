import mpmath as mp

mp.dps = 80

# Kanonische Konstanten
delta_star = mp.mpf('1.710')  # ∆* in GeV
gamma    = mp.mpf('16.339')    # γ (kalibriert)
E_geo    = delta_star / gamma  # geometrische Skala

# Dummy‑Propagatoren für Ghost und Gluon (RGZ‑artig, rein demonstrativ)
def ghost_prop(k):
    return 1 / (k**2 + E_geo**2)

def gluon_prop(k):
    return 1 / (k**2 + E_geo**2)

# Integrand des radialsymmetrischen Dyson‑Schwinger‑Ansatzes
# Maßfaktor k^3 stammt aus 4D‑Sphärenkoordinaten
# f1_dummy = (1/(2 π^2 E_geo^2)) * ∫_0^{k_max} k^3 G(k) D(k) dk

def integrand(k):
    return k**3 * ghost_prop(k) * gluon_prop(k)

# Integrationsgrenze (UV‑Cutoff proportional zu E_geo)
k_max = 20 * E_geo

# Numerische Integration mit mp.quad
result = mp.quad(integrand, [0, k_max])
# Vorfaktor zur Normierung
f1_dummy = result / (2 * mp.pi**2 * E_geo**2)

if __name__ == '__main__':
    print('E_geo        =', mp.nstr(E_geo, 20))
    print('Integral     =', mp.nstr(result, 20))
    print('f1_dummy     =', mp.nstr(f1_dummy, 20))
