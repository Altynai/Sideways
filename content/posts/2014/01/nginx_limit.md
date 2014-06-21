Title: Nginx限制模块的共享内存
Date: 2014-01-22 22:16
Author: Altynai
Category: Code
Tags: Nginx, C/C++
Slug: nginx_limit
Email: Altynai.me@gmail.com


### 起因

对于Nginx中的`limit_conn_zone`和`limit_req_zone`两个模块，搜了一遍，发现网上都是讲这两个模块的意思和基本用法，却好像都没怎么细讲到一个问题：两个模块都配置了一个`内存最大值`来维护`$variable`（一般为`$binary_remote_addr`）所对应的请求数和请求速率，却没细说怎么维护，内存用完了怎么处理等问题。

### 重提

先再提提这两个模块的用法，换起一点回忆。

首先是`limit_conn_zone`

    :::python
    http {  
        limit_conn_zone $binary_remote_addr zone=addr:10m;  
        server {  
            location /home/ {  
                limit_conn addr 5;  
            }
        } 
    }

在`http`上下文中配置了最大为10m的内存块，维护`请求IP`的链接数：最多支持5个来自同一IP的并发连接。

然后是类似的`limit_req_zone`

    :::python
    http {  
        limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;  
        server {  
            location /search/ {  
                limit_req zone=one burst=5;  
            }  
        }  
    }

在`http`上下文中配置了最大为10m的内存块，维护`请求IP`的链接数：最多支持来自同一IP的1个/秒的请求频率，其中`burst=5`表示延迟队列的长度，最多能保持5个请求在等待队列中。

这些具体的信息官方文档上都有，这里就提及一下，主要说说下面的问题：

**拿limit\_conn\_zone来说，如果那块内存满了，新来的IP怎么处理？相应的内存替换机制是什么？**

### 找源码看看

这里参考了`Nginx-1.2.x`版本的源码，针对上面这个问题，可以分析个大概。

内部维护采用的数据结构为红黑树，树节点的key为`$variable`的hash值。

限制IP并发连接的模块在`src\http\modules\ngx_http_limit_conn_module.c`中，这里简化了`ngx_http_limit_conn_handler`函数中的代码，该函数功能上类似一个filter，在请求正式处理之前先进行过滤。

    :::c line_nums=True
    static ngx_int_t
    ngx_http_limit_conn_handler(ngx_http_request_t *r)
        lccf = ngx_http_get_module_loc_conf(r, ngx_http_limit_conn_module);
        limits = lccf->limits.elts;
        // 枚举并发的限制条件
        for (i = 0; i < lccf->limits.nelts; i++) {
            ctx = limits[i].shm_zone->data;
            vv = ngx_http_get_indexed_variable(r, ctx->index);
            len = vv->len;
            r->main->limit_conn_set = 1;
            hash = ngx_crc32_short(vv->data, len);
            shpool = (ngx_slab_pool_t *) limits[i].shm_zone->shm.addr;
            ngx_shmtx_lock(&shpool->mutex);
            node = ngx_http_limit_conn_lookup(ctx->rbtree, vv, hash);
            // 未在红黑树中找到对应结点，表示新来一个IP
            if (node == NULL) {
                n = offsetof(ngx_rbtree_node_t, color)
                    + offsetof(ngx_http_limit_conn_node_t, data)
                    + len;
                node = ngx_slab_alloc_locked(shpool, n);
                // 尝试分配结点内存，发现内存满了，直接返回503，并对连接内存池做次清理
                if (node == NULL) {
                    ngx_shmtx_unlock(&shpool->mutex);
                    ngx_http_limit_conn_cleanup_all(r->pool);
                    return NGX_HTTP_SERVICE_UNAVAILABLE;
                }
                // 分配成功，插入到红黑树中
                lc = (ngx_http_limit_conn_node_t *) &node->color;
                node->key = hash;
                lc->len = (u_char) len;
                lc->conn = 1;
                ngx_memcpy(lc->data, vv->data, len);
                ngx_rbtree_insert(ctx->rbtree, node);
            }
            // 这个IP已经在红黑树中，直接查看是否超了并发限制
            else {
                lc = (ngx_http_limit_conn_node_t *) &node->color;
                // 该IP并发数已经超了，直接返回503，并对连接内存池做次清理
                if ((ngx_uint_t) lc->conn >= limits[i].conn) {
                    ngx_http_limit_conn_cleanup_all(r->pool);
                    return NGX_HTTP_SERVICE_UNAVAILABLE;
                }
                // 新增一个并发
                lc->conn++;
            }
        }
        return NGX_DECLINED;
    }

所以，当发生以下两种情况时，会对内存进行整理的工作：

* 来了一个新IP，我要维护这个新IP的并发数，发现内存不够用了
* 来了一个旧IP，发现这个IP并发数已经>=limit了

其中，`ngx_http_limit_conn_cleanup_all`的操作简单的说即遍历内存池中的结点，对这些结点的每个连接数
- 1，如果连接数为0，则将其从树中删除，释放结点内存。

这样的好处是，在某些恶意IP尝试疯狂发请求时，其并发连接数始终维持在limit，能直接快速的503，根本不需要执行这个请求，而对那些正常的连接数较小的IP并不造成影响。

而`limit_req_zone`的逻辑有点麻烦，看明白了再回来补充。

暂时先写这么个大概，希望对你有用。
