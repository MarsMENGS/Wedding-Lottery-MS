# ========== 日志初始化（必须放在最顶部）==========
import sys
import os
import traceback

# 定义日志文件路径（和EXE同目录的log.txt）
def get_log_path():
    if hasattr(sys, '_MEIPASS'):
        # 打包后：EXE所在目录
        exe_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境：项目根目录
        exe_dir = os.path.abspath('.')
    return os.path.join(exe_dir, '启动日志.txt')

# 初始化日志（覆盖旧日志）
LOG_PATH = get_log_path()
with open(LOG_PATH, 'w', encoding='utf-8') as f:
    f.write(f"=== 程序启动日志 ===\n时间：{os.path.getctime(LOG_PATH)}\nPython版本：{sys.version}\n系统：{sys.platform}\n架构：{sys.maxsize > 2**32 and '64位' or '32位'}\nEXE路径：{sys.executable if hasattr(sys, '_MEIPASS') else '开发环境'}\n\n")

# 自定义日志函数（同时写文件+控制台）
def log(msg):
    print(f"[LOG] {msg}")  # 控制台输出
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"[LOG] {msg}\n")

# 自定义异常捕获函数
def log_exception(e):
    err_msg = f"[ERROR] {type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    print(err_msg)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{err_msg}\n")

# ========== 第一步：日志初始化完成 ==========
log("1. 日志系统初始化完成，开始加载基础依赖")

try:
    # 配置Qt插件路径（关键！）
    log("2. 配置Qt插件路径")
    if hasattr(sys, '_MEIPASS'):
        # 打包后：从COLLECT文件夹加载插件
        plugin_path = os.path.join(os.path.dirname(sys.executable), 'platforms')
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
        os.environ['QT_DEBUG_PLUGINS'] = '1'  # 开启Qt插件调试
        log(f"   Qt插件路径：{plugin_path}，是否存在：{os.path.exists(plugin_path)}")
    else:
        plugin_path = os.path.join(os.path.abspath('.'), 'platforms')
        log(f"   开发环境Qt插件路径：{plugin_path}")

    # 加载PySide6
    log("3. 开始导入PySide6模块")
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon
    log("   PySide6导入成功")

    # 加载自定义模块（适配你的number_validator.py）
    log("4. 开始导入自定义模块")
    try:
        from utils.resource_path import resource_path
        log("   utils.resource_path导入成功")
    except Exception as e:
        log_exception(e)
        raise

    try:
        # ========== 关键修正：导入number_validator中的函数 ==========
        from core.number_validator import contains_digit_4, filter_numbers_without_4, is_valid_gap
        from core.lottery_engine import LotteryEngine
        log("   core模块（抽奖引擎/号码验证）导入成功")
    except Exception as e:
        log_exception(e)
        raise

    try:
        from ui.main_window import MainWindow
        log("   ui.main_window导入成功")
    except Exception as e:
        log_exception(e)
        raise

    # 初始化QApplication
    log("5. 初始化QApplication")
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    log("   QApplication初始化成功")

    # 加载资源文件
    log("6. 加载资源文件（图标/QSS）")
    try:
        logo_path = resource_path("resources/logo.ico")
        log(f"   图标路径：{logo_path}，是否存在：{os.path.exists(logo_path)}")
        app.setWindowIcon(QIcon(logo_path))

        qss_path = resource_path("resources/styles/macos.qss")
        log(f"   QSS路径：{qss_path}，是否存在：{os.path.exists(qss_path)}")
        if os.path.exists(qss_path):
            # with open(qss_path, 'r', encoding='utf-8') as f:
            #     # app.setStyleSheet(f.read())
            log("   QSS样式表加载成功")
        else:
            log("   QSS文件不存在，使用默认样式")
    except Exception as e:
        log_exception(e)
        raise

    # 启动主窗口
    log("7. 初始化主窗口，准备启动程序")
    try:
        engine = LotteryEngine()
        window = MainWindow(engine)
        window.show()
        log("8. 主窗口显示成功，程序启动完成")
    except Exception as e:
        log_exception(e)
        raise

    # 运行程序
    sys.exit(app.exec())

except Exception as e:
    log_exception(e)
    log("程序启动失败，按任意键退出...")
    input()  # 暂停控制台
    sys.exit(1)