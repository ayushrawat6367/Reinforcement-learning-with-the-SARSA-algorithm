Reinforcement Learning with the SARSA Algorithm
This project implements a simple reinforcement learning environment using the SARSA (State-Action-Reward-State-Action) algorithm. The environment is a grid-based world where an agent navigates from a start position to a goal, collecting rewards or penalties along the way.

Project Overview
Environment
The environment consists of a 5x5 grid with the following features:

The agent starts at the top-left corner of the grid.
The goal is located at the bottom-right corner.
There are two positions that provide extra rewards and two positions that incur penalties.
Agent Actions
The agent can take one of four actions:

Move up
Move down
Move left
Move right

Rewards and Penalties:
Reaching the goal: +20 points (ends the episode)
Collecting extra rewards: +5 or +15 points
Hitting a penalty position: -8 or -12 points



Python Libraries required:

NumPy
Matplotlib
Gym
