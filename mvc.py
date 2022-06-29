import tkinter as tk
from tkinter import *

from typing import *
from decimal import Decimal
import hashlib
import copy


class Event:
    def __init__(self, subscribers: List[Callable] = None):
        self._subscribers: List[Callable] = []
        if subscribers is not None and type(subscribers) is list:
            self._subscribers.extend(subscribers)

    def extend(self, subscribers: List[Callable]):
        self._subscribers.extend(subscribers)

    def __call__(self, **kwargs):
        for subscriber in self._subscribers:
            subscriber(**kwargs)


class View:
    def __init__(self):
        self._windows = dict()
        self._events = {'login_button_click': Event(),
                        'add_button_click': Event(),
                        'edit_button_click': Event(),
                        'delete_button_click': Event(),
                        'confirm_add_button_click': Event(),
                        'confirm_edit_button_click': Event(),
                        'exit_button_click': Event()}
        self._entries = dict()

    def subscribe(self, subscribers: Dict[str, List[Callable]]):
        for key in self._events.keys():
            if key in subscribers.keys():
                self._events[key].extend(subscribers[key])

    def start_login_window(self):
        self._windows.update({'login_window': tk.Tk()})
        login_window = self._windows['login_window']
        login_window.title('Вхід в систему')
        login_window.geometry('400x200')

        column_sizes = [50, 100, 100, 50]
        row_sizes = [60, 40, 60, 70]
        for i in range(len(column_sizes)):
            login_window.columnconfigure(index=i, minsize=column_sizes[i])
        for i in range(len(column_sizes)):
            login_window.rowconfigure(index=i, minsize=row_sizes[i])

        Label(login_window, text='Ім\'я користувача:'
              ).grid(row=0, column=1, sticky='se')
        self._entries['nickname_e'] = Entry(login_window, width=30)
        self._entries['nickname_e'].grid(row=0, column=2, sticky='sw')

        Label(login_window, text='Пароль:').grid(row=1, column=1, sticky='e')
        self._entries['password_e'] = Entry(login_window, show="*", width=30)
        self._entries['password_e'].grid(row=1, column=2, sticky='w')

        Button(login_window, text='Увійти', width=10, height=1,
               command=self._events['login_button_click']
               ).grid(row=2, column=1, columnspan=2)

        self._windows['login_window'].mainloop()

    def start_main_window(self):
        main_font = ('Arial', 11)
        self._windows.update({'main_window': tk.Tk()})
        self._windows['main_window'].title('Головне вікно')
        self._windows['main_window'].geometry('740x400')

        left_frame = Frame(self._windows['main_window'], name='left_frame')
        left_frame.grid(row=0, column=0, sticky='n')

        # columns of the table
        col_styles = {'master': left_frame, 'height': 200}
        Frame(name='id_col', **col_styles)
        Frame(name='name_col', **col_styles)
        Frame(name='quantity_col', **col_styles)
        Frame(name='unit_price_col', **col_styles)
        Frame(name='price_col', **col_styles)
        Frame(name='producer_col', **col_styles)

        for i, key in enumerate(left_frame.children):
            left_frame.children[key].grid(row=0, column=i, sticky='n')

        lb_styles = {'bg': 'light grey', 'font': 'main_font',
                     'borderwidth': 1, 'relief': 'solid'}
        Label(left_frame.children['id_col'], name='id_label',
              text='ID', width=3, **lb_styles).grid(row=0, column=0)
        Label(left_frame.children['name_col'], name='name_label',
              text='Назва', width=7, **lb_styles).grid(row=0, column=0)
        Label(left_frame.children['quantity_col'], name='quantity_label',
              text='Кількість', width=11, **lb_styles).grid(row=0, column=0)
        Label(left_frame.children['unit_price_col'], name='unit_price_label',
              text='Ціна за шт.', width=13, **lb_styles).grid(row=0, column=0)
        Label(left_frame.children['price_col'], name='price_label',
              text='Ціна', width=6, **lb_styles).grid(row=0, column=0)
        Label(left_frame.children['producer_col'], name='producer_label',
              text='Виробник', width=10, **lb_styles).grid(row=0, column=0)

        right_frame = Frame(self._windows['main_window'], name='right_frame')
        right_frame.grid(row=0, column=1, padx=(15, 0), sticky='ne')

        Label(right_frame, text='ID:'
              ).grid(row=0, column=0, padx=(10, 0), pady=7)

        Entry(right_frame, name='selected_id_entry', width=10
              ).grid(row=0, column=1, padx=(0, 10), pady=7)
        Button(right_frame, text='Додати', width=10, font=main_font,
               command=self._events['add_button_click']
               ).grid(row=1, column=0, columnspan=2, padx=10, pady=7)
        Button(right_frame, text='Редагувати', width=10, font=main_font,
               command=self._events['edit_button_click']
               ).grid(row=2, column=0, columnspan=2, padx=10, pady=7)
        Button(right_frame, text='Видалити', width=10, font=main_font,
               command=self._events['delete_button_click']
               ).grid(row=3, column=0, columnspan=2, padx=10, pady=7)
        Button(right_frame, text='Вийти', width=10, font=main_font,
               command=self._events['exit_button_click']
               ).grid(row=4, column=0, columnspan=2, padx=10, pady=7)

        self._windows['main_window'].mainloop()

    def start_add_window(self, default_values: Dict = None):
        self._windows.update({'add_window': tk.Tk()})
        self._windows['add_window'].title('Добавити продукт')

        frame = Frame(self._windows['add_window'], name='frame')
        frame.grid(row=1, column=1)

        Label(frame, text='Назва*'
              ).grid(row=0, column=0, pady=5, sticky='w')
        Entry(frame, name='name_entry'
              ).grid(row=0, column=1, pady=5, sticky='w')

        Label(frame, text='Кількість*'
              ).grid(row=1, column=0, pady=5, sticky='w')
        Entry(frame, name='quantity_entry'
              ).grid(row=1, column=1, pady=5, sticky='w')

        Label(frame, text='Виробник'
              ).grid(row=2, column=0, pady=5, sticky='w')
        Entry(frame, name='producer_entry'
              ).grid(row=2, column=1, pady=5, sticky='w')

        Label(frame, text='Ціна*'
              ).grid(row=3, column=0, pady=5, sticky='w')
        Label(frame, text='за одиницю'
              ).grid(row=4, column=0, pady=5, sticky='w')
        Entry(frame, name='unit_price_entry'
              ).grid(row=4, column=1, pady=5, sticky='w')
        Label(frame, text='або загалом'
              ).grid(row=5, column=0, pady=5, sticky='w')
        Entry(frame, name='price_entry'
              ).grid(row=5, column=1, pady=5, sticky='w')
        Button(frame, text=('Редагувати'
                            if default_values is not None
                            else 'Додати'),
               command=(self._events['confirm_edit_button_click']
                        if default_values is not None
                        else self._events['confirm_add_button_click'])
               ).grid(row=6, column=0, columnspan=2, pady=10, sticky='s')

        if default_values is not None:
            frame.children['name_entry'].insert(
                0, default_values['name'])
            frame.children['quantity_entry'].insert(
                0, default_values['quantity'])
            frame.children['producer_entry'].insert(
                0, default_values['producer'])
            frame.children['unit_price_entry'].insert(
                0, default_values['unit_price'])
            frame.children['price_entry'].insert(
                0, default_values['price'])
        self._windows['add_window'].mainloop()

    def extract_login_inputs(self) -> Tuple[str, str]:
        return self._entries['nickname_e'].get(), \
               self._entries['password_e'].get()

    def close_all_windows(self):
        for key in self._windows.keys():
            self._windows[key].destroy()
        self._entries.clear()

    def close_window(self, window_name: str):
        self._windows[window_name].destroy()

    def extract_add_window_inputs(self) -> Dict:
        return_values = dict()
        keys = ['name_entry', 'price_entry', 'unit_price_entry',
                'producer_entry', 'quantity_entry']
        for key in keys:
            return_values[key] = self._windows['add_window'
            ].children['frame'].children[key].get()
        return return_values

    def refresh_table(self, table: Dict):
        columns = self._windows['main_window'
        ].children['left_frame'].children
        column_names = ['name_col', 'quantity_col', 'unit_price_col',
                        'price_col', 'producer_col']
        column_entities = ['name', 'quantity', 'unit_price',
                           'price', 'producer']

        # emptying rows from old values
        for key in columns.keys():
            for label_name in [key for key in columns[key].children.keys()
                               if key not in
                                  map((lambda x: x + '_label'),
                                      column_entities + ['id'])]:
                columns[key].children[label_name].destroy()

        if table == dict(): return

        # filling columns in main_window
        for id in sorted(table.keys(), reverse=False):
            Label(columns['id_col'], text=id,
                  name=f'id{id}').grid(row=id, column=0)
            for column_name, column_entity in \
                    zip(column_names, column_entities):
                Label(columns[column_name], text=table[id][column_entity],
                      name=f'{column_entity}{id}').grid(row=id, column=0)

    def get_selected_id(self) -> int:
        return_value = self._windows['main_window'
        ].children['right_frame'].children['selected_id_entry'].get()
        if return_value == '':
            return 0
        return int(return_value)

    def get_selected_row_values(self) -> Dict:
        keys = ['id', 'name', 'quantity', 'price', 'unit_price', 'producer']
        return {key: self._windows['main_window'
        ].children['left_frame'].children[f'{key}_col'
        ].children[key + str(self.get_selected_id())
                   ].cget('text') for key in keys}


