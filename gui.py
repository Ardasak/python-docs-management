# Imports necessary PyQt modules and other dependencies
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from styles import Styles
import polib  # For working with PO files
import os
import configparser  # For reading and writing configuration files
import deepl  # For translation using DeepL API
import bootstrapping  # Bootstrapping Code

# DeepL authentication key
auth_key = ""

# Creating a DeepL Translator object
translator = deepl.Translator(auth_key)

# Initializing configparser for reading from 'settings.ini'
parser = configparser.ConfigParser()
parser.read("settings.ini")


class BootstrappingDialog(QDialog):
    """Dialog for selecting version of bootstrapping"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Initialize UI components for BootstrappingDialog"""

        # Setting dialog title and geometry
        self.setWindowTitle("Bootstrapping Dialog")
        self.setGeometry(100, 100, 300, 150)

        # Creating main layout for the dialog
        self.layout = QVBoxLayout(self)

        # Adding a combo box with version options
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["3.10", "3.11", "3.12"])
        self.layout.addWidget(self.comboBox)

        # Adding button box with Apply and Cancel buttons
        self.button_box = QDialogButtonBox(self)
        self.cancel_button = self.button_box.addButton(
            QDialogButtonBox.StandardButton.Cancel
        )
        self.ok_button = self.button_box.addButton(
            QDialogButtonBox.StandardButton.Apply
        )

        self.ok_button.setDefault(True)

        self.layout.addWidget(self.button_box)

        # Connecting buttons to their functions
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(self.layout)


def save_changes():
    """Function to save changes to the settings.ini file"""
    with open("settings.ini", "w") as configfile:
        parser.write(configfile)


class ImageLabel(QLabel):
    """Custom QLabel for displaying images"""

    def __init__(self, path, scale):
        super().__init__()
        self.path = path
        back_pixmap = QPixmap(path)
        self.scale = scale
        self.setPixmap(back_pixmap.scaled(scale, scale))

    def changePixmap(self, source):
        """Change the displayed pixmap"""
        self.path = source
        self.setPixmap(QPixmap(source).scaled(self.scale, self.scale))


