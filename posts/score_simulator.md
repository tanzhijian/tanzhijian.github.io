# score-simulator 的一些想法

最近在利用业余时间入门 2023 年前端的新姿势，前两天无聊趁着欧冠决赛前夜，用目前所学到的写了一个前端的比分模拟器 [score-simulator](https://score-simulator.tanzhijian.org/)，小规模发给了一些朋友 roll，反响居然不错，都 roll 得蛮开心的。所以想说一下模拟比赛的原理，以及之后会完善的一些思路。

score-simulator 的模型设想是通过简化的方式来模拟一场比赛，在比赛中随机出现进球，但不能是完全随机，需要参考现实中的表现参数。所以首先是每分钟的射门事件，主队 + 客队本赛季的平均每 90 分钟射门次数，得到比赛每分钟射门的概率。

接下来如果产生了射门，那么是谁的。这里使用了一方射门数 / 射门总数得出主客队射门占比。

但由于两队实力的不均衡，使用了队伍的排名 [clubelo](http://www.clubelo.com/) 作为权重，强的队伍 = 1, 弱的队伍 /= 强的队伍。

再使用双方赛季总预期进球 / 赛季总射门次数，得到双方的每次射门的平均预期进球 xG/Sh，来确定本次射门是否进球。

到这里模拟了每分钟的事件，运行 90 次得到一场比赛的结果。

```python
def whoscored(home_goal: int = 0, away_goal: int = 0) -> tuple[int, int]:
    attempt = rnd.rand(1, 1)
    if attempt < shot_prob_per_minute:
        who = rnd.rand(1, 1)
        if who < shot_percentage:
            shot = rnd.rand(1, 1)
            if shot < home_xg_per_shot:
                home_goal += 1
        else:
            shot = rnd.rand(1, 1)
            if shot < away_xg_per_shot:
                away_goal += 1
    return home_goal, away_goal


def play_game():
    for _ in range(90):
        pass
```

之后会完善一下模拟比赛的模型，比如加上一些正态分布，使得比分结果更为合理，比如一些考虑到防守质量的参数。

还会获取现实的赛程表和数据，也能自己编辑队伍，使得在更多的比赛开场前都能玩一玩。
