# 交互式年度数据报告生成器

**一句话描述**：从零散材料自动生成单文件零依赖的交互式年度报告，含 4 套布局预设、浅色主题、多期对比、悬停交互、缺口智能提示，无需 CDN、无需填表。

---

## 何时使用

**自动触发（不要求 @ 提及）**：当用户提供的零散材料带有"对某段时间的成果做总结/展示"的意味时，应主动启用此技能。典型触发信号：

- **时间跨度表述**：2025 年度、去年、Q1-Q4、2024 H1/H2、本季度
- **成果回顾**：复盘、总结、汇报、回顾、业绩、成效、成果、亮点
- **数量化输出**：指标、增长、里程碑、占比、分布、同比、环比
- **交付场景**：年报、季报、周报、全员会、董事会、复盘会

**不触发场景**：纯技术问答（如"怎么写 SQL"）、菜谱、新闻摘要——除非用户明确说"做个报告"。

---

## 工作流程

### Phase 1: 收料（无固定格式要求）

用户直接把零散材料甩过来，可以是：
- 会议纪要碎碎念
- BI 导出的表格文本
- 聊天记录里飘着的数字
- 半张手写的复盘笔记
- 任何非结构化的文字材料

**不要要求用户填固定 JSON 格式**——那是技能该干的事，不是用户该干的。

### Phase 2: 自动归类（`scripts/intake.py`）

用启发式规则识别并归类：
- 纯数字+单位 → 指标（metrics）
- 时间轴+数值序列 → 增长曲线（growth）
- 事件+季度 → 里程碑（milestones）
- 功能+占比 → 功能分布（features）
- 职能+成就 → 团队亮点（team）
- 明年方向 → 展望（outlook）

输出草稿 JSON（含 `_hint` 提示 agent 复核）。

### Phase 3: Agent 复核与补全

检查草稿质量：
- 核对数字、单位与归类是否准确
- 补充缺失的标题、副标题、时间段
- 设强调色（accent）、预设（preset）
- 给增长曲线写 caption（默认为"月活跃用户"）
- 为需要小数的指标加 `decimals`（如 99.97%）
- 标注口径差异（如月均值 vs 年末值）

最终产出 `REPORT_DATA`（完整 JSON）。

### Phase 4: 生成报告（`scripts/generate.py`）

```bash
cd C:\Users\Administrator\.workbuddy\skills\annual-report\scripts
D:\Python312\python.exe generate.py ..\templates\sample-data.json ..\report.html
```

输出单文件 HTML（零外部依赖），自动应用：
- 浅色/深色主题（默认深色，支持切换）
- 布局预设（dashboard/magazine/poster/deck）
- 多期对比（`growth.series`）
- 悬停 tooltip、同比、PDF 导出、环形↔条形切换

### Phase 5: 缺口智能建议

报告末尾自动出现「数据补全建议」区：
- 自动检测 6 个可选区块缺失（指标/增长/里程碑/功能/团队/展望）
- 每条建议附带**如何获取**（如"补 NPS 指标即可生成指标卡"）
- agent 还可补手动"有但偏薄"的建议（如"指标偏薄，建议补充市场份额"）

### Phase 6: 交付与迭代

交付单文件 HTML，用户可直接：
- 浏览器打开查看
- 打印/PDF 导出（内置 `@media print`）
- 发邮件/托管/嵌入
- 切换主题与布局预设

根据用户反馈迭代数据与文案。

---

## 数据表示（JSON Schema）

