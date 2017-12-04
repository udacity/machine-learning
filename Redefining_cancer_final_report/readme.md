# Project: Redefining Cancer
In recent years, researchers have been looking for new ways to combat cancer through precision medicine and genetic testing. Therefore, Kaggle.com has partnered with Memorial Sloan Kettering Cancer Center (MSKCC) with a goal of coming up with a machine learning algorithm that contribute new insights to genetic testing. 
This project is a submission for this [Kaggle Competition](https://www.kaggle.com/c/msk-redefining-cancer-treatment). 

The full documentation can be find [here](https://github.com/jmt7080/machine-learning/blob/master/Redefining_cancer_final_report/Udacity%20Capstone%20Project%20Paper%202.pdf)
## Install
This Project requires 
1. [Python 3.6 with Anaconda](https://anaconda.org/anaconda/python)
2. [XGBoost](https://github.com/dmlc/xgboost)
3. [MCA](https://pypi.python.org/pypi/mca/1.0.2)
4. [Jupyter Notebook](http://ipython.org/notebook.html)
## Code 
All code necessary for repeating this procedure is found [here](https://github.com/jmt7080/machine-learning/blob/master/Redefining_cancer_final_report/cancer_notebook.ipynb)
## Data 
The data can be downloaded from [here](https://www.kaggle.com/c/msk-redefining-cancer-treatment/data). 
### Features
Each entry has a:
1. Clinical Text: Ground truth data, determines the gene, its variation and its mutation class.
2. Gene: Multiple Genes can appear in one clinical text
3. Variation: Multiple variations can occur in each gene
4. Class: 9 different mutation classes decided by the cancer professional 
![alt text](https://github.com/jmt7080/machine-learning/blob/master/Redefining_cancer_final_report/sample_table.PNG "Sample image")
### Run
Navigate to the folder then run the following:
`jupyter notebook cancer_notebook.ipynb`
