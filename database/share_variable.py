import threading
from typing import Optional

_lock = threading.Lock()
_session_steps: dict[str, list] = {}


def init_session(session_id: str, steps: list = None) -> None:
    """开始一次对话时调用。若提供 steps 则直接持有引用（后续原地修改自动可见）。"""
    with _lock:
        _session_steps[session_id] = steps if steps is not None else []


def add_step(session_id: str, step: str) -> None:
    """向对应session的流程中添加一个步骤。"""
    with _lock:
        if session_id not in _session_steps:
            _session_steps[session_id] = []
        _session_steps[session_id].append(step)


def get_steps(session_id: str) -> Optional[list]:
    """获取某次对话的完整流程步骤列表（嵌套列表结构）。"""
    with _lock:
        return _session_steps.get(session_id, None)


def set_session_steps(session_id: str, steps: list) -> None:
    """一次性写入某次对话的完整步骤列表（覆盖已有记录）。"""
    with _lock:
        _session_steps[session_id] = list(steps)


def remove_session(session_id: str) -> None:
    """对话结束后清理，释放内存。"""
    with _lock:
        _session_steps.pop(session_id, None)
