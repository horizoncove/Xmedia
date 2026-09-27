"""Rule planner. A later build can swap this for a vision grounding model."""

from __future__ import annotations

from dock.phone import Phone


def act(phone: Phone, instruction: str) -> dict:
    text = instruction.strip().lower()
    steps: list[str] = []

    def tap_id(target_id: str) -> bool:
        for t in phone.targets():
            if t.id == target_id:
                phone.tap(t.x + t.w // 2, t.y + t.h // 2)
                steps.append(target_id)
                return True
        return False

    wants_model = any(k in text for k in ("型号", "model", "关于"))
    wants_settings = wants_model or any(k in text for k in ("设置", "settings"))
    wants_messages = any(k in text for k in ("信息", "消息", "值班"))

    if wants_settings:
        if phone.screen == "home":
            tap_id("settings")
        if phone.screen == "settings" and wants_model:
            tap_id("about")
        if phone.screen == "about":
            tap_id("model")
    elif wants_messages:
        if phone.screen == "home":
            tap_id("messages")
        if phone.screen == "messages":
            tap_id("thread")
    else:
        return {
            "ok": False,
            "reason": "no-rule",
            "instruction": instruction,
            "steps": steps,
            **phone.snapshot(),
        }

    return {
        "ok": bool(phone.last_result) or phone.screen != "home",
        "instruction": instruction,
        "steps": steps,
        "answer": phone.last_result,
        **phone.snapshot(),
    }
