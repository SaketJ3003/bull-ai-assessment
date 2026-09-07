def parse_txt(file_path: str) -> str:
    """
    Read a TXT financial document and return its text
    for structured Gemini extraction.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            text = file.read()

    except Exception as exc:
        raise ValueError(
            f"Unable to read TXT file: {exc}"
        ) from exc

    text = text.strip()

    if not text:
        raise ValueError("The TXT file is empty.")

    return text