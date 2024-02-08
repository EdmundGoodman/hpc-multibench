#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A class for test configurations on batch compute."""

from pathlib import Path
from re import search as re_search
from subprocess import PIPE
from subprocess import run as subprocess_run
from tempfile import NamedTemporaryFile
from typing import Optional

BASH_SHEBANG = "#!/bin/sh\n"
JOB_ID_REGEX = r"Submitted batch job (\d+)"


class RunConfiguration:
    """A builder/runner for a run configuration."""

    def __init__(self, run_command: str):
        """Initialise the run configuration file as a empty bash file."""
        self.name: str = ""
        self.sbatch_config: dict[str, str] = {}
        self.module_loads: list[str] = []
        self.environment_variables: dict[str, str] = {}
        self.directory: Optional[Path] = None
        self.build_commands: list[str] = []
        self.run_command: str = run_command
        self.args: Optional[str] = None

    @property
    def sbatch_contents(self) -> str:
        """Construct the sbatch configuration for the run."""
        sbatch_file = BASH_SHEBANG

        for key, value in self.sbatch_config.items():
            sbatch_file += f"#SBATCH --{key}={value}\n"

        if len(self.module_loads) > 0:
            sbatch_file += "module purge\n"
            sbatch_file += f"module load {' '.join(self.module_loads)}\n"

        for key, value in self.environment_variables.items():
            sbatch_file += f"export {key}={value}\n"

        sbatch_file += "\necho '===== ENVIRONMENT ====='\n"
        sbatch_file += "lscpu\n"
        sbatch_file += "echo\n"

        sbatch_file += "\necho '===== BUILD ====='\n"
        if self.directory is not None:
            sbatch_file += f"cd {self.directory}\n"
        sbatch_file += "\n".join(self.build_commands) + "\n"

        sbatch_file += "\necho '===== RUN"
        if self.name != "":
            sbatch_file += f"{self.name} "
        sbatch_file += " ====='\n"
        sbatch_file += f"time srun {self.run_command} {self.args}\n"

        return sbatch_file

    def __repr__(self) -> str:
        """Get the sbatch configuration file defining the run."""
        return self.sbatch_contents

    def run(self) -> Optional[int]:
        """Run the specified run configuration."""
        with NamedTemporaryFile(
            suffix=".sbatch", dir=Path("./"), mode="w+"
        ) as sbatch_tmp:
            sbatch_tmp.write(self.sbatch_contents)
            sbatch_tmp.flush()
            result = subprocess_run(
                ["sbatch", Path(sbatch_tmp.name)], check=True, stdout=PIPE
            )
            job_id_search = re_search(JOB_ID_REGEX, result.stdout.decode("utf-8"))
            if job_id_search is None:
                return None
            return int(job_id_search.group(1))
