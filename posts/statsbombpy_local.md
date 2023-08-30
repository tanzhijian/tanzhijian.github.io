# statsbombpy-local

最近频繁使用 statsbombpy 获取数据，等待网络请求是件很烦的事情，所以想着改写一下这个库，反正都是在 GitHub 请求公开数据，把它的 open-data 拉到本地，每次从本地读取岂不是很爽。

最开始想着 fork 一个分支直接修改，确实很省事，在 public.py 里添加一个本地读取的函数，然后把使用 requests 的地方换成本地读取，再修改一些配置，设定好本地环境变量，改一下测试通过即可。

但是这样做的缺点是如果主分支每次有新版本都得去合并，由于修改删除的代码处数还不少，合并多了就会很烦，所以还是作罢。不过代码还在，[statsbombpy-local-old ](https://github.com/tanzhijian/statsbombpy-local-old/blob/master/statsbombpy/public.py)，想用的仍然可以用。

新建一个从外部扩展功能的库，原代码比较烦的一点是全写的函数，而且没有什么接口可以修改到内部，原本想的是像 requests-file 这样通过 file:// URLs 访问本地文件系统

```python
s = requests.Session()
s.mount('file://', FileAdapter())

resp = s.get('file:///path/to/file')
```

又或者继承一个 Requests 类来改写，但原代码

```python
def get_response(path):
    response = req.get(path)
    response.raise_for_status()
    data = response.json()
    return data
```

这样的写法是摸不到内部，所以只能换一个思路，也就是目前使用的 mock，拦截掉网络请求，从本地本地读取文件后返回请求，但这样的做法可能不是很优雅，因为 mock 通常用于测试。。。

然后就是写。目前可以从 statsbombpy-local 使用 statsbombpy 的所有方法，但只有 competitions, matches, lineups, events 和 frames 从本地读取，其他的几个，player_match_stats，player_season_stats，team_season_stats 需要 key 才能使用，不作考虑保持原样。

而 competition_events，competition_frames，它们的流程是先获取赛事赛季 id，然后获取所有的比赛 id，再获取所有的 events 或者 frames，组一起得到一个 DataFrame。我能做的只是顺着它的思路，获取到赛事，比赛，事件的查询 id 从本地读取文件后注册到 mock，再调用原本函数开始请求，但原本函数里使用了多进程 Pool，于是导致了很多莫名其妙的 ConnectingError，懒得去探究了，就此作罢，继续使用原函数。要用类似的功能现写也用不了几行代码。

暂时这样了，想要使用的 pip 安装即可。
