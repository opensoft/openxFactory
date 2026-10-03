from __future__ import annotations

import subprocess


class DashboardCompatibilityError(TypeError):
    module_name: str

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        super().__init__(
            f"ideation dashboard {module_name} compatibility is unavailable"
        )


CLI_OPERATION_ERRORS: tuple[type[Exception], ...] = (
    OSError,
    RuntimeError,
    ValueError,
    TypeError,
    KeyError,
    subprocess.SubprocessError,
)
