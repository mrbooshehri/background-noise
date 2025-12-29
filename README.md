# Background Noise

Terminal-based ambient noise mixer built with Textual and pygame.

## Features

- Play multiple ambient sounds at once
- Per-sound volume control
- Independent start/stop for each sound
- Motivational quote panel

## Requirements

- Python 3.10+
- WSL/Linux/macOS terminal

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Put your audio files in `audio/sounds/` with these names:

- `sea.ogg`
- `fire.ogg`
- `gull.ogg`
- `rain.ogg`
- `lightning.ogg`
- `cafe.ogg`

## Run

```bash
python main.py
```

## Controls

- Up/Down: move selection
- Left/Right: volume down/up
- Space: toggle sound
- R: refresh quote
- Q: quit

## License

MIT. See `LICENSE`.
