import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import pytest

from aedttest import aedt_test_runner
from aedttest.clusters.job_hosts import get_job_machines


def test_allocate_task_single():
    job_machines = get_job_machines("host1:15,host2:10")
    machines_dict = {machine.hostname: machine.cores for machine in job_machines}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 17}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 15, "tasks": 1}, "host2": {"cores": 2, "tasks": 1}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 15}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 15, "tasks": 1}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 2}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 2, "tasks": 1}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 25}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 15, "tasks": 1}, "host2": {"cores": 10, "tasks": 1}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 26}, machines_dict)
    assert not allocated_machines


def test_allocate_task_multiple():
    """
    Test all possible scenarios of job splitting. Every test is critical
    Returns:

    """
    job_machines = get_job_machines("host1:20,host2:10")
    machines_dict = {machine.hostname: machine.cores for machine in job_machines}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 16, "parametric_tasks": 2}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 16, "tasks": 2}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 24, "parametric_tasks": 2}, machines_dict)
    assert not allocated_machines

    allocated_machines = aedt_test_runner.allocate_task({"cores": 10, "parametric_tasks": 2}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 10, "tasks": 2}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 25, "parametric_tasks": 5}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 20, "tasks": 4}, "host2": {"cores": 5, "tasks": 1}}

    job_machines = get_job_machines("host1:10,host2:15")
    machines_dict.clear()
    for machine in job_machines:
        machines_dict[machine.hostname] = machine.cores

    allocated_machines = aedt_test_runner.allocate_task({"cores": 26, "parametric_tasks": 2}, machines_dict)
    assert not allocated_machines

    allocated_machines = aedt_test_runner.allocate_task({"cores": 10, "parametric_tasks": 2}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 10, "tasks": 2}}

    allocated_machines = aedt_test_runner.allocate_task({"cores": 25, "parametric_tasks": 5}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 10, "tasks": 2}, "host2": {"cores": 15, "tasks": 3}}


def test_allocate_task_within_node():
    job_machines = get_job_machines("host1:15,host2:10")
    machines_dict = {machine.hostname: machine.cores for machine in job_machines}

    allocated_machines = aedt_test_runner.allocate_task_within_node({"cores": 17}, machines_dict)
    assert not allocated_machines

    allocated_machines = aedt_test_runner.allocate_task_within_node({"cores": 15}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 15, "tasks": 1}}

    allocated_machines = aedt_test_runner.allocate_task_within_node({"cores": 2}, machines_dict)
    assert allocated_machines == {"host1": {"cores": 2, "tasks": 1}}


def test_copy_path_file_absolute():
    with TemporaryDirectory(prefix="src_") as src_tmp_dir:
        file = Path(src_tmp_dir, "tmp_file.txt")
        file_no = Path(src_tmp_dir, "not_copy.txt")

        file.touch()
        file_no.touch()
        with TemporaryDirectory(prefix="dst_") as dst_tmp_dir:
            aedt_test_runner.copy_path(str(file), dst_tmp_dir)

            assert Path(dst_tmp_dir, file.name).is_file()
            assert Path(dst_tmp_dir, file.name).exists()
            assert not Path(dst_tmp_dir, file_no.name).exists()


def test_copy_path_file_relative():
    with TemporaryDirectory(prefix="src_", dir=Path.cwd()) as src_tmp_dir:
        # test relative file
        folder_name = Path(src_tmp_dir).name
        file = Path(folder_name) / "tmp_file.txt"
        file_no = Path(folder_name) / "not_copy.txt"

        file.touch()
        file_no.touch()
        with TemporaryDirectory(prefix="dst_") as dst_tmp_dir:
            aedt_test_runner.copy_path(str(file), dst_tmp_dir)

            assert (Path(dst_tmp_dir) / file).is_file()
            assert (Path(dst_tmp_dir) / file).exists()
            assert not (Path(dst_tmp_dir) / file_no).exists()


