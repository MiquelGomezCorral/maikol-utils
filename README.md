# Welcoome to maikol-utils 🧰 V 0.6.5
maikol-utils is a lightweight and reusable Python utility package designed to speed up and clean up your everyday scripting and automation workflows.

Whether you're handling JSON files, managing the file system, cleaning up terminal outputs, or improving logging with colored messages and structured separators — this module brings a collection of practical tools ready to use.
# 🧑‍💻 Author
Developed by [Miquel Gómez](https://miquelgc.net) – Python developer.
Hand-picked utilities from real-world scripting and automation tasks.

# Structure

```
├── LICENSE
├── README.md
├── maikol-utils
│   ├── __init__.py
│   ├── file_utils.py
│   ├── print_utils.py
│   └── time_tracker.py
├── pyproject.toml
├── setup.py
└── usage_examples.ipynb
```

# 🚀 Features
- 🔹 Filesystem helpers: Easily check, load, save, and create files/directories.
- 🖨️ Colorful terminal prints: Add colored, formatted, or warning messages to your logs.
- 📜 Visual bash separators: Make your CLI outputs more structured and readable.
- 🧹 Terminal cleanup: Clear or update printed lines in-place for dynamic feedback.

# 📦 Installation

Option 1: _With pip_
1. With pip: `pip install maikol-utils`

Option 2: _Clonning the repo_
1. Clone it from [github](https://github.com/MiquelGomezCorral/maikol-utils): `git clone https://github.com/MiquelGomezCorral/maikol-utils`

### Examples of each function at the repo notebook
- This [notebook](https://github.com/MiquelGomezCorral/maikol-utils/blob/main/usage_examples.ipynb)


# 📘 Usage

```python
from maikol_utils.print_utils import print_separator, print_warn, clear_bash
from maikol_utils.file_utils import save_json, load_json

# Save data to JSON
save_json("outputs/data.json", {"name": "maikol"})

# Load safely from JSON
data = load_json("outputs/data.json")

# Print a section title with visual separator
print_separator("Processing Data", sep_type="SUPER")

# Warn with color
print_warn("This file is missing some fields!")

# Clean last 2 terminal lines
clear_bash(2)
```
# 📚 Functions Overview
### 🗃 File system
```python
save_json(path, content) — Save Python object to JSON.

load_json(path) — Load JSON or return empty dict if not found.

check_dirs_existance(paths) — Assert if dirs exist.

make_dirs(paths) — Create dirs if not present.
```


### 🎨 Terminal Printing
```python
print_separator(text, sep_type) — Print formatted section headers.

print_color(text, color) — Print in red, green, blue, etc.

print_warn(text) — Print warnings wrapped in ⚠️ emojis.

print_status(msg) — Overwrite previous line with dynamic status.

clear_bash(n) — Clear n lines above in terminal.

print_clear_bash(text, n) — Clear then print a new message.
```


# 🔧 Roadmap

- Add async support for I/O.
- Option to customize color themes.
- CLI preview tool for bash formatting.


### Upload
- If first time
```bash
pip install twine wheel
```
- Upload
```bash
```bash
source ../base_env/bin/activate
rm -fr dist
python -m build
twine upload dist/*
```