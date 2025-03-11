import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.ll = [37.530887, 55.703118]
        self.spn = [0.002, 0.002]
        self.map_theme = "light"
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = '&'.join(['ll=' + ','.join(map(str, self.ll)), 'spn=' + ','.join(map(str, self.spn))])
        theme_param = f'&theme={self.map_theme}'
        map_request = f"{server_address}{ll_spn}{theme_param}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.change_theme = QPushButton('Сменить тему карты', self)
        self.change_theme.move(0, 0)
        self.change_theme.resize(120, 40)
        self.change_theme.clicked.connect(self.change_map_theme)
        self.setFocus()

    def update_image(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.setFocus()

    def change_map_theme(self):
        self.map_theme = "dark" if self.map_theme == "light" else "light"
        self.update_image()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            if self.spn[0] == 1.0 or self.spn[1] == 1.0:
                return
            self.spn = [el + 0.001 for el in self.spn]
        if event.key() == Qt.Key.Key_PageDown:
            if self.spn[0] == 0.001 or self.spn[1] == 0.001:
                return
            self.spn = [el - 0.001 for el in self.spn]
        if event.key() == Qt.Key.Key_Up:
            self.ll[1] += 0.005
            if self.ll[1] > 90:
                self.ll[1] = 90
        if event.key() == Qt.Key.Key_Down:
            self.ll[1] -= 0.005
            if self.ll[1] < -90:
                self.ll[1] = -90
        if event.key() == Qt.Key.Key_Left:
            self.ll[0] -= 0.005
            if self.ll[0] < -180:
                self.ll[0] = -180
        if event.key() == Qt.Key.Key_Right:
            self.ll[0] += 0.005
            if self.ll[0] > 180:
                self.ll[0] = 180
        self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
