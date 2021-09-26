import sys
import os
import time
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import math


class Constant:
    def __init__(self):
        self.gif_dis = os.listdir(f"{os.getcwd()}/image/")  # 获取image下文件夹名
        self.log1 = open(f"{os.getcwd()}/log.txt", mode="r+")
        self.log_txt = self.log1.readlines()
        self.log1.close()
        self.removable_flag = 1
        self.new_log = {"gifNum": "img0",
                        "positionX": 1800,
                        "positionY": 800,
                        "removable_flag": 1,
                        "size_times": 100,
                        "pos_x": 400,
                        "pos_y": 400,
                        "check": "paperblue"}
        self.logRead()
        self.log = open(f"{os.getcwd()}/log.txt", mode="w+")

    def removableSw(self):
        """
        覆写new_log中removable_flag选项

        :return: None
        """
        self.removable_flag = bool(1 - self.removable_flag)
        self.new_log["removable_flag"] = int(self.removable_flag)
        # print(self.removable_flag)

    def logRead(self):
        """
        读取log中的数据并写入new_log

        :return: None
        """

        # del self.log_txt[0]
        try:
            if self.log_txt[-1] == "******":
                self.new_log["gifNum"] = self.log_txt[1].split(" ")[1].rstrip("\n")
                # print(self.new_log["gifNum"])
                for i in self.log_txt[2:8]:
                    j = i.split(" ")
                    self.new_log[j[0]] = int(j[1].rstrip("\n"))
                    # print(self.new_log[j[0]])
                self.removable_flag = self.new_log["removable_flag"]
                pass
            else:
                print("LogInsideWrong!")
            pass
        except:
            print("LogNone!")
            from LogRest import a
            a()

    def end(self):
        """
        往log中写入本次数据

        :return: None
        """
        self.log.write("{time0}\n".format(time0=time.strftime("%Y-%m-%d--%H:%M:%S")))
        self.new_log["positionX"], self.new_log["positionY"] = Pendant.pos_x, Pendant.pos_y
        self.new_log["pos_x"], self.new_log["pos_y"] = int(Pendant.ui_x), int(Pendant.ui_y)
        self.new_log["gifNum"] = Pendant.dis_file
        for i, k in self.new_log.items():
            # print(i, k)
            self.log.write(f"{i} {k}\n")
            pass
        self.log.write("******")
        self.log.close()
        pass


