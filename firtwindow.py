# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets



import quantumrandom


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from time import sleep
from scipy import stats
import struct


def get_rgb_vector(hexNumber):
    vector = tuple(int(hexNumber[i:i+2], 16) for i in range(0, 6, 2))
    print (hexNumber + " = RGB" + str(vector))
    return vector

def euclidian_distance(rgb1,rgb2):
    changeR = rgb2[0] - rgb1[0]
    changeG = rgb2[1] - rgb1[1]
    changeB = rgb2[2] - rgb1[2]
    return (((2*(changeR**2))+(4*(changeG**2))+(3*(changeB**2)))**.5)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(948, 688)


        self.robotAverage = 423.26
        self.robotColorsGenerated = 3485726894
        self.robotConstant = 4.520263823369427

        self.rgb = []
        self.averages = []
        self.colorDistances = []
        self.queryMade = False

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)



        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btn_click)



        self.graphLayoutWidget = QtWidgets.QWidget(Dialog)
        self.graphLayoutWidget.setGeometry(QtCore.QRect(400,10, 550, 210))
        self.graphLayoutWidget.setObjectName("graphLayoutWidget")
        self.graphLayout = QtWidgets.QGridLayout(self.graphLayoutWidget)
        self.graphLayout.setContentsMargins(0, 0, 0, 0)
        self.graphLayout.setSpacing(0)
        self.graphLayout.setObjectName("graphLayout")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 300, 800, 121))
        self.label.setFont(font)
        self.label.setObjectName("label")



        self.figure = plt.figure(figsize=(15,5))
        self.canvas = FigureCanvas(self.figure)
        self.graphLayout.addWidget(self.canvas, 2,2,1,2)
        self.ax = self.figure.add_axes([0.25,0.2,0.75,0.65])
        self.ax.set_xlabel("Num Colors Generated")
        self.ax.set_ylabel("Distance from Blue")
        self.ax.set_title('You vs. control')

        self.figure2 = plt.figure(figsize=(15,5))
        self.canvas2 = FigureCanvas(self.figure2)
        self.graphLayout.addWidget(self.canvas2,2,5,1,2)
        self.ax2 = self.figure2.add_axes([0.2,0.2,0.75,0.65])
        self.ax2.set_title('Colors generated')
        self.ax2.get_xaxis().set_visible(False)








        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 140, 400, 21))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 161, 400, 21))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 182, 400, 45))
        self.label_4.setObjectName("label_4")


        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 240, 791, 380))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")


        self.grid_row = 0
        self.grid_column = 0
        self.NumColorsGenerated = 0
        self.runningAverage = 0

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

        self._translate = QtCore.QCoreApplication.translate

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edges of Psience"))
        self.label.setText(_translate("Dialog", "Can you make the squares more blue?"))
        self.pushButton.setText(_translate("Dialog", "Begin Testing"))
        self.label_2.setText(_translate("Dialog", "No color selected"))

    def btn_click(self):

        self.favoriteColorRGB = (0,0,255)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self._update())
        self.timer.start(50)

        self.label.setText("")
        self.label_2.setText("Loading your random numbers (Courtesy of ANU)")
        self.pushButton.setEnabled(False)
        if self.NumColorsGenerated == 0:
            self.pushButton.setText("(confirmed.)")
        else:
            self.pushButton.setText("continuing...")
        self.sliceIndex = 2
        self.buttonPushed = True



    def _update(self):
        if not self.queryMade:
            self.randomhexnum = str(quantumrandom.get_data(data_type='hex16', array_length=1, block_size=198))
            self.queryMade = True
        sliceNum = self.randomhexnum[self.sliceIndex:self.sliceIndex+6]
        if "'" not in sliceNum:
            self.new_label = QtWidgets.QLabel(self.gridLayoutWidget)
            self.gridLayout.addWidget(self.new_label, self.grid_row,self.grid_column, 1, 1)
            if self.grid_column > 21:
                self.grid_column = 0
                self.grid_row += 1
            else:
                self.grid_column +=1

            if len(sliceNum) == 6:
                self.new_label.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color:#" +sliceNum+";\">█</span></p></body></html>"))
                rgb_vector = get_rgb_vector(sliceNum)
                distance = euclidian_distance(rgb_vector,self.favoriteColorRGB)
                self.average_distance(distance)
                print(str(self.NumColorsGenerated) + " colors generated.")
                self.label_2.setText(str(round(self.runningAverage,2)) + " Euclidian Average")
                self.ax.cla()
                self.ax.axhspan(422,426,0,1,color=('b'))
                self.ax.set_xlabel('Num Colors Generated')
                self.ax.set_ylabel("Distance from Blue")
                self.ax2.set_title('Colors generated')
                #self.ax.axhspan(380,423,0,1,color=('xkcd:greeny yellow'))
                #self.ax.axhspan(425,460,0,1,color=('xkcd:black'))
                self.ax.plot(self.averages[-(int((len(self.averages))-3)):],'r.-')
                colorInt = int(sliceNum,16)
                self.colorDistances.append(distance)
                self.ax2.scatter(colorInt,distance,c=("#"+sliceNum))
                self.canvas.draw()
                self.canvas2.draw()

                print("euclidian distance of " + str(round(distance,2)))
                print("running average = " + str(round(self.runningAverage,2)))
                print("=============================")
                self.sliceIndex += 1
        else:
            self.timer.stop()
            self.label_2.setText("calculating statistics from this run....")
            self.calculate_variance()
            self.calculate_p_value()
            p_value = str(round(self.pValue,3))
            self.append_human_results()
            global_p_value = str(round(self.global_p_value,5))
            if(self.pValue >.05):
                self.label_2.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color: red;\"> p value of " + p_value + ". (Null hypothesis supported.)</span></p></body></html>"))
            else:
                self.label_2.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color: green;\"> p value of " + p_value + ". (Psi hypothesis supported.)</span></p></body></html>"))
            if(self.global_p_value >.05):
                self.label_3.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color: red;\"> global p value of " + global_p_value + ". (null evident.)</span></p></body></html>"))
            else:
                self.label_3.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color: green;\"> global p value of " + global_p_value + ". (psi evident!!)</span></p></body></html>"))
            global_average = str(round(self.global_average,2))
            if(self.global_average > 424):
                self.label_4.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color: red;\"> cumulative average distance of " + global_average + ". <br />(Farther from blue than control.) </span></p></body></html>"))
            else:
                self.label_4.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" color: green;\"> cumulative average distance of " + global_average + ". <br />(Closer to blue than control.) </span></p></body></html>"))

            self.queryMade = False
            self.pushButton.setText("continue?")
            self.pushButton.setEnabled(True)

    def average_distance(self,distance):
        newAverage = ((self.runningAverage*self.NumColorsGenerated) + distance)/(self.NumColorsGenerated + 1)
        self.runningAverage = newAverage
        self.averages.append(newAverage)
        self.NumColorsGenerated += 1

    def calculate_variance(self):
        sum = 0
        for colorDistance in self.colorDistances:
            dataPoint = ((colorDistance - self.runningAverage)**2/(self.NumColorsGenerated-1))
            sum += dataPoint
        standardDeviation = (sum**.5)
        constant = ((standardDeviation)**2/self.NumColorsGenerated)
        variance = (constant + self.robotConstant)**.5
        self.variance = variance

    def calculate_p_value(self):
        tScore = ((self.runningAverage - self.robotAverage)/self.variance)
        degreesOfFreedom = self.robotColorsGenerated + self.NumColorsGenerated -2
        p = 1 - stats.t.cdf(tScore,df=degreesOfFreedom)
        self.pValue = p

    def calculate_gloabal_variance(self,colorDistances,average,numColorsGenerated):
        sum = 0
        for colorDistance in colorDistances:
            dataPoint = ((colorDistance - average)**2/(numColorsGenerated-1))
            sum += dataPoint
        standardDeviation = (sum**.5)
        constant = ((standardDeviation)**2/numColorsGenerated)
        variance = (constant + self.robotConstant)**.5
        return variance

    def calculate_global_p_value(self,colorDistances,average,numColorsGenerated):
        variance = self.calculate_gloabal_variance(colorDistances,average,numColorsGenerated)
        tscore = ((average - self.robotAverage)/variance)
        degreesOfFreedom = self.robotColorsGenerated + numColorsGenerated -2
        p = 1 - stats.t.cdf(tscore,df=degreesOfFreedom)
        self.global_p_value = p


    def append_human_results(self):
        reader = open("results.csv","r")
        contents = reader.read()
        contents = contents.split()
        runningColorsGenerated = int(contents[0])
        runningColorAverage = float(contents[1])
        distances = []
        for distance in (contents[2:]):
            distances.append(float(distance))
        distances+=self.colorDistances
        runningColorAverage = ((runningColorsGenerated*runningColorAverage) + sum(self.colorDistances))/(runningColorsGenerated+self.NumColorsGenerated)
        self.global_average = runningColorAverage
        runningColorsGenerated += self.NumColorsGenerated
        self.calculate_global_p_value(distances,runningColorAverage,runningColorsGenerated)
        reader.close()
        wr = open("results.csv",'w')
        wr.write(str(runningColorsGenerated) + '\n')
        wr.write(str(runningColorAverage) + '\n')
        for distance in distances:
            wr.write(str(distance) + '\n')
        wr.close()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())