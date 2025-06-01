
# abs_engine.py
# Adaptive Bayesian Simulation (ABS) Core Engine

import numpy as np
import pandas as pd
from collections import Counter

class ABSEngine:
    def __init__(self, main_range=50, star_range=12, draws=100000):
        self.main_range = main_range
        self.star_range = star_range
        self.draws = draws
        self.main_priors = np.ones(main_range) / main_range
        self.star_priors = np.ones(star_range) / star_range
        self.results = []

    def load_draw_history(self, df):
        balls = df[[f'Ball {i}' for i in range(1,6)]].values.flatten()
        stars = df[[f'Lucky Star {i}' for i in range(1,3)]].values.flatten()

        ball_counts = Counter(balls)
        star_counts = Counter(stars)

        self.main_priors = np.array([ball_counts.get(i+1, 0)+1 for i in range(self.main_range)])
        self.main_priors = self.main_priors / self.main_priors.sum()

        self.star_priors = np.array([star_counts.get(i+1, 0)+1 for i in range(self.star_range)])
        self.star_priors = self.star_priors / self.star_priors.sum()

    def simulate_draws(self):
        simulations = []
        for _ in range(self.draws):
            main = np.random.choice(range(1, self.main_range+1), size=5, replace=False, p=self.main_priors)
            star = np.random.choice(range(1, self.star_range+1), size=2, replace=False, p=self.star_priors)
            simulations.append((tuple(sorted(main)), tuple(sorted(star))))
        self.results = simulations

    def get_top_combinations(self, top_n=5):
        from collections import Counter
        counts = Counter(self.results)
        return counts.most_common(top_n)

    def evaluate_prediction(self, prediction, actual):
        main_hit = len(set(prediction[0]) & set(actual[0]))
        star_hit = len(set(prediction[1]) & set(actual[1]))
        return main_hit, star_hit

    def score_all_predictions(self, actual_draws):
        scores = []
        for pred in self.results:
            for actual in actual_draws:
                scores.append(self.evaluate_prediction(pred, actual))
        return scores
