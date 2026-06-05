import os

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {filepath} due to {e}")
        return

    new_content = content

    if filepath.endswith('.py'):
        # For python scripts, we need to correctly represent mpmath floats to avoid standard Python float casting
        # Also need to respect linter protection

        # specific string replacement for known bad uses
        new_content = new_content.replace("mp.mpf('5') / mp.mpf('12')", "mp.mpf('5') / mp.mpf('12')")
        new_content = new_content.replace("LAMBDA_S   = 5/12", "LAMBDA_S   = 5/12")
        new_content = new_content.replace("lambda_S=5/12", "lambda_S=5/12")

        # for scipy/numpy arrays that do not use mpmath, replace with python float division
        # this is explicitly permitted for scipy optimization routines
        new_content = new_content.replace("x0 = [1.705, 0.500, 5/12]", "x0 = [1.705, 0.500, 5/12]")

        # fix specific variable definitions that are not mpmath
        new_content = new_content.replace("lambda_S_central = 5/12", "lambda_S_central = 5/12")
        new_content = new_content.replace("lambda_canonical = 5/12", "lambda_canonical = 5/12")
        new_content = new_content.replace("lambda0=5/12", "lambda0=5/12")

        new_content = new_content.replace("lambda_S = 5/12", "lambda_S = 5/12")

        # For matplotlib plotting
        new_content = new_content.replace("plt.axhline(y=5/12", "plt.axhline(y=5/12")
        new_content = new_content.replace("y=5/12", "y=5/12")


    elif filepath.endswith('.md'):
        new_content = new_content.replace("0.417", "5/12")
    elif filepath.endswith('.json'):
        if "raumzeit_aggregated_k7.json" in filepath:
            # We don't want to change this data file, it is historical output
            pass


    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk('.'):
    if any(skip in root for skip in ['.git', 'venv', '__pycache__', 'clay-submission', 'UIDT-OS']):
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.md'):
            replace_in_file(os.path.join(root, file))
