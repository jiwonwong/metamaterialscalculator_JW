import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QComboBox, QLabel, QLineEdit, QTabWidget, QTextEdit,
    QListWidget, QListWidgetItem, QHBoxLayout
)
from material_class import Material

class MetamaterialCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Metamaterial Calculator")
        self.setGeometry(100, 100, 1000, 700)

        self.materials_db = self.load_materials()
        self.layer_stack = []  # Material 객체들을 저장할 리스트

        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout()

        # 입력 폼 + 버튼 묶기
        input_and_button_layout = QVBoxLayout()

        # 재료 선택 및 입력 필드
        grid_layout = QGridLayout()
        material_label = QLabel("Select Material")
        self.material_combo = QComboBox()
        self.material_combo.addItems(list(self.materials_db.keys()))
        self.material_combo.currentTextChanged.connect(self.populate_fields)
        grid_layout.addWidget(material_label, 0, 0)
        grid_layout.addWidget(self.material_combo, 0, 1, 1, 3)

        self.inputs = {}
        labels = [
            ("Thickness", "thickness"),
            ("Loss Factor", "loss_factor"),
            ("VCL", "vcl"),
            ("Static Young's Modulus", "static_young"),
            ("TCL", "tcl"),
            ("Poisson's Ratio", "poisson"),
            ("TOR", "tor"),
            ("Density", "density"),
            ("Phi", "phi"),
            ("Rho1", "rho1"),
            ("Sigma", "sigma"),
            ("Eta", "eta"),
            ("Nu", "nu")
        ]

        for i, (label, key) in enumerate(labels):
            row, col = divmod(i, 2)
            label_widget = QLabel(label)
            input_widget = QLineEdit()
            self.inputs[key] = input_widget
            grid_layout.addWidget(label_widget, row + 1, col * 2)
            grid_layout.addWidget(input_widget, row + 1, col * 2 + 1)

        input_and_button_layout.addLayout(grid_layout)

        # ➕ 층 추가 버튼
        self.add_layer_btn = QPushButton("Add to Layer Stack")
        self.add_layer_btn.clicked.connect(self.add_layer)
        input_and_button_layout.addWidget(self.add_layer_btn)

        main_layout.addLayout(input_and_button_layout)

        # Layer Stack 시각화
        self.layer_list = QListWidget()
        main_layout.addWidget(QLabel("Layer Stack (Top to Bottom):"))
        main_layout.addWidget(self.layer_list)

        # 계산 버튼
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate)
        main_layout.addWidget(self.calculate_btn)

        # 결과 탭
        self.result_tabs = QTabWidget()
        self.graph_tab = QTextEdit("[Graph Output Placeholder]")
        self.result_tab = QTextEdit("[Numerical Result Placeholder]")
        self.result_tabs.addTab(self.graph_tab, "Graph")
        self.result_tabs.addTab(self.result_tab, "Results")
        main_layout.addWidget(self.result_tabs)

        widget.setLayout(main_layout)
        self.populate_fields(self.material_combo.currentText())

    def load_materials(self):
        try:
            with open("materials_sample.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def populate_fields(self, material_name):
        data = self.materials_db.get(material_name, {})
        for key, widget in self.inputs.items():
            value = data.get(key, "")
            widget.setText(str(value))

    def add_layer(self):
        name = self.material_combo.currentText()
        data = {key: self.inputs[key].text() for key in self.inputs}
        try:
            # float로 변환 가능한 값만 변환
            for k in data:
                if data[k] != "":
                    data[k] = float(data[k])
        except ValueError:
            print("Invalid input. Please check the values.")
            return

        material = Material.from_dict({"name": name, "type": "custom", **data})
        self.layer_stack.append(material)
        self.layer_list.addItem(f"{material.name} | Thickness: {material.thickness} mm")

    def calculate(self):
        self.graph_tab.setText("[Graph would be shown here after calculation]")
        summary = "\n".join([
            f"Layer {i+1}: {mat.name}, Thickness: {mat.thickness} mm"
            for i, mat in enumerate(self.layer_stack)
        ])
        self.result_tab.setText("[Layer Stack Summary:]\n" + summary)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MetamaterialCalculator()
    window.show()
    sys.exit(app.exec())