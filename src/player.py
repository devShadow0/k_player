import os
import json
from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

SETTINGS_FILE = "kplayer_settings.json"

class Player(QObject):
    currentSongChanged = Signal(str)

    def __init__(self):
        super().__init__()
        
        # --- NEW: Load directories from JSON ---
        self.directories = self.load_settings()
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)
        
        self.current_playlist = self.get_songs()
        self.current_song_index = -1

    # --- NEW: Settings Management ---
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                return data.get("directories", [])
        return [] # Return empty list if no settings file exists yet

    def save_settings(self, new_directories):
        self.directories = new_directories
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"directories": self.directories}, f, indent=4)
        # Re-scan the songs whenever we save new folders
        self.current_playlist = self.get_songs()

    # --- UPDATED: Scan multiple folders ---
    def get_songs(self):
        songs = []
        for directory in self.directories:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    if file.lower().endswith(".mp3"):
                        songs.append(os.path.join(directory, file))
        return songs

    # ... keep your play_song, toggle_playback, next_song, and prev_song EXACTLY the same ...
    def play_song(self, file_path):
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.media_player.play()
        if file_path in self.current_playlist:
            self.current_song_index = self.current_playlist.index(file_path)
        self.currentSongChanged.emit(file_path)

    def toggle_playback(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def next_song(self):
        if not self.current_playlist: return
        self.current_song_index += 1
        if self.current_song_index >= len(self.current_playlist):
            self.current_song_index = 0 
        self.play_song(self.current_playlist[self.current_song_index])

    def prev_song(self):
        if not self.current_playlist: return
        self.current_song_index -= 1
        if self.current_song_index < 0:
            self.current_song_index = len(self.current_playlist) - 1
        self.play_song(self.current_playlist[self.current_song_index])