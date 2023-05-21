import os
import json
import shutil
import argparse
from common import require
from common.colors import CBEIGE, CGREEN, CEND

yaml = require("yaml", "PyYAML")


def loadPkg() -> dict:
    with open("package.yaml", "r") as f:
        pkg = yaml.load(f, Loader=yaml.SafeLoader)
    return pkg


def sniffReact(path) -> dict:
    with open(os.path.join(path, "package.json"), "r") as f:
        pkg = json.load(f)
    return pkg


def injectReact(path):
    """
    Make developing a react app easy
    """
    # inject package.json
    origin = sniffReact(path)
    extra = loadPkg()

    appName = origin.get("name")
    origin["scripts"] = {}
    for k, v in extra.items():
        newDict = origin.get(k) if isinstance(origin.get(k), dict) else {}
        origin[k] = {**newDict, **v}

    with open(os.path.join(path, "package.json"), "w") as f:
        json.dump(origin, f)

    # copy to react app
    shutil.copytree("templates", path, dirs_exist_ok=True)

    print(f"[{CGREEN}ok{CEND}] inject into {CBEIGE}{appName}{CEND} app")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=injectReact.__doc__)
    parser.add_argument("app", help="react app path")
    args = parser.parse_args()
    injectReact(args.app)
