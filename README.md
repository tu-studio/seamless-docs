# Documentation of the SeamLess system

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt

# To test the docs
sphinx-autobuild docs _build/html

# To build the docs
sphinx-build -W --keep-going -b html docs _build/html
# To build the docs (strict)
sphinx-build -b html docs _build/html
# To deploy the docs
gh workflow run build_sphinx.yml --ref main
```
