import sys
import os
from time import sleep
import logging

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pandas as pd
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
from textwrap3 import wrap

from Arithmetics import Calculator
# from GUI_support import DataFrameModel
from Processors import InputDataProcessor, CalculatingDataProcessor
from functions import get_yaml, flatten, minmax_scale


def create_plot_widget(parent,
                       dataX,
                       dataY,
                       points=None,
                       title=''):
    graph = QGraphicsView(parent)
    graph.setVisible(False)
    scene = QGraphicsScene()
    graph.setScene(scene)
    plot_widget = PlotWidget()
    plot_widget.setBackground('white')
    plot_widget.showGrid(True, True)
    plot_widget.setTitle(title)

    plot_widget.plot(x=dataX,
                     y=dataY,
                     pen=pg.mkPen('black', width=3))

    if points is not None:
        for point in points:
            scatter = pg.ScatterPlotItem(
                size=6, brush=pg.mkBrush(255, 0, 0, 255))
            # creating spots using the random position
            spots = [{'pos': point, 'data': 1}]
            # adding points to the scatter plot
            scatter.addPoints(spots)
            plot_widget.addItem(scatter)

    return plot_widget


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

def clearLayout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())


class QTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class Form(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        tab = QTabWidget()

        self.setWindowTitle('SecAnalysis')
        self.setCentralWidget(tab)
        # self.resize(740, 480)
        self.showMaximized()

        self.first = QWidget()
        self.second = QWidget()
        self.third = QWidget()

        tab.addTab(self.first, 'Главная')
        tab.addTab(self.second, 'Таблицы')
        tab.addTab(self.third, 'Графики')

        self.validate_data_shape_flag = False
        self.validate_rows_flag = False
        self.validate_expert_assessments_caption_flag = False
        self.tables_calculated = False
        self.tables_plotted = False
        self.normalization_flag = False

        self.MainLayout_tab1 = None
        self.Layout1_tab1 = None
        self.Scroller_tab1 = None
        self.ScrollAreaWidgetContents_tab1 = None
        self.Layout2_tab1 = None
        self.Layout3_tab1 = None
        self.Button_ChooseDefDatapath = None
        self.Button_ChooseIntDatapath = None
        self.Button_ChooseConfigs = None
        self.Button_Calculate = None
        self.RadioButton_Validate_data_shape = None
        self.RadioButton_Validate_rows = None
        self.RadioButton_Validate_expert_assessments_caption = None
        self.Button_Plot = None
        self.RadioButton_NormFlag = None
        self.Label_IntDatapath = None
        self.Label_DefDatapath = None
        self.Label_ListConfigs = None
        self.LogTextBox = None
        self.set_first_tab()

        self.Layout1_tab2 = None
        self.scroller_tab2 = None
        self.scrollAreaWidgetContents_tab2 = None
        self.Layout2_tab2 = None
        self.calculator = None
        self.configs = None
        self.tables = None
        self.tables_names = ['Н1', 'Н2', 'Н3', 'З1', 'З2', 'З3', 'Л', 'Р']
        self.Button_SaveAll = None
        # self.set_second_tab()

        self.Layout1_tab3 = None
        self.scroller_tab3 = None
        self.scrollAreaWidgetContents_tab3 = None
        self.Layout2_tab3 = None
        # self.set_third_tab()

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

        self.shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut.activated.connect(self.save_tables_content)

        self.Layout1_tab1 = None
        logging.info('Программа готова к работе.')

    def set_first_tab(self):
        self.MainLayout_tab1 = QGridLayout()

        self.Layout1_tab1 = QVBoxLayout()
        self.Scroller_tab1 = QScrollArea()
        self.Scroller_tab1.setWidgetResizable(True)
        self.ScrollAreaWidgetContents_tab1 = QWidget()
        self.Layout2_tab1 = QGridLayout(self.ScrollAreaWidgetContents_tab1)

        self.Button_ChooseIntDatapath = QPushButton('Выбрать исходные данные Нарушителя')
        # self.Button_ChooseIntDatapath.setGeometry(10, 60, 230, 25)
        self.Button_ChooseIntDatapath.clicked.connect(self.choose_int_datapath)

        self.Button_ChooseDefDatapath = QPushButton('Выбрать исходные данные Защиты')
        # self.Button_ChooseDefDatapath.setGeometry(10, 20, 200, 25)
        self.Button_ChooseDefDatapath.clicked.connect(self.choose_def_datapath)

        self.Button_ChooseConfigs = QPushButton('Выбрать конфигурационные файлы')
        # self.Button_ChooseConfigs.setGeometry(10, 100, 210, 25)
        self.Button_ChooseConfigs.clicked.connect(self.choose_configs_folder)

        self.Button_Calculate = QPushButton('Рассчитать')
        # self.Button_Calculate.setGeometry(240, 100, 120, 25)
        self.Button_Calculate.clicked.connect(self.calculate_tables)

        self.RadioButton_Validate_data_shape = QCheckBox(
            'Проверка соответствия размерности данных из файлов Защиты и Нарушителя и \nразмерности из конфигурационных файлов.')
        # self.RadioButton_NormFlag.setGeometry(10, 150, 120, 25)
        self.RadioButton_Validate_data_shape.clicked.connect(self.change_validate_data_shape_flag)

        self.RadioButton_Validate_rows = QCheckBox(
            'Проверка соответствия названий строк в файлах Защиты и Нарушителя конфигурации.')
        # self.RadioButton_NormFlag.setGeometry(10, 150, 120, 25)
        self.RadioButton_Validate_rows.clicked.connect(self.change_validate_rows_flag)

        self.RadioButton_Validate_expert_assessments_caption = QCheckBox(
            'Проверка соответствия названия серии экспертных заключений в файлах Защиты и Нарушителя конфигурации.')
        # self.RadioButton_NormFlag.setGeometry(10, 150, 120, 25)
        self.RadioButton_Validate_expert_assessments_caption.clicked.connect(
            self.change_validate_expert_assessments_caption_flag)

        self.Button_Plot = QPushButton('Построить графики')
        # self.Button_Calculate.setGeometry(240, 100, 120, 25)
        self.Button_Plot.clicked.connect(self.plot_tables)

        self.RadioButton_NormFlag = QCheckBox('Нормализация графиков')
        # self.RadioButton_NormFlag.setGeometry(10, 150, 120, 25)
        self.RadioButton_NormFlag.clicked.connect(self.change_normalization_flag)

        self.Label_DefDatapath = QLabel()
        self.Label_DefDatapath.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.Label_DefDatapath.setGeometry(220, 20, 500, 40)

        self.Label_IntDatapath = QLabel()
        self.Label_IntDatapath.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.Label_IntDatapath.setGeometry(250, 60, 500, 40)

        self.Label_ListConfigs = QLabel()
        self.Label_ListConfigs.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.Label_ListConfigs.setGeometry(10, 130, 500, 500)

        self.Layout2_tab1.addWidget(self.Button_ChooseIntDatapath)
        self.Layout2_tab1.addWidget(self.Button_ChooseDefDatapath)
        self.Layout2_tab1.addWidget(self.Button_ChooseConfigs)
        self.Layout2_tab1.addWidget(self.Button_Calculate)
        self.Layout2_tab1.addWidget(self.RadioButton_Validate_data_shape)
        self.Layout2_tab1.addWidget(self.RadioButton_Validate_rows)
        self.Layout2_tab1.addWidget(self.RadioButton_Validate_expert_assessments_caption)
        self.Layout2_tab1.addWidget(self.Button_Plot)
        self.Layout2_tab1.addWidget(self.RadioButton_NormFlag)
        self.Layout2_tab1.addWidget(self.Label_DefDatapath)
        self.Layout2_tab1.addWidget(self.Label_IntDatapath)
        self.Layout2_tab1.addWidget(self.Label_ListConfigs)
        # self.Layout2_tab1.addWidget(self.LogTextBox.widget)

        self.Scroller_tab1.setWidget(self.ScrollAreaWidgetContents_tab1)
        # На вертикальный слой добавляется скролл
        self.Layout1_tab1.addWidget(self.Scroller_tab1)

        self.Layout3_tab1 = QVBoxLayout()

        self.LogTextBox = QTextEditLogger()
        self.LogTextBox.widget.setStyleSheet(
            'QPlainTextEdit {font-family: ui-monospace,"Cascadia Mono","Segoe UI Mono","Liberation Mono",Menlo,Monaco,Consolas,monospace;}')
        self.LogTextBox.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)-8s - %(message)s  ',
                                                       datefmt='%d.%m.%Y %H:%M:%S'))
        logging.getLogger().addHandler(self.LogTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        self.Layout3_tab1.addWidget(self.LogTextBox.widget)

        self.MainLayout_tab1.setRowStretch(0, 3)
        self.MainLayout_tab1.setRowStretch(1, 1)
        self.MainLayout_tab1.setRowStretch(2, 2)
        self.MainLayout_tab1.addLayout(self.Layout1_tab1, 0, 0, 2, 0)
        self.MainLayout_tab1.addLayout(self.Layout3_tab1, 2, 0)
        self.first.setLayout(self.MainLayout_tab1)
        # for item in range(10):
        #     logging.debug('damn, a bug')
        #     logging.info('something to remember')
        #     logging.warning('that\'s not right')
        #     logging.error('foobar')

    def change_validate_data_shape_flag(self):
        self.validate_data_shape_flag = self.RadioButton_Validate_data_shape.isChecked()
        if self.validate_data_shape_flag:
            logging.info('Соответствие размерности данных включено.')
        else:
            logging.info('Соответствие размерности данных выключено.')

    def change_validate_rows_flag(self):
        self.validate_rows_flag = self.RadioButton_Validate_rows.isChecked()
        if self.validate_rows_flag:
            logging.info('Соответствие названий строк включено.')
        else:
            logging.info('Соответствие названий строк выключено.')

    def change_validate_expert_assessments_caption_flag(self):
        self.validate_expert_assessments_caption_flag = self.RadioButton_Validate_expert_assessments_caption.isChecked()
        if self.validate_expert_assessments_caption_flag:
            logging.info('Соответствие названия серии экспертных заключений включено.')
        else:
            logging.info('Соответствие названия серии экспертных заключений выключено.')

    def change_normalization_flag(self):
        self.normalization_flag = self.RadioButton_NormFlag.isChecked()
        if self.normalization_flag:
            logging.info('Нормализация графиков включена.')
        else:
            logging.info('Нормализация графиков выключена.')

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
        self.Button_SaveAll.clicked.connect(self.save_tables_content)
        # Добавляю кнопку на слой 2
        self.Layout2_tab2.addWidget(self.Button_SaveAll)

        # Создается виджет таблицы на виджете содержимого
        self.tables = []
        for i, name in zip(range(1, 8 + 1), self.tables_names):
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

    def set_third_tab(self, calculate_plots=False):
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
        if calculate_plots:
            plots_iterator = self.get_plot_data()
            for i, plotX, plotY, actual_point, title in plots_iterator:
                # for i in range(1, 16+1):
                widget = create_plot_widget(parent=self.scrollAreaWidgetContents_tab3,
                                            dataX=plotX,
                                            dataY=plotY,
                                            points=[actual_point],
                                            title=title)
                widget.setMinimumSize(400, 400)
                widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                # noinspection PyArgumentList
                self.Layout2_tab3.addWidget(widget,
                                            i // 2 + i % 2,
                                            2 - i % 2)
        else:
            for i in range(1, 16 + 1):
                widget = create_plot_widget(parent=self.scrollAreaWidgetContents_tab3,
                                            dataX=[],
                                            dataY=[],
                                            title=f'{i}')
                widget.setMinimumSize(400, 400)
                widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                # noinspection PyArgumentList
                self.Layout2_tab3.addWidget(widget,
                                            i // 2 + i % 2,
                                            2 - i % 2)
        # Скролл-арии устанавливается виджет содержимого
        self.scroller_tab3.setWidget(self.scrollAreaWidgetContents_tab3)
        # На вертикальный слой добавляется скролл
        self.Layout1_tab3.addWidget(self.scroller_tab3)
        logging.info('Графики созданы успешно.')

    def update_first_tab(self):
        self.MainLayout_tab1 = None
        self.Layout1_tab1 = None
        self.Scroller_tab1 = None
        self.ScrollAreaWidgetContents_tab1 = None
        self.Layout2_tab1 = None
        self.Layout3_tab1 = None
        self.Button_ChooseDefDatapath = None
        self.Button_ChooseIntDatapath = None
        self.Button_ChooseConfigs = None
        self.Button_Calculate = None
        self.RadioButton_Validate_data_shape = None
        self.RadioButton_Validate_rows = None
        self.RadioButton_Validate_expert_assessments_caption = None
        self.Button_Plot = None
        self.RadioButton_NormFlag = None
        self.Label_IntDatapath = None
        self.Label_DefDatapath = None
        self.Label_ListConfigs = None
        self.LogTextBox = None
        self.first.update()
        # self.MainLayout_tab1.update()

    def update_second_tab(self):
        self.Layout1_tab2 = None
        self.scroller_tab2 = None
        self.scrollAreaWidgetContents_tab2 = None
        self.Layout2_tab2 = None
        self.calculator = None
        self.configs = None
        self.tables = None
        # self.tables_names = ['Н1', 'Н2', 'Н3', 'З1', 'З2', 'З3', 'Л', 'Р']
        self.Button_SaveAll = None
        self.second.update()
        # self.Layout1_tab2.update()
        # self.Layout2_tab2.update()

    def update_third_tab(self):
        self.scroller_tab3 = None
        self.scrollAreaWidgetContents_tab3 = None
        clearLayout(self.Layout2_tab3)
        clearLayout(self.Layout1_tab3)
        self.Layout1_tab3.update()
        self.Layout2_tab3.update()
        self.Layout2_tab3 = None
        self.Layout1_tab3 = None
        self.third.update()

    def choose_def_datapath(self):
        # noinspection PyTypeChecker
        filepath = QFileDialog.getOpenFileName(self,
                                               caption="Выбрать файл",
                                               directory="")
        self.def_datapath = filepath[0]

        text = '\n'.join(wrap(f'Файл данных Защиты: {self.def_datapath}', 80))

        self.Label_DefDatapath.setText(text)
        logging.info(text)

    def choose_int_datapath(self):
        # noinspection PyTypeChecker
        filepath = QFileDialog.getOpenFileName(self,
                                               caption="Выбрать файл",
                                               directory="")
        self.int_datapath = filepath[0]

        text = '\n'.join(wrap(f'Файл данных Нарушителя: {self.int_datapath}', 80))

        self.Label_IntDatapath.setText(text)
        logging.info(text)

    def choose_configs_folder(self):
        # noinspection PyTypeChecker
        files_dir_name = QFileDialog.getExistingDirectory(self,
                                                          caption="Выбрать папку",
                                                          directory="")
        if isinstance(files_dir_name, str) and len(files_dir_name) > 0:
            self.configs_filepaths = [os.path.abspath(f'{files_dir_name}\\{filename}')
                                      for filename in
                                      os.listdir(files_dir_name)]
            files_str = '\n• '.join(['\n  '.join(wrap(fp, 80)) for fp in os.listdir(files_dir_name)])

            text = f'Папка с конфигурационными файлами: {files_dir_name}\n' \
                   f'Выбранные конфигурационные файлы:\n• {files_str}'

            self.Label_ListConfigs.setText(text)
            logging.info(f'Папка с конфигурационными файлами: {files_dir_name}')

    def calculate_tables(self):
        # data_path = r'C:\Users\bzakh\OneDrive\Desktop\Решения для ЛСТ.xlsx'
        if self.configs_filepaths is not None and \
                self.def_datapath is not None and \
                self.int_datapath is not None:
            if any(['yaml' in config for config in self.configs_filepaths]) and \
                    '.xls' in self.def_datapath or '.xlsx' in self.def_datapath or '.csv' in self.def_datapath and \
                    '.xls' in self.int_datapath or '.xlsx' in self.int_datapath or '.csv' in self.int_datapath:
                if self.tables_calculated:
                    self.update_second_tab()
                logging.info('Начат процесс расчета таблиц.')
                self.set_second_tab()
                self.configs = {}
                for filepath in self.configs_filepaths:
                    config = get_yaml(filepath)
                    self.configs.update({config['name']: config})
                    # step1_int_config_path = r'C:\Users\bzakh\OneDrive\Documents\Python_projects\secanalysis\configs\step1_int_config.yaml'

                self.calculator = Calculator()

                idp_int = InputDataProcessor(data_path=self.int_datapath,
                                             calculator=self.calculator,
                                             # sheet_name='Н1',
                                             validate_data=any([self.validate_data_shape_flag,
                                                                self.validate_rows_flag,
                                                                self.validate_expert_assessments_caption_flag]),
                                             config=self.configs['step1_int_config'],
                                             validation_params={
                                                 'validate_data_shape': self.validate_data_shape_flag,
                                                 'validate_rows': self.validate_rows_flag,
                                                 'validate_expert_assessments_caption': self.validate_expert_assessments_caption_flag
                                             })
                self.step1_int_df = idp_int.return_dataframe()
                set_data_to_table(self.step1_int_df, self.tables[0])

                cdp1_int = CalculatingDataProcessor(calculator=self.calculator,
                                                    config=self.configs['step2_int_config'])
                self.step2_int_df = cdp1_int.return_dataframe()
                set_data_to_table(self.step2_int_df, self.tables[1])

                cdp2_int = CalculatingDataProcessor(calculator=self.calculator,
                                                    config=self.configs['step3_int_config'])
                self.step3_int_df = cdp2_int.return_dataframe()
                set_data_to_table(self.step3_int_df, self.tables[2])

                idp_def = InputDataProcessor(data_path=self.def_datapath,
                                             calculator=self.calculator,
                                             # sheet_name='З1',
                                             validate_data=any([self.validate_data_shape_flag,
                                                                self.validate_rows_flag,
                                                                self.validate_expert_assessments_caption_flag]),
                                             config=self.configs['step1_def_config'],
                                             validation_params={
                                                 'validate_data_shape': self.validate_data_shape_flag,
                                                 'validate_rows': self.validate_rows_flag,
                                                 'validate_expert_assessments_caption': self.validate_expert_assessments_caption_flag
                                             })
                self.step1_def_df = idp_def.return_dataframe()
                set_data_to_table(self.step1_def_df, self.tables[3])

                cdp1_def = CalculatingDataProcessor(calculator=self.calculator,
                                                    config=self.configs['step2_def_config'])
                self.step2_def_df = cdp1_def.return_dataframe()
                set_data_to_table(self.step2_def_df, self.tables[4])

                cdp2_def = CalculatingDataProcessor(calculator=self.calculator,
                                                    config=self.configs['step3_def_config'])
                self.step3_def_df = cdp2_def.return_dataframe()
                set_data_to_table(self.step3_def_df, self.tables[5])

                fp_L = CalculatingDataProcessor(calculator=self.calculator,
                                                config=self.configs['L_config'])
                self.L_df = fp_L.return_dataframe()
                set_data_to_table(self.L_df, self.tables[6])

                fp_R = CalculatingDataProcessor(calculator=self.calculator,
                                                config=self.configs['R_config'])
                self.R_df = fp_R.return_dataframe()
                set_data_to_table(self.R_df, self.tables[7])

                self.tables_calculated = True
                logging.info('Расчет таблиц произведен успешно.')
            else:
                logging.error('Все конфигурационные файлы должны быть формата .yaml')
        else:
            msg = 'Расчет таблиц произведен не был. '
            if self.def_datapath is None:
                msg += 'Необходимо выбрать файл с данными Защиты. '
            if self.int_datapath is None:
                msg += 'Необходимо выбрать файл с данными Нарушителя. '
            if self.configs_filepaths is None:
                msg += 'Необходимо выбрать конфигурационные файлы. '
            logging.error(msg)

    def plot_tables(self):
        if self.tables_calculated:
            logging.info('Проведение расчетов подтверждено. Запущен процесс создания графиков.')
            sleep(1)
            if self.tables_plotted:
                logging.info('Обновление страницы с графиками.')
                # self.update_third_tab()
                plots_iterator = self.get_plot_data()
                for i in range(1, self.Layout2_tab3.rowCount()):
                    for j in range(1, self.Layout2_tab3.columnCount()):
                        child = self.Layout2_tab3.itemAtPosition(i, j)
                        # logging.info(f'{i}.{j}: child{type(child)}')
                        # if child is not None and \
                        #    'widget' in dir(child) and \
                        #    child.widget() is not None:
                        #     logging.info(f'{i}.{j}: child.widget{type(child.widget())}')
                        if child is not None and \
                           'widget' in dir(child) and \
                           child.widget() is not None and \
                           isinstance(child.widget(), PlotWidget):
                            # logging.info(f'{i}.{j}: child.widget{type(child.widget())}')
                            _i, dataX, dataY, actual_point, title = next(plots_iterator)
                            child.widget().clear()
                            child.widget().plot(x=dataX,
                                                y=dataY,
                                                pen=pg.mkPen('black', width=3))
                            child.widget().setBackground('white')
                            child.widget().showGrid(True, True)
                            child.widget().setTitle(title)

                            scatter = pg.ScatterPlotItem(
                                size=6, brush=pg.mkBrush(255, 0, 0, 255))
                            # creating spots using the random position
                            spots = [{'pos': actual_point, 'data': 1}]
                            # adding points to the scatter plot
                            scatter.addPoints(spots)
                            child.widget().addItem(scatter)
                # self.set_third_tab(calculate_plots=True)
            else:
                self.set_third_tab(calculate_plots=True)
                self.tables_plotted = True
        else:
            logging.error('Нельзя отобразить графики, не проведя расчеты.')

    def get_plot_data(self):
        X = range(0, 100, 1)

        # plot 1
        formulae = self.calculator.get_variable('e_1')['formulae']
        point = [
            self.calculator.get_variable('t_3_1_avg')['value'],
            self.calculator.get_variable('e_1')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'t_3_1_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 1, X, y, point, f'e_1(t_3_1_avg)'

        # plot 2
        formulae = self.calculator.get_variable('e_2')['formulae']
        point = [
            self.calculator.get_variable('t_3_2_avg')['value'],
            self.calculator.get_variable('e_2')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'t_3_2_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 2, X, y, point, f'e_2(t_3_2_avg)'

        # plot 3
        formulae = self.calculator.get_variable('e_3')['formulae']
        point = [
            self.calculator.get_variable('t_3_3_avg')['value'],
            self.calculator.get_variable('e_3')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'t_3_3_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 3, X, y, point, f'e_3(t_3_3_avg)'

        # plot 4
        formulae = self.calculator.get_variable('e_4')['formulae']
        point = [
            self.calculator.get_variable('t_3_4_avg')['value'],
            self.calculator.get_variable('e_4')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'t_3_4_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 4, X, y, point, f'e_4(t_3_4_avg)'

        # plot 5
        formulae = self.calculator.get_variable('e_1')['formulae']
        point = [
            self.calculator.get_variable('o_3_1_avg')['value'],
            self.calculator.get_variable('e_1')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'o_3_1_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 5, X, y, point, f'e_1(o_3_1_avg)'

        # plot 6
        formulae = self.calculator.get_variable('e_2')['formulae']
        point = [
            self.calculator.get_variable('o_3_2_avg')['value'],
            self.calculator.get_variable('e_2')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'o_3_2_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 6, X, y, point, f'e_2(o_3_2_avg)'

        # plot 7
        formulae = self.calculator.get_variable('e_3')['formulae']
        point = [
            self.calculator.get_variable('o_3_3_avg')['value'],
            self.calculator.get_variable('e_3')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'o_3_3_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 7, X, y, point, f'e_3(o_3_3_avg)'

        # plot 8
        formulae = self.calculator.get_variable('e_4')['formulae']
        point = [
            self.calculator.get_variable('o_3_4_avg')['value'],
            self.calculator.get_variable('e_4')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'o_3_4_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 8, X, y, point, f'e_4(o_3_4_avg)'

        # plot 9
        formulae = self.calculator.get_variable('e_1')['formulae']
        point = [
            self.calculator.get_variable('nu_1_avg')['value'],
            self.calculator.get_variable('e_1')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'nu_1_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 9, X, y, point, f'e_1(nu_1_avg)'

        # plot 10
        formulae = self.calculator.get_variable('e_2')['formulae']
        point = [
            self.calculator.get_variable('nu_2_avg')['value'],
            self.calculator.get_variable('e_2')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'nu_2_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 10, X, y, point, f'e_2(nu_2_avg)'

        # plot 11
        formulae = self.calculator.get_variable('e_3')['formulae']
        point = [
            self.calculator.get_variable('nu_3_avg')['value'],
            self.calculator.get_variable('e_3')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'nu_3_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 11, X, y, point, f'e_3(nu_3_avg)'

        # plot 12
        formulae = self.calculator.get_variable('e_4')['formulae']
        point = [
            self.calculator.get_variable('nu_4_avg')['value'],
            self.calculator.get_variable('e_4')['value']
        ]
        y = [self.calculator.evaluate(formulae, data={'nu_4_avg': x}) for x in X]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 12, X, y, point, f'e_4(nu_4_avg)'

        # plot 13
        formulae = self.calculator.get_variable('e_1')['formulae']
        e_1_values = [self.calculator.evaluate(formulae, data={'t_3_1_avg': x}) for x in X]
        point = [
            self.calculator.get_variable('e_1')['value'],
            self.calculator.get_variable('E')['value']
        ]
        formulae = self.calculator.get_variable('E')['formulae']
        y = [self.calculator.evaluate(formulae, data={'e_1': e_1}) for e_1 in e_1_values]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 13, e_1_values, y, point, f'E(e_1(t_3_1_avg))'

        # plot 14
        formulae = self.calculator.get_variable('e_2')['formulae']
        e_2_values = [self.calculator.evaluate(formulae, data={'t_3_2_avg': x}) for x in X]
        point = [
            self.calculator.get_variable('e_2')['value'],
            self.calculator.get_variable('E')['value']
        ]
        formulae = self.calculator.get_variable('E')['formulae']
        y = [self.calculator.evaluate(formulae, data={'e_2': e_2}) for e_2 in e_2_values]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 14, e_2_values, y, point, f'E(e_2(t_3_2_avg))'

        # plot 15
        formulae = self.calculator.get_variable('e_3')['formulae']
        e_3_values = [self.calculator.evaluate(formulae, data={'t_3_3_avg': x}) for x in X]
        point = [
            self.calculator.get_variable('e_3')['value'],
            self.calculator.get_variable('E')['value']
        ]
        formulae = self.calculator.get_variable('E')['formulae']
        y = [self.calculator.evaluate(formulae, data={'e_3': e_3}) for e_3 in e_3_values]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 15, e_3_values, y, point, f'E(e_3(t_3_3_avg))'

        # plot 16
        formulae = self.calculator.get_variable('e_4')['formulae']
        e_4_values = [self.calculator.evaluate(formulae, data={'t_3_4_avg': x}) for x in X]
        point = [
            self.calculator.get_variable('e_4')['value'],
            self.calculator.get_variable('E')['value']
        ]
        formulae = self.calculator.get_variable('E')['formulae']
        y = [self.calculator.evaluate(formulae, data={'e_4': e_4}) for e_4 in e_4_values]
        if self.normalization_flag:
            yp = minmax_scale(y + [point[1]])
            y = yp[:-1]
            point[1] = yp[-1]
        yield 16, e_4_values, y, point, f'E(e_4(t_3_4_avg))'

    def save_tables_content(self):
        if self.step1_int_df is not None and \
                self.step2_int_df is not None and \
                self.step3_int_df is not None and \
                self.step1_def_df is not None and \
                self.step2_def_df is not None and \
                self.step3_def_df is not None and \
                self.L_df is not None and \
                self.R_df is not None:
            # noinspection PyTypeChecker
            filepath = QFileDialog.getSaveFileName(self,
                                                   'Сохранить файл',
                                                   directory='.',
                                                   initialFilter='.xlsx'
                                                   )
            savepath = filepath[0]

            writer = pd.ExcelWriter(savepath, engine='openpyxl')

            self.step1_int_df.to_excel(writer, sheet_name=self.tables_names[0], startrow=0, startcol=0)
            self.step2_int_df.to_excel(writer, sheet_name=self.tables_names[1], startrow=0, startcol=0)
            self.step3_int_df.to_excel(writer, sheet_name=self.tables_names[2], startrow=0, startcol=0)
            self.step1_def_df.to_excel(writer, sheet_name=self.tables_names[3], startrow=0, startcol=0)
            self.step2_def_df.to_excel(writer, sheet_name=self.tables_names[4], startrow=0, startcol=0)
            self.step3_def_df.to_excel(writer, sheet_name=self.tables_names[5], startrow=0, startcol=0)
            self.L_df.to_excel(writer, sheet_name=self.tables_names[6], startrow=0, startcol=0)
            self.R_df.to_excel(writer, sheet_name=self.tables_names[7], startrow=0, startcol=0)
            writer.save()
