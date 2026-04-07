# AI Job Search Pipeline (VS Code + LaTeX)

A prompt-driven workflow for tailoring resumes, cover letters, and application tracking with AI.

[README.md](README.md) is for setup and usage. [PROMPT.md](PROMPT.md) is the execution spec.

## What You Provide

- [profile.md](profile.md): your factual background, skills, experience, and constraints.
- [job_description.md](job_description.md): one target posting at a time.
- [references](references): optional PDFs or supporting documents.
- Status updates such as `generate resume`, `I applied`, `rejected`, or `offer`.

## What AI Updates

- [resumes/resume.tex](resumes/resume.tex)
- [cover_letters/cover_letter.tex](cover_letters/cover_letter.tex)
- [tracker.md](tracker.md)
- Archived PDFs only after you confirm submission.

Seed templates are read-only during normal use:

- [resumes/template_en.tex](resumes/template_en.tex)
- [resumes/template_de.tex](resumes/template_de.tex)
- [cover_letters/template_en.tex](cover_letters/template_en.tex)
- [cover_letters/template_de.tex](cover_letters/template_de.tex)

## Setup

### VS Code Extensions

Install:

- GitHub Copilot (`github.copilot`)
- GitHub Copilot Chat (`github.copilot-chat`)
- Python (`ms-python.python`)
- Pylance (`ms-python.vscode-pylance`)
- LaTeX Workshop (`James-Yu.latex-workshop`)

Optional:

- Markdown All in One (`yzhang.markdown-all-in-one`)
- Error Lens (`usernamehw.errorlens`)

### OS Dependencies

macOS:

```bash
brew install python
brew install --cask mactex-no-gui
```

Windows (PowerShell):

```powershell
winget install Python.Python.3.12
winget install MiKTeX.MiKTeX
winget install StrawberryPerl.StrawberryPerl
```

Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip texlive-full latexmk perl
```

### Python Environment

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

## How It Works

1. Fill [profile.md](profile.md).
2. Paste the target role into [job_description.md](job_description.md).
3. Run the preflight check:

```bash
python scripts/validate_inputs.py
```

4. Ask AI to follow [PROMPT.md](PROMPT.md).
5. Review generated `.tex` files.
6. Compile the PDFs.
7. Confirm submission.
8. Let AI update [tracker.md](tracker.md) and archive the final PDFs.

## Common Commands

Compile:

```bash
latexmk -pdf resumes/resume.tex
latexmk -pdf cover_letters/cover_letter.tex
```

Extract reference text:

```bash
python scripts/extract_pdf_text.py references/file.pdf
```

Validate inputs:

```bash
python scripts/validate_inputs.py
```

Merge PDFs:

```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf -o misc/merged.pdf
```

Archive a submission:

```bash
python scripts/archive_application.py [application_id]
python scripts/archive_application.py --use-descriptive-name --company "Company" --role "Role"
```

## Troubleshooting

Missing dependency:

```bash
pip install -r requirements.txt
```

`latexmk` missing:

- install the OS dependencies above,
- verify with `which latexmk` on macOS/Linux or `where latexmk` on Windows.

Archive script cannot find PDFs:

- compile the `.tex` files first,
- confirm `resumes/resume.pdf` and `cover_letters/cover_letter.pdf` exist.

Preflight validation fails:

- fill missing inputs in [job_description.md](job_description.md), [profile.md](profile.md), or [tracker.md](tracker.md),
- rerun `python scripts/validate_inputs.py`.
