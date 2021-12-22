# from typing import Iterable

import pandas as pd
import numpy as np

from Arithmetics import Calculator
from functions import get_yaml


# TODO: Возможно, стоит изменить концепцию классов
#  Step1Processor -> InputDataProcessor
#  Step2Processor -> CalculatingDataProcessor

class InputDataProcessor:
    def __init__(self,
                 data_path: str,
                 calculator: Calculator,
                 sheet_name: str = None,
                 validate_data: bool = False,
                 config_path: str = None,
                 config: dict = None,
                 **kwargs):
        self.data_path = data_path
        self.validate_dataframe_flag = validate_data
        self.config_path = config_path
        self.config = config
        self.__calculator = calculator

        self.sheet_name = sheet_name

        val_params = kwargs.get('validation_params', {})
        self.__validate_data_shape_flag = val_params.get('validate_data_shape', False)
        self.__validate_rows_flag = val_params.get('validate_rows', False)
        self.__validate_expert_assessment_caption_flag = val_params.get('validate_expert_assessments_caption', False)
        # self.__validate_aggregation_functions_captions_flag = val_params.get('validate_aggregation_functions_captions', False)

        if not self.validate_dataframe_flag and any([self.__validate_data_shape_flag,
                                                     self.__validate_rows_flag,
                                                     self.__validate_expert_assessment_caption_flag,]):
                                                     # self.__validate_aggregation_functions_captions_flag]):
            print('Error. Нельзя одновременно не указывать флаг валидации и указывать какие-либо параметры валидации.')
        elif self.validate_dataframe_flag and not any([self.__validate_data_shape_flag,
                                                       self.__validate_rows_flag,
                                                       self.__validate_expert_assessment_caption_flag,]):
                                                       # self.__validate_aggregation_functions_captions_flag]):
            print('Error. Нельзя одновременно указывать флаг валидации и не указывать какие-либо параметры валидации.')

        if self.validate_dataframe_flag and self.config_path is None and self.config is None:
            print('Error. Для валидации необходимо указать конфигурацию файла данных или путь до файла с конфигурацией.')
        elif self.validate_dataframe_flag and self.config_path is not None and self.config is not None:
            print('Error. Нельзя одновременно указывать и конфигурацию, и путь до файла с конфигурацией.')
        # elif self.config is None and self.config_path is None:
        #     print('Error: Нельзя одновременно не указывать и конфигурацию, и путь до файла с конфигурацией.')
        elif self.validate_dataframe_flag and self.config is None and self.config_path is not None:
            self.config = get_yaml(self.config_path)


        self.dataframe: pd.DataFrame = None


    def __repr__(self):
        return f'InputDataProcessor(data_path={self.data_path}, config_path={self.config_path})'

    @property
    def calculator(self):
        return self.__calculator

    def read_dataframe(self):
        dataframe_type = self.data_path[self.data_path.rfind('.'):]
        if dataframe_type in ['.xls', '.xlsx']:
            if self.sheet_name:
                self.dataframe = pd.read_excel(self.data_path,
                                               sheet_name=self.sheet_name,
                                               header=[0, 1],
                                               index_col=[0, 1])
            else:
                self.dataframe = pd.read_excel(self.data_path,
                                               header=[0, 1],
                                               index_col=[0, 1])
            return True
        elif dataframe_type in ['.csv']:
            self.dataframe = pd.read_csv()
            return True
        else:
            print(f'Error. Тип файла данных неизвестен: {dataframe_type}')
            return False


    def __validate_data_shape(self) -> bool:
        data_shape = self.dataframe.to_numpy().shape

        cols = list(np.arange(1, self.config['expert_assessments_num'] + 1, 1))
        config_data_shape = (len(self.config['rows']), len(cols))

        res = data_shape == config_data_shape

        if res:
            print('Info. Размерность данных соответствует конфигурации')
        else:
            print(f'Error. Размерность данных ({data_shape}) не соответствует конфигурации ({config_data_shape})')

        return res

    def __validate_rows(self) -> bool:
        data_rows = np.stack(self.dataframe.index.to_numpy())[:, 1]
        config_rows = list(self.config['rows'].keys())
        # noinspection PyTypeChecker
        rows_validation = dict(zip(data_rows,
                                   data_rows == config_rows))

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

    # def __validate_aggregation_functions_captions(self) -> bool:
    #     data_aggregation_functions_captions = np.unique(np.stack(self.dataframe.columns.to_numpy())[:, 0])[1:]
    #
    #     # noinspection PyTypeChecker
    #     funcs_validation = dict(zip(data_aggregation_functions_captions,
    #                                 data_aggregation_functions_captions == self.config['aggregation_functions_captions']))
    #
    #     res = min(funcs_validation.values())
    #
    #     if res:
    #         print('Info. Список функций агрегации соответствует конфигурации')
    #     else:
    #         error_names = '", "'.join(dict(filter(lambda x: not x[1], funcs_validation.items())).keys())
    #         print(f'Error. Список функций агрегации ("{error_names}") не соответствует конфигурации')
    #
    #     return res

    def __validate_dataframe(self) -> bool:
        validations = []
        if self.__validate_data_shape_flag:
            validations.append(self.__validate_data_shape())
        if self.__validate_rows_flag:
            validations.append(self.__validate_rows())
        if self.__validate_expert_assessment_caption_flag:
            validations.append(self.__validate_expert_assessment_caption())
        # if self.__validate_aggregation_functions_captions_flag:
        #     validations.append(self.__validate_aggregation_functions_captions())

        return any(validations)

    def calculate_aggregations(self):
        # sum, avg, max, min, countd - возможные функции агрегации
        for func_i, func_name in enumerate(self.config['aggregation_functions_captions']):
            vals = pd.Series(index=self.dataframe.index, name=(func_name, ''))
            for i in range(self.dataframe.shape[0]):
                row_name = self.dataframe.iloc[i].name[1]
                expert_assessments = self.dataframe.iloc[i].to_list()
                variable = self.config['rows'][row_name][f'variable{func_i+1}']
                formulae = self.config['rows'][row_name][f'formulae{func_i+1}']
                value = self.calculator.evaluate(formulae,
                                                 data=expert_assessments)
                vals[self.dataframe.iloc[i].name] = value
                self.calculator.set_variable(variable,
                                             val=value)
            self.dataframe[(func_name, '')] = vals

    def finalize_dataframe(self):

        self.calculate_aggregations()

        # Очищение от некрасивых надписей под ячейками с названиями функций агрегации (типа 'Unnamed: 12_level_1')
        # ---
        cols = self.dataframe.columns.to_numpy()
        for i in range(self.config['expert_assessments_num'],
                       self.config['expert_assessments_num'] + len(self.config['aggregation_functions_captions'])):
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


