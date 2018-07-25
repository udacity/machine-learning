#
import csv

def save_results(task, agent, num_episodes):
    file_output = 'data.txt'
    episodes = []
    total_rewards = []
    best_rewards = []
    best_index = 1
    labels = ['Episode_index', 'time', 'x', 'y', 'z', 'phi', 'theta', 'psi', 'x_velocity',
              'y_velocity', 'z_velocity', 'phi_velocity', 'theta_velocity',
              'psi_velocity', 'rotor_speed1', 'rotor_speed2', 'rotor_speed3', 'rotor_speed4']
    results = {x : [] for x in labels}

    with open(file_output, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(labels)
        for i_episode in range(1, num_episodes+1):
            state = agent.reset_episode()
            while True:
                rotor_speeds = agent.act(state)
                next_state, reward, done = task.step(rotor_speeds)
                agent.step(rotor_speeds, reward, next_state, done)
                state = next_state
                agent.total_reward += reward
                to_write = [i_episode] + [task.sim.time] + list(task.sim.pose) + list(task.sim.v) + list(task.sim.angular_v) + list(rotor_speeds)
                writer.writerow(to_write)
                for ii in range(len(labels)):
                    results[labels[ii]].append(to_write[ii])
                if done:
                    if agent.total_reward >= agent.best_reward:
                        agent.best_reward = agent.total_reward
                        best_index = i_episode

                        print("\n======== Saving model weights with best reward = {:.2f} ========".format(agent.best_reward))
                        agent.actor_local.model.save_weights("actor_local.h5", overwrite=True)
                        agent.actor_target.model.save_weights("actor_target.h5", overwrite=True)
                        agent.critic_local.model.save_weights("critic_local.h5", overwrite=True)
                        agent.critic_target.model.save_weights("critic_target.h5", overwrite=True)

                    print('\rEpisode {} completed. Score = {:7.3f} (best = {:7.3f})'.format(i_episode, agent.total_reward, agent.best_reward), end="")
                    total_rewards.append(agent.total_reward)
                    best_rewards.append(agent.best_reward)
                    episodes.append(i_episode)
                    break
    return (results, episodes, total_rewards, best_rewards, best_index)
