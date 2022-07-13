import argparse

_parser = argparse.ArgumentParser()
_parser.add_argument("--skip-db-update", dest = "skip_db_update", action="store_true", default = False)
_parser.add_argument("--skip-download", dest = "skip_download", action="store_true", default = False)
_args = _parser.parse_args()

def should_skip_db_update() -> bool:
    return _args.skip_db_update

def should_skip_download() -> bool:
    return _args.skip_download