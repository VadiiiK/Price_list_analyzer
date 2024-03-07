## python version 3.6
import os
import numpy as np
import pandas as pd


# путь папки с файлами, где лежат прайсы
PATH_FOLDER_PRICE = "price"


class PriceMachine:

    def __init__(self, path_folder):
        self.path_folder = path_folder
        self.df = None
        self.data = None
        # self.result = ''
        # self.name_length = 0

    def load_prices(self):
        """
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        """
        # для OS WINDOWS меняем '\' на '/'
        path_new = self.path_folder.replace(os.sep, '/')
        for root, dirs, files in os.walk(path_new):
            for file in files:
                if file[0:5] == 'price':
                    new_paths_file = self.path_folder + '/' + file
                    self.data = pd.read_csv(new_paths_file)

                    for index in self.data.columns:
                        if index == "название" or index == "продукт" or index == "товар" or index == "наименование":
                            self.data = self.data.rename(columns={index: 'Наименование'})
                        elif index == "цена" or index == "розница":
                            self.data = self.data.rename(columns={index: 'цена'})
                        elif index == "фасовка" or index == "масса" or index == "вес":
                            self.data = self.data.rename(columns={index: 'вес'})
                        else:
                            del self.data[index]

                    self.data['файл'] = file
                    self.data['цена за кг.'] = round(self.data['цена'] / self.data['вес'], 1)
                    self.df = pd.concat([self.df, self.data], axis=0, ignore_index=True)
                    self.df['Наименование'] = self.df.Наименование.str.lower()
                    self.df = self.df.sort_values('цена за кг.', ascending=True)
                    self.df.index = np.arange(1, len(self.df) + 1)
        PriceMachine.find_text(self, self.df)
        PriceMachine._search_product_price_weight(self, self.df)
        return self.df

    def _search_product_price_weight(self, df):
        """
            Возвращает номера столбцов
        """
        while True:
            fragment_name = input("Введите наименование товара: ")
            if fragment_name == 'exit':
                print('Работа закончена')
                break
            elif fragment_name == '':
                self.df_enter = self.df[self.df['Наименование'].str.contains('')]
                print(self.df_enter)
                PriceMachine.find_text(self, self.df_enter)
            else:
                self.df_contains = self.df[self.df['Наименование'].str.contains(fragment_name)]
                self.df_contains = self.df_contains.sort_values('цена за кг.', ascending=True)
                self.df_contains.index = np.arange(1, len(self.df_contains) + 1)
                print(self.df_contains)
                PriceMachine.find_text(self, self.df_contains)

    def export_to_html(self, fname='output.html'):
        html = self.df.to_html()
        with open(fname, "w", encoding="cp1251") as file:
            file.write(html)
        return self.df

    def find_text(self, text):
        """
        Выводит полученный результат
        """
        print('-' * 100)
        list_of_items = [t for t in text['Наименование']]
        print(list_of_items)
        print('-' * 100)


pm = PriceMachine(PATH_FOLDER_PRICE)
print(pm.load_prices())
print('the end')
print(pm.export_to_html())

