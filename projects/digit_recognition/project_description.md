# 内容：深度学习
## 项目：搭建一个数字识别项目

## 项目概述

在这个项目中，你将使用你学到的关于深度神经网络和卷积神经网络的知识，建立一个实时相机应用或者是程序，它能够从提供的图片中实时打印出他观察到的数字。首先你将设计并实现一个能够识别数字序列的深度学习模型架构。然后，你将训练这个模型，使得它能够从类似[街景房屋门牌号(SVHN) dataset](http://ufldl.stanford.edu/housenumbers/)这种现实图片中识别出数字序列。模型训练好之后，你将使用一个实时相机应用（可选）或者是在新捕获的图片上建立应用以测试你的模型。最后，一旦你获得了有意义的结果，你将优化你的实现，并且*定位图片上的数字*，以及在新捕获的图像上测试定位效果。

## 软件需求
这个项目需要安装下面这些软件和python包：

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [NumPy](http://www.numpy.org/)
- [SciPy](https://www.scipy.org/)
- [scikit-learn](http://scikit-learn.org/0.17/install.html) (v0.17)
- [TensorFlow](http://tensorflow.org)

你同样需要安装好相应软件使之能够运行[Jupyter Notebook](http://ipython.org/notebook.html).

除了上面提到的，对于那些希望额外使用图像处理软件的，你可能需要安装下面的某一款软件：
- [PyGame](http://pygame.org/)
   - 对于安装PyGame有帮助的链接：
   - [Getting Started](https://www.pygame.org/wiki/GettingStarted)
   - [PyGame Information](http://www.pygame.org/wiki/info)
   - [Google Group](https://groups.google.com/forum/#!forum/pygame-mirror-on-google-groups)
   - [PyGame subreddit](https://www.reddit.com/r/pygame/)
- [OpenCV](http://opencv.org/)

对于那些希望额外选择将应用部署成安卓应用的：
- Android SDK & NDK (查看这个[README](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/android/README.md))

如果你还没有安装Python，优达学城推荐学生安装[Anaconda](http://continuum.io/downloads)这是一个已经打包好的python发行版，它包含了我们这个项目需要的所有的库和软件，请确认你安装的是Python 2.7而不是Python 3.x。然后`pygame`和`OpenCV`可以通过下列命令安装：


**opencv**  
`conda install -c menpo opencv=2.4.11`

**PyGame:**  
Mac:  `conda install -c https://conda.anaconda.org/quasiben pygame`  
Windows: `conda install -c https://conda.anaconda.org/tlatorre pygame`  
Linux:  `conda install -c https://conda.anaconda.org/prkrekel pygame`  

## 开始项目

对于这次作业，你可以在**课程资源**部分找到可下载的`digit_recognition.zip`压缩包，它包含了项目所需要的文件。*你也可以访问我们的[Machine Learning projects GitHub](https://github.com/udacity/machine-learning)以获取这个纳米学位的所有项目文件*

- `digit_recognition.ipynb`：这个文件是你将要修改的主要文件。

另外，你要自己下载并使用[街景房屋门牌号(SVHN)数据集](http://ufldl.stanford.edu/housenumbers/)，同时你还需要[notMNIST](http://yaroslavvb.blogspot.com/2011/09/notmnist-dataset.html)数据集或者是[MNIST](http://yann.lecun.com/exdb/mnist/)数据集。如果你已经完成了课程内容，那么你已经有**notMINIST**数据集了。

在终端或者是命令行中，导航到包含项目文件的文件夹中，然后使用命令`jupyter notebook digit_recognition.ipynb`，在浏览器窗口或者是标签页中打开你的notebook。或者你也可以使用命令`jupyter notebook`或者`ipython notebook`，然后再打开的浏览器窗口中导航到notebook文件。为了完成这个项目你需要跟随notebook中的指引，并回答提出的每一个问题。和项目文件一起我们还提供了一个**README**文件，它包含了一些关于这个项目的额外的必要信息或者是指引。

## 任务

### 项目报告
作为你提交的`digit_recognition.ipynb`的一部分，你需要回答关于你的实现的一些问题。在完成下面的任务的同时，你需要包含关于每一个问题（下面用*斜体*表示）的全面的详细的回答。

### 步骤 1: 设计并测试一个模型架构
设计并实现一个能够识别数字序列的深度学习模型。你可以通过连接[notMNIST](http://yaroslavvb.blogspot.com/2011/09/notmnist-dataset.html)或者是[MNIST](http://yann.lecun.com/exdb/mnist/)的字符来合成数据来训练这个模型。为了产生用于测试的合成数字序列，你可以进行如下的设置：比如，你可以限制一个数据序列最多五个数字，并在你的深度网络上使用五个分类器。同时，你有必要准备一个额外的“空白”的字符，以处理相对较短的数字序列。

在思考这个问题的时候有很多方面可以考虑：
- 你的模型可以基于深度神经网络或者是卷积神经网络。
- 你可以尝试是否在softmax分类器间共享权值。
- 你还可以在深度神经网络中使用循环网络来替换其中的分类层，并且将数字序列里的数字一个一个地输出。

这里有一个[发表的关于这个问题的基准模型的论文](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42241.pdf)([视频](https://www.youtube.com/watch?v=vGPI_JvLoN0))的例子。

***问题***
_你为解决这个问题采取了什么方法？_

***问题***
_你最终的模型架构是什么样的？（什么类型的模型，层数，大小, 连接性等）_

***问题***
_你是如何训练你的模型的？你是如何合成数据集的？_ 请同时包括你创建的合成数据中的一些示例图像。

### 步骤 2: 在真实数据集上训练一个模型

一旦你确定好了一个好的模型架构，你就可以开始在真实的数据上训练你的模型了。特别地，[街景房屋门牌号(SVHN)](http://ufldl.stanford.edu/housenumbers/)数据集是一个大规模的，从谷歌街景数据中采集的门牌号数据。在这个更有挑战性的数据集（这里数字不是整齐排列的，并且会有各种倾斜、字体和颜色）上训练，可能意味着你必须做一些超参数探索以获得一个表现良好的模型。

***问题***
_描述如何为模型准备训练和测试数据。 模型在真实数据集上表现怎么样？_

***问题***
_你（在模型上）做了什么改变？如果做了一些改变，那么你得到一个“好的”结果了妈？有没有任何你探索的导致结果更糟？_

***问题***
_当你在真实数据集做测试的时候你的初始结果和最终结果是什么？你认为你的模型在正确分类数字这个任务上上做的足够好吗？_

### 步骤 3: 在新抓取的图片上测试模型

在你周围拍摄几张数字的图片（至少五张），然后用你的分类器来预测产生结果。或者（可选），你可以尝试使用OpenCV / SimpleCV / Pygame从网络摄像头捕获实时图像，并通过你的分类器分析这些图像。

***问题***
_选择在你周围拍摄的五张候选图片，并提供在报告中。它们中的某些图片是否有一些特殊的性质，可能会导致分类困难？_

***问题***
_与在现实数据集上的测试结果相比，你的模型能够在捕获的图片或实时相机流上表现同样良好吗？_

***问题***
_如果必要的话，请提供关于你是如何建立一个使得你的模型能够加载和分类新获取图像的接口的。_

### 步骤 4: 探索一种提升模型的方式

一旦你基本的分类器训练好了，你就可以做很多事情。一个例子是：（在分类的同时）还能够定位图像上数字的位置。SVHN数据集提供边界框，你可以调试以训练一个定位器。训练一个关于坐标与边框的回归损失函数，然后测试它。

***问题***
_你的模型在真实数据的测试集上定位数字表现的怎么样？包含位置信息之后你的分类结果有变化吗？_

***问题***
在你在**步骤3**所捕获的图像上测试你的定位功能。模型是否准确计算出你找到的图像中的数字的边界框？如果你没有使用图形界面，您可能需要手动探索边界框。_提供一个在捕获的图像上创建边界框的示例_

## 可选步骤 5：为模型封装一个应用或者是程序

为了让你的项目更进一步。如果你有兴趣，可以构建一个安卓应用程序，或者是一个更鲁棒的Python程序。这些程序能够和输入的图像交互，显示分类的数字甚至边界框。比如，你可以尝试通过将你的答案叠加在图像上像[Word Lens](https://en.wikipedia.org/wiki/Word_Lens)应用程序那样来构建一个增强现实应用程序。

如何在安卓上的相机应用程序中加载TensorFlow的模型的示例代码在[TensorFlow Android demo app](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/android)中，你可以再这个基础上做一些简单的修改。


如果你决定探索这条可选路径，请务必记录你的接口和实现，以及你找到的重要结果。你可以通过[点击这个链接](https://review.udacity.com/#!/rubrics/413/view)看到将被用来评价你的工作的相关条目。

## 提交项目

### 评价
你的项目会由Udacity项目评审师根据 <a href="https://review.udacity.com/#!/rubrics/413/view" target="_blank"> **搭建一个数字识别项目量规**</a>进行评审。请注意仔细阅读这份量规并在提交前进行全面的自我评价。这份量规中涉及的所有条目必须全部被标记成*meeting specifications*你才能通过。

### 需要提交的文件
当你准备好提交你的项目的时候，请收集以下的文件，并把他们压缩进单个压缩包中上传。或者你也可以在你的GitHub Repo中的一个名叫`digit_recognition`的文件夹中提供以下文件以方便检查：
 - 回答了所有问题并且所有的代码单元被执行并显示了输出结果的`digit_recognition.ipynb`文件。
 - 一个从项目的notebook文件中导出的命名为**report.html**的**HTML**文件。这个文件*必须*提供。
 - 任何用于这个项目的除SVHN, notMNIST或者MNIST以外的数据集或者是图像

 - 对于可选的图像识别软件部分，你需要提供任何相关的Python文件，以保证能够运行你的代码。 
 - 对于可选的安卓应用部分，你需要为如何获取和使用这个应用编写文档，这部分应该提供一个命名为**documentation.pdf**的pdf报告。

一旦你收集好了这些文件，并阅读了项目量规，请进入项目提交页面。

### 我准备好了！
当你准备好提交项目的时候，点击页面底部的**提交项目**按钮。

如果你提交项目中遇到任何问题或者是希望检查你的提交的进度，请给**machine-support@udacity.com**发邮件，或者你可以访问<a href="http://discussions.youdaxue.com/" target="_blank">论坛</a>.

### 然后？
当你的项目评审师给你回复之后你会马上收到一封通知邮件。在等待的同时你也可以开始准备下一个项目，或者学习相关的课程。
