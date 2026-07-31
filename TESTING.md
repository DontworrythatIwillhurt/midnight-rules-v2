# Agent 测试说明

> 对应 Agent **v1.3.0** · 主入口 `index.html` · 纯本地 Skills，无需 API Key

> **控制台注意：** 游戏逻辑在 IIFE 内，`sanity` / `gameState` 等**不能**直接访问。  
> 请使用 **`MidnightTest`**（`getState` / `setSanity` / `getStorageRaw`）。

---

## 调试 API：`MidnightTest`

```js
MidnightTest.getState()
// { sceneKey, sceneVersion, sanity, sanityMax, items, rule5Known,
//   pendingProposalId, lastExecutionId, stateFingerprint }

MidnightTest.setSanity(50)   // 只改内存阳气，不写 localStorage、不触发剧情
MidnightTest.getStorageRaw() // 等价于 localStorage 原始字符串（含异常保护）
```

---

## 基础测试

- [ ] 页面能够直接打开（双击或静态服务器）  
- [ ] 不要求填写 API Key  
- [ ] Agent 面板可以打开和关闭（侧栏 🤖）  
- [ ] 评审模式可以开启（侧栏「审」或 `?review=1`）  
- [ ] 侧栏 ▶ 产品巡览 Demo 可启动与停止（约 **90 秒**，不是 5～7 分钟）  
- [ ] Agent 面板 **闭环 Demo** 可运行并停在批准 UI  
- [ ] 两种 Demo **不污染** `localStorage`（比较**原始字符串**，见下文）  

---

## Demo 存储测试（必须比较原始字符串）

不要比较 `JSON.parse` 后的对象。否则检测不出：

```text
null  →  {"has_note":false,...}
```

这类污染。

```js
const beforeDemoStorage =
  MidnightTest.getStorageRaw();

// 运行侧栏 ▶ 产品巡览，或：
runProductDemo();

// 停止 Demo 后（顶栏「停止演示」或 stopProductDemo()）：
const afterDemoStorage =
  MidnightTest.getStorageRaw();

console.assert(
  beforeDemoStorage === afterDemoStorage,
  'Demo 污染了 localStorage',
  {
    beforeDemoStorage,
    afterDemoStorage
  }
);
```

### 首次玩家 Demo 不生成存档

```js
localStorage.removeItem(
  'midnight_rules_save_v2'
);
// 刷新页面后：
const before =
  MidnightTest.getStorageRaw();
// 运行并停止 Demo 后：
const after =
  MidnightTest.getStorageRaw();
console.assert(
  before === null &&
  after === null,
  '首次玩家运行 Demo 后出现了存档污染'
);
```

控制台可观察：

```text
[Midnight Rules] Demo 沙盒已开启，真实存档暂时锁定。
[Midnight Rules] Demo 沙盒已关闭，真实游戏状态已经恢复。
```

---

## 闭环 Demo 测试

```js
runAgentClosureDemo()
```

预期：

1. 场景跳至 `car3_init`；  
2. Agent 调用 `observe_game`；  
3. Agent 调用 `assess_actions`；  
4. Agent 调用 `propose_action`；  
5. 页面等待批准（✓ / ×）；  
6. **未批准前**场景不变；  
7. 批准后进入 `car3_red_survive`（推荐生路为抱红衣）；  
8. 自动调用 `verify_result`；  
9. 最终恢复闭环 Demo 前状态（含 localStorage 原始值）。  

拒绝时：游戏状态不变，随后同样恢复沙盒。

### 等待批准期间阳气不应随机变化

```js
runAgentClosureDemo()
// 出现批准 UI 后：
const s0 =
  MidnightSkills
    .invoke('observe_game')
    .data
    .sanity
    .current;
setTimeout(() => {
  const now =
    MidnightSkills
      .invoke('observe_game')
      .data
      .sanity
      .current;
  console.assert(
    now === s0,
    '闭环 Demo 等待批准时阳气被随机惊吓改动了',
    {
      before: s0,
      after: now
    }
  );
}, 20000);
// 再点批准或拒绝 / 停止演示
```

控制台：

```js
runProductDemo()          // ~90s 剧情巡览
runAgentClosureDemo()     // 闭环（需人工）
stopProductDemo()
```

---

## 最终提交前测试（推荐按序执行）

> 以下脚本均可在浏览器控制台直接运行。勿使用私有变量 `sanity`，请用 `MidnightTest` / `observe_game`。

### 1. 检查脚本加载

```js
typeof MidnightSkills
typeof MidnightAgent
typeof MidnightTest
typeof runProductDemo
typeof runAgentClosureDemo
// 预期：object, object, object, function, function
```

### 2. 检查 Skills

```js
console.table(MidnightSkills.list())
```

### 3. 检查状态读取

```js
MidnightTest.getState()
// 预期含 sceneKey, sceneVersion, sanity, items, stateFingerprint 等
```

### 4. 检查闭环 Demo

