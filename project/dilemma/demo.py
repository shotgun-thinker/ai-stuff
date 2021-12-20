import numpy as np


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def generate_by_distribution(prob):
    return np.random.choice(np.arange(2), 1, p=prob)[0]


class Person():
    def __init__(self):
        self.y = [0.5, 0.5]

    def select(self):
        prob = softmax(self.y)
        return generate_by_distribution(prob)

    def update(self, selection, reward):
        N = Experiment.N
        self.y[selection] = (self.y[selection] * N + reward) / (N + 1)


class Experiment():
    N = 0

    payoff = [
        [[-1, -1], [-3, 0]],
        [[0, -3], [-2, -2]]
    ]

    def __init__(self):
        self.git = Person()
        self.angel = Person()

    def simulation(self):
        Experiment.N += 1

        # get selections
        git_selection = self.git.select()
        angel_selection = self.angel.select()

        # distribute rewards
        git_reward, angel_reward = self.reward(git_selection, angel_selection)

        # update y by rewards
        self.git.update(git_selection, git_reward)
        self.angel.update(angel_selection, angel_reward)

    def reward(self, *selection):
        return tuple(Experiment.payoff[selection[0]][selection[1]])

    def run(self, times):
        for i in range(times):
            self.simulation()

        # print
        git_prop = softmax(self.git.y)
        angle_prop = softmax(self.angel.y)
        prob_1 = round(((git_prop[0] + angle_prop[0]) / 2) * 100, 2)
        prob_2 = round(((git_prop[1] + angle_prop[1]) / 2) * 100, 2)
        print(f"probability for choosing \"stays silent\" option: {prob_1}%")
        print(f"probability for choosing \"betrays\" option: {prob_2}%")


for i in [10, 100, 1000, 10000]:
    print(f"[{i} simulations]")
    experiment = Experiment()
    experiment.run(i)
