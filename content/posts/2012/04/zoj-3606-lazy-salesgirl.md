Title: ZOJ 3606 Lazy Salesgirl
Date: 2012-04-19 10:58
Author: Altynai
Category: Code
Tags: ACM, ZOJ
Slug: zoj-3606-lazy-salesgirl

<span style="color: #ff00ff;">【ZOJ
3606】</span><http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemId=4709>

今年浙江省省赛的G题，比赛的最后时刻是我去上去敲的，赛后才明白有个地方写挫了，以至于到比赛结束还没调好=
=真见鬼。

【题意】小女孩卖面包,有100000个顾客要来买(不会同一个时刻来两个顾客),现在有一个时间w,表示如果相邻两个顾客来的时间差严格大于w的话,小女孩在这个时间内会睡着,而新来的那个顾客不会买,只会把小女孩叫醒(既重新开始计算w),还有一点就是,第k个顾客买的面包数量为`(k-1)%3+1`,也就是`1,2,3,1,2,3....`这样的循环,现在让你求平均卖出价(卖得面包的总价/卖给的顾客数)最大的情况下的w最小
= = 描述有点绕,还是不太明白的建议看下原题目的描述..

【解法】

线段树的每个节点维护以下值：

- cnt:线段内已经插入点的个数
- sum[4]:sum[i]表示线段内第一个顾客买的面包数为i情况下该线段的总价

具体操作如下：

- 先对所有顾客按到来的时间排个序
- 再按相邻顾客之间的时间差(第1个顾客和时间0相减)升序排序
- 把那些相同的w的点插入到线段树中(更新到底)
- 统计下当前的w和平均价格,更新答案即可

相关的参考代码如下：

    :::cpp
    #define N 100002
    #define M 4
    #define lson (id<<1)
    #define rson (id<<1|1)
    struct Node{
        int l,r;
        int cnt;
        ll sum[M];
    }seg[N<<2];

    void build(int id,int l,int r){
        seg[id].l=l;
        seg[id].r=r;
        seg[id].cnt=0;
        for(int i=0;i<M;i++)
            seg[id].sum[i]=0;
        if(l==r)
            return;
        int mid=(l+r)>>1;
        build(lson,l,mid);
        build(rson,mid+1,r);
    }

    void push_up(int id){
        seg[id].cnt=seg[lson].cnt+seg[rson].cnt;
        int num=seg[lson].cnt;
        num%=3;
        for(int i=1;i<M;i++){
            int j=i+num;
            j=(j-1)%3+1;
            seg[id].sum[i]=seg[lson].sum[i]+seg[rson].sum[j];
        }
    }

    void update(int id,int pos,ll w){
        if(seg[id].l==pos && seg[id].r==pos){
            seg[id].cnt++;
            for(int i=0;i<M;i++)
                seg[id].sum[i]=w*i;
            return;
        }
        int mid=(seg[id].l+seg[id].r)>>1;
        if(pos<=mid)
            update(lson,pos,w);
        else
            update(rson,pos,w);
        push_up(id);
    }

    int n;
    struct Person{
        int p,t;
        friend bool operator<(const Person& a,const Person& b){
            return a.t<b.t;
        }
    }person[N];

    struct Cost{
        int oldid;
        int w;
        friend bool operator<(const Cost& a,const Cost& b){
            return a.w<b.w;
        }
    }cost[N];

    int main() {
    #ifndef ONLINE_JUDGE
        freopen("in.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif

        int cas,pcas=1;
        scanf("%d",&cas);
        while (scanf("%d",&n) != EOF){
            person[0].p=person[0].t=0;
            for(int i=1;i<=n;i++)
                scanf("%d",&person[i].p);
            for(int i=1;i<=n;i++)
                scanf("%d",&person[i].t);
            sort(person,person+n+1);
            for(int i=1;i<=n;i++){
                cost[i].oldid=i;
                cost[i].w=person[i].t-person[i-1].t;
            }
            sort(cost+1,cost+1+n);

            //segment tree
            double ans1=inf,ans2=0;
            int l=1,r,total=0;
            build(1,1,n);

            while(l<=n){
                r=l;
                while(r<=n && cost[r].w==cost[l].w){
                    int id=cost[r].oldid;
                    update(1,id,person[id].p);
                    total++;
                    r++;
                }

                double tmp1=cost[l].w;
                double tmp2=(double)seg[1].sum[1]/total;

                if(tmp2>ans2){
                    ans2=tmp2;
                    ans1=tmp1;
                }
                else if(tmp2==ans2)
                    ans1=min(ans1,tmp1);
                l=r;
            }
            printf("%.6lf %.6lf\n",ans1,ans2);
        }
        return 0;
    }
