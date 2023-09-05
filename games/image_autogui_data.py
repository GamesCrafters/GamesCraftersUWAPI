"""
===== STEP 1 ===== 
Create a function that returns Image AutoGUI Data for your game, given a variant of that game.
Return None if no Image AutoGUI Data for the given variant.

get_<game>(variant_id) should return JSON of the following form:

    {
        "defaultTheme": <name of default theme>,
        "themes": {
            <name of theme1>: {
                "space": [<width>, <height>],
                "background": <optional, path to background image>,
                "foreground": <optional, path to foreground image>,
                "centers": [ [<x0>,<y0>], [<x1>, <y1>], [<x2>, <y2>], [<x3>, <y3>], ... ],
                "arrowWidth": <optional, width of all arrow move buttons>,
                "lineWidth": <optional, width of all line move buttons>,
                "circleButtonRadius: <optional, radius of all default circle move buttons>,
                "entitiesOverArrows": <optional, Boolean, whether entities are drawn over arrows or not>,
                "entities": {
                    <char1>: {"image": <path to entity image>, "scale": <image scale>},
                    <char2>: { ... }
                    ...
                },
                "sounds": <optional> {
                    <char1>: <string, path to sound file>,
                    <char2>:
                }
                "animationType": <optional, string, animation type>,
                "animationWindow": [start, end] <optional>
            },
            <name of theme2>: {
                ...
            },
            ...
        }
    }

(Scroll all the way down for Step 2).

"""

def get_baghchal(variant_id):
    entities = {f"{i}": {"image": f"general/{i}.svg", "scale": 1.2} for i in range(10)}
    entities["G"] = {"image": "baghchal/G.png", "scale": 0.7},
    entities["T"] = {"image": "baghchal/T.png", "scale": 0.75},
    
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [5, 6],
                "background": "baghchal/grid5Diag.svg",
                "arrowWidth": 0.05,
                "centers": [[0.5 + (i % 5), 0.5 + (i // 5)] for i in range(25)] + [[3.75,5.2], [3.95,5.2], [3.75,5.55], [3.95,5.55]],
                "entitiesOverArrows": True,
                "entities": entities,
                "sounds": {
                    "g": "animals/goat.mp3",
                    "t": "animals/tiger.mp3"
                },
                "animationType": "simpleSlidePlaceRemove",
                "animationWindow": [0, 25]
            }
        }
    }

