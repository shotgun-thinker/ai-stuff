import math
from typing import List, Dict, Optional

from tictactoe.mtree import MTree, State


class Controller:
    def __init__(self):
        # The root of whole tree. Its state is corresponding to an empty board.
        # As a root node, it does not have a parent node.
        self.root = MTree(State([0] * 9), None)

        # Reflection about State and node in MTree.
        self.nodes: Dict[State, MTree] = {}

        # exploration coefficient
        self.ec = 0

    def addState(self, state: State, node: MTree):
        """
        Add a state.
        """
        self.nodes[state] = node

    def getPromisingAction(self, state: State, depth: int = 0):
        """
        Get the promising action on specified state.
        :param state: specified state
        :param depth: the number of simulations before providing an action
        """
        while depth > 0:
            self.simulate(state)
            depth -= 1

        node: MTree = self.nodes[state]
        if node is None:
            self.simulate(state)
            node = self.nodes[state]

        # Get action with max value
        return self.getActionWithMaxValue(node)

    def simulate(self, state: State):
        if state in self.nodes:
            # Specified state be found in MTree.
            node = self.nodes[state]
        else:
            pass

    def select(self, node: MTree):
        while not node.isLeafNode():
            node = self.selectNext(node)
        return node

    def selectNext(self, node: MTree) -> MTree:
        """
        Select the next node.
        :param node: current node
        :return: next node
        """
        max_evaluation = 0
        selected_node = None
        for action, prop in node.props.items():
            evaluation = prop.value + self.ec * math.sqrt(math.log(prop.visitCount) / math.log(1))
            if max_evaluation < evaluation:
                max_evaluation = evaluation
                selected_node = node.actions[action]
        return selected_node

    def getActionWithMaxValue(self, node: MTree) -> Optional[int, bool]:
        if node.isLeafNode():
            return False

        props = node.props
        max_value = -1
        max_value_action = -1
        for action, prop in props.items():
            value = prop.value
            if max_value < value:
                max_value = value
                max_value_action = action

        return max_value_action
