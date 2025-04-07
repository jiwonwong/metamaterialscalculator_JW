# material_class.py

class Material:
    def __init__(
        self,
        name: str,
        type_: str,
        thickness: float = None,
        loss_factor: float = None,
        vcl: float = None,
        static_young: float = None,
        tcl: float = None,
        poisson: float = None,
        tor: float = None,
        density: float = None,
        phi: float = None,
        rho1: float = None,
        sigma: float = None,
        eta: float = None,
        nu: float = None
    ):
        self.name = name
        self.type = type_
        self.thickness = thickness
        self.loss_factor = loss_factor
        self.vcl = vcl
        self.static_young = static_young
        self.tcl = tcl
        self.poisson = poisson
        self.tor = tor
        self.density = density
        self.phi = phi
        self.rho1 = rho1
        self.sigma = sigma
        self.eta = eta
        self.nu = nu

    def __repr__(self):
        return f"<Material {self.name} ({self.type})>"

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "thickness": self.thickness,
            "loss_factor": self.loss_factor,
            "vcl": self.vcl,
            "static_young": self.static_young,
            "tcl": self.tcl,
            "poisson": self.poisson,
            "tor": self.tor,
            "density": self.density,
            "phi": self.phi,
            "rho1": self.rho1,
            "sigma": self.sigma,
            "eta": self.eta,
            "nu": self.nu
        }

    @staticmethod
    def from_dict(data: dict):
        return Material(
            name=data.get("name"),
            type_=data.get("type"),
            thickness=data.get("thickness"),
            loss_factor=data.get("loss_factor"),
            vcl=data.get("vcl"),
            static_young=data.get("static_young"),
            tcl=data.get("tcl"),
            poisson=data.get("poisson"),
            tor=data.get("tor"),
            density=data.get("density"),
            phi=data.get("phi"),
            rho1=data.get("rho1"),
            sigma=data.get("sigma"),
            eta=data.get("eta"),
            nu=data.get("nu")
        )
