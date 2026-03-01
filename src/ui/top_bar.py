from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal

class TopBar(QWidget):
    # Custom signals to tell the main UI when something happens
    search_changed = Signal(str)
    settings_clicked = Signal()
    refresh_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        self.setStyleSheet("""
            TopBar {
                background-color: transparent;
                border-bottom: 1px solid #1C1C1C; /* Soft separator from the song list */
            }
            QLabel {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: bold;
                border: none;
            }
            QLineEdit {
                background-color: #141414;
                color: #FFFFFF;
                border: 1px solid #2A2A2A;
                border-radius: 15px; /* Pill-shaped search bar */
                padding: 5px 15px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #1DB954; /* Highlights green when typing */
                background-color: #1A1A1A;
            }
            QPushButton {
                background-color: transparent;
                color: #AAAAAA;
                font-size: 18px;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #2A2A2A;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 10, 25, 10)
        layout.setSpacing(15)

        # 1. Title
        self.title_label = QLabel("Library")
        
        # 2. Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search songs...")
        self.search_bar.setFixedWidth(250)
        # Emit the text every time a letter is typed
        self.search_bar.textChanged.connect(self.search_changed.emit)

        # 3. Action Buttons
        self.refresh_btn = QPushButton("⟳")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setToolTip("Refresh Library")
        self.refresh_btn.clicked.connect(self.refresh_clicked.emit)

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.setToolTip("Settings & Folders")
        self.settings_btn.clicked.connect(self.settings_clicked.emit)

        # --- Add to Layout ---
        layout.addWidget(self.title_label)
        layout.addStretch() # This pushes the search bar and buttons to the right
        layout.addWidget(self.search_bar)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.settings_btn)