# LSB Steganography Tool

Hide secret messages inside images using the **Least Significant Bit (LSB)** technique. Changing only the last bit of each pixel's RGB value causes a color difference of just ±1 — completely invisible to the human eye.

---

## Features

- Encode text into PNG images
- Decode hidden messages from images
- Optional XOR password encryption
- Capacity checker (how many chars fit in an image)
- Command-line interface (CLI)
- Flask web UI with drag-and-drop

---

## Setup

```bash
# 1. Clone or download the project
cd steganography-tool

# 2. Install dependencies
pip install -r requirements.txt

# 3. You're ready!
```

---

## CLI Usage

```bash
# Hide a message
python cli.py encode input.png "Meet at midnight!" output.png

# Hide with password encryption
python cli.py encode input.png "Top secret" output.png -p mypassword

# Extract hidden message
python cli.py decode output.png

# Extract with password
python cli.py decode output.png -p mypassword

# Check image capacity
python cli.py capacity input.png

# Compare original vs encoded (shows pixel change stats)
python cli.py compare input.png output.png
```

---

## Web UI Usage

```bash
python app.py
# Open http://localhost:5000 in your browser
```

---

## How It Works

Each image pixel has R, G, B values stored as 8-bit integers (0-255).

```
Pixel Red channel: 1 0 1 1 0 1 1 0
                                 ^
                           Least Significant Bit (LSB)
```

We convert our secret message to binary and replace the LSB of each channel:

```
"Hi" → 01001000 01101001

Pixel 1 R: 10110110 → 10110110  (message bit = 0, no change)
Pixel 1 G: 10011011 → 10011011  (message bit = 1, no change)
Pixel 1 B: 11100100 → 11100101  (message bit = 0 → 1, diff = ±1)
...
```

The color changes by at most ±1 — the human eye cannot perceive this difference.

---

## Project Structure

```
steganography-tool/
├── steganography.py   # Core encode/decode logic + XOR encryption
├── cli.py             # Command-line interface
├── app.py             # Flask web application
├── requirements.txt   # Python dependencies
├── templates/
│   └── index.html     # Web UI
├── uploads/           # Temporary file storage (auto-created)
└── README.md
```

---

## Tech Stack

- **Python 3.x**
- **Pillow (PIL)** — image pixel manipulation
- **Flask** — web application framework
- **HTML/CSS/JS** — frontend web UI

---

## Limitations

- Always save output as **PNG** — JPEG compression destroys hidden data (lossy compression changes pixel values)
- Maximum capacity = (width × height × 3) / 8 characters
- Example: a 1920×1080 image can hide ~777,600 characters


---

## Ethical Note

This tool is built for educational purposes. Always use steganography ethically and legally. Never use it to conceal illegal activities.

---

## Author

Built as a cybersecurity portfolio project.
