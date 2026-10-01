import subprocess
import sys
from pathlib import Path


ROOT = Path(
    __file__
).resolve().parent


if __name__ == "__main__":

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(
                ROOT
                / "frontend"
                / "app.py"
            ),
        ],
        check=True,
    )