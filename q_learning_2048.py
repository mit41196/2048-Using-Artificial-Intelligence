import math
import random
import copy
import gym
import gym_2048

env = gym.make("2048-v0")

env.render()


def select(state):
    action = 0
    max1 = -math.inf
    for i in range(4):
        if state[i] >= max1:
            max1 = state[i]
            action = i
    return action


def maxval(state):
    max1 = -math.inf
    for i in range(4):
        if state[i] >= max1:
            max1 = state[i]
    return max1


env.reset()
n, s, j, k = env.step(0)

arr = list(n)

q = [0, 0, 0, 0]
qmatrix = [q]

decay_rate = 0.05
reward = 0
currentstate = []
currentstate = copy.deepcopy(n)
nextstate = []
visited_states = [arr]

x = 1.00
alpha = 0.8
gamma = 0.8

for ep in range(500):
    env.reset()

    for episode in range(1000):
        r = random.uniform(0, 1)
        env.render()

        cs = list(currentstate)
        if r < x:
            move = random.randint(0, 3)

            nextstate, reward, done, info = env.step(move)

        else:
            index1 = visited_states.index(cs)
            move = select(qmatrix[index1])
            nextstate, reward, done, info = env.step(move)

        ns = list(nextstate)
        print(ns, nextstate)
        if ns not in visited_states:
            visited_states.append(ns)
            qmatrix.append([0, 0, 0, 0])

        index1 = visited_states.index(cs)
        index2 = visited_states.index(ns)
        maxv = maxval(qmatrix[index2])
        print(maxv)
        qmatrix[index1][move] = qmatrix[index1][move] + alpha * (reward + gamma * (maxv - qmatrix[index1][move]))
        currentstate = copy.deepcopy(nextstate)
        # if done:
        #     print("done")
        #     break

    x = x - 0.01

for index in range(len(qmatrix)):
    print(qmatrix[index])

print(len(qmatrix))
