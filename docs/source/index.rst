.. rst-class:: hide-me

Home
====================================================================================================


.. raw:: html

   <div class="section-banner">
     <img src="_static/cachai_logo_wide.svg" alt="CACHAI's logo" />
   </div>


Welcome! **cachai**  (Custom Axes and CHarts Advanced Interface) is a fully customizable Python
visualization toolkit designed to deliver polished, publication-ready plots built on top of
Matplotlib. Currently, the package includes the  ``ChordDiagram``  module as its primary feature.
For details on the toolkit's capabilities, motivations and future projections, refer to
`this paper <https://iopscience.iop.org/article/10.3847/2515-5172/adf8df>`_ |:smile:|.

To contribute or report bugs, please visit the
`issues page <https://github.com/DD-Beltran-F/cachai/issues>`_.

.. admonition:: Fun fact
   :class: midtur-style
   
   "Cachai" (/kɑːˈtʃaɪ/) is a slang word from Chilean informal speech, similar to saying "ya know?"
   or "get it?" in English. Don't know how to pronounce it? Think of "kah-CHAI" (like "cut" + 
   "chai" tea, with stress on "CHAI").

----------------------------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 1
   :caption: Contents

   installation
   getting_started
   examples
   documentation/indexdoc
   citing

.. toctree::
   :maxdepth: 1
   :caption: Links

   Source code <https://github.com/DD-Beltran-F/cachai>
   Report an issue <https://github.com/DD-Beltran-F/cachai/issues>
   Changelog <https://github.com/DD-Beltran-F/cachai/releases>
   PyPI <https://pypi.org/project/cachai/>

----------------------------------------------------------------------------------------------------

**About cachai**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
From "*CACHAI’s first module: a fully customizable chord diagram for astronomy and beyond*"" 
(`Beltrán, D. & Dantas, M. L. L., 2025
<https://iopscience.iop.org/article/10.3847/2515-5172/adf8df>`_):

.. container:: paper-block

   Effective data visualization turns complex relationships into intuitive insights, accelerating
   scientific progress across disciplines (e.g. C. Wilke 2019). In astronomy,
   where high-dimensional data are common, the choice of visualization tools directly affects both
   interpretation and communication. Chord diagrams are particularly valuable for illustrating
   weighted, non-directional connections --- such as (anti-)correlations --- between variables 
   (M. Krzywinski et al. 2009), but existing implementations often lack the flexibility.

   In **Python**, support for chord diagrams is limited. **Plotly** offers interactive diagrams
   but minimal stylistic control (Plotly Technologies Inc. 2015), while **Matplotlib** lacks native
   support (J. D. Hunter 2007). In contrast, **R** packages like **Circlize** (Z. Gu et al. 2014)
   and astronomy-focused tools like **Amada** (R. S. de Souza & B. Ciardi 2015) provide more
   options, but often omit key features such as link styling, node gradients, or precise label
   control.

   The :class:`ChordDiagram` module in **cachai** addresses this gap, combining immediate usability with
   room for future expansion. It is shaped by both astronomical and general visualization needs and
   principles (e.g. N. P. Rougier et al. 2014, and references therein), bridging exploratory
   analysis and polished presentation.

   Future modules will expand its capabilities beyond chord diagrams. A more complete description
   is expected to follow in a forthcoming publication.