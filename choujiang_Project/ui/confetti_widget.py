# ui/confetti_widget.py

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QPainter, QColor
import random


class ConfettiParticle(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.emojis = ["🎉", "🎊", "✨", "🎁", "🎈", "💎", "🌟", "💫", "🎀", "💝"]
        self.setText(random.choice(self.emojis))
        self.setFont(QFont("Arial", 20))
        self.setStyleSheet("background: transparent;")
        
    def start_fall(self, start_x, start_y, end_y, duration):
        self.move(start_x, start_y)
        self.show()
        
        # 随机水平偏移
        end_x = start_x + random.randint(-150, 150)
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(duration)
        self.anim.setStartValue(QPoint(start_x, start_y))
        self.anim.setEndValue(QPoint(end_x, end_y))
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.finished.connect(self.deleteLater)
        self.anim.start()


class ConfettiWidget(QWidget):
    """彩带撒花效果 - 直接在父窗口内显示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # 不阻挡鼠标事件
        self.particles = []
        
    def show_confetti(self, count=60):
        # 获取父窗口尺寸并调整自身大小
        if self.parent():
            self.setGeometry(self.parent().rect())
        
        self.show()
        self.raise_()  # 置于顶层
        
        parent_width = self.width()
        parent_height = self.height()
        
        # 创建粒子
        for i in range(count):
            particle = ConfettiParticle(self)
            
            # 随机起始位置（从顶部不同位置）
            start_x = random.randint(0, parent_width)
            start_y = random.randint(-50, 0)
            end_y = parent_height + 50
            
            # 随机持续时间
            duration = random.randint(1500, 3000)
            
            # 延迟启动，产生波浪效果
            QTimer.singleShot(i * 30, lambda p=particle, sx=start_x, sy=start_y, ey=end_y, d=duration: 
                              p.start_fall(sx, sy, ey, d))
            
            self.particles.append(particle)
        
        # 动画结束后清理
        QTimer.singleShot(4000, self._cleanup)
    
    def _cleanup(self):
        self.particles.clear()
        self.hide()
    
    def paintEvent(self, event):
        # 不绘制任何背景，完全透明
        pass
