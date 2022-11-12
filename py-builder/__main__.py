"""
Builds & creates an altInstall for CPython from source.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

VERBOSE = False
DRYRUN = False

CPY_REMOTE = "git@github.com:python/cpython.git"
CPY_DIR = Path(f"{os.getenv('XDG_CACHE_HOME', '.')}/cpython")


def check_repo_exists(clone: bool):
    exists = CPY_DIR.exists() and CPY_DIR.is_dir()
    if not exists:
        if clone:
            clone_repo()
            check_repo_exists(False)
        else:
            raise FileNotFoundError(
            f"Cannot find CPython repository at {CPY_DIR}, pass '--clone' to download"
        )


def clone_repo():
    subprocess.run(args=["git", "clone", CPY_REMOTE], cwd=CPY_DIR.parent)


def update_repo():
    subprocess.run(
        ["git", "checkout", "main"],
        cwd=CPY_DIR,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(["git", "pull"], cwd=CPY_DIR, check=True, stdout=subprocess.DEVNULL)


def get_tags():
    """
    Updates tags, then returns a list of all tags.
    """
    print("Pulling latest tags...")
    subprocess.run(["git", "fetch", "--tags"], cwd=CPY_DIR, check=True)
    result = subprocess.run(
        ["git", "tag"], cwd=CPY_DIR, check=True, text=True, capture_output=True
    )
    tags = set(result.stdout.split("\n"))
    tags.remove("")
    return tags


def build(tag: str):
    update_repo()
    tags = get_tags()
    if tag not in tags:
        tag_not_found_handler(tag, tags)
    print(f"Tag '{tag}' found")

    print(f"\tChecking out {tag}")
    subprocess.run(
        ["git", "checkout", tag],
        cwd=CPY_DIR,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("\tConfiguring...")
    subprocess.run(["./configure"], cwd=CPY_DIR, check=True, stdout=subprocess.DEVNULL)

    print(f"\tRunning 'make'...")
    subprocess.run(
        ["make"],
        cwd=CPY_DIR,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if os.geteuid() != 0:
        print("Running 'make altinstall' with Sudo")
        make_args = ["sudo", "make", "altinstall"]
    else:
        print(f"\tRunning 'make altinstall'...")
        make_args = ["make", "altinstall"]

    subprocess.run(
        make_args,
        cwd=CPY_DIR,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"Done!")
    sys.exit(0)


def tag_not_found_handler(tag: str, tags: set[str]):
    """
    Prints a nice message telling the user that the
    tag provided is not found, and suggests nearby tags.
    """
    nearby_tags = sorted(list(find_near_tags(tag, tags)))
    print(f"Could not find tag '{tag}'.")
    print(f"Maybe you meant: ")
    for t in nearby_tags:
        print(f"\t{t}")

    sys.exit(1)


def find_near_tags(tag: str, tags: set[str]) -> set[str]:
    """
    Return tags 'close to' the user provided tag.
    """
    return {t for t in tags if tag in t}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="py-builder", description="Build and alt-install CPython from source."
    )

    parser.add_argument("tag", type=str, help="Tagged version to build")
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help="Print commands to standard out instead of running.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print and run commands.",
    )
    parser.add_argument(
        "-c",
        "--clone",
        action="store_true",
        help="If the repository is not found, automatically clone from Github",
    )

    args = parser.parse_args()

    DRYRUN = args.dryrun
    VERBOSE = args.verbose

    if DRYRUN:
        raise NotImplementedError("Dryrun is WIP")

    if VERBOSE:
        print("INFO :: Verbose is WIP, default is maximum verbosity")

    check_repo_exists(args.clone)
    build(args.tag)
