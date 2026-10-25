# 土力学速查手册

面向大学生期末考试与考研复习的土力学系统性速查手册：8 个章节 + 1 份全书公式速查总表，公式完整析出，每个公式附参数说明、单位与适用条件。

## 项目结构

| 路径 | 内容 |
|------|------|
| [markdown版本/](markdown版本/) | 全部 Markdown 源文档（**唯一编辑入口**：README、9 章、总册） |
| [PDF导出/](PDF导出/) | 各章 + 总册的 PDF（学术黑白 A4 版式） |
| [LaTeX版本/](LaTeX版本/) | 每个 Markdown 对应的独立可编译 `.tex` 源文件 |
| [.claude/pdf-build/](.claude/pdf-build/) | 构建管线（版式模板、Lua 过滤器、构建脚本） |

## 文档版本

同一份内容维护三种版本，**Markdown 为源**，PDF 与 LaTeX 均由它生成：

| 版本 | 位置 | 特点 |
|------|------|------|
| Markdown | `markdown版本/` | 编辑入口；公式用 LaTeX 语法，Typora / Obsidian 可预览 |
| LaTeX | `LaTeX版本/` | 独立自包含，`xelatex` 直接编译，版式与 PDF 一致 |
| PDF | `PDF导出/` | 学术黑白 A4；总册含居中封面与带页码目录 |

## 构建命令

在项目根目录执行：

| 命令 | 作用 |
|------|------|
| `bash .claude/pdf-build/build_tex.sh` | 重新生成全部 LaTeX 版本 |
| `bash .claude/pdf-build/build.sh` | 重新导出各章 PDF |
| `bash .claude/pdf-build/build_merged.sh` | 重新导出总册 PDF |
| `python .claude/pdf-build/merge.py` | 重新合并总册 Markdown（封面 + 目录 + 各章） |

## 手册使用说明

章节导读、快速入手路径、公式渲染说明与编写维护约定，见 [markdown版本/README.md](markdown版本/README.md)。
