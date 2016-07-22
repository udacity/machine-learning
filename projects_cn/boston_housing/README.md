# 项目1：模型评估与验证
## 波士顿房价预测

### 准备工作

这个项目需要安装**Python 2.7**和以下的Python函数库：

- [NumPy](http://www.numpy.org/)
- [matplotlib](http://matplotlib.org/)
- [scikit-learn](http://scikit-learn.org/stable/)

你还需要安装一个软件，以运行和编辑[ipynb](http://jupyter.org/)文件。

优达学城推荐学生安装 [Anaconda](https://www.continuum.io/downloads)，这是一个常用的Python集成编译环境，且已包含了本项目中所需的全部函数库。我们在P0项目中也有讲解[如何搭建学习环境](https://github.com/udacity/machine-learning/blob/master/projects_cn/titanic_survival_exploration/README.md)。

### 编码

代码的模版已经在`boston_housing.ipynb`文件中给出。你还会用到`visuals.py`和名为`housing.csv`的数据文件来完成这个项目。我们已经为你提供了一部分代码，但还有些功能需要你来实现才能以完成这个项目。

### 运行

在终端或命令行窗口中，选定`boston_housing/`的目录下（包含此README文件），运行下方的命令：

```jupyter notebook boston_housing.ipynb```

这样就能够启动jupyter notebook软件，并在你的浏览器中打开文件。

### 数据


本项目中使用的数据均包含在scikit-learn数据库([`sklearn.datasets.load_boston`] (http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html#sklearn.datasets.load_boston))中，你无需额外下载。关于数据的更多信息，你可以访问[UCI机器学习库](https://archive.ics.uci.edu/ml/datasets/Housing)。