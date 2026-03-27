# DevTools Online

A free, open-source developer toolkit that provides essential everyday utilities right in your browser. Built with Python Flask, DevTools Online offers a clean, fast interface for common encoding, decoding, formatting, and conversion tasks — no sign-up required.

## Features

- **Entirely browser-based** — works offline after initial load
- **No data leaves your machine** — all processing happens client-side
- **Clean, distraction-free UI** — get in, get the job done, get out
- **Single lightweight server** — one command to start

## Tools

| Tool | Description |
|------|-------------|
| **JSON Formatter** | Pretty-print, minify, and validate JSON with syntax highlighting and error reporting. |
| **Base64 Encoder / Decoder** | Encode text to Base64 or decode Base64 back to plain text. Supports UTF-8. |
| **JWT Decoder** | Decode JSON Web Tokens to inspect the header, payload, and signature without verification. |
| **Hash Generator** | Generate MD5, SHA-1, SHA-256, and SHA-512 hashes from arbitrary text input. |
| **UUID Generator** | Create random v4 UUIDs instantly, with bulk generation support. |
| **Regex Tester** | Write and test regular expressions with real-time match highlighting and capture-group display. |
| **URL Encoder / Decoder** | Percent-encode or decode URLs and query-string parameters. |
| **Timestamp Converter** | Convert between Unix timestamps and human-readable dates in multiple formats and time zones. |
| **Text Diff** | Compare two blocks of text side-by-side and see additions, deletions, and changes highlighted. |

## Getting Started

### Prerequisites

- Python 3.8+
- Flask (`pip install flask`)

### Run

```bash
pip install flask
python server.py
```

The application starts on **http://localhost:9001**.

## License

This project is open source and available under the [MIT License](LICENSE).
