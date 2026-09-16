# Changelog

All notable changes to **Grous AI** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0] - 2026-09-15

### Added
- First published build: `releases/GrousAI-v1.0.apk`
  (package `com.grous.ai`, versionCode 1, versionName `1.0`,
  minSdk 21, targetSdk 34).
- Free AI chat over the Groq OpenAI-compatible API with free-tier model
  presets, a custom base-URL option, and automatic fallback when a model is
  rate-limited.
- Coder mode and Education mode.
- Image generation via Pollinations.
- Markdown rendering, streaming responses, and chat export (`.md` / `.txt`).
- Local chat history and on-device settings (user name, personality, theme).
- Light / dark themes and a swipe-out settings drawer.

### Repository
- Added `tools/apk_verify.py` — a dependency-free (Python stdlib only) APK
  verifier: ZIP integrity, binary-manifest audit, permission baseline,
  APK-signing-block detection, signer-certificate extraction, and v1 JAR
  file-digest integrity.
- Added CI (`.github/workflows/apk-verify.yml`) that verifies every APK on
  each push and uploads the report as an artifact.
- Added issue templates, `SECURITY.md`, and this changelog.

### Known limitations
- The published build is signed with the **Android debug keystore** and is
  built **debuggable**. It is suitable for personal / trusted distribution but
  is not a production release build. Rebuild with a release signing config
  (and `android:usesCleartextTraffic` review) before wide distribution.
- `android:usesCleartextTraffic="true"` is set, permitting plain-HTTP requests.
