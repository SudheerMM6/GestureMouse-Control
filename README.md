# Gesture Mouse Control

A Python desktop prototype that uses webcam-based hand tracking to move the cursor and trigger mouse clicks.

## What It Does

- Tracks one hand through the webcam using MediaPipe.
- Maps the index finger position to the screen cursor.
- Uses thumb and index finger distance to switch between movement and click gestures.
- Supports single-click and double-click gestures.

## Tech Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python virtual_mouse.py
```

Press `q` in the OpenCV window to exit.

## Checks

Run a syntax check:

```bash
python -m py_compile virtual_mouse.py
```

## Notes

- A webcam is required.
- Cursor movement depends on lighting, camera quality, and hand position.
- This is a local desktop prototype, not a packaged application.
