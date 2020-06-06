# Music Taster
顾名思义,这个项目用来挖掘音乐风格
大部分是基于歌单进行的关系挖掘,暂不涉及音频分析

### 动机
网易云音乐的红心歌单曲目太多了,想做点归类。

### 包含功能
1. 实现了歌单、歌曲详情的爬取与存储
2. 实现了Song2Vec、Artist2Vec
3. 实现歌曲、歌手的风格近似计算
4. 实现歌单下歌曲、歌手的聚类
5. 附带一个基于flask的API webserver

## 目录结构
1. models——用于存储数据类型对象的相关类文件
2. utils——基本的工具类
3. pipelines——存放各工作流程的脚本
4. datas——存放训练后的模型数据文件
5. api_server——基于flask的api server

## 环境需求
1. 如果进行数据爬取,则需要一个MongoDB实例进行数据管理
2. 安装`requirements.txt`下的依赖包

## Demo

[http://api.jayveehe.com/musictaster](http://api.jayveehe.com/musictaster)

## Data
Google Drive
[Artists Seq Data](https://drive.google.com/file/d/1fO4BkXBB9Rf5DsF7kggr6lROA4gmAB3Z/view?usp=sharing)
[Songs Seq Data](https://drive.google.com/file/d/1_kwmQ87kz3kHIRcAUdFaXY0_x2KCMyBw/view?usp=sharing)
[Artists x Songs Seq Data](https://drive.google.com/file/d/1IHetYu7Lrd_6jVurmq3_0oZ-OalEk5w2/view?usp=sharing)

使用方法:
1. 下载对应的dat文件
2. cPickle.load()

## Demo API Doc
[https://github.com/JayveeHe/MusicTaster/wiki/Music-Taster-Demo-API-Doc](https://github.com/JayveeHe/MusicTaster/wiki/Music-Taster-Demo-API-Doc)

## 使用MIT License
[MIT License](https://github.com/JayveeHe/MusicTaster/blob/master/LICENSE)

