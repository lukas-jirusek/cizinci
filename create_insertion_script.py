# tento soubor slouzi k prevedeni datoveho modelu v Pythonu do insertion scriptu.

from create_model import Model
import constants
from datetime import datetime

def create_insertion_script(filename = constants.SQL_INSERTION_SCRIPT):
    # pomoci modelu ziskame data vsech tabulek, bez duplikatu a tato data prevedeme na SQL INSERT prikazy
    model = Model().create()
    print(f"{datetime.now() : %H:%M:%S}\tVytváření insertion scriptu.")

    with open(filename, "w", encoding="utf-8") as output:
        for pohlavi in model.seznam_pohlavi.values():
            print(f'INSERT INTO pohlavi VALUES ({pohlavi.pohlavi_kod}, "{pohlavi.pohlavi_txt}");', file=output)
        print(file=output)

        for obcanstvi in model.seznam_obcanstvi.values():
            print(f'INSERT INTO obcanstvi VALUES ({obcanstvi.stobcan_kod}, "{obcanstvi.stobcan_txt}");', file=output)
        print(file=output)

        for vek in model.seznam_vek.values():
            print(f'INSERT INTO vek VALUES ({vek.vek_kod}, "{vek.vek_txt}");', file=output)
        print(file=output)
    
        for kraj in model.seznam_kraj.values():
            print(f'INSERT INTO kraj VALUES ({kraj.kraj_kod}, "{kraj.kraj_txt}");', file=output)
        print(file=output)

        for uzemi in model.seznam_uzemi.values():
            print(f'INSERT INTO uzemi VALUES ({uzemi.uzemi_kod}, "{uzemi.uzemi_txt}", {uzemi.kraj});', file=output)
        print(file=output)

        for zaznam in model.zaznamy:
            print(f'INSERT INTO zaznam VALUES ({zaznam.id}, {zaznam.hodnota}, {zaznam.rok}, {zaznam.pohlavi}, {zaznam.obcanstvi}, {zaznam.vek}, {zaznam.uzemi});', file=output)

    print(f"{datetime.now() : %H:%M:%S}\tInsertion script uložen do souboru: '{constants.SQL_INSERTION_SCRIPT}'\n")
        


    
if __name__ == "__main__":
    create_insertion_script()

