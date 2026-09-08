# 交互式年度数据报告生成器

> **你只管把材料甩过来** —— 从零散笔记自动生成单文件零依赖的交互式年度报告

## ✨ 核心特性

- **零依赖单文件** —— 无 CDN、无 Chart.js、离线可开、单文件可邮件/托管
- **散材料 Intake** —— 自动归类零散材料，不用填 JSON
- **缺口智能建议** —— 自动检测缺失项 + 附"如何获取"
- **4 套布局预设** —— 仪表盘/杂志/海报/横屏翻页
- **浅色/深色主题** —— 内置切换，偏好持久化
- **多期对比** —— 支持 3 年+ 同期对比，悬停显示全部数据
- **丰富交互** —— 悬停 tooltip、环比对比、PDF 导出、环形↔条形切换
- **无障碍内建** —— reduced-motion 支持

## 🚀 快速开始

### 1. 用户提供零散材料

```
2025 年度复盘：

月活跃用户 620 万，同比 +38%，去年 450 万
API 调用 52 亿，同比 +189%
可用性 99.97%

Q1 重构核心服务，性能提升 40%
Q2 上线数据分析，覆盖 80% 场景
Q3 开放 API 平台，首月破 10 亿次
Q4 国际化启动，支持英文/西班牙语

功能使用：
数据分析 35%、实时监控 28%、告警通知 20%
报表导出 12%、自定义仪表盘 5%
```

### 2. Intake 直抽

```bash
cd scripts
python intake.py ../../loose-material.txt ../../draft.json
```

### 3. Agent 复核补全

检查草稿，补充标题、强调色、caption、decimals。

### 4. 生成报告

```bash
python generate.py ../../report-data.json ../../report.html
```

输出单文件 `report.html`（零外部依赖），可直接打开查看。

## 📦 文件结构

```
annual-report/
├── SKILL.md                    # 技能定义与使用说明
├── templates/
│   ├── report-template.html    # 单文件零依赖模板（4 套布局预设）
│   ├── sample-data.json        # 完整样例（多期对比）
│   ├── sample-partial.json     # 稀疏样例（缺口检测）
│   └── sample-intake.txt       # Intake 散料样例
├── scripts/
│   ├── generate.py             # 数据 → HTML
│   ├── intake.py               # 散料 → 草稿（自然语言抽取）
│   └── verify.py               # Playwright 端到端自检
└── references/
    ├── design-system.md        # 动效与无障碍说明
    └── intake-examples.md      # Intake 真实样例
```

## 🎨 差异化卖点

| 卖点 | 说明 | 竞品 |
|------|------|------|
| **零依赖单文件** | 无 CDN、无 Chart.js、离线可开 | `interactive-dashboard-builder` 用 jsDelivr CDN |
| **散材料 Intake** | 自动归类零散材料，不用填 JSON | 竞品要求 CSV/结构化输入 |
| **缺口智能建议** | 自动检测缺失项 + 附"如何获取" | 竞品不提供补全建议 |
| **有观点设计** | Sentry/PostHog 暗色仪表盘风，开箱即"哇" | 竞品是空白模板 |
| **内建交互** | 多期对比、悬停 tooltip、浅色主题、PDF 导出 | 竞品依赖外部库或缺失 |
| **无障碍内建** | reduced-motion 支持 | 竞品不考虑 |

## 📝 使用要求

- Python 3.12（推荐）
- 无外部依赖（纯标准库）

## 📄 License

MIT License

## 🙏 致谢

- 设计灵感来自 [Sentry](https://sentry.io/) 与 [PostHog](https://posthog.com/) 的暗色仪表盘风格
- 图表使用内联 SVG，零外部库

---

**一键体验**：下载 `annual-report.zip` → 解压 → 运行 `scripts/generate.py` 即可生成你的第一份年度报告！


## 💛 支持作者

工具永久免费开源。如果它帮到了你，欢迎到爱发电请我喝杯奶茶：
https://afdian.com/a/xiaoqiangdev
你的支持让我能持续更新更多效率工具。
