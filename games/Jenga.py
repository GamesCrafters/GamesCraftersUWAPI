"""
    Author: Nakul Srikanth
"""

import json
import sys
import pickle
import os

from .models import AbstractVariant

class Jenga(AbstractVariant):

    def __init__(self):
        self.DIRECTORY = "data/"
        self.FILENAME = "JengaOutput.txt"
        super(Jenga, self).__init__("Regular - 15 pieces", 'v3')

    def start_position(self):
        return {
            'position': '1_' + 'J' * 15,
            'autoguiPosition': '1_' + 'J' * 15
        }

    def stat(self, position):
        try:
            response = ""

            with open(self.DIRECTORY + self.FILENAME, "r") as JengaDatabaseFile:
                data = JengaDatabaseFile.readlines()
                for line in data:
                    if line == "":
                        break

                    #Parsed_Line formatting to be changed
                    parsed_Lines = line.split(" ")
                    if parsed_Lines[2].strip("\n") == position.split("_")[1]:
                        response = {
                            "position": position,
                            "autoguiPosition": position,
                            "positionValue": parsed_Lines[1],
                            "remoteness": int(parsed_Lines[0]),
                        }
                        break
                
                JengaDatabaseFile.close()

            if response == "":
                print("Error: Could not find position -> " + position )

            return response
        except IOError:
            print("Error: Could not read JengaDatabaseFile")

    def position_data(self, position):
        response = self.stat(position)
        json_moves = []
        moves = GenerateMoves(position.split("_")[1])
        opp_turn = '2' if position[0] == '1' else '1'
        for move in moves:
            response_dict = {
                "move": str(move),
                "autoguiMove": f"A_h_{move}_x",
                **self.stat(f"{opp_turn}_{DoMove(position.split('_')[1], move)}")
            }
            json_moves.append(response_dict)
        response["moves"] = json_moves
        return response
    

################### Jenga Encoded File ##########################

######################################################
# Name: Nakul Srikanth
# 
# Game: Jenga
# 
# Description:
# Players remove pieces from tower and 
# add them to the top of the pile. Player without 
# any legal moves left loses. The topmost finished 
# level and above are unaccesible for moves.
#
#######################################################

def isPrimitive(board):
    if (GenerateMoves(board) != []):
        return False
    return True

def DoMove(board, move):
    if (not isPrimitive(board) and all([board[move + m] == 'J' for m in getAdjacent(move)])):
        return board[:move] + "X" + board[move+1:] + "J"
    else:
        return board
    

def PrimitiveValue(board):
    if isPrimitive(board):
        return "L"
    else:
        return "Not Primitive"

def GenerateMoves(board):
    returnLst = []
    for k in range(((len(board) // 3) - 1) * 3):
        if board[k] == 'J' and all([board[k + m] == 'J' for m in getAdjacent(k)]):
            returnLst.append(k)

    return returnLst

def getAdjacent(move):
    index = move % 3
    if(index == 0):
        return [1]
    elif(index == 1):
        return [-1, 1]
    else:
        return [-1]
    
###################### Solver ###################################

"""
######################################################
# Name: Nakul Srikanth
# 
# Game: Jenga
# 
# Description:
# Players remove pieces from tower and 
# add them to the top of the pile. Player without 
# any legal moves left loses. The topmost finished 
# level and above are unaccesible for moves.
#
#######################################################


import Jenga

pieces = 9
board = "J"*pieces

myDict = {}

def Solver(board):
    board_primitive = Jenga.PrimitiveValue(board)
    if (board_primitive != "Not Primitive"): 
        myDict[board] = (board_primitive, 0)
        return (board_primitive, 0)
    else:
        moves = Jenga.GenerateMoves(board)
        primitives_list = []
        for move in moves:
            new_board = Jenga.DoMove(board, move)
            if new_board in myDict.keys():
                primitives_list.append(myDict[new_board])
            else:
                primitives_list.append(Solver(new_board))
        if ("Lose" in [m for (m, n) in primitives_list]):
            min_remote = 99999999999999
            for item in primitives_list:
                k, v = item
                if k == "Lose" and v < min_remote:
                    min_remote = v
            min_remote += 1
            myDict[board] = ("Win", min_remote)
            return ("Win", min_remote)
        else:
            max_remote = -1
            for item in primitives_list:
                k, v = item
                if k == "win" and v > max_remote:
                    max_remote = v
            max_remote += 1
            myDict[board] = ("Lose", max_remote)
            return ("Lose", max_remote)

def test():
    Solver(board)

    myFile = open("JengaOutput1.txt", 'w')

    for k, v in myDict.items():
        val, remoteness = v
        myFile.write(str(remoteness) + " " + val + " ")
        myFile.write(str(k))
        myFile.write("\n")

    myFile.close()

    return myDict

test()

"""