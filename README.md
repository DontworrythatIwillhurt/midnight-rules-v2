# 午夜规则 Midnight Rules

> 全球青年培育赛 · 数字文化赛道（AI + 文娱）参赛作品  
> **可运行规则怪谈 + 检票口守则智能体（Agent v1.3.0）+ 可编排 Skills**

---

## 项目简介

《午夜规则》是一款规则怪谈交互游戏，内置一个**完全本地运行**的守则智能体。

智能体能够读取当前场景、阳气、遗物、守则、游戏选项和结局条件，并编排多个 Skills，为玩家提供：

- 规则检索  
- 行动风险评估  
- 道具参谋  
- 结局诊断  
- 主动风险预警  
- **观察 → 评估 → 提案 → 人类批准 → 执行 → 验证** 的完整行动闭环  

---

## Agent 目标

帮助玩家：

1. 理解午夜乘客守则；  
2. 识别高风险选项；  
3. 管理阳气和关键遗物；  
4. 识别紧急制动阀诱饵；  
5. 存活到 4:55；  
6. 达成真结局。  

---

## Agent 工作闭环

```text
观察游戏状态
→ 评估候选行动
→ 提出可解释方案
→ 等待玩家批准
→ 调用行动 Skill
→ 改变游戏状态
→ 验证执行结果
→ 更新下一步计划
```

### Skills

| Skill | 作用 |
|-------|------|
| `observe_game` | 读取场景、阳气、遗物、规则与可执行行动 |
| `assess_actions` | 评估当前全部选项的风险 |
| `propose_action` | 生成低风险行动提案 |
| `execute_action` | 在玩家批准后执行行动 |
| `verify_result` | 验证执行后的场景和生存状态 |
| `rulebook` | 查询已知守则 |
| `inventory` | 查询遗物 |
| `sanity` | 诊断阳气状态 |
| `branch_hint` | 基于规则给出当前节点生存提示 |
| `risk_assess` | 评估当前场景风险 |
| `item_advice` | 分析遗物用途 |
| `ending_check` | 检查真结局条件 |
| `scene_narrate` | 根据场景状态生成旁白 |
| `status` | 输出整体进度 |
| `help` | 列出全部 Skills 与示例问法 |

---

## 人类授权机制

**Agent 不会未经允许自动改变游戏状态。**

执行流程：

1. Agent 调用 `propose_action`；  
2. 页面显示行动、风险和依据；  
3. 用户选择「✓ 批准执行」或「× 拒绝行动」；  
4. 只有获得明确批准后，Agent 才会调用 `execute_action`；  
5. 执行后自动调用 `verify_result`。  

额外保护：

- 提案绑定 **场景版本**，切场后旧提案返回 `stale_scene`；  
- 提案绑定 **状态指纹**，阳气、遗物或关键规则变化后返回 `stale_state`；  
- 提案有效期 **30 秒**；  
- 执行前重新读取当前行动，确保行动仍然存在；  
- 未 `approved: true` 时绝不执行；  
- 执行失败时不会错误验证上一次成功记录；  
- Agent **不为**明确致死行动（`risk ≥ 90` / `fatal`）生成可批准提案（`unsafe_action`）。  

---

## 在线体验

| 渠道 | 链接 | 备注 |
|------|------|------|
| **GitHub Pages（v2）** | https://dontworrythatiwillhurt.github.io/midnight-rules-v2/ | 主演示（本仓库形态） |
| **Netlify** | https://kaleidoscopic-tapioca-61193c.netlify.app/ | 备用 |
| **GitHub Pages（旧路径）** | https://dontworrythatiwillhurt.github.io/midnight-rules/midnight-rules/ | 须两层路径，少一层会 404 |

### 本地运行

1. 打开目录，确认存在：`index.html`、`bgm_ghost_bride.mp3`（推荐）  
2. 双击 `index.html`，或用任意静态服务器托管本目录  
3. 点击 **「上车」** → 将 **音频** 设为开  

---

## 推荐评审流程

### 最快闭环评审

1. 点击「上车」；  
2. 打开 🤖 Agent；  
3. 点击「闭环 Demo」；  
4. 查看 `observe_game` 与 `assess_actions`；  
5. 点击「批准执行」或「拒绝行动」；  
6. 查看 `execute_action` 与 `verify_result`；  
7. Demo 结束后自动恢复原状态。  

侧栏 **▶** 为约 **90 秒**的完整产品巡览（不是 5～7 分钟）。

**提交前四条路径：** ① ▶ 跑通并恢复存档 ② 闭环批准 ③ 闭环拒绝 ④ 闭环等待 20 秒确认阳气不随机下降。

### 评审模式按钮路径

