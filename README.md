# spoti-bak：Spotify 中文歌词与汉化设置补丁归档

本仓库用于完整归档此前在 `spoti.pw` 分支上开发的**中文歌词匹配、封面下双语歌词排版与简体中文设置汉化**改动，方便随时在新的上游版本（如 Taurus / Spoti.reborn）中查阅、核对与移植。

> **说明**：这是一个纯粹的**源码快照与 Git 补丁归档库**，不包含未改动的上游基础工程文件，因此不能单独直接编译出完整 IPA。

---

## 归档的核心功能

- **中文歌词智能匹配**：歌名规范化、多艺人联合匹配、版本与曲目时长校验、中文译名识别、多源优先级自动重试与本地缓存更新。
- **多源双语与逐字歌词**：支持 QQ 音乐、酷狗音乐（含 QRC 逐字时间轴）、原文与中文翻译对齐、罗马音/注音，以及 Musixmatch 翻译。
- **播放页封面下歌词布局**：在专辑封面下方稳定展示滚动双语歌词，消除原生延迟布局抖动，支持长间奏居中提示与下一句提前归位。
- **全中文设置界面**：包含 676 条简体中文设置词条、说明文案与动态参数格式化，同时保留英文回退。

---

## 目录导览

| 路径 | 内容说明 |
| --- | --- |
| `patches/consolidated/final.patch` | **最常用的完整汇总补丁**（可直接基于下方说明的 beta 基线应用所有改动） |
| `snapshots/final/` | 最终验证通过版本中，全部 117 个发生过修改的源文件快照 |
| `patches/mainline/` | 主线开发过程中的 45 个独立 Git 提交补丁（按时间顺序排列） |
| `snapshots/initial-lyrics/` | 早期轻量版歌词实现快照（合并上游 beta 之前的 31 个修改文件） |
| `patches/consolidated/initial-lyrics.patch` | 早期轻量版歌词汇总补丁 |
| `snapshots/parallel-ev1/`、`patches/parallel-ev1/` | 另一条实验分支上的 2 个提交与 4 个修改文件 |
| `commits/` | 47 份原始 Git commit 对象文本，可用于核对历史提交记录 |
| `provenance.json` | 完整的提交 SHA、父提交、补丁基线与文件摘要清单 |
| `PORTING.md` | **移植指南**：梳理了各功能模块的文件依赖关系，移植前建议先读这篇 |
| `licenses/`、`NOTICE.md` | 相关开源许可证原文与第三方组件声明 |

### 关键基线 Commit SHA
- **最终汇总补丁 (`final.patch`) 对应的上游基线**：`49e02e204f397b1e4197876dd622d4ee1663188e`
- **最终已验证的完整源码提交**：`a90b2c04474e2fd13fc0dd792ecc85527c5299e7`
- **早期歌词补丁 (`initial-lyrics.patch`) 对应的基线**：`425d68bc1761e90a6b5828864720511bcef79fa9`

---

## 校验归档完整性

仓库内置了独立的校验脚本，无需联网或依赖旧仓库即可核对所有快照、补丁与 SHA-256 摘要：

```bash
python3 tools/verify_archive.py
```

如果本地保留了包含历史提交的旧源码目录，还可以进一步验证所有补丁能否原样还原出当时的 Git 树（不会修改原目录）：

```bash
python3 tools/verify_archive.py --source-repo /path/to/old/spoti.pw
```
