from PySide6.QtWidgets import QMainWindow, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtMultimedia import QMediaPlayer
from src.ui.song_card import SongCard
from src.ui.bottom_player import BottomPlayer
from src.ui.top_bar import TopBar
from src.ui.settings_dialog import SettingsDialog

class PlayerUI(QMainWindow):
    def __init__(self, player_backend):
        super().__init__()
        self.player_backend = player_backend 
        
        self.setWindowTitle("KPlayer - Minimalist Music Player")
        self.resize(1000, 700)
        self.setMinimumSize(QSize(1000, 700))
        self.setStyleSheet("background-color: #0A0A0A;") # Deeper, truer black
        
        self.master_widget = QWidget()
        self.setCentralWidget(self.master_widget)
        self.master_layout = QVBoxLayout(self.master_widget)
        self.master_layout.setContentsMargins(0, 0, 0, 0)
        self.master_layout.setSpacing(0)
        
        self.top_bar = TopBar()
        self.master_layout.addWidget(self.top_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # Custom sleek scrollbar CSS
        self.scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #0A0A0A;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #2A2A2A;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3A3A3A;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.list_container = QWidget()
        self.list_container.setStyleSheet("background-color: #0A0A0A;")
        self.list_layout = QVBoxLayout(self.list_container)
        # Increased side margins for a more "contained" look
        self.list_layout.setContentsMargins(30, 20, 30, 20) 
        self.list_layout.setSpacing(0) # Spacing handled by card margins now
        self.list_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.list_container)

        self.master_layout.addWidget(self.scroll_area)

        self.bottom_player = BottomPlayer()
        self.master_layout.addWidget(self.bottom_player)
        
        self.setup_connections()
        self.load_songs()

    def setup_connections(self):
        # 1. Connect Play/Pause
        self.bottom_player.play_pause_btn.clicked.connect(self.player_backend.toggle_playback)
        
        # 2. Connect Next and Previous
        self.bottom_player.next_btn.clicked.connect(self.player_backend.next_song)
        self.bottom_player.prev_btn.clicked.connect(self.player_backend.prev_song)

        # 3. Connect Slider (Seeking)
        # .sliderMoved triggers when you drag the handle. It passes the new millisecond 
        # value directly to media_player.setPosition() to jump to that interval.
        self.bottom_player.progress_slider.sliderMoved.connect(self.player_backend.media_player.setPosition)

        # 4. Connect Backend signals to UI updates
        mp = self.player_backend.media_player
        mp.positionChanged.connect(self.update_slider_position)
        mp.durationChanged.connect(self.update_slider_duration)
        mp.playbackStateChanged.connect(self.update_play_button)
        
        # 5. Auto-play next song when current song naturally ends
        mp.mediaStatusChanged.connect(self.handle_media_status)
        
        # 6. Update BottomPlayer info when song changes
        self.player_backend.currentSongChanged.connect(self.bottom_player.update_song_details)
        
        # 7. Top Bar Connections ---
        self.top_bar.search_changed.connect(self.filter_songs)
        self.top_bar.refresh_clicked.connect(self.refresh_library)
        self.top_bar.settings_clicked.connect(self.open_settings)

    # --- NEW METHOD ---
    def handle_media_status(self, status):
        # QMediaPlayer.MediaStatus.EndOfMedia means the song finished playing
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player_backend.next_song()
            
    def load_songs(self):
        song_paths = self.player_backend.current_playlist
        for path in song_paths:
            card = SongCard(path)
            # When a card is clicked, tell the backend to play that file
            card.clicked.connect(self.player_backend.play_song)
            self.list_layout.addWidget(card)

    # --- UI Update Slots ---
    def update_slider_position(self, position):
        # Update slider value without triggering sliderMoved
        self.bottom_player.progress_slider.blockSignals(True)
        self.bottom_player.progress_slider.setValue(position)
        self.bottom_player.progress_slider.blockSignals(False)
        self.bottom_player.current_time_label.setText(self.format_time(position))

    def update_slider_duration(self, duration):
        self.bottom_player.progress_slider.setMaximum(duration)
        self.bottom_player.total_time_label.setText(self.format_time(duration))

    def update_play_button(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.bottom_player.play_pause_btn.setText("⏸")
        else:
            self.bottom_player.play_pause_btn.setText("▶")

    def format_time(self, ms):
        seconds = (ms // 1000) % 60
        minutes = (ms // 60000) % 60
        return f"{minutes}:{seconds:02d}"
    
    def filter_songs(self, query):
        query = query.lower()
        # Loop through all the SongCard widgets in the scroll layout
        for i in range(self.list_layout.count()):
            widget = self.list_layout.itemAt(i).widget()
            if widget:
                # Check if the query is in the file path or the parsed title
                # Hide the card if it doesn't match, show it if it does
                if query in widget.title_label.text().lower() or query in widget.artist_label.text().lower():
                    widget.show()
                else:
                    widget.hide()
    
    def refresh_library(self):
        # Clear the current list
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        # Re-fetch and load
        self.player_backend.current_playlist = self.player_backend.get_songs()
        self.load_songs()
    
    def open_settings(self):
        # Open the pop-up and pass it our current folders
        dialog = SettingsDialog(self.player_backend.directories, self)
        
        # .exec() halts the main window and waits for the user to click Save or Cancel
        if dialog.exec(): 
            # If they clicked Save, grab the new list and tell the backend to save it
            new_dirs = dialog.get_directories()
            self.player_backend.save_settings(new_dirs)
            # Instantly reload the UI with the new songs
            self.refresh_library()
    