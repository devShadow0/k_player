from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, current_directories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 350)
        
        # Make it frameless to match our widget theme
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                border: 1px solid #2A2A2A;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QListWidget {
                background-color: #0A0A0A;
                color: #CCCCCC;
                border: 1px solid #1C1C1C;
                border-radius: 5px;
                padding: 5px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #1A1A1A;
                color: white;
                border: 1px solid #2A2A2A;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover { background-color: #2A2A2A; }
            QPushButton#SaveBtn {
                background-color: #1DB954;
                color: black;
                font-weight: bold;
                border: none;
            }
            QPushButton#SaveBtn:hover { background-color: #1ed760; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 1. Header
        self.header_label = QLabel("Music Folders")
        self.header_label.setStyleSheet("padding-bottom:5px; padding-top:5px;")
        layout.addWidget(self.header_label)

        # 2. List of current folders
        self.folder_list = QListWidget()
        self.folder_list.addItems(current_directories)
        layout.addWidget(self.folder_list)

        # 3. Action Buttons (Add/Remove)
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("+ Add Folder")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_folder)
        
        self.remove_btn = QPushButton("- Remove Selected")
        self.remove_btn.setCursor(Qt.PointingHandCursor)
        self.remove_btn.clicked.connect(self.remove_folder)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        layout.addLayout(btn_layout)

        # 4. Save and Cancel Buttons
        bottom_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject) # Closes dialog without saving
        
        self.save_btn = QPushButton("Save & Apply")
        self.save_btn.setObjectName("SaveBtn") # Triggers the special green CSS
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.accept) # Closes dialog and returns Success
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.cancel_btn)
        bottom_layout.addWidget(self.save_btn)
        layout.addLayout(bottom_layout)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            # Check for duplicates before adding
            existing = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
            if folder not in existing:
                self.folder_list.addItem(folder)

    def remove_folder(self):
        selected_items = self.folder_list.selectedItems()
        if not selected_items: return
        for item in selected_items:
            self.folder_list.takeItem(self.folder_list.row(item))

    def get_directories(self):
        return [self.folder_list.item(i).text() for i in range(self.folder_list.count())]