import constants
from tqdm import tqdm
from datetime import datetime

def prepare_data():
    print(f"{datetime.now() : %H:%M:%S}\tKonvertování zdrojových souborů pro lepší manipulaci.")
    for year in tqdm(range(constants.START_YEAR, constants.END_YEAR + 1), leave=False, desc="Upravování souborů: ", unit=" souborů", mininterval=0.01):

        #otevreme soubor pro cteni
        with open(constants.SOURCE_FILENAME.format(year=year), "r", encoding="utf-8") as input:
            lines = input.readlines()

        filtered_lines = []
        for line in lines:
            line = line.strip().split(",")
            for column in line:
                if column == "" or column == '""':
                    #pokud ano, radek do upraveneho souboru nezapisujeme
                    break
            else:
                #pokud maji vsechny sloupce data, radek ulozime
                filtered_lines.append(",".join(line))
            
        with open(constants.EDITED_FILENAME.format(year=year), "w", encoding='utf-8') as output:
            for line in filtered_lines:
                print(line, file=output)

    folder = constants.EDITED_FILENAME.rsplit("/", maxsplit=1)[0]
    print(f"{datetime.now() : %H:%M:%S}\tKonverze {len(range(constants.START_YEAR, constants.END_YEAR + 1))} souborů dokončena, výsledné soubory jsou ve složce '{folder}'.\n")
            

                

if __name__ == "__main__":
    prepare_data()