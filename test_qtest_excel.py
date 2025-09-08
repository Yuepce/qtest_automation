import os
import time
import pytest

# Keep the user's framework style: Excel-driven
import utils.excel_utils as ExcelUtils  # expects your existing Excel helper
from qtest_page import QTestPage

@pytest.mark.qtest
@pytest.mark.TC0014
def test_qtest_login(browser, request):
    """
    Excel-driven quick test:
      - Reads row TC0014 from empf_ui_automation_data.xlsx via ExcelUtils.get_data('TC0014')
      - Expects columns: URL, Execute Flag (Y/N)
    """
    data = ExcelUtils.get_data('TC0014')
    if not data:
        pytest.skip("No data found for TC0014 in Excel control sheet")

    if str(data.get('Execute Flag', data.get('Execute', 'N'))).strip().upper() != 'Y':
        pytest.skip("TC0014 Execute Flag != Y; skipping per control sheet")

    url = data.get('URL', 'https://sunlife.qtestnet.com')

    request.node.driver = browser
    qtest = QTestPage(browser)

    # 1) Open qTest
    browser.get(url)

    # 2) Login (hardcoded inside qtest_page.QTestPage.login for quick bring-up)
    qtest.login()
    time.sleep(3)  # initial settle; later can be removed if necessary

    assert qtest.is_logged_in(), "qTest login failed—check selectors or credentials"

    # Evidence
    os.makedirs("screenshots", exist_ok=True)
    screenshot_path = os.path.join(os.getcwd(), "screenshots", "TC0014.png")
    browser.save_screenshot(screenshot_path)
    try:
        request.node.add_report_section('test','Screenshot', f'<img src="{screenshot_path}">')
    except Exception:
        pass
