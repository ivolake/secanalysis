from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import sys
import os
import pandas as pd

from Arithmetics import Calculator
#from GUI_support import DataFrameModel
from Processors import InputDataProcessor


class Form(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
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
        Button_table = QPushButton('Создать',self.second)
        Button_table.clicked.connect(self.get_table)



        self.Label_ListConfigs = QLabel(self.first)

        self.Label_ListConfigs.setGeometry(200, 100, 300, 20)



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

    # def set_dataframe_widget(self,
    #                          df: pd.DataFrame,
    #                          parent=None):
    #     model = DataFrameModel(df, parent=parent)
    #     self.tableView.setModel(model)
    def get_table(self):
        df = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н1',
                                header=[0, 1], index_col=0)
        old = df.columns[0][1]
        old1 = df.columns[11][1]
        df = df.rename(columns={old: '', old1: ''})
        #df = pd.DataFrame({"a": [4, 5, 6], "b": [7, 8, 9], "c": [10, 11, 12]}, index=[1, 2, 3])
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def choose_folder(self):
        config_dir_name = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        configs = os.listdir(config_dir_name)
        configs_str = '\n•'.join(configs)
        self.Label_ListConfigs.setText(f'Вы выбрали папку: {config_dir_name}\n'
                                       f'Выбранные конфигурационные файлы:\n•{configs_str}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec())

