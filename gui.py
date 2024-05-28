from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from styles import Styles

class AnimatedToggle(QCheckBox):
    def __init__(
        self,
        width=80,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCff",
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.bg_color = bg_color
        self.circle_color = circle_color
        self.active_color = active_color

        self.value = False

        self.label = QLabel(self)
        self.label.setText("Dark")
        self.label.setStyleSheet(Styles.dark_label_style)
        self.label.setFont(QFont("Segoe Script", 10))
        self.label.move(QPoint(29, 5))

        self.stateChanged.connect(self.change_value)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def change_value(self):
        if not self.value:
            self.value = True
        else:
            self.value = False

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)

        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self.bg_color))
            p.drawRoundedRect(
                0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
            )

            p.setBrush(QColor(self.circle_color))
            p.drawEllipse(3, 3, 22, 22)

        else:
            p.setBrush(QColor(self.active_color))
            p.drawRoundedRect(
                0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2
            )

            p.setBrush(QColor(self.circle_color))
            p.drawEllipse(self.width() - 26, 3, 22, 22)

        p.end()


class TranslationWindow(QWidget):
    def __init__(self, parent=None):
        super(TranslationWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.back_pixmap = QPixmap("icons/white_back_arrow.png")

        self.back_pc = QLabel()
        self.back_pc.setPixmap(self.back_pixmap.scaled(60, 60))

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.back_pc)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


class BootstrappingWindow(QWidget):
    def __init__(self, parent=None):
        super(BootstrappingWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.back_pixmap = QPixmap("icons/white_back_arrow.png")

        self.back_pc = QLabel()
        self.back_pc.setPixmap(self.back_pixmap.scaled(60, 60))

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.back_pc)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


class VersionWindow(QWidget):
    def __init__(self, parent=None):
        super(VersionWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.back_pixmap = QPixmap("icons/white_back_arrow.png")

        self.back_pc = QLabel()
        self.back_pc.setPixmap(self.back_pixmap.scaled(60, 60))

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.back_pc)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


