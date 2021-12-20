# Dilemma

## Prison's Dilemma

| A \ B          | B stays silent | B betrays |
| -------------- | -------------- | --------- |
| A stays silent | -1, -1         | -3, 0     |
| A betrays      | 0, -3          | -2, -2    |

Use reinforcement learning to solve this problem. For each person, there are only two actions, which are "stays silent" and "betrays", mark them as "action 0" and "action 1", denote actions vector $a=(0,1)$ , we modify the payoff matrix to the following:

| A \ B | B: 0   | B: 1   |
| ----- | ------ | ------ |
| A: 0  | -1, -1 | -3, 0  |
| A: 1  | 0, -3  | -2, -2 |

We define $Y=(y_1,y_2)$ to index each action. Probability of choosing an action calculated by softmax function. 
$$
\sigma(z)_i=\frac{e^{y_i}}{e^{y_1}+e^{y_2}}
$$
At the beginning, $y=(0.5, 0.5)$, which means the probability for each choice is equal. After each simulation, we adjust $Y$ by rewards. If we select $i$ as action and get an $r$ reward, we update $y_i$ by:
$$
y_i \leftarrow \frac{N*(y_i)+r}{N+1}
$$
where $N$ denotes the number of simulations. 