"""
===== STEP 1 ===== 
Create a function that returns AutoGUIv2 Data for your game, given a variant of that game.
Return None if no AutoGUIv2 Data for the given variant.

get_<game>(variant_id) should return JSON of the following form:

    {
        "defaultTheme": <name of default theme>,
        "themes": {
            <name of theme1>: {
                "backgroundGeometry": [<width>, <height>],
                "backgroundImage": <path to background image; if no background image, omit this attribute>,
                "foregroundImage": <path to foreground image; if no foreground image, omit this attribute>,
                "centers": [ [<x0>,<y0>], [<x1>, <y1>], [<x2>, <y2>], [<x3>, <y3>], ... ]
                "pieces": {
                    <char1>: {
                        "image": <path to piece image>,
                        "scale": <image scale>
                    },
                    <char2>: {
                        ...    
                    }
                    ...
                }
            },
            <name of theme2>: {
                ...
            },
            ...
        }
    }

EXAMPLE:

    def get_ttt(variant_id):
        if variant_id == "regular":
            data = {
                "defaultTheme": "simple",
                "themes": {
                    "simple": {
                        "backgroundGeometry": [30, 30],
                        "backgroundImage": "ttt/background.svg",
                        "centers": [ [5, 5], [15, 5], [25, 5], [5, 15], [15, 15], [25, 15], [5, 25], [15, 25], [25, 25] ],
                        "pieces": {
                            "x": {"image": "ttt/x.svg", "scale": 1.0},
                            "o": {"image": "ttt/x.svg", "scale": 1.0}
                        }
                    }
                }
            }
            return data
        else:
            return None


(Scroll all the way down for Step 2).

"""

