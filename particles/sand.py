from particles.base import MovableSolid

class Sand(MovableSolid):
    ORDER = 1
    NAME = "Sand"
    IMAGE_NAME = "Areia"
    IMAGE_COLOR = (255, 200, 110)
    DESCRIPTION = [
        "AREIA",
        'Areia são pequenos grãos',
        'de rocha e minerais que',
        'foram desgastados ao longo',
        'do tempo pela água, vento',
        'e outros processos naturais.',
        "",
        "No SimuPOO, ela tem uma das,",
        "senão a, lógica mais simples",
        "de todas as partículas.",
    ]

    CONCRETE = True

    def __init__(self):
        super().__init__(
            (255, 200, 110, 15),    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                      # Particle Density
            1.0,                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.2,                    # Particle Heat Conductivity (maior = mais perda de calor)
        )
