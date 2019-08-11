import random
import numpy as np
import json
import time



class Game_recorder:
    def __init__(self,record_games_file):
        self.__file_name = record_games_file
        self.__index = self.read_index()

    def read_record_file(self):
        with open(self.__file_name) as f:
            data = [json.loads(line) for line in f]
        return data

    def add_game(self, data):
        with open(self.__file_name, "a") as json_file:
            json.dump(data, json_file)
            json_file.write('\n')

    def write_game(self, data):
        with open(self.__file_name, "w") as json_file:
            json.dump(data, json_file, sort_keys = True, indent = 4,
               ensure_ascii = False)
    def read_index(self):
        data = self.read_record_file()
        data = data[-1]
        index = data["index"]
        return index

    def get_index(self):
        return self.__index



class Weight_recorder:
    def __init__(self,record_games_file):
        self.__file_name = record_games_file

    def read_record_file(self):
        with open(self.__file_name) as f:
            data = [json.loads(line) for line in f]
        return data

    def add_game(self, data):
        with open(self.__file_name, "a") as json_file:
            json.dump(data, json_file)
            json_file.write('\n')

    def write_game(self, data):
        with open(self.__file_name, "w") as json_file:
            json.dump(data, json_file, sort_keys = True, indent = 4,
               ensure_ascii = False)

    def read_index(self):
        data = self.read_record_file()
        data = data[-1]
        index = data["index"]
        return index