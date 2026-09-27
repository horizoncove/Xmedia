# LOOP Phone Dock · 研发骨架

Lumi 那类「真机物理点按」底座，在这台云环境里做不出机械件。这一套先把**软件合同**和**硬件规格**定下来，并用虚拟手机把「看屏 → 规划 → 点按 → 读结果」跑通。

## 能做什么

- 虚拟手机：主屏 → 设置 → 关于本机
- HTTP：`/screen`、`/tap`、`/swipe`、`/type`、`/act`
- `act("打开设置并读出型号")` 走规则规划，返回 `LOOP-PHONE`
- 硬件规格见 `hardware-spec.md`（给以后打样，不是已制造的机器）

## 跑起来

```bash
cd apps/loop-phone-dock
python3 -m dock.server
# http://127.0.0.1:8787/
```

测试：

```bash
cd apps/loop-phone-dock
python3 -m unittest tests.test_loop -v
```

## 明确不是

- 不是 Lumi 仿制品，不控制别人的真机
- 不绕过 App 反自动化、不碰支付/验证码
- 没有电机、摄像头、RK3576 板子
