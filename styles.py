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

    dark_mode_button_style = """
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

    light_mode_button_style = """
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