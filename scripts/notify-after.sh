#!/usr/bin/env bash
# Ntfyx CLI 0.1.1+. Usage: bash notify-after.sh TOPIC COMMAND [ARG...]
# TOPIC is an existing local CLI alias. No command output or arguments are sent.
set -u
if [ "$#" -lt 2 ]; then
  printf 'Usage: bash notify-after.sh TOPIC COMMAND [ARG...]\n' >&2
  exit 2
fi
ntfyx_topic="$1"
shift
"$@"
ntfyx_job_status=$?
if [ "$ntfyx_job_status" -eq 0 ]; then
  ntfyx_title='Task finished'
else
  ntfyx_title='Task failed'
fi
if ! ntfyx send "Task exited with status ${ntfyx_job_status}. Check the original terminal for details." --title "$ntfyx_title" --topic "$ntfyx_topic" >/dev/null; then
  printf 'Ntfyx notification was not confirmed. Check the connection; job exit status is preserved.\n' >&2
fi
exit "$ntfyx_job_status"
