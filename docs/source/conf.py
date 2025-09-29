# == Configuration file for the Sphinx documentation builder =======================================

# Path. This will tell sphinx where to finde the source code. Otherwise, sphinx will
# go for the pip installed version of cachai
import sys
import os
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information ---------------------------------------------------------------------------
project   = 'cachai'
copyright = '2025, D. Beltrán'
author    = 'Diego Beltrán'
release   = '0.1.0'

# -- General configuration -------------------------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinxemoji.sphinxemoji',
    'sphinx_copybutton',
]

templates_path = ['_templates']
exclude_patterns = [
    '../../cachai/tests/*',
    '../../cachai/data/remote_data.py',
    '../notebooks/*',
]

# -- Options for HTML output -----------------------------------------------------------------------
html_theme       = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files   = ['cachai_rtd_style.css',
                    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css']
html_js_files    = ['cachai_style.js']
html_logo        = '_static/cachai_logo_wide_light.svg'

html_theme_options = {
    'logo_only': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'vcs_pageview_mode': '',
    'flyout_display': 'hidden',
    'version_selector': True,
    'language_selector': True,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Bootstrap icons -------------------------------------------------------------------------------
rst_prolog = """
.. role:: bs-icon(raw)
   :format: html

.. |house-fill| replace:: :bs-icon:`<i class="bi bi-house-fill"></i>`
.. |github| replace:: :bs-icon:`<i class="bi bi-github"></i>`
.. |bug-fill| replace:: :bs-icon:`<i class="bi bi-bug-fill"></i>`
.. |gear-fill| replace:: :bs-icon:`<i class="bi bi-gear-fill"></i>`
.. |rocket-takeoff-fill| replace:: :bs-icon:`<i class="bi bi-rocket-takeoff-fill"></i>`
.. |file-earmark-code-fill| replace:: :bs-icon:`<i class="bi bi-file-earmark-code-fill"></i>`
.. |lightbulb-fill| replace:: :bs-icon:`<i class="bi bi-lightbulb-fill"></i>`
.. |vector-pen| replace:: :bs-icon:`<i class="bi bi-vector-pen"></i>`
.. |book-half| replace:: :bs-icon:`<i class="bi bi-book-half"></i>`
"""

# -- Autodoc options -------------------------------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": False,
    "inherited-members": False,
    "exclude-members": "set",
}

# -- Source-like link ------------------------------------------------------------------------------
from docutils import nodes
from sphinx.util.docutils import SphinxRole

class ViewcodeLinkRole(SphinxRole):
    def run(self):
        target = self.text.strip()
        parts = target.split(".")
        obj = parts[-1]
        mod = ".".join(parts[:-1])
        uri = f"../../_modules/{mod.replace('.', '/')}.html#{obj}"
        
        node = nodes.reference(
            rawtext=self.text,
            text="[source]",
            refuri=uri,
            classes=["viewcode-link"],
        )
        return [node], []

# -- Autodoc hook: skip unwanted modules/members ---------------------------------------------------
def skip_members(app, what, name, obj, skip, options):
    if name.startswith("cachai.tests"):
        return True
    if name == "cachai.data.remote_data":
        return True
    return skip

def setup(app):
    app.connect("autodoc-skip-member", skip_members)
    app.add_role("viewsource", ViewcodeLinkRole())