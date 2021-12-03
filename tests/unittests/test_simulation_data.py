import os
from argparse import Namespace

try:
    from unittest import mock
except ImportError:
    # py27
    import mock

with mock.patch("argparse.ArgumentParser.parse_args", return_value=Namespace(desktop_version="2021.1")):
    from aedttest import simulation_data

TESTS_DIR = os.path.dirname(os.path.dirname(__file__))


class TestParse:
    def teardown(self):
        simulation_data.PROJECT_DICT = {"error_exception": [], "designs": {}}

    def test_parse_variation_string(self):
        result = simulation_data.parse_variation_string("abc")
        assert result == ("abc", "")

        result = simulation_data.parse_variation_string("")
        assert result == ("", "")

        result = simulation_data.parse_variation_string("3m2")
        assert result == ("3", "m2")

        result = simulation_data.parse_variation_string("3.12345678901234mH")
        assert result == ("3.123456789e+00", "mH")

        result = simulation_data.parse_variation_string("3.1234567891e-9mH")
        assert result == ("3.123456789e-09", "mH")

        result = simulation_data.parse_variation_string("3.1234567891e-111mH")
        assert result == ("3.123456789e-111", "mH")

        result = simulation_data.parse_variation_string("3")
        assert result == ("3", "")

        result = simulation_data.parse_variation_string("3.0")
        assert result == ("3.0", "")

    @mock.patch("aedttest.simulation_data.parse_profile_file", return_value="10:00:00")
    @mock.patch("aedttest.simulation_data.parse_mesh_stats", return_value=100)
    def test_extract_design_data(self, mock_parse_mesh, mock_parse_profile_file):
        mock_pyaedt_app = mock.Mock()
        mock_pyaedt_app.available_variations.get_variation_strings.return_value = ["Ia='30'A", "Ia='20'A"]
        mock_pyaedt_app.export_mesh_stats.return_value = None
        mock_pyaedt_app.export_profile.return_value = None

        result_dict = simulation_data.extract_design_data(
            app=mock_pyaedt_app,
            design_name="only_winding2",
            setup_dict={"Setup1": "Setup1 : LastAdaptive"},
            project_dir="/tmp",
            design_dict={"only_winding2": {"mesh": {}, "simulation_time": {}, "report": {}}},
        )

        assert result_dict == {
            "only_winding2": {
                "mesh": {"Ia=30A": {"Setup1": 100}, "Ia=20A": {"Setup1": 100}},
                "simulation_time": {"Ia=30A": {"Setup1": "10:00:00"}, "Ia=20A": {"Setup1": "10:00:00"}},
                "report": {},
            }
        }

    def test_parse_profile_2020r2(self):

        result = simulation_data.parse_profile_file(
            profile_file=os.path.join(TESTS_DIR, "input", "2020R2_profile.prof"),
            design="test_design",
            variation="test_variation",
            setup="test_setup",
        )
        assert result == "00:00:09"

    def test_parse_profile_2021r2(self):
        result = simulation_data.parse_profile_file(
            profile_file=os.path.join(TESTS_DIR, "input", "2021R2_profile.prof"),
            design="test_design",
            variation="test_variation",
            setup="test_setup",
        )
        assert result == "00:00:05"

    def test_parse_profile_2019r1(self):
        result = simulation_data.parse_profile_file(
            profile_file=os.path.join(TESTS_DIR, "input", "R2019R1_profile.prof"),
            design="test_design",
            variation="test_variation",
            setup="test_setup",
        )
        assert result == "00:00:02"

    def test_parse_mesh_stats_no_mesh(self):

        result = simulation_data.parse_mesh_stats(
            mesh_stats_file=os.path.join(TESTS_DIR, "input", "no_mesh.mstat"),
            design="only_winding2",
            variation="n_parallel='2' winding_current='15mA'",
            setup="Setup1",
        )
        assert result is None
        assert simulation_data.PROJECT_DICT == {
            "error_exception": [
                "Design:only_winding2 Variation: n_parallel='2' winding_current='15mA' Setup: Setup1 has no mesh stats"
            ],
            "designs": {},
        }

    def test_parse_mesh_stats(self):
        result = simulation_data.parse_mesh_stats(
            mesh_stats_file=os.path.join(TESTS_DIR, "input", "mesh.mstat"),
            design="test_design",
            variation="test_variation",
            setup="test_setup",
        )
        assert result == 44
