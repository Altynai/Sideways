Title: 项目感受
Date: 2013-10-02 19:16
Author: Altynai
Category: Code
Tags: Django, Nginx, Python, Redis
Slug: atom-summary

忙了一个多月，第一个能说是正式的项目算差不多忙完了（后续优化不算的话），感受颇深，做个小总(tu)结(cao)。

### 学到的东西

**Nginx**  

之前在学校里的时候，知道并稍微了解过一部分相关的资料，但并没有实际上手搭建或者配置过Nginx。由于不是很熟悉相关配置，需要经常一边查文档、资料，一边修改Nginx的配置，然后再测试。在经历了反反复复的几次“配置测试”后，对基本的location匹配，rewrite等有了进一步的认识，同时也养成了经常查官方文档的好习惯: )。其中，最容易搞错的问题在于location的优先级上，下面是一个比较简单的总结：

    :::python
    ~     # 执行一个正则匹配，区分大小写
    ~*    # 执行一个正则匹配，不区分大小写
    ^~    # 进行普通字符匹配，如果匹配，之后不匹配别的选项
    =     # 进行普通字符精确匹配（优先级最高）
    @     # 定义一个命名的location，使用在内部定向时，例如error_page, try_files
    1. 如果满足某个字符精确匹配，停止搜索。
    2. 对于剩余的匹配字符串，进行最长匹配。如果这个匹配使用^~前缀，停止搜索。
    3. 按照定义的顺序，匹配其他正则表达式。
    4. 如果第3条规则产生匹配的话，结果被使用，否则，从第2条规则中获得的匹配进行使用。

在nginx使用过程中，比较常用的命令有：

    :::python
    nginx -t -c nginx.conf  # 设置并测试conf文件语法是否有错误
    nginx -s reload         # 重新加载conf文件

**Supervisord**

这是一个很好的进程管理软件，之前并没有接触过较大型的Django项目，对Django等其他进程的管理都是通过人为的方式进行，如果要进行stop、start、restart等操作就比较麻烦。so，所有的Django Project都是通过它来管理，由于Supervisord本身包含了可视化的管理界面（web页面），对进程的管理比较方便，同时可以在网页上看`tail -f`日志的结果，常用的命令有：

    :::python
    supervisord -c supervisord.conf         # 启动supervisord主程序（自动启动所有进程）
    supervisorctl start program_name        # 启动配置文件中配置的program_name进程
    supervisorctl stop program_name         # 杀死program_name
    supervisorctl restart program_name      # 重启program_name
    supervisorctl start/stop/restart  all   # 启动/杀死/重启所有进程
    supervisorctl reload                    # 载入最新的配置文件，停止原有进程并按新的配置启动
    supervisorctl update                    # 根据最新的配置文件，启动新配置或有改动的进程，配置没有改动的进程不会受影响

**Thumbor**

这个开源项目在我看来不算是一个用来存储图片的项目，是一个图片处理的项目，但是其中包含了比较完整的存储的功能，底层支持mongodb、redis、memcached作为存储机制（同时支持自定义扩展存储模块的机制，通过重写存储模块的代码来实现，修改配置文件中的`STORAGE = 'thumbor.storages.xxxx'`即可）。在项目间隙看了其部分存储图片的源码，由于底层使用了tornado，对tornado稍微有了点了解。在看源码的过程中，对原来项目中图片存储的那部分做了一定的修改，其中最重要的修改就是加了图片的缓存层，将图片缓存到Redis中。自定义存储图片的模块也比较简单：自定义模块继承`thumbor.storages`模块下的`BaseStorage`类，重写`put(self, path, bytes)`等方法即可。其中缓存的图片采用的策略为：

    :::py
    上传图片：如果相同图片已经存在，则操作。反之，将图片存储至mongodb，同时Redis中也存一份
    获得图片：如果图片在缓存中存在，直接返回。如果图片在mongodb中，直接返回，同时Redis中写入一份
    ps：在Redis中更新图片时，设置的过期时间为30天（由于暂时图片总量还不多）  
    
基本命令也比较简单：

    :::python
    thumbor -c thumbor.conf -p port

**Redis**

在大四期间接触过一段时间的Redis，看过Redis部分底层的源码，所以算是对Redis稍微有一部分的了解，但没有在实际环境下运行的相关经验。这次在图片缓存的配置使用中，了解了Redis实际运行过程中的一些情况，并用自带的命令进行了相关的实时信息监控。由于暂时只有一台虚拟机作为缓存服务器，具体配置也比较简单，其中比较重要的`maxmemory`这个参数配了内存的一半，防止fork时爆内存，同时也关了比较坑爹虚拟内存模式。除此之外，尝试配置了`Redis-Live`作为监控Redis-Server的工具，由于暂时每秒处理的命令数量还很小，之后可能打算考虑使用其作为监控程序。

**Django优化**

在代码上线的时候，不久发现服务器的CPU突然高的离谱，`top`看了下，有个`uwsgi`的占用率很不稳定，有时候基本没下过100%，后来排查基本锁定在代码的问题上。在这个过程中，主要学习到的是一些Django优化技巧，最直接的例子就是获得分类信息的接口，其中有一个返回值`has_commodity`，表示某个分类下面是否包含商品。在未优化的情况下，做法是去遍历分类和商品的关系表，然后查看`QuerySet`的大小是是否为0，但其实这是一个比较低效的做法。优化后的方法是直接在`xxxx.objects.filter(**kwargs)`后面加一个`[0]`，这样相当于底层SQL语句加了`limit = 1`的条件，实际效果显而易见。

### 往后的积累和准备

**Shell脚本**

很多时候，很多人为的工作完全可以交给机器自己来做，所以要积累Shell脚本的经验，多学习相关的知识。

**压力测试**

这次由于上线的时间比较紧张，并没有做较大的压力测试，致使产生了上文中比较严重的CPU问题，这个较为重要的性能问题明显可以在压力测试中测出来的。所以需要了解一些相关的压力测试工具（框架），使用并总结出适合的工具（框架）。

**Django**

* 缓存
了解和Django有关的缓存资料和文档，结合Redis（Memcached）作为缓存，在往后的实际操作中把性能放在第一位  

* 优化
积累并总结一些常见的Django查询优化技巧

**Redis**

积累Redis在实际运维过程中的经验，同时也多学习别人的使用经验。关注Redis新版本的动态，思考当数据量上了一个台阶之后所需要的集群方案。

**开阔视野**

多关注时下热门的技术信息，多了解和阅读优秀开源软件的代码，做好积累和消化的工作。