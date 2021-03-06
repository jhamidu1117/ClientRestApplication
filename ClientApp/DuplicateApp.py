from PyQt5 import QtWidgets, QtGui, QtMultimedia, QtCore, QtNetwork

from ClientApp.DuplicateView import Ui_MainWindow
from datetime import datetime
import dateutil.parser

import re
import sys
import os
import json


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        url = QtCore.QUrl.fromLocalFile(self.scriptDir + os.path.sep + 'Resources/Alarm.mp3')
        self.rest_url = "http://127.0.0.1:8000/api/trg-list/"
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.setWindowIcon(QtGui.QIcon(self.scriptDir + os.path.sep + 'Resources/Logo2.ico'))
        self.setWindowTitle('TRG-Duplicate Tracker')
        self.ui.Enter.clicked.connect(self.clickMethod)
        self.ui.TrgLineEdit.returnPressed.connect(self.clickMethod)
        self.currentLocation = ''

    def clickMethod(self):
        line = self.ui.TrgLineEdit.text()
        if re.search('TRG.*', line):
            if self.currentLocation == '':
                self.player.play()
                self.ui.TrgLineEdit.clear()

            self.req = QtNetwork.QNetworkRequest(QtCore.QUrl(self.rest_url))
            self.req.setRawHeader(QtCore.QByteArray(b"Authorization"),
                                  QtCore.QByteArray(b"Token b80f6a9d350fe27bcde23084d47efc304dfd55c4"))
            # self.req.deleteLater()
            self.nam = QtNetwork.QNetworkAccessManager()
            self.nam.finished.connect(self.handle_response)
            self.nam.get(self.req)

        elif re.search('L.*', line):
            self.ui.LocationLabel.setText('Location: ' + line)
            self.currentLocation = line
            self.ui.TrgLineEdit.clear()

    def handle_response(self, reply):

        er = reply.error()
        reply.deleteLater()
        reply.downloadProgress.connect(self.addProgressbar)

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            string = str(bytes_string, 'utf-8')
            data = json.loads(str(bytes_string, 'utf-8'))
            print(data)
            i = 0
            progressBar = 0
            for v in data:
                dateformat = dateutil.parser.parse(str(v['timestamp']))
                datetime_str = datetime.strftime(dateformat, '%H:%M:%S %m/%d/%y')
                self.ui.OutputTable.setRowCount(i + 1)
                self.ui.OutputTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(v['trg_id'])))
                self.ui.OutputTable.setItem(i, 1, QtWidgets.QTableWidgetItem(datetime_str))
                self.ui.OutputTable.setItem(i, 2, QtWidgets.QTableWidgetItem(str(v['location'])))
                i += 1
                progressBar += 25
                self.ui.progressBar.setValue(progressBar)

            self.ui.TrgLineEdit.clear()
            self.ui.progressBar.setValue(0)

        else:
            print("Error occured: ", er)
            print(reply.errorString())
            self.ui.TrgLineEdit.clear()

    def addProgressbar(self, bytesReceived, bytesTotal):
        while bytesReceived != bytesTotal:
            progress = bytesReceived/bytesTotal
            self.ui.progressBar.setValue(progress)


app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())
