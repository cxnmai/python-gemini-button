# Python Gemini Button Demo

Minimal Python UI app with one button.

When clicked, it sends this prompt through your local Conduit agent:

- `hi how are you doing`

and shows the returned text.

## Requirements

- Python 3.9+
- `requests`
- Local Conduit server running (`http://localhost:8080`)

Install dependency:

```bash
pip install requests
```

## Run

```bash
cd apps/python-gemini-button
python app.py
```

## Build a concise executable

Use PyInstaller onefile mode to generate a single executable:

```bash
python -m pyinstaller --onefile --name python-gemini-button app.py
```

Output artifact:

- Linux/macOS: `dist/python-gemini-button`
- Windows: `dist/python-gemini-button.exe`

Conduit publish build command for this app:

```text
python -m pyinstaller --onefile --name python-gemini-button app.py
```

The app uses `sdk/python/conduit_sdk` and will auto-start the Rust `agent` if needed.
It also starts the agent pointed at Conduit API automatically (default: `https://conduit-urcy.onrender.com`).

## Environment variables (optional)

- `AGENT_BASE_URL` (default `http://127.0.0.1:54111`)
- `AGENT_APP_TOKEN` (default `dev-local-token`)
- `CONDUIT_BASE_URL` (default `https://conduit-urcy.onrender.com`)
- `CONDUIT_APP_ID` (default `python-gemini-button`)
- `CONDUIT_PROVIDER` (default `gemini`)
- `CONDUIT_MODEL` (default `models/gemini-2.5-flash`)

## Notes

- If not authenticated yet, first click will show device-code instructions.
- Approve that code in your web app, then click the button again.
- Ensure app id exists on server (admin bootstrap or create app endpoint).
