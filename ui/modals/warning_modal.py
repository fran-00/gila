from PySide6.QtWidgets import QVBoxLayout, QLabel

from .parent_modal import Modal


class WarningModal(Modal):

    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Avviso")
        self.on_modal_layout()

    def on_modal_layout(self):
        """ Creates modal layout and calls methods that adds widgets """
        self.modal_layout = QVBoxLayout(self)
        self.modal_text = QLabel("Messaggio di avviso da sovrascrivere.")
        self.modal_layout.addWidget(self.modal_text)
        self.on_dismiss_button()

    def on_no_internet_connection_label(self):
        self.modal_text.setText("Il computer non è connesso ad internet, controlla la connessione e riprova.")

    def on_key_is_valid_label(self):
        self.modal_text.setText("La chiave API è valida ed è stata registrata con successo!")

    def on_key_is_not_valid_label(self):
        self.modal_text.setText("La chiave API che hai inserito non è valida, riprova.")
