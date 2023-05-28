import sys
import time as tm
import datetime as dt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QApplication, QPushButton
from PyQt5.QtCore import QTimer, QSize
from ProgramDialogs import TimeDialog
from OtherWindows import MarksWindow, EventWindow
from PyQt5.QtGui import QPixmap, QIcon
import re


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.file = open('events.txt', mode='r+', encoding='utf-8')  # Открытие файла
        self.read_file = self.file.read().split('\n')
        self.file.close()
        uic.loadUi('Ui_design/MainWindow_design.ui', self)  # Загрузка дизайн
        self.setFixedWidth(800)  # Установка фиксированного размера окна
        self.setFixedHeight(620)
        self.setWindowIcon(QIcon('design/icon.png'))
        self.setWindowTitle('Календарь школьника')
        self.add_event_button.clicked.connect(self.add_data)
        self.add_event_button.setStyleSheet("background-color : #0078d7")  # Окрас кнопки
        self.markwin_openbutton.clicked.connect(self.open_markwindow)
        self.markwin_openbutton.setStyleSheet("background-color : #0078d7")
        pixmap = QPixmap('design/ceiling_picture.png')  # Назначение изображений
        pixmap2 = QPixmap('design/down_picture.png')
        self.ceiling_picture.setPixmap(pixmap)  # И отображение их
        self.down_picture.setPixmap(pixmap2)
        self.delete_button = QPushButton(self)
        self.delete_button.setGeometry(740, 160, 20, 20)
        self.delete_button.clicked.connect(self.delete_event)
        self.delete_button.setIcon(QIcon('design/delete2.png'))  # Назначение иконки кнопки
        self.delete_button.setIconSize(QSize(20, 20))
        self.calendar.clicked.connect(self.show_events)  # Назначение по нажатию на календарь отображения событий
        self.create_timer()  # Запуск создания таймеров для напоминаний

    def create_timer(self):  # Функция создания таймера

        self.file = open('events.txt', mode='r+', encoding='utf-8')
        self.read_file = self.file.read().split('\n')
        self.file.close()
        self.ddd = dict()
        self.intervals_list = list()
        self.events_list = list()

        for event in self.read_file:  # Цикл взятия событий принадлежащих сегоднешнему дню
            if event:
                time_now = dt.datetime.now()
                event_date, event_time, evnt = event.split('-')
                event_year, event_month, event_day = event_date.split(', ')
                event_hour, event_minute = event_time.split(', ')
                event_datetime = dt.datetime(int(event_year), int(event_month), int(event_day), int(event_hour),
                                             int(event_minute))

                tdelta = event_datetime - time_now
                time_to_timer = int(tdelta.total_seconds())
                if time_to_timer > 0:
                    self.intervals_list.append(time_to_timer)
                    self.events_list.append(evnt)
                    self.ddd[time_to_timer] = evnt

        self.sorted_rooms = dict(sorted(self.ddd.items(), key=lambda item: item[0]))
        self.sorted_events = list(self.sorted_rooms.values())
        self.intervals_list.sort()
        self.count = 0
        try:
            if len(self.intervals_list) != 0:
                self.a = QTimer()  # Создание таймера
                self.a.setInterval(self.intervals_list[0] * 1000)
                self.a.timeout.connect(self.timer)
                self.a.start()
        except OverflowError:
            pass

    def timer(self):  # Функция оповещения о начале события и запуска нового таймера
        self.event_remind = EventWindow(f'{self.sorted_events[self.count][0].upper()}'
                                        f'{self.sorted_events[self.count][1:]}')
        self.event_remind.show()
        self.a.setInterval((self.intervals_list[self.count + 1] - self.intervals_list[self.count]) * 1000)  #
        self.a.start()  # Запуск таймера
        self.count += 1

    def add_data(self):  # Функция, добавляющая дату в файл
        file = open('events.txt', mode='r+', encoding='utf-8')  # Открытие файла
        data = str(self.calendar.selectedDate())  # Переменная с выбранной датой
        data_to_write = data.split('(')[1].replace(')', '')  # Переменная приводящая дату к виду: Число, Месяц, Дата
        event, ok_pressed = QInputDialog.getItem(self, "Введите событие", "Добавить:",  # Диалоговое окно
                                                 ('Введите или выберите событие', 'Урок', 'Занятие с репетитором',
                                                  'Спортивная секция', 'Художественная школа', 'Занятие в бассейне'), 0,
                                                 True)
        if ok_pressed:
            if event and event != 'Введите или выберите событие':  # Проверка на наличие введенного события
                timedial = TimeDialog()  # Вызов диалога для получения времени
                if timedial.exec():
                    time = str(timedial.getItem())
                    time_to_write = time.split('(')[1].replace(')', '')  # Преобазование времени
                    file.seek(0, 2)
                    file.write(f'\n {data_to_write}-{time_to_write}-{event}')
                    file.close()
                    self.create_timer()  # Запись события в файл
            else:
                QMessageBox.warning(self, 'Введите название', 'Пожалуйста введите название события!',
                                    QMessageBox.Ok)  # Открытие уведомления о отсутствии названия события
        file.close()  # Закрытие файла

    def show_events(self):  # Функция для отображения событий
        self.events_list_wg.clear()  # Очистка виджета от прошлых записей
        file = open('events.txt', mode='r+', encoding='utf-8')  # Открытие файла
        read_file = file.read().split('\n')
        data = str(self.calendar.selectedDate()).split('(')[1].replace(')', '')  # Переменная с выбранной датой
        events_to_show = dict()
        for position in read_file:  # Цикл отбора событий на выбранную дату
            if position:
                if position.find(data) != -1:
                    pos_to_remake = position.split('-')
                    time_to_remake = pos_to_remake[1].split(', ')
                    event_to_add = pos_to_remake[2]
                    if len(time_to_remake[1]) == 1:
                        events_to_show[f'{time_to_remake[0]}:0{time_to_remake[1]}'] = event_to_add
                    else:
                        events_to_show[f'{time_to_remake[0]}:{time_to_remake[1]}'] = event_to_add
        format = '%H:%M'
        time_hours = [tm.strptime(t, format) for t in events_to_show.keys()]
        result = [tm.strftime(format, h) for h in sorted(time_hours)]  # Сортировка времени событий
        self.events = list()
        for time in result:  # Цикл добавления событий в виджет
            if time[0] == '0':
                self.events.append(f'{time} - {events_to_show[time[1:]]}')
            else:
                self.events.append(f'{time} - {events_to_show[time]}')
        for event in self.events:
            self.events_list_wg.addItem(event)

        file.close()  # Закрытие файла

    def open_markwindow(self):  # Открытие окна со статистикой оценок
        self.markwin = MarksWindow()
        self.markwin.show()

    def delete_event(self):  # Функция для удаления событий
        with open('events.txt', encoding='utf-8') as f:  # Считываем строки из файла
            lines = f.readlines()
            f.close()
        event = self.events[self.events_list_wg.currentRow()]
        time_to_delete = event.split(' - ')[0].split(':')
        if time_to_delete[0][0] == '0':  # Удаление лишнего из time_to_delete
            time_to_delete[0] = time_to_delete[0][1:]
        if time_to_delete[1][0] == '0':
            time_to_delete[1] = time_to_delete[1][1:]
        time_to_delete = ', '.join(time_to_delete)
        name_to_delete = event.split(' - ')[1]
        date_to_delete = str(self.calendar.selectedDate()).split('(')[1].replace(')', '')
        event_to_delete = f' {"-".join([date_to_delete, time_to_delete, name_to_delete])}\n'
        pattern = re.compile(re.escape(event_to_delete))  # Удаляем событие
        with open('events.txt', mode='w', encoding='utf-8') as f:  # Проверяем удаление
            for line in lines:
                result = pattern.search(line)
                if result is None:
                    f.write(line)
        f.close()  # Закрываем файл
        self.show_events()
        event_to_delete = f' {"-".join([date_to_delete, time_to_delete, name_to_delete])}'  # event_to_delete без \n
        pattern = re.compile(re.escape(event_to_delete))  # Удаляем если событие было добаленно последним
        with open('events.txt', mode='w', encoding='utf-8') as f:
            for line in lines:
                result = pattern.search(line)
                if result is None:
                    f.write(line)
        f.close()  # Закрытие файла
        self.show_events()  # Обновление QListWidget


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':  # Открытие программы
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
