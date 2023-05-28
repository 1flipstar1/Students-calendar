from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTimeEdit


class TimeDialog(QDialog):  # Класс диалогового окна принимающего время
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Введите время")
        button_box = QDialogButtonBox.Ok | QDialogButtonBox.Cancel  # Создание кнопок
        self.buttonBox = QDialogButtonBox(button_box)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.inp = QTimeEdit(self)  # Добавление принятия времени
        self.layout.addWidget(self.inp)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def getItem(self):  # Создание метода возврата времени
        return self.inp.time()



