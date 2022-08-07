from common import *
#################################################################
# Tree data structure for min-max functions
#################################################################

class Node:
    def __init__(self, temp_board):
        self.temp_board = temp_board
        self.parent = None
        self.children = []
        self.direction = INVALID
        self.score = LOW
        self.name = "ROOT"

class MinmaxTree:

    def create_node(self, temp_board):
        return Node(temp_board)

    def insert_node(self, node, temp_board, name="INVALID", direction=DOWN, score=LOW):
        if node is None:
            return self.create_node(temp_board)

        temp_node = Node(temp_board)
        temp_node.parent = node
        temp_node.direction = direction
        temp_node.score = score
        temp_node.name = node.name + "_" + name
        node.children.append(temp_node)

        return node

    def print_nodes(self, node):
        #print(node.name)
        for n in node.children:
            print(node.name + "'s Child:" + str(n.name) + " 's score: " + str(n.score))
            if len(n.children) > 0:
                self.print_nodes(n)

    def find_node(self, root, temp_board):
        for n in root.children:
            if n.temp_board == temp_board:
                return n
            if len(n.children) > 0:
                self.find_node(n, temp_board)

    def get_max_node(self, root, max_score, max_node=None):
        if (root.name != "ROOT" and root.direction != INVALID) or root.name == "ROOT":
            for n in root.children:
                if n.score > max_score:
                    max_score = n.score
                    max_node = n
                if n.direction != INVALID and len(n.children) > 0:
                    max_node = self.get_max_node(n, max_score, max_node)
        return max_node

    def get_best_direction(self, max_node):

        if max_node is None:
            return INVALID
        if max_node.parent.name == "ROOT":
            return max_node.direction
        return self.get_best_direction(max_node.parent)

def main():
    root = None
    tree = MinmaxTree()
    root = tree.insert_node(root, board)
    #tree.print_nodes(root)
    new_board = [1]*16
    board_2 = [2]*16
    board_3 = [3]*16
    board_4 = [4]*16
    tree.insert_node(root, new_board, "UP", UP, 1000)
    tree.insert_node(root, board_2, "DOWN")
    tree.insert_node(root, board_3, "RIGHT")
    tree.insert_node(tree.find_node(root, board_2), board_4, "LEFT", LEFT, 500)
    tree.print_nodes(root)
    max_node = tree.get_max_node(root, LOW)
    direction = tree.get_best_direction(max_node)
    print(direction)


if __name__ == "__main__":
    main()


