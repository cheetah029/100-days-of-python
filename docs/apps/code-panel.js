/*
 * Shows a project's Python source underneath a web app.
 *
 * run.html redirects projects that have a hand-written web version straight to
 * apps/<slug>/, so those projects never showed their code the way every other
 * project does. This rebuilds the same Code panel - file tabs plus a source
 * view - from the data files run.html already uses.
 *
 * Include it from an app page with the slug it belongs to:
 *   <script src="../code-panel.js" data-slug="pomodoro-start"></script>
 */
(function () {
  const script = document.currentScript;
  const slug = script && script.dataset.slug;
  if (!slug) return;

  const base = "../../";

  function build(meta, files) {
    const names = Object.keys(files).sort((a, b) => {
      // entry file first, then the rest alphabetically
      if (meta && a === meta.entry) return -1;
      if (meta && b === meta.entry) return 1;
      return a.localeCompare(b);
    });
    if (!names.length) return;

    const panel = document.createElement("div");
    panel.className = "panel code-panel";

    const heading = document.createElement("h2");
    heading.textContent = "Code";
    panel.appendChild(heading);

    const note = document.createElement("p");
    note.className = "status";
    note.style.marginTop = "0";
    note.textContent =
      "The original Python (tkinter) this web version is based on - " +
      names.length + (names.length === 1 ? " file." : " files.");
    panel.appendChild(note);

    const tabs = document.createElement("div");
    tabs.className = "file-tabs";
    panel.appendChild(tabs);

    const view = document.createElement("div");
    view.className = "code-view";
    panel.appendChild(view);

    const link = document.createElement("p");
    link.className = "status";
    const a = document.createElement("a");
    const srcPath = (meta && meta.src) || (slug + "/" + ((meta && meta.entry) || names[0]));
    a.href = "https://github.com/cheetah029/100-days-of-python/blob/main/projects/" +
             srcPath.split("/").map(encodeURIComponent).join("/");
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = "View this project on GitHub";
    a.style.overflowWrap = "anywhere";
    link.appendChild(a);
    panel.appendChild(link);

    function show(name) {
      tabs.querySelectorAll("button").forEach((b) =>
        b.classList.toggle("active", b.dataset.name === name));
      view.textContent = files[name];
    }
    for (const name of names) {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = name;
      b.dataset.name = name;
      b.onclick = () => show(name);
      tabs.appendChild(b);
    }
    show(names[0]);

    const wrap = document.querySelector(".wrap") || document.body;
    // Sit above the trailing spacer the app pages end with, if there is one.
    const spacer = wrap.querySelector(":scope > div[style*='height']");
    wrap.insertBefore(panel, spacer || null);
  }

  async function load() {
    try {
      const [projectRes, manifestRes] = await Promise.all([
        fetch(base + "data/" + encodeURIComponent(slug) + ".json"),
        fetch(base + "data/manifest.json")
      ]);
      if (!projectRes.ok) return;
      const project = await projectRes.json();
      let meta = null;
      if (manifestRes.ok) {
        const manifest = await manifestRes.json();
        meta = manifest.find((p) => p.slug === slug) || null;
      }
      if (project && project.files) build(meta, project.files);
    } catch (e) {
      /* no code panel is better than a broken app page */
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load, { once: true });
  } else {
    load();
  }
})();