class CreditsWindow(QWidget):
    def __init__(self, parent=None):
        super(CreditsWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.back_pixmap = QPixmap("icons/white_back_arrow.png")

        self.back_pc = QLabel()
        self.back_pc.setPixmap(self.back_pixmap.scaled(60, 60))

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.back_pc)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.back_pixmap = QPixmap("icons/white_back_arrow.png")

        self.back_pc = QLabel()
        self.back_pc.setPixmap(self.back_pixmap.scaled(60, 60))

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.back_pc)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.init()

    def init(self):
        self.main_layout = QHBoxLayout()
        self.layout_vertical = QVBoxLayout()

        self.top_left_layout = QHBoxLayout()

        self.settings_icon = QPixmap("icons/settings-icon.png")
        self.settings_icon_pc = QLabel()

        self.settings_icon = self.settings_icon.scaled(40, 40)

        self.settings_icon_pc.setPixmap(self.settings_icon)

        self.light_dark_toggle = AnimatedToggle()

        self.top_left_layout.addSpacing(15)
        self.top_left_layout.addWidget(self.settings_icon_pc)
        self.top_left_layout.addSpacing(15)
        self.top_left_layout.addWidget(self.light_dark_toggle)

        self.top_left_layout.addStretch()

        self.layout_vertical.addSpacing(15)
        self.layout_vertical.addLayout(self.top_left_layout)

        self.central_text_layout = QHBoxLayout()

        self.logo = QPixmap("icons/python_docs_tr-logo.png")

        self.logo_pc = QLabel()
        self.logo_pc.setPixmap(self.logo.scaled(200, 200))

        self.central_text_layout.addWidget(self.logo_pc)

        self.central_text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.python_docs_tr_label = QLabel(
            """Python
Docs
TR"""
        )

        self.python_docs_tr_label.setStyleSheet(Styles.dark_label_style)
        self.python_docs_tr_label.setFont(QFont("Arial", 50))

        self.central_text_layout.addWidget(self.python_docs_tr_label)

        self.buttons_layout = QVBoxLayout()

        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.translation = QPushButton("Translation")
        self.translation.setStyleSheet(Styles.light_mode_button_style)

        self.bootstrapping = QPushButton("Bootstrapping")
        self.bootstrapping.setStyleSheet(Styles.light_mode_button_style)

        self.version_history = QPushButton("Version History")
        self.version_history.setStyleSheet(Styles.light_mode_button_style)

        self.credits = QPushButton("Credits")
        self.credits.setStyleSheet(Styles.light_mode_button_style)

        self.quit = QPushButton("Quit")
        self.quit.setStyleSheet(Styles.light_mode_button_style)

        self.buttons_layout.addWidget(self.translation)
        self.buttons_layout.addWidget(self.bootstrapping)
        self.buttons_layout.addWidget(self.version_history)
        self.buttons_layout.addWidget(self.credits)
        self.buttons_layout.addWidget(self.quit)

        self.layout_vertical.addSpacing(70)

        self.layout_vertical.addLayout(self.central_text_layout)

        self.layout_vertical.addSpacing(30)

        self.layout_vertical.addLayout(self.buttons_layout)

        self.layout_vertical.addStretch()

        self.setLayout(self.layout_vertical)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStyleSheet(Styles.main_window_background_dark)
        self.setGeometry(400, 200, 1200, 600)
        self.startMainMenu()

    def startMainMenu(self, *args):
        self.window = Window()
        self.window.settings_icon_pc.mousePressEvent = self.startSettings
        self.window.light_dark_toggle.stateChanged.connect(self.change_theme)

        self.window.translation.clicked.connect(self.startTranslation)
        self.window.bootstrapping.clicked.connect(self.startBootstrapping)
        self.window.version_history.clicked.connect(self.startVersionHistory)
        self.window.credits.clicked.connect(self.startCredits)
        self.window.quit.clicked.connect(self.quit)

        self.setWindowTitle("Python Docs TR Management App")
        self.setCentralWidget(self.window)
        self.showMaximized()

    def startCredits(self):
        self.window = CreditsWindow()
        self.window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.window)
        self.showMaximized()

    def startVersionHistory(self):
        self.window = VersionWindow()
        self.window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.window)
        self.showMaximized()

    def startBootstrapping(self):
        self.window = BootstrappingWindow()
        self.window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.window)
        self.showMaximized()

    def startTranslation(self):
        self.window = TranslationWindow()
        self.window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.window)
        self.showMaximized()

    def startSettings(self, *args):
        self.window = SettingsWindow()
        self.window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.window)
        self.showMaximized()

    def quit(self):
        sys.exit()

    def change_theme(self):
        if self.window.light_dark_toggle.value:
            w.setStyleSheet(Styles.main_window_background_light)
            self.window.light_dark_toggle.label.setText("Light")
            self.window.light_dark_toggle.label.move(QPoint(7, 5))

            self.window.translation.setStyleSheet(Styles.dark_mode_button_style)
            self.window.bootstrapping.setStyleSheet(Styles.dark_mode_button_style)
            self.window.version_history.setStyleSheet(Styles.dark_mode_button_style)
            self.window.credits.setStyleSheet(Styles.dark_mode_button_style)
            self.window.quit.setStyleSheet(Styles.dark_mode_button_style)

            self.window.python_docs_tr_label.setStyleSheet(Styles.light_label_style)

        else:
            w.setStyleSheet(Styles.main_window_background_dark)
            self.window.light_dark_toggle.label.setText("Dark")
            self.window.light_dark_toggle.label.move(QPoint(29, 5))

            self.window.translation.setStyleSheet(Styles.light_mode_button_style)
            self.window.bootstrapping.setStyleSheet(Styles.light_mode_button_style)
            self.window.version_history.setStyleSheet(Styles.light_mode_button_style)
            self.window.credits.setStyleSheet(Styles.light_mode_button_style)
            self.window.quit.setStyleSheet(Styles.light_mode_button_style)

            self.window.python_docs_tr_label.setStyleSheet(Styles.dark_label_style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
