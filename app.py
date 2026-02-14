import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

REPO_ROOT = Path(__file__).resolve().parents[2]
SDK_PATH = REPO_ROOT / "sdk" / "python"
sys.path.insert(0, str(SDK_PATH))

from conduit_sdk import AgentProcess, ConduitClient, ConduitError  # noqa: E402


AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "http://127.0.0.1:54111").rstrip("/")
AGENT_APP_TOKEN = os.getenv("AGENT_APP_TOKEN", "dev-local-token")
CONDUIT_BASE_URL = os.getenv("CONDUIT_BASE_URL", "https://conduit-urcy.onrender.com").rstrip("/")

APP_ID = os.getenv("CONDUIT_APP_ID", "python-gemini-button")
PROVIDER = os.getenv("CONDUIT_PROVIDER", "gemini")
MODEL = os.getenv("CONDUIT_MODEL", "models/gemini-2.5-flash")

AGENT = AgentProcess(
    repo_root=str(REPO_ROOT),
    agent_base_url=AGENT_BASE_URL,
    conduit_base_url=CONDUIT_BASE_URL,
)
CLIENT = ConduitClient(
    agent_base_url=AGENT_BASE_URL,
    agent_app_token=AGENT_APP_TOKEN,
    app_id=APP_ID,
    provider=PROVIDER,
    model=MODEL,
)


def ensure_authenticated():
    auth = CLIENT.ensure_auth(force_new_login=False)
    if auth.get("authenticated"):
        return None

    user_code = auth.get("user_code") or "unknown"
    verification_url = auth.get("verification_url") or "unknown"
    if auth.get("state") == "pending":
        return (
            "Authentication required before chat.\n\n"
            f"User code: {user_code}\n"
            f"Open this URL and approve: {verification_url}\n\n"
            "Approval is still pending. After approval, click the button again."
        )

    return (
        "Authentication required before chat.\n\n"
        f"User code: {user_code}\n"
        f"Open this URL and approve: {verification_url}\n\n"
        "After approval, click the button again."
    )


def ask_gemini():
    result = CLIENT.ask("hi how are you doing", max_tokens=128, temperature=0.2)
    return result["content"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gemini Button Demo")
        self.geometry("700x420")

        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        self.button = ttk.Button(frame, text="Ask Gemini", command=self.on_click)
        self.button.pack(anchor=tk.W)

        self.status_var = tk.StringVar(value="Ready")
        self.status = ttk.Label(frame, textvariable=self.status_var)
        self.status.pack(anchor=tk.W, pady=(10, 8))

        self.output = tk.Text(frame, wrap=tk.WORD, height=18)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.insert(
            tk.END,
            "Click 'Ask Gemini'.\n"
            "If not authenticated, the app will show the device-code approval instructions.\n",
        )

    def set_output(self, text: str):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def on_click(self):
        self.button.config(state=tk.DISABLED)
        self.status_var.set("Calling Conduit agent...")

        def worker():
            try:
                auth_message = ensure_authenticated()
                if auth_message:
                    self.after(0, lambda: self.set_output(auth_message))
                    self.after(0, lambda: self.status_var.set("Waiting for authentication"))
                    return

                answer = ask_gemini()
                self.after(0, lambda: self.set_output(answer))
                self.after(0, lambda: self.status_var.set("Done"))
            except ConduitError as exc:
                self.after(0, lambda: self.set_output(f"Error:\n\n{exc}"))
                self.after(0, lambda: self.status_var.set("Error"))
            except Exception as exc:
                self.after(0, lambda: self.set_output(f"Error:\n\n{exc}"))
                self.after(0, lambda: self.status_var.set("Error"))
            finally:
                self.after(0, lambda: self.button.config(state=tk.NORMAL))

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    AGENT.start_if_needed()
    app = App()

    def on_close():
        AGENT.stop()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
