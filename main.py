import sys

from PySide6.QtWidgets import QApplication

from core.model import Model, MainThread
from core.view import View
from core.controller import Controller


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()
    model = Model()
    thread = MainThread(model)
    controller = Controller(view, model, thread)
    view.show()

    sys.exit(app.exec())
