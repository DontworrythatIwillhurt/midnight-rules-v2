# 午夜规则 · Specs 评测说明（Agent v1.3.0）

> 产品形态：**可运行的规则怪谈互动体验 + 检票口守则智能体（Agent）+ 可点名 Skills + 人类批准行动闭环**  
> 主入口文件：`index.html`（单页交付，无构建步骤）  
> 测试说明：[TESTING.md](./TESTING.md) · 项目说明：[README.md](./README.md)

---

## 1. 交付物清单

| 项 | 路径 / 说明 |
|----|-------------|
| 可运行产品 | `index.html` + 同目录资源（图/音频） |
| Agent | 界面 🤖「检票口·守则智能体」；`window.MidnightAgent`（version **1.3.0**） |
| Skills | `window.MidnightSkills`（见下表） |
| 产品巡览 Demo | 侧栏 `▶`；`window.runProductDemo()`（约 90 秒自动剧情，**沙盒隔离**） |
| **闭环 Demo** | Agent 面板「闭环 Demo」；`window.runAgentClosureDemo()`（观察→评估→提案→**人类批准**→执行→验证） |
| 测试文档 | [TESTING.md](./TESTING.md) |
| 在线演示 | GitHub Pages v2：https://dontworrythatiwillhurt.github.io/midnight-rules-v2/ |
| 备用 | Netlify：https://kaleidoscopic-tapioca-61193c.netlify.app/ |

---

## 2. Agent 规格

| 字段 | 内容 |
|------|------|
| 名称 | 检票口·守则智能体 |
| 版本 | **1.3.0** |
| 角色 | 观察状态、评估风险、提出方案；**须玩家批准后**才执行选项 |
| 交互方式 | 自然语言（中文关键词路由）+ 技能芯片 + 评审按钮 + 批准/拒绝 UI |
| 运行约束 | **纯前端、可离线**；不依赖外部大模型 API |
| 可观测性 | 对话区 `Skill · xxx`；Trace（意图/场景/信心）；`MidnightAgent.history` |
| 提案状态 | `MidnightAgent.pendingProposal` / `lastExecution` / `goal` |
| 场景版本 | 全局 `sceneVersion`，提案绑定版本，防过期执行 |

### Agent 工作闭环

```text
观察游戏状态 (observe_game)
→ 评估候选行动 (assess_actions)
→ 提出可解释方案 (propose_action)
→ 等待玩家批准（Human-in-the-loop）
→ 执行行动 (execute_action)
→ 验证结果 (verify_result)
→ 更新下一步计划 (branch_hint 等)
```

### 示例问法

| 问法 | Skill |
|------|--------|
| 「观察当前游戏状态」 | `observe_game` |
| 「分析所有选项」/「哪个最安全」 | `assess_actions` |
| 「替我选择」/「你建议选哪个」 | `propose_action` |
| 「验证刚才的执行结果」 | `verify_result` |
| 「有什么规则」 | `rulebook` |
| 「阳气多少」 | `sanity` |
| 「我有什么道具」 | `inventory` |
| 「现在怎么选」 | `branch_hint` |
| 「现在危险吗」 | `risk_assess` |
| 「蜡烛有什么用」 | `item_advice` |
| 「离真结局还差什么」 | `ending_check` |
| 「旁白一下」 | `scene_narrate` |
| 「列车状态」 | `status` |
| 「帮助」 | `help` |

---

## 3. Skills 规格

