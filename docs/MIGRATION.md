# Sphinx Migration

## Short Summary

Migrated the documentation from MkDocs to Sphinx with a `docs/` source tree, native reStructuredText pages, and an official GitHub Pages workflow.

## Long Summary

The documentation source layout now lives under `docs/` and uses Sphinx instead of MkDocs.
The existing Markdown content was converted to native `.rst` pages so the rendered text stays the same while the source format matches Sphinx conventions.
The old `graveyard/` documentation is now published under an `Archive` section.
Local setup now uses `.venv/`, `requirements-docs.txt`, `sphinx-build`, and `sphinx-autobuild`.
Deployment now uses the official GitHub Pages artifact flow with `actions/upload-pages-artifact` and `actions/deploy-pages`.
The previous MkDocs-specific configuration and workflow assumptions are no longer part of the active docs build.
