"""Plugin host entrypoint. Boots config, loads extensions, runs the CLI."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from core.registry import HookRegistry
from core.loader import PluginLoader
from core.context import HostContext
from services.render_pipeline import RenderPipeline
from utils.config_loader import load_config
from utils.logging_setup import configure_logging

log = logging.getLogger("ad_banner.host")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="ad-banner-gen")
    p.add_argument("--config", default="config/plugins.toml")
    p.add_argument("--list-plugins", action="store_true")
    p.add_argument("--render", metavar="PRESET", default=None)
    p.add_argument("--seed", type=int, default=6767)
    p.add_argument("--trace", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    configure_logging(trace=args.trace)

    repo_root = Path(__file__).resolve().parent.parent
    cfg = load_config(repo_root / args.config)
    ctx = HostContext.from_config(repo_root, cfg)

    registry = HookRegistry()
    loader = PluginLoader(ctx=ctx, registry=registry, config=cfg)
    loaded = loader.load_all()
    log.info("loaded %d plugins: %s", len(loaded), ", ".join(p.name for p in loaded))

    if args.list_plugins:
        for p in loaded:
            print(f"{p.name}\t{p.version}\thooks={','.join(p.hooks)}")
        return 0

    if args.render is None:
        log.error("nothing to do; pass --render <preset> or --list-plugins")
        return 2

    pipeline = RenderPipeline(registry=registry, ctx=ctx, seed=args.seed)
    results = pipeline.render_preset(args.render)
    for r in results:
        print(f"{r.output_path}\t{r.width}x{r.height}\t{r.bytes_written}B\t{r.duration_ms}ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())