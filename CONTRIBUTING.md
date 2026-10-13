# Contributing to ai-ad-banner-creative-generator

Thanks for wanting to build on the generator. This repo is a plugin host:
the core does layout, rendering orchestration, and asset plumbing, and
everything creative (copy models, style presets, brand kits, exporters)
lives in an extension module under `extensions/`.

## Ground rules

- Python 3.12+ is the target. We type-check with `mypy --strict` on `core/`,
  `contracts/`, and `extensions/`.
- Every new capability is a plugin. If you find yourself editing `core/host.py`
  to add a feature, that feature probably belongs in an extension.
- No feature lands without a test in `tests/`.
- Keep the creative pipeline deterministic when a seed is provided. Renders
  must reproduce byte-for-byte given the same seed, canvas, and preset.

## Plugin contract

A plugin is a Python package under `extensions/` that exposes a top-level
`plugin.py` with a `register(registry)` function. The registry hands you the
hook points you asked for. See `contracts/plugin_contract.py` for the
Protocol definitions — those are the only symbols you should import from
the host side.

## Dev setup

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -e ".[dev]"
pytest -q
```

## Adding a plugin

1. `mkdir extensions/ad_creative_<yourname>`
2. Add `plugin.py` with `def register(registry): ...`
3. Drop the plugin name into `config/plugins.toml` under `[enabled]`.
4. Run `python -m core.host --list-plugins` to confirm the loader sees it.

## Style

- Ruff config lives in `pyproject.toml`. Line length 100.
- Comments explain constraints the code can't express. Don't narrate.
- Domain names: canvas, variant, preset, brand_kit, copy_block, export_target.
  Avoid `data`, `tmp`, `x`.

## Reporting bugs

Open an issue with the plugin name, the config block you used, and the
failing render seed. Include the `--trace` output from the host.