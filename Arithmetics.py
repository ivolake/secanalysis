from __future__ import annotations

import numpy as np
from sympy import sympify, Symbol

class Calculator:
    def __init__(self):
        self.__variables: dict = {}
        pass

    def __repr__(self):
        return f'Calculator(variables={self.__variables})'

    @property
    def variables(self):
        return self.__variables

    def set_variable(self,
                     var: str,
                     val: int | float = None,
                     formulae: str = None):
        if val is None:
            val = self.__variables.get(var, {}).get('value', None)
        if formulae is None:
            formulae = self.__variables.get(var, {}).get('symbol', None)

        self.__variables.update({
            var: {
                'value': val,
                'formulae': formulae
            }
        })

    def get_variable(self,
                     var: str):
        variable = self.__variables.get(var, {})
        if variable == {}:
            print(f'Error: переменная {var} отсутствует в оперативной памяти')
        return variable

    def evaluate(self,
                 expression: str,
                 data: list | dict = None):
        if data is None:
            data = {}

        if expression == 'avg':
            return np.mean(data)
        elif expression == 'msd':
            avg = np.mean(data)
            return (sum([(x - avg) ** 2 for x in data]) / len(data)) ** 0.5
        elif expression == 'sum':
            return sum(data)
        elif expression == 'min':
            return min(data)
        elif expression == 'max':
            return max(data)
        elif expression == 'countd':
            return np.unique(data)
        else:
            formulae = sympify(expression)
            formulae_vars = {var.name: var for var in formulae.free_symbols}
            to_substitute = {}
            for var_name in formulae_vars:
                if var_name not in data:
                    value = self.get_variable(var_name).get('value', 0)
                    to_substitute.update({formulae_vars[var_name]: value})
                else:
                    to_substitute.update({formulae_vars[var_name]: data[var_name]})
            return float(formulae.evalf(subs=to_substitute))
