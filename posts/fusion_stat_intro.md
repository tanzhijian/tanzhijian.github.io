# 介绍一下 fusion-stat

更新：已经更新 API

---

最初只是想给 score-simulator 写一个获取数据的脚本，但写着写着应该可以写成一个工具，可以方便获取网络上免费公开足球数据的爬虫工具，到目前为止可以正常给 score-simulator 提供数据了，于是发布了一个版本到 pip 方便自己使用。

他的特点是同时从不同的数据源获取然后组合在一起。因为这确实是获取足球数据一个很麻烦的事情，从一个数据源获取一些数据，从另一个数据源获取另一些数据，他们大多数基础数据是相同的，只有一些不同的特色数据，而 fusion-stat 便是在获取数据时就把它们最大程度的拼接在一起，通过一次调用就可以获得一份尽可能全面的数据。

```python
competitions = Competitions()
fusion = await competitions.gather()
```

使用 httpx 完成 downloader 类似的功能，所以提供了可以在初始化时传入 httpx.AsyncClient 的一些参数，比如 `competitions = Competitions(proxies=PROXIES)`，由于是通过 `**kwargs`，缺乏参数类型补全提示，后续还会改进。每个类都会初始化一个 AsyncClient 作为 client，如果是大量爬取势必会增加开销，所以还可以提前创建好一个 client 每次传入使用:

```python
async with httpx.AsyncClient(proxies=PROXIES) as client:
    competition = Competition(
        fotmob_id="47", 
        fbref_id="9", 
        fbref_path_name="Premier-League",
        official_name="Premier League",
        season=2022,
        client=client,
    )
```

关于参数，最初的设想是只需要传入一个具有唯一特征同时还有可读性的参数，比如：

```python
member = Member("Bukayo Saka")
```

很漂亮但显然不具有可行性。且不说唯一性，单是如何通过一行字符串到最终完成不同数据源的请求 url 都很困难，如果只是赛事，或者球队，即使规模扩大到很大，几百个赛事，几千支球队，可以通过缓存一份数据来提供查询，但更多的球员名，随时在增加的比赛，就不大可能缓存下来了，这无异于还得提供一个数据库。

所以目前采用这样一种方法，不是很方便手动输入，但可以通过上一级获取到的 index 来使用：

```python
fusion = await team.gather()
saka = fusion.members_index()[-2]
saka
```

```
{'fotmob_id': '961995',
 'fbref_id': 'bc7dc64d',
 'fbref_path_name': 'Bukayo-Saka'}
```

```python
member = Member(**saka)
fusion = await member.gather()
```

如果需要长期使用，在第一次获取时本地缓存一份 index，就可以极大的方便后续使用了。

目前数据源只写了很小的一部分，只满足了 score-simulator 的需求，之后会继续完善。如果想要添加更多的数据，或者更多的来源，在 spiders 里面新建一个模块继承 Spider 类，然后实现 request 和 parse:

```python
class Futbol(Spider):

    @property
    def request(self) -> httpx.Request:
        ...

    def parse(self, response: httpx.Response) -> Any:
        ...
```

可以参考其他的爬虫写法。之后在对应的 fusion 添加进去即可，欢迎提交 pr。

总体来说，目前处于一个能用但不好用的地步。需要改进的地方太多，比如最后的数据类 Fusion，虽然都是 fusion，但方法大相径庭，需要一个更好的方案；models 里面的各种杂乱的数据模型类看起来很糟糕；也没有文档，想要正常使用得看源代码。慢慢写了，最初设计的时候并没有规划太多，大部分都是写一步看一步。
