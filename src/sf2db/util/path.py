from pathlib import Path
from typing import Any


def absolute(cwd:str, relative_path: str)-> Any:
   current_dir = Path(cwd).resolve().parent
   full_abs_path=  (current_dir/relative_path).resolve()
   return full_abs_path 