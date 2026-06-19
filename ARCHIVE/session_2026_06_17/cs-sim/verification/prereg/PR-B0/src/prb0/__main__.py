import sys
from .audit import verify_grid, verify_injective
from .calibrate import run_calibration
from .boundary import run_boundary
from .report import generate_gate_report
from .ci import run_ci

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m prb0 <command>")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "verify-grid":
        verify_grid()
    elif cmd == "verify-injective":
        verify_injective()
    elif cmd == "verify-confusion":
        alpha_sweep = "--alpha-sweep" in sys.argv
        from .audit import verify_confusion
        verify_confusion(alpha_sweep=alpha_sweep)
    elif cmd == "calibrate":
        run_calibration()
    elif cmd == "boundary":
        run_boundary()
    elif cmd == "gate-report":
        generate_gate_report()
    elif cmd == "ci":
        run_ci()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
