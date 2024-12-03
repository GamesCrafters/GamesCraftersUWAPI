"""
===== STEP 1 ===== 
Create a function that returns Image AutoGUI Data for your game, given a variant of that game.
Return None if there is no Image AutoGUI Data for the given variant.

get_<game>(variant_id) should return JSON of the following form:

    {
        "defaultTheme": <name of default theme>,
        "themes": {
            <name of theme1>: {
                "space": [<width>, <height>],
                "centers": [ [<x0>,<y0>], [<x1>, <y1>], [<x2>, <y2>], [<x3>, <y3>], ... ],
                "background": <optional, path to background image>,
                "foreground": <optional, path to foreground image>,
                "charImages": {
                    <char1>: {"image": <path to image corresponding to char1>, "scale": <image scale>},
                    <char2>: { ... }
                    ...
                },
                "circleButtonRadius": <optional, radius of all default circle move buttons>,
                "lineWidth": <optional, width of all line move buttons>,
                "arrowWidth": <optional, width of all arrow move buttons>,
                "entitiesOverArrows": <optional, Boolean, whether entities are drawn over arrows>,
                "textEntityFontSize": <optional, font size of all text entities>,
                "textButtonFontSize": <optional, font size of all text move buttons>,
                "sounds": <optional> {
                    <char1>: <string, path to sound file>,
                    <char2>:
                },
                "animationType": <optional, string, animation type>,
                "defaultAnimationWindow": [start, end] <optional>
            },
            <name of theme2>: {
                ...
            },
            ...
        },
        "ambience": <optional, path to sound file>,
    }

(Scroll all the way down for Step 2).

"""

