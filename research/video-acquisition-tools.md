# 抖音视频获取工具：有界调查与实际选型

日期：2026-10-28。只调查维护者的公开仓库、提交、发行说明和源码；本子任务未安装/运行第三方程序、未读本机凭据、未提交链接到公共解析站。

## 结论与本任务结果

本任务已出现足够的新证据，采用轻量的公开 feed 精确 ID 解析流程即可，不再继续安装重型工具。主 Agent 先用该流程取回 7697976597185435475，随后确认三条指定视频均下载成功；未用 Cookie、签名或账号凭据。此处成功来源是本任务主 Agent 的本机结果，不是本研究者独立重跑。

第一条本地证据为 .research-sources/tutorials/vincent/source-info.json：22,765,602 bytes，SHA256 ddd0174c8631773f4d511326d518a6854c0cc0d0066444750b7644942e011464。下载完成不等于已经观看/听音/转写。

此前 yt-dlp 2026.10.26 对目标报 Fresh cookies，IAB/Edge 超时、Firecrawl 普通页失败，说明这些入口在该环境未打通；不应把它扩写成公开视频内容永远无法取得。

## 优先候选：vangie/douyin-transcriber

完整固定提交：[b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123](https://github.com/vangie/douyin-transcriber/commit/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123)；v0.4.0 发布于 2026-10-27。真正与本任务有关的修复是 [2026-10-26 提交 ee454d61f3f3b1e777d0966376c124a00a693b9b](https://github.com/vangie/douyin-transcriber/commit/ee454d61f3f3b1e777d0966376c124a00a693b9b) 和 [v0.3.0 发行说明](https://github.com/vangie/douyin-transcriber/releases/tag/v0.3.0)：旧分享页不再带 videoInfoRes，移动 feed 仍返回目标作品及可播放媒体。

[当前 downloader.go](https://github.com/vangie/douyin-transcriber/blob/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123/internal/downloader/downloader.go) 的真实优先级是 feed → 旧分享页 fallback，README 的“直接从移动分享页读取”已落后于代码。feed URL 为官方公开域 aweme.snssdk.com 的 /aweme/v1/feed/，查询含目标 aweme_id、version_code=270800、app_name=aweme。返回是混合 aweme_list，必须比较 aweme_id 精确选择目标；不能直接取第一条。优先 play_addr_h264，因为来源注释说明它通常带 AAC；仍须用 ffprobe 验证实际音轨。

依赖与 Windows：Go 1.26.0，Cobra 1.10.2；本地转写另需 FFmpeg、whisper.cpp CLI 与 ggml 模型。GoReleaser 配置列出 Windows amd64/arm64，但本次读取的 v0.4.0/v0.3.0 release assets 均为空，不能说已有可下载 Windows EXE。源码使用 os.TempDir、filepath.Join、exec.Command，具备跨平台基础；README 安装仅写 Homebrew、Raycast 也是 macOS 集成，不是 Windows 完整安装证明。

证据：[go.mod](https://github.com/vangie/douyin-transcriber/blob/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123/go.mod)、[构建目标](https://github.com/vangie/douyin-transcriber/blob/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123/.goreleaser.yaml)、[本地转写](https://github.com/vangie/douyin-transcriber/blob/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123/internal/transcriber/local.go)、[缓存](https://github.com/vangie/douyin-transcriber/blob/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123/internal/cache/cache.go)。本机已有视频读取的 Python/FFmpeg/ASR 能力，原创适配一般接口流程比再装 Go、whisper.cpp、Raycast 更直接。

认证/数据去向：当前获取流程不读 Cookie、不需要登录/API key；公开 HTTP 接口若以后返回验证或认证要求，应停止该路径，不绕过验证码。CLI 的可选远程 speech/chat 支持 API key；主入口会读 OPENAI_API_KEY 环境变量，模型发现会探测 Magpie/Ollama/可选远端，默认还会润色转写。当前任务应复用现有本地 ASR，或明确 --no-polish，保留未经润色的识别稿。润色不是作者原话。

适配时应修正的边界：限定抖音输入域名并检查每跳重定向；作品 ID 仅允许数字；媒体限定合理协议/来源并设大小、时间上限；精确 ID 匹配；验证容器、时长和音轨；保持公开资料与本机凭据分离。源实现的域名判断部分使用字符串包含、下载没有字节上限，不能直接升格为通用安全读取器。缓存的 24 小时 TTL 是“不再复用旧缓存”，不是 24 小时后主动删除；Windows 的临时目录不会因此得到自动清理保证。

源码本地 ASR 加了 --no-timestamps，得到的是无时间码文本；本任务需要时间码，应保留现有转写器的分段时间戳，不能为了采用下载器而降低证据质量。

最近成功证据：维护者 2026-10-26 的明确修复说明 + 本任务 2026-10-28 精确 ID 下载成功。尚未证明所有抖音视频、所有网络环境、失效/私密/限制内容均可读取。

## 另外两个可用性有条件的候选

| 候选 | 当前维护/Windows/依赖 | 认证与输出 | 本任务判断 |
|---|---|---|---|
| [JoeanAmier/TikTokDownloader（DouK）](https://github.com/JoeanAmier/TikTokDownloader) | 固定 master 473c90ff70c663cfb69310fff2b8d5192f200661；[5.8 release](https://github.com/JoeanAmier/TikTokDownloader/releases/tag/5.8) 为 2026-09-13，含 Windows X64/ARM64 zip；源码 Python≥3.12，curl_cffi、FastAPI、lxml、openpyxl 等 | 官方使用流程要求配置 Cookie；失败时建议更新/使用登录 Cookie。5.8 已移除从浏览器自动读 Cookie，README 功能列表有旧行。下载/元数据为主，不等于内建可靠逐字稿 | GPL-3.0；作为需要批量管理时的备用。没有找到与这三条目标匹配的近期无 Cookie 成功记录，不会解决认证本身。服务器模式默认局域网、动态外部 Python 加载均不适合无审查开启 |
| [Johnserf-Seed/f2](https://github.com/Johnserf-Seed/f2) | 当前默认 v0.0.1.8-pw3，固定 f6be8c0ffba9a127075bbeafe4838716650b6325，2026-10-06；pyproject 要求 Python≥3.11，httpx、curl_cffi、browser_cookie3 等；文档有 Windows/跨平台路径 | 文档区分游客公开内容与登录内容，有 Cookie 配置及单作品 API；不能把“不登录”理解为永不需要会话 Cookie。可下载媒体/接口数据，ASR仍另接 | Apache-2.0；适合后续多平台适配。最新正式 release 仍为 0.0.1.7（2024-12-31），当前分支依赖与旧版不同；没有核实近期对应目标成功实例。本次不安装 |

F2 证据：[pyproject](https://github.com/Johnserf-Seed/f2/blob/f6be8c0ffba9a127075bbeafe4838716650b6325/pyproject.toml)、[单作品示例](https://github.com/Johnserf-Seed/f2/blob/f6be8c0ffba9a127075bbeafe4838716650b6325/docs/snippets/douyin/one-video.py)、[CLI 文档](https://github.com/Johnserf-Seed/f2/blob/f6be8c0ffba9a127075bbeafe4838716650b6325/docs/guide/apps/douyin/cli.md)。DouK 证据：[README Cookie 段](https://github.com/JoeanAmier/TikTokDownloader/blob/473c90ff70c663cfb69310fff2b8d5192f200661/README.md)、[依赖](https://github.com/JoeanAmier/TikTokDownloader/blob/473c90ff70c663cfb69310fff2b8d5192f200661/pyproject.toml)。源码/发行资产存在是维护证据，不是本机安装验收。

## 不采用的候选

bitabc/douyin-parser：固定 bc493bba5e712c83653090b9822569f5ff6e44fb，最后提交 2026-05-26；纯 Python 核心对 Windows 可适配，运行依赖 Python≥3.11、httpx/FastAPI/uvicorn/Pydantic。parsers.py 当前用标准 json，README/pyproject 中 msgspec 说明存在历史残留。该仓仍依赖旧 _ROUTER_DATA。README 声明 MIT，但整个文件树没有 LICENSE，GitHub 未识别项目许可证；不能描述为已核验完整 MIT 正文。

更关键的是它最后一次提交明确移除媒体代理域名白名单与 IP 防护，api.py 对代理目标仅做协议/主机名基本验证，无鉴权、CORS *、默认 0.0.0.0。不能原样公开部署。2026-05-26 提交曾自报 46 项测试含集成通过，但不是 2026-10-28 的视频解析成功证据。来源：[最后提交](https://github.com/bitabc/douyin-parser/commit/bc493bba5e712c83653090b9822569f5ff6e44fb)、[api.py](https://github.com/bitabc/douyin-parser/blob/bc493bba5e712c83653090b9822569f5ff6e44fb/api.py)、[旧成功自述](https://github.com/bitabc/douyin-parser/commit/c09e0686d52b0ddf294ced12b7a57281159c73cb)。

Evil0ctal/Douyin_TikTok_Download_API：仍活跃，v5.1.8 为 2026-10-27，固定 b5505e3830a2e4b9b8608962f58e96dfe75f23c5，Apache-2.0。当前已是身份池、调度器、PostgreSQL、Redis、浏览器、下载器、转写器、MCP 的自托管多服务系统，Python 3.12–3.13；Windows 通常需 Docker Desktop/WSL2 路径，不是简单脚本。提供本地实例 API key 与身份管理，平台登录要求按端点区分。它有 2026 年的维护与安全修复记录，但本任务三个公开视频无需上这一整套，也不需要账号池、代理轮换或验证码能力。[5.1.8](https://github.com/Evil0ctal/Douyin_TikTok_Download_API/releases/tag/v5.1.8)、[依赖](https://github.com/Evil0ctal/Douyin_TikTok_Download_API/blob/b5505e3830a2e4b9b8608962f58e96dfe75f23c5/pyproject.toml)。

## 完整 MIT 证据（仅适用于 vangie/douyin-transcriber 源码）

来源：[固定提交 LICENSE](https://github.com/vangie/douyin-transcriber/blob/b397d3e8ab2f85c9955ee0cd199b8f66c0f9b123/LICENSE)。版权主体为 **Copyright (c) 2026 BabelCloud**。采用实质代码时须保留该声明与许可；下载器许可不授予第三方视频公开再分发权。下列为其完整许可正文：

```text
MIT License

Copyright (c) 2026 BabelCloud

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

视频仅存本地研究来源目录，公开成果只保留必要摘要、时间码、来源和验证范围；不发布第三方原视频或完整转录。后续分析沿用本机 video-link-reader 的证据分层：元数据、字幕/ASR、抽帧与完整连续观看分别报告。

