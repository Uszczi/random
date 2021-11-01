from dataclasses import dataclass, field
from typing import Any
import core
from PyQt6.QtGui import QImage


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
