# Vincent 公开项目与视频制作方法研究

研究快照：2026-10-28。对象为 Vincentwei1021 的全部公开仓库（含 fork），以及四个核心视频项目。以下判断只对应列出的固定提交；外部网页更新后应重新核对数量和许可。

## 核心结论

“一句话”可以启动完整编排，内部结构既可以来自现有镜头系统，也可以由模型现场编写。用户指定教程的第一例展示了不用既有 Skill、自写 WebGL 与音乐的实验；复杂的 MAD 和 MG 合集则包含素材处理与多轮返修。质量依赖可信材料、叙事任务、具体时序和视觉参数、可寻址的帧渲染、声音设计与验收。仓库和教程都没有证明任意一句话、任意素材、一次运行就稳定得到同等品质。原视频分析见 [教程研究](../tutorials/vincent.md)。

最值得迁移的是四种不同层次的方法：Shotcraft 把产品功能映射到可解释的镜头配方；Talkcraft 用语义和素材类型筛选口播镜头，并把画面绑定到词级时码；Anything2Explainer 先整理事实与因果主线，再选择画面关系；MG 通过完整风格规格、定时渲染接口与专门声音方案复现风格。这些是可选能力，不应合并成每条视频必须执行的巨型流水线。

## 范围、数量与证据

公开仓库完整分页为 30 + 28 + 0，共 **58 个唯一仓库：47 个非 fork、11 个 fork**。每个仓库均读了 README（photo-doodle 没有 README，改读 SKILL.md）及根树；47 个非 fork 另取完整递归树，均未截断。30 个小型网页仓库 README 为通用 Next.js 起步文档，因此补读页面、布局或 CLAUDE 文件确认用途。11 个 fork 只做 README/根树/许可层级审阅，没有伪称审计全部上游实现。完整逐项表见 [repositories.md](repositories.md)，机器可筛选版本为 [repositories.json](repositories.json) 与 [repositories.csv](repositories.csv)。

