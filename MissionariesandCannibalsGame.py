import copy
from collections import deque

goalState = [3,3,1]
initialState = [3,3,0]
pastStates = []

class MissionaryCannibalGame:
    def __init__(self,left_bank,right_bank,presentState):
        self.left_bank = left_bank
        self.right_bank = right_bank
        self.presentState = presentState

    def isGoalState(self):
        return self.presentState == goalState
    
    def isValidState(self):
        return (self.left_bank[0]>=self.left_bank[1] and self.right_bank[0]>=self.right_bank[1]) or (self.left_bank[0]==0 or self.right_bank[0]==0)
    
    def isValidMove(self,move):
        return move[0]<=self.presentState[0] and move[1]<=self.presentState[1] and 0<sum(move)<=2

    def makeMove(self,move):
        print("#####################################")
        # print("Move number: ",no_of_moves)
        print("move:",move)
        newState = {
            'left_bank':[0,0],
            'right_bank':[0,0],
            'presentState':[0,0,0]
        }
        if not self.isValidMove(move):
            print("Invalid Move")
            return 0
        initial_left_bank = copy.deepcopy(self.left_bank)
        initial_right_bank = copy.deepcopy(self.right_bank)
        if not self.presentState[2]:
            newState['left_bank'][0] = self.left_bank[0]-move[0]
            newState['left_bank'][1] = self.left_bank[1]-move[1]
            newState['right_bank'][0] = self.right_bank[0]+move[0]
            newState['right_bank'][1] = self.right_bank[1]+move[1]
            newState['presentState'] = [*newState['right_bank'][0:2],1]
        else:
            newState['right_bank'][0] = self.right_bank[0]-move[0]
            newState['right_bank'][1] = self.right_bank[1]-move[1]
            newState['left_bank'][0] = self.left_bank[0]+move[0]
            newState['left_bank'][1] = self.left_bank[1]+move[1]
            newState['presentState'] = [*newState['left_bank'][0:2],0]
        print("present state:",newState['presentState'])
        print("left bank---> before move:",initial_left_bank,"\t after move:",newState['left_bank'])
        print("right bank---> before move:",initial_right_bank,"\t after move:",newState['right_bank']) 
        print("Boat Position:","right" if newState['presentState'][2]  else"left")

        return newState

class Nodes:
    def __init__(self, data, parent,state):
        self.data = data
        self.parent = parent
        self.state = state
        self.children = []
    
    def __repr__(self):
        return str(self.state)

    def generateChildren(self):
        if not self.data.isValidState() or self.data.isGoalState() or self.state=='repeated':
            return []
        for i in [[1,0],[2,0],[0,1],[0,2],[1,1]]:
            if self.data.isValidMove(i):
                childState = self.data.makeMove(i)
                nodeState=''
                if pastStates.count(childState['presentState']):
                    nodeState = 'repeated'
                else:
                    pastStates.append(childState['presentState'])
                    nodeState = 'new'
                child = MissionaryCannibalGame(childState['left_bank'], childState['right_bank'], childState['presentState'])
                if not child.isValidState():
                    nodeState = 'invalid'
                childnode = Nodes(child,self,nodeState)
                if nodeState == 'new':
                    q.append(childnode)
                self.children.append(childnode)

    def getData(self):
        return self.data
    
    def getState(self):
        return self.state


if __name__ == "__main__":
    q = deque()    
    root = Nodes(MissionaryCannibalGame([3,3],[0,0],[3,3,0]),None,"live")
    q.append(root)
    while q:
        node = q.popleft()

    print(q[0].getData().left_bank)
    print(q[0].getData().right_bank)
    print(q[0].getData().presentState)
    print(q.pop().children)
    root.generateChildren()
    print(root.children)
    print(q)