def test_copy_path_folder_absolute():
    with TemporaryDirectory(prefix="src_") as src_tmp_dir:
        folder = Path(src_tmp_dir, "tmp_folder")

        folder.mkdir()
        file = folder / "tmp_file.txt"
        file2 = folder / "tmp_file2.txt"
        file.touch()
        file2.touch()
        with TemporaryDirectory(prefix="dst_") as dst_tmp_dir:
            aedt_test_runner.copy_path(str(folder), dst_tmp_dir)

            assert Path(dst_tmp_dir, "tmp_folder", file.name).is_file()
            assert Path(dst_tmp_dir, "tmp_folder", file.name).exists()
            assert Path(dst_tmp_dir, "tmp_folder", file2.name).exists()


def test_copy_path_folder_relative():
    with TemporaryDirectory(prefix="src_", dir=Path.cwd()) as src_tmp_dir:
        folder_name = Path(src_tmp_dir).name
        folder = Path(folder_name) / "tmp_folder"

        folder.mkdir()
        file = folder / "tmp_file.txt"
        file2 = folder / "tmp_file2.txt"
        file.touch()
        file2.touch()
        with TemporaryDirectory(prefix="dst_") as dst_tmp_dir:
            aedt_test_runner.copy_path(str(folder), dst_tmp_dir)

            assert (Path(dst_tmp_dir) / file).is_file()
            assert (Path(dst_tmp_dir) / file).exists()
            assert (Path(dst_tmp_dir) / file2).exists()


def test_get_aedt_executable_path():
    with mock.patch.dict(os.environ, {"ANSYSEM_ROOT212": "my/custom/path"}):
        with mock.patch("aedttest.aedt_test_runner.platform.system", return_value="Linux"):
            aedt_path = aedt_test_runner.get_aedt_executable_path("212")
            assert Path(aedt_path) == Path("my/custom/path/ansysedt")

        with mock.patch("aedttest.aedt_test_runner.platform.system", return_value="Windows"):
            aedt_path = aedt_test_runner.get_aedt_executable_path("212")
            assert Path(aedt_path) == Path("my/custom/path/ansysedt.exe")

        with mock.patch("aedttest.aedt_test_runner.platform.system", return_value="MacOS"):
            with pytest.raises(SystemError) as exc:
                aedt_test_runner.get_aedt_executable_path("212")

            assert "Platform is neither Windows nor Linux" in str(exc.value)

    with mock.patch.dict(os.environ, {"ANSYSEM_ROOT212": ""}):
        with pytest.raises(ValueError) as exc:
            aedt_test_runner.get_aedt_executable_path("212")

        assert "Environment variable ANSYSEM_ROOT212" in str(exc.value)


@mock.patch("aedttest.aedt_test_runner.subprocess.call", wraps=lambda x: x)
@mock.patch("aedttest.aedt_test_runner.get_aedt_executable_path", return_value="aedt/install/path")
def test_execute_aedt(mock_aedt_path, mock_call):

    aedt_test_runner.execute_aedt(
        version="212",
        script="my/script/path.py",
        script_args="arg1",
        project_path="custom/pr.aedt",
        machines={"host1": {"cores": 10, "tasks": 2}, "host2": {"cores": 15, "tasks": 3}},
        distribution_config={
            "cores": 2,
            "distribution_types": ["Variations", "Frequencies"],
            "parametric_tasks": 3,
            "multilevel_distribution_tasks": 4,
            "single_node": False,
        },
    )

    assert mock_aedt_path.call_args[0][0] == "212"

    assert mock_call.call_args[0][0] == [
        "aedt/install/path",
        "-machinelist",
        "list=host1:2:10:90%,host2:3:15:90%",
        "-distributed",
        "includetypes=Variations,Frequencies",
        "maxlevels=2",
        "numlevel1=4",
        "-ng",
        "-features=SF6694_NON_GRAPHICAL_COMMAND_EXECUTION",
        "-RunScriptAndExit",
        "my/script/path.py",
        "-ScriptArgs",
        '"arg1"',
        "custom/pr.aedt",
    ]
