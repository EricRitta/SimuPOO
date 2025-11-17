import random
from particles.base import MovableSolid

class Dirt(MovableSolid):
    NAME = "Dirt"
    IMAGE_NAME = "Terra"
    IMAGE_COLOR = (180, 145, 90)
    DESCRIPTION = [
        "TERRA",
        'Terra é uma mistura de minerais,',
        'matéria orgânica, água e ar.',
        'É a base para o crescimento',
        'de plantas e suporta ecossistemas',
        'terrestres inteiros.',
        "",
        "",
        "COMPORTAMENTO",
        "",
        "Cai verticalmente.",
        "",
        "Desliza diagonalmente em",
        "ângulos menores que areia",
        "(maior rigidez).",
        "",
        "Forma pilhas mais compactas.",
    ]
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (180, 145, 90, 10),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.0,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.2,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        self.RIGIDITY = 8
        if random.randint(1, 10) == 1:
            self._COLOR = (
                max(0, min(255, 150 + random.randint(-10, 10))),
                max(0, min(255, 150 + random.randint(-10, 10))),
                max(0, min(255, 150 + random.randint(-10, 10)))
            )
