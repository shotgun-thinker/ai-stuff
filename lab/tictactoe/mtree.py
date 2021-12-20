import math
import random
from typing import List, Dict, Optional

from tictactoe.game import Game


class MTree:
    """
    Tree for Monte-Carlo Tree Search.
    """

    visit = 0

    def __init__(self, state: List[int], parent=None):
        # Marked as the State of current node. State in MCTS is bijection to the complete picture of board.
        self.state: List[int] = state

        # Parent node of curren node. Used on backpropagation.
        self.parent: Optional[MTree] = parent

        # Child nodes of current node.
        # Dict reflection: action => child node object
        self.childList: Dict[int, MTree] = {}

        # Visit count.
        # Auto increases when being chosen or on backpropagation.
        self.visitCountList: Dict[int, int] = {}

        # Average value of current node.
        # <value> = ∑<single value> / <visits>
        self.valueList: Dict[int, int] = {}

    def getExecutableActions(self):
        ret = []
        for i in range(len(self.state)):
            if self.state[i] == 0:
                ret.append(i)
        return ret

    def isLeafNode(self) -> bool:
        """
        Whether this node is a leaf node.
        """
        return len(self.childList) == 0

    def expand(self, action):
        """
        Extend a node
        """
        executable_actions = self.getExecutableActions()
        if action not in executable_actions:
            return

        state = self.state[:]
        state[action] = ((9 - len(executable_actions)) % 2 - 1) & 1
        self.childList[action] = MTree(state, self)

    def expandAll(self):
        executable_actions = self.getExecutableActions()
        player = ((9 - len(executable_actions)) % 2 - 1) & 1

        for action in executable_actions:
            state = self.state[:]
            state[action] = player
            self.childList[action] = MTree(state, self)

    def simulate(self):
        """
        Monte Carlo Simulation
        """
        if self.isLeafNode():
            # Monte Carlo Simulation from current node
            game = Game(self.state)
            action_stack = []  # record actions
            value = 0  # simulation value
            while game.moves < 9:
                index = random.choice(game.getExecutableIndices())
                action_stack.append(index)
                game.move(index)
                if game.isWin():
                    # return 1 if "X" player wins, -1 otherwise
                    value = (-(game.moves() % 2)) & 1
                    break

            # back propagation
            node = self
            while node.parent is not None:
                node = node.parent
                action = action_stack.pop()
        else:
            # not a leaf node, recursively selects a node
            self.childList[self.select()].simulate()

    def select(self):
        # get the max score of actions
        score_list = {}
        for action in self.childList:
            score_list[action] = self.valueList[action] + math.sqrt(
                math.log(MTree.visit) / math.log(self.visitCountList[action]))
        max_score = max(score_list.values())

        # choose an action from the actions set
        candidate = []
        for action, score in score_list.items():
            if score == max_score:
                candidate.append(action)
        return random.choice(candidate)
