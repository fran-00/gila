from PySide6.QtWidgets import QToolBar, QFileDialog
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject


class ToolBar(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_icons()

    def on_toolbar(self):
        self.tb = QToolBar("Toolbar")
        self.on_save_chatlog_action()
        return self.tb

    def on_save_chatlog_action(self):
        save_action = QAction(self.save_icon, "&Esporta Conversazione", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Esporta Conversazione')
        save_action.triggered.connect(self.save_txt_file)
        self.tb.addAction(save_action)

    def on_manage_api_keys_action(self):
        api_keys_action = QAction(self.key_icon, "&Gestisci Chiavi API", self)
        api_keys_action.setStatusTip('Gestisci Chiavi API')
        api_keys_action.triggered.connect(self.open_api_keys_modal)
        self.tb.addAction(api_keys_action)

    def set_icons(self):
        save_icon_path = "ui/icons/floppy.svg"
        self.save_icon = QIcon()
        self.save_icon.addFile(save_icon_path)
        key_icon_path = "ui/icons/key.svg"
        self.key_icon = QIcon()
        self.key_icon.addFile(key_icon_path)

    def save_txt_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self.window, 'Esporta Conversazione', '.txt', '.txt', options = options)
        if file_name:
            with open(file_name, 'w') as file:
                text = self.window.chat.chat_widget.toPlainText()
                file.write(text)
