import sys

import inject
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget

from src.gui.config import setup_app
from src.gui.state import GlobalState

from .load_image import LoadImage
from .result_image import ResultImage


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
