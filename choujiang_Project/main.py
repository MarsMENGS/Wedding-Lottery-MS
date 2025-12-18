# main.py

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_window import MainWindow
from core.lottery_engine import LotteryEngine


def main():
    app = QApplication(sys.argv)
    font = QFont("PingFang SC", 12)
    app.setFont(font)

    engine = LotteryEngine()  # ✅ 空初始化

    window = MainWindow(engine)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()