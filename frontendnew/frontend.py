import sys, time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

app = QApplication(sys.argv)
window = QWidget()
palette = window.palette()
window.setWindowTitle('Keep Going')
palette.setColor(QPalette.Window, QColor('white'))
window.setPalette(palette)
window.setGeometry(100, 100, 500, 300)

label = QLabel('KEEP GOING')
label.setFont(QFont('Tauri', 48, QFont.Bold))
label.setAlignment(Qt.AlignCenter)

layout = QVBoxLayout()
layout.addWidget(label)
window.setLayout(layout)
window.show()

def display_message(speedUp=False, slowDown=False):
    if speedUp:
        window.setWindowTitle('Speed Up')
        palette.setColor(QPalette.Window, QColor('green'))
        text = 'SPEED UP'
        label.setStyleSheet("color: white;")
    elif slowDown:
        window.setWindowTitle('Slow Down')
        palette.setColor(QPalette.Window, QColor('red'))
        text = 'SLOW DOWN'
        label.setStyleSheet("color: white;")
    else:
        window.setWindowTitle('Keep Going')
        palette.setColor(QPalette.Window, QColor('white'))
        text = 'KEEP GOING'
        label.setStyleSheet("color: black;")

    label.setText(text)
    window.setPalette(palette)

time.sleep(5)
display_message(False, True)

sys.exit(app.exec_())
