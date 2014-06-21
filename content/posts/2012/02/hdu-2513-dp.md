Title: Hdu 2513 DP
Date: 2012-02-05 16:26
Author: altynai
Category: ACM
Tags: DP, HDU
Slug: hdu-2513-dp

**<span style="color: #ff00ff;">【Hdu
2513】</span>**http://acm.hdu.edu.cn/showproblem.php?pid=2513  

【题意】给你20\*20的格子（一个蛋糕），有些格子上有樱桃，让你把蛋糕切成若干块，每块是矩形或者正方形，每块蛋糕上有且只有一个樱桃，求总的切的长度最小。  

【想法】我的想法就是用一个状态dp[i][j][x][y]表示切（i,j）到（i+x-1,j+y-1）这个矩形的最小值。然后分情况讨论这个矩形。  
1.矩形内没有樱桃  
2.矩形内只有一个樱桃  
3.矩形是1xN或者Nx1的规模  
4.其他情况

其实有几种情况可以合起来讨论的。  

第4中情况只要枚举切行和切列的情况就可以了，我觉得要注意的地方就是切行和切列的时候要保证2块蛋糕上分别至少有1个樱桃，这样切才是合法的。

最后很容易错的地方就是x,y这两重循环要写在最外面。

``` {.brush: .cpp; .collapse: .true; .light: .false; .toolbar: .true; .notranslate title="hdu 2513"}
int n,m;
bool cake[N][N];
int dp[N][N][N][N];//dp[i][j][a][b]=> min (i,j)->(i+a-1,j+b-1)

int mycount(int x1,int y1,int x2,int y2){
    int cnt=0;
    for(int i=x1;i<=x2;i++){
        for(int j=y1;j<=y2;j++){
            if(cake[i][j])
                cnt++;
        }
    }

    return cnt;
}

inline void zy(int &a,int b){
    if(b<a)
        a=b;
}

int main()
{
#ifndef ONLINE_JUDGE
    freopen("in.txt","r",stdin);
    freopen("out.txt","w",stdout);
#endif

    int cas,pcas=1;
    int x,y,ii,jj;

    while(scanf("%d%d%d",&n,&m,&cas)!=EOF){
        memset(cake,false,sizeof(cake));
        memset(dp,127,sizeof(dp));

        for(int i=0;i<cas;i++){
            scanf("%d%d",&x,&y);
            cake[x][y]=true;
        }

        for(int x=1;x<=n;x++){
            for(int y=1;y<=m;y++){
                for(int i=1;i+x-1<=n;i++){
                    for(int j=1;j+y-1<=m;j++){

                        ii=i+x-1;
                        jj=j+y-1;
                        int cnt=mycount(i,j,ii,jj);

                        if(i==ii && j==jj)
                            dp[i][j][x][y]=0;
                        else if(cnt==0)
                            dp[i][j][x][y]=0;
                        else if(cnt==1)
                            dp[i][j][x][y]=0;
                        else if(i==ii || j==jj)
                            dp[i][j][x][y]=cnt-1;
                        else{

                            //切行
                            for(int row=i;row<ii;row++){
                                if(mycount(i,j,row,jj)>=1 && mycount(row+1,j,ii,jj)>=1){

                                    zy(dp[i][j][x][y],
                                        dp[i][j][row-i+1][y]+dp[row+1][j][ii-(row+1)+1][y]+y);
                                }
                            }
                            //切列
                            for(int column=j;column<jj;column++)
                                if(mycount(i,j,ii,column)>=1 && mycount(i,column+1,ii,jj)>=1){

                                    zy(dp[i][j][x][y],
                                        dp[i][j][x][column-j+1]+dp[i][column+1][x][jj-(column+1)+1]+x);
                                }
                        }
                    }
                }
            }
        }
        printf("Case %d: %d\n",pcas++,dp[1][1][n][m]);
    }
    return 0;
}
```