class PQDPendant(QWidget):

    def __init__(self):
        super().__init__()
        self.gif = None
        self.gif_size = None
        self.pos_x = constant.new_log["positionX"]  # 设置窗口位置、大小
        self.pos_y = constant.new_log["positionY"]
        self.ui_x = constant.new_log["pos_x"]
        self.ui_y = constant.new_log["pos_y"]

        self.path = os.getcwd()  # 获取当前文件位置
        self.dis_file = constant.new_log["gifNum"]
        self.pos_first = self.pos()

        self.lab = QLabel(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # 将窗口设置为透明且无顶框
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 窗口设置自适应

        self.windowInit()

    def windowInit(self):
        """
        初始化窗口并填充Gif

        :return: None
        """
        self.setGeometry(self.pos_x, self.pos_y, self.ui_x, self.ui_y)
        self.setWindowTitle('My Pet')
        self.gif = QMovie('{path1}/image/{file}/0.Gif'.format(file=self.dis_file, path1=self.path))
        self.gif_size = Image.open("{a}/image/{b}/0.gif".format(a=os.getcwd(), b=self.dis_file)).size
        self.gifResize()
        self.gif.setScaledSize(QSize(self.gif_size[0], self.gif_size[1]))
        self.lab.setGeometry(0, 0, self.ui_x, self.ui_y)
        self.lab.setMovie(self.gif)  # 加载Gif
        self.gif.start()  # 启动Gif
        self.show()  # SHOOOOOOOOOOOOW TIME!

    def mousePressEvent(self, MouseEvent):
        if MouseEvent.button() == Qt.LeftButton:
            self.pos_first = MouseEvent.globalPos() - self.pos()
            MouseEvent.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        elif MouseEvent.button() == Qt.RightButton:
            newWin.show()
            pass

            # self.quit() # 调试用右键关闭程序

    def mouseMoveEvent(self, MouseEvent):
        if Qt.LeftButton and constant.removable_flag:
            self.move(MouseEvent.globalPos() - self.pos_first)
            self.pos_x, self.pos_y = self.pos().x(), self.pos().y()
            MouseEvent.accept()
            pass

    def gifChange(self, i):
        """
        更改gif函数

        :param i: gif所在的文件夹名
        :return: None
        """

        self.dis_file = i
        self.windowInit()

    def posReset(self):
        """
        重置gif位置，重置位置为左上角

        :return: None
        """
        self.pos_x, self.pos_y = 0, 0
        self.windowInit()

    def gifResize(self):
        """
        使gif自适应窗口

        :return: None
        """

        x = 400 * constant.new_log["size_times"] / 100
        y = 400 * constant.new_log["size_times"] / 100

        self.ui_x = x
        self.ui_y = y

        times = min(x, y) / max(self.gif_size)
        # print(times)
        temp = (self.gif_size[0] * times, self.gif_size[1] * times)
        self.gif_size = temp
        pass

    def quit(self):
        """
        退出程序

        :return: None
        """
        print("safely quit!")
        constant.end()
        self.close()
        sys.exit()


class NewWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.sizeTxt = QLabel()
        self.sizeTimes = constant.new_log["size_times"]
        self.gif_button = QComboBox()
        # self.resize(800, 200)
        self.initUI()
        self.initGifs()

    def initGifs(self):
        self.gif_button.addItems(constant.gif_dis)
        self.gif_button.currentIndexChanged[str].connect(Pendant.gifChange)  # 绑定更换条目与更改gif函数

    def initUI(self):
        def txtValueChange():
            """
            不要问为什么调整不到100%和500%，问就是二进制的锅。
            :return:
            """
            self.sizeTxt.setText(str(int(20 * math.exp(0.0321887582 * float(sizeLine.value())))) + "%")
            self.sizeTimes = int(self.sizeTxt.text().rstrip("%"))
            constant.new_log["size_times"] = self.sizeTimes
            Pendant.windowInit()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        close_button = QPushButton("关闭软件", self)
        close_button.clicked.connect(Pendant.quit)
        cancel_button = QPushButton("关闭设置", self)
        cancel_button.clicked.connect(self.hide)
        removable_button = QPushButton("锁定", self)
        removable_button.clicked.connect(constant.removableSw)
        reset_button = QPushButton("位置重置", self)
        reset_button.clicked.connect(Pendant.posReset)
        sizeLine = QSlider(Qt.Horizontal)
        sizeLine.setMinimum(0)
        sizeLine.setMaximum(100)
        sizeLine.setSingleStep(1)
        sizeLine.setValue(int(math.log(self.sizeTimes / 20) / 0.0321887582))
        sizeLine.valueChanged.connect(txtValueChange)
        self.sizeTxt.setText("{a}%".format(a=self.sizeTimes))

        box = QHBoxLayout()
        box.addWidget(cancel_button)
        box.addWidget(close_button)
        box.addWidget(removable_button)
        box.addWidget(self.gif_button)
        box.addWidget(reset_button)

        sizeBox = QHBoxLayout()
        sizeBox.addWidget(sizeLine)
        sizeBox.addWidget(self.sizeTxt)

        mainBox = QVBoxLayout()
        mainBox.addLayout(box)
        mainBox.addLayout(sizeBox)

        self.setLayout(mainBox)


constant = Constant()

app = QApplication(sys.argv)
Pendant = PQDPendant()
newWin = NewWindow()
sys.exit(app.exec_())
