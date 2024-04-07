# 我所设想的 fusion-stat 数据模型

目前 fusion-stat 模型总共分为 Competitions, Competition, Team, Staff, Player, Matches, Match, 他们之间自成一派，并没有什么关联，且最大的问题是数据规则是写死的，即开发者制定了所有的规则，用户能修改或定制的部分很少，要么便是自己 import spiders 来重写。

我的设想是统一数据模型。目前为止每个爬虫子模块里面的 item 都是单独定义，很灵活，但当你需要从其他地方导入的时候就不是很优雅，比如会出现大段大段的 `spiders.transfermarkt.competition.Item` 这样的字段，统一设计数据模型之后，就可以从 models 里面导入。

大概思路是这样，以 competition 作为例子：

```python
class Stat:
    def __init__(
        self,
        id: str,
        name: str,
        **fields: typing.Any,
    ) -> None:
        self.id = id
        self.name = name
        self.fields = fields


class Competition(Stat):
    def __init__(
        self,
        id: str,
        name: str,
        country_code: str,
        teams: list['Team'] | None = None,
        matches: list['Match'] | None = None,
    ) -> None:
        super().__init__(id, name)
        self.country_code = country_code
        if teams is None:
            teams = []
        self.teams = teams
        if matches is None:
            matches = []
        self.matches = matches
```

每个爬虫子模块的 Competition Item 从父类继承，只要满足父类对于 Competition 定义的字段即可，每个爬虫的特殊字段都塞到 fields 中，至于数据结构，是类还是 dict，又或者其他再讨论。待到从每个爬虫模块收集的数据完毕之后，他们的合并方式，统一在每个类中实现一些 merge 方法，定义了合并之后字段处理的规则，然后再实现 `add` 方法，每两个数据类结果想要相加，直接调用方法即可，类似于 `competition1.add(competition2)`，甚至可以实现 `__add__` 通过运算符操作

```python
def add(self, new: 'Competition') -> 'Competition':
    teams = self._concat_teams(new.teams)
    matches = self._concat_matches(new.matches)
    fields = self.fields | new.fields
    return Competition(
        id=self.id,
        name=self.name,
        country_code=self.country_code,
        teams=teams,
        matches=matches,
        **fields,
    )

def _merge_teams(
    self,
    news: typing.Sequence['Team'],
) -> list['Team']:
    results: list['Team'] = []
    for query in self.teams:
        selected = process.extractOne(
            query,
            news,
            processor=lambda x: x.name,
        )
        result = selected[0]
        results.append(query.add(result))
    return results

def _concat_matches(
    self,
    news: typing.Sequence['Match'],
) -> list['Match']:
    ...
```

开发者可以任意调整预先要用到的数据类，把他们 add 到一起，比起现版本

```python
class Competition:
    def __init__(
        self,
        fotmob: spiders.fotmob.competition.Item,
        fbref: spiders.fbref.competition.Item,
        official: spiders.official.competition.Item,
        transfermarkt: spiders.transfermarkt.competition.Item,
    ) -> None:
        self._fotmob = fotmob
        self._fbref = fbref
        self._official = official
        self._transfermarkt = transfermarkt
```

这样的形式优雅很多，然后定义数据规则方法，提供 api。

如果用户不认同这些规则，也可以自己 add，比起现版本也会方便很多。