```json
{
  "meta": {
    "title": "2025 Annual Report",
    "subtitle": "Engineering Team Highlights",
    "period": "2025年1月-12月",
    "author": "Product & Engineering",
    "accent": "violet",
    "preset": "dashboard",
    "labels": {
      "metrics": "核心指标",
      "growth": "用户增长",
      "milestones": "产品里程碑",
      "features": "功能使用分布",
      "team": "团队亮点",
      "outlook": "展望 2026"
    }
  },
  "metrics": [
    {
      "label": "月活跃用户",
      "value": 620,
      "unit": "万",
      "prev": 450,
      "delta": "+38%",
      "decimals": 0
    },
    {
      "label": "API 调用",
      "value": 52,
      "unit": "亿",
      "prev": 18,
      "delta": "+189%",
      "decimals": 1
    },
    {
      "label": "可用性",
      "value": 99.97,
      "unit": "%",
      "prev": 99.95,
      "delta": "+0.02%",
      "decimals": 2
    }
  ],
  "growth": {
    "caption": "月活跃用户（MAU）",
    "labels": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
    "series": [
      {
        "label": "2023",
        "data": [0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.2],
        "color": "#666",
        "dash": true
      },
      {
        "label": "2024",
        "data": [1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.5, 3.8, 4.2, 4.5],
        "color": "#999",
        "dash": true
      },
      {
        "label": "2025",
        "data": [3.3, 3.7, 4.2, 4.6, 5.0, 5.5, 5.8, 6.1, 6.3, 6.4, 6.4, 6.55],
        "color": "#c2ef4e"
      }
    ]
  },
  "milestones": [
    {"quarter": "Q1", "title": "重构核心服务", "detail": "性能提升 40%，延迟降低 150ms"},
    {"quarter": "Q2", "title": "上线数据分析", "detail": "覆盖 80% 核心业务场景"},
    {"quarter": "Q3", "title": "开放 API 平台", "detail": "首月调用破 10 亿次"},
    {"quarter": "Q4", "title": "国际化启动", "detail": "支持英文/西班牙语界面"}
  ],
  "features": [
    {"label": "数据分析", "value": 35},
    {"label": "实时监控", "value": 28},
    {"label": "告警通知", "value": 20},
    {"label": "报表导出", "value": 12},
    {"label": "自定义仪表盘", "value": 5}
  ],
  "team": [
    {"label": "工程", "achievement": "重构 50+ 核心模块，性能提升 40%"},
    {"label": "产品", "achievement": "完成 12 个版本迭代，用户满意度达 4.8/5"},
    {"label": "设计", "achievement": "统一设计系统，交付 200+ 组件"},
    {"label": "运营", "achievement": "组织 4 场技术沙龙，覆盖 500+ 开发者"}
  ],
  "outlook": [
    {"title": "深化数据分析", "detail": "增强预测与异常检测能力"},
    {"title": "拓展生态", "detail": "与 5 家头部 SaaS 厂商深度集成"},
    {"title": "全球化", "detail": "支持 10 种语言，覆盖 20 个国家"}
  ],
  "gaps": [
    {"item": "市场份额", "how": "可从第三方行业报告获取"},
    {"item": "客户留存率", "how": "可从 CRM 系统导出"}
  ]
}
```

**关键字段说明**：

| 字段 | 说明 | 必需 |
|------|------|------|
| `meta.title` | 报告标题 | 必需 |
| `meta.accent` | 强调色：lime/cyan/amber/violet/rose/blue | 可选，默认 lime |
| `meta.preset` | 布局预设：dashboard/magazine/poster/deck | 可选，默认 dashboard |
| `metrics[].prev` | 上年/前期值，用于同比 | 可选 |
| `metrics[].delta` | 增长率 | 可选 |
| `metrics[].decimals` | 小数位数 | 可选，默认 0 |
| `growth.series` | 多期对比（`prevData` 为双期写法） | 可选，单期省略 |
| `gaps[].how` | 如何获取该数据 | 可选，自动检测项自动附加 |

---

## 归类规则（`intake.py`）

启发式识别逻辑：

| 信号 | 归类为 | 样例 |
|------|--------|------|
| 纯数字+单位（不含"月"字） | 指标 | "620 万"、"52 亿"、"99.97%" |
| 月份+数值序列 | 增长 | "1月 3.3万、2月 3.7万..." |
| 季度+事件 | 里程碑 | "Q1 重构核心服务"、"Q4 国际化启动" |
| 功能+占比 | 功能分布 | "数据分析 35%、实时监控 28%..." |
| 职能+成就 | 团队亮点 | "工程：重构 50+ 模块" |
| 明年方向/展望 | 展望 | "明年深化数据分析、拓展生态" |

**防误判**：
- 跳过含"月份+数值"开头的行（避免增长行误抽为指标）
- 抽指标前先剥括号内容（消除"（单位 万）"噪声）
- 百分比行除非含"同比/率"等 KPI 信号才当指标

---

## 报告内交互能力

### 1. 浅色/深色主题切换
- 导航右上角按钮，`localStorage` 持久化
- 浅色主题下环形图对比度安全配色

### 2. 多期对比
- `growth.series` 支持多年序列
- 当期实线 + 往期虚线 + 图例
- 悬停浮窗并列各期数值

### 3. 悬停 Tooltip
- 折线图就近取点 → 引导线 + 高亮点 + 浮窗
- 环形图图例悬停 → 对应扇区描边高亮

### 4. 环形 ↔ 条形切换
- 功能分布区右上角切换键
- 条形视图带宽度增长动效

### 5. 同比对比
- 指标卡显示上年/前期值
- 折线图可叠上年虚线（`growth.prevData` 写法）

### 6. PDF 导出 / 打印
- 右下角悬浮按钮调用 `window.print()`
- `@media print` 强制终态（图表填满、隐藏导航/进度/按钮）

### 7. 布局预设（4 套）
- **dashboard**（默认）：暗色仪表盘、居中 Hero、无衬线
- **magazine**：编辑风、衬线标题、左对齐、大留白
- **poster**：海报风、超大字号、一屏一结论
- **deck**：横屏翻页、scroll-snap、每区块一页

### 8. 无障碍
- `prefers-reduced-motion` 下直出终值、动效禁用

---

## 质量门禁（自检清单）

生成前检查：

- [ ] SKILL.md 已触发（语境匹配）
- [ ] Intake 草稿已复核（数字、单位、归类准确）
- [ ] `meta.title`/`period` 已补充
- [ ] 需要小数的指标已加 `decimals`
- [ ] `growth.caption` 已写真实标题（默认"月活跃用户"）

