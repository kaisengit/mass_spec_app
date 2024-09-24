import os
from glob import iglob

all_files = sorted(iglob("backend/mass_spec_app/*/*.py"))
os.execvp(
    "mypy",
    ["mypy", "--strict", "--follow-imports=silent"] + all_files,
)
