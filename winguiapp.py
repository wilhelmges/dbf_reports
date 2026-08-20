import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)

def import_tables():
    print("Початок імпорту таблиць")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(400, 120)
    layout = QVBoxLayout(window)
    label = QLabel("консоль керування")
    label.setAlignment(Qt.Alignment.AlignCenter)
    layout.addWidget(label)
    button = QPushButton("Імпортувати таблиці")
    button.setMinimumHeight(60)
    button.setSizePolicy(
        button.sizePolicy().horizontalPolicy(),
        button.sizePolicy().verticalPolicy()
    )

    button.clicked.connect(import_tables)
    layout.addWidget(button)
    window.show()

    sys.exit(app.exec())