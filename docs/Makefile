# Makefile for Sphinx documentation
# Variables for the command line
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Add the package source dir relative to docs/
PKGDIR        = ../cachai

.PHONY: help clean html

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  html    to make standalone HTML files"

clean:
	rm -rf $(BUILDDIR)/*

html:
# Generate API docs automatically (excluding tests/ and remote_data.py)
#	sphinx-apidoc -o $(SOURCEDIR) $(PKGDIR) \
#		$(PKGDIR)/tests \
#		$(PKGDIR)/data/remote_data.py
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

	

