# -*- coding: utf-8 -*-

class Node(object):
    # 节点类
    def __init__(self, data = '#', lchild = None, rchild = None):
        self.data = data
        self.lchild = lchild
        self.rchild = rchild

class Tree(Node):
    # 树类
    def __init__(self):
        pass

    def create_tree(self, tree):      # 建树
        data = raw_input('-> ')
        if data == '#':
            tree = None
        else:
            tree.data = data
            tree.lchild = Node()
            self.create_tree(tree.lchild)
            tree.rchild = Node()
            self.create_tree(tree.rchild)
    
    def visit(self, tree):        # 访问树的各个节点
        if tree.data is not '#':
            print str(tree.data) + '\t',
    
    def pre_order(self, tree):      # 前序遍历
        if tree is not None:
            self.visit(tree)
            self.pre_order(tree.lchild)
            self.pre_order(tree.rchild)

    def mid_order(self, tree):      #中序遍历
        if tree is not None:
            self.mid_order(tree.lchild)
            self.visit(tree)
            self.mid_order(tree.rchild)
    
    def pos_order(self, tree):      # 后续遍历
        if tree is not None:
            self.pos_order(tree.lchild)
            self.pos_order(tree.rchild)
            self.visit(tree)

if __name__ == '__main__':
    t = Node()
    tree = Tree()
    tree.create_tree(t)
    tree.pre_order(t)
    print ('\n')
    tree.mid_order(t)
    print('\n')
    tree.pos_order(t)
    print('\n')