class CalculatingDataProcessor:
    def __init__(self,
                 calculator: Calculator,
                 config_path: str = None,
                 config: dict = None):
        self.config = config
        self.config_path = config_path
        self.__calculator = calculator

        if self.config_path is None and self.config is None:
            print('Error. Необходимо указать конфигурацию файла данных или путь до файла с конфигурацией.')
        elif self.config_path is not None and self.config is not None:
            print('Error. Нельзя одновременно указывать и конфигурацию, и путь до файла с конфигурацией.')
        # elif self.config is None and self.config_path is None:
        #     print('Error: Нельзя одновременно не указывать и конфигурацию, и путь до файла с конфигурацией.')
        elif self.config is None and self.config_path is not None:
            self.config = get_yaml(self.config_path)

        self.dataframe = None

    def __repr__(self):
        return f'CalculatingDataProcessor(config_path={self.config_path})'

    @property
    def calculator(self):
        return self.__calculator


    def create_dataframe(self):
        cols = self.config['aggregation_functions_captions']
        rows = self.config['rows']
        data_shape = (len(rows), len(cols))
        self.dataframe = pd.DataFrame(np.zeros(data_shape),
                                      index=pd.MultiIndex.from_tuples(zip(range(1,
                                                                                len(rows) + 1),
                                                                          rows)),
                                      columns=cols)

    def calculate_aggregations(self):
        for func_i, func_name in enumerate(self.config['aggregation_functions_captions']):
            vals = pd.Series(index=self.dataframe.index, name=func_name)
            for i in range(self.dataframe.shape[0]):
                row_name = self.dataframe.iloc[i].name[1]
                variable = self.config['rows'][row_name][f'variable{func_i+1}']
                formulae = self.config['rows'][row_name][f'formulae{func_i+1}']
                value = self.calculator.evaluate(formulae)
                # print(f'{formulae} = {value}')
                vals[self.dataframe.iloc[i].name] = value
                self.calculator.set_variable(variable,
                                             val=value,
                                             formulae=formulae)
            self.dataframe[func_name] = vals


    def return_dataframe(self):
        self.create_dataframe()
        self.calculate_aggregations()
        return self.dataframe
