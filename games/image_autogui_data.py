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
                "entities": {
                    <char1>: {"image": <path to entity image>, "scale": <image scale>},
                    <char2>: { ... }
                    ...
                },
                "circleButtonRadius: <optional, radius of all default circle move buttons>,
                "lineWidth": <optional, width of all line move buttons>,
                "arrowWidth": <optional, width of all arrow move buttons>,
                "entitiesOverArrows": <optional, Boolean, whether entities are drawn over arrows>,
                "sounds": <optional> {
                    <char1>: <string, path to sound file>,
                    <char2>:
                }
                "animationType": <optional, string, animation type>,
                "defaultAnimationWindow": [start, end] <optional>
            },
            <name of theme2>: {
                ...
            },
            ...
        }
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
                "entities": {
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
                "entities": {
                    "t": {"image": "chess/wikipedia/K.svg", "scale": 1},
                    "k": {"image": "chess/wikipedia/N.svg", "scale": 1},
                    "r": {"image": "chess/wikipedia/R.svg", "scale": 1},
                    "T": {"image": "chess/wikipedia/kk.svg", "scale": 1},
                    "K": {"image": "chess/wikipedia/nn.svg", "scale": 1},
                    "R": {"image": "chess/wikipedia/rr.svg", "scale": 1},
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
    entities = {
        "R": {"image": "3spot/R.svg", "scale": 1.0},
        "W": {"image": "3spot/W.svg", "scale": 1.0},
        "B": {"image": "3spot/B.svg", "scale": 1.0},
        "h": {"image": "3spot/h.svg", "scale": 0.3},
        "v": {"image": "3spot/v.svg", "scale": 0.3},
    }
    entities.update({f"{i}": {"image": f"general/{i}.svg", "scale": 2} for i in range(10)})
    
    return {
        "defaultTheme": "standard",
        "themes": {
            "standard": {
                "space": [3, 4],
                "centers": [
                    [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [0.5, 1.5], [1.5, 1.5],
                    [2.5, 1.5], [0.5, 2.5], [1.5, 2.5], [2.5, 2.5],
                    [0.35, 3.5], [0.65, 3.5], [2.35, 3.5], [2.65, 3.5], [-99, -99],
                    [1, 0.5], [2, 0.5], [0.5, 1], [1.5, 1], [2.5, 1], [1, 1.5],
                    [2, 1.5], [0.5, 2], [1.5, 2], [2.5, 2], [1, 2.5], [2, 2.5]
                ],
                "background": "3spot/grid.svg",
                "entities": entities,
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade",
                "defaultAnimationWindow": [0, 13]
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
                "background": "achi/achiboard.svg",
                "entities": {
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
                    "entities": {
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

def get_baghchal(variant_id):
    entities = {f"{i}": {"image": f"general/{i}.svg", "scale": 1.2} for i in range(10)}
    entities["G"] = {"image": "baghchal/G.png", "scale": 0.7}
    entities["T"] = {"image": "baghchal/T.png", "scale": 0.75}
    
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [5, 6],
                "centers": [[0.5 + (i % 5), 0.5 + (i // 5)] for i in range(25)] + [[3.75,5.2], [3.95,5.2], [3.75,5.55], [3.95,5.55]],
                "background": "baghchal/grid5Diag.svg",
                "entities": entities,
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
                "space": [10, 8],
                "centers": [
                    [1.25, 4.75], [2.5, 4.05], [3.75, 3.3], [5.00, 2.6],
                    [2.5, 5.5], [3.76, 4.75], [5.00, 4.05], [6.25, 3.3],
                    [3.75, 6.2], [5, 5.5], [6.25, 4.75], [7.5, 4.05],
                    [5.00, 6.95], [6.25, 6.2], [7.5, 5.5], [8.75, 4.75]
                ],
                "background": "beeline/board.svg",
                "entities": {
                    "W": {"image": "beeline/yellow_bee.svg", "scale": 1.4},
                    "B": {"image": "beeline/red_bee.svg", "scale": 1.4}
                },
                "arrowWidth": 0.1,
                "entitiesOverArrows": True,
                "sounds": {"b": "animals/bee.mp3"},
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
                "entities": {
                    "o": {"image": "general/red_circle.svg", "scale": 10},
                    "x": {"image": "general/blue_circle.svg", "scale": 10}
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
        "defaultTheme": "wikipedia",
        "themes": {
            t: {
                "space": [8, 8],
                "arrowWidth": 0.1,
                "background": f"chess/{t}/grid.svg",
                "centers": [[i % 8 + 0.5, i // 8 + 0.5] for i in range(64)],
                "entities": {
                    p: {"image": f"chess/{t}/{pieces[p]}.svg", "scale": 1} for p in pieces
                },
                "animationType": "simpleSlides"
            } for t in ("wikipedia", "lichess")
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
                "entities": {
                    p: {"image": f"chinesechess/{t}/{pieces[p]}.svg", "scale": 1} for p in pieces
                }
            } | theme for t in ("regular", "graphical")
        }
    }

def get_chomp(variant_id):
    return {
        "defaultTheme": "choco",
        "themes": {
            "choco": {
                "space": [7, 4],
                "centers": [[i % 7 + 0.5, i // 7 + 0.5] for i in range(28)],
                "entities": {
                    "x" : {"image": "chomp/x.svg", "scale": 1},
                    "p" : {"image": "chomp/p.svg", "scale": 1},
                    "t" : {"image": "general/basichitbox.svg", "scale": 1}
                },
                "sounds": {"x": "chomp/chomp.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_chungtoi(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [3, 4],
                "centers": [
                    [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [0.5, 1.5], [1.5, 1.5], [2.5, 1.5],
                    [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [99, 99], [99, 99], [99, 99],
                    [1, 3.4], [2, 3.4], [99, 99], [1, 3.8], [2, 3.8], [99, 99]
                ],
                "background": "chungtoi/grid.svg",
                "entities": {
                    "R": {"image": "chungtoi/R.svg", "scale": 1},
                    "W": {"image": "chungtoi/W.svg", "scale": 1},
                    "T": {"image": "chungtoi/T.svg", "scale": 1},
                    "X": {"image": "chungtoi/X.svg", "scale": 1},
                    "t": {"image": "chungtoi/tt.svg", "scale": 1},
                    "x": {"image": "chungtoi/xx.svg", "scale": 1},
                    "Y": {"image": "chungtoi/X.svg", "scale": 0.6},
                    "Z": {"image": "chungtoi/T.svg", "scale": 0.6},
                    "y": {"image": "chungtoi/xx.svg", "scale": 0.6},
                    "z": {"image": "chungtoi/tt.svg", "scale": 0.6}
                }
            }
        }
    }

def get_connect4c(variant_id):
    def get_theme(cols):
        centers = [[0.5 + i // 6, 1.5 + i % 6] for i in range(cols * 6)]
        return {
            "defaultTheme": "normal",
            "themes": {
                "normal": {
                    "space": [cols, 7],
                    "centers": centers + [[i % cols + 0.5, i // cols] for i in range(cols * 2)],
                    "foreground": f"connect4/foreground6x{cols}.svg",
                    "entities": {
                        "X": {"image": "connect4/X.svg", "scale": 1},
                        "O": {"image": "connect4/O.svg", "scale": 1},
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
                "entities": {
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
    return {
        "defaultTheme": "kings",
        "themes": {
            "kings": {
                "space": [size, 1],
                "centers": [[0.5 + i, 0.5] for i in range(size)],
                "entities": {
                    e: {"image": f"dawsonschess/{e}.svg", "scale": 1} for e in 'bxo'
                },
                "circleButtonRadius": 0.15,
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
                "background": "dinododgem/new_grid.svg",
                "entities": {
                    "x": {"image": "dinododgem/hadrosaur.svg", "scale": 1},
                    "o": {"image": "dinododgem/triceratops.svg", "scale": 1}
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
                "entities": {
                    "x": {"image": "dodgem/x.svg", "scale": 1}, 
                    "o": {"image": "dodgem/o.svg", "scale": 1}
                },
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }

def get_dragonsandswans(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [40, 40],
                "centers": [[i % 4 * 10 + 5, i // 4 * 10 + 5] for i in range(16)],
                "background": "swans/grid4.svg",
                "entities": {
                    "x": {"image": "swans/x.png", "scale": 8}, 
                    "o": {"image": "swans/o.svg", "scale": 6}
                },
                "entitiesOverArrows": True,
                "sounds": {
                    "x": "animals/dragon.mp3",
                    "o": "animals/swan.mp3"
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
                "background": "euclidsgame/EuclidBoard.svg",
                "centers": [[i % 10 + 0.5, i // 10 + 0.5] for i in range(100)],
                "entities": {
                    "X": {"image": "euclidsgame/cut.svg", "scale": 0.9},
                },
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
                "entities": {
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

def get_forestfox(variant_id):
    pieces = {
        "a": "bell1", "b": "bell2", "c": "bell3", "d": "bell4", "e": "bell5", "f": "key1",
        "g": "key2", "h":"key3", "i": "key4", "j": "key5", "k": "moon1", "l": "moon2",
        "m": "moon3", "n": "moon4", "o": "moon5", "0": "num0", "1": "num1", "2": "num2",
        "3": "num3", "4": "num4", "5": "num5", "6": "num6", "7": "num7"
    }
    
    centers = [[i % 7 * 150 + 125, i // 7 * 600 + 150] for i in range(14)]
    centers += [[575, 450], [200, 450], [950, 450], [425, 450], [725, 450]]
    # decree card, first card, second card, 1st score, 2nd score
        
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [1150, 900],
                "centers": centers,
                "background": "forestfox/cardboard.svg",
                "entities": {
                    p: {"image": f"forestfox/{pieces[p]}.svg", "scale": 200} for p in pieces
                },
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
                "entities": {
                    "F": {"image": "foxandhounds/F.png", "scale": 1},
                    "G": {"image": "foxandhounds/G.png", "scale": 1},
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

def get_gameofy(variant_id):
    img_autogui_data = {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [8, 6],
                "centers": [
                    [4, 1.2],
                    [3.47, 2.1], [4.53, 2.1],
                    [2.97, 3], [4, 3], [5.03, 3],
                    [2.44, 3.9], [3.47, 3.9], [4.53, 3.9], [5.56, 3.9]
                ],
                "background": "gameofy/dim4.svg",
                "entities": {
                    "W": {"image": "gameofy/blue_circle.svg", "scale": 0.8},
                    "B": {"image": "gameofy/red_circle.svg", "scale": 0.8}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "simpleSlides"
            }
        }
    }
    if variant_id == "dim5" or variant_id == "dim5-misere":
        img_autogui_data["themes"]["basic"]["background"] = "gameofy/dim5.svg"
        img_autogui_data["themes"]["basic"]["centers"] += [
            [1.91, 4.8], [2.97, 4.8], [4.00, 4.8], [5.03, 4.8], [6.09, 4.8]
        ]
    return img_autogui_data

def get_ghost(variant_id):
    centers = [[0.5 + i, 2.5] for i in range(25)] + [[1 + i, 2.5] for i in range(24)] # Word
    centers += [[i % 7 * 2 + 6.5, i // 7 * 2 + 7.5] for i in range(21)] # First 21 letter buttons
    centers += [[8.5 + 2 * i, 13.5] for i in range(5)] # Last 5 letter buttons
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "space": [25, 25],
                "background": "ghost/gray_background.svg",
                "centers": centers,
                "entities": {
                    f"{letter}": {
                        "image": f"general/{letter.upper()}.svg", 
                        "scale": 1 if letter.isupper() else 2
                    } for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_haregame(variant_id):
    def haregame_iadata(name, width, num_width):
        main_centers = [[40 * i + 50, 40 * j + 10] for i in range(num_width) for j in range(3)]
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "space": [width, 100],
                    "centers": [[10, 50]] + main_centers + [[width - 10, 50]],
                    "background": f"haregame/board{name}.svg",
                    "entities": {
                        "d": {"image": "haregame/d.svg", "scale": 20},
                        "r": {"image": "haregame/r.svg", "scale": 20}
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
        return haregame_iadata('small', 180, 3)
    elif variant_id == "m-hounds-first" or variant_id == "m-hare-first":
        return haregame_iadata('medium', 260, 5)
    elif variant_id == "l-hounds-first" or variant_id == "l-hare-first":
        return haregame_iadata('large', 340, 7)
    return None

def get_jenga(variant_id):
    if variant_id == "regular":
        return {
            "defaultTheme": "simple",
            "themes": {
                "simple": {
                    "space": [6, 12], 
                    "centers": [                                    [3.5, 11.5], [4.5, 11.5], [5.5, 11.5], 
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
                    "entities": { "J": {"image": "jenga/JengaPiece.svg", "scale": 1}},
                    "animationType": "entityFade"
                }
            }
        }
    else:
        return None
    
def get_kayles(variant_id):
    size = int(variant_id)
    if size == 1:
        centers = [[1, 0.9], [1, 1.6]]
    else:
        y = size / 2
        centers = [[0.5 + i, y] for i in range(size)] + [[0.5 + i, y + 0.7] for i in range(size)] \
        + [[0.75 + i, y + 0.7] for i in range(size)] + [[1.25 + i, y + 0.7] for i in range(size)]
    return {
        "defaultTheme": "kings",
        "themes": {
            "kings": {
                "space": [max(size, 2), max(size, 2)],
                "centers": centers,
                "background": "kayles/grid.svg",
                "entities": {"x": {"image": "kayles/x.svg", "scale": 1}},
                "circleButtonRadius": 0.12,
                "lineWidth": 0.1,
                "sounds": {"x": "general/place.mp3", "y": "general/remove.mp3"},
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
                    "entities": {
                        "x": {"image": "general/blackpiece.svg", "scale": 9},
                        "o": {"image": "general/whitepiece.svg", "scale": 9}
                    },
                    "circleButtonRadius": 1.5,
                    "sounds": {"x": "general/remove.mp3", "y": "general/slide.mp3"},
                    "animationType": "simpleSlides"
                }
            }
        }
        
    if variant_id in ("4x4", "4x5", "5x5", "5x6", "6x6"):
        return konane_iadata(int(variant_id[0]), int(variant_id[-1]))
    return None

def get_Lgame(variant_id):
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
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [4, 4],
                "centers": centers,
                "background": "Lgame/grid.svg",
                "entities": {
                    c: {
                        "image": f"Lgame/{c}.svg", "scale": 1 if c.isalpha() else 0.6
                    } for c in 'BRWG12345678'
                },
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3",
                    "z": "general/remove.mp3"
                },
                "animationType": "entityFade",
                "defaultAnimationWindow": [0, 16]
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
                "background": "lite3/3x3grid.svg",
                "entities": {
                    "a": {"image": "lite3/o.svg", "scale": 3},
                    "b": {"image": "lite3/o.svg", "scale": 6},
                    "c": {"image": "lite3/o.svg", "scale": 9},
                    "1": {"image": "lite3/x.svg", "scale": 3},
                    "2": {"image": "lite3/x.svg", "scale": 6},
                    "3": {"image": "lite3/x.svg", "scale": 9}
                },
                "circleButtonRadius": 2,
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
                "entities": {
                    "x": {"image": "general/blue_circle.svg", "scale": 10},
                    "o": {"image": "general/red_circle.svg", "scale": 10}
                },
                "entitiesOverArrows": True,
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlides"
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
                    "entities": numbers | {
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
                    "entities": numbers | {
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
                "entities": {
                    "X": {"image": "notakto/x.svg", "scale": 22}
                },
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

def get_othello(variant_id):
    entities = {
        "B": {"image": "general/blackpiece.svg", "scale": 9},
        "W": {"image": "general/whitepiece.svg", "scale": 9},
        "P": {"image": "othello/P.svg", "scale": 6}
    }
    entities.update({f"{i}": {"image": f"general/{i}.svg", "scale": 20} for i in range(10)})
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [40, 50],
                "centers": [
                    [5, 5], [15, 5], [25, 5], [35, 5], 
                    [5, 15], [15, 15], [25, 15], [35, 15], 
                    [5, 25], [15, 25], [25, 25], [35, 25], 
                    [5, 35], [15, 35], [25, 35], [35, 35], 
                    [3, 45], [7, 45], [33, 45], [37, 45], [20, 45]
                ],
                "background": "othello/grid.svg",
                "circleButtonRadius": 1.5,
                "entities": entities,
                "sounds": {"x": "general/place.mp3", "y": "general/remove.mp3"},
                "animationType": "entityFade"
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
                "entities": {
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
    centers = [[i % 4 * 92.5 + 48.75, i // 4 * 92.5 + 48.75] for i in range(16)] # cross centers
    cross_left = [[x - 27.5, y] for x, y in centers] # 16-31: left coord for hori move button
    cross_right = [[x + 27.5, y] for x, y in centers] # 32-47: right coord for hori move button
    cross_top = [[x, y - 27.5] for x, y in centers] # 48-63: top coord for vert move button
    cross_bottom = [[x, y + 27.5] for x, y in centers] # 64-79: bottom coord for vert move button
    centers = centers + cross_left + cross_right + cross_top + cross_bottom

    return {
        "defaultTheme": "moffitt", #because Cameron and Arihant worked in Moffitt
        "themes": {
            "moffitt": {
                "space": [375, 375],
                "centers": centers,
                "background": "quickcross/background.svg",
                "entities": {
                    "v": {"image": "quickcross/V.svg", "scale": 70},
                    "h": {"image": "quickcross/H.svg", "scale": 70},
                    "r": {"image": "quickcross/rotate.svg", "scale": 30}
                },
                "lineWidth": 4,
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3"
                },
                "animationType": "entityFade"
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
                "entities": {
                    "S": {"image": "shifttactoe/S.svg", "scale": 10},
                    "x": {"image": "shifttactoe/x.svg", "scale": 1},
                    "o": {"image": "shifttactoe/o.svg", "scale": 1}
                },
                "arrowWidth": 0.10,
                "animationType": "simpleSlides"
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
                "entities": {
                    "X": { "image": "connect4/X.svg", "scale": 33 }, 
                    "O": { "image": "connect4/O.svg", "scale": 33 }
                },
                "arrowWidth": 5,
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "entityFade"
            }
        }
    }

def get_snake(variant_id):
    return {
        "defaultTheme": "slither",
        "themes": {
            "slither": {
                "space": [4, 4],
                "centers": [[i % 4 + 0.5, i // 4 + 0.5] for i in range(16)],
                "background": "snake/background.svg",
                "entities": {c: {"image": f"snake/{c}.svg", "scale": 1} for c in 'bht'},
                "entitiesOverArrows": True,
                "sounds": {"x": "animals/snake.mp3"},
                "animationType": "simpleSlides"
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
                "background": "snake/background.svg",
                "entities": {
                    "O": {"image": "Lgame/G.svg", "scale": 1}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "entityFade"
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
                "entities": {
                    "X": {"image": "tictactwo/X.svg", "scale": 16}, 
                    "O": {"image": "tictactwo/O.svg", "scale": 16},
                    "G": {"image": "tictactwo/tttgrid.svg", "scale": 56},
                    "g": {"image": "tictactwo/g.svg", "scale": 15},
                    "t": {"image": "tictactwo/t.svg", "scale": 80}
                },
                "circleButtonRadius": 4,
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
                    "entities": {
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
    entities = {
        c: {"image": f"topitop/{c}.svg", "scale": 1 if c.isupper() else 0.3} for c in "BRSLuvw"
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
    s, m = 0.866025, 0.16
    centers += [[x, y - m] for x, y in maincenters] # Bucket place button
    centers += [[x - m * s, y + m / 2] for x, y in maincenters] # Small pile place button
    centers += [[x + m * s, y + m / 2] for x, y in maincenters] # Large pile place button

    centers += [[1.5, 3.3]] # Pass turn button

    return {
        "defaultTheme": "beach",
        "themes": {
            "beach": {
                "space": [3, 4],
                "centers": centers,
                "background": "topitop/grid.svg",
                "entities": entities,
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
                       
def get_yote(variant_id):
    pieces = {"0": "0", "1": "1", "2": "2", "3": "3", "B": "blackpiece", "W": "whitepiece"}
    def yote_iadata(rows, cols):
        rc = rows * cols
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "background": f"yote/grid{rows}x{cols}.svg",
                    "centers": [[100, 100]] * 5 + [
                        [i % cols * 10 + 5, i // cols * 10 + 15] for i in range(rc)],
                    "entities": {
                        p: {"image": f"general/{pieces[p]}.svg", "scale": 9} for p in pieces
                    }
                }
            }
        }
    
    if variant_id not in ("3x3", "3x4", "4x4"):
        return None
    
    rows, cols = int(variant_id[0]), int(variant_id[-1])
    data = yote_iadata(rows, cols)
    data_regular = data["themes"]["regular"]
    
    if variant_id == "3x3":
        data_regular["space"] = [30, 40]
        data_regular["centers"] = [[5, 5], [25, 5]] + data_regular["centers"]
    elif variant_id == "3x4":
        data_regular["space"] = [40, 40]
        data_regular["centers"] = [[5, 5], [35, 5]] + data_regular["centers"]
    elif variant_id == "4x4":
        data_regular["space"] = [40, 50]
        data_regular["centers"] = [[5, 5], [35, 5]] + data_regular["centers"]
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
    "baghchal": get_baghchal,
    "beeline": get_beeline,
    "change": get_change,
    "chess": get_chess,
    "chinesechess": get_chinesechess,
    "chomp": get_chomp,
    "connect4c": get_connect4c,
    "chungtoi": get_chungtoi,
    "dao": get_dao,
    "dawsonschess": get_dawsonschess,
    "dinododgem": get_dinododgem,
    "dodgem": get_dodgem,
    "dragonsandswans": get_dragonsandswans,
    "euclidsgame": get_euclidsgame,
    "fivefieldkono": get_fivefieldkono,
    "forestfox": get_forestfox,
    "foxandhounds": get_foxandhounds,
    "gameofy": get_gameofy,
    "ghost": get_ghost,
    "haregame": get_haregame,
    "jenga": get_jenga,
    "kayles": get_kayles,
    "konane": get_konane,
    "Lgame": get_Lgame,
    "lite3": get_lite3,
    "mutorere": get_mutorere,
    "ninemensmorris": get_ninemensmorris,
    "notakto": get_notakto,
    "othello": get_othello,
    "quickchess": get_quickchess,
    "quickcross": get_quickcross,
    "shifttactoe": get_shifttactoe,
    "slide5": get_slide5,
    "snake": get_snake,
    "tactix": get_tactix,
    "tictactwo": get_tictactwo,
    "tootandotto": get_tootandotto,
    "topitop": get_topitop,
    "yote": get_yote
}

def get_image_autogui_data(game_id, variant_id):
    if game_id in image_autogui_data_funcs:
        return image_autogui_data_funcs[game_id](variant_id)
    return None