生成后检查（`scripts/verify.py`）：

- [ ] 零控制台错误
- [ ] 6 区块渲染正常（指标/增长/里程碑/功能/团队/展望）
- [ ] 多期对比虚线+图例显示
- [ ] 悬停 tooltip 正常
- [ ] 环形↔条形切换正常
- [ ] 浅色主题配色对比度安全
- [ ] PDF 导出触发 `window.print()`
- [ ] 零外部依赖（无 CDN/外部字体/图片 URL）

---

## 快速开始

### 1. 用户提供零散材料

```
2025 年度复盘：

月活跃用户 620 万，同比 +38%，去年 450 万
API 调用 52 亿，同比 +189%
可用性 99.97%

月活走势（单位 万，凑了 12 个月）：
1月 3.3、2月 3.7、3月 4.2、4月 4.6、5月 5.0
6月 5.5、7月 5.8、8月 6.1、9月 6.3、10月 6.4
11月 6.4、12月 6.55

Q1 重构核心服务，性能提升 40%
Q2 上线数据分析，覆盖 80% 场景
Q3 开放 API 平台，首月破 10 亿次
Q4 国际化启动，支持英文/西班牙语

功能使用：
数据分析 35%、实时监控 28%、告警通知 20%
报表导出 12%、自定义仪表盘 5%

工程：重构 50+ 模块，性能提升 40%
产品：12 个版本，满意度 4.8/5
设计：统一设计系统，200+ 组件
运营：4 场沙龙，覆盖 500+ 开发者

明年深化数据分析、拓展生态、全球化
```

### 2. Intake 直抽

```bash
cd C:\Users\Administrator\.workbuddy\skills\annual-report\scripts
D:\Python312\python.exe intake.py ..\..\loose-material.txt ..\..\draft.json
```

输出草稿 `draft.json`（含 `_hint`）。

### 3. Agent 复核补全

检查草稿，补充标题、副标题、强调色、caption、decimals、口径差异。

### 4. 生成报告

```bash
D:\Python312\python.exe generate.py ..\..\report-data.json ..\..\report.html
```

输出单文件 `report.html`（零外部依赖），可直接打开查看。

---

## 差异化卖点

| 卖点 | 说明 | 竞品 |
|------|------|------|
| **零依赖单文件** | 无 CDN、无 Chart.js、离线可开、单文件可邮件/托管 | `interactive-dashboard-builder` 用 jsDelivr CDN |
| **散材料 Intake** | 自动归类零散材料，不用填 JSON | 竞品要求 CSV/结构化输入 |
| **缺口智能建议** | 自动检测缺失项 + 附"如何获取" | 竞品不提供补全建议 |
| **有观点设计** | Sentry/PostHog 暗色仪表盘风，开箱即"哇" | 竞品是空白模板 |
| **内建交互** | 多期对比、悬停 tooltip、浅色主题、PDF 导出 | 竞品依赖外部库或缺失 |
| **无障碍内建** | reduced-motion 支持 | 竞品不考虑 |

---

## 文件结构

```
annual-report/
├── SKILL.md                    # 技能定义与使用说明（本文件）
├── templates/
│   ├── report-template.html    # 单文件零依赖模板（4 套布局预设）
│   ├── sample-data.json        # 完整样例（多期对比）
│   ├── sample-partial.json     # 稀疏样例（缺口检测）
│   └── sample-intake.txt       # Intake 散料样例
├── scripts/
│   ├── generate.py             # 数据 → HTML
│   ├── intake.py               # 散料 → 草稿（自然语言抽取）
│   └── verify.py               # Playwright 端到端自检
├── references/
│   ├── design-system.md        # 动效与无障碍说明
│   └── intake-examples.md      # Intake 真实样例
└── publish/                    # 发布素材包
    ├── cover.png               # 商店封面（2×2 四版式）
    ├── preview-{dashboard,magazine,poster,deck,light}.png
    └── LISTING.md              # 上架文案 + 发布指南
```

---

## 诚实的边界

- **Intake 是草稿生成器，不是"理解"引擎**：启发式对常规中文数字/同比/月份序列很准，但复杂表格、歧义表述仍需 agent 核对补全。
- **多期 `series` 要求各期等长**：长度不一致时不会智能对齐。
- **浅色主题环形图配色**：扇区用的是调色板原色，白底下对比度不如暗色理想（已做对比度安全重映射）。
- **"发布到市场"需用户本人操作**：技能可被本机 CodeBuddy 发现，但上架 cnb.cool 市场需用户授权登录。

---

## 后续优化方向

1. **自然语言 Intake 直通**：直接把聊天/表格文本喂给 agent，agent 自动生成 JSON（不需手动跑 intake.py）
2. **更多布局预设**：如「纸感印刷风」、「终端霓虹风」
3. **多期对比智能对齐**：当各序列长度不一致时按月份/季度对齐
4. **自动生成执行摘要**：从各区块提炼关键结论
