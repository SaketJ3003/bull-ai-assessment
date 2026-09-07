import pandas as pd


def parse_csv(file_path: str) -> str:
    """
    Read a financial CSV file and convert it into a
    structured text representation suitable for Gemini.
    """

    try:
        df = pd.read_csv(file_path)

    except Exception as exc:
        raise ValueError(
            f"Unable to read CSV file: {exc}"
        ) from exc

    if df.empty:
        raise ValueError("The CSV file is empty.")

    # Remove completely empty rows and columns.
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    if df.empty:
        raise ValueError("The CSV file contains no usable data.")

    # Convert NaN values to empty strings.
    df = df.fillna("")

    lines = []

    # Include column names.
    columns = [str(column).strip() for column in df.columns]

    lines.append(
        "CSV COLUMNS: " + " | ".join(columns)
    )

    lines.append("")
    lines.append("CSV DATA:")

    for index, row in df.iterrows():
        values = []

        for column in df.columns:
            value = row[column]

            if value == "":
                value_text = ""
            else:
                value_text = str(value).strip()

            values.append(
                f"{str(column).strip()}: {value_text}"
            )

        lines.append(
            f"Row {index + 1}: " + " | ".join(values)
        )

    return "\n".join(lines)