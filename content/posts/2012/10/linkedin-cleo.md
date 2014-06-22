Title: 对于Cleo@LinkedIn的一些小分析和体会
Date: 2012-10-12 16:51
Author: Altynai
Category: Code
Tags: Java
Slug: linkedin-cleo

Cleo是LinkedIn的一个开源项目，主要应用还是[Typeahead][]这块地方。项目的主页链接：<http://sna-projects.com/cleo/>

大致的介绍以及简单的架构可以在那里看到，这里就不再重复。然后，最下面引用了两篇相关的论文。其中，第一篇是Facebook的Typeahead开发团队成员写的一个关于Typeahead的生命周期的文章，第二篇是几个THU大牛写的相关方案。我对这两篇文章做了简单的翻译，英语水平有限，凑合着看吧，传到百度文库了，地址：[第一篇][]，[第二篇][]。

![][demo-pic]

推荐的做法就是去运行一下它给的[Demo][]，其中有`Generic Typeahead`和`Network Typeahead`这两个部分，然后深入的去研究它的实现机理。

好了，下面主要说一下对`Generic Typeahead`这块的理解（`Network Typeahead`这部分的道理与其基本一致）。

假设现在有一些公司（Document）的列表，数据库中的每条记录就代表一个公司。每个公司都有自己的属性：编号（DocumentId），名称（Name），关键字（Terms，用于搜索匹配），分数（Score，用于结果排序）。举个例子，现在要搜索`Apple Inc`，当你输入`ap`的时候就要显示这条记录了。

### Generic Typeahead对这些Document的信息做了什么处理？

简单的说就是进行以下的三步：

- 通过配置文件来生成硬盘上数据持久化的文件块，包括索引文件，数据段文件等（第二次重新加载原数据的话，可以更改配置文件中的elementStoreCached=true）。

- 对于每个Document，通过[FNVHash][]将其Terms的**特定前缀长度**转化成一个long型值，保存到[Bloom Filter][]的数组（long bloomFilter[]下标为DocumentId）中。

        :::java
        public static final long computeBloomFilter(String s, int prefixLength) {
            int cnt = Math.min(prefixLength, s.length());
            if (cnt <= 0) return 0;
        
            long filter = 0;
            int bitpos = 0;
        
            long hash = Fnv1Hash32.FNV_BASIS;
            for(int i = 0; i < cnt; i++) {
                char c = s.charAt(i);
          
                hash ^= 0xFF & c;
                hash *= Fnv1Hash32.FNV_PRIME;
                hash &= Fnv1Hash32.BITS_MASK;
          
                hash ^= 0xFF & (c >> 8);
                hash *= Fnv1Hash32.FNV_PRIME;
                hash &= Fnv1Hash32.BITS_MASK;
          
                bitpos = (int)(hash % NUM_BITS);
                if(bitpos < 0) bitpos += NUM_BITS;
                filter |= 1L << bitpos;
            }
            return filter;
        }

- 对Terms里面的每个Term，在其[反向索引][]的记录集合中添加当前的DocumentId

- 讲Document写到二进制数据块中。

### 查询的流程是怎么样的？

- 我们可以把一个查询（例如，`"App Inc"`）想象成一个Terms（用空格来分割查询串，例如，`{"App”，“Inc”}`，如果包含中文的话，可以使用[Ansj][]来做中文分词）。

- 对于每个Term，我们在反向索引中找到最小的DocumentId的集合（这个优化方法在第二篇论文中提到过），记错`X`。

- 对查询串做同样的Hash，得到一个long型值queryHashValue。

- 遍历X中的每个DocumentId，如果`queryHashValue & bloomFilter[DocumentId]==queryHashValue`（按位与），则DocumentId对应的Document就是一个满足条件的结果。
这一步可以参照`GenericTypeahead.java`内部的[applyFilter][]函数。

- 对结果集排序，选择score较大的K个返回。

### 整体感悟

Cleo的功能的确很强大，数据大了话能支持分片集群，但是代码写的很是难懂，要完全看懂要花点时间，蛋疼的是其中还引入了另外一个开源项目[Krati][] 有时间的话，请顺带把那个看了吧。

  [Typeahead]: http://en.wikipedia.org/wiki/Typeahead
  [第一篇]: http://wenku.baidu.com/view/4845099e51e79b896802263f.html
  [第二篇]: http://wenku.baidu.com/view/34dd29add1f34693daef3e3f.html
  [Demo]: https://github.com/jingwei/cleo-prime
  [FNVHash]: http://www.isthe.com/chongo/tech/comp/fnv/
  [Bloom Filter]: http://en.wikipedia.org/wiki/Bloom_Filter
  [反向索引]: http://en.wikipedia.org/wiki/Inverted_index "反向索引"
  [Ansj]: http://www.ansj.org/
  [Krati]: http://data.linkedin.com/opensource/krati
  [applyFilter]: https://github.com/linkedin/cleo/blob/master/src/main/java/cleo/search/typeahead/GenericTypeahead.java#L246
  [demo-pic]: http://altynai-blog-images.qiniudn.com/2012/10/linkedin-cleo-1.png
  
