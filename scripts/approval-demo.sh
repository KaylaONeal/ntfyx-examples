#!/usr/bin/env bash
# Harmless demo: a verified, claimed Allow prints a line; no external action.
# Usage: bash approval-demo.sh TOPIC [WAIT, default 60s]
set -u
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  printf 'Usage: bash approval-demo.sh TOPIC [WAIT]\n' >&2
  exit 2
fi
if ntfyx ask 'Continue the demo?' --title 'Review the demo step' --allow-deny --topic "$1" --wait "${2:-60s}" --expires 90s --json; then
  printf 'Approved: demo step only. No deployment or external action ran.\n'
else
  ntfyx_reply_status=$?
  printf 'Stopped: no demo step ran (Ntfyx exit %s).\n' "$ntfyx_reply_status" >&2
  exit "$ntfyx_reply_status"
fi
