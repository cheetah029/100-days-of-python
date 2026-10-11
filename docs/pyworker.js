/*
 * Runs a project's Python in a worker.
 *
 * The point of the worker is input(): Python is synchronous, so input() has to
 * block. On the main thread that would freeze the page and the user could never
 * type anything. Here the worker parks on Atomics.wait while the page stays live,
 * collects the line, and wakes us up.
 *
 * Shared memory layout (one SharedArrayBuffer):
 *   Int32Array  ctl[0]  state: 0 = waiting, 1 = line ready, 2 = EOF/stopped
 *   Int32Array  ctl[1]  byte length of the line
 *   Uint8Array  data    the UTF-8 line, from byte offset CTL_BYTES
 */

const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
const PROJECT_DIR = "/home/pyodide/project";

const CTL_BYTES = 8;
const WAITING = 0, READY = 1, EOF = 2;

let pyodide = null;
let ctl = null;          // Int32Array view
let data = null;         // Uint8Array view
let slug = "";

const lineDec = new TextDecoder();
const outDec = new TextDecoder();
const errDec = new TextDecoder();

function post(msg) { self.postMessage(msg); }

/*
 * Blocks the worker until the page posts a line back. Only this thread parks -
 * the page keeps handling keystrokes, which is the whole reason Python moved here.
 */
function readLine(promptText) {
  Atomics.store(ctl, 0, WAITING);
  post({ type: "input", prompt: String(promptText == null ? "" : promptText) });
  // If the page somehow answered first, Atomics.wait returns "not-equal" at once.
  Atomics.wait(ctl, 0, WAITING);
  if (Atomics.load(ctl, 0) === EOF) return null;
  const len = Atomics.load(ctl, 1);
  // TextDecoder rejects views onto shared memory, so copy the bytes out first.
  return lineDec.decode(new Uint8Array(data.subarray(0, len)));
}

// Hooks that pybootstrap.js expects on the global object.
self.pyInput = readLine;
self.pyClear = () => post({ type: "clear" });

async function ensurePyodide() {
  if (pyodide) return pyodide;
  post({ type: "status", text: "Loading Python…" });
  importScripts(PYODIDE_URL);
  pyodide = await loadPyodide();
  // Stream raw chunks so partial lines (e.g. input prompts) show immediately and
  // newlines are preserved ("batched" mode strips them).
  pyodide.setStdout({
    write: (buf) => { post({ type: "out", text: outDec.decode(buf, { stream: true }) }); return buf.length; }
  });
  pyodide.setStderr({
    write: (buf) => { post({ type: "out", text: errDec.decode(buf, { stream: true }), cls: "err" }); return buf.length; }
  });
  pyodide.globals.set("__run_slug", slug);
  importScripts("pybootstrap.js");
  await pyodide.runPythonAsync(self.BOOTSTRAP_PY);
  return pyodide;
}

async function run(files, entry) {
  const py = await ensurePyodide();
  post({ type: "status", text: "Running…" });
  py.runPython("_prepare_run()");

  // Write every project file into the virtual FS so imports + data files work.
  for (const [name, content] of Object.entries(files)) {
    const parts = name.split("/");
    let dir = PROJECT_DIR;
    for (let i = 0; i < parts.length - 1; i++) {
      dir += "/" + parts[i];
      try { py.FS.mkdir(dir); } catch (e) { /* exists */ }
    }
    py.FS.writeFile(PROJECT_DIR + "/" + name, content);
  }

  const code = files[entry] || Object.values(files)[0];
  // Install any Pyodide-provided packages the project imports (pandas, etc.).
  const allSrc = Object.entries(files).filter(([n]) => n.endsWith(".py")).map(([, c]) => c);
  try { await py.loadPackagesFromImports(allSrc.join("\n")); } catch (e) { /* best effort */ }

  // Fresh globals each run, and behave like `python main.py`.
  const globals = py.globals.get("dict")();
  globals.set("__name__", "__main__");
  globals.set("__file__", PROJECT_DIR + "/" + entry);
  try {
    await py.runPythonAsync(code, { globals });
  } finally {
    globals.destroy();
  }
}

self.onmessage = async (event) => {
  const msg = event.data || {};

  if (msg.type === "init") {
    ctl = new Int32Array(msg.sab, 0, 2);
    data = new Uint8Array(msg.sab, CTL_BYTES);
    slug = msg.slug || "";
    post({ type: "ready" });
    return;
  }

  if (msg.type === "run") {
    try {
      await run(msg.files, msg.entry);
      post({ type: "done" });
    } catch (e) {
      // EOFError here means Stop was pressed while input() was waiting.
      const text = String(e && e.message ? e.message : e);
      post({ type: "error", message: text });
    }
  }
};
