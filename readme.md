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

## Demo API Doc
[https://github.com/JayveeHe/MusicTaster/wiki/Music-Taster-Demo-API-Doc](https://github.com/JayveeHe/MusicTaster/wiki/Music-Taster-Demo-API-Doc)

## 使用MIT License
[MIT License](https://github.com/JayveeHe/MusicTaster/blob/master/LICENSE)

