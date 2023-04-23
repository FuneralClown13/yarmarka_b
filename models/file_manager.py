import os
from PIL import Image
import sys
from random import choice
from flask import flash


class FileManager:
    PATH_TO_STATIC = '/home/funeralclown/yarmarka/static' if sys.platform == 'linux' else 'C:\\Users\\svr01\\PycharmProjects\\yarmarka\\static\\'

    def __init__(self, path: str):
        self.path_link = path
        self.path = path.lstrip("&").replace("&", "/").replace("&&", "/")
        self.path_back = '&'.join(self.path.split("/")[:-1])
        self.path_back = self.path_back if self.path_back else 'gallery'
        self.s_path = f'{FileManager.PATH_TO_STATIC}/{self.path}'

        self.name = str(self.path.split('/')[-1])
        try:
            self.dirs = sorted(list(os.walk(self.s_path))[0][1])
            self.img = self.__filter_files(list(os.walk(self.s_path))[0][2])
        except IndexError:
            self.dirs = []
            self.img = []
        self.catalog = self.__create_catalog()
        self.catalog_list = list(self.catalog.keys())
        self.inf = {
            'name': self.name,
            'path': f'{self.path.replace("/", "&")}'
        }

    def add_img(self, files: list, resize=True) -> None:
        """
        add_img сохраняет фотографии
        :param files: list[file]
        :param resize: сжать фото (default True)
        """
        if isinstance(files, list):
            for file in files:
                try:
                    if file.filename:
                        path_to_img = f'{self.s_path}/{file.filename.lower()}'
                        with open(path_to_img, 'wb') as img:
                            img.write(file.read())
                        if resize:
                            with Image.open(path_to_img) as img:
                                img.load()
                                size = img.width if img.width > img.height else img.height
                                proportion = size / 1000
                                proportion = proportion if proportion > 1 else 1
                                img = img.resize((round(img.width / proportion),
                                                  round(img.height / proportion)))
                                img.save(path_to_img)
                except:
                    flash(f'Файл {file.filename} сохранить не удалось')

    def create_dir(self, name):
        """
        create_dir создает директорию

        :param name: имя директории
        """
        try:
            i = 1
            while name in self.dirs:
                name = f'{name} Copy ({i})'
                i += 1
            os.mkdir(f'{self.s_path}/{name}')
        except FileNotFoundError:
            flash(f'No such file or directory')

    def del_dir(self):
        """
        del_dir удаляет директорию
        """
        try:
            if not self.img:
                os.rmdir(f'{self.s_path}')
            self.inf['path'] = '&'.join(self.inf['path'].split('&')[:-1])
        except FileNotFoundError:
            flash(f'No such file or directory')

    def del_img(self, name):
        """
        del_img удаляет файл

        :param name: имя удаляемого файла
        """
        try:
            os.remove(f'{self.s_path}/{name}')
        except FileNotFoundError:
            flash(f'No such file or directory')

    def __create_catalog(self) -> dict:
        """
        __create_catalog создает каталог дочерних директорий

        ### ### ###

        path -- путь к дочерней директории

        preview -- превью

        preview_link -- путь к превью

        count -- количество файлов в дочерней директории
        """
        catalog = {}
        for dir_child in self.dirs:
            catalog[dir_child] = {'path': f'{self.path.replace("/", "&")}&{dir_child}',
                                  'preview': self.__get_preview(dir_child),
                                  'preview_link': f'{self.path}/{dir_child}',
                                  'count': self.__get_count_files(dir_child)}
        return catalog

    @staticmethod
    def __filter_files(files: list) -> list:
        """
        __filter_files фильтрует список файлов, возвращая файлы подходящего формата
        :param files: список файлов для фильтра
        """
        formats = {'jpg', 'jpeg', 'png', 'webp', 'arw'}
        return [f for f in files if f.split('.')[-1] in formats]

    def __get_preview(self, name: str) -> str:
        """
        __get_preview случайно выбирает файл в дочерней директории и возвращает его как превью
        :param name: имя дочерней директории
        """
        for_choice = self.__filter_files(list(os.walk(f'{self.s_path}/{name}'))[0][2])
        preview = choice(for_choice) if for_choice else ''
        return preview

    def __get_count_files(self, name: str) -> int:
        """
        __get_count_files возвращает количество файлов в дочерней директории
        :param name: имя дочерней директории
        """
        return len(list(os.walk(f'{self.s_path}/{name}'))[0][2])

