from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core import xor
from src.gui.state import GlobalState
from src.utils.images import get_images_path


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
            "",
            str(get_images_path()) + "/new.png",
            "Images (*.png *.jpeg *.jpg)",
        )
        if not file_name:
            return

        actual_file_name = xor.save(file_name, global_state.result_image)
        q = QMessageBox()
        q.setText(f"File {actual_file_name} saved.")
        q.exec()

    def set_pixmap(self, pixmap: Any) -> None:
        self.image_label.setPixmap(QPixmap.fromImage(pixmap))

    def activate_button(self: Any) -> None:
        self.button.setDisabled(False)
