#!/usr/bin/env bash
# A verified choice/text reply completes a harmless demo. Never execute reply text.
# Usage: bash input-demo.sh TOPIC choice|text [WAIT, default 60s]
set -u
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  printf 'Usage: bash input-demo.sh TOPIC choice|text [WAIT]\n' >&2
  exit 2
fi
case "$2" in
  choice) question='Which environment should I check?'; mode=(--choice staging=Staging --choice production=Production) ;;
  text) question='What should I check next?'; mode=(--text) ;;
  *) printf 'Mode must be choice or text.\n' >&2; exit 2 ;;
esac
if ntfyx ask "$question" "${mode[@]}" --topic "$1" --wait "${3:-60s}" --expires 90s --json; then
  printf 'Verified input received. Demo complete; no external action ran.\n'
else
  ntfyx_reply_status=$?
  printf 'Stopped: no verified input (Ntfyx exit %s).\n' "$ntfyx_reply_status" >&2
  exit "$ntfyx_reply_status"
fi
