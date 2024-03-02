import pandas as pd
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk

class CargadorExcel:
    def __init__(self, parent):
        self.parent = parent
        self.dfs = []  # Lista para almacenar los DataFrames cargados
        self.treeview = None  # Inicializa el Treeview como None

    def cargar_excel(self):
        """Permite al usuario cargar hasta 6 archivos Excel y los valida."""
        for _ in range(6):  # Permite cargar hasta 6 archivos
            filepath = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
            )
            if not filepath:  # Si el usuario cancela la selección del archivo
                break
            try:
                df = pd.read_excel(filepath, header=1)
                # Supongamos que validas el Excel aquí (podrías adaptar esta función según cada Excel)
                if self.validar_excel(df):
                    self.dfs.append(df)
                    if len(self.dfs) < 6:  # Pregunta si ya no se han cargado los 6 archivos
                        continuar = messagebox.askyesno("Continuar", "¿Deseas cargar otro archivo Excel?")
                        if not continuar:
                            break
                    else:
                        messagebox.showinfo("Información", "Se han cargado todos los archivos necesarios.")
                else:
                    messagebox.showerror("Error", "El archivo Excel no tiene la estructura esperada.")
                    break
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")
                break

        if self.dfs:
            messagebox.showinfo("Éxito", "Archivos Excel cargados correctamente.")
            # Aquí puedes realizar acciones adicionales ahora que los archivos están cargados

    def mostrar_datos_en_treeview(self, df):
        # Oculta o elimina el logo si está presente
        if hasattr(self.parent, 'logo_label'):
            self.parent.logo_label.pack_forget()

        # Elimina el Treeview anterior si existe
        if self.treeview:
            self.treeview.destroy()

        self.treeview = ttk.Treeview(self.parent.cuerpo_principal)
        self.treeview.pack(expand=True, fill='both')

        # Define las columnas del Treeview
        self.treeview['columns'] = df.columns.tolist()
        self.treeview.column("#0", width=0, stretch=tk.NO)  # Columna fantasma
        for col in df.columns:
            self.treeview.column(col, anchor=tk.CENTER, width=80)
            self.treeview.heading(col, text=col, anchor=tk.CENTER)

        # Agrega los datos del DataFrame al Treeview
        for i, row in df.iterrows():
            self.treeview.insert("", tk.END, values=row.tolist())

        # Desplazamiento vertical
        scrollbar = ttk.Scrollbar(self.parent.cuerpo_principal, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def validar_excel(self, df):
        """Valida la estructura básica de un DataFrame."""
        # Esta es solo una validación de ejemplo. Debes ajustarla según los índices específicos de cada Excel.
        columnas_esperadas = [
            'IDCPU', 'TIPO_REGISTRO', 'ESTADO', 'ASIGNADO_A', 'DNI', 'TIPO_ACTIVO', 'DIRECCION_IP', 'MAC_ADDRESS',
            'LOCAL', 'NOMBRE_ESTACION', 'NOMBRE_USUARIO', 'MARCA', 'MODELO', 'SERIE', 'TIPO_PROCESADOR_VELOCIDAD',
            'MEMORIA_RAM', 'SLOT_DE_MEMORIA', 'CAPACIDAD_DISCO_DURO', 'TIPO_HD', 'SISTEMA_OPERATIVO', 'VERSION_SO',
            'CODIGO_PATRIMONIAL', 'ORDEN_COMPRA', 'FECHA_COMPRA_OC', 'FIN_GARANTIA_OC', 'FECHA_COMPRA', 'FIN_GARANTIA',
            'ACTUALIZADO_HACE', 'PLANILLA', 'CARGO', 'AREA', 'GERENCIA', 'DIRECCION', 'CECO', 'SAP_FICO',
            'DESCRIPCION_CECO', 'ASIGNAR_A', 'TIPO_ESTADO', 'EJECUCION_ESTADO', 'CONFIRMACION'
        ]  # Ajusta esto según tus necesidades
        return all(columna in df.columns for columna in columnas_esperadas)

