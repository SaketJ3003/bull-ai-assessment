from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph

from app.pdf.styles import TABLE_HEADER_STYLE, TABLE_CELL_STYLE


def cell(value):
    if value is None:
        value = "-"

    return Paragraph(str(value), TABLE_CELL_STYLE)


def header(value):
    if value is None:
        value = ""

    return Paragraph(str(value), TABLE_HEADER_STYLE)


def financial_table(headers, rows, col_widths=None, compact=True):
    data = [[header(item) for item in headers]]

    for row in rows:
        data.append([
            item if hasattr(item, "wrap") else cell(item)
            for item in row
        ])

    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1,
        hAlign="LEFT"
    )

    padding = 1.2 if compact else 3

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),

        ("LEFTPADDING", (0, 0), (-1, -1), padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]))

    return table


def key_value_table(items, columns=2):
    rows = []

    for i in range(0, len(items), columns):
        chunk = items[i:i + columns]

        row = []

        for label, value in chunk:
            row.append(header(label))
            row.append(cell(value))

        # Fill incomplete final row
        while len(row) < columns * 2:
            row.append("")
            row.append("")

        rows.append(row)

    # A4 usable width is ~194 mm.
    # Keep this table comfortably inside it.
    label_width = 22 * mm
    value_width = 26 * mm

    widths = [label_width, value_width] * columns

    # If the table is too wide, shrink proportionally.
    total_width = sum(widths)
    max_width = 190 * mm

    if total_width > max_width:
        scale = max_width / total_width
        widths = [width * scale for width in widths]

    table = Table(
        rows,
        colWidths=widths,
        hAlign="LEFT"
    )

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("LEFTPADDING", (0, 0), (-1, -1), 1.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.5),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))

    return table