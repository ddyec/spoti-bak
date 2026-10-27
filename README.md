# spoti-bak：自定义歌词与中文设置改动备份

本仓库用于保存 `ddyec/spoti.pw` 中开发的自定义改动，供以后在选定的新基础版本上核对、移植。它是**补丁与源码归档**，不是完整的上游应用，也不是已移植完成的 GPL 版本。

## 重点保存的功能

- **中文歌词匹配**：标题规范化、多艺人匹配、版本与时长校验、中文译名、来源优先级和重试、缓存更新。
- **歌词来源与同步**：QQ 音乐、酷狗、QRC 逐字时间、翻译对齐、注音、Musixmatch 翻译。
- **播放器歌词布局**：封面下歌词、固定目标位置、抵消原生延迟布局、LRC 长间奏居中和下一句前提前归位。
- **中文设置**：676 条简体中文设置文案、提示和动态参数，保留英文回退及原有设置值。
- 相关诊断、测试、审计结果、文档和构建脚本改动也已保留。

## 从哪里开始看

| 路径 | 用途 |
|---|---|
| `snapshots/final/` | 最终通过构建版本中，117 个相对 beta 基线发生变化的文件 |
| `patches/consolidated/final.patch` | 最终改动的完整补丁，基线为下方的 beta 提交 |
| `patches/mainline/` | 45 个主线自定义提交的逐提交补丁 |
| `snapshots/initial-lyrics/` | 合并 beta 之前较小的歌词实现快照，31 个变化文件 |
| `patches/consolidated/initial-lyrics.patch` | 合并 beta 之前的歌词补丁 |
| `snapshots/parallel-ev1/`、`patches/parallel-ev1/` | 另一条构建分支的 2 个提交及 4 个变化文件 |
| `commits/` | 47 份原始提交对象文本，可核验原始提交 SHA |
| `provenance.json` | 原始 SHA、父提交、作者、补丁基线、原路径、来源分类及文件摘要 |
| `PORTING.md` | 以后移植时的模块与依赖索引 |
| `licenses/`、`NOTICE.md` | 原许可原文、第三方声明与归档边界 |
| `build-evidence-*.json` | 最终版本成功构建的提交和产物摘要记录（不含 IPA） |

最终已验证源码提交：`a90b2c04474e2fd13fc0dd792ecc85527c5299e7`。

最终补丁的上游 beta 基线：`49e02e204f397b1e4197876dd622d4ee1663188e`。

早期歌词及另一条构建分支的基线：`425d68bc1761e90a6b5828864720511bcef79fa9`。

旧项目有一次合并 beta 的提交 `0d06f93455f8e2f2374168799ee16716f99015e6`。归档中该提交的补丁以 **beta 父提交**为基线，保存的是自定义集成差异；不能把它直接接在早期歌词补丁后顺序应用。优先使用 `patches/consolidated/final.patch`，或查看 `provenance.json` 的 `apply_base`。

## 检查备份

```sh
python3 tools/verify_archive.py
```

此检查不依赖旧 GitHub 仓库。它校验全部归档文件的 SHA-256、源码快照和提交补丁清单。

如本地还保留带上述原始提交的旧源码仓库，可进一步验证全部补丁能恢复原始 Git tree，且不会更改旧仓库工作区：

```sh
python3 tools/verify_archive.py --source-repo /path/to/old/spoti.pw
```

关键源码、测试和补丁正文均直接存放在本仓库，不依赖旧 fork 的链接继续存在。旧源码完整应用的未改动部分未复制到这里，因此 `snapshots/final/` 单独不能构建完整 IPA。

原文件的许可和来源已保留。新增功能、提交作者或新文件标记不等于对独立著作权或 GPL 可移植性的认定；具体边界见 `NOTICE.md`。
