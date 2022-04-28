import sys
import os
import time
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import math


# PQDPendant.py
class Constant:
    def __init__(self):
        self.dir = os.getcwd()
        self.gif_dis = os.listdir(f"{self.dir}/image/")  # 获取image下文件夹名
        self.pds_status = {1: {"pdName": 'save1',
                               "pdLog": "save1.txt",
                               "gifNum": "img0",
                               "positionX": 0,
                               "positionY": 0,
                               "removable_flag": 1,
                               "size_times": 100,
                               "pos_x": 400,
                               "pos_y": 400,
                               "check": "paperblue"}}
        self.pendants = {}

        self.pdsStatusRead()
        self.logRead()

        # print('cst yes')

    def removableSw(self, num):
        """
        覆写pds_status[num]中removable_flag选项

        :return: None
        """
        self.pds_status[num]["removable_flag"] = 0 if self.pds_status[num]["removable_flag"] else 1

        # print(self.removable_flag)

    def logRead(self):
        """
        读取log中的数据并写入pds_status[num]

        :return: None
        """
        for i in self.pds_status.keys():
            log1 = open("{dir}/{name}".format(dir=self.dir, name=self.pds_status[i]["pdLog"]), mode="r+")
            log_txt = log1.readlines()
            log1.close()
            try:
                if log_txt[-1] == "******":
                    self.pds_status[i]["gifNum"] = log_txt[1].split(" ")[1].rstrip("\n")
                    # print(self.pds_status[i]["gifNum"])
                    for s in log_txt[2:8]:
                        j = s.split(" ")
                        self.pds_status[i][j[0]] = int(j[1].rstrip("\n"))
                        # print(self.pds_status[i][j[0]])
                    pass
                else:
                    print("LogInsideWrong!")
                pass
            except SystemExit:
                print("LogNone!")
                from LogRest import a
                a()

    def pdsStatusRead(self):
        temp = open(f"{self.dir}//pdsStatus.txt", mode="r+")
        pdsstat = temp.readlines()
        temp.close()
        try:
            cout = 1
            for i in range(1, len(pdsstat), 2):
                self.pds_status[cout] = {}
                self.pds_status[cout]['pdName'] = pdsstat[i].split(" ")[1].rstrip("\n")
                self.pds_status[cout]['pdLog'] = pdsstat[i + 1].split(" ")[1].rstrip("\n")
                cout += 1
            pass
        except SystemExit:
            print('pdsStatus read wrong')
            pass
        pass

    def end(self):
        """
        往log中写入本次数据

        :return: None
        """

        file = open(f"{self.dir}/pdsStatus.txt", mode="w+")
        file.write("{time0}\n".format(time0=time.strftime("%Y-%m-%d--%H:%M:%S")))
        for i in self.pds_status.keys():
            file.write(
                "{name} {constants}\n".format(name="pdName", constants=f"save{i}"))
            file.write(
                "{name} {constants}\n".format(name="pdLog", constants=f"save{i}.txt"))
        file.close()

        for i in self.pds_status.keys():
            file = open("{dir}/{name}".format(dir=self.dir, name=f"save{i}.txt"), mode="w+")
            file.write("{time0}\n".format(time0=time.strftime("%Y-%m-%d--%H:%M:%S")))
            cout = 0
            for j, k in self.pds_status[i].items():
                if cout < 2:
                    cout += 1
                    continue
                # print(i, k)
                file.write(f"{j} {k}\n")
                pass
            file.write("******")
            file.close()
        print("safely quit!")
        pass

    def pdsInit(self):
        for i in self.pds_status.keys():
            self.pendants[i] = PQDPendant(i)

    def pdDel(self, i):
        # print(self.pds_status, self.pendants)
        # os.remove('{dir}/{name}'.format(dir=self.dir, name=self.pds_status[i]["pdLog"]))
        self.pendants[i].close()
        del self.pendants[i]
        del self.pds_status[i]

        # print(self.pds_status, self.pendants)
        pass

    def pdAdd(self):
        # print('add', self.pds_status)
        temp = self.pds_status.keys()
        i = 1
        while i in temp:
            i += 1
        # print(i)
        self.pds_status[i] = {"pdName": 'save{num}'.format(num=i),
                              "pdLog": "save{num}.txt".format(num=i),
                              "gifNum": "img0",
                              "positionX": 0,
                              "positionY": 0,
                              "removable_flag": 1,
                              "size_times": 100,
                              "pos_x": 400,
                              "pos_y": 400,
                              "check": "paperblue"}
        self.pendants[i] = PQDPendant(i)
        # print(self.pds_status)
        pass


