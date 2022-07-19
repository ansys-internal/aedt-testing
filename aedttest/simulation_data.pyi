from typing import Any
from typing import Dict
from typing import List
from typing import Optional

DEBUG: bool

def parse_args() -> str: ...
def parse_args_debug() -> str: ...

pyaedt_path: str
specified_version: Optional[str]
parser: Any
args: Any
PROJECT_DICT: Dict[str, Any]

class AedtTestException(Exception): ...

def parse_mesh_stats(mesh_stats_file: str, design_name: str, variation: str, setup_name: str) -> Optional[int]: ...
def parse_profile_file(profile_file: str, design_name: str, variation: str, setup_name: str) -> Optional[str]: ...
def parse_value_with_unit(string: str) -> str: ...
def extract_data(desktop: Any, project_dir: str, project_name: str, design_names: List[str]) -> Dict[str, Any]: ...
def extract_design_data(
    app: Any, design_name: str, setup_dict: Dict[str, str], project_dir: str, design_dict: Dict[str, Any]
) -> Dict[str, Any]: ...
def compose_variation_string(variation_string: str) -> str: ...
def extract_reports_data(app: Any, design_name: str, project_dir: str, report_names: List[str]) -> Dict[str, Any]: ...
def compose_curve_keys(data_dict: Dict[str, Any]) -> Dict[str, Any]: ...
def check_nan(data_dict: Dict[str, Any]) -> Dict[str, Any]: ...
def generate_unique_file_path(project_dir: str, extension: str) -> str: ...
def main() -> None: ...
