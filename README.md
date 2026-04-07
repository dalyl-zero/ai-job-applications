# AI Job Search Pipeline (VS Code + LaTeX)

This repository is a structured interface for running an AI-driven job application workflow.

The execution logic lives in [PROMPT.md](PROMPT.md).
This README explains only:
- what you should provide,
- what the AI will update,
- what outputs you should expect,
- how to set up VS Code and dependencies.

## What You Need to Provide

For each application cycle, your input is minimal.

1. Update [profile.md](profile.md)
- Your factual background, skills, experience, projects, constraints.
- Keep it concise and measurable.

2. Paste one target posting into [job_description.md](job_description.md)
- One role at a time is recommended.

3. Optional references in [references](references)
- Recommendation letters, old resumes, etc.
- If references are PDF files, AI/scripts can extract text.

4. Explicit status messages during process
- Example: "generate resume", "skip cover letter", "I applied", "rejected", "offer".

## What AI Is Expected to Do

When run with [PROMPT.md](PROMPT.md), AI should:
- read [profile.md](profile.md), [job_description.md](job_description.md), [tracker.md](tracker.md), and references,
- evaluate fit before generation,
- update only working files (not seed templates),
- keep LaTeX structure valid,
- update [tracker.md](tracker.md) on submission/status changes,
- archive final PDFs only after you confirm submission.

Do not treat this README as execution rules; [PROMPT.md](PROMPT.md) is the source of truth for runtime behavior.

## What Files Are Inputs vs Outputs

Inputs you maintain:
- [profile.md](profile.md)
- [job_description.md](job_description.md)
- [references](references)

Files AI updates:
- [resumes/resume.tex](resumes/resume.tex)
- [cover_letters/cover_letter.tex](cover_letters/cover_letter.tex)
- [tracker.md](tracker.md)

Generated outputs:
- `resumes/resume.pdf` (after compile)
- `cover_letters/cover_letter.pdf` (after compile)
- archive PDFs in `resumes/archive/` and `cover_letters/archive/` after submission

Seed templates (do not edit during normal runs):
- [resumes/template_en.tex](resumes/template_en.tex)
- [resumes/template_de.tex](resumes/template_de.tex)
- [cover_letters/template_en.tex](cover_letters/template_en.tex)
- [cover_letters/template_de.tex](cover_letters/template_de.tex)

## VS Code Setup

### Required Extensions

Install from VS Code Extensions:
- GitHub Copilot (`github.copilot`)
- GitHub Copilot Chat (`github.copilot-chat`)
- Python (`ms-python.python`)
- Pylance (`ms-python.vscode-pylance`)
- LaTeX Workshop (`James-Yu.latex-workshop`)

Optional:
- Markdown All in One (`yzhang.markdown-all-in-one`)
- Error Lens (`usernamehw.errorlens`)

### First-Run in VS Code

1. Open this repository folder.
2. Set Python interpreter to `.venv` after environment setup.
3. Confirm LaTeX Workshop can build `.tex` files.
4. Run AI tasks with [PROMPT.md](PROMPT.md) as instruction context.

## OS Dependencies

Install Python + LaTeX toolchain before first use.

### macOS

```bash
brew install python
brew install --cask mactex-no-gui
```

### Windows (PowerShell)

```powershell
winget install Python.Python.3.12
winget install MiKTeX.MiKTeX
winget install StrawberryPerl.StrawberryPerl
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip texlive-full latexmk perl
```

## Local Environment Setup

From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Minimal User Workflow

1. Fill [profile.md](profile.md).
2. Paste target role into [job_description.md](job_description.md).
3. Run preflight check:

```bash
python scripts/validate_inputs.py
```

4. Ask AI to run the workflow defined in [PROMPT.md](PROMPT.md).
5. Review generated `.tex` outputs.
6. Compile PDFs.
7. Confirm submission.
8. Let AI update [tracker.md](tracker.md) and archive outputs.

## Compile Commands

```bash
latexmk -pdf resumes/resume.tex
latexmk -pdf cover_letters/cover_letter.tex
```

## Utility Scripts (Optional Direct Use)

Extract PDF text:

```bash
python scripts/extract_pdf_text.py references/file.pdf
```

Preflight validation:

```bash
python scripts/validate_inputs.py
```

Merge PDFs:

```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf -o misc/merged.pdf
```

Archive submission PDFs:

```bash
python scripts/archive_application.py [application_id]
python scripts/archive_application.py --use-descriptive-name --company "Company" --role "Role"
```

## Troubleshooting

Dependency error (`ModuleNotFoundError: PyPDF2`):

```bash
pip install -r requirements.txt
```

`latexmk` missing:
- install OS LaTeX dependencies above,
- verify with `which latexmk` (macOS/Linux) or `where latexmk` (Windows).

Archive script cannot find PDFs:
- compile `.tex` files first,
- confirm `resumes/resume.pdf` and `cover_letters/cover_letter.pdf` exist.

Preflight validation fails:
- fill missing inputs in [job_description.md](job_description.md), [profile.md](profile.md), or [tracker.md](tracker.md),
- re-run `python scripts/validate_inputs.py`.
