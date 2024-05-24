import mesa
from .model import ParentalLearningModel
from mesa.visualization.modules import TextElement

def network_portrayal(G):
    def node_color(agent):
        if agent.education_level == "High":
            return "#2F4F4F"  # darkslategray
        elif agent.education_level == "Medium":
            return "#008B8B"  # cadetblue
        elif agent.education_level == "Low":
            return "#AFEEEE"  # paleturquoise
        return "#FFFFFF"

    portrayal = {"nodes": [], "edges": []}

    for node_id, agents in G.nodes(data="agent"):
        if agents:
            agent = agents[0]
            portrayal["nodes"].append({
                "id": node_id,
                "color": node_color(agent),
                "size": 2 + agent.time_investment / 10,  # Adjust node size based on time investment
                "label": f"{agent.strategy}"
            })
    
    for source, target in G.edges():
        portrayal["edges"].append({"source": source, "target": target, "color": "#000000"})

    return portrayal

network = mesa.visualization.NetworkModule(network_portrayal, 500, 500)

class ParentCountElement(TextElement):
    def render(self, model):
        high_individual = sum(1 for agent in model.schedule.agents if agent.education_level == "High" and agent.strategy == "Individual Learning")
        high_social = sum(1 for agent in model.schedule.agents if agent.education_level == "High" and agent.strategy != "Individual Learning")
        
        medium_individual = sum(1 for agent in model.schedule.agents if agent.education_level == "Medium" and agent.strategy == "Individual Learning")
        medium_social = sum(1 for agent in model.schedule.agents if agent.education_level == "Medium" and agent.strategy != "Individual Learning")
        
        low_individual = sum(1 for agent in model.schedule.agents if agent.education_level == "Low" and agent.strategy == "Individual Learning")
        low_social = sum(1 for agent in model.schedule.agents if agent.education_level == "Low" and agent.strategy != "Individual Learning")
        
        return (f"High Education Parents: Individual learing - {high_individual}, Social learing - {high_social}<br>"
                f"Medium Education Parents: Individual learing - {medium_individual}, Social learing - {medium_social}<br>"
                f"Low Education Parents: Individual learing - {low_individual}, Social learing - {low_social}")

parent_count_element = ParentCountElement()

chart_outcome = mesa.visualization.ChartModule([
    {"Label": "Average Child Outcome Score (High)", "Color": "#2F4F4F"},  # darkslategray
    {"Label": "Average Child Outcome Score (Medium)", "Color": "#5F9EA0"},  # cadetblue
    {"Label": "Average Child Outcome Score (Low)", "Color": "#AFEEEE"}  # paleturquoise
])

chart_social_strategies = mesa.visualization.ChartModule([
    {"Label": "Social Learning Agents(High)", "Color": "#2F4F4F"},  # darkslategray
    {"Label": "Social Learning Agents(Medium)", "Color": "#5F9EA0"},  # cadetblue
    {"Label": "Social Learning Agents(Low)", "Color": "#AFEEEE"}  # paleturquoise
])

model_params = {
    "num_agents": mesa.visualization.Slider("Number of Agents", 30, 0, 60, 1),
    "optimal_time_investment": mesa.visualization.Slider("Optimal Time Investment", 100, 40, 100, 5),
    "primary_edu_level": mesa.visualization.Choice("Primary Education Level", choices=["High", "Medium", "Low"], value="High"),
    "primary_edu_ratio": mesa.visualization.Slider("Primary Education Level Ratio", 0.13, 0, 1, 0.1),
    "high_individual_learning_ratio": mesa.visualization.Slider("Individual Learning Ratio(High)", 0.7, 0, 1, 0.1),
    "medium_individual_learning_ratio": mesa.visualization.Slider("Individual Learning Ratio(Med)", 0.5, 0, 1, 0.1),
    "low_individual_learning_ratio": mesa.visualization.Slider("Individual Learning Ratio(Low)", 0.5, 0, 1, 0.1),
    "high_threshold": mesa.visualization.Slider("Threshold(High)", 5, 0, 60, 1),
    "medium_threshold": mesa.visualization.Slider("Threshold(Med)", 10, 0, 60, 1),
    "low_threshold": mesa.visualization.Slider("Threshold(Low)", 20, 0, 60, 1),
    "high_switch_probability": mesa.visualization.Slider("Switch Probability(High)", 0.2, 0, 1, 0.05),
    "medium_switch_probability": mesa.visualization.Slider("Switch Probability(Med)", 0.3, 0, 1, 0.05),
    "low_switch_probability": mesa.visualization.Slider("Switch Probability(Low)", 0.1, 0, 1, 0.05),
    "high_initial_time_investment": mesa.visualization.Slider("Initial Time Investment(High)", 100, 40, 110, 5),
    "medium_initial_time_investment": mesa.visualization.Slider("Initial Time Investment(Med)", 80, 40, 110, 5),
    "low_initial_time_investment": mesa.visualization.Slider("Initial Time Investment(Low)", 50, 40, 110, 5),
    "high_avg_node_degree": mesa.visualization.Slider("Average Node Degree(High)", 2, 0, 30, 1),
    "medium_avg_node_degree": mesa.visualization.Slider("Average Node Degree(Med)", 3, 0, 30, 1),
    "low_avg_node_degree": mesa.visualization.Slider("Average Node Degree(Low)", 3, 0, 30, 1),
    "high_rewiring_prob": mesa.visualization.Slider("Rewiring Probability(High)", 0.1, 0, 1, 0.1),
    "medium_rewiring_prob": mesa.visualization.Slider("Rewiring Probability(Med)", 0.5, 0, 1, 0.1),
    "low_rewiring_prob": mesa.visualization.Slider("Rewiring Probability(Low)", 0.1, 0, 1, 0.1),
    "high_primary_social_strategy": mesa.visualization.Choice("Primary Social Strategy(High)", choices=["Copying the highest-scoring neighbor", "Copying the most frequently observed strategy", "Copying randomly"], value="Copying the highest-scoring neighbor"),
    "high_primary_social_ratio": mesa.visualization.Slider("Primary Social Learning Ratio(High)", 0.5, 0, 1, 0.1),
    "medium_primary_social_strategy": mesa.visualization.Choice("Primary Social Strategy(Med)", choices=["Copying the highest-scoring neighbor", "Copying the most frequently observed strategy", "Copying randomly"], value="Copying the most frequently observed strategy"),
    "medium_primary_social_ratio": mesa.visualization.Slider("Primary Social Learning Ratio(Med)", 0.5, 0, 1, 0.1),
    "low_primary_social_strategy": mesa.visualization.Choice("Primary Social Strategy(Low)", choices=["Copying the highest-scoring neighbor", "Copying the most frequently observed strategy", "Copying randomly"], value="Copying randomly"),
    "low_primary_social_ratio": mesa.visualization.Slider("Primary Social Learning Ratio(Low)", 0.5, 0, 1, 0.1)
}

server = mesa.visualization.ModularServer(
    ParentalLearningModel, 
    [network, parent_count_element, chart_outcome, chart_social_strategies], 
    "Parental Learning Model", 
    model_params
)
server.port = 8521  # Default port
server.launch()
