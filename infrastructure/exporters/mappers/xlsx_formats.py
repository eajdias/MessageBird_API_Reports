# Raw dicts for xlsxwriter formats.
# Based on legacy project standards for parity.

FMT_HEADER_BLUE = {
    "bold": True, "bg_color": "#004080", "font_color": "white",
    "border": 1, "font_size": 12, "align": "center", "valign": "vcenter",
}

FMT_HEADER_NAVY = {
    "bold": True, "bg_color": "#1F3864", "font_color": "white",
    "border": 1, "font_size": 12, "align": "center", "valign": "vcenter",
}

FMT_SECTION = {
    "bold": True, "bg_color": "#D9E1F2", "border": 1, "font_size": 11, "align": "left",
}

FMT_CELL = {
    "border": 1, "font_size": 11, "align": "left",
}

FMT_CELL_ALT = {
    "border": 1, "font_size": 11, "align": "left", "bg_color": "#EBF3FB",
}

FMT_TOTAL = {
    "bold": True, "bg_color": "#595959", "font_color": "white",
    "border": 1, "font_size": 11, "align": "left",
}

FMT_BSC_HEADER_KPI = {
    "bold": True, "bg_color": "#2E75B6", "font_color": "white",
    "border": 1, "font_size": 11, "align": "center", "valign": "vcenter",
}

FMT_BSC_KPI_CELL = {
    "bold": True, "border": 1, "font_size": 11, "align": "center",
    "font_color": "#1F5C99",
}

FMT_BSC_KPI_CELL_ALT = {
    "bold": True, "border": 1, "font_size": 11, "align": "center",
    "font_color": "#1F5C99", "bg_color": "#DDEEFF",
}

FMT_BSC_TOTAL_KPI = {
    "bold": True, "bg_color": "#375623", "font_color": "white",
    "border": 2, "font_size": 12, "align": "center",
}
