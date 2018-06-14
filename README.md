# 分布式MapRuduce框架

一款基于RabbitMQ、Redis和Python3的分布式MapReduce框架（目前只实现了简单的K-means算法）

## 安装

安装前请先确保您的设备上安装有python3以及对应的模块。

使用指令安装模块：

```shell
$ pip install -r manager/requirements.txt
```

另外，你的设备上还需要安装有docker，并且需要正在运行的rabbitmq和redis镜像。

在工作目录下运行:

```shell
$ docker build mapper  # 生成mapper的镜像
$ docker build reducer # 生成reducer的镜像
```

准备工作就完成了。

## 运行

使用以下指令运行Reducer：

```shell
$ docker run --link=rabbit --link=redis -d -v ~/log:/var/log reducer:1.0
```

以上是一个例子，这里有几点需要注意：

1. `--link`：这里使用的是docker自带的容器关联，`rabbit`是rabbitmq容器的NAME。当然也可以是别的名字，但是如果要使用别的名字需要在dockerfile中重新配置环境变量`MQ_HOST`。`redis`也同理。
2. `-v ~/log:/var/log`：程序运行的结果会以log的形式输出到容器中的`/var/log`目录下的`result`文件中。这里默认是挂载到宿主机的`~/log`目录下，请根据自己的实际需求进行更改。

使用以下指令运行Mapper：

```shell
$ docker docker run --link=rabbit --link=redis -d mapper:1.0
```

理论上可以同时运行多个mapper和reducer，但是因为实现上的问题，目前只支持多个mapper和一个reducer。

当确认mapper和reducer已经启动成功之后，使用指令：

```shell
$ python3 manager/main.py
```

具体迭代次数可通过修改`manager/main.py`的内容来更改。

## 原理简单描述

`manager/main.py`中写的是主要的业务逻辑。`manager`会将读入的数据存入redis中，并为其附上一个id。之后，它会把这些id写成消息传入消息队列`map`中。

mapper拿到消息之后会从redis中拿出对应的数据进行运算，之后将其结果写入消息中，传入消息队列`reduce`中。

reducer拿到`reduce`队列中的消息之后，会将其运算结果归纳整理，最后将结果写入result文件，然后向`result`队列中发送一条已完成的消息。

manager收到`result`中已完成的消息之后将决定是否继续进行迭代。

目前自带的一组数据是经典的Iris数据集，你也可以自定义数据，但是要注意数据的输入形式。