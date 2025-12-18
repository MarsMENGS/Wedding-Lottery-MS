# ui/rounded_card.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush


class RoundedCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet("""
            background: white;
            border-radius: 16px;
            border: 1px solid #e6f7ff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 20px;
        """)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addStretch(self):
        self.layout.addStretch()