# 素材池与画面唯一性

规则针对同一最终成片，不跨草稿或横竖版互相禁用。视频按实际镜头判重，同一长片里的不同镜头允许使用；同一镜头离场后再次出场禁止，即使源时间不重叠、换文件名、镜像、裁切、重编码或变速。循环同段也禁止。连续一次播放中的局部推近、拉回、慢动作不算二次出场。品牌标识、字体、统一装饰和音轨不一律禁重；有叙事内容的背景视频仍须检查。

## 素材池

每个素材驱动镜头先找至少3个真正不同候选，核验后下载1主选+至少1可用备选，关键镜头至少2备选。记录相关度、画幅、清晰度、时长、许可和适配用途，备选保留在项目内。不能用同镜头裁切版或已在别处使用的镜头凑备选；更换前重算全片冲突。独一无二的事实材料没有替代时记录原因，不以虚构替代；素材不足优先再搜或改结构，不能循环填时长。

## 数据与检查

`asset-manifest.example.json` 的 schema 2 保留原来源字段，增加：
- `segments`：片段 id、asset_id、source_asset_id、source_shot_id、原源区间、derived_from；处理件仍映射原源时间。
- `uses`：出场 id、segment_id、output 区间、timeline_clip_id、speed；一次连续展示只记一次，不用 continuity_id 豁免复播。
- `slots`：镜头用途、candidate_segment_ids、primary_segment_id、backup_segment_ids、important、不足原因。
- `coverage`：最终时间线清点、内嵌页面/生成片段是否检查、视觉对照证据。缺证据默认未核验。

运行 `python scripts/check_visuals.py asset-manifest.json --timeline film.html --ffmpeg <ffmpeg> --out visual-report.json`。判定分三层：
1. 来源关系和原源区间证明重复，或同一 source_shot_id 再出场：FAIL。区间为半开区间，首尾相接不因边界误报，但同镜头仍不可二出。
2. 多时间点的灰度差分指纹、镜像和中心裁切对照发现疑似：需实际观察；不把相似构图直接判成抄用。指纹不是穷尽检测，复杂裁切、内嵌视频和源内回放仍要看审。
3. 疑似在 `similarity_resolutions` 逐对记录 `distinct` 或 `duplicate`、理由及存在的观察证据；未处理疑似、缺映射或未清点最终时间线：UNVERIFIED。

报告绑定素材清单和时间线 SHA-256。修改后必须重跑。源记录检查通过仍不替代完整成片观察；禁止将本工具称为能检测所有画面重复。模板要求复播时改模板结构，不能以模板合同覆盖用户禁重要求。
