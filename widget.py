from PyQt5 import QtWidgets, QtCore, QtGui
import pandas as pd
import random


class MaintWidget(QtWidgets.QWidget):
    def __init__(self, csv_path):
        super().__init__()
        self.is_dragging = False  # 드래그 상태를 추적
        self.mouse_start_position = None
        self.window_start_position = None

        # Load CSV file
        self.words_data = pd.read_csv(
            csv_path, names=["word", "meaning", "example", "sentence_meaning"]
        )
        self.current_index = random.randint(0, len(self.words_data) - 1)

        # Set window properties
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.mainWidget.setLayout(self.mainLayout)

        self.mainWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addStretch()

        self.contentLayout = QtWidgets.QHBoxLayout()
        self.contentLayout.setContentsMargins(20, 0, 20, 0)

        # Content label with HTML styling
        self.contentLabel = QtWidgets.QLabel()
        self.contentLabel.setStyleSheet(
            "color: white; font-size: 16px; background-color: rgba(0, 0, 0, 0);"
        )
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.contentLabel.setFixedWidth(550)

        self.contentLabel.mousePressEvent = self.mousePressEvent
        self.contentLabel.mouseMoveEvent = self.mouseMoveEvent
        self.contentLabel.mouseReleaseEvent = self.mouseReleaseEvent

        self.update_content()  # Initialize with the first word

        # Buttons
        self.button = QtWidgets.QPushButton()
        self.button.setIcon(
            QtGui.QIcon(QtGui.QPixmap("icons/refresh.png").scaled(16, 16))
        )
        self.button.setIconSize(QtCore.QSize(30, 30))

        self.button.setFixedSize(30, 30)
        self.button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
            }
            """
        )

        # Button click events
        self.button.clicked.connect(self.show_random_word)

        # Layouts
        self.contentLayout.addWidget(self.contentLabel)
        self.contentLayout.addStretch(1)
        self.contentLayout.addWidget(self.button)

        self.verticalLayout.addLayout(self.contentLayout)
        self.verticalLayout.addStretch()

        self.mainLayout.addLayout(self.verticalLayout)

        self.setLayout(self.mainLayout)

    def update_content(self):
        """Update the content label with the current word's information."""
        if 0 <= self.current_index < len(self.words_data):
            row = self.words_data.iloc[self.current_index]
            text = (
                f"<h2>{row['word']}</h2>"
                f"<p style='font-size: 16px; '>{row['meaning']}</p>"
                f"<p style='font-size: 14px; '><i>{row['example']}</i></p>"
                f"<p style='font-size: 14px;'>{row['sentence_meaning']}</p>"
            )
            self.contentLabel.setText(text)

    def show_random_word(self):
        """Show the previous word in the list."""
        self.current_index = random.randint(0, len(self.words_data) - 1)
        self.update_content()

    def mousePressEvent(self, event):
        """Handle mouse press event for dragging."""
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = True
            self.mouse_start_position = event.globalPos()
            self.window_start_position = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Handle mouse move event for dragging."""
        if self.is_dragging:
            current_position = event.globalPos()
            offset = current_position - self.mouse_start_position
            self.move(self.window_start_position + offset)

    def mouseReleaseEvent(self, event):
        """Handle mouse release event for dragging."""
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = False
