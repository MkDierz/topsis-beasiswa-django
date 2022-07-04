import numpy as np


class Topsis:
    evaluation_matrix = np.array([])  # Matrix
    weighted_normalized = np.array([])  # Weight matrix
    normalized_decision = np.array([])  # Normalisation matrix
    M = 0  # Number of rows
    N = 0  # Number of columns

    def __init__(self, evaluation_matrix, weight_matrix, criteria):
        # M×N matrix
        self.evaluation_matrix = np.array(evaluation_matrix, dtype="float")

        # M alternatives (options)
        self.row_size = len(self.evaluation_matrix)

        # N attributes/criteria
        self.column_size = len(self.evaluation_matrix[0])

        # N size weight matrix
        self.weight_matrix = np.array(weight_matrix, dtype="float")
        self.weight_matrix = self.weight_matrix / sum(self.weight_matrix)
        self.criteria = np.array(criteria, dtype="float")

    def step_2(self):
        # normalized scores
        self.normalized_decision = np.copy(self.evaluation_matrix)
        sqrd_sum = np.zeros(self.column_size)
        for i in range(self.row_size):
            for j in range(self.column_size):
                sqrd_sum[j] += self.evaluation_matrix[i, j] ** 2
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.normalized_decision[i, j] = self.evaluation_matrix[i, j] / (
                    sqrd_sum[j] ** 0.5
                )

    def step_3(self):

        self.weighted_normalized = np.copy(self.normalized_decision)
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.weighted_normalized[i, j] *= self.weight_matrix[j]

    def step_4(self):
        self.worst_alternatives = np.zeros(self.column_size)
        self.best_alternatives = np.zeros(self.column_size)
        for i in range(self.column_size):
            if self.criteria[i]:
                self.worst_alternatives[i] = min(self.weighted_normalized[:, i])
                self.best_alternatives[i] = max(self.weighted_normalized[:, i])
            else:
                self.worst_alternatives[i] = max(self.weighted_normalized[:, i])
                self.best_alternatives[i] = min(self.weighted_normalized[:, i])

    def step_5(self):
        self.worst_distance = np.zeros(self.row_size)
        self.best_distance = np.zeros(self.row_size)

        self.worst_distance_mat = np.copy(self.weighted_normalized)
        self.best_distance_mat = np.copy(self.weighted_normalized)

        for i in range(self.row_size):
            for j in range(self.column_size):
                self.worst_distance_mat[i][j] = (
                    self.weighted_normalized[i][j] - self.worst_alternatives[j]
                ) ** 2
                self.best_distance_mat[i][j] = (
                    self.weighted_normalized[i][j] - self.best_alternatives[j]
                ) ** 2

                self.worst_distance[i] += self.worst_distance_mat[i][j]
                self.best_distance[i] += self.best_distance_mat[i][j]

        for i in range(self.row_size):
            self.worst_distance[i] = self.worst_distance[i] ** 0.5
            self.best_distance[i] = self.best_distance[i] ** 0.5

    def step_6(self):
        np.seterr(all="ignore")
        self.worst_similarity = np.zeros(self.row_size)
        self.best_similarity = np.zeros(self.row_size)

        for i in range(self.row_size):
            # calculate the similarity to the worst condition
            self.worst_similarity[i] = self.worst_distance[i] / (
                self.worst_distance[i] + self.best_distance[i]
            )

            # calculate the similarity to the best condition
            self.best_similarity[i] = self.best_distance[i] / (
                self.worst_distance[i] + self.best_distance[i]
            )

    def ranking(self, data):
        return [i + 1 for i in data.argsort()]

    def rank_to_worst_similarity(self):
        # return rankdata(self.worst_similarity, method="min").astype(int)
        return self.ranking(self.worst_similarity)

    def rank_to_best_similarity(self):
        # return rankdata(self.best_similarity, method='min').astype(int)
        return self.ranking(self.best_similarity)

    def calc(self):
        # print("Step 1\n", self.evaluation_matrix, end="\n\n")
        self.step_2()
        # print("Step 2\n", self.normalized_decision, end="\n\n")
        self.step_3()
        # print("Step 3\n", self.weighted_normalized, end="\n\n")
        self.step_4()
        # print("Step 4\n", self.worst_alternatives, self.best_alternatives, end="\n\n")
        self.step_5()
        # print("Step 5\n", self.worst_distance, self.best_distance, end="\n\n")
        self.step_6()
        # print("Step 6\n", self.worst_similarity, self.best_similarity, end="\n\n")
