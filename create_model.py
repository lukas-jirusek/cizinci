from database_types import Pohlavi, Obcanstvi, Vek, Kraj, Uzemi, Zaznam
import constants
from datetime import datetime

class Model:
    def __init__(self):
        # vytvoreni promennych pro jednotlive tabulky, tato data jsou pozdeji vyuzita k vytvoreni insertion scriptu
        self.seznam_pohlavi = {}
        self.seznam_obcanstvi = {}
        self.seznam_vek = {}
        self.seznam_kraj = {}
        self.seznam_uzemi = {}
        self.zaznamy = []
    
    def process_file(self, filename):
        with open(filename, "r", encoding="utf-8") as input:

            input.readline()
            for line in input:
                #maxsplit nastavujeme protoze atributa vek ve starsich datech obsahuje carku
                line = [value[1:-1] for value in line.strip().split(",", maxsplit=18)]  

                pohlavi_kod = int(line[4])
                stobcan_kod = int(line[6])
                vek_kod = int(line[8])
                kraj_kod = int(line[13])
                uzemi_kod = int(line[11])

                hodnota = int(line[1])
                rok = int(line[9])

                if pohlavi_kod not in self.seznam_pohlavi:
                    pohlavi_txt = line[16]
                    self.seznam_pohlavi[pohlavi_kod] = Pohlavi(pohlavi_kod, pohlavi_txt)
                
                if stobcan_kod not in self.seznam_obcanstvi:
                    stobcan_txt = line[17]
                    self.seznam_obcanstvi[stobcan_kod] = Obcanstvi(stobcan_kod, stobcan_txt)
                
                if vek_kod not in self.seznam_vek:
                    vek_txt = line[18]
                    self.seznam_vek[vek_kod] = Vek(vek_kod, vek_txt)
                
                if kraj_kod not in self.seznam_kraj:
                    kraj_txt = line[15]
                    self.seznam_kraj[kraj_kod] = Kraj(kraj_kod, kraj_txt)
                
                if uzemi_kod not in self.seznam_uzemi:
                    uzemi_txt = line[14]
                    self.seznam_uzemi[uzemi_kod] = Uzemi(uzemi_kod, uzemi_txt, kraj_kod)
                
                zaznam = Zaznam(len(self.zaznamy) + 1, hodnota, rok, pohlavi_kod, stobcan_kod, vek_kod, uzemi_kod)
                self.zaznamy.append(zaznam)

    def create(self):
        print(f"{datetime.now() : %H:%M:%S}\tVytváření modelu databáze v Pythonu.")
        for year in range(constants.START_YEAR, constants.END_YEAR + 1):
            print(f"{datetime.now() : %H:%M:%S}\tZpracovávání dat pro rok {year}.")
            self.process_file(constants.EDITED_FILENAME.format(year=year))

        print(f"{datetime.now() : %H:%M:%S}\tDatový model dokončen.\n")
        return self


if __name__ == "__main__":
    a = Model().create()
    print(len(a.zaznamy))
    print(len(a.seznam_kraj))
    print(a.seznam_vek)
    input("DONE")
                    
                    