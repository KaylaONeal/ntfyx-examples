#!/usr/bin/env python3
"""A harmless, explicit question/reply workflow. Requires Python 3 and Ntfyx CLI.

Run only after pairing the CLI to a Topic you own. Input is printed as JSON;
it is never evaluated as a command. No deployment or other external action runs.
"""
import argparse
import json
import secrets
import subprocess
import sys


class Stopped(Exception):
    def __init__(self, code, reason):
        self.code, self.reason = code, reason


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="An existing paired CLI Topic alias")
    parser.add_argument("--wait", default="60s")
    parser.add_argument("--expires", default="90s")
    parser.add_argument("--cli", default="ntfyx", help="CLI executable; normally ntfyx on PATH")
    parser.add_argument("--config", help="Optional existing private CLI credential file")
    args = parser.parse_args()
    session = "reply-demo-" + secrets.token_urlsafe(16)
    common = ["--topic", args.topic, "--session-id", session,
              "--session-name", "A harmless reply walkthrough", "--json"]

    def call(arguments, session_flags=True):
        command = [args.cli, *arguments, *(common if session_flags else [])]
        if args.config:
            command += ["--config", args.config]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
        except OSError:
            raise Stopped(20, "CLI could not be started") from None
        if result.returncode:
            raise Stopped(result.returncode if result.returncode > 0 else 130,
                          "CLI did not return an authorized successful result")
        try:
            value = json.loads(result.stdout)
        except (ValueError, TypeError):
            raise Stopped(24, "CLI returned an invalid JSON result") from None
        if not isinstance(value, dict):
            raise Stopped(24, "CLI returned an invalid JSON result")
        return value

    def ask(question, kind, *options):
        value = call(["ask", question, *options, "--wait", args.wait,
                      "--expires", args.expires])
        if (value.get("status") != "answered"
                or value.get("consumption", {}).get("claim_acquired") is not True
                or value.get("response", {}).get("type") != kind):
            raise Stopped(24, "No matching answered result with a one-time claim")
        return value["response"]

    print("Session: " + session, flush=True)
    call(["send", "A synthetic note is ready. No external operation has run.",
          "--title", "Reply walkthrough: start"])
    print("Notification accepted; this alone is not a received-message or approval claim.", flush=True)
    choice = ask("Should this demo prepare a local summary?", "choice",
                 "--choice", "continue=Prepare the demo summary", "--choice", "stop=Stop this demo")
    if choice.get("choice_id") == "stop":
        print("Stopped by your choice. No demo summary was printed.", flush=True)
        return 0
    if choice.get("choice_id") != "continue":
        raise Stopped(24, "Unexpected choice; nothing continued")
    print("Verified and claimed the continue choice.", flush=True)
    note = ask("What short synthetic note should the local summary include? Do not enter secrets.",
               "text", "--text").get("text")
    if not isinstance(note, str) or not note.strip():
        raise Stopped(24, "No valid text reply; nothing continued")
    print("Verified and claimed the text reply.", flush=True)
    decision = ask("Print this local demo summary? No command or external operation will run.",
                   "confirm", "--allow-deny")
    if decision.get("value") != "allow":
        raise Stopped(10, "The final decision did not allow the demo")
    print("Verified and claimed the final Allow.", flush=True)
    # JSON escaping prevents reply text from becoming terminal control syntax.
    print("Demo summary: " + json.dumps({"note": note, "external_action": False}, ensure_ascii=True), flush=True)
    call(["send", "The local demo summary was printed. No external operation ran.",
          "--title", "Reply walkthrough: completed"])
    print("Completion notification accepted. This demonstration is finished.", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Stopped as error:
        print("Stopped: " + error.reason + " (exit " + str(error.code) + ").", file=sys.stderr)
        print("No automatic retry. Inspect an uncertain result before starting another run.", file=sys.stderr)
        sys.exit(error.code)
