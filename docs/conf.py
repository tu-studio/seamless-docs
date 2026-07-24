project = "SeamLess"
author = "TU Studio"
copyright = "2026, TU Studio"
release = "0.0"
version = release
root_doc = "index"
language = "en"

extensions = [
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    ".venv",
    "Thumbs.db",
    ".DS_Store",
]

html_theme = "shibuya"
html_title = "SeamLess Documentation"
html_static_path = ["_static"]
html_logo = "_static/graphics/studio-logo.png"
html_favicon = "_static/graphics/studio-logo.png"
html_css_files = ["custom.css"]

html_theme_options = {
    "github_url": "https://github.com/tu-studio/seamless-docs",
    "nav_links": [
        {
            "title": "About",
            "url": "about",
            "summary": "About the System",
        },
        {
            "title": "Installation",
            "url": "installation/index",
            "summary": "Installation",
        },
        {
            "title": "Maintenance",
            "url": "maintenance/index",
            "summary": "Maintenance",
        },
        {
            "title": "Archive",
            "url": "archive/index",
            "summary": "Archive",
        },
    ],
}