def get_lite3(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "space": [30, 30],
                "background": "lite3/3x3grid.svg",
                "circleButtonRadius": 2,
                "centers": [[x % 3 * 10 + 5, x // 3 * 10 + 5] for x in range(9)],
                "entities": {
                    "a": {"image": "lite3/o.svg", "scale": 3},
                    "b": {"image": "lite3/o.svg", "scale": 6},
                    "c": {"image": "lite3/o.svg", "scale": 9},
                    "1": {"image": "lite3/x.svg", "scale": 3},
                    "2": {"image": "lite3/x.svg", "scale": 6},
                    "3": {"image": "lite3/x.svg", "scale": 9}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "naiveInterpolate"
            }
        }
    }
    
def get_jenga(variant_id):
    if variant_id == "regular":
        return {
            "defaultTheme": "simple",
            "themes": {
                "simple": {
                    "space": [6, 12], 
                    "background": "jenga/JengaBoard.svg",
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
               
                    "entities": { "J": {"image": "jenga/JengaPiece.svg", "scale": 1}}
                }
            }
        }
    else:
        return None

def get_3spot(variant_id):
    return {
        "regular": {
            "defaultTheme": "standard",
            "themes": {
                "standard": {
                    "backgroundGeometry": [3, 4],
                    "backgroundImage": "3spot/grid.svg",
                    "centers": [
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [0.5, 1.5], [1.5, 1.5], 
                        [2.5, 1.5], [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], 
                        [0.35, 3.5], [0.65, 3.5], [2.35, 3.5], [2.65, 3.5], [-99, -99],
                        [1, 0.5], [2, 0.5], [0.5, 1], [1.5, 1], [2.5, 1], [1, 1.5], 
                        [2, 1.5], [0.5, 2], [1.5, 2], [2.5, 2], [1, 2.5], [2, 2.5]
                    ],
                    "pieces": {
                        "R": {"image": "3spot/R.svg", "scale": 1.0},
                        "W": {"image": "3spot/W.svg", "scale": 1.0},
                        "B": {"image": "3spot/B.svg", "scale": 1.0},
                        "h": {"image": "3spot/h.svg", "scale": 0.3},
                        "v": {"image": "3spot/v.svg", "scale": 0.3},
                        "0": {"image": "general/0.svg", "scale": 2},
                        "1": {"image": "general/1.svg", "scale": 2},
                        "2": {"image": "general/2.svg", "scale": 2},
                        "3": {"image": "general/3.svg", "scale": 2},
                        "4": {"image": "general/4.svg", "scale": 2},
                        "5": {"image": "general/5.svg", "scale": 2},
                        "6": {"image": "general/6.svg", "scale": 2},
                        "7": {"image": "general/7.svg", "scale": 2},
                        "8": {"image": "general/8.svg", "scale": 2},
                        "9": {"image": "general/9.svg", "scale": 2}
                    },
                    "sounds": {"x": "general/place.mp3"},
                    "animationType": "naiveInterpolate",
                    "animationWindow": [0, 13]
                }
            }
        }
    }.get(variant_id, None)

def get_ninemensmorris(variant_id):
    sounds = {
        "x": "general/place.mp3",
        "y": "general/slide.mp3",
        "z": "general/remove.mp3"
    }
    return {
        "regular": {
            "defaultTheme": "wikipedia",
            "themes": {
                "wikipedia": {
                    "backgroundGeometry": [300, 300],
                    "backgroundImage": "369mm/board.svg",
                    "arrowWidth": 5,
                    "centers": [
                        [40, 20], [160, 20], [280, 20], [80, 60], [160, 60], [240, 60], 
                        [120, 100], [160, 100], [200, 100], [40, 140], [80, 140], [120, 140], 
                        [200, 140], [240, 140], [280, 140], [120, 180], [160, 180], [200, 180], 
                        [80, 220], [160, 220], [240, 220], [40, 260], [160, 260], [280, 260],
                        [145, 140], [175, 140], [-999, -999], [-999, -999] 
                    ],
                    "pieces": {
                        "0": {"image": "general/0.svg", "scale": 100},
                        "1": {"image": "general/1.svg", "scale": 100},
                        "2": {"image": "general/2.svg", "scale": 100},
                        "3": {"image": "general/3.svg", "scale": 100},
                        "4": {"image": "general/4.svg", "scale": 100},
                        "5": {"image": "general/5.svg", "scale": 100},
                        "6": {"image": "general/6.svg", "scale": 100},
                        "7": {"image": "general/7.svg", "scale": 100},
                        "8": {"image": "general/8.svg", "scale": 100},
                        "9": {"image": "general/9.svg", "scale": 100},
                        "B": {"image": "general/blackpiece.svg", "scale": 28.6},
                        "W": {"image": "general/whitepiece.svg", "scale": 28.6},
                        "z": {"image": "369mm/z.svg", "scale": 38}
                    },
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove",
                    "animationWindow": [0, 24]
                }
            }
        },
        "6mmNoFly": {
            "defaultTheme": "wikipedia",
            "themes": {
                "wikipedia": {
                    "backgroundGeometry": [220, 220],
                    "backgroundImage": "369mm/board6mm.svg",
                    "arrowWidth": 4,
                    "centers": [
                        [30, 20], [110, 20], [190, 20], [70, 60], [110, 60], [150, 60],
                        [30, 100], [70, 100], [150, 100], [190, 100], [70, 140], [110, 140], 
                        [150, 140], [30, 180], [110, 180], [190, 180],
                        [95, 100], [125, 100], [-999, -999], [-999, -999] 
                    ],
                    "pieces": {
                        "0": {"image": "general/0.svg", "scale": 90},
                        "1": {"image": "general/1.svg", "scale": 90},
                        "2": {"image": "general/2.svg", "scale": 90},
                        "3": {"image": "general/3.svg", "scale": 90},
                        "4": {"image": "general/4.svg", "scale": 90},
                        "5": {"image": "general/5.svg", "scale": 90},
                        "6": {"image": "general/6.svg", "scale": 90},
                        "B": {"image": "general/blackpiece.svg", "scale": 23},
                        "W": {"image": "general/whitepiece.svg", "scale": 23},
                        "z": {"image": "369mm/z.svg", "scale": 31}
                    },
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove",
                    "animationWindow": [0, 16]
                }
            }
        }
    }.get(variant_id, None)

def get_topitop(variant_id):
    return {
        "regular": {
            "defaultTheme": "beach",
            "themes": {
                "beach": {
                    "backgroundGeometry": [3, 4],
                    "backgroundImage": "topitop/grid.svg",
                    "centers": [
                        [99, 99], [99, 99], [99, 99], [99, 99], [99, 99], [99, 99], 
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [99, 99], [99, 99], 
                        [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], [99, 99], [99, 99], 
                        [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [99, 99], [99, 99], 
                        [99, 99], [1.5, 3.85], [99, 99], [99, 99], [0.25, 3.15], 
                        [0.25, 3.85], [99, 99], [0.8, 3.15], [0.8, 3.85], 
                        [1.5, 3.15], [1.5, 3.85], [99, 99], [2.4, 3.15], 
                        [2.4, 3.85], [99, 99], [99, 99], [99, 99], [99, 99], [99, 99]
                    ],
                    "pieces": {
                        "0": {"image": "general/0.svg", "scale": 1},
                        "1": {"image": "general/1.svg", "scale": 1},
                        "2": {"image": "general/2.svg", "scale": 1},
                        "3": {"image": "general/3.svg", "scale": 1},
                        "4": {"image": "general/4.svg", "scale": 1},
                        "B": {"image": "topitop/B.svg", "scale": 1},
                        "R": {"image": "topitop/R.svg", "scale": 1},
                        "S": {"image": "topitop/S.svg", "scale": 1},
                        "L": {"image": "topitop/L.svg", "scale": 1},
                        "X": {"image": "topitop/X.svg", "scale": 1},
                        "O": {"image": "topitop/O.svg", "scale": 1},
                        "C": {"image": "topitop/C.svg", "scale": 1},
                        "P": {"image": "topitop/P.svg", "scale": 1},
                        "Q": {"image": "topitop/Q.svg", "scale": 1},
                        "b": {"image": "topitop/bb.svg", "scale": 1},
                        "r": {"image": "topitop/rr.svg", "scale": 1},
                        "s": {"image": "topitop/ss.svg", "scale": 1},
                        "l": {"image": "topitop/ll.svg", "scale": 1}
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_Lgame(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [4, 4],
                    "backgroundImage": "Lgame/grid.svg",
                    "centers": [
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], 
                        [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], [3.5, 1.5], 
                        [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [3.5, 2.5], 
                        [0.5, 3.5], [1.5, 3.5], [2.5, 3.5], [3.5, 3.5], 
                        [-99, -99], [-99, -99], [-99, -99], [-99, -99], [-99, -99], 
                        [0.15, 0.15], [1.15, 0.15], [2.15, 0.15], [0.15, 1.15], [1.15, 1.15], [2.15, 1.15], 
                        [1.85, 0.15], [2.85, 0.15], [3.85, 0.15], [1.85, 1.15], [2.85, 1.15], [3.85, 1.15], 
                        [3.85, 0.75], [3.85, 1.75], [3.85, 2.15], [2.85, 0.75], [2.85, 1.75], [2.85, 2.15], 
                        [3.375, 1.85], [3.375, 2.85], [3.375, 3.85], [2.375, 1.85], 
                        [2.375, 2.25], [2.85, 3.25], [3.85, 3.85], [2.85, 3.85], 
                        [1.85, 3.85], [3.85, 2.85], [2.85, 2.85], [1.85, 2.85], 
                        [2.15, 3.85], [1.15, 3.85], [0.15, 3.85], [2.15, 2.85], 
                        [1.15, 2.85], [0.15, 2.85], [0.625, 3.85], [0.625, 2.85], 
                        [0.625, 1.85], [1.15, 3.25], [1.625, 2.25], [1.625, 1.85], 
                        [0.15, 2.15], [0.15, 1.75], [0.15, 0.75], [1.15, 2.15], 
                        [1.15, 1.75], [1.15, 0.75]
                    ],
                    "pieces": {
                        "B": {"image": "Lgame/B.svg", "scale": 1},
                        "R": {"image": "Lgame/R.svg", "scale": 1},
                        "W": {"image": "Lgame/S1.svg", "scale": 1},
                        "G": {"image": "Lgame/S2.svg", "scale": 1},
                        "1": {"image": "Lgame/L1.svg", "scale": 0.6},
                        "2": {"image": "Lgame/L2.svg", "scale": 0.6},
                        "3": {"image": "Lgame/L3.svg", "scale": 0.6},
                        "4": {"image": "Lgame/L4.svg", "scale": 0.6},
                        "5": {"image": "Lgame/L5.svg", "scale": 0.6},
                        "6": {"image": "Lgame/L6.svg", "scale": 0.6},
                        "7": {"image": "Lgame/L7.svg", "scale": 0.6},
                        "8": {"image": "Lgame/L8.svg", "scale": 0.6}
                    },
                    "sounds": {
                        "x": "general/place.mp3",
                        "y": "general/remove.mp3",
                        "z": "general/remove.mp3"
                    },
                    "animationType": "naiveInterpolate",
                    "animationWindow": [0, 16]
                }
            }
        }
    }.get(variant_id, None)

def get_dodgem(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [4, 4],
                    "piecesOverArrows": True,
                    "backgroundImage": "dodgem/grid.svg",
                    "centers": [
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], 
                        [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], [3.5, 1.5], 
                        [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [3.5, 2.5], 
                        [0.5, 3.5], [1.5, 3.5], [2.5, 3.5], [3.5, 3.5]
                    ],
                    "pieces": {
                        "x": {"image": "dodgem/x.svg", "scale": 1}, 
                        "o": {"image": "dodgem/o.svg", "scale": 1}
                    },
                    "sounds": {"x": "general/slide.mp3"},
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }
    }.get(variant_id, None)

def get_tictactwo(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [104, 124],
                    "backgroundImage": "tttwo/grid.svg",
                    "defaultMoveTokenRadius": 4,
                    "centers": [
                        [12, 12], [32, 12], [52, 12], [72, 12], [92, 12], 
                        [12, 32], [32, 32], [52, 32], [72, 32], [92, 32], 
                        [12, 52], [32, 52], [52, 52], [72, 52], [92, 52], 
                        [12, 72], [32, 72], [52, 72], [72, 72], [92, 72], 
                        [12, 92], [32, 92], [52, 92], [72, 92], [92, 92], 
                        [32, 32], [52, 32], [72, 32], 
                        [32, 52], [52, 52], [72, 52], 
                        [32, 72], [52, 72], [72, 72], [52, 112], 
                        [-999, -999], [-999, -999], [-999, -999]
                    ],
                    "pieces": {
                        "X": {"image": "tttwo/X.svg", "scale": 16.0}, 
                        "O": {"image": "tttwo/O.svg", "scale": 16.0},
                        "G": {"image": "tttwo/tttgrid.svg", "scale": 56.0},
                        "g": {"image": "tttwo/g.svg", "scale": 15.0},
                        "t": {"image": "tttwo/t.svg", "scale": 80.0}
                    },
                    "sounds": {
                        "x": "general/place.mp3",
                        "y": "general/remove.mp3",
                        "z": "general/slide.mp3"
                    },
                    "animationType": "simpleSlidePlaceRemove",
                    "animationWindow": [0, 35]
                }
            }
        }
    }.get(variant_id, None)