class Model:
    @staticmethod
    def _normalize_row(kwargs):
        kwargs['quantity'] = int(kwargs['quantity'])
        if kwargs['price'] != '':
            kwargs['price'] = Decimal(kwargs['price'])
            kwargs['unit_price'] = Decimal(kwargs['price']
                                           / kwargs['quantity'])
        elif kwargs['unit_price'] != '':
            kwargs['unit_price'] = Decimal(kwargs['unit_price'])
            kwargs['price'] = Decimal(kwargs['quantity'
                                      ] * kwargs['unit_price'])
        return kwargs

    def __init__(self):
        self._db = dict()
        # passwords are saved as MD5 hash
        self._users = {1: {'name': 'admin',
                           'password': '63a9f0ea7bb98050796b649e85481845'},
                       2: {'name': 'user2',
                           'password': '7e58d63b60197ceb55a1c487989a3720'}}
        self._id_counter = 0

    def is_in_database(self, nickname, password) -> bool:
        for key in self._users.keys():
            if nickname == self._users[key]['name']:
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                if hashed_password == self._users[key]['password']:
                    return True
        return False

    def add(self, **kwargs):
        if kwargs['name'] != '' and kwargs['quantity'] != '':
            kwargs = self._normalize_row(kwargs)

            self._id_counter += 1
            self._db.update({self._id_counter: kwargs})

    def edit(self, **kwargs):
        if kwargs['name'] != '' and kwargs['quantity'] != '':
            kwargs = self._normalize_row(kwargs)

            self._db[kwargs['id']] = {key: kwargs[key]
                                      for key in kwargs.keys() if key != 'id'}

    def delete(self, id: int):
        if len(self._db) > 1:
            for i in range(id + 1, len(self._db) + 1):
                self._db[i - 1] = self._db[i]
            self._db.pop(len(self._db))
            self._id_counter -= 1
        elif len(self._db) == 1:
            self._db.pop(1)
            self._id_counter -= 1

    def get_table(self) -> Dict:
        return copy.deepcopy(self._db)

    def get_row(self, id: int) -> Dict:
        if type(id) == int and id > 0:
            return copy.deepcopy(self._db[id])


