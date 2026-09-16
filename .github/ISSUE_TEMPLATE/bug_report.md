---
name: Bug report
about: Report a problem with the Grous AI APK
title: ''
labels: ['bug', 'needs triage']
assignees: []
---

## What happened?

A clear, concise description of the bug (what you expected vs. what actually
happened).

## Steps to reproduce

1.
2.
3.

## Expected behaviour

## Device & app details

| Field | Value |
|---|---|
| Android version | e.g. 14 |
| Device / model | e.g. Pixel 8 |
| Grous AI version (versionName) | e.g. 1.0 |
| APK SHA-256 (if known) | run `python3 tools/apk_verify.py <apk>` |

To report the exact artifact you have, run the bundled verifier and paste its
output (it prints the package, version, and SHA-256):

```bash
python3 tools/apk_verify.py path/to/GrousAI-v1.0.apk
```

## Logs / screenshots

<details>
<summary>Console / crash log (if any)</summary>

```
paste here
```
</details>

## Additional context

Anything else that helps (e.g. which model you selected, whether a custom base
URL was configured).
