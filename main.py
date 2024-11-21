import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFontDatabase, QFont

from widget import MaintWidget

from BlurWindow.blurWindow import blur

import asyncio
import qasync


def main():
    app = QtWidgets.QApplication(sys.argv)

    font_db = QFontDatabase()
    if font_db.addApplicationFont("fonts/Pretendard-Bold.ttf") == -1:
        print("Font loading failed. Using default font.")
    app.setFont(QFont("Pretendard"))

    chat_widget = MaintWidget(csv_path="./words.csv")
    chat_widget.setStyleSheet(
        "background-color: rgba(0, 0, 0, 0.4); border-radius: 30px;"
    )

    screen_geometry = app.primaryScreen().availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    widget_width = 650
    widget_height = 150
    x_position = screen_width - widget_width - 40
    y_position = screen_height - widget_height - 70

    chat_widget.setGeometry(x_position, y_position, widget_width, widget_height)
    chat_widget.show()

    try:
        blur(chat_widget.winId())
    except Exception as e:
        print(f"Blur effect failed: {e}")

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    main()
