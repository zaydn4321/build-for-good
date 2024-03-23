def display_message(speedUp=False, slowDown=False):
    import sys
    from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont, QColor, QPalette

    app = QApplication(sys.argv)
    window = QWidget()
    palette = window.palette()

    if speedUp:
        window.setWindowTitle('Speed Up')
        palette.setColor(QPalette.Window, QColor('green'))
        text = 'SPEED UP'
    elif slowDown:
        window.setWindowTitle('Slow Down')
        palette.setColor(QPalette.Window, QColor('red'))
        text = 'SLOW DOWN'
    else:
        window.setWindowTitle('Keep Going')
        palette.setColor(QPalette.Window, QColor('white'))
        text = 'KEEP GOING'

    window.setPalette(palette)
    window.setGeometry(100, 100, 500, 300)

    label = QLabel(text)
    label.setFont(QFont('Tauri', 48, QFont.Bold))
    label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(label)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())


