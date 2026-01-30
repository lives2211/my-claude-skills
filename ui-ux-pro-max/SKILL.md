---
name: ui-ux-pro-max
description: AI-powered design intelligence with 50+ styles, 95+ color palettes, and automated design system generation
---

# UI UX Pro Max

AI 驱动的设计智能系统，提供 50+ 设计风格、95+ 颜色调色板、57 种字体组合。

## 脚本路径

```
D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py
```

---

## 快速使用

### 1. 生成设计系统（最常用）

```bash
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "<产品类型> <行业> <关键词>" --design-system -p "项目名称"
```

**示例：**
```bash
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "saas dashboard modern" --design-system -p "MyApp"
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "beauty spa wellness" --design-system -p "Spa"
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "fintech crypto dark" --design-system -p "CryptoApp"
```

### 2. 保存设计系统

添加 `--persist` 保存到项目：

```bash
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "<查询>" --design-system --persist -p "项目名称"
```

### 3. 搜索特定领域

```bash
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "<关键词>" --domain <领域>
```

| 领域 | 用途 | 示例 |
|------|------|------|
| `style` | UI 风格 | `--domain style "glassmorphism dark"` |
| `color` | 颜色 | `--domain color "fintech"` |
| `typography` | 字体 | `--domain typography "elegant"` |
| `chart` | 图表 | `--domain chart "dashboard"` |
| `ux` | UX指南 | `--domain ux "animation"` |
| `landing` | 落地页 | `--domain landing "hero"` |

### 4. 技术栈指南

```bash
python "D:\Antigravity\.agent\skills\ui-ux-pro-max\scripts\search.py" "<关键词>" --stack <技术栈>
```

**可用技术栈：** `html-tailwind`(默认), `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## 工作流程

1. **分析需求** - 提取产品类型、风格、行业
2. **生成设计系统** - 使用 `--design-system` 获取完整推荐
3. **补充搜索** - 使用 `--domain` 获取更多细节
4. **技术栈指南** - 使用 `--stack` 获取实现指南
5. **实现设计** - 综合结果开始编码

---

## 专业 UI 规则

| 规则 | ✅ 正确 | ❌ 错误 |
|------|---------|---------|
| 图标 | SVG (Heroicons, Lucide) | Emoji 🎨 🚀 |
| 悬停 | 颜色/透明度过渡 | 缩放导致偏移 |
| 光标 | 可点击元素 `cursor-pointer` | 默认光标 |
| 浅色模式 | `bg-white/80` | `bg-white/10` |
