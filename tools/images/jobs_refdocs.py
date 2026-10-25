"""jobs_refdocs.py - the reference-document pictures (Japanese text baked into the picture) in English.
IMAGES3, 2026-10-01, per notes/IMAGES3-BRIEF.md. Same shape as jobs_tierb.py.

Run one job (or one reference's jobs) at a time:
    SY_TL_LOG=notes/_tmp/tl-log-IMAGES3.md PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run --no-project --with pylivemaker \
        --with numpy --with opencv-python-headless python tools/images/batch.py --jobs jobs_refdocs --only ID[,ID]
Previews: review/images/preview-refdocs/.

Method (IMAGE-LANE-PLAN "DONE / NEXT - REFERENCE DOCUMENTS"): mode="lines", one English string per box, printed
text = serif (Cambria), handwritten values = handwriting (Ink Free) in a second job with chain=True; flat white
fill per box on white paper (table rules stay because boxes sit between them), inpaint of the glyph pixels
(mask_color) on coloured or textured ground. Line opts: see batch.py ("IMAGES3 2026-10-01").
Flip-animation frames are built by refdoc_flip.py and 概要 previews by refdoc_overview.py build; both ship
through mode="asis" (chain=True).
Wording: names / places from notes/v2/GLOSSARY.tsv `en` and the shipped English (Motoki-cho, Sawa Prefecture,
Chuo Park, Megasawa City, Motoki Prefectural High School, Revo Heights); dates per STYLE.md CALENDAR.
Reference 95 was shipped earlier by refdoc95.py (FIX1/FIX2, owner-checked); it has no job here.
"""
D = "グラフィック/リファレンス/リファレンス詳細/"
O = "グラフィック/リファレンス/リファレンス概要/"
DARK = [0, 110, 0, 110, 0, 110]          # black / dark-grey glyph pixels
INK = "#111111"


def idcard_front(name, born, room):
    """the two student ID fronts share one layout (65 = 0.png 420x258, 66 = 0.png 420x257)."""
    ip = {"method": "inpaint", "mask_color": DARK, "mask_grow": 3}
    return [
        ("STUDENT ID", [96, 5, 324, 37], dict(ip, align="center", max_size=24)),
        ("Student No.", [10, 50, 89, 68]),
        ("Name", [10, 73, 89, 90]),
        (name, [93, 73, 298, 90]),
        ("Date of birth", [10, 96, 89, 113]),
        (born, [93, 96, 298, 113]),
        ("Address", [10, 118, 89, 135]),
        ("120-10 Nagaminedai, Motoki-cho, Sawa Prefecture", [93, 118, 298, 135]),
        ("Revo Heights Room %s" % room, [93, 141, 298, 158]),
        ("This certifies that the above person is a student of this school.", [10, 163, 298, 186]),
        ("Shiyo 800, April 1", [8, 190, 104, 210]),
        ("Principal  Hitoshi Hanayama", [106, 190, 298, 210]),
        ("Motoki Prefectural High School", [64, 219, 268, 255], dict(ip, align="center", max_size=17)),
        ("119-1 Nakadate, Motoki-cho,\nSawa Prefecture", [268, 222, 418, 254], dict(ip, max_size=11)),
    ]


def idcard_pink(lines):
    """IMAGES3E (66), IMAGES5b (65, same band): the band glyphs are dark purple (R 21-199, G 0-119, band 255,155,205); DARK (all <= 110)
    missed the whole address line, so the English address sat on the Japanese one. Widen school + address masks."""
    m = {"mask_color": [0, 255, 0, 130, 0, 190], "mask_grow": 3}
    return lines[:-2] + [(t, b, dict(o, **m)) for t, b, o in lines[-2:]]


def idback(ip):
    """the two backs share one layout; ip = erase opts (66: inpaint, keeps the stain; 65: flat, sticker protected)."""
    return [
    ("― Notes ―", [110, 60, 310, 96], dict(ip, align="center", max_size=22)),
    ("This card may not be lent or transferred to anyone else.", [26, 115, 324, 134],
     dict(ip, erase=[[24, 113, 325, 226]])),
    ("Carry this card at all times.", [26, 134, 324, 151], {"erase": []}),
    ("If this card is lost or damaged, or any details on it\nchange, report it immediately.", [26, 151, 324, 187],
     {"erase": []}),
    ("For other school rules, access the QR code on the\nright and check them.", [26, 187, 324, 222],
     {"erase": []}),
    ]


IP = {"method": "inpaint", "mask_color": DARK, "mask_grow": 3}

JOBS = [
    # ---- 65 / 66 student ID cards (front 0.png, back 1.png; flip frames 0→1 / 1→0) ----
    {"id": "ref65-front", "screen": "reference 65 detail", "style": "serif", "mode": "lines", "erase": "flat",
     "color": INK, "max_size": 11, "new": True, "note": "student ID front",
     "items": [(D + "rrr65/0.gal", "")],
     "lines": idcard_pink(idcard_front("Natsumi Kogori", "Shiyo 783, July 29", "305"))},
    {"id": "ref65-back", "screen": "reference 65 detail", "style": "serif", "mode": "lines", "erase": "flat",
     "color": INK, "max_size": 11, "new": True, "note": "student ID back; the photo sticker is kept on top",
     "items": [(D + "rrr65/1.gal", "")], "protect": [[59, 91, 162, 249]],
     "lines": idback({})},
    {"id": "ref65-sticker", "screen": "reference 65 detail", "style": "handwriting", "mode": "lines",
     "erase": "inpaint", "chain": True, "color": INK, "max_size": 7, "new": True,
     "note": "marker writing on the photo sticker (5 px in the original)",
     "items": [(D + "rrr65/1.gal", "")],
     "lines": [("Goto's here", [74, 114, 124, 128], {"mask_color": DARK, "mask_grow": 2,
                                                       "erase": [[74, 114, 124, 143]]}),
               ("way too tiny lol", [74, 128, 124, 143], {"erase": []})]},
    {"id": "ref65-zoom", "screen": "reference 65 close-up", "style": "handwriting", "mode": "lines",
     "erase": "inpaint", "color": INK, "max_size": 17, "new": True, "note": "sticker close-up",
     "items": [(D + "rrr65/部分拡大1.gal", "")], "protect": [[20, 30, 28, 110]],
     "lines": [("Goto's here", [16, 48, 100, 72], {"mask_color": DARK, "mask_grow": 3,
                                                     "erase": [[14, 46, 134, 100]]}),
               ("way too tiny lol", [16, 74, 134, 98], {"erase": []})]},
    {"id": "ref66-front", "screen": "reference 66 detail", "style": "serif", "mode": "lines", "erase": "flat",
     "color": INK, "max_size": 11, "new": True, "note": "student ID front",
     "items": [(D + "rrr66/0.gal", "")],
     "lines": idcard_pink(idcard_front("Haruka Niimura", "Shiyo 782, April 30", "306"))},
    {"id": "ref66-back", "screen": "reference 66 detail", "style": "serif", "mode": "lines", "erase": "flat",
     "color": INK, "max_size": 11, "new": True, "note": "student ID back (stain kept: inpaint of the glyphs only)",
     "items": [(D + "rrr66/1.gal", "")],
     "lines": idback(IP)},
    {"id": "ref65-flip", "screen": "reference 65 flip frames", "style": "serif", "mode": "asis", "chain": True,
     "items": [(D + "rrr65/0→1.gal", ""), (D + "rrr65/1→0.gal", "")]},
    {"id": "ref65-stripe", "screen": "reference 65 flip frame", "style": "serif", "mode": "lines", "chain": True,
     "erase": "inpaint", "color": "#6e6e6e", "max_size": 7, "new": True,
     "note": "photo-sticker print on the glare stripe of the flip frame (date already Latin, kept)",
     "items": [(D + "rrr65/1→0.gal", "")],
     "lines": [("3 good friends", [124, 199, 166, 229], {"mask_color": [60, 185, 60, 185, 60, 185], "mask_grow": 2,
                                                          "erase": [[126, 203, 163, 225]], "rot": 20, "rot_h": 9})]},
    {"id": "ref66-flip", "screen": "reference 66 flip frames", "style": "serif", "mode": "asis", "chain": True,
     "items": [(D + "rrr66/0→1.gal", ""), (D + "rrr66/1→0.gal", "")]},
    # ---- 概要 previews rebuilt from the English detail (refdoc_overview.py build <ID>, probe < 12) ----
    {"id": "ov-65-66", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr65.gal", ""), (O + "rr66.gal", "")]},
]


def deathcert(v):
    """the two death certificates (13 = 1000x1416, 71 = 1000x1415) share one printed form (別紙様式13).
    One job per picture, printed labels serif, handwritten values Ink Free (per-line style), erase_first +
    text_only: only glyph pixels are repainted white, table rules and the red seal stay. v = the values;
    v["circle"] = names of the printed choices circled by hand (71); the circle is redrawn round the English."""
    H = {"style": "handwriting"}
    c = v.get("circle", set())

    def ch(key, ell):
        return {"ellipse": ell} if key in c else {}
    return [
        ("Appended Form 13", [690, 62, 900, 92], {"align": "right", "max_size": 18}),
        ("DEATH CERTIFICATE", [300, 110, 700, 152], {"align": "center", "max_size": 26}),
        ("Name", [97, 165, 176, 206], {"align": "center"}),
        (v["name"], [186, 166, 412, 210], dict(H, max_size=26)),
        ("1. Male", [425, 166, 511, 186], ch("male", [421, 166, 470, 187])),
        ("2. Female", [425, 186, 511, 206]),
        ("Date of birth", [515, 166, 606, 206], {"align": "center"}),
        ("Shiyo", [626, 172, 684, 202]),
        (v["born"], [686, 168, 900, 204], dict(H, max_size=22)),
        ("Time of death", [97, 214, 176, 246], {"align": "center", "max_size": 10}),
        ("Shiyo", [186, 216, 244, 244]),
        (v["died"], [244, 214, 455, 246], dict(H, max_size=22)),
        ("a.m.", [458, 216, 502, 244], dict(ch("am", [458, 218, 500, 242]), erase=[[456, 214, 503, 246]])),
        ("p.m.", [503, 216, 548, 244]),
        (v["time"], [552, 214, 720, 246], dict(H, max_size=22)),
        ("Place of death and its type", [97, 252, 176, 350], {"align": "center", "max_size": 10}),
        ("Type of place of death", [182, 252, 415, 281]),
        ("1 Hospital   2 Clinic   3 Long-term care facility   4 Maternity home   5 Nursing home   6 Home",
         [424, 252, 832, 281], {"max_size": 10}),
        ("7 Other", [842, 252, 904, 281], dict(ch("other7", [838, 255, 904, 279]), max_size=10, erase=[[832, 252, 905, 282]])),
        ("Place of death (address)", [182, 285, 415, 317]),
        ("1-1 Shirogaoka, Motoki-cho, Sawa Prefecture", [424, 284, 904, 318], dict(H, max_size=24)),
        ("Name of facility", [182, 321, 415, 352]),
        ("Chuo Park", [424, 320, 640, 353], dict(H, max_size=24)),
        ("Cause of death", [97, 358, 176, 379], {"max_size": 10}),
        ("◆In both I and II, do not write heart failure, respiratory failure, etc. as the terminal state "
         "of a disease.", [96, 381, 177, 457], {"max_size": 8}),
        ("◆In I, write the injuries or diseases that most affected the death, in order of medical cause "
         "and effect.", [96, 463, 177, 540], {"max_size": 8}),
        ("◆In I, write one injury or disease per line.", [96, 551, 177, 593], {"max_size": 8}),
        ("If there are not enough lines, write the rest in (d), in order of medical cause and effect.",
         [96, 603, 177, 680], {"max_size": 8}),
        ("(a) Direct cause", [227, 360, 326, 398], {"max_size": 10}),
        ("(b) Cause of (a)", [227, 406, 326, 446], {"max_size": 10}),
        ("(c) Cause of (b)", [227, 453, 326, 494], {"max_size": 10}),
        ("(d) Cause of (c)", [227, 501, 326, 542], {"max_size": 10}),
        ("Injuries or diseases not related to the direct cause but affecting the course in I",
         [227, 550, 326, 602], {"max_size": 8}),
        (v["a"], [332, 360, 640, 401], dict(H, max_size=22)),
        (v["b"], [332, 406, 640, 447], dict(H, max_size=22)),
        (v["c"], [332, 453, 640, 494], dict(H, max_size=22)),
        (v["d"], [332, 500, 640, 542], dict(H, max_size=22)),
        ("See remarks", [332, 550, 640, 601], dict(H, max_size=22)),
        ("Period from onset (or injury) to death", [645, 362, 724, 424], {"max_size": 9}),
        ("◆Write in years, months, days, etc. If under 1 day, write in hours, minutes, etc. "
         "(e.g. 1 year 3 months, 5 hours 30 minutes)", [645, 435, 725, 553], {"max_size": 8}),
        ("Surgery", [182, 610, 237, 648], {"align": "center"}),
        ("1 No", [240, 612, 288, 646], ch("surg1", [238, 616, 284, 642])),
        ("2 Yes", [290, 612, 342, 646]),
        ("Date of surgery", [648, 610, 728, 648], {"max_size": 10}),
        ("Shiyo", [729, 632, 772, 654], {"max_size": 10}),
        ("year", [784, 632, 830, 654], {"align": "center", "max_size": 10}),
        ("month", [831, 632, 870, 654], {"align": "center", "max_size": 10}),
        ("day", [872, 632, 904, 654], {"align": "center", "max_size": 10}),
        ("Autopsy", [182, 656, 237, 694], {"align": "center"}),
        ("1 No", [240, 658, 288, 692]),
        ("2 Yes", [290, 658, 342, 692], ch("aut2", [287, 662, 334, 688])),
        ("Type of cause of death", [97, 700, 176, 724], {"max_size": 9}),
        ("1 Death from illness or natural causes", [182, 700, 520, 722]),
        ("External cause", [180, 725, 241, 747], dict(ch("ext", [178, 724, 243, 749]), max_size=10)),
        ("Accidental external cause", [243, 725, 520, 747]),
        ("[ 2 Traffic accident   3 Fall   4 Drowning   5 Injury from smoke, fire or flames   6 Suffocation   "
         "7 Poisoning   8 Other ]", [268, 745, 902, 768], {"max_size": 11}),
        ("Other and unknown external causes", [243, 777, 560, 798]),
        ("[ 9 Suicide", [268, 799, 328, 822], {"max_size": 11}),
        ("10 Homicide", [332, 799, 400, 822], dict(ch("homi", [328, 799, 402, 822]), max_size=11, erase=[[322, 797, 404, 827]])),
        ("11 Other and unknown external cause   12 Unknown death ]", [404, 799, 760, 822], {"max_size": 11}),
        ("Additional items for unnatural death", [97, 842, 176, 890], {"max_size": 9}),
        ("◆Write even if the information is hearsay or an estimate.", [96, 892, 177, 932], {"max_size": 8}),
        ("When the injury occurred", [182, 844, 334, 873], {"max_size": 11}),
        ("Shiyo", [338, 846, 377, 870], {"max_size": 10}),
        (v["inj_date"], [378, 845, 498, 871], dict(H, max_size=16)),
        ("a.m.", [499, 848, 526, 869], dict(ch("am2", [496, 846, 528, 870]), max_size=10, erase=[[491, 842, 535, 872]])),
        ("p.m.", [528, 848, 556, 869], {"max_size": 10}),
        (v["inj_time"], [558, 845, 640, 871], dict(H, max_size=16)),
        ("Type of place where the injury occurred", [182, 880, 334, 921], {"max_size": 11}),
        ("1 Residence   2 Factory or construction site   3 Road", [338, 885, 512, 921], {"max_size": 10}),
        ("4 Other (", [514, 885, 562, 921], dict(ch("other4", [510, 889, 552, 917]), max_size=10, erase=[[505, 885, 562, 921]])),
        ("park", [562, 883, 620, 921], dict(H, max_size=16)),
        (")", [621, 885, 640, 921], {"max_size": 10}),
        ("Place where the injury occurred", [646, 860, 724, 905], {"max_size": 10}),
        ("Chuo Park", [728, 866, 904, 910], dict(H, max_size=24)),
        ("Means and circumstances", [182, 928, 420, 951], {"max_size": 11}),
        ("See the cause-of-death section", [184, 956, 640, 998], dict(H, max_size=24)),
        ("Other remarks", [97, 1004, 400, 1020], {"max_size": 9}),
        (v["remarks"], v["remarks_box"], dict(H, max_size=v.get("remarks_size", 24), line_spacing=1.0)),
        ("Diagnosed as above.", [97, 1086, 400, 1106], {"max_size": 11}),
        ("Date of diagnosis   Shiyo", [600, 1088, 796, 1106], {"align": "right", "max_size": 9}),
        (v["diag"], [798, 1086, 904, 1107], dict(H, max_size=12)),
        ("Date this certificate was issued   Shiyo", [560, 1109, 796, 1127], {"align": "right", "max_size": 9}),
        (v["issued"], [798, 1108, 904, 1128], dict(H, max_size=12)),
        ("Name and address of the hospital, clinic or care facility, or the doctor's address",
         [97, 1143, 245, 1197], {"max_size": 9}),
        ("(Name)", [140, 1199, 205, 1219], {"max_size": 10}),
        ("Physician", [233, 1199, 306, 1219], {"max_size": 10}),
        ("Motoki First Hospital", [252, 1143, 640, 1166], dict(H, max_size=18)),
        ("1-12 Sakuramoto-cho, Motoki-cho, Sawa Prefecture", [252, 1166, 640, 1187], dict(H, max_size=18)),
        (v["doctor"], [312, 1192, 640, 1233], dict(H, max_size=28)),
        ("(Note) A death certificate issued by a hospital or clinic is also acceptable, but please submit "
         "this certificate wherever possible.", [97, 1240, 904, 1267], {"max_size": 13}),
    ]


DC13 = dict(name="Eiichiro Niimura", born="757, May 27", died="790, April 8", time="12:00",
            a="Death from hemorrhagic shock", b="Laceration of the main artery of the neck",
            c="A metal spike pierced the neck", d="Fall from a tree", inj_date="790, April 8", inj_time="12:00",
            remarks="A more detailed autopsy of the body is needed. Suspected drug poisoning.",
            remarks_box=[100, 1024, 904, 1080], diag="790, April 8", issued="790, April 9",
            doctor="Tadashi Nakamoto")
DC71 = dict(name="Ryoji Kogori", born="757, June 11", died="800, April 8", time="5:30",
            a="Death from hemorrhagic shock", b="Laceration of the main artery of the neck",
            c="Lacerations by crows", d="Skin flayed from the whole body", inj_date="800, April 8",
            inj_time="5:30",
            remarks="Very likely still alive when first found. Pieces of rubber found under the nails. The flaying "
                    "site is thought to have been a place where rubber sheeting was laid. No reaction to drugs or "
                    "the like. A fresh internal bruise, unlike the flaying, was found on the side of the neck; it is "
                    "extremely likely he was made to lose consciousness by a blow to the cervical spine.",
            remarks_box=[98, 1020, 904, 1084], remarks_size=17, diag="800, April 8", issued="800, April 8",
            doctor="Mikako Nakamoto",
            circle={"male", "am", "other7", "surg1", "aut2", "ext", "homi", "am2", "other4"})
DC_KEEP = [[190, 440, 212, 460], [190, 565, 212, 584], [696, 1180, 768, 1238]]   # I, II, the red seal (kept)
JOBS += [
    {"id": "ref13", "screen": "reference 13 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "max_size": 12, "new": True,
     "note": "death certificate (printed form serif, entries Ink Free; seal kept)",
     "items": [(D + "rrr13/0.gal", "")], "lines": deathcert(DC13), "ignore": DC_KEEP},
    {"id": "ref71", "screen": "reference 71 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "max_size": 12, "new": True,
     "note": "death certificate (printed form serif, entries Ink Free; hand circles redrawn round the English)",
     "items": [(D + "rrr71/0.gal", "")], "lines": deathcert(DC71), "ignore": DC_KEEP},
]


# ---- 32 CV (800x2521): printed form serif, entries Ink Free; Latin digits / phone numbers kept as drawn ----
_H = {"style": "handwriting"}
CV_LINES = [
    ("RESUME", [38, 90, 240, 127], {"max_size": 26}),
    ("As of  Shiyo", [240, 96, 340, 122], {"align": "right", "max_size": 14}),
    ("795, December 3", [344, 94, 540, 123], dict(_H, max_size=18)),
    ("Reading", [42, 124, 138, 142], {"max_size": 10}),
    ("Momoko Goto", [140, 123, 400, 143], dict(_H, max_size=12)),
    ("Name", [40, 142, 120, 161], {"max_size": 12}),
    ("Momoko Goto", [50, 162, 470, 222], dict(_H, max_size=46)),
    ("Date of birth", [42, 222, 200, 241], {"max_size": 12}),
    ("Sex", [474, 222, 536, 241], {"max_size": 12}),
    ("Shiyo", [80, 248, 131, 272], {"max_size": 13}),
    ("780, March 3", [132, 245, 334, 273], dict(_H, max_size=18)),
    ("(age", [336, 248, 384, 272], {"align": "right", "max_size": 15}),
    (")", [409, 248, 446, 272], {"max_size": 15}),
    ("Female", [480, 246, 537, 273], dict(_H, max_size=15)),
    ("Reading", [42, 280, 100, 298], {"max_size": 10}),
    ("Sawa-ken Motoki-cho Shirogaoka 1-20", [102, 279, 600, 298], dict(_H, max_size=11)),
    ("Current address", [40, 298, 200, 317], {"max_size": 12}),
    ("1-20 Shirogaoka, Motoki-cho, Sawa Prefecture", [44, 327, 600, 361], dict(_H, max_size=20)),
    ("Phone", [617, 277, 700, 297], {"max_size": 12}),
    ("Mobile", [617, 320, 700, 339], {"max_size": 12}),
    ("Reading", [43, 369, 140, 387], {"max_size": 10}),
    ("Contact address  (postcode)", [42, 389, 250, 407], {"max_size": 12}),
    ("(Fill in only if you wish to be contacted somewhere other than your current address)",
     [255, 389, 612, 407], {"max_size": 10}),
    ("c/o", [596, 421, 622, 441], {"max_size": 11}),
    ("Year", [56, 455, 108, 475], {"align": "center", "max_size": 11}),
    ("Mo.", [111, 455, 144, 475], {"align": "center", "max_size": 11}),
    ("Education / Work history (list each separately)", [150, 455, 745, 475], {"align": "center", "max_size": 11}),
    ("Entered Motoki Elementary School", [148, 482, 745, 516], dict(_H, max_size=21)),
    ("Graduated from Motoki Elementary School", [148, 522, 745, 556], dict(_H, max_size=21)),
    ("Entered Motoki Junior High School", [148, 562, 745, 596], dict(_H, max_size=21)),
    ("Graduated from Motoki Junior High School", [148, 602, 745, 636], dict(_H, max_size=21)),
    ("Entered Motoki High School", [148, 642, 745, 676], dict(_H, max_size=21)),
    ("Dropped out of Motoki High School", [148, 682, 745, 716], dict(_H, max_size=21)),
    ("End", [148, 722, 745, 756], dict(_H, max_size=21)),
    ("Year", [56, 1352, 108, 1378], {"align": "center", "max_size": 11}),
    ("Mo.", [111, 1352, 144, 1378], {"align": "center", "max_size": 11}),
    ("Education / Work history (list each separately)", [150, 1352, 745, 1378], {"align": "center", "max_size": 11}),
    ("Year", [56, 1600, 108, 1626], {"align": "center", "max_size": 11}),
    ("Mo.", [111, 1600, 144, 1626], {"align": "center", "max_size": 11}),
    ("Licenses / Qualifications", [150, 1600, 745, 1626], {"align": "center", "max_size": 11}),
    ("Passed English Proficiency Test Grade 2", [160, 1632, 745, 1668], dict(_H, max_size=21)),
    ("Passed Kanji Proficiency Test Grade Pre-1", [160, 1676, 745, 1712], dict(_H, max_size=21)),
    ("Reasons for applying, special skills, favorite subjects, etc.", [40, 1855, 525, 1877], {"max_size": 11}),
    ("Commute", [528, 1856, 620, 1877], {"max_size": 11}),
    ("15 min", [636, 1862, 745, 1899], dict(_H, max_size=24)),
    ("Dependents (excluding spouse)", [528, 1899, 750, 1919], {"max_size": 10}),
    ("", [733, 1926, 754, 1948]),
    ("Spouse", [528, 1946, 615, 1967], {"max_size": 11}),
    ("Spouse's support obligation", [617, 1946, 752, 1967], {"max_size": 9}),
    ("I want to gain enough money and skills to become independent soon.", [44, 1899, 525, 1926],
     dict(_H, max_size=16)),
    ("Basically, I have no problem with customer service.", [44, 1926, 525, 1951], dict(_H, max_size=16)),
    ("Personal requests (fill in especially if you have wishes about salary, job type, working hours, "
     "place of work or anything else)", [40, 2010, 745, 2033], {"max_size": 10}),
    ("I can work regardless of the day or time. I would be grateful if you could give me", [44, 2049, 745, 2081],
     dict(_H, max_size=19)),
    ("as many shifts as possible.", [44, 2092, 745, 2124], dict(_H, max_size=19)),
]
JOBS += [
    {"id": "ref32", "screen": "reference 32 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "max_size": 12, "new": True,
     "note": "CV (printed form serif, entries Ink Free; digits and phone numbers kept)",
     "items": [(D + "rrr32/0.gal", "")], "lines": CV_LINES},
]


# ---- 4 investigation report (800x2253, typed): all serif; the photo is kept ----
_B = {"max_size": 13, "line_spacing": 1.15}
# IMAGES3D: body text inside the drawn box (vertical rules at x 67-69 and 717-718 in the source) + 8 px
R4X0, R4X1 = 77, 709
R4_LINES = [
    ("Investigation Report on the Victim's Belongings", [90, 86, 710, 127], {"align": "center", "max_size": 26}),
    ("Shiyo 800, April 20", [420, 134, 736, 158], {"align": "right", "max_size": 16}),
    ("Sawa Prefectural Police, Forensic Science Group", [300, 158, 736, 181], {"align": "right", "max_size": 16}),
    ("1. Subject of investigation", [50, 211, 420, 233], {"max_size": 15}),
    ("Investigation of the smartphone owned by the victim, a girl, in the recent attempted murder of a "
     "high-school girl on the Sakuraoka road.", [R4X0, 237, R4X1, 280], dict(_B, erase=[[56, 237, 732, 280]])),
    ("2. Reason for investigation", [50, 335, 420, 357], {"max_size": 15}),
    ("Because puzzling points were found in the smartphone owned by the girl.", [R4X0, 359, R4X1, 400], dict(_B, erase=[[56, 359, 732, 400]])),
    ("3. Details of investigation", [50, 459, 420, 481], {"max_size": 15}),
    ("The smartphone under investigation had been broken inside the girl's pocket. The girl is believed to "
     "have been hit by a car driven by the suspect, and the smartphone is thought to have been broken at "
     "that time.", [R4X0, 483, R4X1, 550], dict(_B, erase=[[56, 483, 732, 550]])),
    ("4. Results of investigation", [50, 582, 420, 604], {"max_size": 15}),
    ("The smartphone was broken inside the pocket and cannot be started. As the storage device was also "
     "broken, the installed apps and the usage cannot be checked. When the communication status was "
     "checked with the carrier, some kind of packet communication had been going on constantly (whether "
     "this is due to the smartphone's security-check function is still under investigation).",
     [R4X0, 606, R4X1, 702], dict(_B, erase=[[52, 605, 734, 977]])),
    ("A soft alloy with insulation treatment, weighing about 10 grams, was also found in the girl's pocket. "
     "Whether it was in the pocket from the start or inside the smartphone is unknown (when asked, the maker "
     "said that this model contains no such alloy). The girl's smartphone weighs 150 grams, which matches "
     "the maker's specifications. In other words, this insulated alloy may have been in the pocket on its "
     "own from the start.", [R4X0, 706, R4X1, 846], dict(_B, erase=[])),
    ("The smartphone's battery is very old and lasts only about half as long as a new one. The girl's "
     "smartphone had only just been released, so its battery could not have aged this much. From the "
     "above, it is thought that the girl's smartphone had been tampered with in some way.",
     [R4X0, 850, R4X1, 975], dict(_B, erase=[])),
    ("Metal fragment found in the girl's pocket (composition under investigation).", [146, 1540, 660, 1560],
     {"max_size": 15}),
    ("About 50 mm long, 15 mm wide, 1-2 mm thick", [146, 1560, 660, 1582], {"max_size": 15}),
    ("4. Observations", [50, 1617, 420, 1639], {"max_size": 15}),
    ("A battery normally cannot be replaced except at a service center, so it is almost certain that the "
     "smartphone had been tampered with in some way (there is no chance that the girl replaced the battery "
     "herself). However, from the culprit's point of view no advantage can be found in swapping the battery "
     "for an old one, and the possibility that it got in by mistake at the manufacturing stage cannot be "
     "ruled out.", [R4X0, 1643, R4X1, 1740], dict(_B, erase=[[52, 1642, 734, 1966]])),
    ("As for the insulated alloy as well, it is unknown whether the girl simply had it in her pocket or "
     "whether it had been tampered with and built into the casing, like the battery. Even if it was built "
     "in, there is no sign that it blocked any current inside; it was simply inside the smartphone.",
     [R4X0, 1744, R4X1, 1838], dict(_B, erase=[])),
    ("From the above, it is highly likely that the girl put the alloy in her pocket for some reason and, "
     "in addition, that the wrong battery was fitted while the smartphone was being made. However, it is "
     "still too early to put all of this down to coincidence, so the investigation will be continued.",
     [R4X0, 1842, R4X1, 1965], dict(_B, erase=[])),
]
JOBS += [
    {"id": "ref4", "screen": "reference 4 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "max_size": 13, "new": True,
     "note": "investigation report (typed; photo kept)", "ignore": [[150, 1265, 600, 1535]],
     "items": [(D + "rrr4/0.gal", "")], "lines": R4_LINES},
]


# ---- 34 Motoki Station timetable (0.png 835x987) + route map (1.png 982x835) + flip frames 2..17 ----
# 0.png: the 152 destination marks 女/大/西 above the times were replaced by refdoc_marks.py first
# (M = Megasawa, O = Otani, W = West Sawa); this job chains on that output.
_WH = [200, 255, 200, 255, 200, 255]
_WI = {"method": "inpaint", "mask_color": _WH, "mask_grow": 3, "color": "#ffffff"}
TT_LINES = [
    ("Sawa-Iizawa Line   Motoki Station Timetable [Outbound]", [6, 6, 500, 46], {"max_size": 22,
     # IMAGES3D: grey anti-aliased title glyphs (x 10-382, y 15-38) escaped the thr-60 mask
     "mask_color": [0, 215, 0, 215, 0, 215], "mask_grow": 5, "erase": [[8, 14, 385, 40]]}),
    # IMAGES3E: the date (Latin, kept) ends at x 608; Japanese header after it x 629-801 y 15-38
    ("timetable revision (copy)", [616, 6, 832, 46], {"max_size": 20, "align": "right",
     "mask_color": [0, 215, 0, 215, 0, 215], "mask_grow": 5, "erase": [[627, 13, 803, 40]]}),
    ("Sat. & Holidays   for West Sawa, Otani, Megasawa", [8, 66, 356, 97],
     # IMAGES3D: glyphs are white-to-pink (G 176-255) with dark edges, x 18-352 y 73-91 on the red band
     dict(_WI, max_size=17, mask_color=[150, 255, 60, 255, 40, 255], mask_grow=5, erase=[[16, 71, 355, 93]])),
    ("Hr", [360, 66, 401, 97], dict(_WI, align="center", max_size=17)),
    ("Weekdays   for West Sawa, Otani, Megasawa", [406, 66, 832, 97], dict(_WI, max_size=17)),
    ("Black: Local", [576, 420, 690, 466], {"max_size": 13, "align": "center"}),
    ("Red: Express", [576, 478, 690, 524], {"max_size": 13, "align": "center", "color": "#e00000"}),
    ("Purple: Commuter Express", [576, 536, 690, 600], {"max_size": 13, "align": "center", "color": "#7030a0",
                                                         "erase": [[574, 408, 692, 634]]}),
    ("W: for West Sawa", [704, 424, 816, 468], {"max_size": 13, "align": "center"}),
    ("O: for Otani", [704, 476, 816, 520], {"max_size": 13, "align": "center"}),
    ("M: for Megasawa", [704, 528, 816, 572], {"max_size": 13, "align": "center", "erase": [[702, 408, 818, 598]]}),
]
_STATIONS = [  # (x0, x1 of the name column, bottom, English)
    (14, 31, 262, "Megasawa"), (40, 57, 284, "East Megasawa"), (66, 83, 348, "Megasawa Seaside Park"),
    (92, 109, 284, "East Iizawayama"), (119, 135, 241, "Kotoba"), (145, 162, 263, "Rakuyoji"),
    (171, 188, 241, "Shin-Ike"), (197, 214, 263, "Shin-Ike South"), (223, 240, 263, "Shin-Ike East"),
    (249, 266, 241, "Takasato"), (275, 293, 263, "Kami-Takasato"), (302, 318, 241, "Otani"),
    (327, 345, 369, "Iizawa Cable Car"), (354, 370, 241, "Ainaka"), (379, 397, 241, "Sakaibashi"),
    (406, 423, 369, "Sakuraoka Cable Car"), (432, 449, 241, "Sakuraoka"), (458, 475, 306, "West Sawa Kawanaka"),
    (485, 502, 411, "Toyo Urban Plant"), (510, 527, 262, "West Sawa"), (537, 553, 326, "Toyo Urban"),
    (563, 580, 305, "Hanamigaoka West"), (589, 606, 283, "Hanamigaoka"), (615, 631, 262, "Itoshigawa"),
    (641, 658, 327, "Ryoku Beer Garden"), (667, 684, 283, "Motokiyama West"), (693, 710, 284, "Motokiyama East"),
    (719, 736, 284, "Motoki Cemetery"), (745, 762, 241, "Motoki"), (771, 788, 263, "Sakuranada"),
    (797, 814, 348, "Sawa Valley Park"), (824, 840, 241, "Oyama"), (850, 867, 369, "Old Sawa Road Post Town"),
    (876, 893, 242, "Shukuba"), (902, 919, 390, "Taiyo Kosan Ground"), (928, 945, 306, "Minakami-Nakanocho"),
    (955, 971, 282, "Sawa-Minakami"),
]
MAP_LINES = [(name, [x0 - 4, 202, x1 + 4, 430 if x0 < 714 or x0 > 819 else 372],
              {"rot": -90, "max_size": 14, "erase": [[x0 - 3, 201, x1 + 3, b + 4]]})
             for x0, x1, b, name in _STATIONS] + [
    ("Excursion Boat Link Line", [90, 50, 244, 84], {"max_size": 16}),
    ("Takasato Line", [272, 50, 420, 84], {"max_size": 16}),
    ("Future Trolley Line", [822, 50, 980, 84], {"max_size": 16}),
    # IMAGES3E: legend keys are solid boxes (red y 375-396, purple 401-423, black 427-448, x 714-818): flat fill of
    # the inner rectangle with the box colour measured on the source
    ("Express", [716, 376, 818, 397], dict(_WI, max_size=14, method="flat", bg="#f90306", no_rules=True,
                                           erase=[[715, 376, 818, 396]])),
    ("Commuter Express", [716, 402, 818, 423], dict(_WI, max_size=14, method="flat", bg="#6e2fa0", no_rules=True,
                                                     erase=[[715, 402, 818, 423]])),
    ("Local", [716, 428, 818, 449], dict(_WI, max_size=14, method="flat", bg="#010101", no_rules=True,
                                         erase=[[715, 428, 818, 448]])),
    ("← Iizawa Pref.", [240, 451, 372, 475], {"align": "right", "max_size": 15}),
    ("Sawa Pref. →", [378, 451, 520, 475], {"max_size": 15}),
]
JOBS += [
    {"id": "ref34-front", "screen": "reference 34 detail", "style": "serif", "mode": "lines", "chain": True,
     "erase": "maskfill", "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK,
     "new": True, "note": "timetable (destination marks M/O/W set by refdoc_marks.py)",
     "items": [(D + "rrr34/0.gal", "")], "lines": TT_LINES},
    {"id": "ref34-map", "screen": "reference 34 detail", "style": "serif", "mode": "lines",
     "erase": "maskfill", "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK,
     "new": True, "note": "route map; station names set top-to-bottom in the name columns",
     "items": [(D + "rrr34/1.gal", "")], "lines": MAP_LINES},
    {"id": "ref34-flip", "screen": "reference 34 flip frames", "style": "serif", "mode": "asis", "chain": True,
     "items": [(D + "rrr34/%d.gal" % n, "") for n in range(2, 18)]},
]


# ---- 48 class-reunion postcard (reply-paid card): 0.png = outgoing card (address side | invitation),
# 1.png = reply card (address side | reply form), 800x593 each; flip frames 2..17. Address-side text is vertical
# in the original: set top-to-bottom (rot -90) in the same columns. Postal-code digits and phone numbers kept.
_V = {"rot": -90, "align": "center"}
_STAMP_BLUE = [0, 140, 60, 200, 140, 255]
PC_OUT = [
    ("Reply-paid postcard", [166, 15, 304, 33], {"color": "#e05a5a", "max_size": 11, "align": "center",
                                                  "method": "inpaint", "mask_color": [180, 255, 40, 200, 40, 200]}),
    ("JAPAN POST", [58, 135, 100, 148], {"color": "#1a6fc0", "max_size": 7, "align": "center", "method": "inpaint",
                                         "mask_color": _STAMP_BLUE}),
    ("Outgoing", [62, 152, 100, 169], {"color": "#1a8fd0", "max_size": 10, "align": "center", "method": "inpaint",
                                       "mask_color": _STAMP_BLUE}),
    ("1-20 Shirogaoka, Motoki-cho, Sawa Prefecture", [316, 94, 374, 402], dict(_V, max_size=24)),
    # IMAGES3D: the last glyph's vertical stroke (x 215-219, y 434-481) was kept out of the job mask and restored as a table rule: own dark mask_color + no_rules
    ("Saki Goto-sama", [198, 98, 268, 500], dict(_V, max_size=46, erase=[[200, 98, 266, 498]], no_rules=True,
                                                    mask_color=[0, 150, 0, 150, 0, 150], mask_grow=5)),
    ("22-6 Nishida, Minakami City, Sawa Prefecture", [86, 324, 111, 541], dict(_V, max_size=16)),
    ("Tetsuji Ihata", [60, 324, 87, 458], dict(_V, max_size=18)),
    ("(recycled paper)", [330, 560, 398, 576], {"color": "#e05a5a", "max_size": 8, "align": "center",
                                               "method": "inpaint", "mask_color": [180, 255, 40, 200, 40, 200]}),
    ("Minakami Second High School   Year 3, Class 1", [410, 30, 795, 60], {"align": "center", "max_size": 18}),
    ("Class Reunion Invitation", [410, 60, 795, 90], {"align": "center", "max_size": 18}),
    ("Dear all,  In this season of crisp autumn air, I trust that you have all been keeping well since we "
     "last met. We are pleased to tell you that a reunion of Minakami Second High School Year 3, Class 1 "
     "will be held as follows. We know this is a busy time of year, but we sincerely hope you will be able "
     "to attend.   Sincerely,", [406, 102, 794, 204], {"max_size": 13, "line_spacing": 1.1}),
    ("Shiyo 799, October", [414, 204, 600, 222], {"max_size": 13, "erase": [[410, 202, 604, 229]]}),
    ("Details", [560, 278, 640, 299], {"align": "center", "max_size": 14}),
    ("Date & time    Shiyo 800, April 8 (Wed), from 18:00", [404, 312, 794, 335], {"max_size": 14}),
    ("Venue    Hotel Mermaid's Rest, 1-2 Nakanohara 5-chome, Minakami City", [404, 348, 796, 370],
     {"max_size": 14}),
    ("10-minute walk from Sawa-Minakami Station", [462, 369, 796, 387], {"max_size": 14}),
    ("Phone    128-552-XXXX", [462, 387, 796, 405], {"max_size": 14}),
    ("Fee    5,000 yen", [404, 419, 700, 442], {"max_size": 14}),
    ("Reply by    Shiyo 800, January 31 (Fri), must arrive by this date", [404, 455, 796, 478],
     {"max_size": 14}),
    ("Minakami Second High School Year 3, Class 1 Reunion", [470, 490, 796, 512], {"max_size": 14}),
    ("Organizers    Tetsuji Ihata    040-6344-XXXX", [470, 510, 796, 529], {"max_size": 14, "align": "right"}),
    ("Naoko Kukimoto    040-6878-XXXX", [470, 529, 796, 549], {"max_size": 14, "align": "right"}),
]
PC_REPLY = [
    ("Reply-paid postcard", [166, 15, 304, 33], {"color": "#e05a5a", "max_size": 11, "align": "center",
                                                  "method": "inpaint", "mask_color": [180, 255, 40, 200, 40, 200]}),
    ("JAPAN POST", [56, 135, 100, 148], {"color": "#208040", "max_size": 7, "align": "center", "method": "inpaint",
                                         "mask_color": [0, 140, 90, 255, 0, 160]}),
    ("Reply", [60, 152, 104, 172], {"color": "#20a050", "max_size": 11, "align": "center", "method": "inpaint",
                                    "mask_color": [0, 140, 90, 255, 0, 160]}),
    ("22-6 Nishida, Minakami City, Sawa Prefecture", [243, 128, 274, 424], dict(_V, max_size=22)),
    ("To: Tetsuji Ihata", [208, 128, 244, 358], dict(_V, max_size=26)),
    ("(recycled paper)", [330, 560, 398, 576], {"color": "#e05a5a", "max_size": 8, "align": "center",
                                               "method": "inpaint", "mask_color": [180, 255, 40, 200, 40, 200]}),
    ("Minakami Second High School Year 3, Class 1 Reunion", [422, 56, 790, 88], {"align": "center", "max_size": 17}),
    ("Will attend", [440, 114, 640, 154], {"max_size": 28}),
    ("Will not attend", [440, 178, 640, 218], {"max_size": 28}),
    ("(Please circle one.)", [512, 227, 770, 249], {"max_size": 14}),
    ("Even if you will not attend, please fill in your name and address and reply.", [430, 265, 772, 303],
     {"max_size": 14}),
    ("Name", [424, 337, 520, 358], {"max_size": 13}),
    ("(maiden name           )", [612, 354, 760, 371], {"max_size": 12}),
    ("Address", [424, 386, 520, 407], {"max_size": 13}),
    ("Phone", [424, 433, 520, 455], {"max_size": 13}),
    ("Message", [424, 497, 520, 519], {"max_size": 13}),
]
JOBS += [
    {"id": "ref48-out", "screen": "reference 48 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "new": True,
     "note": "reunion postcard, outgoing card (stamp art and postal-code boxes kept)",
     "items": [(D + "rrr48/0.gal", "")], "lines": PC_OUT},
    {"id": "ref48-reply", "screen": "reference 48 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "new": True,
     "note": "reunion postcard, reply card",
     "items": [(D + "rrr48/1.gal", "")], "lines": PC_REPLY},
    {"id": "ref48-flip", "screen": "reference 48 flip frames", "style": "serif", "mode": "asis", "chain": True,
     "items": [(D + "rrr48/%d.gal" % n, "") for n in range(2, 18)]},
]


# ---- 53 cherry-festival poster (800x1076) + the graffiti overlay 落書き.png (293x104) ----
# Lettering sits on a flower pattern: inpaint of the glyph colour only (local, no paid edit). The title's pale
# outline shares the flowers' pink, so the title mask is grown 7 px. The graffiti arrow is kept; only the kanji go.
_BLACK = [0, 90, 0, 90, 0, 90]
_GRAF = [110, 220, 0, 70, 0, 70]
JOBS += [
    {"id": "ref53-title", "screen": "reference 53 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "color": "#ee82b8", "stroke": 3, "stroke_color": "#fff4fa", "new": True,
     "note": "festival poster title (wording = reference title)",
     "items": [(D + "rrr53/0.gal", "")],
     "lines": [("70th Motoki Cherry Festival", [70, 52, 770, 142],
                {"mask_color": [200, 255, 90, 175, 140, 215], "mask_grow": 7, "max_size": 60, "align": "center"})]},
    {"id": "ref53-body", "screen": "reference 53 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "chain": True, "erase_first": True, "color": INK, "new": True, "note": "festival poster",
     "items": [(D + "rrr53/0.gal", "")],
     "lines": [
         ("Shiyo 800, 3/13 – 4/12", [96, 150, 706, 218], {"style": "gothic", "mask_color": _BLACK, "mask_grow": 5,
                                                          "max_size": 46, "align": "center"}),
         ("Motoki-cho, famous for its cherry blossoms,", [70, 282, 740, 340],
          {"mask_color": _BLACK, "mask_grow": 5, "max_size": 32, "align": "center", "erase": [[80, 280, 735, 402]]}),
         ("holds its cherry-blossom festival again this year!", [70, 342, 740, 400],
          {"max_size": 32, "align": "center", "erase": []}),
         ("15 food stalls planned!", [70, 474, 740, 530],
          {"mask_color": _BLACK, "mask_grow": 5, "max_size": 33, "align": "center", "erase": [[80, 472, 735, 584]]}),
         ("And the yearly eating contest will be held too!!", [70, 528, 740, 584],
          {"max_size": 33, "align": "center", "erase": []}),
         ("Event Office    TEL: 991-650-XXXX", [84, 890, 600, 930],
          {"mask_color": _BLACK, "mask_grow": 4, "max_size": 24}),
         ("Please note", [58, 957, 460, 981], {"color": "#e00000", "max_size": 18,
                                               "mask_color": [190, 255, 0, 100, 0, 100], "mask_grow": 4,
                                               "erase": [[56, 955, 456, 1042]]}),
         ("Never climb the cherry trees.", [58, 983, 460, 1009], {"color": "#e00000", "max_size": 18, "erase": []}),
         ("It may cause an unexpected accident.", [58, 1012, 460, 1040],
          {"color": "#e00000", "max_size": 18, "erase": []}),
         ("13th memorial", [520, 893, 780, 1006], {"style": "handwriting", "color": "#b00000", "rot": 12, "rot_h": 62,
                                                  "max_size": 46, "mask_color": _GRAF, "mask_grow": 4,
                                                  "erase": [[522, 895, 776, 1004]]}),
     ]},
    {"id": "ref53-graffiti", "screen": "reference 53 overlay", "style": "handwriting", "mode": "lines",
     "erase": "maskalpha", "color": "#c00000", "new": True, "note": "graffiti overlay (arrow kept)",
     "items": [(D + "rrr53/落書き.gal", "")],
     "lines": [("13th memorial", [62, 0, 293, 104], {"rot": 12, "rot_h": 60, "max_size": 46,
                                                    "erase": [[64, 0, 293, 104]], "mask_grow": 3})]},
]


# ---- 70 cram-school web page (800x1352): sans lettering in the original, set in serif (the owner's printed
# face) except the logo; inpaint of the glyph colour on the textured / gradient grounds; buttons keep their arrows.
_W = [150, 255, 150, 255, 150, 255]
_K = [0, 90, 0, 90, 0, 90]
_NAV = ["Home", "Our Schools", "Courses", "Results", "Info Sessions", "FAQ", "Request Info"]
_NAVX = [0, 115, 229, 343, 457, 571, 685, 800]
_GW = {"color": "#ffffff", "mask_color": _W, "mask_grow": 3, "max_size": 16}
WEB_LINES = [
    ("Phone: 991-651-XXXX", [383, 50, 782, 95], {"max_size": 34, "mask_color": _K}),
    ("10:00–20:00 (Mon–Sat) / 10:00–15:00 (Sun & holidays)", [383, 96, 792, 119], {"max_size": 15, "mask_color": _K}),
] + [(t, [_NAVX[i] + 5, 158, _NAVX[i + 1] - 5, 180], {"max_size": 14, "align": "center", "mask_color": _K})
     for i, t in enumerate(_NAV)] + [
    ("Opening in the Shiyo 800 school year!", [40, 223, 500, 255], {"max_size": 19, "mask_color": _K}),
    ("Results as good as any cram school in the capital region!", [40, 256, 500, 287],
     {"max_size": 19, "mask_color": _K}),
    ("New school year:  Trial lessons now open", [40, 291, 500, 341], {"style": "gothic", "max_size": 32,
                                                                      "mask_color": _K}),
    ("■ Tuition: 2,500 yen / course   ■ Materials: 800–3,800 yen / subject", [40, 343, 570, 368],
     {"max_size": 17, "mask_color": _K}),
    ("Apply for a trial lesson", [80, 398, 258, 438], {"max_size": 17, "color": "#ffffff", "mask_color": _W}),
    ("Find out more", [338, 398, 496, 438], {"max_size": 17, "color": "#ffffff", "mask_color": _W}),
    ("● Important notice", [46, 489, 420, 512], {"max_size": 15, "mask_color": _K}),
    ("Shiyo 800, April 8   8:30", [46, 513, 420, 535], {"max_size": 15, "mask_color": _K}),
    ("Due to the incident at Chuo Park, the high-school course and the high-school entrance exam course are "
     "cancelled.", [46, 535, 792, 557], {"max_size": 15, "mask_color": _K}),
    ("Only the university entrance exam course is held (high-school students may attend).", [46, 557, 792, 580],
     {"max_size": 15, "mask_color": _K}),
    ("Feature!   Erina Goto's Story of Passing the Exam", [80, 651, 720, 689],
     dict(_GW, style="gothic", max_size=24, align="center")),
    ("We interviewed Erina Goto-san, who recently passed the entrance exam for Motoki High School with the best "
     "results since the school was founded!", [48, 733, 752, 792], _GW),
    ("―Congratulations on getting into high school!", [48, 835, 752, 860], _GW),
    ('Goto: "Oh, no, thank you very much!"', [48, 868, 752, 894], _GW),
    ("―What are you looking forward to most in high school right now?", [48, 902, 752, 928], _GW),
    ('Goto: "Let me see... Enjoying my youth to the full, of course! That says it all!"', [48, 935, 752, 961], _GW),
    ("―I see! How many decades ago was I a high-school student, I wonder...", [48, 970, 752, 995], _GW),
    ('Goto: "Ahahaha! But all those years added up, and by some chance you became a teacher at this school and '
     'taught me, right? So I\'m grateful for the high-school life you had, Sensei!"', [48, 1003, 752, 1092], _GW),
    ("―You'll make me cry, saying that.", [48, 1105, 572, 1130], _GW),
    ('Goto: "But you really did help me! Actually, I just went and signed up for the university entrance '
     'exam course too!"', [48, 1138, 572, 1198], _GW),
    ("―Really!? And straight into the university entrance exam course!?", [48, 1206, 572, 1232], _GW),
    ('Goto: "What\'s in the high-school course gets taught in high-school classes anyway, so I thought I\'d '
     'dive straight into a world full of questions!"', [48, 1240, 752, 1299], _GW),
    ("―That's Goto-san for you! Do you have any advice for everyone who has the high-school entrance exam "
     "coming up this year?", [48, 1307, 752, 1352], _GW),
]
JOBS += [
    {"id": "ref70-logo", "screen": "reference 70 detail", "style": "rounded", "mode": "lines", "erase": "inpaint",
     "color": "#ffffff", "stroke": 2, "stroke_color": "#ff7fbf", "new": True, "note": "cram-school logo tiles",
     "items": [(D + "rrr70/0.gal", "")],
     "lines": [("MOTOKI CRAM SCHOOL", [14, 44, 272, 94], {"mask_color": [235, 255, 235, 255, 235, 255],
                                                          "mask_grow": 3, "max_size": 24, "align": "center"})]},
    {"id": "ref70", "screen": "reference 70 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "chain": True, "erase_first": True, "color": INK, "mask_grow": 3, "new": True,
     "note": "cram-school web page", "items": [(D + "rrr70/0.gal", "")], "lines": WEB_LINES},
]
JOBS += [
    {"id": "ov-rest", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (13, 71, 32, 4, 34, 48, 53, 70)]},
]


# ---- 23 newspaper page 1 (0.png 800x519) + 8 close-ups (部分拡大1-8) ----
# Vertical columns become horizontal English blocks in the same article boxes, in reading order; a sentence that
# crosses a block in the JP may cross it in the English. Vertical headlines read top-to-bottom (rot -90).
# Paper is textured: inpaint of the dark glyph pixels; column rules restored (erase_first + text_only).
NP_CAPTION = "Koji Kuji-kun (left) and Kokona Hatanaka-chan (right), who were killed"
NP_R1 = ("Shortly after 4 p.m. on April 8, two second-graders were brutally murdered in Nanami-cho, Megasawa City. "
         "The victims were Koji Kuji-kun (7) and Kokona Hatanaka-chan (7), who attend Megasawa Second Elementary "
         "School in the same city. Because the crime took place in broad daylight, while it was still light, the "
         "police believe it was the work of a random street attacker and are pursuing the investigation. However, "
         "the two victims were killed")
NP_R2 = ("in separate places at almost the same time, so some believe more than one person did it. Also, since "
         "there were no witnesses at all and nothing was caught on nearby security cameras, the view that it was "
         "someone who knows the area is gaining ground, and the search of the vicinity continues.")
NP_SUB = "Spirited away? Residents' unease grows"
NP_MID = ("Despite a case of this scale, the unusual situation of no witnesses and no clues has residents")
NP_R3 = ("voicing their unease. Megasawa Second Elementary School has announced that it will close for the time "
         "being until there is progress in the case. The bodies had been cut through at the abdomen with a single "
         "stroke of a large blade, and some residents say it was a spiriting-away, that it can hardly be the work "
         "of a human. Not only the progress of the case but the method of the crime too is adding to the "
         "residents' unease.")
NP_L1 = ("Koji Kuji-kun, one of the victims, was killed on his way home after playing with a friend. But the spot "
         "is not one with little foot traffic, and since Koji-kun was moving by bicycle, he is thought to have been "
         "ambushed at a moment when no one was watching.")
NP_L2 = ("Even so, the culprit had far too much luck. Suppose the crime was committed at a deliberately chosen "
         "moment: the culprit would have had to chase the bicycle and kill him in a gap when no one was looking, "
         "and, given the location, run 50 meters")
NP_L3 = ("without a sound and kill him within seconds. Since the culprit then also had to vanish without being "
         "seen, it is reasonable to think that he was attacked when the culprit happened to pass by. Kokona "
         "Hatanaka-chan, also a victim,")
NP_L4 = ("had gone shopping with her parents, the three of them, and was killed even though she was holding "
         "hands between the two of them. It is far too removed from anything a human could do.")
_NK = [0, 110, 0, 110, 0, 110]
_NB = {"mask_color": _NK, "mask_grow": 3, "line_spacing": 1.05}
_NB2 = dict(_NB, mask_color=[0, 165, 0, 165, 0, 165], mask_grow=4)
NP_PAGE = [
    ("MEGASAWA NEWSPAPER", [286, 5, 512, 32], dict(_NB2, max_size=16, align="center")),
    ("Shiyo 790, April 9   Friday   No. 24684", [560, 5, 796, 31], dict(_NB2, max_size=13, align="right")),
    (NP_CAPTION, [268, 121, 548, 143], dict(_NB2, max_size=11, align="center")),
    (NP_R1, [266, 146, 548, 265], dict(_NB2, max_size=11)),
    (NP_R2, [396, 270, 548, 388], dict(_NB2, max_size=11)),
    (NP_SUB, [262, 270, 394, 306], dict(_NB2, max_size=13)),
    (NP_MID, [262, 307, 394, 388], dict(_NB2, max_size=11, erase=[[258, 270, 395, 388]])),
    (NP_R3, [266, 393, 548, 512], dict(_NB2, max_size=11)),
    ("Two second-graders butchered", [610, 104, 666, 476], dict(_NB2, rot=-90, max_size=40, align="center")),
    ("Broad daylight: a bizarre case with no witnesses", [572, 176, 607, 464],
     dict(_NB2, rot=-90, max_size=20, align="center")),
    ("Impossible for a human?", [204, 58, 252, 302], dict(_NB2, rot=-90, max_size=30, align="center")),
    ("The method", [204, 314, 252, 440], dict(_NB2, rot=-90, max_size=30, align="center")),
    (NP_L1, [26, 33, 199, 148], dict(_NB2, max_size=11)),
    (NP_L2, [26, 152, 199, 268], dict(_NB2, max_size=11)),
    (NP_L3, [26, 272, 199, 388], dict(_NB2, max_size=11)),
    (NP_L4, [26, 393, 199, 514], dict(_NB2, max_size=11)),
    ("MEGASAWA\nNEWSPAPER", [693, 48, 776, 346], dict(_NB, mask_grow=5, no_rules=True, rot=-90, max_size=40, align="center", erase=[[692, 38, 777, 350]])),
    ("Publisher\nMegasawa Newspaper Co.\n31-16 Kokuji, Megasawa City,\nIizawa Prefecture\nPostcode 995-XXXX\n"
     "© Megasawa Newspaper Co. 790\nPhone 226(541)XXXX", [686, 356, 792, 440], dict(_NB2, max_size=9)),
    ("Game creation tool,\nno programming needed", [686, 445, 792, 490], dict(_NB2, max_size=10, align="center")),
]
_ZB = dict(_NB, max_size=21, line_spacing=1.1)
# IMAGES3C: wider glyph masks against the grey glyph-edge speckle the eye-check found (newsprint ground 200-233):
# page text <= 165 grown 4, close-ups <= 170 grown 5. Masthead / banner lines: no_rules (their big strokes were
# restored as table rules by text_only).
_ZB2 = dict(_ZB, mask_color=[0, 170, 0, 170, 0, 170], mask_grow=5)
JOBS += [
    {"id": "ref23", "screen": "reference 23 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "color": INK, "new": True,
     "note": "newspaper page (photos and the LiveMaker logo kept)", "items": [(D + "rrr23/0.gal", "")],
     "lines": NP_PAGE, "ignore": [[330, 50, 505, 122], [686, 490, 790, 519]]},
    {"id": "ref23-zoom", "screen": "reference 23 close-ups", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "color": INK, "new": True,
     "note": "newspaper close-ups (same English as the page, larger)",
     "items": [(D + "rrr23/部分拡大%d.gal" % n, "", {"lines": L}) for n, L in (
         (1, [(NP_CAPTION, [8, 148, 484, 184], dict(_NB, max_size=20, align="center"))]),
         (2, [(NP_R1, [8, 4, 524, 228], _ZB2)]),
         (3, [(NP_R2, [290, 4, 532, 222], dict(_ZB2, max_size=16)), (NP_SUB, [6, 4, 262, 54], dict(_ZB2, max_size=24)),
              (NP_MID, [6, 56, 262, 222], dict(_ZB2, max_size=16, erase=[[4, 4, 264, 222]]))]),
         (4, [(NP_R3, [8, 4, 528, 216], _ZB2)]),
         (5, [(NP_L1, [6, 4, 304, 207], _ZB2)]),
         (6, [(NP_L2, [6, 4, 298, 210], _ZB2)]),
         (7, [(NP_L3, [6, 4, 336, 218], _ZB2)]),
         (8, [(NP_L4, [6, 4, 328, 220], _ZB2)]),
     )],
     "lines": []},
]
JOBS += [
    {"id": "ov-23", "screen": "reference screen preview", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr23.gal", "")]},
]


# ======== IMAGES3B (second run, 2026-10-01) ========
# ---- 2 smartphone brochure (0.png 800x2205): gradient ground, coloured lettering -> inpaint of the glyph colour;
# headlines / pill labels gothic, bullet text and the spec table serif; Latin (PHONE-X- logos, H125xW67, 128GB,
# copyright) kept as drawn.
_DK = [0, 120, 0, 120, 0, 120]
_WT = [215, 255, 215, 255, 215, 255]
_S2 = {"mask_color": _DK, "color": "#333333", "max_size": 14}
# IMAGES3D: the five left-column feature labels and the red sub-line had erase boxes that already covered the
# Japanese (non-background extents batt x 52-252 y 1277-1298, signal 67-234 / 1350-1372, maint 28-276 / 1424-1446,
# GPS 93-210 / 1497-1519, apps 73-229 / 1569-1594, red line 37-300 / 1138-1153); the anti-aliased glyph edges
# escaped the colour masks. Masks now = "any pixel moved from the pill colour toward the glyph colour", grow 3.
PH_LINES = [
    ("New Smartphone", [36, 110, 322, 156], {"style": "gothic", "mask_color": _DK, "color": "#111111", "max_size": 30,
                                             "erase": [[36, 112, 318, 154]]}),
    ("Irokara", [330, 46, 714, 164], {"style": "rounded", "mask_color": [60, 255, 0, 80, 30, 255], "mask_grow": 3,
                                     "color": "#c8106a", "max_size": 84, "align": "center"}),
    ("Choose from 7 rainbow colors", [44, 402, 700, 450], {"style": "gothic", "color": "#2aa85a", "max_size": 38,
                                                          "mask_color": [0, 150, 120, 235, 0, 170]}),
    ("A smart form with no side buttons", [34, 845, 764, 893], {"style": "gothic", "color": "#1e7fc8", "max_size": 40,
                                                                "mask_color": [0, 140, 60, 210, 120, 255]}),
    ("You can choose the OS you prefer.", [34, 1093, 720, 1135], {"style": "gothic", "color": "#e81c1c", "max_size": 36,
                                                                  "mask_color": [150, 255, 0, 110, 0, 110],
                                                                  "erase": [[34, 1094, 536, 1135]]}),
    ("Please choose one when you buy.", [34, 1135, 520, 1157], {"color": "#e02020", "max_size": 14,
                                                                 "mask_color": [0, 255, 0, 225, 0, 255], "mask_grow": 3,
                                                                 "erase": [[34, 1135, 308, 1157]]}),
    ("Extra-large battery", [24, 1266, 282, 1312], {"style": "gothic", "color": "#ffffff", "max_size": 21,
                                                    "mask_color": [120, 255, 0, 255, 0, 255], "mask_grow": 3,
                                                    "erase": [[49, 1274, 256, 1302]]}),
    ("High-sensitivity signal detection", [24, 1340, 282, 1386], {"style": "gothic", "color": "#ffffff", "max_size": 21,
                                                                  "mask_color": [120, 255, 0, 255, 0, 255], "mask_grow": 3,
                                                                  "erase": [[64, 1347, 238, 1376]]}),
    ("Real-time maintenance", [24, 1413, 282, 1459], {"style": "gothic", "color": "#ffffff", "max_size": 21,
                                                      "mask_color": [140, 255, 0, 255, 0, 255], "mask_grow": 3,
                                                      "erase": [[25, 1421, 280, 1450]]}),
    ("Friend GPS", [24, 1487, 282, 1533], {"style": "gothic", "color": "#555555", "max_size": 21,
                                          "mask_color": [0, 190, 0, 255, 0, 255], "mask_grow": 3, "erase": [[90, 1494, 214, 1523]]}),
    ("Works with all kinds of apps", [24, 1560, 282, 1606], {"style": "gothic", "color": "#ffffff", "max_size": 21,
                                                             "mask_color": [0, 255, 0, 255, 120, 255], "mask_grow": 3,
                                                             "erase": [[70, 1566, 233, 1598]]}),
    ("• Over 24 hours of continuous talk time", [308, 1268, 786, 1310], dict(_S2, max_size=17, color="#222222",
                                                                         erase=[[308, 1275, 567, 1302]])),
    ("• Strong reception even in the mountains and suburbs", [308, 1342, 786, 1384],
     dict(_S2, max_size=17, color="#222222", erase=[[308, 1349, 541, 1376]])),
    ("• Detects faults and viruses through regular communication, then fixes or removes them", [308, 1409, 786, 1429],
     dict(_S2, max_size=12, color="#222222", erase=[[307, 1410, 634, 1430]])),
    ("Communicates externally at regular intervals", [318, 1428, 786, 1445],
     dict(_S2, max_size=12, color="#222222", erase=[[316, 1428, 493, 1446]])),
    ("This function can be switched OFF if you wish", [318, 1444, 786, 1462],
     dict(_S2, max_size=12, color="#222222", erase=[[316, 1444, 509, 1462]])),
    ("• Tells you by voice and on a map where nearby friends are", [308, 1488, 786, 1513],
     dict(_S2, max_size=16, color="#222222", erase=[[308, 1489, 747, 1513]])),
    ("Detection range adjustable; OFF by default", [324, 1512, 786, 1531],
     dict(_S2, max_size=12, color="#222222", erase=[[324, 1512, 536, 1531]])),
    ("• Supports all major apps", [308, 1567, 786, 1599], dict(_S2, max_size=17, color="#222222",
                                                           erase=[[308, 1570, 495, 1596]])),
    ("Specifications (see our website for details)", [180, 1734, 606, 1760], dict(_S2, erase=[[180, 1736, 573, 1758]])),
    ("Size", [180, 1768, 284, 1791], _S2),
    ("Weight", [180, 1801, 284, 1825], _S2),
    ("4.7 inches", [290, 1833, 600, 1857], dict(_S2, erase=[[290, 1835, 362, 1855]])),
    ("Display", [180, 1866, 284, 1888], _S2),
    ("LALAPA HD display", [290, 1864, 600, 1890], dict(_S2, erase=[[290, 1866, 462, 1888]])),
    ("3840x2160 pixels", [290, 1896, 600, 1921], dict(_S2, erase=[[290, 1898, 438, 1919]])),
    ("Storage", [180, 1930, 284, 1953], _S2),
    ("Chip", [180, 1962, 284, 1987], _S2),
    ("64-bit SUN-H11 Hyper", [290, 1960, 600, 1989], dict(_S2, erase=[[290, 1962, 472, 1987]])),
    ("24MP camera", [290, 1993, 600, 2019], dict(_S2, erase=[[290, 1995, 378, 2017]])),
    ("Camera", [180, 2014, 284, 2036], _S2),
    ("16x digital zoom", [290, 2026, 600, 2051], dict(_S2, erase=[[290, 2028, 444, 2049]])),
]
JOBS += [
    {"id": "ref2", "screen": "reference 2 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": INK, "mask_grow": 2, "new": True,
     "note": "smartphone brochure (phone art, OS logos and Latin specs kept)",
     "items": [(D + "rrr2/0.gal", "")], "lines": PH_LINES},
]
JOBS += [
    {"id": "ov-2", "screen": "reference screen preview", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr2.gal", "")]},
]


# ---- 40 girls' volleyball bracket (0.png 852x609): team names / results table / title; seed numbers and scores
# kept as drawn. Readings of the school names guessed where no glossary row exists (logged).
_T40L = ["Minakami West", "Satomizaki", "Oyama", "West Sawa", "Sawa", "Sawa Third", "Kitamura", "Karine Girls'"]
_T40R = ["Motoki", "Sakaibashi", "Kumayama", "Minakami Municipal", "Minamisato", "Kotoriya", "Sawa Girls'", "Sawa South"]
_Y40 = [121, 185, 249, 313, 376, 441, 505, 569]
BR_LINES = [
    ("Shiyo 798 Sawa Prefecture Junior High School Athletic Meet   Volleyball (Girls)", [60, 3, 792, 35],
     {"align": "center", "max_size": 22}),
    ("Champion", [312, 68, 420, 92], {"align": "center", "max_size": 14}),
    ("Minakami West", [424, 68, 530, 92], {"align": "center", "max_size": 14}),
    ("Runner-up", [312, 100, 420, 124], {"align": "center", "max_size": 14}),
    ("Motoki", [424, 100, 530, 124], {"align": "center", "max_size": 14}),
    ("Third place", [312, 148, 420, 172], {"align": "center", "max_size": 14}),
    ("Karine Girls'", [424, 134, 530, 156], {"align": "center", "max_size": 14}),
    ("Sawa Girls'", [424, 165, 530, 188], {"align": "center", "max_size": 14}),
] + [(t, [19, y - 4, 163, y + 19], {"max_size": 15}) for t, y in zip(_T40L, _Y40)] + [
    (t, [702, y - 4, 851, y + 19], {"max_size": 15}) for t, y in zip(_T40R, _Y40)]
JOBS += [
    {"id": "ref40", "screen": "reference 40 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": INK, "new": True,
     "note": "volleyball bracket (seed numbers, scores and bracket lines kept)",
     "items": [(D + "rrr40/0.gal", "")], "lines": BR_LINES},
]



# ---- memo pages (handwritten JP on paper): one English line per JP line, Ink Free, in the JP line's row.
# rows come from work/images/_rows.py (ink extents per line); text None = row kept as drawn (arrows).
def memo(rows, texts, size=18, right=796, pad=3):
    out = []
    for (x0, y0, x1, y1), t in zip(rows, texts):
        if t is None:
            continue
        out.append((t, [max(x0 - pad, 0), y0 - pad, right, y1 + pad],
                    {"max_size": size, "erase": [[max(x0 - pad, 0), y0 - 2, x1 + pad, y1 + 2]]}))
    return out


def scaled(lines, s):
    """a lines list moved onto a copy of the same form drawn at scale s (offset 0)."""
    out = []
    for t, b, *o in lines:
        o = dict(o[0]) if o else {}
        if "erase" in o:
            o["erase"] = [[int(round(v * s)) for v in e] for e in o["erase"]]
        if "ellipse" in o:
            o["ellipse"] = [int(round(v * s)) for v in o["ellipse"]]
        if "max_size" in o:
            o["max_size"] = max(7, int(round(o["max_size"] * s)))
        out.append((t, [int(round(v * s)) for v in b], o))
    return out


# 85 Goto's memo 6 (800x1084)
R85 = [[8, 32, 378, 53], [12, 57, 573, 77], [8, 106, 759, 127], [9, 132, 263, 151], [10, 156, 408, 176],
       [9, 180, 635, 201], [10, 205, 201, 225], [12, 256, 335, 275], [8, 280, 511, 301], [8, 304, 749, 325],
       [10, 329, 552, 350], [8, 379, 667, 399], [10, 404, 511, 424], [7, 428, 620, 450], [14, 454, 20, 472],
       [10, 478, 470, 499], [10, 503, 656, 524], [14, 528, 20, 547], [7, 552, 490, 574], [11, 578, 242, 598],
       [10, 602, 780, 622], [8, 627, 439, 647], [14, 652, 20, 671], [8, 676, 227, 697], [8, 701, 792, 722],
       [7, 726, 210, 747], [8, 751, 366, 772], [11, 800, 759, 821], [10, 825, 620, 846], [9, 851, 387, 870],
       [9, 875, 428, 895], [10, 899, 656, 920], [9, 924, 496, 945], [11, 974, 470, 994], [12, 999, 521, 1019],
       [7, 1024, 387, 1043]]
T85 = [
    None,
    "So, about the detective named Ise-san who came to visit.",
    "He came saying Kogori-senpai's mother was worried about her daughter and had come to see her, but...",
    "He probably had another purpose.",
    "For that, the police would only have needed to phone me.",
    "In other words, he came because he guessed I was hiding Kogori-senpai.",
    "The proof: the bug.",
    "So what should I do here?",
    "Hide where Kogori-senpai and Niimura-senpai are, or contact the police?",
    "Judging by the two of them, it looks like Niimura-senpai dragged Kogori-senpai here by force.",
    "And yet, if Kogori-senpai's whereabouts are being searched for...",
    "Both of them seem to have been caught up in some case the police are involved in.",
    "And a lieutenant named Ise went to the trouble of coming here.",
    "Even though there was such a big incident this morning, the lieutenant came in person!",
    None,
    "The senpais may be connected to this morning's incident.",
    "And Kogori-senpai's mother went out of her way to come here through the police.",
    None,
    "The victim of this morning's incident is probably Kogori-senpai's father.",
    "Yes, that would make sense.",
    "What's more, the police came and even left a bug, so the case isn't over yet.",
    "→ If it follows the Megasawa City murders, one more person will be killed.",
    None,
    "Kogori-senpai's life is in danger!",
    "Niimura-senpai avoided everyone's eyes and asked me for help, so did she notice the danger and",
    "take Kogori-senpai away?",
    "Niimura-senpai must know something.",
    "Niimura-senpai is probably connected to this morning's incident, but she isn't the culprit.",
    "She can't drive a car, and a stunt like flaying a human? No way, no way!",
    "But if she were the culprit, there would be an accomplice.",
    "Then taking Kogori-senpai away would be strange.",
    "Leaving her at home as she was would be the sure way to kill Kogori-senpai, after all.",
    "Therefore, Niimura-senpai is trying to save Kogori-senpai!",
    "In that case I can't keep quiet to the police, can I.",
    "For now, let's try to get in touch without the two of them finding out.",
    "Just talking into the bug should do it.",
]
JOBS += [
    {"id": "ref85", "screen": "reference 85 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "Goto's memo (handwriting; arrows and the heart kept)", "items": [(D + "rrr85/0.gal", "")],
     "lines": [("Kogori-senpai & Niimura-senpai: lovey-dovey bath time", [6, 29, 360, 56],
                {"max_size": 18, "erase": [[6, 30, 360, 55]]})] + memo(R85, T85),
     "ignore": [[360, 30, 380, 55], [12, 452, 22, 474], [12, 526, 22, 549], [12, 650, 22, 673]]},
]


# 27 death certificate (additional): the ref-13 form drawn at 0.8 (template match 0.916, offset 0) + the
# handwritten follow-up notes below it.
_DC27 = [l for l in deathcert(DC13) if l[0] != "DEATH CERTIFICATE"]
R27 = [[40, 1186, 224, 1209], [40, 1215, 358, 1235], [40, 1240, 740, 1261], [41, 1266, 748, 1287],
       [40, 1317, 206, 1338], [40, 1342, 430, 1363], [40, 1394, 206, 1415], [40, 1419, 537, 1441],
       [40, 1471, 206, 1492], [40, 1496, 302, 1517], [40, 1522, 687, 1543], [40, 1548, 741, 1569],
       [40, 1574, 87, 1594], [40, 1625, 206, 1646], [40, 1651, 496, 1671], [40, 1676, 733, 1697],
       [41, 1702, 559, 1723], [43, 1728, 743, 1748], [43, 1754, 751, 1775], [50, 1805, 710, 1826]]
T27 = [
    "Shiyo 788, April 13",
    "Request for a detailed autopsy from the Motoki police.",
    "However, as the drug in the blood needs to be analyzed, we will go no further than submitting a",
    "blood sample. This hospital has already established that it is a drug similar to ephedrine.",
    "Shiyo 788, April 15",
    "The Motoki police ask the Sawa Prefectural Police to investigate the drug.",
    "Shiyo 788, May 30",
    "The blood sample is handed from the Sawa Prefectural Police to the National Police Agency.",
    "Shiyo 788, June 10",
    "Notice from the National Police Agency to the Sawa Prefectural Police.",
    "An order came to halt the investigation into Mr. Eiichiro Niimura's fatal accident at once.",
    "An interim report on the blood sample had been received, but any further drug investigation",
    "was stopped as well.",
    "Shiyo 788, June 12",
    "On the interim report on the blood sample (from the National Police Agency)",
    "A substance extremely similar to ephedrine (C10H15NO), but reportedly not the same",
    "substance. The molecular structure is similar, but the composition differs slightly.",
    "Apart from the drug, many tiny fragments of living matter were also detected. Some organism may",
    "have got into the body (most likely mold or bacteria, but the details are unknown).",
    "(At this point the National Police Agency ordered the investigation halted, so the drug's details are also unknown.)",
]
JOBS += [
    {"id": "ref27", "screen": "reference 27 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": INK, "max_size": 10, "new": True,
     "note": "death certificate, additional (form = ref 13 at 0.8; notes Ink Free; seal kept)",
     "items": [(D + "rrr27/0.gal", "")],
     "lines": scaled(_DC27, 0.8) + [("DEATH CERTIFICATE (additional)", [220, 86, 580, 122],
                                     {"align": "center", "max_size": 21})]
     + [(t, b, dict(o, style="handwriting", max_size=17)) for t, b, o in memo(R27, T27, right=752)],
     "ignore": [[int(v * 0.8) for v in b] for b in DC_KEEP]},
]



# ---- 52 Sakura Sushi web page (0.png 800x2222): white / light lettering on dark wood -> inpaint of the light
# glyph pixels; the two pink logo tiles are refilled flat pink and set in English; photos and the phone number kept.
_LT = [100, 255, 100, 255, 100, 255]   # IMAGES3C: was 150 / grow 2 (2x2 kernel = 1 px): left grey glyph edges
_WB = {"mask_color": _LT, "color": "#f0f0f0", "mask_grow": 5}
_NAV52 = [("Home", 30, 178), ("About Us", 178, 324), ("Menu", 324, 472), ("Delivery", 472, 620),
          ("Gallery", 620, 766)]
_ORD52 = [("Phone", 78, 190), ("Your details", 205, 315), ("Your order", 330, 440), ("Date & time", 456, 566),
          ("Delivery", 580, 690)]
_TAB52 = [("Sakura Sushi", None), ("Address", "101-5 Hayashidera, Motoki-cho, Sawa Prefecture"), ("Phone", None),
          ("Opening hours", "11:00–22:00"), ("Delivery orders", "10:30–19:00"), ("Delivery hours", "11:30–20:00"),
          ("Closed", "Tuesdays (open on public holidays)"), ("Access", "5-minute walk from Motoki Station")]
_TY52 = [1983, 2011, 2038, 2063, 2089, 2114, 2141, 2167]
SU_LINES = [
    ("Sakura Sushi   Reservations & orders here", [260, 14, 724, 47], dict(_WB, max_size=22, align="right",
                                                                        erase=[[286, 12, 724, 51]])),
    ("Sakura\nSushi", [44, 22, 170, 116], {"method": "flat", "bg": "#fdcfce", "color": "#111111", "max_size": 34,
                                         "align": "center", "erase": [[41, 15, 172, 120]]}),
    ("Sakura\nSushi", [524, 1966, 711, 2108], {"method": "flat", "bg": "#fdcfce", "color": "#111111", "max_size": 48,
                                             "align": "center", "erase": [[523, 1964, 712, 2109]]}),
] + [(t, [x0 + 6, 545, x1 - 6, 581], dict(_WB, color="#ffffff", max_size=17, align="center",
                                         erase=[[x0 + 4, 549, x1 - 4, 576]])) for t, x0, x1 in _NAV52] + [
    ("Founded Shiyo 645", [84, 650, 420, 674], dict(_WB, max_size=16)),
    ("A traditional taste nurtured in the land of Motoki", [84, 674, 520, 697], dict(_WB, max_size=16)),
    ("Sakura Sushi is a sushi restaurant a 5-minute walk from Motoki Station. It was founded in Shiyo 645; "
     "because this was then a basin deep in the mountains, it began by selling sushi as preserved food so that "
     "fresh seafood would not spoil. Sakura Sushi has pursued how to make that preserved food delicious, and how "
     "to bring it to a quality that loses nothing to Edomae sushi. Today we can serve fresh ingredients sent "
     "directly from the fishing port, so we welcome you with the finest flavors, outdoing even the sushi shops "
     "of port towns.", [84, 716, 726, 844], dict(_WB, max_size=15, line_spacing=1.05)),
    ("For New Year parties, year-end parties, celebrations, memorial services and more, we prepare menus and "
     "rooms to suit your wishes. We also take delivery and catering orders, so please feel free to contact us.",
     [84, 1060, 726, 1124], dict(_WB, max_size=15, line_spacing=1.05)),
    ("Sakura Sushi's commitment", [72, 1170, 425, 1199], dict(_WB, max_size=19)),
    ("Overwhelming technique and craftsmanship", [72, 1200, 425, 1228], dict(_WB, max_size=19)),
    ("How to make delicious sushi in Motoki, a town in a basin, has been our theme since our founding. That "
     "ingenuity and skill have been handed down to the present day, and we achieve the finest flavors not only "
     "in our nigiri sushi but in everything from clear soups and small dishes to fried foods and sweets.",
     [72, 1251, 425, 1442], dict(_WB, max_size=15, line_spacing=1.05, erase=[[72, 1251, 395, 1376]])),
    ("The finest wasabi", [72, 1452, 425, 1481], dict(_WB, max_size=19)),
    ("We use the finest wasabi from Azumino, Nagano Prefecture, grown on Sakura Sushi's own farm. Grated on "
     "sharkskin by skilled craftsmen, the wasabi is pungent even in small amounts, with a refreshing aroma. Our "
     "carefully chosen wasabi, a fine supporting player, brings out the flavor of the sushi to the fullest.",
     [72, 1480, 726, 1544], dict(_WB, max_size=15, line_spacing=1.05)),
    ("How to order", [74, 1774, 330, 1806], dict(_WB, max_size=20, erase=[[74, 1772, 222, 1806]])),
] + [(t, [x0, 1832, x1, 1872], dict(_WB, color="#ffffff", max_size=15, align="center")) for t, x0, x1 in _ORD52] + [
    ("Reservations & orders", [80, 1914, 420, 1946], dict(_WB, max_size=20, erase=[[80, 1915, 276, 1946]])),
] + [(a, [72, y - 12, 244, y + 12], dict(_WB, max_size=16)) for (a, b), y in zip(_TAB52, _TY52)] + [
    (b, [246, y - 12, 515, y + 12], dict(_WB, max_size=16)) for (a, b), y in zip(_TAB52, _TY52) if b]
JOBS += [
    {"id": "ref52", "screen": "reference 52 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#f0f0f0", "mask_grow": 2, "new": True,
     "note": "sushi-shop web page (photos and the phone number kept; logo tiles refilled)",
     "items": [(D + "rrr52/0.gal", "")], "lines": SU_LINES},
]
JOBS += [
    # 40 / 85 / 27 rebuilt by refdoc_overview.py build; 52 by work/images/_b3/ov52.py (top band only, photo kept)
    {"id": "ov-3b-a", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (40, 85, 27, 52)]},
]



# ---- 1 Oha-Oha! viewer posts (rrr1/シャベッター/0..13.png, 310x78 / 96): show name + post text; the avatar and
# "on Sha-better" (already Latin) kept. 0.png / 1.png of rrr1 are background art without text.
_SHA = ["Yukipin is the goddess of female announcers", "Show Yukipin, not the cherry blossoms",
        "Yukipin is so cute, I want to marry her", "Aaah, Yukipin's segment is over\nGuess I'll go to work",
        "Who's this old geezer in a wig", "Can't tell what this baldy is saying", "Dirty joke lol",
        "Isn't ephedrine being in cherry blossoms\njust a folk myth",
        "Can't really hear this baldy's voice", "Don't really get what he means", "Show Yukipin",
        "This baldy's talk is hard to follow", "Someone explain pls", "Show Yukipin, not the baldy"]


def _sha(t, show="Oha-Oha!"):   # IMAGES13: show name is a parameter (rrr145 cards set the GLOSSARY form)
    two = "\n" in t
    return [(show, [48, 9, 133, 34], {"style": "rounded", "color": "#1c2e46", "max_size": 17,
                                           "erase": [[48, 10, 132, 33]], "mask_color": _DK}),
            (t, [12, 42, 304, 86] if two else [12, 44, 304, 72],
             {"max_size": 15, "method": "flat", "bg": "#c7d9f1",   # IMAGES3C: flat card blue (inpaint left ghosts)
              "erase": [[12, 42, 303, 84]] if two else [[12, 47, 303, 69]]})]


JOBS += [
    {"id": "ref1-posts", "screen": "reference 1 posts", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_color": [0, 120, 0, 120, 0, 120], "mask_grow": 2, "color": "#222222", "new": True,
     "note": "viewer posts on the morning show (avatar and 'on Sha-better' kept)",
     "items": [(D + "rrr1/シャベッター/%d.gal" % n, "", {"lines": _sha(t)}) for n, t in enumerate(_SHA)],
     "lines": []},
]
_RED6 = [110, 255, 0, 95, 0, 95]
JOBS += [
    # 1: rr1 = studio picture + two post cards, rebuilt by work/images/_b3/ov1.py (English cards pasted at the
    # matched scale 0.31); 6 has no detail picture: its 概要 title is typeset in place (wording = reference title).
    {"id": "ov-1", "screen": "reference screen preview", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr1.gal", "")]},
    {"id": "ov-6", "screen": "reference screen preview", "style": "gothic", "mode": "lines", "erase": "inpaint",
     "color": "#e81010", "stroke": 1, "stroke_color": "#3a0000", "mask_grow": 2, "new": True,
     "note": "paranormal-special title card (overview only; no detail picture)", "items": [(O + "rr6.gal", "")],
     "lines": [("Paranormal Special!", [28, 54, 278, 91], {"mask_color": _RED6, "max_size": 26, "align": "center"}),
               ("~Uncanny! The Demon Flower Appears~", [20, 90, 296, 116], {"mask_color": _RED6, "max_size": 17,
                                                                           "align": "center"})]},
]



# ---- 15 Goto's memo 5 (800x1530): rows from _rows.py; arrows kept.
R15 = [[8, 7, 180, 27], [8, 31, 276, 52], [10, 56, 172, 77], [8, 81, 293, 102], [12, 132, 200, 150], [9, 155, 334, 176],
       [8, 181, 200, 200], [16, 205, 275, 226], [8, 231, 223, 250], [16, 255, 490, 275], [8, 280, 635, 300],
       [9, 305, 242, 325], [9, 355, 252, 374], [18, 379, 533, 399], [8, 404, 316, 424], [8, 429, 336, 448],
       [8, 453, 336, 473], [11, 478, 252, 498], [8, 528, 272, 547], [9, 552, 582, 573], [10, 577, 448, 598],
       [8, 627, 190, 647], [12, 652, 572, 673], [12, 677, 272, 697], [12, 701, 490, 722], [8, 726, 561, 747],
       [8, 776, 336, 796], [11, 800, 675, 821], [16, 825, 758, 846], [16, 850, 635, 871], [8, 876, 221, 895],
       [10, 925, 345, 944], [8, 949, 778, 970], [10, 975, 407, 994], [11, 999, 345, 1019], [10, 1048, 614, 1069],
       [16, 1073, 458, 1093], [16, 1098, 334, 1118], [16, 1123, 376, 1143], [8, 1148, 656, 1168], [8, 1173, 376, 1192],
       [10, 1197, 614, 1217], [14, 1223, 20, 1241], [8, 1247, 345, 1268], [14, 1272, 20, 1291], [10, 1297, 593, 1317],
       [12, 1321, 490, 1342], [11, 1346, 574, 1367], [16, 1396, 293, 1416], [12, 1421, 284, 1441], [11, 1446, 284, 1465]]
T15 = [
    "Thoughts on this case.",
    "Victim: Kogori-senpai's father",
    "Injured: Niimura-senpai",
    "Attacker: Niimura-senpai's mother?",
    "First, what needs checking.",
    "Is the culprit Niimura-senpai's mother?",
    "Checking it from the physical side.",
    "・The murder of Kogori-senpai's father",
    "→ Possible (no alibi)",
    "・Appearing at Sakuraoka Station, hitting Niimura-senpai with the car, and going back home.",
    "→ Just barely possible time-wise. Though she'd have had to drive really fast.",
    "So, physically, it's possible.",
    "Then why did she kill herself?",
    "(I can't say for certain it was suicide, but I'll treat it as suicide for now)",
    "① She had achieved the goal she staked her life on",
    "② She needed to destroy some evidence",
    "③ The suicide itself had a meaning",
    "Probably one of these three.",
    "① The goal she staked her life on: what was it?",
    "Killing Kogori-senpai's father and putting Niimura-senpai in a coma?",
    "The former aside, the latter is strange. So this one is out.",
    "② To destroy evidence?",
    "This is quite possible. There may have been important evidence in the house.",
    "But then why suicide?",
    "And of all things, she went out of her way to choose a painful death by fire.",
    "→ She needed to burn to death → Niimura-senpai's mother herself was the evidence?",
    "③ The suicide itself had a meaning",
    "For a suicide to have a meaning, it would mean conveying something to a third party.",
    "・Showing all of Japan a spectacular end, as the culprit of the Megasawa City murders and the Motoki-cho incident.",
    "・If there is an accomplice, she chose 'death by fire' as a message to that person.",
    "→ This is possible too.",
    "So, putting it together from lines ② and ③,",
    "death by fire was a meaningful way to destroy evidence, or to tell an accomplice her intentions.",
    "Or perhaps it was for both ② and ③.",
    "Well, maybe that's too convenient a deduction...",
    "What's unclear is why she drove Niimura-senpai as far as a coma.",
    "・What reason would she have to hurt her own daughter that badly?",
    "・Why didn't she finish her off?",
    "・Why did she leave Kogori-senpai unharmed?",
    "Big brake marks at the scene → my guess: hitting Niimura-senpai was not intentional.",
    "What did she chase the two of them around for?",
    "Probably because partway through it became certain the culprit's goal could not be achieved.",
    None,
    "Hitting Niimura-senpai was a miscalculation.",
    None,
    "In other words, I just need to find out what she meant to do with Niimura-senpai.",
    "But now there is no one left in the Niimura family to talk to.",
    "Probably attacking Kogori-senpai doesn't mean much (just silencing her, at most)",
    "・About Kogori-senpai's mother",
    "No need to write about this.",
    "It'll probably come out in her confession anyway.",
]
JOBS += [
    {"id": "ref15", "screen": "reference 15 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "Goto's memo (handwriting; arrows kept)", "items": [(D + "rrr15/0.gal", "")],
     "lines": memo(R15, T15), "ignore": [[12, 1220, 22, 1243], [12, 1270, 22, 1293]]},
]


# ---- 17 letter from his student days (800x1132, ruled paper). Q1970: the words the node comments point at stay
# Japanese with the English beside them: 晴れ (date line), 短刀直入 (row 4), 気づきませんでした (row 8, gloss on
# the blank rule below). The three scribbled-out words are kept as drawn; tear stains kept.
_H17 = {"max_size": 18}
L17 = [
    ("Shiyo 790, December 19   (Sunny)", [380, 50, 708, 80], dict(_H17, align="right", erase=[[512, 53, 709, 78]])),
    ("To Dai-chan,", [48, 90, 400, 116], dict(_H17, erase=[[48, 92, 145, 115]])),
    ("This is the first time I've sent you a handwritten letter, isn't it. The reason I went to the trouble of",
     [66, 160, 748, 188], dict(_H17, erase=[[69, 162, 747, 186]])),
    ("writing is that I want to tell you something important.", [48, 196, 748, 224], dict(_H17, erase=[[48, 198, 435, 222]])),
    ("(straight to the point): I'll say it. Please break up with me. For a while now, your gaze",
     [147, 231, 748, 260], dict(_H17, erase=[[146, 233, 745, 258]])),
    ("has bothered me, Dai-chan. On our dates you were always looking all around, and at first",
     [48, 267, 748, 296], dict(_H17, erase=[[49, 269, 745, 294]])),
    ("I only wondered, what is he looking at? But I never imagined that at the end of that gaze",
     [48, 303, 748, 331], dict(_H17, erase=[[49, 305, 748, 329]])),
    ("there was always a little girl; only recently I", [48, 339, 525, 367], dict(_H17, erase=[[48, 341, 526, 365]])),
    ("(did not notice)", [527, 368, 748, 394], dict(_H17, max_size=16, erase=[])),
    ("Honestly, your", [66, 408, 217, 439], dict(_H17, erase=[[67, 410, 218, 437]])),
    ("hobby is your own, Dai-chan, so I don't intend to", [259, 408, 748, 439], dict(_H17, erase=[[258, 410, 744, 437]])),
    ("make a fuss about it. Even if you like little girls, as long as you were looking at me, that",
     [48, 446, 748, 473], dict(_H17, erase=[[49, 448, 747, 471]])),
    ("was fine with me. But Dai-chan, more than at me, you were always looking for little girls,",
     [48, 481, 748, 509], dict(_H17, erase=[[48, 483, 745, 507]])),
    ("and you stopped looking at me much...", [48, 517, 748, 544], dict(_H17, erase=[[49, 519, 397, 542]])),
    ("What I truly hate is myself, getting so", [66, 588, 441, 618], dict(_H17, erase=[[66, 590, 441, 616]])),
    ("jealous of little girls like that.", [477, 588, 748, 618], dict(_H17, erase=[[477, 590, 748, 616]])),
    ("You have a strong sense of justice and you're serious, Dai-chan, so I think you would surely probably",
     [48, 623, 748, 652], dict(_H17, erase=[[48, 625, 745, 650]])),
    ("never lay a hand on a little girl. But I can't bear any longer that you only ever look at",
     [48, 659, 748, 687], dict(_H17, erase=[[49, 661, 747, 685]])),
    ("little girls and not at me.", [48, 696, 748, 723], dict(_H17, erase=[[50, 698, 435, 721]])),
    ("I'm truly sorry. This is my", [66, 728, 348, 760], dict(_H17, erase=[[67, 730, 348, 758]])),
    ("own selfishness. I knew very well that you always", [372, 728, 748, 760], dict(_H17, erase=[[372, 730, 746, 758]])),
    ("cared about me, Dai-chan. It's that I could not forgive myself for being", [48, 765, 748, 794],
     dict(_H17, erase=[[47, 767, 745, 792]])),
    ("jealous. I can no longer endure myself for getting jealous like this.", [48, 801, 748, 829],
     dict(_H17, erase=[[49, 803, 745, 827]])),
    ("A hobby like this isn't something that gets cured by talking, and I don't want to meddle in your hobby",
     [48, 837, 748, 865], dict(_H17, erase=[[50, 839, 747, 863]])),
    ("in the first place, so I will be the one to step back.", [48, 873, 748, 901], dict(_H17, erase=[[51, 875, 529, 899]])),
    ("I loved you. Goodbye.", [48, 942, 470, 972], dict(_H17, erase=[[48, 945, 300, 970]])),
    ("Rei Tanizaki", [560, 1015, 745, 1043], dict(_H17, align="right", erase=[[631, 1018, 693, 1041]])),
]
JOBS += [
    {"id": "ref17", "screen": "reference 17 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "letter (Q1970: flagged words kept in Japanese with English beside them; scribbles and tear stains kept)",
     "items": [(D + "rrr17/0.gal", "")], "lines": L17,
     "ignore": [[709, 50, 755, 80], [66, 231, 146, 260], [526, 339, 718, 366], [218, 406, 259, 440],
                [441, 574, 477, 622], [348, 718, 372, 763], [460, 905, 700, 1005]]},
]


# ---- 189 Ryoji Kogori's letter (800x1133, ruled paper, typed-hand font)
R189 = [[79, 114, 717, 137], [50, 164, 704, 188], [53, 216, 741, 239], [50, 267, 745, 291], [50, 319, 724, 342],
        [53, 371, 461, 392], [78, 422, 734, 444], [51, 473, 726, 496], [51, 525, 233, 546], [77, 575, 746, 599],
        [53, 627, 745, 650], [51, 678, 735, 702], [51, 730, 750, 753], [50, 782, 725, 805], [50, 833, 738, 855],
        [50, 884, 736, 908], [50, 935, 733, 959], [50, 987, 378, 1010]]
T189 = [
    "It is now Shiyo 800, April 6, 23:00. The reason I'm going to the trouble of putting this on paper",
    "rather than in an email is so that no evidence at all leaks out. On the night of Shiyo 800, April",
    "7, that is, tomorrow, I've decided to meet Mifuyu-san. I'll negotiate that matter. I'm sorry,",
    "Akane, but please try as hard as you can to act as usual in front of Natsumi.",
    "Needless to say, if this becomes public, Natsumi and Haruka-chan won't be able to live in",
    "society anymore. Everything is for the two of them.",
    "Above all, Natsumi must not learn anything at all. And Haruka-chan will have to live",
    "believing in the curse. Otherwise, Haruka-chan too will be erased",
    "from society.",
    "I've already told you, but be careful of Haruka-chan's mobile phone. There's no knowing",
    "what might be in this house, either. Please live as normally as you can. Trust",
    "me and wait. By the morning of April 8, it should all be over. Mifuyu-san",
    "is no fool. She won't lay a hand on our family. In exchange, I can't make Mifuyu-san's",
    "true nature known to all, either. But if the worst should happen, on April 8",
    "never leave Natsumi alone. If you end up unable to move,",
    "have her spend the time with Haruka-chan, just the two of them. If you keep her at the police",
    "station for no reason, the police may get suspicious. Do it carefully, so that Natsumi and",
    "Haruka-chan don't find out. I'm counting on you.",
]
JOBS += [
    {"id": "ref189", "screen": "reference 189 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "Ryoji Kogori's letter (ruled paper)", "items": [(D + "rrr189/0.gal", "")],
     "lines": [("To Akane,", [50, 58, 400, 88], {"max_size": 20, "erase": [[50, 60, 97, 86]]})]
     + memo(R189, T189, size=19, right=752)
     + [("Ryoji Kogori", [520, 1034, 752, 1065], {"max_size": 20, "align": "right", "erase": [[646, 1036, 751, 1063]]})]},
]


# ---- 45 movie review site (800x1067): title already Latin; chart labels, rating, synopsis, five reviews
_G45 = {"style": "gothic", "color": "#111111"}
L45 = [
    ("(Released Shiyo 799)", [250, 84, 560, 116], dict(_G45, max_size=24, align="center", erase=[[295, 84, 517, 116]])),
    ("Director: Kirk Freeman", [376, 178, 760, 213], dict(_G45, max_size=24, erase=[[376, 178, 654, 213]])),
    ("Story", [505, 230, 610, 253], {"max_size": 16, "align": "center", "erase": [[515, 230, 600, 253]]}),
    ("Cast", [694, 343, 790, 366], {"max_size": 16, "erase": [[694, 343, 760, 366]]}),
    ("Direction", [640, 507, 760, 530], {"max_size": 16, "erase": [[643, 507, 685, 530]]}),
    ("Visuals", [380, 507, 476, 530], {"max_size": 16, "align": "center", "erase": [[383, 507, 472, 530]]}),
    ("Sound", [352, 343, 421, 366], {"max_size": 16, "align": "right", "erase": [[381, 343, 421, 366]]}),
    ("Average 3.0", [36, 576, 172, 618], dict(_G45, max_size=22, erase=[[38, 576, 170, 618]])),
    ("Synopsis", [51, 648, 200, 667], dict(_G45, max_size=13, erase=[[51, 648, 87, 667]])),
    ("A live-action Hollywood remake of a moe anime. The moe anime \"Fascination\", a hit in Japan, comes back",
     [52, 669, 760, 687], dict(_G45, max_size=13, erase=[[52, 669, 723, 687]])),
    ("to Japan renewed by a big-name director! A must-see, even if you're not a fan of the original!",
     [52, 688, 760, 706], dict(_G45, max_size=13, erase=[[52, 688, 451, 706]])),
    ("That was awful...   Butterfly-san   0 points", [52, 740, 600, 758], dict(_G45, max_size=13, erase=[[52, 740, 290, 758]])),
    ("I'm a fan of the original, so I was looking forward to it, but I won't expect anything from remakes like this again.",
     [52, 759, 760, 777], {"max_size": 13, "erase": [[52, 759, 567, 777]]}),
    ("I cried!   B4U-san   5 points", [52, 796, 600, 815], dict(_G45, max_size=13, erase=[[52, 796, 244, 815]])),
    ("It was a bold remake, but I went to see it with a girlfriend and it moved me! Actually, I'd never seen the",
     [52, 815, 760, 833], {"max_size": 13, "erase": [[52, 815, 716, 833]]}),
    ("original, but I was wandering about looking for a good movie, and by chance...", [52, 834, 560, 852],
     {"max_size": 13, "erase": [[51, 834, 503, 852]]}),
    ("(Read more)", [562, 834, 680, 852], {"max_size": 13, "color": "#2a6ac8", "erase": [[503, 834, 592, 852]]}),
    ("Women will probably like it   RAVE-san   2 points", [52, 872, 600, 890], dict(_G45, max_size=13, erase=[[52, 872, 283, 890]])),
    ("I'll grant the director and the casting are good. But the screenwriter should apologize to the original's "
     "fans in Japan right now.", [52, 890, 760, 909], {"max_size": 13, "erase": [[52, 890, 603, 909]]}),
    ("I had a bad feeling   Pose-san   1 point", [52, 928, 600, 946], dict(_G45, max_size=13, erase=[[52, 928, 294, 946]])),
    ("Plenty of masterpieces defy a feeling like this, but once the title is written this way, you can guess.",
     [52, 947, 760, 965], {"max_size": 13, "erase": [[52, 947, 649, 965]]}),
    ("Give us an uncut DVD!   Shiny-san   4 points", [52, 984, 600, 1003], dict(_G45, max_size=13, erase=[[52, 984, 352, 1003]])),
    ("I went to see it with my boyfriend, but he slept through the end (lol). Honestly, it's amazing! A script",
     [52, 1003, 760, 1021], {"max_size": 13, "erase": [[52, 1003, 717, 1021]]}),
    ("no Japanese could write, and that great final scene! But I can't talk about it with him, so minus 1 point (lol).",
     [52, 1022, 760, 1040], {"max_size": 13, "erase": [[51, 1022, 518, 1040]]}),
]
JOBS += [
    {"id": "ref45", "screen": "reference 45 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#111111", "new": True,
     "note": "movie review site (title, poster, chart and stars kept)", "items": [(D + "rrr45/0.gal", "")],
     "lines": L45, "ignore": [[270, 25, 545, 80], [5, 170, 360, 372], [360, 230, 700, 520], [172, 570, 460, 625]]},
]


# ---- 69 picture of the demon flower: 0.png front (drawing + labels), 1.png back (5 vertical columns, right to
# left), 16 turning frames via refdoc_flip.py. English = the shipped node comments (verbatim).
_INK69 = [0, 95, 0, 95, 0, 80]
_HALO = "#d6d2b4"
L69F = [
    ("After the fierce horn, the dead and the demon flowers", [150, 252, 498, 288],
     {"max_size": 20, "mask_color": _INK69, "mask_grow": 2, "erase": [[158, 256, 492, 287]]}),
    ("bloom in profusion.", [150, 293, 330, 327], {"max_size": 20, "mask_color": _INK69, "mask_grow": 2,
                                                  "erase": [[152, 296, 300, 327]]}),
    ("Mount Itohime", [292, 352, 470, 388], {"max_size": 20, "mask_color": _INK69, "mask_grow": 2,
                                            "erase": [[296, 354, 404, 387]]}),
    ("Valley", [220, 556, 303, 590], {"max_size": 18, "align": "right", "mask_color": _INK69, "mask_grow": 2,
                                     "erase": [[270, 556, 303, 590]]}),
    ("Settlement", [50, 588, 175, 622], {"max_size": 18, "align": "center", "mask_color": _INK69, "mask_grow": 2,
                                        "erase": [[70, 588, 148, 622]]}),
]
_COLS69 = [  # (x0, x1, y_end of the JP column, English) right to left
    (339, 368, 600, "The dead come forth from Yomi and demon flowers beyond all nature stand in rows"),
    (305, 334, 600, "Those who have become corpses also become demon flowers and come forth from Yomi"),
    (271, 298, 400, "Only the Green Eye prevails"),
    (236, 265, 615, "Those who have become Green Eyes wither the demon flowers and return the dead to Yomi"),
    (169, 196, 600, "Descendants must without fail don a mask and vestments the color of blood and resist"),
]
L69B = [(t, [x0, 12, x1, ye], {"rot": -90, "max_size": 15, "mask_color": [0, 75, 0, 80, 0, 50], "mask_grow": 3,
                               "erase": [[x0 - 2, 10, x1 + 2, ye + 4]]}) for x0, x1, ye, t in _COLS69]
JOBS += [
    {"id": "ref69-front", "screen": "reference 69 detail", "style": "serif", "mode": "lines", "erase": "texfill",  # IMAGES3C: was inpaint
     "erase_first": True, "color": "#1a1a1a", "stroke": 2, "stroke_color": _HALO, "new": True,
     "note": "demon-flower picture, front labels (drawing kept; paper-coloured halo as in the original)",
     "items": [(D + "rrr69/0.gal", "")], "lines": L69F},
    {"id": "ref69-back", "screen": "reference 69 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1c1e00", "new": True,
     "note": "demon-flower picture, back: five columns set top-to-bottom, right to left (faint see-through of the "
             "front left as drawn)", "items": [(D + "rrr69/1.gal", "")], "lines": L69B},
    {"id": "ref69-flip", "screen": "reference 69 turning frames", "style": "serif", "mode": "asis", "chain": True,
     "items": [(D + "rrr69/%s.gal" % n, "") for n in ("1_1", "2", "3", "4", "5", "図画6", "図画7", "図画8", "図画9",
                                                      "10", "11", "12", "13", "14", "15", "16")]},
]
JOBS += [
    {"id": "ov-3b-b", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (15, 17, 189, 45, 69)]},
]



# ---- 29 Megasawa Newspaper 2 (0.png 800x518 + 6 close-ups) and 91 the Motoki Daily (0.png 800x518 + 5 close-ups):
# same method as ref23 (vertical columns -> horizontal English blocks per article box, in reading order; vertical
# headlines top-to-bottom; textured paper: inpaint of the dark glyphs, column rules restored).
N29_CAP = "Shigefumi Hiramatsu-san (35) and Kayoko Endo-san (44), who were killed"
N29_A = ("Shortly before 8 p.m. on April 8, in Nanami-cho, Megasawa City, Shigefumi Hiramatsu-san (35), a teacher "
         "at Megasawa Second Elementary School, and Kayoko Endo-san (44), president of the same school's PTA, were "
         "brutally murdered by someone.")
N29_SUB = "Strikingly like the case 4 years ago. An impossible method?"
N29_B = ("A similar case occurred in Nanami-cho, Megasawa City, 4 years ago too, and there is still no lead "
         "toward solving it.")
N29_C = ("Unlike last time, it happened at night, when visibility was poor. Even allowing for that, there were no "
         "witnesses to so bold a murder, and the method was so extremely skillful and cruel that it hardly "
         "seems human.")
N29_D = ("Neighbors, too, say the two victims were not people who would be hated this much, so the possibility "
         "of an indiscriminate killing cannot be ruled out. At the same time, as with the last case, this method "
         "that seems beyond human ability has")
N29_E = ("not a few voices worrying that it may be the work of a spiriting-away, and some even say the whole town "
         "should be purified together. The board of education or the police are also issuing warnings to "
         "elementary, junior high and high schools, nursery schools and kindergartens across the city, including "
         "Megasawa Second Elementary School, and parents are to be advised to accompany children to and from "
         "school. However, as two adults were the victims this time, even being accompanied by a parent is no "
         "reason for optimism.")
N29_F1 = ("Because the circumstances closely resemble the murders of two elementary schoolchildren in Shiyo 790, "
          "many believe the same culprit did it. So how much do the last case and this one have in common? The "
          "first point is a method said to be impossible for a human.")
N29_F2 = ("Specifically, judging from how the killings were done, it would take running 50 meters in 3 seconds, "
          "jumping more than 2 meters, and strength enough to cut a human in two with one stroke of a blade. This "
          "is the main reason for the voices saying it was not a human but a spiriting-away of some kind.")
N29_F3 = ("There are other points in common: it happened on April 8, there were two victims, they were killed at "
          "almost the same time, they were connected with Megasawa Second Elementary School, and it happened in "
          "Nanami-cho. But how much is coincidence and how much is intended is unclear. However, given this many "
          "points in common and")
N29_F4 = ("a crime carrying so strong a message, the possibility of large-scale organized crime, such as by a "
          "cult, rather than a grudge cannot be ruled out. In any case, what happens on April 8 should be watched "
          "closely for the next several years.")
_NG = dict(_NB, style="gothic")
_NG2 = dict(_NB2, style="gothic")
NP29 = [
    ("MEGASAWA NEWSPAPER", [286, 5, 512, 32], dict(_NB2, max_size=16, align="center")),
    ("Shiyo 794, April 9   Friday   No. 26145", [560, 5, 796, 31], dict(_NB2, max_size=13, align="right")),
    (N29_CAP, [258, 122, 548, 141], dict(_NB2, max_size=11, align="center")),
    (N29_A, [412, 148, 548, 262], dict(_NB2, max_size=11)),
    (N29_SUB, [343, 148, 410, 262], dict(_NG2, max_size=12)),
    (N29_B, [261, 148, 341, 262], dict(_NB2, max_size=11)),
    (N29_C, [417, 268, 550, 390], dict(_NB2, max_size=11)),
    (N29_D, [263, 268, 415, 390], dict(_NB2, max_size=11)),
    (N29_E, [263, 394, 549, 512], dict(_NB2, max_size=11)),
    ("The nightmare of 4 years ago returns", [612, 150, 666, 508], dict(_NB2, rot=-90, max_size=40, align="center")),
    ("Elementary school teacher and PTA president butchered", [568, 118, 612, 418],
     dict(_NB2, rot=-90, max_size=20, align="center")),
    ("Again, no clues", [568, 420, 612, 508], dict(_NB2, rot=-90, max_size=20, align="center")),
    ("Truly impossible for a human?", [202, 55, 256, 335], dict(_NB2, rot=-90, max_size=30, align="center")),
    ("Comparing the methods", [202, 370, 256, 505], dict(_NB2, rot=-90, max_size=30, align="center")),
    (N29_F1, [16, 40, 199, 150], dict(_NB2, max_size=11)),
    (N29_F2, [16, 156, 199, 272], dict(_NB2, max_size=11)),
    (N29_F3, [12, 276, 200, 390], dict(_NB2, max_size=11)),
    (N29_F4, [12, 396, 200, 512], dict(_NB2, max_size=11)),
    ("MEGASAWA\nNEWSPAPER", [693, 48, 776, 346], dict(_NB, mask_grow=5, no_rules=True, rot=-90, max_size=40, align="center",
                                                    erase=[[692, 38, 777, 350]])),
    ("Publisher\nMegasawa Newspaper Co.\n31-16 Kokuji, Megasawa City,\nIizawa Prefecture\nPostcode 995-XXXX\n"
     "© Megasawa Newspaper Co. 794\nPhone 226(541)XXXX", [686, 356, 792, 440], dict(_NB2, max_size=9)),
    ("Game creation tool,\nno programming needed", [686, 445, 792, 490], dict(_NB2, max_size=10, align="center")),
]
JOBS += [
    {"id": "ref29", "screen": "reference 29 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "color": INK, "new": True,
     "note": "newspaper page (photos and the LiveMaker logo kept)", "items": [(D + "rrr29/0.gal", "")],
     "lines": NP29, "ignore": [[300, 40, 505, 115], [686, 490, 790, 519]]},
    {"id": "ref29-zoom", "screen": "reference 29 close-ups", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "color": INK, "new": True,
     "note": "newspaper close-ups (same English as the page, larger)",
     "items": [(D + "rrr29/部分拡大%d.gal" % n, "", {"lines": L}) for n, L in (
         (1, [(N29_CAP, [6, 146, 482, 184], dict(_NB, max_size=20, align="center"))]),
         (2, [(N29_A, [300, 4, 560, 218], dict(_ZB2, max_size=17)), (N29_SUB, [165, 4, 296, 218], dict(_ZB2, style="gothic", max_size=20)),
              (N29_B, [4, 4, 160, 218], dict(_ZB2, max_size=17))]),
         (3, [(N29_C, [290, 4, 538, 244], dict(_ZB2, max_size=18)), (N29_D, [4, 4, 286, 244], dict(_ZB2, max_size=18))]),
         (4, [(N29_E, [4, 4, 538, 228], dict(_ZB2, max_size=18))]),
         (5, [(N29_F1, [4, 4, 335, 218], dict(_ZB2, max_size=19)), (N29_F2, [4, 228, 335, 441], dict(_ZB2, max_size=19))]),
         (6, [(N29_F3, [4, 4, 330, 226], dict(_ZB2, max_size=19)), (N29_F4, [4, 236, 330, 455], dict(_ZB2, max_size=19))]),
     )],
     "lines": []},
]

N91_CAP = "Chuo Park, where the first butchered body was found (photographed 7:30 a.m.)"
N91_1 = ("Shortly after 5 a.m. on April 8, the brutally murdered body of a man was found in Chuo Park. The victim "
         "was Ryoji Kogori-san (42), a Motoki-cho resident; he was found by a man who was setting up a stall for "
         "the 70th Motoki Cherry Festival.")
N91_2 = ("The day before the incident, Kogori-san told his family he was going on a business trip, and no one had "
         "known where he was since that night. Kogori-san's body was found with the skin flayed from the whole "
         "body, and he was reportedly still breathing when found.")
N91_3 = ("Also, around 9 p.m. the same day, Erina Goto-san (15), who lives in the town, was found killed by someone "
         "near Shirogaoka Nursery School. The cause of death was crushing of the brain from a heavy blow to the "
         "head. Then around 11 p.m., Akane Kogori-san (42) and Natsumi Kogori-san (16), who live nearby, were also "
         "found killed in their home.")
N91_4 = ("Ryoji Kogori-san, found early in the morning, and Akane-san and Natsumi-san, killed at night, were family, "
         "and someone is thought to have targeted the Kogori family. The police have stated their view that "
         "Goto-san, also killed, was close to the Kogoris and was caught up in some trouble.")
N91_5 = ("Mifuyu Niimura-san (42) and Haruka Niimura-san (17), also residents of the town and thought to be "
         "connected with the incident, are missing, and the police are investigating a link with the Chuo Park "
         "incident of the morning of April 8.")
NP91 = [
    ("THE MOTOKI DAILY", [270, 4, 516, 30], dict(_NB2, max_size=15, align="center")),
    ("Shiyo 800, April 9   Thursday   No. 12561", [520, 4, 796, 30], dict(_NB2, max_size=13, align="right")),
    ("4 butchered in Motoki-cho", [26, 48, 664, 134], {"style": "gothic", "color": "#ffffff", "max_size": 66,
                                                       "align": "center", "method": "flat", "bg": "#000000", "no_rules": True,
                                                       "erase": [[24, 46, 666, 136]]}),
    (N91_CAP, [58, 370, 404, 394], dict(_NG2, max_size=12, align="center")),
    (N91_1, [422, 155, 588, 276], dict(_NB2, max_size=11)),
    (N91_2, [422, 282, 588, 398], dict(_NB2, max_size=11)),
    (N91_3, [372, 404, 585, 512], dict(_NB2, max_size=11)),
    (N91_4, [172, 404, 368, 512], dict(_NB2, max_size=11)),
    (N91_5, [20, 404, 168, 512], dict(_NB2, max_size=11)),
    ("The Megasawa City murders again?", [617, 150, 669, 505], dict(_NB2, rot=-90, max_size=40, align="center")),
    ("Can the April 8 tragedy not be stopped?", [590, 185, 617, 455], dict(_NB2, rot=-90, max_size=20, align="center")),
    ("MOTOKI\nDAILY", [700, 48, 772, 240], dict(_NB, mask_grow=5, no_rules=True, rot=-90, max_size=36, align="center", erase=[[700, 45, 772, 300]])),
    ("Publisher\nMotoki Magazine Co.\n1-1 Shirogaoka,\nMotoki-cho,\nSawa Prefecture\nPostcode 909-0036\n"
     "© Motoki Magazine Co.\nShiyo 800\nPhone 126(991)XXXX", [697, 244, 773, 394],
     dict(_NB2, max_size=10, align="center", erase=[[697, 300, 773, 394]])),
    ("Game creation tool,\nno programming needed", [686, 398, 792, 446], dict(_NB2, max_size=10, align="center")),
]
JOBS += [
    {"id": "ref91", "screen": "reference 91 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "color": INK, "new": True,
     "note": "newspaper page (photo and the LiveMaker logo kept; banner refilled black)",
     "items": [(D + "rrr91/0.gal", "")], "lines": NP91, "ignore": [[58, 172, 402, 368], [686, 448, 792, 518]]},
    {"id": "ref91-zoom", "screen": "reference 91 close-ups", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "color": INK, "new": True,
     "note": "newspaper close-ups (same English as the page, larger)",
     "items": [(D + "rrr91/部分拡大%d.gal" % n, "", {"lines": [(t, b, dict(_ZB2, max_size=18))]}) for n, t, b in (
         (1, N91_1, [4, 4, 302, 216]), (2, N91_2, [4, 4, 309, 223]), (3, N91_3, [4, 4, 376, 211]),
         (4, N91_4, [4, 4, 379, 213]), (5, N91_5, [4, 4, 270, 212]))],
     "lines": []},
    {"id": "ov-29-91", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr29.gal", ""), (O + "rr91.gal", "")]},
]



# ---- memo lists 7, 72, 75, 76, 83 (Goto's handwritten memos; same memo() method). 72 carries yellow
# highlighter: inpaint of the dark glyph pixels so the highlight survives under the English. 76 = 75 with the last
# paragraph scribbled out by hand: the scribble and what shows through it are kept.
def _mk(lines, **extra):
    return [(t, b, dict(o, **extra)) for t, b, o in lines]


R7 = [[19, 7, 400, 26], [9, 32, 400, 51], [8, 56, 400, 76], [8, 105, 400, 126], [12, 131, 233, 151], [33, 156, 233, 176],
      [11, 181, 233, 200], [32, 205, 233, 225], [11, 230, 233, 249], [32, 254, 233, 274], [10, 279, 233, 298],
      [30, 304, 233, 324], [8, 403, 520, 423], [16, 429, 520, 448], [16, 453, 520, 472], [16, 478, 520, 498],
      [16, 503, 520, 522], [16, 528, 520, 548], [16, 553, 520, 572], [8, 602, 520, 622], [16, 627, 520, 646],
      [16, 652, 520, 671], [16, 677, 520, 696], [16, 701, 520, 721], [9, 727, 520, 746]]
T7 = ["An incident at Chuo Park!!", "So April 8 really is that kind of day??", "Look into the Megasawa City murders!",
      "Megasawa City murders: findings (online)", "1st: Shiyo 790, April 8", "two second-graders butchered",
      "2nd: Shiyo 794, April 8", "a teacher and the PTA president butchered", "3rd: Shiyo 797, April 8",
      "two junior high students butchered", "This time: Shiyo 800, April 8", "one butchered (identity unknown)",
      "What the three incidents other than this one have in common...", "・They happened on April 8",
      "・The victims were connected with schools", "・They happened in Megasawa City", "・Every 3 to 4 years",
      "・Butchered in a truly awful state", "・No suspects, no clues", "What they have in common with this incident...",
      "・It happened on April 8", "・Every 3 to 4 years", "・Butchered in a truly awful state",
      "・Suspects, clues? (not much time has passed yet)", "Maybe it's a copycat after all..."]
R7R = [[411, 177, 647, 194], [409, 199, 609, 216], [409, 222, 563, 238], [411, 243, 687, 261], [409, 266, 684, 283],
       [412, 288, 680, 306]]
T7R = ["Is there a pattern to this??", "But this time alone is odd...", "In Motoki-cho, and only one person.",
       "The incidents came 4 years, 3 years and 3 years", "apart. What pattern could that be...",
       "For now, on-site investigation for this one!"]
_M7 = memo(R7, T7)
_M7 = [(t, [b[0], b[1], 240 if 4 <= i <= 11 else 796, b[3]], o) for i, (t, b, o) in enumerate(_M7)]
JOBS += [
    {"id": "ref7", "screen": "reference 7 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "Goto's memo 3 (bracket and arrow kept)", "items": [(D + "rrr7/0.gal", "")],
     "lines": _M7 + memo(R7R, T7R, size=16, right=798), "ignore": [[238, 120, 400, 330]]},
]

R72 = [[10, 7, 173, 27], [17, 32, 193, 52], [16, 57, 438, 76], [16, 81, 398, 101], [16, 106, 275, 126], [16, 131, 399, 151],
       [17, 156, 213, 176], [17, 180, 298, 200], [456, 203, 475, 204], [17, 205, 600, 225], [9, 230, 480, 249],
       [29, 255, 331, 275], [12, 304, 228, 324], [16, 329, 523, 349], [16, 354, 645, 374], [12, 379, 315, 399],
       [8, 403, 522, 424], [8, 428, 522, 449], [9, 453, 88, 473], [10, 478, 789, 498], [11, 502, 799, 523],
       [11, 528, 656, 547], [9, 552, 170, 572], [12, 577, 791, 596], [11, 603, 273, 621], [9, 627, 132, 646],
       [12, 652, 750, 671], [9, 676, 90, 696], [8, 701, 315, 720], [8, 750, 799, 771], [11, 777, 331, 795],
       [8, 825, 170, 845], [16, 849, 513, 870], [16, 875, 296, 894], [9, 924, 186, 944], [9, 948, 223, 969],
       [8, 974, 793, 994], [10, 998, 558, 1018], [9, 1049, 170, 1067], [8, 1073, 372, 1093], [9, 1097, 562, 1117],
       [9, 1122, 552, 1143], [11, 1147, 397, 1167], [9, 1172, 780, 1192], [9, 1221, 108, 1241], [16, 1246, 451, 1266],
       [16, 1272, 337, 1291], [17, 1296, 471, 1316], [9, 1320, 414, 1340], [16, 1345, 637, 1365], [9, 1395, 112, 1415],
       [9, 1419, 490, 1439], [9, 1444, 476, 1464], [10, 1469, 792, 1489], [13, 1494, 442, 1514], [11, 1518, 470, 1538],
       [10, 1543, 624, 1563], [13, 1568, 449, 1588], [10, 1593, 789, 1613], [9, 1618, 222, 1637], [8, 1667, 132, 1687],
       [17, 1692, 368, 1712], [17, 1715, 575, 1737], [17, 1742, 376, 1762], [17, 1766, 355, 1786], [9, 1816, 132, 1836],
       [17, 1841, 338, 1861], [9, 1865, 791, 1886], [11, 1891, 791, 1911], [10, 1915, 789, 1935], [11, 1940, 449, 1960],
       [11, 1964, 793, 1985], [9, 1990, 222, 2010], [13, 2039, 356, 2058], [16, 2064, 275, 2083], [16, 2089, 296, 2108],
       [13, 2113, 788, 2133], [10, 2139, 429, 2158], [10, 2164, 565, 2184], [347, 2185, 521, 2186], [12, 2188, 780, 2208],
       [11, 2212, 790, 2233], [10, 2238, 56, 2257]]
T72 = [
    "Chuo Park: findings", "・Several people saw the body",
    "・Age and sex could not be told → wasn't wearing clothes?", "・Found by a 68-year-old man setting up a stall",
    "・Found around 5:10 a.m.", "・Still alive when found! ← this is important", "・The body was bright red",
    "・But died before the ambulance arrived", None,
    "・A fatal accident at Chuo Park on April 8 more than 10 years ago ← super important!!",
    "→ Apparently he doesn't remember exactly how many years ago it was...", "Let's check old newspapers later!",
    "Goto's analysis starts here!!", "・Age and sex can't be told → the body must be very badly damaged",
    "・Still alive when first found → alive despite that much damage???", "A body ends up like this from...",
    "burning to death, dissolving in acid, a flayed body, or a skin disease: those four?",
    "Anyway, it was a body with something wrong with its skin", "① Burned to death?",
    "Actually, burning doesn't make it so bad you can't tell the sex. And if it were burned that much, it couldn't",
    "still be alive, and dumping it in the park would probably be very hard too. Burning it in the park is possible,",
    "but realistically that can't be... Besides, it wouldn't turn bright red.", "② Dissolved by acid?",
    "This is plausible. Depending on how it's done, one can stay alive for a while. But dying at such a perfect",
    "moment...?", "③ A flayed body",
    "Plausible for the same reason as acid. But again, the timing of death is too perfect", "④ A skin disease",
    "Out of the question. It wouldn't even be a crime...",
    "Either dissolved by acid or flayed. Depending on how it's done, apparently one can live for nearly a day.",
    "Let's ask around a bit more!", "What I found out...",
    "・When first found, crows were swarming the body (scary...)", "・The body was an even red, with few patches",
    "Goto's analysis, part 2!", "The flayed-body theory is the strongest.",
    "If it were dissolved by acid, the crows would probably dislike the acid and stay away, and there would surely be",
    "patches. If the skin was flayed with a blade, that's easier to control!", "From all the above...",
    "My guess: the victim had been flayed and was dying!",
    "The direct cause of death: blood loss after crows tore through an artery?",
    "The culprit seems to have dumped the body timed for when the crows wake up.",
    "Then the body was dumped around 4 to 5 a.m.?",
    "The crime scene was almost certainly not Chuo Park. That means the body was carried by car.",
    "The culprit's profile?", "・18 or older (has a driver's license)",
    "・Understands the structure of the human body quite well", "・Practiced (the Megasawa City murderer after all?)",
    "→ For the Megasawa City murders, see the earlier memo!",
    "・If determined, possible for a lone culprit, even a woman (just needs to carry one person)",
    "Culprit profile: hypotheses", "If several culprits or a man, it could be done without knowing the victim.",
    "If a lone culprit or a woman, very likely an acquaintance!",
    "Nobody lets themselves be flayed alive quietly, so you'd have to tie them down somehow, knock them out,",
    "or the like → someone the victim would let their guard down with",
    "If the victim is a Motoki-cho resident, the culprit may be one too.",
    "Since they went out of their way to do it in Motoki-cho, maybe both victim and culprit are residents?",
    "Which means the victim may currently be missing...",
    "At least the culprit is a Motoki-cho resident, right. Dumping a body in Chuo Park without being seen",
    "is impossible without knowing the area.", "Victim profile: hypotheses",
    "・Sex and age both unknown (not a child)",
    "・Likely a Motoki-cho resident (watch for anyone not in Motoki-cho today!)",
    "・Some connection with the Megasawa City murders?", "・If the culprit acted alone, the victim knew the culprit",
    "Crime scene: hypotheses", "・A place where one is extremely unlikely to be seen",
    "→ Possibly someone's home or inside a car. Otherwise the bleeding and so on would quickly",
    "give the scene away, and the things left behind would lead to the culprit in no time. Or",
    "the scene had been prepared very carefully beforehand. Hmm, this is hard to guess... Anyway,",
    "it was definitely a place out of sight.",
    "Ah, but thinking of it that way, it's quite different from the Megasawa City murders. In the Megasawa City murders,",
    "the crime scene = where the bodies were found.", "Forcing a summary for now...", "・The body had been flayed",
    "・The crime scene is not Chuo Park",
    "that's about it... Why go to the trouble of carrying it to Chuo Park? They clearly wanted it",
    "found. They could have hidden it in the mountains...",
    "Hm? Then does that mean the culprit doesn't even intend to run?", None,
    "Hmm, I can't tell more than this. Maybe at least it's a different person from the Megasawa City murderer.",
    "Or maybe there wasn't much time to prepare. For a copycat it's far too different,", "after all.",
]
JOBS += [
    {"id": "ref72", "screen": "reference 72 detail", "style": "handwriting", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 4, "color": "#1a1a1a", "new": True,
     "note": "Goto's memo 1 (yellow highlighter kept under the English; it no longer matches the line lengths)",
     "items": [(D + "rrr72/0.gal", "")], "lines": _mk(memo(R72, T72, size=17), mask_color=[0, 170, 0, 170, 0, 170], mask_grow=4)},   # IMAGES3C: was 140 / 2
]

R75 = [[91, 53, 382, 74], [99, 80, 496, 100], [99, 105, 473, 126], [99, 131, 495, 151], [99, 156, 571, 177],
       [99, 183, 410, 203], [99, 208, 345, 229], [99, 234, 388, 254], [94, 259, 515, 280], [91, 336, 339, 357],
       [99, 362, 624, 383], [91, 388, 411, 408], [99, 413, 410, 434], [99, 440, 429, 460], [91, 465, 495, 485],
       [91, 491, 515, 511], [113, 516, 505, 537], [116, 542, 644, 562], [99, 568, 386, 588], [91, 595, 343, 613],
       [91, 644, 382, 665], [99, 670, 496, 691], [99, 696, 645, 717], [92, 749, 312, 768], [92, 773, 505, 794],
       [94, 799, 505, 819], [95, 824, 569, 845], [90, 850, 558, 871], [91, 876, 322, 896]]
T75 = [
    "Analyzing Kogori-senpai's dream!!", "・A cherry tree in full bloom appears in a pitch-dark landscape",
    "・A bright red person is lying under the cherry tree", "・Senpai runs over and meets that person's eyes",
    "・It was asking for help in a groaning voice (really?)", "・What she took for petals was blood falling",
    "・Senpai gets grabbed by the ankle", "・That person screams at her and the dream ends",
    "Hmm, for a dream about being attacked, a lot of it is strange...", "Questions for Kogori-senpai!!",
    "・Sex and age unknown, but the scream sounded like a man's", "→ Then let's say a man, for now",
    "・It didn't say 'help me'", "・When their eyes met, it grabbed her ankle?",
    "→ After Senpai said 'I'll call for help'", "→ So it wasn't asking for help?",
    "If so, what was it trying to do to Senpai?", "In this situation, the goal was to keep Senpai from moving, maybe?",
    "・What did it scream at the end?", "→ Apparently she doesn't know...", "Summing up Kogori-senpai's dream!!",
    "・Seems like a warning: 'Don't go!'", "・Given Senpai's intuition, there really is some kind of danger",
    "Who could it be...", "It's just like the situation of the Chuo Park victim,",
    "so it's probably a dream from Senpai's usual intuition...", "Which means a man who would warn Senpai of danger,",
    "someone not in Motoki-cho right now, is the victim?", "Kogori-senpai's father...?",
]
_MEMO = {"style": "handwriting", "mode": "lines", "erase": "maskfill", "erase_first": True, "text_only": True,
         "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True}
JOBS += [
    dict(_MEMO, id="ref75", screen="reference 75 detail", note="Goto's memo 2 (before part of it was erased)",
         items=[(D + "rrr75/0.gal", "")], lines=memo(R75, T75)),
    dict(_MEMO, id="ref76", screen="reference 76 detail",
         note="Goto's memo 2' (the scribbled-out last paragraph kept as drawn)",
         items=[(D + "rrr76/0.gal", "")], lines=memo(R75[:23], T75[:23]), ignore=[[60, 725, 600, 905]]),
]

R83 = [[10, 7, 475, 27], [16, 32, 550, 52], [16, 58, 679, 79], [16, 83, 336, 104], [9, 135, 367, 154], [16, 160, 765, 181],
       [16, 186, 498, 206], [7, 238, 105, 257], [11, 263, 421, 284], [16, 289, 624, 309], [16, 315, 635, 334],
       [7, 366, 110, 385], [11, 392, 400, 411], [12, 417, 367, 437], [9, 442, 656, 463], [10, 469, 336, 488],
       [7, 520, 209, 540], [11, 546, 464, 565], [9, 571, 614, 591], [8, 597, 528, 617], [10, 623, 614, 642],
       [9, 648, 763, 668], [8, 699, 402, 719], [8, 724, 656, 745], [10, 752, 378, 770], [8, 776, 207, 796],
       [16, 802, 326, 822], [16, 827, 541, 848], [12, 853, 763, 873], [8, 879, 207, 899]]
T83 = [
    "Summary of what I heard from Ojisan! at Zahha", "・Niimura-senpai's father already died 12 years ago.",
    "・He fell to his death trying to get a balloon Kogori-senpai let go of (his neck was pierced by a fence)",
    "・No sign of foul play at all. Many witnesses.", "Putting the above together with the present situation...",
    "・Niimura-senpai has been lying to Kogori-senpai all along (she hid her father's death!)",
    "・Kogori-senpai was too small to remember the accident", "Question 1",
    "Why did Niimura-senpai keep quiet to Kogori-senpai?",
    "・Because it'd be too heavy for her to learn he died because of her?",
    "・If there's another reason... hmm, I can't think of one...", "Question 2",
    "Why didn't Mr. and Mrs. Kogori tell their daughter?", "Was this also out of consideration for Kogori-senpai?",
    "But Kogori-senpai is already 16. It's about time she was told...", "I really do sense something else.",
    "Question 3 (important!!)", "Why didn't the Kogori family move out of Motoki-cho?",
    "Given Kogori-senpai's health, they should move out of Motoki-cho, with all its cherry trees.",
    "If I were a parent I'd do that, but the Kogori family didn't.",
    "In other words, there was a reason they couldn't move out of Motoki-cho.",
    "Maybe their jobs and such, but even so, they're leaving her April sickness alone too much...",
    "More info! from the Iizawa Prefectural Police via Ojisan",
    "At the time of the first Megasawa City murders, Niimura-senpai apparently showed the police a paper doll.",
    "But of course that couldn't be evidence...", "By Niimura-senpai's logic,",
    "・The person written on the paper doll is cursed", "・Niimura-senpai apparently said 'My father killed them'",
    "That makes Niimura-senpai's mother suspicious, but in the end her alibi is perfect and there's no evidence.",
    "The case went unsolved...",
]
JOBS += [
    dict(_MEMO, id="ref83", screen="reference 83 detail", note="Goto's memo 4", items=[(D + "rrr83/0.gal", "")],
         lines=memo(R83, T83)),
    {"id": "ov-memos", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (7, 72, 75, 76, 83)]},
]



# ---- 書簡 calligraphy letters (10, 16, 182, 286, 313, 314 + scope addition 68, 209): two faces each (0 = pale
# paper, 1 = gold paper, same text layout). Newspaper precedent (ref23): the vertical columns become horizontal
# English blocks in the text area, in reading order, block 1 where the JP text starts (right), sentences may cross
# a block edge. Inpaint of the dark brush pixels over the whole text area (local erase only; the paper texture is
# re-synthesised, so these pages are the first candidates for a paid inpaint if the owner wants one).
def split_blocks(text, n):
    """split text into n parts of about equal length, at sentence ends where possible."""
    import re
    sents = re.findall(r'[^.!?]+[.!?]+["”]?\s*|[^.!?]+$', text)
    total = sum(len(s) for s in sents)
    parts, cur = [], ""
    for s in sents:
        cur += s
        if len(parts) < n - 1 and len(cur) >= total / n * 0.92:
            parts.append(cur.strip()); cur = ""
    parts.append(cur.strip())
    while len(parts) < n:
        parts.append("")
    return parts


def letter(text, x0, x1, n, sig=None, sig_box=None, gap=24, size=20):
    """lines for a letter page: body area x0..x1 (y 0..450) as n blocks right to left; sig = signature (rot -90)."""
    w = (x1 - x0 - gap * (n - 1)) / float(n)
    out = []
    for i, part in enumerate(split_blocks(text, n)):
        bx1 = int(x1 - i * (w + gap)); bx0 = int(bx1 - w)
        out.append((part, [bx0, 14, bx1, 440], {"max_size": size, "line_spacing": 1.12,
                                                "erase": [[x0, 0, x1, 450]] if i == 0 else []}))
    if sig:
        out.append((sig, sig_box, {"rot": -90, "max_size": 26, "align": "right"}))
    return out


L10 = ("I escaped with my life. I have set foot on battlefields many times, but never before had I fought a battle "
       "so ready to die. For the enemy was not human; they were demon warriors. \"Demon warriors\" is a figure of "
       "speech, of course, but I can find no other comparison. They are on far too different a plane to be called "
       "human. A single demon warrior cut down more than ten of our soldiers in the blink of an eye and went on "
       "toward our lord. Though we outnumbered them more than tenfold, we could do nothing, and our lord's head "
       "was taken. Yet there is nothing to regret in this battle. No strategy could have done anything about that. "
       "Coming back alive from that battle is itself our greatest achievement. How will people of later ages see "
       "this battle? Some will say the heavy rain kept us from hearing the surprise attack. Some will say the "
       "bowl-shaped ground left us nowhere to flee. Certainly every theory one can imagine leaves room for "
       "examination. But our Magawa army could never lose to anything of that sort. There is not one chance in ten "
       "thousand that the full strength of the noble Magawa house would fall to some petty lord or other. If it is "
       "possible at all, it is that the petty lord's soldiers themselves have power like demon warriors. Yes, that "
       "was not one chance in ten thousand but one in a hundred million, and yet it happened. Every comrade who "
       "survived says the same as I do, so that horde of demon warriors truly existed. I send this letter to tell "
       "you: beware of the petty lord called Ouda. It is not meant as a historical document. Sooner or later the "
       "Ouda house will invade the Takeda domain too. This is the last token of the alliance between the Magawa "
       "and Takeda houses that I can offer. Please convey this to Lord Genshin. Should Lord Genshin pass away in "
       "future, never, ever think of fighting the Ouda house. The only one who can stand against that horde of "
       "demon warriors is Lord Genshin, who has fully devised measures against them.")
L16 = ("It pains my heart to have deceived that man. But it was necessary for us to live. Surely he will take the "
       "realm. But that has nothing to do with us, the people of Arata. We only wish to live here in peace. That "
       "is the will not of me alone but of every resident. Has it been ten years now since I moved to this "
       "settlement? I believe I can use the language of this land of the rising sun without difficulty. I "
       "sometimes almost forget even my own true name, but I was called Sere. And I understand this country's "
       "circumstances too. Many have entered an age of rival warlords, each seeking the realm for himself, "
       "killing, plundering and attacking one another. To end so mad a world, that medicine should be of use. And "
       "once the realm is united in someone's hands, the things that threaten this settlement should grow fewer "
       "than now, even if they do not vanish. This country has no god. God is only in this settlement. Only the "
       "people of this settlement listen to what I say. No, perhaps my preaching would have gone well had I gone "
       "to other lords, but it seems I had no luck. Every lord I was granted an audience with all but said, \"Who "
       "could believe in a Western god?\" Then I will tell the way of salvation to those who believe, few though "
       "they are. That hideous army of death of the Demon King that arose in my homeland: such a thing must never "
       "happen again. May everlasting peace come to this land of Arata.")
L182 = ("How great a reward will I get? Since that day the pounding in my chest will not settle, and I cannot sleep "
        "at night. It truly can only be called chance, but I knew that face. For years I had served him in the "
        "Emperor's palace. But Lord Kiyomori's strength was plain as day. I went over to Lord Kiyomori's side and "
        "tried to strike down the rebels. In the end they escaped, but Lord Kiyomori declared publicly, \"The "
        "rebels have been put to death.\" Well, after being shown such a difference in strength, they would never "
        "again think of defying him. But perhaps I had not yet won Lord Kiyomori's trust, for to my regret I was "
        "demoted to this eastern land. Here there is only a place name, Motoki; no houses, no fields, only "
        "mountains stretching on and on. Here I can only live quietly, making no great moves. It was just then. He "
        "had come here to clear the wasteland, but no one would ever think he was the Emperor's son. Only I could "
        "have achieved this. Ten years have passed since I left the capital, and I do not know how things stand "
        "in politics. But Lord Kiyomori must still remain at the top of Japan. Now, how great a reward will his "
        "head bring me? It seems I will lose sleep again tonight.")
L286 = ("How foolish. They say they will give up the medicine that Lord Ginosuke, hero of us people of Arata, "
        "bestowed on us. Of course we objected. But they say that disaster happened because the medicine was used "
        "wrongly. Where is the proof of that? Without that sacred implement we cannot live in this land. How are "
        "we to hunt beasts? How are we to defend ourselves against invaders? To show our resolve, we have decided "
        "to leave the land of Arata with those who side with us, taking all the medicine we have. For those who "
        "stay, it will be convenient, since they can be rid of the medicine they no longer need. About half of us, "
        "perhaps, will leave Arata together. But with that many comrades it is enough. We will surely prosper in "
        "another land too. With this medicine, surely anywhere.")
L313 = ("Damn it, what a blunder. At this rate even my head will be cut off. I was supposed to get a reward from "
        "Lord Kiyomori, and just because I let one girl get away, look at me now. They say she served the "
        "Emperor's son, but in that upheaval she won't be found so easily. Or so I thought until a moment ago. "
        "Hiding here as night falls, my head does cool down. That's right, it's only a rumor to begin with. She's "
        "only the daughter of a ruined family, kept at the Emperor's palace as a maid out of pity. What on earth "
        "is there to gain by catching a girl like that? Lord Kiyomori is old now too. Maybe he just wanted to see "
        "something rare before he dies. Or so I thought until a moment ago. Hiding here as the sun comes up, my "
        "head grows clearer still. That is exactly why Lord Kiyomori must want to see her. Even if it's only a "
        "rumor, I just need to bring the girl. If her eye is a jade eye he'll be satisfied, and if not, he'll "
        "accept that. Well, I'd better go look. A girl born with one green eye, about ten years old.")
L314 = ("I have no ability. My father respected my wishes and allowed me to go on to the University of Physical "
        "and Chemical Sciences. But once I graduate, it is my fate to be drawn into the path of politics my family "
        "has followed for generations. That time is near. I do not believe I could ever manage the path of "
        "politics. It was at such a time. Among my great-great-grandfather's belongings I found a journal. It said "
        "that villagers of a remote land had told him of a medicine that lets one bring out tremendous strength, "
        "or something of the kind. Apparently, in the age of wars, one man even mowed down dozens of soldiers. My "
        "great-great-grandfather, it seems, could not accept so dubious a thing, but what if it were real? If I "
        "could obtain it and uncover its secret, could I not serve this country, and would not my own path into "
        "politics be shown? I know it is a facile idea, but I need confidence. And so I go to the Arata "
        "settlement. I will uncover the secret of the medicine. Only by doing this can I avoid becoming a disgrace "
        "to my family. No, by nature I love stories of this sort. I have a strong interest in the secret of this "
        "medicine itself.")
L68 = ("How have you been since? Are you devising a plan to stand against the Ouda house? My instinct tells me you "
       "probably think my ramblings not worth bothering with. I take up my brush again, prepared to be thought of "
       "so. I once sent you a letter about the horde of demon warriors; let me add that even the demon warriors "
       "are not all-powerful. Every one of them moved in an inhuman way, but we did manage to kill at least a few "
       "of the Ouda army's soldiers. Lately, however, something strange has happened. Among those who killed Ouda "
       "soldiers, some have begun to claim that they hear the voices of demons. Not just one or two. Some say a "
       "demon warned them of danger and they escaped death; others say they foresaw the danger to someone they "
       "spoke with and saved that person's life; there are all sorts. What they share is that they hear the "
       "voices of demons telling them of danger. Does killing a demon warrior leave one possessed by such a "
       "demon? Or does one gain a demon's power and become able to avoid danger? I cannot imagine at all what "
       "happened in that battle. I too fought in that battle, but I do not hear the voices of demons. What "
       "happened at Taruhazama? The mystery only deepens. This time I have nothing in particular to advise, but "
       "together with the earlier matter, I would ask you to keep it in a corner of your mind, for reference.")
L209 = ("Conflict, the jade-eye curse-killings, disappearances, the fierce horn, the goddess. Why did these "
        "inexplicable phenomena occur? Several causes can be considered, but it is hard to say for certain. "
        "Therefore, the customs peculiar to this Arata settlement will be restricted to some degree. As a first "
        "step, the use of Droga is banned for the time being. By what logic Droga is tied to these phenomena is "
        "entirely unknown; we cannot even guess whether there is any connection at all. But if there is a logic "
        "beyond our imagining, we have no choice but to forbid what may be suspected before the cause is "
        "identified. Women, too, have now become a powerful fighting force. For hunting and self-defense as well, "
        "we will wait and see without using Droga. But there will surely be those who oppose such a proposal. I "
        "only hope it does not come to Arata splitting apart.")
_LET = [  # (id, text, body x0, x1, blocks, signature, signature box)
    (10, L10, 92, 2012, 4, "Nagamoto Asahi", [22, 250, 66, 448]),
    (16, L16, 76, 1168, 2, "Ginosuke Niimura", [16, 230, 60, 448]),
    (182, L182, 16, 1106, 2, None, None),
    (286, L286, 20, 786, 2, None, None),
    (313, L313, 20, 1072, 2, None, None),
    (314, L314, 26, 1036, 2, None, None),
    (68, L68, 92, 1437, 3, "Nagamoto Asahi", [22, 250, 66, 448]),
    (209, L209, 16, 716, 2, None, None),
]
for _i, _t, _x0, _x1, _n, _s, _sb in _LET:
    _L = letter(_t, _x0, _x1, _n, _s, _sb)
    if _s:
        _L[-1][2]["erase"] = [[_sb[0], 300, _sb[2], 450]]
    JOBS.append({"id": "ref%d-letter" % _i, "screen": "reference %d detail" % _i, "style": "serif", "mode": "lines",
                 "erase": "inpaint", "erase_first": True, "color": "#1a1208", "mask_grow": 3,
                 "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
                 "note": "calligraphy letter, both paper faces (English blocks right to left, as the JP columns)",
                 # IMAGES3C: the dark mottled back face (1.png) is erased with texfill (inpaint left lighter patches)
                 "items": [(D + "rrr%d/0.gal" % _i, ""), (D + "rrr%d/1.gal" % _i, "", {"erase": "texfill"})],
                 "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L]})
JOBS += [
    {"id": "ov-letters", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (10, 16, 182, 286, 313, 314, 68, 209)]},
]


# ---- IMAGES4 2026-10-01: refs 50 / 54 (unlocked by navigator card 87), 300x170 概要 previews.
# Full details exist and are translated below. White paper: flat fill per box, keeping the frame rules.
# max_size = the JP glyph height measured on the source. The 60x30 thumbnails are below legibility: skipped.
JOBS += [
    {"id": "ov-50", "screen": "reference screen preview", "style": "serif", "mode": "lines", "erase": "flat",
     "color": INK, "max_size": 7, "new": True, "note": "medical certificate overview crop",
     "items": [(O + "rr50.gal", "")],
     "lines": [("MEDICAL CERTIFICATE", [70, 50, 230, 67], {"align": "center", "max_size": 11}),
               ("Name:", [40, 80, 84, 92]),
               ("Mifuyu Niimura", [85, 80, 262, 92]),
               ("Address:", [40, 98, 84, 110]),
               ("2-1-5 Jogasaki, Motoki-cho, Motoki District, Sawa Prefecture", [85, 98, 296, 110]),
               ("Central Chateau 405", [85, 117, 262, 128]),
               ("Date of birth:", [34, 134, 84, 146]),
               ("Shiyo 757, December 3", [85, 134, 262, 146])]},
    {"id": "ov-54", "screen": "reference screen preview", "style": "serif", "mode": "lines", "erase": "flat",
     "color": INK, "max_size": 6, "new": True, "note": "class report overview crop",
     "items": [(O + "rr54.gal", "")],
     "lines": [("Iizawa Prefectural Megasawa Second Elementary School", [100, 30, 270, 40], {"align": "right"}),
               ("Document Ho-115", [180, 40, 270, 50], {"align": "right"}),
               ("CLASS REPORT", [90, 51, 210, 64], {"align": "center", "max_size": 10}),
               ("Report date", [26, 71, 61, 83], {"erase": [[26, 73, 61, 81]]}),
               ("Shiyo 789, November 10", [61, 71, 124, 83], {"max_size": 7, "erase": [[61, 73, 124, 81]]}),
               ("Class", [26, 82, 61, 94], {"erase": [[26, 84, 61, 92]]}),
               ("Year 1, Class 1", [61, 82, 124, 94], {"max_size": 7, "erase": [[61, 84, 124, 92]]}),
               ("Teacher", [26, 93, 61, 105], {"erase": [[26, 95, 61, 103]]}),
               ("Midori Sasaki", [61, 93, 124, 105], {"max_size": 7, "erase": [[61, 95, 124, 103]]}),
               ("(1) Details of the problem", [26, 111, 160, 123], {"erase": [[26, 113, 160, 121]]}),
               ("It appears that Haruka Niimura, in my class, is being bullied. It seems to stem from her having "
                "shielded a classmate from bullying. From what I have observed, Haruka Niimura herself shows no "
                "serious fault. As homeroom teacher I cannot overlook the situation any further, and I would like "
                "it to be addressed.", [28, 122, 268, 158]),
               ("(2) Course of action", [26, 160, 160, 170], {"erase": [[26, 162, 160, 170]]})]},
]


# ---- 2026-10-25: full object details omitted by the earlier overview-only scope (display 72/73/76).
MEDICAL50 = [
    ("MEDICAL CERTIFICATE", [160, 139, 640, 180], {"align": "center", "max_size": 30}),
    ("Name:  Mifuyu Niimura", [112, 218, 690, 249], {"max_size": 21}),
    ("Address:  2-1-5 Jogasaki, Motoki-cho,", [112, 267, 692, 298], {"max_size": 21}),
    ("Motoki District, Sawa Prefecture", [226, 301, 692, 332], {"max_size": 21,
                                                                 "erase": [[225, 315, 690, 343]]}),
    ("Central Chateau 405", [226, 335, 692, 366], {"max_size": 21, "erase": []}),
    ("Date of birth:  Shiyo 757, December 3", [112, 370, 692, 403], {"max_size": 21,
                                                               "erase": [[112, 363, 692, 403]]}),
    ("Diagnosis:  Acute stress disorder", [112, 459, 692, 492], {"max_size": 21}),
    ("I certify that, owing to the above illness, a month of recuperation at home is necessary "
     "from Shiyo 788, May 2.", [112, 552, 692, 638], {"max_size": 21, "line_spacing": 1.12}),
    ("Remainder blank", [477, 680, 692, 710], {"align": "right", "max_size": 19}),
    ("Shiyo 788, May 1", [468, 895, 692, 926], {"align": "right", "max_size": 21}),
    ("Tajima Neuropsychiatric Clinic", [351, 942, 692, 975], {"align": "right", "max_size": 21}),
    ("Director", [498, 990, 565, 1021], {"max_size": 20}),
]
CLASS54 = [
    ("Iizawa Prefectural Megasawa Second Elementary School", [383, 86, 719, 105],
     {"align": "right", "max_size": 13}),
    ("Document Ho-115", [506, 106, 719, 125], {"align": "right", "max_size": 14}),
    ("CLASS REPORT", [220, 139, 580, 174], {"align": "center", "max_size": 29}),
    ("Report date", [71, 196, 146, 218], {"max_size": 14}),
    ("Shiyo 789, November 10", [147, 194, 330, 218], {"style": "handwriting", "max_size": 17,
                                                  "erase": [[138, 194, 330, 218]]}),
    ("Class", [71, 224, 145, 246], {"max_size": 15}),
    ("Year 1, Class 1", [147, 222, 330, 246], {"style": "handwriting", "max_size": 18,
                                           "erase": [[138, 222, 330, 246]]}),
    ("Teacher", [71, 251, 145, 274], {"max_size": 15}),
    ("Midori Sasaki", [147, 249, 330, 274], {"style": "handwriting", "max_size": 18,
                                         "erase": [[138, 249, 330, 274]]}),
    ("(1) Details of the problem", [71, 304, 420, 324], {"max_size": 15}),
    ("It appears that Haruka Niimura-san, in my class, is being bullied. It seems to stem from her having "
     "shielded a classmate from bullying. From what I have observed, Haruka Niimura-san herself shows no "
     "serious fault. As homeroom teacher I cannot overlook the situation any further, and I would like "
     "to address it.", [75, 326, 712, 446], {"style": "handwriting", "max_size": 18}),
    ("(2) Course of action", [71, 458, 420, 478], {"max_size": 15,
                                                "erase": [[71, 436, 420, 456]]}),
    ("I would like to visit the homes of Koji Kuji-kun and Kokona Hatanaka-san, who in particular have "
     "been seen bullying, and report the situation.", [75, 480, 712, 551],
     {"style": "handwriting", "max_size": 18}),
    ("(3) From the grade head", [71, 567, 420, 587], {"max_size": 15}),
    ("I investigated following Sasaki-sensei's report, but no particular bullying was observed. "
     "There is no need to visit the homes of the 2 pupils mentioned above.", [75, 590, 712, 684],
     {"style": "handwriting", "max_size": 18}),
    ("(4) From the vice-principal", [71, 699, 420, 718], {"max_size": 15}),
    ("In accordance with the grade head's wishes, action on this matter will be held off.",
     [76, 723, 711, 811], {"style": "gothic", "max_size": 19}),
    ("(5) Remarks", [71, 831, 420, 850], {"max_size": 15}),
    ("There is no need to inform Hatanaka-san, the PTA chair, of this matter.",
     [76, 855, 711, 943], {"style": "gothic", "max_size": 19}),
    ("Principal", [493, 967, 542, 982], {"align": "center", "max_size": 11}),
    ("Vice-principal", [545, 967, 594, 982], {"align": "center", "max_size": 8}),
    ("Grade head", [598, 967, 647, 982], {"align": "center", "max_size": 9}),
    ("Teacher", [652, 967, 700, 982], {"align": "center", "max_size": 11}),
]
GOTO59 = [
    ("Hmm, something really is strange. Going out of her way to invite me where Kogori-senpai is...... "
     "Because she invited me knowing that I'm investigating the case.", [10, 5, 790, 83]),
    ("In other words, Niimura-senpai is trying to get information about the case out of me. "
     "I need to be cautious before going to Senpai's house.", [10, 106, 790, 166]),
    ("Kogori-senpai really hates these disturbing subjects. Both Niimura-senpai and I try to avoid "
     "talking about them in front of Kogori-senpai. And yet she invited me, which means it's something "
     "quite urgent.", [10, 171, 790, 256], {"erase": [[7, 181, 793, 256]]}),
    ("I can't rule out the possibility that Niimura-senpai is involved in the case. "
     "Let's examine that possibility!", [10, 280, 790, 343]),
    ("☆ Could Niimura-senpai be the culprit?", [10, 352, 790, 381]),
    ("The culprit's profile", [10, 381, 790, 406]),
    ("・Can drive a car", [10, 406, 790, 431]),
    ("・Knows human anatomy", [10, 431, 790, 456]),
    ("・Is acquainted with the victim", [10, 456, 790, 481]),
    ("・Lives in Motoki-cho", [10, 481, 790, 506]),
    ("All these conditions have to be met. In other words, Niimura-senpai, who can't drive, "
     "is unlikely to be the culprit.", [10, 506, 790, 554]),
    ("Could there be an accomplice?", [10, 577, 790, 604]),
    ("・Left the body there alive", [10, 604, 790, 629]),
    ("・A gruesome state", [10, 629, 790, 654]),
    ("・Possibly colored the body red", [10, 654, 790, 679]),
    ("The method shows a very strong fixation, so the tendency points to a psychopath or a copycat "
     "of the Megasawa City case. A psychopath is highly likely to act alone. With multiple copycats, "
     "it would mean Niimura-senpai and someone else imitated the Megasawa City case. If Niimura-senpai "
     "has an accomplice, the possibility of her being the culprit isn't entirely out of the question.",
     [10, 679, 790, 816], {"erase": [[7, 678, 793, 804]]}),
    ("Assuming she's the culprit, why invite me? To investigate the current situation, it would be "
     "quicker to go to the park herself. Besides, Senpai must know the risk of hearing what I have "
     "to say (I'll see through the culprit right away ☆).", [10, 823, 790, 903]),
    ("There are 3 reasons she wouldn't go herself.", [10, 927, 790, 951]),
    ("1. She's worried about Kogori-senpai's health", [10, 952, 790, 977]),
    ("2. She's not the culprit, but she's involved", [10, 977, 790, 1002]),
    ("3. She doesn't just want to hear from me; she has something to consult me about",
     [10, 1002, 790, 1049], {"erase": [[7, 1002, 793, 1027]]}),
    ("I see, I see. It's gradually coming into focus. There's a possibility that Niimura-senpai "
     "is involved in the case to some extent. But she's worried about something to do with it. "
     "Now, if I bring the Megasawa City case into this,", [10, 1051, 790, 1147]),
    ("・First Megasawa City case: the victim was in elementary school, Year 2", [10, 1148, 790, 1173]),
    ("・Second Megasawa City case: victims include an elementary school, Year 6 homeroom teacher",
     [10, 1173, 790, 1198]),
    ("・Third Megasawa City case: the victim was in junior high school, Year 3", [10, 1198, 790, 1223]),
    ("→ The targets get older as the years go by. If a case happens this year, Shiyo 800, "
     "it should happen around someone in high school, Year 3.", [10, 1223, 790, 1273]),
    ("Yes, almost certain. Niimura-senpai has some connection with the Megasawa City case too. "
     "Could Niimura-senpai have lived in Megasawa City before? I'll ask her about that as well. "
     "It's all right! Leave it to the genius girl, Erina Goto!", [10, 1300, 790, 1448]),
]
JOBS += [
    {"id": "ref50", "screen": "reference 50 detail (display 72)", "style": "serif", "mode": "lines",
     "erase": "flat", "erase_first": True, "color": INK, "max_size": 21,
     "note": "full medical certificate; original doctor signature and red seal preserved by owner ruling",
     "items": [(D + "rrr50/0.gal", "")], "lines": MEDICAL50},
    {"id": "ref54", "screen": "reference 54 detail (display 73)", "style": "serif", "mode": "lines", "chain": True,
     "erase": "flat", "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60,
     "color": INK, "max_size": 18, "note": "full class report; run refdoc54.py first; first cell expanded, seals kept",
     "items": [(D + "rrr54/0.gal", "")], "lines": CLASS54},
    dict(_MEMO, id="ref59", screen="reference 59 detail (display 76)", new=False, erase="flat",
         note="full Goto memo; reasoning, arrows and source contradiction retained",
         protect=[[10, 801, 30, 824]],
         items=[(D + "rrr59/0.gal", "")], lines=[
             (entry[0], entry[1], {"max_size": 18, **(entry[2] if len(entry) > 2 else {}),
                                      "erase": [[7, 0, 793, 84], [7, 105, 793, 257], [7, 279, 793, 555],
                                             [7, 576, 793, 904], [7, 925, 793, 1275], [7, 1295, 793, 1455]]
                                      if index == 0 else []})
             for index, entry in enumerate(GOTO59)]),
]


GOTO61 = [
    "Information currently known.",
    "・A bug is planted only in Niimura-senpai's phone. (I can't be certain it's a bug, but at least something is inside it.)",
    "・Our phones have a Friend GPS function.",
    "・Using these 2 functions, it's possible to know the other person's information and location with considerable accuracy.",
    "↓",
    "But if what the culprit can learn isn't just sound and location, I can trap them. "
    "For example, stage a false incident in front of the phone.",
    "Putting that aside for now, first I should think about who planted this bug. "
    "Kogori-senpai's father gave her this phone 5 days ago as a gift for moving up a year and advancing to a new school. "
    "And apparently Kogori-senpai's father designed the phone.",
    "↓",
    "Kogori-senpai's father planted the bug!!",
    "But it was Kogori-senpai's father who was killed. The Megasawa City case comes up as the link. "
    "Niimura-senpai seems to be involved in the Megasawa City case.",
    "↓",
    "If this case is connected too, was Kogori-senpai's father also involved in the Megasawa City case? "
    "Then was her mother involved too? Niimura-senpai's mother may also be involved.",
    "↓",
    "However, Niimura-senpai and her mother have alibis...... "
    "I see, I see: Kogori-senpai's parents were used to fabricate alibis. "
    "These 2 may have carried out the crimes. That also explains why there are 2 victims every time.",
    "In other words, here's the truth of the Megasawa City case.",
    "・Niimura-senpai's father died in an accident, and her mother, who became mentally ill, moved to "
    "Megasawa City with Senpai to recuperate.",
    "↓",
    "・Niimura-senpai came to be bullied over her family circumstances, and tried to kill her bullies by making paper dolls.",
    "↓",
    "・Her mother noticed this and asked the Kogori couple to kill them for her. "
    "They chose April 8 as the day of the crimes, when they would have perfect alibis.",
    "↓",
    "・Niimura-senpai came to believe in the curse's fulfillment, and tried to eliminate the troubles "
    "that befell her from then on with paper-doll curses.",
    "↓",
    "・The Kogori couple carried out the crimes on the same date, April 8. "
    "The Kogori couple probably felt responsible for Niimura-senpai's father's death. "
    "So they were helping the Niimura family to atone for it. "
    "That's about how it goes, but there are still things I don't understand.",
    "1. How were the crimes as if people were spirited away carried out? "
    "Even if I can break the alibis, the killing method is unknown. I'll leave this as some kind of trick.",
    "2. Is it really only a matter of the Niimura and Kogori families? "
    "Could those 3 alone really have carried out such large-scale crimes? "
    "I can't help thinking there's something wrong with those 3 alone carrying out the bizarre murders "
    "that shook all of Japan 3 times.",
    "↓",
    "Niimura-senpai's mother may have an accomplice (probably a man). "
    "But Senpai's mother's parents have already passed away, and she has no siblings. "
    "Then perhaps someone on Senpai's father's side of the family is helping......?",
]
GOTO62 = [
    "Shinigami in the Megasawa City case = the Kogori couple",
    "Shinigami in the Motoki-cho case = Niimura-senpai's mother (Mifuyu Niimura)",
    "That's the premise I'll think from. The method of making people seem spirited away can wait "
    "(I'll know once I catch the culprit).",
    "↓",
    "What's puzzling about this case",
    "・The paper doll appeared late",
    "In the Megasawa City case it appeared before Niimura-senpai 1 week to 10 days in advance, "
    "but today the paper doll appeared on the very morning the case happened. → Was this a spur-of-the-moment crime?",
    "↓",
    "But the bug had been planted. It's difficult to steal the phone from Niimura-senpai and plant a bug. "
    "So the case may have been planned before April 3, when the phone was given to her as a present.",
    "↓",
    "They had planned the case, but something unexpected happened. "
    "I wonder what...... I'll ask Niimura-senpai's opinion too.",
    "Niimura-senpai's opinion",
    "・Why kill only Ryoji Kogori-san? If Akane-san were left alive, she might tell the police the truth "
    "about the Megasawa City case. So killing both at the same time would be the usual course.",
    "I wonder if that's really so......",
    "↓",
    "If that were so, it would be either kill both at the same time or leave them alone. "
    "Killing just one is far too risky.",
    "Niimura-senpai's important opinion!",
    "Killing only one makes sense too. Thinking of Kogori-senpai, even if the other survived alone, "
    "she wouldn't confess to the police. Because that would brand Kogori-senpai 'the daughter "
    "of a sick killer' and 'the daughter of a culprit in the Megasawa City case'. "
    "I see. She even keeps quiet about Eiichiro Niimura-san, so she would keep quiet about the Megasawa City case......",
    "↓",
    "I see, the target was someone else. If Kogori isn't the culprit, the people who could be the remaining targets are",
]
from refdoc_memo import flow as _memo_flow

POSTS47 = [
    "Here it comes, here it comes............",
    "Now, it's finally time",
    "Yukipin's heeeere!!!!",
    "Yukipin really is a goddess",
    "Huge lol",
    "Amazing lol",
    "I wanna lick Yukipin's cheeks",
    "That's way too careless lol",
    "So jealous of cherry-blossom-viewing leave",
    "The main event's competitive eating lol",
    "I'd rather eat Yukipin than yakisoba",
    "I'll buy Yukipin's half-eaten yakisoba\nfor 100,000 yen",
    "Monster lol",
    "Yukipin's segment is over......\nGuess I'll go to work",
]


def _sha47(text):
    result = _sha(text)
    result[0][2].update(method="flat", bg="#c7d9f1", erase=[[47, 8, 137, 35]])
    result[1][2]["erase"] = [[11, 43, 304, 75]]
    if "\n" in text or len(text) > 34:
        result[1] = (text, [12, 34, 304, 77], result[1][2])
    return result


POLICE35 = [
    ("Assistant Inspector", [79, 235, 232, 258], {"max_size": 16,
                                                 "erase": [[79, 234, 232, 259]], "method": "flat", "bg": "#c7dbf4",
                                                 "mask_color": [0, 120, 0, 120, 0, 120]}),
    ("Daijiro Ise", [91, 277, 225, 300], {"max_size": 16, "method": "flat", "bg": "#c7dbf4",
                                        "mask_color": [0, 120, 0, 120, 0, 120]}),
    ("No.", [123, 338, 145, 364], {"max_size": 14, "method": "flat", "bg": "#c7dbf4",
                                   "mask_color": [0, 120, 0, 120, 0, 120]}),
    ("Sawa Prefectural\nPolice", [77, 644, 220, 677], {"max_size": 11, "align": "center",
                                                    "color": "#3a381b", "erase": [[74, 644, 222, 677]],
                                                    "mask_color": [0, 200, 0, 180, 0, 160], "mask_grow": 3}),
]

JOBS += [
    dict(_MEMO, id="ref61", screen="reference 61 detail (display 80)", new=False, erase="flat",
         note="full Goto memo; complete reasoning reflowed at 18px, no shortening",
         items=[(D + "rrr61/0.gal", "")], lines=_memo_flow(GOTO61, 1418)),
    dict(_MEMO, id="ref62", screen="reference 62 detail (display 81)", new=False, erase="flat",
         note="full Goto memo; incomplete final sentence remains incomplete",
         items=[(D + "rrr62/0.gal", "")], lines=_memo_flow(GOTO62, 882)),
    {"id": "ref47-posts", "screen": "reference 47 posts (display 70)", "style": "serif", "mode": "lines",
     "erase": "inpaint", "erase_first": True, "mask_color": [0, 120, 0, 120, 0, 120], "mask_grow": 2, "keep_alpha": True,
     "color": "#222222", "note": "complete viewer posts; existing Oha-Oha! / Sha-better layout reused",
     "items": [(D + "rrr47/%d.gal" % number, "", {"lines": _sha47(text),
               "protect": [[296, 68, 310, 77]] if number in (11, 13) else []})
               for number, text in enumerate(POSTS47)], "lines": []},
    {"id": "ref35", "screen": "reference 35 police badge (display 38)", "style": "serif", "mode": "lines",
     "erase": "inpaint", "erase_first": True, "mask_grow": 2, "color": "#172a31",
     "note": "full police badge; original English, number, photo and gold emblem retained",
     "items": [(D + "rrr35/0.gal", ""), (D + "rrr35/1.gal", "")], "lines": POLICE35},
    {"id": "ov-47", "screen": "reference 47 overview", "style": "gothic", "mode": "lines",
     "erase": "inpaint", "erase_first": True, "stroke": 1, "stroke_color": "#ffffff", "color": "#153f80",
     "note": "O69 logo-art exception; full English reading above untouched source logo, root-approved geometry",
     "items": [(O + "rr47.gal", "")],
     "lines": [("Lightning Thunder Visit♪ Yukipin", [4, 0, 296, 24], {"max_size": 18, "erase": []})]},
    {"id": "ov-47-chat", "screen": "reference 47 overview viewer card", "style": "serif", "mode": "lines",
     "erase": "flat", "erase_first": True, "chain": True, "keep_alpha": True,
     "note": "tiny viewer card translated separately; logo-art exception does not waive its text",
     "items": [(O + "rr47.gal", "")],
     "lines": [("Oha-Oha!", [219, 146, 245, 158], {"style": "serif", "color": "#1c2e46", "max_size": 6,
                 "method": "flat", "bg": "#c7d9f1", "erase": [[219, 146, 244, 158]]}),
               ("Now, it's finally time", [205, 158, 299, 170], {"style": "serif", "color": "#222222", "max_size": 6,
                 "method": "flat", "bg": "#c7d9f1", "erase": [[205, 158, 299, 170]]})]},
    {"id": "ov-repair-memos", "screen": "reference memo overviews", "style": "serif", "mode": "asis", "chain": True,
     "note": "top crops rebuilt from complete English details with refdoc_overview.py",
     "items": [(O + "rr%d.gal" % number, "") for number in (59, 61, 62)], "lines": []},
    {"id": "ov-22-label", "screen": "reference 22 overview", "style": "gothic", "mode": "lines",
     "erase": "inpaint", "erase_first": True, "color": "#b82525", "mask_grow": 2,
     "note": "readable produce-box label; tomato illustration and all numbers retained",
     "items": [(O + "rr22.gal", "")],
     "lines": [("Tomato", [162, 39, 218, 65], {"max_size": 13, "align": "center",
                "mask_color": [120, 255, 0, 130, 0, 130], "erase": [[162, 39, 218, 65]]})]},
    {"id": "ref152-repair", "screen": "reference 152 turn states", "style": "serif", "mode": "asis", "chain": True,
     "note": "refdoc152.py piecewise shaded carry from accepted faces; original alpha and unrelated artwork retained",
     "items": [(D + "rrr152/%02d.gal" % number, "") for number in range(1, 19) if number != 13]},
]


# ---- IMAGES6 2026-10-01 (notes/IMAGES6-BRIEF.md): object references unlocked in part 6 (77 81 239 90 93 3 67) and
# scenario reference 222's 概要 sign. Boxes measured on the sources with work/images/_c/rows6.py. 92 (crayon drawing +
# coffin close-up) has no text: no job. The 概要 of 77..67 are top crops of the detail (refdoc_overview probe < 9):
# rebuilt with `refdoc_overview.py build` and shipped by ov-p6 (asis). The 60x30 thumbnails are below legibility.
_RED67 = [150, 255, 0, 110, 0, 110]
T77_1 = ("Today I took Akane to her month-and-a-half checkup. But the whole hospital was oddly hectic, and they just "
         "would not get around to her checkup. Since I had time to spare, I took Akane and looked through the glass "
         "into the newborn nursery. And there, a baby girl born just today was sleeping soundly with an adorable "
         "sleeping face. Her name is Mifuyu-chan. After I had watched her for a while, Akane woke up and started "
         "going \"Ah, ah.\" It was the first time Akane had made a sound other than crying. When I showed her, saying, "
         "\"Look, Akane, see? It's a little girl who was born just today,\" I felt as if Akane smiled. Akane isn't "
         "even old enough to smile yet, but when I showed her Mifuyu-chan, she seemed oddly happy.")
T77_2 = ("According to the nurse, Mifuyu-chan's mother died giving birth. Mifuyu-chan, sleeping so soundly, will never "
         "be able to meet her mother. So, if I can, I want to have Akane become her friend, so that Mifuyu-chan won't "
         "feel lonely, even a little. Maybe I'm sticking my nose in, though. I'll try going to see her again later.")
_R81 = [(94, 115, "Name", "Mifuyu Kanai", 20), (138, 159, "Date of birth", "Shiyo 757, December 3", 20),
        (182, 203, "Hometown", "Motoki-cho, Sawa Prefecture", 20), (225, 247, "High school", "Motoki High School", 20),
        (269, 291, "Occupation", "Office clerk", 20), (316, 334, "Likes", "Freshly cooked rice", 17),
        (359, 378, "Dislikes", "Coffee, spicy food", 17), (404, 422, "Hobby", "Cooking", 17),
        (447, 466, "Special skill", "Can tackle anything earnestly", 17),
        (491, 510, "Wanted in a partner", "Someone who sees what's inside (Family talk is off-limits!)", 17),
        (535, 554, "Family", "Both parents deceased. No siblings.", 17),
        (579, 598, "Days off", "Reading, watching movies", 17),
        (623, 642, "My personality", "Honesty is my only selling point (Modest AND a point men like!)", 17),
        (664, 685, "Past boyfriends", "None in particular (Pretend you don't really get it!)", 20),
        (708, 729, "Ideal date?", "Anywhere is OK as long as we're together (That's right, isn't it?)", 20),
        (752, 773, "Want to marry?", "If I meet someone good (Never look desperate!)", 20),
        (796, 817, "Favorite sport", "None in particular (Looks like Eiichiro-san doesn't have one either)", 20)]
L81 = [("", [25, 90, 790, 942], {"erase": [[25, 90, 790, 942]]})]
for _y0, _y1, _l, _v, _s in _R81:
    L81 += [(_l, [28, _y0 - 4, 208, _y1 + 4], {"max_size": _s, "erase": []}),
            (_v, [214, _y0 - 4, 790, _y1 + 4], {"max_size": 19, "erase": []})]
L81 += [("Other", [28, 836, 208, 866], {"max_size": 17, "erase": []}),
        ("Relax your shoulders first! If you get nervous, you'll make him feel he has to be considerate!",
         [214, 836, 790, 889], {"max_size": 19, "erase": []}),
        ("Okay, okay, stop looking at this memo all the time and look properly at Eiichiro-san!",
         [214, 889, 790, 941], {"max_size": 19, "erase": []})]
_I239 = [(369, 402, "What you see in the seclusion, you shall not tell to others"), (437, 470, "Survive alone"),
         (503, 537, "The use of firearms and machines is forbidden"),
         (570, 604, "You shall not flee from Mount Itohime"),
         (638, 671, "Receive sufficient training before the seclusion"), (705, 738, "You shall not lose your life"),
         (774, 806, "Make use of the sulfur springs"), (842, 869, "You shall not meet people"),
         (909, 940, "You shall not hunt beasts needlessly")]
L239 = ([("Mountain Seclusion Catalog", [52, 60, 740, 134], {"max_size": 46, "erase": [[50, 60, 770, 1015]]}),
         ("In undertaking the mountain seclusion, observe the following", [50, 218, 760, 277],
          {"max_size": 30, "erase": []})]
        + [("One: " + t, [50, a - 4, 770, b + 4], {"max_size": 28, "erase": []}) for a, b, t in _I239]
        + [("One: If you sense anything amiss on Mount Itohime, come down the mountain at once and inform everyone",
            [50, 966, 770, 1066], {"max_size": 28, "line_spacing": 1.05, "erase": []})])
_P90 = {"max_size": 15, "line_spacing": 1.05}
L90 = [("Shiyo 790, April 6", [500, 98, 728, 121], {"align": "right", "max_size": 15, "erase": [[580, 100, 727, 119]]}),
       ("Sales Section, Sales Department    Mamoru Mitsuda", [380, 122, 730, 145],
        {"align": "right", "max_size": 15, "erase": [[564, 124, 728, 143]]}),
       ("ACCOUNT", [280, 152, 520, 188], {"align": "center", "max_size": 26, "erase": [[330, 155, 470, 185]]}),
       ("I report as follows on the traffic accident that occurred in Motoki-cho on Shiyo 790, April 6.",
        [60, 218, 745, 242], {"max_size": 15, "erase": [[88, 221, 725, 240]]}),
       ("Details", [330, 276, 470, 306], {"align": "center", "max_size": 18, "erase": [[388, 280, 413, 302]]}),
       ("1. Summary of the accident", [74, 340, 500, 362], {"max_size": 15, "erase": [[76, 342, 186, 360]]}),
       ("(1) Date and time", [78, 365, 240, 385], {"max_size": 15, "erase": [[82, 366, 445, 384]]}),
       ("Shiyo 790, April 6 (Tue.), around noon", [244, 365, 700, 385], {"max_size": 15, "erase": []}),
       ("(2) Place", [78, 389, 240, 409], {"max_size": 15, "erase": [[82, 390, 365, 408]]}),
       ("Nishinaka 1-chome Intersection, Motoki-cho", [244, 389, 700, 409], {"max_size": 15, "erase": []}),
       ("(3) Situation", [78, 413, 240, 434], {"max_size": 15, "erase": [[82, 414, 333, 433]]}),
       ("Company car collided with a utility pole", [244, 413, 700, 434], {"max_size": 15, "erase": []}),
       ("2. State of the damage", [74, 461, 500, 483], {"max_size": 15, "erase": [[75, 463, 186, 481]]}),
       ("At the intersection in question I came up to a red light and stepped on the brake, but it did not work. "
        "Today there was an entrance ceremony at a nearby elementary school, and many parents and children were "
        "crossing at the crosswalk, so to avoid hitting anyone I turned the wheel and collided with a utility pole.",
        [74, 486, 728, 581], dict(_P90, erase=[[72, 487, 728, 554]])),
       ("3. Cause of the accident", [74, 583, 500, 604], {"max_size": 15, "erase": [[75, 584, 186, 602]]}),
       ("The police investigation found that the brake had been poorly maintained. However, it was possible to slow "
        "down with the hand brake and the gears, so I too bear responsibility.",
        [74, 607, 728, 677], dict(_P90, erase=[[72, 608, 728, 650]])),
       ("4. Measures taken this time", [74, 679, 500, 700], {"max_size": 15, "erase": [[79, 680, 186, 698]]}),
       ("The passenger side was almost completely crushed, so the car has been scrapped. Also, since the utility pole "
        "and guardrail it hit were damaged, claims for compensation are expected. Detailed costs and matters "
        "concerning car insurance will be reported at a later date.",
        [74, 703, 728, 798], dict(_P90, erase=[[72, 704, 728, 771]])),
       ("5. Future countermeasures", [74, 800, 500, 822], {"max_size": 15, "erase": [[75, 801, 186, 820]]}),
       ("Maintenance checks beforehand go without saying, but when a problem like this one occurs, one should also "
        "use the hand brake and the gears to take a lower-risk emergency evasive action. I would ask that this be "
        "made known throughout the company, and I believe that preparing a manual for when a similar problem "
        "suddenly occurs will further reduce accidents. I am deeply sorry for causing this accident.",
        [74, 825, 728, 966], dict(_P90, erase=[[72, 826, 728, 941]])),
       ("End", [620, 968, 730, 991], {"align": "right", "max_size": 15, "erase": [[678, 971, 712, 988]]})]
_W93 = [(749, 772), (773, 797), (798, 822), (823, 847), (848, 872), (873, 897)]
_C93 = [(46, 298, "Western", ["Spring vegetable peperoncino", "Motoki-cho mountain harvest paella", "Fisherman's pasta",
                               "5-cheese pizza", "Hamburg steak plate", "Beef, chicken & pork steak set"]),
        (300, 550, "Japanese", ["Wild vegetable & mushroom pasta", "Tender wagyu beef bowl", "Ultimate egg on rice",
                                "Retro omurice", "Seared fragrant ochazuke", "Select sushi, 10 pieces"]),
        (552, 792, "A la carte", ["Rich tomato fresh cake", "Drunken shrimp salad", "Rich milk tiramisu",
                                  "Russian-roulette takoyaki", "Original rose wine", "Drinks, salad bar"])]
L93M = [("", [40, 712, 792, 900], {"erase": [[44, 714, 296, 898], [298, 714, 548, 898], [550, 714, 790, 898]]})]
for _x0, _x1, _h, _its in _C93:
    L93M.append((_h, [_x0, 712, _x1, 749], {"max_size": 26, "erase": []}))
    L93M += [("・" + t, [_x0, a, _x1, b], {"max_size": 19, "erase": []}) for (a, b), t in zip(_W93, _its)]
_TK93 = {"mask_color": [0, 75, 0, 75, 0, 45], "color": "#1e1e04", "max_size": 22, "align": "center"}
_BR93 = {"mask_color": [0, 100, 0, 100, 0, 90], "color": "#2a1c00", "max_size": 22}
L93M += [("Campaign Ticket", [8, 943, 322, 972], dict(_TK93, erase=[[20, 944, 287, 971]])),
         ("Until Shiyo 790, March 31", [8, 974, 322, 1005], dict(_TK93, erase=[[14, 975, 295, 1004]])),
         ("30% OFF everything!!", [8, 1006, 322, 1037], dict(_TK93, erase=[[64, 1006, 243, 1036]])),
         ("Always at your dinner table", [428, 920, 792, 948], dict(_BR93, erase=[[429, 920, 710, 948]])),
         ("Family Restaurant Zahha", [428, 949, 792, 977], dict(_BR93, erase=[[429, 949, 716, 976]])),
         ("156-1 Nagaminedai, Motoki-cho, Sawa Prefecture", [428, 977, 792, 1006],
          dict(_BR93, erase=[[428, 977, 718, 1006]]))]
_S3 = {"max_size": 14, "color": "#222222"}
_OR3 = {"max_size": 26, "color": "#e46c0a", "mask_color": [170, 255, 50, 180, 0, 110], "mask_grow": 3}
L3 = [("Nanami-so", [108, 42, 292, 86], {"max_size": 34, "align": "center", "color": INK, "erase": [[139, 45, 245, 81]]}),
      ("Location", [107, 128, 170, 145], dict(_S3, erase=[[108, 129, 377, 145]])),
      ("4-1-5 Nanami-cho, Megasawa City, Iizawa Prefecture", [172, 128, 470, 145], dict(_S3, erase=[])),
      ("Structure", [107, 146, 170, 164], dict(_S3, erase=[[108, 147, 306, 163]])),
      ("Wooden, 2 stories   Built 80 years ago", [172, 146, 470, 164], dict(_S3, erase=[])),
      ("Facilities", [107, 164, 170, 182], dict(_S3, erase=[[108, 165, 436, 181], [109, 185, 177, 200]])),
      ("Tokyo Electric Power, public water, city gas, no bath, shared toilet", [172, 164, 470, 202],
       dict(_S3, erase=[], line_spacing=1.0)),
      ("Move in same day!", [468, 33, 792, 69], dict(_OR3, erase=[[478, 36, 690, 66]])),
      ("No deposit or key money!", [468, 73, 792, 107], dict(_OR3, erase=[[478, 76, 690, 104]])),
      ("No spices!", [468, 108, 792, 144], dict(_OR3, erase=[[478, 111, 645, 141]])),
      ("Plenty of facilities nearby!", [468, 145, 792, 181], dict(_OR3, erase=[[478, 148, 690, 178]])),
      ("Storage", [330, 262, 402, 306], {"max_size": 16, "align": "center", "color": INK, "bg": "#fdd4b4",
                                          "erase": [[340, 272, 384, 295]]})]
for (_a, _b), _n, _t in zip([(205, 219), (224, 238), (242, 256), (261, 275), (280, 294)],
                            ["Megasawa Second Elementary School", "Megamall", "Nanami-cho bus stop",
                             "Nanami-cho Hospital", "Meets Nanami-cho store"],
                            ["15 min walk", "15 min walk", "5 min walk", "3 min walk", "5 min walk"]):
    L3 += [(_n, [489, _a - 2, 680, _b + 2], dict(_S3, erase=[[489, _a - 1, 690, _b + 1]])),
           (_t, [682, _a - 2, 762, _b + 2], dict(_S3, erase=[]))]
for (_a, _b), _l, _v in zip([(341, 355), (360, 374), (378, 392), (397, 411)],
                            ["Rent", "Management fee", "Lease term", "Renewal fee"],
                            ["8,000 yen", "1,000 yen", "2 years", "None"]):
    L3 += [(_l, [489, _a - 2, 586, _b + 2], dict(_S3, erase=[[490, _a - 1, 612, _b + 1]])),
           (_v, [588, _a - 2, 700, _b + 2], dict(_S3, erase=[]))]
L3 += [("Comfort Rentals Co., Ltd.", [473, 437, 715, 461], {"max_size": 18, "color": INK, "erase": [[475, 439, 581, 460]]}),
       ("License No.: Iizawa Prefecture Governor (1) No. 10051", [472, 483, 715, 498],
        {"max_size": 11, "color": INK, "erase": [[473, 485, 635, 498]]}),
       ("Address: 1-1-5 Nokita-cho, Megasawa City, Iizawa Prefecture", [472, 498, 715, 511],
        {"max_size": 10, "color": INK, "erase": [[473, 499, 670, 511]]}),
       ("Transaction type: Exclusive agency", [472, 511, 715, 525],
        {"max_size": 10, "color": INK, "erase": [[473, 512, 561, 524]]})]
_P67 = {"max_size": 17, "line_spacing": 1.25}
L67 = [("Written Apology", [240, 40, 560, 77], {"align": "center", "max_size": 28, "erase": [[343, 44, 457, 77]]}),
       ("To the Chief of Sawa Police Headquarters", [48, 123, 480, 148], {"max_size": 17, "erase": [[48, 125, 220, 146]]}),
       ("Shiyo 800, April 9", [480, 157, 750, 182], {"align": "right", "max_size": 17, "erase": [[577, 159, 749, 180]]}),
       ("Motoki Police Station    Daijiro Ise", [400, 190, 752, 215],
        {"align": "right", "max_size": 17, "erase": [[547, 192, 752, 213]]}),
       ("On this occasion, I, Daijiro Ise, in arresting the culprit in the Megasawa City case and the Motoki-cho "
        "flaying murder case, procured expensive equipment without following the prescribed procedures, and moreover "
        "committed the misconduct of keeping minors at the scene of the culprit's attack.",
        [48, 256, 752, 352], dict(_P67, erase=[[48, 259, 752, 348]])),
       ("On Shiyo 800, April 8, while investigating the Motoki-cho flaying murder case, I was asked by a girl who held "
        "an important clue to procure necessary equipment. As a result, I procured a Noh mask, costumes, a mace and a "
        "nata, and furthermore had the girls remain at the scene as decoys to arrest the culprit. Procuring equipment "
        "without my superior's permission at the request of a mere girl of unknown origin violates the prescribed "
        "procedures, and furthermore, keeping minors at the scene while aware of the danger is conduct unbecoming of "
        "a police officer.", [48, 390, 752, 588], dict(_P67, erase=[[47, 393, 752, 583]])),
       ("For this misconduct I have no room for excuse, either as a police officer or as a member of society. I swear "
        "that from now on I will brace myself, take the utmost care never to repeat such misconduct, and, to restore "
        "the trust lost through this series of misconduct, make every possible effort at the Sawa Prefectural Police "
        "and Motoki Police Station.", [48, 626, 752, 756], dict(_P67, erase=[[48, 629, 752, 751]])),
       ("All responsibility for this matter lies with me, Daijiro Ise. I humbly ask that lenient measures be taken "
        "toward me and the subordinates who accompanied me.", [48, 794, 752, 880], dict(_P67, erase=[[48, 797, 752, 852]]))]
L67R = [("Lieutenant Ise's judgment and response in this matter are deemed to have been appropriate,",
         [170, 1000, 790, 1064], {"max_size": 26, "mask_color": _RED67, "erase": [[172, 1000, 772, 1062]]}),
        ("and disciplinary action is deferred.", [170, 1068, 790, 1112],
         {"max_size": 26, "mask_color": _RED67, "erase": [[175, 1074, 362, 1108]]})]
T77_1W = ["Today I took Akane to her month-and-a-half checkup. But the whole hospital was oddly",
          "hectic, and they just would not get around to her checkup. Since I had time to spare, I",
          "took Akane and looked through the glass into the newborn nursery. And there, a baby",
          "girl born just today was sleeping soundly with an adorable sleeping face. Her name is",
          "Mifuyu-chan. After I had watched her for a while, Akane woke up and started going",
          "\"Ah, ah.\" It was the first time Akane had made a sound other than crying. When I",
          "showed her, saying, \"Look, Akane, see? It's a little girl who was born just today,\" I",
          "felt as if Akane smiled. Akane isn't even old enough to smile yet, but when I showed",
          "her Mifuyu-chan, she seemed oddly happy."]
T77_2W = ["According to the nurse, Mifuyu-chan's mother died giving birth. Mifuyu-chan, sleeping so",
          "soundly, will never be able to meet her mother. So, if I can, I want to have Akane",
          "become her friend, so that Mifuyu-chan won't feel lonely, even a little. Maybe I'm",
          "sticking my nose in, though. I'll try going to see her again later."]
assert " ".join(T77_1W) == T77_1 and " ".join(T77_2W) == T77_2
JOBS += [
    {"id": "ref77", "screen": "reference 77 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#1a1a1a", "new": True,
     "note": "diary page on ruled paper (photo kept)", "items": [(D + "rrr77/0.gal", "")],
     "lines": [("Shiyo 757, December 3", [46, 53, 420, 80], {"max_size": 20, "mask_color": DARK, "erase": [[46, 54, 236, 79]]}),
               # IMAGES6 checker fix: one English line per ruled line (rules 117..580, pitch 35.64 = 1.4257 x the
               # Ink Free 19 px line), baseline 3 px above its rule, one empty rule between the paragraphs.
               # Breaks from work/images/_c/wrap77.py (Ink Free 19, width 704).
               ("\n".join(T77_1W), [48, 96, 752, 417], {"max_size": 19, "line_spacing": 1.4257, "align": "left",
                                                        "mask_color": DARK, "erase": [[46, 88, 752, 545]]}),
               ("\n".join(T77_2W), [48, 452, 752, 595], {"max_size": 19, "line_spacing": 1.4257, "align": "left",
                                                         "erase": []})]},
    {"id": "ref81", "screen": "reference 81 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#111111", "new": True,
     "note": "cheat-sheet memo (label / value rows)", "items": [(D + "rrr81/0.gal", "")],
     "lines": [(t, b, dict(o, mask_color=DARK)) for t, b, o in L81]},
    {"id": "ref239", "screen": "reference 239 detail", "style": "serif", "mode": "lines", "erase": "texfill",
     "erase_first": True, "mask_grow": 3, "color": "#1a1208", "new": True,
     "note": "brush-written rules on parchment (texfill keeps the grain)", "items": [(D + "rrr239/0.gal", "")],
     "lines": [(t, b, dict(o, mask_color=[0, 75, 0, 70, 0, 60])) for t, b, o in L239]},
    {"id": "ref90", "screen": "reference 90 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "mask_grow": 3, "color": INK, "new": True, "note": "printed accident account",
     "items": [(D + "rrr90/0.gal", "")], "lines": [(t, b, dict(o, mask_color=DARK)) for t, b, o in L90]},
    {"id": "ref93-head", "screen": "reference 93 detail", "style": "rounded", "mode": "lines", "erase": "inpaint",
     "mask_grow": 4, "color": "#0a0505", "new": True, "note": "restaurant opening flyer",
     "items": [(D + "rrr93/0.gal", "")],
     "lines": [("The famous Zahha opens store No. 35!!", [50, 44, 750, 97],
                {"max_size": 40, "align": "center", "mask_color": [0, 90, 0, 80, 0, 70], "erase": [[68, 46, 732, 95]]}),
               ("Motoki-cho's first family restaurant!!", [50, 101, 750, 154],
                {"max_size": 40, "align": "center", "mask_color": [0, 90, 0, 80, 0, 70], "erase": [[68, 103, 732, 152]]})]},
    {"id": "ref93-big", "screen": "reference 93 detail", "style": "rounded", "mode": "lines", "erase": "inpaint",
     "chain": True, "mask_grow": 7, "color": "#ffff1e", "stroke": 3, "stroke_color": "#9a3c00", "new": True,
     "note": "restaurant opening flyer", "items": [(D + "rrr93/0.gal", "")],
     "lines": [(t, b, {"max_size": 58, "align": "center", "mask_color": [215, 255, 170, 255, 0, 150], "erase": [e]})
               for t, b, e in [("Zahha Store No. 35", [120, 212, 680, 287], [198, 215, 602, 284]),
                               ("Shiyo 790, March 12 (Fri.)", [20, 290, 780, 366], [50, 293, 745, 363]),
                               ("Open from 18:00!!", [90, 368, 710, 444], [110, 371, 701, 441])]]},
    {"id": "ref93-body", "screen": "reference 93 detail", "style": "gothic", "mode": "lines", "erase": "inpaint",
     "chain": True, "mask_grow": 3, "color": "#fff0e0", "new": True, "note": "restaurant opening flyer",
     "items": [(D + "rrr93/0.gal", "")],
     "lines": [("Along with standard menu items such as the drink bar, pizza and pasta, we offer 70 kinds of dishes "
                "in all, including steak, Japanese food and desserts. Don't miss our limited-time menu either!",
                [30, 606, 778, 709], {"max_size": 22, "mask_color": [225, 255, 150, 255, 110, 255],
                                      "erase": [[28, 606, 778, 709]]})]},
    {"id": "ref93-menu", "screen": "reference 93 detail", "style": "gothic", "mode": "lines", "erase": "inpaint",
     "chain": True, "erase_first": True, "mask_grow": 3, "color": "#3c0800", "new": True,
     "note": "restaurant opening flyer", "items": [(D + "rrr93/0.gal", "")],
     "lines": [(t, b, dict({"mask_color": [0, 170, 0, 80, 0, 70]}, **o)) for t, b, o in L93M]},
    {"id": "ref3", "screen": "reference 3 detail", "style": "gothic", "mode": "lines", "erase": "maskfill",
     "mask_grow": 2, "color": "#222222", "new": True, "note": "rental listing (floor plan kept)",
     "items": [(D + "rrr3/0.gal", "")], "lines": [(t, b, dict({"mask_color": DARK}, **o)) for t, b, o in L3]},
    {"id": "ref67", "screen": "reference 67 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "mask_grow": 3, "color": INK, "new": True, "note": "written apology (printed)", "items": [(D + "rrr67/0.gal", "")],
     "lines": [(t, b, dict(o, mask_color=DARK)) for t, b, o in L67]},
    {"id": "ref67-red", "screen": "reference 67 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "chain": True, "mask_grow": 3, "color": "#d81f28", "new": True, "note": "written apology (red handwritten ruling)",
     "items": [(D + "rrr67/0.gal", "")], "lines": L67R},
    {"id": "ov-222", "screen": "reference screen preview", "style": "serif", "mode": "lines", "erase": "inpaint",
     "mask_grow": 2, "color": "#e8eef2", "new": True, "note": "police-station sign (overview only; no detail picture)",
     "items": [(O + "rr222.gal", "")],
     "lines": [("Motoki Police Station", [87, 15, 107, 117],
                {"rot": -90, "align": "center", "max_size": 13, "mask_color": [150, 255, 160, 255, 170, 255],
                 "erase": [[88, 16, 106, 115]]})]},
    {"id": "ov-p6", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (77, 81, 239, 90, 93, 3, 67)]},
]



# ---- IMAGES7 2026-10-01 (notes/IMAGES7-BRIEF.md): object / letter references unlocked in part 7
# (42 28 287 96 98 100 104 108). Boxes measured on the sources with work/images/_c/rows6.py / rows7.py (rows7 =
# rows6 with the form rules removed). The 60x30 thumbnails are below legibility: skipped. Scope B (scenario
# references 99 43 228 229 106 226 21): no legible text on any 概要, no job.
_BK = {"method": "flat", "bg": "#000000"}
_RD42 = "#e01818"


def _l42(t, box, er, **o):
    return (t, box, dict(_BK, erase=er, **o))


L42 = [
    ("SHINIGAMI", [56, 102, 262, 148], dict(_BK, color=_RD42, max_size=34, erase=[[58, 104, 228, 146]])),
    ("SUMMONING", [268, 102, 500, 148], dict(_BK, max_size=34, erase=[[230, 104, 482, 146]])),
    _l42("1. Make a paper doll", [40, 178, 520, 206], [[40, 179, 228, 205]]),
    _l42("Let's make a doll shaped like a person out of paper.", [40, 207, 510, 235], [[38, 208, 482, 234]]),
    _l42("Let's make it by cutting white paper with scissors.", [40, 236, 510, 263], [[38, 236, 530, 262]]),
    _l42("2. Write the name of the person to kill", [40, 351, 500, 379], [[40, 352, 320, 378]]),
    _l42("Let's write a name on the paper doll you made.", [40, 380, 500, 408], [[38, 381, 458, 407]]),
    _l42("You write the name of the person you want to kill.", [40, 409, 500, 437], [[40, 410, 433, 436]]),
    _l42("3. Let's spit on the paper doll", [40, 526, 470, 553], [[40, 527, 419, 552]]),
    _l42("Spit from your mouth and", [40, 555, 470, 582], [[38, 556, 397, 581]]),
    _l42("get the paper doll wet.", [40, 584, 470, 611], [[38, 585, 216, 610]]),
    _l42("This is the signal that calls", [40, 613, 470, 641], [[39, 614, 324, 640]]),
    _l42("the shinigami who will help you.", [40, 643, 470, 670], [[40, 644, 337, 669]]),
    _l42("4. Let's pray to the ancestors", [40, 759, 470, 786], [[39, 760, 419, 785]]),
    _l42("The ancestors are your father and mother,", [40, 788, 560, 815], [[39, 789, 512, 814]]),
    _l42("your grandfather and grandmother.", [40, 816, 560, 843], [[38, 817, 312, 842]]),
    _l42("They are the faraway fathers and mothers who lived long, long before that.", [40, 846, 760, 873],
         [[38, 847, 676, 872]]),
    _l42("The ancestors become shinigami", [40, 875, 560, 902], [[39, 876, 397, 901]]),
    _l42("and kill the person you want to kill for you.", [40, 904, 560, 932], [[40, 905, 433, 931]]),
    _l42("To parents", [58, 966, 400, 990], [[58, 968, 142, 989]], style="gothic", max_size=14, color="#e6e6e6"),
] + [_l42(t, [58, y0, 742, y0 + 19], [[58, y0 + 1, 682, y0 + 18]], style="gothic", max_size=13, color="#e6e6e6")
     for t, y0 in (("These are simplified introductions to sorcery methods of African folk religion.", 1008),
                   ("Locally there is a method of \"smearing vomit on the doll.\"", 1027),
                   ("In Africa bananas grow in abundance, and there is a culture of brewing an alcoholic drink "
                    "(banana beer) from them.", 1046),
                   ("The sorcerer drinks a large amount of banana beer, vomits as a result, and so completes the "
                    "sorcery.", 1065))]

_D96 = {"mask_color": DARK}
L96 = [(t, b, dict(_D96, erase=e, **o)) for t, b, e, o in [
    ("Supermarket Hanamaru", [112, 44, 372, 76], [[121, 45, 352, 74]], {"max_size": 26}),
    ("Supermarket Hanamaru Motoki Central Store", [14, 98, 364, 120], [[60, 99, 321, 119]], {"align": "center"}),
    ("Tel", [60, 123, 150, 144], [[100, 124, 141, 143]], {"align": "right"}),
    ("3-11 Chuo 1-chome, Motoki-cho, Sawa Prefecture", [14, 147, 364, 169], [[64, 148, 315, 168]], {"align": "center"}),
    ("Shiyo 800, April 7 (Tue.) 11:16", [14, 171, 364, 193], [[69, 172, 313, 192]], {"align": "center"}),
    ("RECEIPT", [60, 210, 320, 248], [[104, 211, 277, 247]], {"align": "center", "max_size": 30}),
    ("Sake", [89, 274, 210, 295], [[89, 275, 188, 294]], {}),
    ("Discount", [80, 298, 140, 319], [[79, 299, 118, 318]], {}),
    ("Wrapping", [88, 323, 250, 344], [[88, 324, 167, 343]], {}),
    ("Subtotal", [18, 371, 78, 392], [[18, 372, 58, 391]], {}),
    ("2 items", [80, 371, 160, 392], [[78, 372, 108, 391]], {}),
    ("(incl. consumption tax etc.", [18, 396, 285, 420], [[18, 397, 168, 419]], {}),
    ("TOTAL", [18, 425, 120, 455], [[18, 426, 76, 454]], {"max_size": 24}),
    ("Points paid", [18, 458, 200, 480], [[18, 459, 139, 479]], {}),
    ("Points balance", [18, 482, 200, 504], [[18, 483, 139, 503]], {}),
    ("Member no.", [18, 507, 200, 528], [[18, 508, 99, 527]], {}),
    ("Clerk 101", [250, 555, 352, 577], [[303, 556, 352, 576]], {"align": "right"}),
]]

_HW = {"style": "handwriting"}
_E100 = ["Entered Iizawa Prefectural Toyotake Elementary School", "Graduated from the same school",
         "Entered Iizawa Prefectural Toyotake Junior High School", "Graduated from the same school",
         "Entered Iizawa Prefectural Toyotake High School", "Graduated from the same school",
         "Entered National Kyoto University, Faculty of Education, Department of Social Welfare"]
L100 = [
    ("RESUME", [44, 86, 190, 117], {"max_size": 24, "erase": [[46, 86, 160, 116]]}),
    ("As of Shiyo", [190, 90, 330, 115], {"align": "right", "max_size": 14, "erase": [[258, 86, 532, 117]]}),
    ("798, May 7", [334, 86, 540, 117], dict(_HW, max_size=22, erase=[])),
    ("Reading", [48, 119, 92, 137], {"max_size": 9, "erase": [[50, 120, 93, 136]]}),
    ("Chigaya Niimura", [96, 118, 420, 138], dict(_HW, max_size=14, erase=[[94, 119, 170, 137], [236, 119, 330, 137]])),
    ("Name", [48, 138, 90, 152], {"max_size": 10, "erase": [[50, 138, 75, 151]]}),
    ("Chigaya Niimura", [90, 150, 500, 210], dict(_HW, max_size=46, erase=[[88, 151, 365, 209]])),
    ("Date of birth", [48, 212, 200, 227], {"max_size": 10, "erase": [[50, 213, 99, 226]]}),
    ("Sex", [481, 212, 540, 227], {"max_size": 10, "erase": [[481, 213, 508, 226]]}),
    ("Shiyo 779, May 18", [96, 229, 334, 266], dict(_HW, max_size=24, erase=[[95, 229, 307, 265]])),
    ("born  (age 18)", [338, 233, 478, 265], {"max_size": 15, "erase": [[338, 229, 472, 265]]}),
    ("Female", [478, 228, 545, 266], dict(_HW, max_size=20, erase=[[477, 229, 518, 265]])),
    ("Phone", [622, 262, 700, 278], {"max_size": 10, "erase": [[622, 262, 654, 277]]}),
    ("Reading", [48, 266, 100, 280], {"max_size": 9, "erase": [[50, 266, 95, 279]]}),
    ("Current address", [48, 284, 200, 299], {"max_size": 10, "erase": [[50, 285, 88, 298]]}),
    ("3-1-11 Higashiokubashi, Hamaoka Ward, Tokyo City, Chateau Hamaoka 303", [60, 299, 618, 348],
     dict(_HW, max_size=30, erase=[[60, 299, 620, 347]])),
    ("Mobile", [626, 305, 700, 320], {"max_size": 10, "erase": [[626, 306, 680, 319]]}),
    ("Reading", [48, 350, 100, 364], {"max_size": 9, "erase": [[50, 351, 95, 363]]}),
    ("Contact address  (postcode)", [48, 368, 240, 383], {"max_size": 10, "erase": [[50, 369, 108, 382]]}),
    ("(Fill in only if you wish to be contacted somewhere other than your current address)", [255, 368, 610, 383],
     {"max_size": 9, "erase": [[265, 369, 508, 382]]}),
    ("c/o", [600, 400, 625, 414], {"max_size": 10, "erase": [[611, 400, 623, 413]]}),
    ("Year", [48, 431, 115, 446], {"align": "center", "max_size": 10, "erase": [[75, 432, 89, 445]]}),
    ("Mo.", [116, 431, 145, 446], {"align": "center", "max_size": 10, "erase": [[124, 432, 136, 445]]}),
    ("Education / Work history (list each separately)", [150, 431, 745, 446],
     {"align": "center", "max_size": 10, "erase": [[363, 432, 533, 445]]}),
] + [(t, [150, 452 + 38 * i + 3, 748, 452 + 38 * i + 36],
      dict(_HW, max_size=24, erase=[[147, 452 + 38 * i, 752, 452 + 38 * i + 38]]))
     for i, t in enumerate(_E100)] + [
    ("End", [250, 721, 420, 754], dict(_HW, max_size=24, erase=[[147, 718, 752, 762]])),
    ("Year", [60, 1243, 127, 1259], {"align": "center", "max_size": 10, "erase": [[87, 1244, 100, 1258]]}),
    ("Mo.", [128, 1243, 156, 1259], {"align": "center", "max_size": 10, "erase": [[136, 1244, 148, 1258]]}),
    ("Education / Work history (list each separately)", [160, 1243, 745, 1259],
     {"align": "center", "max_size": 10, "erase": [[361, 1244, 530, 1258]]}),
    ("Year", [60, 1460, 127, 1476], {"align": "center", "max_size": 10, "erase": [[87, 1461, 101, 1475]]}),
    ("Mo.", [128, 1460, 156, 1476], {"align": "center", "max_size": 10, "erase": [[136, 1461, 148, 1475]]}),
    ("Licenses / Qualifications", [160, 1460, 745, 1476],
     {"align": "center", "max_size": 10, "erase": [[417, 1461, 475, 1475]]}),
    ("None", [180, 1478, 450, 1524], dict(_HW, max_size=30, erase=[[184, 1482, 277, 1521]])),
    ("Reasons for applying, special skills, favorite subjects, etc.", [58, 1681, 518, 1697],
     {"max_size": 10, "erase": [[60, 1682, 246, 1696]]}),
    ("Special skills: hunting, parkour", [60, 1712, 515, 1778], dict(_HW, max_size=40, erase=[[60, 1713, 473, 1777]])),
    ("Commute", [522, 1681, 600, 1697], {"max_size": 10, "erase": [[522, 1682, 576, 1696]]}),
    ("10 min", [600, 1686, 742, 1719], dict(_HW, max_size=24, erase=[[606, 1684, 690, 1718]])),
    ("Dependents (excluding spouse)", [522, 1719, 680, 1734], {"max_size": 9, "erase": [[522, 1720, 665, 1734]]}),
    ("", [720, 1744, 736, 1760], {"erase": [[720, 1744, 736, 1760]]}),
    ("Spouse", [522, 1760, 605, 1776], {"max_size": 10, "erase": [[522, 1760, 564, 1775]]}),
    ("Spouse's support obligation", [610, 1760, 745, 1776], {"max_size": 9, "erase": [[611, 1760, 711, 1775]]}),
    ("Personal requests (fill in especially if you have wishes about salary, job type, working hours, "
     "place of work or anything else)", [58, 1815, 745, 1832], {"max_size": 10, "erase": [[60, 1816, 564, 1831]]}),
    ("I grew up deep in the mountains out in the country, so I'm confident in my stamina!!", [62, 1834, 745, 1884],
     dict(_HW, max_size=34, erase=[[64, 1834, 690, 1883]])),
]
JOBS += [
    {"id": "ref42", "screen": "reference 42 detail", "style": "handwriting", "mode": "lines", "erase": "flat",
     "erase_first": True, "color": "#f4f4f4", "max_size": 20, "new": True,
     "note": "children's book page on black (doll and reaper art kept)", "items": [(D + "rrr42/0.gal", "")],
     "lines": L42},
    {"id": "ref96", "screen": "reference 96 detail", "style": "gothic", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#222222", "max_size": 15, "new": True,
     "note": "shop receipt (item codes, prices and numbers kept)", "items": [(D + "rrr96/0.gal", "")], "lines": L96},
    {"id": "ref100", "screen": "reference 100 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 3, "thr": 60, "color": INK, "max_size": 12, "new": True,
     "note": "CV (printed form serif, entries Ink Free; digits and phone numbers kept)",
     "items": [(D + "rrr100/0.gal", "")],
     "lines": [(t, b, dict({"mask_color": [0, 130, 0, 130, 0, 130]}, **o)) for t, b, o in L100]},
]


# ---- IMAGES7: close-ups (部分拡大N) are typeset at their own scale from the detail-page layout: every detail line's
# boxes are mapped into the close-up with the crop geometry found by work/images/_c/match7.py (template match of
# the close-up shrunk by 1/s in the detail; scores 0.80-0.99), sizes x s. A line whose mapped box is mostly outside
# the close-up keeps only its erase (the JP glyph part inside the crop is still erased). Reason (logged in
# tl-log-IMAGES7.md): a crop+upscale of the detail would blow 6-9 px English type up 1.4-2.1x and blur it, while the
# close-ups are where the player reads the text.
def zoom_lines(lines, ox, oy, s, W, H, keep=0.85):
    def tr(b):
        return [(b[0] - ox) * s, (b[1] - oy) * s, (b[2] - ox) * s, (b[3] - oy) * s]

    def clamp(b):
        c = [max(0, int(round(b[0]))), max(0, int(round(b[1]))), min(W, int(round(b[2]))), min(H, int(round(b[3])))]
        return c if c[2] - c[0] > 1 and c[3] - c[1] > 1 else None

    out = []
    for e in lines:
        t, b, o = e[0], e[1], dict(e[2]) if len(e) > 2 else {}
        tb = tr(b)
        cb = clamp(tb)
        ers = [clamp(tr(x)) for x in o.get("erase", [b])]
        ers = [x for x in ers if x]
        if cb is None and not ers:
            continue
        area = (tb[2] - tb[0]) * (tb[3] - tb[1])
        inside = cb and (cb[2] - cb[0]) * (cb[3] - cb[1]) >= keep * area
        o["erase"] = ers
        if o.get("max_size"):
            o["max_size"] = int(round(o["max_size"] * s))
        if "rot_h" in o:
            o["rot_h"] = int(round(o["rot_h"] * s))
        if inside and t:
            out.append((t, cb, o))
        elif ers:
            out.append(("", cb or ers[0], o))
    return out


def zoom_items(rid, layout, crops, extra=None):
    """crops = [(n, s, ox, oy, W, H)] -> batch items for rrr<rid>/部分拡大n.gal with mapped lines."""
    return [(D + "rrr%s/部分拡大%d.gal" % (rid, n), "", dict({"lines": zoom_lines(layout, ox, oy, s, W, H)}, **(extra or {})))
            for n, s, ox, oy, W, H in crops]


# ---- 28 newspaper (Megasawa Newspaper 3): 800x540 + 7 close-ups; columns -> horizontal English blocks (ref23 way)
N28_CAP = "Nanami-so, where the fire broke out (Nanami-cho, Megasawa City)"
N28_2 = ("Shortly after 8 p.m. the day before yesterday, April 8, a fire broke out in a wooden apartment building in "
         "Nanami-cho, Megasawa City, and four people died. The dead were Mifuyu Niimura-san (32) and Haruka "
         "Niimura-chan (7), who lived in the building. The two died in the room where they lived, and the bodies of two "
         "unidentified people were also found in the same room. These bodies are thought to be the parents of a "
         "first-grade elementary school girl (6) who is believed to have escaped from Niimura-san's room.")
N28_3 = ("The surviving girl has no visible injuries, but the mental shock appears to be great, and the police plan to "
         "wait for her to recover before questioning her. Her parents, Ryoji Kogori-san (32) and Akane Kogori-san (32) "
         "of Motoki-cho, Sawa Prefecture, cannot be reached, and the company where Kogori-san works says he is "
         "\"taking paid leave for a memorial service.\"")
N28_4 = ("The four who died are thought to have already been dead when the fire broke out, and it is believed that "
         "someone killed the four and then set the fire, or that one of the four killed the other three and then set "
         "the fire. A nata with a blade about")
N28_5 = ("40 centimeters long and a blunt weapon, believed to have been used in the killings, were found at the scene, "
         "and it is presumed to have been a planned murder and arson, but several questions remain. The autopsy "
         "revealed that the bodies had suffered injuries from extremely strong force, such as a head smashed with a "
         "single blow and lungs burst with a single blow.")
N28_6 = ("Even using the weapons at the scene, inflicting such injuries would be extremely difficult. However, it is "
         "utterly unthinkable that the girl, the only one to survive this incident, could have carried out such "
         "killings, so it is also conceivable that")
N28_7 = ("someone broke into the Niimura home, killed them with a special weapon, and left the nata and blunt weapon "
         "behind as camouflage. The surviving girl is thought to have lived through it by hiding or the like, and she "
         "probably knows the full picture of the incident.")
_NM = {"mask_color": [0, 150, 0, 150, 0, 150]}
_NH = {"mask_color": [0, 110, 0, 110, 0, 110], "no_rules": True}
_GAME = ("Game creation tool,\nno programming needed", [693, 442, 788, 481],
         dict(_NM, align="center", max_size=10, erase=[[694, 443, 787, 480]]))
L28 = [
    ("Megasawa Newspaper", [262, 7, 470, 28], dict(_NM, align="center", max_size=12, erase=[[310, 8, 425, 28]])),
    ("Shiyo 790, April 10   Saturday   No. 24685", [560, 7, 790, 28],
     dict(_NM, align="right", max_size=11, erase=[[564, 8, 788, 28]])),
    ("MEGASAWA\nNEWSPAPER", [694, 48, 773, 342], dict(_NH, rot=-90, align="center", max_size=34,
                                                    mask_color=[0, 90, 0, 90, 0, 90], erase=[[696, 52, 771, 340]])),
    ("Publisher\nMegasawa Newspaper Co.\n31-16 Kokuji, Megasawa City,\nIizawa Prefecture\nPostal code 995-XXXX\n"
     "(C) Megasawa Newspaper Co. 790\nTel 226(541)XXXX", [693, 355, 788, 440],
     dict(_NM, align="center", max_size=8, line_spacing=1.0, erase=[[693, 356, 788, 439]])),
    _GAME,
    ("Fire in Nanami-cho. 4 dead.", [612, 55, 680, 505], dict(_NH, rot=-90, align="center", max_size=48,
                                                             erase=[[612, 56, 680, 505]])),
    ("Fire in an aging wooden house. Died together?", [560, 105, 606, 485],
     dict(_NH, rot=-90, align="center", max_size=30, erase=[[561, 106, 605, 484]])),
    (N28_CAP, [262, 236, 548, 258], dict(_NM, align="center", max_size=11, erase=[[300, 238, 510, 256]])),
    (N28_2, [266, 276, 546, 386], dict(_NM, max_size=10)),
    (N28_3, [314, 396, 544, 508], dict(_NM, max_size=10)),
    ("Extremely unnatural bodies. A murder-suicide?", [204, 82, 260, 492],
     dict(_NH, rot=-90, align="center", max_size=34, erase=[[206, 84, 258, 490]])),
    (N28_4, [36, 38, 198, 150], dict(_NM, max_size=10)),
    (N28_5, [36, 156, 198, 268], dict(_NM, max_size=10)),
    (N28_6, [36, 273, 198, 388], dict(_NM, max_size=10)),
    (N28_7, [36, 395, 198, 508], dict(_NM, max_size=10)),
]
Z28 = [(1, 1.82, 260, 50, 523, 396), (2, 1.75, 263, 270, 498, 207), (3, 1.76, 312, 392, 411, 210),
       (4, 1.75, 31, 34, 296, 200), (5, 1.75, 29, 152, 294, 205), (6, 1.81, 24, 271, 312, 216),
       (7, 1.82, 30, 393, 304, 219)]

# ---- 104 newspaper (Iizawa Newspaper): 800x520 + 4 close-ups
N104_A = ("On the night of August 20, a case occurred in which Tsutomu Kanesaki-san (58), a prefectural employee living "
          "in Iizawa City, was killed. According to the family he lived with, Kanesaki-san came home from work, but "
          "talked with someone on the phone and went straight out again. In this case, the police made an emergency "
          "arrest, on suspicion of murder, of Nobuhiro Shikishima (38), unemployed, a resident of the city who was "
          "present at the scene. Suspect Shikishima is said to have been sitting beside Kanesaki-san's body holding a "
          "bloody blade like a nata.")
N104_B = ("Kanesaki-san and Suspect Shikishima were found in a dead-end alley with a dim streetlight, and it is believed "
          "that Suspect Shikishima either called Kanesaki-san out by phone or killed him in the manner of a random "
          "street attacker. Suspect Shikishima is said to have kept silent since his arrest and not even to respond to "
          "small talk with the police. Kanesaki-san's body appears to have been slashed many times with a large blade, "
          "and he is thought to have been killed out of a very strong grudge. At present the relationship between "
          "Kanesaki-san and Suspect Shikishima is unknown, but it is believed there was some kind of trouble between "
          "the two.")
N104_L1 = ("According to neighbors, Suspect Shikishima was a very polite and earnest company employee, but he recently "
           "lost his job, and his family also left him. Meanwhile, it is said that Kanesaki-san,")
N104_L2 = ("while behaving well as an official of the prefecture, also had a hidden face. Kanesaki-san reportedly gave "
           "money to strangers and did volunteer work, but it is also said that he had cozy ties with organized crime "
           "and was carrying out land grabs by illicit methods.")
N104_L3 = ("It is thought that trouble arose with Suspect Shikishima over that side of him, which may have caused his "
           "strong grudge against Kanesaki-san. In any case, since Suspect Shikishima has no intention of making a "
           "statement, the clear motive is unknown, but the day Kanesaki-san's hidden face is exposed may also")
N104_L4 = ("be near. According to a certain source, Kanesaki-san has recently been seen often in Toyotake, and it is even "
           "rumored that he may have been trying to carry out an illicit land grab in the Arata district, which is "
           "state-owned land.")
_NM4 = {"mask_color": [0, 165, 0, 165, 0, 165]}
L104 = [
    ("Iizawa Newspaper", [262, 6, 470, 27], dict(_NM4, align="center", max_size=12, erase=[[322, 7, 465, 26]])),
    ("Shiyo 750, August 22   Saturday   No. 2468", [560, 6, 790, 27],
     dict(_NM4, align="right", max_size=11, erase=[[606, 7, 780, 26]])),
    ("IIZAWA\nNEWSPAPER", [694, 48, 773, 342], dict(_NH, rot=-90, align="center", max_size=34,
                                                  mask_color=[0, 90, 0, 90, 0, 90], erase=[[696, 52, 771, 340]])),
    ("Publisher\nIizawa Media\nIizawa City, Iizawa Prefecture\n1-10\nPostal code 999-1234\n(C) Iizawa Media\n"
     "Tel 230(500)", [693, 355, 788, 440],
     dict(_NM4, align="center", max_size=8, line_spacing=1.0, erase=[[693, 356, 788, 439]])),
    _GAME,
    ("Prefectural Employee Murdered!", [618, 70, 682, 470], dict(_NH, rot=-90, align="center", max_size=48,
                                                                mask_color=[0, 120, 0, 120, 0, 120],
                                                                erase=[[620, 72, 680, 468]])),
    ("Culprit arrested, but silent! The mystery deepens!", [582, 110, 622, 350],
     dict(_NH, rot=-90, align="center", max_size=26, mask_color=[0, 120, 0, 120, 0, 120], erase=[[584, 112, 620, 348]])),
    ("Suspect Nobuhiro Shikishima being taken away", [312, 188, 536, 206],
     dict(_NM4, align="center", max_size=11, erase=[[345, 190, 495, 205]])),
    (N104_A, [461, 208, 577, 510], dict(_NM4, max_size=10)),
    ("Suspect Shikishima keeps silent! What is his motive!?", [424, 208, 446, 510],
     dict(_NM4, rot=-90, align="center", max_size=14, erase=[[426, 210, 444, 508]], no_rules=True)),
    (N104_B, [283, 208, 412, 510], dict(_NM4, max_size=10)),
    ("Tsutomu Kanesaki-san,\nwho was killed", [26, 118, 106, 150],
     dict(_NM4, align="center", max_size=10, erase=[[32, 120, 106, 148]])),
    ("Kanesaki-san: an angel? Or a devil?", [229, 82, 264, 460],
     dict(_NH, rot=-90, align="center", max_size=30, mask_color=[0, 120, 0, 120, 0, 120], erase=[[231, 84, 262, 458]])),
    (N104_L1, [108, 41, 221, 145], dict(_NM4, max_size=10)),
    (N104_L2, [18, 150, 221, 275], dict(_NM4, max_size=10)),
    (N104_L3, [18, 280, 221, 385], dict(_NM4, max_size=10)),
    (N104_L4, [87, 394, 221, 513], dict(_NM4, max_size=10)),
]
Z104 = [(1, 1.88, 312, 38, 422, 312), (2, 1.43, 280, 202, 427, 450), (3, 1.68, 16, 39, 347, 400),
        (4, 1.68, 16, 278, 347, 400)]

# ---- 108 occult magazine spread (800x569, dark-red print) + 3 close-ups
M108_UL = ("The team assembled in late April, Shiyo 747, all died with their heads smashed a few days after starting their "
           "research. This case shook Motoki-cho and stirred up the residents' unease. After all, Motoki-cho, whose only "
           "merit had been having nothing special about it, had, through a cherry tree that suddenly appeared, become "
           "the scene of a bizarre mass murder case. What's more, far from a culprit, there are no witnesses or items "
           "left behind, and the case is already expected to go unsolved.")
M108_LL = ("Many think, \"There are people who were suddenly erased by the cherry tree that suddenly appeared,\" or \"Isn't "
           "this case caused by the curse of the cherries?\" In the first place, the mere appearance of a cherry tree "
           "that looks several hundred years old is bizarre and mysterious. It is natural to think there is some reason "
           "why a bizarre murder case beyond human understanding like this one occurs. One cannot help but sense the "
           "presence of those who plead, \"You must not learn the secret of this cherry tree,\" and")
M108_B = ("learning the secret of this case, and the secret of the cherry tree, must be extremely dangerous. And yet, "
          "there is no way you readers do not feel the allure of this secret. We will continue to cover this case from "
          "both sides, the murders and the curse. In this corner of next month's issue we will report the "
          "continuation of this Motoki-cho researcher slaughter case and pursue thoroughly whether it is truly the "
          "curse of the cherries, or a crime by a deranged person taking advantage of it. For further news on the "
          "case, wait for next month's issue!")
M108_R1 = ("Have you heard the story of the cherry tree that suddenly appeared? In Motoki-cho, Sawa Prefecture, a small "
           "town with nothing special about it, a single cherry tree suddenly appeared one day. Motoki-cho, which its "
           "own townspeople claim had nothing special about it until now, is said to have taken on a tense atmosphere "
           "from that day on. That is because not only did tourists gather to get a look at this mysterious cherry "
           "tree, but a survey of the cherry tree by a public institution was also to be carried out. The unbelievable "
           "phenomenon of a cherry tree suddenly appearing: that a public institution would investigate it means, in "
           "other words, that this")
M108_R2 = ("mysterious cherry tree really exists. It is said that lodgings were prepared for the researchers and research "
           "facilities were being set up one after another, and the day the secret of this cherry tree would be solved "
           "seemed near.")
_MR = {"mask_color": [0, 235, 0, 205, 0, 205]}
_INK108 = "#8a2a2a"
L108 = [
    ("NO ENTRY", [20, 84, 84, 116], {"rot": 11, "rot_h": 16, "max_size": 16, "color": "#8a1c1c", "method": "inpaint",
                                     "mask_color": [0, 200, 0, 140, 0, 140], "erase": [[22, 88, 82, 113]]}),
    ("Please do not enter", [86, 78, 162, 102], {"rot": 11, "rot_h": 10, "max_size": 9, "color": "#8a1c1c",
                                                 "method": "inpaint", "mask_color": [0, 200, 0, 140, 0, 140],
                                                 "erase": [[86, 83, 160, 98]]}),
    ("The researchers were\nburied with the mystery", [252, 14, 372, 408],
     dict(_MR, rot=-90, align="center", max_size=46, color="#8a0a0a", erase=[[255, 16, 370, 406]])),
    (M108_UL, [22, 186, 240, 297], dict(_MR, max_size=11, erase=[[20, 185, 242, 298]])),
    (M108_LL, [22, 306, 240, 418], dict(_MR, max_size=11, erase=[[20, 305, 242, 419]])),
    (M108_B, [98, 425, 368, 538], dict(_MR, max_size=11, erase=[[96, 424, 370, 539]])),
    ("This Month's Emergency Scoop Special", [432, 24, 768, 55],
     dict(_MR, align="center", max_size=22, color="#a03030", erase=[[437, 26, 764, 54]])),
    (M108_R1, [440, 288, 686, 408], dict(_MR, max_size=11, erase=[[438, 287, 688, 409]])),
    (M108_R2, [596, 413, 686, 542], dict(_MR, max_size=11, erase=[[594, 412, 688, 543]])),
    ("The Curse of the Cherries?\nThose Who Were Buried", [711, 98, 780, 480],
     dict(_MR, rot=-90, align="center", max_size=24, color="#8a0a0a", erase=[[711, 100, 780, 478]])),
]
Z108 = [(1, 1.70, 422, 283, 456, 450), (2, 1.87, 17, 182, 419, 450), (3, 2.00, 92, 418, 567, 255)]

# ---- 287 calligraphy letter, two paper faces (letter() of the 書簡 block; 2 English blocks right to left)
L287 = ("The recent battle with the bandits threatened the survival of the settlement. By joining our strength, we were "
        "able to come through battle after battle. This too was only because we knew the land of Arata well. A great "
        "many years have passed since the founder left this place, but more powerful military governors or land "
        "stewards may appear who set their eyes on this land. If in the future there should appear weapons that "
        "endanger even our advantage of terrain, the land of Arata too would be taken from us. Therefore I say to the "
        "people of the settlement: let every one of you learn how to fight, and do not neglect daily training, so that "
        "we can drive off invaders whenever they appear. As for our weapons, perhaps the nata and the staff, which we "
        "use every day and know well, are suited. But then we too will be required to go outside the settlement to "
        "gather weapons and materials. Therefore it also becomes a threat that our faces, few as we are, may be "
        "remembered. In battle, something to hide the face is needed. So that eternal peace may come to this land of "
        "Arata: one for all, and all for one.")
_L287 = letter(L287, 16, 884, 2)

# ---- 98 guidebook spread (706x500, gothic): layout in detail coordinates; the close-ups are typeset from it
# (zoom_lines), the detail page = the 5 English close-ups pasted back at the matched geometry
# (work/images/_c/paste7.py) + the right-hand band typeset directly (job ref98, chain).
_K98 = {"mask_color": [0, 110, 0, 110, 0, 110], "color": "#1a1a1a"}
_W98 = {"mask_color": [190, 255, 190, 255, 190, 255], "color": "#ffffff", "align": "center"}
_R98 = {"mask_color": [150, 255, 0, 110, 0, 110], "color": "#e01e1e", "align": "center"}
_PILL = "#dc6a14"


def _ini(letter_, rest, ib, rb, rest_er):
    return [(letter_, ib, dict(_R98, max_size=15)), (rest, rb, dict(_K98, max_size=8, erase=[rest_er]))]


G98 = ([
    ("Toyotake", [38, 24, 141, 47], dict(_W98, max_size=15, erase=[[62, 27, 116, 46]])),
    ("Toyotake still has primeval forest from ancient times, and there are said to be areas no one has set foot in "
     "even now. Yet there are also power spots that make use of nature, giving energy to people worn out by the "
     "bustle of the city.", [33, 60, 348, 92], dict(_K98, max_size=8)),
] + _ini("T", "oyotake Climbing", [96, 99, 115, 122], [115, 104, 252, 117], [114, 104, 142, 117]) + [
    ("The sunset seen from Toyotake, known as a graceful mountain, was chosen last year as one of the \"100 Views to "
     "Leave to Future Generations.\" The local food served at the inns at its foot is good for nourishment and "
     "recovery from fatigue, and lately the area has also been drawing attention as a place of recuperation.",
     [91, 116, 257, 156], dict(_K98, max_size=8)),
    ("*There is state-owned land nearby. Entering without permission is punishable.", [36, 156, 257, 165],
     dict(_K98, max_size=7, erase=[[38, 156, 200, 165]])),
    ("The Editor-in-Chief's Extra Trivia", [64, 180, 250, 195], dict(_K98, max_size=8, erase=[[64, 181, 170, 195]])),
    ("At Toyotake Station there is an ice cream shop that has been loved for decades. It's low-key, but I think it's a "
     "local specialty that should be better known in Iizawa Prefecture.", [38, 198, 256, 219], dict(_K98, max_size=8)),
    ("Nakatsu", [32, 231, 138, 258], dict(_W98, max_size=15, erase=[[64, 234, 112, 256]])),
    ("Nakatsu, in the center of the prefecture, is a spot blessed with rivers and mountains and popular with activity "
     "players. Mount Nakatsu, which shows a different face in each of the four seasons, draws photographers from all "
     "over the world.", [31, 265, 348, 298], dict(_K98, max_size=8)),
] + _ini("N", "akatsu Highland Ski Resort", [90, 308, 107, 327], [107, 314, 252, 326], [106, 314, 180, 326]) + [
    ("Located on the north slope of Mount Nakatsu, the highest peak in the prefecture, Nakatsu Highland Ski Resort is "
     "one of the largest in Japan, with a 1,200-meter vertical drop and 40 courses. Spring skiing can be enjoyed until "
     "early May.", [98, 327, 346, 357], dict(_K98, max_size=8)),
] + _ini("K", "amiura Stream", [90, 360, 107, 379], [107, 366, 220, 378], [106, 366, 134, 378]) + [
    ("It is lively with people enjoying boat rides down the river beneath sheer cliffs with a 50-meter drop, and river "
     "fishing. There is also a campsite, so many tourists visit with their families.", [98, 378, 346, 399],
     dict(_K98, max_size=8)),
    ("The Editor-in-Chief's Extra Trivia", [62, 429, 250, 441], dict(_K98, max_size=8, erase=[[62, 429, 160, 441]])),
    ("The first time I visited Iizawa Prefecture was in junior high. That day my family went on a ski trip, and I still "
     "can't forget the taste of the amazake served at the inn where we stayed. They said it was made with carefully "
     "selected sake lees from a brewery in Iizawa City, and pouring that into a body tired from skiing was just "
     "irresistible.", [38, 447, 284, 481], dict(_K98, max_size=8, erase=[[60, 441, 284, 447], [38, 447, 284, 481]])),
    ("Iizawa", [374, 17, 476, 48], dict(_W98, max_size=15, erase=[[400, 20, 452, 46]])),
    ("Iizawa City, the prefectural capital, is famous not only for city sightseeing but also as a \"town of sake.\" Not "
     "just sake: wine, shochu and local beer are popular too. The subway is well developed, so you can wander around "
     "and enjoy drinking tourism to the full while you drink!", [378, 54, 622, 91], dict(_K98, max_size=8)),
] + _ini("I", "izawa Brewery Tour", [511, 102, 531, 122], [530, 108, 622, 120], [529, 108, 570, 120]) + [
    ("More than 30 breweries stand in a row; besides tours of sake making there is plenty of tasting, more than you "
     "could ever get around in one day! There is also a food-stall village that makes use of local ingredients.",
     [512, 121, 621, 161], dict(_K98, max_size=8)),
] + _ini("N", "atural History Museum", [511, 170, 529, 190], [528, 176, 622, 188], [527, 176, 572, 188]) + [
    ("Iizawa City is famous not only for sake but also for the fossils dug up there.", [512, 188, 621, 209],
     dict(_K98, max_size=8)),
    ("Besides a complete Tyrannosaurus skeleton, you can see creatures from the Paleozoic to the Cenozoic all at once.",
     [458, 209, 621, 230], dict(_K98, max_size=8)),
    ("Megasawa", [390, 268, 489, 292], dict(_W98, max_size=15, erase=[[404, 270, 470, 291]])),
    ("One of Japan's largest cities by area. That means many tourist spots are scattered around it. Just driving "
     "around the city in a rental car will leave your heart and stomach fully satisfied!", [490, 272, 634, 311],
     dict(_K98, max_size=8)),
] + _ini("U", "nreal Park", [456, 325, 472, 342], [471, 329, 580, 340], [470, 329, 523, 340]) + [
    ("Japan's largest theme park, completed last year. From thrill rides to fairy tales to horror, everything is "
     "thoroughly crafted, and it is colossal in both quality and quantity!", [456, 341, 622, 369],
     dict(_K98, max_size=8)),
    ("A classic zoo loved by the people of Megasawa City for many years. From this year an albino peacock joins the "
     "family! It has evolved into an even more fun zoo!", [456, 390, 622, 419], dict(_K98, max_size=8)),
] + _ini("I", "izawa Hot Spring Village", [456, 421, 474, 438], [473, 424, 600, 436], [472, 424, 508, 436]) + [
    ("A hot spring resort on the coast. Megasawa City faces both the sea and the mountains, so it is a luxurious area "
     "where you can enjoy the bounty of the mountains, the bounty of the sea and the blessings of the hot springs all "
     "at once. Day trips OK!", [456, 437, 624, 467], dict(_K98, max_size=8)),
] + [(t, b, {"method": "flat", "bg": _PILL, "color": "#ffffff", "align": "center", "max_size": 7, "erase": [b]})
     for t, b in (("Toyotake", [309, 137, 357, 149]), ("Iizawa", [394, 164, 428, 176]), ("Nakatsu", [339, 200, 377, 212]),
                  ("Megasawa", [313, 252, 361, 265]))])
# the right-hand band (outside every close-up): typeset on the pasted-back detail
G98_BAND = [
    ("Enjoy\nit all", [603, 6, 700, 58], dict(_W98, max_size=16, line_spacing=0.95, erase=[[600, 4, 704, 62]])),
    ("A Trip All Around Iizawa Prefecture", [643, 110, 677, 365],
     dict(_K98, rot=-90, align="center", max_size=20, erase=[[646, 113, 673, 360]])),
    ("How to Enjoy Iizawa Prefecture\nBeginner's Edition", [636, 378, 684, 496],
     dict(_W98, rot=-90, max_size=14, mask_color=[180, 255, 150, 255, 150, 255], erase=[[636, 378, 684, 496]])),
]
Z98 = [(1, 1.69, 354, 0, 454, 400), (2, 1.93, 367, 262, 521, 400), (3, 2.12, 258, 96, 412, 400),
       (4, 1.96, 22, 20, 579, 400), (5, 1.52, 17, 223, 503, 400)]

JOBS += [
    {"id": "ref28", "screen": "reference 28 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "mask_grow": 3, "color": INK, "line_spacing": 1.05, "new": True,
     "note": "newspaper page (photo and the LiveMaker logo kept)", "items": [(D + "rrr28/0.gal", "")], "lines": L28},
    {"id": "ref28-zoom", "screen": "reference 28 close-ups", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "mask_grow": 5, "color": INK, "line_spacing": 1.05,
     "note": "newspaper close-ups (same English as the page, own scale)", "items": zoom_items(28, L28, Z28), "lines": []},
    {"id": "ref104", "screen": "reference 104 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "mask_grow": 3, "color": "#222222", "line_spacing": 1.05,
     "new": True, "note": "newspaper page (photos and the LiveMaker logo kept)", "items": [(D + "rrr104/0.gal", "")],
     "lines": L104},
    {"id": "ref104-zoom", "screen": "reference 104 close-ups", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "mask_grow": 5, "color": "#222222", "line_spacing": 1.05,
     "note": "newspaper close-ups (same English as the page, own scale)", "items": zoom_items(104, L104, Z104),
     "lines": []},
    {"id": "ref108", "screen": "reference 108 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": _INK108, "line_spacing": 1.05, "new": True,
     "note": "occult magazine spread (photos kept)", "items": [(D + "rrr108/0.gal", "")], "lines": L108},
    {"id": "ref108-zoom", "screen": "reference 108 close-ups", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 5, "color": _INK108, "line_spacing": 1.05,
     "note": "magazine close-ups (same English as the page, own scale)", "items": zoom_items(108, L108, Z108),
     "lines": []},
    {"id": "ref287-letter", "screen": "reference 287 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy letter, both paper faces (English blocks right to left, as the JP columns)",
     "items": [(D + "rrr287/0.gal", ""), (D + "rrr287/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L287]},
    {"id": "ref98-zoom", "screen": "reference 98 close-ups", "style": "gothic", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 4, "color": "#1a1a1a", "new": True,
     "note": "guidebook close-ups (typeset at own scale from the page layout)", "items": zoom_items(98, G98, Z98),
     "lines": G98},
    {"id": "ref98", "screen": "reference 98 detail", "style": "gothic", "mode": "lines", "erase": "inpaint",
     "chain": True, "erase_first": True, "mask_grow": 3, "color": "#1a1a1a", "new": True,
     "note": "guidebook spread (close-ups pasted back by work/images/_c/paste7.py, then the right band)",
     "items": [(D + "rrr98/0.gal", "")], "lines": G98_BAND},
    {"id": "ov-p7", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (42, 28, 287, 96, 98, 100, 104, 108)]},
]



# ---- IMAGES8 2026-10-02 (notes/IMAGES8-BRIEF.md): object / letter references unlocked in part 8 (142 143 33 158 109)
# + the scenario 概要 rr114 (security-camera caption). Boxes measured on the sources with work/images/_c/rows7.py and
# work/images/_c/blocks8.py. The 60x30 thumbnails are below legibility: skipped. Scope B 概要 without text (112 230 113
# 115 116 117 296 123) and rr231 (blurred marks, QIMAGES8-01): no job. rr33 概要 = a crop of the bear art: no text.
_MON = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
        "November", "December"]
_K142 = {"mask_color": [0, 100, 0, 85, 0, 70], "color": "#231300", "max_size": 17}
_R142 = {"mask_color": [140, 255, 0, 80, 0, 70], "color": "#c41a14", "max_size": 17}
_C142 = {"accident": "Accidental death", "curse": "Curse-killing", "suicide": "Suicide", "illness": "Illness"}
_X142 = {"L": (8, 393), "R": (401, 795)}
_REG142 = [  # (column, name-line top y, name, born (y, m, d), died (y, m, d), cause) - top / middle / bottom panels
    ("L", 7, "Sakura Niimura", (758, 4, 29), (790, 4, 17), "accident"),
    ("L", 96, "Yuriko Shirozaki", (754, 1, 1), (791, 4, 2), "curse"),
    ("L", 185, "Chibana Se", (745, 10, 1), (792, 4, 2), "curse"),
    ("L", 273, "Toya Niimura", (740, 3, 18), (793, 4, 14), "curse"),
    ("L", 363, "Sumire Se", (738, 9, 5), (794, 4, 17), "curse"),
    ("R", 6, "Tetsuji Niijima", (741, 12, 8), (795, 4, 4), "curse"),
    ("R", 95, "Hiroshi Niimura", (749, 11, 16), (796, 4, 2), "curse"),
    ("R", 185, "Takumi Shirozaki", (727, 2, 10), (797, 4, 9), "curse"),
    ("R", 272, "Koji Niijima", (730, 4, 25), (798, 4, 3), "curse"),
    ("R", 362, "Hajime Shirozaki", (746, 9, 30), (799, 4, 10), "curse"),
    ("L", 462, "Tsuya Niimura", (650, 1, 21), (740, 4, 7), "suicide"),
    ("L", 550, "Futoshi Niijima", (654, 12, 11), (742, 4, 21), "illness"),
    ("L", 639, "Takeo Niijima", (679, 10, 1), (745, 4, 22), "suicide"),
    ("L", 728, "Ryota Se", (681, 8, 18), (747, 4, 4), "suicide"),
    ("L", 817, "Hana Shirozaki", (673, 6, 9), (749, 4, 11), "illness"),
    ("R", 461, "Kaede Niimura", (684, 9, 18), (760, 4, 3), "suicide"),
    ("R", 550, "Koichiro Niimura", (725, 4, 1), (760, 4, 6), "accident"),
    ("R", 640, "Ken Shirozaki", (690, 10, 11), (766, 4, 10), "suicide"),
    ("R", 728, "Eiichiro Niimura", (757, 5, 27), (788, 4, 8), "accident"),
    ("R", 817, "Takeharu Shirozaki", (713, 7, 1), (789, 4, 11), "suicide"),
    ("R", 920, "Motoemon Shirozaki", (619, 4, 30), (709, 4, 6), "illness"),
    ("R", 1009, "Karin Niijima", (614, 7, 3), (715, 4, 15), "illness"),
    ("R", 1099, "Satoshi Se", (631, 2, 20), (721, 4, 19), "illness"),
    ("R", 1188, "Kasumi Niimura", (630, 8, 23), (723, 4, 1), "illness"),
    ("R", 1277, "Kikyo Niimura", (663, 10, 25), (735, 2, 1), "illness"),
]


def _d142(d):
    return "Shiyo %d, %s %d" % (d[0], _MON[d[1]], d[2])


L142 = []
for _c, _y, _n, _b, _dd, _cs in _REG142:
    _x0, _x1 = _X142[_c]
    _yb, _yd = _y + 22, _y + 44
    L142 += [
        (_n, [_x0, _y - 3, _x0 + 300, _y + 20], dict(_K142, erase=[[_x0, _y - 2, _x0 + 200, _y + 20]])),
        ("Born " + _d142(_b), [_x0, _yb - 3, _x1, _yb + 20], dict(_K142, erase=[[_x0, _yb - 2, _x1, _yb + 20]])),
        ("Died " + _d142(_dd), [_x0, _yd - 3, _x0 + 228, _yd + 21], dict(_R142, erase=[[_x0, _yd - 2, _x1, _yd + 22]])),
        (_C142[_cs], [_x0 + 236, _yd - 3, _x1, _yd + 21], dict(_R142, erase=[])),
    ]

# ---- 143 Goto's timeline (524x540, handwritten on ruled paper): rows locked to the rules (baseline just above the
# next rule); the drawn arrows of rows 791 / 799 are kept; the 4 notes below the table one per JP line.
_RU143 = [32, 59, 86, 113, 140, 167, 194, 221, 248, 275, 302, 329]
_T143 = [("Shiyo 735", "Kikyo-san dies (February)"),
         ("Shiyo 740", "From here the old people's suicides begin"),
         ("Shiyo 750", "Erika Niimura marries into Arata (moves there)"),
         ("Shiyo 760", "Deaths from illness stop (suicide or accidental death)"),
         ("Shiyo 788", "Eiichiro Niimura dies"),
         ("Shiyo 789", "The last suicide"),
         ("Shiyo 789", "Sakura-san murdered?   The affair in Megasawa"),
         ("Shiyo 791", None),
         (None, "One person curse-killed every year (murder)"),
         ("Shiyo 799", None),
         ("Shiyo 800", "Eiichiro's 13th memorial; Chigaya succeeds as witch")]
_H143 = {"max_size": 18, "mask_color": [0, 140, 0, 140, 0, 140]}
# IMAGES8-FIX 1 (2026-10-02): the last row is ONE line whose box ends at the ruled line's right end (x 506, 368 px
# from x 138). None of the three ruled wordings fits at the 18 px of the other rows (Ink Free: 459 / 395 / 403 px);
# wording 2 is set at 16 px = the size the "Shiyo 760" row gets (351 px). QIMAGES8-04.
_LAST143 = {"max_size": 16, "box_x1": 506}
L143 = []
for _i, (_yr, _tx) in enumerate(_T143):
    _t, _b = _RU143[_i] + 3, _RU143[_i + 1]
    if _yr is None:
        L143.append((_tx, [12, _t, 512, _b], dict(_H143)))
        continue
    L143.append((_yr, [12, _t, 132, _b], dict(_H143)))
    if _tx:
        if _i == len(_T143) - 1:
            L143.append((_tx, [138, _t, _LAST143["box_x1"], _b],
                         dict(_H143, line_spacing=0.9, max_size=_LAST143["max_size"],
                              erase=[[138, _t, 512, _b]])))  # erase area unchanged
        else:
            L143.append((_tx, [138, _t, 512, _b], dict(_H143, line_spacing=0.9)))
for _y0, _y1, _tx in ((415, 433, "· Except for Kikyo-san, they died in April"),
                      (442, 460, "· From Shiyo 740, suicides run rampant"),
                      (468, 487, "· Sakura-san's unnatural body"),
                      (496, 513, "· Did Sakura-san die of April sickness?")):
    L143.append((_tx, [18, _y0 - 3, 512, _y1 + 3], dict(_H143)))

# ---- 33 / 158 書簡 letters, two paper faces each (letter() of the 書簡 block). 33: text area x 22-624 (the bear art
# from x 637 is kept); 158: x 20-922.
L33 = ("Today the settlement suffered severe damage. Fortunately no one died, but the houses in particular were badly "
       "destroyed. I recognize that green-eyed bear. It is the cub that was beside a mother bear I hunted some years "
       "ago. I still remember that the cub was green-eyed in one eye only. The green-eyed bear has grown up and come to "
       "take revenge on this settlement. The beasts of this land are huge to begin with. Attacked by such a beast, we "
       "can only be destroyed, helpless. Somehow we managed to drive it off with fire, but when will that green-eyed "
       "bear appear again? From now on, bears should be hunted together with their cubs: tomorrow I will propose "
       "this to everyone.")
L158 = ("It was supposed to be a long journey with no destination. But sooner than we expected, we found a new land "
        "where we could put down roots. In this land, cherry trees that can make the same medicine as in Arata were "
        "growing wild, though few. On the shore of this great lake, we should have no trouble living, either. I "
        "understand the argument of the Grand Witches who stayed in Arata, too. But are those who doubt the medicine "
        "without firm proof not the same as the witch hunts spoken of in the Western countries? Yes, we believe based "
        "on our own justice. That said, one cannot help thinking, more than a little, that perhaps the Grand Witches "
        "were right after all. Thoughts like this may split us, now so few, even further apart. I have one good idea. "
        "Lord Ginosuke was originally from a Western country, and he left us the teachings of Cerejeira. That "
        "doctrine remains in the Arata settlement too. If we make this medicine a sacred implement and further found "
        "a religion that worships the cherry trees that can make the medicine, a sense of fellowship will grow, and we "
        "will be bound by stronger bonds of trust. What shall we name the religion?")
_L33 = letter(L33, 22, 624, 2)
_L158 = letter(L158, 20, 922, 2)

# ---- 109 occult magazine spread (800x568, red print on white; Occult Magazine 'M', July Shiyo 747 issue) + close-ups
# 1-3 (typeset at their own scale from this layout, zoom_lines) + 部分拡大4 (the left-page vertical title alone).
# Vertical JP columns -> horizontal English blocks in the column area (ref23 way); the narrow two/three-column
# strips and the headings are set rotated (-90, reads top-down) like the newspaper headlines.
_B109 = {"mask_color": [100, 255, 0, 225, 0, 225], "max_size": 10}
_HD109 = {"mask_color": [100, 255, 0, 225, 0, 225], "color": "#a83030"}
M109_R1 = ("We already reported on the Motoki-cho researcher slaughter case in last month's issue, but we have obtained a "
           "rumor that could be its basis. Ever since that cherry tree appeared, mysterious phenomena have been "
           "occurring in Motoki-cho, Sawa Prefecture. It is a being called Motokizakura-sama, which could be taken for "
           "a spirit or for a yokai. Though it bears the name Motokizakura-sama, it is said to appear before the "
           "people of Motoki-cho regardless of the season and to bring happiness. However, how could such a being be "
           "tied to a slaughter case?")
M109_R2 = ("We arrived at an unknown rumor. According to witnesses, Motokizakura-sama at first glance cannot be told apart "
           "from an ordinary human, but the testimony agrees that it is a young woman wearing a kimono with a "
           "cherry-blossom pattern. Furthermore, there are also stories of it being seen in separate places at the same "
           "time, and it is said that there is not just one, but countless of them in the same form. If you can meet "
           "Motokizakura-sama, you will apparently be blessed with sudden good fortune. However, the world is not all "
           "good things. Behind it, it is said, a frightening face is hidden.")
M109_L1 = ("To give the conclusion, this being called Motokizakura-sama seems to be quite troublesome. While it brings "
           "good fortune to those who happen to meet it, there are, it is said, also Motokizakura-sama who on rare "
           "occasions bring death. Motokizakura-sama is also said to be an offshoot of that cherry tree, and whoever "
           "carelessly touches or searches for it will be bewitched by Motokizakura-sama and taste eternal suffering. "
           "There is a case like this.")
M109_L2A = "That cherry tree has an uncanny nature, but there are also people drawn"
M109_L2B = ("to its mystique. It seems some people, hoping to share in its luck, took part of it home. A woman then aged 78 "
            "broke the cherry tree and took it home. But that night, a woman wearing a cherry-blossom-pattern kimono "
            "stood by the old woman's pillow and whispered in her ear, \"My friend.\" A few days after the old woman "
            "stopped being seen, a neighbor visited her house and found she had already passed away.")
M109_L3A = ("Twin sisters, then 10 years old, were climbing and playing in that cherry tree when a woman wearing a "
            "cherry-blossom-pattern kimono")
M109_L3B = ("appeared and invited the sisters, \"Let's play together.\" The two gladly agreed, and the three played until "
            "the sun went down. Meanwhile, when their mother, worried that the sisters never came home, came to the "
            "cherry tree, the two were found hanging by their necks from its branches.")
M109_L4 = ("Indeed, eerie rumors about that cherry tree never seem to stop. Those who carelessly approach it are cursed to "
           "death, and it is said that the one protecting the cherry tree's secret is Motokizakura-sama. If so, that "
           "slaughter case too can be thought of as the work of Motokizakura-sama. Some of you readers must think it "
           "ridiculous that such an uncanny being could be the culprit. But please think")
M109_L5 = ("about it carefully. A cherry tree suddenly appearing is in itself a bizarre enough phenomenon. It would be no "
           "wonder if the series of mysterious deaths were the work of the uncanny. We will thoroughly expose the "
           "secret of this Motokizakura-sama.")
T109 = "Uncanny! Motokizakura-sama\nThe True Face of the Cherry Curse?"
BIG109 = "Where one falls, darkness lies."
_TAPE = {"method": "inpaint", "color": "#b01818", "mask_color": [120, 255, 0, 150, 0, 150]}
TAPE109 = "NO ENTRY  Please do not enter  NO ENTRY"   # two spaces between phrases = 2 NBSP (typeset_ui.wrap strips a trailing NBSP and collapses plain double spaces)
L109 = [
    ("This Month's Emergency Scoop Special", [432, 22, 768, 57],
     dict(_HD109, align="center", max_size=24, erase=[[436, 24, 764, 55]])),
    (T109, [712, 102, 781, 378], dict(_HD109, rot=-90, align="center", max_size=24, color="#9c2020", no_rules=True,
                                      erase=[[714, 102, 779, 376]])),
    (M109_R1, [440, 287, 685, 411], dict(_B109)),
    (M109_R2, [534, 418, 780, 541], dict(_B109)),
    # IMAGES8-FIX 2 (2026-10-02): ONE run along the tape (was 3 overlapping pieces, all rendered at 6 px): 6 px, rot 13,
    # starting at the tape's left end = the photo's left edge (x 414) on the line through the former "NO ENTRY" centre
    # (y 483.9 there). Run 105 px <= tape 112.9 px along 13 deg (x 414..524): nothing dropped. The box is centred on the
    # run's centre (465, 472) with diagonal 108.7 >= 105 (the rot branch centres the text in the box). The double spaces
    # are 2 NBSP (see TAPE109). The three former erase boxes are kept. Close-up 1 (zoom 1.54): 9 px, 162 px run,
    # starts at x 8.6 (photo left edge x 9), tape 174.5 px: nothing dropped there either.
    (TAPE109, [412, 460, 518, 484], dict(_TAPE, rot=13, rot_h=9, max_size=6,
                                         erase=[[421, 472, 454, 486], [453, 467, 477, 478], [476, 464, 490, 475],
                                                [489, 459, 520, 471]])),
    (BIG109, [32, 32, 76, 440], dict(_HD109, rot=-90, align="center", max_size=32, color="#940f0f", no_rules=True,
                                     mask_color=[100, 255, 0, 200, 0, 200], erase=[[33, 33, 75, 438]])),
    (M109_L1, [188, 20, 380, 143], dict(_B109)),
    ("The Old Woman Who\nBroke the Cherry Tree", [140, 20, 175, 140],
     dict(_HD109, rot=-90, max_size=14, erase=[[140, 21, 175, 140]])),
    (M109_L2A, [100, 20, 129, 140], dict(_B109, rot=-90, erase=[[100, 21, 129, 140]])),
    (M109_L2B, [200, 152, 380, 276], dict(_B109)),
    ("The Tragedy That Befell\nthe Twin Sisters", [151, 152, 188, 272],
     dict(_HD109, rot=-90, max_size=14, erase=[[151, 153, 188, 272]])),
    (M109_L3A, [101, 152, 141, 274], dict(_B109, rot=-90, erase=[[101, 153, 141, 274]])),
    (M109_L3B, [265, 285, 380, 409], dict(_B109)),
    # IMAGES8-FIX 3 (2026-10-02): right edge = the JP left column's right edge (last ink x 262 of the indented first
    # column of this paragraph, x 253-262; the right column's JP starts at x 266), measured with
    # work/images/_c/fix8/m109cols.py. The engine re-breaks and steps the size down from max_size until it fits.
    # QIMAGES8-05 ruling (2026-10-02): page text box x1 = 258 (7 px gutter; engine 8 px, 9 lines). The erase box stays
    # at x1 263 so the whole JP column is still erased (and close-up 3's mapped erase box is unchanged).
    (M109_L4, [99, 285, 258, 409], dict(_B109, erase=[[99, 285, 263, 409]])),
    (M109_L5, [277, 418, 380, 541], dict(_B109)),
]
Z109 = [(1, 1.54, 408, 284, 582, 400), (2, 1.51, 93, 13, 438, 400), (3, 1.57, 82, 284, 471, 400)]
_Z109 = zoom_items(109, L109, Z109)
# IMAGES8-FIX 3: close-up 3's left column right edge = its JP left column's right edge, measured on 部分拡大3 (last ink
# x 283 of the indented column x 269-283) -> box x1 284 (the zoom mapping gives the same 284).
for _k, _e in enumerate(_Z109[2][2]["lines"]):
    if _e[0] == M109_L4:
        _Z109[2][2]["lines"][_k] = (_e[0], [_e[1][0], _e[1][1], 284, _e[1][3]], _e[2])
# close-up 1 shows only the lower ends of the boxed title columns (the box is cut by the crop top).
# IMAGES8-FIX 4 (2026-10-02): the strip is no longer typeset here. work/images/_c/paste8.py z109 pastes the English
# page's title box, scaled by the close-up's zoom factor (169.54 / 110.34 = 1.5365, from the tape photo widths), into
# the source close-up and writes the out PNG; item 1 is chained on that PNG and sets every other string, without the
# title's erase-only box (it would erase the pasted English). ORDER: ref109 -> paste8.py z109 -> ref109-zoom.
_n, _s, _ox, _oy, _w, _h = Z109[0]
_Z109[0][2]["lines"] = zoom_lines([e for e in L109 if e[0] != T109], _ox, _oy, _s, _w, _h)
_Z109[0][2]["chain"] = True
_Z109.append((D + "rrr109/部分拡大4.gal", "", {"lines": [
    (BIG109, [3, 4, 43, 396], dict(_HD109, rot=-90, align="center", max_size=34, color="#940f0f",
                                   mask_color=[100, 255, 0, 200, 0, 200], erase=[[0, 0, 46, 400]]))]}))

JOBS += [
    {"id": "ref142", "screen": "reference 142 detail", "style": "serif", "mode": "lines", "erase": "texfill",
     "erase_first": True, "mask_grow": 3, "color": "#231300", "new": True,
     "note": "residents' register on parchment (3 panels; red = death lines)", "items": [(D + "rrr142/0.gal", "")],
     "lines": L142},
    {"id": "ref143", "screen": "reference 143 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#222222", "new": True,
     "note": "handwritten timeline on ruled paper (arrows kept)", "items": [(D + "rrr143/0.gal", "")], "lines": L143},
    {"id": "ref33-letter", "screen": "reference 33 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy letter, both paper faces (English blocks right to left; bear art kept)",
     "items": [(D + "rrr33/0.gal", ""), (D + "rrr33/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L33]},
    {"id": "ref158-letter", "screen": "reference 158 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy letter, both paper faces (English blocks right to left)",
     "items": [(D + "rrr158/0.gal", ""), (D + "rrr158/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L158]},
    {"id": "ref109", "screen": "reference 109 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 2, "color": "#a82c2c", "line_spacing": 1.05, "new": True,
     "note": "occult magazine spread (tree art and photos kept)", "items": [(D + "rrr109/0.gal", "")], "lines": L109},
    {"id": "ref109-zoom", "screen": "reference 109 close-ups", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#a82c2c", "line_spacing": 1.05,
     "note": "magazine close-ups (same English as the page, own scale)", "items": _Z109, "lines": []},
    {"id": "ov-109", "screen": "reference screen preview", "style": "serif", "mode": "lines", "erase": "maskfill",
     "mask_grow": 2, "color": "#a83030", "new": True,
     "note": "magazine 概要 (not a crop of the detail: typeset in place)", "items": [(O + "rr109.gal", "")],
     "lines": [("This Month's Emergency Scoop Special", [26, 24, 278, 50],
                dict(_HD109, align="center", max_size=18, erase=[[28, 25, 276, 49]])),
               # IMAGES8-FIX 5 (2026-10-02): the page's two-line vertical title at the JP 怪 glyph height (16 px: ink
               # rows 75-90 of the source rr109, work/images/_c/fix8/m109ov.py), top-aligned at y 75 (the JP first
               # glyph's top), line 1 nearest the box's right edge (rot -90). The box runs past the picture's bottom
               # (y 323 = 75 + the longer line's 246 px + 2) so the engine keeps 16 px; the picture edge clips the
               # columns as the JP is clipped. Erase area unchanged.
               (T109, [233, 75, 287, 323], dict(_HD109, rot=-90, max_size=16, color="#9c2020",
                                                erase=[[233, 70, 287, 170]]))]},
    {"id": "ov-114", "screen": "reference screen preview", "style": "gothic", "mode": "lines", "erase": "inpaint",
     "mask_grow": 2, "color": "#eeeeee", "new": True,
     "note": "security-camera still (概要 only; CAM04 and the time stamp kept)", "items": [(O + "rr114.gal", "")],
     "lines": [("Escalator Area", [192, 153, 297, 168], {"mask_color": [150, 255, 150, 255, 150, 255], "max_size": 10,
                                                         "align": "left", "erase": [[193, 154, 296, 168]]})]},
    {"id": "ov-p8", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (142, 143, 158)]},
]



# ---- IMAGES9 2026-10-02 (notes/IMAGES9-BRIEF.md): object / letter references unlocked in part 9 (122 141 101 118 119).
# Boxes measured on the sources with work/images/_c/img9/rows9.py, gaps9.py and lines9.py. The 60x30 thumbnails are
# below legibility: skipped. Scope B 概要 (233 234 121 125 126 129 130 120 124): no text, no job (rr124: a blurred
# station sign, QIMAGES9-02). rr118 概要 and rrr118/0 (the photo face) carry no text. rrr118 0→1 / 1→0 (8-frame turn
# animations) are not shipped: QIMAGES9-01.

# ---- 122 missing-person poster (800x1135, dark crumpled paper with burn holes): texfill per line; the title by its
# red, the rest by the near-black ink inside tight boxes (the holes are as dark as the ink: boxes kept off them).
_R122 = {"mask_color": [20, 255, 0, 14, 0, 14], "color": "#4a0303"}
_K122 = {"mask_color": [0, 30, 0, 24, 0, 16], "color": "#0c0600"}
L122 = [
    ("We Are Searching for\na Missing Person!", [45, 58, 755, 300],
     dict(_R122, max_size=92, align="center", line_spacing=1.0, erase=[[80, 60, 724, 168], [46, 192, 716, 300]])),
    ("Name: Erina Goto", [382, 381, 785, 408], dict(_K122, max_size=22, erase=[[380, 381, 612, 408]])),
    ("Sex: Female", [382, 410, 785, 437], dict(_K122, max_size=22, erase=[[380, 410, 482, 437]])),
    ("Age: 15 (first year of high school)", [382, 440, 785, 467], dict(_K122, max_size=22, erase=[[380, 440, 660, 467]])),
    ("Height: 140 cm", [382, 470, 785, 497], dict(_K122, max_size=22, erase=[[380, 470, 525, 497]])),
    ("Hairstyle: Long, wavy hair", [382, 499, 785, 527], dict(_K122, max_size=22, erase=[[380, 499, 680, 527]])),
    ("Clothing: Unknown (in daily life, she prefers to wear skirts)", [382, 529, 785, 587],
     dict(_K122, max_size=22, line_spacing=1.2, erase=[[380, 529, 730, 556], [380, 559, 618, 587]])),
    ("Her whereabouts have been unknown since Shiyo 800, August 1.", [78, 764, 770, 791],
     dict(_K122, max_size=22, erase=[[78, 764, 712, 791]])),
    ("Any information, however small, is welcome.", [78, 793, 770, 821],
     dict(_K122, max_size=22, erase=[[78, 793, 460, 821]])),
    ("Please send information to us here.", [78, 823, 770, 851], dict(_K122, max_size=22, erase=[[78, 823, 462, 851]])),
    ("Contact: Goto", [78, 914, 300, 952], dict(_K122, max_size=28, erase=[[78, 914, 280, 952]])),
    ("Phone No.:", [78, 954, 242, 989], dict(_K122, max_size=28, erase=[[78, 954, 240, 989]])),
    ("Address:", [78, 991, 242, 1028], dict(_K122, max_size=28, erase=[[78, 991, 238, 1028]])),
]

# ---- 141 fan-club web page (800x4110, flat peach #fbd2b4): handles and bodies of 28 posts (post 0020 is dots only),
# 4 photo captions (box from the caption's left edge to x 792, down to the chart's top), 4 radar charts (labels on
# white). The time stamps and the 0001. numbers are Latin and stay. Body boxes run down to 6 px above the next header
# so a longer English body may take one more line.
_B141 = {"mask_color": [0, 130, 0, 130, 0, 130], "bg": "#fbd2b4", "max_size": 17, "color": "#1a1a1a"}
_HAN141 = {"kanrinin": "Admin", "oz": "Oz", "isedai": "Isedai", "kumo": "Kumo", "zabuton": "Zabuton"}
_H141 = [(192, 209, "kanrinin"), (336, 352, "oz"), (432, 447, "isedai"), (527, 544, "kanrinin"), (623, 639, "kanrinin"),
         (1006, 1022, "kumo"), (1102, 1118, "oz"), (1174, 1190, "kumo"), (1269, 1286, "kanrinin"), (1748, 1764, "kumo"),
         (1843, 1860, "zabuton"), (1940, 1955, "isedai"), (2011, 2028, "kanrinin"), (2514, 2530, "kumo"),
         (2586, 2602, "isedai"), (2681, 2698, "zabuton"), (2753, 2770, "kumo"), (2825, 2842, "kanrinin"),
         (2897, 2913, "kumo"), (2968, 2985, "kanrinin"), (3447, 3464, "kumo"), (3519, 3536, "zabuton"),
         (3591, 3607, "isedai"), (3663, 3680, "oz"), (3735, 3751, "kanrinin"), (3855, 3870, "isedai"),
         (3926, 3942, "kumo"), (4022, 4038, "zabuton")]
_T141 = [  # (box, English): bodies [8, first line top - 3, 792, next header top - 6]; captions down to the chart top
    ([8, 213, 792, 330], "Happy New Year, you Motoki-cho lolicons.\nHere's the cosplay report from the other day's "
                         "Comiket that I announced a while back!\nJust so you know, since this is Comiket cosplay, "
                         "there are zero little girls.\nIf that's fine with you, have a look."),
    ([8, 356, 792, 426], "Happy New Year, lolicons.\nThis is about the only time this place gets lively without "
                         "little girls"),
    ([8, 452, 792, 521], "Happy New Year.\nToo bad there are no pretty girls, but well, it's fine once in a while"),
    ([8, 548, 792, 617], "Oh, the regulars are showing up already.\nNot many people here yet, but I'll start "
                         "posting right away"),
    ([262, 673, 792, 794], "First one. The Santa cosplay that's a winter staple. An orthodox cosplay, but her face "
                           "and figure are both flawless. She's bundled up, so her body lines are hard to make out, "
                           "but the absolute territory woven by the miniskirt and knee socks really got to me."),
    ([8, 1027, 792, 1096], "HNY, and right off the bat, you can't even see the socks!\nAbsolute territory only has "
                           "value because you can see the skirt and the socks; no socks is a no-go"),
    ([8, 1122, 792, 1168], "Complaining right away. Kumo-shi is an absolute-territory believer this year too"),
    ([8, 1194, 792, 1263], "Obviously. And this woman's wearing stockings, too. Where are the bare legs? Give her a "
                           "0 for quality, you crap admin"),
    ([262, 1301, 792, 1539], "HNY, Kumo-shi. One more photo that might drive Kumo-shi crazy. A cosplay from 'Slave "
                             "Academy ~Uniform of Fury~', said to be the best anime of last fall. Not of any "
                             "particular character, but of the female-student uniforms, the highest quality was this "
                             "Pipin-san. Pipin-san shot to fame in the summer by taking on a daring swimsuit, but "
                             "this works too. Why the socks aren't in the shot: a crowd of camera guys had her feet "
                             "surrounded, trying to shoot up her skirt. Kumo-shi, you don't want to see camera guys "
                             "like the damned either, right?"),
    ([8, 1769, 795, 1837], "What the heck, if there was a reason like that, say so sooner. Admin, you really had it "
                           "rough. Well, this kind of thing is the privilege of whoever went there"),
    ([8, 1864, 792, 1934], "HNY, you lot.\nForget absolute territory, where are the boobs?"),
    ([8, 1960, 792, 2005], "Pretty girls! Pretty girls!"),
    ([320, 2042, 792, 2280], "Noisy hyenas, first thing in the new year. Number three. This is a cosplay of the main "
                             "character of 'China China', an anime that was popular three years ago. She's an "
                             "unknown, but her figure and her smile were both very good. The camera guys had gone "
                             "off to other cosplayers, so her spot was empty, and I even got to talk with her a "
                             "little. Believe it or not, she apparently has a daughter, and her dream is to cosplay "
                             "together, mother and daughter. She handled things like a grown-up and left a very good "
                             "impression. A cosplayer I want to cheer on personally."),
    ([8, 2535, 792, 2580], "Hey Admin, why didn't you get the daughter in the shot, you useless"),
    ([8, 2606, 792, 2675], "If cosplaying as parent and child is her dream, that means the daughter doesn't "
                           "cosplay\nI won't stand for anyone photographing the daughter without permission"),
    ([8, 2702, 792, 2747], "Kumo-shi wanting to take creep shots, seriously the worst"),
    ([8, 2774, 792, 2819], "Sorry, I went too far"),
    ([8, 2846, 792, 2891], "Kumo-shi's keyboard-warrior act is funny as always lol"),
    ([8, 2918, 792, 2962], "Never mind that, hurry up and post the next one, you trash"),
    ([345, 3004, 792, 3196], "This time's scoop cosplay! An old-hag cosplayer, probably around seventy. A cosplay of "
                             "Makoto Amachi, the main character of that god-tier anime 'Fascination'. I think it's "
                             "the ballerina-style costume from episode five. Very high quality, and a wonderful "
                             "figure that doesn't show her age. Probably the best figure of all the cosplayers. But "
                             "she's just too old, no matter what. Even your Admin was put off by this one, as you'd "
                             "expect."),
    # the JP caption's second paragraph (2 lines from y 3198) gets its own box (explicit line breaks never wrap)
    ([345, 3196, 792, 3250], "But the young woman with her was outrageously beautiful, and the camera guys were all "
                             "facing her."),
    ([8, 3540, 792, 3585], "Kumo-shi, no need to go out of your way to post that lololol"),
    ([8, 3612, 792, 3657], "Honestly, this one's rough"),
    ([8, 3683, 792, 3729], "I'm gonna have a bad first dream of the year. Admin, take responsibility"),
    ([8, 3756, 792, 3849], "And sorry, but that's it for now.\nI'm off to the New Year's shrine visit with my husband "
                           "and daughter.\nSo long, lolicons!"),
    ([8, 3876, 792, 3920], "Have a good one"),
    ([8, 3947, 792, 4016], "I forget sometimes, but Admin's actually a married woman with a kid, huh\nAnd she "
                           "apparently used to be a magazine model"),
    ([8, 4042, 792, 4085], "She said that back in her model days, her work gave her lots of chances to meet cute "
                           "little girls, and that's how she woke up to loli"),
]
_C141 = [  # radar-chart labels (JP boxes): face top, manners left, figure right, gallery / quality below; chart left x
    ([367, 806, 379, 819], [278, 865, 304, 877], [440, 865, 491, 877], [268, 942, 331, 955], [415, 942, 473, 955], 260),
    ([368, 1549, 381, 1562], [280, 1608, 306, 1620], [442, 1608, 493, 1620], [269, 1685, 332, 1697],
     [416, 1685, 475, 1698], 260),
    ([462, 2294, 474, 2307], [373, 2353, 401, 2366], [535, 2353, 586, 2366], [364, 2431, 427, 2443],
     [511, 2431, 568, 2443], 347),
    ([441, 3266, 453, 3279], [352, 3324, 379, 3337], [514, 3325, 565, 3337], [341, 3402, 405, 3414],
     [489, 3402, 548, 3414], 337),
]
_L141C = {"mask_color": [0, 160, 0, 160, 0, 160], "bg": "#ffffff", "max_size": 12, "color": "#404040"}
L141 = [
    ("Motoki Bishojo Appreciation Society", [20, 36, 780, 108],
     {"style": "rounded", "method": "inpaint", "mask_color": [0, 150, 130, 235, 170, 255], "color": "#29a7e6",
      "max_size": 56, "align": "center", "erase": [[136, 38, 666, 106]]}),
    ("Cosplay Report Special Page", [20, 112, 780, 160],
     {"style": "rounded", "method": "inpaint", "mask_color": [0, 150, 130, 235, 170, 255], "color": "#43afda",
      "max_size": 38, "align": "center", "erase": [[143, 112, 661, 158]]}),
]
for _y0, _y1, _h in _H141:
    L141.append((_HAN141[_h], [240, _y0 - 3, 460, _y1 + 3], dict(_B141, erase=[[238, _y0 - 2, 320, _y1 + 3]])))
for _bx, _tx in _T141:
    L141.append((_tx, _bx, dict(_B141, line_spacing=1.12)))
for _fa, _ma, _fi, _ga, _qu, _left in _C141:
    _cx = (_fa[0] + _fa[2]) // 2
    L141 += [("Face", [_cx - 25, _fa[1] - 1, _cx + 25, _fa[3] + 1], dict(_L141C, align="center", erase=[_fa])),
             ("Manners", [max(_left, _ma[2] - 52), _ma[1] - 1, _ma[2] + 1, _ma[3] + 1],
              dict(_L141C, align="right", erase=[_ma])),
             ("Figure", [_fi[0], _fi[1] - 1, _fi[0] + 60, _fi[3] + 1], dict(_L141C, align="left", erase=[_fi])),
             ("Gallery", [_ga[0], _ga[1] - 1, _ga[2], _ga[3] + 1], dict(_L141C, align="center", erase=[_ga])),
             ("Quality", [_qu[0], _qu[1] - 1, _qu[2], _qu[3] + 1], dict(_L141C, align="center", erase=[_qu]))]

# ---- 101 書簡 diary page, two paper faces (letter() of the 書簡 block): text area x 566-1333 (the two drawn figures end
# at x 554 on face 1); face 1 texfill as the 33 / 158 letters.
L101 = ("Would you believe in the existence of demons? No, until a little while ago, I did not believe in them. The "
        "reason my feelings changed like this is that I went to the mountain where demons dwell. Demons have human "
        "form, yet they have no arms or legs, and they go on living even with their entrails hanging out of their "
        "bellies. And they kill one another with movements that seem not human. They also speak human language, but "
        "without any real conversation, the demon I met died. At the time, I had ten attendants with me. Of course "
        "they saw the demons too, but now I alone know of this. For on His Highness's orders, the attendants were "
        "killed, every last one. But now that same Highness is himself on the verge of death. Having lost the power "
        "of the demon warriors and fallen into despair, His Highness no longer has even the will to live.")
_L101 = letter(L101, 566, 1333, 2)

# ---- 118 entrance-ceremony photo: face 1 (the back of the photo, 444x300) = two handwritten lines; the date keeps its
# format with Latin digits. Face 0 is the photo (no text).
L118 = [
    ("Shiyo 764/4/6", [248, 226, 440, 250], {"max_size": 18, "align": "left", "erase": [[244, 226, 358, 250]]}),
    ("Mifuyu and Akane-chan's entrance ceremony", [170, 250, 440, 296],
     {"max_size": 18, "align": "left", "line_spacing": 1.05, "erase": [[217, 250, 438, 274]]}),
]

# ---- 119 cafe receipt (700x387, white form, light-blue header band): the Latin parts (No., the amount, Primavera,
# the stamp, the post code and the phone number) and the 〒 / ☎ marks stay.
_K119 = {"mask_color": [0, 170, 0, 170, 0, 170], "bg": "#ffffff", "color": "#262626"}
L119 = [
    ("Receipt", [17, 12, 300, 62], {"method": "inpaint", "mask_color": [0, 150, 0, 150, 0, 150], "max_size": 42,
                                     "align": "left", "color": "#262626", "erase": [[16, 13, 160, 61]]}),
    ("Valued Customer", [34, 82, 332, 119],
     dict(_K119, max_size=22, align="center", erase=[[137, 80, 162, 119], [297, 80, 330, 119]])),
    ("Shiyo 800, March 25", [372, 82, 692, 119], dict(_K119, max_size=22, align="center", erase=[[374, 80, 690, 119]])),
    ("Amount", [52, 148, 127, 170], dict(_K119, max_size=14, align="center", erase=[[72, 150, 100, 168]])),
    ("For:", [252, 220, 306, 247], dict(_K119, max_size=15, align="right", erase=[[271, 219, 289, 247]])),
    ("Meal charge", [312, 216, 590, 249], dict(_K119, style="handwriting", max_size=26, align="left", color="#1e1e1e",
                                               erase=[[311, 216, 490, 249]])),
    ("Received the above sum with thanks.", [288, 256, 590, 274],
     dict(_K119, max_size=13, align="left", erase=[[289, 256, 444, 274]])),
    ("Incl. consumption tax", [47, 273, 244, 292], dict(_K119, max_size=13, align="left", erase=[[47, 274, 120, 291]])),
    ("Amount excl. tax", [47, 307, 244, 325], dict(_K119, max_size=13, align="left", erase=[[48, 309, 107, 324]])),
    ("Cash / Card", [47, 341, 244, 359], dict(_K119, max_size=13, align="left", erase=[[47, 343, 134, 358]])),
    ("Coffee Lounge Primavera, Hamaoka Branch", [316, 323, 640, 339],
     dict(_K119, max_size=12, align="left", erase=[[316, 323, 532, 339]])),
    ("2-5-XX Higashiokubashi, Hamaoka-ku, Tokyo", [309, 355, 660, 370],
     dict(_K119, max_size=12, align="left", erase=[[309, 355, 485, 370]])),
]

JOBS += [
    {"id": "ref122", "screen": "reference 122 detail", "style": "serif", "mode": "lines", "erase": "texfill",
     "erase_first": True, "mask_grow": 3, "color": "#0c0600", "new": True,
     "note": "missing-person poster on burnt paper (photo, holes and Latin contact data kept)",
     "items": [(D + "rrr122/0.gal", "")], "lines": L122},
    {"id": "ref141", "screen": "reference 141 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#1a1a1a", "new": True,
     "note": "fan-club web page (photos, chart shapes, post numbers and time stamps kept)",
     "items": [(D + "rrr141/0.gal", "")], "lines": L141},
    {"id": "ref101-letter", "screen": "reference 101 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy diary page, both paper faces (English blocks right to left; figure drawings kept)",
     "items": [(D + "rrr101/0.gal", ""), (D + "rrr101/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L101]},
    {"id": "ref118", "screen": "reference 118 detail", "style": "handwriting", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 3, "color": "#3c352c", "new": True,
     "note": "back of a photo, handwritten caption (face 1 only)", "items": [(D + "rrr118/1.gal", "")],
     "lines": [(t, b, dict(o, mask_color=[0, 150, 0, 150, 0, 150])) for t, b, o in L118]},
    {"id": "ref119", "screen": "reference 119 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 2, "color": "#262626", "new": True,
     "note": "cafe receipt form (amount, logo, stamp and Latin numbers kept)", "items": [(D + "rrr119/0.gal", "")],
     "lines": L119},
    {"id": "ov-p9", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (122, 141, 101, 119)]},
]


# ---- IMAGES10 2026-10-02 (notes/IMAGES10-BRIEF.md): object / letter references unlocked in part 10 (86 31 94 132 134 137).
# Boxes measured on the sources with work/images/_c/img10/rows10.py, gaps10.py, samp.py and probe94.py. The 60x30
# thumbnails are below legibility: skipped. rrr237/0 and rr237 (two photos) carry no text: no job. Scope B 概要 (131 238
# 144 133 135 136): no text, no job. Overviews 94 132 134 137 = refdoc_overview build; 86 31 = img10/paste10.py.

# ---- 86 / 31 書簡 letters, two paper faces each (letter() of the 書簡 block; face 1 texfill as 101 / 33 / 158).
L86 = ("We, the people of Arata, hold the rules as our creed. About a hundred years ago, and more than three hundred "
       "years ago as well, our ancestors forbade the use of Droga. It is not something humans should lay hands on. If "
       "it is the cause of that disaster, then we must never lay hands on it. Yet why Droga becomes the cause of "
       "disaster, we do not know. Not a few residents think it must surely be a curse, but amid the flow of this age, "
       "it is high time we cast out supernaturalism. We must find out why Droga becomes the cause of disaster. To "
       "catch up with the great powers, whose civilizations are more advanced than this country's, we too should "
       "learn the secret of Droga scientifically. Next month I will have my son take Droga and present it to the "
       "government. If the government takes an interest in this medicine, it will surely help us unravel its "
       "demon-warrior power. If we can use Droga so that it causes no disaster, the land of Arata can remain at "
       "peace.")
L31 = ("A letter like this can never reach you. I have no intention of showing this letter to anyone; I only set down "
       "my own thoughts. Kikyo-dono, how is the starry sky seen from Tokyo? I am surely looking at the same stars as "
       "Kikyo-dono. Though we are connected through the sky, here and Tokyo are far apart. I am glad I was able to "
       "meet Kikyo-dono. But more than that, it is painful. Is this what love is? What does Kikyo-dono think of me? "
       "Tomorrow I go to Tokyo again. I have been summoned by a high government official. According to Father, the "
       "government has granted what I asked of it, 'Please find a woman who will marry into Arata,' and the one who "
       "will marry that woman is me. Since it is an order from my parent, I have no choice but to accept this "
       "marriage proposal. Kikyo-dono, I want to meet you once more. I know full well that these feelings are fated "
       "to vanish like foam on water. Even so, I cannot accept the proposal until I have put my feelings in order. I "
       "do not know what kind of woman will become my wife, but for the sake of my future wife too, I must accept "
       "this fate. That I can voice nothing but such weakness makes me truly pathetic. And to begin with, I do not "
       "even know what Kikyo-dono thinks of me.")
_L86 = letter(L86, 22, 816, 2)
_L31 = letter(L31, 26, 1134, 3)

# ---- 94 blog page (800x1850): header photo (title white, subtitle red: inpaint, outline by 1-px offset copies),
# green post panel #00b050 (white text, maskfill), light-green sidebar #92d050 (black text, purple / blue links).
# Latin parts kept: the calendar digits, "<<" / ">>", the time 20:25. Comment list re-set whole (it reflows).
_P94 = {"mask_color": [25, 255, 0, 255, 0, 255], "bg": "#00b050", "method": "maskfill", "max_size": 18}
_S94 = {"mask_color": [0, 255, 0, 195, 0, 255], "bg": "#92d050", "method": "maskfill", "style": "gothic",
        "color": "#1a1a1a", "max_size": 12}
_PU94, _BL94 = "#76528e", "#2487a4"


def _p94(t, box, rows=None, **k):
    o = dict(_P94, erase=rows if rows is not None else [box]); o.update(k)
    return (t, box, o)


def _s94(t, box, er, **k):
    o = dict(_S94, erase=er); o.update(k)
    return (t, box, o)


def _outline(t, box, col, o):
    """8 copies of the string 1 px off in each direction (an outline the engine's per-job stroke cannot give)."""
    return [(t, [box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy], dict(o, color=col, erase=[]))
            for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))]


_T94 = {"style": "gothic", "max_size": 42, "align": "left"}
_U94 = {"style": "gothic", "max_size": 24, "align": "left"}
_TT94 = "A Working Teacher's Raw Blog"
_ST94 = "~Teaching is an eternal war with brats and their parents~"
L94 = [
    # header: erase only, then outline copies, then the string
    ("", [30, 106, 652, 156], {"method": "inpaint", "mask_color": [150, 255, 150, 255, 150, 255], "mask_grow": 5,
                               "erase": [[30, 106, 652, 154]]}),
    ("", [24, 153, 562, 188], {"method": "inpaint", "mask_color": [150, 255, 0, 130, 0, 130], "mask_grow": 4,
                               "erase": [[24, 153, 562, 188]]}),
    ("", [24, 153, 562, 188], {"method": "inpaint", "mask_color": [170, 255, 170, 255, 170, 255], "mask_grow": 3,
                               "erase": [[24, 153, 562, 188]]}),
] + _outline(_TT94, [30, 108, 775, 154], "#1e1e1e", _T94) + [(_TT94, [30, 108, 775, 154], dict(_T94, color="#ffffff", erase=[]))] \
  + _outline(_ST94, [26, 155, 775, 187], "#ffffff", _U94) + [(_ST94, [26, 155, 775, 187], dict(_U94, color="#ff2020", erase=[]))] + [
    # post 1
    _p94("Shiyo 800, April 6", [300, 277, 562, 300], [[396, 278, 563, 300]], style="gothic", max_size=17, align="right"),
    _p94("A Gloomy Entrance Ceremony", [36, 300, 562, 334], [[38, 301, 196, 333]], max_size=24),
    _p94("Yes, yes, hi there, everyone. It's Mochiko, a working teacher.", [36, 354, 562, 378]),
    _p94("Ugh, this day is finally coming.", [36, 377, 562, 402]),
    _p94("Today was the opening ceremony, so, well, that much is fine.", [36, 401, 562, 425]),
    _p94("The problem is tomorrow. Tomorrow.", [36, 424, 562, 448]),
    _p94("Entrance Ceremony", [40, 474, 560, 548], [[40, 476, 362, 546]], max_size=48),
    _p94("Taking on new first-years is seriously depressing.", [36, 570, 562, 595]),
    _p94("Well, I'm eternally 22, mind you, but dealing with new first-years every single time is seriously exhausting. "
         "I mean, they're brats I know nothing about, you know? Total strangers, you know? No, the students are still "
         "fine. Among them, there's always at least one student with landmine parents.",
         [36, 594, 562, 708], [[36, 594, 562, 688]]),
    _p94("But, you know, I can honestly put up with that much.", [36, 710, 562, 734]),
    _p94("I mean, every teacher goes through that, and I've been through it a few times myself. Even though I'm "
         "eternally 22.", [36, 733, 562, 801], [[36, 733, 562, 780]]),
    _p94("Into my class, you know,", [36, 803, 562, 826]),
    _p94("Genius Girl", [36, 872, 236, 926], [[36, 876, 482, 923]], max_size=40),
    _p94("is what they call the student I'm getting", [236, 897, 562, 924], [], max_size=17),
    _p94("Really, just once in a blue moon, you know, a student comes along whose head is so off you'd think they've "
         "lost their mind. They should just shut up and go to some top elite high school in the city, so why are they "
         "coming to a backwater high school like this?", [36, 993, 562, 1084], [[36, 993, 562, 1064]]),
    _p94("Those types are seriously scary.", [36, 1084, 562, 1108], [[36, 1063, 562, 1087]]),
    _p94("For example? I'm the one who writes the test questions, right?", [36, 1109, 562, 1133]),
    _p94("So, what do you think happens if the genius girl writes an answer that's different from the one I prepared?",
         [36, 1133, 562, 1179]),
    _p94("I'm too scared to mark it wrong.", [36, 1179, 562, 1203]),
    _p94("Or rather, in cases like that, we hold a little staff meeting.", [36, 1202, 562, 1270], [[36, 1202, 562, 1249]]),
    _p94("\"This genius girl gave this answer. What do you think?\"", [36, 1272, 562, 1296]),
    _p94("\"Well, can't we just call this wrong?\"", [36, 1295, 562, 1319]),
    _p94("\"But what if this is how they phrase it in English-speaking countries...\"", [36, 1318, 562, 1342]),
    _p94("That's how the conversation goes.", [36, 1365, 562, 1388]),
    _p94("Well, I'm an English teacher, so unlike math or science, there's no single absolute answer for the key.",
         [36, 1388, 562, 1456], [[36, 1388, 562, 1435]]),
    _p94("And then there's class time.", [36, 1457, 562, 1481]),
    _p94("Students like that find class pretty boring, so they study on their own, stuff unrelated to the lesson. And I "
         "can't exactly tell them off, can I? They're doing that because my class isn't enough for them, right?",
         [36, 1480, 562, 1572], [[36, 1480, 562, 1551]]),
    _p94("Ugh, I'm done. Let's stop here for today. Once I start complaining, there's no end to it.",
         [36, 1573, 562, 1638], [[36, 1573, 562, 1620]]),
    ("", [36, 1641, 570, 1668], {"method": "maskfill", "bg": "#00b050", "mask_color": [0, 20, 0, 150, 60, 255],
                                 "erase": [[36, 1641, 570, 1668]]}),
    _p94("Posted by Mochiko at 20:25", [36, 1641, 228, 1668], [[36, 1641, 570, 1668]], style="gothic", max_size=15),
    _p94("|Comments (1)|Trackbacks (0)", [230, 1641, 570, 1668], [], style="gothic", max_size=15, color="#002060"),
    # post 2 (cut by the picture's bottom edge as the JP is)
    _p94("Shiyo 800, April 5", [300, 1730, 562, 1754], [[398, 1731, 563, 1754]], style="gothic", max_size=17,
         align="right"),
    _p94("A Failed Marriage Meeting", [36, 1754, 562, 1786], [[36, 1755, 194, 1785]], max_size=24),
    _p94("It's Mochiko, and today is the end of my spring break.", [36, 1808, 562, 1832]),
    _p94("It was a precious Sunday, and it was a disaster.", [36, 1831, 562, 1850]),
    # sidebar
    _s94("Profile", [596, 268, 700, 288], [[596, 269, 665, 287]], max_size=13),
    _s94("Name: Mochiko", [596, 300, 696, 317], [[596, 300, 692, 317]]),
    _s94("Age: 22", [596, 316, 696, 332], [[596, 315, 692, 332]]),
    _s94("Location: Japan", [596, 331, 696, 347], [[596, 331, 692, 347]]),
    _s94("A blog where Mochiko, an English teacher, lets her daily complaints pour out on and on. Board of education "
         "people, please go home.", [596, 348, 780, 412], [[596, 348, 780, 410]], line_spacing=1.0),
    _s94("April 800", [628, 441, 733, 459], [[650, 441, 716, 460]], color=_PU94, align="center"),
] + [_s94(_d, [_c - 13, 466, _c + 13, 484], [[_c - 9, 467, _c + 9, 483]], max_size=11, align="center")
     for _d, _c in (("Sun", 601), ("Mon", 630), ("Tue", 657), ("Wed", 685), ("Thu", 713), ("Fri", 741), ("Sat", 768))] + [
    _s94("Recent Comments", [596, 616, 780, 634], [[596, 617, 677, 633]], max_size=13),
    _s94("", [596, 633, 779, 790], [[596, 633, 779, 790]]),
    _s94("Good job on the opening ceremony", [596, 633, 780, 647], [], max_size=11, color=_PU94),
    _s94("by Moko (800/04/06)", [596, 647, 780, 661], [], max_size=11),
    _s94("There are plenty of men out there", [596, 662, 780, 676], [], max_size=11, color=_PU94),
    _s94("by Hiromi (800/04/05)", [596, 676, 780, 690], [], max_size=11),
    _s94("Let's switch gears", [596, 691, 780, 705], [], max_size=11, color=_PU94),
    _s94("by FUNK (800/04/05)", [596, 705, 780, 719], [], max_size=11),
    _s94("I'm a teacher too. If you're in the Tokyo area, drinks...", [596, 720, 780, 748], [], max_size=11,
         color=_PU94, line_spacing=1.0),
    _s94("by YOU (800/04/05)", [596, 748, 780, 762], [], max_size=11),
    _s94("Are there many cherry trees there?", [596, 763, 780, 777], [], max_size=11, color=_PU94),
    _s94("by Rik (800/04/05)", [596, 777, 780, 791], [], max_size=11),
    _s94("See older comments", [596, 801, 780, 821], [[596, 802, 742, 820]], max_size=13, color=_BL94),
    _s94("Categories", [596, 843, 700, 861], [[596, 844, 642, 860]]),
] + [_s94(_t, [596, _y0 - 3, 720, _y1 + 3], [[596, _y0 - 2, _x1 + 2, _y1 + 2]], color=_BL94)
     for _t, _x1, _y0, _y1 in (("Rants (886)", 651, 862, 875), ("Days Off (45)", 645, 878, 891), ("Meals (2)", 636, 893, 906),
                               ("Diary (0)", 638, 909, 921), ("Other (0)", 650, 924, 937))]

# ---- 132 Goto's memo 10 (800x2163, white): memo() rows from rows10.py (pitch 24.5). The JP symbols ● ・ → ↓ stay as
# drawn (Ink Free has none of them): symbol lines are erased and set from x 26 / 28. Multi-line paragraphs = one
# wrapped box over their JP rows. The kaomoji after the big closing line stays.
def _m132(t, box, er=None, **k):
    o = {"max_size": 18, "erase": er if er is not None else [[box[0], box[1] + 1, box[2], box[3] - 1]]}
    o.update(k)
    return (t, box, o)


L132 = [
    _m132("So, what was it that Kogori-senpai saw...!", [7, 4, 796, 31], [[7, 5, 396, 30]]),
    _m132("The vision Kogori-senpai saw", [29, 53, 796, 82], [[28, 54, 219, 80]]),
    _m132("She saw it during her call with me ('saw', not 'heard'?)", [27, 79, 796, 106], [[26, 79, 619, 106]]),
    _m132("She saw someone who seemed to be Sakura-san and someone who seemed to be Kotaro-san", [27, 104, 796, 129],
          [[26, 104, 505, 129]]),
    _m132("A jar? A tripod?", [27, 129, 796, 153], [[26, 129, 152, 153]]),
    _m132("Someone who seemed to be Sakura-san was covered in blood", [27, 154, 796, 178], [[26, 154, 320, 178]]),
    _m132("It seems more like the past than a premonition", [27, 179, 796, 203], [[26, 179, 319, 202]]),
    _m132("Shirozaki-san's story", [29, 227, 796, 253], [[28, 228, 157, 253]]),
    _m132("There was an oracle", [6, 252, 796, 277], [[6, 253, 154, 276]]),
    _m132("The culprit of the curse-killings will hide in the storage shed at Arata Station", [27, 277, 796, 302],
          [[26, 277, 402, 302]]),
    _m132("Considering what happened to the Kogoris, it doesn't seem like a coincidence. Did someone try to kill the "
          "Kogoris? If so, there was a chance the settlement's residents would attack whoever was in the storage shed.",
          [30, 300, 796, 377], [[29, 301, 794, 327], [6, 326, 794, 352], [6, 354, 40, 376]]),
    _m132("Oracles are apparently absolute information (made known by a being called the witch)", [27, 375, 796, 401],
          [[26, 375, 640, 400]]),
    _m132("In other words, defying one would stir up the residents' distrust, and there's no telling what they'd do to "
          "you. But since when has the witch been giving oracles like that? In the end, the oracles haven't prevented "
          "the curse-killings... No, wait, if an oracle saying 'Kill so-and-so' is what the curse-killing is, would "
          "that hold up? But that's weird too! It means that even after the culprit of the curse-killings is dealt "
          "with, a culprit appears again the next year, right? That's a decisive contradiction! (Or else the "
          "residents are idiots...)",
          [30, 399, 796, 551], [[29, 400, 795, 426], [6, 426, 795, 527], [6, 527, 145, 550]]),
    _m132("B-U-T!", [8, 576, 400, 614], [[8, 578, 234, 612]], max_size=32),
    _m132("Apparently Shirozaki-san's story was all lies!...", [5, 614, 796, 642], [[5, 615, 498, 641]]),
    _m132("Well, that I can understand, but then the storage shed business becomes a coincidence.", [5, 639, 796, 667],
          [[5, 640, 597, 666]]),
    _m132("Shirozaki-san's story has lies in it, but there should be truth in it too.", [5, 664, 796, 690],
          [[5, 665, 452, 689]]),
    _m132("Seems best to start by thinking about Shirozaki-san's story.", [5, 712, 796, 738], [[5, 713, 473, 737]]),
    _m132("How much of what Shirozaki-san says is true?", [29, 762, 796, 788], [[28, 763, 503, 787]]),
    _m132("True: he knew someone would come to the storage shed", [7, 787, 796, 812], [[7, 787, 443, 811]]),
    _m132("Lie: there are oracles from the witch. That was meant to give Kogori-senpai a psychological experience",
          [7, 812, 796, 837], [[7, 812, 794, 836]]),
    _m132("In that case, there must have been someone who could 'foresee' that people would come to the storage shed.",
          [7, 862, 796, 888], [[7, 862, 640, 887]]),
    _m132("The only ones who knew about this were Chiga-nee and Mifuyu-san.", [7, 886, 796, 911], [[7, 886, 473, 910]]),
    _m132("The existence of a third person with precognition", [7, 935, 796, 961], [[7, 935, 239, 960]]),
    _m132("Kogori-senpai and Sakura-san have precognition. It wouldn't be strange if there were one more.",
          [6, 984, 796, 1010], [[6, 984, 722, 1009]]),
    _m132("In other words, that person would be the witch.", [7, 1010, 796, 1035], [[7, 1010, 688, 1035]]),
    _m132("Then who is the witch telling her foresight to? There must be someone who hears the foresight and spreads "
          "it (a receiver).", [7, 1034, 796, 1085], [[7, 1035, 796, 1059], [7, 1062, 101, 1084]]),
    _m132("In this case,", [7, 1110, 796, 1134], [[7, 1110, 102, 1134]]),
    _m132("Witch = Eiichiro Niimura (dead)", [5, 1134, 796, 1161], [[5, 1134, 247, 1160]]),
    _m132("Receiver = Kogori-senpai", [6, 1159, 796, 1184], [[6, 1160, 179, 1183]]),
    _m132("We can reuse that setup as is.", [7, 1184, 796, 1210], [[7, 1184, 307, 1209]]),
    _m132("Who is the receiver? (Thinking about it this way, does it mean Kogori-senpai doesn't have precognition, "
          "but the ability to receive foresight?)", [6, 1230, 796, 1283], [[6, 1231, 795, 1257], [5, 1259, 309, 1282]]),
    _m132("If so,", [7, 1309, 796, 1332], [[7, 1309, 101, 1331]]),
    _m132("Witch = Sakura-san (dead)", [5, 1332, 796, 1358], [[5, 1332, 247, 1357]]),
    _m132("Receiver = Kotaro-san", [6, 1357, 796, 1383], [[6, 1357, 198, 1382]]),
    _m132("is that how it goes?", [7, 1383, 796, 1406], [[7, 1383, 194, 1405]]),
    _m132("Then was Eiichiro Niimura someone with precognition (a receiver)?", [6, 1404, 796, 1431],
          [[6, 1405, 506, 1430]]),
    _m132("But from what Niimura-senpai said, it doesn't sound like that was the case...", [7, 1430, 796, 1458],
          [[7, 1431, 577, 1457]]),
    _m132("Hypothesis 1: When a receiver dies, they become the witch?", [29, 1480, 796, 1506], [[28, 1481, 411, 1505]]),
    _m132("Given the flow, this hypothesis seems right, but it's probably wrong.", [5, 1505, 796, 1530],
          [[5, 1506, 494, 1529]]),
    _m132("The reasons are as follows", [6, 1531, 796, 1556], [[6, 1531, 192, 1555]]),
    _m132("There's no proof Eiichiro Niimura was a receiver", [27, 1554, 796, 1580], [[26, 1555, 443, 1579]]),
    _m132("The Sakura-san = witch theory is Shirozaki-san's lie", [27, 1580, 796, 1606], [[26, 1581, 381, 1606]]),
    _m132("There's no proof Kotaro-san is receiving", [27, 1605, 796, 1629], [[26, 1606, 443, 1628]]),
    _m132("In other words, there's no basis at all supporting this hypothesis", [7, 1629, 796, 1657],
          [[7, 1630, 423, 1656]]),
    _m132("Hypothesis 2: Kotaro-san has precognition", [29, 1678, 796, 1705], [[28, 1679, 371, 1704]]),
    _m132("This one is hard to deny, but I can't affirm it either.", [7, 1703, 796, 1730], [[7, 1704, 452, 1729]]),
    _m132("If he does have precognition, he's completely leaving the residents to die, right?", [5, 1728, 796, 1754],
          [[5, 1728, 618, 1753]]),
    _m132("In this case, you could even say Kotaro-san is the root of everything.", [5, 1753, 796, 1778],
          [[5, 1754, 452, 1777]]),
    _m132("Hypothesis 3: Sakura-san is alive", [29, 1799, 796, 1828], [[28, 1800, 392, 1827]]),
    _m132("It's a far-fetched idea, but actually this one fits best", [5, 1828, 796, 1853], [[5, 1829, 464, 1852]]),
    _m132("The reasons:", [6, 1854, 796, 1876], [[6, 1854, 80, 1875]]),
    _m132("The body's head had been cut off -> hard to confirm who it was", [27, 1878, 796, 1905],
          [[26, 1879, 506, 1904]]),
    _m132("She's hiding somewhere and secretly telling Kotaro-san her foresight", [27, 1903, 796, 1928],
          [[26, 1904, 587, 1927]]),
    _m132("But I don't get the reason for going to the trouble of passing Sakura-san off as dead and continuing to kill "
          "the residents. If the goal is to destroy the settlement, just killing everyone at once would do.",
          [7, 1926, 796, 1978], [[7, 1927, 794, 1952], [7, 1952, 617, 1977]]),
    _m132("Hypothesis 4: Sakura-san is dead but moving around", [29, 1999, 796, 2026], [[28, 2000, 557, 2025]]),
    _m132("To keep the dead Sakura-san moving, residents' corpses are needed, and Kotaro-san is helping with that. In "
          "other words, Sakura-san has become a zombie.", [6, 2024, 796, 2075],
          [[6, 2025, 795, 2050], [5, 2051, 659, 2074]]),
    _m132("Like that could ever happen!", [8, 2079, 382, 2118], [[8, 2080, 372, 2117]], max_size=32),
    _m132("Well, just idle talk, idle talk.", [7, 2119, 796, 2140], [[7, 2119, 196, 2140]], max_size=16),
]

# ---- 134 map in an old book (800x450, mottled orange): near-black brush lettering, texfill; red X, ladder, blobs kept.
_K134 = {"mask_color": [0, 90, 0, 60, 0, 60], "max_size": 26}
L134 = [
    ("Altar", [96, 102, 216, 136], dict(_K134, align="center", erase=[[124, 102, 188, 135]])),
    ("Ritual Implements", [450, 117, 682, 151], dict(_K134, align="center", erase=[[534, 118, 596, 150]])),
    ("Seal Stone", [189, 328, 340, 362], dict(_K134, align="left", erase=[[189, 329, 249, 362]])),
    ("To Mount Itohime", [162, 413, 450, 449], dict(_K134, align="left", erase=[[164, 414, 283, 448]])),
    ("Not to be taken outside the house", [334, 289, 792, 317], dict(_K134, max_size=21, align="left",
                                                                        erase=[[334, 289, 438, 316]])),
    ("Verji shall be sealed here.", [334, 321, 792, 349], dict(_K134, max_size=21, align="left",
                                                               erase=[[334, 321, 689, 349]])),
    ("Breaking the seal is forbidden under any circumstances.", [334, 352, 792, 382],
     dict(_K134, max_size=21, align="left", erase=[[334, 352, 769, 382]])),
    ("The root of the green-eye curse-killings shall be buried forever.", [334, 383, 792, 415],
     dict(_K134, max_size=21, align="left", erase=[[333, 383, 743, 415]])),
]

# ---- 137 instructions in an old book (800x1134, orange paper with stains): faint brown brush ink, texfill; the root,
# the pot on its stand (its faded marks are illegible) and the flask drawing kept.
_K137 = {"mask_color": [0, 135, 0, 66, 0, 45], "max_size": 21}
L137 = [
    ("Making Falsificaso", [50, 40, 600, 85], dict(_K137, max_size=34, erase=[[52, 42, 362, 83]])),
    ("This records how to make the falsificaso used in funerals. Take full care with fire, odors and the like during "
     "production.", [36, 145, 772, 208], dict(_K137, line_spacing=1.3, erase=[[36, 146, 764, 174], [36, 179, 372, 207]])),
    ("1. Collect 100 monme of Arata cherry root (just under 400 grams in today's terms).", [38, 262, 790, 292],
     dict(_K137, erase=[[38, 263, 600, 292]])),
    ("2. Put the crushed Arata cherry root into the production jar.", [38, 358, 572, 388],
     dict(_K137, erase=[[38, 359, 512, 388]])),
    ("3. Pour in enough water (groundwater) to fully soak the Arata cherry root.", [38, 397, 572, 452],
     dict(_K137, line_spacing=1.2, erase=[[38, 398, 537, 424], [58, 427, 112, 451]])),
    ("4. Heat the jar for about 3 days, stirring all the while. Take care not to scorch it.", [38, 458, 572, 514],
     dict(_K137, line_spacing=1.2, erase=[[38, 459, 537, 486], [58, 490, 212, 513]])),
    ("5. Always keep the water deep enough to soak the root; add more as needed when it runs low.",
     [38, 522, 572, 581], dict(_K137, line_spacing=1.2, erase=[[38, 523, 546, 549], [58, 557, 116, 580]])),
    ("6. When a nose-stinging smell rises, stop the fire and the stirring, and leave it for 1 day.",
     [38, 588, 574, 618], dict(_K137, erase=[[38, 589, 571, 616]])),
    ("7. Discard everything except the clear liquid.", [38, 619, 572, 647], dict(_K137, erase=[[38, 620, 421, 646]])),
    ("Discard", [458, 698, 580, 726], dict(_K137, max_size=20, erase=[[458, 699, 516, 725]])),
    ("Discard", [479, 746, 600, 776], dict(_K137, max_size=20, erase=[[479, 747, 542, 775]])),
    ("Discard", [483, 793, 605, 824], dict(_K137, max_size=20, erase=[[483, 794, 544, 823]])),
    ("falsificaso", [250, 776, 366, 796], dict(_K137, max_size=14, align="center", method="inpaint",
                                               erase=[[254, 777, 362, 795]])),
    ("8. Once the clear liquid is filtered, it is complete. This is falsificaso.", [38, 843, 602, 902],
     dict(_K137, line_spacing=1.2, erase=[[38, 844, 546, 873], [58, 875, 112, 900]])),
    ("Important", [80, 943, 300, 972], dict(_K137, erase=[[80, 944, 154, 971]])),
    ("Take special care in handling the pink liquid produced in step 7. Never heat it, pour it into a mountain "
     "stream, or the like. Dig a hole and dispose of it in the ground.", [78, 977, 772, 1036],
     dict(_K137, line_spacing=1.2, erase=[[79, 978, 696, 1005], [79, 1007, 625, 1034]])),
    ("Erika Niimura", [560, 1066, 770, 1102], dict(_K137, max_size=24, align="center", erase=[[618, 1068, 729, 1100]])),
]

JOBS += [
    {"id": "ref86-letter", "screen": "reference 86 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy letter, both paper faces (English blocks right to left)",
     "items": [(D + "rrr86/0.gal", ""), (D + "rrr86/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L86]},
    {"id": "ref31-letter", "screen": "reference 31 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy letter, both paper faces (English blocks right to left)",
     "items": [(D + "rrr31/0.gal", ""), (D + "rrr31/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L31]},
    {"id": "ref94", "screen": "reference 94 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 2, "color": "#ffffff", "new": True,
     "note": "teacher's blog page (photos, calendar digits, time stamp kept)", "items": [(D + "rrr94/0.gal", "")],
     "lines": L94},
    {"id": "ref132", "screen": "reference 132 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "Goto's memo 10 (handwriting; bullets, arrows and the kaomoji kept)", "items": [(D + "rrr132/0.gal", "")],
     "lines": L132},
    {"id": "ref134", "screen": "reference 134 detail", "style": "serif", "mode": "lines", "erase": "texfill",
     "erase_first": True, "mask_grow": 3, "color": "#1a0a05", "new": True,
     "note": "map in an old book (blobs, red X, ladder kept)", "items": [(D + "rrr134/0.gal", "")], "lines": L134},
    {"id": "ref137", "screen": "reference 137 detail", "style": "serif", "mode": "lines", "erase": "texfill",
     "erase_first": True, "mask_grow": 3, "color": "#3d1600", "new": True,
     "note": "instructions in an old book (drawings kept; the pot's faded marks illegible)",
     "items": [(D + "rrr137/0.gal", "")], "lines": L137},
    {"id": "ov-p10", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (86, 31, 94, 132, 134, 137)]},
]


# ---- IMAGES11 2026-10-02 (notes/IMAGES11-BRIEF.md): object / letter references unlocked in part 11 (240 111 208).
# Boxes measured on the sources with work/images/_c/img11/rows11.py, box11.py and cols11.py. The 60x30 thumbnails are
# below legibility: skipped. Scope B rr140 (1-bit, all black): no text, no job. Overviews: rr240 = refdoc_overview
# build (top crop); rr111 / rr208 = img11/paste11.py (1:1 crops of face 0, as 86 / 31 in IMAGES10).

# ---- 240 circular notice (800x1132, white paper, black printed type): flat white fill per line; the ● bullets and
# the two ruled boxes stay as drawn (erase boxes start right of the bullets and stay inside the rules). The 再南
# slip (node 4 asks whether it is a mistake for 'southernmost') is kept as a visible slip: "southermost".
_K240 = {"method": "flat", "bg": "#ffffff", "max_size": 22, "align": "left"}
_R240 = [
    ("Never let anyone of the Niimura family learn of this", 411, 433),
    ("Do not write the readers' names on this document", 444, 465),
    ("After reading, pass it on to the house to the south", 475, 497),
    ("Everyone must read it before the thirteenth-year memorial service begins", 508, 529),
    ("The southermost house is to dispose of this document at once", 540, 562),
    ("Everyone is to wear a Noh mask and red robes", 642, 662),
    ("Those who have hunting rifles are to lie in wait for the witch on the Arata mountain road", 674, 695),
    ("All others are to capture the witch as soon as they find her on the Arata mountain road", 706, 727),
    ("The use of Droga is permitted", 739, 759),
    ("Use the Droga that has already been distributed", 771, 791),
    ("After capturing the witch, take her to the underground storeroom", 802, 824),
]
L240 = [
    ("The Circular Notice", [100, 56, 700, 114], dict(_K240, max_size=44, align="center", erase=[[280, 58, 522, 111]])),
    ("Today, a witch in the likeness of a human girl will attend the thirteenth-year memorial service of the late "
     "Eiichiro Niimura. Because she will be in memorial-service dress, her face and build cannot be seen, but she "
     "will be holding a cherry branch. She holds the cherry branch in order to bring out the witch's power. As soon "
     "as the thirteenth-year memorial service is over, capture the witch without delay. Points to note follow.",
     [50, 147, 750, 306], dict(_K240, line_spacing=1.1, erase=[[45, 146, 755, 307]])),
    ("Circulation of This Document", [50, 372, 600, 402], dict(_K240, erase=[[46, 374, 146, 401]])),
    ("Capturing the Witch", [50, 602, 600, 632], dict(_K240, erase=[[46, 604, 170, 631]])),
    ("Note that the author of this document shall remain anonymous.", [75, 864, 760, 896],
     dict(_K240, erase=[[70, 865, 422, 894]])),
    ("End", [560, 930, 750, 960], dict(_K240, align="right", erase=[[700, 931, 753, 959]])),
]
for _t, _y0, _y1 in _R240:
    L240.append((_t, [79, _y0 - 4, 754, _y1 + 4], dict(_K240, erase=[[72, _y0 - 2, 755, _y1 + 3]])))

# ---- 111 / 208 書簡 diary letters, two paper faces each (letter() of the 書簡 block; face 1 texfill as 86 / 31 / 101).
# Drawings kept: the jar (111, ink up to x 214 on face 1) and the hand (208, up to x 424). The block-0 erase box is
# widened to the whole text area incl. the furigana (111 text ink x 220-857; 208 x 462-965).
L111 = ("At last I have been able to return to Ouda Castle. It seems that at that time I was attacked by a monster "
        "boar and lost consciousness. But someone who lives nearby found me and looked after me. I was surprised "
        "that people live in a place like that. It was a truly strange settlement. The one who looked after me was, "
        "by any reckoning, a Westerner. Why is a foreigner in a place like this? There must be some deep reason, "
        "but more interesting than that are the pink lumps they handed me. They gave me about ten lumps, each a "
        "little smaller than a one-sun cube. When I told them why I had come so deep into the mountains, they said "
        "this would surely be of use. I have been told how to use it, but I wonder whether this can really become "
        "the trump card that defeats Magawa. Doubts remain, but for the Ouda house to survive, there is nothing to "
        "do but cling to this.")
L208 = ("It was decided that she would be enshrined as a goddess. She gouged out both of her own eyes with her bare "
        "hands, and at the last thrust her hands into her eyes and died. It was so sudden that we did not understand "
        "what had happened, but she looked as if she were resisting something. Using a method we had learned from "
        "Ginosuke-dono before, it was decided that her remains would be preserved for a long time, but could it be "
        "that that was what it means to be possessed by a shinigami? I had heard of the concepts of shinigami and "
        "witches from Ginosuke-dono, but having seen such a thing before my very eyes, I cannot help but believe.")
_L111 = letter(L111, 220, 850, 2)
_L111[0][2]["erase"] = [[216, 0, 860, 450]]
_L208 = letter(L208, 462, 962, 2)
# split_blocks put 4 of 5 sentences in block 0 (18 px vs 20 px, block 1 mostly empty): split after sentence 3
_i208 = L208.index("Using a method")
_L208 = [(L208[:_i208].strip(), _L208[0][1], _L208[0][2]), (L208[_i208:], _L208[1][1], _L208[1][2])]
_L208[0][2]["erase"] = [[440, 0, 974, 450]]

JOBS += [
    {"id": "ref240", "screen": "reference 240 detail", "style": "serif", "mode": "lines", "erase": "flat",
     "erase_first": True, "mask_grow": 2, "mask_color": [0, 170, 0, 170, 0, 170], "new": True,
     "note": "printed circular notice (bullets and box rules kept)", "items": [(D + "rrr240/0.gal", "")],
     "lines": L240},
    {"id": "ref111-letter", "screen": "reference 111 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy diary letter, both paper faces (English blocks right to left; jar drawing kept)",
     "items": [(D + "rrr111/0.gal", ""), (D + "rrr111/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L111]},
    {"id": "ref208-letter", "screen": "reference 208 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": [0, 85, 0, 85, 0, 85], "new": True,
     "note": "calligraphy diary letter, both paper faces (English blocks right to left; hand drawing kept)",
     "items": [(D + "rrr208/0.gal", ""), (D + "rrr208/1.gal", "", {"erase": "texfill"})],
     "lines": [(t, b, dict(o, mask_color=[0, 85, 0, 85, 0, 85])) for t, b, o in _L208]},
    {"id": "ov-p11", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr%d.gal" % i, "") for i in (240, 111, 208)]},
]



# ---- IMAGES12 2026-10-02 (notes/IMAGES12-BRIEF.md): object reference 157 unlocked in part 12 (the inn's web page).
# Boxes measured on the sources with work/images/_c/img12/rows12.py, gaps12.py and grid.py. The 60x30 thumbnail is
# below legibility: skipped. rrr157/1-5.gal and 8.gal are photos (slideshow frames) with no text: no job. 0.lcm / 1.lcm
# are LiveCinema motion files that only name the .gal frames (no text, sizes unchanged): not edited, not shipped.
# 0.gal = the page (800x3299; a white veil at alpha ~51 with white glyphs in the alpha plane at rows 238-387 over a
# transparent slideshow window). 7.gal = the same page without the header (rows 0-401 transparent), Gregorian notice
# dates and the plans section 204 px higher. 6.gal = the header banner alone (930x202, same veil).
# Web page = gothic face (brief rule). Header glyphs: inpainta (colour and alpha plane) on the RGB <= 253 mask, so the
# veil's alpha flows back over the glyphs; the rule under the greeting is outside both erase boxes. Latin parts kept:
# the dates in the notice, the small English label subtitles, TEL and the copyright line, the photos.
_G157 = {"style": "gothic", "align": "left"}
_HDR = {"method": "inpainta", "mask_color": [0, 253, 0, 253, 0, 253], "mask_grow": 9, "color": "#ffffff",
        "align": "center"}
_NT = {"method": "inpaint", "mask_color": [0, 150, 0, 150, 0, 130], "mask_grow": 3, "color": "#2b2412", "max_size": 17}
_LB = {"method": "inpaint", "mask_color": [0, 170, 0, 170, 0, 170], "mask_grow": 3, "color": "#1a1a1a",
       "align": "center"}
_TG = {"method": "inpaint", "mask_grow": 5, "color": "#f4f4f4", "align": "center"}
_BD = {"method": "flat", "bg": "#010101", "color": "#eeeeee", "max_size": 16, "line_spacing": 1.45}
_PL = {"method": "flat", "bg": "#fcfcfc", "color": "#333333", "max_size": 16}
_FT = {"method": "flat", "bg": "#010101"}


def _g(t, box, er, base, **k):
    o = dict(_G157)
    o.update(base)
    o["erase"] = er
    o.update(k)
    return (t, box, o)


def _tag(t, box, er, thr, size):
    """tagline in the cell strip: inpaint the white glyphs, then the English in white with a 1-px dark outline."""
    o = dict(_G157)
    o.update(_TG)
    o.update(max_size=size, mask_color=[thr, 255, thr, 255, thr, 255])
    return [("", box, dict(o, erase=[er]))] + _outline(t, box, "#101010", dict(o, erase=[])) + [(t, box, dict(o, erase=[]))]


_T157 = [
    ("Hospitality with the finest Japanese cuisine", [195, 662, 612, 697], [195, 664, 612, 696], 150, 22),
    ("Every guest room, a superb view facing the sea", [120, 1131, 672, 1163], [122, 1131, 672, 1162], 150, 24),
    ("Relaxing waters, unhurried warmth", [195, 1586, 607, 1622], [195, 1586, 607, 1622], 215, 24),
    ("Tranquility for everyone", [150, 2043, 656, 2078], [150, 2043, 656, 2078], 170, 24),
]
_B157 = [
    ("At the Iizawa Taiyo Inn, we use an abundance of fresh seafood caught at the local Megasawa fishing port. For "
     "our other ingredients too, we use goods shipped direct from where they are produced all over Japan, and we "
     "prepare the finest meals. Western and Chinese cuisine can also be prepared to suit our guests' tastes.",
     [110, 718, 690, 856], [100, 720, 700, 852]),
    ("Purely Japanese-style rooms, every one with a view of Iizawa Bay. The Comfort Suite on the top floor has an "
     "open-air bath with hot-spring water flowing straight from the source. Check-in is at 14:00 and check-out is "
     "at 12:00, so you can relax at your leisure.", [105, 1186, 695, 1330], [95, 1188, 700, 1322]),
    ("Blessed with a chloride spring, our inn has the open-air bath \"Amaterasu,\" with a view of the sea breeze and "
     "the open sky, and the indoor grand bathhouse \"Izanami,\" with its spacious tubs. They are also open to "
     "day-trip visitors.", [105, 1660, 695, 1800], [95, 1662, 700, 1762]),
    ("Besides its hot springs, our inn has a variety of facilities, such as a wedding hall, banquet halls, meeting "
     "spaces and a restaurant floor. So that small children can enjoy themselves too, we also provide a kids' "
     "floor, a theater room and, outdoors, an athletic park.", [105, 2117, 695, 2275], [95, 2119, 700, 2254]),
]
# plans section + footer, in 0.gal rows (7.gal: same boxes 204 px higher)
_P157 = [
    ("Recommended Plans", [262, 2521, 538, 2559], [276, 2523, 525, 2559], dict(max_size=29, align="center",
                                                                               color="#2a2a2a")),
    ("Kaiseki Buffet", [40, 2588, 400, 2618], [40, 2589, 198, 2618], dict(max_size=22, color="#2a2a2a")),
    ("At our inn's famous kaiseki buffet, you can eat as much as you like of the dishes you like, such as over 15 "
     "kinds of sashimi, all kinds of grilled dishes, steamed dishes and clear soups.", [226, 2631, 785, 2703],
     [222, 2632, 790, 2702], dict(line_spacing=1.2)),
    ("Per person  ¥8,000~ (tax not included)", [238, 2704, 785, 2727], [236, 2705, 790, 2726], {}),
    ("※Meals are served in the banquet hall. They cannot be served in guest rooms.", [226, 2727, 792, 2749],
     [222, 2728, 792, 2748], {}),
    ("Premium Kaiseki", [40, 2786, 400, 2815], [40, 2787, 148, 2815], dict(max_size=22, color="#2a2a2a")),
    ("A superb course that upgrades the kaiseki cuisine of the regular plan even further and uses the ingredients "
     "of each season without holding back. The head chef decides the dishes day by day, and you will be served the "
     "finest cuisine.", [226, 2828, 785, 2900], [222, 2829, 790, 2899], dict(line_spacing=1.2)),
    ("Hearty! Seaside Grill Course", [40, 2986, 500, 3017], [40, 2987, 270, 3016], dict(max_size=22, color="#2a2a2a")),
    ("More reasonable than the regular plan: a manly course where seafood is grilled before your eyes and you bite "
     "into it heartily! You can choose your room or the garden.", [226, 3029, 785, 3100], [222, 3030, 790, 3099],
     dict(line_spacing=1.2)),
    ("Per person  ¥5,000~ (tax not included)", [238, 3102, 785, 3125], [236, 3103, 790, 3125], {}),
    ("※To prevent food poisoning, please refrain from bringing in your own food.", [226, 3126, 792, 3147],
     [222, 3127, 792, 3146], {}),
]
_F157 = [
    ("Iizawa Taiyo Inn", [45, 3208, 340, 3258], [42, 3208, 330, 3258], dict(max_size=34, color="#f0f0f0",
                                                                          align="center")),
    ("Five-star seaside hot-spring inn  Iizawa Taiyo Inn", [350, 3213, 795, 3230], [348, 3213, 566, 3230],
     dict(max_size=13, color="#a8a8a8")),
    ("502 Minami-Iizawa-cho, Megasawa District, Iizawa Prefecture", [350, 3230, 795, 3247], [348, 3230, 566, 3247],
     dict(max_size=13, color="#a8a8a8")),
]


def _sh157(b, d):
    return [b[0], b[1] + d, b[2], b[3] + d]


def _l157(dy_low, notice_x, notice):
    """line list of the page body (rows >= 400); dy_low = shift of the plans section and footer (0.gal 0, 7.gal -204)."""
    L = [_g("News", [10, 414, 150, 448], [[12, 416, 135, 446]], _NT, max_size=24, align="center", color="#1e1a10")]
    for t, y0, y1 in zip(notice, (410, 434, 458), (432, 456, 479)):
        L.append(_g(t, [notice_x + 2, y0, 795, y1], [[notice_x, y0 + 1, 792, y1 - 1]], _NT))
    for t, box, er, size in (("Dining", [18, 526, 146, 553], [32, 527, 128, 553], 25),
                             ("Rooms", [16, 955, 146, 985], [50, 957, 110, 985], 24),
                             ("Bathing", [16, 1400, 144, 1428], [48, 1402, 112, 1428], 22),
                             ("Amenities", [20, 1862, 200, 1899], [66, 1864, 152, 1899], 30)):
        L.append(_g(t, box, [er], _LB, max_size=size))
    for t, box, er, thr, size in _T157:
        L += _tag(t, box, er, thr, size)
    for t, box, er in _B157:
        L.append(_g(t, box, [er], _BD))
    for t, box, er, k in _P157:
        L.append(_g(t, _sh157(box, dy_low), [_sh157(er, dy_low)], _PL, **k))
    for t, box, er, k in _F157:
        L.append(_g(t, _sh157(box, dy_low), [_sh157(er, dy_low)], _FT, **k))
    return L


_N157 = ["Early-summer kaiseki \"Azure Sea Course\" begins (until 06/15)",
         "Limited-time spring-fish kaiseki \"Spring Aster Course\" begins (until 05/30)",
         "Bookings open for blossom-viewing rooms in the garden"]
_N157_7 = [_N157[0].replace("06/15", "6/15"), _N157[1].replace("05/30", "5/30"), _N157[2]]
_HG157 = "Welcome. Please take your time and relax."
_HT157 = "Iizawa Taiyo Inn"


def _hdr157(dx, dy):
    """header banner lines (0.gal at (0, 0); 6.gal at (+74, -239)); the furigana goes with the title erase box."""
    def m(b):
        return [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy]
    return [_g(_HG157, m([150, 260, 650, 291]), [m([210, 258, 580, 291])], _HDR, max_size=22),
            _g(_HT157, m([100, 310, 700, 382]), [m([165, 296, 630, 386])], _HDR, max_size=56)]


L157_0 = _hdr157(0, 0) + _l157(0, 270, _N157)
L157_7 = _l157(-204, 284, _N157_7)
L157_6 = _hdr157(74, -239)

JOBS += [
    {"id": "ref157", "screen": "reference 157 detail", "style": "gothic", "mode": "lines", "erase": "flat",
     "erase_first": True, "mask_grow": 3, "mask_color": [0, 253, 0, 253, 0, 253], "new": True,
     "note": "inn web page (photos, notice dates, small English label subtitles, TEL and copyright kept)",
     "items": [(D + "rrr157/0.gal", "")], "lines": L157_0},
    {"id": "ref157-p7", "screen": "reference 157 page variant", "style": "gothic", "mode": "lines", "erase": "flat",
     "erase_first": True, "mask_grow": 3, "mask_color": [0, 253, 0, 253, 0, 253], "new": True,
     "note": "inn web page, headerless variant with Gregorian notice dates (same kept parts)",
     "items": [(D + "rrr157/7.gal", "")], "lines": L157_7},
    {"id": "ref157-banner", "screen": "reference 157 header banner", "style": "gothic", "mode": "lines",
     "erase": "flat", "erase_first": True, "mask_grow": 3, "mask_color": [0, 253, 0, 253, 0, 253], "new": True,
     "note": "inn web page header banner (white veil; rule kept)", "items": [(D + "rrr157/6.gal", "")],
     "lines": L157_6},
]
# ov-p12: rr157 = work/images/_c/img12/ov157.py build 0 453 (slideshow photo 5.gal under the English page 0, crop
# (0, 0, 800, 453) resized to 300x170; probe on the JP files: mean abs diff 6.30).
JOBS += [
    {"id": "ov-p12", "screen": "reference screen previews", "style": "gothic", "mode": "asis", "chain": True,
     "items": [(O + "rr157.gal", "")]},
]


# ---- IMAGES13 2026-10-02 (notes/IMAGES13-BRIEF.md): scenario references unlocked in part 13 (145 235).
# 145: 21 viewer-post cards rrr145/シャベッター/0..20 (310x95 / 96, the rrr1 card family: same layout, every card has
# text; no background art in this set). Show name "Oha-Oha!" as rrr1 (QIMAGES13-01 ruled). JP one-line
# posts longer than about 44 characters of English are set on two lines (the two-line box of _sha()).
# rr145 / rr235 概要 = photos without text: no job, no ov-p13 sheet (rr33 / rr118 / rr140 precedent). The 60x30
# サムネ are below legibility: skipped.
_SHA145 = ["Yukipin's not coming on anymore,\nguess I'll go to work", "Wha!? Yukipin!", "Yukipin's back!",
           "Okay, I'm going in late to work today", "Yukipin's here, so I'm kneeling in seiza,\nstark naked",
           "It's okay, Yukipin, I'm here for you", "That's my living spirit, y'know", "A fortune-teller!",
           "Yukipin's face-reading result: you will\nmarry me", "I wanna worship Yukipin's face up close too",
           "Well, it's already settled\nthat she's marrying me", "Yukipin, look over here",
           "Is Yukipin gonna quit her job?", "[Breaking] Yukipin lives in a filthy room",
           "I'll go over and clean it up", "I've worked up an appetite for Yukipin",
           "I'll buy Yukipin's half-eaten bento\nfor 200,000 yen", "Kind of a serious fortune-teller, huh",
           "Sell tons of Yukipin's half-eaten bentos\nand you'd be a millionaire",
           "That's a fortune that makes sense, huh", "I'm glad I was late for work today"]
JOBS += [
    {"id": "ref145-posts", "screen": "reference 145 posts", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_color": [0, 120, 0, 120, 0, 120], "mask_grow": 2, "color": "#222222", "new": True,
     "note": "viewer posts on the morning show (avatar and 'on Sha-better' kept)",
     "items": [(D + "rrr145/シャベッター/%d.gal" % n, "", {"lines": _sha(t)}) for n, t in enumerate(_SHA145)],
     "lines": []},
]


# ---- IMAGES15 2026-10-02 (notes/IMAGES15-BRIEF.md): object reference 152 unlocked in part 15 (a bankbook, flip object).
# Face 0 = cover (500x310: white label band, white-on-pink title and bank name; "SAWAGIN" logo, X034 / XX98765 kept),
# face 1 = the open page (500x620: orange headers on peach, black entries; dates, amounts, row numbers already Latin
# digits, kept). Printed throughout -> serif. Boxes measured with work/images/_c/img15/blobs.py / meas.py on the
# sources. Close-ups 部分拡大1-5 = face 1 at s 1.600, ox 0 (work/images/_c/img15/match15.py, scores 0.89-0.97); only
# the bottom band of each is opaque, so the transparent top is protected (no English spills onto it). Flip frames
# 01-18: see tl-log-IMAGES15.md.
_OR = [120, 255, 0, 222, 0, 200]      # orange glyphs on the peach page (page bg 253,234,219)
_ORC = "#c8641e"
_DK = {"method": "inpaint", "mask_color": DARK, "mask_grow": 3}
_OI = {"method": "inpaint", "mask_color": _OR, "mask_grow": 3, "color": _ORC}
# IMAGES15F 2026-10-02 (checker FIX b): the white-strip glyphs are anti-aliased grey (median ~187 on white), DARK
# (<= 110) left their edges, and the boxes cut 2-3 px off the glyphs (labels x 28-57 / 155-193 y 53-65, name x 285-359
# y 68-83, honorific x 400-409 y 73-82; work/images/_c/img15/strip15f.py). Now: every non-white pixel (all channels
# <= 245) in boxes padded 2 px is painted white (maskfill, flat white strip; inpaint would pull the pink band above).
# The Latin X034 / XX98765 (y 70-82, x <= 206) stay outside every box. Text boxes and sizes unchanged.
_WS = {"method": "maskfill", "mask_color": [0, 245, 0, 245, 0, 245], "mask_grow": 3, "bg": "#ffffff"}
L152_0 = [
    ("Branch No.", [30, 52, 150, 66], dict(_DK, **_WS, erase=[[26, 52, 60, 68]], max_size=10)),
    ("Account No.", [158, 52, 280, 66], dict(_DK, **_WS, erase=[[153, 52, 197, 68]], max_size=10)),
    ("Momoko Goto-sama", [288, 66, 440, 84], dict(_DK, **_WS, erase=[[283, 66, 362, 88], [398, 71, 412, 88]], max_size=15)),
    ("Ordinary Deposit Bankbook", [12, 98, 330, 126],
     dict(_DK, mask_color=[200, 255, 150, 255, 200, 255], erase=[[12, 99, 165, 125]], max_size=24, color="#ffffff")),
    ("Sawa Bank", [357, 266, 480, 297],
     dict(_DK, mask_color=[200, 255, 185, 255, 200, 255], erase=[[357, 268, 460, 295]], max_size=24, color="#ffffff")),
]
_R152 = [(84, 93, "W"), (103, 111, "S"), (121, 130, "S"), (139, 148, "S"), (157, 166, "S"), (176, 185, "I"),
         (194, 203, "T"), (212, 221, "C"), (231, 240, "X"), (249, 258, "W"), (268, 276, "S"), (286, 295, "S"),
         (342, 351, "T"), (360, 369, "C"), (379, 387, "W"), (397, 406, "S"), (415, 424, "S"), (433, 443, "T"),
         (452, 461, "C"), (470, 479, "W"), (489, 497, "S"), (507, 516, "T"), (525, 534, "C")]
_E152 = {"W": "Withdrawal (cash card)", "S": "Salary", "I": "Interest", "T": "Telecom fee (NowCommu)",
         "C": "Card debit (Smile Card)", "X": "Transfer"}
L152_1 = [
    ("Ordinary Deposit", [44, 5, 204, 25], dict(_OI, erase=[[139, 5, 204, 25]], align="right", max_size=17)),
    ("(and Loan Statement)", [251, 5, 452, 25], dict(_OI, erase=[[251, 5, 359, 25]], max_size=17)),
    ("Balance (yen)", [404, 45, 496, 58], dict(_OI, erase=[[420, 46, 480, 58]], align="center", max_size=10)),
    ("(A minus sign shows\nthe loan balance.)", [414, 58, 486, 73],
     dict(_OI, erase=[[414, 59, 486, 71]], align="center", max_size=7, line_spacing=0.85)),
    ("Date", [34, 61, 106, 76], dict(_OI, erase=[[78, 62, 106, 75]], align="right", max_size=11)),
    ("Transaction", [112, 61, 229, 76], dict(_OI, erase=[[145, 62, 194, 75]], align="center", max_size=11)),
    ("Withdrawals (yen)", [234, 61, 314, 76], dict(_OI, erase=[[238, 62, 305, 75]], align="center", max_size=11)),
    ("Deposits (yen)", [318, 61, 398, 76], dict(_OI, erase=[[319, 62, 393, 75]], align="center", max_size=11)),
] + [(_E152[k], [114, y0 - 4, 230, y1 + 4], dict(_DK, erase=[[114, y0 - 2, 229, y1 + 2]], max_size=12, color="#1a1a1a"))
     for y0, y1, k in _R152] + [
    ("For checks of other banks deposited at our branches, or collections treated as due-date deposits, the time "
     "payment\nbecomes possible differs with the bills and checks payable at other banks. For details, please ask at "
     "the counter.", [121, 557, 494, 578], dict(_OI, erase=[[120, 559, 452, 577]], max_size=8)),
]
# close-ups: (n, s, ox, oy, W, H) from match15.py; protect = the transparent rows above the opaque band
Z152 = [(1, 1.6, 0, -32.13, 800, 250, 195), (2, 1.6, 0, 95.0, 800, 250, 198), (3, 1.6, 0, 240.75, 800, 250, 200),
        (4, 1.6, 0, 280.5, 800, 240, 170), (5, 1.6, 0, 350.87, 800, 250, 203)]
JOBS += [
    {"id": "ref152-cover", "screen": "reference 152 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "color": "#1a1a1a", "new": True, "note": "bankbook cover (logo, branch and account numbers kept)",
     "items": [(D + "rrr152/0.gal", "")], "lines": L152_0},
    {"id": "ref152-page", "screen": "reference 152 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "color": "#1a1a1a", "new": True, "note": "bankbook page (dates, amounts, row numbers, arrows, page 5 kept)",
     "items": [(D + "rrr152/1.gal", "")], "lines": L152_1},
    {"id": "ref152-zoom", "screen": "reference 152 close-ups", "style": "serif", "mode": "lines", "erase": "inpaint",
     "color": "#1a1a1a", "note": "bankbook close-ups (same English as the page, own scale)",
     "items": [(D + "rrr152/部分拡大%d.gal" % n, "", {"lines": [e for e in zoom_lines(L152_1, ox, oy, s, W, H) if e[1][3] > top],
                                                     "protect": [[0, 0, W, top]]}) for n, s, ox, oy, W, H, top in Z152],
     "lines": []},
]
# Flip frames rrr152/01-18 (refdoc_flip.py 152 01,..,18 0,1 --mode full; log work/images/_c/img15/flip-full1.log):
# only 13 registers (5.9; the lower page alone). The others are composites (the lower page of face 1 stays put while
# the cover or the upper page hinges over it) and are shaded (per-channel gain 0.14-0.8): scores 16.6-65.7 -> not
# derived, the Japanese originals stay (QIMAGES15-01 in tl-log-IMAGES15.md). The two .lcm descriptors are not touched.
# ov-p15: rr152 = refdoc_overview.py build 152 (top crop (0, 0, 500, 283) of the English cover, probe 2.24).
JOBS += [
    {"id": "ref152-flip", "screen": "reference 152 flip frames", "style": "serif", "mode": "asis", "chain": True,
     "items": [(D + "rrr152/13.gal", "")]},
    {"id": "ov-p15", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr152.gal", "")]},
]


# ---- IMAGES16 2026-10-02 (notes/IMAGES16-BRIEF.md): object reference 153 unlocked by card 191 (a letter, 書簡).
# 153 Goto's letter (800x1132, blue-ruled paper, typed-hand font, ONE page): the ref189 pattern (handwriting face, one
# English line per JP line in the JP line's row, memo()). Rows from work/images/_rows.py ... - 60 3 1 on the source
# (the 1-2 px rule fragments at y 366 / 617 / 687 dropped). Descenders touch the rules (y 224, 295, 438, 473, 545, 580,
# 652, 759): text_only restores the rule pixels after the erase. Node boxes (リファレンスターゲット): date row, row 9,
# row 12 x 319-456, row 14 x 67-271; the English keeps the same sentence in the same row.
R153 = [[67, 161, 719, 184], [52, 200, 744, 224], [67, 234, 744, 256], [46, 272, 742, 296], [49, 305, 743, 328],
        [50, 343, 456, 362], [69, 376, 744, 400], [51, 414, 753, 436], [50, 448, 741, 471], [49, 484, 748, 504],
        [49, 521, 743, 544], [50, 554, 742, 576], [49, 592, 232, 611], [69, 626, 748, 648], [49, 664, 211, 683]]
T153 = [
    "It's been a while! Motoki-cho's genius girl, Erina Goto, is writing you a letter!",
    "That incident the other day was hard in lots of ways, but now let's both look forward!",
    "Golden Week starts today, and I'm planning to really stretch my wings these clear May",
    "days. I'm planning to go to the Unreal Park that opened in Megasawa, but what will you do,",
    "Erika-chan? I can't really picture Golden Week in the Arata settlement, but I hope",
    "you have a nice holiday there too!",
    "Oh, right! The senpais and I are talking about going to the Arata settlement again",
    "over summer vacation. This time, I'm hoping we can all have fun, with nothing to do with",
    "funerals or incidents. Chiga-nee will surely be back by then too, right? Oh, but wasn't",
    "Chiga-nee leaving to study abroad...? But if the dates work out, I'd love to have a",
    "welcome-and-farewell party for Chiga-nee too. So much happened that I never got to ask",
    "for your contact info, Erika-chan, but since it's a good chance, I tried writing a letter!",
    "These days everything gets done on a phone, so something like this feels really fresh!",
    "Well then, see you again in the summer! I'm already looking forward to which impression",
    "you'll greet me with!",
]
JOBS += [
    {"id": "ref153", "screen": "reference 153 detail", "style": "handwriting", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "text_only": True, "mask_grow": 2, "thr": 60, "color": "#1a1a1a", "new": True,
     "note": "Erina Goto's letter (ruled paper)", "items": [(D + "rrr153/0.gal", "")],
     "lines": [("Shiyo 800, May 2", [520, 54, 752, 80], {"max_size": 20, "align": "right", "erase": [[606, 56, 751, 79]]}),
               ("To Erika-chan,", [46, 91, 400, 115], {"max_size": 20, "erase": [[46, 92, 181, 114]]})]
     + memo(R153, T153, size=19, right=752)
     + [("From Motoki-cho's genius girl, Erina Goto!", [300, 731, 752, 758],
         {"max_size": 20, "align": "right", "erase": [[431, 732, 746, 758]]})]},
]
# ov-p16: rr153 = refdoc_overview.py build 153 (see tl-log-IMAGES16.md for the crop and probe). The 60x30 サムネ is
# below legibility: skipped.
JOBS += [
    {"id": "ov-p16", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr153.gal", "")]},
]


# IMAGESR-B 2026-10-04 (notes/IMAGESR-BRIEF.md, lane B): report documents 156 162 163 169 171 174 176 (形式 レポート).
# Each 全体.gal = the finished jigsaw picture (800 px wide, parchment / paper ground, printed Mincho type = Cambria).
# Boxes measured with work/_rows.py and work/images/_c/imgRB/comp.py + span.py on the sources. Dark type on paper:
# texfill of the dark glyph pixels inside the erase boxes; white type on black / red plates: flat fill of the plate
# colour inside the plate body, English set in white. Overview cards rr<ID> = imgRB/ovcard.py (mode asis).
_RBM = [0, 150, 0, 140, 0, 120]                     # dark glyph pixels on parchment (core + anti-aliased rim)
_RBB = {"method": "texfill", "mask_color": _RBM, "align": "left", "max_size": 23, "line_spacing": 1.12}
_RBL = {"method": "texfill", "mask_color": _RBM, "align": "center", "max_size": 24}


def _rbw(bg, **k):
    """white type on a flat plate: fill the erase box with the plate colour, set the English in white."""
    return dict({"method": "flat", "bg": bg, "color": "#ffffff", "align": "center", "max_size": 24}, **k)


def _rbjob(rid, note, lines, **k):
    return dict({"id": "rep%d-whole" % rid, "screen": "reference %d report" % rid, "style": "serif", "mode": "lines",
                 "erase": "texfill", "erase_first": True, "mask_grow": 3, "mask_color": _RBM, "color": "#140303",
                 "new": True, "note": note, "items": [(D + "rrr%d/全体.gal" % rid, "")], "lines": lines}, **k)


# ---- 156 (No.8) 800x2301: title, 4 paragraphs, 3 diagrams, date, signature.
L156 = [
    ("Trauma in the Second Generation", [20, 4, 780, 54], dict(_RBL, max_size=36, erase=[[222, 6, 582, 52]])),
    ("We named those of our brethren who touched the blood of a person given Droga and gained precognition the "
     "second generation. Likewise, we named those of our brethren who used Droga the first generation. Hereafter, "
     "they will be called the first generation and the second generation.",
     [12, 120, 788, 264], dict(_RBB, erase=[[8, 123, 778, 262]])),
    ("Droga", [20, 356, 122, 392], dict(_RBL, max_size=22, erase=[[36, 358, 116, 390], [117, 361, 146, 388]])),  # SWEEP-PIC: 2nd box = the last kana (syringe edge from x ~147)
    ("Blood", [350, 384, 470, 429], _rbw("#010101", erase=[[350, 382, 446, 431]])),
    ("First generation", [120, 546, 356, 582], dict(_RBL, erase=[[176, 548, 298, 580]])),
    ("Second generation", [462, 546, 708, 582], dict(_RBL, erase=[[523, 548, 644, 580]])),
    ("Now, when we examined whether the conditions that trigger the second generation's precognition could be "
     "eased, we succeeded in suppressing the ill health. When they became the second generation, they witnessed "
     "that gruesome scene, so they are thought to have contracted some kind of psychological trauma, but we "
     "investigated whether it is truly caused by trauma. At present, those who have become the second generation "
     "suffer ill health with 100% probability. We questioned the abnormally high incidence of this trauma and "
     "formed the hypothesis that it is an effect of Droga.",
     [12, 650, 788, 934], dict(_RBB, erase=[[8, 653, 795, 933]])),
    ("Re-creating the\nsituation at the time\nof blood contact", [42, 1030, 250, 1104],
     _rbw("#010101", max_size=22, line_spacing=1.05, erase=[[40, 1030, 245, 1104]])),
    ("Danger sense\nIll health", [484, 1042, 680, 1126], _rbw("#010101", erase=[[490, 1048, 672, 1122]])),
    ("To test this possibility, we applied the blood of a first-generation member, in a calm state, to the lips of "
     "a second-generation candidate (the second-generation candidate had been told in advance what kind of "
     "experiment would be performed). After confirming that the candidate had become second generation, we applied "
     "blood to the lips again and left it unwiped for 15 minutes or more, which brought on ill health. From this, it "
     "is hard to believe that trauma had occurred, and we judged that this is, after all, a symptom caused by "
     "Droga. In other words, ill health is induced by re-creating the situation in which one became the second "
     "generation.",
     [12, 1214, 788, 1536], dict(_RBB, erase=[[8, 1218, 778, 1533]])),
    ("Danger sense possible", [110, 1578, 690, 1614], _rbw("#010101", erase=[[300, 1579, 515, 1613]])),
    ("15 minutes later", [230, 1710, 510, 1747], _rbw("#010101", erase=[[320, 1711, 430, 1746]])),
    ("Usable within these 15 minutes", [262, 1840, 520, 1870], _rbw("#c00000", max_size=20, erase=[[268, 1840, 512, 1870]])),
    ("Re-creating the situation\nat the time of blood contact", [4, 1907, 262, 1964],
     dict(_RBL, max_size=19, erase=[[30, 1909, 168, 1962]])),
    ("Ill health", [540, 1907, 700, 1936], dict(_RBL, max_size=19, mask_grow=5, erase=[[570, 1909, 665, 1936]])),  # SWEEP-PIC: grow 5 clears the glyph rims
    ("If Droga is to be used effectively, then beyond the first generation's muscle strengthening, we create the "
     "second generation and, when precognition becomes necessary, re-create the conditions of its creation. "
     "Precognition can be exercised immediately from that moment, so it suffices to end the re-created situation "
     "before 15 minutes have passed.",
     [12, 1990, 788, 2170], dict(_RBB, erase=[[8, 1994, 778, 2168]])),
    ("Shiyo 730, April 18", [12, 2204, 500, 2240], dict(_RBB, erase=[[8, 2206, 256, 2239]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [12, 2240, 790, 2276],
     dict(_RBB, erase=[[8, 2241, 565, 2275]])),
]
JOBS += [_rbjob(156, "report No.8 (parchment; diagrams kept)", L156)]
# rr156 card = imgRB/ovcard.py 156 "Trauma in the Second Generation" 4 104 114 34 none (built from the English page).
JOBS += [{"id": "rep156-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr156.gal", "")]}]

# ---- 162 (No.9) 800x1579: title, 5 paragraphs, two structural formulas (Latin atom labels kept), a spore photo with
# a caption, date, signature. The rr162 card is below legibility (only blurred blobs over blue art): not built.
L162 = [
    ("Constituents of Droga", [20, 4, 780, 56], dict(_RBL, max_size=36, erase=[[254, 7, 564, 53]])),
    ("Until now, it has been a question why using Droga brings muscle strengthening and danger sense. We had been "
     "preparing a component analysis from the start, but it took time to obtain the necessary equipment and budget. "
     "Preparations are now finally complete and the component analysis has been carried out, so we report it here.",
     [12, 120, 788, 298], dict(_RBB, erase=[[8, 124, 778, 297]])),
    ("Our initial hypothesis was that it contains narcotic components (methamphetamine, ephedrine, etc.) and that "
     "these exert some kind of effect. However, the results were entirely different from those.",
     [12, 299, 788, 438], dict(_RBB, erase=[[8, 299, 778, 437]])),
    ("Methamphetamine", [90, 564, 390, 600], dict(_RBL, max_size=23, erase=[[118, 566, 352, 598]])),
    ("Ephedrine", [440, 564, 700, 600], dict(_RBL, max_size=23, erase=[[482, 566, 660, 597]])),
    ("Droga contains a large quantity of biological fragments, and we had thought this was because it was made from "
     "the roots of the Arata cherry. However, when we tested the blood of the first and second generations, it "
     "likewise contained unknown biological fragments. Examining those fragments in detail, we found that they were "
     "spores.",
     [12, 610, 788, 794], dict(_RBB, erase=[[8, 615, 778, 789]])),
    ("Biological fragments (spores) detected in the blood of the second generation", [20, 1138, 780, 1176],
     dict(_RBL, max_size=23, erase=[[115, 1140, 720, 1173]])),
    ("Similar spores are likewise contained in Droga, and it is a question why a medicine made from the roots of the "
     "cherry, an angiosperm, contains spores. At the least, since these spores remain in the second generation as "
     "well, it is thought that the spores contained in Droga are precisely the cause of the muscle strengthening and "
     "danger sense.",
     [12, 1208, 788, 1388], dict(_RBB, erase=[[8, 1213, 778, 1387]])),
    ("If that is so, we will have obtained the power of God scientifically, and the authority of the Holy Cerejeira Church "
     "will also grow.",
     [12, 1388, 788, 1460], dict(_RBB, erase=[[8, 1389, 778, 1457]])),
    ("Shiyo 730, September 30", [12, 1492, 500, 1528], dict(_RBB, erase=[[8, 1494, 259, 1527]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [12, 1528, 790, 1564],
     dict(_RBB, erase=[[8, 1529, 563, 1562]])),
]
JOBS += [_rbjob(162, "report No.9 (parchment; formulas and photo kept)", L162)]



# IMAGESR-A 2026-10-04 (notes/IMAGESR-BRIEF.md): the finished report documents rrr<ID>/全体.gal (lane A: 190 191 127
# 128 138 139 154) + their 概要 cards. Printed pages on mottled paper: Cambria, ink #281c0c, glyph mask = every channel
# <= 185 (the paper never goes below 160 in any channel: work/images/_c/imgR-A/col.py), texfill on the paper, inpaint
# inside table cells (the faint 1 px rules stay; cell erase boxes sit 4 px inside them). Rows / rules measured with
# work/images/_c/imgR-A/rows.py and rules.py. The English is longer than the Japanese, so body text is REFLOWED:
# _rflow() stacks paragraphs from a top y at one fixed size (box = exactly the wrapped height; the same wrap as
# typeset_ui.fit) and every JP row is erased by separate erase-only lines (erase_first). Overview cards = top crops of
# the English page (work/images/_c/imgR-A/ov.py, refdoc_overview.py transform on 全体.png), shipped as mode asis.
import math as _math
from PIL import Image as _Im, ImageDraw as _Dr, ImageFont as _Fn
import typeset_ui as _T

_RINK = "#281c0c"
_RMASK = [0, 185, 0, 185, 0, 185]
_RD = _Dr.Draw(_Im.new("RGB", (4, 4)))
_RFONT = "C:/Windows/Fonts/cambria.ttc"


def _rflow(paras, x0, x1, y0, size, ls=1.0, gap=0.4, align="left", color=None):
    """paragraphs stacked from y0 at one size; returns (lines, end_y). Each box = the wrapped height exactly."""
    font = _Fn.truetype(_RFONT, size)
    asc, desc = font.getmetrics()
    lh = (asc + desc) * ls
    out, y = [], float(y0)
    for p in paras:
        n = len(_T.wrap(_RD, p, font, x1 - x0, 0))
        h = int(_math.ceil(n * lh)) + 1
        o = {"max_size": size, "line_spacing": ls, "erase": [], "align": align}
        if color:
            o["color"] = color
        out.append((p, [x0, int(round(y)), x1, int(round(y)) + h], o))
        y += h + gap * lh
    return out, int(round(y - gap * lh))


def _rerase(*boxes, **kw):
    """erase-only line: the JP rows in these boxes go (texfill on paper unless method= is given)."""
    o = {"erase": [list(b) for b in boxes]}
    o.update(kw)
    return ("", list(boxes[0]), o)


def _rtitle(text, y0, y1, size=34):
    return (text, [8, y0 - 4, 792, y1 + 6], {"max_size": size, "align": "center", "erase": [[8, y0 - 3, 792, y1 + 3]]})


def _rfoot(date, y_date, y_sig, x0=16, size=21):
    """date + signature lines (JP rows start at y_date / y_sig, 22-27 px tall)."""
    return [(date, [x0, y_date - 2, 560, y_date + 28], {"max_size": size, "erase": [[x0 - 6, y_date - 4, 600, y_date + 31]]}),
            (_SIG, [x0, y_sig - 2, 792, y_sig + 28], {"max_size": size, "erase": [[x0 - 6, y_sig - 4, 600, y_sig + 31]]})]


def _rcell(text, x0, y0, x1, y1, size=16, align="center", pad=4, method="inpaint"):
    """a table cell between rules x0/x1, y0/y1: erase 4 px inside the rules, set the English with `pad` margin."""
    return (text, [x0 + pad, y0 + 2, x1 - pad, y1 - 1],
            {"max_size": size, "align": align, "method": method, "erase": [[x0 + 4, y0 + 4, x1 - 3, y1 - 3]]})


_SIG = "Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki"   # = lane B wording

# ---- 190 "Orders to Analyze Droga" (800x1578): title, P1-P2, photo (art, kept), caption, P3-P4, two photographed letter
# halves (ref 10's letter: the right photo = its first half, the left photo = the rest + signature; the shipped ref-10
# English L10 is set in the photos, split where the JP photos split, mid-sentence), caption, date, signature.
R190_P = [
    "In the Arata settlement, from which we originate, something like this reportedly happened more than fifty years "
    "ago. A single messenger from the Arata settlement came to Tokyo. At the time, he introduced Droga to the "
    "government of the day as a powerful weapon. However, the Arata settlement's scheme apparently did not go well, "
    "and he was reportedly urged, politely, to return home. It seems he could not even hand over the medicine.",
    "Just when one thought they had thrown Droga away several hundred years ago, the people of Arata are once again "
    "living lives that rely on Droga. What senseless, foolish people. Unchanged since ancient times, they must surely "
    "be using it for their own desires.",
]
R190_Q = [
    "Incidentally, Kichizo-sama has given the following instruction: \"Determine why Droga has such effects.\" "
    "Kichizo-sama has said that he graduated from a university in the physical and chemical sciences. Indeed, it is "
    "only natural that a person of such a background would wish to consider even a sacred treasure such as Droga from "
    "a scientific angle.",
    "A preliminary investigation found that the young man from the Arata settlement who came to Tokyo at that time "
    "very likely fell in love with a girl living in Tokyo and went to the Arata settlement with her, and that the girl "
    "of that time is apparently still alive and serving as the settlement's head. I will visit her shortly to "
    "negotiate, so that the transaction may be made as peacefully as possible.",
]
_k190 = L10.index("lose to anything of that sort")
_p190a, _e190a = _rflow(R190_P, 20, 788, 106, 20)
_p190b, _e190b = _rflow(R190_Q, 20, 788, 812, 20)
_ph190r, _ = _rflow([L10[:_k190].strip()], 442, 776, 1118, 12, ls=0.93, gap=0, color="#2b2b2b")
_ph190l, _ = _rflow([L10[_k190:].strip()], 44, 390, 1118, 12, ls=0.93, gap=0, color="#2b2b2b")
REP190 = ([_rtitle("Orders to Analyze Droga", 27, 63),
           _rerase([14, 116, 792, 360]),
           ("The Arata settlement, photographed Shiyo 728, September", [60, 752, 740, 787],
            {"max_size": 21, "align": "center", "erase": [[200, 755, 600, 784]]}),
           _rerase([14, 815, 792, 1089]),
           _rerase([40, 1115, 395, 1367], mask_color=[0, 95, 0, 95, 0, 95], mask_grow=2),
           _rerase([436, 1114, 780, 1367], mask_color=[0, 95, 0, 95, 0, 95], mask_grow=2),
           ("Nagamoto Asahi", [200, 1346, 390, 1365], {"max_size": 12, "align": "right", "color": "#2b2b2b", "erase": []}),
           ("A letter by a retainer of the Magawa house, circa Shiyo 310", [40, 1390, 760, 1425],
            {"max_size": 21, "align": "center", "erase": [[180, 1393, 620, 1422]]})]
          + _p190a + _p190b + _ph190r + _ph190l + _rfoot("Shiyo 729, March 15", 1488, 1518))

# ---- 191 "Arata Settlement Survey Findings" (800x1033)
R191_P = [
    "I went to the Arata settlement and promptly conducted the negotiation in question. As we had heard, the girl who "
    "had lived in Tokyo was alive, and I was able to hear the details. When I asked for her cooperation, she agreed "
    "surprisingly readily. According to her, \"That medicine is no longer used now, but it is written about in "
    "documents from long ago. You should refer to those.\" She also said we may take as many of the cherry trees as we "
    "need. I made sure to point out that most of the cherry trees here might be gone, but apparently she does not mind "
    "even so.",
    "This time we withdrew after this negotiation alone; at a later date we will collect the documents and have her "
    "provide several of the cherry trees we need as initial samples. We must also consider how large a budget we can "
    "obtain from the state for transporting the cherry trees and for the research.",
]
R191_Q = [
    "However, a settlement in such a remote land, which had had almost no contact with the outside, was strangely "
    "cooperative with us. Might they too have some purpose of their own?",
]
_p191a, _e191a = _rflow(R191_P, 22, 784, 95, 22)
_p191b, _e191b = _rflow(R191_Q, 22, 784, 822, 22)
REP191 = ([_rtitle("Arata Settlement Survey Findings", 26, 64),
           _rerase([14, 97, 792, 431]),
           ("The Arata settlement's cherry tree against the full moon", [60, 762, 740, 796],
            {"max_size": 21, "align": "center", "erase": [[215, 764, 592, 794]]}),
           _rerase([14, 824, 792, 916])]
          + _p191a + _p191b + _rfoot("Shiyo 729, April 11", 949, 979))

# ---- 127 "Comparison of Methods of Use" (800x1161): P1-P4, lead-in line, 3x8 table (rules x 66 173 430 738,
# y 715 745 775 806 836 867 897 928 958), P5.
R127_P = [
    "Among us, Droga is a sacred implement that only the chosen may use. Our brethren honor their faith and accumulate "
    "virtue so that they may obtain permission to use this sacred implement. Therefore, when we called for test "
    "subjects for this research, many came forward.",
    "First, we had three of our brethren inhale the extracted crystals, burned and vaporized, whereupon a state of "
    "euphoria and muscular strength unthinkable under normal conditions were obtained. However, in the state of "
    "euphoria they would hardly listen to what we said, and one whose behavior deviated especially markedly was knocked "
    "unconscious with an electric shock. The other two gradually regained their composure, and their muscular strength "
    "also returned to normal.",
    "As things stood, even if we brought many cherry trees from Arata and mass-produced it, we could not let our "
    "brethren use it widely. It was first necessary to suppress this state of euphoria and improve it so that they "
    "could act as instructed.",
    "We therefore tried several methods, and by liquefying the drug and injecting it into the muscle, we were able to "
    "control the state of euphoria considerably and to strengthen the increase in muscular strength further. In this "
    "form, however, the number of people it can be given to is limited compared with vaporization, and the duration of "
    "the strength increase also falls to a fraction. An amount that would serve a thousand people by vaporization is "
    "estimated to serve about ten by liquid injection.",
    "Below is a comparison table of vaporization and liquefaction.",
]
_p127, _e127 = _rflow(R127_P, 20, 784, 97, 21)
_y127 = [715, 745, 775, 806, 836, 867, 897, 928, 958]
_t127 = [("", "Vaporization", "Liquefaction"),
         ("Method of use", "Crystals burned directly over fire", "Intramuscular injection"),
         ("No. of users", "Many", "Few"),
         ("Duration", "About 1 hour", "10-15 min"),
         ("Euphoria", "High", "Medium"),
         ("Strengthening", "High", "Extremely high"),
         ("Productivity", "Good", "Fairly good"),
         ("Drawbacks", "Euphoria", "Productivity; excessive muscle strengthening")]
_c127 = []
for _r, _row in enumerate(_t127):
    for _c, (_xa, _xb) in enumerate(((66, 173), (173, 430), (430, 738))):
        if _row[_c]:
            _c127.append(_rcell(_row[_c], _xa, _y127[_r], _xb, _y127[_r + 1], size=15 if _c == 0 else 17, align="left", pad=6))
REP127 = ([_rtitle("Comparison of Methods of Use", 27, 63),
           _rerase([14, 98, 792, 703]),
           _rerase([14, 975, 792, 1036])]
          + _p127 + _c127
          + _rflow(["Each has its merits and demerits, but if mass production of the drug is possible, liquefied "
                    "injection can be called the more practical."], 20, 784, 975, 21)[0]
          + _rfoot("Shiyo 729, May 1", 1070, 1100))

# ---- 128 "Test Report on Droga Administration Experiments" (800x2650): method list, three 6-column tables (rules
# x 38 194 357 469 581 695 762; 11 rows of 34.55 px from y 301 / 777 / 1680), two copies of a run-together heading
# line, P1-P4. Only the cells with Japanese are re-set (subject, 100 m time, prognosis, the header row); the
# cm / kg / acuity cells are Latin digits already and stay as drawn.
R128_M = [
    "Method",
    "1.  Conduct the physical tests described below on 10 brethren in good health (designated Test \"Normal\")",
    "2.  1 hour after Normal, inject the prescribed amount, about 5 ml, intramuscularly into the same brethren",
    "3.  5 minutes after the injection, conduct physical tests equivalent to 1 (designated Test \"Modified\")",
    "4.  Observe the prognosis of the brethren who underwent Modified",
]
R128_P = [
    "Judging by the experimental results, everyone's physical abilities improved to a degree unthinkable under normal "
    "conditions. They produced results far greater than the theoretical limit of muscular strength, and that state "
    "continued for about 10-15 minutes. Immediately afterward, however, half of the brethren died of heart attacks, "
    "and several suffered fractures throughout the body or ruptured internal organs and died. 4 survived, though "
    "seriously injured. Experiments by vaporized inhalation were also carried out; since the subjects did not move as "
    "ordered, they did not yield accurate data, but the impression was that their physical abilities were somewhat "
    "lower than with liquid injection.",
    "When vaporized, the users do not obey orders because of the state of euphoria; with liquid injection, the "
    "excessive muscle strengthening leaves them severely ill or dead. Practical use seems possible by suppressing the state "
    "of euphoria, or by cautioning users in advance not to overuse their strength. We therefore experimented further "
    "with liquid injection after giving the instruction \"Do not overuse your strength,\" whereupon:",
]
R128_Q = [
    "Although physical ability was somewhat lower, the results still far exceeded those of ordinary humans, and none "
    "of the brethren suffered harm to their health of a severe degree or worse. It can therefore be said that liquid "
    "injection after instructing \"Do not exert too much strength\" is the appropriate method.",
    "As an aside, in the Middle Ages it was used mainly by inhaling the gas rather than by injection, so deaths from "
    "excessive muscle strengthening such as this were probably rare. Also, in battles fought with swords as in the "
    "old days, keeping the users in a state of euphoria and having them charge the enemy without being seized by fear "
    "would have been the more efficient tactic. But when vehicles and firearms are used, as now, a state in which they "
    "can be instructed to act according to the plan is required. Of course, it goes without saying that "
    "sophisticated strategies were carried out in the battles of old too, but in the end an all-out fight by the "
    "soldiers was still necessary, so a state of euphoria was probably acceptable to a certain degree.",
]
R128_H = "Subject 100-Meter Dash Vertical Jump Weight Hold Dynamic Visual Acuity Prognosis"
_x128 = [38, 194, 357, 469, 581, 695, 762]
_L128 = "ABCDEFGHIJ"
_S128 = "mmmmmfffff"
_T128 = [  # (ages, 100 m seconds, prognosis) per table
    ([22, 18, 40, 56, 10, 41, 32, 9, 17, 60],
     ["13.55", "15.01", "16.79", "21.00", "20.15", "18.56", "15.83", "28.91", "16.22", "23.35"], ["Good"] * 10),
    ([22, 18, 40, 56, 10, 41, 32, 9, 17, 60],
     ["2.01", "2.55", "2.99", "3.87", "5.19", "4.85", "4.21", "6.15", "3.02", "6.46"],
     ["Dead", "Dead", "Dead", "Dead", "Severe", "Dead", "Severe", "Severe", "Dead", "Severe"]),
    ([23, 16, 44, 57, 11, 43, 31, 8, 19, 64],
     ["4.98", "5.01", "5.56", "5.99", "7.05", "7.01", "6.55", "7.61", "5.33", "7.01"], ["Good"] * 10),
]


def _r128_table(top, ages, secs, prog):
    ys = [int(round(top + 34.55 * k)) for k in range(12)]
    out = []
    for c, h in enumerate(("Subject", "100-Meter Dash", "Vertical Jump", "Weight Hold", "Dynamic Visual Acuity",
                           "Prognosis")):
        out.append(_rcell(h, _x128[c], ys[0], _x128[c + 1], ys[1], size=15))
    for r in range(10):
        sex = "male" if _S128[r] == "m" else "female"
        out.append(_rcell("%s (%s, age %d)" % (_L128[r], sex, ages[r]), _x128[0], ys[r + 1], _x128[1], ys[r + 2], size=16))
        out.append(_rcell("%s sec" % secs[r], _x128[1], ys[r + 1], _x128[2], ys[r + 2], size=17))
        out.append(_rcell(prog[r], _x128[5], ys[r + 1], _x128[6], ys[r + 2], size=17))
    return out


_m128, _ = _rflow(R128_M, 16, 784, 112, 18, gap=0.15)
_p128, _e128a = _rflow(R128_P, 16, 784, 1192, 20)
_q128, _e128b = _rflow(R128_Q, 16, 784, 2097, 20)
REP128 = ([_rtitle("Test Report on Droga Administration Experiments", 21, 52, size=33),
           _rerase([10, 114, 792, 291]),
           (R128_H, [12, 722, 792, 760], {"max_size": 19, "erase": [[10, 727, 600, 757]]}),
           _rerase([10, 1194, 792, 1545]),
           (R128_H, [12, 1627, 792, 1665], {"max_size": 19, "erase": [[10, 1632, 600, 1661]]}),
           _rerase([10, 2099, 792, 2479])]
          + _m128 + _p128 + _q128
          + _r128_table(301, *_T128[0]) + _r128_table(777, *_T128[1]) + _r128_table(1680, *_T128[2])
          + _rfoot("Shiyo 729, June 10", 2510, 2539))

# ---- 138 "Side Effects of Droga" (800x879)
R138_P = [
    "Recently, several of the staff who attended the experiments have complained of \"hallucinations and hearing "
    "things.\" They say they can see dangers about to befall themselves, and the look of death on other people. All of "
    "them alike complain of lethargy, nausea and loss of appetite. Not all the staff who attended the experiments have "
    "such symptoms; only a few of them do. Strangely, the test subjects have no hallucinations or hearing of things; "
    "these occur only in the staff who attended.",
    "Upon investigating this, I was able to find interesting material. It says that precognitives occasionally appear "
    "in the Arata settlement, and that their precognition is limited to danger sense. Since the symptoms are extremely "
    "similar, such precognitives are likely to appear around Droga users. The conditions are unknown, but it is "
    "certain at least that Droga is not merely a drug that boosts muscular strength.",
    "Also, among those who gain precognition, the iris of one eye reportedly sometimes turns green (none of those who "
    "attended the experiments has developed a green eye). In any case, using Droga as a muscle-strengthening drug will "
    "require more detailed verification.",
]
_p138, _e138 = _rflow(R138_P, 34, 778, 100, 25)
REP138 = ([_rtitle("Side Effects of Droga", 11, 47), _rerase([28, 100, 792, 765])] + _p138
          + _rfoot("Shiyo 730, April 1", 805, 840, x0=36, size=23))

# ---- 139 "Experiments in Creating Precognitives" (800x1411): P1-P3, Venn diagram (3 nested circles, labels re-set
# inside their rings; the circles are not erased), P4-P5.
R139_P = [
    "We have pinned down the conditions for gaining the danger sense in question. During the liquid-injection "
    "experiments, since a state of euphoria like that from vaporized inhalation might appear, we had as many as 50 "
    "staff attend for 10 brethren. This was so that they could be restrained even if the brethren went on a rampage "
    "in a state of euphoria.",
    "After the experiments, the brethren died or were seriously injured through compound fractures, severed limbs, "
    "ruptured internal organs and the like, and some of them bled heavily at the time. The staff who attended the "
    "experiments carried their bodies and treated them, and in doing so touched the brethren's blood.",
    "However, not everyone who touched the blood gained precognition; there must be some further condition there as "
    "well. At least, everyone who gained danger sense had touched the brethren's blood, and among those who did not "
    "touch the blood, no staff member gained danger sense. Shown as a Venn diagram, it is as follows.",
]
R139_Q = [
    "Thus, contact with the brethren's blood is necessary to gain the power of danger sense, but it is not always "
    "gained.",
    "Here I wish to make a new proposal. If Droga could be used not as a muscle-strengthening agent but as a danger-sense "
    "inducer, it should be of great use as well. From now on, I wish to treat Droga as something that induces danger "
    "sense and to advance the research.",
]
_p139a, _e139a = _rflow(R139_P, 14, 784, 100, 23)
_p139b, _e139b = _rflow(R139_Q, 14, 784, 1082, 23)
REP139 = ([_rtitle("Experiments in Creating Precognitives", 12, 48),
           _rerase([8, 100, 794, 590]), _rerase([8, 594, 120, 624]),
           ("50 staff", [320, 672, 510, 704], {"max_size": 20, "align": "center", "method": "inpaint",
                                               "erase": [[364, 675, 464, 701]]}),
           ("Touched the subjects' blood", [318, 760, 540, 815], {"max_size": 20, "align": "center", "method": "inpaint",
                                                                  "erase": [[334, 761, 494, 788], [389, 788, 440, 814]]}),
           ("Gained the power of danger sense", [326, 895, 524, 954],
            {"max_size": 20, "align": "center", "method": "inpaint", "erase": [[334, 898, 494, 924], [389, 925, 436, 951]]}),
           _rerase([8, 1082, 794, 1291])]
          + _p139a + _p139b + _rfoot("Shiyo 730, April 7", 1330, 1365, x0=14, size=23))

# ---- 154 "Conditions for Creating Precognitives" (800x1519): P1-P2, 2-column table (rules x 53 249 750; rows at
# y 406 444 482 520 587 625 663 760 798 865 903 970 1008 1075 1113 1181; 4 full-width section rows), P3.
R154_P = [
    "After permission was granted to research Droga as a danger-sense inducer, we first examined under what "
    "conditions danger sense can be gained. Because we examined it from many angles, including the amount of blood, "
    "the body part touched and the time since bleeding, this report is several days later than planned, for which I "
    "offer my apologies here.",
    "That this report is being submitted means we succeeded in pinning down the conditions for gaining danger sense, "
    "but in fact those conditions are extremely strict. Below is a table summarizing them.",
]
R154_Q = [
    "Thus, inducing danger sense in fact requires fiercely strict conditions. We will carry out further verification "
    "of whether it is truly practical under these conditions. If this is put to practical use, we of the Holy Cerejeira "
    "Church will truly gain the divine power called precognition.",
]
_y154 = [406, 444, 482, 520, 587, 625, 663, 760, 798, 865, 903, 970, 1008, 1075, 1113, 1181]
_t154 = [("Conditions for Acquiring the Power of Danger Sense",),
         ("Blood contact site", "Mucous membranes of the head (eyes, lips, etc.)"),
         ("Contact amount", "1 ml or more"),
         ("Time limit", "Within 10 seconds of bleeding, or the blood temperature must be 32 degrees Celsius or higher"),
         ("Conditions for Inducing Danger Sense",),
         ("Air", "Must contain cherry pollen"),
         ("Degree of sealing", "Not possible inside a completely sealed space, even with cherry pollen present. "
                               "However, possible if there is even the slightest gap of less than 1 millimeter."),
         ("Other condition 1", "Reproduce the situation in which the blood was touched"),
         ("Other condition 2", "Perceive the person meeting danger through some sense, such as the eyes or ears"),
         ("Side Effects",),
         ("Ill health", "Lethargy, fatigue, dizziness, nausea, loss of appetite"),
         ("Conditions for ill health", "Same as the danger-inducing conditions above"),
         ("Other", "Exposure to the above danger-inducing conditions for 15 minutes or more causes ill health"),
         ("Other",),
         ("Time until precognition", "Induced immediately once the above danger-inducing conditions are met.")]
_c154 = []
for _r, _row in enumerate(_t154):
    _ya, _yb = _y154[_r], _y154[_r + 1]
    if len(_row) == 1:
        _c154.append(_rcell(_row[0], 53, _ya, 750, _yb, size=19))
    else:
        _c154.append(_rcell(_row[0], 53, _ya, 249, _yb, size=17, align="left", pad=8))
        _c154.append(_rcell(_row[1], 249, _ya, 750, _yb, size=19, align="left", pad=8))
_p154a, _e154a = _rflow(R154_P, 12, 784, 100, 24)
_p154b, _e154b = _rflow(R154_Q, 12, 784, 1222, 24)
REP154 = ([_rtitle("Conditions for Creating Precognitives", 11, 48),
           _rerase([6, 100, 794, 380]), _rerase([6, 1222, 794, 1397])]
          + _p154a + _c154 + _p154b + _rfoot("Shiyo 730, April 16", 1436, 1471, x0=12, size=23))


def _rjob(rid, lines, note):
    return {"id": "rep%d-whole" % rid, "screen": "reference %d finished report" % rid, "style": "serif", "mode": "lines",
            "erase": "texfill", "erase_first": True, "mask_grow": 2, "mask_color": _RMASK, "color": _RINK, "new": True,
            "note": note, "items": [(D + "rrr%d/全体.gal" % rid, "")],
            "lines": [(t, b, dict({"mask_color": _RMASK}, **o)) for t, b, o in lines]}


JOBS += [
    _rjob(190, REP190, "report No.1 (photo kept; the two letter photos carry ref 10's English)"),
    _rjob(191, REP191, "report No.2 (photo kept)"),
    _rjob(127, REP127, "report No.3 (comparison table)"),
    _rjob(128, REP128, "report No.4 (three result tables; cm / kg / acuity digits kept)"),
    _rjob(138, REP138, "report No.5"),
    _rjob(139, REP139, "report No.6 (Venn diagram circles kept)"),
    _rjob(154, REP154, "report No.7 (conditions table)"),
]
JOBS += [{"id": "rep%d-ov" % _i, "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr%d.gal" % _i, "")]} for _i in (190, 191, 127, 128, 138, 139, 154)]

# ---- 163 (No.10) 800x2113: title, 5 paragraphs, two photos with captions, a diagram (two figures, black arrow),
# date, signature.
L163 = [
    ("On the Native Habitat of the Arata Cherry", [20, 4, 780, 56], dict(_RBL, max_size=36, erase=[[183, 7, 620, 53]])),
    ("Last time, we reported that spores are contained in Droga and in the blood of the first generation and others. "
     "From here we split into two teams and decided to study Droga and the ecology of the Arata cherry separately. "
     "This time, the report concerns the ecology of the Arata cherry. The Arata cherry is a cherry that grows wild "
     "only in the Arata district, and its appearance closely resembles the Somei Yoshino. The way it blooms in "
     "spring and quickly scatters is exactly the cherry as we think of it. We checked whether that cherry contains "
     "spores.",
     [12, 118, 788, 406], dict(_RBB, erase=[[8, 123, 790, 403]])),
    ("Somei Yoshino", [60, 698, 340, 731], dict(_RBL, max_size=23, erase=[[116, 700, 285, 729]])),
    ("Arata cherry", [470, 698, 740, 731], dict(_RBL, max_size=23, erase=[[556, 698, 649, 730]])),
    ("As a result, spores were found in the air and in the roots, a decisive difference from the Somei Yoshino. "
     "Because of this, we must re-examine from the start whether the Arata cherry is truly an angiosperm of the "
     "rose family. For it is possible that the Arata cherry is no angiosperm at all, but a fungus or a fern "
     "mimicking a cherry. In that case, the muscle strengthening from Droga and the second generation's danger "
     "sense would be the same as saying that they are deeply tied to the Arata cherry's life history, that is, to "
     "its reproduction and growth. In other words, the fact that spores were found inside the bodies of the second "
     "generation means that the Arata cherry is spreading its reproductive range by some method.",
     [12, 752, 788, 1110], dict(_RBB, erase=[[8, 756, 778, 1106]])),
    ("Droga\n(spores)", [8, 1200, 140, 1272], dict(_RBL, max_size=22, erase=[[36, 1203, 146, 1270]])),  # SWEEP-PIC: box to x 146 = the last kana
    ("Reproduction?", [352, 1226, 474, 1271], _rbw("#010101", max_size=22, erase=[[352, 1226, 452, 1271]])),
    ("First generation\n(intermediate host)", [80, 1388, 370, 1460], dict(_RBL, max_size=23, erase=[[150, 1390, 296, 1458]])),
    ("Second generation\n(intermediate host?)", [455, 1388, 765, 1460], dict(_RBL, max_size=23, erase=[[517, 1390, 692, 1458]])),
    ("There is a possibility of reproductive activity by the Arata cherry", [20, 1490, 780, 1528],
     dict(_RBL, max_size=23, erase=[[150, 1493, 651, 1526]])),
    ("We must be careful. Droga was originally a sacred implement, given only to brethren chosen for having "
     "accumulated virtue. However, spores are seeds used for reproduction. For, in short, it would be no "
     "exaggeration to say that we are being parasitized by the Arata cherry.",
     [12, 1560, 788, 1705], dict(_RBB, erase=[[8, 1565, 778, 1704]])),
    ("To offer a simple consideration: the Arata cherry can be called a variety that offers mammals, humans "
     "included, the attraction of gaining muscle strengthening by ingesting its spores, and in exchange enters "
     "their bodies and accomplishes reproduction. However, at present, the Arata cherry is not showing such "
     "reproductive movement.",
     [12, 1705, 788, 1880], dict(_RBB, erase=[[8, 1706, 778, 1879]])),
    ("We know that this consideration goes against our doctrine, but Kichizo-sama said that he wishes to analyze "
     "Droga scientifically. He must have something in mind.",
     [12, 1881, 788, 1988], dict(_RBB, erase=[[8, 1882, 778, 1985]])),
    ("Shiyo 730, October 10", [12, 2020, 500, 2056], dict(_RBB, erase=[[8, 2022, 275, 2055]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [12, 2056, 790, 2092],
     dict(_RBB, erase=[[8, 2057, 564, 2090]])),
]
JOBS += [_rbjob(163, "report No.10 (parchment; photos and diagram kept)", L163)]
# rr163 card = imgRB/ovcard.py 163 "On the Native Habitat of the Arata Cherry" 4 104 114 34 none.
JOBS += [{"id": "rep163-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr163.gal", "")]}]

# ---- 169 (No.11) 800x2607: title, paragraphs, a 3-line list, two generation diagrams, a ruled table (rules at
# y 1022/1066/1110/1154/1198/1242/1286/1329, x 31/291/534/777: one English string per cell, erased inside the cell),
# date, signature. The rr169 card shows no text (art only): not built.
_T169 = [("", "Second generation", "Third generation"), ("Cherry pollen", "Required", "Required"),
         ("Enclosed space", "Ineffective", "Ineffective"), ("Re-creating the blood application", "Required", "Not required"),
         ("Ill health", "Yes", "No"), ("Sex", "Any", "Women only"), ("Age", "Any", "Ineffective in young children")]
_Y169 = [1022, 1066, 1110, 1154, 1198, 1242, 1286, 1329]
_X169 = [31, 291, 534, 777]
L169 = [
    ("Extending the Generations", [20, 4, 780, 56], dict(_RBL, max_size=36, erase=[[299, 6, 505, 52]])),
    ("Spores were detected in the bodies of the first and second generations, but so far there is no sign of them "
     "germinating. It is unknown whether they merely entered the human body by mistake or whether they originate "
     "from the Arata cherry. However, if spores have been found in every member of the first and second "
     "generations, it would not be strange to conclude that they come from the Arata cherry. On the basis of this "
     "theory, we will pin down the germination conditions of the Arata cherry.",
     [12, 84, 788, 333], dict(_RBB, erase=[[6, 88, 778, 332]])),
    ("As with the second generation, we applied the blood of the second generation to the lips of test subjects and "
     "observed the progress. As a result, the subjects likewise gained the ability to foresee danger. These "
     "subjects are designated the third generation. Summarizing the conditions under which each generation arises:",
     [12, 333, 788, 474], dict(_RBB, erase=[[8, 334, 778, 472]])),
    ("First generation: ingests Droga\n"
     "Second generation: touches the blood of the first generation with a mucous membrane of the head\n"
     "Third generation: touches the blood of the second generation with a mucous membrane of the head",
     [10, 506, 792, 616], dict(_RBB, erase=[[6, 509, 630, 613]])),
    ("Droga", [4, 656, 134, 688], dict(_RBL, max_size=22, erase=[[22, 658, 132, 686]])),
    ("Blood", [214, 731, 330, 781], _rbw("#010101", erase=[[216, 731, 312, 781]])),
    ("Blood", [482, 731, 598, 781], _rbw("#010101", erase=[[484, 731, 581, 781]])),
    ("First generation", [40, 862, 270, 898], dict(_RBL, erase=[[93, 864, 215, 896]])),
    ("Second generation", [305, 862, 541, 898], dict(_RBL, erase=[[362, 864, 484, 896]])),
    ("Third generation", [575, 862, 798, 898], dict(_RBL, erase=[[629, 864, 752, 896]])),
    ("However, the conditions under which danger sense arises differ from those of the second generation. The "
     "following table summarizes those differences.",
     [12, 928, 788, 1004], dict(_RBB, erase=[[8, 931, 778, 999]])),
]
for _r, _row in enumerate(_T169):
    for _c, _t in enumerate(_row):
        if _t:
            _x0, _x1, _y0, _y1 = _X169[_c], _X169[_c + 1], _Y169[_r], _Y169[_r + 1]
            L169.append((_t, [_x0 + 10, _y0 + 3, _x1 - 6, _y1 - 3],
                         dict(_RBB, line_spacing=1.0, erase=[[_x0 + 4, _y0 + 4, _x1 - 3, _y1 - 3]])))
L169 += [
    ("Thus, the second generation requires re-creating the situation of the blood application, while in the third "
     "generation only adult women came to gain precognition. Also, as a physical feature, a phenomenon occurred in "
     "which those who became the third generation had one eye turn green. The turning green does not depend on sex "
     "or age. Considering this, young girls who became the third generation may gain precognition when they grow "
     "up. However, even at this stage no reproduction of the Arata cherry is seen. Also, spores of the Arata cherry "
     "were detected in the third generation as well.",
     [12, 1348, 788, 1632], dict(_RBB, erase=[[8, 1352, 785, 1631]])),
    ("Likewise, it was expected that applying the blood of those who had become the third generation to a mucous "
     "membrane of the head would this time produce a fourth generation. When this experiment was carried out, no "
     "so-called fourth generation arose; there was no physical change and no precognition was gained. Nor were "
     "spores or biological fragments detected in the body. Besides blood contact, we also tried saliva, lymph, "
     "semen, spinal fluid and the like, as well as cell transplant surgery, but none yielded a significant result.",
     [12, 1632, 788, 1880], dict(_RBB, erase=[[6, 1633, 778, 1877]])),
    ("Droga", [2, 1988, 100, 2014], dict(_RBL, max_size=17, erase=[[12, 1990, 96, 2013]])),
    ("Blood", [167, 2046, 240, 2086], _rbw("#010101", max_size=18, erase=[[168, 2046, 232, 2086]])),
    ("Blood", [355, 2051, 425, 2090], _rbw("#010101", max_size=18, erase=[[356, 2051, 418, 2090]])),
    ("Blood", [549, 2049, 620, 2088], _rbw("#010101", max_size=18, erase=[[550, 2049, 612, 2088]])),
    ("First generation", [10, 2146, 212, 2180], dict(_RBL, max_size=23, erase=[[50, 2147, 170, 2179]])),
    ("Second generation", [216, 2146, 414, 2180], dict(_RBL, max_size=23, erase=[[255, 2147, 375, 2179]])),
    ("Third generation", [418, 2146, 600, 2180], dict(_RBL, max_size=23, erase=[[442, 2147, 562, 2179]])),
    ("Nothing happened", [602, 2146, 794, 2180], dict(_RBL, max_size=23, erase=[[606, 2147, 784, 2179]])),
    ("If the transmission of these spores is tied to the life history of the Arata cherry, reproductive activity "
     "should be seen by some method. Whether it reproduces within the first to third generations, or whether a "
     "fourth generation arises by a method different from those so far, further research is needed. However, we "
     "cannot use any more of our brethren for this experiment. We still cannot see the bottom of where using Droga "
     "will lead us.",
     [12, 2226, 788, 2476], dict(_RBB, erase=[[8, 2230, 785, 2474]])),
    ("Shiyo 731, January 9", [12, 2509, 500, 2545], dict(_RBB, erase=[[6, 2511, 238, 2544]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [12, 2545, 790, 2581],
     dict(_RBB, erase=[[8, 2546, 563, 2579]])),
]
JOBS += [_rbjob(169, "report No.11 (parchment; diagrams and table rules kept)", L169)]

# ---- 171 (No.12) 800x729: title, 4 paragraphs, date, signature.
L171 = [
    ("Change in Research Policy", [20, 4, 780, 58], dict(_RBL, max_size=36, erase=[[262, 8, 545, 54]])),
    ("By Kichizo-sama's decision, Droga is no longer to be treated as a sacred implement. With this, there is no "
     "longer any point in continuing the research on Droga.",
     [12, 86, 788, 194], dict(_RBB, erase=[[8, 89, 778, 192]])),
    ("In ancient times, the use of Droga was forbidden in the Arata settlement by the Grand Witch of the time. The "
     "faction that opposed this, that is, our ancestors, took Droga out of the Arata settlement and built the "
     "foundation of the Holy Cerejeira Church in the land of Megasawa. As for why it was forbidden, the reason may be that "
     "they had realized that humans could be used, as here, as tools for the reproduction of an unknown organism.",
     [12, 194, 788, 404], dict(_RBB, erase=[[8, 194, 778, 402]])),
    ("And Kichizo-sama told us to continue elucidating further whether there is any danger beyond humans being made "
     "tools for reproduction. However, because of research of this kind, not a few of our brethren have been "
     "sacrificed, and the scale of the research has no choice but to be reduced.",
     [12, 404, 788, 544], dict(_RBB, erase=[[8, 405, 778, 543]])),
    ("In any case, we will settle on a policy centered on research into the Arata cherry and draw up our future "
     "plans.",
     [12, 544, 788, 616], dict(_RBB, erase=[[8, 545, 785, 613]])),
    ("Shiyo 731, March 2", [12, 648, 500, 684], dict(_RBB, erase=[[8, 650, 240, 683]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [12, 684, 790, 720],
     dict(_RBB, erase=[[8, 685, 565, 718]])),
]
JOBS += [_rbjob(171, "report No.12 (parchment)", L171)]
# rr171 card = imgRB/ovcard.py 171 "Change in Research Policy" 4 84 86 34 brown (the brown brush graffiti is kept as drawn).
JOBS += [{"id": "rep171-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr171.gal", "")]}]

# ---- 174 (No.13) 800x1490: title, 2 paragraphs (smaller type, 24 px glyphs), two photos with captions (the "30μ"
# scale label inside photo 2 kept), date, signature. The 発狂しし doubling in the source is read as 発狂し.
L174 = [
    ("Post-Mortem of the Third Generation", [20, 18, 780, 72], dict(_RBL, max_size=36, erase=[[256, 21, 550, 68]])),
    ("Two years have passed since we began research on Droga and the Arata cherry, but owing to budget and staffing "
     "there have been no particularly favorable results, and we have done nothing but literature research and "
     "verification of the Arata cherry's ecology. However, the other day, one of the third-generation members who "
     "had been cooperating with the experiments suddenly went on a rampage and killed second- and third-generation "
     "brethren one after another. The situation was brought under control about 10 minutes after the attendants "
     "noticed. After that, the third-generation brethren went mad. In this incident, 3 of the second generation and "
     "2 of the third generation died. The first generation suffered no harm.",
     [20, 74, 785, 334], dict(_RBB, erase=[[16, 98, 795, 309]])),
    ("The room after the incident", [20, 700, 780, 736], dict(_RBL, max_size=22, erase=[[322, 703, 482, 733]])),
    ("Why this happened is unknown, but when, as a precaution, we performed a post-mortem on the third-generation "
     "member who went on the rampage, countless very small buds had grown on the surface of the skin. In size, they "
     "were about 100 to 200 microns (0.1 to 0.2 mm). And spores were further being dispersed from those buds. The "
     "true nature of these spores will be reported later, as soon as the research is complete.",
     [20, 752, 785, 958], dict(_RBB, erase=[[16, 794, 780, 944]])),
    ("Buds detected on the skin of a dead third-generation member.\n"
     "At the tips of the string-like parts are spherical sporangia.",
     [20, 1304, 780, 1372], dict(_RBL, max_size=22, erase=[[146, 1308, 646, 1368]])),
    ("Shiyo 731, March 25", [20, 1396, 500, 1430], dict(_RBB, max_size=22, erase=[[17, 1399, 259, 1428]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [20, 1430, 790, 1464],
     dict(_RBB, max_size=22, erase=[[18, 1429, 499, 1459]])),
]
JOBS += [_rbjob(174, "report No.13 (parchment; photos and the 30μ scale kept)", L174)]
# rr174 card = imgRB/ovcard.py 174 "Post-Mortem of the Third Generation" 6 78 80 34 red (the red painted 1015の kept as drawn).
JOBS += [{"id": "rep174-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr174.gal", "")]}]

# ---- 176 (No.14) 800x1581: title, 2 paragraphs, a photo of a brush heading 翠眼呪殺 (inpainted on the dark photo
# ground, English set in the serif face like the calligraphy letters; the two faint, cropped handwritten lines under it
# are below legibility in the original and stay as drawn), a snail photo with caption, date, signature.
L176 = [
    ("Old Records and the Green-Eye Curse-Killing", [20, 18, 780, 72], dict(_RBL, max_size=36, erase=[[257, 21, 550, 69]])),
    ("Alongside our research on the third generation, we had also been investigating the old records of the Arata "
     "settlement. Do you remember the \"green eye\" we reported earlier? Among those records there was a very "
     "interesting account. There is a legend called the \"Green-Eye curse-killing,\" and it said, \"Raise a boy "
     "born with green eyes as he is, and kill a girl born with green eyes at once.\" Considering this sentence "
     "alone, it is thought that, because a green-eyed girl is a being who will one day bring calamity, the "
     "instruction to kill her at once was handed down.",
     [20, 76, 785, 318], dict(_RBB, erase=[[16, 98, 782, 309]])),
    ("Green-Eye Curse-Killing", [205, 385, 515, 480],
     {"method": "inpaint", "mask_color": [0, 42, 0, 40, 0, 36], "max_size": 46, "align": "center", "color": "#151310",
      "erase": [[195, 368, 518, 500]]}),
    ("It would not be so unnatural to connect this with the recent incident. A green-eyed woman will one day bring "
     "calamity. The wording \"Green-Eye curse-killing\" can also be read as killing by the green eye. And then there "
     "are the spores that germinated on the epidermis of the dead third-generation member. That spores germinate "
     "from a dead third-generation member suggests that, as a property of the Arata cherry, some form of "
     "reproduction takes place from there. This Green-Eye curse-killing, that is, even the abnormal behavior in "
     "which a third-generation member dies or kills other second- or third-generation members, may have been due to "
     "parasitism by the Arata cherry. In this world there are also organisms that parasitize other organisms and "
     "manipulate their hosts' behavior. For example, Leucochloridium, which lives in North America and Europe, "
     "parasitizes snails and controls their behavior.",
     [20, 672, 785, 1050], dict(_RBB, erase=[[16, 703, 790, 1035]])),
    ("A snail parasitized by Leucochloridium", [20, 1426, 780, 1462], dict(_RBL, max_size=22, erase=[[137, 1429, 666, 1458]])),
    ("Shiyo 731, April 19", [20, 1486, 500, 1522], dict(_RBB, max_size=22, erase=[[17, 1489, 259, 1519]])),
    ("Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki", [20, 1520, 790, 1552],
     dict(_RBB, max_size=22, erase=[[18, 1519, 499, 1549]])),
]
JOBS += [_rbjob(176, "report No.14 (parchment; photos kept, brush heading in the photo set in English)", L176)]
# rr176 card = imgRB/ovcard.py 176 "Old Records and the Green-Eye Curse-Killing" 4 82 84 34 white (the white chalk scribble kept).
JOBS += [{"id": "rep176-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr176.gal", "")]}]


# ---- IMAGES18 2026-10-08 (notes/IMAGES18-BRIEF.md): ref 146 (scenario, unlocked by card 193). NO JOBS.
# rr146 概要 (300x169) = background art only (snowy settlement at night, falling snow): no Japanese string on the card
# (checked at 4x and histogram-equalized; alpha fully opaque, no hidden layer). Nothing to translate, so no rep146-ov and
# no ov-p18 sheet: the shipped game keeps the original card. The 60x30 サムネ is below legibility: skipped. No 詳細 picture.

# IMAGES18B-L2 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane L2): 書簡 letters 215 288 217 216 183 (part 18 list).
# Same method as the 書簡 calligraphy letters (letter() helper, ref287 / _LET jobs): face 0 (pale paper) and face 1 (gold
# paper) carry the same vertical brush text; English = horizontal blocks right to left, block 1 where the JP starts.
# One job per face (ref<ID>-p0 inpaint, ref<ID>-p1 texfill) + the 概要 card ref<ID>-ov (mode asis): the card is a 1:1
# crop of face 0 (work/images/_c/ovmatch7.py), rebuilt from the English face 0 by work/images/_c/img18bL2/ovcrop.py.
# Body x0..x1 = the JP ink extents (work/images/_c/img18bL2/ink.py) widened 4 px. The 60x30 サムネ: below legibility.
_L2M = [0, 85, 0, 85, 0, 85]


def _l2jobs(rid, text, x0, x1, n, note, sig=None, sig_box=None, size=20):
    _L = letter(text, x0, x1, n, sig, sig_box, size=size)
    if sig:
        _L[-1][2]["erase"] = [[sig_box[0], 300, sig_box[2], 450]]
    lines = [(t, b, dict(o, mask_color=_L2M)) for t, b, o in _L]
    base = {"style": "serif", "mode": "lines", "erase_first": True, "color": "#1a1208", "mask_grow": 3,
            "mask_color": _L2M, "new": True, "lines": lines}
    return [dict(base, id="ref%d-p0" % rid, screen="reference %d detail" % rid, erase="inpaint",
                 note=note + " (face 0, pale paper)", items=[(D + "rrr%d/0.gal" % rid, "")]),
            dict(base, id="ref%d-p1" % rid, screen="reference %d detail" % rid, erase="texfill",
                 note=note + " (face 1, gold paper)", items=[(D + "rrr%d/1.gal" % rid, "")]),
            {"id": "ref%d-ov" % rid, "screen": "reference screen previews", "style": "serif", "mode": "asis",
             "chain": True, "items": [(O + "rr%d.gal" % rid, "")]}]


# ---- 215 Young People These Days (861x450, 24 columns, ink x 20-847): 2 blocks; card rr215 = crop (561, 0) score 0.991
L2_215 = ("How truly lamentable. Is even our faith in Lady Verde, which has continued for more than a hundred years, to end "
          "with our generation? Just before he died, my grandfather left the words \"Be sure to worship Lady Verde,\" "
          "and passed away. Even now I keep this in my heart and go on worshipping Lady Verde. Worshipping Lady "
          "Verde is by no means some evil cult. We only pray, single-mindedly, for the peace of the settlement. We "
          "have no intention of forcing our faith on harmless outsiders, much less of doing them harm. And yet look: "
          "the young people of Arata these days as good as never pray to Lady Verde. Is this, too, the changing of "
          "the times? Though, looked at the other way, one could also say that peaceful times have gone on even "
          "without such prayers. What worries me is whether the disaster our ancestors went through more than a "
          "hundred years ago will be repeated. For us, their descendants, the ancestors left many rules. After I, the "
          "Grand Witch, am gone, I only hope the rules will not, of all things, be broken.")
JOBS += _l2jobs(215, L2_215, 16, 851, 2, "letter (calligraphy)")


# IMAGES18B-R1 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane R1): the finished report documents rrr<ID>/全体.gal of reports
# 178 192 41 155 268 (part 18 list) + their 概要 cards rr<ID>. Pattern = IMAGESR-A: _rflow() reflows each paragraph group
# from its first JP row at one size per page, _rerase() erases the JP rows (texfill on the paper), _rtitle() for the title.
# Own footer / job helpers so the shared _SIG and _rjob defaults stay untouched for the other lanes: the signature uses the
# GLOSSARY / shipped-script form of セレジェイラ聖教 ("the Holy Cerejeira Church"; IMAGESR's "Cerejeira Faith" is in no
# shipped script: QIMAGES18BR1-01). 翠眼呪殺 = "Green-Eye Curse-Killing" (GLOSSARY, rulings-P18). Ink = median of the JP
# glyph cores per page; boxes measured with work/images/_c/img18b-R1/rows.py + grid.py; end-y checks with plan.py.
_R1SIG = "Holy Cerejeira Church, Physics and Chemistry Team: Hajime Shinozaki"


def _r1foot(date, y_date, y_sig, x0=16, size=21):
    """date + signature lines (JP rows start at y_date / y_sig); same boxes as _rfoot, lane-R1 signature."""
    return [(date, [x0, y_date - 2, 560, y_date + 28], {"max_size": size, "erase": [[x0 - 6, y_date - 4, 600, y_date + 31]]}),
            (_R1SIG, [x0, y_sig - 2, 792, y_sig + 28], {"max_size": size, "erase": [[x0 - 6, y_sig - 4, 600, y_sig + 31]]})]


def _r1job(rid, lines, note, ink):
    return dict(_rjob(rid, lines, note), color=ink)


# ---- 178 "Past Events in the Arata Settlement" (800x1716): title, P1, two photographed letter halves (ref 16's letter
# by its writer: the right photo = the first half, the left photo = the rest + signature; the shipped ref-16 English L16
# is set in the photos, split where the JP photos split: "...in someone's hands," | "the things that threaten..."; the
# 190 precedent), P2 (ruby over the name erased with its row), silhouette picture (art, kept), two-line caption, P3-P4,
# date, signature. Ink #231803 (JP glyph cores 35,23,2).
R178_A = [
    "Droga is thought to have originated when it was developed in the Arata settlement around Shiyo 305. Its developer "
    "was a Westerner named Ginosuke Niimura, who at first conducted research on the animals and plants living in the "
    "Arata settlement. It is surmised from his diary that he gradually came to have doubts about the ecology of the "
    "animals and plants, and arrived at the Arata cherry, and then at Droga.",
]
R178_B = [
    "The first to use Droga in earnest was a traveling foot soldier who visited the Arata settlement, and Ginosuke "
    "Niimura shared Droga with the foot soldier. As a result, the foot soldier used Droga and became the ruler of the "
    "realm. This foot soldier was none other than the famous Fujiyoshiro. However, in Yoshiro's generation Droga "
    "vanished from history, while in the Arata settlement it continued to be used quietly as a hunting tool. Thus, it "
    "is unnatural that Droga, which was used in the Arata settlement, is not seen after Yoshiro's generation. For by "
    "using Droga, the Fuji regime could likely have made itself stable from his son's generation on as well.",
]
R178_C = [
    "What can be inferred from this is that, after Yoshiro's generation, either Droga could no longer be used, or they "
    "realized that it was something that must not be used. The former case is hard to believe, since it continued to "
    "be used in the Arata settlement. In the latter case, the results of our experiments so far have made clear that "
    "the use of Droga is extremely dangerous. If Droga ceased to be used after Yoshiro because its side effects were "
    "noticed, then the Arata settlement too must at least have noticed Droga's side effects. It was precisely because "
    "they noticed those side effects that the concept of the \"Green-Eye Curse-Killing\" took shape, and the custom "
    "of culling the third-generation women who suddenly begin to kill people came into being.",
    "If so, some kind of harm caused by Droga must have occurred in the Arata settlement as well. According to the "
    "records, that disaster apparently occurred three times. Could this be the reason our ancestors parted ways with "
    "the Arata settlement?",
]
_k178 = L16.index("the things that threaten")
_p178a, _e178a = _rflow(R178_A, 20, 788, 100, 22)
_p178b, _e178b = _rflow(R178_B, 20, 788, 613, 22)
_p178c, _e178c = _rflow(R178_C, 20, 788, 1230, 22)
_ph178r, _f178r = _rflow([L16[:_k178].strip()], 422, 726, 309, 13, ls=0.93, gap=0, color="#3c3c3c")
_ph178l, _f178l = _rflow([L16[_k178:].strip()], 84, 388, 313, 13, ls=0.93, gap=0, color="#3c3c3c")
REP178 = ([_rtitle("Past Events in the Arata Settlement", 27, 63),
           _rerase([14, 98, 792, 250]),
           _rerase([414, 304, 728, 534], mask_color=[0, 200, 0, 200, 0, 200], mask_grow=2),
           _rerase([76, 309, 394, 527], mask_color=[0, 200, 0, 200, 0, 200], mask_grow=2),
           ("Ginosuke Niimura", [200, 498, 388, 516], {"max_size": 13, "align": "right", "color": "#3c3c3c", "erase": []}),
           _rerase([14, 612, 792, 866]),
           ("A picture said to show Fujiyoshiro in his foot-soldier days", [40, 1140, 760, 1168],
            {"max_size": 21, "align": "center", "erase": [[150, 1140, 655, 1168]]}),
           ("(Foot Soldier Spy at the Battle of Taruhazama, Tokyo City Museum collection)", [16, 1169, 784, 1198],
            {"max_size": 21, "align": "center", "erase": [[150, 1169, 655, 1198]]}),
           _rerase([14, 1229, 792, 1592])]
          + _p178a + _ph178r + _ph178l + _p178b + _p178c + _r1foot("Shiyo 731, June 23", 1626, 1656))
JOBS += [_r1job(178, REP178, "report (part 18 list; letter photos carry ref 16's English, silhouette kept)", "#231803")]

# IMAGES18B-L2 2026-10-15: ref 288
# ---- 288 Mother, I Am Sorry (826x450, 23 columns, ink x 23-814): 2 blocks; card rr288 = crop (526, 0) score 0.992
L2_288 = ("Mother, I am sorry. After all, I am not fit to be the Grand Witch. Since your passing, Mother, I believe I "
          "have tried my very best, such as I am, to uphold the traditions handed down from the ancestors. But it is "
          "no longer the case that every resident has faith in Lady Verde, and the many rules are broken at will. It "
          "is more than I can handle anymore. Why am I so incompetent? Someone like me cannot possibly govern the "
          "settlement. Should the disaster said to have happened more than a hundred years ago happen again, it is "
          "not something I could fully atone for even with my life. Every time I read 'The Teachings of Cerejeira,' "
          "I grow uneasy. Will a hideous trumpet sound, the dead come back to life, evil divine messengers and the "
          "demon king appear, and trample this Arata underfoot? Lord Ginosuke left these teachings because they have "
          "meaning. If such things were to happen, it might be punishment for trampling on the teachings of our "
          "ancestors.")
JOBS += _l2jobs(288, L2_288, 19, 818, 2, "letter (calligraphy)")
# IMAGES18B-R1 2026-10-15 (cont.): rr178 card = work/images/_c/img18b-R1/ovcard.py 178 "Past Events in the Arata Settlement"
# 4 82 84 34 pink (1:1 window page (250, 0); the pink brush scribble over the text is protected and kept as drawn).
JOBS += [{"id": "rep178-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr178.gal", "")]}]

# IMAGES18B-L2 2026-10-15: ref 217
# ---- 217 I Offer My Life (1561x450, 46 columns, ink x 28-1549): 3 blocks (ref68 precedent, 1345 px = 3);
# card rr217 = crop (1260, 0) score 0.886
L2_217 = ("Mother, this year I turn twenty-one. But please forgive me for ending this life with my own hands. Nearly a "
          "year has passed since I became a witch, and the Grand Witch as well. The residents have begun using the "
          "forbidden medicine to hunt. However much I tell them, they only answer, \"That's an old legend,\" or \"As if "
          "medicine could make the demon king appear.\" Only my childhood friends, close to me in age, take my side. To "
          "the older residents, the wisdom of the ancestors has already sunk to nothing more than a worthless old "
          "saying, mere lore. And this, too, is something I must apologize for. One of my eyes has turned green. When "
          "I tended the wound of a man who had gone hunting, I touched his blood. Since then my eye has been green. "
          "Mother, I believe. The wisdom of the ancestors was never meant to bind us; it is meant to protect us. Will "
          "I one day go mad and try to kill the residents? When I die, will many of the residents worship my corpse "
          "and then become cherry trees? I cannot let this settlement, which has lasted nearly six hundred years, die "
          "out in my generation. But Mother, please rest assured. I have finally understood. I have found the way to "
          "kill the demon king, that is, the evil goddess, which even the great Lord Ginosuke could not uncover. She "
          "is an evil being who will take over this settlement and wipe out the humans. The root cause, who "
          "controls every cherry tree. I gave her the name Shigatsu Youka: the bewitching flower that blooms in the "
          "month of death. I have found the way to kill Shigatsu Youka. I am blessed with dependable childhood "
          "friends, and I am happy. But even so, it cannot be resolved without using my life. Mother, please forgive "
          "me these two things. I will offer my life for the settlement. And I will seal away the Verde mummy. Verde "
          "is that goddess's faithful servant. Verde must be sealed away too. To keep passing this on is the only "
          "thing I can do.")
JOBS += _l2jobs(217, L2_217, 24, 1553, 3, "letter (calligraphy)")


# IMAGES18B-L1 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane L1): 書簡 letters 210 211 212 213 214 (part 18 list).
# Same method as the 書簡 calligraphy letters (letter() helper; ref31-letter / ref86-letter / ref111 / ref208): face 0
# (pale paper) and face 1 (gold / dark paper) carry the same vertical text; English = horizontal blocks right to left,
# block 1 where the JP starts. One job per face (ref<ID>-p0 inpaint, ref<ID>-p1 texfill) + the 概要 card ref<ID>-ov
# (mode asis; the card is a 1:1 crop of face 0, rebuilt from the English face 0 by work/images/_c/img18bL1/ovpaste.py).
# Body x0..x1 = JP ink extents (work/images/_c/img18bL1/cols.py); block-0 erase widened to x0-2 .. x1+6 because face 1
# is drawn 3 px right of face 0 (210 211 213 214). 210-213 brush = serif; 214 pen-hand typeface = handwriting
# (QIMAGES18BL1-01). The 60x30 サムネ: below legibility. Log: notes/v2/_tmp/tl-log-IMAGES18B-L1.md.
_L1M = [0, 85, 0, 85, 0, 85]


def _l1jobs(rid, lines, erase0, note, style="serif"):
    """lines = letter() output (one or more areas); erase0 = {line index: widened erase boxes}."""
    for i, boxes in erase0.items():
        lines[i][2]["erase"] = boxes
    lines = [(t, b, dict(o, mask_color=_L1M)) for t, b, o in lines]
    base = {"style": style, "mode": "lines", "erase_first": True, "color": "#1a1208", "mask_grow": 3,
            "mask_color": _L1M, "new": True, "lines": lines}
    return [dict(base, id="ref%d-p0" % rid, screen="reference %d detail" % rid, erase="inpaint",
                 note=note + " (face 0, pale paper)", items=[(D + "rrr%d/0.gal" % rid, "")]),
            dict(base, id="ref%d-p1" % rid, screen="reference %d detail" % rid, erase="texfill",
                 note=note + " (face 1, gold paper)", items=[(D + "rrr%d/1.gal" % rid, "")]),
            {"id": "ref%d-ov" % rid, "screen": "reference screen previews", "style": style, "mode": "asis",
             "chain": True, "items": [(O + "rr%d.gal" % rid, "")]}]


# ---- 210 Ginosuke's Diary 2 (769x450, 24 columns ink x 78-754 + signature x 20-41): 2 blocks, signature as ref16.
L1_210 = ("I have made a tremendous discovery. It was by chance, but I was able to make a strange medicine from the "
          "cherry trees in the Arata settlement. I originally compounded it to restore the strength of a sick person, "
          "but the moment I gave them the medicine, they became agitated and grew abnormally strong. Even five adults "
          "together could not hold them down. However, the effect wore off in about an hour. Sadly, perhaps because "
          "they had driven their body too hard, they then suffered pain all over and in the end died. If this became "
          "known to the world, this age of turmoil would only grow worse. I will not let it out of Arata. But I also "
          "want to look for a way to put this medicine to good use. I can no longer use the medicine on the people "
          "of this settlement, so if only there were some outsider I could trust. I cannot go back to my homeland "
          "now, and if I am to do it, it would after all have to be one of the warlords of this land of the rising "
          "sun. Which warlord can be trusted the most?")
_L1_210 = letter(L1_210, 76, 756, 2, "Ginosuke Niimura", [16, 230, 60, 448])
JOBS += _l1jobs(210, _L1_210, {0: [[74, 0, 762, 450]], 2: [[16, 300, 60, 450]]}, "letter (calligraphy)")

# ---- 211 The Missing (1393x450, 39 columns ink x 27-1380): 3 blocks (ref68's 1345 px had 3).
L1_211 = ("The residents of Arata, who numbered a hundred, are now down to half. A tragedy like that must never be "
          "repeated. Just as I thought so, several of the surviving residents began to go mad. As if possessed by "
          "something, they began to dig up the bodies of those who died in that conflict. They would not listen even "
          "when told to stop. What is more, they gathered the bodies in one place and stayed close beside them, as "
          "if the bodies were gods. Faced with this bizarre sight, we could do nothing. If we were to dispose of the "
          "bodies in secret, what would they do? No, though I say they were possessed by something, they eat and "
          "they sleep. They also do the necessary work as they always have. But whenever they have time, they stay "
          "close beside the bodies, with nothing but rapturous faces and words praising the bodies. Eventually the "
          "bodies rotted and gave off a stench, and when the rotting flesh began to show, they were at last "
          "satisfied, it seems, and buried the bodies again in their original graves. But even so, the words "
          "praising the bodies and the rapturous faces were never cured. Then, in the spring a year later, they "
          "vanished. All of them at once, without a trace. We searched the area, and here and there cherry trees we "
          "had never seen before had sprung up. Finding it suspicious, we examined the cherry trees: the clothes of "
          "the people who had gone missing were wound around the roots. What is more, what seemed to be human bones "
          "lay scattered around the roots. Did they go missing and become cherry trees? Even if that were so, being "
          "reduced to bare bones in a single night is impossible. It is as baffling as the Teachings of Cerejeira "
          "left by the great Lord Ginosuke, but the phenomenon is a different one.")
_L1_211 = letter(L1_211, 25, 1382, 3)
JOBS += _l1jobs(211, _L1_211, {0: [[23, 0, 1393, 450]]}, "letter (calligraphy)")

# ---- 212 Worship the Goddess (827x450, hooded figure x 0-477 kept, 9 columns ink x 509-814): 1 block (QIMAGES18BL1-02).
L1_212 = ("Worship Lady Verde, formerly Tomi. She sacrificed her life so that she would not bring disaster upon the "
          "settlement. She ought to be worshiped. In the past, many died, went missing, and became cherry trees. At "
          "that time, the Evil Goddess descended upon this land. To stand against such an evil goddess, we worship "
          "our own Goddess. Lady Verde will help us.")
_L1_212 = letter(L1_212, 506, 816, 1)
JOBS += _l1jobs(212, _L1_212, {0: [[504, 0, 822, 450]]}, "letter (calligraphy; figure kept)")

# ---- 213 The Fierce Sound and the Goddess (1708x450, red figure x 883-1128 kept): two text areas, each 2 blocks:
# right of the figure (16 columns ink x 1148-1696) = paragraph 1, left of it (24 columns ink x 32-857) = paragraphs 2-4.
L1_213R = ("I heard a strange story from one of the residents. On the night just before they went missing, the Fierce "
           "Sound rang out, she says. It was a hideous sound beyond description, such that one could not tell where "
           "it was coming from. Since most of the residents were asleep at the time, she was the only one who "
           "noticed it. According to her, she heard the sound on her way to the privy. Then, right after that, a "
           "beautiful girl she had never seen before appeared. A girl of some 15 years, wearing a red kimono. When "
           "the girl appeared, they wandered unsteadily out of their houses and followed after her, she says. They "
           "vanished, uttering the words \"Goddess, Goddess.\"")
L1_213L = ("The woman who witnessed it grew frightened, wrapped herself in her futon and stayed that way until "
           "morning, it seems; but because the scene was so unreal, she decided it must have been a dream. But with "
           "the disappearances and then the matter of the new cherry trees, she was at last able to recognize that it "
           "had not been a dream. Naturally, she is not to blame. Anyone who saw such a sight would shrink back. At "
           "the very least, there is no doubt that the Fierce Sound and the girl said to be the Goddess are involved "
           "in their disappearance. But where had such a girl been until now? This land of Arata should be no place "
           "where a girl of tender years could live on her own. It is far too baffling to put down to her seeing "
           "wrongly. Come to think of it, there was a similar passage in the Teachings of Cerejeira, which I read "
           "before. A hideous trumpet sounded, divine messengers and an evil demon king called Abaddon appeared, and "
           "Lord Ginosuke left his homeland and moved here to Arata, it said.")
_L1_213 = letter(L1_213R, 1146, 1698, 2) + letter(L1_213L, 30, 859, 2)
JOBS += _l1jobs(213, _L1_213, {0: [[1144, 0, 1704, 450]], 2: [[28, 0, 865, 450]]}, "letter (calligraphy; figure kept)")

# ---- 214 Glory to Cerejeira (1284x450, pen-hand typeface, 36 columns ink x 25-1270): 3 blocks, handwriting face.
L1_214 = ("The leader has died. I cannot put into words how much I was cared for here. In the first place, I came "
          "here by a mere mistake. I had originally been heading for the Arata settlement, but I heard that they "
          "worshiped a medicine that brings out strength as a sacred implement, and I was convinced that this very "
          "place was the Arata settlement. But I talked with the late leader for many nights and came to see that "
          "our values were close. It was not long after that that I joined the faith. It seems the forebears of this "
          "sect were originally a faction that split off from the Arata settlement, and part of that culture is "
          "still handed down today. Also, one day, I told the leader why I had come here. The leader then gave me an "
          "instruction: \"Someday, I want you to unravel the sacred implement scientifically.\" Yes, that was the "
          "very reason I had set out for the Arata settlement. I agreed at once. It was not long after that that the "
          "leader died suddenly. The leader's will named me as successor. It is a great honor, but sooner or later I "
          "must go into the world of politics. Then I will bring us and the government as close together as I can, "
          "and work to secure the funds to research the medicine. There is the wall of the separation of religion "
          "and state, but something like that can be dealt with one way or another. Surely the late leader named me "
          "expecting that move of mine, too. Glory to the Holy Cerejeira Church.")
_L1_214 = letter(L1_214, 23, 1272, 3)
JOBS += _l1jobs(214, _L1_214, {0: [[21, 0, 1278, 450]]}, "letter (pen hand)", style="handwriting")


# IMAGES18B-R1 2026-10-15 (cont.) ---- 192 "The Arata Incident" (800x1822): title, P1-P2, two photographed halves of ref 101's
# letter (vertical; the right photo = the text up to the cut at its left edge, the left photo = two yokai-like drawings
# (art, kept) + the last five columns, which overlap the right photo's last columns). The shipped ref-101 English L101
# is set in the photos split at a sentence inside that overlap: right = up to "...killed, every last one.", left =
# "But now that same Highness..." to the end (11 px: 12 px does not fit the left photo's 88 px text strip), two-line
# caption, P3, the summary (a lead line + 5 bulleted items; bullets erased and re-set with each item), P4, date,
# signature. Ink #251904 (JP glyph cores 37,25,4).
R192_A = [
    "Around Shiyo 340, infighting broke out in the Arata settlement. A single green-eyed woman suddenly attacked the "
    "residents and tried to kill them. She was restrained at once, but a few days later, it is said, she died in a "
    "frenzy just as she was. At the time there were also Westerners who had moved to the Arata settlement, but the "
    "original residents began to suspect that the Westerners had brought in a curse. That woman was the first to be "
    "born green-eyed, yet she was pure Japanese, with no Western blood mixed in. Even so, she became green-eyed and "
    "went mad trying to kill. The residents' claim was that the green eyes had arisen because of dealings with the "
    "Westerners, and that this had become a curse. From this time on, the conflict between the Westerners and the "
    "residents came into the open, and there were several victims as each side tried to protect its place and its "
    "life.",
    "But the truly terrifying part came after this: once again there appeared people who suddenly turned green-eyed "
    "and went mad trying to attack the residents. And not just one or two. Those who had turned green-eyed attacked "
    "indigenous people and Westerners alike, without distinction, and the population, which had been about a "
    "hundred, fell to half. Only when the last of the frenzied died did the situation finally settle, and they came "
    "to think that it was not a curse by the Westerners. For if it were a curse by the Westerners, the attacks could "
    "not have been directed at the Westerners' side. And the survivors still had one source of unease.",
]
R192_B = [
    "It was the last remaining green-eyed girl. Her name was Tomi, and at the time she was a small child who could "
    "still barely speak. Tomi alone, though green-eyed, did not go mad. The residents discussed what should be done "
    "with Tomi. Green eyes are dangerous, so she should be killed at once. Tomi has not done anything yet, so they "
    "should wait and see. Tomi is valuable for learning why this happened, so Tomi should be studied. Such opinions "
    "flew back and forth, but in the end no answer was reached.",
]
R192_S = [
    "Late March, Shiyo 340: a green-eyed woman went mad and died in a frenzy as she was",
    "Infighting broke out between the indigenous people and the Westerners; about 50 died",
    "People who suddenly turned green-eyed and tried to kill the residents appeared one after another",
    "The last frenzied person died, and the conflict ended",
    "Unable to decide what to do with the girl Tomi, the last green-eyed one",
]
R192_C = [
    "Our ancestors left the Arata settlement about 150 years after this, an oddly long interval. It can be surmised "
    "that a more decisive event occurred during these 150 years, and we are currently investigating the materials "
    "from that time.",
]
_S192 = 22
_k192 = L101.index("But now that same")
_p192a, _e192a = _rflow(R192_A, 20, 788, 99, _S192)
_p192b, _e192b = _rflow(R192_B, 20, 788, 1095, _S192)
_y192 = _e192b + 14
_l192 = [("To summarize:", [48, _y192, 788, _y192 + 28], {"max_size": _S192, "erase": []})]
_y192 += 30
for _it in R192_S:
    _pi, _ei = _rflow([_it], 52, 788, _y192, _S192, gap=0)
    _l192 += [("\u2022", [24, _y192, 46, _y192 + 28], {"max_size": _S192, "erase": []})] + _pi
    _y192 = _ei + 3
_p192c, _e192c = _rflow(R192_C, 20, 788, _y192 + 22, _S192)
_ph192r, _f192r = _rflow([L101[:_k192].strip()], 436, 722, 749, 11, ls=0.93, gap=0, color="#3c3c3c")
_ph192l, _f192l = _rflow([L101[_k192:].strip()], 293, 380, 749, 11, ls=0.93, gap=0, color="#3c3c3c")
REP192 = ([_rtitle("The Arata Incident", 26, 63),
           _rerase([14, 97, 792, 671]),
           _rerase([430, 748, 726, 929], mask_color=[0, 200, 0, 200, 0, 200], mask_grow=2),   # top 748: texfill samples
           _rerase([290, 748, 382, 929], mask_color=[0, 200, 0, 200, 0, 200], mask_grow=2),   # 4 px up (wood above 745)
           ("A letter found among the Arata settlement's storehouse books,\nthought to concern the Arata Incident\n"
            "Yokai-like figures are drawn on it", [16, 1000, 784, 1082],
            {"max_size": 21, "align": "center", "erase": [[96, 1004, 710, 1032], [221, 1034, 581, 1062]]}),
           _rerase([14, 1093, 792, 1305]),
           _rerase([14, 1337, 792, 1546]),
           _rerase([14, 1576, 792, 1667])]
          + _p192a + _ph192r + _ph192l + _p192b + _l192 + _p192c + _r1foot("Shiyo 731, July 20", 1701, 1731))
JOBS += [_r1job(192, REP192, "report (part 18 list; letter photos carry ref 101's English, yokai drawings kept)", "#251904")]

# IMAGES18B-L2 2026-10-15: ref 216
# ---- 216 Condolences (1181x450, 34 columns, ink x 27-1169): 2 blocks (ref182 precedent, 1090 px = 2).
L2_216 = ("You were timid ever since you were a child, and shy, and yet kinder than anyone, a person who could think of "
          "others. We are very proud that you became the Grand Witch. It was a short time, only one year, but as the "
          "Grand Witch you worked for this settlement the whole time. Without you, this settlement would surely have "
          "sunk beneath the cherry trees. But we succeeded in driving off that evil goddess. It is all thanks to you. "
          "Even the old geezers who mocked you, calling it all old customs and rules, seem to have completely mended "
          "their ways. We must pass this down to our descendants. Please, rest in peace. May there be eternal peace "
          "in Arata. And Lord Ginosuke, though it was in such a form, it is an extraordinary honor to have met you. "
          "But, Lord Ginosuke, how bitter it must have been for you, that 'The Teachings of Cerejeira' should be "
          "misused like that. Shigatsu Youka misuses the knowledge Lord Ginosuke gained in his home country, rules the "
          "humans and makes them kill one another. Shigatsu Youka misuses the cherry trees of Arata and misuses human "
          "wisdom. Shigatsu Youka truly is the demon king, the evil goddess. You struck down that demon king. That "
          "courage and wisdom will be handed down for a long time to come. Lord Ginosuke, and Tsubaki, our friend and "
          "a great Grand Witch. Please, rest in peace.")
JOBS += _l2jobs(216, L2_216, 23, 1173, 2, "letter (calligraphy)")[:2]
# rr216 概要 is NOT a crop of face 0 (work/images/_c/ovmatch7.py best score 0.487: the card's JP is the same opening with
# other column breaks), so it is typeset in place like ov-109: JP ink erased over the whole card (inpaint, the face-0 mask),
# the opening of L2_216 pre-wrapped at the page's 20 px into x 8..296 (work/images/_c/img18bL2/ov216.py), first line's ink
# top at the JP first glyph top (y 7); 6 whole lines (a 7th would show only its top 2 px at the card edge).
JOBS += [{"id": "ref216-ov", "screen": "reference screen previews", "style": "serif", "mode": "lines", "erase": "inpaint",
          "erase_first": True, "color": "#1a1208", "mask_grow": 3, "mask_color": _L2M, "new": True,
          "note": "letter 概要 (not a crop of the detail: typeset in place)", "items": [(O + "rr216.gal", "")],
          "lines": [("You were timid ever since you\nwere a child, and shy, and yet\nkinder than anyone, a person\n"
                     "who could think of others. We are\nvery proud that you became the\nGrand Witch. It was a short time,",
                     [8, 1, 296, 163], {"max_size": 20, "line_spacing": 1.12, "mask_color": _L2M,
                                        "erase": [[0, 0, 300, 170]]})]}]

# IMAGES18B-L2 2026-10-15: ref 183
# ---- 183 Last Words (1904x450, 59 columns): addressee column x 1869-1893 (y 6-172), body x 124-1833, date column x 91-116
# (y 132-438), signature columns x 62-85 (y 216-439) and x 32-54 (y 333-441). Body = 3 blocks (ref68 precedent, 1345 px = 3;
# 1718 px here). Addressee, date and signature are set rot -90 in their own columns (the _LET signature precedent: reads
# top-down; addressee from the column top, date / signature ending at the column bottom). Card rr183 = crop (1604, 0) 0.898.
L2_183 = ("Thank you for presenting your reports the other day. Thanks to you, we now know what we must do, and I believe "
          "the matter is already as good as settled. Sadly, however, I probably have no more than a few days left to "
          "live. You seem to have devoted yourself until now to research into the true nature of the medicine and the "
          "ecology of the cherry trees, but it appears you overlooked the existence of the \"root cause.\" In your "
          "reports there was something called \"the Goddess\"; that is precisely the root cause of everything, the "
          "king of the abyss nesting in this land of Arata. In the documents our ancestors wrote, it was written as "
          "\"Abaddon.\" Abaddon means the king of the abyss, and there are also its close aides, the \"divine "
          "messengers.\" The Arata settlement has been watched by Abaddon for several hundred years, and I will "
          "probably be killed by a divine messenger. What Abaddon truly is: a girl who died long ago, that is, the "
          "Goddess. It was written that Lord Ginosuke Niimura, one of our ancestors, suffered that disaster in his "
          "home country, but who would have thought that such a danger lay hidden here as well. With words like "
          "something out of a myth lined up like this, nothing but questions must come to your mind. But there is no "
          "time. So that our descendants in the future are not exposed to the threat of this goddess, I need to leave "
          "my words, even if only a little. Even if I tell the present residents in words, it will someday fade away. "
          "Until now such history has been repeated, and the use and the banning of Droga have also been repeated. "
          "Both the Arata cherry and Droga must be eradicated. But the enemy is far too mighty and vicious. I thought "
          "that, by rights, the storehouse's books should all be disposed of too, so that our descendants cannot find "
          "their way to Droga. But even without them, our descendants would one day make Droga on their own and "
          "repeat the tragedy again. If so, I think I should deliberately leave the storehouse's books and leave "
          "their danger behind as the wisdom of the ancestors, as a rule. The reports you gave us will also become "
          "part of the storehouse's books, and to pass their danger on to our descendants, I will do my best to "
          "preserve all of the storehouse's books. I thank you from the bottom of my heart for providing us with "
          "valuable materials that were of use to us.")
_X183 = [
    ("Hajime Shinozaki-sama", [1862, 6, 1900, 330],
     {"rot": -90, "max_size": 22, "align": "left", "mask_color": _L2M, "erase": [[1862, 0, 1900, 180]]}),
    ("Shiyo 735, January 27", [86, 120, 121, 440],
     {"rot": -90, "max_size": 22, "align": "right", "mask_color": _L2M, "erase": [[86, 125, 121, 445]]}),
    ("Arata Settlement, Grand Witch", [57, 120, 89, 442],
     {"rot": -90, "max_size": 22, "align": "right", "mask_color": _L2M, "erase": [[57, 208, 89, 446]]}),
    ("Kikyo Niimura", [27, 250, 59, 444],
     {"rot": -90, "max_size": 22, "align": "right", "mask_color": _L2M, "erase": [[27, 326, 59, 448]]}),
]
_J183 = _l2jobs(183, L2_183, 120, 1838, 3, "letter (calligraphy; addressee, date and signature rot -90 in their columns)")
for _j in _J183[:2]:
    _j["lines"] = _j["lines"] + _X183
JOBS += _J183
# IMAGES18B-R1 2026-10-15 (cont.): rr192 card = work/images/_c/img18b-R1/ovcard.py 192 "The Arata Incident" 18 70 80 34 pink
# (1:1 window page (250, 0): the JP title rows sit at card y 27-63 = page y 26-63, title x 75 = page 324; ovprobe's 1.60 match
# was thrown off by the pink brush scribble, which is protected and kept as drawn).
JOBS += [{"id": "rep192-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr192.gal", "")]}]


# IMAGES18B-R1 2026-10-15 (cont.) ---- 41 "The Descent of the Goddess" (800x1733): title, P1-P2, two photos of a letter (ref 213's
# letter, shot at a distance: column pitch about 10 px, glyphs 7-8 px, below legibility in the original at native size, so the
# photos stay as drawn: QIMAGES18BR1-07), caption, a dark drawing (art, no text, kept), two-line caption, P3, date, signature.
# Ink #241804 (JP glyph cores 36,24,4).
R41_A = [
    "After the Arata Incident, something even stranger happened. A number of people appeared who tried to dig up the "
    "corpses of those who had died in the Arata Incident and been buried in the ground. They are said to have stayed "
    "close to the corpses they dug up and kept talking to them. It was as if they were worshiping the dead; they did "
    "respond when those around them called to them, but their attachment to the corpses did not end. These perverts "
    "ate and slept like ordinary people in daily life, and hunted and did farm work when needed. But whenever they had "
    "time, their words and behavior stood out, as if they thought of nothing but the corpses, and this was apparently "
    "extremely eerie.",
    "Most of them were men (with a few women as well), and in the spring of the following year they all went missing "
    "at once. But there is also a record that just before they vanished, \"the Fierce Sound\" rang out and the Goddess "
    "descended. What these are metaphors for is unknown, but it can at least be surmised that there was an omen "
    "before they vanished. What deserves attention here is \"the Fierce Sound\" and \"the Goddess.\" In Shiyo 341 it "
    "would have been difficult to elucidate them scientifically, but now there is room to examine whether they can "
    "be reproduced by some method.",
]
R41_B = [
    "According to an investigation by the residents at the time, new cherry trees were apparently found nearby, as many "
    "as the people who had vanished. It is said that they had suddenly sprung up in places where there should have "
    "been no cherry trees until then. The residents apparently thought that the people who went missing might have "
    "turned into cherry trees. As evidence, it is written that clothing thought to belong to the missing people was "
    "wrapped around the roots of the cherry trees. If this is true, it may be a phenomenon connected to the life "
    "cycle of the Arata cherry.",
]
_p41a, _e41a = _rflow(R41_A, 20, 788, 99, 22)
_p41b, _e41b = _rflow(R41_B, 20, 788, 1368, 22)
REP41 = ([_rtitle("The Descent of the Goddess", 27, 63),
          _rerase([14, 97, 792, 551]),
          ("A letter written about the Goddess and the Fierce Sound", [40, 884, 760, 912],
           {"max_size": 21, "align": "center", "erase": [[196, 884, 610, 913]]}),
          ("Picture of the Descent of the Goddess\n(Arata settlement storehouse books)", [40, 1276, 760, 1340],
           {"max_size": 21, "align": "center", "erase": [[322, 1277, 482, 1306], [312, 1307, 493, 1339]]}),
          _rerase([14, 1367, 792, 1578])]
         + _p41a + _p41b + _r1foot("Shiyo 731, October 4", 1613, 1643))
JOBS += [_r1job(41, REP41, "report (part 18 list; letter photos below legibility, kept; drawing kept)", "#241804")]
# IMAGES18B-R1 2026-10-15 (cont.): rr41 card = work/images/_c/img18b-R1/ovcard.py 41 "The Descent of the Goddess" 4 82 84 34 bw mirror
# (the card is a MIRRORED 1:1 window onto page (250, 0), faint text under black spray blobs and white chalk strokes; built
# flipped, flipped back; the blobs and the chalk are protected and kept as drawn).
JOBS += [{"id": "rep41-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr41.gal", "")]}]


# IMAGES18B-R1 2026-10-15 (cont.) ---- 155 "The Goddess Verde" (800x1184): title, P1, a picture (hand holding an eye; art, kept)
# with a 4-line caption to its right, P2, a picture (masked mummy; art, kept) with a 3-line caption to its right, date,
# signature. Captions reflowed in their own column (x 416-788) at one caption size. Ink #221602 (JP glyph cores 34,22,2).
R155_A = [
    "In a report submitted earlier, I recorded the matter of Tomi, the last surviving green-eyed girl. In Shiyo 352, 12 "
    "years after the Arata Incident, Tomi too was finally struck by that frenzy. She desperately resisted the murderous "
    "intent and gouged out her green eye with her own hand. Even so, Tomi's frenzy did not subside, and in the end Tomi "
    "thrust her hand through her eye into her brain and took her own life. With this, the last one with green eyes, "
    "that is, the last of the green-eyed, was gone. The residents believed that women whose eyes had turned green "
    "would, on reaching a certain age, be struck by murderous intent like this. The concept of the \"Green-Eye "
    "Curse-Killing\" is also thought to have arisen in this period.",
]
R155_B = [
    "Holding that Tomi had resisted that murderous intent and thrown away her life to protect the settlement, the "
    "residents made her body into a mummy and preserved it. A custom arose of worshiping that body as an image of the "
    "Goddess. Tomi's mummy was named Verde. Verde (verde) means \"green\" in Portuguese. Since then, a unique religion "
    "in which Japanese and Western cultures intersect has taken shape in the Arata settlement.",
]
R155_C1 = ["Part of the Arata settlement storehouse books.",
           "A picture thought to show Tomi gouging out her eye had been preserved.",
           "(Around Shiyo 352?)"]
R155_C2 = ["This too is from the Arata settlement storehouse books.",
           "Verde's mummy wears a traditional Noh mask and red robes."]
_S155 = 21
_p155a, _e155a = _rflow(R155_A, 20, 788, 99, _S155)
_p155b, _e155b = _rflow(R155_B, 20, 788, 643, _S155)
_c155a, _f155a = _rflow(R155_C1, 416, 788, 433, 19, gap=0.25)
_c155b, _f155b = _rflow(R155_C2, 422, 788, 908, 19, gap=0.25)
REP155 = ([_rtitle("The Goddess Verde", 26, 63),
           _rerase([14, 97, 792, 340]),
           _rerase([410, 431, 790, 544]),
           _rerase([14, 641, 792, 823]),
           _rerase([416, 906, 790, 988])]
          + _p155a + _c155a + _p155b + _c155b + _r1foot("Shiyo 731, December 16", 1099, 1129))
JOBS += [_r1job(155, REP155, "report (part 18 list; two pictures kept, side captions reflowed)", "#221602")]
# IMAGES18B-R1 2026-10-15 (cont.): rr155 card = work/images/_c/img18b-R1/ovcard.py 155 "The Goddess Verde" 18 70 80 34 chalk
# (1:1 window page (250, 0) on a red ground; the white chalk katakana scribble over the text is protected and kept as drawn).
JOBS += [{"id": "rep155-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr155.gal", "")]}]
# IMAGES18B-R2 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane R2): the finished report documents rrr<ID>/全体.gal of reports
# 269 270 272 273 274 (part 18 list) + their 概要 cards rr<ID>. Pattern = lane R1 / IMAGESR-A: _rflow() reflows each
# paragraph group from its first JP row at one size per page, _rerase() erases the JP rows (texfill on the paper),
# _rtitle() for the title. Signature = lane R1's _R1SIG (one wording for both lanes, QIMAGES18BR1-01). White labels on the
# black / red diagram plates: flat fill of the plate colour inside erase boxes measured strictly inside the plate
# (work/images/_c/img18b-R2/pcomp.py + boxchk.py + band.py; slanted arrows = a row of narrow boxes along the band), English
# in white (rot = the arrow's slope). Ink = median of the JP glyph cores per page (col.py); end-y checks with plan.py.
_R2BLK = "#030303"
_R2RED = "#f20707"


def _r2foot(date, y_date, y_sig, x0=16, size=21):
    """date + signature lines (JP rows start at y_date / y_sig); same boxes as _rfoot, the lane-R1 signature _R1SIG."""
    return [(date, [x0, y_date - 2, 560, y_date + 28], {"max_size": size, "erase": [[x0 - 6, y_date - 4, 600, y_date + 31]]}),
            (_R1SIG, [x0, y_sig - 2, 792, y_sig + 28], {"max_size": size, "erase": [[x0 - 6, y_sig - 4, 600, y_sig + 31]]})]


def _r2job(rid, lines, note, ink):
    return dict(_rjob(rid, lines, note), color=ink)


def _r2plate(text, box, erase, bg, size, **k):
    """white label on a diagram plate: flat fill of the plate colour in the erase boxes, English in white."""
    return (text, list(box), dict({"max_size": size, "align": "center", "color": "#ffffff", "method": "flat", "bg": bg,
                                   "erase": [list(e) for e in erase]}, **k))


def _r2cap(text, box, erase, size, **k):
    return (text, list(box), dict({"max_size": size, "align": "center", "erase": [list(e) for e in erase]}, **k))


def _r2bul(items, x0, x1, y0, size, bx=24, gap=3):
    """bulleted items (bullet at bx, text from x0); returns (lines, end_y)."""
    out, y = [], y0
    for it in items:
        p, e = _rflow([it], x0, x1, y, size, gap=0)
        out += [("•", [bx, y, x0 - 4, y + size + 6], {"max_size": size, "erase": []})] + p
        y = e + gap
    return out, y - gap


# ---- 269 "A Study of Arata Cherry Propagation" (800x5256): title, P1 + two bullets, two spore photos (10μ scale bars kept),
# P2-P7, honey-fungus photo + two-line caption, P8 + two bullets + P9, tree photo + caption, P10, food-chain diagram (white
# labels on black / red arrows; four slanted) + caption, P11-P12, diagram 2 (two arrow labels, two figure labels) + caption,
# P13, diagram 3 (three arrow labels, red banner, three figure labels) + caption, P14-P15, date, signature.
# Ink #1e1300 (JP glyph cores 30,19,0); the thin diagram labels and the diagram 2 / 3 captions #2a1b02 (cores 41-44,26-30,2).
R269_A = [
    "From among the reports up to the other day, we excerpt and summarize what concerns the propagation and life cycle "
    "of the Arata cherry. The Arata cherry is a fungus that mimics the Somei-yoshino cherry. Roughly speaking, it is fair "
    "to call it a mushroom. However, its mycelial mat is extremely wide and is thought to spread across the whole Arata "
    "district. The Arata cherry has two kinds of spores.",
]
R269_AB = [
    "Spores dispersed from the part that mimics flowers (photo, left)",
    "Spores with a muscle-strengthening effect, stored in the roots (hyphae) (photo, right)",
]
R269_B = [
    "First, it has mammals feed on its roots and strengthens their muscles. Through this, the mammals learn that feeding "
    "on the roots of the Arata cherry gives them very great strength, and it becomes possible to encourage active "
    "feeding (the first generation).",
    "When a member of the first generation gives birth, the bleeding at childbirth makes the child second generation "
    "without exception. The second generation can exercise precognition by inhaling the spores dispersed from the "
    "flowers (however, with the situation at the time of touching the blood re-created). At birth, the mother suffers "
    "from labor pains and exhaustion, but the child being born is also said to experience extremely great pain when "
    "passing through the birth canal. It is thought that when a member of the second generation is struck by some "
    "serious injury or pain, they become able to foresee danger to those nearby.",
    "Furthermore, when a member of the second generation gives birth, the third generation is born. The third "
    "generation, too, touch their mother's blood at birth and are green-eyed from birth. However, the ability to "
    "foresee danger is limited to girls who have reached a certain age, and at that point an unbearable murderous "
    "intent wells up toward the other members of the second and third generations.",
    "When a member of the third generation dies, spores germinate from the surface of the body, and new spores form at "
    "their tips. When those spores combine with the spores remaining inside the bodies of the first and second "
    "generations, the fourth generation is born. The fourth generation come to hold an obsessive attachment to the "
    "corpses of the third generation, become seedbeds for the cherry in about a year, and the propagation is complete.",
    "In this way, the Arata cherry propagates by an extremely complex and time-consuming method. We will proceed to "
    "consider why the Arata cherry chose such a complex method of propagation.",
]
R269_B2 = [
    "What is the Arata cherry? It has been established that it is a fungus, but our supposition is that it is a true "
    "fungus belonging to the honey fungi.",
]
R269_C = [
    "Honey fungus is not a particularly rare mushroom; it is found in the mountains of Japan and is a common one, treated "
    "as edible. However, honey fungus has two major characteristics:",
]
R269_CB = [
    "On rare occasions it becomes an extremely huge mycelial mat (enough to swallow a mountain)",
    "It has an extremely strong parasitic nature (a parasitic fungus)",
]
R269_C2 = [
    "These two closely resemble the Arata cherry (those who work in forestry detest this honey fungus intensely, because "
    "honey fungus, owing to its strong parasitic nature, makes one tree after another its seedbed and makes the trees "
    "wither). Therefore, the Arata cherry is thought to be a relative of the honey fungus.",
]
R269_D = [
    "Next, why does a relative of the honey fungus mimic the cherry? The advantage of mimicking the cherry lies in how "
    "easily it gathers living things. Honeybees, birds, and the like have the habit of gathering, drawn by beautiful "
    "flowers. What differs from the Somei-yoshino, however, is that it holds a scent and nectar that can gather a "
    "greater number of insects. If many insects can be gathered, the birds and small animals that prey on them gather, "
    "and then the mammals that prey on those gather as well. In other words, it can create a thick food chain. When "
    "living things gather in this way, rich soil is made, and a paradise abundant in food comes into being. Also, the "
    "reason that, among flowers, it mimics the cherry is thought to be to gather around it the animals that have woken "
    "from hibernation in early spring. The more the mammals increase, the more candidates for the Arata cherry's "
    "seedbeds increase, and the Arata cherry's propagation is carried out efficiently.",
]
R269_E = [
    "Furthermore, we must also consider why the Arata cherry takes so much time over its propagation. Because the Arata "
    "cherry needs to keep nutrients in its huge mycelial mat, it needs to keep the soil fertile at all times. For that, "
    "many animals and plants must have their living spheres around it. To maintain such living spheres, the spores of "
    "the Arata cherry must not be found out to be poison. If mammals that had fed on the roots of the Arata cherry were "
    "to germinate at once, they would no longer feed on the Arata cherry, and there is a risk that they would leave the "
    "surroundings of the Arata cherry. It is surmised that by taking time over its propagation, it aims to conceal the "
    "conditions for becoming a seedbed. If there is no harm to the mammals, food is abundant, and when it comes to it, "
    "there is even the means of feeding on the roots to strengthen their muscles: it becomes a place truly worthy of "
    "being called a paradise.",
    "Then why are the second and third generations endowed with the ability to sense danger? That answer, too, can be "
    "explained by considering the life cycle of the Arata cherry. The second generation, regardless of age or sex, has "
    "the ability to foresee danger under certain conditions. To individuals without the ability to sense danger, the "
    "second generation are extremely precious beings. When this is so, the surrounding society will likely treat the "
    "second generation with care. From the Arata cherry's standpoint, they can be called precious parasitic hosts that "
    "spread its seedbeds, so the second generation must bear the next children.",
]
R269_G = [
    "But what of the third generation? The third generation is the final host, and when they die, spores that take over "
    "the first and second generations are dispersed from their epidermis. From the Arata cherry's point of view, the "
    "third generation are individuals it wants to die as soon as possible. For that reason, it makes the surrounding "
    "society kill the third generation quickly. But to make it kill the third generation, it must make them commit acts "
    "that shake the surrounding society. That is, it prompts them to kill the second generation. It makes the "
    "surrounding society learn the phenomenon that, once the third generation reach a certain age, they are driven by "
    "an urge to kill the second generation, and makes it acquire the habit of killing the third generation quickly once "
    "they are born. To make it easy to tell that a newborn child is third generation, the physical trait of one green "
    "eye probably comes about.",
]
R269_H = [
    "In the end, the third generation die, and the first and second generations around them are reduced to the fourth "
    "generation. The fourth generation die in the spring of the following year and sprout cherry trees all at once. "
    "However, by the time it comes to that generation, it is already extremely difficult to surmise that the cause is "
    "the Arata cherry, and the surviving individuals once again lay hands on the roots of the Arata cherry.",
    "The above is our study of the life cycle of the Arata cherry, Droga, and danger sense. However, many points are "
    "still unclear, such as the mechanism of danger sense, the Fierce Sound, and the Goddess.",
]
_S269 = 20
_L269 = "#2a1b02"
_p269a, _e269a = _rflow(R269_A, 20, 788, 101, _S269)
_b269a, _f269a = _r2bul(R269_AB, 52, 788, _e269a + 10, _S269)
_p269b, _e269b = _rflow(R269_B, 20, 788, 645, _S269)
_p269b2, _e269b2 = _rflow(R269_B2, 20, 788, _e269b + 18, _S269)
_p269c, _e269c = _rflow(R269_C, 20, 788, 1824, _S269)
_b269c, _f269c = _r2bul(R269_CB, 52, 788, _e269c + 3, _S269)
_p269c2, _e269c2 = _rflow(R269_C2, 20, 788, _f269c + 3, _S269)
_p269d, _e269d = _rflow(R269_D, 20, 788, 2459, _S269)
_p269e, _e269e = _rflow(R269_E, 20, 788, 3155, _S269)
_p269g, _e269g = _rflow(R269_G, 20, 788, 4092, _S269)
_p269h, _e269h = _rflow(R269_H, 20, 788, 4817, _S269)
REP269 = ([_rtitle("A Study of Arata Cherry Propagation", 26, 63),
           _rerase([14, 98, 792, 342]), _rerase([14, 642, 792, 1397]), _rerase([14, 1821, 792, 2092]),
           _rerase([14, 2456, 792, 2817]), _rerase([14, 3152, 792, 3755]), _rerase([14, 4089, 792, 4419]),
           _rerase([14, 4814, 792, 5085]),
           _r2cap("A photograph of honey fungus\nAlso called \"boribori\" in Hokkaido", [40, 1729, 760, 1792],
                  [[314, 1731, 495, 1759], [186, 1761, 617, 1790]], 21, line_spacing=1.08),
           _r2cap("A tree rotted by Armillaria root rot", [40, 2395, 760, 2426], [[251, 2396, 557, 2424]], 21),
           _r2cap("It builds a food chain and draws in mammals, its hosts", [20, 3090, 780, 3122], [[110, 3091, 693, 3120]], 21),
           _r2cap("Being precious beings, the second generation are treated with care", [20, 4010, 780, 4040],
                  [[176, 4011, 632, 4038]], 20, color=_L269),
           _r2cap("It hastens the deaths of the third generation to promote propagation", [20, 4760, 780, 4790],
                  [[226, 4761, 570, 4788]], 20, color=_L269),
           # food-chain diagram: straight arrows
           _r2plate("Mammals", [10, 2962, 116, 2992], [[28, 2964, 98, 2988]], _R2BLK, 18),
           _r2plate("Mammals", [700, 2966, 788, 3002], [[702, 2972, 772, 2997]], _R2BLK, 18),
           _r2plate("Insects", [255, 2960, 302, 2982], [[265, 2959, 289, 2982]], _R2BLK, 14),
           _r2plate("Insects", [490, 2972, 536, 2994], [[502, 2972, 526, 2996]], _R2BLK, 14),
           _r2plate("Mimics\nthe cherry", [352, 2926, 424, 2974], [[365, 2920, 411, 2944], [365, 2948, 412, 2972]], _R2RED, 17,
                    line_spacing=1.0),
           # slanted arrows (rot = the arrow's slope; erase = narrow boxes along the band, all inside the plate)
           _r2plate("Small animals", [143, 2911, 223, 2951],
                    [[148, 2900, 158, 2930], [158, 2905, 168, 2935], [168, 2910, 178, 2940], [178, 2915, 188, 2945],
                     [188, 2920, 198, 2949], [198, 2924, 208, 2954], [208, 2929, 218, 2964]], _R2BLK, 15, rot=-22, rot_h=18),
           _r2plate("Small animals", [567, 2932, 647, 2972],
                    [[568, 2952, 578, 2984], [578, 2950, 588, 2977], [588, 2946, 598, 2974], [598, 2942, 608, 2969],
                     [608, 2938, 618, 2965], [618, 2934, 628, 2962], [628, 2930, 638, 2958], [638, 2926, 646, 2955]],
                    _R2BLK, 15, rot=20, rot_h=18),
           _r2plate("Birds", [158, 3009, 202, 3041], [[168, 3009, 180, 3039], [180, 3007, 190, 3036]], _R2BLK, 15, rot=15, rot_h=18),
           _r2plate("Birds", [587, 3030, 631, 3062], [[596, 3029, 600, 3055], [600, 3030, 610, 3058], [610, 3033, 621, 3060]],
                    _R2BLK, 15, rot=-15, rot_h=18),
           # diagram 2
           _r2plate("Danger sense", [258, 3802, 390, 3838], [[274, 3809, 366, 3833]], _R2BLK, 18),
           _r2plate("Precious being", [270, 3901, 402, 3936], [[283, 3908, 397, 3932]], _R2BLK, 18),
           _r2cap("Second generation", [140, 3964, 290, 3992], [[164, 3965, 258, 3991]], 18, color=_L269),
           _r2cap("Surrounding society", [470, 3974, 650, 4002], [[515, 3975, 603, 4001]], 18, color=_L269),
           # diagram 3
           _r2plate("Danger sense", [336, 4455, 468, 4490], [[352, 4462, 443, 4486]], _R2BLK, 18),
           _r2plate("Killing", [140, 4506, 226, 4540], [[158, 4511, 203, 4535]], _R2RED, 18),
           _r2plate("Precious being", [346, 4554, 480, 4589], [[360, 4560, 475, 4585]], _R2BLK, 18),
           _r2plate("A culture of regarding green eyes as dangerous takes shape", [90, 4700, 640, 4728],
                    [[235, 4702, 554, 4726]], _R2RED, 18),
           _r2cap("Third generation", [16, 4618, 168, 4645], [[42, 4619, 136, 4644]], 18, color=_L269),
           _r2cap("Second generation", [212, 4617, 366, 4644], [[241, 4618, 336, 4643]], 18, color=_L269),
           _r2cap("Surrounding society", [550, 4626, 730, 4654], [[592, 4627, 686, 4653]], 18, color=_L269)]
          + _p269a + _b269a + _p269b + _p269b2 + _p269c + _b269c + _p269c2 + _p269d + _p269e + _p269g + _p269h
          + _r2foot("Shiyo 732, June 30", 5150, 5180))
JOBS += [_r2job(269, REP269, "report (part 18 list; photos and diagram art kept, 10μ scale bars kept)", "#1e1300")]


# IMAGES18B-R1 2026-10-15 (cont.) ---- 268 "Fourth Generation Experiments" (800x4052): title; P1 + a 5-item numbered list + P2-P4
# + three naming lines; diagram 1 (three figures, two black arrows with white labels, three labels under the figures); P5-P6
# with two quoted lines; diagram 2 (an ellipse with a heading, two small labels, two diagonal black arrows with white labels,
# a label under the crossed-out figure; the ellipse line stays); P7-P8; a photo (no text, kept); a lead line + 5 bulleted
# items; diagram 3 (two black arrows with white labels); a two-line caption; P9-P10; date; signature. Numbered / bulleted
# items: marker + hanging indent (the 192 pattern). 壱 / 弐 / 参 = (I) / (II) / (III) and 遺体（参） = "Corpse (III)" (the
# shipped label forms, QIMAGES18BR1-09). Ink #231803 (JP glyph cores 35,24,3).
def _r1list(items, marks, xm, xt, y, size, x1=788):
    """numbered / bulleted items stacked from y: marker in [xm, xt - 4], text wrapped in [xt, x1]; returns (lines, end_y)."""
    out = []
    for mk, it in zip(marks, items):
        p, e = _rflow([it], xt, x1, y, size, gap=0)
        out += [(mk, [xm, y, xt - 4, y + int(size * 1.3)], {"max_size": size, "erase": []})] + p
        y = e + 3
    return out, y


_S268 = 21
_W268 = {"method": "flat", "bg": "#020101", "color": "#ffffff", "align": "center", "mask_color": [150, 255, 150, 255, 150, 255]}
_D268 = {"method": "inpaint", "mask_color": [110, 255, 110, 255, 110, 255], "mask_grow": 3, "color": "#ffffff",
         "rot_h": 18, "max_size": 15}
R268_1 = [
    "According to the earlier summary of the records, a person who meets certain conditions goes missing, and that "
    "person becomes a cherry tree. This is surmised to be the Arata cherry's method of reproduction. A person who has "
    "become a cherry tree is named the fourth generation. Summarizing, with Droga included, the process from the "
    "Arata Incident to the phenomenon of humans changing into cherry trees:",
]
R268_L = [
    "Droga was abused through the Arata Incident",
    "The third generation was born from the blood spattered in the fighting",
    "The incident ended when all of the frenzied third generation died",
    "A few days later, people appear who dote on the corpses of the dead third generation",
    "A year later, the doting ones go missing and become cherry trees (the doting ones are the fourth generation)",
]
R268_2 = [
    "In the process above, there must have been a condition that turns a human into the fourth generation (the case "
    "of Tomi excepted). In our research, we have in effect been able to reproduce up to 3. That being so, we must "
    "experiment on how the corpse-doting ones of 4 can be produced. At least, not everyone went strange, so here we "
    "will also surmise to some extent the conditions for becoming one who dotes.",
    "Incidentally, new buds sprout on the epidermis of a third-generation corpse, and spores are further released "
    "from there. That means these spores must combine with something so that sexual reproduction takes place. So "
    "far, when it comes to spores inside the human body, there are the first and second generations. If the spores "
    "of the third generation combine with the spores of the first and second generations and germinate as a cherry "
    "tree, that would agree with both the records and our research so far.",
    "So we decided to create one member of the third generation. Droga was administered to one person, others were "
    "made to touch the blood in turn, and a second generation and a third generation were produced.",
]
R268_N = ["First generation (I)", "Second generation (II)", "Third generation (III)", "are the names we give them."]
R268_3 = [
    "When (II) and (III) were made to inhale cherry pollen, that precognition appeared in (II), and (III) went mad. "
    "After confirming that (III) was driven by murderous intent toward (II), we promptly killed it. Afterward, (I) "
    "and (II) were made to live together with the corpse of (III).",
    "As a result, changes were seen in (I) and (II). A week after they began living together, once the decay of "
    "(III) had advanced somewhat, (I) and (II) (hereafter the two are called \"the mutated\") came to show rapt "
    "expressions and more and more delusional talk. When we listened to the mutated talk,",
]
R268_Q = ["\"Soon I will return to the earth,\"", "\"Corpse (III) is waiting,\""]
R268_3b = [
    "they said. Even when cherry pollen was cut off, the symptoms did not change, and they progressed regardless of "
    "the season.",
]
R268_4 = [
    "When the blood of the mutated was sampled, buds of about 100 microns had grown from 10-micron spores, and at the "
    "tips of the buds, sexual spores different from those of Corpse (III) were confirmed. Many of those spores were "
    "already conjugated with the corpse's spores, and here, for the first time, we were able to confirm the existence "
    "of the fourth generation. The fourth generation is the life form that results when the first and second "
    "generations undergo further mutation.",
    "A year later, the two mutants died, and cherry trees about 3 meters in size arose (there was a ceiling, so their "
    "growth is thought to have stopped at 3 meters). They were already in bloom, and their appearance closely "
    "resembled the Somei Yoshino. Those cherry trees used not soil but the two mutants as their seedbed, and a week "
    "later both had withered and died. As with ordinary fungi, unless the mutants die on organic matter such as soil, "
    "the fruiting bodies presumably cannot grow stably. The site had a concrete floor, so it is thought they could "
    "not take root. When found, most of the corpses' muscle, skin and internal organs had dissolved, and a colorless, "
    "transparent mucus had spread across the floor (why the corpses dissolved is unknown).",
]
R268_S = [
    "Formed when the spores inside the bodies of the first and second generations combine with the spores that arose "
    "on the corpse of the third generation",
    "The spores conjugate inside the bodies of the first and second generations (the first and second generations "
    "transition into the fourth generation)",
    "Rapt expressions and delusional talk are seen",
    "The symptoms gradually progress, with a tendency to dote on Corpse (III)",
    "One year after the spores conjugate, cherry trees grow from the first and second generations, and they die",
]
R268_5 = [
    "The Arata cherry stores in its roots spores that produce a body-strengthening component, has mammals ingest "
    "them, and germinates inside the mammals' bodies. They lie hidden in the body until the grandchildren's "
    "generation, make that generation kill one another, and release sexual spores. The first and second generations "
    "who absorb those become fruiting bodies and spread the reproductive range. This is the life cycle of the Arata "
    "cherry.",
    "However, after the earlier experiments, we cannot sacrifice the lives of any more of our brethren, and there "
    "should have been none of our brethren in this experiment either. As for this time's test subjects, it seems "
    "Kichizo-sama secured three cooperators from somewhere. Rumor has it they are prisoners serving life sentences "
    "and condemned men who took plea bargains, but does Kichizo-sama have connections even in such places?",
]
_g268 = 0.45 * _S268
_a268, _y = _rflow(R268_1, 20, 788, 99, _S268)
_b268, _y = _r1list(R268_L, ["1.", "2.", "3.", "4.", "5."], 20, 48, _y + int(_g268 * 2), _S268)
_c268, _y = _rflow(R268_2, 20, 788, _y + int(_g268 * 2), _S268)
_d268, _e268a = _rflow(R268_N, 20, 788, _y + int(_g268), _S268, gap=0)
_f268, _y = _rflow(R268_3, 20, 788, 1278, _S268)
_q268, _y = _rflow(R268_Q, 30, 788, _y, _S268, gap=0)
_h268, _e268b = _rflow(R268_3b, 20, 788, _y, _S268)
_i268, _e268c = _rflow(R268_4, 20, 788, 2154, _S268)
_j268 = [("The traits of the fourth generation are summarized as follows.", [20, 3061, 788, 3061 + int(_S268 * 1.3)],
          {"max_size": _S268, "erase": []})]
_k268, _e268d = _r1list(R268_S, ["•"] * 5, 22, 52, 3061 + int(_S268 * 1.3) + 2, _S268)
_l268, _e268e = _rflow(R268_5, 20, 788, 3635, _S268)
REP268 = ([_rtitle("Fourth Generation Experiments", 26, 63),
           _rerase([14, 97, 792, 944]),
           ("Blood", [208, 1082, 302, 1116], dict(_W268, max_size=20, erase=[[236, 1086, 286, 1113]])),
           ("Blood", [446, 1082, 540, 1116], dict(_W268, max_size=20, erase=[[473, 1086, 523, 1113]])),
           ("First generation (I)", [40, 1204, 262, 1234], {"max_size": 20, "align": "center", "erase": [[82, 1205, 219, 1233]]}),
           ("Second generation (II)", [270, 1204, 504, 1234], {"max_size": 20, "align": "center", "erase": [[318, 1205, 455, 1233]]}),
           ("Third generation (III)", [522, 1204, 752, 1234], {"max_size": 20, "align": "center", "erase": [[569, 1205, 705, 1233]]}),
           _rerase([14, 1276, 792, 1639]),
           ("Living together", [262, 1700, 546, 1752], {"max_size": 32, "align": "center", "erase": [[359, 1702, 450, 1750]]}),
           ("I", [248, 1740, 290, 1766], {"max_size": 20, "align": "center", "erase": [[255, 1740, 282, 1766]]}),
           ("II", [510, 1740, 552, 1766], {"max_size": 20, "align": "center", "erase": [[518, 1740, 544, 1766]]}),
           ("", [277, 1955, 305, 1982], dict(_D268, erase=[[277, 1955, 305, 1982], [297, 1972, 321, 1998]])),
           ("", [492, 1974, 514, 1998], dict(_D268, erase=[[492, 1974, 514, 1998], [512, 1956, 537, 1982]])),
           ("Doting", [279, 1957, 319, 1997], dict(_D268, rot=-43, erase=[])),
           ("Doting", [492, 1958, 532, 1998], dict(_D268, rot=45, erase=[])),
           ("III (dead)", [330, 2112, 510, 2140], {"max_size": 20, "align": "center", "erase": [[375, 2113, 467, 2139]]}),
           _rerase([14, 2152, 792, 2636]),
           _rerase([14, 3059, 792, 3301]),
           ("Doting", [412, 3378, 500, 3416], dict(_W268, max_size=20, erase=[[436, 3384, 488, 3412]])),
           ("Spores", [430, 3456, 520, 3494], dict(_W268, max_size=20, erase=[[447, 3461, 496, 3488]])),
           ("The first and second generations become the fourth generation\nthrough the effect of the spores released "
            "from the dead third generation", [40, 3538, 760, 3596],
            {"max_size": 20, "align": "center", "erase": [[167, 3540, 668, 3594]]}),
           _rerase([14, 3633, 792, 3936])]
          + _a268 + _b268 + _c268 + _d268 + _f268 + _q268 + _h268 + _i268 + _j268 + _k268 + _l268
          + _r1foot("Shiyo 732, May 21", 3970, 4000))
JOBS += [_r1job(268, REP268, "report (part 18 list; diagrams + photo kept, their labels set in English)", "#231803")]
# IMAGES18B-R2 2026-10-15 (cont.): rr269 card = work/images/_c/img18b-R2/ovcard.py 269 "A Study of Arata Cherry Propagation"
# 4 96 98 34 pink (1:1 window page (250, 0), ovprobe 0.47; the red brush scribble over the text is protected and kept as drawn).
JOBS += [{"id": "rep269-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr269.gal", "")]}]
# IMAGES18B-R1 2026-10-15 (cont.): rr268 card = work/images/_c/img18b-R1/ovcard.py 268 "Fourth Generation Experiments" 4 82 84 34
# orangewhite (1:1 window page (250, 0) on a dark ground; the orange brush scribble and the soft white strokes over the text
# are protected and kept as drawn).
JOBS += [{"id": "rep268-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr268.gal", "")]}]
# IMAGES18B-R2 2026-10-15 (cont.) ---- 270 "Methods of Suppressing the Urge to Kill" (800x2609): title, P1, diagram 1 (three
# figures, art kept; white label on the red arrow; three figure labels set in two lines, the two right ones share one JP row)
# + caption, P2-P3, diagram 2 (brain and spore photo kept; white label on the red arrow) + two-line caption, "Postscript"
# heading, P4, photo (kept) + caption, P5-P6, date, signature. Ink #231803 (JP glyph cores 35,24,3); labels / captions
# #271a04 (cores 38-40,25-30,3-9). JP typo 考えらえる read as 考えられる.
R270_A = [
    "Using condemned prisoners who had become third generation, we carried out various experiments. The main subject this "
    "time was the Arata cherry's chain of command. As stated in the previous report, the Arata cherry takes over the brain "
    "and spinal cord of the third generation and, under certain conditions, tries to kill the infected who are its "
    "targets. Besides drugs and medical treatment, the method of suppressing this urge to kill is an extremely simple "
    "one: making a third-generation member who is driven by the urge to kill faint. If they can be made to lose "
    "consciousness, by anesthesia, a hard blow to the head, or the like, the third-generation member remains motionless "
    "until waking. Also, if a third-generation member is restrained or the like and left driven by the urge to kill, they "
    "faint and wake repeatedly at fixed intervals. This is thought to be the brain judging the danger and choosing to "
    "faint of its own accord; at these times, too, the third-generation member becomes motionless, and on waking attempts "
    "once again to kill the target.",
]
R270_B = [
    "However, there are exceptions. In the case of a person in a vegetative state, even if they appear to be completely "
    "without consciousness, they are merely unable to move their body, and their consciousness is in fact sometimes "
    "awake. In other words, these are cases where one mistakenly believes from appearances that there is no "
    "consciousness. When such a person in a vegetative state becomes third generation, they suddenly start to move and "
    "try to kill the target. However, since their brain waves differ from those of a fully awake person, it becomes a "
    "state of complete takeover, in which the body moves but cannot be moved by their own will. In such cases, the "
    "symptoms subside if consciousness is extinguished with anesthesia or the like, but as soon as the anesthesia wears "
    "off, they try to kill the target again.",
]
R270_B2 = [
    "From the above, it is thought that the Arata cherry does not take over the person's will but, after all, acts "
    "directly on the brain and spinal cord to try to kill the target. Since the person is forced into a killing they do "
    "not want while still conscious, for the person it must be a nightmarish phenomenon. However, because carrying out a "
    "killing brings a pleasure beyond anything normally imaginable, if they drown in that desire, it is entirely possible "
    "that they will carry out the next killing half of their own will.",
]
R270_C = [
    "In the case of most test subjects, they try to kill the target regardless of their own will, but very rarely there "
    "are those who can slightly resist that urge. They are, as a rule, young people, roughly fifteen years old or under. "
    "When those who had their first period at 15 or under were driven by the urge to kill, there were cases, with a "
    "probability of about 30%, of their temporarily suppressing the urge to kill and fleeing the scene, or killing "
    "themselves.",
]
R270_D = [
    "Probably because they are at the stage of the growth period and the development of the nervous system is "
    "incomplete, the takeover by the Arata cherry is not perfect either, and it is thought that there is a gap through "
    "which the person's own will can intervene. However, that resistance does not last long either, and in the end it "
    "comes to the conclusion of killing the target.",
    "This is a personal question, but this time the test subject was a girl of tender years. It is hard to think that "
    "she was a prisoner serving life imprisonment or a condemned prisoner either. Where are the test subjects being "
    "brought from? This too is only a rumor, but I have also heard that one of our brethren offered up their own "
    "daughter as a specimen for the sake of honor within the church.",
]
_S270 = 21
_L270 = "#271a04"
_R270 = "#f30a0b"
_p270a, _e270a = _rflow(R270_A, 20, 788, 101, _S270)
_p270b, _e270b = _rflow(R270_B, 20, 788, 733, _S270)
_p270b2, _e270b2 = _rflow(R270_B2, 20, 788, _e270b + 18, _S270)
_p270c, _e270c = _rflow(R270_C, 20, 788, 1634, _S270)
_p270d, _e270d = _rflow(R270_D, 20, 788, 2208, _S270)
REP270 = ([_rtitle("Methods of Suppressing the Urge to Kill", 26, 63),
           _rerase([14, 98, 792, 429]), _rerase([14, 730, 792, 1242]), _rerase([14, 1631, 792, 1810]),
           _rerase([14, 2205, 792, 2476]),
           _r2plate("Urge to kill", [236, 516, 372, 548], [[253, 522, 346, 546]], _R270, 18),
           _r2cap("Third\ngeneration", [126, 626, 250, 668], [[139, 631, 235, 658]], 17, color=_L270, line_spacing=1.0),
           _r2cap("Second\ngeneration", [378, 624, 490, 666], [[387, 627, 482, 653]], 17, color=_L270, line_spacing=1.0),
           _r2cap("Other third\ngeneration", [494, 624, 648, 666], [[499, 627, 641, 653]], 17, color=_L270, line_spacing=1.0),
           _r2cap("It is possible to stop the killing behavior through fainting or anesthesia", [20, 671, 780, 701],
                  [[186, 672, 621, 699]], 21, color=_L270),
           _r2plate("Urge to kill", [318, 1362, 484, 1398], [[356, 1367, 448, 1391]], _R270, 18),
           _r2cap("Faint radio waves from the spores send kill orders to the third generation's brain\n"
                  "(submerging the person's own sense of self while leaving it intact)", [20, 1513, 780, 1572],
                  [[82, 1516, 719, 1542], [222, 1543, 585, 1569]], 20, color=_L270, line_spacing=1.08),
           ("Postscript", [20, 1600, 400, 1630], {"max_size": _S270, "erase": [[17, 1601, 77, 1629]]}),
           _r2cap("A third-generation girl suffering from the urge to kill (15 years old)", [20, 2144, 780, 2176],
                  [[164, 2145, 641, 2175]], 21, color=_L270)]
          + _p270a + _p270b + _p270b2 + _p270c + _p270d + _r2foot("Shiyo 733, March 30", 2511, 2541))
JOBS += [_r2job(270, REP270, "report (part 18 list; figures, brain diagram, spore photo, girl photo kept)", "#231803")]


# IMAGES18B-O1 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane O1): objects 302 303 304 305 306 307 308 309 315 241 (part 18 list).
# Handwritten memo pages (Momoko Goto's memos 1-8, Erina Goto's memo 11): the memo() precedent (ref85 / ref15 / ref132 / ref153):
# one English line per JP row, Ink Free, in the JP row, one size per page; rows and the wrap come from work/images/_c/img18bO1/mk.py
# (dark-pixel rows, band normalised to the page's row height, English wrapped evenly over each JP paragraph's rows). Latin-digit
# dates stay as drawn. 241 is pixel-identical to rrr27/0 (ref27): the ref27 job re-run on rrr241/0.gal. Cards obj<ID>-ov =
# refdoc_overview.py build <ID> (top crop at 0.375, the ov-p16 precedent; the English keeps the JP rows). The 60x30 サムネ: below
# legibility. Log: notes/v2/_tmp/tl-log-IMAGES18B-O1.md.
# IMAGES18B-O1 2026-10-15: ref 302 "Momoko Goto's Memo 1" (800x1132). memo() rows (img18bO1/mk.py); date 800.5.5 kept as drawn (Latin digits).
RO1_302 = [[39, 158, 738, 191], [39, 200, 725, 232], [39, 240, 734, 272], [39, 280, 725, 312], [39, 320, 703, 352], [39, 360, 743, 392], [39, 400, 719, 432], [39, 440, 728, 472], [39, 480, 573, 512]]
TO1_302 = [
    "I'm going to try writing this thing called a diary for the first time. It's",
    "almost a month since Erina died. I was actually going to leave home by",
    "mid-May. But since Erina died, all I do is drift through the days in a daze.",
    "What am I supposed to do with my life? Only noticing after she's dead... I'm",
    "really such an idiot. Only now do I realize how big a part of my life Erina was.",
    "I wanted to make up with her. I wanted us to always be sisters who",
    "got along. If we had been, maybe that wouldn't have happened to Erina.",
    "If I could see Erina again, I wouldn't care if my life were cut in half. I",
    "don't need the money I've saved up, either. I'd throw away everything.",
]
JOBS += [
    dict(_MEMO, id="obj302-0", screen="reference 302 detail", note="Momoko Goto's memo 1 (handwriting; date kept as drawn)",
         items=[(D + "rrr302/0.gal", "")],
         lines=memo(RO1_302, TO1_302, size=21, right=796)),
    {"id": "obj302-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr302.gal", "")]},
]
# IMAGES18B-R2 2026-10-15 (cont.): rr270 card = work/images/_c/img18b-R2/ovcard.py 270 "Methods of Suppressing the Urge to Kill"
# 4 96 98 34 chalk (1:1 window page (250, 0) on a red ground; ovprobe 0.18 was thrown off by the white chalk scribble over the text,
# which is protected and kept as drawn).
JOBS += [{"id": "rep270-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr270.gal", "")]}]
# IMAGES18B-R2 2026-10-15 (cont.) ---- 272 "Treating the Curse-Killing" (800x2047): text only: title, P1 (ends mid-sentence into
# three bullets), P2, bullet heading + P3, bullet heading + P4, P5, date, signature. One chained flow at one size from the first
# JP row (_r2chain: kind "p" = paragraph, "b" = bulleted item; the number = the gap above it in px). Ink #241904 (cores 36,25,4).
def _r2chain(seq, x0, x1, y0, size):
    out, y = [], y0
    for kind, text, gap in seq:
        y += gap
        if kind == "b":
            p, e = _r2bul([text], x0 + 32, x1, y, size)
        else:
            p, e = _rflow([text], x0, x1, y, size, gap=0)
        out += p
        y = e
    return out, y


R272 = [
    ("p", "In fact, when a member of the third generation is driven by murderous intent, there are several methods of "
          "treating it. First, we will explain the mechanism by which the murderous intent arises. The spores that remain "
          "inside the bodies of the third generation differ in quality from those of the first, second, and fourth "
          "generations. Since the fourth generation is born by transitioning from the first or second generation, it is "
          "not particularly unnatural that these three resemble one another. The third generation,", 0),
    ("b", "Regular bleeding (menstruation, habitual bloodletting)", 22),
    ("b", "Inhaling cherry pollen (it need not be the Arata cherry)", 3),
    ("b", "Encountering a member of the second or third generation in a precognitive state", 3),
    ("p", "are struck by murderous intent under these conditions. At this time, a faint electric current is generated by the "
          "spores in the body, which takes over the brain and spinal cord and makes them kill the target. As for the "
          "reason the spores emit a current, this too bears on the propagation of the Arata cherry. The Arata cherry grows "
          "fruiting bodies that mimic the cherry in clusters and gives rise to a food chain there. By making the mammals "
          "that stand at its top feed on the roots, it spreads the next infection. When a member of the third generation "
          "dies, the first and second generations around them come to hold an obsessive attachment to the corpse and "
          "gradually transition into the fourth generation. In other words, the earlier the third generation die, the "
          "sooner the propagation comes. Then why does such murderous intent arise? Conceivable reasons are:", 22),
    ("b", "When the second generation is the target of killing", 22),
    ("p", "The idea is that by making those around them learn of the third generation's murderous intent and abnormal "
          "behavior, it induces the people around them to kill the third generation. In fact, in the Arata settlement this "
          "murderous intent was called the \"Green-Eye Curse-Killing,\" and there was apparently a law that children born "
          "with green eyes were to be killed promptly (could it be that it changes the eye color so that such a "
          "distinction can be made?).", 3),
    ("b", "When the third generation is the target of killing", 22),
    ("p", "In this case, the third-generation members with murderous intent exist, with high probability, as only two "
          "individuals within the same society. If either one dies, the other's murderous intent subsides, but their "
          "mother and grandmother are likely to be first or second generation. In other words, it can be said to be a "
          "society that uses Droga. Before long, the people of that society hold an obsessive attachment to the corpse of "
          "the third-generation member, and the surviving third-generation member loses their place and leaves the "
          "society. One feature of the Arata cherry's ecology is that it grows fruiting bodies that mimic the cherry in "
          "clusters. With these it draws in insects and small animals and gives rise to a food chain around it. Then it "
          "carries out the takeover of the next society. In other words, it becomes possible to grow as many fruiting "
          "bodies as possible within a narrower area. If there were two or more members of the third generation and they "
          "died at close times, the fourth generation would be split into two groups, and it would become impossible to "
          "propagate abundantly in a narrow area. So within one society, it is more convenient for there to be one member "
          "of the third generation. The reason it is more convenient to propagate narrowly than widely is that this makes "
          "it possible to crowd together more insects and small animals, and the mammals drawn to them; in fact, this "
          "Arata cherry lives only in the Arata district. It is thought that in this way it widens its range at places "
          "that do not stray too far from the mycelial mat underground, and propagates widely over a long span of years.", 3),
    ("p", "We have digressed, but we now report the methods of treating this murderous intent of the third generation (the "
          "curse-killing urge). The first is to kill off the spores in the body themselves. For this, a drug produced as a "
          "by-product when Droga is made (hereafter called the \"wonder drug\") can be used as a remedy as it is. The other "
          "is to remove the spores from the body altogether. It has already been established that infection spreads with "
          "about 1 cc of blood; below that, symptoms such as awakening to precognition for only an instant occur, and the "
          "spores are excreted by metabolism within a few seconds (this is not limited to the third generation). In other "
          "words, if the spores are a trace amount, the curse-killing can be nullified by the human body's metabolic "
          "function. Therefore, even without using the wonder drug, if bloodletting and transfusion are repeated to thin "
          "the concentration of spores in the body, a de facto cure should be possible (however, since there is no change "
          "in the amount of melanin in the iris, the eyes remain green).", 22),
]
_S272 = 22
_p272, _e272 = _r2chain(R272, 20, 788, 101, _S272)
REP272 = ([_rtitle("Treating the Curse-Killing", 26, 63), _rerase([14, 98, 792, 1909])]
          + _p272 + _r2foot("Shiyo 733, May 6", 1944, 1975))
JOBS += [_r2job(272, REP272, "report (part 18 list; text only)", "#241904")]
# IMAGES18B-R2 2026-10-15 (cont.): rr272 card = work/images/_c/img18b-R2/ovcard.py 272 "Treating the Curse-Killing" 4 96 98 34 chalk
# (1:1 window page (250, 0) on a purple ground; ovprobe 0.21 was thrown off by the white brush graffiti over the text, which is
# protected and kept as drawn).
JOBS += [{"id": "rep272-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr272.gal", "")]}]


# IMAGES18B-O1 2026-10-15: ref 303 "Momoko Goto's Memo 2" (800x1132). memo() rows (img18bO1/mk.py); date 801.4.8 kept as drawn.
RO1_303 = [[38, 157, 724, 190], [38, 200, 722, 232], [38, 239, 730, 271], [38, 279, 722, 312], [38, 320, 730, 352], [38, 360, 171, 392], [38, 440, 746, 472], [38, 480, 735, 512], [38, 520, 720, 552], [38, 560, 696, 592], [38, 600, 735, 632], [38, 642, 195, 674]]
TO1_303 = [
    "I wondered what notebook this was, and it turned out to be my diary. I've",
    "left it untouched ever since I first wrote in it. Today was Erina's first-year",
    "memorial service, so I'll write something down for now. It seems Erina was",
    "looking into the flaying case and the Megasawa City case before she died,",
    "and I found her memos. I wanted to know the truth about the cases, so I",
    "used them as a guide and looked into all sorts of things this past year.",
    "Mifuyu Niimura and Haruka Niimura are missing. They must be",
    "the culprits. They killed Erina and ran off somewhere. I want to",
    "know why Erina had to be killed. It's not that I'm thinking of",
    "wanting to kill them, or of getting revenge. I want to know why",
    "Erina went through something like that, and what they were",
    "feeling when they killed her. I just want to know the truth.",
]
JOBS += [
    dict(_MEMO, id="obj303-0", screen="reference 303 detail", note="Momoko Goto's memo 2 (handwriting; date kept as drawn)",
         items=[(D + "rrr303/0.gal", "")],
         lines=memo(RO1_303, TO1_303, size=21, right=796)),
    {"id": "obj303-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr303.gal", "")]},
]
# IMAGES18B-R2 2026-10-15 (cont.) ---- 273 "The Role of the Spores" (800x1730): text only: title, P1, four bullet headings each
# with its paragraph, P6, date, signature. One chained flow (_r2chain, defined in the 272 segment). Ink #241803 (cores 36,24,3).
# JP typo 残留していたと胞子と結合 read as 残留していた胞子と結合.
R273 = [
    ("p", "The Arata cherry enters the bodies of mammals with Droga as its medium and makes its spores remain in the body for "
          "a long time. In the experimental results so far, the spores remain in the body for at least four years or more. "
          "The spores circulate through the body at all times together with the blood, but since they can obtain "
          "sufficient nutrients from the blood, it is thought that as long as the host is alive, these spores also go on "
          "living. The role of these spores changes with each generation.", 0),
    ("b", "In the first generation", 22),
    ("p", "Immediately after Droga is ingested, the spores secrete a large amount of α-ephedrine from within, and at the "
          "same time also promote the secretion of adrenaline and noradrenaline. This makes the sympathetic nervous system "
          "abnormally active, temporarily giving the host astonishing physical ability. This is the only symptom seen in "
          "the first generation, but the spores continue to remain.", 3),
    ("b", "In the second generation", 22),
    ("p", "At the time of infection, the spores undergo rapid cell division and stop dividing when they reach a certain "
          "amount. They react to cherry pollen (even other than the spores of the Arata cherry) and drive the autonomic "
          "nervous system into disorder. However, in this case a trigger is needed, and re-creating the time of infection is "
          "the condition. Also, since becoming second generation, except at childbirth, involves with high probability being "
          "caught up in an accident or the like in which one is drenched in a large amount of blood, there are many cases in "
          "which the situation at the time of infection becomes, as it is, a psychological disorder. However, when the host "
          "has overcome that psychological disorder, ill health is no longer seen. Why ill health is necessary for the Arata "
          "cherry is unknown, but at this stage the spores are incomplete, so both hormone secretion and precognition are "
          "probably incomplete. It is also conceivable that a collapse of the hormone balance is simply the cause of the "
          "ill health.", 3),
    ("b", "In the third generation", 22),
    ("p", "As with the second generation, cell division takes place at the time of infection. Unlike the second generation, "
          "there is no ill health, and precognition activates without re-creating the psychological disorder. The spores "
          "emit faint radio waves to the brain and spinal cord in order to kill the second- and third-generation members "
          "who have precognition. Also, when the host dies, the spores germinate on the skin, and from there they send out "
          "spores (hereafter called \"new spores\").", 3),
    ("b", "In the fourth generation", 22),
    ("p", "When the first and second generations inhale the new spores of the third generation, these combine with the "
          "spores that had remained in the body all along. In other words, the spores of the Arata cherry are sexual "
          "spores, and only here is the propagation of the Arata cherry carried out (the birth of the fourth generation). "
          "In about a year, it completely takes over the body of the fourth generation, and fruiting bodies grow.", 3),
    ("p", "From the above, considering mother-to-child infection, which is the Arata cherry's usual route of infection, the "
          "life span of the spores is forty years at the shortest, and at the longest, as long as the host is alive. "
          "However, even having investigated this far, it is unclear why precognition can be obtained. If there is such a "
          "precise biological basis up to this point, it is thought that precognition also has a scientific basis. What I "
          "am focusing on is the murderous intent of the third generation. The spores inside the bodies of the third "
          "generation must be receiving some kind of information from outside and instructing the host to kill. If the way "
          "this information from outside is received can be elucidated, the true nature of precognition can probably be "
          "exposed as well.", 22),
]
_S273 = 22
_p273, _e273 = _r2chain(R273, 20, 788, 101, _S273)
REP273 = ([_rtitle("The Role of the Spores", 26, 63), _rerase([14, 98, 792, 1575])]
          + _p273 + _r2foot("Shiyo 733, August 2", 1610, 1640))
JOBS += [_r2job(273, REP273, "report (part 18 list; text only)", "#241803")]


# IMAGES18B-O1 2026-10-15: ref 304 "Momoko Goto's Memo 3" (793x1122). memo() rows (img18bO1/mk.py); date 801.9.30 kept as drawn; the two rows of yada (14 + 14) set as 'no' x 28.
RO1_304 = [[38, 156, 718, 186], [38, 196, 739, 226], [38, 236, 725, 266], [38, 278, 734, 308], [38, 316, 526, 346], [38, 356, 737, 386], [38, 396, 737, 426], [38, 437, 729, 467], [38, 477, 98, 507], [38, 516, 721, 546], [38, 557, 727, 587], [38, 596, 714, 626], [38, 636, 722, 666], [38, 677, 740, 707], [38, 716, 732, 746], [38, 757, 730, 787], [38, 797, 599, 827], [38, 836, 724, 866], [38, 876, 739, 906], [38, 916, 720, 946], [38, 956, 752, 986], [38, 1001, 721, 1023], [38, 1041, 721, 1063]]
TO1_304 = [
    "The Niimura family apparently comes from a place called the Arata district.",
    "Those two should have nowhere else to turn. So they must be hiding in the",
    "Arata district. But even searching online and at the library, I found out",
    "almost nothing about the Arata settlement. Nowadays, it's strange for",
    "nothing at all to be known about a place. Something must be behind this.",
    "I was able to meet a professor who studies Iizawa",
    "Prefecture in cultural anthropology. When I said I",
    "was Erina's older sister, I got an appointment",
    "surprisingly easily. Erina really was that brilliant, huh.",
    "The Arata district is state-owned land; by law, ordinary citizens may not enter.",
    "Supposedly there are many unusual plants and animals, so the whole area is",
    "protected. But the professor says that's just the official line. As for the Arata",
    "settlement in the district, its people have their own culture and are closed to",
    "outsiders. That alone makes it the perfect place for Mifuyu Niimura to flee to.",
    "Apparently a certain drug was made there long ago, and the land was made",
    "state-owned so its existence wouldn't become public. The professor introduced me",
    "to someone who knows the Arata district well. I'm going to meet them tomorrow.",
    "Come to think of it, today is Erina's 17th birthday. Happy birthday,",
    "Erina. I'd never once forgotten Erina's birthday. Am I maybe starting",
    "to forget Erina? No, I don't want that. I don't want to forget Erina.",
    "I want to keep thinking about Erina forever. I don't want that.",
    "no no no no no no no no no no no no no no",
    "no no no no no no no no no no no no no no",
]
JOBS += [
    dict(_MEMO, id="obj304-0", screen="reference 304 detail", note="Momoko Goto's memo 3 (handwriting; date kept as drawn)",
         items=[(D + "rrr304/0.gal", "")],
         lines=memo(RO1_304, TO1_304, size=20, right=796)),
    {"id": "obj304-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr304.gal", "")]},
]
# IMAGES18B-R2 2026-10-15 (cont.): rr273 card = work/images/_c/img18b-R2/ovcard.py 273 "The Role of the Spores" 4 96 98 34 chalk
# (1:1 window page (250, 0) on a brown ground; ovprobe 0.26 was thrown off by the thin white handwriting over the text, which is
# protected and kept as drawn).
JOBS += [{"id": "rep273-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr273.gal", "")]}]
# IMAGES18B-R2 2026-10-15 (cont.) ---- 274 "How the Eyes Turn Green" (800x1062): title, P1, a plain heading + four bullets, P2, P3
# (one chained flow, _r2chain), a black arrow with a two-line white label (flat fill inside the arrow; the label runs 12 px into
# the arrow head as in the JP) beside an eye drawing (art, kept), date, signature. Ink #150800 (JP glyph cores 21,8,0).
R274 = [
    ("p", "Because we had been concentrating on the investigation of the fourth generation until now, the report on the "
          "third generation had been delayed, so we summarize the report here now.", 0),
    ("p", "Characteristics of the third generation", 22),
    ("b", "One eye is green", 3),
    ("b", "They have precognition equal to or greater than the second generation's", 3),
    ("b", "Sexually mature girls are driven by fierce murderous intent toward the second generation or another member of "
          "the third generation", 3),
    ("b", "They do not become the fourth generation", 3),
    ("p", "As for the reason one eye turns green, eye color is determined by the amount and density of melanin pigment in "
          "the iris. On becoming first generation, adrenaline and noradrenaline are secreted from the spores in large "
          "amounts, and the precursors of adrenaline are tyrosine-type amino acids, that is, catecholamines. Since tyrosine "
          "is also a material of melanin, there are also research results showing that when catecholamines are produced "
          "in the brain, melanin forms as a by-product. The possibility that, for some reason, a change occurs in the "
          "constitution of the third generation and the amount of melanin in the eyes changes cannot be ruled out either.", 22),
    ("p", "In any case, it is thought that such a physical trait is seen in order to let the surrounding society know that "
          "one is third generation, that is, a target to be eliminated at once.", 22),
]
_S274 = 23
_p274, _e274 = _r2chain(R274, 20, 788, 101, _S274)
REP274 = ([_rtitle("How the Eyes Turn Green", 27, 63), _rerase([14, 98, 792, 762]),
           _r2plate("Eye color can tell whether a\nfrenzy (curse-killing) will occur", [134, 829, 422, 886],
                    [[146, 830, 402, 884]], _R2BLK, 18, line_spacing=1.05)]
          + _p274 + _r2foot("Shiyo 734, February 11", 979, 1009))
JOBS += [_r2job(274, REP274, "report (part 18 list; eye drawing kept)", "#150800")]


# IMAGES18B-O1 2026-10-15: note on ref 304 (above): rrr304/0.gal and rr304.gal are Bpp 8 grey-palette originals; batch.py renders
# obj304-0 / obj304-ov and then fails at gal_write (palette refused). Encode them with work/images/_c/img18bO1/galpal.py ORIG OUT_PNG
# work/<path>.gal (rr304.png from work/images/_c/img18bO1/ovbuild.py 304). rr305 has no alpha channel: card PNG = ovbuild.py 305.

# IMAGES18B-O1 2026-10-15: ref 305 "Momoko Goto's Memo 4" (794x1123). memo() rows (img18bO1/mk.py); date 801.10.1 kept as drawn.
RO1_305 = [[46, 132, 731, 162], [46, 168, 744, 200], [46, 208, 722, 240], [46, 248, 736, 280], [46, 288, 280, 318], [46, 321, 716, 353], [46, 362, 746, 392], [46, 400, 736, 432], [46, 440, 727, 472], [46, 480, 728, 510], [46, 513, 718, 548], [46, 556, 127, 586], [46, 592, 743, 624], [46, 632, 744, 664], [46, 672, 743, 702], [46, 704, 721, 742], [46, 744, 743, 777], [46, 784, 734, 816], [46, 828, 81, 858]]
TO1_305 = [
    "I'll sum up what I heard today. The person who met with me today was",
    "someone named Shinji Tomobe, who researches physiology at Iizawa",
    "University. Tomobe-san is quite old now, more someone with an honorary",
    "post than a researcher. Tomobe-san said that long ago, he had heard",
    "about a researcher for a certain religious group, named Hajime Shinozaki.",
    "Mr. Shinozaki was trying to create something like a muscle-strength",
    "enhancer, called Droga, from the cherry trees that grow wild in the Arata",
    "settlement. But Droga's side effects were strong, and it was no use. Those",
    "side effects apparently included too great a strain on the body, and, through",
    "blood infection, other people falling into a depressed state or gaining a",
    "danger-sense ability. But it was a long time ago, so Tomobe-san was vague",
    "in places, and it was a shame that he only half remembered some parts.",
    "I've heard about danger sense from Mom. Apparently one of",
    "Erina's senpais had that kind of ability. And what's more, I heard",
    "that person was killed by Mifuyu Niimura too. It's slowly coming",
    "together. With Droga, someone could have caused the Megasawa",
    "City case too, and if that led to bad blood between the Niimura",
    "family and the Kogori family, it ties in with that flaying case as",
    "well. I see, so Erina's death is the Arata settlement's fault too.",
]
JOBS += [
    dict(_MEMO, id="obj305-0", screen="reference 305 detail", note="Momoko Goto's memo 4 (handwriting; date kept as drawn)",
         items=[(D + "rrr305/0.gal", "")],
         lines=memo(RO1_305, TO1_305, size=21, right=796)),
    {"id": "obj305-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr305.gal", "")]},
]
# IMAGES18B-R2 2026-10-15 (cont.): rr274 card = work/images/_c/img18b-R2/ovcard.py 274 "How the Eyes Turn Green" 4 96 98 34 chalk
# (1:1 window page (250, 0) on a red cracked ground; ovprobe 0.24 was thrown off by the white handwriting over the text, which is
# protected and kept as drawn).
JOBS += [{"id": "rep274-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr274.gal", "")]}]


# IMAGES18B-O1 2026-10-15: ref 306 "Momoko Goto's Memo 5" (800x2312). memo() rows (img18bO1/mk.py); date 802.4.8 kept as drawn; the chant rows (Mifuyu Niimura die x 20 + die x 7, then die x 72) wrapped over the same rows; the red scrawl below (y 1290-2215) kept as drawn (QIMAGES18BO1-02).
RO1_306 = [[39, 159, 743, 191], [39, 199, 734, 231], [39, 240, 730, 272], [39, 280, 733, 312], [39, 320, 148, 352], [39, 360, 731, 392], [39, 400, 719, 432], [39, 440, 744, 472], [39, 480, 727, 512], [39, 520, 727, 552], [39, 560, 736, 592], [39, 600, 71, 632], [39, 640, 719, 672], [39, 680, 712, 712], [39, 720, 715, 752], [39, 760, 719, 792], [39, 800, 712, 832], [39, 840, 744, 872], [39, 884, 721, 916], [39, 924, 721, 956], [39, 965, 721, 997], [39, 1005, 721, 1037], [39, 1045, 721, 1077], [39, 1085, 721, 1117]]
TO1_306 = [
    "Today was Erina's third-year memorial service. It hit me all over again",
    "that Erina is dead. Erina being murdered is just so unfair, after all.",
    "Erina wasn't the kind of girl to earn anyone's hatred. The culprit should",
    "die. If the law judged them, it would surely be the death penalty.",
    "There's no way they can be forgiven for running and hiding forever.",
    "I also looked into Erina's relationships, and there's no doubt",
    "she was on very good terms with Haruka Niimura. Killing",
    "Erina must have been Mifuyu Niimura's own decision. So the",
    "first one who should die is Mifuyu Niimura. Mifuyu Niimura",
    "should die. She has to die. Why didn't I notice that until",
    "now? That's right, Mifuyu Niimura just has to die. If the",
    "police can't catch her, I have no choice but to do it myself.",
    "Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura",
    "die Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura die Mifuyu",
    "Niimura die Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura die",
    "Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura",
    "die Mifuyu Niimura die Mifuyu Niimura die Mifuyu Niimura die Mifuyu",
    "Niimura die Mifuyu Niimura die die die die die die die die",
    "die die die die die die die die die die die die",
    "die die die die die die die die die die die die",
    "die die die die die die die die die die die die",
    "die die die die die die die die die die die die",
    "die die die die die die die die die die die die",
    "die die die die die die die die die die die die",
]
JOBS += [
    dict(_MEMO, id="obj306-0", screen="reference 306 detail", note="Momoko Goto's memo 5 (handwriting; date and the red scrawl kept as drawn)",
         items=[(D + "rrr306/0.gal", "")],
         lines=memo(RO1_306, TO1_306, size=22, right=796)),
    {"id": "obj306-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr306.gal", "")]},
]


# IMAGES18B-O1 2026-10-15: ref 307 "Momoko Goto's Memo 6" (800x1131). memo() rows (img18bO1/mk.py) on dark pixels only; pale grey / pink scribbles behind the text: inpaint of the dark glyph pixels only (ref72 highlighter precedent), so the scribbles stay under the English; date kept.
RO1_307 = [[39, 158, 729, 188], [39, 198, 741, 228], [39, 240, 735, 270], [39, 280, 375, 310], [39, 319, 744, 349], [39, 360, 714, 390], [39, 400, 720, 430], [39, 441, 738, 471], [39, 480, 234, 510], [39, 521, 722, 551], [39, 562, 738, 592], [39, 602, 746, 632], [39, 642, 264, 672], [39, 682, 735, 712], [39, 723, 712, 753]]
TO1_307 = [
    "If Mifuyu Niimura should die, then the Arata settlement that shelters",
    "her is just as guilty. I'll kill every last one of them. What should I do",
    "about Haruka Niimura? She probably hasn't done anything, and she took",
    "very good care of Erina. I'll decide what to do with her once I see her face.",
    "This past month, all I've thought about is how to kill Mifuyu Niimura and",
    "the settlement's residents. I even saw it in a dream. I only know that",
    "woman from photos, but her face as she coughed up blood beneath me, with",
    "me astride her, twisted in agony, is a magnificent sight even now when I",
    "remember it. But after that, the residents nearly killed me, and I woke up.",
    "Yes, there are a lot of people I have to kill. Realistically, killing as",
    "many as 30 people at once is hard. A knife won't do it, especially when",
    "there's something like Droga. I absolutely need something like a gun.",
    "I'll get one even if it means using up every last bit of my money.",
    "Even so, my all-important savings are running low. Since Erina died, I",
    "haven't taken many shifts at my part-time job, and everything costs money.",
]
JOBS += [
    dict(_MEMO, erase="inpaint", mask_grow=3, text_only=False, id="obj307-0", screen="reference 307 detail", note="Momoko Goto's memo 6 (handwriting; scribbles and date kept)",
         items=[(D + "rrr307/0.gal", "")],
         lines=_mk(memo(RO1_307, TO1_307, size=21, right=796), mask_color=[0, 200, 0, 200, 0, 200], mask_grow=3)),
    {"id": "obj307-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr307.gal", "")]},
]


# IMAGES18B-O1 2026-10-15: ref 308 "Momoko Goto's Memo 7" (800x2315). memo() rows (img18bO1/mk.py); two text blocks (y 157-873, 1303-1856); date 803.11.7 kept as drawn.
RO1_308 = [[39, 154, 737, 192], [39, 198, 499, 231], [39, 240, 719, 272], [39, 280, 744, 312], [39, 320, 739, 352], [39, 360, 740, 392], [39, 400, 744, 432], [39, 440, 339, 472], [39, 480, 720, 512], [39, 520, 736, 552], [39, 560, 720, 592], [39, 600, 722, 632], [39, 640, 738, 672], [39, 680, 723, 712], [39, 720, 704, 753], [39, 762, 734, 794], [39, 800, 743, 832], [39, 844, 239, 876], [39, 1302, 722, 1334], [39, 1342, 730, 1374], [39, 1384, 722, 1416], [39, 1424, 741, 1456], [39, 1464, 744, 1496], [39, 1504, 752, 1536], [39, 1544, 744, 1576], [39, 1584, 115, 1616], [39, 1624, 743, 1656], [39, 1664, 735, 1696], [39, 1704, 735, 1736], [39, 1744, 72, 1776], [39, 1784, 735, 1816], [39, 1824, 455, 1856]]
TO1_308 = [
    "Today is the second-worst day of my life. There's the phrase 'sleep on",
    "brushwood, taste gall'; for that, I'll write down what happened last night.",
    "At long last, I managed to get a gun. Not only finding a",
    "way to get one, but earning the dealers' trust took me a",
    "whole year and a half. They aren't all that interested in",
    "why I need a gun. They checked whether I was someone",
    "it was safe to sell a gun to, and whether I might report",
    "them to the police. Needless to say, I'm not a police spy.",
    "Yesterday was the day of the deal. I met the dealer for the first",
    "time. Beforehand, the guy had told me 2.5 million yen for a gun and",
    "144 bullets. Compared with the going rate I had looked up, that",
    "was outrageous. But I had no other choice. I went to meet the",
    "dealer with the cash. But I can't forget his face when we met. For",
    "a little while, he stared at my whole body and my face. And then he",
    "said, \"The going rate's gone up. You'll need 4 million yen.\" I don't",
    "have that kind of money anymore, and he knew it when he jacked up",
    "the price. Before I could answer that I couldn't, he went on:",
    "\"Spend the night with me tonight, and I'll keep it at 2.5 million.\"",
    "It was truly humiliating. Even now, the feel of him is still all over",
    "my body. But I had no option of defying him. I did everything he",
    "told me to. Everything. When morning came, he and the 2.5 million",
    "were gone. By my pillow lay the gun and bullets he had promised.",
    "When I saw them, I thought of shooting myself in the head right",
    "then and there. That's how humiliating it was. I actually put the",
    "gun to my temple. But just then, Erina's face came into my mind.",
    "If I'm going to die anyway, it'll be after I've seen it all through.",
    "Either way, I'm going to be executed as a mass murderer.",
    "In that case, I'll destroy the Arata settlement, ready to",
    "die. My money, my body, my pride, my life: I don't care if I",
    "throw them all away, if it's for Erina.",
    "I'm really such an idiot. What would Erina think if",
    "she saw me now? What is it that I'm even doing?",
]
JOBS += [
    dict(_MEMO, id="obj308-0", screen="reference 308 detail", note="Momoko Goto's memo 7 (handwriting; date kept as drawn)",
         items=[(D + "rrr308/0.gal", "")],
         lines=memo(RO1_308, TO1_308, size=21, right=796)),
    {"id": "obj308-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr308.gal", "")]},
]


# IMAGES18B-O1 2026-10-15: ref 309 "Momoko Goto's Memo 8" (800x2319). memo() rows (img18bO1/mk.py) on pixels <= 185 (the blue-grey tear stains are >= 192, the ink and the ink blurred by the stains are darker); erase = inpaint of those pixels only, so the stains stay (ref17 tear-stain precedent); the five large-type rows set in a larger size; date 804.4.6 kept.
RO1_309 = [[38, 158, 725, 188], [38, 199, 744, 229], [38, 239, 724, 269], [38, 279, 671, 309], [38, 320, 742, 350], [38, 360, 740, 390], [38, 400, 723, 430], [38, 440, 725, 470], [38, 481, 717, 511], [38, 521, 715, 551], [38, 562, 627, 592], [38, 602, 736, 632], [38, 642, 732, 672], [38, 682, 726, 712], [38, 722, 744, 752], [38, 764, 726, 794], [38, 803, 707, 833], [38, 843, 733, 873], [38, 884, 716, 914], [38, 925, 102, 955], [38, 1305, 728, 1335], [38, 1346, 490, 1376], [38, 1427, 721, 1457], [38, 1468, 740, 1498], [38, 1508, 283, 1538], [38, 1593, 745, 1640], [38, 1659, 726, 1705], [38, 1727, 687, 1774], [38, 1795, 714, 1841], [38, 1862, 510, 1908], [38, 1964, 106, 1994], [38, 2045, 258, 2075], [38, 2124, 172, 2154]]
TO1_309 = [
    "After what happened when I got the gun, my heart was in utter turmoil.",
    "A few friends used to get in touch with me now and then. Since Erina died,",
    "they had looked out for me, and sometimes met up with me too. Until",
    "that incident, I'd tried to treat my friends as normally as I could.",
    "But my heart had reached its limit too. I took it out on my friends, or",
    "ignored them. It's been about a month now with no word from",
    "anyone. They must have given up on me. Well, that's fine. Nothing good",
    "comes of getting involved with me. It's better if everyone hates me.",
    "I hate myself too. Why did I end up like this? Every bit of it is Mifuyu",
    "Niimura's fault. That woman derailed my life. I will never forgive that",
    "woman, who killed Erina and drove me mad, or the settlement.",
    "I've reached my limit. Once I had the gun, all that was left was to go to",
    "the settlement, but honestly, I was hesitating over whether I'd really go",
    "there to kill. Would I really kill as many as 30 people? Was I okay with",
    "getting the death penalty for it? But it doesn't matter anymore. Life as it",
    "is now is nothing but painful for me. In that case, I'll just end it all.",
    "Tomorrow, I'm going to the Arata settlement. Really, I should have",
    "scouted it out first, but I didn't have that much energy or money. Well, it's",
    "not that hard anyway. Once I get to the settlement, all I have to do is",
    "shoot dead everyone I meet. Okay, time to sleep. Tomorrow's an early day.",
    "it hurts it hurts it hurts it hurts it hurts it hurts it hurts it hurts",
    "it hurts it hurts it hurts it hurts it hurts it hurts it hurts it hurts",
    "I want to redo everything. I wanted to stay close with",
    "Erina. I wanted Erina to always love me. I wanted",
    "everyone to like me. I wanted to keep liking everyone.",
    "Don't talk nonsense. Be ready for all of",
    "it. What have I done all this for? My",
    "money, my body, my relationships, all",
    "wrecked to get here, so don't go whining",
    "now. I'm living only to kill people.",
    "It hurts",
    "I want to see Erina",
    "Somebody help me",
]
JOBS += [
    dict(_MEMO, erase="inpaint", mask_grow=3, text_only=False, id="obj309-0", screen="reference 309 detail", note="Momoko Goto's memo 8 (handwriting; tear stains and date kept)",
         items=[(D + "rrr309/0.gal", "")],
         lines=_mk(memo(RO1_309[0:25], TO1_309[0:25], size=21, right=796) + memo(RO1_309[25:30], TO1_309[25:30], size=36, right=796) + memo(RO1_309[30:33], TO1_309[30:33], size=21, right=796), mask_color=[0, 185, 0, 185, 0, 185], mask_grow=3)),
    {"id": "obj309-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr309.gal", "")]},
]


# IMAGES18B-O2 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane O2): overview cards only, part 18 list (scenes 147 148 236 149 150
# 151 160 161 165 166 168 243; side tales 204 205 206 207 279 280 281 282 283 290). Log notes/v2/_tmp/tl-log-IMAGES18B-O2.md.
# Cards with legible Japanese: 166 (blackboard), 206 (book page: brush heading + two handwritten lines), 279 (document page).
# Each is built by work/images/_c/img18bO2/card.py <ID> (erase the JP glyphs, set the English; see its docstring) into
# work/images/out/... and shipped here as built (mode asis, the rep<ID>-ov / ov-p16 card pattern). No title is added: the JP
# cards carry none (the IMAGES18B-L1 card rule). 206 = the book page shipped in 00000EDF-00001DB5 (heading + the two rules
# verbatim); 279 = the document in 00002199 (ref 279's body), shipped English verbatim, page-level quotes dropped.
# Skipped, no job: textless art 147 148 236 149 150 151 160 161 243 204 207 280 281 282 283 290; marks below legibility 165
# (a ~4 px katakana wall sign), 168 (blurred menu slips), 205 (blurred book pages) (QIMAGES18BO2-01..03; QIMAGES8-01 /
# QIMAGES9-02 / QIMAGES10-04 precedent). The 60x30 サムネ: below legibility, not extracted.
JOBS += [
    {"id": "ov166", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "note": "blackboard card (chalk heading + 3 lines, card.py 166)", "items": [(O + "rr166.gal", "")]},
    {"id": "ov206", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "note": "book page card (brush heading + two rules, card.py 206)", "items": [(O + "rr206.gal", "")]},
    {"id": "ov279", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "note": "document page card (tilted 12.5 deg, card.py 279)", "items": [(O + "rr279.gal", "")]},
]


# IMAGES18B-O1 2026-10-15: ref 315 "Erina Goto's Memo 11" (800x1843). memo() rows (img18bO1/mk.py), Erina's memo hand (the ref132 / ref153 pattern); the heading row one size up; the symbols (white circle, circled 1-3, middle dot, arrow) stay as drawn and the English starts after them (ref132 precedent: XO1_315 lines).
RO1_315 = [[19, 24, 551, 56], [19, 111, 780, 137], [19, 137, 783, 164], [19, 164, 273, 191], [19, 246, 784, 271], [19, 271, 784, 296], [19, 304, 95, 325], [19, 379, 768, 406], [19, 406, 781, 433], [19, 433, 770, 460], [19, 460, 784, 486], [19, 486, 702, 512], [19, 568, 611, 595], [19, 706, 723, 729], [19, 729, 782, 757], [19, 757, 605, 784], [19, 809, 431, 840], [19, 892, 781, 919], [19, 919, 780, 944], [19, 945, 476, 972], [19, 1026, 780, 1053], [19, 1053, 781, 1080], [19, 1080, 779, 1107], [19, 1109, 783, 1136], [19, 1137, 116, 1159], [19, 1215, 778, 1242], [19, 1242, 768, 1269], [19, 1269, 679, 1296], [19, 1350, 780, 1376], [19, 1377, 367, 1402], [19, 1487, 759, 1512], [19, 1512, 680, 1538], [19, 1569, 593, 1593], [19, 1593, 782, 1620], [19, 1621, 772, 1647], [19, 1647, 520, 1674], [19, 1785, 366, 1808]]
TO1_315 = [
    "Let me sum up the danger sense I experienced",
    "From what I've heard, what I experienced is a state that can actually happen.",
    "In other words, touching the blood of someone with danger sense changed my",
    "eye color, and I gained danger sense too. This is the third generation.",
    "Most of what I experienced were events inside the danger",
    "sense (from here on I'll write 'in the dream'), so there should",
    "be some differences from real danger sense. The way I see it...",
    "Probably not. That time I was able to dodge Mifuyu Niimura's attack, but",
    "if someone really did that to me, I shouldn't have the time to get out of",
    "the way. If I remember right, from sensing the danger to being attacked",
    "I had about 2 seconds. I'm not that athletic, and if it really happened, I'd",
    "panic. It was only in the dream: a hallucination made to suit me.",
    "No to this one too. That would make the real me and the me in the dream contradict each other.",
    "being third-generation, and grieved over Kogori-senpai's death.",
    "Hmm, it does contradict after all. When I was cured",
    "in the dream, the real me was still third-generation.",
    "I guess that's about it for the differences in symptoms between the dream and reality.",
    "This is a bit strange. Second generation or third generation, you can't",
    "sense danger unless you can identify the other person. Even supposing",
    "it was to protect my life, there's way too much information.",
    "With the Noh mask and the red robes, there was no way to tell who it was. No,",
    "maybe that's not so? At that point I already thought Niimura-senpai was",
    "suspicious, and next in line, Mifuyu Niimura comes up as a culprit at the same time.",
    "If it works on assumptions like that, does that mean I could recognize who it",
    "was once I thought the shinigami was Mifuyu Niimura? Hmm, it's a bit vague...",
    "This is strange too, isn't it. Simply sensing danger should have been enough, and even so,",
    "there was far too much extra information. Droga's symptoms are one thing, but frankly,",
    "the information about the people living in the Arata settlement shouldn't be needed.",
    "I thought about it a lot, but this one bugs me a little too.",
    "How do I put it... that girl's design? I guess you could call it.",
    "There's probably a reason she looked like that, too. At first I thought she stood in for",
    "Kogori-senpai, but then something like Kogori-senpai's ghost would be easier to understand.",
    "Come to think of it...",
    "Kogori-senpai said danger sense feels \"like receiving a signal from somewhere",
    "else,\" didn't she? I've only experienced it once, so I can't say for sure, but",
    "does that mean someone was sending me a signal? In other words...",
    "Hmm... this smells a little fishy...",
]
XO1_315 = [
    ("What is danger sense?", [43, 79, 796, 113], {"max_size": 18, "erase": [[40, 80, 200, 112]]}),
    ("How is the real third generation different from what I experienced?", [43, 213, 796, 246], {"max_size": 18, "erase": [[40, 214, 535, 245]]}),
    ("Can you dodge when you're attacked?", [43, 349, 796, 382], {"max_size": 18, "erase": [[40, 350, 482, 381]]}),
    ("Do you feel revulsion toward the second generation?", [45, 541, 796, 571], {"max_size": 18, "erase": [[42, 542, 378, 570]]}),
    ("The real me", [39, 593, 796, 625], {"max_size": 18, "erase": [[36, 594, 133, 624]]}),
    ("At least until Kogori-senpai woke me up, I was third-generation", [43, 621, 796, 651], {"max_size": 18, "erase": [[40, 622, 627, 650]]}),
    ("The me in the dream", [39, 646, 796, 677], {"max_size": 18, "erase": [[36, 647, 667, 676]]}),
    ("Partway through, I was injected with falsificaso, was cured of", [43, 672, 796, 706], {"max_size": 18, "erase": [[40, 673, 781, 705]]}),
    ("The content of the danger sense?", [42, 862, 796, 895], {"max_size": 18, "erase": [[39, 863, 579, 894]]}),
    ("Why could I be sure Mifuyu Niimura was the shinigami?", [43, 997, 796, 1029], {"max_size": 18, "erase": [[40, 998, 445, 1028]]}),
    ("How could I learn about people I didn't know at all?", [44, 1189, 796, 1218], {"max_size": 18, "erase": [[41, 1190, 625, 1217]]}),
    ("That girl with no eyes?", [43, 1319, 796, 1353], {"max_size": 18, "erase": [[40, 1320, 242, 1352]]}),
    ("Looks just like me", [39, 1406, 796, 1434], {"max_size": 18, "erase": [[36, 1407, 176, 1433]]}),
    ("Has no eyes", [39, 1430, 796, 1460], {"max_size": 18, "erase": [[36, 1431, 215, 1459]]}),
    ("Makes others kill people with danger sense", [39, 1456, 796, 1487], {"max_size": 18, "erase": [[36, 1457, 267, 1486]]}),
    ("Knows that Mifuyu Niimura is the culprit", [39, 1671, 796, 1702], {"max_size": 18, "erase": [[36, 1672, 401, 1701]]}),
    ("Knows the people of the Arata settlement well", [39, 1698, 796, 1731], {"max_size": 18, "erase": [[36, 1699, 469, 1730]]}),
    ("Has no eyes, is another me, and wants the people with danger sense dead", [39, 1725, 796, 1755], {"max_size": 18, "erase": [[36, 1726, 548, 1754]]}),
]
JOBS += [
    dict(_MEMO, id="obj315-0", screen="reference 315 detail", note="Erina Goto's memo 11 (handwriting; symbols kept as drawn)",
         items=[(D + "rrr315/0.gal", "")],
         lines=memo(RO1_315[0:1], TO1_315[0:1], size=24, right=796) + memo(RO1_315[1:37], TO1_315[1:37], size=18, right=796) + XO1_315),
    {"id": "obj315-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr315.gal", "")]},
]


# IMAGES18B-O1 2026-10-15: ref 241 "The Truth, 14 Years On" (800x2281): rrr241/0.png is pixel-identical to rrr27/0.png (ref27,
# shipped 2026-10-01; checked numerically, diff 0), so obj241-0 is the ref27 job (the ref-13 form at 0.8 + the handwritten
# follow-up notes, the same English) run on rrr241/0.gal. Card rr241 = rr27's JP card (diff 0): refdoc_overview.py build 241.
_O1_27 = next(j for j in JOBS if j["id"] == "ref27")
JOBS += [
    dict(_O1_27, id="obj241-0", screen="reference 241 detail",
         note="death certificate, additional = ref27's page (pixel-identical; ref27's English)", items=[(D + "rrr241/0.gal", "")]),
    {"id": "obj241-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr241.gal", "")]},
]


# IMAGES18B-L3 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane L3): 書簡 letters 219 218 285 289 (part 19 list work/untr17/refimages.txt).
# Same as lane L1 (its helper _l1jobs above is reused): face 0 (pale paper) and face 1 (gold / dark / grey paper) carry the
# same vertical text, face 1 drawn 3 px right of face 0 on all four (work/images/_c/img18bL3/align.py); English = horizontal
# blocks right to left, block 1 where the JP starts; body x0..x1 = JP ink extents (img18bL3/ink.py), block-0 erase widened
# to x0-2 .. x1+6. One job per face (ref<ID>-p0 inpaint, ref<ID>-p1 texfill) + the 概要 card ref<ID>-ov (mode asis): every
# card is a 1:1 crop of face 0 at its top right (work/images/_c/ovmatch7.py, scale 1.00, score >= 0.991), rebuilt from the
# English face 0 at the English block-0 left edge and first line (img18bL3/ovpos.py + ovcrop.py, the rr101 fix).
# 219 218 285 brush = serif (QIMAGES18BL1-01 ruling); 289 printed Mincho with ruby = serif (Cambria, printed precedent).
# 289 face 1 is a REDACTED copy: seven black scribbles over six names. ref289-p1-set sets the English on face 1 like
# face 0; img18bL3/redact289.py then blanks the six English spans marked {..} in L3_289M and pastes the seven JP scribbles
# (cut from the JP face 1, turned 90 degrees, scaled to each span) over them; ref289-p1 (asis) ships that picture
# (QIMAGES18BL3-01). The 60x30 サムネ: below legibility. Log: notes/v2/_tmp/tl-log-IMAGES18B-L3.md.


def _l3strip(s):
    return s.replace("{", "").replace("}", "")


# ---- 219 The Sealed Goddess (967x450, 27 columns, ink x 23-954): 2 blocks; card rr219 = crop (667, 0) score 0.993
L3_219 = ("Amazing. This is amazing. I've got talent. I found a mummy deep inside the underground storeroom. A mummy "
          "wearing a Noh mask and red robes. It must be one of the ancestors, no doubt about it. I proposed that we "
          "bring the mummy up above ground and enshrine it as a god. After all, when I looked into it, it turns out "
          "she's the Goddess who saved the settlement long ago! I'm the one who found the Goddess. But everyone is "
          "acting strange somehow. I thought they'd gladly agree, but they say, \"Why was it hidden in a place like "
          "that?\" and \"Wasn't it sealed away because it's something that brings disaster?\" What's with them? Does it "
          "gall them that much that I found the Goddess? Well, fine. I'll make her into a god even if I have to force "
          "it. After all, she's in the storehouse's books, so there's no mistake that she's a god. True, I also found "
          "places where it's written that the Goddess is bad news, or that she lays curses. But stuff like that is "
          "obviously superstition. Besides, I know something. In this settlement there's a medicine that is no longer "
          "used. A medicine made from the roots of the cherry trees. I looked that up in the storehouse's books too. "
          "If anyone gets in my way, maybe I'll just make them disappear with that medicine.")
JOBS += _l1jobs(219, letter(L3_219, 23, 954, 2), {0: [[21, 0, 960, 450]]}, "letter (calligraphy)")

# ---- 218 Happiness in the Next Life (954x450, 26 columns, ink x 23-941): 2 blocks; card rr218 = crop (654, 0) score 0.991
L3_218 = ("A green-eyed child was born. In accordance with the rules, we swiftly laid the child to rest. The child's "
          "mother begged, \"I will leave the settlement with the child, so please let us go.\" It has been a long while "
          "since I last saw a mother like this, but they all say the same words. If she leaves the settlement with the "
          "child, the mother will fall under the groundless suspicion of having had relations with Westerners. If the "
          "existence of Westerners comes under suspicion, the very survival of this settlement is at stake. That is "
          "why we may neither let a green-eyed child live nor let it escape. If possible, I wanted the mother to hand "
          "the child over herself, but as expected, that could not be. I too am a mother with a child. I understand "
          "her feelings so well it hurts. But through that child, danger comes to the settlement. And the first one "
          "to be killed is that mother. It pains me, but we took the child from her and cut off its head with a nata. "
          "The mother's wailing is still seared into my ears. Such is the cold and cruel deed of me, the Grand Witch. "
          "Though it was for the settlement, I took the life of an innocent baby. Will I fall into hell? But I pray "
          "that at least that child may be born to a life full of happiness in the next life.")
JOBS += _l1jobs(218, letter(L3_218, 23, 941, 2), {0: [[21, 0, 947, 450]]}, "letter (calligraphy)")

# ---- 285 The Grand Witch's Death (827x450, 23 columns, ink x 24-815): 2 blocks; card rr285 = crop (527, 0) score 0.993
L3_285 = ("The Grand Witch is dead. She was struck on the head. This must surely be the wrath of Lady Verde, of the "
          "Goddess. The Grand Witch abolished Droga, wiped out the cherry trees down to the roots, and on top of that "
          "hid Lady Verde away deep underground. How miserable we have been made to feel because of this selfish Grand "
          "Witch! We people of Arata, who lost our god, lost Droga and lost even the cherry trees, have nothing left. "
          "Yet sadly, in this settlement I am the only one who is sane. Everyone adored the Grand Witch and is "
          "grieving her death. To adore that Grand Witch, who robbed us of what was irreplaceable, is sheer madness. "
          "I have no allies. That is why only the Goddess, who brought divine punishment down on that Grand Witch, "
          "stays on my side. But if I were to call the Goddess's body back above ground now, I would be regarded as "
          "a traitor. Goddess, I am sorry. For now, please just wait for the day the Grand Witch's curse on everyone "
          "is lifted.")
JOBS += _l1jobs(285, letter(L3_285, 24, 815, 2), {0: [[22, 0, 821, 450]]}, "letter (calligraphy)")

# ---- 289 Righteous Guidance (1286x450, printed Mincho with ruby, 38 columns, ink x 38-1262): 3 blocks (ref214's 1249 px
# had 3); card rr289 = crop (986, 0) score 0.991. {..} = the spans blacked out on face 1 (redact289.py; face 0 shows all).
L3_289M = ("It has been reported that all of the research by the Shinozaki Team is finished. Only a few of us, the "
           "brethren of the Holy Cerejeira Church, remain. Now that they know the secret of Droga, which they revered as "
           "a sacred implement, it cannot be helped if their hearts turn away. But that does not mean we can disband "
           "the sect. What is needed is the will to take over the research findings and protect this country, the "
           "world, from the threat of {Shigatsu Youka}. But neither can we make this public. If the secret of Droga "
           "became known to the world, there would surely be scoundrels who would break in to misuse it. Fortunately, "
           "my efforts paid off, and we are now able to intervene to some degree even in the police organization. "
           "Should an incident occur in which Droga was used, it must be covered up at any cost. It must never become "
           "known to the public. I too have been stricken by illness and have little life left. I must pass this on "
           "to my children, and to our descendants. The {Holy Cerejeira Church} will have only this {Mikogami family} as "
           "its brethren, and will let itself fade from the memories of all others. It goes against my wishes, but it "
           "is the last righteous guidance I can give as the leader of the sect. Never lay a hand on Droga. And if "
           "anyone does lay a hand on it, dispose of them swiftly. And do not forgive those people of the {Uneme "
           "family} who split off from {Cerejeira}. Sooner or later they will surely try to rebuild the sect with the "
           "power of Droga. The only ones who may rightly bear the name of Cerejeira are we, the {Mikogami} family.")
L3_289 = _l3strip(L3_289M)
_J289 = _l1jobs(289, letter(L3_289, 38, 1262, 3), {0: [[36, 0, 1268, 450]]}, "letter (printed)")
_J289[1] = dict(_J289[1], id="ref289-p1-set",
                note="letter (printed) (face 1, grey paper: English set; the scribbles go on after, img18bL3/redact289.py)")
JOBS += _J289[:2] + [{"id": "ref289-p1", "screen": "reference 289 detail", "style": "serif", "mode": "asis",
                      "chain": True, "items": [(D + "rrr289/1.gal", "")]}] + _J289[2:]
# IMAGES18B-R3 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane R3): the finished report documents rrr<ID>/全体.gal of reports
# 284 276 275 277 (part 19 list) + their 概要 cards rr<ID>. Pattern = lanes R1 / R2 (IMAGESR-A): one chained flow per text
# group at one size per page (lane R2's _r2chain / _r2bul: kind "p" = paragraph, "b" = bulleted item, the number = the gap
# above it in px: 22 = a JP blank line, 10 = a new paragraph without a blank line (_rflow's 0.4 line), 3 = the next item),
# _rerase() erases the JP rows (texfill on the paper), _rtitle() for the title = the table row's English title. Footer =
# lane R2's _r2foot (date + lane R1's signature _R1SIG, QIMAGES18BR1-01). Ink = median of the JP glyph cores per page
# (work/images/_c/img18b-R3/col.py); end-y checks with img18b-R3/plan.py.
# ---- 284 "The Fourth Generation" (800x1806): text only: title, P1, P2 (ends in "as for the infected," into three
# bulleted items), P3 + two bullets, P4 + four bullets, P5, P6, date, signature. Ink #231803 (JP glyph cores 35,24,3).
R284 = [
    ("p", "At last enough information on the fourth generation has been gathered to report, so we summarize it in "
          "writing. First of all, we wish to state this at the outset. The existence of the Arata cherry should be erased "
          "from this world at once. It is not something humans should lay hands on (the details will be summarized at a "
          "later date on a separate sheet).", 0),
    ("p", "Now, we report anew on the existence of the fourth generation. Once more, as for the infected,", 10),
    ("b", "The first generation: users of Droga. Only after use do they have extraordinary strength, dynamic vision, "
          "and a painkilling effect.", 22),
    ("b", "The second generation: those whose mucous membranes of the head touched the blood of the first generation. "
          "Precognition (hallucinations disguised as such) and a depressive state set in when they inhale cherry pollen.", 3),
    ("b", "The third generation: those whose mucous membranes of the head touched the blood of the second generation. "
          "One eye turns green. They have precognition (hallucinations disguised as such) less limited than the second "
          "generation's, but in sexually mature girls a fierce murderous intent wells up toward the second generation and "
          "other members of the third generation.", 3),
    ("p", "These cycles should be connected to the growth and propagation of the Arata cherry, but up to this point that "
          "was not seen. Therefore we had supposed the existence of a fourth generation. To give the conclusion first, the "
          "fourth generation does exist, but it is quite different in nature from the methods of infection so far. The "
          "conditions for producing the fourth generation are as follows.", 22),
    ("b", "Being of the first generation or the second generation", 22),
    ("b", "Staying for a certain time in the same space as the corpse of a member of the third generation (no cremation "
          "or the like)", 3),
    ("p", "With this, the fourth generation is complete. That is, the first and second generations transition into the "
          "fourth generation by meeting the above conditions. The characteristics of the fourth generation are as "
          "follows.", 22),
    ("b", "An abnormal fixation on the corpse of the third generation (affection, worship, etc.)", 22),
    ("b", "A marked lack of intelligence (they lose their intelligence as time passes)", 3),
    ("b", "Death about one year after onset", 3),
    ("b", "On death, a fruiting body (a cherry tree) rapidly grows from the body", 3),
    ("p", "The fourth generation is thus one that ends up in an extremely abnormal state. This fourth generation is the "
          "final host of the Arata cherry, and it propagates by way of the first generation through to the fourth "
          "generation. At first glance it seems an abnormal ecology, but looking at the natural world, that is not "
          "necessarily so. For example, Leucochloridium, a parasite discovered in Germany in the 19th century, has "
          "similar characteristics, and if we consider the Arata cherry a somewhat deviant example of the same, its "
          "ecology too follows a cycle of sorts.", 22),
    ("p", "However, as for why it evolved to take such a roundabout method of propagation, long-term observation is "
          "needed. If additional research is to be done, it should be to seal off the Arata district and observe the "
          "ecology of the Arata cherry. Most of the Arata cherries have been cut down, but the main body must be sleeping "
          "beneath the ground there. This, however, is an extremely dangerous matter. As stated at the beginning, the "
          "Arata cherry is not something humans should be involved with. Humans must not be in the land of Arata.", 22),
]
_S284 = 22
_p284, _e284 = _r2chain(R284, 20, 788, 117, _S284)
REP284 = ([_rtitle("The Fourth Generation", 44, 80), _rerase([14, 115, 792, 1660])]
          + _p284 + _r2foot("Shiyo 734, June 2", 1691, 1721))
JOBS += [_r2job(284, REP284, "report (part 19 list; text only)", "#231803")]
# IMAGES18B-R3 2026-10-15 (cont.): rr284 card = work/images/_c/img18b-R3/ovcard.py 284 "The Fourth Generation" 8 116 117 34 chalk
# (1:1 window page (250, 0) on a brown ground, img18b-R3/winchk.py 0.80; ovprobe 0.27 was thrown off by the white handwriting over
# the text, which is protected and kept as drawn, QIMAGESRB-04).
JOBS += [{"id": "rep284-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr284.gal", "")]}]


# IMAGES18B-O3 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane O3): object 245 New Year's card (part 19 list work/untr17/refimages.txt).
# 0.png = address side (400x592, printed: the ref48 postcard pattern, serif; the vertical address columns are set top-to-bottom
# (rot -90) in the JP columns; postal-code digits, "NIPPON", the lottery digits 000000 and the stamp art kept), 1.png = picture
# side (pen-hand message: the IMAGES18B-L1 ref214 pattern, handwriting face, one horizontal block in the JP text area, signature
# rot -90); 1_1, 2..16 = flip frames (perspective views of one face) by refdoc_flip.py, shipped mode asis; rr245 = top crop of
# face 0 (refdoc_overview.py build 245). The two .lcm motion files are not pictures (no job). The 60x30 サムネ: below legibility.
# Boxes measured on the source with work/images/_c/img18bO3/meas.py / zoom.py. Log: notes/v2/_tmp/tl-log-IMAGES18B-O3.md.
_O3V = {"rot": -90, "align": "center"}
_O3K = [0, 200, 0, 200, 0, 200]           # black print and its grey edges (the red art has R > 200)
_O3R = [150, 255, 0, 215, 0, 215]         # red print and its pink edges on white
_O3W = {"method": "maskfill", "bg": "#ffffff"}
_O3RED = "#d01020"
_O3VW = dict(_O3V, **_O3W)
L245_0 = [
    ("Postcard", [166, 17, 296, 36], dict(_O3W, mask_color=_O3R, erase=[[168, 19, 294, 34]], color=_O3RED,
                                          max_size=11, align="center")),
    ("JAPAN POST", [70, 121, 114, 132], dict(_O3W, mask_color=_O3R, erase=[[72, 122, 111, 132]], color=_O3RED,
                                             max_size=7, align="center")),
    ("New Year's\nGreetings", [40, 176, 77, 210], dict(_O3W, mask_color=[120, 255, 0, 150, 0, 160],
                                                       erase=[[48, 176, 64, 192], [54, 192, 71, 208]], color=_O3RED,
                                                       max_size=9, align="center")),
    ("3 Okayori-cho, Nakajima Ward, Minakami City, Sawa Prefecture", [334, 122, 394, 442],
     dict(_O3VW, mask_color=_O3K, erase=[[337, 123, 362, 440]], max_size=16)),
    ("Sawa Prison", [246, 122, 274, 226], dict(_O3VW, mask_color=_O3K, erase=[[248, 123, 270, 223]], max_size=16)),
    ("Akane Kogori-sama", [194, 114, 238, 422], dict(_O3VW, mask_color=_O3K, erase=[[197, 117, 233, 419]], max_size=30)),
    ("Room 408, Sunshine Village, 1-12 Nakagaoka 5-chome, Motoki City, Sawa Prefecture", [48, 238, 120, 464],
     dict(_O3VW, mask_color=_O3K, erase=[[49, 239, 117, 462]], max_size=15)),
    ("Natsumi Kogori", [20, 352, 50, 460], dict(_O3VW, mask_color=_O3K, erase=[[21, 358, 49, 456]], max_size=18)),
    ("(recycled paper postcard)", [300, 505, 396, 518], dict(_O3W, mask_color=_O3R, erase=[[320, 505, 376, 518]],
                                                             color=_O3RED, max_size=8, align="right")),
    ("Drawing: Jan. 15   New Year's money handed out: Jan. 17-Jul. 17   (Bring it to a post office without cutting "
     "off the number part.)", [6, 518, 396, 531], dict(_O3W, mask_color=_O3R, erase=[[18, 519, 378, 531]],
                                                         color=_O3RED, max_size=8, align="center")),
    ("Group B0000", [24, 540, 136, 565], {"method": "inpaint", "mask_color": [0, 170, 0, 150, 40, 255], "mask_grow": 3,
                                          "erase": [[40, 541, 130, 564]], "color": "#20106a", "max_size": 15,
                                          "align": "center"}),
    ("New Year's\nmoney", [150, 538, 186, 560], {"method": "inpaint", "mask_color": [150, 255, 60, 255, 60, 255],
                                                 "mask_grow": 2, "erase": [[154, 546, 187, 558]], "color": "#ffffff",
                                                 "max_size": 9, "align": "center"}),
]
JOBS += [
    {"id": "obj245-0", "screen": "reference 245 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "thr": 60, "color": INK, "new": True,
     "note": "New Year's card, address side (postal codes, NIPPON, stamp art, lottery digits kept)",
     "items": [(D + "rrr245/0.gal", "")], "lines": L245_0},
]
# IMAGES18B-R3 2026-10-15 (cont.) ---- 276 "Three Characteristics" (800x3360): title; text group A (P1, numbered heading + P2,
# heading + P3, heading + P4, circled heading + P5 + four bullets); diagram 1 (heading on the paper; tree, dots, two figures,
# person: art, kept; white labels on two horizontal and two slanted black arrows; three paper labels) + a two-line caption;
# group B (circled heading + P6); diagram 2 (two horizontal black arrows with white labels; three paper labels) + a two-line
# caption; group C (P7); date; signature. One chained flow per group at one size (_r2chain). Arrow labels: flat fill of the
# plate colour inside boxes measured strictly inside the arrow (work/images/_c/img18b-R3/band.py + boxchk.py + cover2.py:
# slanted arrows = a row of 10 px column boxes along the shaft, every white glyph pixel covered, no paper pixel inside),
# English in white, rot = the shaft's slope (R2's _r2plate). Circled digits set as characters (Cambria has U+2460-2463).
# 菌糸 = "hyphae" (GLOSSARY + shipped), 菌床 = "mycelial mat" (QIMAGES18BR2-02), 危険予知能力 = "the ability to sense danger"
# (R2 269), 危険予知 = "danger sense" (GLOSSARY). Ink #241804 (body cores 36,24,4); labels and captions #281d08 (cores 40,29,8).
R276_A = [
    ("p", "The Arata cherry has several notable characteristics. First is its abnormal degree of gigantism. This does not "
          "mean that each cherry tree is large. The main body sleeps deep underground and has spread its roots throughout "
          "the very breeding ground. However, such a tendency toward gigantism is quite common in the natural world, so it "
          "is not particularly important. The Arata cherry shows three major characteristics not seen in other organisms.", 0),
    ("p", "1. The existence of intelligence", 22),
    ("p", "The Arata cherry shows notable intelligence. For its own prosperity it infects mammals, beginning with us "
          "humans, and uses its intelligence for growth and propagation.", 3),
    ("p", "2. Manipulation of mammals", 22),
    ("p", "This is deeply connected to the existence of intelligence, but the Arata cherry can spread hyphae throughout "
          "the bodies of mammals and take over the flesh itself. This tendency is especially marked in corpses that have "
          "completely lost consciousness. The Arata cherry extends its hyphae into the bodies of corpses whose decay has not "
          "progressed much, and manipulates them as it pleases. Moreover, since a corpse's behavior depends on the "
          "personality and intelligence the person had in life, at first glance it can even look as though they had come "
          "back to life. Thinking of it the other way around, we can assume that the Arata cherry reuses the intelligence "
          "of the people it has taken over just as it is, and the hypothesis can be made that this leads directly to the "
          "Arata cherry's intelligence. By this reasoning, if the corpses and the main body of the Arata cherry become one, "
          "it has the intelligence of the countless people who have died in Arata up to now, so it may possess an "
          "intelligence surpassing that of humans.", 3),
    ("p", "3. Five-sense perception", 22),
    ("p", "When the Arata cherry manipulates mammals in this way, it should be manipulating them based on the intelligence "
          "in its main body. However, the only thing linking the mammals and the Arata cherry is the spores in their "
          "bodies, and they are physically separated. Yet minute biological fragments such as the spores in the body do "
          "not have the power to manipulate mammals and make them use language (it is hard to think that a brain (the "
          "spores) only microns in size could manipulate mammals). That is, in order to manipulate mammals, some kind of "
          "pipe connecting the main body of the Arata cherry (the mycelial mat part) and the spores is necessary. What was "
          "put forward as a hypothesis is the so-called brain waves. That is, the mechanism is that the main body sends "
          "signals to each spore (mammal) by something like telepathy, and in response to those signals the spores run an "
          "electric current through the brain and spinal cord. From this, two things are inferred.", 3),
    ("p", "① The true nature of precognition", 22),
    ("p", "With this hypothesis, it is possible to explain the ability to sense danger. The sequence is as follows.", 3),
    ("b", "Using the countless scattered spores and cherry pollen as relay points, it probes the surroundings of all "
          "mammals", 3),
    ("b", "When a particular mammal falls into a dangerous situation, it sends a signal to the spores remaining in the "
          "bodies of the second and third generations", 3),
    ("b", "The second and third generations can learn of that mammal's dangerous situation", 3),
    ("b", "As a limitation, precognition is possible only for mammals that the second and third generations perceive with "
          "their five senses (because knowing the situation of every living thing would be too much information)", 3),
]
R276_B = [
    ("p", "② Five-sense perception", 0),
    ("p", "Under the mechanism of ①, it would be impossible unless the Arata cherry knew what the second and third "
          "generations see and hear. That is, just as signals are sent from the Arata cherry to the spores in the body, it "
          "is also possible for signals to be returned from the spores in the body to the Arata cherry. However, since the "
          "amount of information the spores in the body can sense is limited, it is thought that at most they transmit what "
          "was seen or heard, and that complex information such as thoughts is impossible.", 3),
]
R276_C = [
    ("p", "If additional research is to be done, it should be to seal off the Arata district and observe the ecology of "
          "the Arata cherry. Most of the Arata cherries have been cut down, but the main body must be sleeping beneath the "
          "ground there. As we have said before, the Arata cherry should be erased from this world at once. All the more, "
          "it is not something humans should even be permitted to take in hand. By taking Droga in hand, our ancestors "
          "brought about many sacrifices, and abandoned Droga. Scientifically too, we cannot but say that our ancestors "
          "were right. We are well aware that this statement is impermissible for the church. We will accept any "
          "punishment without complaint. We must keep humans away from the land of Arata and destroy the Arata cherry, "
          "the Goddess.", 0),
]
_S276 = 22
_p276a, _e276a = _r2chain(R276_A, 20, 788, 99, _S276)
_p276b, _e276b = _r2chain(R276_B, 20, 788, 2306, _S276)
_p276c, _e276c = _r2chain(R276_C, 20, 788, 2911, _S276)
_L276 = "#281d08"
_A3_276 = [[170, 1930, 180, 1973], [180, 1929, 190, 1970], [190, 1928, 200, 1975], [200, 1942, 210, 1983], [210, 1950, 220, 1990],
           [220, 1957, 230, 1998], [230, 1965, 240, 2006], [240, 1973, 250, 2015], [250, 1980, 260, 2021], [260, 1988, 270, 2029],
           [270, 1995, 280, 2036], [280, 2003, 290, 2044], [290, 2011, 300, 2051], [300, 2018, 310, 2059], [310, 2026, 320, 2067],
           [320, 2034, 330, 2084], [330, 2041, 340, 2083], [340, 2041, 345, 2083]]
_A1_276 = [[545, 2009, 555, 2064], [555, 2010, 565, 2067], [565, 2005, 575, 2070], [575, 1999, 585, 2051], [585, 1993, 595, 2045],
           [595, 1987, 605, 2039], [605, 1981, 615, 2033], [615, 1975, 625, 2027], [625, 1968, 635, 2021], [635, 1962, 645, 2014],
           [645, 1956, 655, 2009], [655, 1950, 665, 2002], [665, 1953, 675, 1996]]
REP276 = ([_rtitle("Three Characteristics", 26, 63), _rerase([14, 97, 792, 1612]), _rerase([14, 2302, 792, 2516]),
           _rerase([14, 2907, 792, 3182]),
           # diagram 1
           ("The mechanism of danger sense", [20, 1640, 400, 1668], {"max_size": _S276, "erase": [[16, 1640, 276, 1669]]}),
           _r2plate("② Recognizes the subject", [315, 1708, 605, 1743], [[362, 1708, 531, 1743]], _R2BLK, 20),
           _r2plate("④ Notice of danger information", [278, 1840, 550, 1866], [[328, 1840, 519, 1866]], _R2BLK, 18),
           _r2plate("③ Danger information exchange", [174, 1943, 346, 2075], _A3_276, _R2BLK, 16, rot=-37.6, rot_h=22),
           _r2plate("① Recognizes presence", [547, 1968, 677, 2049], _A1_276, _R2BLK, 16, rot=32, rot_h=22),
           _r2cap("Arata cherry", [100, 1886, 200, 1914], [[114, 1886, 185, 1913]], 18, color=_L276),
           _r2cap("Relayed via spores or pollen\n(transmissible over several hundred km)", [270, 1880, 580, 1933],
                  [[318, 1881, 530, 1932]], 18, color=_L276, line_spacing=1.0),
           _r2cap("Foresees the subject's danger", [565, 1903, 795, 1930], [[587, 1904, 793, 1929]], 18, color=_L276),
           _r2cap("Countless pollen grains and spores transmit the conditions around the subject\n"
                  "If there is anything that poses a threat nearby, the infected are notified", [16, 2219, 784, 2276],
                  [[170, 2219, 722, 2276]], 20, color=_L276, line_spacing=1.0),
           # diagram 2
           _r2plate("Five-sense information", [345, 2584, 612, 2610], [[422, 2584, 523, 2610]], _R2BLK, 18),
           _r2plate("Voices and hallucinations", [312, 2710, 582, 2735], [[393, 2710, 516, 2735]], _R2BLK, 18),
           _r2cap("Arata cherry", [92, 2769, 192, 2797], [[108, 2770, 177, 2795]], 18, color=_L276),
           _r2cap("Relayed via spores or pollen\n(transmissible over several hundred km)", [285, 2752, 595, 2805],
                  [[334, 2753, 546, 2804]], 18, color=_L276, line_spacing=1.0),
           _r2cap("Perceived information", [606, 2770, 780, 2798], [[645, 2771, 738, 2797]], 18, color=_L276),
           _r2cap("By the same principle, it is thought able to perceive the five-sense information of the infected\n"
                  "In some cases, it can also give false precognitive information", [16, 2833, 784, 2890],
                  [[152, 2833, 723, 2890]], 20, color=_L276, line_spacing=1.0)]
          + _p276a + _p276b + _p276c + _r2foot("Shiyo 734, December 7", 3246, 3276))
JOBS += [_r2job(276, REP276, "report (part 19 list; tree / figures / dots kept; arrow labels re-set)", "#241804")]


# IMAGES18B-O3 2026-10-15 (cont.): ref 245 face 1 = picture side (rrr245/1, 400x592): pen-hand message in 10 vertical columns
# (ink x 224-371, y 318-569) + signature column (x 208-218, y 503-566) on a pale green gradient. The IMAGES18B-L1 ref214 pattern:
# handwriting face, one horizontal English block (letter(), n 1) in the JP text area, signature rot -90; erase = inpaint of the
# glyph pixels (G <= 192; the gradient ground has G >= 204 in the box). "A Happy New Year!", the art and the photo are kept.
_O3M1 = [0, 200, 0, 192, 0, 200]
L245_1 = [
    ("Happy New Year! Let's stay well in Shiyo 815 too! I told you this at our last visit too, but I finally moved into a "
     "new apartment building! It's a fairly new apartment building called Sunshine Village. As you can see in the photo, "
     "it's pretty big and impressive! I wrote the address on the front too, so please send your letters here! I'll come "
     "to see you again!", [222, 318, 376, 570], {"max_size": 20, "line_spacing": 1.12, "erase": [[220, 315, 377, 572]]}),
    ("Natsumi Kogori", [203, 498, 223, 572], {"rot": -90, "max_size": 26, "align": "right", "erase": [[205, 500, 222, 570]]}),
]
JOBS += [
    {"id": "obj245-1", "screen": "reference 245 detail", "style": "handwriting", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 3, "mask_color": _O3M1, "color": "#2e3826", "new": True,
     "note": "New Year's card, picture side (handwriting; art, photo and the English greeting kept)",
     "items": [(D + "rrr245/1.gal", "")], "lines": [(t, b, dict(o, mask_color=_O3M1)) for t, b, o in L245_1]},
]
# IMAGES18B-R3 2026-10-15 (cont.): rr276 card = work/images/_c/img18b-R3/ovcard.py 276 "Three Characteristics" 4 96 98 34 orangewhite
# (1:1 window page (250, 0) on a green ground, img18b-R3/winchk.py 0.73; the orange brush scribble over the text is protected and
# kept as drawn, QIMAGESRB-04; R1's mode "orangewhite").
JOBS += [{"id": "rep276-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr276.gal", "")]}]


# IMAGES18B-O3 2026-10-15 (cont.): ref 245 flip frames (refdoc_flip.py 245 <seq> 0,1 --mode full, four chained sequences from the
# flattest view to the edge-on one: 1_1,2,3,4 / 9,10,11,12 (face 0) and 8,7,6,5 / 16,15,14,13 (face 1); log
# work/images/_c/img18bO3/flip-full1.log). Face 0 frames: match 3.9-6.3 (4: 12.5, 12: 9.2, the edge-on ones). Face 1 frames were
# rendered from another revision of the picture side (lighter green ground, message columns broken differently), so the raw
# match stays 16-28 although the geometry registers: high-pass NCC on the unchanged art (img18bO3/flipchk.py) 0.85-0.87 for
# 16 15 8 7 6, 0.77 for 14, 0.66 for 13; the frames now show the English face 1 with the final picture's colours. Frame 5 (76 px
# wide, edge-on back view) did not register (NCC -0.02): no job, the Japanese original stays (the ref34 frame-10 precedent;
# QIMAGES18BO3-06). The two .lcm motion files are not touched.
_O3F = [("1_1", "serif"), ("2", "serif"), ("3", "serif"), ("4", "serif"), ("6", "handwriting"), ("7", "handwriting"),
        ("8", "handwriting"), ("9", "serif"), ("10", "serif"), ("11", "serif"), ("12", "serif"), ("13", "handwriting"),
        ("14", "handwriting"), ("15", "handwriting"), ("16", "handwriting")]
JOBS += [{"id": "obj245-%s" % n, "screen": "reference 245 flip frames", "style": st, "mode": "asis", "chain": True,
          "items": [(D + "rrr245/%s.gal" % n, "")]} for n, st in _O3F]


# IMAGES18B-O3 2026-10-15 (cont.): rr245 card = refdoc_overview.py build 245 (top crop (0, 0, 400, 227) of the English face 0 at
# 0.75, probe 11.25; the card's own alpha kept). The card carries no title (the JP card has none: a crop of the address side).
JOBS += [{"id": "obj245-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr245.gal", "")]}]
# IMAGES18B-R3 2026-10-15 (cont.) ---- 275 "The Purpose of Falsificacao" (800x1243): title (= the table row's English title,
# verbatim: QIMAGES18BR3-03), P1, P2; a diagram (black deer, two black arrows, red deer: art, kept; a tall black bar with the
# vertical label ドローガ over a dashed line (kept) and 相殺 below it, beside a shorter black bar with the vertical label 特効薬;
# paper labels 根を捕食 / the caption under the bars / a two-line label under the red deer); P3; date; signature. Vertical bar
# labels: flat fill of the bar colour inside boxes strictly inside the bar (boxchk.py: no paper pixel), English in white set
# top-down (rot -90, the series precedent for vertical JP lines). 特効薬 = "wonder drug" (GLOSSARY, rulings-P18, lane R2's 272).
# Ink #241803 (body cores 36,24,3); labels #271c05 (cores 37-40,26-30,5-8).
R275_A = [
    ("p", "As a method of treating the curse-killing, the most effective method is to give an intramuscular injection of "
          "the wonder drug that appears as a by-product when Droga is produced. With this, the spores in the body quickly "
          "die off, and the green eyes also return to normal. No notable side effects are seen either. We investigated "
          "why the wonder drug comes into being as a by-product.", 0),
    ("p", "To begin with, wild animals prey on the roots of the Arata cherry and so strengthen their muscles. In other "
          "words, they are eating Droga and the wonder drug at the same time. If they did not take in the wonder drug, the "
          "same phenomena as with the vaporized intake and the liquefied intake in the earlier experiments would occur: "
          "that is, a severe strain on the body and a state of elation. By also taking in the components of the wonder "
          "drug at the same time, which keep that under control to a certain degree, they can strengthen their muscles, "
          "if not as much as with vaporization or liquefaction, and hold down the state of elation. Thus they succeed in "
          "holding down excessive strain on the body.", 22),
]
R275_B = [
    ("p", "Originally, if it is to be used as a muscle-strengthening agent, eating the roots as they are would be ideal, "
          "but since that is difficult for humans, the method of use since ancient times has been to refine them and "
          "extract only the Droga for use. Eating the roots is, to put it in a comparison, like taking in a poison and its "
          "remedy at the same time, and taking in only refined Droga is the same as taking into the body only the poison "
          "that is the muscle-strengthening agent.", 0),
]
_S275 = 22
_p275a, _e275a = _r2chain(R275_A, 20, 788, 99, _S275)
_p275b, _e275b = _r2chain(R275_B, 20, 788, 944, _S275)
_L275 = "#271c05"
_V275 = {"rot": -90, "align": "center", "color": "#ffffff", "method": "flat", "bg": "#010101"}
REP275 = ([_rtitle("The Purpose of Falsificacao", 26, 63), _rerase([14, 97, 792, 521]), _rerase([14, 942, 792, 1125]),
           ("Droga", [356, 562, 401, 668], dict(_V275, max_size=20, erase=[[358, 570, 400, 665]])),
           ("Offset", [356, 682, 401, 770], dict(_V275, max_size=20, erase=[[358, 702, 400, 756]])),
           ("Wonder drug", [413, 676, 459, 770], dict(_V275, max_size=20, erase=[[416, 682, 456, 766]])),
           _r2cap("Eats the roots", [60, 720, 235, 748], [[97, 721, 196, 748]], 20, color=_L275),
           _r2cap("The excess of Droga is offset by the wonder drug", [180, 791, 625, 821], [[241, 792, 582, 820]], 20,
                  color=_L275),
           _r2cap("Suppresses elation and strain\n(infection does occur)", [505, 851, 795, 907], [[540, 852, 770, 906]], 20,
                  color=_L275, line_spacing=1.0)]
          + _p275a + _p275b + _r2foot("Shiyo 734, December 7", 1158, 1188))
JOBS += [_r2job(275, REP275, "report (part 19 list; deer / arrows / bars kept; bar and paper labels re-set)", "#241803")]
# IMAGES18B-R3 2026-10-15 (cont.): rr275 card = work/images/_c/img18b-R3/ovcard.py 275 "The Purpose of Falsificacao" 4 96 98 34 bw mirror
# (the card is a MIRRORED 1:1 window onto page (250, 0), img18b-R3/winchk2.py 0.43 mirrored vs 0.21 plain; the table row notes
# ミラー; faint page text under a bold black handwritten overlay, which is protected and kept as drawn, QIMAGESRB-04; R1 rr41 pattern).
JOBS += [{"id": "rep275-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr275.gal", "")]}]


# IMAGES18B-O4 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane O4): objects 175 (0 + 部分拡大1) 184 249 (part 19 list) + 250 (0 + 1)
# 252 258 259 (part 20 list) + 262 (part 21) + 266 (part 22). Job ids obj<ID>-<page> (obj175-zoom1 = rrr175/部分拡大1) and
# obj<ID>-ov (the 概要 card, mode asis; every card is a top crop of its page, rebuilt from the English page by
# refdoc_overview.py build / img18bO4/ovbuild.py). Pen-hand pages = memo() + Ink Free (img18bO4/mk.py, the O1 / ref189
# pattern); printed pages = Cambria; brush letter = serif (QIMAGES18BL1-01). Log: notes/v2/_tmp/tl-log-IMAGES18B-O4.md.
# The 60x30 サムネ: below legibility, not extracted. rrr250/1.gal (5-frame dissolve of page 0, no legible glyph): no job.
# IMAGES18B-O4 2026-10-15: ref 250 "Eiichiro Niimura's Letter" (800x1132). page 0 only (1.gal = a 5-frame dissolve of this page, text below legibility in every frame: skipped). memo() rows (img18bO4/mk.py), the ref189 / ref153 ruled-letter pattern: one English line per JP row, inside the rules (right 690); signature right-aligned in its row.
RO4_250 = [[113, 144, 680, 174], [113, 193, 687, 224], [113, 248, 681, 275], [113, 296, 679, 327], [113, 352, 682, 376], [113, 400, 696, 432], [113, 456, 684, 480], [113, 504, 681, 536], [113, 560, 687, 584], [113, 609, 687, 640], [113, 661, 688, 688], [113, 712, 688, 742], [113, 768, 243, 792]]
TO4_250 = [
    "Sakura, thank you for everything up to now. You were",
    "always, always by my side, Sakura, and I think I was truly",
    "blessed. But I can't stay here anymore. You held me back",
    "together with my brother, but I've decided to leave",
    "Arata after all. I'm leaving Arata Station at 8 this",
    "morning, so by the time you're reading this, Sakura, I'll",
    "already be gone. Because of me, you broke the rule, Sakura,",
    "and on top of that made everyone lie. Even if you stay with",
    "me, I'll surely just be a burden. I can't keep leaning on your",
    "kindness anymore, Sakura. I'll find happiness my own way,",
    "with my own strength. Please, Sakura, be happy too. I",
    "may come home for a visit now and then, but if you don't",
    "want to see me, that's fine too. I'm really sorry.",
]
JOBS += [
    dict(_MEMO, id="obj250-0", screen="reference 250 detail", note="Eiichiro Niimura's letter (ruled paper)",
         items=[(D + "rrr250/0.gal", "")],
         lines=memo(RO4_250, TO4_250, size=22, right=690) + [("Eiichiro Niimura", [400, 868, 690, 897], {"max_size": 22, "align": "right", "erase": [[562, 869, 688, 896]]})]),
    {"id": "obj250-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr250.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 252 "Sakura Niimura's Letter" (800x1132). memo() rows (img18bO4/mk.py), the ref189 / ref153 ruled-letter pattern: addressee row, one English line per JP row inside the rules (right 750), signature right-aligned in its row; the grey rules stay (text_only).
RO4_252 = [[52, 112, 744, 138], [52, 160, 744, 192], [52, 213, 736, 240], [52, 264, 744, 296], [52, 317, 743, 344], [52, 368, 743, 395], [52, 417, 745, 448], [52, 470, 741, 498], [52, 523, 743, 552], [52, 574, 743, 600], [52, 624, 746, 655], [52, 678, 384, 703]]
TO4_252 = [
    "It's been a week. This is Sakura. I'm sorry that the other day,",
    "though I listened to what you came to me about, I couldn't help",
    "with anything. But I've thought it over since then, and thought",
    "about whether I could help you even a little, Mifuyu-chan. In this",
    "box are natas and maces that Shirozaki-san made, Noh masks, and red",
    "robes, two of each. If you sell these, you shouldn't have trouble",
    "getting by for a few months. But unfortunately, ongoing support",
    "goes against the rule, so it's hard for me to help any more than this.",
    "Please put these to good use. I'll think more, too, about how I can",
    "help you and the others, Mifuyu-chan. But please, use these to",
    "exchange for money. I absolutely did not send them to you as weapons.",
    "Well then, let's meet at Soichiro's third-year memorial service next.",
]
JOBS += [
    dict(_MEMO, id="obj252-0", screen="reference 252 detail", note="Sakura Niimura's letter (ruled paper)",
         items=[(D + "rrr252/0.gal", "")],
         lines=memo(RO4_252, TO4_252, size=22, right=750) + [("Mifuyu Niimura-sama", [46, 56, 450, 90], {"max_size": 22, "erase": [[47, 58, 186, 88]]}), ("Sakura Niimura", [400, 727, 750, 758], {"max_size": 22, "align": "right", "erase": [[618, 729, 747, 757]]})]),
    {"id": "obj252-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr252.gal", "")]},
]
# IMAGES18B-R3 2026-10-15 (cont.) ---- 277 "External Release of the Reports" (800x970): text only: title; P1 + two bulleted
# conditions + its continuation + two more bulleted conditions + its continuation (the JP sentence runs on after the second list:
# lower-case continuation, lane R2's 272 pattern); P2; P3; one footer row = date + the writer's name only (no church / team line
# on this page, so not _R1SIG). One chained flow at one size (_r2chain). 氏 = "Ms." (lane O1's 氏 = "Mr." precedent; 彼女 on the
# page). Ink #231803 (JP glyph cores 35,24,3).
R277 = [
    ("p", "This investigation of Droga and the Arata cherry was made possible by the goodwill of Ms. Kikyo Niimura, an "
          "original resident who is called \"the Grand Witch.\" However, two conditions were set at that time.", 0),
    ("b", "Not to lay hands on the cherry trees of the Niimura main family (to preserve the samples)", 3),
    ("b", "To disclose the results of the reports", 3),
    ("p", "Those were the conditions. In particular, as for the latter, she wished to be told promptly once a treatment "
          "for the side effects caused by Droga was found, so we will now compile this report and provide it to Ms. "
          "Niimura. At that time we set conditions of our own as well,", 3),
    ("b", "That the reports not be taken outside the settlement", 3),
    ("b", "That they be kept under strict control", 3),
    ("p", "those two. She said these posed no problem either, so the other day we provided the reports to Ms. Niimura.", 3),
    ("p", "According to what she said, she had been especially troubled by the killings by the green-eyed and the mass "
          "disappearances, and it seems that for her it would be enough just to find a lead toward solving them. This "
          "report will probably be of use.", 22),
    ("p", "Truly, I would like to study the Arata cherry more deeply, but it seems that part of the information in this "
          "report has leaked within the church as well, and it will probably no longer be possible to keep up appearances "
          "as a religious group. If permitted, I would like to continue the investigation personally, but what will become "
          "of me, who made this report that is in effect a written accusation? However, the ancestors of Megasawa, "
          "beginning with Kichizo-sama, truly sought to guide us toward our happiness. I know that there was no falsehood "
          "in their hearts. It is only that they mistook the object of their worship. The Goddess, no, the evil god called "
          "Shigatsu Youka.", 10),
]
_S277 = 22
_p277, _e277 = _r2chain(R277, 20, 788, 99, _S277)
REP277 = ([_rtitle("External Release of the Reports", 26, 63), _rerase([14, 97, 792, 855])]
          + _p277
          + [("Shiyo 735, January 9", [16, 886, 290, 916], {"max_size": 21, "erase": [[10, 884, 430, 919]]}),
             ("Hajime Shinozaki", [300, 886, 600, 916], {"max_size": 21, "erase": []})])
JOBS += [_r2job(277, REP277, "report (part 19 list; text only; footer = date + name)", "#231803")]



# IMAGES18B-O5 2026-10-15 (notes/IMAGES18B-BRIEF.md, lane O5): overview cards only: part 19 scenes 242 246 177 244 180 181
# 185 186 187 188 247 248 + side tales 291 292 293 294 (work/untr17/refimages.txt); part 20 scenes 251 253 254 256 257 297 260
# (work/untr18); part 21 scenes 261 267 298 263 299 264 265 (work/untr19). Log notes/v2/_tmp/tl-log-IMAGES18B-O5.md.
# NO JOBS: every SOURCE card (300x169) was read at 2x and the candidates zoomed at 3-12x (work/images/_c/img18bO5/sheet*.png, z*.png).
# Skipped, no job: textless art 242 (office: pillar plaque and door plate blank) 177 244 (a round mesh of loops, no characters)
# 180 181 185 186 187 188 247 248 291 292 293 294 251 254 257 297 260 261 267 298 263 299 264 265; marks below legibility
# 246 (spreadsheet cells on a laptop screen), 253 (car license plate), 256 (phone bezel logo) (QIMAGES18BO5-01..03; the
# QIMAGES18BO2-01..03 / QIMAGES8-01 / QIMAGES9-02 precedent). The 60x30 サムネ: below legibility, not extracted.
# IMAGES18B-R3 2026-10-15 (cont.): rr277 card = work/images/_c/img18b-R3/ovcard.py 277 "External Release of the Reports" 4 96 98 34 dark mirror
# (the card is a MIRRORED 1:1 window onto page (250, 0), img18b-R3/winchk2.py + a flipped comparison; faint page text on a light
# pink ground under thin black pen handwriting, which is protected and kept as drawn, QIMAGESRB-04; protect mode "dark" =
# every channel < 120, the counterpart of the simple "white" mode, QIMAGES18BR3-04).
JOBS += [{"id": "rep277-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
          "items": [(O + "rr277.gal", "")]}]


# IMAGES18B-O4 2026-10-15: ref 258 "Erina Goto's Memo 12" (800x1362). memo() rows (img18bO4/mk.py), Erina's memo hand (the ref315 pattern); the heading one size up; the six boxed rows in their own size (their English is ~1.6x the JP and the box is fixed), set from 5 px right of the kept bullet (XO4_258); the box border and the four arrow rows stay as drawn.
RO4_258 = [[10, 49, 672, 82], [10, 110, 414, 134], [10, 134, 166, 157], [10, 161, 248, 183], [10, 183, 331, 207], [10, 233, 459, 256], [10, 282, 459, 304], [10, 504, 759, 530], [10, 530, 264, 552], [10, 554, 594, 578], [10, 582, 352, 602], [10, 604, 449, 627], [10, 630, 697, 654], [10, 654, 364, 676], [10, 704, 791, 728], [10, 728, 533, 752], [10, 777, 792, 800], [10, 805, 98, 824], [10, 854, 544, 876], [10, 904, 491, 926], [10, 926, 791, 950], [10, 950, 792, 975], [10, 975, 770, 1000], [10, 1001, 139, 1024], [10, 1049, 791, 1072], [10, 1078, 56, 1096], [10, 1101, 479, 1122], [10, 1126, 799, 1148], [10, 1151, 781, 1174], [10, 1174, 720, 1197], [10, 1222, 758, 1248], [10, 1248, 656, 1272], [10, 1296, 414, 1320]]
TO4_258 = [
    "Sudden news from Niimura-senpai's mother!!!",
    "Murders every year in the Arata settlement, where her family home is!",
    "The old people's suicides!",
    "A body dead from a fall, with its head cut off!",
    "Killed not with a knife, but with a blunt weapon!",
    "What on earth awaits ahead...!?",
    "For now, if I sum up what's happening...",
    "That's about all that's clear as fact, but there must be a contradiction in here.",
    "What we do know is the method of killing.",
    "Chigaya-san testifies that she killed them with a knife, but they were actually beaten to death.",
    "That's strange... No matter how you look at it, it's strange!",
    "In other words, it's possible Chigaya-san didn't kill them.",
    "The other thing that bugs me: Chigaya-san apparently has precognition like Kogori-senpai's, too.",
    "If I tie this in...",
    "Chigaya-san's precognition isn't precognition; she's receiving a signal",
    "sent from someone. (Kogori-senpai once said it feels like that, too)",
    "In other words, it's possible that someone is making Chigaya-san",
    "hallucinate and hear things: \"I killed them with a knife.\"",
    "There's only 1 answer to look for. All that's left is to track down who that someone really is.",
    "I see, I'm gradually starting to see what precognition really is, too.",
    "Precognition could be thought of as a trap to make what the precognitive",
    "says believable. If Kogori-senpai told me, \"It's dangerous, so do X,\" I'd do",
    "exactly that too, after all. So if Kogori-senpai received a will with malice",
    "in it, the people around her would end up in danger instead.",
    "But what I don't get is why someone was making",
    "Chigaya-san hallucinate and hear things like that.",
    "Oh, I get it! A scapegoat for when push comes to shove!",
    "I don't know if 'someone' is human or not, but if it's a being nobody has recognized",
    "until now, then 'someone' probably wants to keep hiding what it really is. So as long",
    "as there's even one person convinced 'I'm the culprit,' it can get away. Is that it?",
    "But still... then why is there such a fatal difference as a knife versus a blunt weapon...",
    "Well, I guess I can think about this after I actually meet Chigaya-san.",
    "Alright! Tomorrow I'm eating a feast at a ryotei!",
]
XO4_258 = [
    ("Until Shiyo 789, old people kept killing themselves", [25, 330, 772, 359], {"max_size": 15, "erase": [[22, 331, 392, 358]]}),
    ("Shiyo 790, Sakura Niimura-san threw herself to her death, and her head was cut off", [25, 354, 772, 383], {"max_size": 15, "erase": [[22, 355, 557, 382]]}),
    ("Shiyo 791 to Shiyo 795, Chigaya Niimura-san killed residents who suspected her father was the culprit, one by one", [25, 380, 772, 409], {"max_size": 15, "erase": [[22, 381, 763, 408]]}),
    ("Shiyo 793 to Shiyo 795, that father was kept under constant watch (he asked for it himself)", [25, 403, 772, 433], {"max_size": 15, "erase": [[22, 404, 771, 432]]}),
    ("From Shiyo 796, they happen even though Chigaya-san didn't do it herself (the residents' doing?)", [25, 428, 772, 458], {"max_size": 15, "erase": [[22, 429, 732, 457]]}),
    ("From Shiyo 798, Chigaya-san is in Tokyo for school (they happen with Chigaya-san not there)", [25, 452, 772, 483], {"max_size": 15, "erase": [[22, 453, 670, 482]]}),
]
JOBS += [
    dict(_MEMO, id="obj258-0", screen="reference 258 detail", note="Erina Goto's memo 12 (handwriting; bullets, arrows and the box kept as drawn)",
         items=[(D + "rrr258/0.gal", "")],
         lines=memo(RO4_258[0:1], TO4_258[0:1], size=26, right=792) + memo(RO4_258[1:33], TO4_258[1:33], size=18, right=792) + XO4_258),
    {"id": "obj258-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr258.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 259 "Erina Goto's Memo 13" (800x1510). memo() rows (img18bO4/mk.py), Erina's memo hand (the ref315 / 258 pattern); the heading one size up; circled numbers, arrows, the white circle and the bullets stay as drawn and the English starts after them (XO4_259); row 22 is split around its arrow.
RO4_259 = [[20, 26, 748, 56], [20, 139, 751, 162], [20, 166, 360, 191], [20, 272, 471, 296], [20, 462, 318, 485], [20, 676, 227, 699], [20, 703, 144, 726], [50, 811, 200, 833], [20, 918, 770, 943], [20, 943, 771, 968], [20, 973, 93, 994], [20, 1024, 360, 1048], [20, 1052, 772, 1076], [20, 1081, 93, 1102], [20, 1107, 471, 1128], [20, 1134, 771, 1157], [20, 1158, 365, 1185], [20, 1187, 471, 1210], [20, 1214, 759, 1238], [20, 1240, 759, 1264], [20, 1376, 773, 1399], [20, 1401, 770, 1425], [20, 1429, 426, 1452]]
TO4_259 = [
    "Check whether there's anything Chiga-nee didn't tell us!",
    "died every year. For the first 5 years Chiga-nee did it with her own hands, but for the 4",
    "years after that, people died even though Chiga-nee has no memory of killing them.",
    "she's the one who killed them, but given the situation, there's a contradiction.",
    "death). After that, it happens every April (the dates vary)",
    "Right now I'm on the bullet train home.",
    "Goto's analysis!",
    "whether there's anything in the Arata settlement that nobody knows",
    "From what I've heard, Droga apparently has been made since hundreds of years",
    "ago. And by Westerners who came over to Japan back then, at that. In other",
    "words, there should be foreign languages mixed in with the archaic language.",
    "And the important thing is to doubt everything.",
    "On top of things that defy common sense getting mixed in,",
    "'someone' must have gotten ahead of us many times over.",
    "For example, trying to frame Chiga-nee as the culprit.",
    "That way, if someone arrives at Chiga-nee being the culprit,",
    "the chances of them getting as far as 'someone' go down.",
    "Speaking of things that defy common sense, what could there be?",
    "The existence of Droga and things like telepathy has already become clear.",
    "Things like this that look like nothing but paranormal phenomena may well become obstacles too.",
    "Things like that have to be kept in view too. But there must definitely be a scientific",
    "basis for them. If you write off unknown phenomena as nothing but paranormal",
    "phenomena, no matter how things turn out, you'll never get to the truth, after all.",
]
XO4_259 = [
    ("What happened in the Arata settlement? (What)", [45, 82, 792, 111], {"max_size": 18, "erase": [[42, 83, 409, 110]]}),
    ("After Sakura-san killed herself, her head was cut off by Kotaro-san. After that, 1 person", [45, 109, 792, 138], {"max_size": 18, "erase": [[42, 110, 776, 137]]}),
    ("Who was killed, and who killed them (Who/Whom)", [45, 215, 792, 246], {"max_size": 18, "erase": [[42, 216, 431, 245]]}),
    ("The people killed were all people who had doubts about Kotaro-san. Chiga-nee says", [45, 243, 792, 273], {"max_size": 18, "erase": [[42, 244, 774, 272]]}),
    ("How were they killed (How)", [45, 325, 792, 353], {"max_size": 18, "erase": [[42, 326, 376, 352]]}),
    ("Every head was smashed. But Chiga-nee thought she'd stabbed them to death with a knife.", [45, 349, 792, 379], {"max_size": 18, "erase": [[42, 350, 762, 378]]}),
    ("When did the cases happen (When)", [45, 405, 792, 434], {"max_size": 18, "erase": [[42, 406, 321, 433]]}),
    ("The first trigger was Shiyo 790, April 17 (Sakura-san's", [45, 431, 792, 461], {"max_size": 18, "erase": [[42, 432, 787, 460]]}),
    ("Where did the cases happen? (Where)", [45, 511, 792, 541], {"max_size": 18, "erase": [[42, 512, 376, 540]]}),
    ("The Arata settlement", [45, 539, 792, 569], {"max_size": 18, "erase": [[42, 540, 134, 568]]}),
    ("Why did cases like these happen (Why)", [45, 592, 792, 623], {"max_size": 18, "erase": [[42, 593, 376, 622]]}),
    ("What I asked Chiga-nee to do", [45, 754, 792, 783], {"max_size": 18, "erase": [[42, 755, 240, 782]]}),
    ("Go to the Arata settlement as soon as possible, and look into", [32, 781, 792, 811], {"max_size": 18, "erase": [[29, 782, 761, 810]]}),
    ("If there's writing she can't read in the storehouse's books or such, have her send photos", [32, 861, 792, 891], {"max_size": 18, "erase": [[29, 862, 603, 890]]}),
    ("Dead people moving", [32, 1265, 792, 1293], {"max_size": 18, "erase": [[29, 1266, 295, 1292]]}),
    ("Reading minds", [32, 1292, 792, 1321], {"max_size": 18, "erase": [[29, 1293, 183, 1320]]}),
    ("Teleportation", [32, 1317, 792, 1347], {"max_size": 18, "erase": [[29, 1318, 140, 1346]]}),
    ("Being able to kill just by willing it", [32, 1346, 792, 1374], {"max_size": 18, "erase": [[29, 1347, 250, 1373]]}),
]
JOBS += [
    dict(_MEMO, id="obj259-0", screen="reference 259 detail", note="Erina Goto's memo 13 (handwriting; circled numbers, arrows, circle and bullets kept as drawn)",
         items=[(D + "rrr259/0.gal", "")],
         lines=memo(RO4_259[0:1], TO4_259[0:1], size=24, right=792) + memo(RO4_259[1:23], TO4_259[1:23], size=18, right=792) + XO4_259 + [("Doubt everything", [32, 836, 203, 863], {"max_size": 18, "erase": [[29, 837, 203, 862]]}), ("this is essential for finding the root of the Why", [230, 836, 792, 863], {"max_size": 18, "erase": [[229, 837, 617, 862]]})]),
    {"id": "obj259-ov", "screen": "reference screen previews", "style": "handwriting", "mode": "asis", "chain": True,
     "items": [(O + "rr259.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 184 "Notice of Removal from Enrollment" (800x1132, printed notice on white, page frame x 32/767 y 32/1099).
# Cambria (printed precedent), glyph mask = every channel <= 130 (the red seal over 京東大学 / 学長 is never in the mask and stays as
# drawn), inpaint; header lines in their rows (right-aligned as the JP); body re-wrapped at 22 px, one entry per line (pitch 38,
# paragraph gap 12; img18bO4/mk184.py) because the JP underline under 本日をもって除籍しました is redrawn under its English
# ("has removed you from enrollment as of today") as a flat 1 px ellipse (QIMAGES18BO4-03).
_M184 = [0, 130, 0, 130, 0, 130]
L184 = [
    ("No. 1026", [480, 136, 686, 161], {"max_size": 18, "align": "right", "erase": [[606, 137, 689, 161]]}),
    ("Shiyo 801, October 8", [400, 163, 686, 188], {"max_size": 18, "align": "right", "erase": [[531, 164, 689, 187]]}),
    ("Chigaya Niimura-dono", [113, 217, 480, 243], {"max_size": 18, "erase": [[110, 218, 213, 242]]}),
    ("Kyoto University", [400, 270, 686, 295], {"max_size": 18, "align": "right", "erase": [[606, 271, 689, 295]]}),
    ("President   Hiroshi Sayama", [380, 297, 686, 322], {"max_size": 18, "align": "right", "erase": [[550, 298, 689, 322]]}),
    ("Notice of Removal from Enrollment", [116, 376, 684, 414], {"max_size": 27, "align": "center", "erase": [[324, 377, 477, 413]]}),
    ("", [112, 476, 689, 604], {"erase": [[112, 476, 689, 604], [112, 621, 689, 749], [112, 767, 689, 894]]}),
    ("Without taking the prescribed procedures, you have not", [116, 476, 686, 514], {"max_size": 22, "erase": []}),
    ("attended a single class for about half a year, from Shiyo 801,", [116, 514, 686, 552], {"max_size": 22, "erase": []}),
    ("April 13 to today.", [116, 552, 686, 590], {"max_size": 22, "erase": []}),
    ("In addition, your tuition for the first semester of the Shiyo", [116, 602, 686, 640], {"max_size": 22, "erase": []}),
    ("801 academic year is unpaid, and although we have inquired", [116, 640, 686, 678], {"max_size": 22, "erase": []}),
    ("repeatedly in writing, we have received no reply of any", [116, 678, 686, 716], {"max_size": 22, "erase": []}),
    ("kind.", [116, 716, 686, 754], {"max_size": 22, "erase": []}),
    ("This university has determined that you no longer have any", [116, 766, 686, 804], {"max_size": 22, "erase": []}),
    ("intention of remaining enrolled and, under University", [116, 804, 686, 842], {"max_size": 22, "erase": []}),
    ("Regulations Article 10, Item 7, has removed you from", [116, 842, 686, 880], {"max_size": 22, "erase": [], "ellipse": [404, 872, 616, 872], "ellipse_w": 1}),
    ("enrollment as of today. Please take note of this.", [116, 880, 686, 918], {"max_size": 22, "erase": [], "ellipse": [116, 910, 327, 910], "ellipse_w": 1}),
    ("End", [560, 961, 686, 990], {"max_size": 20, "align": "right", "erase": [[635, 962, 689, 990]]}),
]
JOBS += [
    {"id": "obj184-0", "screen": "reference 184 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 2, "mask_color": _M184, "color": "#111111", "new": True,
     "note": "notice of removal from enrollment (printed; red seal kept, underline redrawn)",
     "items": [(D + "rrr184/0.gal", "")],
     "lines": [(t, b, dict(o, mask_color=_M184)) for t, b, o in L184]},
    {"id": "obj184-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr184.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 249 "Arata Settlement Survey Report" (800x2301, two sheets, transparent seam y 1132-1168):
# printed report = Cambria (the R-lane pattern), glyph mask every channel <= 130, inpaint on the white paper; the table
# rules (incl. the light ones), the sheet edges and the bullets (x 74-81) stay; one size (17 px, line spacing 1.0) for the
# whole page, each cell box = its wrapped height from the first JP text row (img18bO4/mk249.py, text249.py). 内約 = 内訳
# and 形成期 = 形跡 (typos, translated as intended).
_M249 = [0, 130, 0, 130, 0, 130]
L249 = [
    ("", [70, 103, 730, 162], {"erase": [[70, 103, 730, 162], [72, 207, 400, 232], [72, 240, 730, 333], [72, 345, 400, 369], [72, 378, 730, 504], [72, 516, 400, 541], [72, 549, 730, 575], [96, 586, 730, 645], [96, 657, 730, 682], [96, 694, 730, 719], [96, 731, 730, 756], [96, 765, 730, 857], [96, 866, 730, 891], [72, 902, 400, 927], [72, 936, 730, 962], [72, 1274, 400, 1299], [72, 1308, 730, 1333], [72, 1345, 400, 1370], [72, 1378, 730, 1605], [72, 1618, 400, 1642], [72, 1651, 730, 1710], [72, 1722, 400, 1746], [72, 1755, 730, 1881], [72, 1893, 400, 1918], [72, 1926, 730, 1985]]}),
    ("The survey of the Arata settlement that existed in the Arata district is complete, so the series of events is reported here.", [74, 101, 728, 144], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("A phone call came in from a girl in the Arata settlement asking for help. However, since it was nighttime, the rescue was carried out early the next morning. According to the girl, the driver of the Arata Line train had been killed.", [74, 239, 728, 303], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("A rescue helicopter heads to the Arata settlement. Separately, another team confirms the death of the Arata Line driver. The neck had been severed with a sharp blade; death was instantaneous. In light of this, the information from the girl was judged highly credible, and a survey team for the Arata settlement was formed at once.", [74, 377, 728, 462], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("No survivors. Breakdown of the circumstances of death:", [74, 548, 728, 570], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Kana Niimura (15): When she was found, her death was at first thought to be from wild animals, but strictly speaking, she bled to death from losing her right arm.", [98, 585, 728, 628], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Erina Goto (17): Suffocation from compression of the neck.", [98, 653, 728, 675], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Natsumi Kogori (18): Died of a cerebral contusion", [98, 690, 728, 712], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Others: 25 people, cause of death unknown.", [98, 728, 728, 750], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Each of them died in what appears to be their own home. There were no external injuries, but since many of the bodies had the blood of the above victims on them, the victims are thought to have been killed by them.", [98, 764, 728, 828], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("The bodies are placed under the jurisdiction of the Iizawa Prefectural Police", [98, 862, 728, 884], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("2 mummies are found in the remains of a fire that broke out in the settlement.", [74, 935, 728, 957], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("A search of the Arata district is carried out on a scale of 300 people.", [74, 1307, 728, 1329], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("The causes of death of the 3 girls are determined as above.", [74, 1377, 728, 1399], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("The cause of death of the other 25 is multiple organ failure. Hyphae are detected in their bodies, and more than 1 month is thought to have passed since the hyphae developed in the brain. In other words, as of April 9 they would have been dead for more than 1 month, but from the rigidity and the state of decomposition of the bodies, it was found that the times of death of the brain and the body differ. They had been brain-dead for more than 1 month. However, since there are traces of their having lived until recently, it is thought that for some reason they were able to move even after brain death.", [74, 1411, 728, 1559], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Of the 2 mummies, one is found to have been dead about 1 year, and the other several hundred years or more. However, the damage is severe, and further examination is impossible.", [74, 1645, 728, 1709], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("On the instructions of the National Police Agency, the search of the Arata district is forcibly halted. No major leads. Also on the same day, all the bodies of those who died of multiple organ failure vanish, except for their bones. At that time, countless things that looked like plant branches had spread all through the body storage room.", [74, 1750, 728, 1835], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("All investigative authority passes to the National Police Agency. At the same time, all the bodies and the plant branches are also collected.", [74, 1922, 728, 1965], {"max_size": 17, "line_spacing": 1.0, "erase": []}),
    ("Shiyo 802, April 8   22:00", [74, 207, 600, 233], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 9   5:00", [74, 345, 600, 370], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 9   7:00", [74, 516, 600, 542], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 9   9:00", [74, 902, 600, 928], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 10", [74, 1274, 600, 1300], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 15", [74, 1345, 600, 1371], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 16", [74, 1618, 600, 1643], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 17", [74, 1722, 600, 1747], {"max_size": 17, "erase": []}),
    ("Shiyo 802, April 18", [74, 1893, 600, 1919], {"max_size": 17, "erase": []}),
]
JOBS += [
    {"id": "obj249-0", "screen": "reference 249 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 2, "mask_color": _M249, "color": "#111111", "new": True,
     "note": "Arata settlement survey report (printed table; rules and bullets kept)",
     "items": [(D + "rrr249/0.gal", "")],
     "lines": [(t, b, dict(o, mask_color=_M249)) for t, b, o in L249]},
    {"id": "obj249-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr249.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 266 "Erika Niimura's Note" (600x1708, vertical brush letter on vertically ruled paper, two
# sheets y 0-848 / 859-1708; transparent seam y 849-858). The 書簡 letter() pattern: serif, horizontal English blocks right
# to left (one per sheet, top-aligned at the first JP column top), addressee / signature rot -90 in their columns (ref183);
# glyph mask _L1M (every channel <= 85: the grey rules stay), inpaint. Sheet 1 block widened over its blank ruled columns
# (QIMAGES18BO4-05). img18bO4/mk266.py.
L266 = [
    ("I'm heading out now to search for Chigaya. The place is the back of the underground storeroom. There's a chance Chigaya is there. I might need everyone's help too, so at least don't slack on getting ready. I may head for the summit of Mount Itohime. This should surely settle everything. Also, it looks like the lore handed down through the generations will be useful. The wisdom of the ancestors really is nothing to scoff at. Kotaro, as far as you're able, I'd like you to think, based on the rule and the rules that", [66, 88, 500, 661], {"max_size": 28, "line_spacing": 1.12, "erase": [[64, 80, 502, 765]]}),
    ("this settlement has, about whether there's a way to help solve this. It's all right. This year, for sure.", [66, 947, 555, 1063], {"max_size": 28, "line_spacing": 1.12, "erase": [[460, 940, 556, 1625]]}),
    ("To Kotaro,", [519, 86, 556, 420], {"rot": -90, "max_size": 24, "align": "left", "erase": [[519, 80, 556, 205]]}),
    ("Erika Niimura", [402, 1300, 444, 1622], {"rot": -90, "max_size": 24, "align": "right", "erase": [[404, 1480, 442, 1626]]}),
]
JOBS += [
    {"id": "obj266-0", "screen": "reference 266 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "mask_grow": 3, "mask_color": _L1M, "color": "#1a1208", "new": True,
     "note": "Erika Niimura's note (vertical brush letter, two sheets; English blocks right to left)",
     "items": [(D + "rrr266/0.gal", "")],
     "lines": [(t, b, dict(o, mask_color=_L1M)) for t, b, o in L266]},
    {"id": "obj266-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr266.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 175 "The Person Who Took Custody" (800x520 newspaper page "Daily Iizawa" + 部分拡大1 400x357):
# the ref104 / ref28 newspaper pattern (same page template: _GAME ad box, publisher block, masthead box). Vertical JP headlines
# set rot -90; the article columns become horizontal English blocks in their column area (N104 way), one size (9 px) for the
# article body; the photo and the LiveMaker logo / URL kept. The big blurred headline (legible) is set sharp in the blurred
# glyphs' mid grey (QIMAGES18BO4-06); the blurred subhead and the blurred columns are below legibility and stay as drawn.
# Close-up 1 = zoom_items at its own scale (match7.py: s 1.45, crop (2, 273), score 0.893; the QIMAGES7-04 method).
N175_A = ("Before dawn on April 9, Kana Niimura-san (12), who lives in the Arata district, was taken into protection at the "
          "Toyotake police box. Niimura-san appeared at the police box alone and is currently in temporary protective custody "
          "at a child guidance center in Iizawa Prefecture. Niimura-san recently lost both her parents in an accident and, "
          "having nowhere to go, reportedly")
N175_B = ("asked the police box for help. Relatives or acquaintances of Niimura-san are asked to contact our company.")
L175 = [
    ("Daily Iizawa", [262, 6, 510, 27], dict(_NM4, align="center", max_size=12, erase=[[264, 8, 506, 27]])),
    ("Shiyo 802, April 10   Sunday   No. 4511", [560, 6, 796, 27],
     dict(_NM4, align="right", max_size=11, erase=[[571, 9, 785, 27]])),
    ("DAILY\nIIZAWA", [706, 48, 776, 342], dict(_NH, rot=-90, align="center", max_size=34,
                                              mask_color=[0, 90, 0, 90, 0, 90], erase=[[708, 52, 774, 340]])),
    ("Publisher\nIizawa Newspaper Co.\n1-1 Shimatoki, Iizawa City,\nIizawa Prefecture\nPostal code 995-9876\n"
     "(C) Megasawa Newspaper Co. 802\nTel 220(551)XXXX", [693, 355, 788, 440],
     dict(_NM4, align="center", max_size=8, line_spacing=1.0, erase=[[693, 356, 788, 439]])),
    _GAME,
    ("Cherry Blossom Season Is Here!\nFull Bloom Everywhere", [610, 40, 676, 512],
     dict(_NH, rot=-90, align="center", max_size=34, color="#6e6e6e", mask_color=[0, 205, 0, 205, 0, 205],
          erase=[[612, 36, 672, 516]])),
    ("Seeking Someone\nto Take Custody", [204, 300, 263, 460],
     dict(_NH, rot=-90, align="center", max_size=24, mask_color=[0, 150, 0, 150, 0, 150], erase=[[205, 302, 262, 457]])),
    (N175_A, [22, 286, 197, 397], dict(_NM4, max_size=9, erase=[[20, 284, 198, 398]])),
    (N175_B, [124, 408, 197, 515], dict(_NM4, max_size=9, erase=[[123, 407, 198, 516]])),
    ("Kana Niimura-san (12)", [24, 485, 114, 505], dict(_NM4, align="center", max_size=9, erase=[[28, 484, 112, 503]])),
]
Z175 = [(1, 1.45, 2, 273, 400, 357)]
JOBS += [
    {"id": "obj175-0", "screen": "reference 175 detail", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "mask_grow": 3, "color": "#222222", "line_spacing": 1.05, "new": True,
     "note": "newspaper page (photo, LiveMaker logo / URL and the blurred columns kept)", "items": [(D + "rrr175/0.gal", "")],
     "lines": L175},
    {"id": "obj175-zoom1", "screen": "reference 175 close-up", "style": "serif", "mode": "lines", "erase": "inpaint",
     "erase_first": True, "text_only": True, "thr": 60, "mask_grow": 5, "color": "#222222", "line_spacing": 1.05,
     "note": "newspaper close-up (same English as the page, own scale)", "items": zoom_items(175, L175, Z175), "lines": []},
    {"id": "obj175-ov", "screen": "reference screen previews", "style": "serif", "mode": "asis", "chain": True,
     "items": [(O + "rr175.gal", "")]},
]


# IMAGES18B-O4 2026-10-15: ref 262 "Analysis of Occult Magazine 'M'" (800x5210 web page; part 21 fence). Built by
# work/images/_c/img18bO4/mk262.py (web text: text262.py + lay262.py; geometry: match262c.py). ORDER: paste262.py -> obj262-0
# (chain=True, the paste8.py / ref109-zoom precedent) -> obj262-ov. Web text = gothic (ref157 precedent), one entry per
# colour run (yellow spans = separate runs, ref98 precedent); erase-only entries fill the navy ground flat (inpaint on the
# photo). Cover = gothic, inpaint per line. Panels P2 P4 P5 P6 P7 = the shipped L108 / L109 at their own scale (zoom_lines,
# QIMAGES7-04) shifted into the panel, magazine ink / paper as the shipped jobs (maskfill, bg = the panel paper #fafafa);
# P1 P3 P8 and P4's cut title / tape = pasted from the shipped English renders (paste262.py). P7: the two red-boxed JP words
# stay as drawn (protect; ref17 Q1970 precedent), the English of those two columns starts below the boxes. The kana
# wordplay (acrostic, reversed chant) is romanized with short glosses in [ ] (QIMAGES18BO4-08).
_W262 = [
    ("", [40, 31, 760, 77], {"erase": [[40, 31, 760, 77]], "method": "flat", "bg": "#0c0111"}),
    ("", [55, 83, 735, 127], {"erase": [[55, 83, 735, 127]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 221, 508, 362], {"erase": [[26, 221, 508, 362]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 543, 774, 637], {"erase": [[26, 543, 774, 637]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 660, 140, 683], {"erase": [[28, 660, 140, 683]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 1182, 338, 1440], {"erase": [[26, 1182, 338, 1440]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 1440, 774, 1509], {"erase": [[26, 1440, 774, 1509]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 1578, 205, 1601], {"erase": [[28, 1578, 205, 1601]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 2128, 367, 2566], {"erase": [[26, 2128, 367, 2566]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 2588, 367, 2818], {"erase": [[26, 2588, 367, 2818]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3206, 774, 3255], {"erase": [[26, 3206, 774, 3255]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 3276, 158, 3301], {"erase": [[36, 3276, 158, 3301]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3345, 458, 3438], {"erase": [[26, 3345, 458, 3438]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 3460, 328, 3485], {"erase": [[28, 3460, 328, 3485]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3506, 458, 3737], {"erase": [[26, 3506, 458, 3737]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 3758, 368, 3784], {"erase": [[36, 3758, 368, 3784]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3804, 774, 3851], {"erase": [[26, 3804, 774, 3851]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 3873, 190, 4012], {"erase": [[36, 3873, 190, 4012]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4034, 440, 4057], {"erase": [[28, 4034, 440, 4057]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 4203, 696, 4258], {"erase": [[36, 4203, 696, 4258]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4279, 136, 4302], {"erase": [[28, 4279, 136, 4302]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 4302, 774, 4463], {"erase": [[26, 4302, 774, 4463]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 4554, 774, 4623], {"erase": [[26, 4554, 774, 4623]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 4642, 466, 4674], {"erase": [[36, 4642, 466, 4674]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 4692, 774, 4738], {"erase": [[26, 4692, 774, 4738]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4761, 434, 4783], {"erase": [[28, 4761, 434, 4783]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4806, 434, 4829], {"erase": [[28, 4806, 434, 4829]], "method": "inpaint", "mask_color": [140, 255, 140, 255, 140, 255], "mask_grow": 3}),
    ("", [28, 5068, 732, 5146], {"erase": [[28, 5068, 732, 5146]], "method": "inpaint", "mask_color": [140, 255, 0, 140, 0, 150], "mask_grow": 3}),
    ("", [30, 5165, 498, 5190], {"erase": [[30, 5165, 498, 5190]], "method": "inpaint", "mask_color": [140, 255, 140, 255, 140, 255], "mask_grow": 3}),
    ("The Truth Hidden in Occult Magazine 'M'!", [99, 30, 705, 76], {"max_size": 34, "color": "#fdf8fe", "erase": [], "line_spacing": 1.0}),
    ("A Mass Murder the State Itself Covered Up!", [80, 82, 724, 128], {"max_size": 34, "color": "#fdf8fe", "erase": [], "line_spacing": 1.0}),
    ("Do you all know", [30, 222, 144, 245], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Occult Magazine 'M'?", [145, 222, 296, 245], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Those of you who view this", [297, 222, 492, 245], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("site probably know it. It is", [30, 245, 215, 268], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("a magazine with a long history, first", [216, 245, 465, 268], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("published in Shiyo 745,", [30, 268, 200, 291], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("and it carries ghosts, yokai, UFOs, UMAs", [201, 268, 487, 291], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("and other unknown phenomena. It has especially strong support", [30, 291, 478, 314], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("among middle and high school students, and even now it is often", [30, 314, 488, 337], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("used among students as something to talk about.", [30, 337, 377, 360], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Of course, I'm a fan of M too, and lately I've been collecting M's back issues, in other words the issues", [30, 544, 752, 567], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("published so far. Among them was something baffling, so I'll introduce it. It's", [30, 567, 565, 590], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the June and July issues of", [566, 567, 761, 590], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Shiyo 747,", [30, 590, 110, 613], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("quite old ones. But the back issues I got are well preserved, and the text and photos can be", [111, 590, 763, 613], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("seen clearly.", [30, 613, 122, 636], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("First, the June issue", [30, 660, 175, 683], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("The murder case of researchers that", [30, 1187, 275, 1210], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("happened in Motoki-cho, Sawa Prefecture.", [30, 1210, 315, 1233], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("In", [316, 1210, 332, 1233], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("late Shiyo 747, a public research group was", [30, 1233, 325, 1256], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("launched in Motoki-cho, Sawa Prefecture. Its", [30, 1256, 331, 1279], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("research purpose is said to have been to learn", [30, 1279, 342, 1302], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the true nature of a cherry tree said to have", [30, 1302, 327, 1325], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("suddenly sprouted in Shiyo 737. But a few", [30, 1325, 314, 1348], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("days after the research began, a case", [30, 1348, 285, 1371], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("occurred in which all the researchers", [30, 1371, 279, 1394], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("were", [280, 1371, 315, 1394], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("beaten to death at their lodgings in", [30, 1394, 268, 1417], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Motoki-cho.", [30, 1417, 113, 1440], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("This is the article on it.", [114, 1417, 271, 1440], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Normally you'd think someone beat the researchers to death, but the article at the time closes by saying it", [30, 1440, 774, 1463], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("will", [30, 1463, 57, 1486], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("approach the case from both sides, murder and curse, and run the continuation in the next issue.", [58, 1463, 737, 1486], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Including the curse is a very M-like way to close, as befits an occult magazine.", [30, 1486, 586, 1509], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("However, in the July issue,", [30, 1578, 221, 1601], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("As you can see, a yokai called", [30, 2129, 246, 2152], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Motokizakura-sama", [30, 2152, 172, 2175], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("suddenly appears, and the", [173, 2152, 361, 2175], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("article concludes that the murder case was its", [30, 2175, 356, 2198], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("doing. At a glance, you could say it's a very", [30, 2198, 335, 2221], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("M-like conclusion. But what's baffling is that,", [30, 2221, 348, 2244], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("rather than getting into the truth of the case, it", [30, 2244, 356, 2267], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("merely digs up rumors from Motoki-cho and", [30, 2267, 341, 2290], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("brings them in as the conclusion. In other", [30, 2290, 321, 2313], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("words,", [30, 2313, 80, 2336], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the only causal link to the case is that 'it", [81, 2313, 367, 2336], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("happened in Motoki-cho.'", [30, 2336, 214, 2359], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("What's more, this", [215, 2336, 337, 2359], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("murder case actually happened. Even so,", [30, 2359, 320, 2382], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("concluding without running the details of the", [30, 2382, 342, 2405], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("case, and without even making up something to", [30, 2405, 365, 2428], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("connect the case and the rumors, is rather", [30, 2428, 329, 2451], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("sloppy, isn't it? From the August issue on,", [30, 2451, 327, 2474], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("neither this case nor Motokizakura-sama", [30, 2474, 320, 2497], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("appears. To me it looks as if this case was", [30, 2497, 335, 2520], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("forcibly brought to a close.", [30, 2520, 221, 2543], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("I tried to get information on the case", [30, 2588, 290, 2611], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("elsewhere, but for some reason there was", [30, 2611, 329, 2634], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("none, either online or in libraries. Of course", [30, 2634, 338, 2657], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("there were articles from when the case first", [30, 2657, 339, 2680], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("happened, but nothing that looked into it deeply", [30, 2680, 370, 2703], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("and no impressions from the police or the like;", [30, 2703, 361, 2726], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("there was only what kind of case had", [30, 2726, 293, 2749], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("happened, and", [30, 2749, 137, 2772], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("what happened afterward is", [138, 2749, 335, 2772], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("completely unknown.", [30, 2772, 179, 2795], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("In other words, I thought", [180, 2772, 353, 2795], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("that perhaps, for some reason,", [30, 2795, 248, 2818], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("this murder case", [249, 2795, 369, 2818], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("was hushed up.", [30, 2818, 142, 2841], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("And there's one more strange thing about this July issue. When you read the text, there are a lot of", [30, 3207, 723, 3230], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("strange turns of phrase. For example, in this part,", [30, 3230, 377, 3253], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Sakura (rei no)' [the cherry (in question)]", [30, 3276, 341, 3299], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("is how it's written, and right below it, the phrase is 'rei no", [30, 3345, 434, 3368], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("sakura' [the cherry in question]. Normally you'd write 'rei no", [30, 3368, 452, 3391], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("sakura.' I thought there might be some intention behind this.", [30, 3391, 451, 3414], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("What's more, this: 'Where one falls, darkness lies.'", [30, 3460, 381, 3483], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("It feels like eerie wording for effect, but there is nothing at", [30, 3506, 445, 3529], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("all in this article about 'falling' or 'darkness.' I thought this", [30, 3529, 433, 3552], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("might be a hint from the reporter. After all, the previous", [30, 3552, 421, 3575], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("issue said it would pursue the truth of the murder case, yet", [30, 3575, 447, 3598], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the July issue wraps it up in this strange way.", [30, 3598, 350, 3621], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("If I were the", [351, 3598, 439, 3621], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("reporter, I'd want to write the truth in more detail,", [30, 3621, 378, 3644], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("and if for", [379, 3621, 446, 3644], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("some reason I couldn't write it, that would be terribly", [30, 3644, 402, 3667], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("frustrating. So at the very least, I'd want", [30, 3667, 310, 3690], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("to leave readers", [311, 3667, 430, 3690], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("some kind of hint.", [30, 3690, 159, 3713], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("'Sakura (rei no)' and 'Where one falls, darkness lies'", [30, 3758, 400, 3781], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("When I wondered whether I could expose the truth from these 2 points, I finally found something that", [30, 3804, 738, 3827], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("seemed to be it. In other words, if you follow the first characters of this article's paragraphs (danraku,", [30, 3827, 746, 3850], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'where one falls'),", [30, 3850, 160, 3873], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Mo'u sude ni [already]", [41, 3873, 209, 3896], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Mi'chi no uwasa [an unknown rumor]", [41, 3896, 305, 3919], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Ke'tsuron o ieba [to give the conclusion]", [41, 3919, 339, 3942], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Sa'kura (rei no) [that cherry tree]", [41, 3942, 289, 3965], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Re'i no sakura [that cherry tree]", [41, 3965, 274, 3988], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Ta'shika ni [indeed]", [41, 3988, 192, 4011], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("If you turn these into hiragana and line up the first characters,", [30, 4034, 462, 4057], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("mo mi ke sa re ta \u2192 momikesareta [hushed up]", [30, 4200, 717, 4260], {"max_size": 32, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("is what you get.", [30, 4279, 143, 4302], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("If my guess is right, wasn't it that the reporter, for some reason, was not allowed to write the continuation", [30, 4302, 769, 4325], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("and wanted to convey, as at least a hint, that", [30, 4325, 347, 4348], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'this case has been hushed up'?", [348, 4325, 577, 4348], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("As proof, not even the", [578, 4325, 739, 4348], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("newspapers ran any follow-up on the case. What's more, the ones killed were an 'official' research group.", [30, 4348, 770, 4371], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Couldn't one also think that", [30, 4371, 224, 4394], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the state hushed up this case?", [225, 4371, 446, 4394], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("And though the tree suddenly sprouted, the", [447, 4371, 754, 4394], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("state set up a research group for a single tree. That being so, you could say the state knew the true", [30, 4394, 731, 4417], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("nature of this cherry tree to some extent, and the group was made to look into its details further.", [30, 4417, 710, 4440], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("When I looked further into this matter, I got some interesting information. In Motoki-cho there are", [30, 4554, 712, 4577], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("apparently several households that worship Motokizakura-sama as a god. The words they chant when", [30, 4577, 744, 4600], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("they pray are", [30, 4600, 124, 4623], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("\"Taresaro Koniraku Sahan Iuyu Kinke\"", [30, 4646, 294, 4669], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("a strange phrase. As it is, you can't tell what it means, but if you read it backward,", [30, 4692, 605, 4715], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Kenki Yuui Nhasa Kuraniko Rosareta", [30, 4761, 285, 4784], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("kenkyuuin   wa   sakura   ni   korosareta", [30, 4806, 301, 4829], {"max_size": 15, "color": "#cfd0e4", "erase": [], "line_spacing": 1.0}),
    ("The researchers were killed by the cherry", [26, 5066, 719, 5146], {"max_size": 38, "color": "#ff2538", "erase": [], "line_spacing": 1.0}),
    ("Now, what do you make of this case?", [30, 5164, 281, 5189], {"max_size": 15, "color": "#cfd0e4", "erase": [], "line_spacing": 1.0}),
]
_CV262 = [
    ("Finally solved!!  The truth about Bigfoot!!", [530, 139, 737, 157], {"color": "#e8e8e8", "mask_color": [150, 255, 150, 255, 150, 255], "erase": [[532, 139, 737, 157]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("Monthly Occult Report Magazine", [519, 163, 700, 179], {"color": "#7a48b8", "mask_color": [50, 160, 15, 110, 70, 230], "erase": [[519, 164, 630, 179]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("All phenomena,\nright here", [518, 210, 582, 236], {"color": "#dcd8d0", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[518, 211, 576, 235]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("April Issue", [516, 249, 574, 265], {"color": "#dcd8d0", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[516, 249, 560, 265]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("em", [693, 262, 738, 283], {"color": "#ff1a1a", "mask_color": [140, 255, 0, 110, 0, 110], "erase": [[690, 259, 740, 283]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("All-Out Special!", [517, 290, 600, 301], {"color": "#e81818", "mask_color": [140, 255, 0, 120, 0, 120], "erase": [[517, 290, 566, 301]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("Expose the truth of the eerie 'apocalyptic sound'!", [517, 301, 736, 314], {"color": "#ece8dc", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[517, 301, 712, 314]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("Spring Ghost Footage", [527, 326, 640, 341], {"color": "#eef040", "mask_color": [140, 255, 130, 255, 0, 150], "erase": [[527, 326, 598, 341]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("The lost 'Kowloon Walled City' mystery", [527, 341, 670, 352], {"color": "#e4ece4", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[527, 341, 622, 352]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 8}),
    ("A new door to Maya civilization", [527, 351, 670, 362], {"color": "#e4ece4", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[527, 351, 622, 362]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 8}),
    ("Plot hidden in the great quake", [527, 361, 670, 372], {"color": "#e4ece4", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[527, 361, 622, 372]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 8}),
    ("5 psychic investigators", [527, 371, 670, 382], {"color": "#e4ece4", "mask_color": [130, 255, 130, 255, 120, 255], "erase": [[527, 371, 622, 382]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 8}),
    ("This Month's DVD", [587, 414, 662, 425], {"color": "#f2dedb", "mask_color": [140, 255, 110, 255, 100, 255], "erase": [[587, 414, 630, 425]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("Qigong and yoga: what happens\nif you draw out 100% of the\nhuman body's abilities?", [587, 425, 745, 456], {"color": "#f2dedb", "mask_color": [140, 255, 110, 255, 100, 255], "erase": [[587, 425, 718, 446]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
    ("800 yen (tax incl.)", [655, 458, 745, 474], {"color": "#f2f0b8", "mask_color": [130, 255, 130, 255, 90, 255], "erase": [[686, 459, 737, 473]], "method": "inpaint", "mask_grow": 2, "line_spacing": 1.0, "max_size": 12}),
]


def _o4panel(L, ox, oy, s, W, H, dx, dy, color, drop=(), grow=3):
    """a shipped magazine layout at its own scale inside a 262 panel (zoom_lines), shifted by (dx, dy); serif, the
    shipped ink colour unless the line has its own, maskfill on the panel paper."""
    out = []
    for t, b, o in zoom_lines([e for e in L if e[0] not in drop], ox, oy, s, W, H):
        o = dict(o)
        o["erase"] = [[e[0] + dx, e[1] + dy, e[2] + dx, e[3] + dy] for e in o.get("erase", [])]
        o.setdefault("color", color)
        o.update(style="serif", line_spacing=1.05, bg="#fafafa", mask_grow=grow)
        o.setdefault("method", "maskfill")
        out.append((t, [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy], o))
    return out


_P2 = _o4panel(L108, 95.1, 418.1, 1.5723, 445, 209, 342, 1184, _INK108)
_P4 = _o4panel(L109, 429.4, 284.4, 1.1364, 406, 306, 372, 2121, "#a82c2c", drop=(T109, TAPE109))
_P5 = _o4panel(L109, 93.5, 13.5, 1.1905, 351, 321, 389, 2442, "#a82c2c")
_P6 = _o4panel(L109, 93.7, 273.7, 1.2853, 379, 347, 389, 2776, "#a82c2c")
_P7 = _o4panel(L109, 93.2, 14.2, 1.6779, 169, 452, 462, 3275, "#a82c2c")
# P7: the red boxes (x 490-528 y 3292-3396 around 桜（例の）, x 512-546 y 3520-3595 around 例の桜) stay as drawn (protect below);
# the English of those two columns (M109_L2A, M109_L3A) starts 2 px below each box.
for _k, _e in enumerate(_P7):
    if _e[0] == M109_L2A:
        _P7[_k] = (_e[0], [_e[1][0], 3398, _e[1][2], _e[1][3]], _e[2])
    elif _e[0] == M109_L3A:
        _P7[_k] = (_e[0], [_e[1][0], 3597, _e[1][2], _e[1][3]], _e[2])
JOBS += [
    {"id": "obj262-0", "screen": "reference 262 detail", "style": "gothic", "mode": "lines", "erase": "flat",
     "erase_first": True, "chain": True, "mask_grow": 2, "color": "#d2cad6", "new": True,
     "note": "web page on occult magazine 'M' (panels = refs 108 / 109 English; photos, logo and art kept)",
     "items": [(D + "rrr262/0.gal", "")],
     "protect": [[489, 3291, 529, 3397], [511, 3519, 547, 3596]],
     "lines": _W262 + [(t, b, dict(o, style="gothic")) for t, b, o in _CV262] + _P2 + _P4 + _P5 + _P6 + _P7},
    {"id": "obj262-ov", "screen": "reference screen previews", "style": "gothic", "mode": "asis", "chain": True,
     "items": [(O + "rr262.gal", "")]},
]


# SWEEP-ACROSTIC 2026-10-16 (notes/SWEEP-ACROSTIC-BRIEF.md; owner ruling 2026-10-16 01:40): the hidden message of refs 109
# and 262 rebuilt in English. The shipped jobs ref109 / ref109-zoom / obj262-0 above stay as they were; their copies here
# carry new ids and the new text. ORDER: ref109-ac -> work/images/_c/paste8.py z109 -> ref109-zoom-ac ->
# work/images/_c/sweepac/paste262ac.py -> obj262-0-ac (chain) [-> the 262 card only if its window changed].
# ref 109: nine paragraphs whose first letters spell COVERED UP; only each paragraph's opening clause is new, every other
# sentence is the shipped M109_* text word for word. The three long boxes R1 / R2 / L4 now hold two paragraphs each: one
# text entry per paragraph, stacked in the shipped box at the largest common size <= the box's max_size, a half-line gap
# between the two, the stack centred like the engine centres one string (_ac_split; computed per context, so the page,
# every close-up and every 262 panel stack the paragraphs at their own scale). ref 262: the acrostic explanation in
# English letters, the decoded "C-O-V-E-R-E-D U-P", the chant "Yrrehce Htybdel Likerew Srehcrae Sereht" and its backward
# reading (sweepac/text262ac.py + lay262ac.py, built by sweepac/mkchunk.py); panels P4-P7 from the new 109 layout.
AC109_P1 = ("Covering the Motoki-cho researcher slaughter case already in last month's issue, we have since obtained a "
            "rumor that could be its basis.")
AC109_P2 = ("Over the time since that cherry tree appeared, mysterious phenomena have been occurring in Motoki-cho, Sawa "
            "Prefecture. It is a being called Motokizakura-sama, which could be taken for a spirit or for a yokai. Though "
            "it bears the name Motokizakura-sama, it is said to appear before the people of Motoki-cho regardless of the "
            "season and to bring happiness. However, how could such a being be tied to a slaughter case?")
AC109_P3 = ("Various witnesses led us to an unknown rumor. According to them, Motokizakura-sama at first glance cannot be "
            "told apart from an ordinary human, but the testimony agrees that it is a young woman wearing a kimono with a "
            "cherry-blossom pattern. Furthermore, there are also stories of it being seen in separate places at the same "
            "time, and it is said that there is not just one, but countless of them in the same form.")
AC109_P4 = ("Encounter Motokizakura-sama, and you will apparently be blessed with sudden good fortune. However, the world "
            "is not all good things. Behind it, it is said, a frightening face is hidden.")
AC109_P5 = ("Reaching the conclusion, this being called Motokizakura-sama seems to be quite troublesome. While it brings "
            "good fortune to those who happen to meet it, there are, it is said, also Motokizakura-sama who on rare "
            "occasions bring death. Motokizakura-sama is also said to be an offshoot of that cherry tree, and whoever "
            "carelessly touches or searches for it will be bewitched by Motokizakura-sama and taste eternal suffering. "
            "There is a case like this.")
AC109_P6A = "Even that cherry tree's uncanny nature draws people"     # + M109_L2B (unchanged) = paragraph 6
AC109_P7A = ("Darker still: twin sisters, then 10 years old, were climbing and playing in that cherry tree when a woman "
             "wearing a cherry-blossom-pattern kimono")             # + M109_L3B (unchanged) = paragraph 7
AC109_P8 = ("Uncanny rumors about that cherry tree never seem to stop. Those who carelessly approach it are cursed to "
            "death, and it is said that the one protecting the cherry tree's secret is Motokizakura-sama. If so, that "
            "slaughter case too can be thought of as the work of Motokizakura-sama.")
AC109_P9A = ("Perhaps some of you readers think it ridiculous that such an uncanny being could be the culprit. But please "
             "think")                                               # + M109_L5 (unchanged) = paragraph 9
_AC_SEP = "\x1e"   # paragraph break inside one text box; _ac_split turns it into stacked entries
_AC109 = {M109_R1: AC109_P1 + _AC_SEP + AC109_P2, M109_R2: AC109_P3 + _AC_SEP + AC109_P4, M109_L1: AC109_P5,
          M109_L2A: AC109_P6A, M109_L3A: AC109_P7A, M109_L4: AC109_P8 + _AC_SEP + AC109_P9A}
_AC_D = _Dr.Draw(_Im.new("RGBA", (8, 8)))


def _ac_split(lines, ls=1.05, gap=0.5):
    """entries whose text holds several paragraphs (joined by _AC_SEP) -> one entry per paragraph, stacked in the entry's
    box at the largest common size <= the entry's max_size whose lines fit with no gap (Cambria = the serif style,
    typeset_ui.wrap / fit rules), then a gap between paragraphs of the leftover height, at most round(gap * line height)
    px (at least 1/5 line after a paragraph whose last line is over 3/4 full, else one size smaller); the stack
    centred vertically in the box (the engine centres one string). The first sub-entry keeps the erase boxes of the whole box, the others erase nothing; every sub-entry is
    capped at the common size, its box is the paragraph's own line band (floor / ceil), so the engine sets that size."""
    out = []
    for e in lines:
        t, b, o = e[0], e[1], (e[2] if len(e) > 2 else {})
        if _AC_SEP not in t:
            out.append(e)
            continue
        paras = t.split(_AC_SEP)
        x0, y0, x1, y1 = b
        bw, bh = x1 - x0, y1 - y0
        best = None
        for s in range(6, int(o["max_size"]) + 1):
            f = _Fn.truetype("C:/Windows/Fonts/cambria.ttc", s)
            a, d = f.getmetrics()
            lh = (a + d) * o.get("line_spacing", ls)
            ws = [_T.wrap(_AC_D, p, f, bw, 0) for p in paras]
            body = lh * sum(len(w) for w in ws)
            if max(_T.tlen(_AC_D, l, f) for w in ws for l in w) > bw or body > bh:
                break
            g = max(0, min(int(round(gap * lh)), int((bh - body) // (len(paras) - 1))))
            # the break must show: a paragraph ending in a line over 3/4 of the box width needs a gap of >= 1/5 line
            if any(_T.tlen(_AC_D, w[-1], f) > 0.75 * bw for w in ws[:-1]) and g < _math.ceil(0.2 * lh):
                break
            best = (s, lh, [len(w) for w in ws], g, body + g * (len(paras) - 1))
        assert best, "paragraph stack does not fit in %r" % (b,)
        s, lh, ns, g, tot = best
        y = y0 + (bh - tot) / 2.0
        for k, (p, n) in enumerate(zip(paras, ns)):
            oo = dict(o, max_size=s)
            oo["erase"] = o.get("erase", [list(b)]) if k == 0 else []
            out.append((p, [x0, int(_math.floor(y)), x1, int(_math.ceil(y + n * lh))], oo))
            y += n * lh + g
    return out


# page: the shipped layout L109 with the new text (boxes, erase boxes, sizes, colours unchanged)
L109AC = [(_AC109.get(t, t), b, o) for t, b, o in L109]
_L109AC = _ac_split(L109AC)
# close-ups 1-3 + 4: the shipped construction (zoom_items, the close-up 3 x1 284 override, item 1 chained on
# paste8.py z109 without the title, 部分拡大4 = the vertical title alone, unchanged), then the paragraph stacks per close-up
_Z109AC = zoom_items(109, L109AC, Z109)
for _k, _e in enumerate(_Z109AC[2][2]["lines"]):
    if _e[0] == _AC109[M109_L4]:
        _Z109AC[2][2]["lines"][_k] = (_e[0], [_e[1][0], _e[1][1], 284, _e[1][3]], _e[2])
_n, _s, _ox, _oy, _w, _h = Z109[0]
_Z109AC[0][2]["lines"] = zoom_lines([e for e in L109AC if e[0] != T109], _ox, _oy, _s, _w, _h)
_Z109AC[0][2]["chain"] = True
_Z109AC.append((_Z109[3][0], _Z109[3][1], dict(_Z109[3][2])))
for _it in _Z109AC:
    _it[2]["lines"] = _ac_split(_it[2]["lines"])
_W262AC = [
    ("", [40, 31, 760, 77], {"erase": [[40, 31, 760, 77]], "method": "flat", "bg": "#0c0111"}),
    ("", [55, 83, 735, 127], {"erase": [[55, 83, 735, 127]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 221, 508, 362], {"erase": [[26, 221, 508, 362]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 543, 774, 637], {"erase": [[26, 543, 774, 637]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 660, 140, 683], {"erase": [[28, 660, 140, 683]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 1182, 338, 1440], {"erase": [[26, 1182, 338, 1440]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 1440, 774, 1509], {"erase": [[26, 1440, 774, 1509]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 1578, 205, 1601], {"erase": [[28, 1578, 205, 1601]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 2128, 367, 2566], {"erase": [[26, 2128, 367, 2566]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 2588, 367, 2818], {"erase": [[26, 2588, 367, 2818]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3206, 774, 3255], {"erase": [[26, 3206, 774, 3255]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 3276, 158, 3301], {"erase": [[36, 3276, 158, 3301]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3345, 458, 3438], {"erase": [[26, 3345, 458, 3438]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 3460, 328, 3485], {"erase": [[28, 3460, 328, 3485]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3506, 458, 3737], {"erase": [[26, 3506, 458, 3737]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 3758, 368, 3784], {"erase": [[36, 3758, 368, 3784]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 3804, 774, 3851], {"erase": [[26, 3804, 774, 3851]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 3873, 190, 4012], {"erase": [[36, 3873, 190, 4012]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4034, 440, 4057], {"erase": [[28, 4034, 440, 4057]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 4203, 696, 4258], {"erase": [[36, 4203, 696, 4258]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4279, 136, 4302], {"erase": [[28, 4279, 136, 4302]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 4302, 774, 4463], {"erase": [[26, 4302, 774, 4463]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 4554, 774, 4623], {"erase": [[26, 4554, 774, 4623]], "method": "flat", "bg": "#0c0111"}),
    ("", [36, 4642, 466, 4674], {"erase": [[36, 4642, 466, 4674]], "method": "flat", "bg": "#0c0111"}),
    ("", [26, 4692, 774, 4738], {"erase": [[26, 4692, 774, 4738]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4761, 434, 4783], {"erase": [[28, 4761, 434, 4783]], "method": "flat", "bg": "#0c0111"}),
    ("", [28, 4806, 434, 4829], {"erase": [[28, 4806, 434, 4829]], "method": "inpaint", "mask_color": [140, 255, 140, 255, 140, 255], "mask_grow": 3}),
    ("", [28, 5068, 732, 5146], {"erase": [[28, 5068, 732, 5146]], "method": "inpaint", "mask_color": [140, 255, 0, 140, 0, 150], "mask_grow": 3}),
    ("", [30, 5165, 498, 5190], {"erase": [[30, 5165, 498, 5190]], "method": "inpaint", "mask_color": [140, 255, 140, 255, 140, 255], "mask_grow": 3}),
    ("The Truth Hidden in Occult Magazine 'M'!", [99, 30, 705, 76], {"max_size": 34, "color": "#fdf8fe", "erase": [], "line_spacing": 1.0}),
    ("A Mass Murder the State Itself Covered Up!", [80, 82, 724, 128], {"max_size": 34, "color": "#fdf8fe", "erase": [], "line_spacing": 1.0}),
    ("Do you all know", [30, 222, 144, 245], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Occult Magazine 'M'?", [145, 222, 296, 245], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Those of you who view this", [297, 222, 492, 245], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("site probably know it. It is", [30, 245, 215, 268], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("a magazine with a long history, first", [216, 245, 465, 268], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("published in Shiyo 745,", [30, 268, 200, 291], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("and it carries ghosts, yokai, UFOs, UMAs", [201, 268, 487, 291], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("and other unknown phenomena. It has especially strong support", [30, 291, 478, 314], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("among middle and high school students, and even now it is often", [30, 314, 488, 337], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("used among students as something to talk about.", [30, 337, 377, 360], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Of course, I'm a fan of M too, and lately I've been collecting M's back issues, in other words the issues", [30, 544, 752, 567], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("published so far. Among them was something baffling, so I'll introduce it. It's", [30, 567, 565, 590], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the June and July issues of", [566, 567, 761, 590], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Shiyo 747,", [30, 590, 110, 613], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("quite old ones. But the back issues I got are well preserved, and the text and photos can be", [111, 590, 763, 613], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("seen clearly.", [30, 613, 122, 636], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("First, the June issue", [30, 660, 175, 683], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("The murder case of researchers that", [30, 1187, 275, 1210], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("happened in Motoki-cho, Sawa Prefecture.", [30, 1210, 315, 1233], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("In", [316, 1210, 332, 1233], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("late Shiyo 747, a public research group was", [30, 1233, 325, 1256], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("launched in Motoki-cho, Sawa Prefecture. Its", [30, 1256, 331, 1279], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("research purpose is said to have been to learn", [30, 1279, 342, 1302], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the true nature of a cherry tree said to have", [30, 1302, 327, 1325], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("suddenly sprouted in Shiyo 737. But a few", [30, 1325, 314, 1348], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("days after the research began, a case", [30, 1348, 285, 1371], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("occurred in which all the researchers", [30, 1371, 279, 1394], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("were", [280, 1371, 315, 1394], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("beaten to death at their lodgings in", [30, 1394, 268, 1417], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Motoki-cho.", [30, 1417, 113, 1440], {"max_size": 15, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("This is the article on it.", [114, 1417, 271, 1440], {"max_size": 15, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Normally you'd think someone beat the researchers to death, but the article at the time closes by saying it", [30, 1440, 774, 1463], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("will", [30, 1463, 57, 1486], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("approach the case from both sides, murder and curse, and run the continuation in the next issue.", [58, 1463, 737, 1486], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("Including the curse is a very M-like way to close, as befits an occult magazine.", [30, 1486, 586, 1509], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("However, in the July issue,", [30, 1578, 221, 1601], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("As you can see, a yokai called", [30, 2129, 246, 2152], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Motokizakura-sama", [30, 2152, 172, 2175], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("suddenly appears, and the", [173, 2152, 361, 2175], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("article concludes that the murder case was its", [30, 2175, 356, 2198], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("doing. At a glance, you could say it's a very", [30, 2198, 335, 2221], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("M-like conclusion. But what's baffling is that,", [30, 2221, 348, 2244], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("rather than getting into the truth of the case, it", [30, 2244, 356, 2267], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("merely digs up rumors from Motoki-cho and", [30, 2267, 341, 2290], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("brings them in as the conclusion. In other", [30, 2290, 321, 2313], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("words,", [30, 2313, 80, 2336], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the only causal link to the case is that 'it", [81, 2313, 367, 2336], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("happened in Motoki-cho.'", [30, 2336, 214, 2359], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("What's more, this", [215, 2336, 337, 2359], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("murder case actually happened. Even so,", [30, 2359, 320, 2382], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("concluding without running the details of the", [30, 2382, 342, 2405], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("case, and without even making up something to", [30, 2405, 365, 2428], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("connect the case and the rumors, is rather", [30, 2428, 329, 2451], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("sloppy, isn't it? From the August issue on,", [30, 2451, 327, 2474], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("neither this case nor Motokizakura-sama", [30, 2474, 320, 2497], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("appears. To me it looks as if this case was", [30, 2497, 335, 2520], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("forcibly brought to a close.", [30, 2520, 221, 2543], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("I tried to get information on the case", [30, 2588, 290, 2611], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("elsewhere, but for some reason there was", [30, 2611, 329, 2634], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("none, either online or in libraries. Of course", [30, 2634, 338, 2657], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("there were articles from when the case first", [30, 2657, 339, 2680], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("happened, but nothing that looked into it deeply", [30, 2680, 370, 2703], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("and no impressions from the police or the like;", [30, 2703, 361, 2726], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("there was only what kind of case had", [30, 2726, 293, 2749], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("happened, and", [30, 2749, 137, 2772], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("what happened afterward is", [138, 2749, 335, 2772], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("completely unknown.", [30, 2772, 179, 2795], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("In other words, I thought", [180, 2772, 353, 2795], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("that perhaps, for some reason,", [30, 2795, 248, 2818], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("this murder case", [249, 2795, 369, 2818], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("was covered up.", [30, 2818, 149, 2841], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("And there's one more strange thing about this July issue. When you read the text, there are a lot of", [30, 3207, 723, 3230], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("strange turns of phrase. For example, in this part,", [30, 3230, 377, 3253], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'Sakura (rei no)' [the cherry (in question)]", [30, 3276, 341, 3299], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("is how it's written, and right below it, the phrase is 'rei no", [30, 3345, 434, 3368], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("sakura' [the cherry in question]. Normally you'd write 'rei no", [30, 3368, 452, 3391], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("sakura.' I thought there might be some intention behind this.", [30, 3391, 451, 3414], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("What's more, this: 'Where one falls, darkness lies.'", [30, 3460, 381, 3483], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("It feels like eerie wording for effect, but there is nothing at", [30, 3506, 445, 3529], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("all in this article about 'falling' or 'darkness.' I thought this", [30, 3529, 433, 3552], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("might be a hint from the reporter. After all, the previous", [30, 3552, 421, 3575], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("issue said it would pursue the truth of the murder case, yet", [30, 3575, 447, 3598], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the July issue wraps it up in this strange way.", [30, 3598, 350, 3621], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("If I were the", [351, 3598, 439, 3621], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("reporter, I'd want to write the truth in more detail,", [30, 3621, 378, 3644], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("and if for", [379, 3621, 446, 3644], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("some reason I couldn't write it, that would be terribly", [30, 3644, 402, 3667], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("frustrating. So at the very least, I'd want", [30, 3667, 310, 3690], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("to leave readers", [311, 3667, 430, 3690], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("some kind of hint.", [30, 3690, 159, 3713], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("'Sakura (rei no)' and 'Where one falls, darkness lies'", [30, 3758, 400, 3781], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("When I wondered whether I could expose the truth from these 2 points, I finally found something that", [30, 3804, 738, 3827], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("seemed to be it. In other words, if you follow the first characters of this article's paragraphs", [30, 3827, 674, 3850], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("(where\u00a0one\u00a0falls),", [30, 3850, 163, 3873], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'C'overing the Motoki-cho...", [41, 3873, 238, 3896], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'O'ver the time...", [41, 3896, 158, 3919], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'V'arious witnesses...", [41, 3919, 189, 3942], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'E'ncounter Motokizakura-sama...", [41, 3942, 275, 3965], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'R'eaching the conclusion...", [41, 3965, 231, 3988], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'E'ven that cherry tree's...", [41, 3988, 219, 4011], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'D'arker still...", [41, 4011, 138, 4034], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'U'ncanny rumors...", [41, 4034, 172, 4057], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'P'erhaps some of you...", [41, 4057, 210, 4080], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("If you line up the first characters of these,", [30, 4103, 327, 4126], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("C-O-V-E-R-E-D U-P \u2192 covered up", [30, 4200, 565, 4260], {"max_size": 32, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("is what you get.", [30, 4279, 143, 4302], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("If my guess is right, wasn't it that the reporter, for some reason, was not allowed to write the continuation", [30, 4302, 769, 4325], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("and wanted to convey, as at least a hint, that", [30, 4325, 347, 4348], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("'this case has been covered up'?", [348, 4325, 584, 4348], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("As proof, not even the", [585, 4325, 746, 4348], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("newspapers ran any follow-up on the case. What's more, the ones killed were an 'official' research group.", [30, 4348, 770, 4371], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("Couldn't one also think that", [30, 4371, 224, 4394], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the state covered up this case?", [225, 4371, 453, 4394], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("And though the tree suddenly sprouted, the", [454, 4371, 761, 4394], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("state set up a research group for a single tree. That being so, you could say the state knew the true", [30, 4394, 731, 4417], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("nature of this cherry tree to some extent, and the group was made to look into its details further.", [30, 4417, 710, 4440], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("When I looked further into this matter, I got some interesting information. In Motoki-cho there are", [30, 4554, 712, 4577], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("apparently several households that worship Motokizakura-sama as a god. The words they chant when", [30, 4577, 744, 4600], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("they pray are", [30, 4600, 124, 4623], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("\"Yrrehce Htybdel Likerew Srehcrae Sereht\"", [30, 4646, 333, 4669], {"max_size": 16, "color": "#f5fa46", "erase": [], "line_spacing": 1.0}),
    ("a strange phrase. As it is, you can't tell what it means, but if you read it backward,", [30, 4692, 605, 4715], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("theresearcherswerekilledbythecherry", [30, 4761, 290, 4784], {"max_size": 16, "color": "#d2cad6", "erase": [], "line_spacing": 1.0}),
    ("the\u00a0\u00a0\u00a0researchers\u00a0\u00a0\u00a0were\u00a0\u00a0\u00a0killed\u00a0\u00a0\u00a0by\u00a0\u00a0\u00a0the\u00a0\u00a0\u00a0cherry", [30, 4806, 363, 4829], {"max_size": 15, "color": "#cfd0e4", "erase": [], "line_spacing": 1.0}),
    ("The researchers were killed by the cherry", [26, 5066, 719, 5146], {"max_size": 38, "color": "#ff2538", "erase": [], "line_spacing": 1.0}),
    ("Now, what do you make of this case?", [30, 5164, 281, 5189], {"max_size": 15, "color": "#cfd0e4", "erase": [], "line_spacing": 1.0}),
]
_P4AC = _ac_split(_o4panel(L109AC, 429.4, 284.4, 1.1364, 406, 306, 372, 2121, "#a82c2c", drop=(T109, TAPE109)))
_P5AC = _ac_split(_o4panel(L109AC, 93.5, 13.5, 1.1905, 351, 321, 389, 2442, "#a82c2c"))
_P6AC = _ac_split(_o4panel(L109AC, 93.7, 273.7, 1.2853, 379, 347, 389, 2776, "#a82c2c"))
_P7AC = _ac_split(_o4panel(L109AC, 93.2, 14.2, 1.6779, 169, 452, 462, 3275, "#a82c2c"))
# P7: the two red-boxed JP words stay as drawn (protect, QIMAGES18BO4-09); the English of those two columns (paragraph 6's
# and paragraph 7's openers) starts 2 px below each box, as shipped.
for _k, _e in enumerate(_P7AC):
    if _e[0] == AC109_P6A:
        _P7AC[_k] = (_e[0], [_e[1][0], 3398, _e[1][2], _e[1][3]], _e[2])
    elif _e[0] == AC109_P7A:
        _P7AC[_k] = (_e[0], [_e[1][0], 3597, _e[1][2], _e[1][3]], _e[2])
JOBS += [
    {"id": "ref109-ac", "screen": "reference 109 detail", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 2, "color": "#a82c2c", "line_spacing": 1.05, "new": True,
     "note": "occult magazine spread (tree art and photos kept; acrostic rebuild)", "items": [(D + "rrr109/0.gal", "")],
     "lines": _L109AC},
    {"id": "ref109-zoom-ac", "screen": "reference 109 close-ups", "style": "serif", "mode": "lines", "erase": "maskfill",
     "erase_first": True, "mask_grow": 3, "color": "#a82c2c", "line_spacing": 1.05,
     "note": "magazine close-ups (same English as the page, own scale; acrostic rebuild)", "items": _Z109AC, "lines": []},
    {"id": "obj262-0-ac", "screen": "reference 262 detail", "style": "gothic", "mode": "lines", "erase": "flat",
     "erase_first": True, "chain": True, "mask_grow": 2, "color": "#d2cad6", "new": True,
     "note": "web page on occult magazine 'M' (panels = refs 108 / 109 English; acrostic and chant in English letters)",
     "items": [(D + "rrr262/0.gal", "")],
     "protect": [[489, 3291, 529, 3397], [511, 3519, 547, 3596]],
     "lines": _W262AC + [(t, b, dict(o, style="gothic")) for t, b, o in _CV262] + _P2 + _P4AC + _P5AC + _P6AC + _P7AC},
]

# SWEEP-PIC 2026-10-16 (notes/SWEEP-PICTURES-BRIEF.md; log notes/v2/_tmp/tl-log-SWEEP-PIC.md): NO new jobs. In-place string edits:
# the IMAGESR report signature (lane B literals in L156 L162 L163 L169 L171 L174 L176 + lane A _SIG) now reads "Holy Cerejeira Church, ..."
# (QIMAGES18BR1-01); rep176 "Jade-Eye" -> "Green-Eye" x6 (QIMAGES18BR1-02); rep269 "(mycelium)" -> "(hyphae)" (QIMAGES18BR3-02).
# rrr302.gal (概要) and rr300.gal (概要): no job (unreferenced near-duplicate / textless art).
# SWEEP-PIC 2026-10-16 follow-up (coordinator rulings QSWEEP-01 / -02): body "the Cerejeira faith" -> "the Holy Cerejeira Church" in
# rep162 / rep154 / rep171; ref69-back columns 3-4 "Jade Eye(s)" -> "Green Eye(s)" (= tsv-en/リファレンスターゲット.tsv row 69); the
# back-face turning frames 図画8 図画9 10-15 rebuilt with refdoc_flip.py 69 ... 0,1 --mode full; the front-face frames kept as shipped.

# IMAGESPZ-PZ2 2026-10-16 (notes/IMAGESPZ-BRIEF.md, lane PZ2; rulings notes/v2/_tmp/rulings-IMAGESPZ.md): the report-puzzle UNSOLVED
# sheets rrr<ID>/_full.gal of reports 176 178 192 284 (base sheet + pieces composed by tools/images/report_puzzle.py). Each job = the
# shipped report job of that ID (same helper, same lines = the shipped body English verbatim, same erase boxes) with only the body mask
# tightened to the darker sheet (work/images/_c/pz-PZ2/sep.py: glyph vs paper colour, glyph positions from 全体.png), + the scrawl lines
# last (Ink Free "handwriting", stroke colour = mean of the stroke cores, one English line per JP line in its row; erase = texfill of the
# stroke colour inside the JP row). Rows measured with work/images/_c/pz-PZ2/rows.py. Log: notes/v2/_tmp/tl-log-IMAGESPZ-PZ2.md.
def _pz2body(lines, mask, drop=(), keep=()):
    """the shipped body lines with the glyph mask replaced (lines whose text is in drop are left out; masks in keep stay)."""
    out = []
    for e in lines:
        t, b, o = e[0], list(e[1]), (dict(e[2]) if len(e) > 2 else {})
        if t and t in drop:
            continue
        if o.get("mask_color") not in [list(k) for k in keep]:
            o["mask_color"] = list(mask)
        out.append((t, b, o))
    return out


def _pz2scr(text, row, color, size, mask, grow=5, x1=790, align="left", rot=None, rot_h=None, erase=None):
    """one scrawl line: JP row [x0, y0, x1, y1] -> English box over the same row, erase of the stroke colour in the row."""
    x0, y0, xe, y1 = row
    o = {"style": "handwriting", "color": color, "max_size": size, "align": align, "method": "texfill",
         "mask_color": list(mask), "mask_grow": grow,
         "erase": erase if erase is not None else [[max(x0 - 8, 0), max(y0 - 8, 0), min(xe + 8, 800), y1 + 8]]}
    if rot:
        o["rot"], o["rot_h"] = rot, rot_h
    return (text, [max(x0 - 6, 0), y0 - 4, x1, y1 + 4], o)


def _pz2job(rid, base, lines, note):
    return dict(base, id="puz%d-full" % rid, screen="reference %d unsolved sheet" % rid, note=note,
                items=[(D + "rrr%d/_full.gal" % rid, "")], lines=lines)


# ---- 176 (800x1581): the shipped rep176 page burnt dark (black photo boxes, red / orange scorch) + a white chalk scrawl in 8 rows.
# The brush-heading photo and the snail photo are solid black on this sheet: the heading line (inpaint in the photo) is left out.
# Body mask: max channel <= 45 (sep.py: glyph 69 % caught at 40, paper 5 %; the shipped _RBM would take ~65 % of the paper).
_PZ2_DARK176 = [0, 45, 0, 45, 0, 45]
_PZ2_CHALK = [150, 255, 150, 255, 150, 255]
_PZ2_C176 = "#ece2de"
PZ176 = (_pz2body(L176, _PZ2_DARK176, drop=("Green-Eye Curse-Killing",))
         + [_pz2scr("Dammit", [66, 99, 536, 225], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("Kuji and Hatanaka", [78, 280, 704, 399], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("apparently ran away.", [60, 460, 656, 560], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("Is faith in the Goddess", [33, 671, 750, 787], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("worth only that much?", [56, 833, 765, 938], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("I'm different.", [62, 1051, 593, 1178], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("With Droga,", [83, 1212, 635, 1296], _PZ2_C176, 110, _PZ2_CHALK),
            _pz2scr("I will draw near to the Goddess.", [26, 1350, 774, 1481], _PZ2_C176, 110, _PZ2_CHALK)])
JOBS += [_pz2job(176, _rbjob(176, "", L176), PZ176, "report 176 unsolved sheet (burnt page + white chalk scrawl, 8 rows)")]

# IMAGESPZ-PZ2 2026-10-16 (cont.) ---- 178 (800x1716): the shipped rep178 page darkened (vignette, near-black paper) + a pink pen scrawl
# in 21 rows, most slanted ~4-5 deg up to the right. Slanted rows: _pz2rot sets the English left-aligned on the JP centre line from the
# JP row's left edge (centre y at x0 + slope from work/images/_c/pz-PZ2/colrows.py), rot = the slope; erase = the JP row's rectangle.
# Body mask: max channel <= 22 (sep.py: paper median 52, glyph median 14; at 20 glyph 68 % / paper 3 %), grow 3; same boxes as REP178.
_PZ2_INKF = "C:/Windows/Fonts/Inkfree.ttf"


def _pz2rot(text, x0, yl, k, size, color, mask, erase, xmax=790, grow=4):
    """a slanted scrawl line: JP centre line y = yl + k * (x - x0); English left-aligned on it from x0 at `size` (auto-fit shrinks
    it only when it would run past xmax); rot = the JP slope; erase = the given JP row rectangle(s) (stroke-colour mask, texfill)."""
    a = _math.atan(k)
    seg = min((_Fn.truetype(_PZ2_INKF, size).getlength(text) + 10) * _math.cos(a), xmax - x0)
    cx, cy, hh = x0 + seg / 2.0, yl + k * seg / 2.0, abs(k) * seg / 2.0 + 2
    o = {"style": "handwriting", "color": color, "max_size": size, "method": "texfill", "mask_color": list(mask),
         "mask_grow": grow, "erase": [list(e) for e in erase], "rot": round(-_math.degrees(a), 2), "rot_h": int(size * 1.45)}
    return (text, [int(round(cx - seg / 2.0)), int(round(cy - hh)), int(round(cx + seg / 2.0)), int(round(cy + hh))], o)


def _pz2flat(text, x0, yc, size, color, mask, erase, xmax=790, grow=4):
    """a level scrawl line: English left-aligned from x0, centred on the JP row centre yc."""
    o = {"style": "handwriting", "color": color, "max_size": size, "align": "left", "method": "texfill",
         "mask_color": list(mask), "mask_grow": grow, "erase": [list(e) for e in erase]}
    return (text, [x0 - 2, int(yc - size * 0.72), xmax, int(yc + size * 0.72)], o)


def _pz2grow(lines, grow):
    return [(t, b, dict(o, mask_grow=grow)) for t, b, o in lines]


_PZ2_PINK = [130, 255, 75, 190, 95, 220]   # pink pen strokes (cores ~191,141,143; nothing else on the sheet falls in this range)
_PZ2_C178 = "#bf8d8f"
_s178 = 44                                  # JP glyphs ~40 px tall; Ink Free 44 = cap height ~37
PZ178 = (_pz2grow(_pz2body(REP178, [0, 22, 0, 22, 0, 22]), 3) + [
    _pz2rot("This is all I could find out.", 24, 74, -0.083, _s178, _PZ2_C178, _PZ2_PINK, [[18, 10, 646, 96]]),
    _pz2rot("If any surviving brethren", 24, 136, -0.079, _s178, _PZ2_C178, _PZ2_PINK, [[18, 68, 632, 156]]),
    _pz2rot("see this, please put it", 24, 195, -0.081, _s178, _PZ2_C178, _PZ2_PINK, [[18, 126, 622, 214]]),
    _pz2flat("to use.", 43, 249, _s178, _PZ2_C178, _PZ2_PINK, [[37, 222, 256, 275]]),
    _pz2rot("Someone is pulling the strings", 57, 376, -0.074, _s178, _PZ2_C178, _PZ2_PINK, [[50, 312, 662, 396]]),
    _pz2rot("behind this experiment. It's Uneme.", 57, 433, -0.068, _s178, _PZ2_C178, _PZ2_PINK, [[50, 372, 662, 454]]),
    _pz2rot("Written \"court lady,\" read \"Uneme.\"", 57, 500, -0.077, _s178, _PZ2_C178, _PZ2_PINK, [[50, 432, 662, 522]]),
    _pz2rot("If that one sets eyes on you, you're", 57, 559, -0.075, _s178, _PZ2_C178, _PZ2_PINK, [[50, 492, 662, 575]]),
    _pz2flat("finished.", 77, 615, _s178, _PZ2_C178, _PZ2_PINK, [[71, 589, 186, 642]]),
    _pz2rot("Listen, Uneme is insane.", 81, 740, -0.079, _s178, _PZ2_C178, _PZ2_PINK, [[74, 670, 706, 756]]),
    _pz2rot("That one is using this experiment,", 95, 862, -0.081, _s178, _PZ2_C178, _PZ2_PINK, [[88, 796, 690, 882]]),
    _pz2rot("this Holy Cerejeira Church,", 95, 920, -0.068, _s178, _PZ2_C178, _PZ2_PINK, [[88, 855, 690, 940]]),
    _pz2rot("trying to rake in obscene", 95, 981, -0.075, _s178, _PZ2_C178, _PZ2_PINK, [[88, 915, 690, 1003]]),
    _pz2flat("profits.", 110, 1040, _s178, _PZ2_C178, _PZ2_PINK, [[104, 1014, 223, 1067]]),
    _pz2rot("The reports Hajime Shinozaki-san", 112, 1167, -0.081, _s178, _PZ2_C178, _PZ2_PINK, [[105, 1098, 708, 1190]]),
    _pz2rot("compiled are only surface matters,", 112, 1228, -0.079, _s178, _PZ2_C178, _PZ2_PINK, [[105, 1160, 742, 1250]]),
    _pz2flat("nothing more.", 129, 1280, _s178, _PZ2_C178, _PZ2_PINK, [[123, 1252, 394, 1307]]),
    _pz2rot("Whatever happens, brethren,", 146, 1408, -0.083, _s178, _PZ2_C178, _PZ2_PINK, [[140, 1340, 732, 1428]]),
    _pz2flat("run.", 145, 1471, _s178, _PZ2_C178, _PZ2_PINK, [[139, 1445, 205, 1497]]),
    _pz2rot("And let the outside world", 153, 1589, -0.075, _s178, _PZ2_C178, _PZ2_PINK, [[146, 1524, 742, 1610]]),
    _pz2flat("know.", 160, 1653, _s178, _PZ2_C178, _PZ2_PINK, [[154, 1629, 221, 1678]])])
JOBS += [_pz2job(178, _r1job(178, REP178, "", "#231803"), PZ178, "report 178 unsolved sheet (darkened page + pink pen scrawl, 21 rows)")]

# IMAGESPZ-PZ2 2026-10-16 (cont.) ---- 192 (800x1822): the shipped rep192 page on a purple-grey scratched ground (dark at the top, lighter
# in the middle) + a salmon-pink brush scrawl in 14 level rows (glyphs ~55-65 px). Body: REP192 verbatim, same boxes; the glyph mask is
# picked per erase box by its centre y (sep.py per box: the largest max-channel threshold that takes <= ~6 % of the paper there).
def _pz2bodyb(lines, bands, grow=3):
    """the shipped body lines; each line's glyph mask = max channel <= the threshold of the band (y0, y1, thr) holding the centre of
    its first erase box (lines that erase nothing are kept as they are)."""
    out = []
    for e in lines:
        t, b, o = e[0], list(e[1]), (dict(e[2]) if len(e) > 2 else {})
        eb = o.get("erase", [b])
        if eb:
            yc = (eb[0][1] + eb[0][3]) / 2.0
            thr = [v for y0, y1, v in bands if y0 <= yc < y1][0]
            o["mask_color"], o["mask_grow"] = [0, thr, 0, thr, 0, thr], grow
        out.append((t, b, o))
    return out


_PZ2_SALMON = [205, 255, 60, 195, 0, 205]   # brush cores ~235,174,178; the grey paper / scratches stay below r 205 or above g 195
_PZ2_C192 = "#ebaeb2"
_s192 = 50
PZ192 = (_pz2bodyb(REP192, [(0, 90, 25), (90, 740, 40), (740, 990, 85), (990, 1080, 85), (1080, 1320, 65), (1320, 1560, 48),
                            (1560, 1680, 30), (1680, 1822, 25)]) + [
    _pz2flat("I heard Uneme and Kichizo-sama", 4, 82, _s192, _PZ2_C192, _PZ2_SALMON, [[0, 43, 764, 121]]),
    _pz2flat("talking.", 11, 170, _s192, _PZ2_C192, _PZ2_SALMON, [[5, 136, 446, 203]]),
    _pz2flat("Damn you, Uneme.", 11, 341, _s192, _PZ2_C192, _PZ2_SALMON, [[5, 308, 456, 374]]),
    _pz2flat("Toying with Kichizo-sama's pure", 14, 507, _s192, _PZ2_C192, _PZ2_SALMON, [[8, 461, 798, 553]]),
    _pz2flat("heart.", 19, 600, _s192, _PZ2_C192, _PZ2_SALMON, [[13, 567, 320, 633]]),
    _pz2flat("I heard some people ran away, but", 18, 763, _s192, _PZ2_C192, _PZ2_SALMON, [[12, 723, 800, 803]]),
    _pz2flat("against Uneme's power, after all,", 27, 845, _s192, _PZ2_C192, _PZ2_SALMON, [[21, 806, 800, 884]]),
    _pz2flat("is there really nothing to be", 28, 930, _s192, _PZ2_C192, _PZ2_SALMON, [[22, 892, 800, 967]]),
    _pz2flat("done?", 32, 1029, _s192, _PZ2_C192, _PZ2_SALMON, [[26, 997, 258, 1061]]),
    _pz2flat("Somehow I must bring back", 40, 1190, _s192, _PZ2_C192, _PZ2_SALMON, [[34, 1150, 800, 1229]]),
    _pz2flat("Kichizo-sama's heart.", 30, 1280, _s192, _PZ2_C192, _PZ2_SALMON, [[24, 1245, 642, 1314]]),
    _pz2flat("The Holy Cerejeira Church is not", 44, 1440, _s192, _PZ2_C192, _PZ2_SALMON, [[38, 1402, 800, 1477]]),
    _pz2flat("an evil cult.", 44, 1536, _s192, _PZ2_C192, _PZ2_SALMON, [[38, 1507, 344, 1565]]),
    _pz2flat("That Uneme is the root of all evil.", 52, 1699, _s192, _PZ2_C192, _PZ2_SALMON, [[46, 1660, 800, 1738]])])
JOBS += [_pz2job(192, _r1job(192, REP192, "", "#251904"), PZ192, "report 192 unsolved sheet (purple-grey page + salmon brush scrawl, 14 rows)")]

# IMAGESPZ-PZ3 2026-10-16 (notes/IMAGESPZ-BRIEF.md, lane PZ3; log notes/v2/_tmp/tl-log-IMAGESPZ-PZ3.md): the UNSOLVED report sheets
# rrr274 / rrr275 / rrr277 _full.gal (base sheet + pieces composed; tools/images/report_puzzle.py cuts them afterwards). Ruling 1
# (notes/v2/_tmp/rulings-IMAGESPZ.md): on these three the body is NOT typeset and NOT erased; scrawl lines only. Helper = lane R2 _r2job
# (texfill, erase_first) re-labelled. One English line per JP scrawl row (work/images/_c/pz-PZ3/part.py balanced split, one size per
# sheet), stroke-colour mask per row (rows.py / gap.py / core.py). 274: row 12 split around the eye drawing (QIMAGESPZPZ3-03).
_PZ3O274 = {"style": "handwriting", "color": "#ffedeb", "max_size": 29, "align": "left", "mask_color": [180, 255, 170, 255, 170, 255], "mask_grow": 5}
_PZ3_274 = [
    ("Hatanaka is dead. Apparently his head was crushed", [25, 34, 785, 77], dict(_PZ3O274, erase=[[20, 34, 786, 77]])),  # 634/758 px
    ("by a powerful force. They say it was pulverized", [30, 105, 785, 148], dict(_PZ3O274, erase=[[25, 106, 740, 148]])),  # 581/753 px
    ("as if a cannonball had hit it. There's no way human", [30, 177, 785, 220], dict(_PZ3O274, erase=[[25, 178, 760, 219]])),  # 621/753 px
    ("strength could do that. Was it the work of someone", [31, 248, 785, 291], dict(_PZ3O274, erase=[[26, 249, 765, 290]])),  # 629/752 px
    ("who used Droga after all? Could it be that, to test", [30, 319, 785, 362], dict(_PZ3O274, erase=[[25, 320, 766, 361]])),  # 625/753 px
    ("Droga's practical use, Droga has finally come to", [29, 390, 785, 433], dict(_PZ3O274, erase=[[24, 391, 766, 432]])),  # 575/754 px
    ("be used outside the sect as well? If so, it may be", [29, 460, 785, 503], dict(_PZ3O274, erase=[[24, 461, 766, 503]])),  # 604/754 px
    ("only a matter of time before I'm killed too.", [30, 530, 697, 573], dict(_PZ3O274, erase=[[25, 529, 590, 575]])),  # 528/665 px
    ("Hatanaka's two sons grieved terribly, but now it has turned", [25, 602, 785, 645], dict(_PZ3O274, erase=[[20, 602, 756, 646]])),  # 733/758 px
    ("into a fierce rage at the sect. Yes, this is how our rage will", [32, 674, 785, 717], dict(_PZ3O274, erase=[[27, 675, 744, 717]])),  # 721/751 px
    ("be handed down across the generations. Never, ever forgive", [30, 744, 785, 787], dict(_PZ3O274, erase=[[25, 744, 762, 788]])),  # 732/753 px
    ("the Holy Cerejeira Church. Even", [30, 818, 478, 861], dict(_PZ3O274, erase=[[25, 817, 483, 863]])),  # 392/446 px
    ("if the sect", [630, 818, 785, 861], dict(_PZ3O274, erase=[[625, 817, 765, 863]])),  # 132/153 px
    ("is destroyed, never forgive the Mikogami clan. No mercy,", [30, 888, 785, 931], dict(_PZ3O274, erase=[[25, 889, 748, 931]])),  # 686/753 px
    ("down to the women and children of the last generation.", [29, 958, 785, 1001], dict(_PZ3O274, erase=[[24, 959, 782, 1001]])),  # 671/754 px
]
_PZ3O275 = {"style": "handwriting", "color": "#080200", "max_size": 35, "align": "left", "mask_color": [0, 60, 0, 50, 0, 50], "mask_grow": 4}
_PZ3_275 = [
    ("How could this be. Was I mistaken? I", [90, 84, 762, 134], dict(_PZ3O275, erase=[[85, 86, 727, 133]])),  # 559/670 px
    ("thought one of the test subjects had carried", [89, 156, 762, 206], dict(_PZ3O275, erase=[[84, 158, 730, 205]])),  # 660/671 px
    ("these reports out as an inside whistleblower", [89, 229, 762, 279], dict(_PZ3O275, erase=[[84, 229, 706, 280]])),  # 650/671 px
    ("and left them somewhere people would see", [88, 301, 762, 351], dict(_PZ3O275, erase=[[83, 302, 686, 351]])),  # 623/672 px
    ("them. But it's the reverse. Uneme staged", [88, 374, 762, 424], dict(_PZ3O275, erase=[[83, 375, 735, 423]])),  # 619/672 px
    ("all of this. Doing this stirs up distrust", [89, 446, 762, 496], dict(_PZ3O275, erase=[[84, 446, 729, 496]])),  # 563/671 px
    ("among the brethren and makes the sect", [89, 517, 762, 567], dict(_PZ3O275, erase=[[84, 519, 744, 566]])),  # 591/671 px
    ("fall apart. Kichizo-sama will fall from power", [89, 592, 762, 642], dict(_PZ3O275, erase=[[84, 590, 728, 645]])),  # 641/671 px
    ("too. All that will be left are the results of", [97, 661, 762, 711], dict(_PZ3O275, erase=[[92, 662, 732, 710]])),  # 620/663 px
    ("the Droga research. Once the sect is gone,", [89, 730, 762, 780], dict(_PZ3O275, erase=[[84, 729, 730, 782]])),  # 622/671 px
    ("Uneme will move the world, unhindered by", [87, 806, 762, 856], dict(_PZ3O275, erase=[[82, 806, 664, 857]])),  # 604/673 px
    ("anyone, and make a fortune. But who should", [96, 877, 762, 927], dict(_PZ3O275, erase=[[91, 878, 727, 927]])),  # 645/664 px
    ("I tell this truth to? The anti-sect forces", [87, 949, 762, 999], dict(_PZ3O275, erase=[[82, 949, 726, 1000]])),  # 614/673 px
    ("can no longer be stopped. Ah, did everything", [88, 1021, 762, 1071], dict(_PZ3O275, erase=[[83, 1022, 731, 1071]])),  # 639/672 px
    ("go just as Uneme wanted?", [89, 1093, 603, 1143], dict(_PZ3O275, erase=[[84, 1094, 504, 1142]])),  # 387/512 px
    ("I TOLD YOU SO, YOU FOOLS", [33, 1164, 785, 1236], {"style": "handwriting", "color": "#6e0c12", "max_size": 44, "align": "left", "mask_color": [80, 255, 0, 45, 0, 60], "mask_grow": 5, "erase": [[26, 1158, 785, 1238]]}),
]
_PZ3O277 = {"style": "handwriting", "color": "#1b0000", "max_size": 28, "align": "left", "mask_color": [0, 90, 0, 70, 0, 70], "mask_grow": 3}
_PZ3_277 = [
    ("I heard it from a subordinate I trust. So it was all", [37, 46, 767, 88], dict(_PZ3O277, erase=[[32, 48, 756, 87]])),  # 617/728 px
    ("something Uneme-san arranged. I had been looked", [37, 87, 767, 129], dict(_PZ3O277, erase=[[32, 90, 759, 127]])),  # 599/728 px
    ("after since I was a child, so I never even tried to", [41, 129, 767, 171], dict(_PZ3O277, erase=[[36, 132, 751, 168]])),  # 601/724 px
    ("doubt it. They say the reports so far had also been", [42, 170, 767, 212], dict(_PZ3O277, erase=[[37, 174, 750, 209]])),  # 609/723 px
    ("falsified before they were delivered to me. Many of the", [35, 211, 767, 253], dict(_PZ3O277, erase=[[30, 212, 718, 252]])),  # 666/730 px
    ("brethren were sacrificed. I was truly a fool.", [40, 253, 648, 295], dict(_PZ3O277, erase=[[35, 255, 531, 293]])),  # 523/606 px
    ("But if I make this public, Uneme-san will set out in", [47, 336, 767, 378], dict(_PZ3O277, erase=[[42, 338, 758, 376]])),  # 616/718 px
    ("earnest to crush the sect. On the surface, I will keep", [39, 377, 767, 419], dict(_PZ3O277, erase=[[34, 379, 752, 417]])),  # 645/726 px
    ("Uneme-san's name out of it and write a memo calling for", [42, 417, 767, 459], dict(_PZ3O277, erase=[[37, 419, 755, 458]])),  # 672/723 px
    ("the eradication of Droga and the erasure of its traces.", [44, 460, 767, 502], dict(_PZ3O277, erase=[[39, 463, 634, 499]])),  # 657/721 px
    ("I too have little life left. If I go to where the brethren", [35, 541, 767, 583], dict(_PZ3O277, erase=[[30, 543, 759, 582]])),  # 689/730 px
    ("who were sacrificed are and let them see me burned", [40, 583, 767, 625], dict(_PZ3O277, erase=[[35, 585, 749, 623]])),  # 622/725 px
    ("in the flames of hell, will it be even a small comfort?", [40, 625, 767, 667], dict(_PZ3O277, erase=[[35, 626, 752, 666]])),  # 624/725 px
    ("What I did is truly inexcusable.", [38, 666, 477, 708], dict(_PZ3O277, erase=[[33, 670, 394, 705]])),  # 365/437 px
    ("But the Holy Cerejeira Church can never be allowed", [39, 748, 767, 790], dict(_PZ3O277, erase=[[34, 750, 753, 789]])),  # 608/726 px
    ("to disband. From now on, a watch must be kept", [41, 789, 767, 831], dict(_PZ3O277, erase=[[36, 792, 746, 829]])),  # 562/724 px
    ("for anyone who uses Droga. The Mikogami family", [39, 831, 767, 873], dict(_PZ3O277, erase=[[34, 833, 757, 871]])),  # 580/726 px
    ("will not forgive those who misuse Droga.", [41, 872, 643, 914], dict(_PZ3O277, erase=[[36, 874, 634, 913]])),  # 482/600 px
]
JOBS += [
    # 274 re-done after the QIMAGESPZPZ3-01 ruling (body readable on this sheet): body = the shipped REP274 lines verbatim, ink
    # #150800, same erase boxes, BUT erased beforehand by work/images/_c/pz-PZ3/pre274.py (glyph mask from 全体.png with _RMASK:
    # on the red sheet _RMASK takes the whole page and the cracks share the print colour), so this job CHAINS from that output:
    # always run pre274.py right before `runpz-PZ3.sh puz274-full`, then `--previews-only` (preview = JP original | result).
    # Scrawl lines after the body (drawn on top, ruling 4); eye drawing kept.
    dict(_r2job(274, [(t, b, dict(o, erase=[])) for t, b, o in REP274] + _PZ3_274,
                "unsolved sheet: body (REP274) + white chalk scrawl re-set; eye drawing kept (QIMAGESPZPZ3-01)", "#150800"),
         id="puz274-full", screen="reference 274 unsolved sheet", chain=True, items=[(D + "rrr274/_full.gal", "")]),
    dict(_r2job(275, _PZ3_275, "unsolved sheet: black brush scrawl + red katakana row re-set; mirrored ghost print kept (ruling 1)",
                "#080200"),
         id="puz275-full", screen="reference 275 unsolved sheet", style="handwriting", items=[(D + "rrr275/_full.gal", "")]),
    dict(_r2job(277, _PZ3_277, "unsolved sheet: black pen scrawl re-set; mirrored ghost print + blood kept (ruling 1)", "#1b0000"),
         id="puz277-full", screen="reference 277 unsolved sheet", style="handwriting", items=[(D + "rrr277/_full.gal", "")]),
]
# end IMAGESPZ-PZ3

# IMAGESPZ-PZ2 2026-10-16 (cont.) ---- 284 (800x1806): the shipped rep284 page on dark red paper with pink blotches + a grey-white brush
# scrawl in 15 level rows (glyphs ~43 px, x 75-709, pitch ~118). Body: REP284 verbatim, same boxes; mask per erase box (_pz2bodyb):
# title 45, body 55, footer 60 (sep.py per y band: <= ~5 % of the paper).
_PZ2_GREY = [150, 255, 150, 255, 150, 255]  # brush cores ~209,190,193; rows2.py: nothing outside the 15 rows reaches this range
_PZ2_C284 = "#d1bec1"
_s284 = 42


def _pz2r284(text, y0, y1, x1=709):
    return _pz2flat(text, 77, (y0 + y1) / 2.0, _s284, _PZ2_C284, _PZ2_GREY, [[69, y0 - 8, x1 + 8, y1 + 8]], xmax=795)


PZ284 = (_pz2bodyb(REP284, [(0, 100, 45), (100, 1680, 55), (1680, 1806, 60)]) + [
    _pz2r284("Word on the wind is, in Megasawa City,", 60, 102, 707),
    _pz2r284("there's a move to break up the sect,", 177, 220, 696),
    _pz2r284("it seems. Well, Uneme will probably crush", 296, 338, 703),
    _pz2r284("it soon, but the people's will doesn't", 412, 456, 707),
    _pz2r284("change that easily. If this faction", 531, 574, 704),
    _pz2r284("would just grow, then even Uneme", 648, 692, 704),
    _pz2r284("couldn't put it down so easily.", 767, 810, 709),
    _pz2r284("Could it be Kuji, Hatanaka, or the like", 884, 928, 703),
    _pz2r284("who made a move?", 1004, 1046, 232),
    _pz2r284("Well, so the time that had to come", 1121, 1165, 696),
    _pz2r284("has finally come, has it? I'd better", 1238, 1283, 708),
    _pz2r284("hide myself soon too. Fortunately,", 1355, 1401, 677),
    _pz2r284("the personal details of those involved", 1475, 1519, 706),
    _pz2r284("in this research probably haven't leaked", 1593, 1637, 704),
    _pz2r284("outside.", 1712, 1754, 330)])
JOBS += [_pz2job(284, _r2job(284, REP284, "", "#231803"), PZ284, "report 284 unsolved sheet (red blotched page + grey-white brush scrawl, 15 rows)")]


# IMAGESPZ-PZ1 2026-10-16 (notes/IMAGESPZ-BRIEF.md, lane PZ1; rulings notes/v2/_tmp/rulings-IMAGESPZ.md; log
# notes/v2/_tmp/tl-log-IMAGESPZ-PZ1.md): the UNSOLVED report sheets rrr<ID>/_full.gal of reports 41 155 169 174 (base sheet + pieces
# composed; tools/images/report_puzzle.py cuts 土台 / N / Na out of the render). Body = the shipped report job's lines verbatim and its
# erase boxes, with a sheet-specific glyph mask + ink (the sheets are recoloured: the shipped masks would select the whole page;
# work/images/_c/pz-PZ1/mk.py). Scrawl = style handwriting, one English line per JP line in its row, erased with a mask on the
# stroke colour (texfill), set last so it crosses the body as drawn. Row boxes from work/images/_c/pz-PZ1/bbox.py.
def _pz1body(lines, mask, noerase_below=None, plate=None):
    """the shipped body lines with this sheet's glyph mask; erase boxes reaching below noerase_below dropped (art there);
    flat-plate lines (white type on a plate) set without the plate fill in `plate` colour when given."""
    out = []
    for t, b, o in lines:
        o = dict(o)
        if o.get("method") == "flat" and plate:
            o = {"erase": [], "color": plate, "align": o.get("align", "center"), "max_size": o.get("max_size", 24),
                 "line_spacing": o.get("line_spacing", 1.0)}
        else:
            o["mask_color"] = mask
            if noerase_below is not None:
                o["erase"] = [e for e in o.get("erase", [b]) if e[3] <= noerase_below]
        out.append((t, b, o))
    return out


def _pz1s(text, bb, ink, mask, size, pad=6, x1=792, tpad=0, **k):
    """one scrawl line: bb = the JP row's stroke bbox [x0, y0, x1, y1]; text box from the row start to x1 (tpad px taller above and
    below, so the line height does not cap the size under the JP stroke height), erase = bbox + pad."""
    o = {"style": "handwriting", "color": ink, "mask_color": mask, "mask_grow": 5, "max_size": size, "align": "left",
         "method": "texfill", "erase": [[max(0, bb[0] - pad), max(0, bb[1] - pad), bb[2] + pad, bb[3] + pad]]}
    o.update(k)
    return (text, [max(0, bb[0] - 4), max(0, bb[1] - tpad), x1, bb[3] + tpad], o)


def _pz1job(rid, base, scrawl, note):
    j = dict(base)
    j.update(id="puz%d-full" % rid, screen="reference %d unsolved sheet" % rid, items=[(D + "rrr%d/_full.gal" % rid, "")],
             lines=list(base.get("lines", [])) + scrawl, note=note, new=True)
    return j


# ---- 41 (800x1733): dark grey sheet, black handprints / drips, white chalk scrawl (10 rows, sentence case). The body on this sheet is
# a MIRRORED ghost of the print (align.py: correlation with the left-right flipped 全体 -7.5 / -6.1 vs -1.3 / -0.7 unflipped), so the
# body stays as drawn: no body erase, scrawl only (QIMAGESPZPZ1-01; ruling 1's criterion for 274 275 277). Chalk mask: every channel > 110.
_PZ41M = [111, 255, 111, 255, 111, 255]
_PZ41I = "#d0cecb"
PZ41 = [_pz1s(t, bb, _PZ41I, _PZ41M, 84) for t, bb in (
    ("This much", [60, 105, 547, 212]),
    ("is nothing", [83, 242, 776, 355]),
    ("I'm going to get close", [44, 450, 754, 594]),
    ("to the Goddess", [52, 610, 703, 715]),
    ("But it hurts", [107, 720, 646, 834]),
    ("My head hurts", [50, 838, 637, 984]),
    ("Ever since the", [46, 988, 750, 1139]),
    ("green-eyed corpse", [47, 1152, 735, 1307]),
    ("and I became one", [60, 1337, 614, 1484]),
    ("What am I", [37, 1490, 783, 1730]))]
JOBS += [_pz1job(41, {"style": "handwriting", "mode": "lines", "erase": "texfill", "erase_first": True, "mask_grow": 5,
                      "mask_color": _PZ41M, "color": _PZ41I}, PZ41,
                 "report 41 unsolved sheet (white chalk scrawl; mirrored ghost body kept as drawn)")]

# ---- 155 (800x1184): red sheet with dark veins; the shipped REP155 page (body unmirrored, glyph cores ~40,0,0: mask [0,75,0,30,0,30]
# catches 0.83-0.98 of them) + a pink-white chalk scrawl, 6 rows, ALL CAPS (ruling 2; QIMAGESPZPZ1-02).
_PZ155M = [140, 255, 110, 255, 100, 255]
_PZ155I = "#e8cfc8"
PZ155 = [_pz1s(t, bb, _PZ155I, _PZ155M, 96) for t, bb in (
    ("SAME AS EVER", [74, 45, 626, 170]),
    ("MY HEAD HURTS", [72, 187, 455, 318]),
    ("THE CORPSE STARTED", [62, 336, 758, 505]),
    ("STINKING, DAMN IT", [38, 552, 664, 658]),
    ("BUT I KIND OF LIKE", [65, 730, 755, 836]),
    ("THIS ONE.", [58, 880, 477, 999]))]
JOBS += [_pz1job(155, _r1job(155, _pz1body(REP155, [0, 75, 0, 30, 0, 30]), "", "#260000"), PZ155,
                 "report 155 unsolved sheet (red page + pink-white chalk scrawl)")]

# ---- 169 (800x2607): dark brown sheet with a faint body (unmirrored; contrast median -6 at the top) and red / black tree art over the
# lower half. Body = L169 verbatim, ink #2c1614 (the darker JP strokes); erase (mask [0,58,0,32,0,32]) only for boxes ending above
# y 1700 (under the tree the JP has no contrast and a colour mask would take the branches); the three Blood plates without plate fill
# (QIMAGESPZPZ1-03). Scrawl, ALL CAPS: 5 white chalk rows (semi-transparent, mask r>=95 g>=82 b>=80), the red brush (クルシイ /
# タスケテ / イタイ / ムスメヲカエセ as an L: down the left edge, then along the bottom / カエリタイ rising to the right), and a
# pink-white two-row line at the bottom right.
_PZ169W = [95, 255, 82, 255, 80, 255]
_PZ169R = [105, 255, 0, 80, 0, 80]
_PZ169P = [140, 255, 95, 255, 95, 255]
PZ169 = ([_pz1s(t, bb, "#9c8c89", _PZ169W, 130, tpad=15) for t, bb in (
             ("HAPPY", [72, 90, 589, 291]),
             ("I CAN USE", [102, 379, 737, 521]),
             ("DROGA", [65, 595, 646, 722]),
             ("GLORY TO", [60, 782, 782, 940]),
             ("CEREJEIRA", [71, 969, 723, 1156]))]
         + [_pz1s(t, bb, "#881210", _PZ169R, 120, x1=760) for t, bb in (
             ("IT'S AGONY", [126, 1399, 588, 1532]),
             ("HELP ME", [82, 1552, 660, 1716]),
             ("IT HURTS", [335, 1806, 697, 1998]))]
         + [("", [26, 1808, 264, 2434],
             {"mask_color": _PZ169R, "mask_grow": 5, "method": "texfill", "erase": [[26, 1808, 264, 2434], [101, 2418, 592, 2607]]})]
         + [(t, b, {"style": "handwriting", "color": "#881210", "max_size": s, "align": "left", "erase": []}) for t, b, s in (
             ("GIVE", [30, 1814, 262, 1935], 84),
             ("MY", [30, 1941, 262, 2080], 84),
             ("DAUGHTER", [30, 2085, 330, 2245], 84),
             ("BACK", [30, 2290, 400, 2600], 110))]
         + [("I WANT TO GO HOME", [290, 2178, 770, 2302],
             {"style": "handwriting", "color": "#881210", "mask_color": _PZ169R, "mask_grow": 5, "max_size": 110, "rot": 15,
              "rot_h": 110, "method": "texfill", "erase": [[264, 2196, 486, 2372], [478, 2083, 798, 2343]]})]
         + [_pz1s(t, bb, "#c8a4a2", _PZ169P, 76, x1=770) for t, bb in (
             ("THE GODDESS", [413, 2353, 767, 2447]),
             ("IS GREAT", [487, 2467, 780, 2584]))])
# IMAGESPZ-PZ1 2026-10-16 (cont.) checker round 1: 169's red block re-laid inside the page with no overlaps (the ムスメヲ column set as
# horizontal words stacked in its spot, BACK at the column foot; the rising カエリタイ line kept at 15 deg inside x 276-783), red =
# the JP brush sampled bright (#881210); every scrawl line drawn 9 times on a 0..2 px grid (_pz1bold) for a stroke weight near the JP.


def _pz1bold(lines, d=2):
    out = []
    for t, b, o in lines:
        out.append((t, b, o))
        if t:
            for dx in range(d + 1):
                for dy in range(d + 1):
                    if dx or dy:
                        out.append((t, [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy], dict(o, erase=[])))
    return out


PZ169 = _pz1bold(PZ169)
JOBS += [_pz1job(169, _rbjob(169, "", _pz1body(L169, [0, 58, 0, 32, 0, 32], noerase_below=1700, plate="#6a4a48"),
                             color="#2c1614", mask_color=[0, 58, 0, 32, 0, 32]), PZ169,
                 "report 169 unsolved sheet (faint body; white chalk + red brush + pink-white scrawls)")]

# ---- 174 (800x1490): ochre parchment, the shipped L174 page (body cores ~12,0,0: mask [0,60,0,35,0,35] catches 0.89-1.00 of them,
# 0.00 of the paper) + two reds: a dark-crimson pen (rows 1, 2, 7) and a translucent red brush (rows 3-6, 8, 9); one erase mask
# [65,200,0,45,0,40] for both. ALL CAPS (katakana scrawl). Digits as drawn.
_PZ174M = [65, 200, 0, 45, 0, 40]
_PZ174A = "#760604"   # checker round 1: every row in the JP brush red sampled bright (stroke cores ~100-118,4,2), drawn bold
_PZ174B = "#760604"
PZ174 = [_pz1s(t, bb, ink, _PZ174M, 84, tpad=12) for t, bb, ink in (
    ("I'M IN ROOM 1015", [64, 58, 776, 136], _PZ174A),
    ("MY SONS TOO, TWO OF THEM", [74, 163, 779, 278], _PZ174A),
    ("YOU IN 1105", [87, 334, 681, 427], _PZ174B),
    ("STOLE THE KEY", [51, 480, 765, 606], _PZ174B),
    ("TO THE EAST DOOR", [59, 617, 730, 724], _PZ174B),
    ("WHEN DO WE RUN", [73, 759, 683, 861], _PZ174B),
    ("AS SOON AS TONIGHT", [48, 940, 726, 1076], _PZ174A),
    ("GOT IT", [53, 1110, 440, 1280], _PZ174B),
    ("AT ONE IN THE NIGHT", [107, 1326, 769, 1431], _PZ174B))]
# checker round 1: over the dark lower photo the JP brush is dark red (~53,2,2), outside the mask above: one more erase-only pass
# there (red with g, b <= 28), so the whole ワカッタ / コンヤニデモ strokes go; then every row bold (_pz1bold).
PZ174 = _pz1bold(PZ174 + [("", [40, 985, 735, 1290], {"mask_color": [35, 200, 0, 28, 0, 26], "mask_grow": 4, "method": "texfill",
                                                       "erase": [[40, 985, 735, 1290]]})])
JOBS += [_pz1job(174, _rbjob(174, "", _pz1body(L174, [0, 60, 0, 35, 0, 35]), color="#0c0000", mask_color=[0, 60, 0, 35, 0, 35]),
                 PZ174, "report 174 unsolved sheet (parchment page + two red scrawls)")]
