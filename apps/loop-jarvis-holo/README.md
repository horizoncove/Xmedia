# LOOP JARVIS · Holographic Command Core

基于开源全息 HUD 改造的 **LOOP PARK 值班中枢** 前端。

## 来源与许可

- 视觉与交互骨架来自 [LeiQingliang/J.A.R.V.I.S.-Holographic-Interface](https://github.com/LeiQingliang/J.A.R.V.I.S.-Holographic-Interface)（MIT）
- 官方仓当前缺 `components/` / `services/`；本目录以完整镜像 [xxjun9527/jarvis-holographic](https://github.com/xxjun9527/jarvis-holographic) 为可运行底本
- 保留上游 `LICENSE`；LOOP 侧仅做品牌与值班中枢场景适配

## 能力

- 摄像头背景 + MediaPipe 手势（旋转地球 / 捏合切换战术地形 / 情报面板）
- 3D 全息地球与战术地形（R3F + drei + postprocessing）
- HUD 叠层、声效、语音唤醒与 LLM 对话（可选 DeepSeek 兼容接口）
- 高德地图视图（可选 Key）

## 启动

```bash
cd apps/loop-jarvis-holo
cp .env.example .env.local   # 按需填 LLM / 高德；可不填，界面仍可启动
npm install
npm run dev                  # http://127.0.0.1:3000
```

浏览器需允许摄像头；手势与语音依赖本机权限。Cloud Agent 环境可能无摄像头，仍可看引导屏与 HUD 壳。

## 与本仓其它原型的关系

| 路径 | 角色 |
| --- | --- |
| `apps/loop-jarvis-hud/` | 轻量单页气氛原型（无 Three.js） |
| `apps/loop-jarvis-holo/` | **本目录**：真全息 / 手势 / 3D（推荐主路径） |

正式业务数据仍应对接 `loop-luobo` 与 `/ops`，本项目先锁交互壳。
