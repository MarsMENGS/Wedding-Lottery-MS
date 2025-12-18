# ui/setup_page.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QLineEdit, QSpinBox, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox,
    QGraphicsDropShadowEffect, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class Card(QFrame):
    """macOS风格卡片容器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)


class SetupPage(QWidget):
    save_requested = Signal(int, int, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #f5f5f7;")
        self.init_ui()

    def init_ui(self):
        # 主滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(24)
        layout.setContentsMargins(40, 30, 40, 30)

        # 顶部标题
        header = QFrame()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("⚙️ 奖项设置")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1d1d1f;
        """)
        
        subtitle = QLabel("配置抽奖号码范围和奖项信息")
        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #86868b;
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        # === 号码范围卡片 ===
        range_card = Card()
        range_layout = QVBoxLayout(range_card)
        range_layout.setContentsMargins(28, 24, 28, 24)
        range_layout.setSpacing(16)
        
        range_title = QLabel("🔢 号码范围")
        range_title.setStyleSheet("""
            font-size: 17px;
            font-weight: 600;
            color: #1d1d1f;
        """)
        
        range_hint = QLabel("系统将自动排除含数字「4」的号码")
        range_hint.setStyleSheet("font-size: 13px; color: #86868b;")
        
        range_input_layout = QHBoxLayout()
        range_input_layout.setSpacing(16)
        
        self.start_input = QSpinBox()
        self.end_input = QSpinBox()
        self.start_input.setRange(1, 9999)
        self.end_input.setRange(1, 9999)
        self.start_input.setValue(1)
        self.end_input.setValue(200)
        
        spinbox_style = """
            QSpinBox {
                padding: 12px 16px;
                border: 2px solid #e5e5e5;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 500;
                background: white;
                color: #1d1d1f;
                min-width: 100px;
            }
            QSpinBox:focus {
                border-color: #667eea;
                background: white;
            }
        """
        self.start_input.setStyleSheet(spinbox_style)
        self.end_input.setStyleSheet(spinbox_style)
        
        start_label = QLabel("起始号码")
        end_label = QLabel("结束号码")
        dash_label = QLabel("—")
        for lbl in [start_label, end_label]:
            lbl.setStyleSheet("font-size: 14px; color: #86868b; font-weight: 500;")
        dash_label.setStyleSheet("font-size: 20px; color: #c7c7cc;")
        
        range_input_layout.addWidget(start_label)
        range_input_layout.addWidget(self.start_input)
        range_input_layout.addWidget(dash_label)
        range_input_layout.addWidget(end_label)
        range_input_layout.addWidget(self.end_input)
        range_input_layout.addStretch()
        
        range_layout.addWidget(range_title)
        range_layout.addWidget(range_hint)
        range_layout.addLayout(range_input_layout)

        # === 奖项配置卡片 ===
        prize_card = Card()
        prize_layout = QVBoxLayout(prize_card)
        prize_layout.setContentsMargins(28, 24, 28, 24)
        prize_layout.setSpacing(16)
        
        prize_title = QLabel("🏆 奖项配置")
        prize_title.setStyleSheet("""
            font-size: 17px;
            font-weight: 600;
            color: #1d1d1f;
        """)
        
        # 添加奖项输入
        add_layout = QHBoxLayout()
        add_layout.setSpacing(12)
        
        self.prize_name_input = QLineEdit()
        self.prize_name_input.setPlaceholderText("奖品名称，如：一等奖")
        self.prize_name_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e5e5e5;
                border-radius: 10px;
                font-size: 15px;
                background: white;
                color: #1d1d1f;
                min-width: 180px;
            }
            QLineEdit:focus {
                border-color: #667eea;
                background: white;
            }
            QLineEdit::placeholder {
                color: #aaaaaa;
            }
        """)
        
        self.prize_count_input = QSpinBox()
        self.prize_count_input.setRange(1, 100)
        self.prize_count_input.setValue(1)
        self.prize_count_input.setStyleSheet(spinbox_style)
        
        self.add_prize_btn = QPushButton("➕ 添加")
        self.add_prize_btn.setCursor(Qt.PointingHandCursor)
        self.add_prize_btn.setStyleSheet("""
            QPushButton {
                background: #34c759;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #2db84d;
            }
        """)
        self.add_prize_btn.clicked.connect(self.add_prize)
        
        count_label = QLabel("人数")
        count_label.setStyleSheet("font-size: 14px; color: #86868b; font-weight: 500;")
        
        add_layout.addWidget(self.prize_name_input)
        add_layout.addWidget(count_label)
        add_layout.addWidget(self.prize_count_input)
        add_layout.addWidget(self.add_prize_btn)
        add_layout.addStretch()
        
        # 奖项列表
        self.prize_list = QListWidget()
        self.prize_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e5e5e5;
                border-radius: 12px;
                padding: 8px;
                background: white;
                font-size: 15px;
                color: #1d1d1f;
            }
            QListWidget::item {
                padding: 14px 16px;
                border-radius: 8px;
                margin: 2px 0;
                color: #1d1d1f;
            }
            QListWidget::item:selected {
                background: #667eea;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background: #f5f5fa;
            }
        """)
        self.prize_list.setMinimumHeight(200)
        
        # 删除按钮
        self.delete_btn = QPushButton("🗑️ 删除选中")
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background: #ff3b30;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #e5352b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_prize)
        
        prize_layout.addWidget(prize_title)
        prize_layout.addLayout(add_layout)
        prize_layout.addWidget(self.prize_list)
        prize_layout.addWidget(self.delete_btn, alignment=Qt.AlignRight)

        # === 保存按钮 ===
        self.save_btn = QPushButton("💾  保存配置并开始抽奖")
        self.save_btn.setFixedHeight(56)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 17px;
                font-weight: 600;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd6, stop:1 #6a4190);
            }
        """)
        self.save_btn.clicked.connect(self.validate_and_save)

        # 组装布局
        layout.addWidget(header)
        layout.addWidget(range_card)
        layout.addWidget(prize_card)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def add_prize(self):
        name = self.prize_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "提示", "请输入奖品名称")
            return
        count = self.prize_count_input.value()
        item = QListWidgetItem(f"🎁  {name}    ×{count}人")
        item.setData(Qt.UserRole, {"name": name, "count": count})
        self.prize_list.addItem(item)
        self.prize_name_input.clear()
        self.prize_count_input.setValue(1)
        self.prize_name_input.setFocus()

    def delete_prize(self):
        current = self.prize_list.currentRow()
        if current >= 0:
            self.prize_list.takeItem(current)

    def validate_and_save(self):
        if self.prize_list.count() == 0:
            QMessageBox.warning(self, "提示", "请至少添加一个奖项")
            return
        start = self.start_input.value()
        end = self.end_input.value()
        if start >= end:
            QMessageBox.warning(self, "提示", "起始号码必须小于结束号码")
            return
        prizes = [
            self.prize_list.item(i).data(Qt.UserRole)
            for i in range(self.prize_list.count())
        ]
        self.save_requested.emit(start, end, prizes)
