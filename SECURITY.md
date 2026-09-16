# Security policy

## Supported releases

The **latest release** on the
[Releases page](https://github.com/samiarTheDevAi/Grous-AI-apk/releases) is
the only release that receives security attention. Earlier releases are
unsupported.

## Reporting a vulnerability

**Please do not open a public issue for a security vulnerability.**

Report vulnerabilities privately so they can be reviewed and fixed before
public disclosure:

- Use GitHub's **private vulnerability disclosure**: open a new report via
  [`Security` → `Reporting a vulnerability`](https://github.com/samiarTheDevAi/Grous-AI-apk/security/advisories/new)
  (the "Report a vulnerability" button on this repository).

Include, where possible:

- a description of the issue and its potential impact,
- steps to reproduce it,
- the affected APK / release (and its SHA-256 if you have it).

We aim to acknowledge a report within **3 business days** and will keep you
posted as we work on a fix. Once a fix is available we publish a patch release
and, where appropriate, a public security advisory describing the fix and the
safe version.

## Verifying a release

Releases are distributed as pre-built APKs in [`releases/`](releases). To
confirm a downloaded APK is exactly the one that was published (and was not
tampered with in transit), use the bundled verifier:

```bash
python3 tools/apk_verify.py path/to/GrousAI-v1.0.apk
```

The tool performs cryptographic checks — it verifies the SHA-256 file digests
recorded in the APK's JAR signature against the actual file bytes, validates
ZIP integrity, audits the permissions against the documented baseline, and
extracts the signing certificate's subject and SHA-256 fingerprint. A file that
has been modified after signing will **fail** verification.

Pin the exact artifact by its SHA-256 (published in the
[README](README.md#verifying-the-apk) and in each GitHub release).

## Threat model & current posture

- **Permissions:** the app requests `INTERNET` only. Any build that requests
  additional permissions fails the verifier and is not accepted.
- **Signing:** the currently published build is signed with the **Android
  debug keystore** and is built **debuggable**. This is acceptable for personal
  / trusted distribution but is **not** a production signing posture. Before
  wide distribution the app should be rebuilt and signed with a dedicated
  release keystore (see [README — Security considerations](README.md#security-considerations)).
- **Network:** inference calls are sent to the provider you configure over
  HTTPS. `android:usesCleartextTraffic="true"` is currently set, which permits
  plain-HTTP traffic — treat user-supplied custom base URLs accordingly.
- **Data:** chat history and settings are stored locally on the device. Chats
  are sent to the inference provider you select in order to generate responses.

## Scope

This policy covers the APK artifacts published in this repository and the
verification tooling. Vulnerabilities in third-party services the app talks to
(Groq, Pollinations, or user-supplied endpoints) are out of scope here — report
them to the respective provider.
