import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_and_requirements_pin_the_same_packages():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    from_pyproject = set(pyproject["project"]["dependencies"])
    from_requirements = {
        line.strip() for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }
    assert from_pyproject == from_requirements
