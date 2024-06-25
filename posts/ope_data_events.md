# open-data events 文档笔记

原文档 pdf 不方便查阅特做整理, 机器翻译手动整理结构

v4.0

本文档描述了StatsBomb开放事件数据的JSON格式。

## Format

data/events 目录中的比赛文件将采用 JSON 格式。文件名将采用 1234.json 格式，其中 1234 是比赛 ID。内容是一个包含两支球队的事件信息的数组。一些元素有子元素（通常是名称/ID 对）或子数组（这些将在文档后面详细介绍）。

* id: uuid, 每个事件的唯一标识符

* index: int, 每场比赛中事件排序的序列符号。自增的整数

* preiod: int, 时间戳对应的比赛部分
    * 1: 1st Half
    * 2: 2nd Half
    * 3: 3rd Period
    * 4: 4th Period
    * 5: Penalty Shootout

* timestamp: timestamp, 比赛中事件发生的时间，精确到毫秒。

* minute: int, 事件发生时时钟上的分钟数。半场结束时重置为 45 分钟，加时赛开始时重置为 90 分钟。

* second: int, timestamp 的第二部分

* type: object, (id: int, name: str), event 事件类型的 ID/名称。
    * 42, Ball Receipt, 接到传球
    * 2, Ball Recovery, 尝试夺回球权
    * 3, Dispossessed, 球员被防守球员拦截而带球失败，因此丢失球权
    * 4, Duel, 比赛中对立双方两名球员之间 50 对 50 的较量
    * 5, Camera On, 发出信号停止摄像机捕捉比赛过程以进行重播/视频剪辑
    * 6, Block, 站在球的路径上阻挡球
    * 8, Offside, 越位。由射门或解围（非传球）导致的事件。对于造成越位的传球，请查看传球部分
    * 9, Clearance, 防守球员为消除危险而采取的行动，并非有意将球传给队友
    * 10, Interception, 通过移动到传球路线/做出反应进行拦截，阻止对手的传球到达队友手中
    * 14, Dribble, 球员试图带球突破对手
    * 16, Shot, 用身体任何（合法）部位试图进球
    * 17, Pressure, 对接球、带球或传球的对方球员施加压迫
    * 18, Half Start, 裁判吹哨开始一个部分的比赛
    * 19, Substitution
    * 20, Own Goal Against, 对方球员的乌龙球
    * 21, Foul Won, 犯规获胜的定义是，一名球员在遭到对方球员犯规后，为本队赢得任意球或点球
    * 22, Foul Committed, 任何被裁判判为犯规的违规行为, 越位不被视为犯规
    * 23, Goal Keeper, 守门员可以执行的动作
    * 24, Bad Behaviour, 当球员由于比赛之外的违规行为而收到黄牌时
    * 25, Own Goal For, 该队进了一粒乌龙球
    * 26, Player On, 球员离开事件发生后，球员返回球场
    * 27, Player Off, 一名球员未经替换就离开/被抬出球场
    * 28, Shield, 球员保护出界的球以防止对手继续比赛
    * 30, Pass, 球在队友之间传递
    * 33, 50/50, 两名球员争夺无球权的球
    * 34, Half End, 向裁判发出哨声，表示某一场比赛部分结束
    * 35, Starting XI, 标明首发 11 名球员、他们的位置以及球队阵型
    * 36, Tactical Shift, 表示球队的战术变化，显示球员的新位置和球队的新阵型
    * 37, Error, 当一名球员被判定犯下控球失误，从而导致射门时
    * 38, Miscontrol, 球员因触球失误丢球
    * 39, Dribbled Past, 球员被对手带球突破
    * 40, Injury Stoppage, 因受伤而停止比赛
    * 41, Referee Ball-Drop, 因伤病暂停后，裁判放下球，继续比赛
    * 43, Carry, 球员在移动或站立时控制脚下的球

* possession: int, 表示比赛中当前唯一的一次控球。一次控球表示在比赛期间，球处于比赛状态，并且由一支球队控制球

* possession_team: object, (id: int), 开始控球的球队的 ID。请注意，即使在控球期间试图铲球等对手事件中，此 ID 也会显示

