Title: 空数组
Date: 2013-04-23 18:43
Author: Altynai
Category: Code
Tags: C/C++, Redis
Slug: empty-array

这是在看Redis源码的时候遇到的，由于底层字符串是封装了C风格的字符串，在`src/sds.h`可以看到这个结构的申明：

    :::c
    typedef char *sds;
    struct sdshdr {
        int len;
        int free;
        char buf[];
    };

### buf为什么定义成*空数组*？

这个结构体的大小是8，即使你写成`char buf[0]`，它的大小还是8，但是`buf`不是0的时候显然`sizeof(sdshdr)`就变了，此时还要考虑内存对齐的情况。这么定义的好处在于`buf`这个字符缓冲区不会被定死，可以很好的处理变长的问题。

如果定义成`char* buf`的话，结构体的大小会变大，而且在构造函数里需要给`buf`动态的分配空间，这里管理的不好就会有内存泄露的问题。

### 技巧

`buf`这个指针的大小本身不算进结构体，*它指向的是紧跟在*`free`*后面的那个空间*，  

所以，在新建`sds`的时候，Redis实际上新建了一个`sdshdr`，返回的是这个`sdshdr`中`buf`的地址。

    :::c
    struct sdshdr *sh = malloc(sizeof(struct sdshdr) + buflen + 1);
    // other things
    return (char*)sh->buf;

里面有个技巧就是通过`buf`获得`sdshdr*`，换句话说，通过\`sds\`得到\`sdshdr\`。
    
    :::c
    sds s = .....
    struct sdshdr *sh = (void*) (s - (sizeof(struct sdshdr)));
