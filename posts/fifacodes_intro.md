# 介绍一下 fifacodes

fusion-stat 的开发过程有很多国家名称和国家代码转换的场景，一些数据源是使用国家名称，另外一些使用国家代码，在使用时需要那么一个工具来统一他们。最开始打算使用 pycountry, 但对于足球数据来说大多是使用国际足联成员国的国家地区来区分，而国际足联国家代码与 ISO 3166-1 三位字母代码是有差异的，比如使用英格兰 ENG 而不是英国 GBR。搜索了一下并没有现成的工具，只能自己写一个。

首先是数据源，维基百科有现成的表，爬下来即可。但直接使用有个问题是，国家代码是标准的，数据源与数据源的国家名称不一定是标准的，比如我国，大多数数据源是 China，一小部分是 China PR，以至于还需要一个 custom 来添加更多的别名，所幸两百多个国际足联成员国数量并不大，有了基础数据之后，这个 custom 采用手工维护即可。

接下来是方法了，我的设想是，整个国家代码和名称可以抽象成一个 Counties 类，而这个类本质上是一个只读 dict，可以通过 dict 的所有方法索引查询到一个包含代码和名称的 Country 类。

而索引可以并不只限于代码，它的数据特殊性在于，代码是唯一的，名称是唯一的，同时代码与名称之间也是唯一的，所以可以把他们全部添加为索引，既可以用代码也可以用名称，像这样:

```pycon
>>> counties.get('ENG')
Country(code='ENG', name='England')
>>> counties['England']
Country(code='ENG', name='England')
```

这样使用起来可以不论数据源是使用何种识别方式，都能很好的处理。但由于代码和名称同时在索引内，使用一些迭代方法的时候会出现重复的 value，所以最简单的方法便是使用两个 dict，使用 getitem 的方法时用 key + value 的 dict，使用 iter 时用只有 key 的 dict。

同时还有一个搜索方法，使用 rapidfuzz 来实现 key 的搜索，如果不确定准确的 key，输入一部分也可以获得结果：

```pycon
>>> counties.search('ARG')
[Country(code='ARG', name='Argentina'), Country(code='AFG', name='Afghanistan'), Country(code='ALG', name='Algeria')]
>>> counties.search_one('Argent')
Country(code='ARG', name='Argentina')
```

一些参数也是可以调节的：

```pycon
>>> counties.search('Fran', limit=2, score_cutoff=70)
[Country(code='FRA', name='France'), Country(code='IRN', name='Iran')]
```

基本功能就这些了，已经可以 pip 安装使用。

对于数据的更新，我的设想是默认的基础数据只通过脚本爬取维基百科进行更新，手动维护的 custom 接收 pr 提交，添加的条目代码通常不会有增加，而名称只作为别名添加到索引，返回的 value, Country 仍然使用 default 中的名称，这样比较好规范。