* play_pattern: object, (id: int, name: str), 与此事件相关的比赛模式的 ID/名称
    * 1, Regular Play, 该事件不属于以下任何 play_patterns
    * 2, From Corner, 该事件是角球之后比赛进程的一部分
    * 3, From Free Kick, 该事件是任意球之后比赛过程的一部分
    * 4, From Throw In, 此事件是界外球之后比赛过程的一部分
    * 5, Other
    * 6, From Counter 该事件是反击的一部分:
        * 控球开始于反击球队最后三分之一区域外的一次常规比赛失误
        * 控球至少有 75% 直接朝向球门（以我们的控球链指标衡量）
        * 反击向球门前进了至少 18 码。
        * 此定义不是收集的一部分，而是从上述逻辑中得出的
    * 7, From Goal Kick, 该事件是球门球后比赛过程的一部分
    * 8, From Keeper, 这一事件是守门员开球后比赛进程的一部分
    * 9, From Kick Off, 该事件是开球后比赛进程的一部分

* team: object, (id: int, name: str), 此事件所关联的球队的 ID/名称。仅当事件与特定球队相关时，才会显示对象

* player: object, (id: int, name: str), 与该事件相关的球员的 ID/名称（仅当事件与特定球员相关时才会显示对象）

* position: object, (id: int, name: str), 事件发生时球员所处位置的 ID / 名称
    * 1, GK, Goalkeeper
    * 2, RB, Right Back
    * 3, RCB, Right Center Back
    * 4, CB, Center Back
    * 5, LCB, Left Center Back
    * 6, LB. Left Back
    * 7, RWB, Right Wing Back
    * 8, LWB, Left Wing Back
    * 9, RDM, Right Defensive Midfield
    * 10, CDM, Center Defensive Midfield
    * 11, LDM, Left Defensive Midfield
    * 12, RM, Right Midfield
    * 13, RCM, Right Center Midfield
    * 14, CM, Center Midfield
    * 15, LCM, Left Center Midfield
    * 16, LM, Left Midfield
    * 17, RW, Right Wing
    * 18, RAM, Right Attacking Midfield
    * 19, CAM, Center Attacking Midfield
    * 20, LAM, Left Attacking Midfield
    * 21, LW, Left Wing
    * 22, RCF, Right Center Forward
    * 23, ST, Striker
    * 24, LCF, Left Center Forward
    * 25, SS, Sencondary Striker

* location: array, (x: int, y: int), 包含两个整数值的数组。这些是事件的 x 和 y 坐标（仅当事件具有高度坐标时才显示）

* duration: float, 如果相关，则事件持续的时间（以秒为单位）

* under_pressure: bool, 该动作是在对手施加压力的情况下做出的

* off_camera: bool: 事件发生时，摄像机处于关闭状态

* out, bool, 如果事件的结果是球出界，则添加

* related_events: `array[uuid]`, 相关事件 ID 的逗号分隔列表。例如，射门可能与守门员事件和拦截事件相关。相应事件的 related_events 列中将包含射门的 ID

* tactics: object
    * formation: int, 对于“首发 XI 或战术换班”类型的事件，添加了“战术”对象。阵型项目描述了正在使用的阵型, 433
    * lineup: `array[player: object[id: int, name: str], position: object[id: int, name: str], jersey_number: int]`, 对于“首发 XI 或战术换人”类型的事件，添加了“战术”对象。阵容项描述了球员及其位置

## Event Type Objects

如果事件属于具有附加详细信息的类型，则这些详细信息将嵌套在以该事件类型命名的对象中。例如，Shot 类型的事件将具有嵌套数据框，其中包含描述该事件类型的附加变量。以下是按字母顺序排列的嵌套数据框列表及其包含的变量。

* 50-50
    * outcome: object, (id: int, name: str), 50 50争夺结果的ID/名称, values:
        * 108, Won
        * 109, Lost
        * 147, Success To Team, 球员赢得 50/50 并将球控制到己方
        * 148, Success To Opposition, 球员赢得 50/50，但将球踢到对方
    * counterpress: bool, 在 open play 转换后 5 秒内采取压迫

