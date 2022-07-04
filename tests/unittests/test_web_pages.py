import json
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from .test_aedt_test_runner import TESTS_DIR
from .test_aedt_test_runner import BaseElectronicsDesktopTester

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


class TestProjectWebPage(BaseElectronicsDesktopTester):
    def setup_class(self):
        super().setup(self)
        self.aedt_tester.only_reference = True

        with open(TESTS_DIR / "input" / "project_report.json") as file:
            proj_dict = json.load(file)

        self.aedt_tester.initialize_results()
        self.aedt_tester.render_project_html("just_winding_221", proj_dict)

        self.webpage = self.aedt_tester.results_path / "just_winding_221.html"
        self.rel_path = str(self.aedt_tester.results_path).lower()
        driver.get(str(self.webpage))

    def teardown_class(self):
        driver.close()

    def test_title(self):
        assert driver.title == "just_winding_221"

    def test_simtime_link(self):
        simtime_link = driver.find_element(
            by=By.XPATH, value="/html/body/div/div/div/section/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[2]/a"
        )
        assert simtime_link.text == "00:00:07"

        profile_path = Path(simtime_link.get_attribute("href").replace("file:///", ""))
        assert profile_path.relative_to(self.rel_path) == Path(r"reference_folder\profiles\_VMG6BS.prof")

    def test_sim_name(self):
        sim_name = driver.find_element(
            by=By.XPATH, value="/html/body/div/div/div/section/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td[1]"
        )
        assert sim_name.text == "Maxwell2DDesign1:Setup1:xs=0.5mm"

    def test_mesh_link(self):
        mesh_link = driver.find_element(
            by=By.XPATH, value="/html/body/div/div/div/section/div[3]/div/div/div[2]/div/table/tbody/tr[1]/td[2]/a"
        )
        assert mesh_link.text == "133"

        profile_path = Path(mesh_link.get_attribute("href").replace("file:///", ""))
        assert profile_path.relative_to(self.rel_path) == Path(r"reference_folder\profiles\_7GWPCH.mstat")

    def test_mesh_name(self):
        mesh_name = driver.find_element(
            by=By.XPATH, value="/html/body/div/div/div/section/div[3]/div/div/div[2]/div/table/tbody/tr[2]/td[1]"
        )
        assert mesh_name.text == "Maxwell2DDesign1:Setup1:xs=6.000000000e-01mm"

    def test_plot_button(self):
        button = driver.find_element(by=By.XPATH, value="/html/body/div/div/div/section/div[8]/div/div/button")

        assert button.text == "Maxwell2DDesign1:Loss Plot 1:SolidLoss:Pass=2 xs=0.6mm"

    def test_error_messages(self):
        msg = driver.find_element(
            by=By.XPATH, value="/html/body/div/div/div/section/div[1]/div/div/div[2]/div/table/tbody/tr/td"
        )

        assert msg.text == "Design:Maxwell2DDesign1 Variation: xs=6.000000000e-01mm Setup: Setup1 has no mesh stats"
