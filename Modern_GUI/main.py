from formularios.form_maestro_design import FormularioMaestroDesign

def open_dashboard():
    app = FormularioMaestroDesign()
    app.mainloop()

if __name__ == "__main__":
    open_dashboard()