class AnimatedToggle(QCheckBox):
    """Custom QCheckBox for toggle functionality"""

    def __init__(
        self,
        width=80,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCff",
        last_value=False,
    ):
        QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.bg_color = bg_color
        self.circle_color = circle_color
        self.active_color = active_color

        self.last_value = last_value

        self.label = QLabel(self)
        self.label.setText("Dark")
        self.label.setStyleSheet(Styles.dark_label_style)
        self.label.setFont(QFont("Segoe Script", 10))
        self.label.move(QPoint(29, 5))

        self.stateChanged.connect(self.change_value)

    def hitButton(self, pos: QPoint):
        """Check if the button is clicked"""
        return self.contentsRect().contains(pos)

    def change_value(self):
        """Change the value of the toggle"""
        if not self.last_value:
            self.last_value = True
        else:
            self.last_value = False

    def paintEvent(self, e):
        """Paint the toggle button"""
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
    """Widget for translation functionality"""

    def __init__(self, toggle, parent=None):
        super(TranslationWindow, self).__init__(parent)
        self.toggle = toggle
        self.init()

    def init(self):
        """Initialize UI components for TranslationWindow"""

        # Creating ImageLabel instance for back button
        self.back_pc = ImageLabel("icons/white_back_arrow.png", 60)

        # Get last opened file path from settings.ini
        self.last_opened_file = parser.get("SETTINGS", "last_opened_file")
        self.pofile = None

        self.id_list_widget = QListWidget()
        self.id_list_widget.setStyleSheet(Styles.list_widget_style)
        self.id_list_widget.itemSelectionChanged.connect(
            lambda: self.on_selection_changed("id")
        )

        self.tr_list_widget = QListWidget()
        self.tr_list_widget.itemSelectionChanged.connect(
            lambda: self.on_selection_changed("tr")
        )
        self.tr_list_widget.setStyleSheet(Styles.list_widget_style)

        self.id_text_edit = QTextEdit(self)
        self.id_text_edit.setStyleSheet(Styles.text_edit_style)
        self.id_text_edit.setPlaceholderText("Select an entry.")
        self.id_text_edit.setReadOnly(True)

        self.tr_text_edit = QTextEdit(self)
        self.tr_text_edit.setStyleSheet(Styles.text_edit_style)
        self.tr_text_edit.setPlaceholderText("Type something here...")
        self.tr_text_edit.textChanged.connect(lambda: self.on_text_changed())

        self.set_fuzzy_checkbox = QCheckBox("Set Fuzzy")
        self.set_fuzzy_checkbox.setStyleSheet(Styles.checkbox_style)
        self.set_fuzzy_checkbox.stateChanged.connect(self.fuzzy_changed)

        # If last opened file doesn't exist, prompt user to select a file
        if not os.path.exists(self.last_opened_file):
            self.select_file()
        else:
            self.pofile = polib.pofile(self.last_opened_file)

        self.add_lists()

        # Setting up main layout and sub-layouts
        self.main_layout = QVBoxLayout()

        self.top_left_layout = QHBoxLayout()

        self.top_left_layout.addWidget(self.back_pc)
        self.top_left_layout.addWidget(self.toggle)
        self.top_left_layout.addStretch()

        self.center_layout = QHBoxLayout()

        # Adding widgets to center layout
        self.center_layout.addWidget(self.id_list_widget)
        self.center_layout.addWidget(self.tr_list_widget)

        # Setting up bottom layout and its sub-layouts
        self.bottom_layout = QHBoxLayout()
        self.bottom_left_layout = QVBoxLayout()
        self.bottom_right_layout = QVBoxLayout()
        self.bottom_right_all_file = QHBoxLayout()
        self.bottom_right_pick_file = QHBoxLayout()

        self.bottom_left_layout.addWidget(self.id_text_edit)
        self.bottom_left_layout.addWidget(self.tr_text_edit)

        # Adding translation related buttons
        self.translate_all_button = QPushButton("Translate File")
        self.translate_all_button.setStyleSheet(Styles.dark_button_style)
        self.translate_all_button.clicked.connect(self.translate_file)


        self.pickFile = QPushButton("Pick File")
        self.pickFile.setStyleSheet(Styles.dark_button_style)
        self.pickFile.clicked.connect(self.select_file)

        self.fuzzy_checkbox = QCheckBox("Only Fuzzies")
        self.fuzzy_checkbox.setStyleSheet(Styles.checkbox_style)

        self.translate_entry_button = QPushButton("Translate Entry")
        self.translate_entry_button.setStyleSheet(Styles.dark_button_style)
        self.translate_entry_button.clicked.connect(self.translate_entry)

        # Adding buttons to bottom right layout
        self.bottom_right_pick_file.addWidget(self.set_fuzzy_checkbox)
        self.bottom_right_pick_file.addWidget(self.pickFile)

        self.bottom_right_all_file.addWidget(self.translate_all_button)
        self.bottom_right_all_file.addWidget(self.fuzzy_checkbox)

        self.bottom_right_layout.addLayout(self.bottom_right_pick_file)
        self.bottom_right_layout.addLayout(self.bottom_right_all_file)
        self.bottom_right_layout.addWidget(self.translate_entry_button)

        # Adding bottom layouts to main layout
        self.bottom_layout.addLayout(self.bottom_left_layout)
        self.bottom_layout.addLayout(self.bottom_right_layout)

        # Adding all layouts to main layout
        self.main_layout.addLayout(self.top_left_layout)
        self.main_layout.addLayout(self.center_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)

    def add_lists(self):
        # Populate list widgets if pofile is not None
        if self.pofile != None:
            self.tr_text_edit.setEnabled(True)
            for entry in self.pofile:
                self.id_list_widget.addItem(QListWidgetItem(entry.msgid))
                self.tr_list_widget.addItem(QListWidgetItem(entry.msgstr))

        else:
            self.tr_text_edit.setEnabled(False)

    def select_file(self):
        self.pofile = None

        home_directory = os.path.expanduser("~")
        self.last_opened_file = QFileDialog.getOpenFileName(
            self,
            "Open File",
            home_directory,
            "PO Files (*.po)",
        )

        # If user selects a .po file, load it using polib
        if self.last_opened_file[0].endswith(".po"):
            self.pofile = polib.pofile(self.last_opened_file[0])
            parser.set("SETTINGS", "last_opened_file", self.last_opened_file[0])
            save_changes()

        self.id_list_widget.clear()
        self.tr_list_widget.clear()

        self.add_lists()

    def fuzzy_changed(self):
        """Handle changing fuzzy state of translation entries"""
        if not self.set_fuzzy_checkbox.isChecked():
            for entry in self.pofile.fuzzy_entries():
                if entry.msgid == self.id_list_widget.currentItem().text():
                    entry.flags.remove("fuzzy")
        else:
            for entry in self.pofile:
                if entry.msgid == self.id_list_widget.currentItem().text():
                    if not "fuzzy" in entry.flags:
                        entry.flags.append("fuzzy")

        self.pofile.save()

    def translate_file(self):
        """Translate all entries in the .po file"""
        for index, entry in enumerate(self.pofile):
            if self.fuzzy_checkbox.isChecked():
                if not "fuzzy" in entry.flags:
                    continue
            translation = translator.translate_text(entry.msgid, target_lang="TR").text
            entry.msgstr = translation

            self.tr_list_widget.item(index).setText(translation)

        self.id_list_widget.setCurrentRow(0)
        self.id_text_edit.setText(self.id_list_widget.currentItem().text())
        self.tr_text_edit.setText(self.tr_list_widget.currentItem().text())

        self.pofile.save()
        self.update()

    def translate_entry(self):
        """Translate the selected entry in the .po file"""
        for entry in self.pofile:
            if entry.msgid == self.id_list_widget.currentItem().text():
                translation = translator.translate_text(
                    entry.msgid, target_lang="TR"
                ).text
                entry.msgstr = translation
        self.pofile.save()

        self.tr_list_widget.item(self.tr_list_widget.currentRow()).setText(translation)
        self.tr_text_edit.setText(translation)

    def on_selection_changed(self, obj):
        """Handle selection change in list widgets"""
        if obj == "id":
            selected = self.id_list_widget.selectedItems()
            selected_index = self.id_list_widget.row(selected[0])
        else:
            selected = self.tr_list_widget.selectedItems()
            selected_index = self.tr_list_widget.row(selected[0])

        self.id_list_widget.setCurrentRow(selected_index)
        self.tr_list_widget.setCurrentRow(selected_index)

        if "fuzzy" in self.pofile[selected_index].flags:
            self.set_fuzzy_checkbox.setChecked(True)
        else:
            self.set_fuzzy_checkbox.setChecked(False)

        self.id_text_edit.setText(self.id_list_widget.currentItem().text())
        self.tr_text_edit.setText(self.tr_list_widget.currentItem().text())

    def on_text_changed(self):
        """Handle text change in translation text edit"""
        translation = self.tr_text_edit.toPlainText()

        for entry in self.pofile:
            if entry.msgid == self.id_list_widget.currentItem().text():
                entry.msgstr = translation
        self.pofile.save()

        self.tr_list_widget.item(self.tr_list_widget.currentRow()).setText(translation)


