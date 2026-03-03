# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Seamless'
version = '0.0'
copyright = '2026, TU Studio'
author = 'Fares Schulz, Max Weidauer, Manolo Müller'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.intersphinx',
        'sphinx.ext.viewcode',
        'sphinx.ext.napoleon',
        'sphinx.ext.graphviz',
        'myst_parser'
]

# templates_path = ['sphinx/_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"

# Add custom CSS for better syntax highlighting
html_static_path = ['sphinx/_static']
html_css_files = [
    'custom.css',
]

html_theme_options = {
    "github_url": "https://github.com/tu-studio/seamless-docs",
    "nav_links": [
            {
                "title": "About",
                "url": "about",
                "summary": "About the Seamless system"
            },

            # {
            #     "title": "Getting Started",
            #     "url": "getting_started",
            #     "summary": "How to get started with Anira"
            # },
            # {
            #     "title": "Usage Guide",
            #     "url": "usage",
            #     "summary": "Detailed usage instructions for Anira"
            # },
            # {
            #     "title": "API Documentation",
            #     "url": "api/index",
            #     "children": [
            #             {
            #                     "title": "Class List",
            #                     "url": "api/classlist",
            #                     "summary": "List of all classes in the API",
            #             },
            #             {
            #                     "title": "Struct List",
            #                     "url": "api/structlist",
            #                     "summary": "List of all structs in the API",
            #             },
            #     ]
            # },

    ]
}
