class Styles:

    main_window_background_light = """
        background-color: rgba(200, 200, 200, 0.9); 
    """

    main_window_background_dark = """
        background-color: rgba(30, 30, 30, 0.9); 
    """

    light_label_style = """
        QLabel {background-color:rgba(0,0,0,0%); color: rgb(0, 0, 0)}
    """

    dark_label_style = """
        QLabel {background-color:rgba(0,0,0,0%); color: rgb(255, 255, 255)}
    """

    light_button_style = """
        QPushButton {
            width: 150px;
            background-color: #2E2E2E;
            border: 2px solid #555555;
            border-radius: 12px;
            color: #FFFFFF;
            font-size: 16px;
            padding: 10px 20px;
            outline: none;
        }
        QPushButton:hover {
            background-color: #3C3C3C;
            border: 2px solid #666666;
        }
        QPushButton:pressed {
            background-color: #1C1C1C;
            border: 2px solid #444444;
        }
    """

    dark_button_style = """
        QPushButton {
            width: 150px;
            background-color: #FFFFFF;
            border: 2px solid #CCCCCC;
            border-radius: 12px;
            color: #333333;
            font-size: 16px;
            padding: 10px 20px;
            outline: none;
        }
        QPushButton:hover {
            background-color: #F2F2F2;
            border: 2px solid #BBBBBB;
        }
        QPushButton:pressed {
            background-color: #E6E6E6;
            border: 2px solid #AAAAAA;
        }
    """

    list_widget_style = """
            QListWidget {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
            }
            
            QListWidget::item {
                background-color: #ffffff;
                padding: 10px;
                margin-bottom: 5px;
                border-radius: 3px;
            }
            
            QListWidget::item:selected {
                background-color: #a0c0ff;
                color: #ffffff;
            }

            QScrollBar {
                background-color: #FFFFFF;
            }

            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: gray;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {
                background: none;
                border: none;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {
                background: none;
                border: none;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """

    text_edit_style = """           
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 14px;
            }"""

    checkbox_style = """QCheckBox {
                spacing: 5px;
                font-size: 14px;
                color: #ffffff; /* White text color */
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #ccc; /* Default border */
                background-color: #fff; /* Default background */
            }
            QCheckBox::indicator:checked {
                background-color: #007bff; /* Blue background when checked */
                border: 2px solid #007bff; /* Blue border when checked */
            }
            QCheckBox::indicator:checked:hover {
                background-color: #0056b3; /* Darker blue on hover */
                border: 2px solid #0056b3;
            }
            QCheckBox::indicator:checked:pressed {
                background-color: #003d80; /* Even darker blue when pressed */
                border: 2px solid #003d80;
            }"""