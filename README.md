# Final Project

### Summary
This research project investigates the dynamics of misperceptions in parenting norms among U.S. college students through the use of agent-based modeling. Addressing key concerns such as the complexity of design concepts, causal claims, and the definition of social norms, the study aims to elucidate how social learning strategies, demographic variables, and group sizes contribute to these misperceptions. Hypotheses include an increasing trend in parental investment, potential overestimation of such investment by students, and the influence of social learning strategies and group sizes on these misperceptions. Despite limitations in capturing real-world complexities, the project employs a rigorous methodological approach, combining historical data analysis, surveys, and simulation modeling. Preliminary results indicate an upward trend in parental time investment in childcare and reveal the impact of different learning strategies on the dissemination of parenting norms. This research contributes to a deeper understanding of the perceptions and misperceptions of parenting norms among college students, offering insights into the broader implications of social norm dynamics.


### Research Questions  
* How do social learning strategies, demographic variables, and social network contribute to the misperceptions of parenting norms among college students?
* Is there an increasing trend in parental investment in childcare, and do students overestimate this investment?
* How do different social learning strategies and group sizes influence the dissemination and adoption of parenting norms? 

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
   * Data folder contains all the CSV files for the data used 
   * Notebooks folder contains all the iPython files of the codes
      * Census_ACS.ipynb file extracts the medium income level of U.S. states    
      * ATUS.ipynb file contains the preprocessing, exploratory data analysis, visualization, and OLS model results on the ATUS-related data file.
      * ps subfolder contains:
        * model.py contains all the python script for the setup of the ABM model
        * server.py contains all the python script for seting up and running a server.
        * agent.py contains all the python script for the setup of the agent
      * requirement.text contains all the required libraries.
      * batchrun.py contains all the python script for the batch run
      * analysis.ipynb contains all codes for the results for the batch run
      * batch_run_results_.csv is not in the repo due to the size limitation
   * Proposal section folder contains all the write-up for the project
   * Figures folder contains sample figures for the project
   * Final_proposal.pdf contains the final compiled pdf file for the write-up     


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
16. mesa~=2.0


### Class setup

This is the link to my project on Overleaf: [link](https://www.overleaf.com/project/65fdea773626b7f87306b866). 

This is the link to my Zotero/Mendeley Group library: [link]().
