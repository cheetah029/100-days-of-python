# Runnability audit — 100-days-of-python (98 projects)

Date: 2026-10-04. Method: read docs/run.html, docs/build_manifest.py, docs/turtle_compat.py; pattern-scanned all 98 projects; manually reviewed every flagged file; verified Skulpt keyboard support directly in the skulpt-stdlib.js source.

**Result: 95 PASS, 3 FAIL.**

| slug | type | verdict | reason |
|---|---|---|---|
| Day-7-Hangman-1-Start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| Day-7-Hangman-2-Start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| Day-7-Hangman-3-Start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| Day-7-Hangman-4-Start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| Day-7-Hangman-5-Start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| NATO-alphabet-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| band-name-generator-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| blackjack-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| blind-auction-completed | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| blind-auction-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| caesar-cipher-1-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| caesar-cipher-2-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| caesar-cipher-3-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| caesar-cipher-4-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| calculator-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| coffee-machine-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-3-exercise-1 | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-4-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-printing-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-1-variables-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-10-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-10-end | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-10-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-12-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-13-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-13-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-13-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-13-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-18-3-start | turtle | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-18-4-start | turtle | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-18-5-start | turtle | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-2-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-2-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-2-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-2-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-26-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-26-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-26-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-26-3-test-your-code | console | PASS | False positive on scan: the script creates testing_copy.py itself via open("w") before importing it; the unittest harness with mocked input() runs in the Pyodide virtual FS. |
| day-26-4-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-26-5-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-4-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-5-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-5-test-your-code | console | PASS | False positive on scan: the script creates testing_copy.py itself; the unittest harness runs in the Pyodide virtual FS. |
| day-3-end-1 | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-multiple-if | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-3-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-30-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-30-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-4-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-4-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-4-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-4-list-practice | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-4-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-5-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-5-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-5-3-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-5-4-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-5-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-6-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-8-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-8-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-8-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-9-1-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-9-2-exercise | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-9-end | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| day-9-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| etch-a-sketch-start | turtle | PASS | Keyboard works: Skulpt turtle implements onkey/onkeypress via a real document keydown listener (verified in skulpt-stdlib.js source); arrow keys mapped. Note: canvas needs one click for keyboard focus (Skulpt behavior). |
| exercise-tracking-end | console | FAIL | main.py:10-11 os.environ["NT_APP_ID"]/["NT_API_KEY"] raises KeyError immediately; main.py:1 requests has no sockets in Pyodide, so the Nutritionix/Sheety POSTs cannot work. |
| flash-card-project-start | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| flight-club | console | FAIL | main.py:1,31 requests.post() to api.sheety.co — no network sockets in Pyodide; live submission would also send visitor emails to a third-party endpoint. |
| guess-the-number-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| higher-lower-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| hirst_painting-start | turtle | PASS | Runs in its assigned runner; no incompatible patterns found. |
| kanye-quotes-start | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| mail-merge-project-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| mile-to-kilo-converter | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| oop-coffee-machine-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| password-generator-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| password-manager-start | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| pomodoro-start | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| pong-game | turtle | PASS | Keyboard via Skulpt onkey (verified in Skulpt source); game loop yields at time.sleep() so Stop/Reset terminates it. |
| quiz-game-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| quizzler-app-start | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| rock-paper-scissors-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| snake-game | turtle | PASS | Same as pong-game: Skulpt onkey + sleep-yielding game loop. |
| tip-calculator-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| tkinter-widget-demo | tkinter | PASS | Runs in its assigned runner; no incompatible patterns found. |
| treasure-island-start | console | PASS | Runs in its assigned runner; no incompatible patterns found. |
| turtle-crossing-start | turtle | PASS | Same as pong-game: Skulpt onkey + sleep-yielding game loop. |
| turtle-race-start | turtle | PASS | screen.textinput is implemented by docs/turtle_compat.py via input(), which the turtle runner serves through a browser prompt dialog. |
| us-states-game-start | turtle | FAIL | main.py:2 import pandas — Skulpt (turtle runner) has no pandas and never installs packages; main.py:6-7 screen.addshape("blank_states_img.gif") — Skulpt cannot load GIF image shapes, so the map never renders. |

## Fixes for the 3 failures

### 1. exercise-tracking-end (console) — needs API keys + network
Fails at `os.environ["NT_APP_ID"]` (KeyError) before any network call; even past that, `requests.post` to Nutritionix/Sheety cannot work in Pyodide (no sockets). Minimal fix: add a per-slug shim in run.html that pre-populates `os.environ` with demo values and stubs `requests.post` to return a canned fake response, clearly labeled demo mode. Alternative: convert to a small web app with an exercise-name input and a local estimate table.

### 2. flight-club (console) — network signup form
`requests.post(USERS_ENDPOINT, ...)` submits the visitor's name/email to a Sheety endpoint — no sockets in Pyodide, and live submission would leak visitor data to a third party. Minimal fix: stub `requests.post` in the runner for this slug to return a fake 200 response (demo mode, no real submission), or replace with a web form that shows the confirmation message without sending anything.

### 3. us-states-game-start (turtle) — pandas + GIF map
Skulpt has no pandas and the turtle runner never installs packages, so `import pandas` raises; `screen.addshape("blank_states_img.gif")` cannot render in Skulpt, so the game is unplayable without the map. Minimal fix: build a web rewrite under docs/apps/us-states-game-start/index.html (like the 7 tkinter rewrites) — embed 50_states.csv coordinates as JSON, draw the map (blank_states_img.gif can be served as a static asset), prompt for state names, write correct guesses at their coordinates, and offer the states_to_learn.csv download.

## Notes

- `replit.clear` and `os.system("clear")` are stubbed by the console runner; `input()` uses prompt dialogs; `unittest` self-test harnesses (day-3-5, day-26-3) run fine in the virtual FS.
- pandas in the *console* runner works (NATO-alphabet-start): run.html calls `py.loadPackagesFromImports`, and pandas is an official Pyodide package. It does not work in the *turtle* (Skulpt) runner.
- Turtle game loops (`while game_is_on:` + `time.sleep`) are intentional: sleep yields to the runner, so Stop/Reset terminates them. Keyboard games need one click on the canvas for focus (Skulpt behavior).
- mile-to-kilo-converter web rewrite nit: Python uses `round(miles*1.609)` (integer); the web version shows 3 decimals. Cosmetic only.