def get_shifttactoe(variant_id):
    return {
        "default": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [9, 6],
                    "arrowWidth": 0.10,
                    "foregroundImage": "stt/foreground.svg",
                    "centers": [
                        [3.5, 0.5], [4.5, 0.5], [5.5, 0.5], 
                        [3.5, 1.5], [4.5, 1.5], [5.5, 1.5], 
                        [0, 2.5], [1, 2.5], [2, 2.5], 
                        [2.5, 2.5], [3.5, 2.5], [4.5, 2.5], 
                        [5.5, 2.5], [6.5, 2.5], [7, 2.5], 
                        [8, 2.5], [9, 2.5], [0, 3.5], 
                        [1, 3.5], [2, 3.5], [2.5, 3.5], 
                        [3.5, 3.5], [4.5, 3.5], [5.5, 3.5], 
                        [6.5, 3.5], [7, 3.5], [8, 3.5], 
                        [9, 3.5], [0, 4.5], [1, 4.5], 
                        [2, 4.5], [2.5, 4.5], [3.5, 4.5], 
                        [4.5, 4.5], [5.5, 4.5], [6.5, 4.5], 
                        [7, 4.5], [8, 4.5], [9, 4.5], 
                        [2.5, 5.5], [6.5, 5.5], [3.5, 2.5], 
                        [4.5, 2.5], [5.5, 2.5], [3.5, 3.5], 
                        [4.5, 3.5], [5.5, 3.5], [3.5, 4.5], 
                        [4.5, 4.5], [5.5, 4.5]
                    ],
                    "pieces": {
                        "S": {"image": "stt/S.svg", "scale": 10},
                        "x": {"image": "stt/x.svg", "scale": 1},
                        "o": {"image": "stt/o.svg", "scale": 1}
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_tootandotto(variant_id):
    pieces = {
        "T": {"image": "tootnotto/T.svg", "scale": 10.0 }, 
        "t": {"image": "tootnotto/tt.svg", "scale": 10.0}, 
        "O": {"image": "tootnotto/O.svg", "scale": 10.0}, 
        "o": {"image": "tootnotto/oo.svg", "scale": 10.0}
    }
    sounds = {"x": "general/remove.mp3"}
    return {
        "4": {
            "defaultTheme": "dan",
            "themes": {
                "dan": {
                    "backgroundGeometry": [100, 70],
                    "backgroundImage": "tootnotto/board4.svg",
                    "foregroundImage": "tootnotto/foreground4.svg",
                    "centers": [
                        [35, 65], [45, 65], [55, 65], [65, 65],
                        [35, 55], [45, 55], [55, 55], [65, 55],
                        [35, 45], [45, 45], [55, 45], [65, 45],
                        [35, 35], [45, 35], [55, 35], [65, 35],
                        [5, 65], [5, 55], [5, 45], [5, 35],
                        [15, 65], [15, 55], [15, 45], [15, 35],
                        [85, 65], [85, 55], [85, 45], [85, 35],
                        [95, 65], [95, 55], [95, 45], [95, 35],
                        [35, 5], [45, 5], [55, 5], [65, 5],
                        [35, 15], [45, 15], [55, 15], [65, 15],
                    ],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "naiveInterpolate"
                }
            }
        },
        "5": {
            "defaultTheme": "dan",
            "themes": {
                "dan": {
                    "backgroundGeometry": [110, 70],
                    "backgroundImage": "tootnotto/board5.svg",
                    "foregroundImage": "tootnotto/foreground5.svg",
                    "centers": [
                        [35, 65], [45, 65], [55, 65], [65, 65], [75, 65],
                        [35, 55], [45, 55], [55, 55], [65, 55], [75, 55],
                        [35, 45], [45, 45], [55, 45], [65, 45], [75, 45],
                        [35, 35], [45, 35], [55, 35], [65, 35], [75, 35],
                        [5, 65], [5, 55], [5, 45], [5, 35], [5, 25],
                        [15, 65], [15, 55], [15, 45], [15, 35], [15, 25],
                        [95, 65], [95, 55], [95, 45], [95, 35], [95, 25],
                        [105, 65], [105, 55], [105, 45], [105, 35], [105, 25],
                        [35, 5], [45, 5], [55, 5], [65, 5], [75, 5],
                        [35, 15], [45, 15], [55, 15], [65, 15], [75, 15]
                    ],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "naiveInterpolate"
                }
            }
        },
        "6": {
            "defaultTheme": "dan",
            "themes": {
                "dan": {
                    "backgroundGeometry": [120, 70],
                    "backgroundImage": "tootnotto/board6.svg",
                    "foregroundImage": "tootnotto/foreground6.svg",
                    "centers": [
                        [35, 65], [45, 65], [55, 65], [65, 65], [75, 65], [85, 65],
                        [35, 55], [45, 55], [55, 55], [65, 55], [75, 55], [85, 55],
                        [35, 45], [45, 45], [55, 45], [65, 45], [75, 45], [85, 45],
                        [35, 35], [45, 35], [55, 35], [65, 35], [75, 35], [85, 35],
                        [5, 65], [5, 55], [5, 45], [5, 35], [5, 25], [5, 15],
                        [15, 65], [15, 55], [15, 45], [15, 35], [15, 25], [15, 15],
                        [105, 65], [105, 55], [105, 45], [105, 35], [105, 25], [105, 15],
                        [115, 65], [115, 55], [115, 45], [115, 35], [115, 25], [115, 15],
                        [35, 5], [45, 5], [55, 5], [65, 5], [75, 5], [85, 5],
                        [35, 15], [45, 15], [55, 15], [65, 15], [75, 15], [85, 15]
                    ],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "naiveInterpolate"
                }
            }
        }
    }.get(variant_id, None)

def get_chungtoi(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [3, 4],
                    "backgroundImage": "ctoi/grid.svg",
                    "centers": [
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], 
                        [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], 
                        [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], 
                        [99, 99], [99, 99], [99, 99], 
                        [1, 3.4], [2, 3.4], [99, 99], 
                        [1, 3.8], [2, 3.8], [99, 99]
                    ],
                    "pieces": {
                        "R": {"image": "ctoi/R.svg", "scale": 1},
                        "W": {"image": "ctoi/W.svg", "scale": 1},
                        "T": {"image": "ctoi/T.svg", "scale": 1},
                        "X": {"image": "ctoi/X.svg", "scale": 1},
                        "t": {"image": "ctoi/tt.svg", "scale": 1},
                        "x": {"image": "ctoi/xx.svg", "scale": 1},
                        "Y": {"image": "ctoi/X.svg", "scale": 0.6},
                        "Z": {"image": "ctoi/T.svg", "scale": 0.6},
                        "y": {"image": "ctoi/xx.svg", "scale": 0.6},
                        "z": {"image": "ctoi/tt.svg", "scale": 0.6}
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_chomp(variant_id):
    return {
        "4x7": {
            "defaultTheme": "choco",
            "themes": {
                "choco": {
                    "backgroundGeometry": [7, 4],
                    "centers": [
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], 
                        [4.5, 0.5], [5.5, 0.5], [6.5, 0.5], 
                        [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], [3.5, 1.5], 
                        [4.5, 1.5], [5.5, 1.5], [6.5, 1.5], 
                        [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [3.5, 2.5], 
                        [4.5, 2.5], [5.5, 2.5], [6.5, 2.5], 
                        [0.5, 3.5], [1.5, 3.5], [2.5, 3.5], [3.5, 3.5], 
                        [4.5, 3.5], [5.5, 3.5], [6.5, 3.5]
                    ],
                    "pieces": {
                        "x" : {"image": "chomp/x.svg", "scale": 1},
                        "p" : {"image": "chomp/p.svg", "scale": 1}
                    },
                    "sounds": {"x": "chomp/chomp.mp3"},
                    "animationType": "naiveInterpolate"
                }
            }
        }
    }.get(variant_id, None)

def get_dawsonschess(variant_id):
    size = int(variant_id)
    return {
        "defaultTheme": "kings",
        "themes": {
            "kings": {
                "backgroundGeometry": [size, 1],
                "centers": [[0.5 + i, 0.5] for i in range(size)],
                "pieces": {
                    "b": {"image": "dawsonschess/b.svg", "scale": 1},
                    "x": {"image": "dawsonschess/x.svg", "scale": 1},
                    "o": {"image": "dawsonschess/o.svg", "scale": 1}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "naiveInterpolate"
            }
        }
    }

def get_chess(variant_id):
    if variant_id != "7-man":
        return None
    pieces = {
                "K": "K", "Q": "Q", "R": "R", "B": "B", "N": "N", 
                "P": "P", "k": "kk", "q": "qq", "r": "rr", 
                "b": "bb", "n": "nn", "p": "pp"
            }
    return {
            "defaultTheme": "wikipedia",
            "themes": {
                "wikipedia": {
                    "backgroundGeometry": [8, 8],
                    "arrowWidth": 0.1,
                    "backgroundImage": "chess/wikipedia/grid.svg",
                    "centers": [[0.5 + (i % 8), 0.5 + (i // 8)] for i in range(64)],
                    "pieces": {k: {"image": "chess/wikipedia/{}.svg".format(v), "scale": 1} for (k, v) in pieces.items()},
                    "animationType": "simpleSlidePlaceRemove"
                },
                "lichess": {
                    "backgroundGeometry": [8, 8],
                    "arrowWidth": 0.1,
                    "backgroundImage": "chess/lichess/grid.svg",
                    "centers": [[0.5 + (i % 8), 0.5 + (i // 8)] for i in range(64)],
                    "pieces": {k: {"image": "chess/lichess/{}.svg".format(v), "scale": 1} for (k, v) in pieces.items()},
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }

def get_foxandhounds(variant_id):
    return {
            "defaultTheme": "lichess",
            "themes": {
                "lichess": {
                    "backgroundGeometry": [8, 8],
                    "arrowWidth": 0.1,
                    "backgroundImage": "chess/lichess/grid.svg",
                    "centers": [[0.5 + (i % 8), 0.5 + (i // 8)] for i in 
                                (1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,
                                 33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62)],
                    "piecesOverArrows": True,
                    "pieces": {
                        "F": {"image": "foxandhounds/F.png", "scale": 1},
                        "G": {"image": "foxandhounds/G.png", "scale": 1},
                    },
                    "sounds": {
                        "f": "animals/fox.mp3",
                        "h": "animals/dog.mp3"
                    },
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }

def get_snake(variant_id):
    return {
        "defaultTheme": "slither",
        "themes": {
            "slither": {
                "backgroundGeometry": [4, 4],
                "piecesOverArrows": True,
                "backgroundImage": "snake/background.svg",
                "centers": [[0.5 + i % 4, 0.5 + i // 4] for i in range(16)],
                "pieces": {
                    "b": {"image": "snake/b.svg", "scale": 1},
                    "h": {"image": "snake/h.svg", "scale": 1},
                    "t": {"image": "snake/t.svg", "scale": 1}
                },
                "sounds": {"x": "animals/snake.mp3"},
                "animationType": "simpleSlidePlaceRemove"
            }
        }
    }
    
def get_quickcross(variant_id):
    center_maps = [
        [48.75, 48.75], [141.25, 48.75], [233.75, 48.75], [326.25, 48.75],
        [48.75, 141.25], [141.25, 141.25], [233.75, 141.25], [326.25, 141.25],
        [48.75, 233.75], [141.25, 233.75], [233.75, 233.75], [326.25, 233.75],
        [48.75, 326.25], [141.25, 326.25], [233.75, 326.25], [326.25, 326.25],
    ]
    width = 27.5
    left_cross = [[center_maps[i][0] - width, center_maps[i][1]] for i in range(len(center_maps))]
    right_cross = [[center_maps[i][0] + width, center_maps[i][1]] for i in range(len(center_maps))]
    top_cross = [[center_maps[i][0], center_maps[i][1] - width] for i in range(len(center_maps))]
    bottom_cross = [[center_maps[i][0], center_maps[i][1] + width] for i in range(len(center_maps))]
    mapping_list = center_maps + left_cross + right_cross + top_cross + bottom_cross

    return {
        "defaultTheme": "moffitt", #because Cameron and Arihant worked in Moffitt
        "themes": {
            "moffitt": {
                "backgroundGeometry": [375, 375],
                "backgroundImage": "quickcross/background.svg",
                #centers contains mappings to points in the background svg that point to the following:
                #centers[0->15]: centers, [16->31]: left coordinate for horizontal piece
                #centers[32->47]: right coordinate for horizontal piece
                #centers[48->63]: top coordinate for vertical piece
                #centers[64->79]: bottom coordinate for vertical piece.
                "centers": mapping_list,
                "pieces": {
                    "v": {
                        "image": "quickcross/V.svg", "scale": 70.0
                    },
                    "h": {
                        "image": "quickcross/H.svg", "scale": 70.0
                    },
                    "r": {
                        "image": "quickcross/rotate.svg", "scale": 30.0
                    }
                },
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/remove.mp3"
                },
                "animationType": "naiveInterpolate"
            }
        }
    }

def get_haregame(variant_id):
    pieces = {
        "d": {"image": "haregame/d.svg", "scale": 20},
        "r": {"image": "haregame/r.svg", "scale": 20}
    }
    sounds = {
        "r": "animals/bunny.mp3",
        "d": "animals/dog.mp3"
    }
    if variant_id == "s-hounds-first" or variant_id == "s-hare-first":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [180, 100],
                    "piecesOverArrows": True,
                    "arrowWidth": 2,
                    "backgroundImage": "haregame/boardsmall.svg",
                    "centers": [[10, 50]] + [[40*i + 50, 40*j + 10] for i in range(3) for j in range(3)] + [[170, 50]],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }
    elif variant_id == "m-hounds-first" or variant_id == "m-hare-first":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [260, 100],
                    "piecesOverArrows": True,
                    "arrowWidth": 2,
                    "backgroundImage": "haregame/boardmedium.svg",
                    "centers": [[10, 50]] + [[40*i + 50, 40*j + 10] for i in range(5) for j in range(3)] + [[250, 50]],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }
    elif variant_id == "l-hounds-first" or variant_id == "l-hare-first":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [340, 100],
                    "piecesOverArrows": True,
                    "arrowWidth": 2,
                    "backgroundImage": "haregame/boardlarge.svg",
                    "centers": [[10, 50]] + [[40*i + 50, 40*j + 10] for i in range(7) for j in range(3)] + [[330, 50]],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }
    return None

def get_connect4c(variant_id):
    sounds = {"x" : "general/remove.mp3"}
    pieces = {
        "X": { "image": "connect4/X.svg", "scale": 1.0 }, 
        "O": { "image": "connect4/O.svg", "scale": 1.0 }, 
        "a": { "image": "connect4/a.svg", "scale": 0.8 }
    }
    if variant_id == "6x6":
        return {
            "defaultTheme": "normal",
            "themes": {
                "normal": {
                    "backgroundGeometry": [6, 7],
                    "foregroundImage": "connect4/foreground6x6.svg",
                    "centers": [[0.5 + i // 6, 1.5 + i % 6] for i in range(36)] + [[0.5 + i, 0.5] for i in range(6)],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "naiveInterpolate"
                }
            }
        }
    elif variant_id == "6x7":
        return {
            "defaultTheme": "normal",
            "themes": {
                "normal": {
                    "backgroundGeometry": [7, 7],
                    "foregroundImage": "connect4/foreground6x7.svg",
                    "centers": [[0.5 + i // 6, 1.5 + i % 6] for i in range(42)] + [[0.5 + i, 0.5] for i in range(7)],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "naiveInterpolate"
                }
            }
        } 
    return None

def get_mutorere(variant_id):
    return {
        "defaultTheme": "octagon",
        "themes": {
            "octagon": {
                "backgroundGeometry": [100, 100],
                "piecesOverArrows": True,
                "backgroundImage": "mutorere/board.svg",
                "centers": [
                    [50 + 17 * x, 50 + 17 * y] for x, y in 
                    [[0, 0], [-1, -2.41421], [-2.41421, -1], [-2.41421, 1], [-1, 2.41421],
                     [1, 2.41421], [2.41421, 1], [2.41421, -1], [1, -2.41421]]
                ],
                "pieces": {
                    "x": {"image": "general/blue_circle.svg", "scale": 10},
                    "o": {"image": "general/red_circle.svg", "scale": 10}
                },
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlidePlaceRemove"
            }
        }
    }
    
def get_achi(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [100, 100],
                "backgroundImage": "achi/achiboard.svg",
                "piecesOverArrows": True,
                "arrowWidth": 4,
                "defaultMoveTokenRadius": 6.5,
                "centers": [
                    [10, 10], [50, 10], [90, 10],
                    [10, 50], [50, 50], [90, 50],
                    [10, 90], [50, 90], [90, 90],
                ],
                "pieces": {
                    "x": {"image": "general/blackpiece.svg", "scale": 15},
                    "o": {"image": "general/whitepiece.svg", "scale": 15}
                },
                "sounds": {
                    "x": "general/place.mp3",
                    "y": "general/slide.mp3"
                },
                "animationType": "simpleSlidePlaceRemove"
            }
        }
    }

def get_dinododgem(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [6, 6],
                    "piecesOverArrows": True,
                    "arrowWidth": 0.09,
                    "backgroundImage": "dinododgem/new_grid.svg",
                    "centers": [
                        [0.5, 5.5], [0.5, 4.5], [0.5, 3.5], [0.5, 2.5], [0.5, 1.5], 
                        [1.5, 5.5], [1.5, 4.5], [1.5, 3.5], [1.5, 2.5], [1.5, 1.5], 
                        [2.5, 5.5], [2.5, 4.5], [2.5, 3.5], [2.5, 2.5], [2.5, 1.5], 
                        [3.5, 5.5], [3.5, 4.5], [3.5, 3.5], [3.5, 2.5], [3.5, 1.5], 
                        [4.5, 5.5], [4.5, 4.5], [4.5, 3.5], [4.5, 2.5], [4.5, 1.5], 
                        [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], [4.5, 0.5], [5.5, 1.5], 
                        [5.5, 2.5], [5.5, 3.5], [5.5, 4.5]
                    ],
                    "pieces": {
                        "x": {"image": "dinododgem/hadrosaur.svg", "scale": 1},
                        "o": {"image": "dinododgem/triceratops.svg", "scale": 1}
                    },
                    "sounds": {
                        "x": "animals/tiger.mp3",
                        "y": "animals/dragon.mp3"  
                    },
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }
    }.get(variant_id, None)
    
def get_quickchess(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [4, 3],
                    "backgroundImage": "quickchess/grid.svg",
                    "centers": [
                        [0.5, 0.5], [0.5, 1.5], [0.5, 2.5], 
                        [1.5, 0.5], [1.5, 1.5], [1.5, 2.5], 
                        [2.5, 0.5], [2.5, 1.5], [2.5, 2.5], 
                        [3.5, 0.5], [3.5, 1.5], [3.5, 2.5],
                    ],
                    "pieces": {
                        "Q": {"image": "chess/wikipedia/Q.svg", "scale": 1},
                        "R": {"image": "chess/wikipedia/R.svg", "scale": 1},
                        "K": {"image": "chess/wikipedia/K.svg", "scale": 1},
                        "q": {"image": "chess/wikipedia/qq.svg", "scale": 1},
                        "r": {"image": "chess/wikipedia/rr.svg", "scale": 1},
                        "k": {"image": "chess/wikipedia/kk.svg", "scale": 1}
                    },
                    "sounds": {
                        "x": "general/slide.mp3",
                        "y": "general/slideThenRemove.mp3"
                    },
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }
    }.get(variant_id, None)

def get_tactix(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [4, 4],
                "backgroundImage": "snake/background.svg",
                "centers": [[0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], 
                            [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], [3.5, 1.5], 
                            [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [3.5, 2.5], 
                            [0.5, 3.5], [1.5, 3.5], [2.5, 3.5], [3.5, 3.5], 
                            [0.05, 0.08], [1.95, 0.08], 
                            [1.05, 0.4], [2.95, 0.4], [2.05, 0.08], 
                            [3.95, 0.08], [0.05, 0.16], 
                            [2.95, 0.16], [1.05, 0.32], [3.95, 0.32], 
                            [0.05, 0.24], [3.95, 0.24], 
                            [0.05, 1.08], [1.95, 1.08], 
                            [1.05, 1.4], [2.95, 1.4], [2.05, 1.08], 
                            [3.95, 1.08], [0.05, 1.16], [2.95, 1.16], 
                            [1.05, 1.32], [3.95, 1.32], 
                            [0.05, 1.24], [3.95, 1.24], [0.05, 2.08], [1.95, 2.08], 
                            [1.05, 2.4], [2.95, 2.4], [2.05, 2.08], [3.95, 2.08], 
                            [0.05, 2.16], [2.95, 2.16], [1.05, 2.32], [3.95, 2.32], 
                            [0.05, 2.24], [3.95, 2.24], 
                            [0.05, 3.08], [1.95, 3.08], [1.05, 3.4], [2.95, 3.4], 
                            [2.05, 3.08], [3.95, 3.08], [0.05, 3.16], [2.95, 3.16], 
                            [1.05, 3.32], [3.95, 3.32], [0.05, 3.24], 
                            [3.95, 3.24], [0.08, 0.05], 
                            [0.08, 1.95], [0.4, 1.05], [0.4, 2.95], 
                            [0.08, 2.05], [0.08, 3.95], 
                            [0.16, 0.05], [0.16, 2.95], 
                            [0.32, 1.05], [0.32, 3.95], [0.24, 0.05], 
                            [0.24, 3.95], [1.08, 0.05], 
                            [1.08, 1.95], [1.4, 1.05], [1.4, 2.95], 
                            [1.08, 2.05], [1.08, 3.95], 
                            [1.16, 0.05], [1.16, 2.95], [1.32, 1.05], 
                            [1.32, 3.95], [1.24, 0.05], [1.24, 3.95], 
                            [2.08, 0.05], [2.08, 1.95], [2.4, 1.05], [2.4, 2.95], 
                            [2.08, 2.05], [2.08, 3.95], [2.16, 0.05], [2.16, 2.95], 
                            [2.32, 1.05], [2.32, 3.95], [2.24, 0.05], 
                            [2.24, 3.95], [3.08, 0.05], [3.08, 1.95], 
                            [3.4, 1.05], [3.4, 2.95], [3.08, 2.05], [3.08, 3.95], 
                            [3.16, 0.05], [3.16, 2.95], [3.32, 1.05], [3.32, 3.95], 
                            [3.24, 0.05], [3.24, 3.95]],
                "pieces": {
                    "O": {"image": "Lgame/S2.svg", "scale": 1}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "naiveInterpolate"
            }
        }
    }

def get_othello(variant_id):
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "backgroundGeometry": [40, 50],
                "backgroundImage": "othello/grid.svg",
                "defaultMoveTokenRadius": 1.5,
                "centers": [
                    [5, 5], [15, 5], [25, 5], [35, 5], 
                    [5, 15], [15, 15], [25, 15], [35, 15], 
                    [5, 25], [15, 25], [25, 25], [35, 25], 
                    [5, 35], [15, 35], [25, 35], [35, 35], 
                    [3, 45], [7, 45], [33, 45], [37, 45], [20, 45]
                ],
                "pieces": {
                    "B": {"image": "othello/B.svg", "scale": 9},
                    "W": {"image": "othello/W.svg", "scale": 9},
                    "0": {"image": "general/0.svg", "scale": 20},
                    "1": {"image": "general/1.svg", "scale": 20},
                    "2": {"image": "general/2.svg", "scale": 20},
                    "3": {"image": "general/3.svg", "scale": 20},
                    "4": {"image": "general/4.svg", "scale": 20},
                    "5": {"image": "general/5.svg", "scale": 20},
                    "6": {"image": "general/6.svg", "scale": 20},
                    "7": {"image": "general/7.svg", "scale": 20},
                    "8": {"image": "general/8.svg", "scale": 20},
                    "9": {"image": "general/9.svg", "scale": 20},
                    "P": {"image": "othello/P.svg", "scale": 6}
                },
                "sounds": {"x": "general/place.mp3"},
                "animationType": "naiveInterpolate"
            }
        }
    }
    
def get_gameofy(variant_id):
    pieces = {
        "W": {"image": "gameofy/blue_circle.svg", "scale": 0.8}, 
        "B": {"image": "gameofy/red_circle.svg", "scale": 0.8}
    }
    sounds = {
        "x": "general/place.mp3"
    }
    if variant_id == "dim4" or variant_id == "dim4-misere":
        return {
            "defaultTheme": "basic",
            "themes": {
                "basic": {
                    "backgroundGeometry": [8, 6],
                    "backgroundImage": "gameofy/dim4.svg",
                    "centers": [
                        [4, 1.2],
                        [3.47, 2.1], [4.53, 2.1],
                        [2.97, 3], [4, 3], [5.03, 3], 
                        [2.44, 3.9], [3.47, 3.9], [4.53, 3.9], [5.56, 3.9]
                    ],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove"
                },
            }
        }
    elif variant_id == "dim5" or variant_id == "dim5-misere":
        return {
            "defaultTheme": "basic",
            "themes": {
                "basic": {
                    "backgroundGeometry": [8, 6],
                    "backgroundImage": "gameofy/dim5.svg",
                    "centers": [
                        [4, 1.2], 
                        [3.47, 2.1], [4.53, 2.1], 
                        [2.97, 3], [4, 3], [5.03, 3], 
                        [2.44, 3.9], [3.47, 3.9], [4.53, 3.9], [5.56, 3.9], 
                        [1.91, 4.8], [2.97, 4.8], [4.00, 4.8], [5.03, 4.8], [6.09, 4.8], 
                    ],
                    "pieces": pieces,
                    "sounds": sounds,
                    "animationType": "simpleSlidePlaceRemove"
                },
            }
        }
    
def get_notakto(variant_id):
    pieces = {
        "X": {"image": "notakto/x.svg", "scale": 1}
    }
    if variant_id == "regular":
        return {
            "defaultTheme": "basic",
            "themes": {
                "basic": {
                    "backgroundGeometry": [3, 3],
                    "backgroundImage": "notakto/grid1.svg",
                    "centers": [
                        [0.5, 0.5], [1.5, 0.5], [2.5, 0.5],
                        [0.5, 1.5], [1.5, 1.5], [2.5, 1.5],
                        [0.5, 2.5], [1.5, 2.5], [2.5, 2.5]
                    ],
                    "pieces": pieces
                },
            }
        }
    elif variant_id == "board2":
        return {
            "defaultTheme": "basic",
            "themes": {
                "basic": {
                    "backgroundGeometry": [136, 66],
                    "backgroundImage": "notakto/grid2.svg",
                    "centers": [
                        [11, 11], [33, 11], [55, 11],
                        [11, 33], [33, 33], [55, 33],
                        [11, 55], [33, 55], [55, 55],  
                        [81, 11], [103, 11], [125, 11],
                        [81, 33], [103, 33], [125, 33],
                        [81, 55], [103, 55], [125, 55]
                    ],
                    "pieces": pieces
                },
            }
        }
    elif variant_id == "board3":
        return {
            "defaultTheme": "basic",
            "themes": {
                "basic": {
                    "backgroundGeometry": [136, 136],
                    "backgroundImage": "notakto/grid3.svg",
                    "centers": [
                        [11, 11], [33, 11], [55, 11],
                        [11, 33], [33, 33], [55, 33],
                        [11, 55], [33, 55], [55, 55],
                        [81, 11], [103, 11], [125, 11],
                        [81, 33], [103, 33], [125, 33],
                        [81, 55], [103, 55], [125, 55],
                        [46, 81], [68, 81], [90, 81],
                        [46, 103], [68, 103], [90, 103],
                        [46, 125], [68, 125], [90, 125]
                    ],
                    "pieces": pieces
                },
            }
        }

def get_beeline(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [10, 8],
                "backgroundImage": "beeline/board.svg",
                "arrowWidth": 0.1,
                "piecesOverArrows": True,
                "centers": [
                    [1.25, 4.75], [2.5, 4.05], [3.75, 3.3], [5.00, 2.6],
                    [2.5, 5.5], [3.76, 4.75], [5.00, 4.05], [6.25, 3.3],
                    [3.75, 6.2], [5, 5.5], [6.25, 4.75], [7.5, 4.05],
                    [5.00, 6.95], [6.25, 6.2], [7.5, 5.5], [8.75, 4.75]
                ],
                "pieces": {
                    "W": {"image": "beeline/yellow_bee.svg", "scale": 1.4},
                    "B": {"image": "beeline/red_bee.svg", "scale": 1.4}
                },
                "sounds": {"b": "animals/bee.mp3"},
                "animationType": "simpleSlidePlaceRemove"
            },
        }
    }

def get_1dchess(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [8, 1],
                "backgroundImage": "1dchess/grid.svg",
                "piecesOverArrows": False,
                "arrowWidth": 0.1,
                "centers": [[0.5 + i, 0.5] for i in range(8)],
                "pieces": {
                    "t": {"image": "chess/wikipedia/K.svg", "scale": 1},
                    "k": {"image": "chess/wikipedia/N.svg", "scale": 1},
                    "r": {"image": "chess/wikipedia/R.svg", "scale": 1},
                    "T": {"image": "chess/wikipedia/kk.svg", "scale": 1},
                    "K": {"image": "chess/wikipedia/nn.svg", "scale": 1},
                    "R": {"image": "chess/wikipedia/rr.svg", "scale": 1},
                },
                "sounds": {
                    "x": "general/slide.mp3",
                    "y": "general/slideThenRemove.mp3"
                },
                "animationType": "simpleSlidePlaceRemove"
            },
        }
    }

def get_chinesechess(variant_id):
    pieces = {
        "K": "general_r", "A": "advisor_r", "R": "chariot_r", "B": "elephant_r", 
        "N": "horse_r", "P": "soldier_r", "Q": "soldier_r", "C":"cannon_r", 
        "k": "general_b", "a": "advisor_b", "r": "chariot_b", "b": "elephant_b", 
        "n": "horse_b", "p": "soldier_b", "q": "soldier_b", "c":"cannon_b"
    }
    
    sounds = {
        "x": "general/slide.mp3",
        "y": "general/slideThenRemove.mp3"
    }
    
    return {
        "defaultTheme": "regular",
        "themes": {
            "regular": {
                "backgroundGeometry": [9, 10],
                "arrowWidth": 0.1,
                "backgroundImage": "chinesechess/board.svg",
                "centers": [[0.5 + (i % 9), 0.5 + (i // 9)] for i in range(90)],
                "pieces": {k: {"image": "chinesechess/regular/{}.svg".format(v), "scale": 1} for (k, v) in pieces.items()},
                "sounds": sounds,
                "animationType": "simpleSlidePlaceRemove"
            },
            "graphical": {
                "backgroundGeometry": [9, 10],
                "arrowWidth": 0.1,
                "backgroundImage": "chinesechess/board.svg",
                "centers": [[0.5 + (i % 9), 0.5 + (i // 9)] for i in range(90)],
                "pieces": {k: {"image": "chinesechess/graphical/{}.svg".format(v), "scale": 1} for (k, v) in pieces.items()},
                "sounds": sounds,
                "animationType": "simpleSlidePlaceRemove"
            }
        }
    }

def get_dao(variant_id):    
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [4, 4],
                "backgroundImage": "dao/grid.svg",
                "arrowWidth": 0.1,
                "piecesOverArrows": True,
                "centers": [
                    [0.5, 0.5], [1.5, 0.5], [2.5, 0.5], [3.5, 0.5],
                    [0.5, 1.5], [1.5, 1.5], [2.5, 1.5], [3.5, 1.5],
                    [0.5, 2.5], [1.5, 2.5], [2.5, 2.5], [3.5, 2.5],
                    [0.5, 3.5], [1.5, 3.5], [2.5, 3.5], [3.5, 3.5],
                ],
                "pieces": {
                    "O": {"image": "dao/W.svg", "scale": 0.9},
                    "X": {"image": "dao/B.svg", "scale": 0.9}
                },
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlidePlaceRemove"
            },
        }
    }

def get_change(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [80, 80],
                "backgroundImage": "change/graph.svg",
                "arrowWidth": 1,
                "piecesOverArrows": True,
                "centers": [
                    [70, 26], [70, 44], [70, 62],
                    [50, 17], [50, 35], [50, 53], [50, 71],
                    [30, 8], [30, 26], [30, 44], [30, 62],
                    [10, 17], [10, 35], [10, 53]
                ],
                "pieces": {
                    "o": {"image": "general/red_circle.svg", "scale": 10},
                    "x": {"image": "general/blue_circle.svg", "scale": 10}
                },
                "sounds": {"x": "general/slide.mp3"},
                "animationType": "simpleSlidePlaceRemove"
            },
        }
    }
    
def get_fivefieldkono(variant_id):
    return {
            "defaultTheme": "basic",
            "themes": {
                "basic": {
                    "backgroundGeometry": [200, 200],
                    "backgroundImage": "fivefieldkono/board.svg",
                    "piecesOverArrows": True,
                    "arrowWidth": 5,
                    "centers": [[20 + 40 * i, 20 + 40 * j] for j in range(0,5) for i in range(0,5)],
                    "pieces": {
                        "x": {"image": "general/whitepiece.svg", "scale": 25},
                        "o": {"image": "general/blackpiece.svg", "scale": 25}
                    },
                    "sounds": {"x": "general/slide.mp3"},
                    "animationType": "simpleSlidePlaceRemove"
                }
            }
        }

def get_dragonsandswans(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [40, 40],
                "backgroundImage": "swans/grid4.svg",
                "piecesOverArrows": True,
                "centers": [[5 + 10 * i, 5 + 10 * j] for j in range(0,4) for i in range(0,4)],
                "pieces": {
                    "x": {"image": "swans/x.png", "scale": 8}, 
                    "o": {"image": "swans/o.svg", "scale": 6}
                },
                "sounds": {
                    "x": "animals/dragon.mp3",
                    "o": "animals/swan.mp3"
                },
                "animationType": "simpleSlidePlaceRemove"
            }
        }
    }

def get_forestfox(variant_id):
    pieces = {
        "a": "bell1", "b": "bell2", "c": "bell3", "d": "bell4", "e": "bell5", 
        "f": "key1", "g": "key2", "h":"key3", "i": "key4", "j": "key5", 
        "k": "moon1", "l": "moon2", "m": "moon3", "n": "moon4", "o": "moon5", 
        "0": "num0", "1": "num1", "2": "num2", "3": "num3", "4": "num4",
        "5": "num5", "6": "num6", "7": "num7"
    }
        
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [1150, 900],
                "backgroundImage": "forestfox/cardboard.svg",
                "arrowWidth": 2,
                "defaultMoveTokenRadius": 6.5,
                "centers": [
                    [125, 150], [275, 150], [425, 150], [575, 150], [725, 150], [875, 150], [1025, 150],
                    [125, 750], [275, 750], [425, 750], [575, 750], [725, 750], [875, 750], [1025, 750],
                    [575, 450], [200, 450], [950, 450], [425, 450], [725, 450]
                ], # decree card, first card, second card, 1st score, 2nd score
                "pieces": {k: {"image": "forestfox/{}.svg".format(v), "scale": 200} for (k, v) in pieces.items()}
            }
        }
    }
    
def get_euclidsgame(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [10, 10],
                "backgroundImage": "euclidsgame/EuclidBoard.svg",
                "centers": [[0.5 + i, 0.5 + j] for j in range(10) for i in range(10)] + [[2.5 + k, 10.5] for k in range(6)],
                "pieces": {
                    "X": {"image": "euclidsgame/cut.svg", "scale": 0.9},
                }
            }
        }
    }

def get_ghost(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [25, 25],
                "backgroundImage": "ghost/gray_background.svg",
                "centers": [[0.5 + i, 2.5] for i in range(25)] + [[1 + i, 2.5] for i in range(24)] + [[6.5 + 2 * i, 7.5] for i in range(7)] + [[6.5 + 2 * i, 9.5] for i in range(7)] + [[6.5 + 2 * i, 11.5] for i in range(7)] + [[8.5 + 2 * i, 13.5] for i in range(5)],
                "pieces": {
                    f"{letter}": {
                        "image": f"general/{letter.upper()}.svg", "scale": 1 if letter.isupper() else 2
                    } for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "naiveInterpolate"
            }
        }
    }

