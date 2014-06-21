Title: Hdu 4391 Paint The Wall 线段树(优化)
Date: 2012-08-23 21:57
Author: Altynai
Category: Code
Tags: HDU, ACM
Slug: hdu-4391-paint-the-wall

<span style="color: #ff00ff;">【hdu
4391】</span><http://acm.hdu.edu.cn/showproblem.php?pid=4391>

【题意】100000个点，100000个操作，操作1把[l,r]的点涂成颜色z，操作2查询[l,r]内颜色为z的点个数，`0<=z<=2^31`

【思路】2012多校最后一场，当时是我上去敲的，我一开始的思路：线段树记录两个附加域
ncolor表示这段的颜色（-1表示这段为多种颜色）nor表示整段所有颜色的或值。更新就不多说了，`push_up`和`push_down`函数不要写错就好。然后查询的时候，假设查询到一个线段，如果这个线段内部包含z这个颜色，那么一定满足`nor&z>=z`（都看成二进制就好理解了），交了之后T了。。。后来想了一下这个剪枝太他妈的不够了。。因为`z=0`的话，会更新到每个叶子！这你妹！后来想到再附加上两个域：vmin和vmax表示线段内最小和最大的颜色编号（算得上是query时候的一个剪枝）。然后就过了。

    :::cpp
    #define ll unsigned int
    #define lson (id<<1)
    #define rson (id<<1|1)

    int n, m, color[N];
    struct Node {
        int l, r;
        ll vmin, vmax;
        ll ncolor, nor;
    } node[N * 4];

    void push_up(int id) {
        if(node[lson].ncolor == -1 || node[rson].ncolor == -1)
            node[id].ncolor = -1;
        else if(node[lson].ncolor != node[rson].ncolor)
            node[id].ncolor = -1;
        else
            node[id].ncolor = node[lson].ncolor;

        node[id].nor = node[lson].nor | node[rson].nor;
        node[id].vmin = min( node[lson].vmin, node[rson].vmin);
        node[id].vmax = max( node[lson].vmax, node[rson].vmax);
    }

    void push_down(int id) {
        if(node[id].ncolor != -1) {
            node[lson].ncolor = node[id].ncolor;
            node[lson].nor = node[id].nor;
            node[lson].vmin = node[id].vmin;
            node[lson].vmax = node[id].vmax;

            node[rson].ncolor = node[id].ncolor;
            node[rson].nor = node[id].nor;
            node[rson].vmin = node[id].vmin;
            node[rson].vmax = node[id].vmax;
        }
    }

    void build(int id, int l, int r) {
        node[id].l = l;
        node[id].r = r;
        if(l == r) {
            node[id].ncolor = color[l];
            node[id].nor = color[l];
            node[id].vmax = color[l];
            node[id].vmin = color[l];
            return;
        }

        int mid = (l + r) >> 1;
        build(lson, l, mid);
        build(rson, mid + 1, r);
        push_up(id);
    }

    void update(int id, int l, int r, ll z) {
        if(node[id].l == l && node[id].r == r) {
            node[id].ncolor = z;
            node[id].nor = z;
            node[id].vmax = z;
            node[id].vmin = z;
            return;
        }
        push_down(id);
        int mid = (node[id].l + node[id].r) >> 1;
        if(r <= mid)
            update(lson, l, r, z);
        else if(l > mid)
            update(rson, l, r, z);
        else {
            update(lson, l, mid, z);
            update(rson, mid + 1, r, z);
        }
        push_up(id);
    }

    int query(int id, int l, int r, ll z) {
        if(node[id].vmax < z || node[id].vmin > z)
            return 0;
        if((node[id].nor & z) < z)
            return 0;

        int mid = (node[id].l + node[id].r) >> 1;

        if(node[id].l == l && node[id].r == r) {

            if(node[id].ncolor != -1) {

                if(node[id].ncolor == z)
                    return node[id].r - node[id].l + 1;
                else
                    return 0;
            }
            else {

                if((node[id].nor & z) >= z)
                    return query(lson, l, mid, z) + query(rson, mid + 1, r, z);
                else
                    return 0;
            }
        }
        push_down(id);
        if(r <= mid)
            return query(lson, l, r, z);
        else if(l > mid)
            return query(rson, l, r, z);
        else
            return query(lson, l, mid, z) + query(rson, mid + 1, r, z);
    }

    int main() {
    #ifndef ONLINE_JUDGE
        freopen("in.txt", "r", stdin);
        freopen("out.txt", "w", stdout);
    #endif

        int a, l, r;
        ll z;
        while(scanf("%d%d", &n, &m) != EOF) {
            for(int i = 0; i < n; i++)
                scanf("%u", &color[i]);

            build(1, 0, n - 1);
            while(m--) {
                scanf("%d%d%d%u", &a, &l, &r, &z);
                if(a == 1)
                    update(1, l, r, z);
                else
                    printf("%d\n", query(1, l, r, z));
            }
        }
        return 0;
    }

