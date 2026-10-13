"""Typed errors raised across the plugin boundary."""


class AdBannerError(Exception):
    """Base for every error the host raises."""


class PluginLoadError(AdBannerError):
    """Raised when a plugin fails import, manifest parse, or registration."""


class PluginSandboxError(AdBannerError):
    """Raised when a plugin tries to escape its declared capability set."""


class RenderError(AdBannerError):
    """Raised when the render pipeline cannot complete a request."""