def get_slide5(variant_id):
    return {
        "defaultTheme": "basic",
        "themes": {
            "basic": {
                "backgroundGeometry": [300, 300],
                "foregroundImage": "slide5/foreground5x5.svg",
                "centers": [
                    [50, 175], [75, 200], [100, 225], [125, 250], [150, 275],
                    [75, 150], [100, 175], [125, 200], [150, 225], [175, 250],
                    [100, 125], [125, 150], [150, 175], [175, 200], [200, 225],
                    [125, 100], [150, 125], [175, 150], [200, 175], [225, 200],
                    [150, 75], [175, 100], [200, 125], [225, 150], [250, 175],
                    [5, 130], [35, 160], [30, 105], [60, 135], [55, 80], [85, 110], [80, 55], [110, 85], [105, 30], [135, 60],
                    [195, 30], [165, 60], [220, 55], [190, 85], [245, 80], [215, 110], [270, 105], [240, 135], [295, 130], [265, 160]
                ],
                "arrowWidth": 5,
                "pieces": {
                    "X": { "image": "connect4/X.svg", "scale": 33 }, 
                    "O": { "image": "connect4/O.svg", "scale": 33 }
                },
                "sounds": {"x": "general/remove.mp3"},
                "animationType": "naiveInterpolate"
            }
        }
    }

