Title: NaoNaYang
Date: 2011-09-15 07:58
Author: Altynai
Category: Code
Tags: ACM
Slug: zjut-naonayang

最后大家讨论了一下，我们队是去福州赛区(11月19-20号)和上海赛区(去打酱油..)

今天把队名弄了一下`NaoNaYang`其实我更喜欢`NiMengDaoDiXiangNaoNaYang`哈哈

差不多还有将近2个月的时间，所以这2个月的时间里，大家决定有时间就在一起开场比赛，这样算是保持一种状态的方法吧。

昨天第一场状态不佳啊...水题都要很久才过..坑爹了

题目来自[2008 Asia Regional Beijing][]

自己做过的几题就在这里稍微提及一下：

<span style="color: #ff00ff;">[hdu
2485]</span> <http://acm.hdu.edu.cn/showproblem.php?pid=2485>

由于只有50个点，先floyd一下，然后找割点，很显然，找割点的时候就是拆点网络流的模型。

关键是K，只有满足`dis[1][i]+dis[i][n]<=K`的点才拆点，以为这些点才是关键点。

其他的边按 `<i'-j>`连就好了，答案就是`maxflow(1,n+n)`

<span style="color: #ff00ff;">[hdu
2487]</span> <http://acm.hdu.edu.cn/showproblem.php?pid=2487>

首先找到一个字母的点，然后按`→↓←↑`的方向确定出4个角，看看是不是一个矩形。

如果能组成矩形，然后就有两个注意点：

- 矩形的长和宽≥3

- 这个矩形中间的区域必须全都是'.'

<span style="color: #ff00ff;">[hdu
2489] </span><http://acm.hdu.edu.cn/showproblem.php?pid=2489>

简单的`1<<15`的状态压缩dp，dp[state]表示state的点集组成的树的最小总边权和(点权和是固定的)


<span style="color: #ff00ff;">[hdu
2492]</span><http://acm.hdu.edu.cn/showproblem.php?pid=2492>

通过树状数组，求出每个位置i左右两边比它小和比它大的个数，然后乘一下就好了。

不管怎么样，希望接下去的状态好一点。

  [2008 Asia Regional Beijing]: http://acm.hdu.edu.cn/search.php?field=problem&key=2008%20Asia%20Regional%20Beijing&source=1&searchmode=source
