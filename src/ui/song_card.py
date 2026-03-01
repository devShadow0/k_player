import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

class SongCard(QWidget):
    clicked = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
        self.setFixedHeight(75) # Slightly slimmer
        self.setStyleSheet("""
            SongCard {
                background-color: transparent;
                border-bottom: 1px solid #1A1A1A; /* Minimalist separator */
                border-radius: 8px; /* Rounded corners for hover state */
            }
            SongCard:hover {
                background-color: #141414; /* Very subtle hover highlight */
                border-bottom: 1px solid transparent; /* Hide separator on hover */
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 20, 10)
        
        self.art_label = QLabel()
        self.art_label.setFixedSize(50, 50) # Slightly smaller art
        self.art_label.setStyleSheet("background-color: #222; border-radius: 6px;")
        
        info_layout = QVBoxLayout()
        self.title_label = QLabel(os.path.basename(file_path))
        self.title_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #E0E0E0;")
        self.artist_label = QLabel("Unknown Artist")
        self.artist_label.setStyleSheet("font-size: 12px; color: #888888;")
        
        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.artist_label)
        info_layout.setAlignment(Qt.AlignVCenter)
        
        self.duration_label = QLabel("0:00")
        self.duration_label.setStyleSheet("font-size: 13px; color: #666666;")
        
        layout.addWidget(self.art_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(self.duration_label)
        
        self.parse_metadata()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.file_path)
        super().mousePressEvent(event)

    def parse_metadata(self):
        try:
            audio = MP3(self.file_path, ID3=ID3)
            duration = int(audio.info.length)
            mins, secs = divmod(duration, 60)
            self.duration_label.setText(f"{mins}:{secs:02d}")
            
            if audio.tags:
                if "TIT2" in audio.tags:
                    self.title_label.setText(str(audio.tags["TIT2"]))
                if "TPE1" in audio.tags:
                    self.artist_label.setText(str(audio.tags["TPE1"]))
                    
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