def get_konane(variant_id):
    pieces = {
        "x": {"image": "general/blackpiece.svg", "scale": 9},
        "o": {"image": "general/whitepiece.svg", "scale": 9}
    }
    if variant_id == "4x4":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [40, 40],
                    "backgroundImage": "konane/grid4x4.svg",
                    "defaultMoveTokenRadius": 1.5,
                    "centers": [[5+10*i, 5+10*j] for j in range(0,4) for i in range(0,4)],
                    "pieces": pieces
                }
            }
        }
    elif variant_id == "4x5":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [50, 40],
                    "backgroundImage": "konane/grid4x5.svg",
                    "defaultMoveTokenRadius": 1.5,
                    "centers": [[5+10*i, 5+10*j] for j in range(0,4) for i in range(0,5)],
                    "pieces": pieces
                }
            }
        }
    elif variant_id == "5x5":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [50, 50],
                    "backgroundImage": "konane/grid5x5.svg",
                    "defaultMoveTokenRadius": 1.5,
                    "centers": [[5+10*i, 5+10*j] for j in range(0,5) for i in range(0,5)],
                    "pieces": pieces
                }
            }
        }
    
    elif variant_id == "5x6":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [60, 50],
                    "backgroundImage": "konane/grid5x6.svg",
                    "defaultMoveTokenRadius": 1.5,
                    "centers": [[5+10*i, 5+10*j] for j in range(0,5) for i in range(0,6)],
                    "pieces": pieces
                }
            }
        }
    elif variant_id == "6x6":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [60, 60],
                    "backgroundImage": "konane/grid6x6.svg",
                    "defaultMoveTokenRadius": 1.5,
                    "centers": [[5+10*i, 5+10*j] for j in range(0,6) for i in range(0,6)],
                    "pieces": pieces
                }
            }
        }
   
