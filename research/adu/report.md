# 阿杜模板逐项审阅（2026-10-28）

本报告服务于总导演 Skill 的选型与设计语法升级。它是有证据边界的研究，不是“全部模板已下载、已运行、已看完”的声明。

## 覆盖与获取范围

- [作者主页](https://motiongit.com/@adunext)两页共 **28 个模板页面**：13 个标为免费（匿名访问仍需登录领取个人包），15 个达标后开放。
- [官方目录](https://github.com/motiontemplates/all)为其中 16 个提供技术仓库；12 个知识讲解模板的 repository/commit 为 null。技术仓库除 385712 外主要是介绍、参数与网页，不含当前制作实现。
- 28 个官网 Overview 和 Files 清单均读取。Files 清单公开文件名、大小与哈希，未提供源码正文入口；不把“可看到文件名”写成“已读源码”。
- 28 个 Demo 均做 ffprobe；各取 3 个离散时间点，已观察所有模板的样本画面。它不等于连续观看；本次未试听，不评判完整音画节奏。
- 历史仓库固定为 `4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf`，审读 11 个当前选中风格的合同、关键样式、运动与声音实现；没有逐一审查全部历史候选版本。另只读审阅本机已存 Kinetic 0.2.7 公开包，不执行安装/渲染脚本。
- 本次没有登录、索取密钥、获取个人包、执行未知代码、发布或宣称运行通过。官网各页 Runtime verification 均标为 Not verified。

## 28 个现行页面逐项清单

版本为本次读取值，可能继续更新。每个横/竖版独立登记；时长列保留页面声明，实际 Demo 流时长见 inventory.json。全表声明 60fps。F=免费但登录领取个人包；G=达标后免费。

| # | 模板 / 来源 | 版本 | 画幅与像素 | 页面时长 | 获取 | 直接用途 |
|---|---|---|---|---|---|---|
| 1 | [酷炫科技风](https://motiongit.com/@adunext/385712) | 0.2.44-alpha.3 | 9:16 / 1080×1920 | 01:05 | F | 科技观点、重点概念、双项比较和行动收尾 |
| 2 | [活力海报 · 口播讲解 · 竖屏](https://motiongit.com/@adunext/vibrant-poster-portrait) | 2.7.18-alpha.3 | 9:16 / 1080×1920 | 03:14 | F | 观点、两来源分屏、步骤、问答和总结 |
| 3 | [活力海报 · 口播讲解](https://motiongit.com/@adunext/vibrant-poster) | 2.7.18-alpha.2 | 16:9 / 1920×1080 | 03:14 | F | 观点、两来源分屏、步骤、问答和总结 |
| 4 | [鲜色角色 · 叙事讲解 · 竖屏](https://motiongit.com/@adunext/template-05-native-portrait) | 2.7.18-alpha.3 | 9:16 / 1080×1920 | 02:02 | F | 人物/物件接力、成果复用、反馈升级 |
| 5 | [鲜色角色 · 叙事讲解](https://motiongit.com/@adunext/template-05-native) | 2.7.18-alpha.2 | 16:9 / 1920×1080 | 02:02 | F | 人物/物件接力、成果复用、反馈升级 |
| 6 | [科技控制台 · 口播讲解 · 竖屏](https://motiongit.com/@adunext/template-04-dark-console-portrait) | 2.7.18-alpha.3 | 9:16 / 1080×1920 | 02:10 | F | 技术流程、输入融合、步骤执行与交付 |
| 7 | [科技控制台 · 口播讲解](https://motiongit.com/@adunext/template-04-dark-console) | 2.7.20-alpha.2 | 16:9 / 1920×1080 | 02:10 | F | 技术流程、输入融合、步骤执行与交付 |
| 8 | [深色立体 · 多屏展陈 · 竖屏](https://motiongit.com/@adunext/template-03-native-portrait) | 2.7.18-alpha.3 | 9:16 / 1080×1920 | 02:03 | F | 真实作品比较、软件评测、成果与作品集 |
| 9 | [深色立体 · 多屏展陈](https://motiongit.com/@adunext/template-03-native) | 2.7.18-alpha.2 | 16:9 / 1920×1080 | 02:03 | F | 真实作品比较、软件评测、成果与作品集 |
| 10 | [纸面透视 · 口播讲解 · 竖屏](https://motiongit.com/@adunext/template-02-expanded-portrait) | 2.7.18-alpha.4 | 9:16 / 1080×1920 | 04:21 | F | 条件、两难、因果链、资料整理与行动 |
| 11 | [纸面透视 · 口播讲解](https://motiongit.com/@adunext/template-02-expanded) | 2.7.21-alpha.3 | 16:9 / 1920×1080 | 04:21 | F | 条件、两难、因果链、资料整理与行动 |
| 12 | [现代图文 · 口播讲解 · 竖屏](https://motiongit.com/@adunext/template-01-integrated-portrait) | 2.7.18-alpha.3 | 9:16 / 1080×1920 | 01:58 | F | 论点、真实证据、方法拆解、归纳与片尾 |
| 13 | [现代图文 · 口播讲解](https://motiongit.com/@adunext/template-01-integrated) | 2.7.18-alpha.2 | 16:9 / 1920×1080 | 01:58 | F | 论点、真实证据、方法拆解、归纳与片尾 |
| 14 | [彩色几何 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-byrne) | 2.7.2 | 16:9 / 1920×1080 | 00:23.866667 | G | 直角三角形、边与面积、全等拼接和不变量 |
| 15 | [点阵手账 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-sketchnote) | 2.7.2 | 16:9 / 1920×1080 | 00:19.95 | G | 方法步骤、学习过程、修订和回顾 |
| 16 | [双色孔版 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-riso) | 2.7.2 | 16:9 / 1920×1080 | 03:14.766667000000012 | G | 增长、倍率、基数、最终增量比例和套印 |
| 17 | [地铁线路图 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-metro) | 2.7.2 | 16:9 / 1920×1080 | 03:13.400000000000006 | G | 状态流、占用/释放、权限边界、制动和队列 |
| 18 | [纸雕层叠 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-papercut) | 2.7.2 | 16:9 / 1920×1080 | 03:18.80000000000001 | G | 层序、剖面、褶皱、位移和侵蚀搬运 |
| 19 | [等距系统图 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-isometric) | 2.7.2 | 16:9 / 1920×1080 | 03:15.679563000000002 | G | 设备内部、物质/热/功路径与边界 |
| 20 | [发光玻璃板 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-lightboard) | 2.7.2 | 16:9 / 1920×1080 | 03:30.30000000000001 | G | 信号叠加、相位、幅值、时延和反馈 |
| 21 | [博物馆展墙 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-timeline) | 2.7.2 | 16:9 / 1920×1080 | 03:42.216667 | G | 计量机制、不同条件下的计时或工具演进 |
| 22 | [生长导图 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-mindmap) | 2.7.2 | 16:9 / 1920×1080 | 03:34.066666999999995 | G | 层级、路径分流、对象去向和尺度转换 |
| 23 | [粉笔黑板 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-chalkboard) | 2.7.2 | 16:9 / 1920×1080 | 03:29.983332999999988 | G | 观察与成因、光照/视线/遮挡/轨道/投影 |
| 24 | [黏土实验台 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-clay) | 2.7.2 | 16:9 / 1920×1080 | 03:27 | G | 对象拆合、附着、受力与路径追踪 |
| 25 | [瑞士信息设计 · 知识讲解模板](https://motiongit.com/@adunext/knowledge-explainer-swiss) | 2.7.2 | 16:9 / 1920×1080 | 03:12.316666999999995 | G | 比例、分母、加权均值和分组比较 |
| 26 | [卡通讲解风](https://motiongit.com/@adunext/cartoon-explainer) | 0.1.0-alpha8 | 16:9 / 1920×1080 | 04:35.266666999999984 | G | 教程步骤、框架、工作区、角色反馈 |
| 27 | [字符剧场](https://motiongit.com/@adunext/character-theater) | 0.1.0-alpha8 | 16:9 / 1920×1080 | 02:35.98333299999999 | G | 字形角色、第一人称说明、作品故事 |
| 28 | [突破边界](https://motiongit.com/@adunext/break-boundaries) | 0.1.1-alpha.2 | 3:4 / 1440×1920 | 02:40.400000000000006 | G | 约束与突破、判断/行动、窗口变化、总结交付 |

## 每套视觉体系的观察与迁移规则

下表合并同体系的横/竖版解释，但 inventory.json 保留每个版本、独立 Demo、素材与证据。配色词来自实际抽帧和作者说明；当前 token 代码不可读的条目不臆造十六进制值。运动说明来自作者文档/已读历史实现；抽帧本身不能证明转场连续。

| 体系 | 配色与构图 | 组件、运动与转场 | 迁移边界 |
|---|---|---|---|
| [金属科技](https://motiongit.com/@adunext/385712) | 黑底、银色立体字，蓝光与少量金色；大面积暗部；主体文字与发光线居中；矩形/圆形人物窗单独占位 | 机械翻牌、光线书写、火花强调、空间卡；公开版 B1–B4 为关键词/要点/比较/行动 | 官网 0.2.44 与公开 0.2.7 独立更新；公开包仅 16:9；英文竖版仅 B1–B4，S 系列仍横版 |
| [活力海报](https://motiongit.com/@adunext/vibrant-poster) | 黑与纸白切换；荧光黄绿作主重音，辅蓝/红；大标题、双色分屏、警示带、荧光答案卡；竖版上下重排 | 大字冲击、回声、划除与显露；作者声明 25 原生组，70 库控件，7 类已融入表达 | 原生口播与 poster-kit 分开入口；70 控件不等于全部完成美术验收；不能把估算文字节奏当真实配音时码 |
| [鲜色角色](https://motiongit.com/@adunext/template-05-native) | 纸白与鲜亮蓝紫橙绿卡片；暗场用于聚焦；分组标签、彩色资产格与人物圆窗分层；竖版格子在标签下方 | 关键词递进、聚能、交接、三反馈汇聚；原生组与新控件分开 | 六关键词、二到三接力、三反馈等固定关系必须确实存在；示例数量不是事实 |
| [科技控制台](https://motiongit.com/@adunext/template-04-dark-console) | 黑/深灰，青蓝发光线，紫色玻璃与成功绿；主仪器台+人物窗，状态和输出分区；竖版纵向堆叠 | 路径汇聚、完成爆发、检查列表、玻璃图表；原生动作与新增组件分开 | 不能因无人物模式存在就删去原生组的必需人物；紫色柱图是当前具体更新，不代表全组件已验证 |
| [深色立体展陈](https://motiongit.com/@adunext/template-03-native) | 黑/深灰+蓝重点，穿插白场作节奏转折；九宫格、重点放大、软件窗口、人物大卡/圆窗 | 多屏错峰、分组高亮、同一中心作品接力放大、镜头推进 | 材料稀少时不要强套九屏/作品墙；新稿数值和结论必须有真实来源 |
| [纸面透视](https://motiongit.com/@adunext/template-02-expanded) | 米白纸面与墨绿暗场，薄荷绿重点，暖红次重点；纸卡/天平/批注/资料窗口；竖版从横向序列改成上下关系 | 倾斜回稳、纸卡聚合、手写展开、小球引导、开箱和交付 | 象征插图不充当实测证据；固定数量关系不靠虚构材料填满 |
| [现代图文](https://motiongit.com/@adunext/template-01-integrated) | 米白、近黑、钴蓝；克制低对比网格；大标题、方法卡、媒体窗、目录/分屏；竖版保持层级并重排 | 原节奏、连续形变、纵深、杂志分屏、节拍字效的完整组 | 按意义选择完整组；不能只按每句字幕随机换动画；文本容量和媒体槽位以当前包为准 |
| [彩色几何](https://motiongit.com/@adunext/knowledge-explainer-byrne) | 泛黄纸面、红蓝黄主色、黑几何区；图形左、说明右；颜色固定映射到边/面积 | 测量、刚体复制、拼接重排、面积等价 | 页面仅 23.8667 秒早期样片；严格原生几何限直角三角形模型，不能把任意换题称为已证明 |
| [点阵手账](https://motiongit.com/@adunext/knowledge-explainer-sketchnote) | 奶油纸、深墨字、薄荷绿与黄色标记；点阵页、手写标题、贴纸、箭头、荧光标签 | 沿步骤留痕、镜头接力、旁注修订、回顾路径 | 页面仅 19.95 秒早期样片；超容量应拆页，不用小字塞满 |
| [双色孔版](https://motiongit.com/@adunext/knowledge-explainer-riso) | 纸白、深蓝与粉红，网点与错版感；数值、点阵、曲线与公式共享尺度 | 保留/复制谱系、逐轮增长、线性/指数比较、信息套印 | 每轮翻倍不是默认事实；倍率、轮次、曲线、公式必须来自同一数据模型 |
| [地铁线路](https://motiongit.com/@adunext/knowledge-explainer-metro) | 米白底、低饱和线色、黑色翻牌状态板；路线图为主、右侧读数为辅；空间位置承担状态含义 | 沿线运动、车尾释放区段、制动包络、翻牌读数 | 直线路权模型与弧线移动不同；透视隧道/部分总览仅限源演出，不能任意换稿继承 |
| [纸雕层叠](https://motiongit.com/@adunext/knowledge-explainer-papercut) | 深青背景，砂土/橄榄/奶油多层纸色；单一连续剖面占主体；层的颜色与身份保持 | 切开、守恒折叠、沿切口错位、碎屑与通道搬运 | 有限二维教学剖面与定性类比；源地图和历史摆位不可直接改标签当新知识 |
| [等距系统](https://motiongit.com/@adunext/knowledge-explainer-isometric) | 浅冷灰背景、青蓝结构、暖橙热量；等距全景与局部剖面来回切换 | 铰链剖开、壁面换热、相变、封闭压缩、能量账 | 教学热学不是工程仿真；区分物质、热量和电功箭头，不把封闭压缩说成泵送 |
| [发光玻璃板](https://motiongit.com/@adunext/knowledge-explainer-lightboard) | 近黑背景，青/粉/黄发光细线；同点波形与探针、耳部/反馈回路对应 | 同点叠加、相位变化、探针移动、残差信号反馈 | 有限模型不是实际声场测试；纵轴放大不等于信号增大 |
| [博物馆展墙](https://motiongit.com/@adunext/knowledge-explainer-timeline) | 墨绿展墙、奶油展签、金棕线条；展品序列总览→放大单件→回到展墙 | 日影、流量累积、齿轮/擒纵、摆长、共振反馈 | 每件机制有适用条件；不是按年代排列名词，也不是任意机械/量子系统仿真 |
| [生长导图](https://motiongit.com/@adunext/knowledge-explainer-mindmap) | 暖白底，浅蓝与叶绿，有方向的带状连接；主线/局部放大/回总图；节点保留整体位置 | 树枝生长、沿线跟踪、同批对象聚散、合并后分流 | 新原生拓扑为有根树；源水循环网络不可当任意新循环网复用 |
| [粉笔黑板](https://motiongit.com/@adunext/knowledge-explainer-chalkboard) | 深绿黑板、粉白线、淡黄光路与浅蓝主体；全局几何与局部视图并列；轨道/光线有明确含义 | 同一球体沿轨道、遮挡、局部放大、同态不同投影 | 示意尺度不等于真实比例；月相/食现象不能任意改名成另一系统 |
| [黏土实验台](https://motiongit.com/@adunext/knowledge-explainer-clay) | 桃色桌面、浅蓝/黄/绿柔软物体；实验器皿和对象是主体，局部放大后回到来源 | 保面积拆合、头尾附着、受力分裂、后代轨迹 | 是有界教学类比，不是真实化学/流体模拟；对象来源身份必须可追踪 |
| [瑞士信息设计](https://motiongit.com/@adunext/knowledge-explainer-swiss) | 暖白/灰网格、黑文字、红色重点；对齐的数字/点阵/分母/百分比共享阅读路径 | 点数计数、重排、分组迁移、合并比例联动 | 统计口径、分母与算法要明示；不能把各组百分比直接平均当总体比例 |
| [手绘卡通](https://motiongit.com/@adunext/cartoon-explainer) | 暖纸底、黑描边、黄标题条，辅蓝/绿；浏览器式真人窗与手绘机器人/道具并置 | 手绘线展开、步骤演示、原生转场 | alpha 新稿适配仍完善；某些数字演出保留源结构；人物/音乐不自动可复用 |
| [角色剧场](https://motiongit.com/@adunext/character-theater) | 白与黑舞台交替；少量蓝/红反馈标记；字形小人、规则长卷、作品墙和聚光舞台 | 消息出场、作品翻阅、风暴、马赛克、字形聚合揭幕 | alpha 新稿适配受限；保留源角色结构不能解释为任意角色自动化 |
| [破框](https://motiongit.com/@adunext/break-boundaries) | 黑白纸框，少量蓝色计数与像素提示；3:4 纸框内的真人窗、计数与台阶；框体承担叙事 | 压缩、重开、撕裂破框、攀阶和彩蛋 | 1440×1920 是 3:4，不能当 9:16；原生换稿仍 alpha，源作品/肖像/配乐不得默认使用 |

## 字体、素材和声音的可确认范围

- 现代图文、纸面、立体、控制台、角色、海报的当前 Files 清单均有 Geist、Geist Mono、Noto Sans SC 的许可文件；未得到当前包字体 CSS，不能把许可文件存在等同于所有画面均使用这些字体。

- 12 套知识模板的清单含通用 Inter/Noto Sans SC；原生表达另分化：几何/展墙有 Fraunces、Noto Serif SC、ZCOOL XiaoWei；手账有 Long Cang、LXGW WenKai、JetBrains Mono；孔版有 ZCOOL QingKe HuangYou；地铁/等距有 JetBrains Mono；纸雕有 Fraunces、WenKai、XiaoWei；光板有 WenKai/Noto Serif SC；导图有 WenKai/Noto Serif SC；黑板有 Long Cang/WenKai；黏土有 WenKai；瑞士主要 Inter/Noto Sans SC。完整文件名和 SHA-256 见逐项 inventory。这里只确认清单，不确认实际 fallback/字形布局。

- 卡通清单有 Geist、Geist Mono、Instrument Serif；剧场有 Geist/Geist Mono；破框另有 Fusion Pixel 12px 中文。破框还列出 CC0 音效署名文件和录音目录，需取得包后读逐项许可，不能仅由文件名断言每条录音都可任意再分发。

- 口播路线通常需要本期人物原片/原声、匹配文稿或 SRT、所选场景所需的真实录屏/图片/数据。只给文稿可规划，正式同步需真实音频时长。没有人物时应走模板明确的人物缺省或纯图文入口，不沿用示例人物。知识路线按内容准备命题、模型、单位、数据与来源，可选真人全屏进入后缩圆窗。

- 28 个视频均探测音轨，但本次没有听音。原声、BGM、动作 SFX 应分开核验。Kinetic 官网说明当前 36 秒英文竖屏 Demo 含原生 SFX 和 CC0 配乐、无旁白；这不能推断其他 Demo 的音乐许可。

- 13 个免费页面明确声明模板代码 MIT，字体、品牌、人物、示例图像与音频分开许可。另15个达标解锁页面本次未见 MIT/SPDX 正文；只列出 TEMPLATE-LICENSE.txt，**当前完整许可未核实**，不能借用相邻模板的 MIT 声明。旧仓库本身为 MIT，THIRD_PARTY 明确示范 MP4 仅供观看，未赠与原始人物、声轨、截图、音乐素材使用权。当前个人包可能带本人 API 标识，分享模板链接，不把个人包归档为公开源码。

## 历史公开源码：11 个风格逐项对照

以下均来自 [adu-motion-video 固定提交](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf)；这是历史 Skill 路线，不能冒充当前官网包。每个 selection 的 manifest、样式与关键运动文件均已提取可追溯清单。组数是源合同容量，不是本次渲染验收结果。

| 编号 | 已读版本 / 公开目录 | 组数 | 可迁移设计语法 |
|---|---|---|---|
| 01-A 原片节奏 | [classic-performance@1.0.0](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/classic-performance/1.0.0) | 3 | 主张→容器→三对象分发→证据→回应；真实证据放大后再给结论。 |
| 01-B 连续形变 | [continuous-performance@1.0.0](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/continuous-performance/1.0.0) | 2 | 同一容器/对象连续变换角色；拆成三层再汇入规则，保持实体身份。 |
| 01-C 纵深舞台 | [stage-performance@1.0.0](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/stage-performance/1.0.0) | 3 | 1600px perspective 与 rotateY 组织纵深；层级服务焦点，完整动作后才切。 |
| 01-D 杂志分屏 | [editorial-performance@1.2.0-candidate](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/editorial-performance/1.2.0-candidate) | 13 | 杂志分屏、章目录、资料窗口；13 组含真实作品与新基础表达，长句落到字幕。 |
| 01-E 节拍字效 | [kinetic-performance@1.2.0-candidate](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/kinetic-performance/1.2.0-candidate) | 4 | 强字效压在语义落点；真实三项编舞单独成组，不用二项布局硬塞第三项。 |
| 02-A 纸面天平 | [paper-balance@1.0.0](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/paper-balance/1.0.0) | 1 | 天平倾斜→回稳→用途→插图→批注→三步行动；象征画面与证据分工。 |
| 02-B 纸面聚合 | [paper-ball-performance@1.0.0](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/paper-ball-performance/1.0.0) | 2 | 六卡旋吸为网络；七日历→六能力→三产物→交付卡，数量是编舞合同。 |
| 03-A 多屏展陈 | [anim4-showcase-macro@1.3.1-candidate](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/dark-3d-showcase/1.3.1-candidate) | 10 | 九屏→中央成果放大保持同源素材；多屏比较与重点报告必须连续接力。 |
| 04-A 仪器台演示 | [doubao-console-performance@0.3.0-candidate](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/doubao-console-performance/0.3.0-candidate) | 4 | 双输入融合、三步对话、手册交付；终点需留结果阅读和音效尾音。 |
| 05-A 角色与物件接力 | [vivid-sticker-performance@0.2.0-candidate](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/vivid-sticker-performance/0.2.0-candidate) | 5 | 准备者→同一物件→接收者；三反馈汇聚升级；自然收尾是独立变体。 |
| 06-A 原生竖屏 | [vibrant-color-performance@0.1.0-candidate](https://github.com/adunext/adu-motion-video/tree/4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf/packs/vibrant-color-performance/0.1.0-candidate) | 7 | 纸白/红/蓝/荧光黄绿的大字节奏；四原生+三基础组；历史版只提供竖屏。 |

### 可直接纳入导演流程的具体合同

1. **先判断表达关系与材料，再选完整镜头组。** `references/automatic-selection.md` 以语义、数量、文字容量、媒体区间、动作窗、前后依赖为硬条件；风格统一/变化只在合法候选中优化。`coherent-first` 不等于固定两三组无限循环，ABAB 也需整片节奏检查。

2. **分离三条时钟。** 真人与字幕跟随输出时间，动作跟随可映射的源时间，声音事件落到全片时间。保护窗内动作保持原速，延长发生在允许读字区；不能通过整体慢放去塞长文稿。句级字幕不能冒充词级对齐。

3. **每个镜头保存入口、状态、动作、结果、出口和尾音。** 纸天平 710–1070 帧（60fps）中的主动作不能压缩；三步每项最多4字。控制台 three-step-chat 在 26.7s 成功音后源段 26.81s 就结束，作者明确尾音越过组尾，独立片尾不能硬切。

4. **身份与数量是叙事约束。** 纸聚合是六卡/十一节点；多屏展陈的九路比较需要九段真实视频，作品墙要求至少27个独立作品；不能用重复铺格伪装独立作品。s02→s03 中央视频须同一素材。

5. **Typography 是可测容量。** 现代图文旧版 paper/ink/blue 为 `#F7F7F5/#0A0A0A/#2462EA`，标题108/88/56px，主标题 line-height1.12。公开 Kinetic `core/basic.js` 的 fit 使用真实 canvas.measureText，B1 118→80px 有界收缩；正文超过两行即拒绝。这些是源风格参数，不是所有项目通用字号。

6. **横竖版按角色重排。** 旧竖版 portrait-island 保留本地舞台后重新安置标题/人物/媒体/字幕；不把整张16:9等比塞进9:16。官网新竖版的安全区与旧版不同：Kinetic 页面写右96px/顶88px，captionPosition 默认 bottom .24 / left .08 / right .16；这些是该模板编辑预设，不是平台永恒规范。

7. **动作层次有主有次。** 公开 Kinetic `core/lib.js` 以 expo/out5/inout/spring 构成动作族；默认 show 0.55s，exit0.35s；B2 卡片 .16s 错峰、.55s 入场；B1 字符 .045s 错峰、主字 .28s、说明 .6s。火花/漂浮/呼吸只补重点，实际文稿时长与理解优先。

8. **音效属于动作，不是任意“加音效”。** `SOURCE_S` 记录 owner/call，B1 hit 在 +.58s、线写在 +1.25s，B2 每卡与错峰同拍。`references/audio.md` 当前路线要求显式完整配乐，不自动循环；全片音乐时钟不因换模板重启。源策略目标约 -15到-16 LUFS / TP≤-0.5dBTP 只是检查目标，最终 AAC 仍复测和试听。

9. **先检验内容模型，再采用知识风格。** 几何检查不变量，瑞士检查分母，孔版检查倍率/步长，地铁检查占用释放，光板检查观测点/尺度，等距检查系统边界，导图区分树和循环，黑板区分光路/视线/推论。漂亮模型不能替代事实依据。

10. **更新与证据分开保存。** 旧源码、候选状态、个人包与官网版本各有边界。现行顶层音频/字体策略已改动：旧 pack README 的 synth 默认或强制原字体是历史说明，不应覆盖当前 3.14 的显式曲目与便携字体回退。选中精确版本后重新核对冲突、当前入口和实际预览。

## 适配陷阱与验收建议

- 不把“全开源/有技术仓库”理解为匿名可下载每个当前制作包；不把公开 Files 哈希目录理解为源码正文。
- 不把 23.8667s 几何、19.95s 手账短样片写成完整特征影片。知识模板另10套展示源成片也只证明那条内容的演示，不证明任意换稿模型成立。
- 不把 70 控件、25 原生组、7 类已融入表达合成一句“70种均经过艺术验收”。原生口播和新增组件工作流可能相互独立。
- 不把静音局部 Demo、截图、顺序/反向寻帧稳定、schema通过或完整解码当成连续声画验收。
- 先看信息密度、人物裁切、字幕与平台界面避让；再看相邻镜头接力、结果阅读、尾音、BGM全长和最终编码。保留实际片段时间点和文件版本；未看的维度明确留空。
- 本次读取中部分卡片时长与页面 Runtime 秒数相差约1秒；Kinetic 卡片36秒、Runtime65秒且公开包是横屏。inventory 同时保存这些值，不自动合并。

## 额外发现：未纳入作者28页计数的预览项目

[motiontemplates/all](https://github.com/motiontemplates/all)另列“3D书 · 阿杜和那个影响了”：16:9、1920×1080、60fps，第8版完整成片演示，下载即将开放；repository/version未给。它使用照片、立体书页和双语字幕做个人叙事。本次仅核对目录记录，未读源码、未抽样此额外预览、未运行；不能加入可立即制作的模板数。

## 证据索引

- [逐项机器清单](inventory.json)：28 条含版本、画幅、具体入口声明、素材、字体/许可文件与哈希、参数表、Demo URL、实际流时长、抽帧时间、技术仓库commit、审阅状态。
- 历史仓库：`4a52ae2cff542cfb0bfcf6e93e5120c55d0110cf`；实际公网快照内容保存在 `.research-sources/adu/legacy`。
- 公共 Kinetic：`kinetic-package-evidence.json`保存本机原包 SHA-256；只读提取位于 `.research-sources/adu/kinetic-public`。
- `source-map.json` 保存28份公开文件目录；`pages.json/pages/`保存页面证据；`legacy-audit.json`保存选中实现静态信息；`media-audit.json`保存流检查与抽帧结果。
- 元宝搜索已执行一次作补充线索（request_id `1b7c6bba-6dd7-422c-bc10-75405e56c81c`）；其结果未作为未核实事实采用。GitHub API遇匿名速率限制、git clone遇传输中断，改用官方固定提交快照和现成公开包，无认证绕过。

### 实际观察的抽帧联系表

以下是抽帧，不是完整播放记录。

（第三方演示抽帧仅保留于私人研究证据；公共报告使用原模板页面链接。）

（第三方演示抽帧仅保留于私人研究证据；公共报告使用原模板页面链接。）

（第三方演示抽帧仅保留于私人研究证据；公共报告使用原模板页面链接。）

（第三方演示抽帧仅保留于私人研究证据；公共报告使用原模板页面链接。）
