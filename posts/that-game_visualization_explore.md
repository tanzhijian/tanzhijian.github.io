# that-game 的可视化功能探讨

我发现 that-game 通过设计好的数据格式，或许可以很方便的完成各个级别的可视化

文章只为探讨，所有的示例图都为引用的效果图，其具体功能还未实现

## Pitch

```python
pitch = Pitch(length=105, width=68)
pitch.show()
```

![](https://mplsoccer.readthedocs.io/en/latest/_images/sphx_glr_plot_pitches_003.png)

```python
pitch = Pitch(length=105, width=68, vertical=True)
pitch.show()
```

![](https://mplsoccer.readthedocs.io/en/latest/_images/sphx_glr_plot_pitches_009.png)

这样可以很方便的预览设置的 pitch 是否与自己心目中的一样

## Location

每一个单独的 Location 都可以单独的查看在 pitch 中的位置

```python
location = Location(x=60, y=40, pitch=pitch)
location.show()
```

## Event

### Shot

可以预览单次射门的状况

```python
shot = Shot(...)
shot.show()
```

![](https://mplsoccer.readthedocs.io/en/latest/_images/sphx_glr_plot_shot_freeze_frame_001.png)

### Pass

可以预览单次 pass 的传球图，传球方，接球方，球的轨迹，穿过的球员(如果有)

### 其他

其他的一些 type 类我还没有写完，比如 duel, block, dribble, 都会以单点的形式在 pitch 上描绘

## Game

可以从 game 的角度查看更多

### shots

```python
game = Game(...)
shots = game.shots()
shots.shotmap(selected='home')
```

![](https://mplsoccer.readthedocs.io/en/latest/_images/sphx_glr_plot_scatter_008.png)

### passes

```python
passes = game.passes()
passes.network(selected='home')
```

![](https://soccermatics.readthedocs.io/en/latest/_images/Denmark.png)

```python
passes.passmap(selected='home')
```

![](https://mplsoccer.readthedocs.io/en/latest/_images/sphx_glr_plot_lines_001.png)

```python
passes.passmap(id='66')
```

![](https://soccermatics.readthedocs.io/en/latest/_images/TAA.png)

### 其他

```python
touches = game.touches()
touches.heatmap(selected='home')
```

![](https://mplsoccer.readthedocs.io/en/latest/_images/sphx_glr_plot_heatmap_001.png)

### games

可以站在 games 集合的角度查看一些统计数据

```python
games = Games(Game(...), Game(...), Game(...))
shots = games.shots()
shots.shotmap(team='liverpool')
```

![](https://soccermatics.readthedocs.io/en/latest/_images/Liverpool_shot_map.png)

```python
touches = games.touches()
touches.countmap()
```

接下来就是设计好用的 api 和参数，以及具体代码实现。坑越挖越大了。
