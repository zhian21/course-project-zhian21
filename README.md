# Final Project

### Summary
This project employs Agent-Based Modeling (ABM) to investigate the influence of parenting norms and misperceptions among college students, aiming to enhance interventions based on the social norms approach. By integrating surveys, social media analysis, and simulations, the research seeks to understand how misperceptions of parenting norms affect student behaviors and to identify strategies for correcting these misperceptions. The multifaceted methodology draws on diverse data sources, including population and economic statistics, the America Time Use Survey, and social media content, to model the emergence and evolution of parenting norms within college environments. The project's use of ABM allows for the exploration of complex social interactions and the impact of societal forces on individual decision-making processes. Despite challenges such as the simplification of real-world complexities and potential biases from reliance on survey data and social media scraping, the research holds promise for offering meaningful insights into supporting positive parenting behaviors among college-aged populations. Through a comprehensive review of literature on social norms, cultural evolution, and the role of misperceptions, the project addresses a significant gap in existing research, with the potential to contribute valuable knowledge on the dynamics of social norms and the mechanisms through which interventions can effectively align behaviors with actual norms.

### Research Questions  
* How can we develop and validate a methodology for identifying and measuring misperceptions within a defined cultural group, considering the complex interplay between personal attitudes and social expectations?
* What are the mechanisms through which misperceptions influence individual behaviors, specifically within the framework of interventions aimed at modifying social norms? 

### Data Sources
* **Data Source 1 - American Time Use Survey (ATUS)**  
Url: https://www.bls.gov/tus/data.htm  
Url: https://www.bls.gov/tus/data/datafiles-0322.htm (**the oversized data file**)  
The data consists of the responses of respondents from the year 2003 to 2022. The data contains demographic information of the respondents along with time spent on different diary activities on a 24-hour basis.

* **Data Source 2 - US Census Data - American Community Survey(API)**  
Url: https://data.census.gov/  
Url: https://api.census.gov/data/2022/acs/acs5/variables.html  
The ACS data contains socioeconomic and demographic data from respondents across the states.

### Github Navigation Steps  
* First clone the repository at your local machine.
* The structure of the repository is as follows:
   * Data folder contains all the CSV files
   * Notebooks folder contains all the iPython files of the codes
      * Census_ACS.ipynb file extracts the medium income level of U.S. states    
      * ATUS.ipynb file contains the preprocessing, exploratory data analysis, visualization, and OLS model results on the ATUS-related data file.
      * pd_grid subfolder contains:
        * model.py contains all the python script for the setup of the ABM model
        * server.py contains all the python script for seting up and running a server.
        * agent.py contains all the python script for the setup of the agent
      * requirement.text contains all the required libraries.
      * batchrun.py contains all the python script for the batch run
      * analysis_updated.ipynb contains all codes for the results for the second batch run
      * batch_run_results_2.csv contains the output for the second batch run
   * Proposal section folder contains all the write-up for the project
   * Figures folder contains sample figures for the project     


* Presentation folder contains in-class presentation slides

### Required Libraries  
1. python == 3.11.8
2. numpy == 1.26.1
3. pandas == 2.1.1
4. matplotlib = 3.8.2
5. seaborn == 0.13.1
6. statsmodels == 0.14.1
7. transformers == 4.38.2
8. praw == 7.7.1
9. openpyxl == 3.0.10
10. requests == 2.31.0
11. bs4 == 4.12.2
12. geopandas == 0.11.1
13. plotly == 5.9.0
14. scipy == 1.9.0
15. scikit-learn (sklearn) == 1.1.1


### Class setup

This is the link to my project on Overleaf: [link](https://www.overleaf.com/project/65fdea773626b7f87306b866). 

This is the link to my Zotero/Mendeley Group library: [link]().
