MATERIAL_DEFINITIONS = {
    "fluid": {
        "color": "#91d1f3",
        "properties": [
            {"name": "rho", "label": "Density (\u03c1) [kg/m^3]"},
            {"name": "c", "label": "Sound Speed (c) [m/s]"}
        ]
    },
    "solid": {
        "color": "#b4f091",
        "properties": [
            {"name": "rho", "label": "Density (\u03c1) [kg/m^3]"},
            {"name": "E", "label": "Young's Modulus (E) [Pa]"},
            {"name": "eta", "label": "Loss Factor (\u03b7)"},
            {"name": "nu", "label": "Poisson's Ratio (\u03bd)"}
        ]
    },
    "poro": {
        "color": "#f3e291",
        "properties": [
            {"name": "phi", "label": "Porosity (\u03c6)"},
            {"name": "sigma", "label": "Flow Resistivity (\u03c3) [Rayls/m]"},
            {"name": "TOR", "label": "Tortuosity (\u03b1\u221e)"},
            {"name": "VCL", "label": "Viscous Length (\u039b) [m]"},
            {"name": "TCL", "label": "Thermal Length (\u039b\u2032) [m]"},
            {"name": "rho1", "label": "Frame Density (\u03c1\u2081) [kg/m^3]"},
            {"name": "E1", "label": "Frame Modulus (E\u2081) [Pa]"},
            {"name": "eta", "label": "Loss Factor (\u03b7)"},
            {"name": "nu", "label": "Poisson's Ratio (\u03bd)"}
        ]
    },
    "stiff panel": {
        "color": "#f3a6a6",
        "properties": [
            {"name": "hp", "label": "Panel Thickness (h\u209a) [m]"},
            {"name": "rho", "label": "Density (\u03c1) [kg/m^3]"},
            {"name": "E", "label": "Young's Modulus (E\u209a) [Pa]"},
            {"name": "eta", "label": "Loss Factor (\u03b7\u209a)"},
            {"name": "nu", "label": "Poisson's Ratio (\u03bd\u209a)"}
        ]
    },
    "Unbonded": {
        "color": "#dddddd",
        "properties": []
    }
}
