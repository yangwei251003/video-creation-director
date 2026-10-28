# 原创设计验证场

15秒、30fps、三个连续镜头，分别输出1920×1080与1080×1920。默认静音，用于字体、信息组件、阅读窗口和转场验证。

```sh
npm ci
npm run check
npm run studio
npm run render:wide
npm run render:vertical
```

依赖固定Remotion 4.0.539，使用帧时间与本地字体。若无可用Chrome，按Remotion提示准备其浏览器；本次Windows验证显式使用已安装Chrome。需要时在渲染命令尾部添加 `--browser-executable=<Chrome path>`。

字体为官方Noto Sans SC与Noto Serif SC，原始OFL许可证与来源散列在 `public/fonts/`。`fetch_fonts.py` 可以从已固定的官方源重新取得并按Git blob核验；源码更新不应静默替换旧字库。

`src/Opening.tsx`、`src/Structure.tsx`、`src/Closing.tsx`定义三镜头，`src/design.tsx`定义字体/颜色/共享部件，`src/Root.tsx`登记两种画幅。修改真实文字后再次检查换行、字符覆盖、安全区与转场中段，不仅检查编译。

这不是对第三方模板的复制，也不是全题材通用模板。公开示例只含原创图形与已获OFL授权的字体，未使用研究中下载的第三方教程/演示视频。
