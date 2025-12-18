# ui/draw_page.py

from PySide6.QtWidgets import (
    QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect,
    QMessageBox, QScrollArea
)
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QColor
from .animated_label import AnimatedNumberLabel
from .confetti_widget import ConfettiWidget


class WinnerCard(QFrame):
    """中奖号码展示卡片"""
    def __init__(self, number, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(str(number))
        label.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: white;
            background: transparent;
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(102, 126, 234, 100))
        self.setGraphicsEffect(shadow)


class DrawPrizeWidget(QWidget):
    """单个奖项的抽奖界面"""
    
    prize_completed = Signal(str)  # 单个奖项完成信号
    
    def __init__(self, prize_name, prize_count, engine, existing_winners=None, parent=None):
        super().__init__(parent)
        self.prize_name = prize_name
        self.prize_count = prize_count
        self.engine = engine
        self.winner_list = existing_winners if existing_winners else []
        self.is_rolling = False
        self.init_ui()
        
        # 恢复已有结果的UI状态
        if self.winner_list:
            self._restore_ui_state()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(30)

        # 奖品名称
        self.title = QLabel(self.prize_name)
        self.title.setStyleSheet("""
            font-size: 42px;
            font-weight: 700;
            color: #1d1d1f;
            letter-spacing: 2px;
        """)
        self.title.setAlignment(Qt.AlignCenter)

        # 副标题
        self.subtitle = QLabel(f"共 {self.prize_count} 个名额")
        self.subtitle.setStyleSheet("""
            font-size: 16px;
            color: #86868b;
            font-weight: 500;
        """)
        self.subtitle.setAlignment(Qt.AlignCenter)

        # 号码显示区
        self.number_container = QFrame()
        self.number_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 24px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.number_container.setGraphicsEffect(shadow)
        
        number_layout = QVBoxLayout(self.number_container)
        number_layout.setContentsMargins(60, 50, 60, 50)
        
        self.number_label = AnimatedNumberLabel()
        number_layout.addWidget(self.number_label)

        # 按钮
        self.draw_btn = QPushButton("🎰  开始抽奖")
        self.draw_btn.setFixedSize(200, 56)
        self.draw_btn.setCursor(Qt.PointingHandCursor)
        self._set_btn_normal_style()
        self.draw_btn.clicked.connect(self.toggle_draw)

        # 中奖记录区域
        self.winner_section = QFrame()
        self.winner_section.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.6);
                border-radius: 16px;
            }
        """)
        winner_layout = QVBoxLayout(self.winner_section)
        winner_layout.setContentsMargins(20, 16, 20, 16)
        
        winner_title = QLabel("🏆 已中奖号码")
        winner_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #86868b;
        """)
        
        self.winner_cards_layout = QHBoxLayout()
        self.winner_cards_layout.setSpacing(12)
        self.winner_cards_layout.setAlignment(Qt.AlignCenter)
        
        self.no_winner_label = QLabel("暂无中奖")
        self.no_winner_label.setStyleSheet("color: #c7c7cc; font-size: 14px;")
        self.winner_cards_layout.addWidget(self.no_winner_label)
        
        winner_layout.addWidget(winner_title, alignment=Qt.AlignCenter)
        winner_layout.addLayout(self.winner_cards_layout)

        # 进度提示
        self.progress_label = QLabel(f"0 / {self.prize_count}")
        self.progress_label.setStyleSheet("""
            font-size: 14px;
            color: #86868b;
        """)
        self.progress_label.setAlignment(Qt.AlignCenter)

        # 布局
        layout.addStretch(1)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.number_container, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.draw_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.progress_label)
        layout.addStretch(1)
        layout.addWidget(self.winner_section)

    def _restore_ui_state(self):
        """恢复已有抽奖结果的UI状态"""
        self.no_winner_label.hide()
        
        for num in self.winner_list:
            card = WinnerCard(num, self)
            self.winner_cards_layout.addWidget(card)
        
        self.progress_label.setText(f"{len(self.winner_list)} / {self.prize_count}")
        
        if len(self.winner_list) >= self.prize_count:
            self.draw_btn.setText("✅ 已完成")
            self.draw_btn.setEnabled(False)
            self._set_btn_completed_style()
            # 显示最后一个中奖号码
            self.number_label.show_final_number(self.winner_list[-1])

    def _set_btn_normal_style(self):
        self.draw_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 18px;
                font-weight: 600;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd6, stop:1 #6a4190);
            }
            QPushButton:disabled {
                background: #d1d1d6;
                color: #86868b;
            }
        """)

    def _set_btn_stop_style(self):
        self.draw_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b6b, stop:1 #ee5a5a);
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 18px;
                font-weight: 600;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ee5a5a, stop:1 #dd4a4a);
            }
        """)

    def _set_btn_completed_style(self):
        self.draw_btn.setStyleSheet("""
            QPushButton {
                background: #34c759;
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 18px;
                font-weight: 600;
            }
        """)

    def toggle_draw(self):
        if self.is_rolling:
            self.stop_draw()
        else:
            self.start_draw()

    def start_draw(self):
        if len(self.winner_list) >= self.prize_count:
            QMessageBox.information(self, "提示", f"{self.prize_name} 已全部抽完！")
            return
            
        self.is_rolling = True
        self.draw_btn.setText("🛑  停止")
        self._set_btn_stop_style()
        
        if self.engine.valid_numbers:
            min_val = min(self.engine.valid_numbers)
            max_val = max(self.engine.valid_numbers)
            self.number_label.start_rolling(min_val, max_val)

    def stop_draw(self):
        self.is_rolling = False
        
        try:
            winner = self.engine.draw_once(self.prize_name)
            if winner is None:
                self.draw_btn.setText("已抽完")
                self.draw_btn.setEnabled(False)
                return

            self.winner_list.append(winner)
            self.number_label.stop_rolling(winner)
            
            QTimer.singleShot(2600, lambda: self.on_draw_complete(winner))

        except Exception as e:
            self._set_btn_normal_style()
            self.draw_btn.setText("🎰  开始抽奖")
            QMessageBox.critical(self, "错误", f"抽奖失败：{str(e)}")

    def on_draw_complete(self, winner):
        if self.no_winner_label.isVisible():
            self.no_winner_label.hide()
        
        card = WinnerCard(winner, self)
        self.winner_cards_layout.addWidget(card)
        
        self.progress_label.setText(f"{len(self.winner_list)} / {self.prize_count}")
        
        # 彩带效果
        main_window = self.window()
        if main_window:
            central = main_window.centralWidget()
            if central:
                self.confetti = ConfettiWidget(central)
                self.confetti.show_confetti(count=80)
        
        if len(self.winner_list) >= self.prize_count:
            self.draw_btn.setText("✅ 已完成")
            self.draw_btn.setEnabled(False)
            self._set_btn_completed_style()
            self.prize_completed.emit(self.prize_name)
        else:
            self.draw_btn.setText("🎰  开始抽奖")
            self._set_btn_normal_style()


