# fusion-stat 能否使用可读性 id

fusion-stat 的 0.0.6 版本更新计划中曾有一项是所有的 id 具有可读性，在我看来是一项能很大提升使用体验的特性，目前的主流数据应用中，都是采用随机或顺序生成的 "id" 类型的 id，比如 Arsenal, fotmob 是 9825, fbref 是 18bb7c10，transfermarkt 是 11。这反映在 url 查询中则是 https://fbref.com/en/squads/18bb7c10/Arsenal-Stats, https://www.transfermarkt.com/fc-arsenal/startseite/verein/11, 虽说添加了名字在 url 中提升可读性，但名字并不是查询的必要条件，真正的查询是通过 id，所以如果能在 id 中实现既有唯一性，又有可读性，就能很好的改善，甚至还可以拼写出 id。

要实现这样的 id，需要探讨两个问题，第一，能不能设计出设计出这样的 id，第二，能不能在 fusion-stat 中顺利实装。

fusion-stat 目前模型以及相互关系是这样的：

```python
class Competition:
    teams: list[Team]
    matches: list[Match]


class Team:
    staffs: list[Staff]
    players: list[Player]


class Staff:
    team: Team
    competition: Competition


class Player:
    team: Team
    competition: Competition


class Match:
    competition: Competition
    home: Team
    away: Team
```

而要考虑的因素：

1. 唯一
2. 可读
3. 尽可能的固定
4. 相互关系中的一致

首先是 competition, 赛事的名字不具有唯一性，比如在 fotmob 搜索 Premier League, 会得到 10 个以上的结果，但通常在一个足协单位内，赛事名称是具有唯一性的，比如英格兰的赛事就只有一个 Premier League，使用赛事名字和地区的组合便可用作 competition 的 id，ENG_Premier-League 这样的字符串具有可读性，而赛事名字和赛事地区都是很容易获取的特征，相互关系的一致也能保证。

然后是 team，与 competition 一样，这个世界上可能会有几个 Arsenel，但英格兰内只有一个 Arsenal，所以采用 ENG_Arsenal 这样的字符串作为 id 也是可行的。

接下来是 staff 和 player，名字不具有唯一性，所属俱乐部随着转会经常会变，甚至国籍也有可能更换。出生地是个不错的特征，但通常不能在 team 的数据源内找到，从而无法保证上下文一致，所以能采用的是名字 + 生日，比如 2001-09-05_Bukayo-Saka，同一天生日的人是否具有同名，放在世界范围内可能有很多，但放在球员里面可能就是很小概率的事件了，暂且把它当作可行。

最后是 match, 比赛日期 + 主队 + 客队名字，比如 2023-09-03_Crystal_Palace_vs_Wolverhampton_Wanderers, 和上面 team 讨论的一样，可能会 or, 但是 and 的概率很小，可以当作可行。

下面就是添加到 fusion-stat。country_name 和 country_code 各个数据源使用不一致，在写了 fifacodes 之后可以很好的解决。

后面的工作就没那么好进行下去了，上一级获取下一级的数据可以做到，最主要还是卡在了如何在下一级的数据中获取到上一级一致的特征。比如在 match 中需要获取 competition 和 team 所有的 id 特征，名字是基本特征容易获取到，但国家在目前的数据源内并不能找全，诚然目前可以把 competition 的国家用在 team，但之后添加了洲际比赛，世界级比赛，国家队比赛，这些就没办法使用了。

最终还是放弃了在 0.0.6 版本中更新 id，有可行性，但以目前的数据广度还不能实装，且 player 级的唯一性还需进一步优化，只能在未来不断扩展新的数据源中重点考虑这些特征直到全部可用了。
