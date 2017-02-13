import numpy as np

class dependent_bandit():
    def __init__(self, difficulty):
        self.num_actions = 2
        self.difficulty = difficulty
        self.reset()

    def set_restless_prob(self):
        self.bandit = np.array([self.restless_list[self.timestep], 1 - self.restless_list[self.timestep]])

    def reset(self):
        self.timestep = 0
        if self.difficulty == 'restless':
            variance = np.random.uniform(0, .5)
            self.restless_list = np.cumsum(np.random.uniform(-variance, variance, (150, 1)))
            self.restless_list = (self.restless_list - np.min(self.restless_list)) / (
            np.max(self.restless_list - np.min(self.restless_list)))
            self.set_restless_prob()
        if self.difficulty == 'easy': bandit_prob = np.random.choice([0.9, 0.1])
        if self.difficulty == 'medium': bandit_prob = np.random.choice([0.75, 0.25])
        if self.difficulty == 'hard': bandit_prob = np.random.choice([0.6, 0.4])
        if self.difficulty == 'uniform': bandit_prob = np.random.uniform()
        if self.difficulty != 'independent' and self.difficulty != 'restless':
            self.bandit = np.array([bandit_prob, 1 - bandit_prob])
        else:
            self.bandit = np.random.uniform(size=2)

    def pullArm(self, action):
        # Get a random number.
        if self.difficulty == 'restless': self.set_restless_prob()
        self.timestep += 1
        bandit = self.bandit[action]
        result = np.random.uniform()
        if result < bandit:
            # return a positive reward.
            reward = 1
        else:
            # return a negative reward.
            reward = 0
        if self.timestep > 99:
            done = True
        else:
            done = False
        return reward, done, self.timestep

    def pullArmForTest(self):
        # Get a random number.
        optimal_action = np.argmax(self.bandit)
        bandit = self.bandit[optimal_action]
        result = np.random.uniform()
        if result < bandit:
            # return a positive reward.
            optimal_reward = 1
        else:
            # return a negative reward.
            optimal_reward = 0
        return optimal_reward

    def get_optimal_arm(self):
        return np.argmax(self.bandit)


class dependent_bandit2():
    def __init__(self):
        self.num_actions = 11
        self.reset()

    def set_restless_prob(self):
        self.bandit = np.array([self.restless_list[self.timestep], 1 - self.restless_list[self.timestep]])

    def reset(self):
        self.timestep = 0
        self.bandit_target_arm = np.random.choice([range(10)])

    def pullArm(self, action):
        # Get a random number.
        self.timestep += 1
        if action == 10:
            #pull informative arm
            reward = self.bandit_target_arm / 10
        elif action == self.bandit_target_arm:
            reward = 5
        else:
            reward = 1

        if self.timestep > 99:
            done = True
        else:
            done = False
        return reward, done, self.timestep

    def pullArmForTest(self):
        # Get a random number.
        return 5

    def get_optimal_arm(self):
        return self.bandit_target_arm


# env = dependent_bandit("restless")
# print("The probabilities for the arm are: {}".format(env.bandit))
# print("pulling arm 0")
# for i in range(10):
#     r, d, t = env.pullArm(0)
#     print("The probabilities for the arm are: {}".format(env.bandit))
#     print("reward = {}, terminated = {}, timestep = {}".format(r, d, t))
#
# print("pulling arm 1")
# for i in range(10):
#     r, d, t = env.pullArm(1)
#     print("The probabilities for the arm are: {}".format(env.bandit))
#     print("reward = {}, terminated = {}, timestep = {}".format(r, d, t))

