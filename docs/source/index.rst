.. rst-class:: hide-me

Home
====================================================================================================


.. raw:: html

   <div class="section-banner">
     <img src="_static/cachai_logo_wide.svg" alt="CACHAI's logo" />
   </div>


Welcome! **cachai**  (Custom Axes and CHarts Advanced Interface) is a fully customizable Python
visualization toolkit designed to deliver polished, publication-ready plots built on top of
Matplotlib. Currently, the package includes the  ``chplot.chord``  module as its primary feature.
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

.. container:: toctree-columns

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

**What's new?**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <div class="news-grid">

    <div id="news-modal" class="news-modal">
      <div class="news-modal-window">
        <button
          class="news-modal-close"
          aria-label="Close">
          &times;
        </button>

        <iframe
          id="news-modal-frame"
          class="news-modal-frame"
          title="News article">
        </iframe>
      </div>
    </div>

    <a href="https://pypi.org/project/cachai/0.1.5/" class="news-version-card" target="_blank"
    rel="noopener noreferrer">
      <div class="news-content">
        <div class="news-title">
          <span class="news-version">v0.1.5</span> Improvement to the highlighting of Chord Diagrams
        </div>
        <div class="news-date">
          22 August 2026
        </div>
        <div class="news-summary">
          The highlighting functionality for chord diagrams has been improved. It is now more
          intuitive and user-friendly. In addition, the
          <span class="code-text">highlight_threshold</span> method has been added, which allows
          highlighting based on the correlation coefficient.
        </div>
      </div>
    </a>

    <a href="#" class="news-card" data-news="python-meeting">
      <div class="news-content">
      <div class="news-title">
          Cachai made an appearance in the “Python meetings” at the PUC Institute of Astrophysics!
      </div>
      <div class="news-date">
          21 November 2025
      </div>
      <div class="news-summary">
          Today we had the opportunity to present Cachai at the <span class="bf-text">Python Meeting
          #12</span> of the Institute of Astrophysics at the Pontificia Universidad Católica de
          Chile (PUC). The <span class="it-text">Python Meetings</span> are practical sessions
          organized by the institute's graduate students, aimed at students and researchers
          intere<span class="news-readmore">...read more</span>

      </div>
      </div>
      <div class="news-image">
      <img src="_static/news/ia_uc.png"
            alt="Facade of the Institute of Astrophysics at PUC">
      </div>
    </a>
     
    <a href="https://pypi.org/project/cachai/0.1.0/" class="news-version-card" target="_blank"
    rel="noopener noreferrer">
      <div class="news-content">
        <div class="news-title">
          <span class="news-version">v0.1.0</span> Introducing the new documentation
        </div>
        <div class="news-date">
          29 September 2025
        </div>
        <div class="news-summary">
          Cachai now comes with a completely redesigned documentation in <span class="bf-text">Read
          <span class="it-text">the</span> Docs</span>, including detailed guides, API references,
          and examples to help you get started.
        </div>
      </div>
    </a>

    <a href="#" class="news-card" data-news="rnaas-I">
      <div class="news-content">
      <div class="news-title">
          We've published our first article about cachai!
      </div>
      <div class="news-date">
          11 August 2025
      </div>
      <div class="news-summary">
          We are very happy to announce that <span class="bf-text">Cachai has its first published
          article</span>! It is now available in the <span class="it-text">Research Notes of the
          American Astronomical Society</span> (RNAAS) as an open-access publication. The article,
          by <span class="bf-text">Diego Beltrán</span> and <span class="bf-text">Dr. Maria Luiza L.
          Dantas</span>, introduces the Chord Diagram mo<span class="news-readmore">...read more</span>
      </div>
      </div>
      <div class="news-image">
      <img src="_static/news/RNAAS-cover-2018.jpg"
            alt="RNAAS cover of 2018">
      </div>
    </a>
    
    <a href="https://pypi.org/project/cachai/0.0.2/" class="news-version-card" target="_blank"
    rel="noopener noreferrer">
      <div class="news-content">
        <div class="news-title">
          <span class="news-version">v0.0.2</span> First stable release
        </div>
        <div class="news-date">
          5 August 2025
        </div>
        <div class="news-summary">
          This first release of the package includes the
          <span class="code-text">chplot.chord</span> module, which allows you to plot chord
          diagrams. It also includes modules for testing and accessing sample datasets.
        </div>
      </div>
    </a>

    <a href="#" class="news-card" data-news="chord-diagrams">
      <div class="news-content">
      <div class="news-title">
          Introducing the "Chord Diagrams"
      </div>
      <div class="news-date">
          5 August 2025
      </div>
      <div class="news-summary">
          While working on our astrophysics research, we wanted to use
          <span class="bf-text">chord diagrams</span> to visualize correlations between several physical
          parameters. However, we struggled to find a <span class="mono-text">Python</span> implementation
          that offered the level of customization we were used to with tools like
          <span class="mono-text">matplotlib</span></span><span class="news-readmore">...read more</span>
      </div>
      </div>
      <div class="news-image">
      <img src="_static/news/introducing_chords_chord.png"
            alt="Chord Diagram example">
      </div>
    </a>

   </div>


----------------------------------------------------------------------------------------------------

**More about cachai**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
From "*CACHAI’s first module: a fully customizable chord diagram for astronomy and beyond*" 
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