#######import##############
##PyQt5

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import urllib.request
import pafy

ui,_ = loadUiType('/home/mohamed/Desktop/udacity/Projects/MyDownloader/untitled.ui')

class MainApp(QMainWindow , ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI()
        self.Handle_btns()

    def UI(self):
        self.setWindowTitle('MyDownloder')
        self.setFixedSize(702,327)


    def Handle_btns(self):
        self.pushButton.clicked.connect(self.Browsebtn)
        self.pushButton_2.clicked.connect(self.Downloadbtn)
        self.pushButton_3.clicked.connect(self.Browsebtn2)
        self.pushButton_4.clicked.connect(self.Downloadbtn2)
        self.pushButton_5.clicked.connect(self.Searchbtn)
        self.pushButton_13.clicked.connect(self.Searchbtn2)
        self.spinBox.valueChanged.connect(self.valuechange)
        self.pushButton_12.clicked.connect(self.Browsebtn3)
        self.pushButton_11.clicked.connect(self.Downloadbtn3)
    def normalSize(self,size):
        L=["B","KB","MB","GB","TB"]
        c=0
        while (size>1024 and c< 4) :
            c+=1
            size/=1024
        size=((size*100)//1)/100
        return  "{} ".format(size)+L[c]
    ##########################################################################
    #############################DownloadFile#################################
    ##########################################################################

    def Browsebtn(self):
        saveLocation = QFileDialog.getSaveFileName(self , caption="Save As" , directory="C:\\Users\\Mohamed Sayed\\OneDrive\\Desktop" , filter="All Files (*.*)")
        saveLocation=str(saveLocation)
        name=saveLocation.split(',')[0].split("'")[1]
        self.lineEdit_2.setText(name)
    def Filesizelbl(self,size):
        self.label_3.setText("File Size : "+self.normalSize(size))

    def progressbar(self, blocknum , blocksize , totalsize):
        flag=0
        if flag == 0 :
            self.Filesizelbl(totalsize)
            flag=1
        read = blocknum * blocksize
        percent= read *100 /totalsize
        self.progressBar.setValue(percent)
        QApplication.processEvents() # solve Not Responding problem

    def MyReset(self):
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.label_3.setText("File Size : ")

    def Downloadbtn(self):
        url=self.lineEdit.text()
        saveLocation=self.lineEdit_2.text()

        #urllib ==> (url , saveLocation ,progress)
        try:
            urllib.request.urlretrieve(url,saveLocation,self.progressbar)
        except Exception :
            QMessageBox.warning(self,"Download Error","The Download Faild")
            self.MyReset()
            return
        QMessageBox.information(self,"Download Completed","The Download Finished")
        self.MyReset()
##########################################################################
########################YouTubeDownloadVideo##############################
##########################################################################

    def Searchbtn(self):
        url = self.lineEdit_4.text()
        if self.comboBox.count() > 0:
            self.comboBox.clear()
        try:
            myvid = pafy.new(url)
            mystreams=myvid.streams
            for s in mystreams :
                size=self.normalSize(s.get_filesize())
                data="{}  {}  {}".format(s.extension,s.quality,size)
                self.comboBox.addItem(data)
        except Exception:
            QMessageBox.warning(self, "Wrong URL", "Enter Valid URL")
            return
        self.pushButton_3.setEnabled(True)
        self.comboBox.setEnabled(True)



    def Browsebtn2(self):
        saveLocation = QFileDialog.getExistingDirectory(self, caption="Save As",
                                                   directory="C:\\Users\\Mohamed Sayed\\OneDrive\\Desktop")

        saveLocation = str(saveLocation)
        self.lineEdit_3.setText(saveLocation)
        self.pushButton_4.setEnabled(True)



    def progressbar2(self,total, recvd, ratio, rate, eta):
        percent = recvd * 100 / total
        self.progressBar_2.setValue(percent)
        QApplication.processEvents()  # solve Not Responding problem

    def Filesizelbl2(self,size):
        self.label_5.setText("Video Size : " +self.normalSize(size))

    def MyReset2(self):
        self.progressBar_2.setValue(0)
        self.lineEdit_4.setText('')
        self.lineEdit_3.setText('')
        self.comboBox.clear()
        self.label_5.setText("Video Size : ")
        self.label_23.setText("Video Name :")
        self.pushButton_3.setEnabled(False)
        self.comboBox.setEnabled(False)

    def Downloadbtn2(self):
        self.pushButton_4.setEnabled(False)
        url = self.lineEdit_4.text()
        saveLocation = self.lineEdit_3.text()
        try:
            myvid = pafy.new(url)
            mystream=myvid.streams[self.comboBox.currentIndex()]
            self.Filesizelbl2(mystream.get_filesize())
            self.label_23.setText("Video Name : "+str(mystream.title))
            mystream.download(filepath=saveLocation,quiet=True ,callback=self.progressbar2)
        except Exception:
            QMessageBox.warning(self, "Download Error", "The Download Faild")
            self.MyReset2()
            return
        QMessageBox.information(self, "Download Completed", "The Download Finished")
        self.MyReset2()

 ##########################################################################
 #############################DownloadPlayList#############################
 ##########################################################################
    def valuechange(self):
        self.spinBox_2.setMinimum(self.spinBox.value())

    def Searchbtn2(self):
        PlayListurl = self.lineEdit_10.text()
        if self.comboBox_3.count() > 0:
            self.comboBox_3.clear()
        try:
            playlist = pafy.get_playlist(PlayListurl)
            numberOfVideoes=len(playlist['items'])
            self.spinBox_2.setMaximum(numberOfVideoes)
            self.spinBox.setMaximum(numberOfVideoes)
            self.spinBox_2.setValue(numberOfVideoes)
            video=playlist['items'][0]['pafy']
            mystreams = video.streams
            for s in mystreams :
                data = "{}  {}".format(s.extension, s.quality)
                self.comboBox_3.addItem(data)
        except Exception:
            QMessageBox.warning(self, "Wrong URL", "Enter Valid URL")
            return
        self.lcdNumber.display(numberOfVideoes)
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self.pushButton_12.setEnabled(True)
        self.comboBox_3.setEnabled(True)

    def Browsebtn3(self):
        saveLocation = QFileDialog.getExistingDirectory(self, caption="Save As",
                                                        directory="C:\\Users\\Mohamed Sayed\\OneDrive\\Desktop")

        saveLocation = str(saveLocation)
        self.lineEdit_9.setText(saveLocation)
        self.pushButton_11.setEnabled(True)
    def progressbar3(self,total, recvd, ratio, rate, eta):
        percent = recvd * 100 / total
        self.progressBar_5.setValue(percent)
        QApplication.processEvents()  # solve Not Responding problem

    def Filesizelbl3(self, size):
        self.label_18.setText("File Size : " + self.normalSize(size))

    def MyReset3(self):
        self.progressBar_5.setValue(0)
        self.lineEdit_10.setText('')
        self.lineEdit_9.setText('')
        self.comboBox_3.clear()
        self.label_18.setText("Video Size : ")
        self.label_22.setText("Current Video :")
        self.label_24.setText("Video Name :")
        self.lcdNumber.display(0)
        self.spinBox.setValue(1)
        self.spinBox_2.setValue(1)
        self.spinBox_2.setMinimum(1)
        self.pushButton_12.setEnabled(False)
        self.comboBox_3.setEnabled(False)
        self.spinBox.setEnabled(False)
        self.spinBox_2.setEnabled(False)


    def Downloadbtn3(self):
        self.pushButton_11.setEnabled(False)
        PlayListurl = self.lineEdit_10.text()
        saveLocation = self.lineEdit_9.text()

        try:
            playlist = pafy.get_playlist(PlayListurl)
            numberOfVideoes = len(playlist['items'])
            os.chdir(saveLocation)
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))
            start=self.spinBox.value()-1
            end=self.spinBox_2.value()
            for i in range(start,end) :
                video=playlist['items'][i]['pafy']
                mystreams=video.streams
                target=video.getbest()
                selectedQuality = self.comboBox_3.currentText().split("  ")[1]
                for mystream in mystreams :
                    if str(mystream.quality) == selectedQuality :
                        target=mystream
                        break

                self.Filesizelbl3(target.get_filesize())
                self.label_24.setText("Video Name : " + str(target.title))
                self.label_22.setText("Current Video : "+str(i-start+1)+"/"+str(end-start))
                target.download(quiet=True ,callback=self.progressbar3)
        except Exception:
            QMessageBox.warning(self, "Download Error", "The Download Faild")
            self.MyReset3()
            return
        QMessageBox.information(self, "Download Completed", "The Download Finished")
        self.MyReset3()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
