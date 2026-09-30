# Ntfyx examples

**Encrypted notifications from CLI tools and scripts. Questions from agents. Receive and reply on your iPhone or a phone-authorized Web Inbox.**

Ntfyx means **notify x to me**. Official website: https://ntfyx.me

## Availability

The signed CLI 0.1.1 is available for macOS and Linux. The hosted Web Inbox and encrypted API are online. The iPhone app is awaiting App Store review; a compatible iPhone build is needed to pair. There is no announced public App Store download or Android app. This repository contains usage examples, not the application's source code.

## Install and pair

```sh
curl -fsSL https://ntfyx.me/install.sh | bash
ntfyx version --json
ntfyx connect
```

Create a named Topic on the iPhone, open Connect Topic and scan the computer's fresh QR. Only authorize a device you trust. The QR expires after five minutes; do not publish it. Use `ntfyx topics` to find your local CLI alias. Replace `Work` below with that alias.

Free includes one active Topic. Ntfyx Plus supports up to twenty active Topics. Connecting a Source or browser to an existing Topic does not create another Topic. Other limits remain shared: https://ntfyx.me/limits/

## Examples

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

`notify-after.sh` sends only a fixed status summary, not command arguments, prompts, stdout or stderr. Job output stays in the original terminal. A failed notification prints a warning and preserves the job's exit status. A zero Claude process exit is not proof that a model's answer is correct. This wrapper reports process completion; it is not an interactive per-turn hook.

`approval-demo.sh` uses synchronous `ntfyx ask --allow-deny`, which verifies the answer and acquires a one-time claim before returning success. Deny, an unanswered wait, transport failure and an already-consumed request do not continue. The only permitted demo step prints a line. It never deploys, transfers money, or runs a user-supplied command. Do not use the exit status of a read-only `ntfyx result` as authorization. Real external actions need their own idempotency and crash recovery; do not automatically rerun an uncertain action.

## Guides

- [Claude Code completion notifications](https://ntfyx.me/docs/claude-code-notifications/)
- [Shell script notifications](https://ntfyx.me/docs/notifications/)
- [Wait for a phone approval](https://ntfyx.me/docs/phone-approval/)
- [Web Inbox](https://ntfyx.me/docs/web/)
- [Agent and local MCP configuration](https://ntfyx.me/docs/agents/)
- [中文使用说明](https://ntfyx.me/zh/docs/)
- [FAQ](https://ntfyx.me/docs/faq/)

## What encryption protects

Clients encrypt titles, bodies, choices and replies before sending them. Each receiver gets its own encrypted copy. The service processes ciphertext plus operational metadata such as routing IDs, time, size and notification tokens. A newly authorized browser cannot read earlier phone history. Revocation cannot erase already-delivered content.

End-to-end encryption does not protect a compromised endpoint or conceal all metadata. Independent security review is not complete. Purchase restoration does not restore encryption keys. Read the [security model](https://ntfyx.me/security/) and [privacy notice](https://ntfyx.me/privacy/).

## Verification

The examples are exercised using the compiled CLI, an isolated local encrypted relay, programmatic phone authorization and signed browser replies. Cases cover a successful job, failed job, unchanged command arguments, notification failure, Allow, Deny, timeout, transport failure and repeat claim rejection. Published screenshots show that local Web test with synthetic messages; they are not an iPhone/APNs acceptance claim or a Claude-generated output.

The separately tested native Claude Code permission adapter has a documented version and mode boundary. Local stdio MCP does not mean Ntfyx is listed in the ChatGPT or Claude cloud app directory. See the agent guide for supported configurations.

CLI release notes and signed downloads: https://ntfyx.me/changelog/ and https://ntfyx.me/download/

Support: https://ntfyx.me/support/ · Never include keys, pairing links, recovery codes or private messages in a public issue.
