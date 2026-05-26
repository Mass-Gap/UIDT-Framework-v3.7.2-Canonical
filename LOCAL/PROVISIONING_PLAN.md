# UIDT-OS System Provisioning and Workspace Installation Plan
**Project:** Vacuum Information Density as the Fundamental Geometric Scalar  
**Document version:** 1.0.0  
**Target Environment:** Windows 11 / PowerShell 7 (Host) & Linux/Docker (Container)  
**Classification:** Scientific Infrastructure & Repository Governance  

---

## 1. Auto-Start Script Evaluation & Recommendations

An audit of the existing startup and synchronization batch scripts has revealed critical issues that conflict with the UIDT-OS Elite Rules and modern reproducibility standards.

### Existing Scripts Reviewed:
1. **[antigravity_startup_sync.bat](file:///c:/Users/badbu/Documents/github/UIDT-Framework-V3.9/UIDT-OS/scripts/antigravity_startup_sync.bat)**:
   - *Purpose:* Prunes remote git, checks branch status, runs a quick verification test, and removes ephemeral/internal leak folders (`.kiro`, `.trae`).
   - *Defects:*
     - Hardcoded path (`cd /d "c:\Users\badbu\Documents\github\UIDT-Framework-V3.9"`). This breaks compatibility if the workspace is cloned elsewhere.
     - Written in CMD Batch (`.bat`), which lacks advanced error catching, logging, and state serialization.
     - Ephemeral cleanup does not log which files were removed.
2. **[startup_uidt_cache.bat](file:///c:/Users/badbu/Documents/github/UIDT-Framework-V3.9/UIDT-OS/scripts/startup_uidt_cache.bat)**:
   - *Purpose:* Calls `python LOCAL\scripts\startup_optimizer.py`.
   - *Defects:*
     - **Direct Rule Violation:** Invokes `python` on line 3, violating the Windows launcher rule (`py`). On Windows hosts, using `python` directly can accidentally invoke Windows App Store stub or mismatched global versions instead of the active workspace runtime.
3. **[startup_optimizer.py](file:///c:/Users/badbu/Documents/github/UIDT-Framework-V3.9/UIDT-OS/LOCAL/scripts/startup_optimizer.py)**:
   - *Purpose:* Verifies directory structure, checks critical files, tests MCP server availability, verifies the SQLite database, and executes auto-caching.
   - *Defects:*
     - Executes subprocess commands using `["python", ...]` (lines 113, 177), which violates the Windows launcher rule.
     - Does not verify package integrity or check for missing requirements prior to importing modules.
     - Database health check only counts claims; it does not check SQLite integrity (`PRAGMA integrity_check;`).

### Proposed Solution:
A unified PowerShell script **`UIDT-OS/scripts/uidt_startup.ps1`** should replace the existing `.bat` files. This script will:
- Dynamically resolve the repository root directory relative to the script location.
- Enforce the `py` launcher for all Windows operations.
- Verify that `mpmath==1.3.0` and `pytest==8.2.2` are installed and match required versions before proceeding.
- Validate the integrity of SQLite databases (`uidt_os.db` and project databases).
- Report on any uncommitted changes in protected paths (`CANONICAL/`, `LEDGER/`, `core/`, `modules/`).
- Auto-prune duplicate or conflicted Jules PRs from the local branch mapping.

---

## 2. Required System Tools (Windows Host)

To ensure full local support for the repository management suite, the following core system tools must be installed.

| Tool / CLI | Installation command (winget) | Purpose in UIDT-OS Workflow |
| :--- | :--- | :--- |
| **Git** | `winget install --id Git.Git -e` | Version control engine. |
| **GitHub CLI (`gh`)** | `winget install --id GitHub.cli -e` | Auth, PR checks, issue tracking, and CI/CD log fetching. |
| **PowerShell 7** | `winget install --id Microsoft.PowerShell -e` | Executes the administrative pipeline and intake guards. |
| **Python 3.11** | `winget install --id Python.Python.3.11 -e` | Local physics verification runtime. |
| **Node.js LTS** | `winget install --id OpenJS.NodeJS.LTS -e` | Runs local MCP servers (e.g. SQLite, filesystem). |
| **Delta** | `winget install --id dandavison.delta -e` | High-fidelity scientific diff classification. |
| **ripgrep (`rg`)** | `winget install --id BurntSushi.ripgrep.MSVC -e` | Fast, low-resource workspace search. |
| **jq** | `winget install --id jqlang.jq -e` | Direct validation and manipulation of `LEDGER/CLAIMS.json`. |
| **yq** | `winget install --id MikeFarah.yq -e` | Validating workflow files and YAML configurations. |
| **actionlint** | `winget install --id rhysd.actionlint -e` | Linting and validation of GitHub Actions. |
| **shellcheck** | `winget install --id koalaman.shellcheck -e` | Syntax and safety verification for local shell scripts. |

---

## 3. Required Python Packages

All Python packages must be installed using the Windows launcher `py -m pip`.

### 3.1 Physics & Mathematics Core
```powershell
py -m pip install mpmath==1.3.0 pytest==8.2.2 numpy==2.4.2 scipy==1.17.0 matplotlib==3.10.8 pandas sympy
```
* **mpmath:** Enforces 80-digit arbitrary precision mathematics (no float conversions).
* **pytest:** Powers the mathematical verification suites.
* **sympy:** Symbolic validation of mathematical operators.

### 3.2 Lints, Type Checking & Verification
```powershell
py -m pip install ruff mypy pyright pytest-cov hypothesis coverage tox
```
* **ruff/mypy/pyright:** Static analysis. Ruff should be configured *not* to auto-delete physical constants or unused variables representing vacuum baselines.
* **hypothesis:** Property-based testing for mathematical boundary conditions.

### 3.3 Security, Serialization & Lockfiles
```powershell
py -m pip install check-jsonschema jsonschema pydantic pip-tools pip-audit safety detect-secrets bandit semgrep
```
* **check-jsonschema / jsonschema:** Structural validation of claims JSON and database mapping.
* **pip-tools:** Enforces hash-locked `requirements.lock` creation.
* **detect-secrets / bandit / semgrep:** Prevents accidental leakage of local API keys, absolute paths, or credentials.

### 3.4 Scientific Citation & API Integration
```powershell
py -m pip install requests httpx beautifulsoup4 arxiv bibtexparser pybtex habanero
```
* **arxiv / bibtexparser / habanero:** Cross-references claimed physical limits and lattice coefficients against DOIs and arXiv metadata.

### 3.5 Local Vector DB & Document Ingestion
```powershell
py -m pip install chromadb llama-index sentence-transformers networkx graphviz pymupdf pdfplumber pypdf python-docx python-pptx
```
* **chromadb / llama-index:** Local vector database to cache PDF contents and manuscripts.
* **pymupdf / pdfplumber:** Raw text and math parsing from external physics papers.

### 3.6 Formal Verification
```powershell
py -m pip install z3-solver
```
* **z3-solver:** SMT solver to perform logical closure verification of claim dependencies.

---

## 4. Local Guard Scripts & Verification Tools (To Be Created)

These tools must be created locally inside `.codex/tools/` or `.uidt-local/tools/` to act as defensive layers for the repository:

1. **`uidt_pr_intake_guard.ps1`**  
   Audits incoming PRs. Detects whether they are Drafts, checks if they touch protected files, validates the presence of the Claims Table and Reproduction Notes, and verifies the DOI/arXiv status.
2. **`uidt_protected_path_guard.ps1`**  
   Pre-commit/Pre-push hook to block unauthorized modifications to `CANONICAL/`, `LEDGER/`, `core/`, `modules/`, and governance files.
3. **`uidt_diff_classifier.ps1`**  
   Parses `git diff` and classifies changes into `SAFE_DOCS`, `SAFE_LOCAL_TOOLING`, `REVIEW_REQUIRED`, `SCIENTIFIC_BEHAVIOR_CHANGE`, or `HARD_BLOCK`.
4. **`uidt_numerics_scan.py`**  
   Scans Python code for float leakage (e.g. `float()`), custom rounding functions, `unittest.mock` usage, missing `mp.dps = 80` declarations, or low-precision assertions.
5. **`uidt_evidence_scan.py`**  
   Scans documentation and commit messages to verify that evidence categories (`[A]`, `[A-]`, `[B]`, etc.) match the ledger and prevents inflation of claims (e.g. claiming a phenomenological constant is mathematically proven).
6. **`uidt_citation_resolver.py`**  
   Validates Zenodo and arXiv DOIs defined in PR bodies and `CITATION.cff` using online resolvers.
7. **`uidt_claim_traceability_scan.py`**  
   Maps Claim IDs in code and papers back to their entry in `LEDGER/CLAIMS.json` and verification scripts.
8. **`uidt_version_drift_check.ps1`**  
   Verifies consistency between the active framework version in `CANONICAL/CONSTANTS.md`, `CITATION.cff`, `STATUS.md`, and Dockerfile labels.
9. **`uidt_dependency_repro_check.ps1`**  
   Checks that `requirements.txt` is strictly pinned, checks for the existence of hash-locked dependency lists, and audits the Dockerfile for digest-pinned base images.
10. **`uidt_filesystem_guard.ps1`**  
    Blocks root-level file creation (such as test scripts, temp folders, or scratch directories) to prevent filesystem pollution.
11. **`uidt_ci_log_reader.ps1`**  
    Retrieves and parses failing logs from GitHub Actions using the `gh` CLI to expose precise Python/Pytest exceptions.

---

## 5. Required Agent Skills (Instruction Sets)

The following instruction sets (markdown rules) must be added to `.codex/skills/` to define the behavioral logic of AI agents:

* **`uidt-repo-guardian.md`**: Protocol for protected paths and write restrictions.
* **`uidt-pr-intake-guardian.md`**: Procedures for triaging, reviewing, and staging incoming PRs.
* **`uidt-diff-reviewer.md`**: Logical guidelines for certifying that code changes do not alter physics formulas.
* **`uidt-numerical-verifier.md`**: Instructions for enforcing `mpmath` and blocking floats/mocks.
* **`uidt-evidence-auditor.md`**: Enforces strict evidence category grades and limits.
* **`uidt-citation-verifier.md`**: Checks citation resolving and DOI validation.
* **`uidt-filesystem-auditor.md`**: Enforces the absolute file layout defined in `filesystem-tree.md`.
* **`uidt-reproducibility-auditor.md`**: Verifies dependency hash locking and digest-pinned containers.

---

## 6. Execution Workflow: System Provisioning

To prepare the system for operation, the following sequential execution workflow is planned:

### Phase 1: Host System Provisioning
Install all missing external tools on the Windows host machine via PowerShell using Administrator privileges:
```powershell
# Run in Administrator PowerShell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
winget install --id Microsoft.PowerShell -e
winget install --id Python.Python.3.11 -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id dandavison.delta -e
winget install --id sharkdp.bat -e
winget install --id sharkdp.fd -e
winget install --id BurntSushi.ripgrep.MSVC -e
winget install --id jqlang.jq -e
winget install --id MikeFarah.yq -e
winget install --id rhysd.actionlint -e
winget install --id koalaman.shellcheck -e
```

### Phase 2: Python Environment Setup
Prepare the virtual environment and install the required numerical, linting, validation, and citation packages:
```powershell
# Enforce py launcher usage
py -m venv .venv
.venv\Scripts\Activate.ps1

# Upgrade package management
py -m pip install --upgrade pip setuptools wheel

# Install science core
py -m pip install mpmath==1.3.0 pytest==8.2.2 numpy==2.4.2 scipy==1.17.0 matplotlib==3.10.8 pandas sympy

# Install lints and testing
py -m pip install ruff mypy pyright pytest-cov hypothesis coverage tox

# Install security and serialization
py -m pip install check-jsonschema jsonschema pydantic pip-tools pip-audit safety detect-secrets bandit semgrep

# Install citation and ingestion tools
py -m pip install requests httpx beautifulsoup4 arxiv bibtexparser pybtex habanero

# Install vector databases and processing
py -m pip install chromadb llama-index sentence-transformers networkx graphviz pymupdf pdfplumber pypdf python-docx python-pptx

# Install formal verification
py -m pip install z3-solver
```

### Phase 3: Auto-Start Script Refactoring
1. Rename/deprecate `UIDT-OS/scripts/antigravity_startup_sync.bat`.
2. Create `UIDT-OS/scripts/uidt_startup.ps1` incorporating:
   - `py` launcher enforcement.
   - Dynamic path resolution.
   - SQLite `integrity_check` for `uidt_os.db` and project databases.
   - Requirement verification checks.
   - Safe cleanup logging.
3. Update `UIDT-OS/uidt.bat` or create `UIDT-OS/uidt.ps1` to link into the new startup script.
4. Establish local configuration injection to update the user settings for Cursor/Trae/Claude Desktop MCP servers automatically via PowerShell.
