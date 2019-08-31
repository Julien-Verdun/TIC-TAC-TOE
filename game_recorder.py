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
            json.dump(data, json_file) #, sort_keys = True, indent = 4,ensure_ascii = False)
    def read_index(self):
        data = self.read_record_file()
        data = data[-1]
        index = data["index"]
        return index

    def get_index(self):
        return self.__index
"""
game_recorder = Game_recorder("record_games.JSON")
print(game_recorder.get_index())
print(game_recorder.read_record_file())
"""

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
            json.dump(data, json_file)

    def read_index(self):
        data = self.read_record_file()
        data = data[-1]
        index = data["index"]
        return index

"""
weight_recorder = Weight_recorder("test.JSON")
data = {}
data["weight1"] = np.zeros(10).tolist()
data["weight2"] = np.zeros(10).tolist()
weight_recorder.add_game(data)
print(weight_recorder.read_record_file())
"""