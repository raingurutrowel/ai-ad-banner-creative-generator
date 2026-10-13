"""Shared contracts for the plugin host and every extension module.

Only symbols re-exported here are stable across host versions. Plugin authors
should import from `contracts`, never from `core` internals.
"""

from contracts.plugin_contract import (
    PluginManifest,
    PluginProtocol,
    RegistryProtocol,
    PluginContext,
)
from contracts.render_contract import (
    CanvasSpec,
    CopyBlock,
    RenderRequest,
    RenderResult,
    StylePreset,
)
from contracts.errors import (
    PluginLoadError,
    PluginSandboxError,
    RenderError,
)

__all__ = [
    "PluginManifest",
    "PluginProtocol",
    "RegistryProtocol",
    "PluginContext",
    "CanvasSpec",
    "CopyBlock",
    "RenderRequest",
    "RenderResult",
    "StylePreset",
    "PluginLoadError",
    "PluginSandboxError",
    "RenderError",
]