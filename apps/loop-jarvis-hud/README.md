# LOOP JARVIS · Quantum HUD

好莱坞青蓝体全息风格的值班中枢动态原型（单页 HTML）。

## 打开

```bash
# 任意静态服务器
python3 -m http.server 8765 --directory apps/loop-jarvis-hud
# 浏览器打开 http://127.0.0.1:8765
```

或直接打开 `index.html`。

## 已做

- 中央量子核 + 轨道环
- 粒子纠缠场（鼠标扰动）
- 南门雷达扫描 / 客流四字段跳动
- 街区白模热力点
- Agent 星座、待授权工单（可点「授权」）
- 语音条轮播 + telemetry 流

## 边界

这是视觉与交互气氛原型，不接真实 API。正式编排应对接 `/ops` 与 `loop-luobo` 数据面。
