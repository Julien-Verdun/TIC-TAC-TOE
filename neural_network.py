
import random
import numpy as np
import json


from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam


#Activation function

def sigmoid(x,a=1):
    """
    Comput the result of implementation of sigmoid function to an array x.
    """
    return 1/(1+np.exp(-a*x))


class NeuralNetwork:
    def __init__(self):
        self.__input_layer = np.random.random((9,1))
        self.__weight1 = np.random.random((9,18))
        self.__hidden_layer = np.random.random((18, 1))
        self.__weight2 = np.random.random((18,9))
        self.__output_layer = np.random.random((9, 1))

        self.__game_recorder = Game_recorder("record_games.JSON")

        self.__weight_recorder = Game_recorder("record_weight.JSON")


    #GET methods
    def get_input_layer(self):
        return self.__input_layer
    def get_weight1(self):
        return self.__weight1
    def get_hidden_layer(self):
        return self.__hidden_layer
    def get_weight2(self):
        return self.__weight2
    def get_output_layer(self):
        return self.__output_layer

    #Computing the layers
    def comput_hidden_layer(self):
        self.__hidden_layer = sigmoid(np.transpose(self.__input_layer).dot(self.__weight1))
    def comput_output_layer(self):
        self.__hidden_layer = sigmoid(self.__hidden_layer.dot(self.__weight2))
    def comput_next_square(self):
        return np.argmax(self.__output_layer)


    #prediction with trained neural network
    def predict_square(self,input):
        self.__input_layer = input
        self.comput_hidden_layer()
        self.comput_output_layer()
        output_square = self.comput_next_square()
        return output_square


    def train_neural_network(self):
        games = self.__game_recorder.read_record_file()
        # list of the lists of values of each square
        board_values_list = np.zeros((len(games),9))
        # list of the result of the game
        end_state_list = np.zeros(len(games))

        for i in range(len(games)):
            board_values_list[i][:] = np.array(games[i]["board_values"])
            if games[i]["end_state"] == "IA_victory":
                end_state_list[i] = 1
            elif games[i]["end_state"] == "Player_victory":
                end_state_list[i] = -1
            else:
                end_state_list[i] = 0


        model = Sequential()
        model.add(Dense(18, input_dim=9, activation='relu'))
        model.add(Dropout(0.5))
        #model.add(Dense(18, activation='relu'))
        #model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
        print(model.summary())

        model.fit(board_values_list, end_state_list,epochs=10,batch_size=5)
        #_, acc = model.evaluate(x_test, y_test, batch_size=16)
        #print('test accuracy: ', acc)


        data = {}
        data["weight1"]  = self.get_weight1().tolist()
        data["weight2"] =  self.get_weight2().tolist()
        self.__weight_recorder.write_game(data)


class Game_recorder:
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