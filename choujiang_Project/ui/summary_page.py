# ui/summary_page.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QScrollArea, QGraphicsDropShadowEffect,
    QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QBrush


class PrizeCard(QFrame):
    """奖项展示卡片 - 渐变背景"""
    
    # 不同奖项的渐变色
    GRADIENTS = [
        ("#667eea", "#764ba2", "#f093fb"),  # 一等奖 - 紫色渐变
        ("#11998e", "#38ef7d", "#56ccf2"),  # 二等奖 - 青绿渐变  
        ("#f093fb", "#f5576c", "#ff9966"),  # 三等奖 - 粉橙渐变
        ("#4facfe", "#00f2fe", "#43e97b"),  # 四等奖 - 蓝绿渐变
        ("#fa709a", "#fee140", "#f8b500"),  # 五等奖 - 粉黄渐变
    ]
    
    def __init__(self, prize_name, winners, index=0, parent=None):
        super().__init__(parent)
        self.prize_name = prize_name
        self.winners = winners
        self.gradient_colors = self.GRADIENTS[index % len(self.GRADIENTS)]
        
        self.setMinimumHeight(280)
        self.setStyleSheet("border-radius: 20px;")
        
        # 阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 奖项名称
        title = QLabel(self.prize_name)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: white;
            background: transparent;
            letter-spacing: 2px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # 分隔线
        line = QFrame()
        line.setFixedHeight(2)
        line.setStyleSheet("background: rgba(255,255,255,0.3); border: none;")
        
        # 中奖号码区域
        winners_container = QWidget()
        winners_container.setStyleSheet("background: transparent;")
        winners_layout = QHBoxLayout(winners_container)
        winners_layout.setSpacing(15)
        winners_layout.setAlignment(Qt.AlignCenter)
        
        for num in self.winners:
            num_label = QLabel(str(num))
            num_label.setFixedSize(70, 70)
            num_label.setAlignment(Qt.AlignCenter)
            num_label.setStyleSheet("""
                QLabel {
                    background: rgba(255, 255, 255, 0.25);
                    border-radius: 35px;
                    font-size: 26px;
                    font-weight: 700;
                    color: white;
                    border: 2px solid rgba(255,255,255,0.4);
                }
            """)
            winners_layout.addWidget(num_label)
        
        # 中奖人数
        count_label = QLabel(f"共 {len(self.winners)} 人中奖")
        count_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255,255,255,0.8);
            background: transparent;
        """)
        count_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(line)
        layout.addStretch()
        layout.addWidget(winners_container)
        layout.addWidget(count_label)
        layout.addStretch()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制渐变背景
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(self.gradient_colors[0]))
        gradient.setColorAt(0.5, QColor(self.gradient_colors[1]))
        gradient.setColorAt(1, QColor(self.gradient_colors[2]))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)


class SummaryPage(QWidget):
    """抽奖结果汇总页面"""
    
    reset_requested = Signal()  # 重新抽奖信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #1a1a2e;")
        self.results = {}  # {prize_name: [winners]}
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        # 顶部标题栏
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("🏆 抽奖结果汇总")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: white;
            letter-spacing: 2px;
        """)
        
        # 重新抽奖按钮
        self.reset_btn = QPushButton("🔄 重新抽奖")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 107, 107, 0.8);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255, 107, 107, 1);
            }
        """)
        self.reset_btn.clicked.connect(self.reset_requested.emit)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.reset_btn)
        
        # 副标题
        subtitle = QLabel("恭喜以下幸运嘉宾！")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: rgba(255,255,255,0.6);
        """)
        
        # 卡片滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)
        
        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.cards_layout = QHBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(25)
        self.cards_layout.setContentsMargins(10, 10, 10, 20)
        self.cards_layout.setAlignment(Qt.AlignCenter)
        
        scroll.setWidget(self.cards_container)
        
        layout.addWidget(header)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(scroll, 1)
    
    def update_results(self, prize_drawn: dict):
        """更新抽奖结果"""
        self.results = prize_drawn
        self.refresh_cards()
    
    def refresh_cards(self):
        """刷新卡片显示"""
        # 清除旧卡片
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 创建新卡片
        for i, (prize_name, winners) in enumerate(self.results.items()):
            if winners:  # 只显示有中奖者的奖项
                card = PrizeCard(prize_name, winners, i)
                card.setFixedWidth(300)
                self.cards_layout.addWidget(card)
    
    def clear_results(self):
        """清空结果"""
        self.results = {}
        self.refresh_cards()

