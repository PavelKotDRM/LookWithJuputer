from IPython.display import clear_output
from IPython.display import display
import ipywidgets as widgets
import pandas as pd
import polars as pol


class DataOut():
    """"Класс для просмотра DataFrame елементов по 10 за раз
    """
    def __init__(self, data_set: pd.DataFrame | pol.DataFrame, id_start=0, line_range=(0, 10), lib_work: str ="pandas") -> None:
        """Инициализация класса

        Args:
            data_set (pd.DataFrame or pol.DataFrame): Просматриваемый DataFrame
            id_start (int, optional): С какого индекса начинаем. Defaults to 0.
            line_range (tuple, optional): С какого по какой индес смотрим. Defaults to (0, 10).
            lib_work (str, optional)
        """
        self.data_set = data_set
        self.id_start = id_start
        self.line_range = line_range
        self.lib = lib_work
        self.columns = []
        self.to_display = None
        match lib_work:
            case "pandas":
                self.columns = data_set.columns.to_list()
                self.to_display = display(self.data_set[self.columns].iloc[self.id_start+self.line_range[0]:self.id_start+self.line_range[1]],display_id=True)
            case "polars":
                self.columns = data_set.columns
                self.to_display = display(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]],display_id=True)
            case _:
                self.columns = data_set.columns
                self.to_display = display(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]],display_id=True)

    def on_range_change(self, data: dict):
        """Метод реагирующий на изменение длинны выводимого дата фрейма

        Args:
            data (_type_): Получаемые данные от события ipywidgets
        """
        self.line_range = data['new']
        match self.lib:
            case "pandas":
                self.to_display.update(self.data_set[self.columns].iloc[self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])
            case "polars":
                self.to_display.update(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])
            case _:
                self.to_display.update(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])

    def on_value_change(self, data: dict) -> None:
        """Метод на изменение индекса начала просматриваниия

        Args:
            data (dict): Получаемые данные от события ipywidgets
        """
        self.id_start = data['new']
        match self.lib:
            case "pandas":
                self.to_display.update(self.data_set[self.columns].iloc[self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])
            case "polars":
                self.to_display.update(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])
            case _:
                self.to_display.update(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])

    def on_change_tag(self, data: dict) -> None:
        """Метод реакции на изменение выводимых колонок

        Args:
            data (dict): Получаемы данные от события ipywidgets
        """
        self.columns = data['new']
        match self.lib:
            case "pandas":
                self.to_display.update(self.data_set[self.columns].iloc[self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])
            case "polars":
                self.to_display.update(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])
            case _:
                self.to_display.update(self.data_set[self.columns][self.id_start+self.line_range[0]:self.id_start+self.line_range[1]])

class DataShow():
    """Класс для отображения DataFrame в Jupyter
    """
    def __init__(self) -> None:
        self.display = None
        self.tab = None
        self.slider_database = None
        self.slider_range_index = None
        self.tags_colum = None

    def show_tablet(self, data_set: pd.DataFrame | pol.DataFrame, id_start=0, line_range=(0, 10), lib_work:str="pandas") -> None:
        if self.display:
            clear_output()
            self.display = None
        self.tab = widgets.Tab()
        self.slider_database = widgets.IntSlider(min=0, max=len(data_set)-1, step=10, description='Индекс: ')
        self.slider_range_index = widgets.IntRangeSlider(value=line_range, min=0, max=10, step=1, description='С .. по ..')
        match lib_work:
                case "pandas":
                    self.tags_colum = widgets.TagsInput(value=data_set.columns.tolist(), allowed_tags=data_set.columns.tolist())
                case "polars":
                    self.tags_colum = widgets.TagsInput(value=data_set.columns, allowed_tags=data_set.columns)
                case _:
                    self.tags_colum = widgets.TagsInput(value=data_set.columns, allowed_tags=data_set.columns)
        self.tab.children = [self.slider_database, self.slider_range_index, self.tags_colum]
        self.tab.titles = ['Индексы', 'Диапазон', 'Колонки']
        self.display = display(self.tab, display_id=True, clear=True)
        change_pd_out = DataOut(data_set, id_start=id_start, line_range=line_range, lib_work=lib_work)
        self.slider_range_index.observe(change_pd_out.on_range_change, names='value')
        self.slider_database.observe(change_pd_out.on_value_change, names='value')
        self.tags_colum.observe(change_pd_out.on_change_tag, names='value')