def get_baghchal(variant_id):
    return {
        "regular": {
            "defaultTheme": "stolen_art",
            "themes": {
                "stolen_art": {
                    "backgroundGeometry": [6, 7],
                    "backgroundImage": "baghchal/grid5Diag.svg",
                    "centers": [[1 + (i % 5), 1 + (i // 5)] for i in range(25)] + [[3.3,5.7], [3.5,5.7], [-1,-1], [3.4,6.1], [3.6,6.1]],
                    "pieces": {
                        "G": {
                            "image": "baghchal/G.png",
                            "scale": 0.75
                        },
                        "T": {
                            "image": "baghchal/T.png",
                            "scale": 0.75
                        },
                        "-": {
                            "image": "baghchal/-.svg",
                            "scale": 0.75
                        },
                        "0": {
                            "image": "baghchal/0.svg",
                            "scale": 1.3
                        },
                        "1": {
                            "image": "baghchal/1.svg",
                            "scale": 1.3
                        },
                        "2": {
                            "image": "baghchal/2.svg",
                            "scale": 1.3
                        },
                        "3": {
                            "image": "baghchal/3.svg",
                            "scale": 1.3
                        },
                        "4": {
                            "image": "baghchal/4.svg",
                            "scale": 1.3
                        },
                        "5": {
                            "image": "baghchal/5.svg",
                            "scale": 1.3
                        },
                        "6": {
                            "image": "baghchal/6.svg",
                            "scale": 1.3
                        },
                        "7": {
                            "image": "baghchal/7.svg",
                            "scale": 1.3
                        },
                        "8": {
                            "image": "baghchal/8.svg",
                            "scale": 1.3
                        },
                        "9": {
                            "image": "baghchal/9.svg",
                            "scale": 1.3
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_3spot(variant_id):
    return {
        "regular": {
            "defaultTheme": "standard",
            "themes": {
                "standard": {
                    "backgroundGeometry": [
                        3,
                        4
                    ],
                    "backgroundImage": "3spot/grid.svg",
                    "centers": [
                        [
                            0.5,
                            0.5
                        ],
                        [
                            1,
                            0.5
                        ],
                        [
                            1.5,
                            0.5
                        ],
                        [
                            2,
                            0.5
                        ],
                        [
                            2.5,
                            0.5
                        ],
                        [
                            0.5,
                            1
                        ],
                        [
                            1,
                            1
                        ],
                        [
                            1.5,
                            1
                        ],
                        [
                            2,
                            1
                        ],
                        [
                            2.5,
                            1
                        ],
                        [
                            0.5,
                            1.5
                        ],
                        [
                            1,
                            1.5
                        ],
                        [
                            1.5,
                            1.5
                        ],
                        [
                            2,
                            1.5
                        ],
                        [
                            2.5,
                            1.5
                        ],
                        [
                            0.5,
                            2.0
                        ],
                        [
                            1,
                            2.0
                        ],
                        [
                            1.5,
                            2.0
                        ],
                        [
                            2,
                            2.0
                        ],
                        [
                            2.5,
                            2.0
                        ],
                        [
                            0.5,
                            2.5
                        ],
                        [
                            1,
                            2.5
                        ],
                        [
                            1.5,
                            2.5
                        ],
                        [
                            2,
                            2.5
                        ],
                        [
                            2.5,
                            2.5
                        ],
                        [
                            0.3,
                            3.5
                        ],
                        [
                            0.7,
                            3.5
                        ],
                        [
                            -1,
                            -1
                        ],
                        [
                            2.3,
                            3.5
                        ],
                        [
                            2.7,
                            3.5
                        ]
                    ],
                    "pieces": {
                        "R": {
                            "image": "3spot/R.svg",
                            "scale": 1.0
                        },
                        "W": {
                            "image": "3spot/W.svg",
                            "scale": 1.0
                        },
                        "B": {
                            "image": "3spot/B.svg",
                            "scale": 1.0
                        },
                        "h": {
                            "image": "3spot/h.svg",
                            "scale": 0.3
                        },
                        "v": {
                            "image": "3spot/v.svg",
                            "scale": 0.3
                        },
                        "0": {
                            "image": "3spot/0.svg",
                            "scale": 2.0
                        },
                        "1": {
                            "image": "3spot/1.svg",
                            "scale": 2.0
                        },
                        "2": {
                            "image": "3spot/2.svg",
                            "scale": 2.0
                        },
                        "3": {
                            "image": "3spot/3.svg",
                            "scale": 2.0
                        },
                        "4": {
                            "image": "3spot/4.svg",
                            "scale": 2.0
                        },
                        "5": {
                            "image": "3spot/5.svg",
                            "scale": 2.0
                        },
                        "6": {
                            "image": "3spot/6.svg",
                            "scale": 2.0
                        },
                        "7": {
                            "image": "3spot/7.svg",
                            "scale": 2.0
                        },
                        "8": {
                            "image": "3spot/8.svg",
                            "scale": 2.0
                        },
                        "9": {
                            "image": "3spot/9.svg",
                            "scale": 2.0
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_369mm(variant_id):
    return {
        "regular": {
            "defaultTheme": "wikipedia",
            "themes": {
                "wikipedia": {
                    "backgroundGeometry": [
                        300,
                        300
                    ],
                    "backgroundImage": "369mm/board.svg",
                    "centers": [
                        [
                            145,
                            140
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            175,
                            140
                        ],
                        [
                            40,
                            20
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            160,
                            20
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            280,
                            20
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            80,
                            60
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            160,
                            60
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            240,
                            60
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            120,
                            100
                        ],
                        [
                            160,
                            100
                        ],
                        [
                            200,
                            100
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            40,
                            140
                        ],
                        [
                            80,
                            140
                        ],
                        [
                            120,
                            140
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            200,
                            140
                        ],
                        [
                            240,
                            140
                        ],
                        [
                            280,
                            140
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            120,
                            180
                        ],
                        [
                            160,
                            180
                        ],
                        [
                            200,
                            180
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            80,
                            220
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            160,
                            220
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            240,
                            220
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            40,
                            260
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            160,
                            260
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            280,
                            260
                        ]
                    ],
                    "pieces": {
                        "0": {
                            "image": "369mm/0.svg",
                            "scale": 100.0
                        },
                        "1": {
                            "image": "369mm/1.svg",
                            "scale": 100.0
                        },
                        "2": {
                            "image": "369mm/2.svg",
                            "scale": 100.0
                        },
                        "3": {
                            "image": "369mm/3.svg",
                            "scale": 100.0
                        },
                        "4": {
                            "image": "369mm/4.svg",
                            "scale": 100.0
                        },
                        "5": {
                            "image": "369mm/5.svg",
                            "scale": 100.0
                        },
                        "6": {
                            "image": "369mm/6.svg",
                            "scale": 100.0
                        },
                        "7": {
                            "image": "369mm/7.svg",
                            "scale": 100.0
                        },
                        "8": {
                            "image": "369mm/8.svg",
                            "scale": 100.0
                        },
                        "9": {
                            "image": "369mm/9.svg",
                            "scale": 100.0
                        },
                        "B": {
                            "image": "369mm/X.svg",
                            "scale": 130.0
                        },
                        "W": {
                            "image": "369mm/O.svg",
                            "scale": 130.0
                        },
                        "-": {
                            "image": "369mm/-.svg",
                            "scale": 1.0
                        }
                    }
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
                    "backgroundGeometry": [
                        3,
                        4
                    ],
                    "backgroundImage": "topitop/grid.svg",
                    "centers": [
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            0.5
                        ],
                        [
                            1.5,
                            0.5
                        ],
                        [
                            2.5,
                            0.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            1.5
                        ],
                        [
                            1.5,
                            1.5
                        ],
                        [
                            2.5,
                            1.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            2.5
                        ],
                        [
                            1.5,
                            2.5
                        ],
                        [
                            2.5,
                            2.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            1.5,
                            3.85
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.25,
                            3.15
                        ],
                        [
                            0.25,
                            3.85
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.8,
                            3.15
                        ],
                        [
                            0.8,
                            3.85
                        ],
                        [
                            1.5,
                            3.15
                        ],
                        [
                            1.5,
                            3.85
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            2.4,
                            3.15
                        ],
                        [
                            2.4,
                            3.85
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ]
                    ],
                    "pieces": {
                        "-": {
                            "image": "topitop/-.svg",
                            "scale": 1.0
                        },
                        "0": {
                            "image": "topitop/0.svg",
                            "scale": 1.0
                        },
                        "1": {
                            "image": "topitop/1.svg",
                            "scale": 1.0
                        },
                        "2": {
                            "image": "topitop/2.svg",
                            "scale": 1.0
                        },
                        "3": {
                            "image": "topitop/3.svg",
                            "scale": 1.0
                        },
                        "4": {
                            "image": "topitop/4.svg",
                            "scale": 1.0
                        },
                        "B": {
                            "image": "topitop/B.svg",
                            "scale": 1.0
                        },
                        "R": {
                            "image": "topitop/R.svg",
                            "scale": 1.0
                        },
                        "S": {
                            "image": "topitop/S.svg",
                            "scale": 1.0
                        },
                        "L": {
                            "image": "topitop/L.svg",
                            "scale": 1.0
                        },
                        "X": {
                            "image": "topitop/X.svg",
                            "scale": 1.0
                        },
                        "O": {
                            "image": "topitop/O.svg",
                            "scale": 1.0
                        },
                        "C": {
                            "image": "topitop/C.svg",
                            "scale": 1.0
                        },
                        "P": {
                            "image": "topitop/P.svg",
                            "scale": 1.0
                        },
                        "Q": {
                            "image": "topitop/Q.svg",
                            "scale": 1.0
                        },
                        "b": {
                            "image": "topitop/bb.svg",
                            "scale": 1.0
                        },
                        "r": {
                            "image": "topitop/rr.svg",
                            "scale": 1.0
                        },
                        "s": {
                            "image": "topitop/ss.svg",
                            "scale": 1.0
                        },
                        "l": {
                            "image": "topitop/ll.svg",
                            "scale": 1.0
                        }
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
                    "backgroundGeometry": [
                        4,
                        4
                    ],
                    "backgroundImage": "Lgame/grid.svg",
                    "centers": [
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            0.5
                        ],
                        [
                            1.5,
                            0.5
                        ],
                        [
                            2.5,
                            0.5
                        ],
                        [
                            3.5,
                            0.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            1.5
                        ],
                        [
                            1.5,
                            1.5
                        ],
                        [
                            2.5,
                            1.5
                        ],
                        [
                            3.5,
                            1.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            2.5
                        ],
                        [
                            1.5,
                            2.5
                        ],
                        [
                            2.5,
                            2.5
                        ],
                        [
                            3.5,
                            2.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.5,
                            3.5
                        ],
                        [
                            1.5,
                            3.5
                        ],
                        [
                            2.5,
                            3.5
                        ],
                        [
                            3.5,
                            3.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            0.15,
                            0.15
                        ],
                        [
                            1.15,
                            0.15
                        ],
                        [
                            2.15,
                            0.15
                        ],
                        [
                            0.15,
                            1.15
                        ],
                        [
                            1.15,
                            1.15
                        ],
                        [
                            2.15,
                            1.15
                        ],
                        [
                            1.85,
                            0.15
                        ],
                        [
                            2.85,
                            0.15
                        ],
                        [
                            3.85,
                            0.15
                        ],
                        [
                            1.85,
                            1.15
                        ],
                        [
                            2.85,
                            1.15
                        ],
                        [
                            3.85,
                            1.15
                        ],
                        [
                            3.85,
                            0.75
                        ],
                        [
                            3.85,
                            1.75
                        ],
                        [
                            3.85,
                            2.15
                        ],
                        [
                            2.85,
                            0.75
                        ],
                        [
                            2.85,
                            1.75
                        ],
                        [
                            2.85,
                            2.15
                        ],
                        [
                            3.375,
                            1.85
                        ],
                        [
                            3.375,
                            2.85
                        ],
                        [
                            3.375,
                            3.85
                        ],
                        [
                            2.375,
                            1.85
                        ],
                        [
                            2.375,
                            2.25
                        ],
                        [
                            2.85,
                            3.25
                        ],
                        [
                            3.85,
                            3.85
                        ],
                        [
                            2.85,
                            3.85
                        ],
                        [
                            1.85,
                            3.85
                        ],
                        [
                            3.85,
                            2.85
                        ],
                        [
                            2.85,
                            2.85
                        ],
                        [
                            1.85,
                            2.85
                        ],
                        [
                            2.15,
                            3.85
                        ],
                        [
                            1.15,
                            3.85
                        ],
                        [
                            0.15,
                            3.85
                        ],
                        [
                            2.15,
                            2.85
                        ],
                        [
                            1.15,
                            2.85
                        ],
                        [
                            0.15,
                            2.85
                        ],
                        [
                            0.625,
                            3.85
                        ],
                        [
                            0.625,
                            2.85
                        ],
                        [
                            0.625,
                            1.85
                        ],
                        [
                            1.15,
                            3.25
                        ],
                        [
                            1.625,
                            2.25
                        ],
                        [
                            1.625,
                            1.85
                        ],
                        [
                            0.15,
                            2.15
                        ],
                        [
                            0.15,
                            1.75
                        ],
                        [
                            0.15,
                            0.75
                        ],
                        [
                            1.15,
                            2.15
                        ],
                        [
                            1.15,
                            1.75
                        ],
                        [
                            1.15,
                            0.75
                        ]
                    ],
                    "pieces": {
                        "B": {
                            "image": "Lgame/B.svg",
                            "scale": 1.0
                        },
                        "R": {
                            "image": "Lgame/R.svg",
                            "scale": 1.0
                        },
                        "W": {
                            "image": "Lgame/S1.svg",
                            "scale": 1.0
                        },
                        "G": {
                            "image": "Lgame/S2.svg",
                            "scale": 1.0
                        },
                        "1": {
                            "image": "Lgame/L1.svg",
                            "scale": 0.6
                        },
                        "2": {
                            "image": "Lgame/L2.svg",
                            "scale": 0.6
                        },
                        "3": {
                            "image": "Lgame/L3.svg",
                            "scale": 0.6
                        },
                        "4": {
                            "image": "Lgame/L4.svg",
                            "scale": 0.6
                        },
                        "5": {
                            "image": "Lgame/L5.svg",
                            "scale": 0.6
                        },
                        "6": {
                            "image": "Lgame/L6.svg",
                            "scale": 0.6
                        },
                        "7": {
                            "image": "Lgame/L7.svg",
                            "scale": 0.6
                        },
                        "8": {
                            "image": "Lgame/L8.svg",
                            "scale": 0.6
                        }
                    }
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
                    "backgroundGeometry": [
                        4,
                        4
                    ],
                    "backgroundImage": "dodgem/grid.svg",
                    "centers": [
                        [
                            0.5,
                            0.5
                        ],
                        [
                            1.5,
                            0.5
                        ],
                        [
                            2.5,
                            0.5
                        ],
                        [
                            3.5,
                            0.5
                        ],
                        [
                            0.5,
                            1.5
                        ],
                        [
                            1.5,
                            1.5
                        ],
                        [
                            2.5,
                            1.5
                        ],
                        [
                            3.5,
                            1.5
                        ],
                        [
                            0.5,
                            2.5
                        ],
                        [
                            1.5,
                            2.5
                        ],
                        [
                            2.5,
                            2.5
                        ],
                        [
                            3.5,
                            2.5
                        ],
                        [
                            0.5,
                            3.5
                        ],
                        [
                            1.5,
                            3.5
                        ],
                        [
                            2.5,
                            3.5
                        ],
                        [
                            3.5,
                            3.5
                        ]
                    ],
                    "pieces": {
                        "x": {
                            "image": "dodgem/x.svg",
                            "scale": 1
                        },
                        "o": {
                            "image": "dodgem/o.svg",
                            "scale": 1
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_tttwo(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [
                        104,
                        124
                    ],
                    "backgroundImage": "tttwo/grid.svg",
                    "centers": [
                        [
                            12,
                            12
                        ],
                        [
                            32,
                            12
                        ],
                        [
                            52,
                            12
                        ],
                        [
                            72,
                            12
                        ],
                        [
                            92,
                            12
                        ],
                        [
                            12,
                            32
                        ],
                        [
                            32,
                            32
                        ],
                        [
                            52,
                            32
                        ],
                        [
                            72,
                            32
                        ],
                        [
                            92,
                            32
                        ],
                        [
                            12,
                            52
                        ],
                        [
                            32,
                            52
                        ],
                        [
                            52,
                            52
                        ],
                        [
                            72,
                            52
                        ],
                        [
                            92,
                            52
                        ],
                        [
                            12,
                            72
                        ],
                        [
                            32,
                            72
                        ],
                        [
                            52,
                            72
                        ],
                        [
                            72,
                            72
                        ],
                        [
                            92,
                            72
                        ],
                        [
                            12,
                            92
                        ],
                        [
                            32,
                            92
                        ],
                        [
                            52,
                            92
                        ],
                        [
                            72,
                            92
                        ],
                        [
                            92,
                            92
                        ],
                        [
                            12,
                            112
                        ],
                        [
                            92,
                            112
                        ],
                        [
                            999,
                            999
                        ],
                        [
                            999,
                            999
                        ],
                        [
                            52,
                            112
                        ]
                    ],
                    "pieces": {
                        "x": {
                            "image": "tttwo/a.svg",
                            "scale": 56.0
                        },
                        "o": {
                            "image": "tttwo/b.svg",
                            "scale": 56.0
                        },
                        "s": {
                            "image": "tttwo/s.svg",
                            "scale": 56.0
                        },
                        "X": {
                            "image": "tttwo/X.svg",
                            "scale": 16.0
                        },
                        "O": {
                            "image": "tttwo/O.svg",
                            "scale": 16.0
                        },
                        "-": {
                            "image": "tttwo/null.svg",
                            "scale": 1.0
                        },
                        "G": {
                            "image": "tttwo/s.svg",
                            "scale": 16.0
                        },
                        "0": {
                            "image": "tttwo/0.svg",
                            "scale": 50.0
                        },
                        "1": {
                            "image": "tttwo/1.svg",
                            "scale": 50.0
                        },
                        "2": {
                            "image": "tttwo/2.svg",
                            "scale": 50.0
                        },
                        "3": {
                            "image": "tttwo/3.svg",
                            "scale": 50.0
                        },
                        "4": {
                            "image": "tttwo/4.svg",
                            "scale": 50.0
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_stt(variant_id):
    return {
        "default": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [
                        9,
                        6
                    ],
                    "foregroundImage": "stt/foreground.svg",
                    "centers": [
                        [
                            3.5,
                            0.5
                        ],
                        [
                            4.5,
                            0.5
                        ],
                        [
                            5.5,
                            0.5
                        ],
                        [
                            3.5,
                            1.5
                        ],
                        [
                            4.5,
                            1.5
                        ],
                        [
                            5.5,
                            1.5
                        ],
                        [
                            0,
                            2.5
                        ],
                        [
                            1,
                            2.5
                        ],
                        [
                            2,
                            2.5
                        ],
                        [
                            2.5,
                            2.5
                        ],
                        [
                            3.5,
                            2.5
                        ],
                        [
                            4.5,
                            2.5
                        ],
                        [
                            5.5,
                            2.5
                        ],
                        [
                            6.5,
                            2.5
                        ],
                        [
                            7,
                            2.5
                        ],
                        [
                            8,
                            2.5
                        ],
                        [
                            9,
                            2.5
                        ],
                        [
                            0,
                            3.5
                        ],
                        [
                            1,
                            3.5
                        ],
                        [
                            2,
                            3.5
                        ],
                        [
                            2.5,
                            3.5
                        ],
                        [
                            3.5,
                            3.5
                        ],
                        [
                            4.5,
                            3.5
                        ],
                        [
                            5.5,
                            3.5
                        ],
                        [
                            6.5,
                            3.5
                        ],
                        [
                            7,
                            3.5
                        ],
                        [
                            8,
                            3.5
                        ],
                        [
                            9,
                            3.5
                        ],
                        [
                            0,
                            4.5
                        ],
                        [
                            1,
                            4.5
                        ],
                        [
                            2,
                            4.5
                        ],
                        [
                            2.5,
                            4.5
                        ],
                        [
                            3.5,
                            4.5
                        ],
                        [
                            4.5,
                            4.5
                        ],
                        [
                            5.5,
                            4.5
                        ],
                        [
                            6.5,
                            4.5
                        ],
                        [
                            7,
                            4.5
                        ],
                        [
                            8,
                            4.5
                        ],
                        [
                            9,
                            4.5
                        ],
                        [
                            2.5,
                            5.5
                        ],
                        [
                            6.5,
                            5.5
                        ],
                        [
                            3.5,
                            2.5
                        ],
                        [
                            4.5,
                            2.5
                        ],
                        [
                            5.5,
                            2.5
                        ],
                        [
                            3.5,
                            3.5
                        ],
                        [
                            4.5,
                            3.5
                        ],
                        [
                            5.5,
                            3.5
                        ],
                        [
                            3.5,
                            4.5
                        ],
                        [
                            4.5,
                            4.5
                        ],
                        [
                            5.5,
                            4.5
                        ]
                    ],
                    "pieces": {
                        "S": {
                            "image": "stt/S.svg",
                            "scale": 5.0
                        },
                        "x": {
                            "image": "stt/x.svg",
                            "scale": 1.0
                        },
                        "o": {
                            "image": "stt/o.svg",
                            "scale": 1.0
                        },
                        "-": {
                            "image": "stt/null.svg",
                            "scale": 1.0
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_tootnottopy(variant_id):
    return {
        "6": {
            "defaultTheme": "dan",
            "themes": {
                "dan": {
                    "backgroundGeometry": [
                        120,
                        70
                    ],
                    "backgroundImage": "tootnotto/board.svg",
                    "centers": [
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            35,
                            5
                        ],
                        [
                            45,
                            5
                        ],
                        [
                            55,
                            5
                        ],
                        [
                            65,
                            5
                        ],
                        [
                            75,
                            5
                        ],
                        [
                            85,
                            5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            5,
                            15
                        ],
                        [
                            15,
                            15
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            35,
                            15
                        ],
                        [
                            45,
                            15
                        ],
                        [
                            55,
                            15
                        ],
                        [
                            65,
                            15
                        ],
                        [
                            75,
                            15
                        ],
                        [
                            85,
                            15
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            105,
                            15
                        ],
                        [
                            115,
                            15
                        ],
                        [
                            5,
                            25
                        ],
                        [
                            15,
                            25
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            105,
                            25
                        ],
                        [
                            115,
                            25
                        ],
                        [
                            5,
                            35
                        ],
                        [
                            15,
                            35
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            35,
                            35
                        ],
                        [
                            45,
                            35
                        ],
                        [
                            55,
                            35
                        ],
                        [
                            65,
                            35
                        ],
                        [
                            75,
                            35
                        ],
                        [
                            85,
                            35
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            105,
                            35
                        ],
                        [
                            115,
                            35
                        ],
                        [
                            5,
                            45
                        ],
                        [
                            15,
                            45
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            35,
                            45
                        ],
                        [
                            45,
                            45
                        ],
                        [
                            55,
                            45
                        ],
                        [
                            65,
                            45
                        ],
                        [
                            75,
                            45
                        ],
                        [
                            85,
                            45
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            105,
                            45
                        ],
                        [
                            115,
                            45
                        ],
                        [
                            5,
                            55
                        ],
                        [
                            15,
                            55
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            35,
                            55
                        ],
                        [
                            45,
                            55
                        ],
                        [
                            55,
                            55
                        ],
                        [
                            65,
                            55
                        ],
                        [
                            75,
                            55
                        ],
                        [
                            85,
                            55
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            105,
                            55
                        ],
                        [
                            115,
                            55
                        ],
                        [
                            5,
                            65
                        ],
                        [
                            15,
                            65
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            35,
                            65
                        ],
                        [
                            45,
                            65
                        ],
                        [
                            55,
                            65
                        ],
                        [
                            65,
                            65
                        ],
                        [
                            75,
                            65
                        ],
                        [
                            85,
                            65
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            105,
                            65
                        ],
                        [
                            115,
                            65
                        ]
                    ],
                    "pieces": {
                        "v": {
                            "image": "tootnotto/v.svg",
                            "scale": 100.0
                        },
                        "T": {
                            "image": "tootnotto/T.svg",
                            "scale": 10.0
                        },
                        "O": {
                            "image": "tootnotto/O.svg",
                            "scale": 10.0
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_ctoi(variant_id):
    return {
        "regular": {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [
                        3,
                        4
                    ],
                    "backgroundImage": "ctoi/grid.svg",
                    "centers": [
                        [
                            0.5,
                            0.5
                        ],
                        [
                            1.5,
                            0.5
                        ],
                        [
                            2.5,
                            0.5
                        ],
                        [
                            0.5,
                            1.5
                        ],
                        [
                            1.5,
                            1.5
                        ],
                        [
                            2.5,
                            1.5
                        ],
                        [
                            0.5,
                            2.5
                        ],
                        [
                            1.5,
                            2.5
                        ],
                        [
                            2.5,
                            2.5
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            1,
                            3.4
                        ],
                        [
                            2,
                            3.4
                        ],
                        [
                            99,
                            99
                        ],
                        [
                            1,
                            3.8
                        ],
                        [
                            2,
                            3.8
                        ],
                        [
                            99,
                            99
                        ]
                    ],
                    "pieces": {
                        "R": {
                            "image": "ctoi/R.svg",
                            "scale": 1.0
                        },
                        "W": {
                            "image": "ctoi/W.svg",
                            "scale": 1.0
                        },
                        "T": {
                            "image": "ctoi/T.svg",
                            "scale": 1.0
                        },
                        "X": {
                            "image": "ctoi/X.svg",
                            "scale": 1.0
                        },
                        "t": {
                            "image": "ctoi/tt.svg",
                            "scale": 1.0
                        },
                        "x": {
                            "image": "ctoi/xx.svg",
                            "scale": 1.0
                        },
                        "Y": {
                            "image": "ctoi/X.svg",
                            "scale": 0.6
                        },
                        "Z": {
                            "image": "ctoi/T.svg",
                            "scale": 0.6
                        },
                        "y": {
                            "image": "ctoi/xx.svg",
                            "scale": 0.6
                        },
                        "z": {
                            "image": "ctoi/tt.svg",
                            "scale": 0.6
                        }
                    }
                }
            }
        }
    }.get(variant_id, None)

def get_chomp(variant_id):
    return {
        "3x2": {
            "defaultTheme": "choco",
            "themes": {
                "choco": {
                    "backgroundGeometry": [2, 3],
                    "centers": [
                        [0.5, 0.5],
                        [1.5, 0.5],
                        [0.5, 1.5],
                        [1.5, 1.5],
                        [0.5, 2.5],
                        [1.5, 2.5]
                    ],
                    "pieces": {
                        "x" : {
                            "image": "chomp/x.svg",
                            "scale": 1.0
                        }
                    }
                }
            }
        },
        "4x7": {
            "defaultTheme": "choco",
            "themes": {
                "choco": {
                    "backgroundGeometry": [7, 4],
                    "centers": [
                        [0.5, 0.5],
                        [1.5, 0.5],
                        [2.5, 0.5],
                        [3.5, 0.5],
                        [4.5, 0.5],
                        [5.5, 0.5],
                        [6.5, 0.5],
                        [0.5, 1.5],
                        [1.5, 1.5],
                        [2.5, 1.5],
                        [3.5, 1.5],
                        [4.5, 1.5],
                        [5.5, 1.5],
                        [6.5, 1.5],
                        [0.5, 2.5],
                        [1.5, 2.5],
                        [2.5, 2.5],
                        [3.5, 2.5],
                        [4.5, 2.5],
                        [5.5, 2.5],
                        [6.5, 2.5],
                        [0.5, 3.5],
                        [1.5, 3.5],
                        [2.5, 3.5],
                        [3.5, 3.5],
                        [4.5, 3.5],
                        [5.5, 3.5],
                        [6.5, 3.5]
                    ],
                    "pieces": {
                        "x" : {
                            "image": "chomp/x.svg",
                            "scale": 1.0
                        }
                    }
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
                    "b": {
                        "image": "dawsonschess/b.svg",
                        "scale": 1
                    },
                    "x": {
                        "image": "dawsonschess/x.svg",
                        "scale": 1
                    },
                    "o": {
                        "image": "dawsonschess/o.svg",
                        "scale": 1
                    }
                }
            }
        }
    }

def get_chess(variant_id):
    if variant_id != '7-man':
        return None
    pieces = {"K": "K", "Q": "Q", "R": "R", "B": "B", "N": "N", "P": "P", "k": "kk", "q": "qq", "r": "rr", "b": "bb", "n": "nn", "p": "pp"}
    return {
            "defaultTheme": "regular",
            "themes": {
                "regular": {
                    "backgroundGeometry": [8, 8],
                    "backgroundImage": "chess/grid.svg",
                    "centers": [[0.5 + (i % 8), 0.5 + (i // 8)] for i in range(64)],
                    "pieces": {k: {"image": "chess/{}.svg".format(v), "scale": 1} for (k, v) in pieces.items()}
                }
            }
        }

def get_snake(variant_id):
    if variant_id != "regular":
        return None
    return {
        "defaultTheme": "slither",
        "themes": {
            "slither": {
                "backgroundGeometry": [4, 4],
                "backgroundImage": "snake/background.svg",
                "centers": [[0.5 + i % 4, 0.5 + i // 4] for i in range(16)],
                "pieces": {
                    "b": {
                        "image": "snake/b.svg",
                        "scale": 1.0
                    },
                    "h": {
                        "image": "snake/h.svg",
                        "scale": 1.0
                    },
                    "t": {
                        "image": "snake/t.svg",
                        "scale": 1.0
                    }
                }
            }
        }
    }

def get_connect4c(variant_id):
    if variant_id == '6x6':
        return {
            "defaultTheme": "normal",
            "themes": {
                "normal": {
                    "backgroundGeometry": [6, 7],
                    "foregroundImage": "connect4/foreground6x6.svg",
                    "centers": [[0.5 + i // 6, 1.5 + i % 6] for i in range(36)] + [[0.5 + i, 0.5] for i in range(6)],
                    "pieces": {
                        "X": {
                            "image": "connect4/X.svg",
                            "scale": 1.0
                        },
                        "O": {
                            "image": "connect4/O.svg",
                            "scale": 1.0
                        },
                        "a": {
                            "image": "connect4/a.svg",
                            "scale": 0.8
                        }
                    }
                }
            }
        }
    elif variant_id == '6x7':
        return {
            "defaultTheme": "normal",
            "themes": {
                "normal": {
                    "backgroundGeometry": [7, 7],
                    "foregroundImage": "connect4/foreground6x7.svg",
                    "centers": [[0.5 + i // 6, 1.5 + i % 6] for i in range(42)] + [[0.5 + i, 0.5] for i in range(7)],
                    "pieces": {
                        "X": {
                            "image": "connect4/X.svg",
                            "scale": 1.0
                        },
                        "O": {
                            "image": "connect4/O.svg",
                            "scale": 1.0
                        },
                        "a": {
                            "image": "connect4/a.svg",
                            "scale": 0.8
                        }
                    }
                }
            }
        } 
    return None

"""
===== STEP 2 ===== 
Add your function to the autoGUIv2DataFuncs dict.
"""

autoGUIv2DataFuncs = {
    "baghchal": get_baghchal,
    "3spot": get_3spot,
    "369mm": get_369mm,
    "topitop": get_topitop,
    "Lgame": get_Lgame,
    "dodgem": get_dodgem,
    "tttwo": get_tttwo,
    "stt": get_stt,
    "tootnottopy": get_tootnottopy,
    "ctoi": get_ctoi,
    "chomp": get_chomp,
    "dawsonschess": get_dawsonschess,
    "chess": get_chess,
    "snake": get_snake,
    "connect4c": get_connect4c
}

def get_autoguiV2Data(game_id, variant_id):
    if game_id in autoGUIv2DataFuncs:
        return autoGUIv2DataFuncs[game_id](variant_id)
    return None