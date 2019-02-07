# Machine Learning Engineer Nanodegree
## Capstone Proposal
Eoin Cunning
Febuary 6th, 2019

I propse basing my capstone project around a Kaggle competition, New York Stock Exchange. 
This is my first experience on Kaggle and hope to appy some of domain knowledge as a developer in finance with technical knowlege from ml course . 

Details available at: https://www.kaggle.com/dgawlik/nyse

### Domain Background
The project is provides finicial data for NYSE listed stocks. And one of the challenges laid out is to attempt "One day ahead prediction: Rolling Linear Regression, ARIMA, Neural Networks, LSTM". 

Traditionally stock trading has been performed by humans but with all the unseen un-quantifible decsions that go into human decision making the idea here is to replace that human element with machine learning. Can a machine given historical tick data make predictions on futures movement and therefore recommend cetrain stocks to buy.
Wall steet has been attempting this same problem in various forms with various degrees of sucsess for years now.
We know this problem is solveable as there are multiple papers written on the subject from using SVMs to model the Indian Stock Market[1] to using LSTM to predict stock price movement [2].

I have selected this problem as it gives me the opportunity to join a Kaggle competition, interact with other machine learning practicioners, and learning from them and also emparting some of my knowledge by writing public available code with Kernels. 

[1] Support Vector Machines for Prediction of Futures Prices in Indian Stock Market - Shom Prasad Das, Sudarsan Padhy 

[2] Predicting Stock Prices Using LSTM - Murtaza Roondiwala, Harshal Patel, Shraddha Varma

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.259.969&rep=rep1&type=pdf
https://www.ijsr.net/archive/v6i4/ART20172755.pdf

### Problem Statement

The Problem here is to take historical time series tick data. Engieer it into a form where we associate features being previous prices and predict the next day value of the same prices.
This can be a regression or classification problem as we can attempt to predict the exact value of the next day price (regression) or more simply we could try and output a trade signal that would be true or false depending on what we predict the behaviour to be. (classification)

### Datasets and Inputs

The source of the data we will be using for this problem is a Kaggle dataset. From Kaggles description of the data. 
#### Dataset consists of following files:

- prices.csv: raw, as-is daily prices. Most of data spans from 2010 to the end 2016, for companies new on stock market date range is shorter. There have been approx. 140 stock splits in that time, this set doesn't account for that.
- prices-split-adjusted.csv: same as prices, but there have been added adjustments for splits.
securities.csv: general description of each company with division on sectors
- fundamentals.csv: metrics extracted from annual SEC 10K fillings (2012-2016), should be enough to derive most of popular fundamental indicators.

This price data acts as both our inputs and outs as it is both the prices are both the historical data we need ot feed into our algorithm but also the futures values we are trying to predict for the previous timeseries data.

### Solution Statement
A solution to his problem would been a trained model that given historical tick data could either sucseffully predict and up and down price movent in the given stock. Or predict the next day value to within a decided margin of error. 
To be considered a solution to this problem it must out perform a benchmark model of our choosing.

### Benchmark Model
If we impose the constraints that prices must move in ticks and must move up or down. 
Then theoricatilly the very worst we model we ccould come up with would randomly guess up or down based on previous price movement.
This lends itself well to a Random Forest Regressor so that is what we will use as the benchmark to compare our trained and refined model.

### Evaluation Metrics
The evaluation metric we have selected for this problem to quantify its performance is the R-square and root-mean-squared-error. 
As we will be atempted 
 RMSE = \sqrt{\frac{1}{n}\Sigma_{i=1}^{n}{\Big(\frac{d_i -f_i}{\sigma_i}\Big)^2}}
 
In this section, propose at least one evaluation metric that can be used to quantify the performance of both the benchmark model and the solution model. The evaluation metric(s) you propose should be appropriate given the context of the data, the problem statement, and the intended solution. Describe how the evaluation metric(s) are derived and provide an example of their mathematical representations (if applicable). Complex evaluation metrics should be clearly defined and quantifiable (can be expressed in mathematical or logical terms).


### Project Design
_(approx. 1 page)_


Using https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html as a guide to consider our various options regards algorithmns.

We can first consider this as regression problem with out goal to 

Based on the literature surround this problem a SVM could be reasonable approach.

In this final section, summarize a theoretical workflow for approaching a solution given the problem. Provide thorough discussion for what strategies you may consider employing, what analysis of the data might be required before being used, or which algorithms will be considered for your implementation. The workflow and discussion that you provide should align with the qualities of the previous sections. Additionally, you are encouraged to include small visualizations, pseudocode, or diagrams to aid in describing the project design, but it is not required. The discussion should clearly outline your intended workflow of the capstone project.