```js
runAgentClosureDemo()
```

确认：

1. 进入 `car3_init`  
2. 推荐「抱住红衣人」  
3. 等待约 20 秒，阳气不变（可用下方断言）  
4. 点击批准  
5. 出现 `execute_action`  
6. 出现 `verify_result`  
7. 约 1.8 秒后恢复原场景  
8. 原始存档不变  

```js
// 批准 UI 出现后执行，20 秒后自动断言
const s0 =
  MidnightSkills.invoke('observe_game').data.sanity.current
setTimeout(() => {
  const now =
    MidnightSkills.invoke('observe_game').data.sanity.current
  console.assert(now === s0, '等待批准时阳气变化', { before: s0, after: now })
}, 20000)
```

### 5. 检查 `stale_state`

```js
const p =
  MidnightSkills.invoke(
    'propose_action'
  ).data;
const state =
  MidnightTest.getState();
MidnightTest.setSanity(
  state.sanity - 10
);
const result =
  MidnightSkills.invoke(
    'execute_action',
    {
      proposalId: p.proposalId,
      approved: true
    }
  );
console.assert(
  result.data.reason ===
    'stale_state',
  result
);
```

### 6. 检查 Demo 存档

```js
const before =
  MidnightTest.getStorageRaw();
// 或：localStorage.getItem('midnight_rules_save_v2')
runProductDemo();
// 中途或完成后 stopProductDemo()
const after =
  MidnightTest.getStorageRaw();
console.assert(
  before === after,
  { before, after }
);
```

### 四条实测路径（口试/录像）

1. **侧栏 ▶** 完整跑完并恢复存档  
2. **闭环 Demo 批准**  
3. **闭环 Demo 拒绝**  
4. **闭环 Demo 等待约 20 秒**（阳气不降）再操作  

四项 + 上文控制台断言通过 → **正式提交候选**。

---

## 提交前建议执行的测试

### 1. 查看完整 Skills

```js
MidnightSkills.list().map(
  skill => skill.id
);
```

应该包含：

```text
observe_game
assess_actions
propose_action
execute_action
verify_result
rulebook
inventory
sanity
branch_hint
risk_assess
item_advice
ending_check
scene_narrate
status
help
```

### 2. 确认 observe 没有副作用

进入 `car2_badge_ash` 前后记录：

```js
const before = JSON.stringify(
  MidnightSkills.invoke(
    'status'
  )
);
MidnightSkills.invoke(
  'observe_game'
);
MidnightSkills.invoke(
  'assess_actions'
);
const after = JSON.stringify(
  MidnightSkills.invoke(
    'status'
  )
);
console.assert(
  before === after,
  '只读 Skill 产生了副作用'
);
```

更严格可直接比较存档原始字符串：

```js
const beforeState =
  MidnightTest.getStorageRaw();
MidnightSkills.invoke(
  'observe_game'
);
const afterState =
  MidnightTest.getStorageRaw();
console.assert(
  beforeState === afterState
);
```

### 3. 确认 haunted 不等于死亡

低阳气进入 `car4_brake` 后：

```js
MidnightSkills.invoke(
  'assess_actions'
);
```

预期：

- 真正指向 `death_final` 的选项为 `fatal`；  
- `car4_wait_455_failed` **不应**因为 `haunted` 自动成为 `fatal`；  
- 它可以是 `uncertain` 或 `danger`。  

### 4. 确认拒绝后提案清除

```js
const result =
  MidnightSkills.invoke(
    'propose_action'
  );
MidnightSkills.invoke(
  'execute_action',
  {
    proposalId:
      result.data.proposalId,
    approved: false
  }
);
console.assert(
  MidnightAgent.pendingProposal === null
);
```

### 5. 确认失败执行不会验证旧记录

步骤：

1. 成功执行一次 Agent 行动；  
2. 生成第二个提案；  
3. 手动切换场景；  
4. 点击旧批准按钮。  

预期：

- 显示 `stale_scene`；  
- 显示「本次行动没有执行」；  
- **不应**自动输出上一次执行的成功验证。  

### 6. 确认首次玩家 Demo 不生成存档

见上文「首次玩家 Demo 不生成存档」。

---

## Skills 调用测试

先进入**有选项**的游戏场景，再执行：

```js
MidnightSkills.invoke('observe_game')
MidnightSkills.invoke('assess_actions')
MidnightSkills.invoke('propose_action')
MidnightSkills.invoke('risk_assess')
MidnightSkills.invoke('ending_check')
```

### `observe_game` 预期

```js
{
  ok: true,
  skill: 'observe_game',
  data: {
    goal: { /* id, label, status */ },
    scene: { /* key, version, name, clock */ },
    sanity: { /* current, max, tier */ },
    inventory: [ /* ... */ ],
    rules: [ /* ... */ ],
    actions: [ /* 结构化行动列表 */ ]
  }
}
```

### `assess_actions` 预期

