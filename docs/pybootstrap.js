/*
 * Python-side setup, shared by the worker and the main-thread fallback.
 *
 * The host supplies two hooks on the global object before this runs:
 *   pyInput(promptText) -> the line the user typed, or null for EOF/cancel.
 *                          The HOST echoes the line; Python must not print it.
 *   pyClear()           -> wipe the terminal.
 *
 * Careful: this is a String.raw template, so a backtick anywhere in the Python
 * below - comments included - would end the literal and break the whole script.
 */
self.BOOTSTRAP_PY = String.raw`
import builtins, os, sys, types, shutil, js

def _clear_screen(*_a, **_k):
    js.pyClear()

def _web_input(prompt=""):
    text = "" if prompt is None else str(prompt)
    if text:
        sys.stdout.write(text)
        sys.stdout.flush()
    v = js.pyInput(text)
    if v is None:
        raise EOFError("input cancelled by user")
    return str(v)
builtins.input = _web_input

_replit = types.ModuleType("replit")
_replit.clear = _clear_screen
sys.modules["replit"] = _replit

_real_system = os.system
def _system(cmd):
    if str(cmd).strip() in ("clear", "cls"):
        _clear_screen()
        return 0
    return 0
os.system = _system

PROJECT_DIR = "/home/pyodide/project"

def _prepare_run():
    """Fresh project dir + forget modules imported from a previous run."""
    os.chdir("/home/pyodide")
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None) or ""
        if f.startswith(PROJECT_DIR + "/"):
            del sys.modules[name]
    shutil.rmtree(PROJECT_DIR, ignore_errors=True)
    os.makedirs(PROJECT_DIR)
    os.chdir(PROJECT_DIR)
    if PROJECT_DIR not in sys.path:
        sys.path.insert(0, PROJECT_DIR)

# Demo shims for projects that need API keys / network access.
# exercise-tracking-end reads Nutritionix/Sheety credentials from the environment
# and flight-club POSTs signups to a Sheety endpoint; neither can work in the
# browser (no secrets here, no sockets in Pyodide), so both run in demo mode:
# harmless placeholder credentials plus a fake "requests" that never sends.
_RUN_SLUG = globals().get("__run_slug", "")
if _RUN_SLUG in ("exercise-tracking-end", "flight-club"):
    os.environ.setdefault("NT_APP_ID", "demo-app-id")
    os.environ.setdefault("NT_API_KEY", "demo-api-key")
    os.environ.setdefault("SHEET_API_ENDPOINT", "https://example.invalid/demo-sheet")
    os.environ.setdefault("TOKEN", "demo-token")

    class _DemoResponse:
        status_code = 200
        text = '{"ok": true}  (demo mode - nothing was actually sent)'
        def json(self):
            return {"exercises": [
                {"name": "running", "duration_min": 30, "nf_calories": 300},
                {"name": "cycling", "duration_min": 45, "nf_calories": 400},
            ]}

    def _demo_post(url, json=None, headers=None, **kwargs):
        print(f"[demo mode] POST {url} - not actually sent.")
        return _DemoResponse()

    _requests_stub = types.ModuleType("requests")
    _requests_stub.post = _demo_post
    _requests_stub.get = _demo_post
    sys.modules["requests"] = _requests_stub
    print(f"[demo mode] {_RUN_SLUG}: API calls are simulated; nothing leaves your browser.")
`;
