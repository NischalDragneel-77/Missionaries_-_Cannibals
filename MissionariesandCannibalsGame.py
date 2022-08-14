import copy
print(dir(copy))
class MissionaryCannibalGame:
    def __init__(self,left_bank,right_bank):
        self.left_bank = left_bank
        self.right_bank = right_bank
        self.goalState = [3,3,1]
        self.initialState = [3,3,0]
        self.presentState = self.initialState
        self.no_of_moves = 0
    
    def isGoalState(self):
        return self.presentState == self.goalState
    
    def isValidState(self):
        return (self.left_bank[0]>=self.left_bank[1] and self.right_bank[0]>=self.right_bank[1]) or (self.left_bank[0]==0 or self.right_bank[0]==0)
    
    def isValidMove(self,move):
        return move[0]<=self.presentState[0] and move[1]<=self.presentState[1] and 0<sum(move)<=2

    def makeMove(self,move):
        self.no_of_moves += 1
        print("#####################################")
        print("Move number: ",self.no_of_moves)
        print("move:",move)
        if not self.isValidMove(move):
            print("Invalid Move")
            return exit()
        initial_left_bank = copy.deepcopy(self.left_bank)
        initial_right_bank = copy.deepcopy(self.right_bank)
        if not self.presentState[2]:
            self.left_bank[0] = self.left_bank[0]-move[0]
            self.left_bank[1] = self.left_bank[1]-move[1]
            self.right_bank[0] = self.right_bank[0]+move[0]
            self.right_bank[1] = self.right_bank[1]+move[1]
            self.presentState = [*self.right_bank[0:2],1]
        else:
            self.right_bank[0] = self.right_bank[0]-move[0]
            self.right_bank[1] = self.right_bank[1]-move[1]
            self.left_bank[0] = self.left_bank[0]+move[0]
            self.left_bank[1] = self.left_bank[1]+move[1]
            self.presentState = [*self.left_bank[0:2],0]
        print("present state:",self.presentState)
        print("left bank---> before move:",initial_left_bank,"\t after move:",self.left_bank)
        print("right bank---> before move:",initial_right_bank,"\t after move:",self.right_bank) 
        print("Boat Position:","right" if self.presentState[2]  else"left")
        if not self.isValidState():
            print("Invalid State")
            self.left_bank = initial_left_bank
            self.right_bank = initial_right_bank
            self.presentState = self.initialState
            return exit()
        if self.isGoalState():
            print("Goal state reached")
            return exit()
    
    # def possibleMoves(self):
    #     if self.presentState[0]:
    #         x = self.presentstate[0]
    #         for i in range(0,x):
    #             availableMoves.append(i)

game1 = MissionaryCannibalGame([3,3],[0,0])

# sequence_of_move = [[0,2],[0,1],[0,2],[0,1],[2,0],[1,1],[2,0],[0,1],[0,2],[0,1],[0,2]]
# sequence_of_move = [[2,0],[0,0],[0,2],[0,1],[2,0],[1,1],[2,0],[0,1],[0,2],[0,1],[0,2]]
# for i in sequence_of_move:
#     game1.makeMove(i)

# game1.makeMove([0,2])
# game1.makeMove([0,1])
# game1.makeMove([0,2])
# game1.makeMove([0,1])
# game1.makeMove([2,0])
# game1.makeMove([1,1])
# game1.makeMove([2,0])
# game1.makeMove([0,1])
# game1.makeMove([0,2])
# game1.makeMove([0,1])
# game1.makeMove([0,2])