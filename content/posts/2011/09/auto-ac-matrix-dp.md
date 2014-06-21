Title: hdu 3962 & hdu 2243 & zjut 1734 AC自动机,矩阵,DP
Date: 2011-09-20 13:13
Author: Altynai
Category: Code
Tags: DP, ACM
Slug: auto-ac-matrix-dp

<span style="color: #ff00ff;">[hdu
3962]</span> <http://acm.hdu.edu.cn/showproblem.php?pid=3962>

题目大意：给你N个DNA片段，问你长度为L的DNA中至少包含2个给定片段的种数。

思路：想到一共的种数为`4^L`，我们只要减去不包含和只包含1个给点片段的种数。

首先，构造好自动机，然后就是构造矩阵。假设自动机一共有n个结点（包括）root，编号0,1....n-1，矩阵的规模为（2n
X 2n）

- i点（0≤i＜n）表示到trie图中i点不经过危险结点的路径数

- i点（n≤i＜2*n）表示到trie图中i-n点经过一次危险结点的路径数

所以，对于i点（0≤i＜n）的每一个儿子结点j：

如果j是安全结点，`matrix[i][j]++ matrix[i+n][j+n]++`

否则`matrix[i][j+n]++`


    :::cpp
    #include <iostream>
    #include <algorithm>
    #include <queue>
    #include <string>
    #include <cstdio>
    #include <set>
    #define N 4
    #define M 70
    #define mod 10007
    using namespace std;
    int n,L;
    char ch[M];

    //以上题目所需数据
    inline int toInt(char c){
        if(c=='A')
            return 0;
        else if(c=='C')
            return 1;
        else if(c=='G')
            return 2;
        else
            return 3;
    }
    int root,tot;
    int que[M],head,tail;
    struct Node
    {
        int child[N],fail,flag;

        void init(){
            memset(child,0,sizeof(child));
            fail=-1,flag=0;
        }
    }T[M];

    void init(){
        root=tot=0;
        T[root].init();
    }

    void insert(char* s)
    {
        int p=root,index;
        while(*s)
        {
            index=toInt(*s);
            if(!T[p].child[index]){
                T[++tot].init();
                T[p].child[index]=tot;
            }
            p=T[p].child[index];
            s++;
        }
        T[p].flag=1;
    }

    void build_ac_auto(){
        head=tail=0;
        que[tail++]=root;

        int u,son,p;
        while(head<tail){
            u=que[head++];
            for(int i=0;i<N;i++){
                if(T[u].child[i]){
                    son=T[u].child[i];
                    p=T[u].fail;
                    if(u==root)
                        T[son].fail=root;//第二层的fail直接指向root
                    else
                    {
                        T[son].fail=T[p].child[i];
                        T[son].flag|=T[ T[son].fail ].flag;
                    }
                    que[tail++]=son;
                }else{//trie图中从根出发不存在,直接设立虚拟节点,即root
                    p=T[u].fail;
                    if(u==root)
                        T[u].child[i]=root;
                    else
                        T[u].child[i]=T[p].child[i];
                }
            }
        }
    }

    //以上自动机结束

    inline int toId(int i,int bi){
        if(bi==0)
            return i;
        else
            return i+tot+1;
    }

    inline int Pow(int n,int L){
        int res=1;
        while(L){
            if(L&1)
                res=res*n;
            n*=n;
            res%=mod;
            n%=mod;
            L>>=1;
        }
        return res;
    }
    struct Matrix
    {
        int mat[M][M];
        void init(){
            memset(mat,0,sizeof(mat));
        }
        void one(){
            for(int i=0;i<M;i++)
                mat[i][i]=1;
        }
        void put(int n){
            for(int i=0;i<=n;i++){
                for(int j=0;j<=n;j++)
                    printf("%d ",mat[i][j]);
                puts("");
            }
            puts("");
        }
        friend Matrix operator*(const Matrix& a,const Matrix& b){
            Matrix res;
            res.init();
            for(int i=0;i<M;i++){
                for(int j=0;j<M;j++){
                    for(int k=0;k<M;k++){
                        res.mat[i][j]+=a.mat[i][k]*b.mat[k][j];
                        res.mat[i][j]%=mod;
                    }
                }
            }
            return res;
        }
    }op,ymd;

    int main()
    {
    #ifndef ONLINE_JUDGE
        freopen("in.txt","r",stdin);
        freopen("out.txt","w",stdout);
    #endif

        int cas,pcas=1;
        //scanf("%d",&cas);
        while(scanf("%d%d",&n,&L)!=EOF)
        {
            init();
            for(int i=0;i<n;i++){
                scanf("%s",&ch);
                insert(ch);
            }
            build_ac_auto();

            int ans=Pow(4,L);
            op.init();
            for(int i=0;i<=tot;i++){
                for(int j=0;j<N;j++){
                    int id=T[i].child[j];
                    if(T[id].flag==0)
                        op.mat[toId(i,0)][toId(id,0)]++;
                    else
                        op.mat[toId(i,0)][toId(id,1)]++;
                    if(T[id].flag==0)
                        op.mat[toId(i,1)][toId(id,1)]++;
                }

            }
            ymd.init();
            ymd.one();
            while(L){
                if(L&1)
                    ymd=ymd*op;
                op=op*op;
                L>>=1;
            }
            for(int j=0;j<=tot;j++){
                for(int k=0;k<2;k++){
                    ans-=ymd.mat[0][toId(j,k)];
                    if(ans<0)
                        ans+=mod;
                }
            }
            if(ans<0)
                ans+=mod;
            printf("%d\n",ans);
        }
        return 0;
    }

<span style="color: #ff00ff;">[hdu
2243]</span> <http://acm.hdu.edu.cn/showproblem.php?pid=2243>

题目大意：给你N个词根，问你长度≤L的单词中至少包含1个给定片段的种数。

思路：一共的种数为`26^1+26^2+....+26^L`，我们只要减去不包含词根种数。

方法和上面一题一样，只不过矩阵规模n X n

对于i点（0≤i＜n）的每一个儿子结点j:

如果i和j都是安全结点，`matrix[i][j]++`

然后就是求矩阵`A + A^2 + A^3 + .... + A^L`,这个就是经典的双重2分题目了。

详细可见<span style="color: #ff00ff;">[poj
3233] </span><http://acm.pku.edu.cn/JudgeOnline/problem?id=3233>

这题由于是mod 2^64 所以只要用`unsigned long long`就行了，因为溢出截取的低位部分范围就是`[0,2^64)`

代码就不贴了~上面的这个代码稍微改一下就行了。

<span style="color: #ff00ff;">[zjut
1734]</span> <http://acm.zjut.edu.cn/ShowProblem.aspx?ShowID=1734>

同样的，先构造好自动机，然后处理dp部分。dp[i][j]表示第i天到trie图中的第j个结点还存活的概率。

由于给出单细胞的初始序列，我们可以根据这个序列，看看初始在root点经过这个序列跑到了trie图中的哪个点，假如是A点，那么初始化dp[0][A]=1.0

转移：对于i结点的儿子j，如果i，j都是安全结点，`dp[k+1][j]+=dp[k][i]*P(a,c,g,t)`

代码忘记存了 = = 不过应该还好敲的吧。