class CreditsWindow(QWidget):
    """Widget for displaying credits to DeepL API"""

    def __init__(self, toggle, parent=None):
        super(CreditsWindow, self).__init__(parent)
        self.toggle = toggle
        self.init()

    def init(self):
        """Initialize UI components for CreditsWindow"""
        # Creating ImageLabel instance for back button
        self.back_pc = ImageLabel("icons/white_back_arrow.png", 60)

        self.main_layout = QVBoxLayout()

        self.top_left_layout = QHBoxLayout()

        self.top_left_layout.addWidget(self.back_pc)
        self.top_left_layout.addWidget(self.toggle)
        self.top_left_layout.addStretch()

        self.main_layout.addLayout(self.top_left_layout)

        self.credits_logo = ImageLabel("icons/deepl_logo.png", 300)
        self.credits_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.credits_label = QLabel(self)
        self.credits_label.setText("Credits to DeepL API")
        self.credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.credits_label.setStyleSheet("font-size: 24px; color: #333;")

        self.credits_info = QLabel(self)
        self.credits_info.setText(
            "This application uses the DeepL API for translation services."
        )
        self.credits_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.credits_info.setStyleSheet("font-size: 16px; color: #666;")

        self.main_layout.addStretch()

        self.main_layout.addWidget(self.credits_logo)
        self.main_layout.addWidget(self.credits_label)
        self.main_layout.addWidget(self.credits_info)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


