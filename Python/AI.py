import json
import os
import random
import numpy as np
from keras.models       import Sequential
from keras.layers       import Dense
from keras.optimizers   import Adam
from createfile         import main as createfile
from gamelogic          import findsquare as findsquare

def findtablero(num):
    found = False
    while found == False:
        folder = os.path.abspath("../Tableros/")
        tablero = folder + "/" + str(num) + ".json"
        if os.path.isfile(tablero) == False:
                print(tablero)
                found = True
                open(tablero, "a+")
                createfile(tablero)
        else: num += 1
        return tablero

tablero = findtablero(1)
goal_steps = 10
intial_games = 10000
player = 1

def model_data_preparation():
    training_data = []
    accepted_scores = []
    for game_index in range(intial_games):
        score = 0
        game_memory = []
        previous_observation = []
        for step_index in range(goal_steps):
            actionx = random.randrange(0, 6)
            actiony = random.randrange(0, 10)
            action = str(actionx) + str (actiony)
            done, info = findsquare(action, tablero, player)
            with open (tablero, "r") as jsonfile:
                observation = json.load[jsonfile]
            if len(previous_observation) > 0:
                game_memory.append([previous_observation, action])
            reward = 0
            done = True
            found1 = False
            found2 = False
            for square in observation["boxes"]:
                if square[player] == player:
                     found1 = True
                     reward += 1
                     if square["cordx"] or square["cordy"] == 0 or square["cordx"] == 5 or square["cordy"] == 9:
                        reward += 1
                        if square["cordx"] and square["cordy"] == 0 or square["cordx"] == 5 and square["cordy"] == 9:
                                reward += 1


                elif square[player] != 0:
                     found2 = True
                     reward -= 1
                     if square["cordx"] or square["cordy"] == 0 or square["cordx"] == 5 or square["cordy"] == 9:
                        reward -= 1
                        if square["cordx"] and square["cordy"] == 0 or square["cordx"] == 5 and square["cordy"] == 9:
                                reward -= 1
            if found1 and found2 == True: done = False
            previous_observation = observation
            score += reward
            if done:
                break
            
        if score > 0:
            accepted_scores.append(score)
            for data in game_memory:
                if data[1] == 1:
                    output = [0, 1]
                elif data[1] == 0:
                    output = [1, 0]
                training_data.append([data[0], output])
        
        env.reset()

    print(accepted_scores)
    
    return training_data

def build_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dense(52, activation='relu'))
    model.add(Dense(output_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam())
    return model

def train_model(training_data):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))
    model.fit(X, y, epochs=10)
    return model