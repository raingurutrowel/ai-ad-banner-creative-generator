"""HostContext — the sandboxed handle handed to plugins."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import httpx

from contracts.errors import PluginSandboxError
from utils.config_loader import HostConfig

log = logging.getLogger("ad_banner.context")

_ALLOWED_WRITE_ROOTS = ("renders", "exports")


@dataclass
class HostContext:
    repo_root: str
    assets_root: str
    render_root: str
    export_root: str
    granted_caps: set[str]

    @classmethod
    def from_config(cls, repo_root: Path, cfg: HostConfig) -> "HostContext":
        return cls(
            repo_root=str(repo_root),
            assets_root=str(repo_root / cfg.assets_root),
            render_root=str(repo_root / cfg.render_root),
            export_root=str(repo_root / cfg.export_root),
            granted_caps=set(cfg.default_caps),
        )

    def _resolve_within(self, root: str, rel_path: str) -> Path:
        candidate = (Path(root) / rel_path).resolve()
        root_resolved = Path(root).resolve()
        if root_resolved not in candidate.parents and candidate != root_resolved:
            raise PluginSandboxError(f"path escapes sandbox: {rel_path}")
        return candidate

    def read_asset(self, rel_path: str) -> bytes:
        if "fs:read" not in self.granted_caps:
            raise PluginSandboxError("fs:read not granted")
        return self._resolve_within(self.assets_root, rel_path).read_bytes()

    def write_render(self, rel_path: str, payload: bytes) -> None:
        if "fs:write" not in self.granted_caps:
            raise PluginSandboxError("fs:write not granted")
        top = rel_path.split("/", 1)[0]
        if top not in _ALLOWED_WRITE_ROOTS:
            raise PluginSandboxError(f"writes only allowed under {_ALLOWED_WRITE_ROOTS}")
        target = self._resolve_within(self.repo_root, rel_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    def fetch(self, url: str, *, timeout_s: float = 10.0) -> bytes:
        if "net:http" not in self.granted_caps:
            raise PluginSandboxError("net:http not granted")
        resp = httpx.get(url, timeout=timeout_s)
        resp.raise_for_status()
        return resp.content