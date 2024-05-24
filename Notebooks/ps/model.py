import random
import networkx as nx
import mesa
from mesa.datacollection import DataCollector
from .agent import ParentAgent

class ParentalLearningModel(mesa.Model):
    def __init__(self, num_agents=40, optimal_time_investment=40,
                 primary_edu_ratio=0.33, primary_edu_level="High",
                 high_individual_learning_ratio=0.7, medium_individual_learning_ratio=0.7, low_individual_learning_ratio=0.7,
                 high_primary_social_ratio=0.5, medium_primary_social_ratio=0.5, low_primary_social_ratio=0.5,
                 high_primary_social_strategy="Copying the highest-scoring neighbor",
                 medium_primary_social_strategy="Copying the highest-scoring neighbor",
                 low_primary_social_strategy="Copying the highest-scoring neighbor",
                 high_threshold=5, medium_threshold=10, low_threshold=15,
                 high_initial_time_investment=30, medium_initial_time_investment=30, low_initial_time_investment=30,
                 high_avg_node_degree=4, medium_avg_node_degree=4, low_avg_node_degree=4,
                 high_rewiring_prob=0.1, medium_rewiring_prob=0.1, low_rewiring_prob=0.1,
                 high_switch_probability=0.1, medium_switch_probability=0.3, low_switch_probability=0.5):
        super().__init__()

        self.num_agents = num_agents

        # Ensure node degrees do not exceed the number of agents
        high_avg_node_degree = min(high_avg_node_degree, num_agents)
        medium_avg_node_degree = min(medium_avg_node_degree, num_agents)
        low_avg_node_degree = min(low_avg_node_degree, num_agents)

        # Assign the individual learning ratios as class attributes
        self.high_individual_learning_ratio = high_individual_learning_ratio
        self.medium_individual_learning_ratio = medium_individual_learning_ratio
        self.low_individual_learning_ratio = low_individual_learning_ratio

        # Assign the primary social ratios as class attributes
        self.high_primary_social_ratio = high_primary_social_ratio
        self.medium_primary_social_ratio = medium_primary_social_ratio
        self.low_primary_social_ratio = low_primary_social_ratio

        # Assign the initial time investment and threshold values as class attributes
        self.high_initial_time_investment = high_initial_time_investment
        self.medium_initial_time_investment = medium_initial_time_investment
        self.low_initial_time_investment = low_initial_time_investment
        self.high_threshold = high_threshold
        self.medium_threshold = medium_threshold
        self.low_threshold = low_threshold

        # Assign the average node degrees
        self.high_avg_node_degree = high_avg_node_degree
        self.medium_avg_node_degree = medium_avg_node_degree
        self.low_avg_node_degree = low_avg_node_degree

        # Assign the switch probabilities
        self.high_switch_probability = high_switch_probability
        self.medium_switch_probability = medium_switch_probability
        self.low_switch_probability = low_switch_probability

        # Separate network graphs for different education levels with varying parameters
        self.high_edu_graph = nx.watts_strogatz_graph(num_agents, high_avg_node_degree, high_rewiring_prob)
        self.medium_edu_graph = nx.watts_strogatz_graph(num_agents, medium_avg_node_degree, medium_rewiring_prob)
        self.low_edu_graph = nx.watts_strogatz_graph(num_agents, low_avg_node_degree, low_rewiring_prob)

        # Create a unified graph
        self.G = nx.Graph()
        self.G.add_nodes_from(self.high_edu_graph.nodes(data=True))
        self.G.add_nodes_from(self.medium_edu_graph.nodes(data=True))
        self.G.add_nodes_from(self.low_edu_graph.nodes(data=True))
        self.G.add_edges_from(self.high_edu_graph.edges(data=True))
        self.G.add_edges_from(self.medium_edu_graph.edges(data=True))
        self.G.add_edges_from(self.low_edu_graph.edges(data=True))

        self.grid = mesa.space.NetworkGrid(self.G)

        self.schedule = mesa.time.RandomActivation(self)
        self.optimal_time_investment = optimal_time_investment

        self.set_education_ratios(primary_edu_ratio, primary_edu_level)
        self.set_social_learning_ratios("High", high_individual_learning_ratio, high_primary_social_ratio, high_primary_social_strategy)
        self.set_social_learning_ratios("Medium", medium_individual_learning_ratio, medium_primary_social_ratio, medium_primary_social_strategy)
        self.set_social_learning_ratios("Low", low_individual_learning_ratio, low_primary_social_ratio, low_primary_social_strategy)

        # Calculate the number of agents for each education level
        num_high_edu = int(num_agents * self.high_edu_ratio)
        num_medium_edu = int(num_agents * self.medium_edu_ratio)
        num_low_edu = int(num_agents * self.low_edu_ratio)

        # Ensure all agents are assigned
        total_assigned_agents = num_high_edu + num_medium_edu + num_low_edu
        remaining_agents = num_agents - total_assigned_agents

        # Distribute any remaining agents randomly among the education levels
        for _ in range(remaining_agents):
            random_choice = random.choice(["High", "Medium", "Low"])
            if random_choice == "High":
                num_high_edu += 1
            elif random_choice == "Medium":
                num_medium_edu += 1
            elif random_choice == "Low":
                num_low_edu += 1

        agent_id = 0
        used_nodes = set()
        social_learning_agents = {"High": [], "Medium": [], "Low": []}

        for education_level, count, graph in [("High", num_high_edu, self.high_edu_graph), 
                                              ("Medium", num_medium_edu, self.medium_edu_graph), 
                                              ("Low", num_low_edu, self.low_edu_graph)]:
            initial_time_investment = getattr(self, f"{education_level.lower()}_initial_time_investment")
            threshold = getattr(self, f"{education_level.lower()}_threshold")
            available_nodes = list(graph.nodes())

            # Determine the number of individual learning agents and social learning agents
            num_individual_learning = round(count * getattr(self, f"{education_level.lower()}_individual_learning_ratio"))
            num_social_learning = count - num_individual_learning

            # Assign individual learning agents
            for _ in range(num_individual_learning):
                node = random.choice(available_nodes)
                while node in used_nodes:
                    node = random.choice(available_nodes)
                used_nodes.add(node)
                strategy = "Individual Learning"
                agent = ParentAgent(agent_id, self, education_level, initial_time_investment, strategy=strategy, threshold=threshold)
                self.grid.place_agent(agent, node)
                self.schedule.add(agent)
                agent_id += 1

            # Assign social learning agents
            for _ in range(num_social_learning):
                node = random.choice(available_nodes)
                while node in used_nodes:
                    node = random.choice(available_nodes)
                used_nodes.add(node)
                strategy_weights = {
                    "highest": self.high_primary_social_ratio if education_level == "High" else self.medium_primary_social_ratio if education_level == "Medium" else self.low_primary_social_ratio,
                    "most_frequent": (1 - self.high_primary_social_ratio) / 2 if education_level == "High" else (1 - self.medium_primary_social_ratio) / 2 if education_level == "Medium" else (1 - self.low_primary_social_ratio) / 2,
                    "random": (1 - self.high_primary_social_ratio) / 2 if education_level == "High" else (1 - self.medium_primary_social_ratio) / 2 if education_level == "Medium" else (1 - self.low_primary_social_ratio) / 2
                }
                strategy = random.choices(
                    ["Copying the highest-scoring neighbor", "Copying the most frequently observed strategy", "Copying randomly"], 
                    weights=[strategy_weights['highest'], strategy_weights['most_frequent'], strategy_weights['random']], k=1
                )[0]
                social_learning_agents[education_level].append(node)
                agent = ParentAgent(agent_id, self, education_level, initial_time_investment, strategy=strategy, threshold=threshold)
                self.grid.place_agent(agent, node)
                self.schedule.add(agent)
                agent_id += 1

        self.datacollector = DataCollector(
            model_reporters={
                "Average Time Investment (High)": lambda m: self.average_time_investment("High"),
                "Average Time Investment (Medium)": lambda m: self.average_time_investment("Medium"),
                "Average Time Investment (Low)": lambda m: self.average_time_investment("Low"),
                "Average Child Outcome Score (High)": lambda m: self.average_child_outcome_score("High"),
                "Average Child Outcome Score (Medium)": lambda m: self.average_child_outcome_score("Medium"),
                "Average Child Outcome Score (Low)": lambda m: self.average_child_outcome_score("Low"),
                "Social Learning Agents(High)": lambda m: self.count_social_learning_agents("High"),
                "Social Learning Agents(Medium)": lambda m: self.count_social_learning_agents("Medium"),
                "Social Learning Agents(Low)": lambda m: self.count_social_learning_agents("Low"),
                "Clustering Coefficient": lambda m: nx.average_clustering(m.G),
                "Average Path Length": lambda m: nx.average_shortest_path_length(m.G) if nx.is_connected(m.G) else float('inf')
            }
        )

        self.discrepancy_thresholds = {"High": high_threshold, "Medium": medium_threshold, "Low": low_threshold}
        self.switch_probabilities = {"High": high_switch_probability, "Medium": medium_switch_probability, "Low": low_switch_probability}
        self.social_learning_strategies = ["Copying the highest-scoring neighbor",
                                           "Copying the most frequently observed strategy",
                                           "Copying randomly"]

        self.running = True
        self.datacollector.collect(self)

    def set_education_ratios(self, primary_ratio, primary_edu_level):
        remaining_ratio = (1 - primary_ratio) / 2
        if primary_edu_level == "High":
            self.high_edu_ratio = primary_ratio
            self.medium_edu_ratio = remaining_ratio
            self.low_edu_ratio = remaining_ratio
        elif primary_edu_level == "Medium":
            self.medium_edu_ratio = primary_ratio
            self.high_edu_ratio = remaining_ratio
            self.low_edu_ratio = remaining_ratio
        elif primary_edu_level == "Low":
            self.low_edu_ratio = primary_ratio
            self.high_edu_ratio = remaining_ratio
            self.medium_edu_ratio = remaining_ratio

    def set_social_learning_ratios(self, education_level, individual_ratio, primary_social_ratio, primary_social_strategy):
        social_ratio = 1 - individual_ratio
        remaining_ratio = (social_ratio - primary_social_ratio) / 2
        strategy_ratios = {
            "highest": primary_social_ratio,
            "most_frequent": remaining_ratio,
            "random": remaining_ratio
        }
        setattr(self, f"{education_level.lower()}_social_strategy_ratios", strategy_ratios)

    def average_time_investment(self, education_level):
        agents = [agent for agent in self.schedule.agents if agent.education_level == education_level]
        if agents:
            return sum(agent.time_investment for agent in agents) / len(agents)
        return 0

    def average_child_outcome_score(self, education_level):
        agents = [agent for agent in self.schedule.agents if agent.education_level == education_level]
        if agents:
            return sum(agent.child_outcome_score for agent in agents) / len(agents)
        return 0
    
    def count_social_learning_agents(self, education_level):
        return sum(1 for agent in self.schedule.agents if agent.education_level == education_level and agent.strategy != "Individual Learning")

    def all_child_outcome_scores_20(self):
        return all(agent.child_outcome_score == 20 for agent in self.schedule.agents)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.all_child_outcome_scores_20():
            self.running = False
