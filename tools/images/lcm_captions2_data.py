# -*- coding: utf-8 -*-
"""Item 5b (2026-11-03): English for the 18 used LiveCinema files (lcm-usage/USAGE.md).
JP caption -> (EN caption, source). Source "reused <file> #k" = the shipped English line of that scene, verbatim;
"fresh" = no shipped English for these words. Line breaks (CR LF) keep the role they have in the Japanese
(leading blank lines place the caption under the previous one; a long block wraps inside the Japanese width)."""
S = "　"
N = "\r\n"

RECAP = {
    # 感染 (00000488-line48 = the scene's lines)
    "古郡先輩の頭部が、" + N + "強風に持ち去られたかのように消えてしまった。":
        ("Kogori-senpai's head," + N + "as if carried off by a strong wind, disappeared.",
         "reused 00000488-0000048E / 00000EDF-00001E79 (line 'Kogori-senpai's head, as if carried off by a strong wind, disappeared.')"),
    N + "古郡先輩の……直感と同じ……？":
        (N + "Kogori-senpai's... same as her intuition...?", "reused 00000488-line48 #11"),
    N + N + "どうして私にも古郡先輩と同じ直感が……？":
        (N + N + "Why do I have the same intuition" + N + "as Kogori-senpai, too...?", "reused 00000488-line48 #12"),
    ("逃げろ……！　ここは危険だ……！　危機が" + N + "迫っている！　桜の警告……！　やっぱりあれ" + N
     + "は使ってはいけなかったんだ！　力を手にした" + N + "者は四月に死ぬ　桜の呪いだ　桜から離れるん" + N
     + "だ！　ちがうあれは事故だったんだ！　春花は" + N + "渡さない　家族に憧れていた　死神から逃れら" + N
     + "れない　魔女の呪い　私が六人殺した　違う殺" + N + "したのは俺たちだ" + N + N
     + "能面を着けて　これが荒田集落の習わし　麻薬" + N + "……？　夢見るくらいいいじゃない　誰が私を助" + N
     + "けたの？　そんなの信じない……　魔女が死神" + N + "を呼び出す　春花を助けて　茜……　死体の" + N
     + "様相にも美観を求める　"):
        ("WRAP:Run...!" + S + "It's dangerous here...!" + S + "Danger is closing in!" + S
         + "The cherry trees' warning...!" + S + "So that really should never have been used!" + S
         + "Whoever takes the power dies in April" + S + "It's the cherry trees' curse" + S
         + "Get away from the cherry trees!" + S + "No, that was an accident!" + S + "I won't hand Haruka over"
         + S + "Longed for a family" + S + "No escaping the shinigami" + S + "The witch's curse" + S
         + "I killed six people" + S + "No, the ones who killed were us"
         + "||" + "Wearing the Noh mask" + S + "This is the custom of the Arata settlement" + S + "Drugs...?" + S
         + "It's all right just to dream, isn't it?" + S + "Who saved me?" + S + "I don't believe that..." + S
         + "The witch summons the shinigami" + S + "Save Haruka" + S + "Akane..." + S
         + "Seeking beauty even in the look of a corpse" + S,
         "reused 00000488-line48 #0-#5, #7-#10 (the collage skips #6 as the Japanese does)"),
    # 放棄
    "なつみ……お前、まだ温かいな……。":
        ("Natsumi... you're still warm...", "reused 00000EAF-line74 #17-#18"),
    N + "さよなら、五島。": (N + "Goodbye, Goto.", "reused 00000366-00000376 #113"),
    N + N + "お前だけでも、生き延びてくれ……": (N + N + "You, at least, survive...", "reused 00000366-00000376 #113"),
    ("でも、私はもう考えるのをやめた。変に頭が回るの" + N + "って、苦痛でしかない。もう疲れてしまった。何が天" + N
     + "才少女よ。そんな肩書き、もうまっぴら。もう、何も" + N + "考えたくない。新村先輩の言った通りだ。みんなが" + N
     + "死んでしまったのなら、もう……どうでもいい。呪い" + N + "だというなら……もう、それでいい……。作戦は……" + N
     + "失敗だ。"):
        ("WRAP:But, I was done with thinking. Having a head that turns oddly fast is nothing but torment. "
         "I'm already worn out. Some genius girl. A title like that, I've had enough of it. "
         "Now, I don't want to think about anything. It's just as Niimura-senpai said. "
         "If everyone has died, then now... none of it matters. If it's a curse... then now, that's fine... "
         "The Operation... failed.",
         "reused 0000037D-000003FC #88-#94; FRESH: 'I'm already worn out.' (もう疲れてしまった。 is only in the recap)"),
    # 春花と魔女と死神
    "「お父さん！　私、なつみ！　どうしてこんなことに……」":
        ("\"Dad! It's me, Natsumi! How did this happen...\"", "reused 00000641-0000064C #43"),
    "しかし、春花から連絡が来ることは、" + N + "2度となかった。" + N + "1週間待っても。" + N + "1か月待っても。" + N + "1年待っても……。":
        ("But I never heard from Haruka" + N + "again." + N + "Even after waiting a week." + N
         + "Even after waiting a month." + N + "Even after waiting a year...", "reused 00000656-00000681 #87, #89-#91"),
    "「信じ……なさい……。春花ちゃんを……」":
        ("\"Trust... in... Haruka-chan...\"", "reused 00000641-0000064C #55-#56"),
    "「やっぱり女神様の予言通りだ」":
        ("\"It's just as the Goddess" + N + "predicted, after all.\"",
         "FRESH (no shipped line; 女神様 = the Goddess, 予言 = prediction per GLOSSARY)"),
    # 監視
    "私、この知らない人に殺されるの……？":
        ("Am I going to be killed by this stranger...?",
         "FRESH (the scene says 私、こんなところで死ぬの……？; style follows its shipped 'Am I going to die in a place like this...?')"),
    N + "どうして私が？": (N + "Why me?", "reused 0000020D-000002E3 #95"),
    N + N + "先輩、早くこの町から逃げて……": (N + N + "Senpai, get out of this town, quickly...", "reused 0000020D-000002E3 #96"),
    "祀耀800年4月9日　0:05　匿名" + N + "五島絵梨奈（15）" + N + "死因：頭部強打による脳挫滅だって" + N + "脳挫滅ってことは、頭がぐしゃぐしゃってことだな":
        ("WRAP:Shiyo 800, April 9" + S + "0:05" + S + "Anonymous" + N + "erina goto (15)" + N
         + "cause of death: crushing of the brain from a hard blow to the head, they say" + N
         + "crushing of the brain means her head's all smashed to mush, huh",
         "reused 0000020D-000002E3 #106-#109 (board post; lower case as shipped)"),
    # 私にできること
    "「やめろお父さん！　私だ！　春花だ！" + N + "　頼むからなつみには手を出さないでくれ！」":
        ("\"Stop it, Dad! It's me! It's Haruka!" + N + S + "I'm begging you, don't lay a hand" + N + S
         + "on Natsumi!\"",
         "reused 000004F9-00000502 #98"),
    N + N + "「やっぱりあれはお父さんだ！　死神になったお父さんだ！」":
        (N + N + "\"That was Dad after all! It's Dad, turned into a shinigami!\"",
         "reused 000004F9-00000502 #125 (the recap drops 「おい五島！」 as the Japanese does)"),
    "「命に代えても、守ってみせる」": ("\"Even if it costs my life," + N + "I'll protect you.\"", "reused 0000050E-00000515 #143"),
    # 葛藤
    ("「おばさん……春花のお父さんのこと……" + N + "　本当に……すみませんでした」" + N + N + N + "「なつみちゃん……。" + N
     + "　もう……そういう問題じゃ" + N + "　ないのよ……」"):
        ("\"Obasan... about Haruka's dad..." + N + S + "I'm truly... sorry.\"" + N + N + N + "\"Natsumi-chan..." + N
         + S + "It's... not about that" + N + S + "anymore...\"",
         "reused 00000564-0000057A #172-#173, #180-#181 (the recap drops さっき聞きました。 as the Japanese does)"),
    "「春花が……消えちゃった……」": ("\"Haruka's... gone...\"", "reused 00000F0D-00002056 #21 (recap drops 五島……)"),
    # 永劫回帰 ending
    "さあ、行こう。": ("All right," + N + "let's go.",
                      "FRESH for this card; same wording as the shipped 「さあ、行こう。」 in 00000EDF-00001DBA"),
    "永劫回帰、私はこの世界で。": ("Eternal Recurrence." + N + "I, in this world.",
                            "FRESH; 永劫回帰 = 'Eternal Recurrence' as the shipped arc name writes it (no reading: it "
                            "carries no pun; coordinator 2026-11-03); echoes the shipped 'Natsumi, I'm alive, in this "
                            "world.' (00002225 #167)"),
}

NAMES = {"古郡なつみ": "Natsumi Kogori", "五島絵梨奈": "Erina Goto", "伊勢大二郎": "Daijiro Ise", "新村夏菜": "Kana Niimura"}

UI = {
    "終": ("The End", "fresh (no shipped END card; 終 on the route-end card)"),
    "既読スキップ中": ("Skipping read text", "fresh, from the shipped menu 'Skip Read Text' + 中 (in progress)"),
    "自動送り中": ("Auto-advancing text", "fresh, from the shipped menu 'Auto Text Advance' + 中 (in progress)"),
    "右クリックで実況モード": ("Right-click for commentary mode", "shipped term 'Commentary mode' (システムテキスト)"),
    "写真数上限オーバー": ("Photo limit exceeded", "fresh; 'photo' as in the shipped album UI"),
    "新": ("New", "as the shipped pictures 'New topics'"),
    "旧": ("Old", "as the shipped pictures 'Old topics'"),
}
