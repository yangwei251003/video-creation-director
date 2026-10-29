# OpenFilm 本地工作台

每次制作、剪辑视频都通过OpenFilm桌面工作台组织工程、对话修改及手动调整。固定验证基线：[v0.2.6](https://github.com/openfilm/openfilm/releases/tag/v0.2.6)，源码 `ea8cf6dcbb367065ce16d75e9784dbe2ab3e013c`。浏览器Studio与桌面版不是同一能力：聊天在桌面版。安装/连接/渲染/手改/连续看听审分别记录。

## 接入

优先后台操作：读取工程文件、软件自带CLI和本地接口，必要时用无头页面检查；不默认占用用户正在使用的屏幕和鼠标。后台方式不足才进行短暂、明确范围的前台验证，完成一个小阶段立即停止输入并释放桌面锁。接口测试、无头界面测试与真实前台手改分别记录。

优先官方Windows x64安装包，本机路径见local-environment.json。正常桌面包带渲染依赖，不要求Bun、Docker。用户级原安装、设置先备份，不初始化新账号或改CODEX_HOME。用Settings→Agents→Locate指定本机真实codex.exe；不要把会执行npx临时下载的包装器当固定版本。本机验证起点Codex CLI 0.151.0，沿用已有登录、模型和审批设置，不使用无审批/权限放开开关。

OpenFilm默认筛选技能/MCP，需明确允许video-creation-director、dynamic-skill-router和实际用到的能力；不要全量启动所有MCP。项目AGENTS.md指向导演并说明本片授权；新聊天让Agent读取实际SKILL版本作为加载证据。配置存在不等于连接成功；遇到连接错误查日志中的非敏感摘要，不输出认证文件。

模型列表也不等于当前账号能推理。遇到“not supported when using Codex with a ChatGPT account”，先查询实际会话提供的模型与推荐值，在该项目/会话内选择可用项并真实发起一次局部编辑；不改用户全局模型、账号或审批设置。若需升级CLI，另存固定版本并验证后再接入，不使用每次自动下载的包装器。

## 项目

默认 `Documents/VideoCreation/Projects/<项目名>`，包含 film.html、pages、assets/source与derived、asset-manifest.json、audio-cues.json、review.json和导出目录。研究原片、私人配置、完整转写不进公共仓库。外部资源渲染前落地，标题/字幕和要手改的布局保留DOM元素。

镜头可由Remotion/MotionGit制作后加入时间线，但烘焙片段内部文字不再可手改；应把需编辑内容放在页面覆盖层。使用对应固定版本[项目规范](https://github.com/openfilm/openfilm/blob/ea8cf6dcbb367065ce16d75e9784dbe2ab3e013c/packages/openfilm/SPEC.md)核对seek、data属性和导出，不猜API。

## 修改和音画联动

每次修改前读取最新film.html、页面、手动覆盖项和revision，先保存命名版本。保持稳定clip id，尊重锁定轨道，不整片重生覆盖用户手改。用户要求一句修改时只改相关对象，完成后重读并核对其他修改仍存在。

v0.2.6原生Link/Unlink支持page与SFX，主轨联动及ripple也已存在。短音效/字幕可跟主镜头移动，跨多个镜头的长音乐按全片时间；锁定轨道可能不跟随。Unlink只去显式链接，主轨联动可能仍在。优先验证原生行为，不叠加第二个自动同步watcher。裁切、删除及页面内部动作重定时后检查声音事件并按需修复。

实测限制：短促SFX与长画面显式Link后，原生同边裁切会受最短片段长度限制，可能无法缩短画面。不要把音效强拉长或截断来绕过。用原生单独裁切（界面Alt-alone，后台只给需要裁切的画面/页面生成操作）保留完整音效事件，再核对起音、尾音及是否仍在镜头内；若动作本身被删，删除对应事件。底层整片背景若成为主轨，会影响场景级ripple，按实际主轨和显式Link设计，不能只看开关名称。

后台辅助：`scripts/openfilm_project.py` 读取真实时间线、带revision应用操作、保存/恢复原生命名版本；restore不自动丢弃未保存改动。`scripts/openfilm_agent.py` 调用已安装桌面包的Codex适配器，在后台读写同一工程；它是版本固定的内部接口适配，和前台聊天界面验证分开。原生CLI用于look/render。具体调用见[素材与后台操作](resource-library.md)。

交付前验证：聊天能读导演→创建/打开工程→手动编辑→Agent局部修改不覆盖手改→移动/裁切/删除后的声音→撤销/重开/恢复→实际导出。仅源码支持不得写成本机实测通过。未连上时继续诊断并明确缺口，不能以独立MP4代替工作台交付。
