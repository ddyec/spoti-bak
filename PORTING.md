# 后续移植索引

所有下列源码路径均相对于 `snapshots/final/`；原始路径和 blob SHA 见 `provenance.json`。

## 1. 中文搜索、匹配、翻译

入口在 `tweak/Sources/Shared/LyricsSources/`：

- `LyricsMatching.m`：标题、艺人、译名、版本和时长等匹配约束。
- `QQMusic.m`、`KuGou.m`：国内来源查询、候选校验、歌词解析和翻译/注音。
- `QQMusicQRC.c/.h`、`QQMusicDecoder-LICENSE`：QRC 解码及其第三方声明。
- `LyricsSources.h/.m`：查询模型、来源顺序、缓存、翻译合并与显示结果发布。
- `LyricsHook.x`、`Shared/Lyrics/KaraokeSource.x`：旧版 Spotify 请求接口和歌词缓存的集成。这一层需要按新基础项目重新接入。
- `Musixmatch.m`、`NetEase.m`、`LrcLib.m` 等：相关来源适配修改。

移植时保留来源优先级、艺人/版本校验和有界请求。不要为了找得到歌词而取消候选身份检查；不要用另一句的译文填补缺失翻译。

## 2. 封面与歌词时间轴

- `Redesigned/Player/PlayerPreview.x`：预览布局、歌词行、已知间奏判定。
- `Redesigned/Player/PlayerArtwork.x`、`Player.h`：绝对位置锚点、阴影同步和原生布局修正。
- `Redesigned/Lyrics/SGRKaraokeView.m/.h`：逐字视图、换行和翻译显示的相关差异。
- `Native/Player/LyricsPreview.x`：原生外观的歌词预览回退。

长间奏按已有歌词时间轴判断，阈值沿用 7 秒；下一句前 750 毫秒开始回位。临时缓存/时钟未知状态保留此前位置。不要把“原生歌词存在”视为“已留够显示空间”。

这些文件依赖旧项目的 `SGKaraokeLine`、播放器时钟、UIKit 视图树以及具体 Spotify 类。换基础项目后须重接接口；快照不代表可直接拷贝编译。

## 3. 中文设置

- `localization/zh-Hans.json`：676 条文案的可编辑来源。
- `Core/SGLocalization*`、`Core/SGChinese.inc`：查找、语言回退及编译进代码的词条。
- `Settings/SGPageStyle.*`、`SGPage.m`、`SGModPage.m`、`SGOrderPage.m`：显示层集成。

只翻译展示文本和格式模板，不翻译设置键、功能标识、URL、用户自定义名称或参数值。用于新版时仍需逐页接入。

## 4. 验证材料

- `scripts/test-preview-anchor.py`：从生产源码抽取几何/时间轴函数的可移植 C 回归。
- `scripts/test-localization.py`、`scripts/generate-localization.py`：词条与占位符校验，macOS 上运行 Foundation 回归。
- `scripts/test-lyrics-identity.py`、`test-lyrics-requests.py`、`test-lyrics-order.py`：身份、翻译对齐、来源顺序与请求测试；需要完整基础代码及部分 macOS SDK。
- `docs/lyrics-*`、`docs/english-*`、`docs/stay-*`：匹配审计、边界案例和原始结果。
- `docs/player-preview-anchor-2026-10-23.md`：封面/歌词方案与真机验收场景。

成功构建记录针对原始提交 `a90b2c0` 和 Spotify 9.1.78，而不是尚未选定的新 GPL 基础项目。测试通过和许可来源是两件需要分别核对的事。
