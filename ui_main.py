from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox, QScrollArea, QListWidget, QCheckBox
from layer_canvas import LayerCanvas
from material_definitions import MATERIAL_DEFINITIONS
import json


class SoundInsulationUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sound Insulation Performance")
        self.resize(1000, 600)

        self.layers = []
        self.active_layer_index = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.init_left_panel()
        self.init_right_panel()

    def init_left_panel(self):
        left_panel = QWidget()
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        self.main_layout.addWidget(left_panel)

        config_box = QGroupBox("Layer Configuration")
        config_layout = QVBoxLayout()
        config_box.setLayout(config_layout)

        row_layout = QHBoxLayout()
        self.material_dropdown = QComboBox()
        self.material_dropdown.addItems(["Select Material"] + [k for k in MATERIAL_DEFINITIONS.keys() if k != "Unbonded"])
        self.thickness_input = QLineEdit()
        self.thickness_input.setPlaceholderText("Thickness (mm)")
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_layer)
        row_layout.addWidget(self.material_dropdown)
        row_layout.addWidget(self.thickness_input)
        row_layout.addWidget(self.add_button)

        self.bonded_checkbox = QCheckBox("Interface is bonded")
        self.bonded_checkbox.setChecked(True)

        config_layout.addLayout(row_layout)
        config_layout.addWidget(self.bonded_checkbox)

        self.layer_list_widget = QListWidget()
        self.layer_list_widget.setFixedHeight(100)
        self.layer_list_widget.itemClicked.connect(self.on_layer_selected_from_list)
        config_layout.addWidget(self.layer_list_widget)

        self.canvas = LayerCanvas(self.layers, self.on_layer_selected, self.get_active_layer_index)
        config_layout.addWidget(self.canvas)

        left_layout.addWidget(config_box)

        self.property_panel = QGroupBox("Material Properties")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.property_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        layout = QVBoxLayout(self.property_panel)
        layout.addWidget(scroll)

        left_layout.addWidget(self.property_panel)

        self.calc_button = QPushButton("Run Calculation")
        self.calc_button.clicked.connect(self.run_calculation)
        left_layout.addWidget(self.calc_button)

    def init_right_panel(self):
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        self.main_layout.addWidget(right_panel)

        right_layout.addWidget(QLabel("[Calculation and Plot Area Placeholder]"))

    def add_layer(self):
        material_name = self.material_dropdown.currentText()
        try:
            thickness = float(self.thickness_input.text())
        except ValueError:
            return

        if material_name == "Select Material" or thickness <= 0:
            return

        interface_mode = "bonded" if self.bonded_checkbox.isChecked() else "unbonded"

        new_layer = {
            "material": material_name,
            "type": material_name,
            "thickness": thickness,
            "interface": interface_mode,
            "fields": [],
            "metadata": [],
            "values": {}
        }
        self.layers.append(new_layer)
        self.canvas.update()

        summary = f"{material_name} ({thickness:.2f} mm)"
        self.layer_list_widget.addItem(summary)

    def on_layer_selected_from_list(self, item):
        index = self.layer_list_widget.row(item)
        self.on_layer_selected(index)

    def on_layer_selected(self, index):
        if index < 0 or index >= len(self.layers):
            return

        self.active_layer_index = index
        layer = self.layers[index]
        self.generate_property_fields(layer)

    def get_active_layer_index(self):
        return self.active_layer_index

    def clear_property_panel(self):
        for i in reversed(range(self.property_layout.count())):
            widget = self.property_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def generate_property_fields(self, layer):
        self.clear_property_panel()
        material_type = layer["type"]
        prop_definitions = MATERIAL_DEFINITIONS.get(material_type, {}).get("properties", [])

        existing_values = layer.get("values", {})
        layer["fields"] = []
        layer["metadata"] = []

        for prop in prop_definitions:
            label_widget = QLabel(prop["label"])
            input_widget = QLineEdit()

            if prop["name"] in existing_values:
                input_widget.setText(str(existing_values[prop["name"]]))

            self.property_layout.addWidget(label_widget)
            self.property_layout.addWidget(input_widget)

            layer["fields"].append((label_widget, input_widget))
            layer["metadata"].append((prop["name"], prop["label"], input_widget))

    def update_layer_values(self):
        if self.active_layer_index is not None:
            layer = self.layers[self.active_layer_index]
            values = {}
            for name, _, field in layer.get("metadata", []):
                text = field.text()
                if text:
                    try:
                        values[name] = float(text)
                    except ValueError:
                        continue
            layer["values"] = values

    def run_calculation(self):
        self.update_layer_values()
        print("[INFO] Running calculation with layers:")
        print(json.dumps(self.layers, indent=2))
