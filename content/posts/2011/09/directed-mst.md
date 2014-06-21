Title: 最小树形图
Date: 2011-09-04 16:17
Author: Altynai
Category: Code
Tags: ACM
Slug: directed-mst

9月3号的大连网络赛的第9题，当时题目看完之后发现是从来没有做过的类型，费用流的话也不像是费用流。

赛后才知道原来是最小树形图，o(VE)的复杂度，然后趁今天的一段空闲时间去找了点资料看看。

我只写一下我自己理解的一些东西，因为概念等信息网上都有。

这个叫"朱-刘算法"有点像求mst的算法，先选取每个点(非根点)入边中权值最小的那条边，这样组成一个集合E。

而有环的判断有点像kruskal中判断选取的当前边的两点是否属于同一个联通块。

"朱-刘算法"中最关键的部分就是处理出现有向环的情况了。

当把环缩点，修改非环点到环的距离和环到非环点的距离的时候，可以想象成是这样：

> 现在有一个环C，C中有一个点B，B在环中的前驱结点为
pre[B]，除此之外环外有一个点A，存在边(A,B) ∈ E

> 我们可以知道(A,B)的权值肯定是≥
(pre[B],B)这条边的权值的，证明也很简单，如果不成立，那么pre[B]就变成了A了。

> 所以更新的操作就是w(A,B)-=w(pre[B],B)，这关键的一步我是这样理解的：

> 因为这个环C肯定是和根结点不联通的，所以还要加一条类似(A,B)边，才又可能满足C与根节点联通。

> 而假设我们真的加入了(A,B)这条边，根据最小树形图的定义，我们可以知道(pre[B],B)这条边这个时候相当于是作废了

> 但我们也因此付出了相应的“代价"，而这个”代价"，就是w(A-B)-w(pre[B],B)，并且，已经知道，这个代价肯定是≥0的。

之后，我们只要重复进行上面的过程就行了。

但，这些只是基础，毕竟，光有模板是没有用的，还有很多这货的变形版没遇到过，所以，接下来还是要去找点扩展资料来看的。

网上都在说的模板题。

【TJU 2248】 <http://acm.tju.edu.cn/toj/showp2248.html>

    :::cpp
    struct Edge{
        int u,v,cost;
        void read(){scanf("%d%d%d",&u,&v,&cost);u--,v--;}
    }e[M];

    int pre[N],in[N],id[N];
    int flag[N];

    int Zhu_Liu(int NV,int NE,int root){
        int res=0;

        while(true){

            //1.找每个点的最小入边
            memset(in,63,sizeof(in));
            in[root]=0;
            for(int i=0;i<NE;i++){
                //去掉自环的情况
                if(e[i].u==e[i].v)
                    continue;
                if(e[i].cost<in[ e[i].v ]){
                    in[ e[i].v ]=e[i].cost;
                    pre[ e[i].v ]=e[i].u;
                }
            }
            //2.判断是否有独立的点（没有入边的点，或者与图不连通的点）
            for(int i=0;i<NV;i++)
                if(in[i]==INF)
                    return -1;
            //3.找环并标记
            int newID=0;
            memset(id,-1,sizeof(id));
            memset(flag,-1,sizeof(flag));
            for(int i=0;i<NV;i++){
                if(i==root)
                    continue;
                res+=in[i];
                int v=i;
                while(flag[v]!=i && v!=root){
                    flag[v]=i;
                    v=pre[v];
                }
                //找到一个有向环
                if(v!=root && id[v]==-1){
                    for(int u=pre[v];u!=v;u=pre[u])
                        id[u]=newID;
                    id[v]=newID++;
                }
                //如果找不到环，说明是一条有向链，以root开始
            }
            if(newID==0)//没有环
                break;
            //4.缩点，重标号
            for(int i=0;i<NV;i++)
                if(id[i]==-1)
                    id[i]=newID++;

            for(int i=0;i<NE;i++){
                if(e[i].u==e[i].v)
                    continue;
                e[i].cost-=in[ e[i].v ];
                e[i].u=id[ e[i].u ];
                e[i].v=id[ e[i].v ];
            }
            NV=newID;
            root=id[root];
        }
        return res;
    }
