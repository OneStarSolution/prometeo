import os
from math import ceil
from concurrent.futures import ProcessPoolExecutor

import pandas as pd


class FileUtils:

    ALLOWED_EXTENSIONS = ['csv', 'xls', 'xlsx']

    @staticmethod
    def read_parallel(paths, workers=4, concat=True, **read_options):
        """ Concat the dataframes using multiple proccess """

        dim = ceil(len(paths) / workers)
        chunks = (paths[k: k + dim] for k in range(0, len(paths), dim))
        temp = []

        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    FileUtils.read_chunk, chunk, **read_options) for chunk in chunks
            ]

        for future in futures:
            temp.append(future.result())

        if concat:
            temp = pd.concat(temp)

        return temp

    @staticmethod
    def read_chunk(paths, concat=False, **read_options):
        dfs = []
        for path in paths:
            data = FileUtils.read_single_file(path, **read_options)

            dfs.append(data)

        if concat:
            dfs = pd.concat(dfs, sort=False, ignore_index=True)

        return dfs

    @staticmethod
    def read_single_file(path, **read_options):
        """ Read the DF in input paths and concatenate it. """
        data = None

        try:
            file_name = path.split('/')[-1]
            extension = file_name.split('.')[-1]

            if extension in FileUtils.ALLOWED_EXTENSIONS:
                if extension == "xlsx" or extension == 'xls':
                    data = pd.read_excel(path, **read_options)
                if extension == "csv":
                    data = pd.read_csv(path, **read_options)
            else:
                print(
                    f'The extension: {extension} in {file_name} is not allowed')

        except Exception:
            print(f"File {file_name} could not be read")

        return data

    @staticmethod
    def get_files_in_folder(folder_path, include_path=True, extensions=[]):
        """Return a list of file paths in the current folder
        Arguments:
            folder_path {str} -- Directory path in where the files are.
        Keyword Arguments:
            include_path {bool} -- Returns the filepath (default: {True})
            extensions {list} -- Specify the file extensions (default: {[]})
        """
        files = os.listdir(folder_path)

        if extensions:
            files_with_extensions = set()
            for extension in extensions:
                for file_name in files:
                    # Skip opened files
                    if '~$' in file_name:
                        continue
                    if extension.lower() in file_name.lower():
                        files_with_extensions.add(file_name)
            files = files_with_extensions

        if include_path:
            files = [f'{folder_path}/{file_name}' for file_name in files]

        return files

    @staticmethod
    def read(paths, concat=False, **read_options):

        data = None

        if type(paths) == list and len(paths) > 1:
            data = FileUtils.read_chunk(paths, concat=concat, **read_options)
        elif type(paths) == str:
            path = paths
            data = FileUtils.read_single_file(path, **read_options)
        elif type(paths) == list and len(paths) == 1:
            path = paths[0]
            data = FileUtils.read_single_file(path, **read_options)

        return data

    @staticmethod
    def delete_duplicates(data, inplace=True, keep='first', subset=None):
        """ Remove duplicates"""
        if not data.empty and inplace:
            data.drop_duplicates(inplace=inplace, keep=keep, subset=subset)
        elif not data.empty:
            return data.drop_duplicates(inplace=inplace, keep=keep, subset=subset)
