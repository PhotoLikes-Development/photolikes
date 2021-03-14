from argparse import ArgumentParser
from os import system, popen
from pathlib import Path
from typing import Iterable

PROJECT_ROOT_PATH = Path()
BUMP_OPTIONS = ("major", "minor", "patch")


def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument("bump",
                           choices=BUMP_OPTIONS,
                           metavar="bump",
                           help=f"A version to bump during the release {BUMP_OPTIONS}.")
    argparser.add_argument("tag_message", type=str, help="A message for the release tag.")
    return argparser.parse_args()


class Version:
    def __init__(self, vals: Iterable[int]):
        self.vals = tuple(vals)

    @classmethod
    def read_from_file(cls, path: Path) -> 'Version':
        if not path.exists():
            return cls((0, 0, 0))

        with path.open() as f:
            return cls(map(int, f.readline().split(".")))

    def write_to_file(self, path: Path):
        with path.open("w") as f:
            return f.write(str(self))

    def bump(self, version_to_bump) -> 'Version':
        bump_index = BUMP_OPTIONS.index(version_to_bump)
        assert bump_index != -1
        return Version(self.vals[:bump_index] + (self.vals[bump_index] + 1,) + (0,) * len(self.vals[bump_index + 1:]))

    def __str__(self):
        return ".".join(map(str, self.vals))


def execute(*commands):
    for command in commands:
        print(f"{PROJECT_ROOT_PATH.absolute()}> {command}")
        assert system(command) == 0, "A error happened during command execution! (non-zero return code)"


def check_clean_git_working_tree():
    git_status = popen("git status --porcelain").readlines()
    changed_tracking_files = [line for line in git_status if line and not line.startswith("??")]
    if changed_tracking_files:
        files_to_commit = '\n'.join(changed_tracking_files)
        raise EnvironmentError(f"Fix uncommitted changes!\n{files_to_commit}")


def get_tag_message(args):
    tag_message: str = args.tag_message
    return tag_message.capitalize().rstrip(".") + "."


if __name__ == "__main__":
    args = parse_args()

    version_path = PROJECT_ROOT_PATH.joinpath("version").absolute()
    version = Version.read_from_file(version_path)
    new_version = version.bump(args.bump)

    check_clean_git_working_tree()
    execute(f"git flow release start {new_version}")
    new_version.write_to_file(version_path)
    print(f"Bumped {args.bump} version to {new_version} from {version} in {version_path}.")
    execute(
        f"git add version",
        f'git commit -m "[auto] Bump version from {version} to {new_version}"',
        f'git flow release finish -m "{get_tag_message(args)}" {new_version}'
    )

    confirmation = None
    while confirmation not in ["yes", "no"]:
        confirmation = input("Push the new version to remote (yes/no): ")

    if confirmation == "yes":
        print("Pushing all the changes!")
        execute(
            "git push origin master",
            "git push origin develop",
            "git push origin --tags"
        )
    else:
        print("NOT pushing the new version to remote.")
