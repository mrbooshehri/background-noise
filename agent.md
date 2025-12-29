# Ambient Noise Terminal Application (Textual + Python)

## Project Overview

This project is a **terminal-based ambient noise generator** built with **Python** and the **Textual** TUI (Text User Interface) framework.

The application allows users to:

* Play **multiple ambient sound effects simultaneously** (MP3 format)
* Control **individual volume levels per sound line**
* Start/stop sounds independently
* Display a **motivational quote** fetched from the ZenQuotes API

The app is designed for focus, relaxation, and productivity sessions directly inside the terminal.

---

## Core Features

### 🎧 Ambient Sound Mixer

The application supports the following sound effects:

| Sound Name | Description                  |
| ---------- | ---------------------------- |
| Sea        | Ocean waves                  |
| Fire       | Campfire crackling           |
| Sea Gulf   | Calm gulf water              |
| Rain       | Steady rainfall              |
| Lightning  | Occasional thunder/lightning |
| Busy Cafe  | Coffee shop background noise |

Each sound:

* Plays **simultaneously** with others
* Has its **own volume control** (0–100%)
* Can be toggled ON/OFF independently

---

### 🔊 Independent Volume Control

* Each sound line has a dedicated volume slider or +/- controls
* Volume changes affect only the selected sound
* Volume updates happen **in real-time** without restarting playback

---

### 💬 Motivational Quotes

* Fetches a random motivational quote from:

  ```
  https://zenquotes.io/api/random
  ```
* Displays quote text and author in a dedicated panel
* Refreshes:

  * On app start
  * On user action (e.g. key press)

---

## Architecture

### High-Level Architecture

```
┌───────────────────────────────┐
│        Textual UI App         │
│                               │
│  ┌──────────┐  ┌──────────┐  │
│  │ Sound UI │  │ Quote UI │  │
│  └────┬─────┘  └────┬─────┘  │
│       │              │        │
└───────┼──────────────┼────────┘
        │              │
┌───────▼───────┐  ┌───▼────────┐
│ Sound Engine  │  │ Quote Fetch │
│ (Audio Mixer)│  │ (HTTP)      │
└───────┬───────┘  └────────────┘
        │
┌───────▼───────────────────────┐
│      Audio Backend (MP3)      │
│   pygame / pydub / simpleaudio│
└───────────────────────────────┘
```

---

## Technology Stack

| Layer          | Tool                                |
| -------------- | ----------------------------------- |
| TUI Framework  | Textual                             |
| Language       | Python 3.10+                        |
| Audio Playback | pygame.mixer or pydub + simpleaudio |
| HTTP Client    | requests                            |
| File Format    | MP3                                 |

---

## Audio Engine Design

### Responsibilities

* Load MP3 files
* Loop sounds continuously
* Manage per-sound volume
* Allow simultaneous playback

### Recommended Approach

* Use **pygame.mixer**
* Assign **one mixer channel per sound**

Example internal structure:

```python
sounds = {
    "sea": {"file": "sea.mp3", "channel": 0, "volume": 0.5},
    "fire": {"file": "fire.mp3", "channel": 1, "volume": 0.5},
    "rain": {"file": "rain.mp3", "channel": 2, "volume": 0.5},
}
```

Each channel:

* Loops infinitely
* Volume adjustable independently

---

## Textual UI Layout

### Main Layout Sections

```
┌──────────────────────────────────────┐
│ Ambient Noise Mixer                  │
├──────────────────────────────────────┤
│ Sea        [ ON ]  Volume: ████▌     │
│ Fire       [ ON ]  Volume: ██▌       │
│ Rain       [ OFF ] Volume: █████     │
│ Lightning  [ OFF ] Volume: █▌        │
│ Cafe       [ ON ]  Volume: ███       │
├──────────────────────────────────────┤
│ "Do something today your future     │
│  self will thank you for."           │
│  — Anonymous                         │
└──────────────────────────────────────┘
```

---

## User Interaction

### Keyboard Controls (Suggested)

| Key   | Action                     |
| ----- | -------------------------- |
| ↑ / ↓ | Navigate sound list        |
| ← / → | Decrease / Increase volume |
| Space | Toggle sound ON/OFF        |
| R     | Refresh quote              |
| Q     | Quit application           |

---

## Quote Service Design

### API Response Example

```json
[
  {
    "q": "Your limitation—it’s only your imagination.",
    "a": "Unknown"
  }
]
```

### Handling Strategy

* Fetch asynchronously to avoid UI blocking
* Gracefully handle network errors
* Cache last quote if API is unreachable

---

## File Structure

```
ambient-noise-app/
├── agent.md
├── main.py
├── ui/
│   ├── app.py
│   ├── sound_panel.py
│   └── quote_panel.py
├── audio/
│   ├── engine.py
│   └── sounds/
│       ├── sea.mp3
│       ├── fire.mp3
│       ├── rain.mp3
│       ├── lightning.mp3
│       ├── cafe.mp3
│       └── gulf.mp3
├── services/
│   └── quotes.py
└── requirements.txt
```

---

## Non-Functional Requirements

* Low CPU usage
* Smooth audio playback without glitches
* Works on Linux and macOS terminals
* Handles missing sound files gracefully

---

## Future Enhancements

* Preset profiles (Focus, Sleep, Cafe)
* Save/load volume configurations
* Timer-based auto-stop
* Offline quote cache
* Theme customization

---

## License

MIT License

---

## Summary

This project combines **Textual**, **audio mixing**, and **motivational content** to create a powerful yet minimal **terminal-based ambient noise experience** tailored for developers and productivity-focused users.

