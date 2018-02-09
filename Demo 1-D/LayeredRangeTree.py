from abc import ABC, abstractmethod
import math

class Node(ABC):
    @abstractmethod
    def isLeaf(self):
        pass

class InternalNode(Node):

    def __init__(self, k):
        self.factor = 0
        self.k = k
        self.child = [None, None]
    
    def isLeaf(self):
        return False

class LeafNode(Node):
    
    def __init__(self, k, v):
        self.k = k
        self.v = v

    def isLeaf(self):
        return True

class LayeredRangeTree:
    def __init__(self):
        self.root = None

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
    def search( self, x1, x2 ):
        S = self.searchTrees( x1, x2 )
        leaves = []
        for node in S:
            list = []
            self.__inorderLeaves__(node, list)
            leaves.extend( [n.k for n in list] )            
        return sorted(leaves)

    def searchTrees(self, x1, x2):
        lca = self.getLCA( x1, x2 )

        if lca.isLeaf():
            if lca.k != x1 or lca.k != x2:
                return []
            return [lca]
        
        S1 = self.getLeftChildren( lca, x1 )
        S2 = self.getRightChildren( lca, x2 )
        S1.extend(S2)
        for n in S1:
            print(n.k)
        return S1

    def getLeftChildren(self, lca, x):
        S = []
        node = lca.child[0]
        while not node is None and not node.isLeaf():
            if node.k >= x:
                S.append(node.child[1])
                node = node.child[0]
            else:
                node = node.child[1]
        if not node is None and node.isLeaf() and node.k >= x:
            S.append(node)
        return S

    def getRightChildren(self, lca, x):
        S = []
        node = lca.child[1]
        while not node is None and not node.isLeaf():
            if node.k <= x:
                S.append(node.child[0])
                node = node.child[1]
            else:
                node = node.child[0]
        if not node is None and node.isLeaf() and node.k <= x:
            S.append(node)
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
                print( "Nodo Hoja: ", node.k )
            else:
                print( "Nodo: ", node.k, " : ", node.factor, " - " , "" if node.child[0] is None else node.child[0].k, " - " , "" if node.child[1] is None else node.child[1].k )
                if not node.child[0] is None:
                    Q.insert(0,node.child[0])
                if not node.child[1] is None:
                    Q.insert(0,node.child[1])

    """---------------------------------------------------------------------------------------------------------
                                                 get Height
    ------------------------------------------------------------------------------------------------------------"""
    def __getHeight__(self, node):
        if node is None or node.isLeaf():
            return 0
        return 1 + max( self.__getHeight__( node.child[0] ), self.__getHeight__( node.child[1] ) )
        
    def getHeight(self):
        return self.__getHeight__(self.root)
    
