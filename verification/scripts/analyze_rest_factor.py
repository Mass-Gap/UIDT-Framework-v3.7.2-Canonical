import mpmath as mp

def analyze_rest_factor(rest_value: str) -> None:
    """Vergleicht den Restfaktor mit fundamentalen Konstanten."""
    mp.dps = 80
    rest = mp.mpf(rest_value)
    # Kandidaten mit theoretischer Motivation
    candidates = {
        '4/pi': mp.mpf('4') / mp.pi,
        'sqrt(e/2)': mp.sqrt(mp.e / mp.mpf('2')),
        '9/7': mp.mpf('9') / mp.mpf('7'),
        'area ratio S4/S3': (mp.mpf('2') * mp.pi**(mp.mpf('5')/mp.mpf('2')) / mp.gamma(mp.mpf('5')/mp.mpf('2'))) / (mp.mpf('2') * mp.pi**mp.mpf('2') / mp.gamma(mp.mpf('2'))),
        'volume ratio B4/B3': (mp.pi**mp.mpf('2') / mp.gamma(mp.mpf('3'))) / (mp.pi**(mp.mpf('3')/mp.mpf('2')) / mp.gamma(mp.mpf('5')/mp.mpf('2'))),
    }
    for name, value in candidates.items():
        diff = mp.fabs(rest - value)
        print(f"{name}: value={value}, diff={diff}")

if __name__ == '__main__':
    analyze_rest_factor('1.28623938766881')
