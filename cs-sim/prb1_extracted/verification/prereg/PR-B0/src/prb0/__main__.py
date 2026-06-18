import sys
from .audit import verify_grid, verify_injective
from .calibrate import run_calibration
from .boundary import run_boundary
from .report import generate_gate_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m prb0 <command>")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "verify-grid":
        verify_grid()
    elif cmd == "verify-injective":
        verify_injective()
    elif cmd == "calibrate":
        run_calibration()
    elif cmd == "boundary":
        run_boundary()
    elif cmd == "gate-report":
        generate_gate_report()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
