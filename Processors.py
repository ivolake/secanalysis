from typing import Iterable

import pandas as pd
import numpy as np

from functions import get_yaml


class Step1Processor():
    def __init__(self,
                 data_path: str,
                 sheet_name: str = None,
                 validate_data: bool = False,
                 config_path: str = None,
                 config: dict = None,
                 **kwargs):
        self.data_path = data_path
        self.validate_dataframe_flag = validate_data
        self.config_path = config_path
        self.config = config

        self.sheet_name = sheet_name

        val_params = kwargs.get('validation_params', {})
        self.__validate_data_shape_flag = val_params.get('validate_data_shape', False)
        self.__validate_rows_flag = val_params.get('validate_rows', False)
        self.__validate_expert_assessment_caption_flag = val_params.get('validate_expert_assessments_caption', False)
        self.__validate_aggregation_functions_flag = val_params.get('validate_aggregation_functions', False)

        if not self.validate_dataframe_flag and any([self.__validate_data_shape_flag,
                                                     self.__validate_rows_flag,
                                                     self.__validate_expert_assessment_caption_flag,
                                                     self.__validate_aggregation_functions_flag]):
            print('Error. Нельзя одновременно не указывать флаг валидации и указывать какие-либо параметры валидации.')
        elif self.validate_dataframe_flag and not any([self.__validate_data_shape_flag,
                                                       self.__validate_rows_flag,
                                                       self.__validate_expert_assessment_caption_flag,
                                                       self.__validate_aggregation_functions_flag]):
            print('Error. Нельзя одновременно указывать флаг валидации и не указывать какие-либо параметры валидации.')

        if self.validate_dataframe_flag and self.config is None and self.config is None:
            print('Error. Для валидации необходимо указать конфигурацию файла данных или путь до файла с конфигурацией.')
        elif self.validate_dataframe_flag and (self.config is not None or self.config is not None):
            if self.config is not None and self.config_path is not None:
                print('Error. Нельзя одновременно указывать и конфигурацию, и путь до файла с конфигурацией.')
            # elif self.config is None and self.config_path is None:
            #     print('Error: Нельзя одновременно не указывать и конфигурацию, и путь до файла с конфигурацией.')

        self.dataframe: pd.DataFrame = None


    def __repr__(self):
        return f'Step1Processor(data_path={self.data_path})'


    def read_dataframe(self):
        dataframe_type = self.data_path[self.data_path.rfind('.'):]
        if dataframe_type in ['.xls', '.xlsx']:
            self.dataframe = pd.read_excel(self.data_path, sheet_name=self.sheet_name, header=[0, 1], index_col=[0, 1])
            return True
        elif dataframe_type in ['.csv']:
            self.dataframe = pd.read_csv()
            return True
        else:
            print(f'Error. Тип файла данных неизвестен: {dataframe_type}')
            return False


    def __validate_data_shape(self) -> bool:
        data_shape = self.dataframe.to_numpy().shape

        cols = list(np.arange(1, self.config['expert_assessments_num'] + 1, 1)) + self.config['aggregation_functions']
        config_data_shape = (len(self.config['rows']), len(cols))

        res = data_shape == config_data_shape

        if res:
            print('Info. Размерность данных соответствует конфигурации')
        else:
            print(f'Error. Размерность данных ({data_shape}) не соответствует конфигурации ({config_data_shape})')

        return res

    def __validate_rows(self) -> bool:
        data_rows = np.stack(self.dataframe.index.to_numpy())[:, 1]
        # noinspection PyTypeChecker
        rows_validation = dict(zip(data_rows,
                                   data_rows == self.config['rows']))

        res = min(rows_validation.values())

        if res:
            print('Info. Названия строк соответствуют конфигурации')
        else:
            error_names = '", "'.join(dict(filter(lambda x: not x[1], rows_validation.items())).keys())
            print(f'Error. Названия строк "{error_names}" не соответствуют конфигурации')

        return res

    def __validate_expert_assessment_caption(self) -> bool:
        data_expert_assessment_caption = np.unique(np.stack(self.dataframe.columns.to_numpy())[:, 0])[0]

        res = data_expert_assessment_caption == self.config['expert_assessments_caption']

        if res:
            print('Info. Название серии экспертных заключений соответствует конфигурации')
        else:
            print(f'Error. Название серии экспертных заключений "{data_expert_assessment_caption}" не соответствует конфигурации')

        return res

    def __validate_aggregation_functions(self) -> bool:
        data_aggregation_functions = np.unique(np.stack(self.dataframe.columns.to_numpy())[:, 0])[1:]

        # noinspection PyTypeChecker
        funcs_validation = dict(zip(data_aggregation_functions,
                                    data_aggregation_functions == self.config['aggregation_functions']))

        res = min(funcs_validation.values())

        if res:
            print('Info. Список функций агрегации соответствует конфигурации')
        else:
            error_names = '", "'.join(dict(filter(lambda x: not x[1], funcs_validation.items())).keys())
            print(f'Error. Список функций агрегации ("{error_names}") не соответствует конфигурации')

        return res

    def __validate_dataframe(self) -> bool:
        if self.config is None:
            self.config = get_yaml(self.config_path)

        validations = []
        if self.__validate_data_shape_flag:
            validations.append(self.__validate_data_shape())
        if self.__validate_rows_flag:
            validations.append(self.__validate_rows())
        if self.__validate_expert_assessment_caption_flag:
            validations.append(self.__validate_expert_assessment_caption())
        if self.__validate_aggregation_functions_flag:
            validations.append(self.__validate_aggregation_functions())

        return any(validations)

    def finalize_dataframe(self):

        # Очищение от некрасивых надписей под ячейками с названиями функций агрегации (типа 'Unnamed: 12_level_1')
        # ---
        cols = self.dataframe.columns.to_numpy()
        for i in range(self.config['expert_assessments_num'],
                       self.config['expert_assessments_num'] + len(self.config['aggregation_functions'])):
            cols[i] = (cols[i][0], '')
        self.dataframe.columns = pd.MultiIndex.from_tuples(cols,
                                                           names=self.dataframe.columns[self.config['expert_assessments_num']:].names)
        # ---

        # # Очищение от дополнительного столбца чисел в индексе
        # # ---
        # self.dataframe.index = np.stack(self.dataframe.index.to_numpy())[:, 1]
        # # ---
        return True

    def create_dataframe(self):
        dataframe_read = self.read_dataframe()
        if dataframe_read and self.validate_dataframe_flag:
            dataframe_validated = self.__validate_dataframe()
        else:
            dataframe_validated = False

        dataframe_finalized = self.finalize_dataframe()

        return dataframe_read and dataframe_validated and dataframe_finalized

    def return_dataframe(self):
        dataframe_created = self.create_dataframe()
        if dataframe_created:
            return self.dataframe
        else:
            print('Датафрейм еще не создан. Создать датафрейм можно с помощью метода create_dataframe.')


