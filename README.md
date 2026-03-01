
# KPlayer 🎵

A sleek, modern, and minimalist offline music player built with Python. KPlayer features a custom frameless UI, live search, persistent multi-folder library management.

## ✨ Features

* **Modern Frameless UI:** Custom translucent design with smooth rounded corners, dark mode aesthetics, and a draggable header.
* **Smart Library Management:** Add multiple music directories to your library. Settings are persistently saved to a local `.json` file.
* **Live Search:** Instantly filter your music library by song title or artist name as you type.
* **Rich Metadata Parsing:** Automatically extracts and displays MP3 ID3 tags, including high-quality album art, track title, artist, and accurate durations.
* **Precision "Jump" Slider:** Custom-built progress slider that instantly seeks to the exact clicked position for a fluid user experience.

## 📁 Project Structure

```text
KPlayer/
├── assets/
│   └── logo_256.png             # Application icon
├── src/
│   ├── ui/
│   │   ├── bottom_player.py     # Playback controls and jump slider
│   │   ├── settings_dialog.py   # Multi-folder management UI
│   │   ├── song_card.py         # Individual track UI with metadata
│   │   └── top_bar.py           # Live search and header actions
│   ├── player.py                # Audio engine and state management
│   ├── player_ui.py             # Master frameless layout and routing
│   └── windows_smtc.py          # Windows overlay and media key hooks
├── main.py                      # Application entry point
└── requirements.txt

```
---

**Author:** Kaushal Prakash