| 项目 | 固定提交 | 当前准确计数 | 易误读处 |
|---|---|---|---|
| video-shotcraft | [43bd349a1366](https://github.com/Vincentwei1021/video-shotcraft/commit/43bd349a136651865ecfa6ea1cf012f6e957d304) | 124 张镜头配方卡、150 个当前变体/预览；66 个历史 demo；1 个完整 Ink Press 工程、9 个主题皮肤 | 125 个 shots/*.md 包含 ATTRIBUTION.md；152 个活动区 TSX 文件不是 152 张卡；卡与变体不可相加 |
| video-talkcraft | [a7c29edfb240](https://github.com/Vincentwei1021/video-talkcraft/commit/a7c29edfb2404612dde6a5a1c8aa94232e85625b) | 108 张卡、108 个卡 TSX、108 个 HTML demo；12 个背景预设 | 当前 README 已写 108；仓库 description 仍写 109；旧 gallery-zh.png 显示 78 |
| anything2explainer | [735c79c8724e](https://github.com/Vincentwei1021/anything2explainer/commit/735c79c8724e897e8971cd59dde7e5aa11e4d6ce) | 1 套讲解视觉体系；24 种画面关系模式；RAG 示例 44 镜头、8 构建组 | 44 个 SC 源码不是 44 个独立成片模板；中英 RAG 是同题的两个语言版本 |
| mg-styles-15 | [49052d80bfaf](https://github.com/Vincentwei1021/mg-styles-15/commit/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c) | 15 份风格提示、15 个演示入口、15 个 MP4；各 10 秒 | 14 横屏 + 1 竖屏；cel 和 3D 为 24 fps，其余 30 fps；编号不连续不表示缺片 |

Shotcraft 当前数值来自 [画廊索引](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/gallery/api/library.json)，历史数来自 [legacy manifest](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/demos/_legacy/manifest.json)。Talkcraft 采用 [卡片索引](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/references/cards-index.json)、README 与目录的交叉计数。Anything 的关系表来自 [分镜文档 §4](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/reference/narration-storyboard.md)；MG 采用 [FILMS 索引](https://github.com/Vincentwei1021/mg-styles-15/blob/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c/site/data.js) 与实际树。Shotcraft 索引生成时间字段较旧，不能用它代替此次固定提交的检索日期。

全量目录已分别抽取卡片用途、类别、时长/能量、语义/输入、参数名与典型值、源码路径、demo 入口、许可及验证状态。重点推理审阅覆盖工作流、相关组件和代表镜头的实现机制。源文本获取和结构抽取不等于每个 demo 的逐帧、逐音审片；此次未运行任何第三方脚本、未安装项目依赖，也没有声称本机渲染通过。

索引共有 **554 条分层记录**：124 shot_card、150 shot_variant、66 legacy_demo、108 talk_card、15 motion_style、1 full_video_template、1 explainer_system、24 relationship_pattern、44 reference_shot、9 theme_skin、12 background_preset。这不是 554 套模板。筛选说明和记录在 [template-inventory.json](template-inventory.json)，表格版在 [template-inventory.csv](template-inventory.csv)，一致性核对见 [validation.json](validation.json)。

## 观察到什么，没有观察到什么

实际观察 20 张静态图：MG 15 片各一张 poster；Shotcraft cover 的首帧；Talkcraft 一张旧版画廊截图；RAG 的标题、混合检索、重排漏斗三个参考帧。MG 的构图、材质、排版与风格差异可以据此描述；速度、运动连贯性、声音内容与音画同步不能据此判定。Shotcraft cover 含过渡/空白区域，不能把该静帧当完整质量结论。

内置浏览器打开演示站超时，因此 **完整样片播放数为 0，听音数为 0，本机重渲染数为 0**。没有等待或反复重试拖延研究。各记录保留 motion_validation=not-played、audio_validation=not-listened。静帧来自固定提交的公开原图，原始图与下载 URL 只保存在研究来源目录；没有打包第三方影片或字体供再分发。

## Shotcraft：把“质感”拆成镜头的职责和参数

主要依据：[入口](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/SKILL.md)、[制作流程](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/references/pipeline.md)、[审美规则](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/references/aesthetic-rules.md)、[Ink Press 模板](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/template/TEMPLATE.md)。入口有“六阶段”旧措辞，但 pipeline 实际从阶段 0 到 7，不能按宣传文字臆造阶段数。

| 类别 | 卡数 | 变体/预览数 |
|---|---:|---:|
| 开场与品牌 | 11 | 11 |
| 文字与字卡 | 22 | 25 |
| 界面登场与陈列 | 21 | 22 |
| 运镜与空间 | 10 | 13 |
| 数据与指标 | 5 | 9 |
| 交互与功能演示 | 11 | 13 |
| 转场 | 15 | 19 |
| 节奏与蒙太奇 | 8 | 8 |
| 光效与强调 | 15 | 23 |
| 收尾 | 6 | 7 |

每张卡的价值不只是效果名，而是“为什么这样动”、适合表达什么、典型参数、已知失败和准确源码。配方应按镜头职责选：例如先生成无字框架再落文字，两个阶段在平面/三维运动上区分；卡片批量飞入需要可见的预备动作、逐渐变化的发牌间隔、实体堆叠厚度和落位收敛。照抄一个 overshoot 函数不会自动得到这些关系。

例如 [框架再文字生成卡](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/references/shots/effects/assemble-then-type-flyin.md) 给出 10 个骨架件、19 个文字块和明确断点，并解释字符变多后的落位预算、空格排版与停止后清除 transform。参数服务可读性；换字数、画幅和品牌后必须重新验证，而不是把数字永久定死。

Ink Press 是一个 1920×1080、30 fps、1085 帧（约 36.2 秒）、10 场景的完整产品片。它交替安排品牌、功能演示与文字停顿，最后收束到品牌。原样风格是暖纸底 #f2eee6、墨字 #13110f、琥珀强调 #955905，衬线主标题与等宽细字。4 张字卡、字幕、转场和 30 余条 SFX 分轨声明。字体是系统栈，不等于跨平台一致的字体文件。

模板有 **9 个皮肤**：Ink Press、Modern Light、Midnight、Sage、Coral、Iris、Deep Ocean、Obsidian Violet、Vintage Kraft。后八种共享同一场景结构和七项语义色；Sage/Coral/Iris 的兼容 ID 仍是 solar-pop/coral-burst/color-play。Ink Press 原栅格截图没有调色编辑器；主题只覆盖适配模板场景，不会自动改变全部 Gallery 卡。来源：[主题说明](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/template/THEMES.md)、[色板](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/template/src/themes/palettes.json)。

最可迁移的素材工程是：整页高分辨率截图、透明元素切片、同坐标系 layout 数据，以及单独的高清特写区域。PageCam 的布局级 zoom 避免 3D 变换前先降采样再放大造成文字发糊；实际效果仍受浏览器/渲染版本影响。飞入不是随便漂到画面中央，而是回到真实界面槽位。

可复用实现原则包括统一时间轴、镜头相对时间、确定性随机、速度相关模糊、可检查的 props/schema 和预览/导出共用清单。内容、颜色、字号可以暴露给使用者；关键缓动、落点与持有时间应有护栏，但并非永远不能修改。工作台的 palette / 单镜头覆盖优先级明确，避免改颜色后预览与导出不是同一结果。

音频资产树实际为 149 个 SFX（16 个分类目录）与 5 首 BGM，另有模板内 11 个选用音效副本，不能重复算为新音效。声音方法来自 [sound-design](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/references/sound-design.md) 和 [beat-sync](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/references/music-beat-sync.md)：测量采样起音、将 SFX 相对镜头定位、按样本峰值处理而不是盲调系数、长样本按语境截断、重复声音做克制变化。配乐需拍点序列与能量结构，单一 BPM 数值不足。

音频对齐要区分采样级起音和视频帧量化。在 30 fps 的最近帧定位下，理论量化误差可到约 16.7 ms，因此不能把小于 5 ms 的声学检测精度宣传成所有视觉切点的精度。来源中的 ≤3 帧或品牌停留 1 秒等是具体产品片的工作阈值，采用时应注明语境。

## Talkcraft：口播语义、素材与时间的三向约束

主要依据：[语义标注](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/references/semantic-annotation.md)、[卡片分类](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/references/taxonomy.md)、[镜头设计](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/references/shot-design.md)、[设计语言](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/references/design-language.md)、[审片协议](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/references/review-protocol.md)。

108 卡按 7 类分布：字幕花字 22、数据信息图 14、素材呈现 27、人物互动 10、转场结构 13、强调标注 14、运镜 8。26 个语义标签与 7 类输入（人、视频、图、截图、文、UI、场间关系）构成可检索目录。先判断一句话是在提出问题、给证据、比较、列举、解释机制还是收束，再检查手里确实有什么素材，最后选择卡片。

独立句子不是天然独立镜头。它把主语义、次语义、实体和视觉需求写到结构化语义表，再用候选矩阵写入 SHOTBOOK。镜头可以容纳多句，但必须有一个主要视觉任务。词级时间戳是事实源，镜头起点、cue 与字幕共用秒值，在进入帧渲染边界才量化，避免多处各自四舍五入。

皮肤与动效核心分开：可以更换字体、色板、材质、数据和真实界面；仍需保留或有意识地重新调校相对时序、几何、揭示顺序与层级。例如双色块对句的意义在于相同结构与反色，文本裁切紧跟色块边缘，而非两个元素无关地淡入。卡片确实存在硬编码示例内容，工作台参数化宣称不能代替对具体源文件的检查。

文档推荐浅色、少量强调色和克制阴影，但模板 theme.ts 仍包含一套深色/青金 token。它们属于不同样例层，不是复制模板就自动落实统一设计语言的证明。12 个 Backdrop 组件覆盖深浅网状渐变、极光、光束网格、聚光、点阵、发光球、纸纹、虹彩、玻璃与水墨；全部已在索引单列，不能把背景组件当成新增口播卡。

字体栈包含 PingFang SC、Hiragino Sans GB、Microsoft YaHei 与 Menlo/SF Mono/Cascadia Code 等系统候选。在 Windows 上不应假定苹果字体存在。选定字体后应检查中文覆盖、字重、数字等宽、标点、缩小到目标手机宽度的可读性，并锁定真实加载文件。

确定性桥接比“用网页动画库”更关键：关闭实时动画引擎循环，构建暂停时间线，按帧 seek 后捕获；Three.js 的 seek、相机更新、render 顺序要一致；避免非有限插值输入和未初始化的可见状态。帧内随机需固定种子或索引，细密纹理应避免亚像素爬动。静态规则扫描只能提示审查点，不能直接宣布每张卡都确定性通过。

独立审片的有用部分是证据包：分镜、完整接触表、原始关键帧、参考卡对应帧、词级 cue 表、SFX 可闻性证据、语义候选矩阵。高风险时刻增加前中后三帧或短片段；按理解/遮挡/事实、明显设计与同步问题、微调分级。镜头接缝需看相邻片段，不能只看每个镜头中间的漂亮一帧。

## Anything2Explainer：把资料转成可视的因果关系

主要依据：[研究简报](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/reference/research-brief.md)、[叙事指导](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/reference/narration-guidance.md)、[解说/配音/分镜](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/reference/narration-storyboard.md)、[风格](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/reference/style-guide.md)、[构图与光](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/reference/composition-and-light.md)。

研究阶段应输出来源、主张、可用数字和必要限定，叙事阶段找到唯一主线，而不是照资料目录顺序复述。每个例子与比喻必须帮助观众推理；章界交接的是问题、结果或实体，不能只用“接下来”报幕。RAG 样例的具体语境可供理解，不应强制所有题材都复用它。

关系库比领域模板更可泛化：主体属性、具象类比、核心概念、证据来源、流程、方案比较、邻近、层级、容器、合并、漏斗、曲线、有据回答、清单、权衡、网络、循环、量级、回扣、时间、公式、表格、规模、机制对照，共 24 类；它们已单独索引，并指向对应样例 SC 文件。按关系找画法比为所有概念套发光盒子更有用。

其视觉系统是明确选择的黑底科普风：紫色表示当前焦点，橙色用于比较/指标，白边描绘对象，灰色降级次要信息；HUD、内容、字幕、进度条分层。Noto Sans SC Black 的压窄中文、Audiowide 大字、Exo 2 Italic 强调与 Orbitron 数字各有角色。英文不沿用中文压窄和基线补偿。模板字体许可另有 OFL 文档，但字体选择和 1280×720 的像素安全区都不能直接成为所有视频的规则。

组件提供文本、盒子、胶囊、箭头、文档/数据库/分块/LLM 图标、漏斗、计数与强调效果。光照和动作必须指向本镜头的主角。关系流程应由真实的流动、筛选、堆叠和结果变化解释，持续漂浮不是解释机制。

配音先得到实长和词/块边界，再生成 timeline 与字幕；句级缓存便于局部修改。中文默认 Edge TTS、英文默认 Kokoro 只是该项目配置；Kokoro 无词边界时采用分块合成，不能因此声称词级对齐等价。确认脚本后再构建只是降低返工成本的方法，用户授权直出时不应转化成反复审批。

每镜头在适合的内容单元内放 2–4 句、末拍留阅读时间、共享时间令牌、章界承接实体，都是可以适配的设计思路。固定字数、每章运镜次数、紫色像素比例、主角尺寸和 glitch 频次只对这套样例体系有意义。RAG 中文约 4′35″、英文约 5′02″是 README/文档所报时长，本次未用媒体测量验证。

## MG：15 种风格、15 套参数化设计和声音

逐项设计、技术路线、字体、参数、音频与静帧观察见 [mg-styles.md](mg-styles.md)。原始入口为 [长提示模板](https://github.com/Vincentwei1021/mg-styles-15/blob/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c/template.md)、[项目说明](https://github.com/Vincentwei1021/mg-styles-15/blob/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c/README.md)。15 种是逐帧手绘、等轴 2.5D、扁平矢量、线条、3D 渲染、形变、贴纸科普、HUD、拼贴、弥散玻璃、包豪斯、Synthwave、像素、液态、综艺花字。

其提示本身不是一句话，而是角色/任务、输出尺寸与时长、技术路线、分时段创意种子、风格特征、工作方法、约束、工艺检查与交付。来源明确承认每次同一提示会得到不同影片，原作经历多轮修改，一次运行通常达不到同样完成度。作者自报的 AI 评审分数不是本研究打分，也不是效果保证。

风格差异不仅是颜色：cel 用离散帧和绘制变体；isometric 用真实正交投影；morph 需要路径对应；3D 需要材质、布光和预计算物理；pixel 需要整数网格；liquid 需要几何粘连与断颈；HUD 需要层级与可信的信息组织；综艺花字依赖动作先行和情绪时机。这些机制应成为选型条件。

渲染约定把画面变成时间的函数：renderAt(t)、固定 seed、暂停并 seek 动画、等待 document.fonts.ready / 资源 ready、预计算物理、必要时做时间超采样，再编码。[render harness](https://github.com/Vincentwei1021/mg-styles-15/blob/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c/harness/render.mjs) 含原作者系统路径和临时目录约定，未经 Windows 适配不能宣称本机开箱可用。

声音不是统一套一首 BGM。共享 cue（BPM、关键拍、drop、outro 等）驱动画面与采样/合成声部，按风格选择音色，区分节奏、空间和动作音效，做 ducking、立体声相关性与峰值/响度检查。[音频系统](https://github.com/Vincentwei1021/mg-styles-15/blob/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c/lib/audio/README.md) 的项目目标为 10 秒、24-bit WAV、约 -14 LUFS 与受控 true peak；这不是所有平台统一强制标准。

可复现也有边界：README 说明同一环境的音轨脚本确定性，但按 requirements 版本复跑，仅 4/15 与原片音轨在最低有效位范围内匹配，另外 11 个局部不同，疑与数值库版本有关。固定 seed 不等于跨环境 bit-exact。字体文件未附仓库，缺字库会回退并改变构图；每套字体与照片/音乐/HDRI/字形轮廓均需单独核对。

## 一句话生成的真实机制与迁移方式

| 层 | 应准备或保存的信息 | 解决的问题 |
|---|---|---|
| 任务简报 | 受众、平台/画幅、时长、核心信息、素材、风格、声音、交付和授权 | 一句话省略的事实不能靠任意猜测填满 |
| 内容证据 | 主张、来源、日期、限定、数字与素材权利 | 防止效果漂亮但讲错或误用素材 |
| 设计约定 | 字体实际文件/字重、角色分工、色板、构图、安全区、阅读时间、声音角色 | 保持全片一致且可读 |
| 语义与镜头库 | 输入类型、视觉关系、时长/能量、参数、已知坑、源码/许可 | 让检索匹配叙事任务而非只挑酷炫效果 |
| 镜头计划 | 每镜头目标、实体、cue、入场/变化/落定/退出、转场、音效 | 把抽象愿望变成可执行内容 |
| 执行约定 | 秒/帧边界、确定性随机、字体/资源 ready、截图坐标、同源预览和导出 | 保证可寻址、可检查、可重做 |
| 验收与改稿 | 完整内容检查、代表帧/高风险短片段、真实听音、技术参数与剩余问题 | 检出一张海报无法暴露的运动/声音问题 |

可迁移的是上表结构和判断方式；作者的代码、完整技能文本、具体影片素材需要各自许可。对商业或可能公开再分发的定制 Skill，优先原创实现这些一般方法，保留研究来源，而不是把 Noncommercial 内容换名字或整包拼装。

## 明确不应移植的强制项

| 来源里的要求/倾向 | 本任务应如何处理 |
|---|---|
| 每阶段都确认，或先必须选择创作模式 | 按用户已有授权决定；用户要求直接做就推进，只问会实质改变结果的必要缺口。Shotcraft 自身已区分自主与共同创作，不能歪曲成始终强制审批。 |
| Anything 的时长/语言、文案、配音、首 30 秒四个强制确认点 | 当成可能有价值的低成本检查机会；不是宿主之外新增的审批权。 |
| 要求指定全新上下文审片 Agent；原生委派不便时转无头 CLI 并绕过批准 | 不继承权限绕行、强制子 Agent 或固定评审次数；在真实可用工具和授权内做必要独立检查。 |
| 宣传作者账号、邀请投稿、自动打开工作台/浏览器、自动发布/上传 | 研究来源署名与宣传/外部写入不同；只做用户本次授权的交付。 |
| 结束后自动把经验写回全局 SKILL | 仅在当前项目保存可核实记录；升级全局需在明确范围内单独处理。 |
| 所有片禁手持、禁游戏 UI 音、每效果只能用一次、固定结尾 riser→impact→sparkle | Ink Press/产品片的审美选择；游戏、搞笑、纪实、音乐片可有相反要求。 |
| 所有片必须浅色、只有一个强调色、只能慢推、不得硬切 | 按品牌、题材、节奏与可读性选择；不同 MG 风格已提供反例。 |
| 所有科普都黑底紫光、必须固定运镜次数和像素大小、中文永远压窄 | 保存为具名风格预设与分辨率参数；不同画幅/语言重新测试。 |
| “已验收”、AI 评分、作者叙述能证明本机效果 | 只记录为来源自述；在新环境实际观察/听音/渲染后才能作本机完成判断。 |

## 每仓许可与重用边界

已检查所有仓库可见根许可和 GitHub 元数据；汇总是 MIT 13、Apache-2.0 2、PolyForm Noncommercial 2、AGPL-3.0 1、CC0 1、自定义 Remotion 1、已审查根目录未发现项目许可证 38。NOASSERTION 不代表没有许可：Talkcraft、Anything2Explainer 与 Remotion 都需读正文。逐仓文件路径/URL 已写入 repositories.json。

Shotcraft 代码/文档为 [Apache-2.0](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/LICENSE)，但 [音频归属](https://github.com/Vincentwei1021/video-shotcraft/blob/43bd349a136651865ecfa6ea1cf012f6e957d304/assets/audio/ATTRIBUTION.md) 单独适用；不要把 149 个音效当随 Apache 许可可任意重发的包。MG 项目代码、提示、文档与影片为 [MIT](https://github.com/Vincentwei1021/mg-styles-15/blob/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c/LICENSE)，第三方音频/纹理/地图/图片、OFL 字形、BSD 高亮组件保留自身条款。

Talkcraft 与 Anything2Explainer 工具包均为 PolyForm Noncommercial 1.0.0（[Talkcraft](https://github.com/Vincentwei1021/video-talkcraft/blob/a7c29edfb2404612dde6a5a1c8aa94232e85625b/LICENSE) / [Anything](https://github.com/Vincentwei1021/anything2explainer/blob/735c79c8724e897e8971cd59dde7e5aa11e4d6ce/LICENSE)）；README 明确商业使用需事先授权，生成影片属于创作者。输出归属不抹去工具包商用条件和输入素材权利。Synapse 为 AGPL；Remotion fork 需遵守其独立许可。无许可证的小网页或 photo-doodle 可描述其用途，不能整包搬入新 Skill 并宣称获准开源。

本报告和索引没有加入原仓库可执行代码或整个 SKILL；完整来源缓存仅用于本次本地研究。若主项目后续归档 GitHub，应排除 .research-sources/vincent，公开研究摘要也应保留来源与许可边界。

## 与目标抖音作品的关系

目标作品 ID 为 7697976597185435475，短链标识为 tYhwe8oDW9E。对已读取仓库文本搜索未发现该 ID、短链或对应逐字稿。仓库中有作者账号入口、教程入口，以及 Anything2Explainer 对其视觉参照来源的说明，但这不能证明目标视频的原话或完整操作过程。本报告不冒称观看目标作品，不把仓库推论写成视频台词。主线程另查得的标题、作者、发布日期摘要应单独标为网页检索证据。

## 推荐给主 Skill 的落点

保留三条轻量分流：产品/界面演示参考 Shotcraft，口播/解说按 Talkcraft 与关系库筛镜头，风格实验参考 MG。所有路线共用简报、真实来源、素材清单、设计约定、镜头计划和证据化验收，但按项目规模裁剪。模板选择必须区分镜头词汇、主题皮肤、完整成片、风格提示和渲染器。

优先采用可验证的工程做法：实际字体检查；同坐标素材；内容与皮肤分离；同源时间轴；声音角色与真实对齐；过渡接缝检查；预览和导出一致。对于授权、问答数量、工具选择、发布与全局改动，仍由用户目标和宿主规则决定。

## 文件与核对

- repositories.json / repositories.csv / repositories.md：58 仓库逐项用途、fork、审阅深度、固定提交、许可与来源路径。
- template-inventory.json / template-inventory.csv：554 条分层记录，逐卡参数/来源、15 风格、主题/背景与参考镜头。
- mg-styles.md：15 套风格逐项技术/字体/音频/静帧观察。
- validation.json：计数一致性、唯一 ID、文档/实现覆盖与真实观察数量。

已完成的核对：58 仓库无重复，124+108 张活动卡文档齐全，124 张 Shotcraft 卡均能定位实现路径，554 个 ID 唯一。未验证：全部 demo 的运动、所有音轨、服务与 TTS 当前可用性、本机依赖安装/渲染、Windows 剪映导入、每个第三方素材的实际商用授权链。仓库声明和静态源码不能代替这些验证。

