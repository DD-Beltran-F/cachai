// Customize Parameters-like docstring sections
document.addEventListener("DOMContentLoaded", () => {
  const keywords = ["Parameters", "Other Parameters", "Other Methods",
                    "Attributes", "Other Attributes"];
  document.querySelectorAll("dl > dt").forEach(dt => {
    const title = dt.textContent.trim();
    if (keywords.includes(title)) {
      const dd = dt.nextElementSibling;
      if (dd) {
        const innerDl = dd.querySelector("dl");
        if (innerDl && !innerDl.classList.contains("simple")) {
          innerDl.classList.add("simple");
        }
      }
    }
  });
});

// Customize "Returns" docstring sections
document.addEventListener("DOMContentLoaded", () => {
  const highlightKeywords = ["Returns"];
  document.querySelectorAll("dl > dt").forEach(dt => {
    const title = dt.textContent.trim();
    if (highlightKeywords.includes(title)) {
      dt.classList.add("highlight-dt");
    }
  });
});

$(document).ready(function () {
    $('a.external').attr('target', '_blank');
});

// Add cross-reference to non-indexed definitions in modules summary
document.addEventListener("DOMContentLoaded", function () {
  // Process every autosummary table inside a section
  document.querySelectorAll("section table.autosummary").forEach(function (table) {
    let section = table.closest("section");
    if (!section) return;

    // Try to find a nearby/global <a> that already links to the page generated for "name"
    function findExistingHrefFor(name) {
      // 1) Search in the same section
      let sel = 'a[href$="' + name + '.html"], a[href*="/' + name + '.html"]';
      let a = section.querySelector(sel);
      if (a) return a.getAttribute("href");

      // 2) Seacrh globally but prefer refs inside "generated/"
      a = document.querySelector('a[href*="generated/"][href$="' + name + '.html"]');
      if (a) return a.getAttribute("href");

      // 3) Any ref that end with "name.html"
      a = document.querySelector('a[href$="' + name + '.html"]');
      if (a) return a.getAttribute("href");

      return null;
    }

    // Get a moduleName from the section id (fallback)
    function deriveModuleNameFromSectionId(id) {
      if (!id) return "";
      // If it contains "cachai" use it as base and convert "-" to "."
      if (id.indexOf("cachai") !== -1) {
        let s = id.replace(/-/g, ".").replace(/(?:cachai\.){2,}/g, "cachai.");
        // Slice until the first "cachai"
        let idx = s.indexOf("cachai");
        if (idx > 0) s = s.slice(idx);
        return s.replace(/^\.+|\.+$/g, "");
      }
      // If it doesn't contains "cachai", just convert "-" to "."
      return id.replace(/-/g, ".");
    }

    // Replace each <code> with <a> linking to the generated page
    table.querySelectorAll("code.xref.py.py-obj").forEach(function (el) {
      let funcName = el.textContent.trim();
      if (!funcName) return;

      // 1) Try to re-use an existing ref (best result)
      let href = findExistingHrefFor(funcName);

      // 2) If it doesn't exists, construct it from section.id (with fallback to "cachai")
      if (!href) {
        let moduleName = deriveModuleNameFromSectionId(section.id || "");
        // If the result is poor, use "cachai" by default
        if (!moduleName || moduleName === "testing") moduleName = "cachai";
        href = "generated/" + moduleName + "." + funcName + ".html";
      }

      // Constuct node <a><code><span class="pre">func</span></code></a>
      let span = document.createElement("span");
      span.setAttribute("class", "pre");
      span.textContent = funcName;

      let code = document.createElement("code");
      code.setAttribute("class", "xref py py-obj docutils literal notranslate");
      code.appendChild(span);

      let a = document.createElement("a");
      a.setAttribute("class", "reference internal");
      a.setAttribute("href", href);
      // Title: calculate from the href
      let title = href.replace(/^.*generated\//, "").replace(/\.html$/, "").replace(/\//g, ".");
      a.setAttribute("title", title);
      a.appendChild(code);

      el.replaceWith(a);
    });
  });
});


// Section banner scroll animation
document.addEventListener("scroll", function() {
  const banner = document.querySelector(".section-banner");
  if (!banner) return;

  if (window.scrollY > 50) {
    banner.classList.add("shrink");
  } else {
    banner.classList.remove("shrink");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // Remove "<class>." in methods signatures
  document.querySelectorAll("dt.sig span.sig-prename.descclassname").forEach(el => {
    el.remove();
  });

  // Remove all the empty <dl class="field-list simple">
  document.querySelectorAll("dl.field-list.simple").forEach(dl => {
    if (!dl.textContent.trim()) {
      dl.remove();
    }
  });
});