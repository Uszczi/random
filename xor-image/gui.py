import sys
from dataclasses import field, dataclass
from typing import Any
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

import core

# TODO add injector


@dataclass
class GlobalState:
    image_path: str = ""
    key_path: str = ""
    widget_layout: Any = field(init=False)
    result_image: Any = field(init=False)

    def set_image_path(self, path: str) -> None:
        self.image_path = path
        self._make_encryption()

    def set_key_path(self, path: str) -> None:
        self.key_path = path
        self._make_encryption()

    def set_result_widget(self, widget):
        self.widget_layout = widget

    def _make_encryption(self):
        if not self.image_path or not self.key_path:
            return

        image = core.xor(self.image_path, self.key_path)
        h, w, _ = image.shape

        def f(_):
            return

        result_image = QImage(
            image.data, w, h, 3 * w, QImage.Format.Format_RGB888, f, f
        )
        self.widget_layout.set_pixmap(result_image)
        self.widget_layout.activate_button()
        self.result_image = image


class LoadImage(QWidget):
    def __init__(self, image_text, button_function):
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
        self.button.clicked.connect(lambda: self.open(button_function))
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def open(self, function) -> None:
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
    def __init__(self, global_state):
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
        self.button.clicked.connect(lambda: self.save(global_state))
        self.button.setDisabled(True)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def save(self, global_state) -> None:
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

    def set_pixmap(self, pixmap):
        self.image_label.setPixmap(QPixmap.fromImage(pixmap))

    def activate_button(self):
        self.button.setDisabled(False)


class MainWidget(QWidget):
    def __init__(self, global_state: GlobalState):
        super().__init__()
        self.global_state = global_state
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
    def __init__(self):
        super().__init__()
        global_state = GlobalState()
        main_widget = MainWidget(global_state)
        self.setCentralWidget(main_widget)
        self.resize(1600, 900)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
