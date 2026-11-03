"""refnode_map.py - which English text each object-reference check point marks (data for refnode_boxes.py).

Key (ref id, point). Value: list of members, or "keep".
  (job id, line index, None)    the whole English line
  (job id, line index, "words") only these English words inside that line (a Japanese rectangle on a phrase)
  ("jp",)                       also keep the Japanese rectangle's area (photos, digits, arrows that were not re-set)
Each entry was decided by reading the Japanese inside the Japanese rectangle on work/images/png/.../rrr<ID>/0.png
and finding the English that translates it in tools/images/jobs_refdocs.py (lane 2, 2026-11-03).
Points not listed use the automatic rule (job lines whose box lies mostly inside the Japanese rectangle).
"""
MAP = {
    ("53", 2): [("jp",), ("ref53-body", 9, None)],                  # ←十三回忌 graffiti: arrow kept + "13th memorial"
    ("72", 2): [("ref72", 37, None), ("ref72", 38, None)],          # 以上のことから… / 皮をはがされて死にかけていたと推測！
    ("32", 1): [("jp",), ("ref32", 32, None)],                      # 795 11 元木高校中退
    ("32", 2): [("jp",), ("ref32", 40, None), ("ref32", 41, None)], # 英検2級合格 / 漢検準1級合格
    ("23", 1): [("jp",), ("ref23", 2, None)],                       # photos + caption 殺害された…
    ("29", 1): [("jp",), ("ref29", 2, None)],                       # photos + caption
    ("7", 1): [("ref7", 0, None), ("ref7", 1, None), ("ref7", 2, None)],
    ("13", 3): [("ref13", 37, None)],                               # 特記事項参照
    ("83", 2): [("ref83", 21, "leaving her April sickness alone too much...")],  # 四月病を放置しすぎかなあ……。
    ("17", 7): [("ref17", 26, None)],                               # signature 谷崎玲
    ("52", 3): [("ref52", 14, "How to make delicious sushi in Motoki, a town in a basin, has been our theme since our founding.")],
    ("50", 3): [("jp",), ("ref50", 10, None), ("ref50", 11, None)], # clinic + Director (doctor's name and seal kept)
    ("59", 4): [("ref59", 18, None)],                               # 1. 古郡先輩の体調を気にしている
    ("67", 1): [("ref67", 5, "and furthermore had the girls remain at the scene as decoys to arrest the culprit")],
    ("67", 2): [("ref67", 5, "Procuring equipment without my superior's permission")],   # 上長に無許可で部品備を調達
    ("81", 1): [("ref81", 13, None), ("ref81", 14, None)],          # 嫌いなもの コーヒー、辛いもの
    ("81", 3): [("ref81", 17, None), ("ref81", 18, None)],          # 特技 何事も真面目に取り組める
    ("81", 4): [("ref81", 20, "(Family talk is off-limits!)")],   # (家族の話はNG!)
    ("81", 5): [("ref81", 32, "(Never look desperate!)")],        # (絶対にがっつかないこと!)
    ("90", 1): [("ref90", 0, None), ("ref90", 1, None)],            # date + 営業部営業課 満田守
    ("90", 4): [("ref90", 13, "Today there was an entrance ceremony at a nearby elementary school")],  # 本日付近小学校で入学式
    ("90", 5): [("ref90", 17, "The passenger side was almost completely crushed, so the car has been scrapped.")],
    ("90", 6): [("ref90", 15, "so I too bear responsibility.")],  # 私自身にも責任があります。
    ("90", 7): [("ref90", 19, "I would ask that this be made known throughout the company")],  # 全社に周知していただき
    ("3", 3): [("ref3", n, None) for n in range(22, 30)],          # 賃料 / 管理費 / 契約期間 / 更新料 with values
    ("4", 1): [("ref4", 6, None)],                                  # 少女所有のスマートフォンに不可解な点が見られたため。
    ("4", 2): [("ref4", 8, "the smartphone is thought to have been broken at that time")],  # スマートフォンが破損
    ("4", 3): [("ref4", 10, "some kind of packet communication had been going on constantly")],
    ("4", 4): [("ref4", 11, "which matches the maker's specifications. In other words, this insulated alloy may have "
                "been in the pocket on its own from the start.")],
    ("4", 5): [("ref4", 12, "had been tampered with in some way")],  # 何らかの細工が施されていた
    ("4", 6): [("jp",), ("ref4", 13, None), ("ref4", 14, None)],   # photo + caption
    ("132", 1): [("ref132", 2, "('saw', not 'heard'?)")],          # (『聞こえた』じゃなくて『見えた』?)
    ("132", 3): [("ref132", 23, None)],                             # 第三の予知能力者の存在
    ("132", 5): [("ref132", 44, None)],                             # つまり、この仮説を支持する根拠が一切ない
    ("132", 6): [("ref132", 48, None)],                             # この場合、幸太郎さんが全ての元凶とも言える。
    ("132", 8): [("ref132", 58, None)],                             # まあ、戯言じゃ戯言じゃ。
    ("94", 3): [("ref94", 29, "eternally 22")],                    # 永遠の22歳
    ("94", 4): [("ref94", 29, "landmine parents")],                # 地雷保護者
    ("94", 7): [("ref94", 53, None)],                               # お見合い失敗
    ("100", 3): [("ref100", 40, "hunting")],                       # 狩り
    ("100", 4): [("ref100", 40, "parkour")],                       # パルクール
    ("141", 1): [("jp",), ("ref141", 4, None), ("ref141", 32, None)],  # comment 0003: number/date + Isedai + text
    ("143", 2): [("ref143", 8, None), ("ref143", 9, None)],         # 祀耀788年 新村栄一郎死亡
    ("143", 3): [("ref143", 15, None)],                             # 毎年一人ずつ呪殺(他殺)
    ("153", 2): [("ref153", 8, "The senpais and I are talking about going to the Arata settlement again"),
                 ("ref153", 9, "over summer vacation.")],         # 夏休みにまた、荒田集落へ行こうって先輩たちと話しています。
    ("153", 3): [("ref153", 12, "welcome-and-farewell party for Chiga-nee")],  # チガ姉の送迎会
    ("153", 4): [("ref153", 13, "I tried writing a letter!")],     # お手紙にしてみました!
    ("157", 2): [("ref157", 51, "The Comfort Suite on the top floor has an open-air bath with hot-spring water "
                  "flowing straight from the source.")],          # 最上階のコンフォートスイートには、源泉かけ流しの露天風呂。
    ("189", 1): [("ref189", 2, "so that no evidence at all leaks out.")],      # あらゆる証拠を漏らさないためだ。
    ("189", 2): [("ref189", 3, "I'll negotiate that matter.")],               # 例の件を交渉する。
    ("189", 3): [("ref189", 6, "Everything is for the two of them.")],        # 全ては2人のためだ。
    ("189", 4): [("ref189", 8, "Haruka-chan")],                                # 春花ちゃん(もまた、社会から抹殺)
    ("189", 5): [("ref189", 10, "be careful of Haruka-chan's mobile phone.")], # 春花ちゃんの携帯電話には要注意だ。
    ("189", 6): [("ref189", 13, "She won't lay a hand on our family.")],      # 俺たち家族に手を出すことはしないだろう。
    ("189", 7): [("ref189", 16, "have her spend the time with Haruka-chan, just the two of them.")],
    ("189", 8): [("ref189", 17, "Do it carefully")],                          # 慎重にやってくれ。
    ("239", 6): [("ref239", 7, None)],                              # 一、命落とすことなかれ
    ("239", 7): [("ref239", 8, None)],                              # 一、硫黄の湯を活用せよ
    ("239", 8): [("ref239", 9, None)],                              # 一、人に会うべからず
    ("239", 9): [("ref239", 10, None)],                             # 一、無駄に獣狩るべからず
    ("239", 10): [("ref239", 11, None)],                            # 一、糸姫山の異変を感じたらすぐに下山し皆に知らせよ
    ("240", 1): [("ref240", 1, "She holds the cherry branch in order to bring out the witch's power.")],
    ("240", 2): [("ref240", 1, "As soon as the thirteenth-year memorial service is over, capture the witch without delay.")],
    ("240", 3): [("ref240", 8, None)],                              # 閲覧後、南の家に回すこと
    ("240", 4): [("ref240", 10, "southermost")],                   # 再南 (picture spells "southermost")
    ("241", 3): [("obj241-0", 94, "This hospital has already established that it is a drug similar to ephedrine.")],
    ("241", 6): [("obj241-0", 109, "(most likely mold or bacteria, but the details are unknown)")],
    ("250", 1): [("obj250-0", 0, "Sakura, thank you for everything up to now.")],   # サクラ、今までありがとう。
    ("250", 2): [("obj250-0", 4, "I'm leaving Arata Station at 8 this"), ("obj250-0", 5, "morning,")],  # 今日の朝8時には荒田駅を出る
    ("250", 3): [("obj250-0", 7, "Even if you stay with"), ("obj250-0", 8, "me, I'll surely just be a burden.")],
    ("250", 4): [("obj250-0", 10, "Please, Sakura, be happy too.")],  # サクラも幸せになって。
    ("258", 3): [("obj258-0", 36, "(he asked for it himself)")],     # (自分から願い出た)
    ("258", 4): [("obj258-0", 37, "(the residents' doing?)")],       # (住人たちの仕業?)
    ("258", 5): [("obj258-0", 11, None)],                           # つまり、茅萱さんは殺していない可能性もある。
    ("258", 9): [("obj258-0", 30, "such a fatal difference as a knife versus a blunt weapon...")],
    ("258", 10): [("obj258-0", 32, None)],                          # さーて!明日は料亭でごちそう食べるぞー!
    ("259", 1): [("obj259-0", 8, "Droga apparently has been made since hundreds of years"), ("obj259-0", 9, "ago.")],
    ("259", 2): [("obj259-0", 12, None), ("obj259-0", 13, None)],
    ("259", 3): [("obj259-0", n, None) for n in range(37, 41)],    # the four listed phenomena
    ("315", 2): [("obj315-0", 2, "changed my"), ("obj315-0", 3, "eye color,")],   # 目の色が変わり
    ("315", 3): [("obj315-0", 10, "and if it really happened, I'd"), ("obj315-0", 11, "panic.")],  # 本当に起きたらパニックになっちゃうよ。
    ("315", 5): [("obj315-0", 23, "does that mean I could recognize who it")],     # 相手を認識できたってことになるのかな?
    ("315", 6): [("obj315-0", 27, None)],
    ("315", 7): [("obj315-0", 36, None)],                           # ふむ……ちょっときな臭いね……。
    # reflowed full-page memos (refdoc_memo.flow): one English paragraph per Japanese paragraph
    ("61", 1): [("ref61", 2, None)],                                # ・私たちの携帯にはフレンドGPS機能がある
    ("61", 2): [("ref61", 5, None)],                                # しかし、もし犯人が知ることのできる情報が…狂言をするとか。
    ("61", 3): [("ref61", 8, None)],                                # 古郡先輩のお父さんが盗聴器を仕込んだ!!
    ("61", 4): [("ref61", 24, None)],                               # 1. 神隠し的犯行の手法とは?…
    ("61", 5): [("ref61", 27, None)],                               # 新村先輩のお母さんに協力者がいる可能性(おそらく黒幕)…
    ("62", 1): [("ref62", 5, None), ("ref62", 6, None)],            # ・紙人形が出てくるのが遅い / 女ケ沢市事件の時は…
    ("62", 2): [("ref62", 8, None)],                                # しかし、盗聴器が仕込まれていた。…
    ("62", 3): [("ref62", 15, None)],                               # だとしたら、2人同時殺すか、手を出さないかのどちらか。…
    ("62", 4): [("ref62", 19, None)],                               # となると、ターゲットは別にいたはず。…
    ("59", 6): [("ref59", 26, "It's all right! Leave it to the genius girl, Erina Goto!")],  # 大丈夫!天才少女、五島絵梨奈にお任せ!
    ("239", 2): [("ref239", 3, None)],                              # 一、一人で生き残れ
}
