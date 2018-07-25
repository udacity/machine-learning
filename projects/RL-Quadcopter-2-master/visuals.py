#
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N

def plotbest(agent, task):
    labels = ['time', 'x', 'y', 'z', 'rotor_speed1', 'rotor_speed2', 'rotor_speed3', 'rotor_speed4']
    results = {x : [] for x in labels}
    state = agent.reset_episode()
    while True:
        rotor_speeds = agent.act(state)
        next_state, reward, done = task.step(rotor_speeds)
        agent.step(rotor_speeds, reward, next_state, done)
        state = next_state
        agent.total_reward += reward
        to_write = [task.sim.time] + list(task.sim.pose[:3]) + list(rotor_speeds)
        for ii in range(len(labels)):
            results[labels[ii]].append(to_write[ii])
        if done: break
    plt.plot(results['time'], results['x'], 'X-', color='green', markersize=6, linewidth=1.0, label='x')
    plt.plot(results['time'], results['y'], 'o-', color='blue', markersize=6, linewidth=1.0, label='y')
    plt.plot(results['time'], results['z'], '-', color='red', label='z')
    plt.legend()
    _ = plt.show()

def plot_conclusion(agent, task, episodes, total_rewards, best_rewards, N=10):
    labels = ['time', 'x', 'y', 'z', 'rotor_speed1', 'rotor_speed2', 'rotor_speed3', 'rotor_speed4']
    results = {x : [] for x in labels}
    state = agent.reset_episode()
    while True:
        rotor_speeds = agent.act(state)
        next_state, reward, done = task.step(rotor_speeds)
        agent.step(rotor_speeds, reward, next_state, done)
        state = next_state
        agent.total_reward += reward
        to_write = [task.sim.time] + list(task.sim.pose[:3]) + list(rotor_speeds)
        for ii in range(len(labels)):
            results[labels[ii]].append(to_write[ii])
        if done: break

    plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
    plt.subplot(1,2,1)
    plt.plot(results['time'], results['x'], 'X-', color='green', markersize=6, linewidth=1.0, label='x')
    plt.plot(results['time'], results['y'], 'o-', color='blue', markersize=6, linewidth=1.0, label='y')
    plt.plot(results['time'], results['z'], '-', color='red', label='z')
    plt.legend()

    mean_rewards = running_mean(total_rewards, N)
    plt.subplot(1,2,2)
    plt.plot(episodes[-len(mean_rewards):], mean_rewards, color='blue', label='Running mean rewards')
    plt.plot(episodes, total_rewards, color='grey', label='Total rewards')
    plt.plot(episodes, best_rewards, color='orange', label='Best rewards')
    plt.xlabel('Episodes')
    plt.ylabel('Total Rewards')
    plt.legend()
    _ = plt.show()

def plot_results_all(results, episodes, total_rewards, best_rewards, best_index):
    best = pd.DataFrame(results)
    results = best[best.Episode_index==best_index]
    plt.subplots(nrows=6, ncols=4, figsize=(16, 28))
    plt.subplot(6,4,1)
    plt.plot(results['time'], results['x'], label='x')
    plt.legend()
    plt.subplot(6,4,2)
    plt.plot(results['time'], results['y'], label='y')
    plt.legend()
    plt.subplot(6,4,3)
    plt.plot(results['time'], results['z'], label='z')
    plt.legend()
    plt.subplot(6,4,5)
    plt.plot(results['time'], results['x_velocity'], label='x_velocity')
    plt.legend()
    plt.subplot(6,4,6)
    plt.plot(results['time'], results['y_velocity'], label='y_velocity')
    plt.legend()
    plt.subplot(6,4,7)
    plt.plot(results['time'], results['z_velocity'], label='z_velocity')
    plt.legend()
    plt.subplot(6,4,9)
    plt.plot(results['time'], results['phi'], label='phi')
    plt.legend()
    plt.subplot(6,4,10)
    plt.plot(results['time'], results['theta'], label='theta')
    plt.legend()
    plt.subplot(6,4,11)
    plt.plot(results['time'], results['psi'], label='psi')
    plt.legend()
    plt.subplot(6,4,13)
    plt.plot(results['time'], results['phi_velocity'], label='phi_velocity')
    plt.legend()
    plt.subplot(6,4,14)
    plt.plot(results['time'], results['theta_velocity'], label='theta_velocity')
    plt.legend()
    plt.subplot(6,4,15)
    plt.plot(results['time'], results['psi_velocity'], label='psi_velocity')
    plt.legend()
    plt.subplot(6,4,17)
    plt.plot(results['time'], results['rotor_speed1'], label='Rotor 1 revolutions / second')
    plt.legend()
    plt.subplot(6,4,18)
    plt.plot(results['time'], results['rotor_speed2'], label='Rotor 2 revolutions / second')
    plt.legend()
    plt.subplot(6,4,19)
    plt.plot(results['time'], results['rotor_speed3'], label='Rotor 3 revolutions / second')
    plt.legend()
    plt.subplot(6,4,20)
    plt.plot(results['time'], results['rotor_speed4'], label='Rotor 4 revolutions / second')
    plt.legend()
    plt.subplot(6,4,21)
    plt.plot(episodes, total_rewards, label='Total Rewards')
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.legend()
    plt.subplot(6,4,22)
    plt.plot(episodes, best_rewards, label='Best Rewards')
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.legend()
    _ = plt.show()