def get_0to10by1or2(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [9, 11],
                "centers": [[4.5, 0.5 + i] for i in range(10, -1, -1)],
                "background": "0to10by1or2/grid.svg",
                "charImages": {
                    "x": {"image": "0to10by1or2/x.svg", "scale": "1"}
                },
                "arrowWidth": 0.1,
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_1dchess(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [8, 1],
                "centers": [[0.5 + i, 0.5] for i in range(8)],
                "background": "1dchess/grid.svg",
                "charImages": {
                    "K": {"image": "chess/wikipedia/K.svg", "scale": 1},
                    "N": {"image": "chess/wikipedia/N.svg", "scale": 1},
                    "R": {"image": "chess/wikipedia/R.svg", "scale": 1},
                    "k": {"image": "chess/wikipedia/kk.svg", "scale": 1},
                    "n": {"image": "chess/wikipedia/nn.svg", "scale": 1},
                    "r": {"image": "chess/wikipedia/rr.svg", "scale": 1},
                },
                "arrowWidth": 0.1,
                "entitiesOverArrows": False,
                "sounds": {
                    "x": "general/slide.mp3",
                    "y": "general/slideThenRemove.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_3spot(variant_id):
    char_images = {
        "R": {"image": "3spot/R.svg", "scale": 1.0},
        "W": {"image": "3spot/W.svg", "scale": 1.0},
        "B": {"image": "3spot/B.svg", "scale": 1.0},
        "h": {"image": "3spot/h.svg", "scale": 0.3},
        "v": {"image": "3spot/v.svg", "scale": 0.3},
    }
    char_images.update({f"{i}": {"image": f"general/{i}.svg", "scale": 2} for i in range(10)})
    centers = [
        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [0.5, 1.5], [1.5, 1.5],
        [2.5, 1.5], [0.5, 2.5], [1.5, 2.5], [2.5, 2.5],
        [0.35, 3.5], [0.65, 3.5], [2.35, 3.5], [2.65, 3.5], [-99, -99],
        [1, 0.5], [2, 0.5], [0.5, 1], [1.5, 1], [2.5, 1], [1, 1.5],
        [2, 1.5], [0.5, 2], [1.5, 2], [2.5, 2], [1, 2.5], [2, 2.5]
    ]
    centers = [[x + 0.0125, y + 0.0125] for x, y in centers] # need to adjust b/c of stroke width
    return {
        "defaultTheme": "standard",
        "themes": {
            "standard": {
                "space": [3.025, 4],
                "centers": centers,
                "background": "3spot/grid.svg",
                "charImages": char_images,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_achi(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [100, 100],
                "centers": [[i % 3 * 40 + 10, i // 3 * 40 + 10] for i in range(9)],
                "background": "achi/board.svg",
                "charImages": {
                    "x": {"image": "general/blackpiece.svg", "scale": 15},
                    "o": {"image": "general/whitepiece.svg", "scale": 15}
                },
                "circleButtonRadius": 6.5,
                "arrowWidth": 4,
                "entitiesOverArrows": True,
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/slide.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_adugo(variant_id):
    def adugo_iadata(dim):
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [dim * 10, dim * 10],
                    "background": f"adugo/grid{dim}x{dim}.svg",
                    "centers": [[100, 100]] + [
                        [i % dim * 10 + 5, i // dim * 10 + 5] for i in range(dim * dim)
                    ],
                    "charImages": {
                        "B": {"image": "general/blackpiece.svg", "scale": 9},
                        "W": {"image": "general/whitepiece.svg", "scale": 9}
                    },
                    "animationType": "simpleSlides",
                    "defaultAnimationWindow": [1, 27]
                }
            }
        }

    if variant_id in ("3x3", "5x5"):
        return adugo_iadata(int(variant_id[0]))
    return None

def get_allqueenschess(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [5, 5],
                "centers": [[i % 5 + 0.5, i // 5 + 0.5] for i in range(25)],
                "background": "allqueenschess/board.svg",
                "charImages": {
                    "W": {"image": "chess/wikipedia/Q.svg", "scale": 1},
                    "B": {"image": "chess/wikipedia/qq.svg", "scale": 1}
                },
                "entitiesOverArrows": True,
                "arrowWidth": 0.06,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_baghchal(variant_id):
    char_images = {f"{i}": {"image": f"general/{i}.svg", "scale": 1.2} for i in range(10)}
    char_images["G"] = {"image": "baghchal/G.svg", "scale": 0.7}
    char_images["T"] = {"image": "baghchal/T.svg", "scale": 0.75}
    
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [5, 6],
                "centers": [[0.5 + (i % 5), 0.5 + (i // 5)] for i in range(25)] + [[3.75,5.2], [3.95,5.2], [3.75,5.55], [3.95,5.55]],
                "background": "baghchal/grid5Diag.svg",
                "charImages": char_images,
                "arrowWidth": 0.05,
                "entitiesOverArrows": True,
                "sounds": {
                    "g": "animals/goat.mp3",
                    "t": "animals/tiger.mp3"
                },
                "animationType": "simpleSlides",
                "defaultAnimationWindow": [0, 25]
            }
        }
    }

def get_beeline(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [240, 144],
                "centers": [
                    [30, 71.9], [60, 54.6], [90, 37,3], [120, 20],
                    [60, 89.2], [90, 71.9], [120, 54.6], [150, 37.3],
                    [90, 106.5], [120, 89.2], [150, 71.9], [180, 54.6],
                    [120, 123.8], [150, 106.5], [180, 89.2], [210, 71.9]
                ],
                "background": "beeline/board.svg",
                "charImages": {
                    "W": {"image": "beeline/W.svg", "scale": 34.5},
                    "B": {"image": "beeline/B.svg", "scale": 34.5}
                },
                "arrowWidth": 2,
                "entitiesOverArrows": True,
                "sounds": {"b": "animals/bee.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_bishoppuzzle(variant_id):
    rows = int(variant_id[0])
    cols = int(variant_id[2])
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [cols, rows],
                "centers": [[0.5 + i // rows, 0.5 + i % rows] for i in range(rows * cols)],
                "background": f"bishoppuzzle/{variant_id}.svg",
                "charImages": {
                    "X": {"image": "chess/wikipedia/B.svg", "scale": 1},
                    "O": {"image": "chess/wikipedia/bb.svg", "scale": 1},
                },
                "entitiesOverArrows": True,
                "arrowWidth": 0.1,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_change(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [80, 80],
                "centers": [
                    [70, 26], [70, 44], [70, 62], [50, 17], [50, 35], [50, 53], [50, 71],
                    [30, 8], [30, 26], [30, 44], [30, 62], [10, 17], [10, 35], [10, 53]
                ],
                "background": "change/graph.svg",
                "charImages": {
                    "o": {"image": "general/redpiece.svg", "scale": 10},
                    "x": {"image": "general/bluepiece.svg", "scale": 10}
                },
                "arrowWidth": 1,
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_chess(variant_id):
    pieces = {
        "K": "K", "Q": "Q", "R": "R", "B": "B", "N": "N", 
        "P": "P", "k": "kk", "q": "qq", "r": "rr", 
        "b": "bb", "n": "nn", "p": "pp"
    }
    return {
        "defaultTheme": "Wikipedia",
        "themes": {
            t: {
                "space": [8, 8],
                "arrowWidth": 0.1,
                "background": f"chess/{l}/grid.svg",
                "centers": [[i % 8 + 0.5, i // 8 + 0.5] for i in range(64)],
                "charImages": {
                    p: {"image": f"chess/{l}/{pieces[p]}.svg", "scale": 1} for p in pieces
                },
                "sounds": {
                    "x": "general/slide.mp3",
                    "y": "general/slideThenRemove.mp3"
                },
                "animationType": "simpleSlides"
            } for t, l in (("Wikipedia", "wikipedia"), ("Lichess", "lichess"))
        }
    }

def get_chinesechess(variant_id):
    pieces = {
        "K": "general_r", "A": "advisor_r", "R": "chariot_r", "B": "elephant_r", "N": "horse_r",
        "P": "soldier_r", "Q": "soldier_r", "C":"cannon_r", "k": "general_b", "a": "advisor_b",
        "r": "chariot_b", "b": "elephant_b", "n": "horse_b", "p": "soldier_b", "q": "soldier_b", 
        "c":"cannon_b"
    }
    
    theme = {
        "space": [9, 10],
        "centers": [[i % 9 + 0.5, i // 9 + 0.5] for i in range(90)],
        "background": "chinesechess/board.svg",
        "arrowWidth": 0.1,
        "sounds": {
            "x": "general/slide.mp3",
            "y": "general/slideThenRemove.mp3"
        },
        "animationType": "simpleSlides"
    }
    
    return {
        "defaultTheme": "regular",
        "themes": {
            t: {
                "charImages": {
                    p: {"image": f"chinesechess/{t}/{pieces[p]}.svg", "scale": 1} for p in pieces
                }
            } | theme for t in ("regular", "graphical")
        }
    }

def get_chomp(variant_id):
    rows, cols = variant_id.split('x')
    rows, cols = int(rows), int(cols)
    return {
        "defaultTheme": "choco",
        "themes": {
            "choco": {
                "space": [cols, rows],
                "centers": [[i % cols + 0.5,rows - (i // cols) - 0.5] for i in range(rows * cols)],
                "charImages": {
                    "x" : {"image": "chomp/x.svg", "scale": 1.01},
                    "p" : {"image": "chomp/p.svg", "scale": 1.01},
                    "t" : {"image": "general/basichitbox.svg", "scale": 1}
                },
                "sounds": {"x": "chomp/chomp.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_chopsticks(variant_id):
    ctrorig = [[25.5, 22.5], [28.5, 18.5], [27, 14.5], [24.5, 10.5]]
    ctrs = ctrorig + [[x, 100 - y] for x, y in ctrorig] + [[100 - x, 100 - y] for x, y in ctrorig] + \
        [[100 - x, y] for x, y in ctrorig] # finger centers (16)
    
    x, y = 42, 17
    ctrs += [[x, y], [x, 100 - y], [100 - x, 100 - y], [100 - x, y]] # Straight-line attack arrow endpoints (4)

    x,y = 39, 28
    ctrs += [[x, y], [x, 100 - y], [100 - x, 100 - y], [100 - x, y]] # Diagonal-line attack arrow endpoints (4)

    ctrs += [[x, 50] for x in [ # Transfer move button centers (18)
        5,12,19,26,33,8.5,15.5,22.5,29.5, 95,88,81,74,67,91.5,84.5,77.5,70.5]]

    char_images = {c : {"image": f"chopsticks/{c}.svg", "scale": 100} for c in '678901234'}

    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100],
                "centers": ctrs,
                "background": "chopsticks/knuckles.svg",
                "foreground": "chopsticks/foreground.svg",
                "charImages": char_images | {"f" : {"image": "chopsticks/finger.svg", "scale": 100}},
                "arrowWidth": 1,
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_chungtoi(variant_id):
    gridctrs = [[i % 3 + 0.5, i // 3 + 0.5] for i in range(9)]
    ctrs = gridctrs + [[-99, -99]]
    ctrs += [[x - 0.2, y] for x, y in gridctrs]
    ctrs += [[x + 0.2, y] for x, y in gridctrs]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [3, 3],
                "centers": ctrs,
                "background": "chungtoi/grid.svg",
                "charImages": {
                    "T": {"image": "chungtoi/T.svg", "scale": 1.28},
                    "X": {"image": "chungtoi/X.svg", "scale": 1.28},
                    "t": {"image": "chungtoi/tt.svg", "scale": 1.28},
                    "x": {"image": "chungtoi/xx.svg", "scale": 1.28},
                    "p": {"image": "chungtoi/p.svg", "scale": 0.4},
                    "q": {"image": "chungtoi/q.svg", "scale": 0.4},
                    "r": {"image": "chungtoi/rotate.svg", "scale": 1.2},
                },
                "arrowWidth": 0.04,
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3",
                    "z": "general/slide.mp3"
                },
                "animationType": "simpleSlides",
                "defaultAnimationWindow": [0, 9]
            }
        }
    }

def get_connect4(variant_id):
    def get_theme(cols):
        centers = [[0.5 + i // 6, 1.5 + i % 6] for i in range(cols * 6)]
        return {
            "defaultTheme": "normal",
            "themes": {
                "normal": {
                    "space": [cols, 7],
                    "centers": centers + [[i % cols + 0.5, i // cols] for i in range(cols * 2)],
                    "foreground": f"connect4/foreground6x{cols}.svg",
                    "charImages": {
                        "X": {"image": "general/blue_circle.svg", "scale": 1},
                        "O": {"image": "general/red_circle.svg", "scale": 1},
                    },
                    "arrowWidth": 0.13,
                    "sounds": {"x": "general/remove.mp3"},
                    "animationType": "entityFade"
                }
            }
        }
    if variant_id == "6x6":
        return get_theme(6)
    elif variant_id == "6x7":
        return get_theme(7)
    return None

def get_dao(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [4, 4],
                "centers": [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)],
                "background": "dao/grid.svg",
                "charImages": {
                    "O": {"image": "dao/W.svg", "scale": 0.9},
                    "X": {"image": "dao/B.svg", "scale": 0.9}
                },
                "arrowWidth": 0.1,
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_dawsonschess(variant_id):
    size = int(variant_id)
    char_images = {"t": {"image": "general/basichitbox.svg", "scale": 44}} | {
        e: {"image": f"dawsonschess/{e}.svg", "scale": 45} for e in 'bx'}
    return {
        "defaultTheme": "kings",
        "themes": {
            "kings": {
                "space": [45 + (size - 1) * 44, 45],
                "centers": [[22.5 + i * 44, 22.5] for i in range(size)],
                "charImages": char_images,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_dinododgem(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [6, 6],
                "centers": [[i // 5 + 0.5, 5.5 - (i % 5)] for i in range(25)] +[
                    [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], [4.5, 0.5], 
                    [5.5, 1.5], [5.5, 2.5], [5.5, 3.5], [5.5, 4.5]
                ],
                "background": "dinododgem/grid.svg",
                "charImages": {
                    "o": {"image": "dinododgem/purple.svg", "scale": 0.9},
                    "x": {"image": "dinododgem/triceratops.svg", "scale": 0.9}
                },
                "arrowWidth": 0.09,
                "entitiesOverArrows": True,
                "sounds": {
                    "x": "animals/tiger.mp3",
                    "y": "animals/dragon.mp3"  
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_dodgem(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [4, 4],
                "centers": [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)],
                "background": "dodgem/grid.svg",
                "charImages": {
                    "o": {"image": "general/bluepiece.svg", "scale": 1}, 
                    "x": {"image": "general/redpiece.svg", "scale": 1}
                },
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_domineering(variant_id):
    scale, p = 1, 1
    sL = int(variant_id) # sideLength

    if sL == 4:
        scale, p = 24.625, 13.0625
    elif sL == 5:
        scale, p = 19.76, 10.48
    else:
        scale, p = 16.5, 8.75
    
    q = p + scale / 2
    centers = [[i % sL * scale + p, i // sL * scale + p] for i in range(sL * sL)]
    centers += [[i % (sL - 1) * scale + q, i // (sL - 1) * scale +p] for i in range(sL * (sL - 1))]
    centers += [[i % sL * scale + p, i // sL * scale + q] for i in range(sL * (sL - 1))]

    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100],
                "centers": centers,
                "background": f"domineering/{variant_id}.svg",
                "charImages": {
                    "u": {"image": "domineering/u.svg", "scale": scale * 1.1},
                    "d": {"image": "domineering/d.svg", "scale": scale * 1.1},
                    "l": {"image": "domineering/l.svg", "scale": scale * 1.1},
                    "r": {"image": "domineering/r.svg", "scale": scale * 1.1},
                    "h": {"image": "3spot/h.svg", "scale": scale / 2.5}, 
                    "v": {"image": "3spot/v.svg", "scale": scale / 2.5}, 
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_dragonsandswans(variant_id):
    char_images = {
        "x": {"image": "swans/D.svg", "scale": 8}, 
        "o": {"image": "swans/o.svg", "scale": 6},
        "s": {"image": "swans/s.svg", "scale": 6}
    }
    char_images |= {c: {"image": f"general/{c}.svg", "scale": 8.8} for c in '0123456789'}
    centers = [[i % 4 * 10 + 5, i // 4 * 10 + 5] for i in range(16)]
    centers += [[28.7, 43], [30.2, 43], [28.7, 46], [30.2, 46]]
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [40, 50],
                "centers": centers,
                "background": "swans/grid4.svg",
                "charImages": char_images,
                "entitiesOverArrows": True,
                "sounds": {
                    "x": "animals/dragon.mp3",
                    "o": "animals/swan.mp3"
                },
                "animationType": "simpleSlides",
                "defaultAnimationWindow": [0, 16]
            }
        }
    }

def get_dshogi(variant_id):
    board = [[100 + x * 100, 100 + y * 100] for y in range(4) for x in range(3)]
    forest_captured = [[425, 450], [550, 450], [485, 325]]
    sky_captured = [[550, 51], [425, 51], [485, 175]]
    giraffe_placement = [[100 + x * 100, 75 + y * 100] for y in range(4) for x in range(3)]
    elephant_placement = [[75 + x * 100, 125 + y * 100] for y in range(4) for x in range(3)]
    chick_placement = [[125 + x * 100, 125 + y * 100] for y in range(4) for x in range(3)]
    centers = board + forest_captured + sky_captured + giraffe_placement + \
              elephant_placement + chick_placement
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [601, 501],
                "centers": centers,
                "background": "dshogi/background.svg",
                "charImages": {
                    "a": {"image": "dshogi/a.svg", "scale": 100},
                    "A": {"image": "dshogi/A.svg", "scale": 100},
                    "b": {"image": "dshogi/b.svg", "scale": 100},
                    "B": {"image": "dshogi/B.svg", "scale": 100},
                    "c": {"image": "dshogi/c.svg", "scale": 100},
                    "C": {"image": "dshogi/C.svg", "scale": 100},
                    "d": {"image": "dshogi/d.svg", "scale": 100},
                    "D": {"image": "dshogi/D.svg", "scale": 100},
                    "e": {"image": "dshogi/e.svg", "scale": 100},
                    "E": {"image": "dshogi/E.svg", "scale": 100},
                    "g": {"image": "dshogi/g.svg", "scale": 100},
                    "G": {"image": "dshogi/G.svg", "scale": 100},
                    "h": {"image": "dshogi/h.svg", "scale": 100},
                    "H": {"image": "dshogi/H.svg", "scale": 100},
                    "l": {"image": "dshogi/l.svg", "scale": 100},
                    "L": {"image": "dshogi/L.svg", "scale": 100},
                    "0": {"image": "dshogi/GG.svg", "scale": 50},
                    "1": {"image": "dshogi/EE.svg", "scale": 50},
                    "2": {"image": "dshogi/CC.svg", "scale": 50},
                },
                "arrowWidth": 2,
                "sounds": {
                    "x": "general/slide.mp3",
                    "y": "general/place.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_euclidsgame(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [10, 10],
                "background": "euclidsgame/grid.svg",
                "centers": [[i % 10 + 0.5, i // 10 + 0.5] for i in range(100)],
                "charImages": {
                    "X": {"image": "euclidsgame/cut.svg", "scale": 0.9},
                    "h": {"image": "euclidsgame/h.svg", "scale": 1}
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade",
                "defaultAnimationWindow": [0, 100]
            }
        }
    }

def get_fivefieldkono(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [200, 200],
                "centers": [[i % 5 * 40 + 20, i // 5 * 40 + 20] for i in range(25)],
                "background": "fivefieldkono/board.svg",
                "charImages": {
                    "x": {"image": "general/whitepiece.svg", "scale": 25},
                    "o": {"image": "general/blackpiece.svg", "scale": 25}
                },
                "arrowWidth": 5,
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_fourfieldkono(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [4, 4],
                "centers": [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)],
                "background": "fourfieldkono/4fk.svg",
                "charImages": {
                    "x": {"image": "general/whitepiece.svg", "scale": 0.9},
                    "o": {"image": "general/blackpiece.svg", "scale": 0.9}
                },
                "arrowWidth": 0.08,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_forestfox(variant_id):
    pieces = {
        "a": "bell1", "b": "bell2", "c": "bell3", "d": "bell4", "e": "bell5", "f": "key1",
        "g": "key2", "h":"key3", "i": "key4", "j": "key5", "k": "moon1", "l": "moon2",
        "m": "moon3", "n": "moon4", "o": "moon5"
    }
    nums = {str(n): {"image": f"general/{n}.svg", "scale": 450} for n in range(8)}
    char_images = {p: {"image": f"forestfox/{pieces[p]}.svg", "scale": 200} for p in pieces}
    char_images = char_images | {"z": {"image": "forestfox/button.svg", "scale": 350}}
    handcenters = [[i % 7 * 150 + 125, i // 7 * 600 + 150] for i in range(14)]
    centers = handcenters + [[575, 450], [200, 450], [950, 450], [425, 450], [725, 450]]
    centers += [[x, y + 80] for x, y in handcenters]
    # decree card, first card, second card, 1st score, 2nd score
        
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [1150, 900],
                "centers": centers,
                "background": "forestfox/cardboard.svg",
                "charImages": nums | char_images,
                "circleButtonRadius": 16,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_foxandhounds(variant_id):
    return {
        "defaultTheme": "lichess",
        "themes": {
            "lichess": {
                "space": [8, 8],
                "centers": [
                    [i % 8 + 0.5, i // 8 + 0.5] for i in 
                    (1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30,
                     33, 35, 37, 39, 40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62)
                ],
                "background": "chess/lichess/grid.svg",
                "charImages": {
                    "F": {"image": "foxandhounds/F.svg", "scale": 1},
                    "G": {"image": "foxandhounds/G.svg", "scale": 1},
                },
                "arrowWidth": 0.1,
                "entitiesOverArrows": True,
                "sounds": {
                    "f": "animals/fox.mp3",
                    "h": "animals/dog.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_ghost(variant_id):
    centers = [[12.5, 2.63]]
    centers += [[i % 7 * 2.5 + 5, i // 7 * 2.5 + 8.5] for i in range(21)] # First 21 letter buttons
    centers += [[7.5 + 2.5 * i, 16] for i in range(5)] # Last 5 letter buttons
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [25, 25],
                "background": "ghost/gray_background.svg",
                "centers": centers,
                "charImages": {}, # We only use text entities and move buttons.
                "textEntityFontSize": 1.2,
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_graphgame(variant_id):
    centers, space, arrowWidth, scale, img = None, None, None, None, None
    if variant_id == "0":
        centers = [[50, 94.588], [59, 79], [41, 79], [59, 61], [41, 61], [59, 43], [41, 43], 
          [59, 25], [41, 25], [59, 7], [41, 7]]
        space = [100, 100]
        arrowWidth = 0.8
        scale = 5
        img = 'P'
    elif variant_id == "1":
        centers = [[70,5], [83,5], [83,15], [70,15], [83,25], [70,25], [70,35],[83,35],
                [70,45],[83,45],[70,55],[83,55], [50,65], [40, 65], [60,55], [40, 55],
                [20,75], [40,75], [25,85], [8,55], [23,55]]
        space = [90, 90]
        arrowWidth = 0.5
        scale = 4
        img = 'pp'
    else:
        space = [100, 100]
        centers = [[41,14],[32,31],[50,31],[14,50],[32,50],[68,50],[86,50],[14,68],[32,68],
                   [50,68],[68,68],[86,68],[14,86],[32,86],[50,86],[68,86]]
        arrowWidth = 0.8
        scale = 5
        img = 'P'
    
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": space,
                "background": f"graphgame/graph{variant_id}.svg",
                "centers": centers,
                "charImages": {
                    "x": {"image": f"chess/wikipedia/{img}.svg", "scale": scale}
                },
                "arrowWidth": arrowWidth,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_towersofhanoi(variant_id):
    num_poles = int(variant_id[0])
    num_disks = int(variant_id[-1])
    width = (num_poles * 4) * (num_disks + 2)
    x_offset, x_step = width // (num_poles * 2), width // num_poles
    y_offset, y_step = 4 + width // 2, 4

    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [width, width],
                "centers": [
                    [x_offset + x * x_step, y_offset + y * y_step] 
                    for y in range(num_disks) for x in range(num_poles)],
                "background": f"towersofhanoi/z{num_poles}_{num_disks}.svg",
                "charImages": {
                    c: {"image": f"towersofhanoi/{c}.svg", "scale": 40} for c in 'ABCDEFGH'
                },
                "arrowWidth": 1,
                "sounds": {"x": "general/slideThenRemove.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_hareandhounds(variant_id):
    def hareandhounds_iadata(name, width, num_width):
        main_centers = [[40 * i + 50, 40 * j + 10] for i in range(num_width) for j in range(3)]
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [width, 100],
                    "centers": [[10, 50]] + main_centers + [[width - 10, 50]],
                    "background": f"hareandhounds/board{name}.svg",
                    "charImages": {
                        "d": {"image": "hareandhounds/d.svg", "scale": 20},
                        "r": {"image": "hareandhounds/r.svg", "scale": 20}
                    },
                    "arrowWidth": 2,
                    "entitiesOverArrows": True,
                    "sounds": {
                        "r": "animals/bunny.mp3",
                        "d": "animals/dog.mp3"
                    },
                    "animationType": "simpleSlides"
                }
            }
        }

    if variant_id == "s-hounds-first" or variant_id == "s-hare-first":
        return hareandhounds_iadata('small', 180, 3)
    elif variant_id == "m-hounds-first" or variant_id == "m-hare-first":
        return hareandhounds_iadata('medium', 260, 5)
    elif variant_id == "l-hounds-first" or variant_id == "l-hare-first":
        return hareandhounds_iadata('large', 340, 7)
    return None

def get_jan(variant_id):
    return {
        "defaultTheme": "default",
        "themes": {
            "default": {
                "space": [800, 800],
                "centers": [ [((i % 4) * 200) + 100, ((i // 4) * 200) + 100] for i in range(16)],
                "background": "jan/board.svg",
            "charImages": {
                    "b": {"image": "general/blackpiece.svg", "scale": 125},
                    "w": {"image": "general/whitepiece.svg", "scale": 125},
                },
                "circleButtonRadius": 6.5,
                "arrowWidth": 25,
                "entitiesOverArrows": True,
                "sounds": {
                    "s": "general/slide.mp3",
                },
                "animationType": "simpleSlides",
            }
        }
    }

def get_jenga(variant_id):
    return {
        "defaultTheme": "simple",
        "themes": {
            "simple": {
                "space": [6, 12], 
                "centers": [             [3.5, 11.5], [4.5, 11.5], [5.5, 11.5], 
                            [0.5, 10.5], [1.5, 10.5], [2.5, 10.5],   
                                            [3.5, 9.5], [4.5, 9.5], [5.5, 9.5], 
                            [0.5, 8.5], [1.5, 8.5], [2.5, 8.5],   
                                            [3.5, 7.5], [4.5, 7.5], [5.5, 7.5], 
                            [0.5, 6.5], [1.5, 6.5], [2.5, 6.5],                                    
                                            [3.5, 5.5], [4.5, 5.5], [5.5, 5.5], 
                            [0.5, 4.5], [1.5, 4.5], [2.5, 4.5], 
                                            [3.5, 3.5], [4.5, 3.5], [5.5, 3.5], 
                            [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], 
                                            [3.5, 1.5], [4.5, 1.5], [5.5, 1.5], 
                            [0.5, 0.5], [1.5, 0.5], [2.5, 0.5]],
                "background": "jenga/JengaBoard.svg",
                "charImages": { 
                    "J": {"image": "jenga/JengaPiece.svg", "scale": 0.9875},
                    "h": {"image": "general/basichitbox.svg", "scale": 0.9875}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_joust(variant_id):
    if variant_id not in ("4x4", "5x4"):
        return None
    r = int(variant_id[0])
    c = int(variant_id[2])
    d = max(r,c)
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [d, d],
                "background": f"joust/grid{variant_id}.svg",
                "centers": [[(i % c) + (1+d-c)/2, (i // c) + (1+d-r)/2] for i in range(r * c)],
                "charImages": {
                    "X": {"image": "chess/wikipedia/N.svg", "scale": 1},
                    "O": {"image": "chess/wikipedia/nn.svg", "scale": 1},
                    "B": {"image": "joust/B.svg", "scale": 1.005},
                },
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }
    
def get_kayles(variant_id):
    size = int(variant_id)
    if size == 1:
        centers = [[1, 0.9], [1, 1.6]]
    else:
        y = size / 2
        centers = [[0.5 + i, y] for i in range(size)] + [[0.5 + i, y + 0.7] for i in range(size)] \
        + [[0.75 + i, y + 0.7] for i in range(size)] + [[1.25 + i, y + 0.7] for i in range(size)]
    return {
        "ambience": "kayles/ambience.mp3",
        "defaultTheme": "kings",
        "themes": {
            "kings": {
                "space": [max(size, 2), max(size, 2)],
                "centers": centers,
                "background": "kayles/grid.svg",
                "charImages": {
                    "x": {"image": "kayles/x.svg", "scale": 1}
                },
                "circleButtonRadius": 0.12,
                "lineWidth": 0.1,
                "sounds": {"x": "kayles/strike.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_konane(variant_id):
    def konane_iadata(rows, cols):
        rc = rows * cols
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [cols * 10, rows * 10],
                    "background": f"konane/grid{rows}x{cols}.svg",
                    "centers": [[i % cols * 10 + 5, i // cols * 10 + 5] for i in range(rc)],
                    "charImages": {
                        "x": {"image": "general/whitepiece.svg", "scale": 9},
                        "o": {"image": "general/blackpiece.svg", "scale": 9},
                        "h": {"image": "general/basichitbox.svg", "scale": 10}
                    },
                    "sounds": {"x": "general/remove.mp3", "y": "general/slide.mp3"},
                    "animationType": "simpleSlides"
                }
            }
        }
        
    if variant_id in ("4x4", "4x5", "5x5", "5x6", "6x6"):
        return konane_iadata(int(variant_id[0]), int(variant_id[-1]))
    return None

def get_lewthwaitesgame(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [50, 50],
                "centers": [[i % 5 * 10 + 5, i // 5 * 10 + 5] for i in range(25)],
                "background": "lewthwaitesgame/grid.svg",
                "charImages": {
                    "W": {"image": "general/whitepiece.svg", "scale": 7},
                    "B": {"image": "general/blackpiece.svg", "scale": 7},
                },
                "entitiesOverArrows": True,
                "arrowWidth": 1,
                "sounds": {
                    "x": "general/slide.mp3",
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_lgame(variant_id):
    centers = [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)] + [[-99, 99]] * 5 # 5 multipartchars
    centers += [
        [0.15, 0.15], [1.15, 0.15], [2.15, 0.15], [0.15, 1.15], [1.15, 1.15], [2.15, 1.15],
        [1.85, 0.15], [2.85, 0.15], [3.85, 0.15], [1.85, 1.15], [2.85, 1.15], [3.85, 1.15],
        [3.85, 0.75], [3.85, 1.75], [3.85, 2.15], [2.85, 0.75], [2.85, 1.75], [2.85, 2.15],
        [3.375, 1.85], [3.375, 2.85], [3.375, 3.85], [2.375, 1.85], [2.375, 2.25], [2.85, 3.25],
        [3.85, 3.85], [2.85, 3.85], [1.85, 3.85], [3.85, 2.85], [2.85, 2.85], [1.85, 2.85], 
        [2.15, 3.85], [1.15, 3.85], [0.15, 3.85], [2.15, 2.85], [1.15, 2.85], [0.15, 2.85], 
        [0.625, 3.85], [0.625, 2.85], [0.625, 1.85], [1.15, 3.25], [1.625, 2.25], [1.625, 1.85], 
        [0.15, 2.15], [0.15, 1.75], [0.15, 0.75], [1.15, 2.15], [1.15, 1.75], [1.15, 0.75]
    ] # L-shaped move button centers, 6 centers for each of 8 L-piece orientations
    char_images = {
        c: {
            "image": f"lgame/{c}.svg", "scale": 1 if c.isalpha() else 0.6
        } for c in 'WG12345678'
    }
    char_images |= {
        c: {
            "image": f"lgame/{c}.svg", "scale": 5
        } for c in 'HIJKLMNO'
    }
    char_images |= {
        c: {
            "image": f"lgame/{c}{c}.svg", "scale": 5
        } for c in 'hijklmno'
    }
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [4, 4],
                "centers": centers,
                "background": "lgame/grid.svg",
                "charImages": char_images,
                "arrowWidth": 0.035,
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3",
                    "z": "general/slide.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_lightsout(variant_id):
    sideLength = int(variant_id)
    sL2 = sideLength * sideLength
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [sideLength, sideLength],
                "centers": [[i % sideLength + 0.5, i // sideLength + 0.5] for i in range(sL2)],
                "background": "lightsout/background.svg",
                "charImages": {
                    c: {"image": f"lightsout/{c}.svg", "scale": 1} for c in "01t"
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_lite3(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [30, 30],
                "centers": [[x % 3 * 10 + 5, x // 3 * 10 + 5] for x in range(9)],
                "background": "ttt/3x3grid.svg",
                "charImages": {
                    "a": {"image": "ttt/o.svg", "scale": 3},
                    "b": {"image": "ttt/o.svg", "scale": 6},
                    "c": {"image": "ttt/o.svg", "scale": 9},
                    "1": {"image": "ttt/x.svg", "scale": 3},
                    "2": {"image": "ttt/x.svg", "scale": 6},
                    "3": {"image": "ttt/x.svg", "scale": 9},
                    "h": {"image": "general/basichitbox.svg", "scale": 9}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }
    
def get_mutorere(variant_id):
    return {
        "defaultTheme": "octagon",
        "themes": {
            "octagon": {
                "space": [100, 100],
                "centers": [ [50 + 17 * x, 50 + 17 * y] for x, y in 
                    [[0, 0], [-1, -2.41421], [-2.41421, -1], [-2.41421, 1], [-1, 2.41421],
                     [1, 2.41421], [2.41421, 1], [2.41421, -1], [1, -2.41421]]
                ],
                "background": "mutorere/board.svg",
                "charImages": {
                    "x": {"image": "general/bluepiece.svg", "scale": 10},
                    "o": {"image": "general/redpiece.svg", "scale": 10}
                },
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_nim(variant_id):
    try:
        piles = variant_id.split('_')
        for i in range(len(piles)):
            piles[i] = int(piles[i])
    except Exception as err:
        return None
    
    height = 0.5
    width = 1
    
    m, n = max(piles), len(piles)
    adjusted_m, adjusted_n = m * height + 2, (n * 2 + 1) * width
    sideLength = max(adjusted_m, adjusted_n)
    h_spacing = (sideLength - n) / (n + 1) + 1 # spacing between pile x-centers
    x = h_spacing - 0.5 # x-coordinate of starting pile
    
    centers = []
    labels = []
    for i in range(len(piles)):
        pile_size = piles[i]
        for j in range(pile_size):
            centers.append([x, sideLength - 1.5 - height * j])
        labels.append([x, sideLength - 0.5])
        x += h_spacing
    
    centers += labels
    textEntityFontSize = 1

    return {
        "defaultTheme": "kings",
        "themes": {
            "kings": {
                "space": [sideLength, sideLength],
                "centers": centers,
                "background": "nim/grid.svg",
                "charImages": {
                    "x": {"image": "nim/x.svg", "scale": 1},
                    "t": {"image": "nim/t.svg", "scale": 1}
                },
                "textEntityFontSize": textEntityFontSize,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_ninemensmorris(variant_id):
    sounds = {
        "x": "general/place.mp3",
        "y": "general/slide.mp3",
        "z": "general/remove.mp3"
    }
    if variant_id == "regular":
        numbers = {n: {"image": f"general/{n}.svg", "scale": 100} for n in '0123456789'}
        centers = [
            [40, 20], [160, 20], [280, 20], [80, 60], [160, 60], [240, 60], [120, 100], [160, 100],
            [200, 100], [40, 140], [80, 140], [120, 140], [200, 140], [240, 140], [280, 140],
            [120, 180], [160, 180], [200, 180], [80, 220], [160, 220], [240, 220], [40, 260],
            [160, 260], [280, 260], [145, 140], [175, 140], [-999, -999], [-999, -999] 
        ]
        return {
            "defaultTheme": "wikipedia",
            "themes": {
                "wikipedia": {
                    "space": [300, 300],
                    "centers": centers,
                    "background": "369mm/board.svg",
                    "charImages": numbers | {
                        "B": {"image": "general/blackpiece.svg", "scale": 28.6},
                        "W": {"image": "general/whitepiece.svg", "scale": 28.6},
                        "z": {"image": "369mm/z.svg", "scale": 38}
                    },
                    "arrowWidth": 5,
                    "sounds": sounds,
                    "animationType": "simpleSlides",
                    "defaultAnimationWindow": [0, 24]
                }
            }
        }
    elif variant_id == "6mmNoFly":
        numbers = {n: {"image": f"general/{n}.svg", "scale": 90} for n in '0123456'}
        centers = [
            [30, 20], [110, 20], [190, 20], [70, 60], [110, 60], [150, 60], [30, 100], [70, 100],
            [150, 100], [190, 100], [70, 140], [110, 140], [150, 140], [30, 180], [110, 180],
            [190, 180], [95, 100], [125, 100], [-999, -999], [-999, -999]
        ]
        return {
            "defaultTheme": "wikipedia",
            "themes": {
                "wikipedia": {
                    "space": [220, 220],
                    "centers": centers,
                    "background": "369mm/board6mm.svg",
                    "charImages": numbers | {
                        "B": {"image": "general/blackpiece.svg", "scale": 23},
                        "W": {"image": "general/whitepiece.svg", "scale": 23},
                        "z": {"image": "369mm/z.svg", "scale": 31}
                    },
                    "arrowWidth": 4,
                    "sounds": sounds,
                    "animationType": "simpleSlides",
                    "defaultAnimationWindow": [0, 16]
                }
            }
        }
    else:
        return None

def get_notakto(variant_id):
    def ttt(x, y):
        # Return 9 tic-tac-toe grid coordinates given center of top left
        return [[x + 22 * (i % 3), y + 22 * (i // 3)] for i in range(9)]
    
    notakto_iadata = {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "charImages": {
                    "X": {"image": "notakto/x.svg", "scale": 22},
                    "h": {"image": "general/basichitbox.svg", "scale": 20}
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }
    notakto_basic_theme = notakto_iadata["themes"]["basic"]

    if variant_id == "regular":
        notakto_basic_theme["space"] = [66, 66]
        notakto_basic_theme["background"] = "notakto/grid1.svg"
        notakto_basic_theme["centers"] = ttt(11, 11)
    elif variant_id == "board2":
        notakto_basic_theme["space"] = [136, 66]
        notakto_basic_theme["background"] = "notakto/grid2.svg"
        notakto_basic_theme["centers"] = ttt(11, 11) + ttt(81, 11)
    elif variant_id == "board3":
        notakto_basic_theme["space"] = [136, 136]
        notakto_basic_theme["background"] = "notakto/grid3.svg"
        notakto_basic_theme["centers"] = ttt(11, 11) + ttt(81, 11) + ttt(46, 81)
    else:
        return None
    return notakto_iadata

def get_npuzzle(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [3, 3],
                "centers": [[i % 3 + 0.5, i // 3 + 0.5] for i in range(9)],
                "charImages": {
                    str(n): {"image": f"npuzzle/{n}.svg", "scale": 1} for n in range(1, 9)
                },
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_nqueens(variant_id):
    N = int(variant_id)
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [N, N],
                "centers": [[i % N + 0.5, i // N + 0.5] for i in range(N * N)],
                "background": f"nqueens/grid{N}.svg",
                "charImages": {
                    "Q": {"image": "chess/wikipedia/Q.svg", "scale": 1},
                    "h": {"image": "general/basichitbox.svg", "scale": 1}
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_nutictactoe(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [5, 5],
                "centers": [[i % 4 + 1, i // 4 + 0.5] for i in range(20)],
                "background": "nutictactoe/board.svg",
                "charImages": {
                    "X": {"image": "ttt/x.svg", "scale": 1},
                    "O": {"image": "ttt/o.svg", "scale": 1}
                },
                "arrowWidth": 0.075,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_oddoreven(variant_id):
    ctrs = [[i * 10 + 5, 10] for i in range(15)]
    ctrs += [[30 + i % 2 * 10, 90 - i // 2 * 10] for i in range(12)]
    ctrs += [[110 + i % 2 * 10, 90 - i // 2 * 10] for i in range(12)]
    ctrs += [[75, 25], [35, 105], [115, 105]]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [150, 150],
                "centers": ctrs,
                "background": "oddoreven/board.svg",
                "charImages": {
                    "n": {"image": "oddoreven/n.svg", "scale": 10},
                    "x": {"image": "general/bluepiece.svg", "scale": 10},
                    "o": {"image": "general/redpiece.svg", "scale": 10}
                },
                "textEntityFontSize": 10,
                "textButtonFontSize": 8,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_othello(variant_id):
    char_images = {
        "B": {"image": "general/blackpiece.svg", "scale": 9},
        "W": {"image": "general/whitepiece.svg", "scale": 9},
        "h": {"image": "general/basichitbox.svg", "scale": 10},
        "P": {"image": "othello/P.svg", "scale": 6}
    }
    char_images.update({f"{i}": {"image": f"general/{i}.svg", "scale": 20} for i in range(10)})
    centers = [[5 + i % 4 * 10, 5 + i // 4 * 10] for i in range(16)]
    centers += [[3, 45], [7, 45], [33, 45], [37, 45], [20, 45]]
    centers = [[x + 0.06, y + 0.06] for x, y in centers]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [40.12, 50],
                "centers": centers,
                "background": "othello/grid.svg",
                "charImages": char_images,
                "sounds": {"x": "general/place.mp3", "y": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_pegsolitaire(variant_id):
    scale = 18
    arrowWidth = 2
    ctrs = []
    if variant_id == 'triangle':
        ctrs = [[50, 12.2398], [40.15, 29.3005], [59.85, 29.3005], [30.3, 46.3612], [50, 46.3612], [69.7, 46.3612], [20.45, 63.4219], [40.15, 63.4219], [59.85, 63.4219], [79.55, 63.4219], [10.6, 80.4826], [30.3, 80.4826], [50, 80.4826], [69.7, 80.4826], [89.4, 80.4826]]
    elif variant_id == 'star':
        ctrs = [[50, 12.2398], [20.45, 29.3005], [40.15, 29.3005], [59.85, 29.3005], [79.55, 29.3005], [30.3, 46.3612], [50, 46.3612], [69.7, 46.3612], [20.45, 63.4219], [40.15, 63.4219], [59.85, 63.4219], [79.55, 63.4219], [50, 80.4826]]
    elif variant_id == 'trapezoid':
        ctrs = [[28.7857, 29.1562], [42.9286, 29.1562], [57.0714, 29.1562], [71.2143, 29.1562], [21.7143, 41.4043], [35.8571, 41.4043], [50.0, 41.4043], [64.1429, 41.4043], [78.2857, 41.4043], [14.6429, 53.6523], [28.7857, 53.6523], [42.9286, 53.6523], [57.0714, 53.6523], [71.2143, 53.6523], [85.3571, 53.6523], [7.5714, 65.9004], [21.7143, 65.9004], [35.8571, 65.9004], [50.0, 65.9004], [64.1429, 65.9004], [78.2857, 65.9004], [92.4286, 65.9004]]
        scale = 13
        arrowWidth = 1.25
    # elif variant_id == 'cross':
    #     ctrs = [[35.8571, 7.5714], [50.0, 7.5714], [64.1429, 7.5714], [35.8571, 21.7143], [50.0, 21.7143], [64.1429, 21.7143], [7.5714, 35.8571], [21.7143, 35.8571], [35.8571, 35.8571], [50.0, 35.8571], [64.1429, 35.8571], [78.2857, 35.8571], [92.4286, 35.8571], [7.5714, 50.0], [21.7143, 50.0], [35.8571, 50.0], [50.0, 50.0], [64.1429, 50.0], [78.2857, 50.0], [92.4286, 50.0], [7.5714, 64.1429], [21.7143, 64.1429], [35.8571, 64.1429], [50.0, 64.1429], [64.1429, 64.1429], [78.2857, 64.1429], [92.4286, 64.1429], [35.8571, 78.2857], [50.0, 78.2857], [64.1429, 78.2857], [35.8571, 92.4286], [50.0, 92.4286], [64.1429, 92.4286]]
    #     scale = 6.5
    #     arrowWidth = 1.25
    else:
        return None
    return {
        'defaultTheme': 'regular',
        'themes': {
            "regular": {
                'space': [100, 100],
                'background': f'pegsolitaire/{variant_id}.svg',
                'centers': ctrs,
                'charImages': {c: {'image': 'general/brownpiece.svg', 'scale': scale} for c in 'abcd'},
                'arrowWidth': arrowWidth,
                'sounds': {'x': 'general/slideThenRemove.mp3'},
                'animationType': 'simpleSlides'
            },
        }
    }

def get_ponghauki(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100], 
                "centers": [[10, 10], [90, 10], [50, 50], [10, 90], [90, 90]],
                "background": "ponghauki/board.svg",
                "charImages": {
                    "x": {"image": "general/bluepiece.svg", "scale": 15},
                    "o": {"image": "general/redpiece.svg", "scale": 15}
                },
                "entitiesOverArrows": True,
                "sounds": {
                    "x": "general/slide.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_quickchess(variant_id):
    pieces = {"Q": "Q", "R": "R", "K": "K", "q": "qq", "r": "rr", "k": "kk"}
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [4, 3],
                "centers": [[i // 3 + 0.5, i % 3 + 0.5] for i in range(12)],
                "background": "quickchess/grid.svg",
                "charImages": {
                    c: {"image": f"chess/wikipedia/{pieces[c]}.svg", "scale": 1} for c in pieces
                },
                "sounds": {
                    "x": "general/slide.mp3",
                    "y": "general/slideThenRemove.mp3"
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_quickcross(variant_id):
    centers = [[i % 4 * 100 + 50, i // 4 * 100 + 50] for i in range(16)] # cross centers
    cross_left = [[x - 32, y] for x, y in centers] # 16-31: left coord for hori move button
    cross_right = [[x + 32, y] for x, y in centers] # 32-47: right coord for hori move button
    cross_top = [[x, y - 32] for x, y in centers] # 48-63: top coord for vert move button
    cross_bottom = [[x, y + 32] for x, y in centers] # 64-79: bottom coord for vert move button
    centers = centers + cross_left + cross_right + cross_top + cross_bottom

    return {
        "defaultTheme": "moffitt", #because Cameron and Arihant worked in Moffitt
        "themes": {
            "moffitt": {
                "space": [400, 400],
                "centers": centers,
                "background": "quickcross/background.svg",
                "charImages": {
                    "v": {"image": "quickcross/V.svg", "scale": 70},
                    "h": {"image": "quickcross/H.svg", "scale": 70},
                    "r": {"image": "quickcross/rotate.svg", "scale": 70}
                },
                "lineWidth": 6,
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3"
                },
                "animationType": "entityFade"
            }
        }
    }

def get_quixo(variant_id):
    def helper(max_size): 
        src_centers = [[i, j] for i in range(2, max_size + 1, 4) for j in range(2, max_size + 1, 4)]
        up_centers = [[i - 2, j] for i, j in src_centers]
        right_centers = [[i, j + 2] for i, j in src_centers]
        down_centers = [[i + 2, j] for i, j in src_centers]
        left_centers = [[i, j - 2] for i, j in src_centers]
        centers =src_centers + up_centers + right_centers + down_centers + left_centers
        
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [max_size, max_size],
                    "centers": centers,
                    "charImages": {
                        "X": {"image": "quixo/x.svg", "scale": 4},
                        "O": {"image": "quixo/o.svg", "scale": 4}, 
                        "B": {"image": "quixo/blank.svg", "scale": 4}
                    },
                    "arrowWidth": 0.1,
                    "sounds": {"x": "general/slide.mp3"},
                    "animationType": "entityFade"
                }
            }
        }
    
    if variant_id == "5x5": 
        return helper(20)
    if variant_id == "4x4": 
        return helper(16)
    if variant_id == "3x3":
        return helper(12)

def get_rubikscube(variant_id):
    # Color Centers
    centers = [
        [38.75, 41.25], [38.75, 31.25], [46.25, 43.75], [46.25, 33.75],
        [8.75, 28.75], [16.25, 26.5], [8.75, 18.75], [16.25, 16.5],
        [42.5, 25], [50, 22.5], [50, 27.5], [57.5, 25],
        [53.75, 33.75], [61.25, 31.25], [53.75, 43.75], [61.25, 41.25],
        [83.75, 16.5], [83.75, 26.5], [91.25, 18.75], [91.25, 28.75],
        [50, 67.5], [42.5, 70], [57.5, 70], [50, 72.5]
    ]

    # Arrow Endpoints
    centers += [
        [48.5,53.5],[33.5,48.5], [1,17],[1,33], [33.5,21.5],[48.5,16.5], [69, 27],[69, 43],
        [96.5,11.5],[81.5,6.5], [51.5,78.5],[66.5,73.5], [31, 27],[31, 43], [3.5,11.5],[18.5,6.5],
        [66.5,21.5],[51.5,16.5], [51.5,53.5],[66.5,48.5], [99,17],[99,33], [48.5,78.5],[33.5,73.5],
    ]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100],
                "centers": centers,
                "foreground": "rubikscube/fg.svg",
                "charImages": {
                    c: {"image": f"rubikscube/{c}.svg", "scale": 100} for c in 'abcdefghijklmnopqr'
                },
                "arrowWidth": 1,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_rubiksmagic(variant_id):
    entity_ctrs = [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)]
    up_button_ctrs = [[x - 0.2, y] for x, y in entity_ctrs]
    down_button_ctrs = [[x + 0.2, y] for x, y in entity_ctrs]
    char_images = {c: {"image": f"rubiksmagic/{c if c.isupper() else c+c}.svg", "scale": 1} for c in 'UuDd'} |\
          {c: {"image": f"rubiksmagic/{c}.svg", "scale": 0.4} for c in 'pqrs'}
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [4, 4],
                "centers": entity_ctrs + up_button_ctrs + down_button_ctrs,
                "background": "rubiksmagic/background.svg",
                "charImages": char_images,
                "entitiesOverArrows": True,
                "arrowWidth": 0.1,
                "sounds": {"x": "general/remove.mp3", "y": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_rushhour(variant_id):
    pieces = {
        "L": "left", "m": "horizontal", "R": "right", "T": "top",
        "M": "vertical", "B": "bottom", "1": "left_red", "2": "right_red"
    }
    scale, st = 12.375, 6.6875
    centers = [[st + i % 6 * scale, st + i // 6 * scale] for i in range(36)]
    centers += [[81.4375, 31.4375], [93.8125, 31.4375]] # Location of car when it escapes grid
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [100, 100],
                "centers": centers,
                "background": "rushhour/grid.svg",
                "charImages": {
                    p: {"image": f"rushhour/{pieces[p]}.svg", "scale": scale * 1.05} for p in pieces
                },
                "arrowWidth": 1,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_shifttactoe(variant_id):
    centers = [[i % 3 + 3.5, i // 3 + 2.5] for i in range(9)] * 2
    centers += [[i % 3 + 3.5, i // 3 + 0.5] for i in range(6)]
    centers += [[i % 3, i // 3 + 2.5] for i in range(9)]
    centers += [[i % 3 + 7, i // 3 + 2.5] for i in range(9)]
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [9, 6],
                "centers": centers,
                "foreground": "shifttactoe/foreground.svg",
                "charImages": {
                    "S": {"image": "shifttactoe/S.svg", "scale": 10},
                    "x": {"image": "shifttactoe/x.svg", "scale": 1},
                    "o": {"image": "shifttactoe/o.svg", "scale": 1}
                },
                "arrowWidth": 0.10
            }
        }
    }

def get_slide5(variant_id):
    piece_centers = [[25 * (i // 5 + i % 5 + 2), 25 * (i % 5 - i // 5 + 7)] for i in range(25)]
    arrow_centers = [
        [5, 130], [35, 160], [30, 105], [60, 135], [55, 80], [85, 110], [80, 55], [110, 85],
        [105, 30], [135, 60], [195, 30], [165, 60], [220, 55], [190, 85], [245, 80],
        [215, 110], [270, 105], [240, 135], [295, 130], [265, 160]
    ]
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [300, 300],
                "centers": piece_centers + arrow_centers,
                "foreground": "slide5/foreground5x5.svg",
                "charImages": {
                    "X": { "image": "general/blue_circle.svg", "scale": 35 }, 
                    "O": { "image": "general/red_circle.svg", "scale": 35 }
                },
                "arrowWidth": 5,
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_snake(variant_id):
    char_images = {c: {"image": f"snake/{c}.svg", "scale": 1.01} for c in '0123456789'}
    char_images = char_images | {c: {"image": f"snake/{c}.svg", "scale": 1} for c in 'ht'}
    centers = [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)]
    return {
        "defaultTheme": "slither",
        "themes": {
            "slither": {
                "space": [4, 4],
                "centers": centers + centers,
                "background": "snake/grid.svg",
                "charImages": char_images,
                "entitiesOverArrows": True,
                "sounds": {"x": "animals/snake.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_squaredance(variant_id):
    scale = 9.9375
    entity_ctrs = [[5.09375 + (i % 4 * scale), 5.09375 + (i // 4 * scale)] for i in range(16)]
    up_button_ctrs = [[x - 2, y] for x, y in entity_ctrs]
    down_button_ctrs = [[x + 2, y] for x, y in entity_ctrs]
    char_images = {c: {"image": f"squaredance/{c if c.isupper() else c+c}.svg", "scale": scale} for c in 'UuDdWXYZ'} |\
          {c: {"image": f"squaredance/{c}.svg", "scale": 4} for c in 'qrst'}
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [40, 40],
                "centers": entity_ctrs + up_button_ctrs + down_button_ctrs,
                "background": "squaredance/background.svg",
                "foreground": "squaredance/foreground.svg",
                "charImages": char_images,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_tactix(variant_id):
    centers = [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)]
    centers += [
        [0.05, 0.08], [1.95, 0.08], [1.05, 0.4], [2.95, 0.4], [2.05, 0.08], [3.95, 0.08],
        [0.05, 0.16], [2.95, 0.16], [1.05, 0.32], [3.95, 0.32], [0.05, 0.24], [3.95, 0.24],
        [0.05, 1.08], [1.95, 1.08], [1.05, 1.4], [2.95, 1.4], [2.05, 1.08], [3.95, 1.08],
        [0.05, 1.16], [2.95, 1.16], [1.05, 1.32], [3.95, 1.32], [0.05, 1.24], [3.95, 1.24],
        [0.05, 2.08], [1.95, 2.08], [1.05, 2.4], [2.95, 2.4], [2.05, 2.08], [3.95, 2.08],
        [0.05, 2.16], [2.95, 2.16], [1.05, 2.32], [3.95, 2.32], [0.05, 2.24], [3.95, 2.24],
        [0.05, 3.08], [1.95, 3.08], [1.05, 3.4], [2.95, 3.4], [2.05, 3.08], [3.95, 3.08],
        [0.05, 3.16], [2.95, 3.16], [1.05, 3.32], [3.95, 3.32], [0.05, 3.24], [3.95, 3.24],
        [0.08, 0.05], [0.08, 1.95], [0.4, 1.05], [0.4, 2.95], [0.08, 2.05], [0.08, 3.95],
        [0.16, 0.05], [0.16, 2.95], [0.32, 1.05], [0.32, 3.95], [0.24, 0.05], [0.24, 3.95],
        [1.08, 0.05], [1.08, 1.95], [1.4, 1.05], [1.4, 2.95], [1.08, 2.05], [1.08, 3.95],
        [1.16, 0.05], [1.16, 2.95], [1.32, 1.05], [1.32, 3.95], [1.24, 0.05], [1.24, 3.95],
        [2.08, 0.05], [2.08, 1.95], [2.4, 1.05], [2.4, 2.95], [2.08, 2.05], [2.08, 3.95],
        [2.16, 0.05], [2.16, 2.95], [2.32, 1.05], [2.32, 3.95], [2.24, 0.05], [2.24, 3.95],
        [3.08, 0.05], [3.08, 1.95], [3.4, 1.05], [3.4, 2.95], [3.08, 2.05], [3.08, 3.95],
        [3.16, 0.05], [3.16, 2.95], [3.32, 1.05], [3.32, 3.95], [3.24, 0.05], [3.24, 3.95]
    ]
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [4, 4],
                "centers": centers,
                "background": "tactix/grid.svg",
                "charImages": {
                    "O": {"image": "tactix/o.svg", "scale": 1}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_teeko(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [600, 600],
                "centers": [[i * 100, j * 100] for j in range(1, 6) for i in range(1, 6)],
                "background": "teeko/board.svg",
                "charImages": {
                    "X": {"image": "teeko/x.svg", "scale": 80},
                    "O": {"image": "teeko/o.svg", "scale": 80},
                },
                "arrowWidth": 7,
                "sounds": {
                    "x": "general/slide.mp3",
                    "y": "general/place.mp3",
                },
                "animationType": "simpleSlides"
            }
        }
    }

def get_tictactwo(variant_id):
    # 25 piece centers, 9 grid centers, 1 center for "Move grid button", 3 multipart move chars
    centers = [[i % 5 * 20 + 12, i // 5 * 20 + 12] for i in range(25)]
    centers += [[i % 3 * 20 + 32, i // 3 * 20 + 32] for i in range(9)]
    centers += [[52, 112]] + [[-999, -999]] * 3
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [104, 124],
                "centers": centers,
                "background": "tictactwo/background.svg",
                "charImages": {
                    "X": {"image": "tictactwo/X.svg", "scale": 16}, 
                    "O": {"image": "tictactwo/O.svg", "scale": 16},
                    "G": {"image": "tictactwo/tttgrid.svg", "scale": 56},
                    "Z": {"image": "tictactwo/g.svg", "scale": 15},
                    "T": {"image": "tictactwo/t.svg", "scale": 80},
                    "h": {"image": "general/basichitbox.svg", "scale": 16}
                },
                "arrowWidth": 2,
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3",
                    "z": "general/slide.mp3"
                },
                "animationType": "simpleSlides",
                "defaultAnimationWindow": [0, 35]
            }
        }
    }

def get_toadsandfrogspuzzle(variant_id):
    board_length = int(variant_id) + 1
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [board_length, 3],
                "centers": [[i + 0.5, 2] for i in range(board_length)],
                "background": f"toadsandfrogs/pond{variant_id}.svg",
                "charImages": {
                    "x": {"image": "toadsandfrogs/bluefrog.svg", "scale": 0.9},
                    "o": {"image": "toadsandfrogs/redfrog.svg", "scale": 0.9},
                    "h": {"image": "general/basichitbox.svg", "scale": 0.9}
                },
                "sounds": {"x": "animals/frog.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_tootandotto(variant_id):
    def tootandotto_iadata(cols):
        pieces = {"T": "T", "t": "tt", "O": "O", "o": "oo"}
        centers = [[i % cols * 10 + 35, 65 - 10 * (i // cols)] for i in range(cols * 4)]
        pieces_left_xcoords = (5, 15, 85 + 10 * (cols - 4), 95 + 10 * (cols - 4))
        centers += [[j, 65 - 10 * i] for j in pieces_left_xcoords for i in range(cols)]
        centers += [[i % cols * 10 + 35, i // cols * 10 + 5] for i in range(cols * 2)]
        return {
            "defaultTheme": "dan",
            "themes": {
                "dan": {
                    "space": [100 + 10 * (cols - 4), 70],
                    "centers": centers,
                    "background": f"tootandotto/background{cols}.svg",
                    "foreground": f"tootandotto/foreground{cols}.svg",
                    "charImages": {
                        c: {"image": f"tootandotto/{pieces[c]}.svg", "scale": 10} for c in pieces
                    },
                    "sounds": {"x": "general/remove.mp3"},
                    "animationType": "entityFade"
                }
            }
        }
    
    if variant_id in ("4", "5", "6"):
        return tootandotto_iadata(int(variant_id))
    return None

def get_topitop(variant_id):
    # The four building components, 3 placement move buttons, and 1 passturn button
    char_images = {
        c: {"image": f"topitop/{c}.svg", "scale": 1 if c.isupper() else 0.3} for c in "BRSLtuvw"
    } | {"P": {"image": "othello/P.svg", "scale": 0.5}}

    centers = []
    maincenters = [[i % 3 + 0.5, i // 3 + 0.5] for i in range(9)] # Centers of the 9 grid spaces
    for x, y in maincenters:
        # These are the centers of the building components in different scenarios.
        # For example, a bucket has different coordinates if it is not stacked on anything
        # vs. if it is stacked on a small sandpile vs. if stacked on both a small and large pile.
        # (1) Bucket if on ground, (2) bucket if on small, (3) bucket if on largesmall, 
        # (4) small if on ground, (5) small if on large, (6) large (can only be on ground)
        centers += [[x, y - 0.57], [x, y - 0.2], [x, y], [x, y - 0.37], [x, y], [x, y]]
    centers += [[-99, -99], [-99, -99]] # information about disallowedMove is hidden

    # Endpoints of arrow move buttons. There are a total of 40 different arrows that can point
    # from one square to an adjacent square. However, there are only 40 endpoints and not 80
    # because some arrows are just the reverse of each other. If the grid slots are numbered 0-8
    # in row-major order, then the first two coordinates here are the endpoints of the arrows
    # pointing from 0->1, then 0->3, then 0->4, then 1->2, 1->3, 1->4, 1->5, 2->4, 2->5, etc.
    # So the arrow endpoints are ordered by starting square are no instances in which you point
    # from a higher to a lower square e.g. we don't have 4->2 because we can just do 2->4.
    centers += [
        [0.77, 0.5], [1.23, 0.5], [0.5, 0.77], [0.5, 1.23], [0.8, 0.8], [1.2, 1.2], [1.77, 0.5],
        [2.23, 0.5], [1.2, 0.8], [0.8, 1.2], [1.5, 0.77], [1.5, 1.23], [1.8, 0.8], [2.2, 1.2],
        [2.2, 0.8], [1.8, 1.2], [2.5, 0.77], [2.5, 1.23], [0.77, 1.5], [1.23, 1.5], [0.5, 1.77],
        [0.5, 2.23], [0.8, 1.8], [1.2, 2.2], [1.77, 1.5], [2.23, 1.5], [1.2, 1.8], [0.8, 2.2],
        [1.5, 1.77], [1.5, 2.23], [1.8, 1.8], [2.2, 2.2], [2.2, 1.8], [1.8, 2.2], [2.5, 1.77],
        [2.5, 2.23], [0.77, 2.5], [1.23, 2.5], [1.77, 2.5], [2.23, 2.5]
    ]

    # Placement move buttons' centers form equilateral triangle at the center of each grid space
    s, m, o = 0.866025, 0.18, 0.04
    centers += [[x, y - m + o] for x, y in maincenters] # Bucket place button
    centers += [[x - m * s, y + m / 2 + o] for x, y in maincenters] # Small pile place button
    centers += [[x + m * s, y + m / 2 + o] for x, y in maincenters] # Large pile place button

    centers += [[1.5, 3.3]] # Pass turn button

    return {
        "defaultTheme": "beach",
        "themes": {
            "beach": {
                "space": [3, 4],
                "centers": centers,
                "background": "topitop/grid.svg",
                "charImages": char_images,
                "arrowWidth": 0.03,
                "sounds": {
                    "v": "general/remove.mp3",
                    "w": "general/place.mp3",
                    "x": "general/place.mp3",
                    "y": "general/place.mp3",
                    "z": "general/slide.mp3"
                },
                "animationType": "simpleSlides",
                "defaultAnimationWindow": [0, 54]
            }
        }
    }

def get_y(variant_id):
    fg = "y/dim4.svg"
    ctrs = [[50, 15.7328], [37.875, 36.7339], [62.125, 36.7339], [25.75, 57.735], [50, 57.735],
            [74.25, 57.735], [13.625, 78.7361], [37.875, 78.7361], [62.125, 78.7361],
            [86.375, 78.7361]]
    scale = 25
    if variant_id == "dim5" or variant_id == "dim5-misere":
        fg = "y/dim5.svg"
        ctrs = [[50, 12.9326], [40.3, 29.7335], [59.7, 29.7335], [30.6, 46.5344], [50, 46.5344],
                [69.4, 46.5344], [20.9, 63.3353], [40.3, 63.3353], [59.7, 63.3353],
                [79.1, 63.3353], [11.2, 80.1362], [30.6, 80.1362], [50, 80.1362],
                [69.4, 80.1362], [88.8, 80.1362]]
        scale = 20

    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [100, 100],
                "centers": ctrs,
                "foreground": fg,
                "charImages": {
                    c: {"image": f"y/{c}.svg", "scale": scale} for c in "WBh"
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }
                       
def get_yote(variant_id):
    pieces = {f'{c}': f'{c}' for c in range(10)}
    pieces |= {"B": "blackpiece", "W": "whitepiece"}
    def yote_iadata(rows, cols):
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "background": f"yote/grid{rows}x{cols}.svg",
                    "centers": [[i % cols * 10 + 5, i // cols * 10 + 15] for i in range(rows * cols)],
                    "charImages": {
                        p: {"image": f"general/{pieces[p]}.svg", "scale": 9} for p in pieces
                    }
                }
            }
        }
    
    rows, cols = int(variant_id[0]), int(variant_id[-1])
    data = yote_iadata(rows, cols)
    data_regular = data["themes"]["regular"]
    
    if variant_id == "3x3":
        data_regular["space"] = [30, 40]
        data_regular["centers"] = data_regular["centers"] + [[5, 5], [25, 5]]
    elif variant_id == "3x4":
        data_regular["space"] = [40, 40]
        data_regular["centers"] = data_regular["centers"] + [[5, 5], [35, 5]]
    elif variant_id == "4x4":
        data_regular["space"] = [40, 50]
        data_regular["centers"] = data_regular["centers"] + [[5, 5], [35, 5]]
    return data
    
"""
===== STEP 2 ===== 
Add your function to the image_autogui_data_funcs dict in alphabetical order by game_id.
"""

image_autogui_data_funcs = {
    "0to10by1or2": get_0to10by1or2,
    "1dchess": get_1dchess,
    "3spot": get_3spot,
    "achi": get_achi,
    "adugo": get_adugo,
    "allqueenschess": get_allqueenschess,
    "baghchal": get_baghchal,
    "beeline": get_beeline,
    "bishoppuzzle": get_bishoppuzzle,
    "change": get_change,
    "chess": get_chess,
    "chinesechess": get_chinesechess,
    "chomp": get_chomp,
    "chopsticks": get_chopsticks,
    "connect4": get_connect4,
    "chungtoi": get_chungtoi,
    "dao": get_dao,
    "dawsonschess": get_dawsonschess,
    "dinododgem": get_dinododgem,
    "dodgem": get_dodgem,
    "domineering": get_domineering,
    "dragonsandswans": get_dragonsandswans,
    "dshogi": get_dshogi,
    "euclidsgame": get_euclidsgame,
    "fivefieldkono": get_fivefieldkono,
    "fourfieldkono": get_fourfieldkono,
    "forestfox": get_forestfox,
    "foxandhounds": get_foxandhounds,
    "ghost": get_ghost,
    "graphgame": get_graphgame,
    "towersofhanoi": get_towersofhanoi,
    "hareandhounds": get_hareandhounds,
    "jan": get_jan,
    "jenga": get_jenga,
    "joust": get_joust,
    "kayles": get_kayles,
    "konane": get_konane,
    "lewthwaitesgame": get_lewthwaitesgame,
    "lgame": get_lgame,
    "lightsout": get_lightsout,
    "lite3": get_lite3,
    "mutorere": get_mutorere,
    "nim": get_nim,
    "ninemensmorris": get_ninemensmorris,
    "notakto": get_notakto,
    "npuzzle": get_npuzzle,
    "nqueens": get_nqueens,
    "nutictactoe": get_nutictactoe,
    "oddoreven": get_oddoreven,
    "othello": get_othello,
    "pegsolitaire": get_pegsolitaire,
    "ponghauki": get_ponghauki,
    "quickchess": get_quickchess,
    "quickcross": get_quickcross,
    "quixo": get_quixo,
    "rubikscube": get_rubikscube,
    "rubiksmagic": get_rubiksmagic,
    "rushhour": get_rushhour,
    "shifttactoe": get_shifttactoe,
    "slide5": get_slide5,
    "snake": get_snake,
    "squaredance": get_squaredance,
    "tactix": get_tactix,
    "teeko": get_teeko,
    "tictactwo": get_tictactwo,
    "toadsandfrogspuzzle": get_toadsandfrogspuzzle,
    "tootandotto": get_tootandotto,
    "topitop": get_topitop,
    "y": get_y,
    "yote": get_yote
}

def get_image_autogui_data(game_id, variant_id):
    if game_id in image_autogui_data_funcs:
        return image_autogui_data_funcs[game_id](variant_id)
    return None
