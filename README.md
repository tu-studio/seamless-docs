# Documentation of the SeamLess system

currently built using mkdocs, will be migrated to sphinx in the future
to build:

```bash
cd old/Documentation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# To test the docs
mkdocs serve --livereload

# To deploy the docs
mkdocs gh-deploy


```
