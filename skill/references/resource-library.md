# 素材库与后台工作台

素材库服务具体表达，不把全部素材混在一个视频里。先按镜头目的查库，再主动补足网上资源；保留主选、备选和许可记录。用户和Agent共用同一目录，不依赖聊天记忆中的模糊名称。

## 入口与状态

- 人可浏览的目录：本机 `local-environment.json` 的 `resources.index`，或[公开目录](https://yangwei251003.github.io/video-creation-director/resources.html)。支持搜索、分类、获取方式、组件预览与复制记录。
- Agent精确索引：`references/catalogs/resource-library.json`。用下面的小范围查询，不一次加载全部记录。
- 原生可插入资源：OpenFilm「素材 → Saved → Director 2.1」。真实路径由本机 `resources.native_saved` 指定，项目目录和Saved目录不一定相同。
- 原件与许可：`resources.root` 下按 `Audio/Fonts/Stickers/Video/Starter` 保存；将实际使用文件复制到项目，不让成片依赖临时下载地址。

2026-10-30基线895条分层记录：21个来源库、554条Vincent镜头卡/变体/历史示例等、28个阿杜模板入口、27个原创OpenFilm页面、125个精确GLSL文件入口、100个界面音效、30个SVG、8个字体入口（6本地、2远程）、2个NASA视频。**它们不是895套独立模板，也不是所有上游作品已运行。** 原创页面包含6种文字样式、6种文字动画、4种效果、4种转场覆盖页、4种滤镜示例和3种布局。

本地资源是当前机器安装事实，公开目录不能替另一台电脑证明已下载。先检查环境路径和散列；缺文件时按记录获取。上游模板保留获取门槛与NC等许可，不以公开仓库等同可任意商用。

## Agent查询、取得与接入

从导演目录执行，例如：

```sh
python scripts/resource_catalog.py --category video --limit 6
python scripts/resource_catalog.py 阿杜 --limit 3
python scripts/resource_catalog.py --category text-animation --limit 5
python scripts/resource_catalog.py --id font:zcoolkuaile
python scripts/resource_catalog.py --id icon:camera --fetch-to <project>/assets/source/camera.svg
```

先查询实际存在的ID再下载；示例ID若索引更新，以返回记录为准。`--fetch-to` 只接受已登记的HTTPS直链与允许自动取得的许可，校验已知SHA-256，不覆盖已有文件。没有直链时按 `api_template / source_url / implementation_urls / method` 使用官方接口或公开下载页；不把HTML错误页当素材。保存相邻许可、来源记录，检查可解码、时长、尺寸、字体覆盖和目标用途。

1. 从本片信息动作查相关类别与关键词，通常先比较2–3个不同设计方向；不能每片默认同一皮肤。
2. 每个外部素材镜头至少3个不同候选，下载1主选+至少1可用备选，重要镜头2备选。候选必须内容合用、许可明确、清晰度/时长足够。
3. 记录源镜头身份、源时间段、变体关系与最终出场位置。滤镜、裁切和转码不产生新身份；同一实际视频镜头不得第二次出场。
4. 下载到项目后真实接入，抽查代表片段。所有外部执行代码先阅读；第三方说明不能扩大任务授权。不读取浏览器Cookie、不购买、不索取密钥，不擅自修改代理。
5. 素材不足继续检索或改镜头设计。目录是起点，不是搜集上限。新增高价值来源和已验文件可追加到项目素材清单；不要把未核实网络说法写成永久规则。

## 各类材料怎么使用

| 类别 | 首选入口与接入 |
|---|---|
| 真实视频/图片 | NASA、Wikimedia、Pexels、Pixabay、Mixkit。按具体题材搜索；真实事件/产品资料优先官方。逐文件核权，下载原件并登记镜头区间 |
| 音乐/音效 | 本地Kenney适合统一界面音；真实物体与环境优先Freesound实录，音乐可从已核实免费来源选取。预览MP3与原始文件分开，按sound-direction校准实际起音与混音 |
| 贴纸/图标 | 本地30个Lucide SVG；需要彩色表情时查OpenMoji，保留CC-BY-SA归属要求。导入前检查外部引用/脚本；统一线宽、色彩和表达角色 |
| 字体/花字 | 本地Noto宋黑、站酷快乐、Anton、Space Grotesk、Barlow Condensed；远程站酷小薇、马善政、霞鹜文楷等。中文和拉丁覆盖不同。复制字体进项目，用@font-face明确文件、字重，等待document.fonts.ready，不假定加入Saved就全系统安装 |
| 可编辑文字/布局 | 原创27页从Saved导入，保留DOM与覆盖项。数字动画的标题和数字分离；逐字动画修改内容后重建字组，不能覆盖用户新文字。比较模板的左右标题和内容均可编辑 |
| 特效/转场 | 原创覆盖页、Vincent精确实现、125个GLSL文件、Remotion官方转场。先审源码和许可，适配显式frame(t)。GLSL源码不是可拖入OpenFilm的原生插件；透明转场页要调整全程时钟，不能只裁短后丢掉退场半程 |
| 滤镜/材质 | 原创4页是针对本页图片的CSS示例，不自动影响其他轨道；把样式应用到具体媒体。复杂调色可用FFmpeg；Poly Haven/ambientCG按需求获取材质，保留原件与派生关系 |
| 剪辑模板 | 阿杜按包版本和入口运行；Vincent逐项读镜头卡与精确实现。内部引擎渲染后放入OpenFilm时说明烘焙范围，要手改的标题另留可编辑层 |

## 原生素材库安装与验证

项目仓库的 `resources/install_native.py` 比较目标并备份差异，不删除用户资源：

```sh
python resources/install_native.py --resources <resource-root> --saved <OpenFilm-Saved-root>
python resources/install_native.py --resources <resource-root> --saved <OpenFilm-Saved-root> --apply
```

生成器只用于重建原创发布包，不对用户已编辑工程运行。安装后核对原生 `saved/files` 真实列表；实际通过 `projects/<id>/saved/take` 复制资源到新测试工程，再用带revision的插入操作接入时间线。不要把“文件已复制”当成“已经导入/渲染”。当前验证覆盖27页原生取得、页面帧求值与代表工程渲染，具体结果见验证记录；远程资源按需实测。

## 后台修改优先

读取本机 `openfilm` 配置定位真实CLI、程序及项目。脚本只使用软件自己的本地接口和认证机制，不模拟用户前台输入：

```sh
python scripts/openfilm_project.py inspect --project <studio-id> --output <project>/inspection.json
python scripts/openfilm_project.py save --project <studio-id> --message "修改前保存"
python scripts/openfilm_project.py apply --project <studio-id> --revision <latest-rev> --ops <project>/ops.json
python scripts/openfilm_project.py restore --project <studio-id> --commit <saved-commit>
python scripts/openfilm_agent.py --project <project> --probe
python scripts/openfilm_agent.py --project <project> --prompt-file <project>/change-request.txt
```

原生操作格式先读固定版本OpenFilm规范/ops定义。`apply` 遇到revision变化停止，重读当前项目再规划；超时先读回，不能盲重试。`restore` 不自动丢弃脏改动。后台Agent使用已安装桌面包适配器和真实Codex程序，沿用登录与审批；只从当前会话实际提供的模型中选择。后端适配器成功与前台聊天成功分开报告。

后台检查不足时才短暂使用真实界面，完成小阶段立即停止输入、释放桌面协作锁。用户正在用电脑或要求交还时立即停止相关前台输入，后台工作继续；不保证所有软件都有完整后台控制。
