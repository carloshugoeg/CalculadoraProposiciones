# la clase q tiene la definicion de cada componente

from dataclasses import dataclass, field
from typing import Literal

# estos son los tipos que puede tener cada componente
ComponentType = Literal['variable', 'operator', 'connector', 'grouping']


@dataclass
class LogicComponent:
    # la clase para cada componente logico
    value: str
    type: ComponentType
    symbol: str = field(init=False)

    def __post_init__(self):
        self.symbol = self.value



# milito, este es el diccionario de cada variable para que lo uses en la UI
VARIABLES = {v: LogicComponent(v, 'variable') for v in "pqrstuvwxyz"}

# negacion
OPERATORS = {
    '¬': LogicComponent('¬', 'operator'),
}

# conectores como el Y y el O
CONNECTORS = {
    '∧': LogicComponent('∧', 'connector'),
    '∨': LogicComponent('∨', 'connector'),
    '→': LogicComponent('→', 'connector'),
    '↔': LogicComponent('↔', 'connector'),
}

# aqui van los parentesis
GROUPING = {
    '(': LogicComponent('(', 'grouping'),
    ')': LogicComponent(')', 'grouping'),
}

#MILITO NOTA
# este diccionario es el que debes usar para tener todos los componentes en el UI
# te da mas facil acceso
ALL_COMPONENTS = {**VARIABLES, **OPERATORS, **CONNECTORS, **GROUPING}
