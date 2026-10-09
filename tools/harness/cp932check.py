TEST = 'TEST 01 abc ABC 0123 -- em\u2014dash macrons \u0101\u012b\u016b\u0113\u014d \u014c\u014d curly \u201cquoted\u201d \u2018single\u2019 ellipsis\u2026 straight "quoted" \'single\' end.'
bad=[]
for ch in TEST:
    try: ch.encode('cp932')
    except Exception: bad.append(ch)
print("BAD:", [(c, hex(ord(c))) for c in dict.fromkeys(bad)])
# alternatives
for c in ['\u2015','\u2014','\u2212','\u301c','\uff5e','\u2026','\u201c','\u201d','\u2018','\u2019','\u00e9','\u0101']:
    try:
        e=c.encode('cp932'); print(hex(ord(c)), repr(c), "OK", e.hex())
    except Exception as ex: print(hex(ord(c)), repr(c), "FAIL")