def get_yote(variant_id):
    pieces = {
        "0": {"image": "general/0.svg", "scale": 9},
        "1": {"image": "general/1.svg", "scale": 9},
        "2": {"image": "general/2.svg", "scale": 9},
        "3": {"image": "general/3.svg", "scale": 9},
        "B": {"image": "general/blackpiece.svg", "scale": 9},
        "W": {"image": "general/whitepiece.svg", "scale": 9}
    }
    if variant_id == "3x3":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [30, 40],
                    "backgroundImage": "yote/grid3x3.svg",
                    "centers": [[5, 5], [25, 5], [100, 100], [100, 100],[100, 100],[100, 100],[100, 100]]+
                                [[5+10*i, 15+10*j] for j in range(0,3) for i in range(0,3)],
                    "pieces": pieces
                }
            }
        }
    elif variant_id == "3x4":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [40, 40],
                    "backgroundImage": "yote/grid3x4.svg",
                    "centers": [[5, 5], [35, 5], [100, 100], [100, 100],[100, 100],[100, 100],[100, 100]]+
                                [[5+10*i, 15+10*j] for j in range(0,3) for i in range(0,4)],
                    "pieces": pieces
                }
            }
        }
    elif variant_id == "4x4":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [40, 50],
                    "backgroundImage": "yote/grid4x4.svg",
                    "centers": [[5, 5], [35, 5], [100, 100], [100, 100],[100, 100],[100, 100],[100, 100]]+
                                [[5+10*i, 15+10*j] for j in range(0,4) for i in range(0,4)],
                    "pieces": pieces
                }
            }
        }
    
def get_adugo(variant_id):
    pieces = {
        "B": {"image": "general/blackpiece.svg", "scale": 9},
        "W": {"image": "general/whitepiece.svg", "scale": 9}
    }
    if variant_id == "5x5":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [50, 50],
                    "backgroundImage": "adugo/grid5x5.svg",
                    "centers": [[100, 100]]+
                                [[5+10*i, 5+10*j] for j in range(0,5) for i in range(0,5)],
                    "pieces": pieces
                }
            }
        }
    elif variant_id == "3x3":
        return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [30, 30],
                    "backgroundImage": "adugo/grid3x3.svg",
                    "centers": [[100, 100]]+
                                [[5+10*i, 5+10*j] for j in range(0,3) for i in range(0,3)],
                    "pieces": pieces
                }
            }
        }

"""
===== STEP 2 ===== 
Add your function to the autoGUIv2DataFuncs dict.
"""

image_autogui_data_funcs = {
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