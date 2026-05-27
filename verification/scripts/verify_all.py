import subprocess
import sys
import os
from pathlib import Path


REQUIRED_SCRIPTS = [
    "verification/scripts/verify_rg_fixed_point.py",
    "verification/scripts/verify_light_quark_masses.py",
]

OPTIONAL_LEGACY_SCRIPTS = [
    # Historical entry points referenced by older reproduction notes. They are
    # reported when absent, but never counted as passed by this runner.
    "verification/scripts/verify_spectral_gap.py",
    "verification/scripts/verify_cosmology.py",
]

def run_script(script_path):
    print(f"========================================")
    print(f"Running {script_path}...")
    print(f"========================================")
    try:
        # Resolve python executable
        result = subprocess.run([sys.executable, script_path], check=True)
        print(f"[SUCCESS] {script_path} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {script_path} failed with exit code {e.returncode}.\n")
        sys.exit(1)

def run_pytest():
    print(f"========================================")
    print(f"Running full pytest suite...")
    print(f"========================================")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "verification/tests/", "-v"], check=True)
        print(f"[SUCCESS] Pytest suite completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Pytest suite failed with exit code {e.returncode}.\n")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure working directory is the repository root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(repo_root)

    print("Starting UIDT Framework Verification Suite...\n")

    missing_required = [
        script for script in REQUIRED_SCRIPTS if not Path(script).is_file()
    ]
    if missing_required:
        print("[ERROR] Required verification scripts are missing:")
        for script in missing_required:
            print(f"  - {script}")
        sys.exit(1)

    missing_optional = [
        script for script in OPTIONAL_LEGACY_SCRIPTS if not Path(script).is_file()
    ]
    if missing_optional:
        print("[INFO] Optional legacy verification entry points are absent:")
        for script in missing_optional:
            print(f"  - {script}")
        print("They are not counted as passed by this unified runner.\n")

    for script in REQUIRED_SCRIPTS:
        run_script(script)

    run_pytest()

    print("========================================")
    print("[ALL PASSED] Unified verification completed successfully.")
    print("========================================")