class Controller:
    def __init__(self, view: View = None, model: Model = None):
        self._view = view
        self._model = model
        self._view.subscribe({
            'login_button_click': [self._on_login_button_click],
            'add_button_click': [self._on_add_button_click],
            'edit_button_click': [self._on_edit_button_click],
            'delete_button_click': [self._on_delete_button_click],
            'confirm_add_button_click': [self._on_confirm_add_button_click],
            'confirm_edit_button_click': [self._on_confirm_edit_button_click],
            'exit_button_click': [self._on_exit_button_click]
        })

    def start(self):
        self._view.start_login_window()

    def _on_login_button_click(self):
        input_nickname, input_password = self._view.extract_login_inputs()
        if self._model.is_in_database(nickname=input_nickname,
                                      password=input_password):
            self._view.close_all_windows()
            self._view.start_main_window()
            self._view.refresh_table(self._model.get_table())

    def _on_add_button_click(self):
        self._view.start_add_window()

    def _on_confirm_add_button_click(self):
        extracted_inputs = self._view.extract_add_window_inputs()
        temp = {key[:-len('_entry')]: extracted_inputs[key]
                for key in extracted_inputs.keys()}
        self._model.add(**temp)
        self._view.close_window('add_window')

        self._view.refresh_table(self._model.get_table())

    def _on_edit_button_click(self):
        if self._view.get_selected_id() == 0: return
        try:
            self._model.get_row(self._view.get_selected_id())
        except:
            return
        selected_row_values = self._view.get_selected_row_values()
        self._view.start_add_window(
            default_values={key: selected_row_values[key]
                            for key in selected_row_values.keys()
                            if key != 'id'})

    def _on_confirm_edit_button_click(self):
        extracted_inputs = self._view.extract_add_window_inputs()
        temp = {key[:len(key) - len('_entry')]: extracted_inputs[key]
                for key in extracted_inputs.keys()}
        self._model.edit(id=self._view.get_selected_id(), **temp)
        self._view.close_window('add_window')

        self._view.refresh_table(self._model.get_table())

    def _on_delete_button_click(self):
        self._model.delete(self._view.get_selected_id())
        self._view.refresh_table(self._model.get_table())

    def _on_exit_button_click(self):
        self._view.start_login_window()
        self._view.close_window('main_window')


class Main:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(view=self.view, model=self.model)
        self.controller.start()


if __name__ == "__main__":
    Main()
