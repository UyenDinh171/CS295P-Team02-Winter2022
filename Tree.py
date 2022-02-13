# Yunfan Geng
# Uyen Dinh
# CS295P - Winter 2022

# A very simple binary tree.  This implementation assumes that leftChild
# and rightChild are both None (for a leaf) or both are Tree objects.
# An extra piece of information, lexiconItem, is carried on each leaf.
class Tree: 
    def __init__(self, categoryName, leftChild, rightChild, lexiconItem=None):
        self.categoryName = categoryName
        if leftChild is None:
            self.leftChild = None
            self.rightChild = None
            self.lexiconItem = lexiconItem
        else:
            self.leftChild = leftChild
            self.rightChild = rightChild
            self.lexiconItem = None
    
    # walkTree and getLeaves together return a list of the tree's leaves,
    # in left to right order.
    def walkTree(self, l):
        if (self.leftChild is None):
            l.append([self.categoryName, self.lexiconItem])
        # with C1F right child will be none, check if it is none then walk to the left child.
        elif (self.rightChild is None):
            self.leftChild.walkTree(l)
        else:
            self.leftChild.walkTree(l)
            self.rightChild.walkTree(l)
    
    def getLeaves(self):
        l = []
        self.walkTree(l)
        return l


    # This built in function is invoked whenever Python sees str(someTreeObject)
    def __str__(self):
        if self.leftChild is None:
            return '[' + str(self.categoryName) + ' ' + str(self.lexiconItem) + ']'
        elif self.rightChild is None:
            return '[' + str(self.categoryName) + str(self.leftChild) + ']'
        else:
            return '[' + str(self.categoryName) + str(self.leftChild) + str(self.rightChild) + ']'
