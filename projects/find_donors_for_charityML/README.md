## Dataset Summary

The census dataset we investigate here consists of approximately 32,000 data points, with each datapoint having 13 features (described in detail below). 

Our goal is to use this data to construct a model that accurately predicts whether a new individual - given values for their 13 features - makes less or more than \$50,000 dollars per year. 

### Features
1.  age: an integer value designating the age of the census taker. 

2.  workclass: a categorical variable identifying the general type of labor performed by the census taker permitted choices 

{Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked}

3.  education level: a categorical variable indicating level of completed education, permitted choices

{Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool}

4.  education-num: an integer feature indicating the number of years completed in school. 

5.  marital-status: a categorical feature with permitted choices 

{Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse} 

6.  occupation: a categorical variable indicating general occupation area, permitted choices 

{Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces}

7.  relationship: a categorical variable indicating general relationship status, permitted choices 

{Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried}

8.  race: a categorical variable indicating race, permitted choices 

{White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black} 

9.  sex: a categorical variable indicating sex, permitted choices 

{Female, Male} 

10.  capital-gain: continuous. 

11.  capital-loss: continuous. 

12.  hours-per-week: continuous. 

13.  native-country: categorical variable indicating native country, permitted choices

{United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands}

### Reference
The dataset used here is a simplified version of a dataset originally published in the article

Ron Kohavi, *"Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid",* Proceedings of the Second International Conference on Knowledge Discovery and Data Mining, 1996 

You may find this paper online at 
https://www.aaai.org/Papers/KDD/1996/KDD96-033.pdf

And the original dataset may be found at
https://archive.ics.uci.edu/ml/datasets/Census+Income