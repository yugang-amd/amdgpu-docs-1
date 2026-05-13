"""Configuration file for the Sphinx documentation builder."""
import os
from pathlib import Path
import shutil

html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "instinct.docs.amd.com")
html_context = {}
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True
project = "AMD GPU Driver (amdgpu)"

version = "30.30.3"
rocm_version = '7.2.3'
rocm_directory_version = '7.2.3' # in 6.0 rocm was located in /opt/rocm-6.0.0
amdgpu_version = '30.30.3' # directory in https://repo.radeon.com/rocm/apt/ and https://repo.radeon.com/amdgpu-install/
amdgpu_url_version = '30.30.3'
release = version
html_title = f"AMD GPU Driver (amdgpu) {version}"
author = "Advanced Micro Devices, Inc."
copyright = "Copyright (c) 2026 Advanced Micro Devices, Inc. All rights reserved."

# Supported linux version numbers
ubuntu_version_numbers = [('24.04', 'noble'), ('22.04', 'jammy')]
debian_version_numbers = [('13', 'noble'), ('12', 'jammy')]
rhel_release_version_numbers = ['10', '9', '8']
rhel_version_numbers = ['10.1', '10.0', '9.7', '9.6', '9.4', '8.10']
sles_version_numbers = ['15.7']
ol_release_version_numbers = ['10', '9', '8']
ol_version_numbers = ['10.1', '9.7', '8.10']
rl_version_numbers = ['9.7']

html_context = {
    "ubuntu_version_numbers" : ubuntu_version_numbers,
    "debian_version_numbers" : debian_version_numbers,
    "sles_version_numbers" : sles_version_numbers,
    "rhel_release_version_numbers" : rhel_release_version_numbers,
    "rhel_version_numbers" : rhel_version_numbers,
    "ol_release_version_numbers" : ol_release_version_numbers,
    "ol_version_numbers" : ol_version_numbers,
    "rl_version_numbers" : rl_version_numbers
}


# Required settings
html_theme = "rocm_docs_theme"
html_theme_options = {
    "flavor": "amdgpu",
    "announcement": f"<a id='rocm-banner' href='https://instinct.docs.amd.com/projects/amdgpu-docs/en/31.20.0-preview/'>AMD GPU Driver 31.20.0</a> is a technology preview intended for use only with <a id='rocm-banner' href='https://rocm.docs.amd.com/en/7.12.0-preview/index.html'>AMD ROCm 7.12.0 technology preview</a>. For production use, continue to use AMD GPU Driver {version} documentation.",
    "link_main_doc": True,
    "use_download_button": True,
    # Add any additional theme options here
}
extensions = [
    "rocm_docs",
    "sphinxcontrib.datatemplates",
    "sphinx_substitution_extensions",
]

# Table of contents
external_toc_path = "./sphinx/_toc.yml"

exclude_patterns = ['.venv']

EXCLUDED_DIRS = {
    "_build",
    "_templates",
    "_static",
    ".git",
    ".venv",
}

def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def generate_combined_markdown(app, exception):
    if exception:
        return

    docs_root = Path(app.srcdir)
    output_file = Path(app.outdir) / "llms.txt"

    print(output_file)

    all_files = sorted(docs_root.rglob("*.md"))

    combined = []
    combined.append("# Combined Documentation\n")

    for doc_file in all_files:
        if should_skip(doc_file):
            continue

        relative = doc_file.relative_to(docs_root)

        combined.append(f"\n---\n")
        combined.append(f"\n# {relative}\n")

        try:
            content = doc_file.read_text(encoding="utf-8")
            combined.append(content)
            combined.append("\n")

        except Exception as e:
            combined.append(f"\n[ERROR reading file: {e}]\n")

    output_file.write_text(
        "\n".join(combined),
        encoding="utf-8",
    )

def setup(app):
    app.connect("build-finished", generate_combined_markdown)

# Add the following replacements to every RST file.
rst_prolog = f"""
.. |version| replace:: {version}
.. |rocm_version| replace:: {rocm_version}
.. |amdgpu_version| replace:: {amdgpu_version}
.. |amdgpu_url_version| replace:: {amdgpu_url_version}
.. |rocm_directory_version| replace:: {rocm_directory_version}
"""
