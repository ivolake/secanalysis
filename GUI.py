from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import os
import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
from textwrap3 import wrap

from Arithmetics import Calculator
# from GUI_support import DataFrameModel
from Processors import InputDataProcessor, CalculatingDataProcessor
from functions import get_yaml, flatten


def create_plot_widget(parent,
                       dataX,
                       dataY,
                       title=''):

    graph = QGraphicsView(parent)
    graph.setVisible(False)
    scene = QGraphicsScene()
    graph.setScene(scene)
    plot_widget = pg.PlotWidget()
    plot_widget.setBackground('white')
    plot_widget.showGrid(True, True)
    plot_widget.setTitle(title)

    plot_item = plot_widget.plot(x=dataX,
                                 y=dataY,
                                 pen=pg.mkPen('black', width=3))

    return plot_widget, plot_item


def set_data_to_table(df, table):
    # df = pd.read_excel(r'C:\Users\bzakh\OneDrive\Desktop\Решения для ЛСТ.xlsx', sheet_name='Н1',
    #                    header=[0, 1], index_col=0)
    # df = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н1',
    #                         header=[0, 1], index_col=0)
    df_t = flatten(df)
    table.setRowCount(df_t.shape[0])
    table.setColumnCount(df_t.shape[1])
    # for i in range(len(df.index)):
    #     for j in range(len(df.columns)):
    #         self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
    for i in range(df_t.shape[0]):
        for j in range(df_t.shape[1]):
            table.setItem(i, j, QTableWidgetItem(str('{}\n'.format(df_t.iloc[i][j]))))
    # self.table.resizeColumnsToContents()
    table.resizeRowsToContents()


