# Machine Learning Engineer Nanodegree
## Capstone Proposal
Praveen Origanti
January 12th, 2018

## Proposal
Cryptocurrency Price Indicator (Investment and Trading)

### Domain Background
Cryptocurrency (or digital currency) is a revolutionary concept enabling peer-to-peer currency exchange without relying on a central authority (like banks). Most cryptocurrencies use a decentralized/distributed ledger system, operating on the principles of cryptography, crowdsourcing and game theory. Satoshi Nakamoto first proposed these principles and defined the first blockchain database whose unit of currency is defined as bitcoin [1 - https://bitcoin.org/bitcoin.pdf]. The 

Bitcoin was created in 2009 and has mostly been limited to exploration by technological enthusiasts. The U.S. Treasury classified bitcoin as a convertible decentralized virtual currency in 2013 and the Commodity Futures Trading Commission, CFTC, classified bitcoin as a commodity in September 2015. Since then, it has garnered greater attention from general public and media. Mostly driven by speculative investments, it has seen an exponential rise in value in the last couple of years and several scholars expect the trend to continue, while others consider it to a bubble. Also, numerous other cryptocurrencies have been created as either variants of bitcoin or new platforms to support other applications. Ethereum, Litecoin, Ripple are a few among the popular ones, also referred to as alt-coins.

Personally, I've been impressed with the technology for a while, but haven't made any investments. I would like to take this opportunity to understand the market (and technology) better and decide if it is a good time to invest in cryptocurrencies.

### Problem Statement

The objective is to predict the price of bitcoin and ethereum given historic data on these cryptocurrencies. Given the volatility in these markets, it is hard to arrive at useful models just based on price data [3 - https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/]. In this light, I would also like to explore the possibility of adding major associated events to this dataset such as regulatory acceptance (twitter or news feed), new feature additions (code changes) etc. 

### Datasets and Inputs

The historic price data on these cryptocurrencies (along with other alt-coins) is available on coinmarketcap.com. For each day, open/close/low/high/ prices, volume and market cap are available as part of this data.

Also for the historic events on bitcoin, I would like to leverage the details on https://99bitcoins.com/price-chart-history/ and grade the nature of these events manually on a scale of 1-10, 10 being extremely positive event. 

Time permitting, I plan to gather additional associated events based on newsfeed (from google news or twitter or github changes) 

### Solution Statement

I'd begin with applying supervised learning algorithms (SVMs, random forests and boosting) to the available data. Also as this data has temporal information (time series), recurrent neural networks or LSTMs could be applied. The final model would be created by stacking the learned models based on different algorithms.

### Benchmark Model

Two benchmark models - 

(a) LSTMs applied to bitcoin and ethereum prediction as explained in this blog post ([3]) and 
(b) Kaggle kernel using Bayesian forecasting methods ([4] - https://www.kaggle.com/ara0303/forecasting-of-bitcoin-prices). 

In this section, provide the details for a benchmark model or result that relates to the domain, problem statement, and intended solution. Ideally, the benchmark model or result contextualizes existing methods or known information in the domain and problem given, which could then be objectively compared to the solution. Describe how the benchmark model or result is measurable (can be measured by some metric and clearly observed) with thorough detail.

### Evaluation Metrics
_(approx. 1-2 paragraphs)_

Mean Squared Error (MSE) and Mean Absolute Error (MAE) are two potential metrics for this mode. The benchmark models employ MSE. Since this is framed as a regression problem and the target is continuous, MSE/MAE are sensible evaluation metrics.

R^2 is another potential metric, but not sure if this will help in coming up with more accurate models.

The model results would be considered satisfactory if the predicted results are within +/- 10% of the actual future price.

### Project Design
_(approx. 1 page)_

Train -> Test
Regularization


Analysis of the data 
Also for the historic events on bitcoin, I would like to leverage the details on https://99bitcoins.com/price-chart-history/ and grade the nature of these events manually on a scale of 1-10, 10 being extremely positive event. 

Time permitting, I plan to gather additional associated events based on newsfeed (from google news or twitter or github changes) 

In this final section, summarize a theoretical workflow for approaching a solution given the problem. Provide thorough discussion for what strategies you may consider employing, what analysis of the data might be required before being used, or which algorithms will be considered for your implementation. The workflow and discussion that you provide should align with the qualities of the previous sections. Additionally, you are encouraged to include small visualizations, pseudocode, or diagrams to aid in describing the project design, but it is not required. The discussion should clearly outline your intended workflow of the capstone project.

-----------

**Before submitting your proposal, ask yourself. . .**

- Does the proposal you have written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Solution Statement** and **Project Design**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your proposal?
- Have you properly proofread your proposal to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
