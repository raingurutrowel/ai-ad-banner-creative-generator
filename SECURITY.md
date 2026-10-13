# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@ad-banner-creative.dev` with a description, a minimal
reproduction, and the plugin list loaded at the time. Do not open a public
issue for anything that lets a plugin escape its sandbox or read files
outside the configured `assets_root`.

## Threat model

The generator loads third-party extension modules. That is the whole attack
surface. We treat plugins as untrusted:

- Plugins run in-process but are handed a restricted `PluginContext` that
  exposes only the asset store, the render bus, and the config slice they
  declared in their manifest.
- A plugin that declares `fs:write` gets writes scoped to `renders/` and
  `exports/` only. Path traversal outside those roots raises
  `PluginSandboxError` and the host disables the plugin for the session.
- Network access is denied by default. A plugin that needs a remote copy
  model must declare `net:http` and the host will prompt on first load.

## Out of scope

- Prompt injection in user-supplied copy blocks. That is data, not code.
- Malicious brand kits. Validate them yourself before shipping to a client.

## Hardening checklist for plugin authors

- Declare the narrowest capability set that works.
- Never shell out. Use the render bus.
- Never write to `config/`. The host owns config.