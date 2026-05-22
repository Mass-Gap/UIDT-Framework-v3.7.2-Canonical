import mpmath as mp

def compute_total_suppression(gamma_val, steps=99):
    """
    Computes the total holographic suppression over 'steps' RG steps.
    Each step scales down the flow by q = 1/gamma.
    """
    mp.dps = 80
    gamma = mp.mpf(gamma_val)
    q = mp.mpf('1') / gamma
    return q ** steps

if __name__ == '__main__':
    mp.dps = 80
    gamma_val = mp.mpf('16.339')
    suppression = compute_total_suppression(gamma_val, steps=99)
    print(f"Total suppression factor: {suppression}")
    print(f"log10(suppression): {mp.log10(suppression)}")
    
    target = mp.mpf('1e-120')
    ratio = target / suppression
    print(f"Residual factor needed to reach 10^(-120): {ratio}")
