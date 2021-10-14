import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
################################################
items_list=["C","C++","Java","Python","JavaScript","C#","Swift","go","Ruby","Lua","PHP"]
datas_list=[1972,1983,1995,1991,1992,2000,2014,2009,1995,1993,1995]

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.combobox1 = QComboBox(self, minimumWidth=200)
        self.combobox2 = QComboBox(self, minimumWidth=200)
        self.combobox3 = QComboBox(self, minimumWidth=200)
        self.combobox4 = QComboBox(self, minimumWidth=200)

        layout.addWidget(QLabel("增加单项，不带数据", self))
        layout.addWidget(self.combobox1)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(QLabel("增加单项，附带数据", self))
        layout.addWidget(self.combobox2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(QLabel("增加多项，不带数据", self))
        layout.addWidget(self.combobox3)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addWidget(QLabel("设置模型，不带数据", self))
        layout.addWidget(self.combobox4)

        #初始化combobox
        self.init_combobox1()
        self.init_combobox2()
        self.init_combobox3()
        self.init_combobox4()

        #增加选中事件
        self.combobox1.activated.connect(self.on_combobox1_Activate)
        self.combobox2.activated.connect(self.on_combobox2_Activate)
        self.combobox3.activated.connect(self.on_combobox3_Activate)
        self.combobox4.activated.connect(self.on_combobox4_Activate)

    ####### addItem()  增加单项元素，不带数据  #########
    def init_combobox1(self):
        for i in range(len(items_list)):
            self.combobox1.addItem(items_list[i])
        self.combobox1.setCurrentIndex(-1)

    def on_combobox1_Activate(self, index):
        print('1 = ' + str(self.combobox1.count()))#返回列表框下拉项数目
        print('2 = ' +  str(self.combobox1.currentIndex()))#返回选中项索引
        print('3 = ' +  str(self.combobox1.currentText()))#返回选中项的文本内容
        print('4 = ' +  str(self.combobox1.currentData()))#返回当前数据
        print('5 = ' +  str(self.combobox1.itemData(self.combobox1.currentIndex())))
        print('6 = ' +  str(self.combobox1.itemText(self.combobox1.currentIndex())))
        print('7 = ' +  str(self.combobox1.itemText(index)))

    ####### addItem()  增加单项元素，附带数据  #########
    def init_combobox2(self):
        for i in range(len(items_list)):
            self.combobox2.addItem(items_list[i],datas_list[i])
        self.combobox2.setCurrentIndex(-1)

    def on_combobox2_Activate(self, index):
        print(self.combobox2.count())
        print(self.combobox2.currentIndex())
        print(self.combobox2.currentText())
        print(self.combobox2.currentData())
        print(self.combobox2.itemData(self.combobox2.currentIndex()))
        print(self.combobox2.itemText(self.combobox2.currentIndex()))
        print(self.combobox2.itemText(index))


    ####### addItems()  增加多项元素，不带数据  #########
    def init_combobox3(self):
        self.combobox3.addItems(items_list)
        self.combobox3.setCurrentIndex(-1)

    def on_combobox3_Activate(self, index):
        print(self.combobox3.count())
        print(self.combobox3.currentIndex())
        print(self.combobox3.currentText())
        print(self.combobox3.currentData())
        print(self.combobox3.itemData(self.combobox3.currentIndex()))
        print(self.combobox3.itemText(self.combobox3.currentIndex()))
        print(self.combobox3.itemText(index))



    ####### setModel()  设置数据模型，不带数据  #########
    def init_combobox4(self):
        self.tablemodel = QStringListModel(items_list)
        self.combobox4.setModel(self.tablemodel)
        self.combobox4.setCurrentIndex(-1)

    def on_combobox4_Activate(self, index):
        print(self.combobox4.count())
        print(self.combobox4.currentIndex())
        print(self.combobox4.currentText())
        print(self.combobox4.currentData())
        print(self.combobox4.itemData(self.combobox4.currentIndex()))
        print(self.combobox4.itemText(self.combobox4.currentIndex()))
        print(self.combobox4.itemText(index))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
