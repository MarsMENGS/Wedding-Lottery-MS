# ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QLabel, QPushButton, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from .draw_page import DrawPage
from .setup_page import SetupPage
from .summary_page import SummaryPage


class NavButton(QPushButton):
    """导航按钮"""
    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.setText(f"{icon}  {text}")
        self.setCheckable(True)
        self.setFixedHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style(False)
    
    def _update_style(self, selected):
        if selected:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.95);
                    border: none;
                    border-radius: 12px;
                    padding: 12px 20px;
                    font-size: 15px;
                    font-weight: 600;
                    color: #5a4a78;
                    text-align: left;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.15);
                    border: none;
                    border-radius: 12px;
                    padding: 12px 20px;
                    font-size: 15px;
                    font-weight: 500;
                    color: #ffffff;
                    text-align: left;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.3);
                    color: #ffffff;
                }
            """)
    
    def setChecked(self, checked):
        super().setChecked(checked)
        self._update_style(checked)


class SideBar(QWidget):
    """侧边栏"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 30, 16, 30)
        self.layout.setSpacing(8)
        
        # Logo区域
        logo_label = QLabel("💒")
        logo_label.setStyleSheet("font-size: 48px; background: transparent;")
        logo_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("婚礼抽奖")
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            background: transparent;
            letter-spacing: 2px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Lucky Draw System")
        subtitle.setStyleSheet("""
            font-size: 11px;
            color: rgba(255, 255, 255, 0.7);
            background: transparent;
            letter-spacing: 1px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(logo_label)
        self.layout.addWidget(title_label)
        self.layout.addWidget(subtitle)
        self.layout.addSpacing(40)
        
        # 导航按钮
        self.nav_buttons = []
        self.draw_btn = NavButton("🎯", "开始抽奖")
        self.setup_btn = NavButton("⚙️", "奖项设置")
        self.summary_btn = NavButton("🏆", "抽奖结果")
        self.summary_btn.hide()  # 默认隐藏
        
        self.nav_buttons = [self.draw_btn, self.setup_btn, self.summary_btn]
        
        for btn in self.nav_buttons:
            self.layout.addWidget(btn)
        
        self.layout.addStretch()
        
        # 底部版权
        footer = QLabel("Made By Mars ❤️")
        footer.setStyleSheet("""
            font-size: 11px;
            color: rgba(100, 0, 255, 0.6);
            background: transparent;
        """)
        footer.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(footer)
    
    def show_summary_btn(self):
        self.summary_btn.show()
    
    def hide_summary_btn(self):
        self.summary_btn.hide()


class MainWindow(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setWindowTitle("婚礼抽奖系统")
        self.resize(1920, 1080)
        self.setMinimumSize(1920, 1080)
        self.setup_ui()
        self.apply_global_style()


    # 设置侧边栏颜色
    def apply_global_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #fffdd;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 侧边栏
        self.sidebar = SideBar()
        self.sidebar.draw_btn.clicked.connect(lambda: self.switch_page(0))
        self.sidebar.setup_btn.clicked.connect(lambda: self.switch_page(1))
        self.sidebar.summary_btn.clicked.connect(lambda: self.switch_page(2))

        # 内容区
        self.stacked = QStackedWidget()
        self.stacked.setStyleSheet("""
            QStackedWidget {
                background: #fffdd;
            }
        """)

        # 抽奖页
        self.draw_page = DrawPage(self.engine)
        self.draw_page.all_prizes_completed.connect(self.on_all_completed)
        self.stacked.addWidget(self.draw_page)

        # 设置页
        self.setup_page = SetupPage()
        self.setup_page.save_requested.connect(self.on_settings_saved)
        self.stacked.addWidget(self.setup_page)
        
        # 汇总页
        self.summary_page = SummaryPage()
        self.summary_page.reset_requested.connect(self.on_reset_lottery)
        self.stacked.addWidget(self.summary_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked)

        # 默认页面
        if self.engine.prizes:
            self.switch_page(0)
        else:
            self.switch_page(1)

    def switch_page(self, index):
        self.stacked.setCurrentIndex(index)
        
        # 更新按钮状态
        for i, btn in enumerate(self.sidebar.nav_buttons):
            btn.setChecked(i == index)
        
        # 刷新页面数据
        if index == 0:
            self.draw_page.load_prizes(self.engine.prizes)
        elif index == 2:
            self.summary_page.update_results(self.engine.prize_drawn)

    def on_settings_saved(self, start, end, prizes):
        try:
            self.engine.set_settings(start, end, prizes)
            # 隐藏汇总按钮（新配置）
            self.sidebar.hide_summary_btn()
            QMessageBox.information(
                self, "✅ 配置成功",
                f"号码范围：{start} ~ {end}\n"
                f"奖项数量：{len(prizes)} 项\n\n"
                "点击「开始抽奖」开始使用！"
            )
            self.switch_page(0)
        except ValueError as e:
            QMessageBox.critical(self, "❌ 配置错误", str(e))
    
    def on_all_completed(self):
        """所有奖项抽完时触发"""
        self.sidebar.show_summary_btn()
        self.summary_page.update_results(self.engine.prize_drawn)
    
    def on_reset_lottery(self):
        """重新抽奖"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要清空所有抽奖结果并重新开始吗？\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 重置引擎
            self.engine.used_numbers.clear()
            self.engine.prize_drawn = {p["name"]: [] for p in self.engine.prizes}
            # 重置UI
            self.sidebar.hide_summary_btn()
            self.summary_page.clear_results()
            self.draw_page.load_prizes(self.engine.prizes)
            self.switch_page(0)
            QMessageBox.information(self, "已重置", "抽奖已重置，可以重新开始！")