| Skill ID | 名称 | 输入 | 输出 | 副作用 |
|----------|------|------|------|--------|
| `observe_game` | **状态观察** | 无 | 场景/阳气/遗物/守则/结构化行动 | 无 |
| `assess_actions` | **行动评估** | 无 | 全部选项风险排序与推荐 | 无 |
| `propose_action` | **行动提案** | `actionId?` | 待批准提案（30 秒有效） | 写入 `pendingProposal` |
| `execute_action` | **执行行动** | `{ proposalId, approved }` | 执行结果 / 拒绝原因 | **须批准**；可能切场景 |
| `verify_result` | **结果验证** | 无 | 场景变化/存活/遗物/目标 | 无 |
| `help` | 能力说明 | 无 | 技能列表与闭环示例 | 无 |
| `rulebook` | 守则查询 | 无 | 已解锁/未解锁规则 | 无 |
| `inventory` | 遗物清单 | 无 | 持有/未持有道具 | 无 |
| `sanity` | 阳气诊断 | 无 | 数值、档位、建议 | 无 |
| `branch_hint` | 抉择提示 | 当前场景 | 生存向轻度提示 | 无 |
| `risk_assess` | 场景风险 | `sceneKey?` | 风险等级/推荐动作 | 无 |
| `item_advice` | 道具参谋 | `itemId?` | 遗物可规避死法 | 无 |
| `ending_check` | 结局诊断 | 全局状态 | 真结局缺口 | 无 |
| `scene_narrate` | 场景旁白 | 当前场景 | 氛围旁白 | 无 |
| `status` | 列车状态 | 全局存档 | 死亡/成就/遗物进度 | 无 |

统一调用：

```js
MidnightSkills.invoke('observe_game')
MidnightSkills.invoke('assess_actions')
MidnightSkills.invoke('propose_action')
MidnightSkills.invoke('execute_action', { proposalId, approved: true })
MidnightSkills.invoke('verify_result')
MidnightSkills.invoke('risk_assess', { sceneKey: 'car3_darkness' })
MidnightSkills.invoke('item_advice', { itemId: 'has_candle' })
MidnightSkills.invoke('ending_check')
MidnightAgent.ask('替我选择')
// → { reply, skillResult, trace }
// trace: intent / skill / at(scene) / confidence / args
```

### 评测调试 API（控制台）

游戏主逻辑在 IIFE 内，私有变量不可直接访问。评测请用：

```js
MidnightTest.getState()      // sceneKey / sanity / stateFingerprint / ...
MidnightTest.setSanity(50)   // 只改内存阳气，不写 localStorage
MidnightTest.getStorageRaw() // 存档原始字符串
runAgentClosureDemo()
runProductDemo()
stopProductDemo()
```

### 人类授权与安全

| 规则 | 说明 |
|------|------|
| 默认不执行 | `propose_action` 只提案，不改状态 |
| 明确批准 | `execute_action` 要求 `approved === true` |
| 场景版本 | `proposal.sceneVersion === sceneVersion`，否则 `stale_scene` |
| 状态指纹 | 提案绑定场景、阳气、遗物和关键规则；状态变化时返回 `stale_state` |
| 过期 | 提案 30 秒后失效 |
| 行动仍存在 | 执行前重新读取 `getCurrentAgentActions()` 校验 |
| 失败不误验 | 执行失败时**不**调用 `verify_result`（避免读上一次成功记录） |
| 实时验证 | `verify_result` 读取当前场景/阳气/遗物，而非仅执行瞬间快照 |

### 只读 Skills 不修改状态

以下 Skill **禁止**写入 `gameState` / `localStorage` / 场景：

| 只读 | 说明 |
|------|------|
| `observe_game` | 调用 `node.options()` 仅读取；不触发 unlock |
| `assess_actions` | 同上 |
| `propose_action` | 只写 `pendingProposal` 内存提案，不改游戏进度 |
| `verify_result` / `rulebook` / `inventory` / `sanity` / `branch_hint` / `risk_assess` / `item_advice` / `ending_check` / `scene_narrate` / `status` / `help` | 查询与诊断 |

规则五解锁在 **`car2_badge_ash.text()`** 进入场景时发生，**不在** `options()` 中，保证 observe/assess 无副作用。

### 结构化选项字段（STORY_NODES）

关键节点已逐步写入：

