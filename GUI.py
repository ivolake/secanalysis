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
# from GUI_support import DataFrameModel
from Processors import InputDataProcessor
from functions import get_yaml


class Form(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Старый интерфейс

        tab = QTabWidget()

        self.setWindowTitle('SecAnalysis')
        self.setCentralWidget(tab)
        self.resize(740, 480)

        self.first = QWidget()
        self.second = QWidget()
        self.third = QWidget()

        tab.addTab(self.first, 'Главная')
        tab.addTab(self.second, 'Таблицы')
        tab.addTab(self.third, 'Графики')

        self.Label_ListConfigs = None
        self.set_first_tab()

        self.vertLayout = None
        self.scroller = None
        self.scrollAreaWidgetContents_2 = None
        self.vertLayout_2 = None
        self.table = None
        self.table2 = None
        self.table3 = None
        self.table4 = None
        self.table5 = None
        self.table6 = None
        self.table7 = None
        self.table8 = None
        self.set_second_tab()

        self.plotWdgt = None
        self.set_third_tab()

        self.filepaths = None

    def set_first_tab(self):
        Button_ChooseConfigs = QPushButton('Выбрать конфиги', self.first)
        Button_ChooseConfigs.setGeometry(10, 100, 120, 20)
        Button_ChooseConfigs.clicked.connect(self.choose_folder)

        Button_table = QPushButton('Рассчитать', self.first)
        Button_table.setGeometry(150, 100, 120, 20)
        Button_table.clicked.connect(self.calculate_tables)
        self.Label_ListConfigs = QLabel(self.first)
        self.Label_ListConfigs.setGeometry(20, 110, 500, 200)

    def set_second_tab(self):
        # Создается вертикальный слой на вкладке
        self.vertLayout = QVBoxLayout(self.second)
        # Создание скроллера на вкладке
        self.scroller = QScrollArea(self.second)
        self.scroller.setWidgetResizable(True)
        # Создаётся виджет содержимого скролла
        self.scrollAreaWidgetContents_2 = QWidget()
        # Создается второй вертикальный слой на виджете содержимого
        self.vertLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        # Создается виджет таблицы на виджете содержимого
        self.table = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table.setMinimumSize(1200, 650)
        self.table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table2 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table2.setMinimumSize(1200, 650)
        self.table3 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table3.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table3.setMinimumSize(1200, 650)
        self.table4 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table4.setMinimumSize(1200, 650)
        self.table4.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table5 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table5.setMinimumSize(1200, 650)
        self.table5.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table6 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table6.setMinimumSize(1200, 650)
        self.table6.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table7 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table7.setMinimumSize(1200, 650)
        self.table7.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table8 = QTableWidget(self.scrollAreaWidgetContents_2)
        self.table8.setMinimumSize(1200, 650)
        self.table8.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # Добавляю таблицу на слой 2
        self.vertLayout_2.addWidget(self.table)
        self.vertLayout_2.addWidget(self.table2)
        self.vertLayout_2.addWidget(self.table3)
        self.vertLayout_2.addWidget(self.table4)
        self.vertLayout_2.addWidget(self.table5)
        self.vertLayout_2.addWidget(self.table6)
        self.vertLayout_2.addWidget(self.table7)
        self.vertLayout_2.addWidget(self.table8)
        # Скрол-арии устанавливается виджет содержимого
        self.scroller.setWidget(self.scrollAreaWidgetContents_2)
        # На вертикальный слой добавляется скрол
        self.vertLayout.addWidget(self.scroller)

    def set_third_tab(self):
        # Примеры создания графиков
        graph = QGraphicsView(self.third)
        scene = QGraphicsScene()

        graph.setScene(scene)

        self.plotWdgt = pg.PlotWidget()
        dataX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        dataY = list(reversed([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        plot_item = self.plotWdgt.plot(x=dataX, y=dataY)

        proxy_widget = scene.addWidget(self.plotWdgt)

    def calculate_tables(self):
        pass
        # # data_path = r'C:\Users\bzakh\OneDrive\Desktop\Решения для ЛСТ.xlsx'
        # if self.filepaths is not None:
        #     if any(['yaml' in config for config in self.filepaths]):
        #         configs = {}
        #         for filepath in self.filepaths:
        #             config = get_yaml(filepath)
        #             configs.update({config['name']: config})
        #             # step1_int_config_path = r'C:\Users\bzakh\OneDrive\Documents\Python_projects\secanalysis\configs\step1_int_config.yaml'
        #
        #         calculator = Calculator()
        #
        #         idp_int = InputDataProcessor(data_path=configs[''],
        #                                      calculator=calculator,
        #                                      sheet_name='Н1',
        #                                      validate_data=True,
        #                                      config_path=step1_int_config_path,
        #                                      validation_params={
        #                                          'validate_data_shape': True,
        #                                          'validate_rows': True,
        #                                          'validate_expert_assessments_caption': True
        #                                      })
        #         step1_int_df = idp_int.return_dataframe()
        #     else:
        #         print('Ошибка. Все конфигурационные файлы должны быть формата .yaml')
        # else:
        #     print('Ошибка. Необходимо выбрать конфигурационные файлы.')


    def set_data_to_table(self, df, table):
        # df = pd.read_excel(r'C:\Users\bzakh\OneDrive\Desktop\Решения для ЛСТ.xlsx', sheet_name='Н1',
        #                    header=[0, 1], index_col=0)
        # df = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н1',
        #                         header=[0, 1], index_col=0)
        old = df.columns[0][1]
        old1 = df.columns[10][1]
        df = df.rename(columns={old: '', old1: ''})
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        # for i in range(len(df.index)):
        #     for j in range(len(df.columns)):
        #         self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        for i in range(11):
            for j in range(2):
                self.table.setItem(j, i, QTableWidgetItem(str('{}\n'.format(df.columns[i][j]))))
        # self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def choose_folder(self):
        # noinspection PyTypeChecker
        files_dir_name = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.filepaths = os.listdir(files_dir_name)
        files_str = '\n• '.join(self.filepaths)
        self.Label_ListConfigs.setText(f'Вы выбрали папку: {files_dir_name}\n'
                                       f'Выбранные конфигурационные файлы:\n• {files_str}')

