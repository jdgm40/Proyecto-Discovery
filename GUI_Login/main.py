from forms.form_login import App
from Modern_GUI.main import open_dashboard

if __name__ == "__main__":
    app = App()
    if app.logged_in:
        open_dashboard()