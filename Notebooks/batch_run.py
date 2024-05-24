from ps.model import ParentalLearningModel
from mesa.batchrunner import batch_run
import numpy as np
import pandas as pd

# Define ranges for parameters
primary_edu_ratio_range = [0.13, 0.53]
individual_learning_ratio_range = [0.3, 0.7]
primary_social_ratio_range = [0.3, 0.7]
switch_probability_range = [0.3, 0.7]
threshold_range = [5, 51]

# Parameters to vary
parameters = {
    "primary_edu_ratio": primary_edu_ratio_range,
    "high_individual_learning_ratio": individual_learning_ratio_range,
    "medium_individual_learning_ratio": individual_learning_ratio_range,
    "low_individual_learning_ratio": individual_learning_ratio_range,
    "high_primary_social_ratio": primary_social_ratio_range,
    "medium_primary_social_ratio": primary_social_ratio_range,
    "low_primary_social_ratio": primary_social_ratio_range,
    "high_switch_probability": switch_probability_range,
    "medium_switch_probability": switch_probability_range,
    "low_switch_probability": switch_probability_range,
    "high_threshold": threshold_range,
    "medium_threshold": threshold_range,
    "low_threshold": threshold_range,
    "num_agents": [30],
    "optimal_time_investment": [100],
    "primary_edu_level": ["High"],
    "high_initial_time_investment": [90],
    "medium_initial_time_investment": [80],
    "low_initial_time_investment": [50],
    "high_avg_node_degree": [2],
    "medium_avg_node_degree": [3],
    "low_avg_node_degree": [3],
    "high_rewiring_prob": [0.1],
    "medium_rewiring_prob": [0.5],
    "low_rewiring_prob": [0.1],
    "high_primary_social_strategy": ["Copying the highest-scoring neighbor"],
    "medium_primary_social_strategy": ["Copying the most frequently observed strategy"],
    "low_primary_social_strategy": ["Copying randomly"]
}

# The main block to avoid multiprocessing issues
if __name__ == '__main__':
    # Run the batch simulation
    results = batch_run(
        model_cls=ParentalLearningModel,
        parameters=parameters,
        iterations= 50,
        max_steps=40,
        data_collection_period=1,
        number_processes=4
    )

    # Convert results to pandas DataFrame
    df = pd.DataFrame(results)

    # Save the data to a CSV file
    df.to_csv("batch_run_results.csv")
