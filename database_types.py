from dataclasses import dataclass

@dataclass
class Pohlavi:
    pohlavi_kod: int        #kod pohlavi, 1 = muz, 2 = zena, pouzito jako klic
    pohlavi_txt: str        #retezec pohlavi: "muz" nebo "zena"

    def __init__(self, pohlavi_kod, pohlavi_txt):
        self.pohlavi_kod = pohlavi_kod
        self.pohlavi_txt = pohlavi_txt

@dataclass
class Obcanstvi:
    stobcan_kod: int        #kod obcanstvi, pr. Ukrajina: 804, pouzito jako klic
    stobcan_txt: str        #text obcanstvi, napr. "Alzirsko"

    def __init__(self, stobcan_kod, stobcan_txt):
        self.stobcan_kod = stobcan_kod
        self.stobcan_txt = stobcan_txt

#database_types.py (cast kodu)

@dataclass
class Vek:
    vek_kod: int            #kod veku, napr: 400000600005000, pouzito jako klic
    vek_txt: str            #vekove rozmezi jako text, napr. <0; 5)

    def __init__(self, vek_kod, vek_txt):
        self.vek_kod = vek_kod
        self.vek_txt = vek_txt

@dataclass
class Kraj:
    kraj_kod: int           #kod kraje: napr: 3069, pouzito jako klic
    kraj_txt: str           #nazev kraje: "Ústecký kraj"

    def __init__(self, kraj_kod, kraj_txt):
        self.kraj_kod = kraj_kod
        self.kraj_txt = kraj_txt

@dataclass
class Uzemi:
    uzemi_kod: int          #kod kraje: napr: 40509, pouzito jako klic
    uzemi_txt: str          #nazev kraje: "Teplice"
    kraj: Kraj              #kraj kde se Uzemi nachazi

    def __init__(self, uzemi_kod, uzemi_txt, kraj):
        self.uzemi_kod = uzemi_kod
        self.uzemi_txt = uzemi_txt
        self.kraj = kraj

@dataclass
class Zaznam:
    id: int                 #id zaznamu
    hodnota: int            #pocet cizincu v tomto zaznamu
    rok: int                #rok daneho zaznamu
    pohlavi: Pohlavi        #pohlavi cizincu daneho zaznamu
    obcanstvi: Obcanstvi    #obcanstvi cizincu daneho zaznamu
    vek: Vek                #vek cizincu v tomto zaznamu
    uzemi: Uzemi            #uzemi kde cizinci v tomto zaznamu ziji

    def __init__(self, id, hodnota, rok, pohlavi, obcanstvi, vek, uzemi):
        self.id = id
        self.hodnota = hodnota
        self.rok = rok
        self.pohlavi = pohlavi
        self.obcanstvi = obcanstvi
        self.vek = vek
        self.uzemi = uzemi
