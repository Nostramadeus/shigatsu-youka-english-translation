"""jobs_tierb.py - Tier B picture jobs: the rest of the UI (right-click menu, main menu, encyclopedia,
reference screen, chatter, document mode, the engine's own option menu, shatter frames, the blurred wallpaper
twin) plus the three part-1 story pictures. Copy of the jobs_part1.py shape; jobs_part1.py is untouched.

Run: batch.py --jobs jobs_tierb [--only ID] [--no-ship]

Each job: id, screen, style (FONTS in batch.py: gothic / serif / rounded / handwriting / brush), items = the
pictures that share a layout, one English string per item, erase method, optional overrides (3rd tuple element).
Erase methods: flat | alpha | inpaint | inpainta (colour AND alpha plane, for lettering over icon art) |
maskfill (paint the glyph pixels in the plate colour) | maskalpha.
Modes: default | words (one string per word_boxes entry) | boxes | blank (erase only) |
rotated (rot_lines = strings set at an angle) | lines (one string per named box, erased box by box, so table
rules and icon columns survive: this is how the help panels are rebuilt).
`max_size` caps the auto-fit so a menu keeps one type size instead of one size per button. Other job keys:
mask_grow, alpha_thr (lettering on a semi-transparent fade), keep_alpha, align, chain (start from the previous
job's output instead of the Japanese original, for a second pass on the same picture).
Wording that already exists in patch/labels-*.tsv, tsv-en/ or GLOSSARY is reused verbatim; `wording` names it.
new=True jobs are logged to notes/_tmp/tl-log-IMAGES2.md.
"""
import os

M = "グラフィック/メニュー/"
R = "グラフィック/メニュー/右クリック/"
W = "グラフィック/メニュー/右クリック/ワード/"
TK = "グラフィック/メニュー/右クリック/雑談/"
RF = "グラフィック/リファレンス/"
D = "グラフィック/ドキュメント/"
E = "グラフィック/インターフェース/システムメニュー/"
S = "グラフィック/システム/"
BG = "グラフィック/背景/"

# ---------------------------------------------------------------------------------------------------------
# the engine's own option menu: one label per state file (plain / (選択) / (ON)). The bracket glyphs are part
# of the file name, so the files are matched by prefix against the extracted folder instead of hard-coded.
ENGINE_LABELS = [
    ("オプション", "Options"),
    ("ゲーム終了", "Quit game"),
    ("サウンドを再生する", "Play sound"),
    ("シナリオ回想", "Scenario replay"),
    ("セリフ", "Effects"),
    ("セーブ", "Save"),
    ("タイトル画面に戻る", "Return to the title"),
    ("テキスト速度", "Text speed"),
    ("ディスプレイモード", "Display mode"),
    ("フォント選択", "Select font"),
    ("フルスクリーン", "Full screen"),
    ("ロード", "Load"),
    ("効果音", "Ambient"),
    ("文字を消す", "Hide the text"),          # the picture reads テキスト非表示
    ("_文字を消す", "Hide the text"),         # second widget set; the picture reads 文字を消す
    ("既読文章をスキップ", "Skip text you have read"),
    ("終了", "Quit"),
    ("自動テキスト送り", "Auto text advance"),
    ("自動テキスト送り速度", "Auto text advance speed"),
    ("読んだ文章を飛ばす", "Skip text already read"),
    ("音量調整", "Volume"),
    ("ＭＩＤＩ出力ポート", "MIDI output port"),
    # ＢＧＭ is already Latin (full-width ＢＧＭ): left alone.
]


def _engine_items():
    folder = "work/images/png/" + E.rstrip("/")
    names = sorted(os.listdir(folder)) if os.path.isdir(folder) else []
    items = []
    for base, en in ENGINE_LABELS:
        for n in names:
            if not n.endswith(".png"):
                continue
            stem = n[:-4]
            if stem == base or (stem.startswith(base) and stem[len(base):].startswith(("(", "（"))):
                items.append((E + stem + ".gal", en))
    return items