* Bad Behaviour: object, (id: int, name: str), 红黄牌的 ID/名称
    * 65, Yellow Card
    * 66, Second Yellow
    * 67, Red Card

* Ball Receipt: object, (id: int, name: str), 指定球接收结果的属性选项的 ID/名称
    * 9, Incomplete

* Ball Recovery
    offensive: bool, 如果恢复进攻则添加
    recovery_failure: bool: 如果恢复失败则添加

* Block
    * deflection: bool, 如果是偏转则添加
    * offensive: bool, 如果该阻挡具有攻击性则添加
    * save_block: bool, 如果阻挡了射门则添加
    * counterpress: bool, 在常规比赛转换后 5 秒内采取紧逼行动

* Carry
    * end_location: array, (x: int, y: int)

* Clearance
    * aerial_won: bool, 如果高空解围则添加
    * body_part: object, (id: int, name: str), 触球身体部位的 ID/名称
        * 37, Head
        * 38, Left Foot
        * 40, Right Foot
        * 70, Other

* Dribble
    * Overrun: bool, 当球越过原来的防守队员进入另一名球员的球权时添加
    * Nutmeg: bool, 当球从对方球员腿间穿过时添加
    * outcome: object, (id: int, name: str)
        * 8, Complete
        * 9, Incomplete
    * No Touch: bool, 如果球员试图通过将球漏过对手而不是接触球来进行带球

* Dribbled Past
    * counterpress: bool, 在常规比赛转换后 5 秒内采取紧逼行动

* Duel
    * counterpress: bool
    * type: object, (id: int, name: str), Id/Name 为对抗的类型
        * 10, Aerial Lost, 争夺空中对抗但没能抢到球
        * 11, Tackle, 抢断对方球员的控球权
    * outcome: object, (id: int, name: str), 对抗结果的 Id/名称
        * 1， Lost
        * 4, Won, 抢断最终落入抢断队员手中
        * 13, Lost In Play, 将球踢向对手的抢断
        * 14, Lost Out, 铲球将球击出界外，有利于对手
        * 15, Success
        * 16, Success In Play, 将球传给队友的抢断
        * 17， Success Out, 抢断将球击出界外，有利于抢断者的球队

* Foul Committed
    * counterpress: bool
    * offensive: bool
    * type: object, (id: int, name: str), Id/Name 为犯规的类型
        * 19, 6 Seconds, 因 6 秒违例被判犯规
        * 20, Backpass Pick, 因回传用手接球违例被判犯规
        * 21, Dangerous Play, 危险动作导致犯规
        * 22, Dive, 因假摔而犯规
        * 23, Foul Out, 因犯规被罚出场
        * 24, Handball, 手球犯规
    * advantage: bool, 如果裁判判定为进攻有利比赛继续则添加
    * penalty: bool, 如果被判点球添加
    * card: object, (id: int, name: str), 卡牌的类型
        * 5, Yellow Card
        * 6, Second Yellow
        * 7, Red Card

* Foul Won
    * defensive: bool, 如果在失去控球权的情况下犯规，则添加
    * advantage: bool, 如果裁判判定为进攻有利比赛继续则添加
    * penalty: bool, 如果判罚点球则添加

