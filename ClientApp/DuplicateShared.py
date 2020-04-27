import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QSlider, QTextEdit, QGridLayout
from PyQt5.QtWidgets import QPushButton, QMessageBox, QAction, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QSize, QUrl
import bcrypt


import re
import os
import pandas as pd
import io

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/Logo2.ico'))
        self.setMinimumSize(QSize(400, 100))
        self.setWindowTitle('TRG-Duplicate Tracker')

        bar = self.menuBar()
        account_menu = bar.addMenu('Accounts')
        login_action = QAction('Login', self)
        login_action.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/ChangeUser.ico'))
        login_action.triggered.connect(self.logout)
        
        logout_action = QAction('Logout', self)
        logout_action.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/LogOut.ico'))
        logout_action.triggered.connect(self.logout)
        
        signup_action = QAction('New Account', self)
        signup_action.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'Resources/AddUser.ico'))
        signup_action.triggered.connect(self.addUser)

        account_menu.addAction(login_action)
        account_menu.addAction(logout_action)
        account_menu.addAction(signup_action)

        self.newAccountWidget = SignUpWidget()
        self.loginWidget = LoginWidget()
        self.layout = QStackedLayout()

        self.layout.addWidget(self.loginWidget)
        self.layout.addWidget(self.newAccountWidget)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


    def addUser(self):
        self.newAccountWidget.nameEdit.clear()
        self.newAccountWidget.PswdEdit.clear()
        self.newAccountWidget.pswdConEdit.clear()
        self.layout.setCurrentIndex(1)
        self.newAccountWidget.layout.setCurrentIndex(0)
    def logout(self):
        self.loginWidget.enterUserName.clear()
        self.loginWidget.enterPSWD.clear()
        self.layout.setCurrentIndex(0)
        self.loginWidget.layout.setCurrentIndex(0)


class LoginWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        url = QUrl.fromLocalFile(scriptDir + os.path.sep + 'Resources/Alarm.mp3')
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.blankWidget = QWidget()
        self.dupWidget = DuplicateTracker()
        self.layout = QStackedLayout()

        self.usrn = ''
        self.pswd = ''
        self.initUI()

    def initUI(self):
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.loginMethod)
        self.enterUserName = QLineEdit()
        self.enterUserName.setPlaceholderText('example@gotrg.com')
        self.enterPSWD = QLineEdit()
        self.enterPSWD.setPlaceholderText('*******')
        self.enterPSWD.setEchoMode(QLineEdit.Password)

        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.enterUserName)
        self.hbox.addWidget(self.enterPSWD)
        self.hbox.addWidget(self.okButton)
        self.hbox.addStretch(1)

        self.blankWidget.setLayout(self.hbox)
        self.layout.addWidget(self.blankWidget)
        self.layout.addWidget(self.dupWidget)
        self.setLayout(self.layout)


    def loginMethod(self):
        self.usrn = self.enterUserName.text()
        self.pswd = self.enterPSWD.text()
        userBase = pd.read_csv(r'Users.csv', index_col='User')
        if self.usrn in userBase.index:
            epswd = str(self.pswd).encode('UTF-8')
            basepswd = str(userBase.loc[self.usrn, 'hash']).encode('UTF-8')
            if bcrypt.checkpw(epswd, basepswd):
                print('Password Accepted')
                self.layout.setCurrentIndex(1)
            else:
                print('incorrect password')
        else:
            print('user not found')
            print(userBase)


class SignUpWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.blankWidget = QWidget()
        self.dupWidget = DuplicateTracker()
        self.layout = QStackedLayout()
        self.initUI()

    def initUI(self):
        self.helpLable = QLabel()
        self.helpLable.setText('Enter new username and Password')
        self.nameLable = QLabel()
        self.nameLable.setText('User Name: ')
        self.pswdLable = QLabel()
        self.pswdLable.setText('PassWord: ')
        self.pswdConfirm = QLabel()
        self.pswdConfirm.setText('Confirm Password: ')
        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText('User')
        self.PswdEdit = QLineEdit()
        self.PswdEdit.setPlaceholderText('****')
        self.PswdEdit.setEchoMode(QLineEdit.Password)
        self.pswdConEdit = QLineEdit()
        self.pswdConEdit.setPlaceholderText('****')
        self.pswdConEdit.setEchoMode(QLineEdit.Password)
        self.saveButton = QPushButton()
        self.saveButton.setText('Save')
        self.saveButton.clicked.connect(self.storepswd)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.helpLable, 0, 1)
        grid.addWidget(self.nameLable, 1, 0)
        grid.addWidget(self.nameEdit, 1, 1)
        grid.addWidget(self.pswdLable, 2, 0)
        grid.addWidget(self.PswdEdit, 2, 1)
        grid.addWidget(self.pswdConfirm, 3, 0)
        grid.addWidget(self.pswdConEdit, 3, 1)
        grid.addWidget(self.saveButton, 4, 1)

        self.blankWidget.setLayout(grid)
        self.layout.addWidget(self.blankWidget)
        self.layout.addWidget(self.dupWidget)
        self.setLayout(self.layout)

    def storepswd(self):
        if self.PswdEdit.text() == self.pswdConEdit.text():
            userBase = pd.read_csv(r'Users.csv', index_col='User')
            if self.nameEdit.text() not in userBase.index:
                userBase.reset_index(inplace=True)
                pwd = str(self.PswdEdit.text()).encode('UTF-8')
                salt = bcrypt.gensalt()
                slug = bcrypt.hashpw(pwd, salt)
                users = pd.DataFrame({'User': [self.nameEdit.text()],
                                      'hash': [bytes(slug).decode('UTF-8')]})
                #print(userBase)
                #print(users)
                userBase = userBase.append(users, sort=False, ignore_index=True)
                userBase.to_csv(r'Users.csv', index=False, header=True)
                self.nameEdit.clear()
                self.PswdEdit.clear()
                self.pswdConEdit.clear()
                self.layout.setCurrentIndex(1)
            else:
                QMessageBox.about(self, 'Warning', 'Username Taken')
                self.nameEdit.clear()
                self.PswdEdit.clear()
                self.pswdConEdit.clear()
        else:
            QMessageBox.about(self, 'Warning', 'Passwords did not match')
            self.nameEdit.clear()
            self.PswdEdit.clear()
            self.pswdConEdit.clear()


class DuplicateTracker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        url = QUrl.fromLocalFile(scriptDir + os.path.sep + 'Alarm.mp3')
        content = QMediaContent(url)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.currentLocation = ''
        self.initUI()

    def initUI(self):
        self.scanlabel = QLabel('TRGs:')

        self.scanline = QLineEdit()
        self.scanline.setPlaceholderText('TRG-#########')

        self.histdisp = QTextEdit()
        self.histdisp.setFrameStyle(QTextEdit.NoFrame)
        self.histdisp.viewport().setAutoFillBackground(False)
        self.histdisp.setLineWrapMode(QTextEdit.NoWrap)
        self.histdisp.setReadOnly(True)

        self.enterbutton = QPushButton('Enter')
        self.enterbutton.clicked.connect(self.clickMethod)
        self.scanline.returnPressed.connect(self.clickMethod)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.scanlabel, 0, 0)
        grid.addWidget(self.scanline, 1, 0)
        grid.addWidget(self.enterbutton, 2, 0)
        grid.addWidget(self.histdisp, 1, 1, 2, 1)

        self.setLayout(grid)


    def clickMethod(self):
        print(self.scanline.text())
        line = self.scanline.text()
        self.scanline.clear()
        data = pd.read_csv(r'TRGs.csv', index_col='TRGID')
        if re.search('TRG.*', line):
            if self.currentLocation == '':
                self.player.play()
                QMessageBox.about(self, 'Warning', 'Scan Location To Continue')
                return 0

            newtext = re.sub(' ', '', line)
            newTRG = pd.DataFrame({'TRGID': [newtext],
                                   'timeStamp': [pd.Timestamp.now()],
                                   'Location': [self.currentLocation]})
            newTRG['timeStamp'] = newTRG['timeStamp'].apply(lambda x: x.strftime('%x %X'))

            if newtext in data.index:
                self.player.play()
                QMessageBox.about(self, 'Warning', 'Duplicate Found:\nPlease Notify your line lead\n' + newtext)
                return 0

            data.reset_index(inplace=True)
            data = data.append(newTRG, ignore_index=True, sort=False)
            data.to_csv(r'TRGs.csv', index=False, header=True)
            result = data.tail(3)
            result = result.to_string(index=False)
            self.histdisp.setText(result)
        elif re.search('L.*', line):
            print('Location updated' + line)
            self.scanlabel.setText('Location: ' + line)
            self.currentLocation = line
        else:
            self.player.play()
            QMessageBox.about(self, 'Warning', 'TRG not Found')
            return 0



if __name__ == "__main__":
    wk_dir = os.path.dirname('__file__')
    excelFile = 'TRGs.csv'
    excelPath = os.path.join(wk_dir, excelFile)
    TRGs = pd.read_csv(excelPath)

    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

