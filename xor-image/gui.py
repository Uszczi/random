import sys

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

from core import xor

pp = {}

# TODO add global path names
# TODO add global result image
# TODO add save button button


class Image(QWidget):
    def __init__(self, image_text, load_button=False):
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

        button_text = "Load image" if load_button else ""
        self.button = QPushButton(button_text)
        layout.addWidget(self.button)
        if load_button:
            self.button.clicked.connect(lambda: self.open(image_text))
        else:
            pp["dd"] = self

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def open(self, image_text):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.jpeg *.jpg)"
        )
        #         file_name, _ = QFileDialog.getSaveFileName(
        #     self,
        #     "QFileDialog.getSaveFileName()",
        #     "",
        #     "Images (*.png *.jpeg *.jpg)",
        # )
        if file_name:
            image = QImage(file_name)
            if image.isNull():
                QMessageBox.information(
                    self, "Image Viewer", "Cannot load %s." % file_name
                )
                return
            self.image_label.setPixmap(QPixmap.fromImage(image))

            if "key" in image_text:
                pp["key_path"] = file_name
            else:
                pp["image_path"] = file_name

            if pp.get("image_path") and pp.get("key_path"):
                result = xor(pp.get("image_path"), pp.get("key_path"))
                h, w, d = result.shape

                def f(_):
                    return

                result_image = QImage(
                    result.data,
                    w,
                    h,
                    3 * w,
                    QImage.Format.Format_RGB888,
                    f,
                    f,
                )
                pp["dd"].image_label.setPixmap(QPixmap.fromImage(result_image))


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.load_image = Image("Image to process", load_button=True)
        self.key_image = Image("Image as key", load_button=True)
        self.result_image = Image("Result")

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.load_image)
        self.h_layout.addWidget(self.key_image)
        self.h_layout.addWidget(self.result_image)

        self.setLayout(self.h_layout)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        main_widget = MainWidget()
        self.setCentralWidget(main_widget)
        self.resize(1600, 900)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