class Form(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        tab = QTabWidget()

        self.setWindowTitle('SecAnalysis')
        self.setCentralWidget(tab)
        # self.resize(740, 480)

        self.first = QWidget()
        self.second = QWidget()
        self.third = QWidget()

        tab.addTab(self.first, 'Главная')
        tab.addTab(self.second, 'Таблицы')
        tab.addTab(self.third, 'Графики')

        self.Button_ChooseDefDatapath = None
        self.Button_ChooseIntDatapath = None
        self.Button_ChooseConfigs = None
        self.Button_Calculate = None
        self.Label_IntDatapath = None
        self.Label_DefDatapath = None
        self.Label_ListConfigs = None
        self.set_first_tab()

        self.Layout1_tab2 = None
        self.scroller_tab2 = None
        self.scrollAreaWidgetContents_tab2 = None
        self.Layout2_tab2 = None
        self.tables = None
        self.tables_names = ['Н1', 'Н2', 'Н3', 'З1', 'З2', 'З3', 'Л', 'Р']
        self.Button_SaveAll = None
        self.set_second_tab()

        self.Layout1_tab3 = None
        self.scroller_tab3 = None
        self.scrollAreaWidgetContents_tab3 = None
        self.Layout2_tab3 = None
        self.set_third_tab()

        self.def_datapath = None
        self.int_datapath = None
        self.configs_filepaths = None

        self.step1_int_df = None
        self.step2_int_df = None
        self.step3_int_df = None
        self.step1_def_df = None
        self.step2_def_df = None
        self.step3_def_df = None
        self.L_df = None
        self.R_df = None

    def set_first_tab(self):
        self.Button_ChooseDefDatapath = QPushButton('Выбрать исходные данные защиты', self.first)
        self.Button_ChooseDefDatapath.setGeometry(10, 20, 200, 25)
        self.Button_ChooseDefDatapath.clicked.connect(self.choose_def_datapath)

        self.Button_ChooseIntDatapath = QPushButton('Выбрать исходные данные нарушителя', self.first)
        self.Button_ChooseIntDatapath.setGeometry(10, 60, 230, 25)
        self.Button_ChooseIntDatapath.clicked.connect(self.choose_int_datapath)

        self.Button_ChooseConfigs = QPushButton('Выбрать конфигурационные файлы', self.first)
        self.Button_ChooseConfigs.setGeometry(10, 100, 210, 25)
        self.Button_ChooseConfigs.clicked.connect(self.choose_configs_folder)

        self.Button_Calculate = QPushButton('Рассчитать', self.first)
        self.Button_Calculate.setGeometry(240, 100, 120, 25)
        self.Button_Calculate.clicked.connect(self.calculate_tables)

        self.Label_DefDatapath = QLabel(self.first)
        self.Label_DefDatapath.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.Label_DefDatapath.setGeometry(220, 20, 500, 40)

        self.Label_IntDatapath = QLabel(self.first)
        self.Label_IntDatapath.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.Label_IntDatapath.setGeometry(250, 60, 500, 40)

        self.Label_ListConfigs = QLabel(self.first)
        self.Label_ListConfigs.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.Label_ListConfigs.setGeometry(10, 130, 500, 500)

    def set_second_tab(self):
        # Создается вертикальный слой на вкладке
        self.Layout1_tab2 = QVBoxLayout(self.second)
        # Создание скроллера на вкладке
        self.scroller_tab2 = QScrollArea(self.second)
        self.scroller_tab2.setWidgetResizable(True)
        # Создаётся виджет содержимого скролла
        self.scrollAreaWidgetContents_tab2 = QWidget()
        # Создается второй вертикальный слой на виджете содержимого
        self.Layout2_tab2 = QGridLayout(self.scrollAreaWidgetContents_tab2)

        # Сохранение содержимого таблиц
        self.Button_SaveAll = QPushButton('Сохранить в excel-файл', self.scrollAreaWidgetContents_tab2)
        self.Button_SaveAll.setMinimumSize(150, 20)
        self.Button_SaveAll.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.Button_SaveAll.clicked.connect(lambda x: self.save_tables_content)
        # Добавляю кнопку на слой 2
        self.Layout2_tab2.addWidget(self.Button_SaveAll)

        # Создается виджет таблицы на виджете содержимого
        self.tables = []
        for i, name in zip(range(1, 8+1), self.tables_names):
            widget = QTableWidget(self.scrollAreaWidgetContents_tab2)
            widget.setMinimumSize(1200, 800)
            widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            widget_title = QLabel(self.scrollAreaWidgetContents_tab2)
            widget_title.setAlignment(Qt.AlignmentFlag.AlignTop)
            widget_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            widget_title.setMinimumSize(1200, 50)
            widget_title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            widget_title.setText(name)
            widget_title.setStyleSheet('QLabel {font: 15pt "Consolas";}')

            self.Layout2_tab2.addWidget(widget)
            self.Layout2_tab2.addWidget(widget_title)
            self.tables.append(widget)

        # Скролл-арии устанавливается виджет содержимого
        self.scroller_tab2.setWidget(self.scrollAreaWidgetContents_tab2)
        # На вертикальный слой добавляется скролл
        self.Layout1_tab2.addWidget(self.scroller_tab2)

    def set_third_tab(self):
        # Примеры создания графиков
        # graph = QGraphicsView(self.third)
        # scene = QGraphicsScene()
        #
        # graph.setScene(scene)
        #
        # self.plotWdgt = pg.PlotWidget()
        # dataX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # dataY = list(reversed([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        # plot_item = self.plotWdgt.plot(x=dataX, y=dataY)
        #
        # proxy_widget = scene.addWidget(self.plotWdgt)

        # Создается вертикальный слой на вкладке
        self.Layout1_tab3 = QVBoxLayout(self.third)
        # Создание скроллера на вкладке
        self.scroller_tab3 = QScrollArea(self.third)
        self.scroller_tab3.setWidgetResizable(True)
        # Создаётся виджет содержимого скролла
        self.scrollAreaWidgetContents_tab3 = QWidget()
        # Создается второй вертикальный слой на виджете содержимого
        self.Layout2_tab3 = QGridLayout(self.scrollAreaWidgetContents_tab3)
        # Создаются виджеты графиков
        for i in range(1, 16+1):
            widget, _ = create_plot_widget(parent=self.scrollAreaWidgetContents_tab3,
                                           dataX=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                           dataY=list(reversed([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                                           title=f'acbde{i}')
            widget.setMinimumSize(400, 400)
            widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self.Layout2_tab3.addWidget(widget,
                                        i // 2 + i % 2,
                                        2 - i % 2)
        # Скролл-арии устанавливается виджет содержимого
        self.scroller_tab3.setWidget(self.scrollAreaWidgetContents_tab3)
        # На вертикальный слой добавляется скролл
        self.Layout1_tab3.addWidget(self.scroller_tab3)


    def choose_def_datapath(self):
        # noinspection PyTypeChecker
        filepath = QFileDialog.getOpenFileName(self,
                                               caption="Выбрать файл",
                                               directory=".")
        self.def_datapath = filepath[0]

        text = '\n'.join(wrap(f'Вы выбрали файл: {self.def_datapath}', 80))

        self.Label_DefDatapath.setText(text)

    def choose_int_datapath(self):
        # noinspection PyTypeChecker
        filepath = QFileDialog.getOpenFileName(self,
                                               caption="Выбрать файл",
                                               directory=".")
        self.int_datapath = filepath[0]

        text = '\n'.join(wrap(f'Вы выбрали файл: {self.int_datapath}', 80))

        self.Label_IntDatapath.setText(text)

    def choose_configs_folder(self):
        # noinspection PyTypeChecker
        files_dir_name = QFileDialog.getExistingDirectory(self,
                                                          caption="Выбрать папку",
                                                          directory=".")
        if isinstance(files_dir_name, str) and len(files_dir_name) > 0:
            self.configs_filepaths = [os.path.abspath(f'{files_dir_name}\\{filename}')
                                      for filename in
                                      os.listdir(files_dir_name)]
            files_str = '\n• '.join(['\n  '.join(wrap(fp, 80)) for fp in os.listdir(files_dir_name)])

            text = f'Вы выбрали папку: {files_dir_name}\n'\
                   f'Выбранные конфигурационные файлы:\n• {files_str}'

            self.Label_ListConfigs.setText(text)

    def calculate_tables(self):
        pass
        # data_path = r'C:\Users\bzakh\OneDrive\Desktop\Решения для ЛСТ.xlsx'
        if self.configs_filepaths is not None and \
           self.def_datapath is not None and \
           self.int_datapath is not None:
            if any(['yaml' in config for config in self.configs_filepaths]) and \
               '.xls' in self.def_datapath or '.xlsx' in self.def_datapath or '.csv' in self.def_datapath and \
               '.xls' in self.int_datapath or '.xlsx' in self.int_datapath or '.csv' in self.int_datapath:
                configs = {}
                for filepath in self.configs_filepaths:
                    config = get_yaml(filepath)
                    configs.update({config['name']: config})
                    # step1_int_config_path = r'C:\Users\bzakh\OneDrive\Documents\Python_projects\secanalysis\configs\step1_int_config.yaml'

                calculator = Calculator()


                idp_int = InputDataProcessor(data_path=self.int_datapath,
                                             calculator=calculator,
                                             # sheet_name='Н1',
                                             validate_data=True,
                                             config=configs['step1_int_config'],
                                             validation_params={
                                                 'validate_data_shape': True,
                                                 'validate_rows': True,
                                                 'validate_expert_assessments_caption': True
                                             })
                self.step1_int_df = idp_int.return_dataframe()
                set_data_to_table(self.step1_int_df, self.tables[0])


                cdp1_int = CalculatingDataProcessor(calculator=calculator,
                                                    config=configs['step2_int_config'])
                self.step2_int_df = cdp1_int.return_dataframe()
                set_data_to_table(self.step2_int_df, self.tables[1])


                cdp2_int = CalculatingDataProcessor(calculator=calculator,
                                                    config=configs['step3_int_config'])
                self.step3_int_df = cdp2_int.return_dataframe()
                set_data_to_table(self.step3_int_df, self.tables[2])


                idp_def = InputDataProcessor(data_path=self.def_datapath,
                                             calculator=calculator,
                                             # sheet_name='З1',
                                             validate_data=True,
                                             config=configs['step1_def_config'],
                                             validation_params={
                                                 'validate_data_shape': True,
                                                 'validate_rows': True,
                                                 'validate_expert_assessments_caption': True
                                             })
                self.step1_def_df = idp_def.return_dataframe()
                set_data_to_table(self.step1_def_df, self.tables[3])


                cdp1_def = CalculatingDataProcessor(calculator=calculator,
                                                    config=configs['step2_def_config'])
                self.step2_def_df = cdp1_def.return_dataframe()
                set_data_to_table(self.step2_def_df, self.tables[4])


                cdp2_def = CalculatingDataProcessor(calculator=calculator,
                                                    config=configs['step3_def_config'])
                self.step3_def_df = cdp2_def.return_dataframe()
                set_data_to_table(self.step3_def_df, self.tables[5])


                fp_L = CalculatingDataProcessor(calculator=calculator,
                                                config=configs['L_config'])
                self.L_df = fp_L.return_dataframe()
                set_data_to_table(self.L_df, self.tables[6])


                fp_R = CalculatingDataProcessor(calculator=calculator,
                                                config=configs['R_config'])
                self.R_df = fp_R.return_dataframe()
                set_data_to_table(self.R_df, self.tables[7])

            else:
                print('Ошибка. Все конфигурационные файлы должны быть формата .yaml')
        elif self.configs_filepaths is not None:
            print('Ошибка. Необходимо выбрать конфигурационные файлы.')
        elif self.def_datapath is not None:
            print('Ошибка. Необходимо выбрать файл с данными защиты.')
        elif self.int_datapath is not None:
            print('Ошибка. Необходимо выбрать файл с данными нарушителя.')

    def save_tables_content(self):
        filepath = QFileDialog.getOpenFileName(self,
                                               caption="Сохранить файл",
                                               directory=".")
        savepath = filepath[0]
        self.step1_int_df.to_excel(savepath, sheet_name=self.tables_names[0])
        self.step2_int_df.to_excel(savepath, sheet_name=self.tables_names[1])
        self.step3_int_df.to_excel(savepath, sheet_name=self.tables_names[2])
        self.step1_def_df.to_excel(savepath, sheet_name=self.tables_names[3])
        self.step2_def_df.to_excel(savepath, sheet_name=self.tables_names[4])
        self.step3_def_df.to_excel(savepath, sheet_name=self.tables_names[5])
        self.L_df.to_excel(savepath, sheet_name=self.tables_names[6])
        self.R_df.to_excel(savepath, sheet_name=self.tables_names[7])


