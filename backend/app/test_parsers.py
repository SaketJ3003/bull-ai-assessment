import os
import tempfile

from app.parsers.csv_parser import parse_csv
from app.parsers.txt_parser import parse_txt


def test_csv_parser():
    csv_content = """Year,Sales,EBITDA,PAT
FY25A,20243,637,527
FY26E,35020,1248,927
FY27E,54632,3575,2643
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline=""
    ) as file:
        file.write(csv_content)
        csv_path = file.name

    try:
        result = parse_csv(csv_path)

        assert "CSV COLUMNS:" in result
        assert "FY25A" in result
        assert "20243" in result
        assert "637" in result
        assert "527" in result

        print("CSV PARSER: SUCCESS")
        print(result)

    finally:
        os.remove(csv_path)


def test_txt_parser():
    txt_content = """
Company: Eternal Ltd.
Revenue FY25A: 20243
EBITDA FY25A: 637
Adjusted PAT FY25A: 527
"""

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8"
    ) as file:
        file.write(txt_content)
        txt_path = file.name

    try:
        result = parse_txt(txt_path)

        assert "Eternal Ltd." in result
        assert "20243" in result
        assert "637" in result
        assert "527" in result

        print("TXT PARSER: SUCCESS")
        print(result)

    finally:
        os.remove(txt_path)


if __name__ == "__main__":
    test_csv_parser()
    test_txt_parser()

    print("\nALL PARSER TESTS PASSED")