# ui/side_menu.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class SideMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setStyleSheet("""
            background: white;
            border-right: 1px solid #e6f7ff;
            border-radius: 16px;
            padding: 20px 0;
        """)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        self.add_item("🏠 首页", "home.png")  # 图标占位
        self.add_item("⚙️ 设置", "settings.png")
        self.add_item("📊 统计", "stats.png")
        self.add_item("📤 导出结果", "export.png")

    def add_item(self, text, icon_path=""):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            color: #555;
            font-size: 14px;
            background: transparent;
            margin-left: -15px;
        """)
        btn.clicked.connect(lambda: self.on_click(text))
        self.layout.addWidget(btn)

    def on_click(self, text):
        print(f"点击了：{text}")