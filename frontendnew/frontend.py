def display_message(speedUp=False, slowDown=False):
    import sys
    from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont, QColor, QPalette

    app = QApplication(sys.argv)
    window = QWidget()

    if speedUp:
        window.setWindowTitle('Speed Up')
        palette = window.palette()
        palette.setColor(QPalette.Window, QColor('green'))
        window.setPalette(palette)
        label = QLabel('SPEED UP')
    elif slowDown:
        window.setWindowTitle('Slow Down')
        palette = window.palette()
        palette.setColor(QPalette.Window, QColor('red'))
        window.setPalette(palette)
        label = QLabel('SLOW DOWN')

    window.setGeometry(100, 100, 500, 300)

    label.setFont(QFont('Tauri', 48, QFont.Bold))
    label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(label)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())