* GoalKeeper
    * position: object, (id: int, name: str), 守门员射门前站位选项的 ID/名称
        * 42, Moving, 射门时守门员正在移动
        * 43, Prone, 射门时守门员倒在地上
        * 44, Set, 射门时守门员处于静止状态
    * technique: object, (id: int, name: str), 守门员使用的技术技术选项的 ID/名称
        * 45, Diving, 守门员飞身进行扑救
        * 46, Standing, 守门员站立进行扑救
    * body_part: object, (id: int, name: str), 守门员扑救时使用的身体部位
        * 35, Both Hands
        * 36, Chest
        * 37, Head
        * 38, Left Foot
        * 39, Left Hand
        * 40, Right Foot
        * 41, Right Hand
    * type: object, (id: int, name: str), 指定守门员事件类型的 ID/名称。每次射门都会有一个相关的守门员事件。如果没有失球或没有扑救，守门员类型将为“Shot Faced”）
        * 25, Collected
        * 26, Goal Conceded, 失球
        * 27, Keeper Sweeper, 当守门员离开自己的防线和/或禁区扑球时
        * 28, Penalty Conceded, 守门员在点球中失球
        * 29, Penalty Saved
        * 30, Punch, 守门员拳击球（类似清球）
        * 31, Save, 守门员扑救非射门
        * 32, Shot Faced, 射门未导致扑救或失球
        * 33, Shot Saved, 守门员扑出对方射门
        * 34, Smother, 相当于禁区外球员的抢断，守门员出来抢断球员
        * 113, Shot Saved Off T, 守门员扑出了对方偏离目标的射门
        * 114, Shot Saved To Post, 射门被守门员扑出，击中门柱
        * 110, Saved To Post, 守门员扑救非射门击中门柱
        * 109, Penalty Saved To Post
    * outcome: object, (id: int, name: str)
        * 47, Claim, 守门员清道夫动作，但是接住了球
        * 48, Clear, 守门员清道夫动作，但是清除了球
        * 49, Collected Twice, 守门员在第一次接球失误后，又多次尝试接球
        * 50, Fail, 动作失败
        * 51, In Play, 守门员扑救，将球挡回场内
        * 52, In Play Danger, 守门员扑救，将球挡给对方球员
        * 53, In Play Safe, 守门员扑救，将球挡给队友
        * 55, No Touch, 守门员未触球就丢球
        * 56, Saved Twice, 守门员在第一次扑救失败后，又多次尝试扑救
        * 15, Success
        * 58, Touched In, 尽管守门员触球，但还是丢球
        * 59, Touched Out, 守门员触球出界
        * 4, Won, 获得球权
        * 16, Success In Play, 将球传给队友的扑救
        * 17, Success Out, 将球扑出界外，有利于拦截方的球队
        * 13， Lost In Play, 将球击向对手的扑救
        * 14, Lost Out, 将球击出界外，有利于对手
        * 117, Punched Out, 守门员将球扑出界外

* Half End
    * Early Video End: bool, 如果比赛视频不完整且比赛在本节结束前结束，则添加
    * Match Suspended: bool, 裁判决定结束或推迟比赛

* Half Start
    * Late Video Start: bool, 如果比赛视频未完成并在开球后开始，则添加

* Injury Stoppage
    * in_chain: bool, 如果比赛暂停前球在受伤球员的球队手中，则添加

* Interception
    * outcome, object, (id: int, name: str)
        * 1, Lost
        * 13, Lost In Play, 将球击给对手的拦截
        * 14, Lost Out, 拦截将球击出界外，有利于对方
        * 15, Success
        * 16, Success In Play, 将球传给队友的拦截
        * 17, Success Out, 拦截将球击出界外，有利于拦截方的球队
        * 4, Won, 拦截后球落入拦截者手中

* Miscontrol
    * aerial_won: bool, 如果事件发生在空中，则添加

