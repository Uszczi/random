import sys
from typing import Any, Callable

import inject
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.config import setup_app
from src.core import core
from src.state import GlobalState


class LoadImage(QWidget):
    def __init__(self, image_text: str, button_function: Callable):
        super().__init__()

        self.image_label = QLabel(image_text)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: #7c9c85")
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setMaximumSize(500, 500)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        self.button = QPushButton("Load image")
        self.button.clicked.connect(lambda: self.open(button_function))  # type: ignore
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def open(self, function: Callable) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.jpeg *.jpg)"
        )

        if file_name:
            image = QImage(file_name)
            if image.isNull():
                QMessageBox.information(
                    self, "Image Viewer", "Cannot load %s." % file_name
                )
                return
            self.image_label.setPixmap(QPixmap.fromImage(image))
            function(file_name)


class ResultImage(QWidget):
    def __init__(self, global_state: GlobalState) -> None:
        super().__init__()

        self.image_label = QLabel("Result image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: #7c9c85")
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setMaximumSize(500, 500)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        self.button = QPushButton("Save image")
        self.button.clicked.connect(lambda: self.save(global_state))  # type: ignore
        self.button.setDisabled(True)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def save(self, global_state: Any) -> None:
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getSaveFileName()",
            "",
            "Images (*.png *.jpeg *.jpg)",
        )
        actual_file_name = core.save(file_name, global_state.result_image)
        q = QMessageBox()
        q.setText(f"File {actual_file_name} saved.")
        q.exec()

    def set_pixmap(self, pixmap: Any) -> None:
        self.image_label.setPixmap(QPixmap.fromImage(pixmap))

    def activate_button(self: Any) -> None:
        self.button.setDisabled(False)


class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        global_state = inject.instance(GlobalState)
        self.load_image = LoadImage("Image to process", global_state.set_image_path)
        self.key_image = LoadImage("Image as key", global_state.set_key_path)
        self.result_image = ResultImage(global_state)
        global_state.set_result_widget(self.result_image)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.load_image)
        self.h_layout.addWidget(self.key_image)
        self.h_layout.addWidget(self.result_image)

        self.setLayout(self.h_layout)


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        main_widget = MainWidget()
        self.setCentralWidget(main_widget)
        self.resize(1600, 900)


def main() -> None:
    setup_app()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