class Step2Processor:
    def __init__(self, step1_df: pd.DataFrame):
        self.step1_df = step1_df

    def return_dataframe(self):
        ...
        return ...



def func1():
    data_H1 = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н1',header=[0, 1], index_col=0)
    old = data_H1.columns[0][1]
    old1 = data_H1.columns[11][1]
    data_H1 = data_H1.rename(columns={old: '', old1: ''})
    data_H2 = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н2',header=0, index_col=0)
    data_H2.dropna(inplace=True)
    data_H1['Среднее значение'] = 0
    data_H1['Среднее значение'] = data_H1['Данные экспертов относительно времени реализации функций'].mean(axis=1)
    avr = list(data_H1['Среднее значение'])
    # Осуществление доступа к периферийным устройствам охранного мониторинга территории и акватории
    # =ОКРУГЛ(Н1!M3+Н1!M4*0,5+Н2!M5*0,5;2)
    H21 = round(avr[0] + avr[1] * 0.5 + avr[2] * 0.5, 2) # H2 sheet C3 cell
    # Осуществление доступа к серверу поста управления
    # ОКРУГЛ(0,25*(Н1!M6+Н1!M7+Н1!M8+Н1!M9);2)
    H22 = round(0.25 * (avr[3] + avr[4] + avr[5] + avr[6]), 2) # H2 sheet C4 cell
    # Анализ состояния подходов к охраняемой зоне
    # =Н1!M10+Н1!M11
    H23 = round(avr[7] + avr[8], 2) # H2 sheet C5 cell
    # Анализ состояния инженерной защиты охраняемой зоны
    # =Н1!M12+Н1!M13+Н1!M14
    H24 = round(avr[9] + avr[10] + avr[11], 2) # H2 sheet C6 cell
    # Анализ состояния систем охранного мониторинга территории и акватории охраняемой зоны
    # =СУММ(Н1!M15:M19)
    H25 = round(sum(avr[12:17]), 2) # H2 sheet C7 cell
    # Блокирование информации устройств охранного мониторинга территории и акватории
    # Н1!M20+Н1!M21
    H26 = round(sum(avr[17:19]), 2) # H2 sheet C8 cell
    # Блокирование работы оборудования управления КФЗ
    # Н1!M22+Н1!M23
    H27 = round(sum(avr[19:21]), 2) # H2 sheet C9 cell
    # Блокирование информации АРМов ДЛ
    # Н1!M24+0,5*Н1!M25
    H28 = round(avr[21] + avr[22] * 0.5, 2) # H2 sheet C10 cell
    # Преодоление периметра территории и акватории охраняемой зоны
    # 0,2*(СУММ(Н1!M26:M30))
    H29 = round(0.2 * sum(avr[23:28]), 2) # H2 sheet C11 cell
    # Продвижение нарушителей внутри территории и акватории охраняемой зоны к цели
    # 0,33*(СУММ(Н1!M31:M35))
    H210 = round(0.33 * sum(avr[28:33]), 2) # H2 sheet C12 cell
    # Выполнение задания и уход нарушителей с территории и акватории охраняемой зоны
    # =ОКРУГЛ(Н1!M36+0,33*(СУММ(Н1!M37:M41));2)
    H211 = round(avr[33] + 0.33 * sum(avr[34:39]), 2) # H2 sheet C13 cell
    data_H2['Среднее значение времени реализации функций'] = 0
    tavr = [H21, H22, H23, H24, H25, H26, H27, H28, H29, H210, H211]
    data_H2['Среднее значение времени реализации функций'] = tavr
    data_H3 = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='Н3',index_col=0)
    data_H3.dropna(inplace=True)
    data_H3['Среднее значение времени реализации функций'] = 0
    H3 = []
    H3 = (sum(tavr[0:2]), round(sum(tavr[2:5]), 2), round(0.33 * sum(tavr[5:8]), 2), round(sum(tavr[8:11]), 2))
    data_H3['Среднее значение времени реализации функций'] = H3
    data31 = pd.read_excel(r'C:\Users\inven\Desktop\Jupyter_Notes\Reshenia_dlya_LST.xlsx', sheet_name='З1',header=[0, 1], index_col=0)
    # data31.columns[0][1]
    old = data31.columns[0][1]
    # data31.columns[11][1]
    old1 = data31.columns[11][1]
    old2 = data31.columns[12][1]
    data31.rename(columns={old: '', old1: '', old2: ''}, inplace=True)
    data31[['Среднее значение', 'Среднеквадратическое отклонение']] = 0
    data31['Среднее значение'] = data31['Данные экспертов относительно времени реализации функций'].mean(axis=1).round(1)
    data31['Среднеквадратическое отклонение'] = data31['Данные экспертов относительно времени реализации функций'].std(ddof=0, axis=1)


    pass