* Pass
    * recipient: object, (id: int, name: str), Id / Name 传球接收者的球员，或未完成传球的接收者的球员
    * length: float, 以码为单位的传球长度, 16.03
    * angle: float, 以弧度表示的通过角度，其中 0 指向正前方，0 到 π 之间的正值表示顺时针方向的角度，0 到 -π 之间的负值表示逆时针方向的角度, -2.49
    * height: object, (id: int, name: str), 传球高度的 ID / 名称
        * 1, Ground Pass, 球没有离开地面
        * 2, Low Pass, 球离开地面但在最高高度时低于肩膀的高度
        * 3, High Pass, 球在最高高度超过肩膀的高度
    * end_location: array, (x: int, y: int)
    * assisted_shot_id: uuid, 如果这次传球是助攻，那么关联射门的事件 id
    * backheel: bool, 如果用脚后跟传球则添加
    * deflected: bool, 如果传球偏转则添加
    * miscommunication: bool, 如果传球存在沟通不畅则添加
    * cross: bool, 如果传球是传中则添加
    * cut-back: bool, 如果传球是回传则添加
    * switch: bool, 如果传球是转移（球垂直转移了至少 50% 的球场），则添加
    * shot-assist: bool, 如果传球是对射门的助攻（但未进球），则添加
    * goal-assist: bool, 如果传球助攻进球，则添加
    * body-part: object, (id: int, name: str)
        * 68, Drop Kick, 传球来自守门员的 drop kick
        * 37, Head, 传球来自头球
        * 69, Keeper Arm, 传球来自守门员的手手抛球
        * 38, Left Foot
        * 70, Other
        * 40, Right Foot
        * 106, No Touch, 一名球员故意让球从自己身边经过，而不是接球，而是传给身后的队友。也称为“假动作”）。
    * type: object, (id: int, name: str)
        * 61, Corner
        * 62, Free Kick
        * 63, Goal Kick
        * 64, Interception
        * 65, Kick Off, 比赛开始时或得分后开球时的传球
        * 66, Recovery, 一触式传球抢断
        * 67, Throw-in
    * outcome: object, (id: int, name: str)
        * 9, Incomplete, 球未到达队友，比赛仍在进行中
        * 74, Injury Clearance, 因受伤而停止比赛，球出界
        * 75, Out, 球出界
        * 76, Pass Offside, 球传到队友手中但传球被判越位
        * 77, Unknown, 结果未知（即在飞行过程中被判犯规）
    * Technique: object, (id: int, name: str), 传球技术的 ID / 名称
        * 104, Inswinging, 适用于内旋高/低角球
        * 105, Outswinging, 适用于外旋高/低角球
        * 107, Straight, 不适用于内旋角球或外旋角球
        * 108, Through Ball, 传球突破最后一道防线

* Player Off
    * Permanent: bool, 如果球员永久离开比赛，则添加。适用于没有替补球员但球员因伤无法重返球场的情况

* Pressure
    * counterpress: bool, 在常规比赛转换后 5 秒内采取紧逼行动

* Shot
    * key_pass_id: uuid
    * end_location: array, (x: int, y: int)
    * aerial_won: bool, 如果射门是空中胜利，则添加
    * follows_dribble: bool, 如果射门是在盘带后进行的，则添加
    * first_time: bool, 如果射门是第一次触球，则添加
    * freeze_frame: array, 每次射门都包含一个名为 freeze_frame 的对象，该对象是一个数组，其中包含射门时相关球员的信息，每个 freezeframe 对象都是一个数据框，每个球员占一行，包括他们的位置、球队、ID、姓名以及位置 ID 和姓名
    * open_goal: bool, 如果射门是在空门的情况下进行的，则添加
    * statsbomb_xg: float
    * deflected: bool, 如果射门偏出则添加
    * technique: object, (id: int, name: str), 射门技术的 ID / 名称
        * 89, Backheel
        * 90, Diving Header
        * 91, Half Volley, 半临空
        * 92, Lob, 为了越过对方球员而射出的球具有较高的弧线
        * 93, Normal, 不属于任何其他技术的射门
        * 94, Overhead Kick
        * 95, Volley
    * body_part: object, (id: int, name: str)
        * 37, Head
        * 38, Laft Foot
        * 70, Other
        * 40, Right Foot
    * type: object, (id: int, name: str)
        * 61, Corner
        * 62, Free Kick
        * 87, Open Play
        * 88, Penalty
        * 65, Kick Off, 开球后直接射门
    * outcome: object, (id: int, name: str)
        * 96, Blocked
        * 97, Goal
        * 98, Off T
        * 99, Post
        * 100, Saved
        * 101, Wayward, 射门毫无威胁，偏离球门太远或力量不足以到达球门线（或球员没有碰到球的失误）
        * 115, Saved Off T
        * 116, Saved To Post

* Substitution
    * replacement: object, (id: int, name: str), 对于替换，上场球员的 ID/姓名。球员详情（主要事件）描述下场球员。
    * outcome: object, (id: int, name: str), 替换类型选项的 Id/Name
        * 102, Injury
        * 103, Tactical
