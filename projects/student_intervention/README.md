# 项目 2： 监督学习
## 搭建一个学生干预系统

### 安装

这个项目要求使用 **Python 2.7** 并且需要安装下面这些python包：

- [NumPy](http：//www.numpy.org/)
- [pandas](http：//pandas.pydata.org)
- [scikit-learn](http：//scikit-learn.org/stable/)

你同样需要安装好相应软件使之能够运行[Jupyter Notebook](http://jupyter.org/)

优达学城推荐学生安装[Anaconda](https：//www.continuum.io/downloads), 这是一个已经打包好的python发行版，它包含了我们这个项目需要的所有的库和软件。


### 代码

初始代码包含在 `student_intervention.ipynb` 这个notebook文件中。这里面有一些代码已经实现好来帮助你开始项目，但是为了完成项目，你还需要实现附加的功能。

### 运行

在命令行中，确保当前目录为 `student_intervention/` 文件夹的最顶层（目录包含本 README 文件），运行下列命令：

```jupyter notebook student_intervention.ipynb```

​这会启动 Jupyter Notebook 并把项目文件打开在你的浏览器中。

## 数据

​这个项目的数据包含在 `student-data.csv` 文件中。这个数据集包含以下属性： ​

- `school` ： 学生的学校（二元特征：值为“GP”或者是“MS”）
- `sex` ： 学生的性别（二元特征：“F”表示女性 或者是 “M”表示男性）
- `age` ： 学生的年龄（数值特征：从15到22）
- `address`： 学生的家庭住址类型（二元特征：“U”表示城市 或者是 “R”表示农村）
- `famsize`： 家庭大小（二元特征：“LE3”表示小于等于3 或者 “GT3”表示大于3）
- `Pstatus`： 父母共同生活状态（二元特征：“T”表示共同生活 或者是 “A”表示分居）
- `Medu`： 母亲的教育程度 （数值特征：0 - 未受教育,  1 - 小学教育（4年级）, 2 - 5年级到9年级, 3 - 中学教育 或者 4 - 更高等级教育）
- `Fedu`： 父亲的教育程度 （数值特征：0 - 未受教育,  1 - 小学教育（4年级）, 2 - 5年级到9年级, 3 - 中学教育 或者 4 - 更高等级教育）
- `Mjob` ： 母亲的工作 （常量特征： "teacher", "health" 表示和健康看护相关的工作, "services" 表示公务员（比如：行政人员或者警察）, "at_home"表示在家， "other"表示其他）
- `Fjob` ： 父亲的工作 （常量特征： "teacher", "health" 表示和健康看护相关的工作, "services" 表示公务员（比如：行政人员或者警察）, "at_home"表示在家， "other"表示其他）
- `reason` ： 选择这所学校的原因 （常量特征："home"表示离家近, "reputation"表示学校声誉, "course"表示课程偏好 或者 "other"表示其他）
- `guardian` ： 学生的监护人 （常量特征："mother"表示母亲, "father"表示父亲 或者 "other"表示其他）
- `traveltime` ： 到学校需要的时间 （数值特征： 1 - 小于15分钟., 2 - 15到30分钟., 3 - 30分钟到1小时, 4 - 大于1小时）
- `studytime`： 每周学习时间 （数值特征： 1 - 小于2个小时, 2 - 2到5个小时, 3 - 5到10个小时, 4 - 大于10个小时）
- `failures`：过去考试失败的次数 （数值特征： n 如果 1<=n<3, 其他 4）
- `schoolsup` ： 额外的教育支持 （二元特征： yes 或者 no）
- `famsup` ： 家庭教育支持 （二元特征： yes 或者 no）
- `paid` ： 和课程有关的其他付费课堂 （数学或者葡萄牙语） （二值特征： yes 或者 no）
- `activities` ： 课外活动 （二元特征： yes 或者 no）
- `nursery` ： 参加托儿所 （二元特征： yes 或者 no）
- `higher` ： 希望得到高等教育（二元特征： yes 或者 no）
- `internet` ： 在家是否能够访问网络 （二元特征： yes 或者 no）
- `romantic` ： 有没有谈恋爱 （二元特征： yes 或者 no）
- `famrel` ： 与家人关系的好坏 （数值特征： 从 1 - 非常差 到 5 - 非常好）
- `freetime` ： 放学后的空闲时间（数值特征： 从 1 - 非常少 到 5 - 非常多）
- `goout` ： 和朋友出去（数值特征： 从 1 - 非常少 到 5 - 非常多）
- `Dalc` ： 工作日饮酒量（数值特征：从 1 - 非常少 到 5 - 非常多）
- `Walc` ： 周末饮酒量（数值特征：从 1 - 非常少 到 5 - 非常多）
- `health` ： 当前健康状况 （数值特征： 从 1 - 非常差 到 5 - 非常好）
- `absences` ：在学校的缺席次数 （数值特征： 从 0 到 93）
- `passed` ： 学生是否通过最终的考试 （二元特征： yes 或者 no）