class PQDPendant(QWidget):

    def __init__(self, num):
        super().__init__()
        self.num = num
        self.gif = None
        self.gif_size = None
        self.pos_x = constant.pds_status[self.num]["positionX"]  # 设置窗口位置、大小
        self.pos_y = constant.pds_status[self.num]["positionY"]
        self.ui_x = constant.pds_status[self.num]["pos_x"]
        self.ui_y = constant.pds_status[self.num]["pos_y"]

        self.path = os.getcwd()  # 获取当前文件位置
        self.dis_file = constant.pds_status[self.num]["gifNum"]
        self.pos_first = self.pos()

        self.lab = QLabel(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # 将窗口设置为透明且无顶框
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 窗口设置自适应

        self.windowInit()
        # print('pd', self.num, "yes")

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
        newWin.acceptNum(self.num)
        if MouseEvent.button() == Qt.LeftButton:
            self.pos_first = MouseEvent.globalPos() - self.pos()
            MouseEvent.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        elif MouseEvent.button() == Qt.RightButton:
            newWin.show()
            # print(constant.pendants, "\n\n", constant.pds_status)
            pass

    def mouseMoveEvent(self, MouseEvent):
        newWin.acceptNum(self.num)
        if Qt.LeftButton and constant.pds_status[self.num]["removable_flag"]:
            self.move(MouseEvent.globalPos() - self.pos_first)
            self.pos_x, self.pos_y = self.pos().x(), self.pos().y()
            constant.pds_status[self.num]["positionX"] = self.pos_x
            constant.pds_status[self.num]["positionY"] = self.pos_y
            MouseEvent.accept()
            pass

    def gifChange(self, i):
        """
        更改gif函数

        :param i: gif所在的文件夹名
        :return: None
        """

        self.dis_file = i
        constant.pds_status[self.num]["gifNum"] = i
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
        使gif自适应窗口，但长宽比和原图可能会有些许误差，别问，问就是二进制得锅

        :return: None
        """

        x = 400 * constant.pds_status[self.num]["size_times"] / 100
        y = 400 * constant.pds_status[self.num]["size_times"] / 100

        self.ui_x = x
        self.ui_y = y

        constant.pds_status[self.num]["pos_x"] = int(x)
        constant.pds_status[self.num]["pos_y"] = int(y)

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
        constant.end()
        self.close()
        sys.exit()


class NewWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.num = 1
        self.pd = constant.pendants[1]
        self.sizeTxt = QLabel()
        self.sizeTimes = constant.pds_status[self.num]["size_times"]
        self.gif_button = QComboBox()
        # self.resize(800, 200)
        self.initUI()
        self.initGifs()

    def initGifs(self):
        self.gif_button.addItems(constant.gif_dis)
        self.gif_button.currentIndexChanged[str].connect(self.pdGifChange)  # 绑定更换条目与更改gif函数

    def initUI(self):
        def txtValueChange():
            """
            不要问为什么调整不到100%和500%，问就是二进制的锅。
            :return:
            """
            self.sizeTxt.setText(str(int(20 * math.exp(0.0321887582 * float(sizeLine.value())))) + "%")
            self.sizeTimes = int(self.sizeTxt.text().rstrip("%"))
            constant.pds_status[self.num]["size_times"] = self.sizeTimes
            self.pdReSize()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        close_button = QPushButton("关闭软件", self)
        close_button.clicked.connect(self.pdquit)
        cancel_button = QPushButton("关闭设置", self)
        cancel_button.clicked.connect(self.hide)
        removable_button = QPushButton("锁定", self)
        removable_button.clicked.connect(self.pdLock)
        reset_button = QPushButton("位置重置", self)
        reset_button.clicked.connect(self.pdPosReset)
        add_button = QPushButton("增加摆件", self)
        add_button.clicked.connect(self.pdAdd)
        del_button = QPushButton("删除摆件", self)
        del_button.clicked.connect(self.pdDel)
        sizeLine = QSlider(Qt.Horizontal)
        sizeLine.setMinimum(0)
        sizeLine.setMaximum(100)
        sizeLine.setSingleStep(1)
        sizeLine.setValue(int(math.log(self.sizeTimes / 20) / 0.0321887582))
        sizeLine.valueChanged.connect(txtValueChange)
        self.sizeTxt.setText("{a}%".format(a=self.sizeTimes))

        boxPds = QHBoxLayout()  # 二级
        boxPds.addWidget(cancel_button)
        boxPds.addWidget(close_button)
        boxPds.addWidget(add_button)
        boxPds.addWidget(del_button)

        boxPd = QHBoxLayout()  # 二级
        boxPd.addWidget(removable_button)
        boxPd.addWidget(self.gif_button)
        boxPd.addWidget(reset_button)

        sizeBox = QHBoxLayout()  # 二级
        sizeBox.addWidget(sizeLine)
        sizeBox.addWidget(self.sizeTxt)

        mainBox = QVBoxLayout()  # 一级
        mainBox.addLayout(boxPds)
        mainBox.addLayout(boxPd)
        mainBox.addLayout(sizeBox)

        self.setLayout(mainBox)

    def acceptNum(self, num):
        """
        接受pd对象序号

        :param num:
        :return:
        """
        self.num = num
        self.pd = constant.pendants[self.num]

    def pdquit(self):
        self.pd.quit()
        pass

    def pdPosReset(self):
        self.pd.posReset()
        pass

    def pdGifChange(self, i):
        self.pd.gifChange(i)
        pass

    def pdReSize(self):
        self.pd.windowInit()
        pass

    def pdLock(self):
        constant.removableSw(self.num)
        pass

    def pdAdd(self):
        constant.pdAdd()
        pass

    def pdDel(self):
        if len(constant.pendants.keys()) != 1:
            constant.pdDel(self.num)
            self.num = [i for i in constant.pendants.keys()][0]
        pass


app = QApplication(sys.argv)

constant = Constant()
constant.pdsInit()
newWin = NewWindow()

sys.exit(app.exec_())
