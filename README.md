# Midnight Rules（午夜规则）

> 全球青年培育赛 · 数字文化赛道（AI + 文娱）参赛作品  
> **第三轮形态：可运行怪谈体验 + 检票口守则智能体（Agent）+ Skills**

---

## 🎮 在线演示
[
| 渠道 | 链接 | 备注 |
|------|------|------|
(https://dontworrythatiwillhurt.github.io/midnight-rules-v2/)

### 本地运行

1. 打开目录，确认存在：`index.html`、`bgm_ghost_bride.mp3`（推荐）  
2. 双击 `index.html`，或用任意静态服务器托管本目录  
3. 点击 **「上车」** → 将 **音频** 设为开  

---

## 🤖 Agent + Skills（评测入口）

| 操作 | 说明 |
|------|------|
| 侧栏 **🤖** | 打开「检票口·守则智能体」 |
| 侧栏 **▶** | **一键产品 Demo**（带 Specs 能力标签 + 步骤进度 + 可停止） |
| 侧栏 **审** | **评审模式**（四按钮核心能力 + Trace） |
| 输入框 | 自然语言：结局差什么 / 危险吗 / 蜡烛有什么用 / 规则 / 阳气… |
| 技能芯片 | 一键 `invoke`（含 risk_assess / ending_check / item_advice） |
| Trace | 面板内显示：意图 · 技能 · 场景 · 信心 |

控制台可调：

```js
MidnightSkills.invoke('ending_check')
MidnightSkills.invoke('risk_assess', { sceneKey: 'car3_init' })
MidnightAgent.ask('离真结局还差什么')
runProductDemo()
stopProductDemo()
setReviewMode(true)
```

> Agent **纯本地 Skills**，不调用外部 API，无密钥泄露/反代薅羊毛风险。

完整评测说明见 **[SPECS.md](./SPECS.md)**。

---

## 🎯 用户价值（一句话）

在中式规则怪谈的地铁末班车里，用 **可验证的禁忌、遗物与阳气** 做生存博弈，并用 **智能体 Skills** 把复杂状态讲清楚——既沉浸宣泄，又演示 AI 文娱交互。

---

## 🛠️ 技术要点

1. **HTML5 全屏 VN**：场景图/滤镜/氛围层随节点切换  
2. **Web Audio +《鬼新娘》BGM**：环境合成 + 成曲循环（mp3 优先，兼容手机）  
3. **状态机**：死亡边界、限时抉择、真结局条件（线索 + 阳气）  
4. **Agent Skills**：`rulebook` / `inventory` / `sanity` / `branch_hint` / `risk_assess` / `item_advice` / `ending_check` / `scene_narrate` / `status` / `help`；主动护航（低阳气/获道具/入高危场景自动提示）；评审模式（`?review=1`）

---

## 📦 交付检查（第三轮）

- [ ] 打开线上链接可玩（Netlify 或 GitHub **双层路径**）  
- [ ] ▶ Demo **2–3 分钟**关键路径跑通（生路标绿 + 女学生结局）  
- [ ] 🤖 问答与 Skill 芯片可用  
- [ ] 音频在用户点击后可播放（同目录 `bgm_ghost_bride.mp3`）  
- [ ] 手机竖屏：对话框/场景名完整、无方块乱码  
- [ ] 对照 [SPECS.md](./SPECS.md) 自检表全部勾选  

---

## 📁 主要文件

| 文件 | 作用 |
|------|------|
| `index.html` | 游戏 + Agent + Skills 全部逻辑 |
| `SPECS.md` | 评测规格与 Demo 路径 |
| `bgm_ghost_bride.mp3` | 背景音乐（务必与页面同目录部署） |
| `red_girl_*.png` 等 | 真结局女学生与关键场景图 |
