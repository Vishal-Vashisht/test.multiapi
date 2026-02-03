from flask import send_file

from collections.abc import MutableMapping
from io import BytesIO

import xlsxwriter
from .exceptions import ValidationError


def _normalize_data(obj, parent_key="", sep="_"):
    items = []
    for key, value in obj.items():
        if key == "count":
            continue
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(_normalize_data(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def _make_data(data: list):
    final_data = []
    for item in data:
        normalized_data = _normalize_data(item)
        final_data.append(normalized_data)
    return final_data


def generate_xls(data, header=None, title=None, _filters=None):
    """Generate XLS.

    Args:
    ----
        data: list of data
        header: headers
        title: title
        _filters:

    Returns:
    -------

    """
    if not _filters:
        _filters = {}
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet()
    _xls_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "white",
            "font_size": 9,
        },
    )
    workbook.add_format({"bold": True})
    row, col = 0, 0
    _cell_format = workbook.add_format()
    _cell_format.set_quote_prefix()
    _headers = header
    if not _headers:
        normalized_data = _make_data(data)
        if normalized_data:
            _headers = list(normalized_data[0].keys())
        data = normalized_data
    if not data:
        return output
    cols_number = len(_headers)
    if title:
        worksheet.merge_range(
            row,
            col,
            row,
            cols_number - 1,
            title,
            _xls_format,
        )
    if _filters:
        row += 1
        if isinstance(_filters, list):
            for _filter in _filters:
                for key, value in _filter.items():
                    worksheet.write(row, 0, f"{key}: {value}", _xls_format)
                    row += 1
        else:
            for key, value in _filters.items():
                worksheet.write(row, 0, f"{key}: {value}", _xls_format)
                row += 1
        row += 1
    for len_headers in range(cols_number):
        worksheet.write(row, len_headers, _headers[len_headers], _xls_format)
    row += 1
    for row_item in data:
        for item in _headers:
            worksheet.write(
                row,
                col,
                f"{row_item.get(item)}"
                if row_item.get(item) is not None
                else "",
                _cell_format,
            )
            col += 1
        row += 1
        col = 0
    workbook.close()
    return output


def _handle_export(
    export: str,
    body: dict,
    allow_filters: str | None = "true",
):
    """Handle export functionality in all apis."""
    _filters = body.get("filters") if allow_filters == "true" else {}
    data = body.get("results", [])
    title = body.get("title", "")
    if export == "xls":
        content_type = "application/vnd.ms-excel"
        buffer = generate_xls(
            data=data,
            title=title,
            _filters=_filters,
        )
    elif export == "xlsx":
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        buffer = generate_xls(
            data=data,
            title=title,
            _filters=_filters,
        )
    else:
        raise ValidationError(status=400, title="")
    file_name = f"export.{export}"
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype=content_type,
        as_attachment=True,
        download_name=file_name
    )