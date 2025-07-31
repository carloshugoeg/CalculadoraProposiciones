# ui/panels.py
# Contiene las clases para los diferentes paneles de la interfaz gráfica.
# Cada clase hereda de ttk.Frame y es responsable de una sección de la UI.
#Hugo, no tocar visual, qué se puede modificar es la lógica de los botones y la expresión.


import tkinter as tk
from tkinter import ttk
from .theme import COLORES, FUENTES, ESTILO_CONFIG
from logic.components import VARIABLES, OPERATORS, CONNECTORS, GROUPING


class ComponentsPanel(ttk.Frame):
    """Panel izquierdo que muestra los componentes lógicos para seleccionar.""" 
    def __init__(self, parent, component_click_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.component_click_callback = component_click_callback

        self.configure(style="TFrame")

        # Título del panel
        title = ttk.Label(self, text="🧩 Componentes", style="Title.TLabel", anchor="center")
        title.pack(fill="x", pady=(0, 10))

        # Contenedor para cada uno de los botones por si requiere modificar
        contenedores = ttk.Frame(self, style="TFrame")
        contenedores.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear grupos de componentes
        self._crear_grupo(contenedores, "Variables", VARIABLES.values(), COLORES["accent"])
        self._crear_grupo(contenedores, "Operador", OPERATORS.values(), COLORES["error"])
        self._crear_grupo(contenedores, "Conectivos", CONNECTORS.values(), COLORES["success"])
        self._crear_grupo(contenedores, "Agrupación", GROUPING.values(), COLORES["warning"])

    def _crear_grupo(self, parent, title, components, color):
        """Crea una sección para un grupo de componentes."""
        group_frame = ttk.LabelFrame(parent, text=title, style="TLabelframe")
        group_frame.pack(fill="x", pady=10, padx=5)

        # Configurar grid para botones
        num_cols = 3
        for i, comp in enumerate(components):
            btn = tk.Button(
                group_frame,
                text=comp.symbol,
                bg=color,
                **ESTILO_CONFIG["button"]
            )
            btn.configure(command=lambda c=comp: self.component_click_callback(c))
            btn.grid(row=i // num_cols, column=i % num_cols, padx=4, pady=4, sticky="ew")
            group_frame.grid_columnconfigure(i % num_cols, weight=1)


class BuilderPanel(ttk.Frame):
    

    def __init__(self, parent, generate_callback, undo_callback, clear_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.generate_callback = generate_callback
        self.undo_callback = undo_callback
        self.clear_callback = clear_callback

        self.configure(style="Card.TFrame")
        self.pack(fill="x", padx=10, pady=10)

        # Título
        title = ttk.Label(self, text="🔧 Constructor", style="CardTitle.TLabel", anchor="center")
        title.pack(fill="x", pady=(0, 10))

        # Frame para mostrar la expresión, es necesario para que se vea bien
        expr_frame = ttk.Frame(self, style="TFrame", relief="sunken", height=80)
        expr_frame.pack(fill="x", padx=10, pady=10)

        self.expr_label = ttk.Label(expr_frame, text="Construye tu expresión aquí...", style="Expression.TLabel")
        self.expr_label.pack(padx=10, pady=10, fill="x")

        # Frame para el mensaje de validación, en este caso es un excepción par tomarlo en cuenta
        self.validation_label = ttk.Label(self, text="", style="Validation.TLabel", anchor="center")
        self.validation_label.pack(fill="x", padx=10, pady=(0, 10))

        # Frame para los botones de acción
        buttons_frame = ttk.Frame(self, style="TFrame")
        buttons_frame.pack(pady=10)

        generate_btn = tk.Button(buttons_frame, text="📊 Generar Tabla", bg=COLORES["success"],
                                 command=self.generate_callback, **ESTILO_CONFIG["button"])
        undo_btn = tk.Button(buttons_frame, text="↩️ Deshacer", bg=COLORES["warning"], command=self.undo_callback,
                             **ESTILO_CONFIG["button"])
        clear_btn = tk.Button(buttons_frame, text="🗑️ Limpiar", bg=COLORES["error"], command=self.clear_callback,
                              **ESTILO_CONFIG["button"])

        generate_btn.pack(side="left", padx=5)
        undo_btn.pack(side="left", padx=5)
        clear_btn.pack(side="left", padx=5)

    def actualizar_expresion(self, expression_str: str):
        
        if not expression_str:
            self.expr_label.configure(text="Construye tu expresión aquí...")
        else:
            self.expr_label.configure(text=expression_str)

    def actualizar_validacion(self, message: str, is_valid: bool):
        self.validation_label.configure(text=message)
        if is_valid:
            self.validation_label.configure(style="ValidationSuccess.TLabel")
        else:
            self.validation_label.configure(style="ValidationError.TLabel")


class TablePanel(ttk.Frame):
    #Aquí es para mostrar la tabla de verdad generada

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(style="Card.TFrame")
        self.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Título
        title = ttk.Label(self, text="📋 Tabla de Verdad", style="CardTitle.TLabel", anchor="center")
        title.pack(fill="x", pady=(0, 10))

        # Contenedor para el Treeview y scrollbars
        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        v_scroll = ttk.Scrollbar(container, orient="vertical")
        h_scroll = ttk.Scrollbar(container, orient="horizontal")

        self.tree = ttk.Treeview(
            container,
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
            style="Treeview"
        )

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

    def display_table(self, headers: list[str], data: list[list[str]], expression_str: str):
        """Limpia la tabla anterior y muestra los nuevos datos."""
        self.limpiar_tabla()

        # Configurar columnas
        final_header = f"Resultado: {expression_str}"
        all_headers = headers + [final_header]
        self.tree["columns"] = all_headers
        self.tree["show"] = "headings"

        for header in all_headers:
            self.tree.heading(header, text=header, anchor="center")
            self.tree.column(header, anchor="center", width=100)

        # Configurar tags para colorear V y F
        self.tree.tag_configure('V', foreground=COLORES["success"], font=FUENTES["table_body"])
        self.tree.tag_configure('F', foreground=COLORES["error"], font=FUENTES["table_body"])

        # Insertar filas de datos
        for i, row_data in enumerate(data):
            tagged_row = []
            for value in row_data:
                tag = 'V' if value == 'V' else 'F'
                tagged_row.append(tag)

            self.tree.insert("", "end", values=row_data, tags=tuple(tagged_row))

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = []
