import re
import subprocess
import tomllib
from pathlib import Path


def main():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    package_name_pattern = re.compile(r"^([-a-zA-Z\d]+)(\[[-a-zA-Z\d,]+])?")
    dependencies = pyproject["project"]["dependencies"]

    to_remove = []
    to_add = []
    for dependency in dependencies:
        package_match = package_name_pattern.match(dependency)
        assert package_match, f"Invalid package name: '{dependency}'"
        package, extras = package_match.groups()
        to_remove.append(package)
        to_add.append(f"{package}{extras or ''}")

    subprocess.check_call(["uv", "remove", *to_remove, "--no-sync"])
    subprocess.check_call(["uv", "add", *to_add, "--no-sync"])
    subprocess.check_call(["uv", "sync"])


if __name__ == "__main__":
    main()
