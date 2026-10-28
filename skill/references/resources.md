# 内部能力与使用边界

统一入口为 `video-creation-director`。Motion、MotionGit、Remotion、FFmpeg、现有视频镜头技能保留为按需内部能力；不同时运行全部，也不擅自卸载用户其他技能。

- MotionGit：[官网](https://motiongit.com/)、[公共目录](https://github.com/motiontemplates/all)。每个实际包独立检查许可、入口、画幅和依赖。
- Motion：[AI Kit](https://motion.dev/docs/ai-kit)、[免费 MCP 安装说明](https://motion.dev/docs/ai-kit-install)。文档检索与网页动效；Motion+ 不是默认免费，Motion 本身不导出视频。
- Remotion：[官方文档](https://www.remotion.dev/docs)、[渲染闪烁排查](https://www.remotion.dev/docs/flickering)、[许可](https://www.remotion.dev/license)。根据具体组织和用途核实许可，不把所有应用场景视为免费。工程包版本一致并锁定。
- Vincent：[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)、[mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)、[video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft)、[anything2explainer](https://github.com/Vincentwei1021/anything2explainer)。前二分别 Apache-2.0/MIT；后二本次核对为 PolyForm Noncommercial 1.0.0，工具包商业使用需额外授权。音频逐文件许可另查。
- 阿杜：[作者页](https://motiongit.com/@adunext)、[adu-motion-video](https://github.com/adunext/adu-motion-video)。官网包、GitHub历史示例、公开 beta 包不是同一版本。

环境路径只保存在本机 `local-environment.json`（不随公开仓库发布）。用 `scripts/preflight.py` 现场核对可执行文件与必要字体。MCP 遵循用户 on-demand-tools acquire/release，记录本任务 lease，启用配置 ≠ 宿主已加载 ≠ 实际工具调用成功。只释放自己持有的 lease。

候选生成/转写/编辑器按当前任务再核实；不因为列在资源里就声称已安装或收费已授权。不要输出、索取、上传密钥、Cookie 或个人模板凭据。