JOBS = [
    # ==== right-click menu: the item buttons (navy = normal, dark red = hover) ==============================
    dict(id="rc-buttons", screen="right-click menu", style="gothic", erase="flat", max_size=26,
         items=[(R + "_リファレンス.gal", "References"), (R + "_リファレンスs.gal", "References"),
                (R + "リファレンス.gal", "References"), (R + "リファレンスs.gal", "References"),
                (R + "_ワード.gal", "Encyclopedia"), (R + "_ワードs.gal", "Encyclopedia"),
                (R + "ワード.gal", "Encyclopedia"), (R + "ワードs.gal", "Encyclopedia"),
                (R + "_雑談.gal", "Chatter"), (R + "_雑談s.gal", "Chatter"),
                (R + "雑談.gal", "Chatter"), (R + "雑談s.gal", "Chatter"),
                (R + "スクロール速度.gal", "Scroll speed"), (R + "スクロール速度s.gal", "Scroll speed"),
                (R + "セーブ.gal", "Load"), (R + "セーブs.gal", "Load"),
                (R + "タイトルへ.gal", "Title screen"), (R + "タイトルへs.gal", "Title screen"),
                (R + "チュートリアル.gal", "Tutorial"), (R + "チュートリアルs.gal", "Tutorial"),
                (R + "ドキュメント.gal", "Documents"), (R + "ドキュメントs.gal", "Documents"),
                (R + "ミニマップ.gal", "Minimap"), (R + "ミニマップs.gal", "Minimap"),
                (R + "メモ.gal", "Memo"), (R + "メモs.gal", "Memo"),
                (R + "音量調整.gal", "Volume"), (R + "音量調整s.gal", "Volume"),
                (R + "閉じる.gal", "Close"), (R + "閉じるs.gal", "Close"),
                (R + "名前変更.gal", "Rename"), (R + "名前変更s.gal", "Rename"),
                (R + "現在の編のみ.gal", "Current arc only"), (R + "現在の編のみs.gal", "Current arc only"),
                (R + "人物タブ.gal", "People"), (R + "人物タブs.gal", "People"),
                (R + "出来事タブ.gal", "Events"), (R + "出来事タブs.gal", "Events"),
                (R + "用語タブ.gal", "Terms"), (R + "用語タブs.gal", "Terms")],
         wording="GLOSSARY (reference / encyclopedia / chatter), labels-0000001E (Scroll speed), "
                 "tsv-en/チュートリアル.tsv (Tutorial, Memo, people, events)", new=True,
         note="the file name is not the label: セーブ.gal reads ロード, ワード/_ワード read 事典, 現在の編のみ reads 現在の編のみ表示"),
    dict(id="rc-yesno", screen="right-click menu (quit prompt)", style="brush", erase="inpaint", caps=False, stroke=0,
         items=[(R + "タイトルはいボタンs.gal", "Yes", {"color": "#942724"}),
                (R + "タイトルいいえボタンs.gal", "No", {"color": "#942724"})],
         wording="tsv-en/注意.tsv (Yes / No)"),
    dict(id="rc-window-captions", screen="right-click menu (section captions)", style="gothic", erase="alpha",
         mode="words", max_size=26,
         items=[(R + "ウィンドウテキスト.gal", None)],
         words=["Library", "Scenario navigator", "Config"],
         word_boxes=[[4, 2, 150, 40], [4, 98, 262, 142], [4, 190, 152, 234]],
         wording="tsv-en/チュートリアル.tsv (scenario navigator)", new=True),
    # ==== main menu ========================================================================================
    dict(id="mainmenu-buttons", screen="main menu", style="gothic", erase="inpaint", max_size=32,
         items=[(M + "シナリオナビ.gal", "Scenario navigator", {"box": [78, 14, 296, 66]}),
                (M + "リファレンス.gal", "References", {"box": [78, 14, 296, 66]}),
                (M + "各種設定.gal", "Settings", {"box": [78, 14, 296, 66]})],
         wording="tsv-en/チュートリアル.tsv (scenario navigator, references)", new=True),
    dict(id="mainmenu-navi-on", screen="main menu (hover bar)", style="gothic", erase="inpaint",
         mode="words", max_size=22, color="#ffffff", stroke=0,
         items=[(M + "シナリオナビオン.gal", None)],
         words=["Scenario navigator",
                "The navigation map for the\nmain scenario. You advance\nthe scenario from here."],
         word_boxes=[[82, 14, 230, 66], [234, 6, 490, 72]], new=True),
    dict(id="mainmenu-ref-on", screen="main menu (hover bar)", style="gothic", erase="inpaint",
         mode="words", max_size=22, color="#ffffff", stroke=0,
         items=[(M + "リファレンスオン.gal", None)],
         words=["References",
                "View the references (reference\nmaterial) obtained in a scenario."],
         word_boxes=[[84, 18, 232, 62], [236, 10, 486, 68]], new=True),
    dict(id="mainmenu-settings-on", screen="main menu (hover bar)", style="gothic", erase="inpaint",
         mode="words", max_size=22, color="#ffffff", stroke=0,
         items=[(M + "各種設定オン.gal", None)],
         words=["Settings", "Configures the game system."],
         word_boxes=[[80, 18, 200, 62], [232, 20, 484, 58]], new=True),
    dict(id="mainmenu-caption", screen="main menu (screen caption)", style="gothic", erase="inpaint",
         box=[20, 20, 430, 100], textbox=[26, 24, 370, 98], max_size=52,
         items=[(M + "メインメニュー.gal", "Main menu")], new=True),
    # ==== encyclopedia: category banners ====================================================================
    dict(id="word-banners", screen="encyclopedia (category banners)", style="serif", erase="inpaint", max_size=58,
         items=[(W + "人物.gal", "People", {"box": [6, 6, 220, 97], "textbox": [10, 14, 216, 90]}),
                (W + "事件.gal", "Events", {"box": [6, 6, 205, 97], "textbox": [10, 14, 200, 90]}),
                (W + "場所.gal", "Places", {"box": [6, 6, 210, 97], "textbox": [10, 14, 205, 90]}),
                (W + "物.gal", "Things and Concepts", {"box": [6, 6, 282, 97], "textbox": [10, 14, 248, 90]}),
                (W + "ギャラリー.gal", "Gallery", {"box": [6, 6, 322, 97], "textbox": [10, 14, 260, 90]}),
                (W + "楽曲紹介.gal", "Music", {"box": [6, 6, 284, 97], "textbox": [10, 14, 258, 90]})],
         wording="GLOSSARY (Things and Concepts), tsv-en/チュートリアル.tsv (people, events)", new=True),
    dict(id="word-titles", screen="encyclopedia (screen title bar)", style="gothic", erase="inpaint",
         box=[0, 0, 220, 56], textbox=[6, 2, 215, 54], max_size=40,
         items=[(W + "ワードタイトル.gal", "Encyclopedia"), (W + "ワードタイトル2035.gal", "Encyclopedia"),
                (W + "ワードタイトル赤.gal", "Encyclopedia")],
         wording="GLOSSARY (encyclopedia)"),
    dict(id="word-gallery-title", screen="encyclopedia (gallery title bar)", style="gothic", erase="inpaint",
         box=[0, 0, 230, 57], textbox=[6, 2, 245, 55], max_size=44,
         items=[(W + "ギャラリータイトル.gal", "Gallery")], new=True),
    dict(id="word-updated", screen="encyclopedia (update banner)", style="serif", erase="alpha", spacing=4,
         items=[(W + "事典更新.gal", "Encyclopedia updated")],
         wording="GLOSSARY (encyclopedia)", new=True),
    dict(id="word-tut-category", screen="encyclopedia tutorial mock screen (category buttons)", style="serif",
         erase="inpaint", mode="lines", mask_color=[150, 255, 150, 255, 140, 255], color="#f4f4f0",
         max_size=34, mask_grow=7, align="center",
         items=[(W + "チュートリアルカテゴリ.gal", None)],
         lines=[("People", [38, 74, 250, 124]), ("Places", [326, 74, 540, 124]),
                ("Events", [38, 150, 250, 200]), ("Things and Concepts", [326, 150, 560, 200]),
                ("Points left 21132", [0, 296, 160, 338])],
         wording="GLOSSARY (Things and Concepts), tsv-en/チュートリアル.tsv (people, events)", new=True),
    dict(id="word-tut-map", screen="encyclopedia tutorial mock screen (map labels)", style="serif",
         erase="inpaint", mode="lines", mask_color=[120, 255, 120, 255, 120, 255], color="#f2f6ff",
         max_size=15, mask_grow=9, align="left", stroke=1, stroke_color="#101820",
         items=[(W + "チュートリアル場所.gal", None)],
         lines=[("Motoki-cho, Sawa Prefecture", [196, 4, 434, 48]),
                ("Goto house", [234, 78, 332, 98]), ("Motoki H.S.", [386, 106, 492, 126]),
                ("Chuo Park", [298, 134, 396, 154]), ("Cram school", [148, 188, 246, 208]),
                ("Police stn.", [248, 200, 352, 220]), ("Zahha #35", [430, 264, 530, 284]),
                ("Repo Heights", [454, 294, 558, 314])],
         wording="GLOSSARY (Motoki-cho, Sawa Prefecture, Motoki High School, Chuo Park, the Motoki cram school, "
                 "Motoki Police Station, Zahha)", new=True,
         note="map labels abbreviated so the English fits the same spots; the title's furigana line is dropped; "
              "五島家 = Goto house and レポハイツ = Repo Heights are new (Q2444)"),
    dict(id="word-tut-caption", screen="encyclopedia tutorial mock screens (caption)", style="gothic",
         erase="inpaint", chain=True, mask_color=[0, 110, 0, 110, 0, 110], box=[0, 0, 108, 34], textbox=[4, 4, 100, 30],
         color="#0a0a0a", stroke=0, max_size=20, keep_edges=True,
         items=[(W + "チュートリアルカテゴリ.gal", "Encyclopedia"), (W + "チュートリアル人物.gal", "Encyclopedia"),
                (W + "チュートリアル出来事.gal", "Encyclopedia"), (W + "チュートリアル場所.gal", "Encyclopedia"),
                (W + "チュートリアル物.gal", "Encyclopedia")],
         wording="GLOSSARY (encyclopedia)",
         note="the five mock screens the encyclopedia tutorial shows; their list rows are deliberately pixelated "
              "in the original and stay as they are"),
    # ==== chatter ==========================================================================================
    dict(id="talk-labels", screen="chatter", style="gothic", erase="flat", max_size=24,
         items=[(TK + "古い話題.gal", "Old topics"), (TK + "新しい話題.gal", "New topics"),
                (TK + "雑談を終える.gal", "End chatter"), (TK + "話題追加.gal", "A topic has been added.")],
         wording="GLOSSARY (chatter)", new=True),
    dict(id="talk-room-title", screen="chatter (room caption)", style="gothic", erase="inpainta",
         box=[0, 0, 400, 57], textbox=[16, 6, 350, 52], max_size=34, alpha_thr=8,
         mask_color=[0, 140, 0, 84, 0, 95], keep_edges=True, color="#0a0a0a", stroke=0, mask_grow=9,
         items=[(TK + "雑談タイトル.gal", "Chat Room"), (TK + "雑談タイトル2.gal", "Lounge")], new=True,
         note="雑談タイトル reads 談話室, 雑談タイトル2 reads レストルーム; 'Rest Room' avoided (reads as a toilet in US English) -> Q2441"),
    # ==== reference screen ==================================================================================
    dict(id="ref-heading", screen="reference screen (title bar)", style="gothic", erase="inpaint",
         box=[0, 0, 232, 50], textbox=[8, 8, 205, 44], max_size=30,
         items=[(RF + "rタイトル.gal", "References"), (RF + "rタイトルr.gal", "References")],
         wording="tsv-en/チュートリアル.tsv (the references)"),
    dict(id="ref-filters", screen="reference screen (filter plates)", style="serif", erase="inpaint", pad=2,
         color="#f5f5f5", stroke=1, stroke_color="#101010", max_size=20,
         items=[(RF + "フィルター/fNew.gal", "New"), (RF + "フィルター/fその他.gal", "Other"),
                (RF + "フィルター/fオブジェクト.gal", "Object"), (RF + "フィルター/fシナリオ.gal", "Scenario"),
                (RF + "フィルター/f中断.gal", "Broken off"), (RF + "フィルター/f書簡.gal", "Letters"),
                (RF + "フィルター/f読了.gal", "Complete")],
         wording="tsv-en/チュートリアル.tsv (object, scenario, letters, other; new (unread), broken off, complete)",
         note="the file f読了 carries the word 完了"),
    dict(id="ref-filter-bar", screen="reference screen (filter bar)", style="serif", erase="inpaint", max_size=28,
         items=[(RF + "フィルター/フィルター.gal", "Filter")],
         wording="tsv-en/チュートリアル.tsv (the filter)"),
    dict(id="ref-icon-buttons", screen="reference screen (icon buttons)", style="gothic", erase="inpainta",
         stroke=2, max_size=62,
         items=[(RF + "見る.gal", "View"), (RF + "読む.gal", "Read"), (RF + "回転.gal", "Rotate")],
         wording="part-1 scene-ref-buttons (View)", new=True,
         note="the word and the icon are drawn in one colour and overlap, so the icon cannot be kept: the picture "
              "becomes the word alone, in the icon's colour"),
    dict(id="ref-break-ribbon", screen="reference screen (corner ribbon)", style="gothic", erase="inpaint",
         mode="rotated", rotate=45, rot_box=[80, 20], rot_center=[31, 29], caps=True, stroke=0, color="#ffffff",
         mask_color=[185, 255, 185, 255, 185, 255], max_size=17,
         items=[(RF + "中断アイコン概要.gal", "BREAK")],
         wording="patch/labels-0000001E (break-off data)", new=True),
    # ==== document mode (handwriting = Ink Free) ============================================================
    dict(id="doc-buttons", screen="document mode", style="handwriting", erase="flat", max_size=26,
         items=[(D + "はい.gal", "Yes"), (D + "はいs.gal", "Yes"),
                (D + "いいえ.gal", "No"), (D + "いいえs.gal", "No"),
                (D + "キャンセル.gal", "Cancel"), (D + "キャンセルs.gal", "Cancel"),
                (D + "アルバムタグ.gal", "Album"), (D + "アルバムタグs.gal", "Album"),
                (D + "メモタグ.gal", "Memo"), (D + "メモタグs.gal", "Memo"),
                (D + "コメント管理.gal", "Edit comment"), (D + "コメント管理s.gal", "Edit comment"),
                (D + "写真削除.gal", "Delete photo"), (D + "写真削除s.gal", "Delete photo"),
                (D + "名前管理.gal", "Manage names"), (D + "名前管理s.gal", "Manage names"),
                (D + "削除.gal", "Delete"), (D + "削除s.gal", "Delete")],
         wording="tsv-en/注意.tsv (Yes / No), tsv-en/チュートリアル.tsv (Cancel, Memo)", new=True,
         note="コメント管理.gal carries the word コメント編集"),
    dict(id="doc-title", screen="document mode (paper title strip)", style="handwriting", erase="inpaint",
         items=[(D + "タイトル.gal", "Documents")],
         wording="title menu (DOCUMENTS)", new=True),
    # ==== the engine's own option menu (block-compressed -> REENC path) =====================================
    dict(id="engine-menu", screen="engine option menu", style="rounded", erase="alpha", keep_edges=True,
         items=_engine_items(),
         wording="tsv-en/システムテキスト.tsv (the right-click tooltips describing the same items)", new=True,
         note="white lettering with a per-state outline on a transparent plate; ＢＧＭ left alone (already Latin)"),
    # ==== help panels (rebuilt, not retouched: erase each cell, set the English line) ========================
    # Cambria Regular (the `serif` pick) is used for the dense panels: the gothic pick is an ultra-bold face and
    # turns into a blob at 16-18 px, which is the size these tables need.
    dict(id="help-navigator", screen="navigator right-click (mouse/key help)", style="serif", erase="flat",
         mode="lines", mask_color=[150, 255, 150, 255, 150, 255], color="#f2f2f2", max_size=19, keep_alpha=True,
         items=[(R + "チュートリアルウィンドウ.gal", None)], new=True,
         lines=[("Scroll the screen", [14, 10, 222, 38]), (": Move the mouse pointer to the screen edge", [228, 10, 674, 38]),
                ("Play a scenario", [14, 38, 222, 64]), (": Left-click a scenario node", [228, 38, 674, 64]),
                ("View a synopsis", [14, 64, 222, 92]), (": Right-click a scenario node (played scenarios only)", [228, 64, 674, 114]),
                ("Scroll the screen fast", [14, 118, 222, 146]), (": Hold the Ctrl button down", [228, 118, 674, 146]),
                ("Go to the scenario in focus", [14, 172, 318, 200]), (": Left-click an empty place", [324, 172, 674, 200]),
                ("Call Mikka Tachiki", [14, 200, 318, 228]), (": Right-click an empty place", [324, 200, 674, 228]),
                ("Shortcut to the references", [14, 246, 340, 272]), (": R button", [346, 246, 674, 272]),
                ("Shortcut to the encyclopedia", [14, 272, 340, 298]), (": D button", [346, 272, 674, 298]),
                ("Shortcut to chatter", [14, 298, 340, 324]), (": T button", [346, 298, 674, 324]),
                ("Shortcut to load", [14, 324, 340, 350]), (": L button", [346, 324, 674, 350]),
                ("Quit the game: just close the window (it autosaves)", [14, 372, 674, 404])],
         wording="tsv-en/システムテキスト.tsv (簡易1-12 describe the same operations)"),
    dict(id="help-keys", screen="engine option menu (key help)", style="serif", erase="inpaint",
         mode="lines", mask_color=[170, 255, 170, 255, 170, 255], color="#f2f2f2", max_size=20, mask_grow=7,
         items=[(E + "シナリオチュートリアル.gal", None)], new=True,
         lines=[("Left-click the screen or Enter", [14, 10, 390, 40]), (": Advance the text", [396, 10, 790, 40]),
                ("Ctrl key", [14, 40, 390, 70]), (": Fast-forward the effects and text", [396, 40, 790, 70]),
                ("Right-click the screen", [14, 70, 390, 100]), (": Show the option menu", [396, 70, 790, 100]),
                ("Space key", [14, 100, 390, 132]), (": Hide the text window", [396, 100, 790, 132]),
                ("Mouse wheel", [14, 132, 390, 164]), (": Show the text log", [396, 132, 790, 164]),
                ("Auto advance", [14, 192, 150, 220]), (": Advance the text at the speed you set", [154, 192, 790, 220]),
                ("Skip read text", [14, 220, 150, 248]), (": Fast-forward text you have already read", [154, 220, 790, 248]),
                ("Log", [14, 248, 150, 276]), (": Show the text log full screen", [154, 248, 790, 276]),
                ("Save", [14, 276, 150, 306]), (": Create break-off data for the scenario (30 max)", [154, 276, 790, 306]),
                ("Load", [14, 306, 150, 336]), (": Load break-off data for the scenario", [154, 306, 790, 336]),
                ("Move the pointer to the top edge", [14, 368, 452, 398]), (": Show the scenario information", [456, 368, 790, 398]),
                ("Left-click the scenario information", [14, 398, 452, 428]), (": Keep it on screen", [456, 398, 790, 428])],
         wording="tsv-en/システムテキスト.tsv (break-off data, text log, auto text advance)"),
    dict(id="help-chatter", screen="chatter (topic legend)", style="serif", erase="flat",
         mode="lines", mask_color=[170, 255, 170, 255, 170, 255], color="#f2f2f2", max_size=17, keep_alpha=True,
         items=[(TK + "ヘルプ.gal", None)], new=True,
         lines=[("New topic", [4, 8, 108, 30]), ("A topic you have not chosen yet", [192, 8, 668, 30]),
                ("Related topic", [4, 40, 108, 62]), ("A topic that makes other topics appear", [192, 40, 668, 62]),
                ("Conditional topic", [4, 84, 108, 130]),
                ("Choosing a particular option makes other topics appear. Once it has appeared, choosing a different option hides it again.", [192, 80, 668, 132]),
                ("Topic in season", [4, 148, 108, 192]),
                ("A topic that can no longer be chosen once you pass a certain scenario (once locked, it never appears again).", [192, 146, 668, 194]),
                ("Affection change", [4, 206, 108, 250]),
                ("Choosing a particular option raises or lowers affection. A topic turned red means affection fell, a topic turned blue means it rose.", [192, 204, 668, 252]),
                ("Affection-locked topic", [4, 264, 108, 306]), ("(none)", [116, 264, 186, 306]),
                ("A topic you can choose once affection is high enough. A topic whose condition is not met is darkened.", [192, 262, 668, 308]),
                ("• All the same, no topic unlocks until you reach a certain scenario.", [4, 320, 668, 352]),
                ("• Careful: once you pass a certain scenario, every topic you had unlocked can no longer be chosen (in that sense they are all 'topics in season').", [4, 362, 668, 414])],
         wording="GLOSSARY (a topic in season, a topic)",
         note="the icon column (新 / key / if / 旬 / heart) is left as it is: those marks stay Japanese in the game, "
              "so the legend must show the mark the player actually sees"),
    dict(id="sys-test-button", screen="system (unused test button)", style="gothic", erase="flat", max_size=26,
         items=[(S + "テスト.gal", "Test"), (S + "テストs.gal", "Test")], new=True,
         note="a test asset; translated anyway because it costs nothing if the game ever shows it"),
    # ==== Tier C, part 1: the three story pictures =========================================================
    dict(id="story-door-sign", screen="part-1 story art (door plate)", style="gothic", erase="inpaint", caps=True,
         mask_color=[0, 115, 0, 115, 0, 115], box=[110, 150, 840, 360], textbox=[130, 175, 820, 340],
         color="#101010", stroke=0, mask_grow=9,
         items=[(BG + "霊安室表札.gal", "Mortuary")],
         wording="lns-en (mortuary, 4 hits)", new=True),
    dict(id="story-end-card", screen="part-1 story art (arc end card)", style="brush", erase="inpaint", caps=True,
         mask_color=[120, 255, 0, 95, 0, 95], box=[520, 315, 790, 505], textbox=[540, 330, 770, 490],
         stroke=0, mask_grow=9,
         items=[(BG + "手直し・追加/明徴編完.gal", "END")], new=True,
         note="only the 終 mark is translated; the arc logo above it stays Japanese brush art until the owner "
              "decides on the episode logos (the two must be decided together)"),
    dict(id="story-newspaper", screen="part-1 story art (newspaper page)", style="serif", erase="inpaint",
         mode="rotated", rotate=8.5, mask_color=[0, 120, 0, 120, 0, 120], box=[30, 80, 660, 372],
         color="#141414", stroke=0, mask_grow=9,
         items=[(BG + "空撮.gal", None)], new=True,
         rot_lines=[("Body of unknown sex", [500, 58], [305, 140], 46),
                    ("found in Motoki-cho, Sawa Pref.", [486, 56], [318, 212], 44),
                    ("At around 5 a.m. in Chuo Park, Motoki-cho, Sawa Pref.,", [545, 36], [366, 270], 26),
                    ("...a body was discovered.", [380, 34], [228, 318], 26)],
         note="HEADLINE + the first paragraph. The second paragraph lower down is soft-focus and clipped by the "
              "frame in the original; re-setting it needs the photo-grade paint-out the plan reserves for Tier C "
              "(Q2443). The leading ellipsis mirrors the JP, which is cut off by the frame in the same place"),
    # ==== shatter frames (the navigator cancel button breaking up) ==========================================
    dict(id="cancel-shatter", screen="navigator (cancel shatter animation)", style="gothic", erase="maskfill",
         mode="blank", mask_color=[0, 205, 0, 205, 0, 200], keep_edges=True, mask_grow=5,
         items=[(S + "キャンセル粉砕/キャンセル粉砕2.gal", None), (S + "キャンセル粉砕/キャンセル粉砕3.gal", None),
                (S + "キャンセル粉砕/キャンセル粉砕4.gal", None)],
         note="the shards keep their shape; the Japanese fragments are painted out so no Japanese flies apart"),
]