| 字段 | 含义 |
|------|------|
| `id` | 稳定 actionId，供提案绑定 |
| `safe` | 剧情语义是否为生路（与 `safety` 风险档位独立） |
| `risk` | 0–100 风险分 |
| `tags` | 语义标签 |
| `reasons` | 可解释依据（Agent 直接展示） |
| `haunted` | 阳气过低时的**幻觉干扰**（UI 标记） |
| `act` | 点击副作用（如扣阳气） |

**`haunted` 不等于死亡。** `isDeathTarget` 仅当 `next`/`event` 以 `death` 开头时判定为 fatal。低阳气模糊真结局项（如 `car4_wait_455_failed`）可为 `danger`/`uncertain`，不得因 `haunted` 被标成 fatal。

未标注字段的旧选项仍兼容：由 `getCurrentAgentActions` 根据 `next`/`safe`/`risk` 推断（`haunted` 可提高风险分，但不强制 100）。

### Agent 主动护航（非查询）

| 触发 | 行为 |
|------|------|
| 阳气跌破 30 / 45 | 主动提示危险与回阳 |
| 获得关键遗物 | 主动说明用法与规避 |
| 进入 car2 / car3 / 无光 / car4 | 主动一句风险摘要 |
| Demo 恢复中 | `demoIsolationActive` 时**不**触发护航 |

### 评审模式

- 侧栏 **审** 或 URL `?review=1`
- 按钮：**状态观察** / **行动评估** / **行动提案** / **规则检索** / **结局诊断**
- 行动提案会弹出批准/拒绝 UI
- 默认展开 Trace  
- **Demo 与评审模式下随机惊吓暂停**（含耳语 `applySanity(-3)`；`demoRunning` / `demoIsolationActive` / `review-mode` / `suppressSceneStateEffects` 均拦截）

### 提案失效原因（`execute_action`）

| reason | 含义 |
|--------|------|
| `not_approved` | 未 `approved: true` |
| `missing_proposal` | 无待批准提案 |
| `proposal_mismatch` | proposalId 不匹配 |
| `stale_scene` | 场景键或 `sceneVersion` 已变 |
| **`stale_state`** | **状态指纹**变化（阳气 / 遗物 / rule5 等），须重新观察与提案 |
| `expired` | 超过 30 秒 |
| `action_unavailable` | 行动已不在当前选项中 |
| `invalid_action` | 指定的 `actionId` 在当前场景不存在（`propose_action`） |
| `unsafe_action` | Agent 拒绝为明确致死行动（`safety === fatal` 或 `risk ≥ 90`）生成提案 |

---

## 4. 用户价值（评审口述要点）

1. **情绪价值**：在可控的规则怪谈中释放学业/工作压力，而非无意义惊吓堆砌。  
2. **文化价值**：中式「守则 / 禁忌 / 红白意象 / 末班地铁」符号化表达。  
3. **机制价值**：「规则—道具—心神」三重状态机；真结局要求线索 + 阳气 ≥ 45。  
4. **智能体价值**：从「查询助手」升级为 **观察—评估—提案—人类批准—执行—验证** 的可演示 Agent 闭环。  

---

## 5. 一键产品巡览（约 90 秒）

> 侧栏 **▶** · `runProductDemo()` · 累计等待约 **89 秒**（不是 5～7 分钟）

1. 打开页面 → 点「上车」→ 确认「音频: 开」。  
2. 点侧栏 **▶**。  
3. 观察：  
   - 顶栏「演示模式」横幅；  
   - Agent 依次调用 Skills 与场景链（站台 → 烛 → 守则 → 车厢一纸条 → 工牌 → 化灰 → 车厢三 → 红衣 → 无光/蜡烛 → 制动阀生路标绿 → 真结局 → 尾声）；  
   - 演示中正文无侵蚀乱码、无随机插曲。  
4. 演示结束/停止后：真实 `localStorage` **原始字符串**与演示前完全一致（含原本为 `null`）。  
5. 同时恢复：场景版本、`runRNG` 内部状态、`usedInterludes`、`glitchedRuleId`、Trace、音频（合成层与成曲 BGM 可独立恢复）。  
6. 控制台：`stopProductDemo()` 可中止。  

