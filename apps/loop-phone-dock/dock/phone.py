"""Virtual phone. Screens and hit targets are in pixel space (390x844)."""

from __future__ import annotations

from dataclasses import dataclass, field


W, H = 390, 844


@dataclass
class Target:
    id: str
    label: str
    x: int
    y: int
    w: int
    h: int
    action: str

    def contains(self, px: int, py: int) -> bool:
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
        }


@dataclass
class Phone:
    screen: str = "home"
    model: str = "LOOP-PHONE"
    typed: str = ""
    log: list[str] = field(default_factory=list)
    last_result: str = ""

    def targets(self) -> list[Target]:
        if self.screen == "home":
            return [
                Target("settings", "设置", 40, 180, 140, 88, "open-settings"),
                Target("messages", "信息", 210, 180, 140, 88, "open-messages"),
            ]
        if self.screen == "settings":
            return [
                Target("about", "关于本机", 24, 160, 342, 64, "open-about"),
                Target("back", "返回", 24, 740, 120, 48, "go-home"),
            ]
        if self.screen == "about":
            return [
                Target("model", f"型号 {self.model}", 24, 160, 342, 64, "read-model"),
                Target("back", "返回", 24, 740, 120, 48, "go-settings"),
            ]
        if self.screen == "messages":
            return [
                Target("thread", "值班群", 24, 160, 342, 64, "open-thread"),
                Target("back", "返回", 24, 740, 120, 48, "go-home"),
            ]
        if self.screen == "thread":
            return [
                Target("field", "输入框", 24, 680, 250, 48, "focus-field"),
                Target("send", "发送", 286, 680, 80, 48, "send"),
                Target("back", "返回", 24, 740, 120, 48, "go-messages"),
            ]
        return []

    def snapshot(self) -> dict:
        titles = {
            "home": "主屏",
            "settings": "设置",
            "about": "关于本机",
            "messages": "信息",
            "thread": "值班群",
        }
        return {
            "screen": self.screen,
            "title": titles.get(self.screen, self.screen),
            "width": W,
            "height": H,
            "model": self.model,
            "typed": self.typed,
            "last_result": self.last_result,
            "targets": [t.as_dict() for t in self.targets()],
            "log": self.log[-12:],
        }

    def tap(self, x: int, y: int) -> dict:
        hit = next((t for t in self.targets() if t.contains(x, y)), None)
        if hit is None:
            self.log.append(f"tap miss {x},{y} on {self.screen}")
            return {"ok": False, "reason": "miss", **self.snapshot()}
        self._run(hit.action)
        self.log.append(f"tap {hit.id} -> {self.screen}")
        return {"ok": True, "hit": hit.id, **self.snapshot()}

    def swipe(self, x1: int, y1: int, x2: int, y2: int) -> dict:
        self.log.append(f"swipe {x1},{y1}->{x2},{y2}")
        if y1 - y2 > 80 and self.screen == "home":
            self.screen = "settings"
        return {"ok": True, **self.snapshot()}

    def type_text(self, text: str) -> dict:
        if self.screen != "thread":
            return {"ok": False, "reason": "no-field", **self.snapshot()}
        self.typed += text
        self.log.append(f"type {text!r}")
        return {"ok": True, **self.snapshot()}

    def _run(self, action: str) -> None:
        if action == "open-settings":
            self.screen = "settings"
        elif action == "open-messages":
            self.screen = "messages"
        elif action == "open-about":
            self.screen = "about"
        elif action == "open-thread":
            self.screen = "thread"
        elif action == "go-home":
            self.screen = "home"
        elif action == "go-settings":
            self.screen = "settings"
        elif action == "go-messages":
            self.screen = "messages"
        elif action == "read-model":
            self.last_result = self.model
        elif action == "focus-field":
            self.last_result = "field-focus"
        elif action == "send":
            # Research build never auto-sends. The button only records intent.
            self.last_result = f"held:{self.typed}" if self.typed else "held:empty"
            self.log.append("send held for confirmation")
