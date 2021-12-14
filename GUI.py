from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import os
import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np

from Arithmetics import Calculator
#from GUI_support import DataFrameModel
from Processors import InputDataProcessor


class Form(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)


        ### Старый интерфейс

        tab = QTabWidget()
        self.first = QWidget()
        self.second = QWidget()
        self.third = QWidget()

        tab.addTab(self.first, 'Main Menu')
        tab.addTab(self.second, 'Tables')
        tab.addTab(self.third, 'Graphics')

        Button_ChooseConfigs = QPushButton('Выбрать конфиги', self.first)
        Button_ChooseConfigs.setGeometry(10, 100, 120, 20)
        Button_ChooseConfigs.clicked.connect(self.choose_folder)



        scroll = QScrollArea(self.second)
        layout = QVBoxLayout(self.second)
        self.table = QTableWidget(self.second)

        scroll.setWidget(self.table)
        layout.addWidget(self.table)
        Button_table = QPushButton('Рассчитать',self.first)
        Button_table.setGeometry(150, 100, 120, 20)
        Button_table.clicked.connect(self.get_table)
        self.Label_ListConfigs = QLabel(self.first)
        self.Label_ListConfigs.setGeometry(20, 110, 500, 200)

        # Примеры создания графиков
        graph = QGraphicsView(self.third)
        scene = QGraphicsScene()

        graph.setScene(scene)

        self.plotWdgt = pg.PlotWidget()
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        plot_item = self.plotWdgt.plot(data)

        proxy_widget = scene.addWidget(self.plotWdgt)


        # imv = pg.ImageView(self.third)
        #
        # # Create random 3D data set with noisy signals
        # img = pg.gaussianFilter(np.random.normal(
        #     size=(200, 200)), (5, 5)) * 20 + 100
        #
        # # setting new axis to image
        # img = img[np.newaxis, :, :]
        #
        # # decay data
        # decay = np.exp(-np.linspace(0, 0.3, 100))[:, np.newaxis, np.newaxis]
        #
        # # random data
        # data = np.random.normal(size=(100, 200, 200))
        # data += img * decay
        # data += 2
        #
        # # adding time-varying signal
        # sig = np.zeros(data.shape[0])
        # sig[30:] += np.exp(-np.linspace(1, 10, 70))
        # sig[40:] += np.exp(-np.linspace(1, 10, 60))
        # sig[70:] += np.exp(-np.linspace(1, 10, 30))
        #
        # sig = sig[:, np.newaxis, np.newaxis] * 3
        # data[:, 50:60, 30:40] += sig
        #
        # # Displaying the data and assign each frame a time value from 1.0 to 3.0
        # imv.setImage(data, xvals=np.linspace(1., 3., data.shape[0]))
        #
        # # Set a custom color map
        # colors = [
        #     (0, 0, 0),
        #     (45, 5, 61),
        #     (84, 42, 55),
        #     (150, 87, 60),
        #     (208, 171, 141),
        #     (255, 255, 255)
        # ]

        # self.GraphWidget = pg.ImageView(self.third)
        # self.GraphWidget.setGeometry(140, 80, 400, 120)
        # self.GraphWidget.setObjectName("GraphWidget")



        ###DEBUG-----

        # data_path = r'C:\Users\bzakh\OneDrive\Desktop\Решения для ЛСТ.xlsx'
        # step1_int_config_path = r'C:\Users\bzakh\OneDrive\Documents\Python_projects\secanalysis\configs\step1_int_config.yaml'
        #
        # calculator = Calculator()
        #
        # idp_int = InputDataProcessor(data_path=data_path,
        #                              calculator=calculator,
        #                              sheet_name='Н1',
        #                              validate_data=True,
        #                              config_path=step1_int_config_path,
        #                              validation_params={
        #                                  'validate_data_shape': True,
        #                                  'validate_rows': True,
        #                                  'validate_expert_assessments_caption': True
        #                              })
        # step1_int_df = idp_int.return_dataframe()
        #
        # self.set_dataframe_widget(df=step1_int_df,
        #                           parent=self.second)

        ###----------

        self.setWindowTitle('Calc1.0')
        self.setCentralWidget(tab)
        self.resize(740, 480)


    def get_table(self):
        df = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н1',
                                header=[0, 1], index_col=0)
        old = df.columns[0][1]
        old1 = df.columns[11][1]
        df = df.rename(columns={old: '', old1: ''})
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        # for i in range(len(df.index)):
        #     for j in range(len(df.columns)):
        #         self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        for i in range(12):
            for j in range(2):
                self.table.setItem(j,i,QTableWidgetItem(str('{}\n'.format(df.columns[i][j]))))
        #self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


    def choose_folder(self):
        config_dir_name = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        configs = os.listdir(config_dir_name)
        configs_str = '\n• '.join(configs)
        self.Label_ListConfigs.setText(f'Вы выбрали папку: {config_dir_name}\n'
                                       f'Выбранные конфигурационные файлы:\n• {configs_str}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec())

