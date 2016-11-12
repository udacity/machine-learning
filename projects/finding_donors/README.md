# 机器学习纳米学位
# 监督学习
## 项目: 为CharityML寻找捐献者
### 安装

这个项目要求使用 Python 2.7 并且需要安装下面这些python包：

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org/)
- [scikit-learn](http://scikit-learn.org/stable/)
- [matplotlib](http://matplotlib.org/)

你同样需要安装好相应软件使之能够运行 [iPython Notebook](http://ipython.org/notebook.html)

优达学城推荐学生安装[Anaconda](https://www.continuum.io/downloads), 这是一个已经打包好的python发行版，它包含了我们这个项目需要的所有的库和软件。

### 代码

初始代码包含在`finding_donors.ipynb`这个notebook文件中。你还会用到`visuals.py`和名为`census.csv`的数据文件来完成这个项目。我们已经为你提供了一部分代码，但还有些功能需要你来实现才能以完成这个项目。
这里面有一些代码已经实现好来帮助你开始项目，但是为了完成项目，你还需要实现附加的功能。  
注意包含在`visuals.py`中的代码设计成一个外部导入的功能，而不是打算学生去修改。如果你对notebook中创建的可视化感兴趣，你也可以去查看这些代码。


### 运行
在命令行中，确保当前目录为 `finding_donors/` 文件夹的最顶层（目录包含本 README 文件），运行下列命令：

```bash
jupyter notebook finding_donors.ipynb
```

​这会启动 Jupyter Notebook 并把项目文件打开在你的浏览器中。

### 数据

修改的人口普查数据集含有将近32,000个数据点，每一个数据点含有13个特征。这个数据集是Ron Kohavi的论文*"Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid",*中数据集的一个修改版本。你能够在[这里](https://www.aaai.org/Papers/KDD/1996/KDD96-033.pdf)找到论文，在[UCI的网站](https://archive.ics.uci.edu/ml/datasets/Census+Income)找到原始数据集。

**特征**

- `age`: 一个整数，表示被调查者的年龄。 
- `workclass`: 一个类别变量表示被调查者的通常劳动类型，允许的值有 {Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked}
- `education_level`: 一个类别变量表示教育程度，允许的值有 {Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool}
- `education-num`: 一个整数表示在学校学习了多少年 
- `marital-status`: 一个类别变量，允许的值有 {Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse} 
- `occupation`: 一个类别变量表示一般的职业领域，允许的值有 {Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces}
- `relationship`: 一个类别变量表示家庭情况，允许的值有 {Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried}
- `race`: 一个类别变量表示人种，允许的值有 {White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black} 
- `sex`: 一个类别变量表示性别，允许的值有 {Female, Male} 
- `capital-gain`: 连续值。 
- `capital-loss`: 连续值。 
- `hours-per-week`: 连续值。 
- `native-country`: 一个类别变量表示原始的国家，允许的值有 {United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands}

**目标变量**

- `income`: 一个类别变量，表示收入属于那个类别，允许的值有 {<=50K, >50K}