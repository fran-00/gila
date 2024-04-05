from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CurrentSettings(QObject):

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.current_llm = None
        self.current_temperature = None
        self.llms = [
            "GPT-4",
            "GPT-4 Turbo",
            "GPT-3.5 Turbo",
            # "Gemini Pro",
            "Cohere Chat"
        ]
        self.widget_container = QWidget(objectName="current_settings_widget")
        self.on_current_settings_layout()

    def on_current_settings_layout(self):
        current_settings_layout = QVBoxLayout(self.widget_container)
        self.current_settings_label = QLabel("", objectName="settings_label")
        current_settings_layout.addWidget(self.current_settings_label)
        return current_settings_layout

    def update_settings_label(self, settings):
        """ Called from Controller when new chat is started, return current settings """
        self.chat_id = settings[0]
        self.chat_custom_name = settings[1]
        self.current_llm = settings[2]
        self.current_temperature = settings[3]
        self.current_chat_date = settings[4]
        settings_string = f"""<div>
            - <b>ID</b>: {self.chat_id}<br>
            - <b>Nome</b>: {self.chat_custom_name if self.chat_custom_name is not None else 'Nome non impostato'}<br>
            - <b>Modello</b>: {self.current_llm}<br>
            - <b>Temperatura</b>: {self.current_temperature}<br>
            - <b>Ultima modifica</b>: {self.current_chat_date if self.current_chat_date is not None else 'Appena creata'}
            </div>"""
        self.current_settings_label.setText(settings_string)

    def on_show_widgets(self):
        """ Shows settings label on call """
        self.widget_container.show()

    def on_hide_widgets(self):
        """ Hides settings label on call """
        self.widget_container.hide()
