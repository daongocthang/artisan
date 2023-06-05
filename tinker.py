import os
import json
import shutil
import sys
from common import require
from common.colors import CBEIGE, CGREEN, CEND, CRED
import argparse


yaml = require("yaml", "PyYAML")

basedir = os.path.dirname(os.path.abspath(__file__))


def loadPkg() -> dict:
    with open(os.path.join(basedir, "package.yaml"), "r") as f:
        pkg = yaml.load(f, Loader=yaml.SafeLoader)
    return pkg


def sniffReact(path) -> dict:
    with open(os.path.join(path, "package.json"), "r") as f:
        pkg = json.load(f)
    return pkg


def tinker_react_app(dst_dir):
    """Make developing a react app easy

    Args:
        dst_dir (str): destination directory (default: current directory)
    """

    # inject package.json
    origin = sniffReact(dst_dir)
    extra = loadPkg()

    origin["scripts"] = {}
    for k, v in extra.items():
        newDict = origin.get(k) if isinstance(origin.get(k), dict) else {}
        origin[k] = {**newDict, **v}

    with open(os.path.join(dst_dir, "package.json"), "w") as f:
        json.dump(origin, f)

    print(f"[{CGREEN}ok{CEND}] remake {CBEIGE}package.json{CEND} succesfully")

    # copy to react app
    shutil.copytree(os.path.join(basedir, "templates"),
                    dst_dir, dirs_exist_ok=True)
    for x in os.listdir(os.path.join(basedir, "templates")):
        print(f"[{CGREEN}ok{CEND}] create {CBEIGE}{x}{CEND} succesfully")


def tinker_vscode(dst_dir):
    """Format a consistent style

    Args:
        dst_dir (str): destination directory (default: current directory)
    """

    src_dir = os.path.join(basedir, "templates\\.vscode")
    shutil.copytree(src_dir, os.path.join(
        dst_dir, '.vscode'), dirs_exist_ok=True)
    print(f"[{CGREEN}ok{CEND}] create {CBEIGE}.vscode/setting.json{CEND} successfully")

    src_dir = os.path.join(basedir, "templates\\.prettierrc")
    shutil.copy(src_dir, dst_dir)
    print(f"[{CGREEN}ok{CEND}] create {CBEIGE}.prettierrc{CEND} successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simplify coding")
    parser.add_argument("-t", "--type", help="[reat-app, vscode]", default="vscode")
    parser.add_argument("-d", "--dest", default=os.getcwd(),
                        help="default: current directory")

    args = parser.parse_args()

    try:
        print("\nDestination: ", CGREEN + args.dest + CEND+"\n")

        if args.type == "react-app":
            tinker_react_app(args.dest)

        if args.type == "vscode":
            tinker_vscode(args.dest)

    except FileNotFoundError as e:
        import re
        print(re.sub(r"Errno\s\d+", f"{CRED}Errno {e.errno}{CEND}", str(e)))
