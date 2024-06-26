import numpy as np
import matplotlib.pyplot as plt
import gym #library for reinforcement problems
from gym import spaces
import time

class GridEnv(gym.Env):
    metadata = { 'render.modes': [] }
    
    def __init__(self):
        self.observation_space = spaces.Discrete(25)
        self.action_space = spaces.Discrete(4)
        self.done = False
        
    def reset(self):
        
        self.done = False
        self.state = np.zeros((5,5))
        self.agent_pos = [0, 0]
        self.goal_pos = [4,4]        
        self.extra_rew1_pos = [1,3] 
        self.extra_rew2_pos = [3,2] 
        self.penal1_pos = [2,1] 
        self.penal2_pos = [2,4] 
        self.state[tuple(self.agent_pos)] = 1
        self.state[tuple(self.goal_pos)] = 0.8
        self.state[tuple(self.extra_rew1_pos)] = 0.7
        self.state[tuple(self.extra_rew1_pos)] = 0.7
        self.state[tuple(self.extra_rew1_pos)] = 0.3
        self.state[tuple(self.extra_rew1_pos)] = 0.3
        observation = self.state.flatten()        



        return observation
    
    def step(self, action):

        self.state = np.random.choice(self.observation_space.n)
        if action == 0:
          self.agent_pos[0] += 1
        if action == 1:
          self.agent_pos[0] -= 1
        if action == 2:
          self.agent_pos[1] += 1
        if action == 3:
          self.agent_pos[1] -= 1
          
        self.agent_pos = np.clip(self.agent_pos, 0, 4)
        self.state = np.zeros((5,5))
        self.state[tuple(self.agent_pos)] = 1
        self.state[tuple(self.goal_pos)] = 3
        self.state[tuple(self.extra_rew1_pos)] = 2
        self.state[tuple(self.extra_rew2_pos)] = 2
        self.state[tuple(self.penal1_pos)] = 4
        self.state[tuple(self.penal2_pos)] = 4
        observation = self.state.flatten()
        
        reward = 0
        if (self.agent_pos == self.goal_pos).all():
          reward = 20 
          self.done = True

        elif (self.agent_pos == self.extra_rew1_pos).all():
            reward = +5 

        elif (self.agent_pos == self.extra_rew2_pos).all():
            reward = 15 
        elif (self.agent_pos == self.penal1_pos).all():
            reward = -8 

        elif (self.agent_pos == self.penal2_pos).all():
            reward = -12 
        
        return self.agent_pos, reward, self.done

    def render(self):
        plt.imshow(self.state)
        plt.show()

env = GridEnv()
total_reward=0
observation = env.reset()
for _ in range(10):
    action = env.action_space.sample() 
    observation, reward, done = env.step(action) 
    total_reward = total_reward + reward
    print('State: {} Action : {} Reward: {}'.format(observation,action,total_reward))
    env.render()

#Hyperparameter:
epsilon = 0.75
total_episodes = 5000
max_timesteps = 20
alpha = 0.85
gamma = 0.75
avg_timesteps=0
decay_factor = (0.01/1)**(1/total_episodes)
det_epsilon = 0.99 
all_action=[0,1,2,3]
allstates = {(0,0): 0, (0,1): 1, (0,2): 2, (0,3): 3, (0,4): 4,
              (1,0): 5, (1,1): 6, (1,2): 7, (1,3): 8, (1,4): 9,
                (2,0): 10, (2,1): 11, (2,2): 12, (2,3): 13, (2,4): 14,
                  (3,0): 15, (3,1): 16, (3,2): 17, (3,3): 18, (3,4): 19,
                    (4,0): 20, (4,1): 21, (4,2): 21, (4,3): 23, (4,4): 24,}


Q=np.zeros((25,4))

#Functions to choose  greedy action and Q_value following SARSA Algorithm
def greedy_algo(all_action,state1):
  action=0
  if np.random.uniform(0, 1) < epsilon:
      action = env.action_space.sample()
  else:
      action = np.argmax(Q[state1, :])
  return action
  


def Q_update(state1,action1,reward,state2,action2):
  new_value = Q[state1][action1] + alpha*(reward + gamma*Q[state2][action2] - Q[state1][action1])
  return new_value

rewar_tot= []
total_timesteps = []
epsilon_values = []

for i in range(1, total_episodes+1 ):
  env.reset() 
  state1=0
  action1=greedy_algo(all_action, state1)
  total_rewards = 0
  t = 0
  while t<max_timesteps:

    
    if det_epsilon < np.random.uniform(0, 1):
      state2_pos, reward, done = env.step(action)
      state2 = allstates[tuple(state2_pos)]
      action2=greedy_algo(action1,state2)

      Q_update(state1,action1,reward,state2,action2)

      state1=state2
      action1=action2
    
      t += 1
      total_rewards += total_rewards

      if done:
        break
  rewar_tot.append(total_rewards)
  total_timesteps.append(t)

  if epsilon > 0.01: 
    epsilon = epsilon*decay_factor
  else:
    epsilon = 0.01
  epsilon_values.append(epsilon) 

x = [episode for episode in range(total_episodes)]
y_reward = rewar_tot
y_epsilon = epsilon_values

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4))
ax1.plot(x, y_epsilon)
ax1.set_title("Epsilon decay")

#episodes vs rewards
ax2.plot(x,y_reward)
ax2.set_title("Rewards per episode")