### Agent 闭环 Demo（约 20–40 秒，取决于评委批准时间）

> Agent 面板 **「闭环 Demo」** · `runAgentClosureDemo()`

1. 点击「上车」；  
2. 打开 🤖 Agent；  
3. 点击「闭环 Demo」；  
4. Agent 依次调用：  
   - `observe_game`  
   - `assess_actions`  
   - `propose_action`  
5. 页面暂停并等待评委选择：  
   - 「✓ 批准执行」  
   - 「× 拒绝行动」  
6. 批准后调用：  
   - `execute_action`  
   - `verify_result`  
7. 拒绝后不改变游戏状态；  
8. 演示结束后恢复原始存档、场景与音频状态。  

沙盒细节：跳到 `car3_init`（纸条+工牌、阳气充足；**不**启动 8 秒死亡倒计时）；批准后通常进入 `car3_red_survive`。

### 人工游玩抽检（可选 3–5 分钟）

站台取烛 → 车厢一摸纸条 → 工牌化解乘务员 → 车厢三抱红衣/蜡烛过无光 → 车厢四拒拉阀（阳气 ≥ 45）→ 女学生真结局。

### 自由闭环抽检

有选项的场景 → 「审」→ 状态观察 → 行动评估 → 行动提案 → 批准执行 → 查看 `verify_result`。

### 交互可观测点（C）

| 机制 | 表现 |
|------|------|
| 生路高亮 | Demo/导览时非死亡选项带绿色「生路」角标 |
| 抉择反馈 | 点击后顶部 toast：安全 / 大凶 |
| 限时抉择 | 车厢三原 8 秒；Demo 中暂停倒计时 |
| 人类批准 | 提案后出现 ✓ 批准 / × 拒绝 |
| 心神门槛 | 真结局选项需阳气 ≥ 45，不足则模糊/扣阳 |
| Demo 沙盒 | 演示期间 `saveGame` 不写真实存档 |

---

## 6. 运行与边界

| 项 | 说明 |
|----|------|
| 浏览器 | Chrome / Edge / Safari 最新版 |
| 本地打开 | `index.html` 与 `bgm_ghost_bride.mp3` 同目录；须点击后播音频 |
| 手机 | 竖屏已适配；允许缩放；BGM 请用 mp3 |
| 存档 | `localStorage` 键 `midnight_rules_save_v2` |
| Demo 副作用 | **无**真实写入；结束后恢复快照 |

---

## 7. Specs 自检表（提交前勾选）

- [ ] 线上链接可打开且为正确路径  
- [ ] 上车后音频可开  
- [ ] 🤖 Agent 可打开、可输入、有回复  
- [ ] 芯片可调用全部 Skills（含 observe / assess / propose / verify）  
- [ ] 闭环：提案 → 批准 → 执行 → 验证  
- [ ] 未批准时场景不变；切场后旧提案失效  
- [ ] ▶ 产品巡览（~90s）可完整跑完且 **不污染** 存档（原始字符串一致）  
- [ ] 「闭环 Demo」（20–40s）可等待批准并恢复原状态  
- [ ] 正文无「方块乱码」；手机竖屏可用  
- [ ] 真结局条件可讲清（纸条 + 工牌 + 阳气 ≥ 45 + 拒拉阀）  
- [ ] README / SPECS / TESTING 链接与版本一致  

---

## 8. 能力演进摘要

| 方向 | 已实现 |
|------|--------|
| **C 交互深度** | 生路高亮、抉择 toast、限时机制、人类批准闭环、结构化行动 |
| **F 视听打磨** | 女学生真结局、关键场景底图、BGM 多格式、无障碍侧栏 button |
| **Agent 升级** | v1.3.0 观察/评估/提案/执行/验证；场景版本；Demo 沙盒；评审五按钮；Trace |

---

*版本：Agent Skills **v1.3.0** · 与 `index.html` 内 `MidnightAgent.version` 对齐*
