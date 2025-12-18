# ui/animated_label.py

from PySide6.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor
import random


class AnimatedNumberLabel(QLabel):
    """带滚动动画的号码显示标签"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_number = 0
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(280, 140)
        self._set_idle_style()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_random_number)
        
        self.min_val = 1
        self.max_val = 999
        self.final_number = None
        self.is_stopping = False
        self.step = 0
        self.total_steps = 50

    def _set_idle_style(self):
        """待机状态样式"""
        self.setText("? ? ?")
        self.setGraphicsEffect(None)
        self.setStyleSheet("""
            QLabel {
                font-size: 72px;
                font-weight: 700;
                color: #c7c7cc;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f5f5f7);
                border-radius: 20px;
                letter-spacing: 8px;
            }
        """)
    
    def show_final_number(self, number):
        """直接显示最终号码（用于恢复状态）"""
        self.setText(str(number))
        self._set_winner_style()

    def _set_rolling_style(self):
        """滚动中样式"""
        self.setStyleSheet("""
            QLabel {
                font-size: 72px;
                font-weight: 700;
                color: #667eea;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f0ff);
                border-radius: 20px;
                letter-spacing: 4px;
            }
        """)

    def _set_winner_style(self):
        """中奖号码样式"""
        self.setStyleSheet("""
            QLabel {
                font-size: 80px;
                font-weight: 800;
                color: #ffffff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 20px;
                letter-spacing: 4px;
            }
        """)
        
        # 添加发光效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(102, 126, 234, 150))
        self.setGraphicsEffect(shadow)

    def start_rolling(self, min_val: int, max_val: int):
        """开始无限滚动"""
        self.min_val = min_val
        self.max_val = max_val
        self.is_stopping = False
        self.final_number = None
        self._set_rolling_style()
        self.timer.start(50)

    def stop_rolling(self, final_number: int):
        """停止滚动并显示最终号码"""
        self.final_number = final_number
        self.is_stopping = True
        self.step = 0
        self.total_steps = 50  # 2.5秒减速

    def start_animation(self, min_val: int, max_val: int, final_number: int, duration_ms: int = 2500):
        """兼容旧接口：直接开始并结束动画"""
        self.min_val = min_val
        self.max_val = max_val
        self.final_number = final_number
        self.step = 0
        self.total_steps = duration_ms // 50
        self.is_stopping = True
        self._set_rolling_style()
        self.timer.start(50)

    def _update_random_number(self):
        if self.is_stopping:
            self.step += 1
            if self.step >= self.total_steps:
                self.timer.stop()
                self.setText(str(self.final_number))
                self._set_winner_style()
                return

            # 减速效果：越接近结束，变化越慢
            progress = self.step / self.total_steps
            
            # 动态调整定时器间隔（减速）
            if progress > 0.7:
                self.timer.setInterval(int(50 + (progress - 0.7) * 300))
            
            # 号码逐渐靠近最终值
            if progress > 0.6:
                offset = int((1 - progress) * (self.max_val - self.min_val) / 3)
                low = max(self.min_val, self.final_number - offset)
                high = min(self.max_val, self.final_number + offset)
                num = random.randint(low, high)
            else:
                num = random.randint(self.min_val, self.max_val)
            
            self.setText(str(num))
        else:
            # 无限滚动模式
            num = random.randint(self.min_val, self.max_val)
            self.setText(str(num))
