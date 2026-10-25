REFERENCE = "グラフィック/リファレンス/フィルター/"

FILTERS = [
    ("new", "fNew", "fNews", "fNews", "New"),
    ("other", "fその他", "fその他s", "fその他s", "Other"),
    ("object", "fオブジェクト", "fオブジェクトs", "fobjects", "Object"),
    ("scenario", "fシナリオ", "fシナリオs", "fscenarios", "Scenario"),
    ("interrupted", "f中断", "f中断s", "f中断s", "Broken off"),
    ("letters", "f書簡", "f書簡s", "fletterss", "Letters"),
    ("complete", "f読了", "f読了s", "f読了s", "Complete"),
]

JOBS = [
    {
        "id": "ref-hover-" + identifier,
        "screen": "reference filter hover",
        "style": "serif",
        "erase": "inpaint",
        "pad": 2,
        "color": "#f5f5f5",
        "stroke": 1,
        "stroke_color": "#101010",
        "max_size": 20,
        "items": [(REFERENCE + selected + ".gal", wording)],
        "normal_path": REFERENCE + normal + ".gal",
        "runtime_path": REFERENCE + runtime + ".gal",
        "wording": "Accepted normal ref-filters labels in jobs_tierb.py",
    }
    for identifier, normal, selected, runtime, wording in FILTERS
]