class DrawPage(QWidget):
    all_prizes_completed = Signal()  # 所有奖项完成信号
    
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setStyleSheet("background: #f5f5f7;")
        self.prize_widgets = {}  # 保存奖项widget引用
        self.completed_prizes = set()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 顶部标题
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #e5e5e5;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        header_title = QLabel("🎯 抽奖中心")
        header_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #1d1d1f;
        """)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        # Tab切换
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #f5f5f7;
            }
            QTabBar::tab {
                background: transparent;
                padding: 14px 28px;
                margin-right: 4px;
                font-size: 15px;
                font-weight: 500;
                color: #86868b;
                border-bottom: 3px solid transparent;
            }
            QTabBar::tab:selected {
                color: #667eea;
                font-weight: 600;
                border-bottom: 3px solid #667eea;
            }
            QTabBar::tab:hover:!selected {
                color: #1d1d1f;
            }
        """)
        
        layout.addWidget(header)
        layout.addWidget(self.tab_widget)
        
        # 空状态提示
        self.empty_label = QLabel("请先在「奖项设置」中配置奖项")
        self.empty_label.setStyleSheet("""
            font-size: 18px;
            color: #86868b;
        """)
        self.empty_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.empty_label)
        self.empty_label.hide()

    def load_prizes(self, prizes):
        """加载奖项，保持已有结果"""
        if not prizes:
            self.tab_widget.hide()
            self.empty_label.show()
            return
        
        self.empty_label.hide()
        self.tab_widget.show()
        
        # 检查是否需要重建（奖项配置变化）
        current_names = {p["name"] for p in prizes}
        cached_names = set(self.prize_widgets.keys())
        
        if current_names != cached_names:
            # 配置变化，重建所有
            self.tab_widget.clear()
            self.prize_widgets.clear()
            self.completed_prizes.clear()
            
            for prize in prizes:
                existing = self.engine.prize_drawn.get(prize["name"], [])
                widget = DrawPrizeWidget(
                    prize["name"], prize["count"], self.engine, existing
                )
                widget.prize_completed.connect(self.on_prize_completed)
                self.prize_widgets[prize["name"]] = widget
                self.tab_widget.addTab(widget, f"  {prize['name']}  ")
                
                if len(existing) >= prize["count"]:
                    self.completed_prizes.add(prize["name"])
            
            # 检查是否全部完成
            if len(self.completed_prizes) == len(prizes):
                self.all_prizes_completed.emit()

    def on_prize_completed(self, prize_name):
        """单个奖项完成"""
        self.completed_prizes.add(prize_name)
        
        if len(self.completed_prizes) == len(self.engine.prizes):
            self.all_prizes_completed.emit()
