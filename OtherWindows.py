from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTableWidget, QAbstractItemView
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QInputDialog, QMessageBox
from PyQt5 import QtCore
import sys


class MarksWindow(QMainWindow):  # Класс окна статистики оценок
    def __init__(self):
        super().__init__()
        self.bd = sqlite3.connect('DataBase/project.sqlite')  #
        self.cursor = self.bd.cursor()
        self.initUI()

    def initUI(self):  # Создание дизайна окна
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Статистика оценок')
        add_mark_button = QPushButton(self)  # Создание кнопки для добавления оценки
        add_mark_button.setGeometry(160, 50, 140, 30)
        add_mark_button.setText('Добавить оценку')
        add_mark_button.clicked.connect(self.add_mark)
        add_subject_button = QPushButton(self)  # Создание кнопки для добавления предмета
        add_subject_button.setGeometry(10, 50, 140, 30)
        add_subject_button.setText('Добавить предмет')
        add_subject_button.clicked.connect(self.add_subject)
        delete_button = QPushButton(self)  # Добавление кнопки для удаления предмета/оценки
        delete_button.setGeometry(310, 52, 24, 24)
        delete_button.setIcon(QIcon('design/delete1.png'))  # Назначение иконки кнопки
        delete_button.setIconSize(QSize(24, 24))
        delete_button.clicked.connect(self.delete_subject)
        picture_show = QLabel(self)  # Создание labelа для отображения изображения
        picture_show.setGeometry(0, 0, 500, 40)
        pixmap = QPixmap('design/markswindow_picture.png')  # Назначение изображения
        picture_show.setPixmap(pixmap)
        self.table = QTableWidget(self)  # Создание таблицы
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Отключение редактирования
        self.table.setGeometry(10, 90, 480, 300)
        self.apdate_table()

    def apdate_table(self):  # функция обновления таблицы
        self.subjects = self.cursor.execute("""SELECT name FROM subjects
                                """).fetchall()  # Взятие названий предметов из базы данных
        self.subjects_to_table = list()  #
        for i in range(len(self.subjects)):
            self.subjects_to_table.append(self.subjects[i][0])
        self.subjects_to_table.sort()
        ROW_COUNT = len(self.subjects_to_table)  # Постоянное количество строк
        COLUMNS_COUNT = 4  # Постоянное количество столбцов
        self.table.setRowCount(ROW_COUNT)
        self.table.setColumnCount(COLUMNS_COUNT)
        self.table.setHorizontalHeaderLabels(['Предмет',
                                              'Все оценки',
                                              'Средняя оценка',
                                              'Предпологаемая оценка'])  # Назначение значений столбцов
        counter = 0
        for subject in self.subjects_to_table:  # Цикл назначения ячеек 1ого столбца
            self.table.setItem(counter, 0, QTableWidgetItem(subject))
            counter += 1
        counter = 0
        for i in range(len(self.subjects_to_table)):  # Цикл назначения ячеек остальных столбцов
            subject = self.subjects_to_table[i]
            subject_id = self.cursor.execute(f'''SELECT id FROM subjects
            WHERE name = "{subject}"''').fetchall()[0][0]
            marks = [str(*mark) for mark in self.cursor.execute(f'''SELECT mark FROM marks
            WHERE subject_id = {subject_id}''').fetchall()]
            self.table.setItem(counter, 1, QTableWidgetItem(', '.join(marks)))
            marks = [int(*mark) for mark in self.cursor.execute(f'''SELECT mark FROM marks
            WHERE subject_id = {subject_id}''').fetchall()]
            sum_of_marks = sum(marks)
            num_of_marks = len(marks)
            if num_of_marks:
                middle_mark = round(sum_of_marks / num_of_marks, 2)
                self.table.setItem(counter, 2, QTableWidgetItem(str(middle_mark)))
                if num_of_marks >= 3:
                    self.table.setItem(counter, 3, QTableWidgetItem(str(round(middle_mark))))
                else:
                    self.table.setItem(counter, 3, QTableWidgetItem('Недостаточно оценок'))
            counter += 1
        self.table.resizeColumnsToContents()  # Изменение размера столбцо под контент
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Отключение изменения размера

    def add_mark(self):  # Функция добавления оценки
        subject, ok_pressed = QInputDialog.getItem(self, "Выберите предмет", "Выберите предмет:",  # Диалоговое окно
                                                   ('---', *self.subjects_to_table), 0, False)
        if ok_pressed:
            if subject and subject != '---':
                subject_id = self.cursor.execute(f'''SELECT id FROM subjects 
                            WHERE name = "{subject}"''').fetchall()[0][0]
                mark, ok_pressed = QInputDialog.getItem(self, 'Выберите оценку', 'Выберите оценку:',
                                                        ('---', '5', '4', '3', '2'), 0, False)
                if ok_pressed:
                    if mark and mark != '---':
                        self.cursor.execute(f'''INSERT INTO marks(subject_id, mark)
                         VALUES ({subject_id}, {mark})''')  # Запись оценки в файл
                        self.bd.commit()
                        self.apdate_table()  # Обновление таблицы
                    else:
                        QMessageBox.warning(self, 'Ошибка выбора оценки', 'Пожалуйста введите оценку!',
                                            QMessageBox.Ok)  # Уведомление об отсутствии оценки
            else:
                QMessageBox.warning(self, 'Ошибка выбора предмета', 'Пожалуйста введите название предмета!',
                                    QMessageBox.Ok)  # Уведомление об отсутствии названия предмета

    def add_subject(self):  # Функция добавления предмета
        subject_to_add, ok_pressed = QInputDialog.getText(self, "Выберите предмет", "Выберите предмет:")
        if ok_pressed:
            if subject_to_add:
                if subject_to_add[0].isalpha():
                    subject_to_add = subject_to_add[0].upper() + subject_to_add[1:]
                try:
                    self.cursor.execute(f'''INSERT INTO subjects(name) VALUES ('{subject_to_add}')''')  #
                    self.bd.commit()
                    self.apdate_table()  #
                except sqlite3.IntegrityError:
                    QMessageBox.warning(self, 'Ошибка добавления предмета', 'Предмет с таким названием уже добавлен!',
                                        QMessageBox.Ok)  # Уведомление о наличии предмета с таким названием
            else:
                QMessageBox.warning(self, 'Ошибка добавления предмета', 'Пожалуйста введите название предмета!',
                                    QMessageBox.Ok)  # Уведомление об отсутствии названия предмета
        self.apdate_table()

    def delete_subject(self):  # Функция удаления предмета
        for i in self.table.selectedIndexes():
            self.subjects.sort()
            subject = self.subjects[i.row()][0]
            subject_id = self.cursor.execute(f'''SELECT id FROM subjects
                        WHERE name = "{subject}"''').fetchall()[0][0]
            if i.column() == 0:
                quest = QMessageBox.question(self, 'Подтверждение удаления',
                                             'Вы действительно хотите удалить этот предмет?',
                                             QMessageBox.Yes | QMessageBox.No)
                if quest == QMessageBox.Yes:
                    self.cursor.execute(f"""DELETE from subjects
    where name = '{subject}'""")
                    self.bd.commit()
                    self.cursor.execute(f"""DELETE from marks
    where subject_id = {subject_id}
    """)
                    self.table.removeRow(i.row())

            if i.column() == 1:
                if self.table.item(i.row(), 1).text():
                    quest = QMessageBox.question(self, 'Подтверждение удаления',
                                                 'Вы действительно хотите удалить оценки?',
                                                 QMessageBox.Yes | QMessageBox.No)
                    if quest == QMessageBox.Yes:
                        self.cursor.execute(f"""DELETE from marks
                        where subject_id = {subject_id}""")
                        self.bd.commit()
                        self.table.setItem(i.row(), 2, QTableWidgetItem(None))
                        self.table.setItem(i.row(), 3, QTableWidgetItem(None))
                else:
                    QMessageBox.warning(self, 'Ошибка удаления',
                                        'В данной ячейке отсутствуют оценки!',
                                        QMessageBox.Ok)
            self.apdate_table()


