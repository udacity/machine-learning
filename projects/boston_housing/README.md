# Predicting Boston Housing Prices
# Model Evaluation & Validation Project

## Install

This project requires Python 2.7 and the following Python libraries installed:

- [NumPy](http://www.numpy.org/)
- [scikit-learn](http://scikit-learn.org/stable/)

In addition, you will need to be able to run an iPython Notebook to complete this project.

## Code

Template code is provided in the `boston_housing.ipynb` notebook file. While some code has already been implemented to get you started, you will need to implement additional functionality when requested throughout the notebook.

## Run

In a terminal/command window, go to the top-level project directory `boston_housing/` (that contains this README). Then run:

```ipython notebook boston_housing.ipynb```

## Data

The dataset used in this project is included with the scikit-learn library ([`sklearn.datasets.load_boston`](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html#sklearn.datasets.load_boston)). You do not have to download it separately.

It contains the following attributes for each housing area, including median value (which you will try to predict):

- CRIM: per capita crime rate by town
- ZN: proportion of residential land zoned for lots over 25,000 sq.ft.
- INDUS: proportion of non-retail business acres per town
- CHAS: Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
- NOX: nitric oxides concentration (parts per 10 million)
- RM: average number of rooms per dwelling
- AGE: proportion of owner-occupied units built prior to 1940
- DIS: weighted distances to five Boston employment centres
- RAD: index of accessibility to radial highways
- TAX: full-value property-tax rate per $10,000
- PTRATIO: pupil-teacher ratio by town
- B: 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
- LSTAT: % lower status of the population
- MEDV: Median value of owner-occupied homes in $1000's