class Window(QWidget):
    """Main window widget with navigation buttons"""

    def __init__(self, toggle, parent=None):
        super(Window, self).__init__(parent)
        self.toggle = toggle
        self.init()

    def init(self):
        """Initialize UI components for Window"""
        self.main_layout = QHBoxLayout()
        self.layout_vertical = QVBoxLayout()

        self.top_left_layout = QHBoxLayout()

        self.top_left_layout.addSpacing(15)
        self.top_left_layout.addWidget(self.toggle)

        self.top_left_layout.addStretch()

        self.layout_vertical.addSpacing(15)
        self.layout_vertical.addLayout(self.top_left_layout)

        self.central_text_layout = QHBoxLayout()

        self.logo_pc = ImageLabel("icons/python_docs_tr-logo.png", 200)

        self.central_text_layout.addWidget(self.logo_pc)

        self.central_text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.python_docs_tr_label = QLabel(
            """Python
Docs
TR"""
        )

        self.python_docs_tr_label.setFont(QFont("Arial", 50))

        self.central_text_layout.addWidget(self.python_docs_tr_label)

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.translation = QPushButton("Translation")

        self.bootstrapping = QPushButton("Bootstrapping")

        self.credits = QPushButton("Credits")

        self.quit = QPushButton("Quit")

        self.buttons_layout.addWidget(self.translation)
        self.buttons_layout.addWidget(self.bootstrapping)
        self.buttons_layout.addWidget(self.credits)
        self.buttons_layout.addWidget(self.quit)

        self.layout_vertical.addSpacing(70)

        self.layout_vertical.addLayout(self.central_text_layout)

        self.layout_vertical.addSpacing(30)

        self.layout_vertical.addLayout(self.buttons_layout)

        self.layout_vertical.addStretch()

        self.setLayout(self.layout_vertical)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStyleSheet(Styles.main_window_background_dark)
        self.setGeometry(400, 200, 1200, 600)
        self.light_dark_toggle = AnimatedToggle()
        self.startMainMenu()

    def startMainMenu(self, *args):
        """Initialize and display the main menu window"""
        self.window = Window(self.light_dark_toggle)
        self.light_dark_toggle.stateChanged.connect(self.change_theme)

        if parser.get("SETTINGS", "isLight") == "True":
            self.light_dark_toggle.setChecked(True)

        self.window.translation.clicked.connect(self.startTranslation)
        self.window.bootstrapping.clicked.connect(self.startBootstrapping)
        self.window.credits.clicked.connect(self.startCredits)
        self.window.quit.clicked.connect(self.quit)

        self.setWindowTitle("Python Docs TR Management App")
        self.setCentralWidget(self.window)
        self.showMaximized()
        self.change_theme()

    def startCredits(self):
        """Switch to the CreditsWindow"""
        self.credits_window = CreditsWindow(self.light_dark_toggle)
        self.credits_window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.credits_window)
        self.showMaximized()
        self.change_theme()

    def startBootstrapping(self):
        """Start the BootstrappingDialog"""
        dialog = BootstrappingDialog()

        if dialog.exec():
            bootstrapping.main(dialog.comboBox.currentText())
        else:
            pass

    def startTranslation(self):
        """Switch to the TranslationWindow"""
        self.translation_window = TranslationWindow(self.light_dark_toggle)
        self.translation_window.back_pc.mousePressEvent = self.startMainMenu
        self.setCentralWidget(self.translation_window)
        self.showMaximized()
        self.change_theme()

    def quit(self):
        """Quit the application"""
        sys.exit()

    def change_theme(self):
        """Change the application theme based on toggle state"""
        if self.light_dark_toggle.last_value:
            self.setStyleSheet(Styles.main_window_background_light)
            self.light_dark_toggle.label.setText("Light")
            self.light_dark_toggle.label.move(QPoint(7, 5))

            # Change back button image and styles to light mode
            for image in self.findChildren(ImageLabel):
                if image.path == "icons/white_back_arrow.png":
                    image.changePixmap("icons/black_back_arrow.png")

            for label in self.findChildren(QLabel):
                label.setStyleSheet(Styles.light_label_style)

            for button in self.findChildren(QPushButton):
                button.setStyleSheet(Styles.light_button_style)

            self.light_dark_toggle.last_value = True

            parser.set(section="SETTINGS", option="isLight", value="True")
            save_changes()

        else:
            self.setStyleSheet(Styles.main_window_background_dark)
            self.light_dark_toggle.label.setText("Dark")
            self.light_dark_toggle.label.move(QPoint(29, 5))

            # Change back button image and styles to dark mode
            for image in self.findChildren(ImageLabel):
                if image.path == "icons/black_back_arrow.png":
                    image.changePixmap("icons/white_back_arrow.png")

            for label in self.findChildren(QLabel):
                label.setStyleSheet(Styles.dark_label_style)

            for button in self.findChildren(QPushButton):
                button.setStyleSheet(Styles.dark_button_style)

            self.light_dark_toggle.last_value = False
            parser.set(section="SETTINGS", option="isLight", value="False")
            save_changes()


if __name__ == "__main__":
    # Main entry point of the application
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