class EventWindow(QMainWindow):  # Класс окна уведомления
    def __init__(self, event):
        super().__init__()
        self.event = str(event)  # Принятие названия начавшегося события
        uic.loadUi('Ui_design/EventWindow_design.ui', self)  #
        self.initUI()

    def initUI(self):  # Доработка дизайна
        self.setWindowTitle('Начало события')
        self.ok_button.setStyleSheet("background-color : #0078d7")  # Окрашивание кнопки
        self.event_label.setText(f'Начинается занятие:\n{self.event}')  # Редактирование текста
        self.event_label.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание по центру
        self.ok_button.clicked.connect(self.close)  # Присвоение функции закрытия кнопке
        event_to_check = self.event.lower()

        if event_to_check == 'урок':  # Определение типа события
            self.label.setPixmap(QPixmap('design/zvonok.png'))

        elif event_to_check.split()[0] == 'урок':
            self.label.setPixmap(QPixmap('design/zvonok.png'))

        elif event_to_check == 'занятие с репетитором':
            self.label.setPixmap(QPixmap('design/repetitor.png'))

        elif ' '.join(event_to_check.split()[0:3]) == 'занятие с репетитором':
            self.label.setPixmap(QPixmap('design/repetitor.png'))

        elif event_to_check == 'художественная школа':
            self.label.setPixmap(QPixmap('design/art_school.png'))

        elif ' '.join(event_to_check.split()[0:2]) == 'художественная школа':
            self.label.setPixmap(QPixmap('design/art_school.png'))

        elif event_to_check == 'спортивная секция':
            self.label.setPixmap(QPixmap('design/sport.png'))

        elif ' '.join(event_to_check.split()[0:2]) == 'спортивная секция':
            self.label.setPixmap(QPixmap('design/sport.png'))

        elif event_to_check == 'занятие в бассейне':
            self.label.setPixmap(QPixmap('design/basseyn.png'))

        elif event_to_check.split()[0] == 'занятие в бассейне':
            self.label.setPixmap(QPixmap('design/basseyn.png'))

        else:
            self.label.setPixmap(QPixmap('design/reminder.png'))


if __name__ == '__main__':  # Открытие программы
    app = QApplication(sys.argv)
    ex = EventWindow('Занятие в Яндекс Лицее')
    ex.show()
    sys.exit(app.exec_())
