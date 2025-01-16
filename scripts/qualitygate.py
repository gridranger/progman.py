from logging import error, basicConfig, INFO, info
from subprocess import run


class QualityGate:

    def __init__(self):
        basicConfig(level=INFO)
        self._failed = []
        self._return_code = 0

    def run(self) -> None:
        self.check_step("Lint", ["ruff", "check", "."])
        self.check_step("Test", ["pytest"])
        if self._return_code > 0:
            error(f"The following step(s) failed: {', '.join(self._failed)}")
            exit(self._return_code)
        else:
            info("All checks passed. 🙂")

    def check_step(self, step_name: str, command: list[str]):
        result = run(command, text=True)
        if result.returncode > 0:
            self._failed.append(step_name)
            self._return_code = result.returncode


if __name__ == "__main__":
    QualityGate().run()
