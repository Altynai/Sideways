Title: ZOJ 2706 Thermal Death of the Universe
Date: 2011-11-06 00:19
Author: Altynai
Category: Code
Tags: ACM
Slug: zoj-2706-thermal-death-of-the-universe

<span style="color: #ff00ff;">**【ZOJ
2706】**</span><http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=2706>

题意：给你一个30,000的序列，然后有30,000个操作，每个操作把某个区间的所有值变成这个区间的平均数，小数四舍五入的原则给定，求最后的序列。

这题很显然是线段树，而且需要lazy操作（lazy为true表示当前整段是否相同），lazy操作需要的地方：<span
style="color: #ff00ff;">update（区间更新）、Search（得到区间sum）和query（去除所有的lazy标记，得到最后的序列）</span>，一开始死活都没有发现WA在哪里，后来才发现Search（得到区间sum）操作的时候忘记lazy的pushdown操作了，这个下次要注意。

还有一点要注意的就是区间的和为负数的情况，这样ceil和floor和整数是不一样的。

    :::cpp
    #include <iostream>
    #include <cstdio>
    #include <cstring>
    #include <string>
    #include <algorithm>
    #include <cmath>
    #include <stack>
    using namespace std;
    #define N 30005
    #define ll long long

    struct Node{
        int l,r;
        ll sum,v;
        bool lazy;

        void mark(ll v){
            this->v=v;
            lazy=true;
            sum=v*(r-l+1);
        }
    }seg[N<<2];

    ll val[N],oldSum,curSum,segSum;
    int n,m;

    void build(int l,int r,int id){
        seg[id].l=l;
        seg[id].r=r;
        seg[id].lazy=false;
        if(l==r){
            seg[id].sum=val[l];
            return;
        }
        int mid=(l+r)>>1;
        build(l,mid,id<<1);
        build(mid+1,r,id<<1|1);
        seg[id].sum=seg[id<<1].sum+seg[id<<1|1].sum;
    }

    void update(int l,int r,int id,ll average){

        if(seg[id].l==l && seg[id].r==r){
            seg[id].mark(average);
            return;
        }

        if(seg[id].lazy){
            seg[id<<1].mark(seg[id].v);
            seg[id<<1|1].mark(seg[id].v);
            seg[id].lazy=false;
        }

        int mid=(seg[id].l+seg[id].r)>>1;
        if(r<=mid)
            update(l,r,id<<1,average);
        else if(l>mid)
            update(l,r,id<<1|1,average);
        else{
            update(l,mid,id<<1,average);
            update(mid+1,r,id<<1|1,average);
        }
        seg[id].sum=seg[id<<1].sum+seg[id<<1|1].sum;
    }

    ll Search(int l,int r,int id){
        if(seg[id].l>=l && seg[id].r<=r)
            return seg[id].sum;
        if(seg[id].lazy){

            seg[id<<1].mark(seg[id].v);
            seg[id<<1|1].mark(seg[id].v);

            seg[id].lazy=false;
        }
        int mid=(seg[id].l+seg[id].r)>>1;
        if(r<=mid)
            return Search(l,r,id<<1);
        else if(l>mid)
            return Search(l,r,id<<1|1);
        else
            return Search(l,mid,id<<1)+Search(mid+1,r,id<<1|1);
    }

    void query(int id){
        if(seg[id].l==seg[id].r){
            if(seg[id].l!=1)
                putchar(' ');
            printf("%lld",seg[id].sum);
            return;
        }
        if(seg[id].lazy){

            seg[id<<1].mark(seg[id].v);
            seg[id<<1|1].mark(seg[id].v);

            seg[id].lazy=false;
        }
        query(id<<1);
        query(id<<1|1);
    }
    ll myceil(ll sum,int n){
        if(sum>=0)
            return sum/n+(sum%n!=0);
        else
            return sum/n;
    }

    ll myfloor(ll sum,int n){
        if(sum>=0)
            return sum/n;
        else
            return sum/n-(sum%n!=0);
    }
    int main()
    {
    #ifndef ONLINE_JUDGE
        freopen("in.txt","r",stdin);
        freopen("out.txt","w",stdout);
    #endif

        while(scanf("%d%d",&n,&m)!=EOF){
            oldSum=0;
            for(int i=1;i<=n;i++){
                scanf("%lld",&val[i]);
                oldSum+=val[i];
            }
            build(1,n,1);

            int l,r;
            ll average;

            while(m--){
                scanf("%d%d",&l,&r);
                curSum=Search(1,n,1);
                segSum=Search(l,r,1);
                if(curSum<=oldSum)
                    average=myceil(segSum,r-l+1);
                else
                    average=myfloor(segSum,r-l+1);
                update(l,r,1,average);
            }
            query(1);
            puts("");puts("");
        }
        return 0;
    }
