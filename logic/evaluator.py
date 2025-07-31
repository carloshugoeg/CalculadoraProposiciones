# aqui esta la logica para evaluar la expresion

from .components import LogicComponent


class ExpressionEvaluator:
    def __init__(self):
        # diccionario para la jerarquia de operaciones (lo que hicimos en Estructura de Datos I)
        self.precedence = {'¬': 3, '∧': 2, '∨': 2, '→': 1, '↔': 1}

    def _to_postfix(self, expression: list[LogicComponent]) -> list[LogicComponent]:
        """
        Aqui reuse el codigo de estructuras de aquella vez que nos pidieron determinar la jerarquia de las operaciones
        en el arbol
        """
        output_queue = []
        operator_stack = []
        # aqui recorremos toda la expresion para ordenarla de forma posfija como aquella vez usamos
        for token in expression:
            if token.type == 'variable':
                output_queue.append(token)
            elif token.type in ['operator', 'connector']:
                while (operator_stack and operator_stack[-1].value != '(' and
                       self.precedence.get(operator_stack[-1].value, 0) >= self.precedence.get(token.value, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.value == '(':
                operator_stack.append(token)
            elif token.value == ')':
                while operator_stack and operator_stack[-1].value != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1].value == '(':
                    operator_stack.pop()

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    def _evaluate_postfix(self, postfix_expr: list[LogicComponent], values: dict[str, bool]) -> bool:
        """
        otra vez reuse el codigo de lo del arbol de expresiones de aquella vez
        """
        if not postfix_expr:
            return False

        value_stack = []

        for token in postfix_expr:
            if token.type == 'variable':
                value_stack.append(values[token.value])
            elif token.value == '¬':
                operand = value_stack.pop()
                value_stack.append(not operand)
            else:
                if len(value_stack) < 2:
                    raise ValueError("faltan elemenos")
                op2 = value_stack.pop()
                op1 = value_stack.pop()

                if token.value == '∧':
                    value_stack.append(op1 and op2)
                elif token.value == '∨':
                    value_stack.append(op1 or op2)
                elif token.value == '→':
                    # aqui use las leyes que vimos en razo para simplifcar estos cosos
                    value_stack.append((not op1) or op2)
                elif token.value == '↔':
                    # doble implicacion era esto (p → q) ∧ (q → p)
                    value_stack.append(((not op1) or op2) and ((not op2) or op1))

        if len(value_stack) != 1:
            raise ValueError("La pila esta vacia")

        return value_stack[0]

    def evaluate(self, expression: list[LogicComponent], values: dict[str, bool]) -> bool:
        """
        es para evaluar todo, encontre el codigo en Stack Overflow.
        """
        postfix_expression = self._to_postfix(expression)
        return self._evaluate_postfix(postfix_expression, values)
