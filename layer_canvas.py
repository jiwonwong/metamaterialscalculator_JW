from PyQt6.QtWidgets import QWidget, QInputDialog
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import QRect, Qt

from material_definitions import MATERIAL_DEFINITIONS


class LayerCanvas(QWidget):
    def __init__(self, layers, on_click_callback, get_active_index):
        super().__init__()
        self.layers = layers
        self.on_click_callback = on_click_callback
        self.get_active_index = get_active_index

        self.setMinimumHeight(120)
        self.layer_rects = []

    def paintEvent(self, event):
        painter = QPainter(self)
        canvas_width = self.width()

        image_offset = 20  # 여백을 약간 남김

        # 레이어 시각화
        SCALE = 3
        total_width = sum(int(float(layer.get("thickness", 0) or 0) * SCALE) for layer in self.layers)
        x_offset = image_offset + max((canvas_width - image_offset - total_width) // 2, 0)

        self.layer_rects = []
        for i, layer in enumerate(self.layers):
            thickness = float(layer.get("thickness", 0) or 0)
            if thickness <= 10:
                scale = -2/3 * (thickness - 1) + 8
            else:
                scale = 2
            width = int(thickness * scale)

            material_type = layer.get("type", "")
            definition = MATERIAL_DEFINITIONS.get(material_type, {})
            color = QColor(definition.get("color", "#AAAAAA"))

            rect = QRect(x_offset, 10, width, 100)
            self.layer_rects.append(rect)
            painter.setBrush(color)

            active_index = self.get_active_index()
            pen = QPen(Qt.GlobalColor.red, 3) if i == active_index else QPen(Qt.GlobalColor.black, 1)
            painter.setPen(pen)
            painter.drawRect(rect)
            x_offset += width

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        for i, rect in enumerate(self.layer_rects):
            if rect.contains(pos):
                new_thickness, ok = QInputDialog.getDouble(
                    self, "Edit Thickness",
                    f"Enter new thickness for layer {i+1} (mm):",
                    value=float(self.layers[i].get("thickness", 1.0)),
                    min=0.01, max=1000.0, decimals=2
                )
                if ok:
                    self.layers[i]["thickness"] = new_thickness
                    self.on_click_callback(i)
                    self.update()
                break
