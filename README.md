<div align="center">

<img src="assets/grous-ai-icon.png" alt="Grous AI icon" width="120" height="120" />

# Grous AI

Free AI chat for Android — Groq-powered, no credit card required.

[![License: MIT](https://img.shields.io/badge/License-MIT-635bff.svg)](LICENSE)
[![APK verify](https://github.com/samiarTheDevAi/Grous-AI-apk/actions/workflows/apk-verify.yml/badge.svg)](https://github.com/samiarTheDevAi/Grous-AI-apk/actions/workflows/apk-verify.yml)
[![Platform: Android](https://img.shields.io/badge/Platform-Android-3ddc84.svg)](#requirements)
[![minSdk: 21](https://img.shields.io/badge/minSdk-21%20(Android%205.0)-00c2a8.svg)](#requirements)

</div>

---

## What is Grous AI?

Grous AI is a lightweight Android app that gives you **free AI chat on your
phone**. It talks to [Groq's](https://groq.com) fast OpenAI-compatible API
using free-tier models — no subscription, no dev tier, no credit card. It is a
single-activity WebView app, so the entire experience (chat, modes, themes,
image generation) lives in a small, inspectable web bundle.

The default model is a free Groq endpoint (`openai/gpt-oss-120b`), and the app
falls back to other free models automatically when one is rate-limited.

## Features

- **Free AI chat** on Groq's fast inference API (no credit card)
- **Model picker** with free-tier presets and a custom-base-URL option
- **Coder mode** — a coding-tuned system prompt for code help
- **Education mode** — step-by-step, exam-friendly answers
- **Image generation** via [Pollinations](https://pollinations.ai)
- **Markdown rendering**, streaming responses, and one-tap chat export
  (`.md` / `.txt`)
- **Local chat history** and settings (persisted on-device)
- **Light / dark themes** and a swipe-out settings drawer
- **Personalisation** (user name, assistant personality)

## Download & install

1. Grab the latest APK from the
   [Releases page](https://github.com/samiarTheDevAi/Grous-AI-apk/releases).
2. On your phone, allow *"Install unknown apps"* for your file manager /
   browser when prompted.
3. Tap the `.apk` to install.

> This repo distributes the **pre-built APK only** — it does not contain the
> app source. See [Verifying the APK](#verifying-the-apk) to confirm a
> download is exactly the one that was signed and published.

## Requirements

| | |
|---|---|
| Android version | **5.0 (API 21)** or newer |
| Target SDK | 34 (Android 14) |
| Package name | `com.grous.ai` |
| Permissions | `INTERNET` only (plus an internal, signature-protected permission) |
| Network | Internet connection required (all inference is remote) |

## Verifying the APK

This repository ships a dependency-free verification tool —
[`tools/apk_verify.py`](tools/apk_verify.py) — that checks a Grous AI release
APK **without the Android SDK or Java**. Run it against any downloaded APK:

```bash
python3 tools/apk_verify.py path/to/GrousAI-v1.0.apk
```

The tool performs real, cryptographic checks — not just a file-size match:

1. **ZIP integrity** — every entry decompresses with a valid CRC-32.
2. **Manifest audit** — decodes the binary `AndroidManifest.xml` (built-in
   AXML parser) and reports package, version, min/target SDK, permissions,
   and activities.
3. **Permission baseline** — *fails* if the APK requests any permission
   outside the documented baseline (see below).
4. **Signature detection** — locates the APK Signing Block and reports which
   schemes (v1/v2/v3) are present.
5. **Signing certificate** — extracts the signer certificate and reports its
   subject, key size, and SHA-256 fingerprint; *warns* on a debug keystore.
6. **v1 JAR integrity** — verifies every file digest recorded in
   `META-INF/MANIFEST.MF` against the actual APK bytes. A mismatch means the
   file was tampered with and **fails** the build.
7. **SHA-256** — prints the artifact hash for pinning.

It exits `0` on pass (warnings allowed), `1` on fail, `2` on usage/IO error.
Add `--strict` to promote the debug-keystore / debuggable warnings to hard
failures (the correct gate for a production release). Add `--report-dir DIR`
to also write a JSON report, the SHA-256, and a human-readable manifest
summary.

### Expected output for the published v1.0 build

```
PASS  GrousAI-v1.0.apk
      package    : com.grous.ai
      version    : 1 (1.0)
      minSdk     : 21   targetSdk: 34
      permissions: android.permission.INTERNET, com.grous.ai.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
      signing    : v2, ...  (cert: Android Debug)
      SHA-256    : ba81ee759b23cde14f01e7985832341389a4dd994001a58046f1b13f37e732f3
      warning    : signed with the Android DEBUG keystore ...
      strict     : built debuggable ... (use --strict to fail on this)
```

| Artifact | SHA-256 |
|---|---|
| `GrousAI-v1.0.apk` | `ba81ee759b23cde14f01e7985832341389a4dd994001a58046f1b13f37e732f3` |
| Signing cert (Android Debug, RSA-2048) | `df40276bc60e907df47ec14e77efee164732d32981e0b657e800f020c01275a0` |

> The published APK is signed with the **Android debug keystore** and is built
> **debuggable**. That is fine for personal / trusted distribution, but it is
> not a production release key. See
> [Security considerations](#security-considerations).

## Security considerations

**Permissions.** The app requests `android.permission.INTERNET` and nothing
else user-facing. The second entry in the manifest
(`com.grous.ai.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`) is auto-generated by
the Android Gradle Plugin and is signature-protected — it is not a real
privilege. The verifier *fails* any build that adds a permission outside this
baseline.

**Debug-signed, debuggable build.** The currently published APK is signed with
the **Android debug keystore** (`CN=Android Debug`, RSA-2048) and has
`android:debuggable="true"`. Consequences:

- A debuggable build allows anyone with USB / ADB access to attach a debugger
  to the app process. Do not use it on a device you don't trust.
- A debug key is machine-specific and **cannot** be used to sign future
  updates; to update the app in place you must re-sign with the *same* key
  every time. Plan to move to a proper release keystore before wider
  distribution.

To produce a release build, rebuild with a release signing config
(`signingConfigs.release` + `buildTypes.release { signingConfig ... }`) and
confirm the verifier passes with `--strict`.

**Cleartext traffic.** The manifest sets `android:usesCleartextTraffic="true"`,
so plain-HTTP (non-TLS) requests are permitted. The app's own API calls go to
`https://` endpoints; this flag is kept for flexibility with user-supplied
custom base URLs. If you only ever use HTTPS, it can be removed.

**API keys.** The app calls a remote inference API. Any API key you enter is
stored on-device and sent to that provider over the network — review where a
custom base URL points before using it.

**Data.** Chat history and settings are stored locally on the device. The app
has no account system and does not upload your chats anywhere except the
inference provider you select, in order to generate responses.

## Repository layout

```
.
├── releases/                 # published APK artifacts
│   └── GrousAI-v1.0.apk
├── assets/
│   └── grous-ai-icon.png     # app icon (rendered by tools/make_icon.py)
├── tools/
│   ├── apk_verify.py         # dependency-free APK verifier (stdlib only)
│   └── make_icon.py          # renders the icon PNG, no dependencies
├── .github/
│   ├── workflows/
│   │   └── apk-verify.yml    # CI: verify every APK on each push
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE                   # MIT
└── README.md
```

## CI

[`.github/workflows/apk-verify.yml`](.github/workflows/apk-verify.yml) runs the
verifier against every `releases/*.apk` on each push to `main` (and on
pull requests), uploads the generated report as a workflow artifact, and fails
the build on a hard check (corruption, tampering, wrong package, unexpected
permissions, or an unsigned APK). Warnings such as the debug keystore are
reported but do not block the build — flip the workflow to `--strict` once a
proper release build is published.

## Releases

See the [Releases page](https://github.com/samiarTheDevAi/Grous-AI-apk/releases)
and [CHANGELOG.md](CHANGELOG.md).

## License

Distributed under the [MIT License](LICENSE).
