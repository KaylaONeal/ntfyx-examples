# Ntfyx — AI Agent Notifications & Phone Replies: examples

**Encrypted notifications from CLI tools and scripts. Questions from agents. Receive and reply on your iPhone, Android phone or a phone-authorized Web or Chrome Inbox.**

Ntfyx means **notify x to me**. Official website: https://ntfyx.me

## Availability

Signed CLI 0.5.0 is public for Windows x64/ARM64, macOS Apple silicon/Intel and Linux glibc x64/ARM64. The shell examples below require a POSIX shell. The Python walkthrough requires Python 3; its recorded end-to-end run used Linux x64. Ntfyx is available on the App Store and Google Play; use the Downloads page for current phone versions, platform requirements and store links. The encrypted Web Inbox is an optional receiver authorized by your primary phone. This repository contains MIT-licensed shell and Python usage examples, not the application's core source. Ntfyx uses a hosted relay and does not provide a supported self-hosting package.

For HTTPS notifications without the CLI, phone app 1.5.2 or later can prepare a short `sk_` sending link for MyNotify with the test body `hello`. The HTTPS service reads this request before encrypted delivery. See the [HTTPS guide](https://ntfyx.me/docs/http-push/) and [current app availability](https://ntfyx.me/download/).

## Install and pair

```sh
curl -fsSL https://ntfyx.me/install.sh | bash
ntfyx version --json
ntfyx connect
```

Choose an existing Topic, such as MyNotify, or create one within your allowance on the phone. Open Connect Topic and scan the computer's fresh QR. Only authorize a device you trust. The QR expires after five minutes; do not publish it. Use `ntfyx topics` to find your local CLI alias. Replace `Work` below with that alias.

Free includes one notification subscription and one custom Topic for your own tools. Connecting a Source or browser to an existing Topic does not create another Topic. See current [plans](https://ntfyx.me/pricing/) and [service limits](https://ntfyx.me/limits/) for shared message, device, storage and retention allowances.

## Examples

[`rich-message.json`](rich-message.json) demonstrates Markdown, callouts, metrics, tables, progress and native charts. It requires CLI 0.5.0+ and App 1.7.0+, Chrome 0.3.0+ or the updated Web Inbox. Store review and public availability are separate; check the [Downloads page](https://ntfyx.me/download/) for the version currently available before sending rich content.

```sh
# Local validation needs neither pairing nor MCP and makes no network request.
ntfyx validate-message --message-file rich-message.json --json
# Sending requires a paired Topic alias.
ntfyx send --message-file rich-message.json --topic Work --session-id report-1 --session-name "Build report" --priority normal --dedupe-key report-1
# The same JSON can arrive through stdin. This is an alternative to the file command.
cat rich-message.json | ntfyx send --message-stdin --topic Work --session-id report-1 --session-name "Build report" --priority normal --dedupe-key report-1
```

Use a new dedupe key for a new report; reuse the exact input, metadata and key after an uncertain send. The JSON contains only optional `title` / `summary` and required `content`; keep Topic, Session, priority and dedupe parameters on the command line. File and JSON-stdin inputs are mutually exclusive and cannot be combined with positional text, `--stdin`, `--format`, `--title` or `--summary`. No MCP installation is required. [Rich message guide](https://ntfyx.me/docs/rich-messages/).

Download or clone this repository, read the small scripts, then run from its root.

```sh
# Send a notification directly.
ntfyx send "Backup finished" --title "Backup" --topic Work

# Notify after a command exits, preserving its exit status.
bash scripts/notify-after.sh Work bash -c 'printf "Example job finished\n"'

# Notify after a noninteractive Claude Code query exits.
# Requires your own Claude Code installation, authentication and permitted usage.
bash scripts/notify-after.sh Work claude -p "Explain this project's README without changing files."

# Ask for a reply; only Allow continues this harmless demonstration.
bash scripts/approval-demo.sh Work
```

### A complete reply workflow

[Agent reply walkthrough](https://ntfyx.me/docs/agent-reply-walkthrough/) ([中文](https://ntfyx.me/zh/docs/agent-reply-walkthrough/)) uses one Session for a status message, a Continue/Stop choice and a text question. Inspect the script first, then use your paired Topic alias:

```sh
python3 scripts/agent-reply-walkthrough.py Work
```

Requires Python 3 and the signed CLI 0.1.4 or later. The script checks the structured answer and one-time claim before continuing. It prints a fixed demonstration result; it never runs the text returned from the phone as a command. Stop, expiry and unavailable answers stop the workflow. A claimed step is not automatically retried after an unknown result. The walkthrough was rerun on 24 October 2026 with the published CLI 0.4.1 and the real staging API. Continue, Stop, Deny and timeout passed, and each temporary Inbox was deleted. The verification used a programmatic receiver; it does not claim a physical-phone test or native agent permission-hook coverage.

For a first HTTPS notification without a computer, follow the [phone hello walkthrough](https://ntfyx.me/docs/https-push-walkthrough/) ([中文](https://ntfyx.me/zh/docs/https-push-walkthrough/)). HTTPS ingress reads the submitted content before encrypting delivery; the CLI workflow encrypts messages and replies at its endpoints.

`notify-after.sh` sends only a fixed status summary, not command arguments, prompts, stdout or stderr. Job output stays in the original terminal. A failed notification prints a warning and preserves the job's exit status. A zero Claude process exit is not proof that a model's answer is correct. This wrapper reports process completion; it is not an interactive per-turn hook.

`approval-demo.sh` uses synchronous `ntfyx ask --allow-deny`, which verifies the answer and acquires a one-time claim before returning success. Deny, an unanswered wait, transport failure and an already-consumed request do not continue. The only permitted demo step prints a line. It never deploys, transfers money, or runs a user-supplied command. Do not use the exit status of a read-only `ntfyx result` as authorization. Real external actions need their own idempotency and crash recovery; do not automatically rerun an uncertain action.

## Guides

- [AI agent notification and reply tools](https://ntfyx.me/docs/agent-notifications/) ([中文：Agent 通知工具](https://ntfyx.me/zh/docs/agent-notifications/))
- [Compare phone alerts, replies and remote-session tools](https://ntfyx.me/docs/coding-agents-on-your-phone/)

- [Claude Code completion notifications](https://ntfyx.me/docs/claude-code-notifications/)
- [Codex phone approvals and hook trust](https://ntfyx.me/docs/codex-phone-approval/)
- [Codex usage and reset-credit alerts](https://ntfyx.me/docs/codex-usage-alerts/)
- [Compare Ntfyx, ntfy, Pushover and Bark](https://ntfyx.me/docs/notification-tools/)
- [Shell script notifications](https://ntfyx.me/docs/notifications/)
- [Wait for a phone approval](https://ntfyx.me/docs/phone-approval/)
- [Web Inbox](https://ntfyx.me/docs/web/)
- [Agent and local MCP configuration](https://ntfyx.me/docs/agents/)
- [中文使用说明](https://ntfyx.me/zh/docs/)
- [FAQ](https://ntfyx.me/docs/faq/)

## What encryption protects

For CLI and agent messages, clients encrypt titles, bodies, choices and replies before sending them. Each receiver gets its own encrypted copy. The service processes ciphertext plus operational metadata such as routing IDs, time, size and notification tokens. A newly authorized browser cannot read earlier phone history. Revocation cannot erase already-delivered content.

End-to-end encryption does not protect a compromised endpoint or conceal all metadata. Independent security review is not complete. Purchase restoration does not restore encryption keys. Read the [security model](https://ntfyx.me/security/) and [privacy notice](https://ntfyx.me/privacy/).

## Verification

The examples are exercised using the compiled CLI, an isolated local encrypted relay, programmatic phone authorization and signed browser replies. Cases cover a successful job, failed job, unchanged command arguments, notification failure, Allow, Deny, timeout, transport failure and repeat claim rejection. Published screenshots show that local Web test with synthetic messages; they are not an iPhone/APNs acceptance claim or a Claude-generated output.

The separately tested native Claude Code permission adapter has a documented version and mode boundary. Local stdio MCP does not mean Ntfyx is listed in the ChatGPT or Claude cloud app directory. See the agent guide for supported configurations.

## Scheduling and backups

The [script notification guide](https://ntfyx.me/docs/notifications/) includes a small temporary archive example, a Linux user-crontab template with explicit PATH and local logging, and a job/notification failure table. Pair and run under the same user. Try the exact command manually before scheduling. A successful archive is not a restore test, and this wrapper cannot report a job that never started or was killed before notification.

## Native approvals versus completion alerts

The wrapper above reports process exit on macOS/Linux. The native adapters have a narrower scope: as checked on 30 September 2026, Linux x64 Claude Code 2.1.283 / 2.1.284 non-interactive Bash, Edit and Write, and Codex 0.158.0 interactive Bash and apply_patch. These real-host checks used a programmatic receiver, not a physical iPhone. Apple silicon Mac native approvals were separately verified with Claude Code 2.1.303 and Codex 0.163.0 (CLI 0.1.5+). Intel Mac and Windows native permission approvals remain in the terminal; Windows CLI/local MCP questions are supported. Codex requires the person's `/hooks` trust, and `codex exec` does not trigger its permission hook. Use either the plugin or `ntfyx setup` for an agent to avoid duplicate hooks. Retain the agent's local sandbox and policy.

CLI release notes and signed downloads: https://ntfyx.me/changelog/ and https://ntfyx.me/download/

Support: https://ntfyx.me/support/ · Never include keys, pairing links, recovery codes or private messages in a public issue.

## When the agent needs a choice or missing information

```sh
# Harmless demos: verified replies only; no external action or shell evaluation.
bash scripts/input-demo.sh Work choice
bash scripts/input-demo.sh Work text
```

The agent or script must explicitly call `ask` or the local MCP tool. Ntfyx does not automatically forward every terminal prompt. Native permission approvals use supported host hooks and have a separate platform/version matrix.

- [Agent waiting for input](https://ntfyx.me/docs/agent-waiting-for-input/)
- [Multiple projects and agents](https://ntfyx.me/docs/multiple-agent-notifications/)
- [SSH and server jobs](https://ntfyx.me/docs/ssh-job-notifications/)
