import random
from mesa import Agent

class ParentAgent(Agent):
    def __init__(self, unique_id, model, education_level, initial_time_investment, strategy=None, threshold=10):
        super().__init__(unique_id, model)
        self.education_level = education_level
        self.strategy = strategy
        self.time_investment = initial_time_investment
        self.child_outcome_score = 0
        self.threshold = threshold
        self.num_switches = 0  # Counter for strategy switches

    def step(self):
        if self.strategy == "Individual Learning":
            self.update_time_investment()
        elif self.strategy == "Copying the highest-scoring neighbor":
            self.copy_highest_scoring_neighbor()
        elif self.strategy == "Copying the most frequently observed strategy":
            self.copy_most_frequent_strategy()
        elif self.strategy == "Copying randomly":
            self.copy_randomly()
        self.calculate_child_outcome_score()
        self.check_and_switch_strategy()

    def copy_highest_scoring_neighbor(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        best_neighbor = max(neighbors, key=lambda a: a.child_outcome_score, default=None)
        if best_neighbor and best_neighbor.child_outcome_score > self.child_outcome_score:
            self.time_investment = best_neighbor.time_investment

    def copy_most_frequent_strategy(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        neighbor_investments = [neighbor.time_investment for neighbor in neighbors]
        if neighbor_investments:
            most_frequent_investment = max(set(neighbor_investments), key=neighbor_investments.count)
            self.time_investment = most_frequent_investment

    def copy_randomly(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        if neighbors:
            random_neighbor = random.choice(neighbors)
            self.time_investment = random_neighbor.time_investment

    def update_time_investment(self):
        pass  # Individual learners keep their time investment the same

    def calculate_child_outcome_score(self):
        optimal_time = self.model.optimal_time_investment
        discrepancy = abs(self.time_investment - optimal_time)
        if discrepancy <= 10:
            self.child_outcome_score = 20
        else:
            self.child_outcome_score = 0

    def check_and_switch_strategy(self):
        optimal_time = self.model.optimal_time_investment
        discrepancy = abs(self.time_investment - optimal_time)
        
        if discrepancy > self.threshold:
            switch_probability = getattr(self.model, f"{self.education_level.lower()}_switch_probability")
            if random.random() < switch_probability:
                self.num_switches += 1  # Increment the counter for strategy switches
                if self.strategy == "Individual Learning":
                    strategy_ratios = getattr(self.model, f"{self.education_level.lower()}_social_strategy_ratios")
                    total_ratio = sum(strategy_ratios.values())
                    
                    # Check for zero total_ratio
                    if total_ratio == 0:
                        return
                    
                    choice_weights = [
                        strategy_ratios['highest'] / total_ratio,
                        strategy_ratios['most_frequent'] / total_ratio,
                        strategy_ratios['random'] / total_ratio
                    ]
                    self.strategy = random.choices(self.model.social_learning_strategies, weights=choice_weights, k=1)[0]
                else:
                    self.strategy = "Individual Learning"
