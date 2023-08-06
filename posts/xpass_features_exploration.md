# xPass 模型的特征探索

StatsBomb 最近频繁的使用一个新指标 xPass，根据预期进球 xG 的名字可以暂且把它的中文叫做预期传球，那具体的解释呢，可以看他们在文章 [Using xPass To Measure The Impact Of Gamestate On Team Style ](https://statsbomb.com/articles/soccer/using-xpass-to-measure-the-impact-of-gamestate-on-team-style/) 提到的：

> The definition that you’ll find on our Assist website is: The estimated likelihood of an attempted pass being completed successfully based on the location of the pitch and context the pass is attempted under, and location of the target location of the pass.
>
> In its simplest form it is a measurement of the difficulty of completing a pass. A pass with a high pass success probability (xPass) is likely to be completed a high percentage of the time - you can think of these as safe, low-risk passes. A pass across the back between two CBs, who aren’t being pressured, would have a high xPass value, for example.
>
> By contrast, a pass with a low xPass value is likely to be completed a low percentage of the time - you can think of these as risky, more direct passes. Consider a full back playing a ball from his own half into the channels, whilst being pressured by an opponent, for example.
>
> Loosely speaking, playing more high xPass passes would equate to being more measured in possession and playing more ‘safe’ passes, whereas playing passes with a lower xPass value would indicate a more direct style of play.

有几个比较重要的句子划一下：

* 根据球场位置、传球的环境以及传球目标的位置，完成传球成功的可能性
* 最简单的用法是衡量完成传球的难度：
    * 较高的 xPass 可能会在很高比例的时间内完成，可以将其视为安全低风险的传球，比如两名中后卫之间的回传球
    * 较低的 xPass 占有的时间比率很低，可以将其视为有风险的更加直接的传球

通过上面的描述可以得到训练一个 xPass 模型主要的特征：

* 传球队员坐标
* 接球队员坐标

这两者可能是最重要的特征了，从中可以得出一些计算特征：

* 传球距离
* 传球队员和接球队员的区域划分?：是否需要把场上位置划分为一些区域来分块，这个特征不是很确定
* 传球队员和接球队员的位置？需不需要一个 passmap 来确定场上位置？也不确定

接下来是传球的环境，可以理解为：

* 传球队员的受干扰程度，根据 xG 的干扰射门特征的计算可以假设成传球事件坐标半径 1 米内有无防守队员
* 接球队员受干扰程度，同上
* 是否有球员干扰传球路线，在传球路线上下各延伸出 0.5 米形成一个长方形区域，区域内是否有球员，区分队友和对手

作为衍生物，甚至可以顺便计算了 packing :)

而 label, 则通过下一次事件来确定是否为一次成功的传球，比如传球事件的下一次事件换成了对手的事件，或者定位球事件，则不是一次成功的传球

接来下将抽时间使用 StatsBomb 的公开数据来训练一个基于上面假设的 xPass 模型，只是 StatsBomb 公开数据并没有他们已经计算好的 xPass 作为参考，但可以通过他们对于 xPass 的运用来做一些验证，这些之后再探讨
