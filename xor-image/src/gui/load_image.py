from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.utils.images import get_images_path


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
            self,
            "",
            str(get_images_path()),
            "Images (*.png *.jpeg *.jpg)",
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
