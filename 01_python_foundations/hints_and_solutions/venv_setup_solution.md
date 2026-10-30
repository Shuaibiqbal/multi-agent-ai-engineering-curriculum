# Basic (venv, start to finish) — Solution

> [Back to the exercise](../README.md#ex-venv_setup) · [Hint 1](venv_setup_hints.md#hint-1) · [Hint 2](venv_setup_hints.md#hint-2) · [Solution](venv_setup_solution.md)

**Where this exercise is saved:** `practice/venv_setup_practice.md` — notes, not a script. Every block below is a terminal command, so there is nothing to `python`-run: keep a Markdown file with each command you ran and the output you got back, and you will have your own record of the sequence the next time you start a project.

**Story — `venv_setup_practice.md`:** every later document installs packages into a project, so a virtual environment — an isolated, per-project Python with its own installed packages, kept separate from the system Python — has to be second nature before any real code exists. Writing the steps down once (create, activate, install, freeze), with what each one prints, makes it something you can repeat without thinking. **If not:** the first import error in a later document would send you guessing about which Python and which packages you're actually using.

## Solution

**Story:** the same four steps, but with Windows' different activate command (`.venv\Scripts\activate` instead of `source .venv/bin/activate`) — so the notes work on any teammate's machine, not just yours. **If not:** a Windows teammate would get stuck on the very first step.

macOS / Linux:
```bash
# → practice/venv_setup_practice.md
python -m venv .venv
source .venv/bin/activate
pip install requests
pip freeze > requirements.txt
```

Windows (PowerShell):
```powershell
# → practice/venv_setup_practice.md
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install requests
pip freeze > requirements.txt
```
**Expected output**, either platform, after `pip freeze > requirements.txt`: no console output (it's redirected into the file). Open `requirements.txt` to see the same 5 lines shown above.
