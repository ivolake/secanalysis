import os
import pandas as pd



class Step2:
    def __init__(self, step1_df):
        self.step1_df = step1_df

    def func1(self):
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
        H21 = round(avr[0] + avr[1] * 0.5 + avr[2] * 0.5, 2)
        # Осуществление доступа к серверу поста управления
        # ОКРУГЛ(0,25*(Н1!M6+Н1!M7+Н1!M8+Н1!M9);2)
        H22 = round(0.25 * (avr[3] + avr[4] + avr[5] + avr[6]), 2)
        # Анализ состояния подходов к охраняемой зоне
        # =Н1!M10+Н1!M11
        H23 = round(avr[7] + avr[8], 2)
        # Анализ состояния инженерной защиты охраняемой зоны
        # =Н1!M12+Н1!M13+Н1!M14
        H24 = round(avr[9] + avr[10] + avr[11], 2)
        # Анализ состояния систем охранного мониторинга территории и акватории охраняемой зоны
        # =СУММ(Н1!M15:M19)
        H25 = round(sum(avr[12:17]), 2)
        # Блокирование информации устройств охранного мониторинга территории и акватории
        # Н1!M20+Н1!M21
        H26 = round(sum(avr[17:19]), 2)
        # Блокирование работы оборудования управления КФЗ
        # Н1!M22+Н1!M23
        H27 = round(sum(avr[19:21]), 2)
        # Блокирование информации АРМов ДЛ
        # Н1!M24+0,5*Н1!M25
        H28 = round(avr[21] + avr[22] * 0.5, 2)
        # Преодоление периметра территории и акватории охраняемой зоны
        # 0,2*(СУММ(Н1!M26:M30))
        H29 = round(0.2 * sum(avr[23:28]), 2)
        # Продвижение нарушителей внутри территории и акватории охраняемой зоны к цели
        # 0,33*(СУММ(Н1!M31:M35))
        H210 = round(0.33 * sum(avr[28:33]), 2)
        # Выполнение задания и уход нарушителей с территории и акватории охраняемой зоны
        # =ОКРУГЛ(Н1!M36+0,33*(СУММ(Н1!M37:M41));2)
        H211 = round(avr[33] + 0.33 * sum(avr[34:39]), 2)
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
        data31.columns[0][1]
        old = data31.columns[0][1]
        data31.columns[11][1]
        old1 = data31.columns[11][1]
        old2 = data31.columns[12][1]
        data31.rename(columns={old: '', old1: '', old2: ''}, inplace=True)
        data31[['Среднее значение', 'Среднеквадратическое отклонение']] = 0
        data31['Среднее значение'] = data31['Данные экспертов относительно времени реализации функций'].mean(axis=1).round(1)
        data31['Среднеквадратическое отклонение'] = data31['Данные экспертов относительно времени реализации функций'].std(ddof=0, axis=1)


        pass

    def get_result(self):
        df = ...
        return df