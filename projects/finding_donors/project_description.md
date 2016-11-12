# 内容： 监督学习
## 项目：为CharityML寻找捐献者

## 项目概况
在这个项目中，你将使用监督技术和分析能力对美国人口普查数据进行分析，以帮助CharityML（一个虚拟的慈善机构）识别最有可能向他们捐款的人，你将首先探索数据以了解人口普查数据是如何记录的。接下来，你将使用一系列的转换和预处理技术以将数据整理成能用的形式。然后，你将在这个数据上评价你选择的几个算法，然后考虑哪一个是最合适的。之后，你将优化你现在为CharityML选择的模型。最后，你将探索选择的模型和它的预测能力。

## 项目亮点
这个项目设计成帮助你熟悉在sklearn中能够使用的多个监督学习算法，并提供一个评价模型在某种类型的数据上表现的方法。在机器学习中准确理解在什么时候什么地方应该选择什么算法和不应该选择什么算法是十分重要的。

完成这个项目你将学会以下内容：
- 知道什么时候应该使用预处理以及如何做预处理。
- 如何为问题设置一个基准。
- 判断在一个特定的数据集上几个监督学习算法的表现如何。
- 调查候选的解决方案模型是否足够解决问题。

## 软件要求

这个项目要求使用 Python 2.7 并且需要安装下面这些python包：

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org/)
- [scikit-learn](http://scikit-learn.org/stable/)
- [matplotlib](http://matplotlib.org/)

你同样需要安装好相应软件使之能够运行 [iPython Notebook](http://ipython.org/notebook.html)

优达学城推荐学生安装[Anaconda](https://www.continuum.io/downloads), 这是一个已经打包好的python发行版，它包含了我们这个项目需要的所有的库和软件。请注意你安装的是2.7而不是3.X

## 开始项目

对于这个项目，你能够在**Resources**部分找到一个能下载的`find_donors.zip`。*你也可以访问我们的[机器学习项目GitHub](https://github.com/udacity/machine-learning)获取我们纳米学位中的所有项目*

这个项目包含以下文件：

- `find_donors.ipynb`: 这是你需要工作的主要的文件。
- `census.csv`: 项目使用的数据集，你将需要在notebook中载入这个数据集。
- `visuals.py`: 一个实现了可视化功能的Python代码。不要修改它。

在终端或命令提示符中，导航到包含项目文件的文件夹，使用命令`jupyter notebook finding_donors.ipynb`以在一个浏览器窗口或一个标签页打开notebook文件。或者你也可以使用命令`jupyter notebook`或者`ipython notebook`然后在打开的网页中导航到需要的文件夹。跟随notebook中的指引，回答每一个问题以成功完成项目。在这个项目中我们也提供了一个**README**文件，其中也包含了你在这个项目中需要了解的信息或者指引。

## 提交项目

### 评价
你的项目会由Udacity项目评审师根据**<a href="#" target="_blank">为CharityML寻找捐献者项目量规</a>**进行评审。请注意仔细阅读这份量规并在提交前进行全面的自我评价。这份量规中涉及的所有条目必须全部被标记成*meeting specifications*你才能通过。

### 需要提交的文件
当你准备好提交你的项目的时候，请收集以下的文件，并把他们压缩进单个压缩包中上传。或者你也可以在你的GitHub Repo中的一个名叫`finding_donors`的文件夹中提供以下文件以方便检查：
 - 回答了所有问题并且所有的代码单元被执行并显示了输出结果的`finding_donors.ipynb`文件。
 - 一个从项目的notebook文件中导出的命名为**report.html**的**HTML**文件。这个文件*必须*提供。

一旦你收集好了这些文件，并阅读了项目量规，请进入项目提交页面。

### 我准备好了！
当你准备好提交项目的时候，点击页面底部的**提交项目**按钮。

如果你提交项目中遇到任何问题或者是希望检查你的提交的进度，请给**machine-support@udacity.com**发邮件，或者你可以访问<a href="http://discussions.youdaxue.com/" target="_blank">论坛</a>.

### 然后？
当你的项目评审师给你回复之后你会马上收到一封通知邮件。在等待的同时你也可以开始准备下一个项目，或者学习相关的课程。