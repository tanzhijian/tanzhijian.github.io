# 关于在 fusion_stat.models 中使用 shortlist 作为匹配辅助的探讨

fusion-stat 有一个一直让我不安的地方，就是在使用 rapidfuzz.process.extractOne 匹配时返回唯一结果的正确性，我并不确定他在扩展越来越多的数据源后能不能继续保持良好的运转，所以一直在探索一些方法解决。而今晚想到一个暂且看上去还不错，但也不是很好的，先上代码吧

```python
import typing
import warnings
from abc import ABC

from rapidfuzz import fuzz, process

_S1 = typing.TypeVar('_S1')
_S2 = typing.TypeVar('_S2')


MINIMUM_SIMILARITY = 50
SIMILARITY_DIFFERENCE = 5


class BaseModel(ABC):
    def __init__(self, show_warning: bool = True) -> None:
        self.show_warning = show_warning
        self._shortlist: list[typing.Any] = []

    @property
    def shortlist(self) -> list[typing.Any]:
        return self._shortlist

    def extract(
        self,
        query: _S1,
        choices: list[_S2],
        scorer: typing.Callable[..., int | float] = fuzz.WRatio,
        processor: typing.Callable[..., typing.Sequence[typing.Hashable]]
        | None = None,
        score_cutoff: int | float | None = None,
    ) -> _S2:
        results = process.extract(
            query,
            choices,
            scorer=scorer,
            processor=processor,
            score_cutoff=score_cutoff,
        )

        first = results[0]
        second = results[1] if len(results) > 1 else None
        if first[1] < MINIMUM_SIMILARITY:
            if self.show_warning:
                warnings.warn(
                    (
                        'The result similarity is less than 50%, '
                        'please check the shortlist.'
                    ),
                    SimilarityWarnings,
                )
            self._shortlist.append((query, results))
        elif (
            second is not None
            and abs(first[1] - second[1]) < SIMILARITY_DIFFERENCE
        ):
            if self.show_warning:
                warnings.warn(
                    (
                        'There are results that are too similar, '
                        'please check the shortlist.'
                    ),
                    SimilarityWarnings,
                )
            self._shortlist.append((query, results))

        return results[0][0]


class SimilarityWarnings(Warning):
    pass
```

我的大致思路是每个 model 都继承 BaseModel 获得 shortlist 和 extract，extract 是对 rapidfuzz.process.extract 的扩写，基本就是通过 rapidfuzz.process.extract 先获得初步结果 results，然后再进行一系列的判定：

* 如果最接近的结果小于 50% 则提示
* 如果最接近的两个结果过于相似也提示
* 并把所有的结果放到候选列表 shortlist
* 最终仍然会返回最接近的结果

在使用 rapidfuzz.process.extractOne 的地方替换成使用 self.extract。当然了上面的代码只是一个初步的草稿，并没有考虑太多的条件，数值胡乱设一些，shortlist 也没有封装，但大致思路是，在程序一些不能很好判定的时候，把检查核对交给使用者

但不好的地方在于，fusion-stat 面对的足球数据源通常只有两类：每个数据源都能够一一对应的数据类型，比如赛事，参赛球队，比赛，历史数据；每个数据源不能一一对应上的数据类型，比如球员名单，一些数据源会包含二队，青年队，位置参数，每个数据源对于位置的理解是有差别；而 extractOne 基本是在匹配后一类时会出错，所以 self.extract 并不能成为一个通用方法，而是专用方法

另一个顾虑是，在使用 extractOne 匹配不能一一对应的数据时目前是设置了 score_cutoff 参数一刀切，最小匹配策略，而如果想在这上面优化，默认返回的匹配结果将会是一个很大的问题，因为没有达到标准，如果要返回大概率将会是一个错误的结果，而同时还需要把 shorlist 交给使用者判定，如果使用者没有注意到 shortlist 呢，或者只是想把它跑在一个自动化程序里面并不想每天去观察改动呢

所以原本打算在 0.0.5 使用上这个功能，但又暂时不考虑了
