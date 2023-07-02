# 简介
AFinChat是一款ChatGPT的插件，可以装载在ChatGPT的自定义插件中，用来联网获取A股行情、财务、新闻等信息，便于后续分析  
整体的思路：权限申请 -> 本地运行该项目 -> 官网安装 -> 顺利使用
# 权限申请
首先你必须有ChatGPT的插件开发权限，如果没有的话可以去https://openai.com/waitlist/plugins
申请，在申请界面要选I am a developer and want to build a plugin  
**提示：并非开通了ChatGPT plus就可以有开发者权限，当前插件使用权限与开发权限是分开的，必须单独申请**

# 运行方法

这个文件我没细看，把很多不需要的东西放进来了，后面会进行精简。大家也可以看情况自己装一下，主要就是quart、quart_cors、baostock、httpx四个库，怕麻烦一次性打包装也行
```
pip3 install - requirements.txt
```
quart这个框架有个问题，就是不能在notebook里面直接运行，spyder的IPython Console也不行，不然会说已经有一个服务在运行了，所以就用最原始的方式运行即可，文件里默认的端口是5023  
```
python3 server.py
```

# 官网安装
具体开发以及使用的思路请参考这篇知乎回答（不是我）https://zhuanlan.zhihu.com/p/629207240
也可以参考OpenAI的官方文档https://platform.openai.com/docs/plugins/examples  
**重点提示：如果你是一个完完全全的小白，建议放弃该项目，看个乐即可**

# 使用示例
**总结最近新闻**  
![image](https://github.com/Doujiang2333/AFinChat/assets/125125837/0e8785a0-29e9-4e4b-b167-ebaa333b9bd8)  
**获取财务信息**  
![image](https://github.com/Doujiang2333/AFinChat/assets/125125837/63411791-4eba-43f2-98de-6d1eb298384d)  
**配合Wolfram可以股价图**  
![image](https://github.com/Doujiang2333/AFinChat/assets/125125837/1da25141-3bf8-4e86-a66c-799116d7c7ff)  

# 主要代码说明 - 主打的就是个爬虫
server.py 是主程序，除了Openai规定的标准端点，有三个核心端点：  
* GET /news/{keywords} - 检索有关给定关键字的最新新闻，用的是东方财富网的一个爬虫
* GET /financialstatement/{stockcode}/{company_type}/{report_type}/{report_date} - 检索给定股票的财务报表，用的是巨潮的一个爬虫，支持三张表的主要数据，可以区分一般企业与金融企业
* GET /{stockquotes}/{stockcode}/{adjustflag}/{start_date}/{end_date/freq} - 用于获取股票的历史行情信息，使用的是baostock库

openai.yaml 是Openai的一个规范化说明文件，是对函数、参数、返回信息的说明，是ChatGPT会直接读取的内容，教给它如何去调用server.py中的函数
其他的没啥大用

# 支持
想要交流和支持，可以关注公众号“豆浆科技”，在菜单栏进入Albeta充点即可，用爱发电
![image](https://github.com/Doujiang2333/AFinChat/assets/125125837/ee8b0e5a-5801-4384-bd6c-cbf668318ae0)



# 未来开发计划
1. 等待OpenAI官方插件审核通过
2. 支持港股行情
3. 支持基金、基金经理分析
