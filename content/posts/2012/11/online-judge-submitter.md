Title: Online Judge Submitter
Date: 2012-11-08 21:01
Author: Altynai
Category: Code
Tags: Python
Slug: online-judge-submitter

做这个的东西就是为了熟练掌握一下Python，书买了很久，看了一大半了，但具体实现的代码很少。给自己订了了目标，主要是为了掌握一些基本点和网络编程的小入门，之前看到过有人做过类似的，所以也尝试的做了一个，虽然不怎么实用。

原理也很简单：  

- 给OJ发Post的login请求，在response中获得Cookie  
- 带上之前的cookie提交代码，然后根据runId（没的话直接去搜用户提交记录）来获取Judge结果

细节还是很多的：用户名密码，题目编号，文件对应的编译器，网页源代码中正则出有用数据，etc.
这几天加紧补上国内其他主要OJ的相关部分，这里也当做日志记录好了。

项目地址：<https://github.com/Altynai/OnlineJudgeSubmitter>

**【2012.11.08】Add ZOJ (<http://acm.zju.edu.cn>)**

**【2012.11.09】Add POJ (<http://poj.org>), HDU(<http://acm.hdu.edu.cn>) 修改了部分错误**
