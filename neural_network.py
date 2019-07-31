
import random
import numpy as np
import json
import time

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
        """
        self.__game_recorder = Game_recorder("record_games.JSON")
        self.__weight_recorder = Game_recorder("record_weight.JSON")
        """
        self.__NNtrainer = NeuralNetwork_trainer("record_games.JSON","record_weight.JSON")
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
    def predict_output(self,input):
        self.__NNtrainer.predict(input)

    def train_neural_network(self):
        t0 = time.time()
        self.__NNtrainer.train_neural_network()
        t1 = time.time()
        print("Time to train the neural network : ", t1-t0)



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



class NeuralNetwork_trainer:
    def __init__(self,record_games_file,record_weight_file):
        self.__game_recorder = Game_recorder(record_games_file)
        self.__weight_recorder = Game_recorder(record_weight_file)

        #model builder
        self.__model = Sequential()
        # add a hidden layer with 18 nodes
        self.__model.add(Dense(18, input_dim=9, activation='sigmoid'))
        self.__model.add(Dropout(0.95))
        # add an other hidden layer with 18 nodes
        #self.__model.add(Dense(18, activation='relu'))
        #self.__model.add(Dropout(0.95))
        # add the output layer
        self.__model.add(Dense(1, activation='sigmoid'))


    def get_games(self):
        """
        Return the games set, in JSON format, by calling the Game_recorder class.
        """
        return self.__game_recorder.read_record_file()
    def games_to_list_of_data(self,games):
        """
        Turn the games JSON variable into the list of board_value and end_state.
        """
        # list of the lists of values of each square
        board_values_list = np.zeros((len(games), 9))
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
        return board_values_list,end_state_list
    def data_to_train_test(self,board_values_list,end_state_list,rate_set = 0.8):
        """
        Take both the list of all board values (included in board_values_list)
        and games result (included in end_state_list) recorded and divide both list
        into 2 lists, one consists of the n% of the values (n is the rate_set) and the
        other the rest of the values.
        The list are splited in order to provide train and test dataset for the neural network.
        """
        board_values_list_train = board_values_list[:int(rate_set*len(board_values_list))]
        board_values_list_test = board_values_list[int(rate_set*len(board_values_list)):]
        end_state_list_train = end_state_list[:int(rate_set*len(end_state_list))]
        end_state_list_test = end_state_list[int(rate_set*len(end_state_list)):]
        return board_values_list_train,board_values_list_test,end_state_list_train,end_state_list_test

    def train_neural_network(self):
        """
        Train the Neural Network with a part of the record data and display the efficiency of
        the training with the other part of the record data.
        Write the learnt weights on a JSON file.
        """
        games = self.get_games()
        board_values_list,end_state_list = self.games_to_list_of_data(games)
        board_values_list_train, board_values_list_test, end_state_list_train, end_state_list_test = self.data_to_train_test(board_values_list,end_state_list)


        self.__model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
        print(self.__model.summary())

        print(self.__model.fit(board_values_list_train, end_state_list_train,epochs=10,batch_size=5))

        _ , acc = self.__model.evaluate(board_values_list_test, end_state_list_test, batch_size=2)
        print('test accuracy: ', acc)

        weights = self.__model.get_weights()

        [weight1,hidden_layer1,weight2,output_layer] = weights

        data = {}
        data["weight1"]  = weight1.tolist()
        data["weight2"] =  weight2.tolist()
        self.__weight_recorder.write_game(data)

        print('Neural Network train')

    def predict(self,board_values):
        return self.__model.predict(board_values)


"""
nn = NeuralNetwork()
input = np.array([0,0,1,0,0,-1,1,0,0])
print(input)
print(nn.predict_output(input))
"""