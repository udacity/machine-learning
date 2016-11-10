# 机器学习工程师纳米学位
# 深度学习
## 项目：搭建一个数字识别项目

### 安装

这个项目要求使用 **Python 2.7** 并且需要安装下面这些python包：

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

对于那些希望选择额外选择将应用部署成安卓应用的：
- Android SDK & NDK (查看这个[README](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/android/README.md))

如果你还没有安装Python，优达学城推荐学生安装[Anaconda](http://continuum.io/downloads)这是一个已经打包好的python发行版，它包含了我们这个项目需要的所有的库和软件，请确认你安装的是Python 2.7而不是Python 3.x。然后`pygame`和`OpenCV`可以通过下列命令安装：

Mac:  
```bash
conda install -c https://conda.anaconda.org/quasiben pygame
conda install -c menpo opencv=2.4.11
```

Windows & Linux:  
```bash
conda install -c https://conda.anaconda.org/tlatorre pygame
conda install -c menpo opencv=2.4.11
```

### 代码

初始代码包含在`digit_recognition.ipynb`这个notebook文件中。这里面没有提供给你代码，为了完成项目，你需要在notebook中实现基本的功能并回答关于你的实现和结果的问题。

### 运行

在命令行中，确保当前目录为 `digit_recognition/` 文件夹的最顶层（目录包含本 README 文件），运行下列命令：
```bash
ipython notebook digit_recognition.ipynb
```  
或者
```bash
jupyter notebook digit_recognition.ipynb
```

这会启动 Jupyter Notebook 并把项目文件打开在你的浏览器中。


### 数据

因为这个项目没有直接提供任何的代码，你要自己下载并使用[街景房屋门牌号(SVHN)数据集](http://ufldl.stanford.edu/housenumbers/)，同时你还需要[notMNIST](http://yaroslavvb.blogspot.com/2011/09/notmnist-dataset.html)数据集或者是[MNIST](http://yann.lecun.com/exdb/mnist/)数据集。如果你已经完成了课程内容，那么你已经有**notMINIST**数据集了。