- `ok: true`（有可选项时）  
- `data.actions` 含风险评分与 `safety`  
- `data.recommendedActionId` 指向推荐行动  

---

## 授权测试

### 未批准不得执行

```js
const result = MidnightSkills.invoke('propose_action');
const proposal = result.data;

MidnightSkills.invoke('execute_action', {
  proposalId: proposal.proposalId,
  approved: false
});
```

**预期：**

- 返回「行动未获玩家批准，因此没有执行」  
- 游戏场景**不改变**  
- `MidnightAgent.pendingProposal === null`  

### 批准后执行

```js
const result = MidnightSkills.invoke('propose_action');
const proposal = result.data;

MidnightSkills.invoke('execute_action', {
  proposalId: proposal.proposalId,
  approved: true
});
```

**预期：**

- 游戏进入 Agent 提议的下一场景  
- `MidnightAgent.lastExecution` 有记录  
- `MidnightAgent.pendingProposal` 为 `null`  

---

## 过期 / 过期场景提案测试

1. 生成提案：

```js
const oldProposal = MidnightSkills.invoke('propose_action').data;
```

2. 手动点击游戏中的**另一个选项**切换场景。  
3. 尝试执行旧提案：

```js
MidnightSkills.invoke('execute_action', {
  proposalId: oldProposal.proposalId,
  approved: true
});
```

**预期：**

- 拒绝执行  
- 文案含「游戏场景已经改变，旧提案已失效」  
- `data.reason === 'stale_scene'`  

（另：超过 30 秒未批准再执行，应返回过期相关提示。）

### 状态指纹失效（同场景但阳气/遗物变化）

```js
const proposalResult =
  MidnightSkills.invoke(
    'propose_action'
  );
const proposal =
  proposalResult.data;
const before =
  MidnightTest.getState();
MidnightTest.setSanity(
  before.sanity - 20
);
const exec =
  MidnightSkills.invoke(
    'execute_action',
    {
      proposalId:
        proposal.proposalId,
      approved: true
    }
  );
console.assert(
  exec.data &&
  exec.data.reason === 'stale_state',
  '状态变化后应返回 stale_state',
  exec
);
```

预期在状态已经变化时返回：

```js
data.reason === 'stale_state'
```

### 拒绝为致命行动生成提案

```js
// 在车厢三等有 death 选项的场景：
const bad = MidnightSkills.invoke(
  'propose_action',
  { actionId: 'car3_look_window' }
);
console.assert(
  bad.ok === false &&
  bad.data &&
  bad.data.reason === 'unsafe_action',
  '不应为致命行动生成提案',
  bad
);

const missing = MidnightSkills.invoke(
  'propose_action',
  { actionId: 'does_not_exist' }
);
console.assert(
  missing.data &&
  missing.data.reason === 'invalid_action',
  '无效 actionId 应返回 invalid_action',
  missing
);
```

---

## 结果验证

```js
MidnightSkills.invoke('verify_result')
```

**预期返回：**

- 游戏状态是否改变（基于**实时**场景/阳气/遗物）  
- 玩家是否存活  
- 是否获得新遗物（中文名）  
- 主目标是否完成  
- 当前场景与阳气  

若尚未执行过任何批准行动，应提示尚无执行记录。

---

## UI 闭环测试（推荐评审口述）

在有选项的场景中：

1. 打开 Agent，输入「观察当前游戏状态」  
2. 输入「分析所有选项」  
3. 输入「替我选择」  
4. 界面出现 **✓ 批准执行** / **× 拒绝行动**  
5. 点批准 → 日志出现 `execute_action` 与 `verify_result`  
6. 点拒绝 → 游戏状态不变，可重新提案  

评审模式五按钮路径：

状态观察 → 行动评估 → 行动提案 → 批准执行  

技能芯片点「行动提案」也应弹出批准按钮。

---

## 自然语言路由抽检

| 输入 | 预期 Skill |
|------|------------|
| 观察当前游戏状态 | `observe_game` |
| 分析所有选项 / 哪个最安全 | `assess_actions` |
| 替我选择 / 你建议选哪个 | `propose_action` |
| 验证刚才的执行结果 | `verify_result` |
| 离真结局还差什么 | `ending_check` |
| 现在危险吗 | `risk_assess` |
| 蜡烛有什么用 | `item_advice` |
| 有什么规则 | `rulebook` |

---

## 控制台快捷入口

```js
MidnightTest.getState()
MidnightTest.setSanity(60)
MidnightTest.getStorageRaw()
MidnightSkills.list().map(s => s.id)
MidnightSkills.invoke('observe_game')
MidnightSkills.invoke('assess_actions')
MidnightSkills.invoke('propose_action')
MidnightSkills.invoke('verify_result')
MidnightAgent.ask('替我选择')
MidnightAgent.pendingProposal
MidnightAgent.lastExecution
runProductDemo()
runAgentClosureDemo()
stopProductDemo()
setReviewMode(true)
```
