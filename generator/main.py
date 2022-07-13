import asyncio

from utils import args
from utils import db
from utils import log
from utils import nix
from vscode import marketplace_api as api

async def main():
    if not args.should_skip_db_update():
        extensions_data = await api.get_extensions_data()
        db.update_extensions(extensions_data)
    else:
        log.info("Skipped database update")
    
    extensions = db.get_all_extensions()

    if not args.should_skip_download():
        await api.download_extensions([e for e in extensions.values() if e["sha256"] is None])
    else:
        log.info("Skipped downloading extensions")

    to_update = [e for e in extensions.values() if e["sha256"] is not None]
    versions = api.extract_versions(to_update)
    sha256 = api.compute_sha256(to_update)
    for e, v, s in zip(to_update, versions, sha256):
        e["version"] = v
        e["sha256"] = s
    db.modify_extensions(to_update)

    nix.output_flake([
        e for e in extensions.values() if e["sha256"] is not None
    ])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
