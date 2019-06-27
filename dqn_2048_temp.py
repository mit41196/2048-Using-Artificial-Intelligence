import random
import numpy as np
from collections import deque
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
import gym
import gym_2048
import tensorflow as tf
from keras import backend as k
import h5py

'''
References (Huber Loss):

https://en.wikipedia.org/wiki/Huber_loss
https://www.tensorflow.org/api_docs/python/tf/losses/huber_loss
'''


def loss(y_true, y_pred, clip_delta=1.0):
    error = y_true - y_pred
    cond = k.abs(error) <= clip_delta

    squared_loss = 0.5 * k.square(error)
    quadratic_loss = 0.5 * k.square(clip_delta) + clip_delta * (k.abs(error) - clip_delta)

    return k.mean(tf.where(cond, squared_loss, quadratic_loss))


def remember(states, actions, rewards, next_states, finish):
    memory.append((states, actions, rewards, next_states, finish))


def act(states):
    if np.random.rand() <= epsilon:
        return random.randrange(action_size)
    act_values = model.predict(states)
    return np.argmax(act_values[0])


def replay(batch_sizes, epsilon):

    minibatch = random.sample(memory, batch_sizes)
    for states, actions, rewards, next_states, finish in minibatch:
        target = model.predict(states)
        if finish:
            target[0][actions] = rewards
        else:
            t = model.predict(next_states)[0]
            target[0][actions] = reward + gamma * np.amax(t)

        model.fit(states, target, epochs=1, verbose=0)

    epsilon = epsilon - epsilon_decay
    return epsilon


EPISODES = 50
env = gym.make('2048-v0')
h5py.File('./save/dqn_2048.h5', 'a')

state_size = 16
action_size = env.action_space.n
memory = deque(maxlen=25000)
gamma = 0.7
epsilon = 1.0
learning_rate = 0.6
epsilon_decay = 0.3

done = False
batch_size = 32
max_element = 0


model = Sequential()
model.add(Dense(48, input_dim=state_size, activation='relu'))
model.add(Dense(48, activation='relu'))
model.add(Dense(24, activation='tanh'))
model.add(Dense(24, activation='relu'))
model.add(Dense(action_size, activation='linear'))
model.compile(loss=loss,
              optimizer=Adam(lr=learning_rate))

model.set_weights(model.get_weights())

for e in range(EPISODES):

    state = env.reset()
    state = np.reshape(state, [1, state_size])
    counter = 0
    for time in range(1000):
        env.render()
        action = act(state)
        next_state, reward, done, info = env.step(action)

        next_state = np.reshape(next_state, [1, state_size])
        remember(state, action, reward, next_state, done)
        state = next_state

        if done:
            model.set_weights(model.get_weights())
            break

        if len(memory) > batch_size:
            epsilon = replay(batch_size, epsilon)

        if e % 10 == 0:
            model.save_weights("./save/dqn_2048.h5")
        max_element = max(max_element, np.max(next_state))
        counter += 1

print('final', max_element)
