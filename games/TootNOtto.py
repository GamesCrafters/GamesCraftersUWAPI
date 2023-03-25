# -*- coding: iso-8859-15 -*-
import json
import sys
import pickle
import os

from .models import AbstractGameVariant


class TootNOtto(AbstractGameVariant):

    def pos_to_UWAPI(self, position):

        ### BOARD

        SPACER = "-" #"█"
        DOWN   = "v" #"↓"

        """
            ----------------x4444
            --------------------x5555
            ------------------------x6666

            ROWS=4, COLS=4, WIDTH=COLS+6=10, HEIGHT=7
            ███TTTT███
            ███OOOO███
            ███↓↓↓↓███
            TO█----█OT
            TO█----█OT
            TO█----█OT
            TO█----█OT

            ROWS=4, COLS=5, WIDTH=COLS+6=11, HEIGHT=7
            ███TTTTT███
            ███OOOOO███
            TO█↓↓↓↓↓█OT
            TO█-----█OT
            TO█-----█OT
            TO█-----█OT
            TO█-----█OT

            ROWS=4, COLS=6, WIDTH=COLS+6=12, HEIGHT=7
            ███TTTTTT███
            TO█OOOOOO█OT
            TO█↓↓↓↓↓↓█OT
            TO█------█OT
            TO█------█OT
            TO█------█OT
            TO█------█OT

        ### Each position is ROWS*COLS of {-TO} + xo + 0-6 X Ts + 0-6 X Os + 0-6 O Ts + 0-6 O Os
        ### Each move is (slot, 'T' or 'O')

        """
        xo = position[self.ROWS*self.COLS]
        Ts = int(position[self.ROWS*self.COLS + 1 + {'x':0,'o':2}[xo]])
        Os = int(position[self.ROWS*self.COLS + 1 + {'x':1,'o':3}[xo]])
        Tsx = int(position[self.ROWS*self.COLS + 1 + 0])
        Osx = int(position[self.ROWS*self.COLS + 1 + 1])
        Tso = int(position[self.ROWS*self.COLS + 1 + 2])
        Oso = int(position[self.ROWS*self.COLS + 1 + 3])

        ### HEADER

        s = "R_"
        s += {"x":"A","o":"B"}[position[self.ROWS*self.COLS]]
        s += "_"
        s += str(7)
        s += "_"
        s += str(self.COLS+6)
        s += "_"

        ### ROW 1

        s += SPACER*3
        #s += ("T" if Ts > 0 else "█") * self.COLS
        # for col in range(self.COLS):
        #     s += ("T" if (Ts > 0 and position[((self.ROWS-1)*self.COLS)+col]=="-") else SPACER)
        s += SPACER * self.COLS

        s += SPACER*3

        ### ROW 2

        if self.COLS < 6:
            s += SPACER*2
        else:
            s += ("T" if Tsx == 6 else SPACER)
            s += ("O" if Osx == 6 else SPACER)
        s += SPACER
        #s += ("O" if Os > 0 else "█") * self.COLS
        # for col in range(self.COLS):
        #     s += ("O" if (Os > 0 and position[((self.ROWS-1)*self.COLS)+col]=="-") else SPACER)
        s += SPACER * self.COLS
        s += SPACER
        if self.COLS < 6:
            s += SPACER*2
        else:
            s += ("O" if Oso == 6 else SPACER)
            s += ("T" if Tso == 6 else SPACER)

        ### ROW 3   

        if self.COLS == 4:
            s += SPACER*2
        else:
            s += ("T" if Tsx >= 5 else SPACER)
            s += ("O" if Osx >= 5 else SPACER)
        s += SPACER
        s += DOWN * self.COLS
        s += SPACER
        if self.COLS == 4:
            s += SPACER*2
        else:
            s += ("O" if Oso >= 5 else SPACER)
            s += ("T" if Tso >= 5 else SPACER)

        ### ROW 4 to 7

        for row in range(4,0,-1):
            s += ("T" if Tsx >= row else SPACER)
            s += ("O" if Osx >= row else SPACER)
            s += SPACER
            s += position[(row-1)*self.COLS:(row)*self.COLS] # print board for that row
            s += SPACER
            s += ("O" if Oso >= row else SPACER)
            s += ("T" if Tso >= row else SPACER)

        return s

    def UWAPI_to_pos(self, UWAPI_position):
        return UWAPI_position.split("_")[-1]

    def ListFiles(self, directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f != "DOWN" and f != "UP"]

    def GetValueRemoteness(self, current_tier, parentSig, mySig, position):
        if os.path.exists(os.getcwd()+'/'+self.DIRECTORY+"/"+str(current_tier)+"/"+"DB"+parentSig+"_"+mySig+"_up.p"):
            tierDB = pickle.load(open(os.getcwd()+'/'+self.DIRECTORY+"/"+str(current_tier)+"/"+"DB"+parentSig+"_"+mySig+"_up.p","rb"))
            if position in tierDB:
                return tierDB[position]
        for filename in filter(lambda f: f != ("DB"+parentSig+"_"+mySig+"_up.p"), self.ListFiles(os.getcwd()+'/'+self.DIRECTORY+"/"+str(current_tier))):
            tierDB = pickle.load(open(os.getcwd()+'/'+self.DIRECTORY+"/"+str(current_tier)+"/"+filename,"rb"))
            if position in tierDB:
                return tierDB[position]
        print("BADELSE, in GetValueRemoteness, couldn't find " + position)
        exit()

    def GetValueRemotnessEasy(self, position):
        return self.GetValueRemoteness(sum([1 for s in position[0:(self.ROWS*self.COLS)] if s != "-"]),
            position[0:self.COLS], position[0:self.COLS], position)

    def GenerateMoves(self, position):
        xo = position[self.ROWS*self.COLS]
        Ts = int(position[self.ROWS*self.COLS + 1 + {'x':0,'o':2}[xo]])
        Os = int(position[self.ROWS*self.COLS + 1 + {'x':1,'o':3}[xo]])
        slots = list(filter(lambda col:position[((self.ROWS-1)*self.COLS)+col]=='-',range(self.COLS)))
        return [(slot,'T') for slot in slots if Ts > 0] + \
               [(slot,'O') for slot in slots if Os > 0] 

    def DoMove(self, position, move):
        (slot,TO) = move
        row = min(filter(lambda row:position[(row*self.COLS)+slot]=='-',range(self.ROWS)))
        topRow = row*self.COLS
        xo = position[self.ROWS*self.COLS]
        TOs = list(map(int,position[self.ROWS*self.COLS+1:self.ROWS*self.COLS+5]))
        index = {'xT':0,'xO':1,'oT':2,'oO':3}[xo+TO]
        TOs[index] = TOs[index] - 1
        return position[0:topRow]+\
               position[topRow:topRow+slot]+\
               TO+\
               position[topRow+slot+1:self.ROWS*self.COLS]+\
               {'x':'o','o':'x'}[xo]+\
               "".join(map(str,TOs))

    def MoveToUWAPI(self, position, move):
        return "A_"+move[1].lower()+"_"+str(3+int(move[0])+((self.COLS+6) if move[1] == "O" else 0))

    def __init__(self, COLS):

        self.COLS   = COLS
        self.ROWS   = 4
        self.NINROW = 4
        self.NAME = "" + str(self.ROWS) + "x" + str(self.COLS) + "Toot-N-Otto"
        self.DIRECTORY = "data/" + self.NAME + "F"
 
        name   = "" + str(self.ROWS) + "x" + str(self.COLS) + " Toot-N-Otto"
        desc   = str(COLS) + "x4"
        status = "stable"
        gui_status = 'v2'

        super(TootNOtto, self).__init__(name, desc, status=status, gui_status=gui_status)

    def start_position(self):
        #return "R_A_1_3_RL-"
        #return "R_A_1_3_RL-_----------------x4444"
        initial_position = ("-" * self.ROWS * self.COLS) + "x" + (str(self.COLS) * 4)
        return self.pos_to_UWAPI(initial_position) + "_" + initial_position

    def stat(self, UWAPI_position):
        position_value_char,remoteness = self.GetValueRemotnessEasy(self.UWAPI_to_pos(UWAPI_position))
        position_value = {'t':'tie','w':'win','l':'lose'}[position_value_char]
        response = {
            "position"     : UWAPI_position,
            "positionValue": position_value,
            "remoteness"   : remoteness,
        }
        return response

    def next_stats(self, UWAPI_position):
        position = self.UWAPI_to_pos(UWAPI_position)
        position_value_char,remoteness = self.GetValueRemotnessEasy(position)
        response = []
        if remoteness != 0:
            moves = self.GenerateMoves(position)
            for move in moves:
                UWAPI_move = self.MoveToUWAPI(position,move)
                next_position = self.DoMove(position,move)
                next_UWAPI_position = self.pos_to_UWAPI(next_position)+"_"+next_position
                next_res = {
                    "move": UWAPI_move,
                    "moveName": f'{move[1]}-{move[0] + 1}',
                    **self.stat(next_UWAPI_position)
                }
                response.append(next_res)
        return response

    def get_player(self, position_str):
        return position_str.split('_')[1]