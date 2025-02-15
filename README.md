**FRC Match Outcome Prediction (matches from 2023) – ML Classification**  
  
**Project Overview**  
This project applies machine learning classification to predict the outcome of FIRST Robotics Competition (FRC) 3v3 matches for the 2023 season. Using match data from The Blue Alliance API, I collected and processed thousands of matches, creating a dataset that enables real-time, blind prediction of whether the blue or red alliance will win.
  
**Quick Summary**  
Predicted the rate at which blue alliance would win with a peak of 80.07% accuracy over hundreds of matches using logistic regression on a train test paradigm.  
The model has been posted to chiefDeplhi in order to give teams around the globe access to these accurate *live* predictions.  
As of now, at least 5-10 teams have at least tried it out and found useful, correct predictions in the 2025 season.    
  
**Data Collection & Feature Engineering**
1. Data Retrieval
Used The Blue Alliance API (handled in dataHolder files) to extract raw match data.
2. Key Predictive Metrics
For each match, I calculated six key metrics that capture the difference between the blue and red alliances:

scorediff – Average total point difference between alliances.  
rpdiff – Difference in ranking points (awarded for specific achievements).  
autodiff – Difference in autonomous period points.  
endgamediff – Difference in endgame points.  
linkdiff – Difference in link (cycle completion) points.  
lastfive – Difference in win rate over the last five matches.  
Each metric is calculated as:  

blue alliance’s average value - red alliance’s average value  

**3. Calculation Breakdown Example: scorediff**  
For match n, scorediff is calculated by:  
  
Finding each individual team’s average past match score (before match n). Summing these averages for the three blue alliance teams. Summing these averages for the three red alliance teams. Taking the difference: scorediff  
  
=
(
∑
past scores of 
𝐵
1
,
𝐵
2
,
𝐵
3
3
)
−
(
∑
past scores of 
𝑅
1
,
𝑅
2
,
𝑅
3
3
)
  
=( 
3
∑past scores of B 
1
​
 ,B 
2
​
 ,B 
3 )−( 
3
∑past scores of R 
1
​
 ,R 
2
​
 ,R 
3 )  

  
This ensures the metric reflects an expected scoring difference based purely on historical data before match n, allowing for live, blind predictions without data leakage.  

4. Exploratory Data Analysis (EDA)  
Used 2D visualization and correlation analysis (eda_analysis.R) to determine which features were most predictive of match outcomes.
The most influential features were scorediff, rpdiff, and lastfive.  
5. Dataset Construction  
The dataset (csv_creator.R) was structured so that each row represents a match, with pre-match feature values ensuring no future data influences predictions.
Machine Learning Models & Performance
The dataset was used to train and evaluate multiple classification models in R (model_analysis.R):

  
**Model	Accuracy (%)**  
Note: in order to reproduce the same model with the same results, ensure that your random seed in the R file is identical to mine.
Logistic Regression	80.07 (Best)
Linear Discriminant Analysis (LDA)	78.6
Quadratic Discriminant Analysis (QDA)	75.3
Decision Trees	72.1
Random Forest (with tuning)	79.2
Hyperparameter tuning was performed where applicable.
Logistic regression achieved the best accuracy (80.07%), demonstrating that the predictive metrics were well-structured for classification.

**Files & Structure**  
dataHolderLarge.py – Handles API calls to collect match data.
allRcode.R – Performs Exploratory Data Analysis (EDA) to determine the most predictive features.
csvCreatorLarge.py – Processes raw data and generates the dataset used for model training.
allRcode.R – Implements machine learning classification models, evaluates different methods, and determines the best-performing approach.
Some of the exact json files I pulled, and csvs I used, are included in the git to see.

**Key Results & Insights**  
Logistic regression provided the best accuracy (80.07%), making it the most effective model for match outcome classification.
Scorediff, rpdiff, and lastfive were the strongest predictive features.
The methodology ensures live, blind predictions, making it possible to forecast match results in real-time using only prior match data.
