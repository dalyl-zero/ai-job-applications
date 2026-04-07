"""Archive resume and cover letter PDFs at application submission time.

Usage:
    python scripts/archive_application.py [application_id]
    python scripts/archive_application.py --use-descriptive-name --company "Company Name" --role "Role Name"

PDFs are copied from their working directories (resumes/, cover_letters/)
into the respective archive/ subdirectories with a dated archive filename.
"""

import os
import argparse
from datetime import datetime
import re
from PyPDF2 import PdfReader, PdfWriter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESUME_DIR = os.path.join(PROJECT_ROOT, "resumes")
COVER_DIR = os.path.join(PROJECT_ROOT, "cover_letters")
RESUME_ARCHIVE = os.path.join(RESUME_DIR, "archive")
COVER_ARCHIVE = os.path.join(COVER_DIR, "archive")


def sanitize(name):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def _build_identifier(application_id=None, company=None, role=None, use_descriptive_name=False):
    if application_id:
        return sanitize(application_id)

    if use_descriptive_name and company and role:
        return f"{sanitize(company)}_{sanitize(role)}"

    return f"application_{datetime.today().strftime('%H%M%S')}"


def _copy_pdf_without_metadata(src, dst):
    reader = PdfReader(src)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Keep output generic by removing identifying producer/author fields.
    writer.add_metadata({})

    with open(dst, "wb") as f:
        writer.write(f)


def archive_file(file_type, identifier):
    today = datetime.today().strftime("%Y-%m-%d")
    base_name = f"{today}_{identifier}_{file_type}.pdf"

    if file_type == "resume":
        src = os.path.join(RESUME_DIR, "resume.pdf")
        archive_dir = RESUME_ARCHIVE
    else:
        src = os.path.join(COVER_DIR, "cover_letter.pdf")
        archive_dir = COVER_ARCHIVE

    if not os.path.isfile(src):
        print(f"Warning: No {file_type} PDF found at {src}")
        return False

    os.makedirs(archive_dir, exist_ok=True)
    dst = os.path.join(archive_dir, base_name)
    _copy_pdf_without_metadata(src, dst)
    print(f"Archived: {dst}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive application PDFs with privacy-safe defaults.")
    parser.add_argument("application_id", nargs="?", help="Generic application id (for example: app_001)")
    parser.add_argument("--company", help="Company name (optional; only used with --use-descriptive-name)")
    parser.add_argument("--role", help="Role name (optional; only used with --use-descriptive-name)")
    parser.add_argument(
        "--use-descriptive-name",
        action="store_true",
        help="Use company/role in archive filename. Disabled by default for privacy.",
    )

    args = parser.parse_args()
    identifier = _build_identifier(
        application_id=args.application_id,
        company=args.company,
        role=args.role,
        use_descriptive_name=args.use_descriptive_name,
    )

    archive_file("resume", identifier)
    archive_file("cover_letter", identifier)
