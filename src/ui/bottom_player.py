import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel, QStyle
from PySide6.QtGui import QPixmap, QImage, QFontMetrics
from PySide6.QtCore import Qt
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

# --- NEW CLASS: Custom Slider that jumps to the clicked position ---
class JumpSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Calculate the exact value based on where the mouse clicked
            val = self.style().sliderValueFromPosition(
                self.minimum(),
                self.maximum(),
                int(event.position().x()),
                self.width()
            )
            self.setValue(val)
            # Emit the signal so the backend actually seeks to this new time
            self.sliderMoved.emit(val)
            
        super().mousePressEvent(event)


class BottomPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100) # Give it a little more breathing room
        self.setStyleSheet("""
            BottomPlayer {
                background-color: #0F0F0F; /* Slightly offset from main black */
                border-top: 1px solid #1C1C1C; /* Soft separator */
            }
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                color: #1DB954; /* Spotify Green */
            }
            /* Thinner, sleeker slider */
            QSlider::groove:horizontal {
                border-radius: 2px;
                height: 4px; 
                background: #333333;
            }
            QSlider::sub-page:horizontal {
                background: #1DB954; /* Green progress fill */
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                width: 10px;
                height: 10px;
                margin: -3px 0;
                border-radius: 5px;
            }
            QSlider::handle:horizontal:hover {
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QLabel {
                color: #999999;
                font-size: 11px;
                font-weight: bold;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 10, 25, 15)

        # --- 1. LEFT: Song Info ---
        self.left_container = QWidget()
        self.left_container.setFixedWidth(250)
        
        info_layout = QHBoxLayout(self.left_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        self.art_label = QLabel()
        self.art_label.setFixedSize(56, 56)
        self.art_label.setStyleSheet("background-color: #222; border-radius: 6px;")
        
        text_layout = QVBoxLayout()
        self.title_label = QLabel("--")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
        self.artist_label = QLabel("--")
        self.artist_label.setStyleSheet("font-size: 12px; color: #AAAAAA;")
        
        self.title_label.setMinimumWidth(0)
        self.artist_label.setMinimumWidth(0)
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.artist_label)
        text_layout.setAlignment(Qt.AlignVCenter)
        
        info_layout.addWidget(self.art_label)
        info_layout.addSpacing(10) # Add a little gap between art and text
        info_layout.addLayout(text_layout)
        
        # --- 2. CENTER: Controls & Slider ---
        self.center_container = QWidget()
        center_layout = QVBoxLayout(self.center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setAlignment(Qt.AlignCenter)
        
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignCenter)
        controls_layout.setSpacing(20) # Spread buttons out
        
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setStyleSheet("font-size: 18px;")
        self.play_pause_btn = QPushButton("▶")
        self.play_pause_btn.setStyleSheet("font-size: 32px;")
        self.next_btn = QPushButton("⏭")
        self.next_btn.setStyleSheet("font-size: 18px;")
        
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.play_pause_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setCursor(Qt.PointingHandCursor)

        controls_layout.addWidget(self.prev_btn)
        controls_layout.addWidget(self.play_pause_btn)
        controls_layout.addWidget(self.next_btn)

        slider_layout = QHBoxLayout()
        slider_layout.setSpacing(10)
        self.current_time_label = QLabel("0:00")
        
        # --- APPLIED CUSTOM SLIDER HERE ---
        self.progress_slider = JumpSlider(Qt.Horizontal)
        self.progress_slider.setCursor(Qt.PointingHandCursor)
        self.total_time_label = QLabel("0:00")
        
        slider_layout.addWidget(self.current_time_label)
        slider_layout.addWidget(self.progress_slider)
        slider_layout.addWidget(self.total_time_label)

        center_layout.addLayout(controls_layout)
        center_layout.addSpacing(5)
        center_layout.addLayout(slider_layout)

        # --- 3. RIGHT: Empty Balance Container ---
        self.right_container = QWidget()
        self.right_container.setFixedWidth(250)
        right_layout = QHBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.left_container)
        main_layout.addWidget(self.center_container)
        main_layout.addWidget(self.right_container)

    def update_song_details(self, file_path):
        # We fetch the metadata just like before
        raw_title = os.path.basename(file_path)
        raw_artist = "Unknown Artist"
        self.art_label.clear()
        
        try:
            audio = MP3(file_path, ID3=ID3)
            if audio.tags:
                if "TIT2" in audio.tags:
                    raw_title = str(audio.tags["TIT2"])
                if "TPE1" in audio.tags:
                    raw_artist = str(audio.tags["TPE1"])
                    
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        img = QImage.fromData(tag.data)
                        pixmap = QPixmap.fromImage(img).scaled(
                            60, 60, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                        )
                        self.art_label.setPixmap(pixmap)
                        break
        except Exception:
            pass
            
        # Optional Polish: Elide (add "...") text if it's too long to fit in our locked container
        metrics = QFontMetrics(self.title_label.font())
        elided_title = metrics.elidedText(raw_title, Qt.ElideRight, 140)
        self.title_label.setText(elided_title)
        
        metrics_artist = QFontMetrics(self.artist_label.font())
        elided_artist = metrics_artist.elidedText(raw_artist, Qt.ElideRight, 140)
        self.artist_label.setText(elided_artist)