1. 点击「上车」；  
2. 点击侧栏 **「审」** 进入评审模式（或 URL 加 `?review=1`）；  
3. 点击 **「状态观察」**；  
4. 点击 **「行动评估」**；  
5. 点击 **「行动提案」**；  
6. 点击 **「批准执行」**；  
7. 查看 `execute_action` 和 `verify_result` 日志。  

也可以在 Agent 输入框中输入：

```text
观察当前游戏状态
分析所有选项
替我选择
验证刚才的执行结果
离真结局还差什么
```

侧栏其它入口：

| 操作 | 说明 |
|------|------|
| **🤖** | 打开检票口·守则智能体 |
| **▶** | **产品巡览**（约 90 秒自动剧情，沙盒隔离） |
| Agent 面板 **闭环 Demo** | **观察→评估→提案→评委批准→执行→验证**（约 20–40 秒，含等待批准） |
| **审** | 评审模式 + Trace |
| 技能芯片 | 一键 `invoke` 全部 Skills |

控制台：

```js
MidnightTest.getState()           // 场景/阳气/指纹（评测用）
MidnightTest.setSanity(50)        // 测 stale_state，不写存档
MidnightSkills.invoke('observe_game')
MidnightSkills.invoke('assess_actions')
MidnightSkills.invoke('propose_action')
MidnightSkills.invoke('ending_check')
MidnightAgent.ask('替我选择')
runProductDemo()          // 侧栏 ▶ 产品巡览（~90s）
runAgentClosureDemo()     // Agent 闭环 Demo（需人工批准）
stopProductDemo()
setReviewMode(true)
```

更完整的验收用例见 **[TESTING.md](./TESTING.md)**；评测规格见 **[SPECS.md](./SPECS.md)**。

---

## Demo 沙盒

一键 Demo 运行在**临时状态**中，不会修改玩家真实：

- 存档（`localStorage`）  
- 道具  
- 成就  
- 死亡次数  
- 通关次数  
- 规则解锁状态  

停止 Demo 后自动恢复演示前的真实进度。

---

## 技术架构

```text
玩家
  ↓
游戏 UI
  ↓
MidnightAgent
  ├─ 意图路由
  ├─ 持续任务目标
  ├─ 待批准提案
  └─ 执行历史
  ↓
MidnightSkills
  ├─ observe_game
  ├─ assess_actions
  ├─ propose_action
  ├─ execute_action
  ├─ verify_result
  ├─ rulebook / inventory / sanity
  ├─ risk_assess / item_advice / ending_check
  └─ scene_narrate / status / help / branch_hint
  ↓
STORY_NODES / gameState / localStorage
```

### 实现说明

- 当前 Agent 为**本地规则驱动智能体**，不依赖外部 API Key，可在 GitHub Pages 中直接运行。  
- 自然语言入口使用轻量意图路由；核心决策基于结构化游戏状态、守则、阳气、道具和场景选项。  
- 单文件交付：`index.html`（含样式与逻辑），无构建步骤。  

### 其它技术要点

1. HTML5 全屏 VN：场景图 / 滤镜 / 氛围层随节点切换  
2. Web Audio +《鬼新娘》BGM（mp3 优先，兼容手机）  
3. 状态机：死亡边界、限时抉择、真结局条件（线索 + 阳气 ≥ 45）  

---

## 交付检查

- [ ] 线上链接可打开  
- [ ] ▶ 产品巡览（~90s）可跑通且**不污染** `localStorage`（比较原始字符串）  
- [ ] 「闭环 Demo」可停在批准 UI，批准/拒绝后恢复原状态  
- [ ] 🤖 可问答；芯片与评审按钮可用  
- [ ] 闭环：观察 → 评估 → 提案 → 批准 → 执行 → 验证  
- [ ] 音频在用户点击后可播放  
- [ ] 手机竖屏：对话框完整、可缩放  
- [ ] 对照 [SPECS.md](./SPECS.md) / [TESTING.md](./TESTING.md)  

---

## 主要文件

| 文件 | 作用 |
|------|------|
| `index.html` | 游戏 + Agent + Skills 全部逻辑 |
| `README.md` | 项目说明（本文） |
| `SPECS.md` | 评测规格与 Demo 路径 |
| `TESTING.md` | Agent 测试说明 |
| `bgm_ghost_bride.mp3` | 背景音乐（与页面同目录部署） |
| `red_girl_*.png` 等 | 真结局与关键场景图 |

---

## 定位

本项目已从「游戏中的规则查询助手」升级为：

> **能够观察游戏、评估行动、提出计划、等待人类批准、执行行动并验证结果的交互式游戏 Agent。**
