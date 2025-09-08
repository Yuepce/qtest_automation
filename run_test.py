import os
import pytest

if __name__ == "__main__":
    # Ensure screenshots folder exists
    os.makedirs("screenshots", exist_ok=True)

    # Run only the TC0014 / qtest test path
    exit_code = pytest.main([
        "-s",
        "-q",
        "-k", "TC0014 or qtest",
        "--html=report.html",
    ])
    raise SystemExit(exit_code)
