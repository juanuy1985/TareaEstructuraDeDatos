from abc import ABC, abstractmethod
from timeit import default_timer as timer
import random
import math

class FractionalLayerCell:
    def __init__( self, k, v, pos0, pos1 ):
        self.k = k
        self.v = v
        self.children = [pos0, pos1]

    def __str__(self):
        return "k: " + str(self.k) + " v: " + str(self.v) + " : children " + str(self.children)
        #return str(self.k) + " : children " + str(self.children)
            

class Node(ABC):

    def __init__(self):
        self.fractionalLayer = []
    
    @abstractmethod
    def isLeaf(self):
        pass

class InternalNode(Node):

    def __init__(self, k):
        super(InternalNode, self).__init__()
        self.factor = 0
        self.k = k
        self.child = [None, None]
    
    def isLeaf(self):
        return False

class LeafNode(Node):
    
    def __init__(self, k, v):
        super(LeafNode, self).__init__()
        self.k = k
        self.v = v

    def isLeaf(self):
        return True

class LayeredRangeTree:
    def __init__(self, points = None):
        self.root = None
        if not points is None:
            self.__bulk__( points )
            
    """---------------------------------------------------------------------------------------------------------
                                              Insert - Bulk
    ------------------------------------------------------------------------------------------------------------"""
    def __bulk__( self, points ):

        pointsX = sorted( points, key = lambda x : x[0] ) #Ordenamos los puntos por su coordenada x
        pointsY = sorted( points, key = lambda x : x[1] ) #Ordenamos los puntos por su coordenada y
        #-------------- Creación de los indices para la componente X --------------#

        internalNodes = [ InternalNode( point[0] ) for point in pointsX ]
        leaves = [ LeafNode( point[0], point ) for point in pointsX ]
        list = []
        self.root = self.makeTree( internalNodes, list )
        index = 0
        
        for node in list:
            if node.child[0] is None:
                node.child[0] = leaves[index]
                index = index + 1

            if index < len(leaves) and node.child[1] is None:
                node.child[1] = leaves[index]
                index = index + 1
        #------------- Creación de la estructura Fractional Cascade --------------#
        self.root.fractionalLayer = [ FractionalLayerCell( point[1], point, -1 ,-1  ) for point in pointsY ]
        
        self.makeFractionalCascadeRecursive( self.root )

    def makeFractionalCascadeRecursive( self, node ):

        if node is None:
            return

        if not node.isLeaf():

            index = [0, 0]
            
            for cell in node.fractionalLayer:
                compare = cell.v[0] > node.k # Se realiza la partición por la coordenada X
                if not node.child[compare] is None:
                    node.child[compare].fractionalLayer.append( FractionalLayerCell( cell.k, cell.v, -1, -1 ) )
                    cell.children[compare] = index[compare]
                    index[compare] += 1

            index = [0, 0]
            
            for cell in node.fractionalLayer:
                compare = cell.v[0] <= node.k # Se realiza la partición por la coordenada X                
                if not node.child[compare] is None:
                    while index[compare] < len(node.child[compare].fractionalLayer) and cell.k > node.child[compare].fractionalLayer[ index[compare] ].k: 
                        index[compare] += 1
                cell.children[compare] = index[compare]
                        
            self.makeFractionalCascadeRecursive( node.child[0] )
            self.makeFractionalCascadeRecursive( node.child[1] )
        pass
        
    """---------------------------------------------------------------------------------------------------------
                                                Insert
    ------------------------------------------------------------------------------------------------------------"""
    def insert(self, k, v):
        if self.root is None:
            self.root = InternalNode(k)
            self.root.child[0] = LeafNode(k,v)
        else:
            if(self.__insert__( self.root, k, v )):
                if abs(self.root.factor) == 2:
                    self.root = self.balanceSubTree( self.root )

    def __insert__(self, node, k, v):
        if node.k == k:
            return False
        index = (node.k < k)
        if not node.child[index] is None:
            if node.child[index].isLeaf():
                tmp = node.child[index]
                node.child[index] = InternalNode(k)
                node.child[index].child[0] = LeafNode(k,v)
                node.child[index].child[1] = tmp
                node.factor += -1 if index == 0 else 1
                return True
            elif self.__insert__( node.child[index], k, v ):
                if abs( node.child[index].factor ) == 2:
                    node.child[index] = self.balanceSubTree(node.child[index])
                    return False
                node.factor += -1 if index == 0 else 1
                if node.factor == 0:
                    return False
                return True
            return False
        else:
            node.child[index] = InternalNode(k)
            node.child[index].child[0] = LeafNode(k,v)
            node.factor += -1 if index == 0 else 1
            return True

    def balanceSubTree(self, root):
        internalNodes = self.inorderInternals(root)
        leafNodes = self.getLeaves(root)
        list = []
        newRoot = self.makeTree( internalNodes, list )
        index = 0
        for node in list:
            if node.child[0] is None:
                node.child[0] = leafNodes[index]
                index = index + 1

            if index < len(leafNodes) and node.child[1] is None:
                node.child[1] = leafNodes[index]
                index = index + 1
        return newRoot


    def inorderInternals(self, node):
        list = []
        self.__inorderInternals__(node, list)
        return list

    def __inorderInternals__(self, node, list):
        if node is None or node.isLeaf():
            return
        self.__inorderInternals__(node.child[0], list)
        list.append(node)
        self.__inorderInternals__(node.child[1], list)
        
    def getLeaves( self, node ):
        list = []
        self.__inorderLeaves__(node, list)
        return list
    
    def __inorderLeaves__(self, node, list):
        if node is None:
            return
        if node.isLeaf():
            list.append(node)
        else:
            self.__inorderLeaves__(node.child[0], list)
            self.__inorderLeaves__(node.child[1], list)
        
    def makeTree(self, internalNodes, list):
        newRoot = InternalNode(0)
        self.makeTreeRecursive(internalNodes, 0, len(internalNodes)-1, newRoot, list)
        return newRoot

    def makeTreeRecursive( self, internalNodes, a, b, node, list ):
        m = math.ceil( (a+b)/2 )
        childrenLeft = 0
        childrenRight = 0
        if a < b:
            if a < m:
                node.child[0] = InternalNode(0)
                childrenLeft = 1 + self.makeTreeRecursive( internalNodes, a, m-1, node.child[0], list )
            if b > m:
                node.child[1] = InternalNode(0)
                childrenRight = 1 + self.makeTreeRecursive( internalNodes, m+1, b, node.child[1], list )
        node.k = internalNodes[m].k
        if node.child[0] is None or node.child[1] is None:
            list.append(node)
        node.factor = childrenRight - childrenLeft
        return max(childrenLeft,childrenRight)

    """---------------------------------------------------------------------------------------------------------
                                                     Search
    ------------------------------------------------------------------------------------------------------------"""
    def binary_search( self, list, element ):
        ini = 0
        fin = len(list)
        m = math.floor(( ini + fin ) / 2)
        while ini < fin:
            if list[m].k == element:
                return m
            if list[m].k > element:
                fin = m 
            else:
                ini = m+1
            m = math.floor(( ini + fin ) / 2)
        if m>= len(list) or (list[m].k>element and m > 0):
            return m-1
        return m

    def totalSearch(self, x1, x2):
        lca = self.getLCA( x1[0], x2[0] )

        if lca.isLeaf():
            if lca.k != x1[0] or lca.k != x2[0]:
                return []
            return [lca]

        S1 = self.getLeftChildren( lca, x1, x2 )

        S2 = self.getRightChildren( lca, x1, x2  )

        S1.extend(S2)
        
        return S1
    
    def search( self, x1, x2 ):
        S = self.searchTrees( x1, x2 )
        leaves = []
        for node in S:
            list = []
            self.__inorderLeaves__(node, list)
            leaves.extend( [n.k for n in list] )            
        return sorted(leaves)

    def searchTrees(self, x1, x2):
        lca = self.getLCA( x1[0], x2[0] )

        if lca.isLeaf():
            if lca.k != x1 or lca.k != x2:
                return []
            return [lca]
        
        S1 = self.getLeftChildren( lca, x1 )
        S2 = self.getRightChildren( lca, x2 )
        S1.extend(S2)
        return S1

    def getLeftChildren(self, lca, a, b):
        S = []
        posA = self.binary_search( lca.fractionalLayer, a[1] )
        posB = self.binary_search( lca.fractionalLayer, b[1] )
        node = lca.child[0]
        posA = lca.fractionalLayer[posA].children[0]
        posB = lca.fractionalLayer[posB].children[0]
        pos1 = 0
        pos2 = 0
        while not node is None and not node.isLeaf():
            if node.k >= a[0]:
                if len(node.fractionalLayer) > posA:
                    pos1 = node.fractionalLayer[posA].children[1]
                    posA = node.fractionalLayer[posA].children[0]
                else:
                    pos1 = len(node.fractionalLayer)
                    
                if len(node.fractionalLayer) > posB:
                    pos2 = node.fractionalLayer[posB].children[1]
                    posB = node.fractionalLayer[posB].children[0]
                else:
                    pos2 = len(node.fractionalLayer)
                    
                if pos2 < len(node.child[1].fractionalLayer) and node.child[1].fractionalLayer[pos2].v[1] <= b[1]:
                    pos2 += 1
                S.extend( [cell.v for cell in node.child[1].fractionalLayer][pos1:pos2] )
                
                node = node.child[0]
            else:
                if len(node.fractionalLayer) > posA:
                    posA = node.fractionalLayer[posA].children[1]
                if len(node.fractionalLayer) > posB:
                    posB = node.fractionalLayer[posB].children[1] 
                node = node.child[1]
            
        if not node is None and node.isLeaf() and node.k >= a[0]:# and node.v[1] >= a[1]:
            S.extend( [cell.v for cell in node.fractionalLayer if cell.v[1] >= a[1] and cell.v[1] <= b[1]] )
        return S

    def getRightChildren(self, lca, a, b):
        S = []
        posA = self.binary_search( lca.fractionalLayer, a[1] )
        posB = self.binary_search( lca.fractionalLayer, b[1] )
        node = lca.child[1]
        posA = lca.fractionalLayer[posA].children[1]
        posB = lca.fractionalLayer[posB].children[1]
        pos1 = -1
        pos2 = -1
        while not node is None and not node.isLeaf():
            if node.k <= b[0]:
                if len(node.fractionalLayer) > posA:
                    pos1 = node.fractionalLayer[posA].children[0]
                    posA = node.fractionalLayer[posA].children[1]
                else:
                    pos1 = len(node.fractionalLayer)
                
                if len(node.fractionalLayer) > posB:
                    pos2 = node.fractionalLayer[posB].children[0]
                    posB = node.fractionalLayer[posB].children[1]
                else:
                    pos2 = len(node.fractionalLayer)
                
                if pos2 < len(node.child[0].fractionalLayer) and node.child[0].fractionalLayer[pos2].v[1] <= b[1]:
                    pos2 += 1
                S.extend( [cell.v for cell in node.child[0].fractionalLayer][pos1:pos2] )
                node = node.child[1]
            else:
                if len(node.fractionalLayer) > posA:
                    posA = node.fractionalLayer[posA].children[0]
                if len(node.fractionalLayer) > posB:
                    posB = node.fractionalLayer[posB].children[0] 
                node = node.child[0]
            
        if not node is None and node.isLeaf() and node.k <= b[0]:
            S.extend( [cell.v for cell in node.fractionalLayer if cell.v[1] >= a[1] and cell.v[1] <= b[1]] )
        return S

    def getLCA( self, x1, x2 ):
        node = self.root

        while not node is None and not node.isLeaf():
            if node.k > x1 and node.k > x2:
                node = node.child[0]
            elif node.k < x1 and node.k < x2:
                node = node.child[1]
            else:
                break
        return node
    
    """---------------------------------------------------------------------------------------------------------
                                                    Print
    ------------------------------------------------------------------------------------------------------------"""
    
    def print(self):
        if self.root is None:
            return

        Q = []
        Q.append( self.root )

        while(len(Q)>0):
            node = Q.pop()
            if(node.isLeaf()):
                print( "Nodo Hoja: ", node.v )
            else:
                print( "Nodo: ", node.k, " : ", node.factor, " - " , "" if node.child[0] is None else node.child[0].k, " - " , "" if node.child[1] is None else node.child[1].k )
                if not node.child[0] is None:
                    Q.insert(0,node.child[0])
                if not node.child[1] is None:
                    Q.insert(0,node.child[1])
                    
            for cell in node.fractionalLayer:
                print( cell )
            print("")

    """---------------------------------------------------------------------------------------------------------
                                                 get Height
    ------------------------------------------------------------------------------------------------------------"""
    def __getHeight__(self, node):
        if node is None or node.isLeaf():
            return 0
        return 1 + max( self.__getHeight__( node.child[0] ), self.__getHeight__( node.child[1] ) )
        
    def getHeight(self):
        return self.__getHeight__(self.root)

cases = [ 100, 1000, 2000, 4000, 5000, 8000, 10000, 20000, 30000, 40000, 50000, 80000, 100000, 150000, 200000, 250000, 275000, 300000 ]

ranges =    [
                [10,10],[20,20],
                [10,10],[50,50],
                [10,10],[100,100],
                [10,10],[1000,1000],
                [10,10],[2000,2000],
                [10,10],[10000,10000],
                [10,10],[100000,100000],
                [10,10],[150000,150000],
                [10,10],[200000,200000],
                [10,10],[1000000,1000000]
            ]

for n in cases:
    points = []
    for i in range(n):
        points.append( [random.random()*1000000,random.random()*1000000] )
    tree = LayeredRangeTree(points)

    index = 0
    while index < len(ranges):
        start = timer()
        points = tree.totalSearch( ranges[index], ranges[index+1] )
        end = timer()
        print("{0}\t{1}\t{2}\t{3}".format(n, [ranges[index], ranges[index+1]] , end - start, len(points)))
        index += 2
