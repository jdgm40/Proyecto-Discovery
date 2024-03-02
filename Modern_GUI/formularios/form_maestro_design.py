import tkinter as tk
import os
from tkinter import font

from cargar_excel import CargadorExcel
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import utiles.util_ventana as util_ventana
import utiles.util_imagenes as util_img

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.config_window()
        self.load_images()  # Cargar imágenes antes de construir los controles
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()

    def get_project_root(self) -> str:
        """Encuentra y devuelve la ruta absoluta al directorio raíz del proyecto."""
        current_dir = os.path.dirname(__file__)
        # Este bucle sube en la jerarquía de directorios hasta que encuentra el directorio 'GUI_Login' o 'Modern_GUI'
        while os.path.basename(current_dir) not in {'GUI_Login', 'Modern_GUI'}:
            current_dir = os.path.dirname(current_dir)
            if current_dir == os.path.dirname(current_dir):  # Si llegamos al directorio raíz del sistema
                raise Exception("Directorio raíz del proyecto no encontrado.")
        return os.path.dirname(current_dir)  # Retorna el directorio padre del encontrado

    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Discovery')
        self.iconbitmap(self.resolve_path("Modern_GUI/imagen/logo.ico"))
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def resolve_path(self, relative_path):
        project_root = self.get_project_root()
        absolute_path = os.path.join(project_root, relative_path)
        print(f"Resolving path: {absolute_path}")  # Depuración para ver la ruta resuelta
        return absolute_path

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def load_images(self):
        # Asegúrate de que la ruta sea correcta, especialmente si has cambiado nombres de carpetas
        path_logo = self.resolve_path("Modern_GUI/imagen/logo.png")
        path_perfil = self.resolve_path("Modern_GUI/imagen/Perfil.png")
        self.logo = util_img.leer_imagen(path_logo, (560, 136))
        self.perfil = util_img.leer_imagen(path_perfil, (100, 100))
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Aquí asumimos que la instancia de CargadorExcel ya ha sido creada,
        # por ejemplo, en el método __init__ de FormularioMaestroDesign.
        self.cargador_excel = CargadorExcel(self)

        # En lugar de una etiqueta, usamos un botón que se vea como una etiqueta
        self.buttonCargarExcel = tk.Button(self.barra_superior, text="Cargar Excel",
                                           command=self.cargador_excel.cargar_excel, font=("Roboto", 15),
                                           bg=COLOR_BARRA_SUPERIOR, fg="#fff", bd=0, highlightthickness=0)
        self.buttonCargarExcel.pack(side=tk.LEFT, padx=10)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Farmacias Peruanas")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):

        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
         
         # Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        
        self.buttonDashBoard = tk.Button(self.menu_lateral)        
        self.buttonProfile = tk.Button(self.menu_lateral)        
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)        
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", "\uf109", self.buttonDashBoard),
            ("Buscador", "\uf007", self.buttonProfile),
            ("Filtrador", "\uf03e", self.buttonPicture),
            ("Comparador", "\uf129", self.buttonInfo),
            ("Cesados", "\uf013", self.buttonSettings)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

    def controles_cuerpo(self):
        # Define el área principal como un Frame en la UI
        self.cuerpo_principal = tk.Frame(self, bg='white')
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

        # Cargar y mostrar el logo
        self.logo_image = util_img.leer_imagen("Modern_GUI/imagen/logo.png",
                                               (560, 136))  # Ajusta el tamaño según sea necesario
        self.logo_label = tk.Label(self.cuerpo_principal, image=self.logo_image)
        self.logo_label.pack(expand=True)  # Centrar el logo

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def controles_cuerpo(self):
        # Define el área blanca como un Frame
        self.cuerpo_principal = tk.Frame(self, bg='white')
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)