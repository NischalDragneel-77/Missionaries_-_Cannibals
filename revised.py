from collections import deque
import igraph
from igraph import *

def validMove(node):
   validMoves=[]
   for move in [[1,0],[2,0],[0,1],[0,2],[1,1]]:
      if node.presentState[0]>=move[0] and node.presentState[1]>=move[1] and 0<sum(move)<=2:
         validMoves.append(move)
      else:
         continue
   return validMoves

def isValidState(node):
   return (node.left_bank[0]>=node.left_bank[1] and node.right_bank[0]>=node.right_bank[1]) or (node.left_bank[0]==0 or node.right_bank[0]==0)

def generateChildren(parent,move):
   # no_of_nodes += 1
   newState = {
            'left_bank':[0,0],
            'right_bank':[0,0],
            'presentState':[0,0,0]
        }
   if not parent.presentState[2]:
      newState['left_bank'][0] = parent.left_bank[0]-move[0]
      newState['left_bank'][1] = parent.left_bank[1]-move[1]
      newState['right_bank'][0] = parent.right_bank[0]+move[0]
      newState['right_bank'][1] = parent.right_bank[1]+move[1]
      newState['presentState'] = [*newState['right_bank'][0:2],1]
   else:
      newState['right_bank'][0] = parent.right_bank[0]-move[0]
      newState['right_bank'][1] = parent.right_bank[1]-move[1]
      newState['left_bank'][0] = parent.left_bank[0]+move[0]
      newState['left_bank'][1] = parent.left_bank[1]+move[1]
      newState['presentState'] = [*newState['left_bank'][0:2],0]
   child = Nodes(newState['left_bank'],newState['right_bank'],newState['presentState'],'not checked',parent,nodes_generated)
   return child

class Nodes:
   def __init__(self,left_bank,right_bank,presentState,status,parent,index):
      self.left_bank = left_bank
      self.right_bank = right_bank
      self.presentState = presentState
      self.parent = parent
      self.children = []
      self.status = status
      self.color = 'yellow'
      self.leaf = False
      self.index = index
      
   # def __repr__(self):
   #    return str(self.presentState)
   

if __name__=="__main__":
   nodes_generated = 0
   q=deque()
   pastStates=[]
   g = Graph(directed=True)
   g.vs['nodes'] = []
   g.es['label'] = []
   root = Nodes([3,3],[0,0],[3,3,0],'live',None,nodes_generated)
   q.append(root)
   g.add_vertex(1)
   g.vs[nodes_generated]['nodes'] = root
   g.vs[nodes_generated]['name'] = root.index
   while q:
      node = q.popleft()
      
      if node.presentState == [3,3,1] or node.presentState == [0,0,0]:
         node.status = 'goal'
         node.color = 'green'
         pastStates.append(node.presentState)
         node.leaf = True
         continue

      if not isValidState(node):
         node.status = 'invalid'
         node.color = 'red'
         pastStates.append(node.presentState)
         node.leaf = True
         continue

      if pastStates.count(node.presentState):
         node.status = 'repeated'
         node.color = 'blue'
         pastStates.append(node.presentState)
         node.leaf = True
         continue


      pastStates.append(node.presentState)
      if (node.status != 'invalid' or node.status != 'repeated'):
         possibleMoves = validMove(node)
         for i in possibleMoves:
            nodes_generated += 1
            child = generateChildren(node, i)
            node.children.append(child)
            q.append(child)
            g.add_vertex(1)
            g.vs[nodes_generated]['nodes'] = child
            g.vs[nodes_generated]['name'] = child.index
            v1 = g.vs.find(name=node.index)
            v2 = g.vs.find(name = child.index)
            print(v1,v2)
            g.add_edge(v1,v2)
            g.es[g.get_eid(v1,v2)]['label'] = str(i)
   print(len(pastStates))
   print(g)
   layout = g.layout('tree')
   visual_style = {}
   visual_style["vertex_size"] = 50
   visual_style["vertex_shape"] = 'rectangle'
   visual_style["vertex_label_size"] = 15
   visual_style["vertex_color"] = [nodes.color for nodes in g.vs['nodes']]
   visual_style["vertex_label"] = [nodes.presentState for nodes in g.vs['nodes']]
   visual_style["edge_label"] = g.es['label']
   # visual_style["edge_width"] = [1 + 2 * int(is_formal) for is_formal in g.es["is_formal"]]
   visual_style["layout"] = layout
   visual_style["bbox"] = (1920, 1080)
   plot(g,"statespacetree.png", **visual_style)
