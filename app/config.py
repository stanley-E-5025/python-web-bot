import sys
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


STEPS = {
    "title": "Recording 5/8/2023 at 5:12:58 PM",
    "steps": [
        {
            "type": "setViewport",
            "width": 1440,
            "height": 764,
            "deviceScaleFactor": 1,
            "isMobile": False,
            "hasTouch": False,
            "isLandscape": False,
        },
        {
            "type": "navigate",
            "url": "https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
                    "title": "Workbook: Open Data Regulatory Services - Violations",
                }
            ],
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["#tabZoneId1 div.tab-clip"],
                ['xpath///*[@id="tabZoneId1"]/div/div/div/div[1]'],
                ["pierce/#tabZoneId1 div.tab-clip"],
            ],
            "offsetY": 249,
            "offsetX": 734,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["div.QFLowerBound > div"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyQuantitativeDateQuickFilter_0"]/div/div[2]/div[1]/div'
                ],
                ["pierce/div.QFLowerBound > div"],
            ],
            "offsetY": 5,
            "offsetX": 33,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["body > span span > span"],
                ["xpath//html/body/span/div[3]/span/span"],
                ["pierce/body > span span > span"],
                ["text/5/8/2023"],
            ],
            "offsetY": 4.5,
            "offsetX": 30.28125,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["#tabZoneId6 div.tabComboBoxNameContainer"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_0"]/div/div[3]/span/div[1]'
                ],
                ["pierce/#tabZoneId6 div.tabComboBoxNameContainer"],
            ],
            "offsetY": 8,
            "offsetX": 141,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "#FI_federated\\.00w687c1maup7s1dd4wh40d7d2b6\\,none\\:Address\\:nk7677579796986060413_6318501153575507500_\\(All\\) input"
                ],
                [
                    'xpath///*[@id="FI_federated.00w687c1maup7s1dd4wh40d7d2b6,none:Address:nk7677579796986060413_6318501153575507500_(All)"]/div[2]/input'
                ],
                [
                    "pierce/#FI_federated\\.00w687c1maup7s1dd4wh40d7d2b6\\,none\\:Address\\:nk7677579796986060413_6318501153575507500_\\(All\\) input"
                ],
            ],
            "offsetY": 7,
            "offsetX": 8,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["button.apply > span.label"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_0_menu"]/div[3]/button[2]/span[2]'
                ],
                ["pierce/button.apply > span.label"],
                ["text/Apply"],
            ],
            "offsetY": 4,
            "offsetX": 45,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["#\\32 9035048760"],
                ['xpath///*[@id="29035048760"]'],
                ["pierce/#\\32 9035048760"],
            ],
            "offsetY": 28,
            "offsetX": 176,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["div.tab-toolbar"],
                ['xpath///*[@id="toolbar-container"]/div[1]'],
                ["pierce/div.tab-toolbar"],
            ],
            "offsetY": 15,
            "offsetX": 953,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["#download-ToolbarButton > span.tabToolbarButtonText"],
                ['xpath///*[@id="download-ToolbarButton"]/span[2]'],
                ["pierce/#download-ToolbarButton > span.tabToolbarButtonText"],
            ],
            "offsetY": 1.25,
            "offsetX": 3.9375,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["aria/Crosstab"],
                ["button:nth-of-type(3)"],
                [
                    'xpath///*[@id="DownloadDialog-Dialog-Body-Id"]/div/fieldset/button[3]'
                ],
                ["pierce/button:nth-of-type(3)"],
            ],
            "offsetY": 11,
            "offsetX": 119,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "div.f1lp596a > div > div > div:nth-of-type(1) > div > div > div > div"
                ],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[1]/div[2]/div/div/div[1]/div/div/div/div'
                ],
                [
                    "pierce/div.f1lp596a > div > div > div:nth-of-type(1) > div > div > div > div"
                ],
            ],
            "offsetY": 26.5,
            "offsetX": 19.5,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "div.f1lp596a > div > div > div:nth-of-type(2) > div > div > div > div"
                ],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div'
                ],
                [
                    "pierce/div.f1lp596a > div > div > div:nth-of-type(2) > div > div > div > div"
                ],
            ],
            "offsetY": 23.5,
            "offsetX": 15.5,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["label:nth-of-type(2)"],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[2]/div[2]/div/label[2]'
                ],
                ["pierce/label:nth-of-type(2)"],
            ],
            "offsetY": 8,
            "offsetX": 4.5703125,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["aria/Download Crosstab", "aria/Download"],
                [
                    "#export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id button"
                ],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[3]/button'
                ],
                [
                    "pierce/#export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id button"
                ],
            ],
            "offsetY": 10,
            "offsetX": 37.40625,
        },
    ],
}
