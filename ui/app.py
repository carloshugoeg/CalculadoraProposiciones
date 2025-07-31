import tkinter as tk
from tkinter import ttk, messagebox
import itertools

from .theme import COLORES, FUENTES
from .panels import ComponentsPanel, BuilderPanel, TablePanel
from logic.expression import LogicalExpression
from logic.evaluator import ExpressionEvaluator
from logic.components import LogicComponent


class TruthTableApp(tk.Tk):
    #Clase principal de la aplicación que hereda de tk.Tk.
    #Gestiona la ventana principal y la interacción entre los paneles y la lógica.
    def __init__(self):
        super().__init__()

        
        self.expression = LogicalExpression()
        self.evaluator = ExpressionEvaluator()

        self.title("Generador de Tablas de Verdad 🧠")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLORES["background"])

        self._setup_styles()

        self._create_widgets()

    def _setup_styles(self):
        """Configura los estilos personalizados para los widgets de ttk."""
        style = ttk.Style(self)
        style.theme_use('clam')

        # Estilo para frames principales
        style.configure("TFrame", background=COLORES["surface"])

        # Estilo para paneles tipo "tarjeta"
        style.configure("Card.TFrame", background=COLORES["surface"], borderwidth=1, relief="solid")

        # Estilos para etiquetas
        style.configure("TLabel", background=COLORES["surface"], foreground=COLORES["primary_text"], font=FUENTES["body"])
        style.configure("Title.TLabel", background=COLORES["background_light"], foreground=COLORES["on_primary"],
                        font=FUENTES["title"])
        style.configure("CardTitle.TLabel", background=COLORES["surface"], foreground=COLORES["primary_text"],
                        font=FUENTES["subtitle"])
        style.configure("Expression.TLabel", background="#ecf0f1", foreground=COLORES["primary_text"],
                        font=FUENTES["component"], padding=10)

        # Estilos para validación
        style.configure("Validation.TLabel", font=FUENTES["body"])
        style.configure("ValidationSuccess.TLabel", foreground=COLORES["success"], font=FUENTES["body"])
        style.configure("ValidationError.TLabel", foreground=COLORES["error"], font=FUENTES["body"])

        # Estilo para LabelFrame
        style.configure("TLabelframe", background=COLORES["surface"], bordercolor=COLORES["border"])
        style.configure("TLabelframe.Label", background=COLORES["surface"], foreground=COLORES["primary_text"],
                        font=FUENTES["body"])

        # Estilo para Treeview (tabla)
        style.configure("Treeview", rowheight=30, fieldbackground=COLORES["surface"], font=FUENTES["body"])
        style.configure("Treeview.Heading", font=FUENTES["table_header"], background=COLORES["table_header"],
                        foreground=COLORES["on_primary"], relief="raised")
        style.map("Treeview.Heading", background=[('active', COLORES["accent"])])

    def _create_widgets(self):
        """Crea y organiza los paneles principales de la aplicación."""
        # Frame izquierdo para los componentes 
        self.components_panel = ComponentsPanel(self, self._on_component_click)
        self.components_panel.pack(side="left", fill="y", padx=10, pady=10)

        # Frame derecho para el constructor y la tabla
        right_frame = ttk.Frame(self, style="TFrame")
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.configure(style="TFrame")

        # Panel del constructor (arriba)
        self.builder_panel = BuilderPanel(
            right_frame,
            generate_callback=self._on_generate_table,
            undo_callback=self._on_undo,
            clear_callback=self._on_clear
        )

        # Panel de la tabla (abajo)
        self.table_panel = TablePanel(right_frame)

    def _on_component_click(self, component: LogicComponent):
        """Manejador para cuando se hace clic en un botón de componente."""
        if not self.expression.add_component(component):
            # Podríamos mostrar un feedback visual de error brevemente
            pass
        self._actuailzar_constructor()

    def _on_undo(self):
        #Manejador para el botón 'Deshacer
        self.expression.remove_last()
        self._actuailzar_constructor()

    def _on_clear(self):
        #anejador para el botón 'Limpiar'
        self.expression.clear()
        self._actuailzar_constructor()
        self.table_panel.limpiar_tabla()

    def _on_generate_table(self):
        #Manejador para el botón 'Generar Tabla'
        valido, message = self.expression.is_valid_to_generate()
        if not valido:
            messagebox.showerror("Expresión Inválida", message)
            return

        variables = self.expression.get_variables()
        if not variables:
            messagebox.showerror("Error", "La expresión no contiene variables para evaluar.")
            return

        if len(variables) > 10:
            messagebox.showwarning("Límite Excedido",
                                   f"La expresión tiene {len(variables)} variables. El máximo permitido es 10.")
            return

        try:
            datos_tabla = self._calcular_tabla(variables)
            self.table_panel.display_table(variables, datos_tabla, str(self.expression))
        except Exception as e:
            messagebox.showerror("Error de Evaluación", f"No se pudo generar la tabla.\nError: {e}")

    def _actuailzar_constructor(self):
        """Actualiza la UI del panel constructor con el estado actual de la expresión."""
        expr_str = str(self.expression)
        self.builder_panel.actualizar_expresion(expr_str)

        # Actualizar validación en tiempo real
        is_valid, message = self.expression.is_valid_to_generate()
        if not expr_str:
            self.builder_panel.actualizar_validacion("", True)  # Sin mensaje si está vacío
        else:
            self.builder_panel.actualizar_validacion(message, is_valid)

    def _calcular_tabla(self, variables: list[str]) -> list[list[str]]:

        num_vars = len(variables)
        combinaciones = list(itertools.product([True, False], repeat=num_vars))

        tabla_filas = []
        for combo in combinaciones:
            values_dict = dict(zip(variables, combo))

            resultado = self.evaluator.evaluate(self.expression.components, values_dict)

            # Convierte los booleanos a 'V' y 'F' para mostrar
            valores_fila = ['V' if v else 'F' for v in combo]
            resultado = 'V' if resultado else 'F'

            tabla_filas.append(valores_fila + [resultado])

        return tabla_filas
