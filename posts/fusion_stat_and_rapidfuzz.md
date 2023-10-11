# 关于在 fusion-stat 中使用 rapidfuzz 匹配名字

最近一有时间就在写一个叫 [fusion-stat](https://github.com/tanzhijian/fusion-stat) 的开源项目，这是我一直想做却一直搁置直到最近才下决心开坑的东西，这个世界上有很多免费公开的足球数据源，每个数据源有相同的数据也有特有的数据，很多时候这些数据都是分散的，fusion-stat 就是想做这么一件事，把各类数据源的不同数据寻找到相关的特征从而把它们匹配连接起来，使得一次调用便可以获取到多个来源的数据，譬如

```python
team = Team("Arsenal")
team.get()
team.info
team.players
```

输出的数据可以从各个数据来源中填充。

从各个数据源获取到需要的数据并不难，难在如何把它们准确的拼接起来，并不是每个数据源的名称都是一样的，比如 "UEFA Champions League" 与 "Champions League"; "Man United" 与 "Manchester United", "Manchester Utd"; "Gabriel Dos Santos" 与 "Gabriel"，直观能想到的就是自然语言处理，实体消歧义，实体链接，但用一个机器学习的模型对于这样一个项目太重了，且需要手动来标注校对很多数据，以我一个人的业余时间并不能做到，如果是本地项目可以使用数据库，也不是什么难的事情，对于足球这样的小数据你甚至可以手动拼接很可能效率高于写代码。。。但。。。所以只好想其他的方法，那就先用计算相似度了。

足球数据有一些特有的特征，比如球队，每个赛事内的球队名很难有相似的，且虽然是不同的数据源，但只要是一样的赛事一样的赛季，就一定可以一一对应上的，比如

```python
for t1 in teams_1:
    t2 = process.extractOne(t1, teams_2)
    print(f"{t1} is {t2[0]}")
```

```
Manchester City is Man City
Tottenham Hotspur is Tottenham
Liverpool is Liverpool
West Ham United is West Ham
Arsenal is Arsenal
Brighton & Hove Albion is Brighton
Crystal Palace is Crystal Palace
Brentford is Brentford
Nottingham Forest is Nottm Forest
Aston Villa is Aston Villa
Manchester United is Man United
Chelsea is Chelsea
Fulham is Fulham
Newcastle United is Newcastle
Wolverhampton Wanderers is Wolves
AFC Bournemouth is Bournemouth
Sheffield United is Man United
Everton is Everton
Luton Town is Luton
Burnley is Burnley
```

效果很好，但其他的数据，联赛，不同国家之间的联赛名可能会极其相似，比如 意甲联赛叫 Serie A，巴西的联赛也叫 Série A，但加上一些其他特征，比如国家或者地区，每个国家的各级联赛名字基本很难相似；球员名也是，每个球队不可避免的有些球员名之间极为相似，比如阿森纳的 Gabriel，他在 FotMob 的名字是 Gabriel，在 FBref 的名字是 Gabriel Dos Santos，如果只使用名字来做匹配拼接，他俩的相似度不如 Gabriel Jesus，所以需要加上其他的特征，比如目前在 fusion-stat 中使用到的国家和位置

```python
def fuzzy_similarity_mean(
    l1: list[str], l2: list[str], **kwargs: typing.Any
) -> float:
    scores = [fuzz.ratio(s1, s2) for s1, s2 in zip(l1, l2)]
    return sum(scores) / len(scores)


process.extractOne(
    ["Gabriel", "BRA", "DF"], 
    [
        ["Gabriel Dos Santos", "BRA", "DF"],
        ["Gabriel Jesus", "BRA", "FW"],
        ["Gabriel Martinelli", "BRA", "FW"],
    ],
    scorer=fuzzy_similarity_mean,
)
```

```
(['Gabriel Dos Santos', 'BRA', 'DF'], 85.33333333333333, 0)
```

对球员名和赛事并不是每个数据源都是相同的数量，上面提到的 FotMob 和 FBref，一线队名单一个是 25 一个 23，所以需要加上一个预设分数，如果相似度分数低于某个值则判定为两个人不予匹配，我大概设了一个值目前测试下来没什么问题，但也只是暂时，你不能避免万一某一支球队里面有两兄弟，他们名字只差一个字母，出生年月日，国籍，身高，位置都一样。。。需要在日后开发中再改进了。

至少对于目前开放的六个联赛的数据是没问题的。
