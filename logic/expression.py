#expresion lleva doble s? JAJAJ expression? bueno ahi revisas esto, y q te recordas de borrar el comentario luego


from .components import LogicComponent


class LogicalExpression:
    """
    voy a crear una lista para almacenar la expresion

    OTRA VEZ, reusare el codigo de estructuras, al final si nos sirvió para algo el curso
    """

    def __init__(self):
        self.components: list[LogicComponent] = []

    def add_component(self, component: LogicComponent) -> bool:
        """
        cree un metodo para ver si se puede agregar, todos los ifs estan adentro para que sea mas facil de leer
        """
        if self._is_valid_addition(component):
            self.components.append(component)
            return True
        return False

    def remove_last(self):
        """esto es para el deshacer,RECORDA CREAR EL BOTON PARA ESTO"""
        if self.components:
            self.components.pop()

    def clear(self):
        """Limpia toda la expresión. Igual necesita boton"""
        self.components = []

    def get_variables(self) -> list[str]:
        """
        creo una lista con las variables para saber cuantas veces debemos de hacer las operaciones
        """
        variables = {comp.value for comp in self.components if comp.type == 'variable'}
        return sorted(list(variables))

    def is_valid_to_generate(self) -> tuple[bool, str]:
        """
        valdacion final
        """
        if not self.components:
            return False, "La expresión está vacía"

        # Voy a enumerar las validaciones para que tengas una idea de que hace cada cosa, cualquier cosa me avisas

        # 1. Validar balance de paréntesis
        parens_balance = 0
        for comp in self.components:
            if comp.value == '(':
                parens_balance += 1
            elif comp.value == ')':
                parens_balance -= 1
            if parens_balance < 0:
                # revisa que los errores se muestren plz
                return False, "Paréntesis de cierre ')' sin uno de apertura"

        if parens_balance != 0:
            return False, "Paréntesis desbalanceados. Faltan cierres."

        # 2. Validar que no termine con un operador o conector
        last_comp = self.components[-1]
        if last_comp.type in ['operator', 'connector'] or last_comp.value == '(':
            return False, "La expresión no puede terminar con un operador o paréntesis abierto"

        return True, "Expresion valida"

    def _is_valid_addition(self, new_comp: LogicComponent) -> bool:
        """
        esta logica me costo mucho, revisa si tiene errores
        aqui estan los ifs que dije arriba, hacen las validaciones para ver si
        se puede añadir
        """
        if not self.components:
            # El primer componente solo puede ser variable, negación o '('
            return new_comp.type == 'variable' or new_comp.type == 'operator' or new_comp.value == '('

        last_comp = self.components[-1]

        # aqui estan las reglas
        if last_comp.type == 'variable' or last_comp.value == ')':
            # no permite que haya otra cosa que no sea variable o cierre
            return new_comp.type == 'connector' or new_comp.value == ')'

        if last_comp.type == 'operator' or last_comp.type == 'connector' or last_comp.value == '(':
            return new_comp.type == 'variable' or new_comp.type == 'operator' or new_comp.value == '('

        return False

    def __str__(self) -> str:
        """Esto es lo q debes poner que se construye en el textbox"""
        return " ".join(comp.value for comp in self.components)
