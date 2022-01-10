import sqlite3
import constants
from tqdm import tqdm
import os

def confirm_to_clear(prompt = "Pokračujte zmáčknutím enteru."):
    input(prompt)
    os.system('cls' if os.name == 'nt' else 'clear')

def pohlavi_text(cursor: sqlite3.Cursor, pohlavi_kod):
    return cursor.execute(f"""
    SELECT pohlavi_txt 
    FROM pohlavi 
    WHERE pohlavi_kod = {pohlavi_kod};
    """).fetchone()[0]

def obcanstvi_text(cursor: sqlite3.Cursor, stobcan_kod):
    return cursor.execute(f"""
    SELECT stobcan_txt
    FROM obcanstvi
    WHERE stobcan_kod = {stobcan_kod};
    """).fetchone()[0]

def vek_text(cursor: sqlite3.Cursor, vek_kod):
    return cursor.execute(f"""
    SELECT vek_txt 
    FROM vek 
    WHERE vek_kod = {vek_kod};
    """).fetchone()[0]

def kraj_text(cursor: sqlite3.Cursor, kraj_kod):
    return cursor.execute(f"""
    SELECT kraj_txt 
    FROM kraj 
    WHERE kraj_kod = {kraj_kod};
    """).fetchone()[0]

def uzemi_text(cursor: sqlite3.Cursor, uzemi_kod):
    return cursor.execute(f"""
    SELECT uzemi_txt 
    FROM uzemi 
    WHERE uzemi_kod = {uzemi_kod};
    """).fetchone()[0]

def uzemi_kraj_text(cursor: sqlite3.Cursor, uzemi_kod):
    kraj_kod = cursor.execute(f"""
    SELECT kraj_kod 
    FROM uzemi 
    WHERE uzemi_kod = {uzemi_kod};
    """).fetchone()[0]

    return kraj_text(cursor, kraj_kod)

def oblast_info(cursor, oblast, oblast_type):
    oblast_txt = f"{' - Zvolená oblast: ':35}"
    if oblast:
        if oblast_type == "kraj":
            oblast_txt += f"{kraj_text(cursor, oblast)}"
        elif oblast_type == "uzemi":
            oblast_txt += f"{uzemi_text(cursor, oblast)} ({uzemi_kraj_text(cursor, oblast)})"
    else:
        oblast_txt += "Celá ČR"
    return oblast_txt

def obcanstvi_info(cursor, obcanstvi):
    obcanstvi_txt = f"{' - Zvolené občanství cizince: ':35}"
    if obcanstvi:
        obcanstvi_txt += obcanstvi_text(cursor, obcanstvi)
    else:
        obcanstvi_txt += "Jakékoli"
    return obcanstvi_txt

def rok_info(cursor, rok):
    rok_txt = f"{' - Zvolený rok: ':35}"
    if rok:
        rok_txt += str(rok)
    else:
        rok_txt += f"{constants.START_YEAR} - {constants.END_YEAR}"
    return rok_txt

def vek_text_to_vek(vek_txt):
    vek_txt = vek_txt[1:-1].split(",")
    vek_mensi = int(vek_txt[0].strip())
    vek_vetsi = vek_txt[1].strip()

    if vek_vetsi == "N":
        return vek_mensi + 2.5
    
    return (vek_mensi + int(vek_vetsi)) / 2

def pocet_info_silent(cursor, oblast = None, obcanstvi = None, rok = None, oblast_type = None):

    if not obcanstvi:
        obcanstvi = "obcanstvi_kod"
    
    if not rok:
        rok = "rok"

    

    if oblast and oblast_type == "kraj":
        sql_command = f"""
            SELECT SUM(hodnota)
            FROM zaznam 
            JOIN uzemi ON zaznam.uzemi_kod = uzemi.uzemi_kod
            WHERE kraj_kod = {oblast}
            AND rok = {rok}
            AND obcanstvi_kod = {obcanstvi}
            """
    else:
        if not oblast:
            oblast = "uzemi_kod"

        sql_command = f"""
            SELECT SUM(hodnota)
            FROM zaznam 
            WHERE uzemi_kod = {oblast}
            AND rok = {rok}
            AND obcanstvi_kod = {obcanstvi}
            """
    res = cursor.execute(sql_command).fetchone()[0]
    return res

def pocet_obcanstvi(cursor):
    return cursor.execute("SELECT COUNT(stobcan_kod) from obcanstvi;").fetchall()[0][0]

def pocet_info(cursor, oblast = None, obcanstvi = None, rok = None, oblast_type = None):
    tento_rok = pocet_info_silent(cursor, oblast, obcanstvi, rok, oblast_type)
    if rok == constants.START_YEAR:
        print(f"Celkový počet cizinců: {tento_rok}\n")
    else:
        minuly_rok = pocet_info_silent(cursor, oblast, obcanstvi, rok - 1, oblast_type)
        print(f"Celkový počet cizinců: {tento_rok}\t{tento_rok - minuly_rok :+} změna oproti roku {rok - 1}\n")

    

def vek_info(cursor, oblast = None, obcanstvi = None, rok = None, oblast_type = None):

    if not obcanstvi:
        obcanstvi = "obcanstvi_kod"
    
    if not rok:
        rok = "rok"

    

    if oblast and oblast_type == "kraj":
        sql_command = f"""
            SELECT vek_kod, SUM(hodnota)
            FROM zaznam 
            JOIN uzemi ON zaznam.uzemi_kod = uzemi.uzemi_kod
            WHERE kraj_kod = {oblast}
            AND rok = {rok}
            AND obcanstvi_kod = {obcanstvi}
            GROUP BY vek_kod
            ORDER BY vek_kod;
            """
    else:
        if not oblast:
            oblast = "uzemi_kod"
        sql_command = f"""
            SELECT vek_kod, SUM(hodnota)
            FROM zaznam 
            WHERE uzemi_kod = {oblast}
            AND rok = {rok}
            AND obcanstvi_kod = {obcanstvi}
            GROUP BY vek_kod
            ORDER BY vek_kod;
            """
    zaznamy = cursor.execute(sql_command).fetchall()
    veky = {vek_text(cursor, vek) : pocet for vek, pocet in zaznamy}

    print("Věkové složení:\n")
    print(f"\t{'Věkové rozmezí':17}| Počet")
    print(f"\t{'-' * 30}")
    for rozmezi, pocet in veky.items():
        print(f"\t{rozmezi:17}| {pocet}")

    prumerny_vek = sum(vek_text_to_vek(vek) * pocet for vek, pocet in veky.items()) / sum(veky.values())
    print(f"\n\tPrůměrný věk: {prumerny_vek:.1f}\n")

def pohlavi_info(cursor, oblast = None, obcanstvi = None, rok = None, oblast_type = None):

    if not obcanstvi:
        obcanstvi = "obcanstvi_kod"
    
    if not rok:
        rok = "rok"

    

    if oblast and oblast_type == "kraj":
        sql_command = f"""
            SELECT pohlavi_kod, SUM(hodnota)
            FROM zaznam 
            JOIN uzemi ON zaznam.uzemi_kod = uzemi.uzemi_kod
            WHERE kraj_kod = {oblast}
            AND rok = {rok}
            AND obcanstvi_kod = {obcanstvi}
            GROUP BY pohlavi_kod
            ORDER BY pohlavi_kod;
            """
    else:
        if not oblast:
            oblast = "uzemi_kod"
        sql_command = f"""
            SELECT pohlavi_kod, SUM(hodnota)
            FROM zaznam 
            WHERE uzemi_kod = {oblast}
            AND rok = {rok}
            AND obcanstvi_kod = {obcanstvi}
            GROUP BY pohlavi_kod
            ORDER BY pohlavi_kod;
            """
    zaznamy = cursor.execute(sql_command).fetchall()
    pohlavi_dict = {pohlavi_text(cursor, pohlavi) : pocet for pohlavi, pocet in zaznamy}

    print("Složení dle pohlaví:")
    print(f"\t{'Pohlaví':9}| {'Počet':8} | Procento")
    print(f"\t{'-' * 35}")
    for pohlavi, pocet in pohlavi_dict.items():
        print(f"\t{pohlavi:9}| {pocet:<8} | {(pocet * 100) / sum(pohlavi_dict.values()) : .2f} %")
    print()

def top_n_obcanstvi(cursor, rok=constants.END_YEAR):
    sql_command = f"""
        SELECT obcanstvi_kod, SUM(hodnota) AS suma
        FROM zaznam 
        WHERE rok = {rok}
        GROUP BY obcanstvi_kod
        ORDER BY SUM(hodnota) DESC LIMIT {constants.ROW_LIMIT}
        """
    
    return [obcan_kod[0] for obcan_kod in cursor.execute(sql_command)]
    



def tabulka_zvoleno_nic(cursor):
    obcanstvi = top_n_obcanstvi(cursor)
    table = [["", "SOUČET"] + [obcanstvi_text(cursor, obcan) for obcan in obcanstvi]]
    for rok in tqdm(range(constants.START_YEAR, constants.END_YEAR + 1), leave=False, desc="Vytváření tabulky: "):
        radek = [rok, pocet_info_silent(cursor, None, None, rok)]
        for obcan in obcanstvi:
            radek.append(pocet_info_silent(cursor, None, obcan, rok))
        table.append(radek)
    

    table = list(zip(*table))

    table.insert(2, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.insert(1, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.insert(0, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))

    print(f"Vývoj počtu cizinců v letech {constants.START_YEAR} - {constants.END_YEAR} (omezeno na {constants.ROW_LIMIT} občanství s nejvíce cizinci v roce {constants.END_YEAR}):")

    for row in table:
        print(f"{row[0]:30}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:8}", end = " |")
        print()
    
    print(f" + {pocet_obcanstvi(cursor) - len(obcanstvi)} dalších občanství")
    print()

def tabulka_zvolena_oblast(cursor, oblast, oblast_type):
    obcanstvi = top_n_obcanstvi(cursor)
    table = [["", "SOUČET"] + [obcanstvi_text(cursor, obcan) for obcan in obcanstvi]]
    for rok in tqdm(range(constants.START_YEAR, constants.END_YEAR + 1), leave=False, desc="Vytváření tabulky: "):
        radek = [rok, pocet_info_silent(cursor, oblast, None, rok, oblast_type)]
        for obcan in obcanstvi:
            radek.append(pocet_info_silent(cursor, oblast, obcan, rok, oblast_type))
        table.append(radek)
    

    table = list(zip(*table))

    table.insert(2, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.insert(1, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.insert(0, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))

    print(f"Vývoj počtu cizinců v letech {constants.START_YEAR} - {constants.END_YEAR} (omezeno na {constants.ROW_LIMIT} občanství s nejvíce cizinci v roce {constants.END_YEAR}):")

    for row in table:
        print(f"{row[0]:30}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:8}", end = " |")
        print()
    
    print(f" + {pocet_obcanstvi(cursor) - len(obcanstvi)} dalších občanství")
    print()

def seznam_kraju(cursor):
    sql_command = f"""
        SELECT kraj_kod
        FROM kraj 
        ORDER BY kraj_kod;
        """
    return [kraj_kod[0] for kraj_kod in cursor.execute(sql_command)]

def tabulka_zvolen_rok(cursor, rok):
    obcanstvi = top_n_obcanstvi(cursor, rok)
    table = [["", "SOUČET"] + [obcanstvi_text(cursor, obcan) for obcan in obcanstvi]]
    for kraj in tqdm(seznam_kraju(cursor), leave=False, desc="Vytváření tabulky: "):
        kraj_txt = kraj_text(cursor, kraj).replace("kraj", "").replace("Kraj", "").strip()
        if kraj_txt.startswith("Hlavní"):
            kraj_txt = "Praha"
        if len(kraj_txt) > 10:
            kraj_txt = kraj_txt[:8] + ".."
        radek = [kraj_txt, pocet_info_silent(cursor, kraj, None, rok, "kraj")]
        for obcan in obcanstvi:
            radek.append(pocet_info_silent(cursor, kraj, obcan, rok, "kraj"))
        table.append(radek)
    
    table = list(zip(*table))

    table.insert(2, tuple(["-" * 30] + ["-" * 10] * (len(table[0]) - 1)))
    table.insert(1, tuple(["-" * 30] + ["-" * 10] * (len(table[0]) - 1)))
    table.insert(0, tuple(["-" * 30] + ["-" * 10] * (len(table[0]) - 1)))

    print(f"Vývoj počtu cizinců v roce {rok} (omezeno na {constants.ROW_LIMIT} občanství s nejvíce cizinci v roce {rok}):")

    for row in table:
        print(f"{row[0]:30}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:>10}", end = " |")
        print()
    
    print(f" + {pocet_obcanstvi(cursor) - len(obcanstvi)} dalších občanství")
    print()

def tabulka_zvolene_obcanstvi(cursor, obcanstvi):

    """
           rok rok rok
    celkem
    kraj
    kraj
    """

    """
        celkem kraj kraj
    rok
    rok
    """

    table = [["", "SOUČET"] + [kraj_text(cursor, kraj) for kraj in seznam_kraju(cursor)]]
    for rok in tqdm(range(constants.START_YEAR, constants.END_YEAR + 1), leave=False, desc="Vytváření tabulky: "):
        radek = [rok, pocet_info_silent(cursor, None, obcanstvi, rok)]
        for kraj in seznam_kraju(cursor):
            radek.append(pocet_info_silent(cursor, kraj, obcanstvi, rok, "kraj"))
        table.append(radek)
    

    table = list(zip(*table))

    table.insert(2, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.insert(1, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.insert(0, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))
    table.append(tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))

    print(f"Vývoj počtu cizinců v letech {constants.START_YEAR} - {constants.END_YEAR}:")

    for row in table:
        print(f"{row[0]:30}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:8}", end = " |")
        print()
    print()


def tabulka_zvolana_oblast_rok(cursor, oblast, oblast_type, rok):
    constants.ROW_LIMIT *= 4

    obcanstvi = top_n_obcanstvi(cursor, rok)
    table = [["", "Počet"]]
    #print(list(obcanstvi_text(cursor, obcan) for obcan in obcanstvi))
    for obcan in obcanstvi:
        radek = [obcanstvi_text(cursor, obcan), pocet_info_silent(cursor, oblast, obcan, rok, oblast_type)]
        table.append(radek)

    table.insert(1, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))

    print(f"Nejpočetnější národnosti:")

    for row in table:
        print(f"{row[0]:30}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:>8}", end = " |")
        print()
    print(f" + {pocet_obcanstvi(cursor) - len(obcanstvi)} dalších občanství")
    print()

    constants.ROW_LIMIT //= 4

def tabulka_zvolana_oblast_obcanstvi(cursor, oblast, oblast_type, obcanstvi):
    table = [["", "Počet"]]
    for rok in range(constants.START_YEAR, constants.END_YEAR + 1):
        radek = [rok, pocet_info_silent(cursor, oblast, obcanstvi, rok, oblast_type)]
        table.append(radek)
    table = list(zip(*table))
    table.insert(1, tuple(["-" * 8] + ["-" * 8] * (len(table[0]) - 1)))

    print(f"Vývoj počtu cizinců:")

    for row in table:
        print(f"{row[0]:8}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:>8}", end = " |")
        print()
    print()

def tabulka_zvolen_rok_obcanstvi(cursor, rok, obcanstvi):

    table = [["", "Počet"]]
    #print(list(obcanstvi_text(cursor, obcan) for obcan in obcanstvi))
    for kraj in seznam_kraju(cursor):
        radek = [kraj_text(cursor, kraj), pocet_info_silent(cursor, kraj, obcanstvi, rok, "kraj")]
        table.append(radek)

    table.insert(1, tuple(["-" * 30] + ["-" * 8] * (len(table[0]) - 1)))

    print(f"Počet cizinců v jednotlivých krajích:")

    for row in table:
        print(f"{row[0]:30}", end = " |")
        for col in row[1:]:
            print(f"{col if col else 0:>8}", end = " |")
        print()
    print()




def perform_query(cursor, oblast = None, obcanstvi = None, rok = None, oblast_type = None):
    print("\nVýsledek dotazu vyhovující následujícím parametrům:\n")
    print(oblast_info(cursor, oblast, oblast_type))
    print(obcanstvi_info(cursor, obcanstvi))
    print(rok_info(cursor, rok))
    print()


    pocet_info(cursor, oblast, obcanstvi, rok if rok else constants.END_YEAR, oblast_type)

    vek_info(cursor, oblast, obcanstvi, rok if rok else constants.END_YEAR, oblast_type)

    pohlavi_info(cursor, oblast, obcanstvi, rok if rok else constants.END_YEAR, oblast_type)
    
    if oblast == None and obcanstvi == None and rok == None:
        tabulka_zvoleno_nic(cursor)
    elif oblast and obcanstvi == None and rok == None:
        tabulka_zvolena_oblast(cursor, oblast, oblast_type)
    elif oblast == None and obcanstvi == None and rok != None:
        tabulka_zvolen_rok(cursor, rok)
    elif oblast == None and obcanstvi != None and rok == None:
        tabulka_zvolene_obcanstvi(cursor, obcanstvi)
    elif oblast != None and obcanstvi == None and rok != None:
        tabulka_zvolana_oblast_rok(cursor, oblast, oblast_type, rok)
    elif oblast != None and obcanstvi != None and rok == None:
        tabulka_zvolana_oblast_obcanstvi(cursor, oblast, oblast_type, obcanstvi)
    elif oblast == None and obcanstvi != None and rok != None:
        tabulka_zvolen_rok_obcanstvi(cursor, rok, obcanstvi)

def vybrat_rok():
    while True:
        print("Vyberte rok pro dotaz:")
        print(f"\t0 - všechny roky ({constants.START_YEAR} - {constants.END_YEAR})")
        for index, rok in enumerate(range(constants.START_YEAR, constants.END_YEAR + 1), start=1):
            print(f"\t{index} - {rok}")
        print()
        response = input(f"Vyberte možnost <0 - {index}>: ")
        try:
            response = int(response)
        except ValueError:
            print("Neplatný vstup, zkuste to znova.\n")
            continue
        if response not in range(0, index + 1):
            print(f"Vstup musí být číslo mezi <0 - {index}>, zkuste to znova.\n")
            continue
        if response == 0:
            return None
        return response + constants.START_YEAR - 1

def vybrat_uzemi(cursor, kraj):
    kraj_kod, kraj_txt = kraj
    uzemi = cursor.execute(f"SELECT uzemi_kod, uzemi_txt FROM uzemi WHERE kraj_kod = {kraj_kod};").fetchall()
    while True:
        print("Vyberte oblast pro dotaz:")
        print(f"\t0 - celý {kraj_txt}")
        for index, uzemi_tup in enumerate(uzemi, start=1):
            print(f"\t{index} - {uzemi_tup[1]}")
        print()
        response = input(f"Vyberte možnost <0 - {index}>: ")
        try:
            response = int(response)
        except ValueError:
            print("Neplatný vstup, zkuste to znova.\n")
            continue
        if response not in range(0, index + 1):
            print(f"Vstup musí být číslo mezi <0 - {index}>, zkuste to znova.\n")
            continue
        if response == 0:
            return kraj_kod, "kraj"
        return uzemi[response - 1][0], "uzemi"


def vybrat_kraj(cursor):
    kraje = cursor.execute("SELECT kraj_kod, kraj_txt FROM kraj;").fetchall()
    while True:
        print("Vyberte oblast pro dotaz:")
        print(f"\t0 - celá ČR")
        for index, kraj in enumerate(kraje, start=1):
            print(f"\t{index} - {kraj[1]}")
        print()
        response = input(f"Vyberte možnost <0 - {index}>: ")
        try:
            response = int(response)
        except ValueError:
            print("Neplatný vstup, zkuste to znova.\n")
            continue
        if response not in range(0, index + 1):
            print(f"Vstup musí být číslo mezi <0 - {index}>, zkuste to znova.\n")
            continue
        if response == 0:
            return None, None
        return vybrat_uzemi(cursor, kraje[response - 1])
        
def vybrat_obcanstvi(cursor):
    constants.ROW_LIMIT *= 5
    obcanstvi = top_n_obcanstvi(cursor)
    constants.ROW_LIMIT /= 5
    while True:
        print("Vyberte občanství pro dotaz:")
        print(f"\t0 - jekékoli občanství")
        for index, obcan_kod in enumerate(obcanstvi, start=1):
            print(f"\t{index} - {obcanstvi_text(cursor, obcan_kod)}")
        print()
        response = input(f"Vyberte možnost <0 - {index}>: ")
        try:
            response = int(response)
        except ValueError:
            print("Neplatný vstup, zkuste to znova.\n")
            continue
        if response not in range(0, index + 1):
            print(f"Vstup musí být číslo mezi <0 - {index}>, zkuste to znova.\n")
            continue
        if response == 0:
            return None
        return obcanstvi[response - 1]

def zmenit_limit():
    while True:
        n = input("Zadejte nový limit: ")
        try:
            n = int(n)
        except ValueError:
            print("Neplatná hodnota, zkuste to znova.")
            continue
        if n < 0:
            print("Limit musí být pozitivní, zkuste to znova.")
            continue
        return n
        

def user_interface(cursor):
    oblast = None
    oblast_type = None
    obcanstvi = None
    rok = None
    while True:
        print("\nDatabáze cizinců.")
        print("\nJsou vybrány následující parametry:\n")
        print(oblast_info(cursor, oblast, oblast_type))
        print(obcanstvi_info(cursor, obcanstvi))
        print(rok_info(cursor, rok))

        print("\nVyberte z následujících možností:")
        print("1 - změnit vybrané území")
        print("2 - změnit vybrané občanství cizince")
        print("3 - změnit vybraný rok")
        print("4 - změnit limit počtu občanství ve výsledku dotazu")
        print("5 - provést dotaz s vybranými parametry")
        print("6 - ukončit program")

        response = input("\nZadejte možnost: ")

        if response == "1":
            oblast, oblast_type = vybrat_kraj(cursor)
        elif response == "2":
            obcanstvi = vybrat_obcanstvi(cursor)
        elif response == "3":
            rok = vybrat_rok()
        elif response == "4":
            constants.ROW_LIMIT = zmenit_limit()
        elif response == "5" or response == "":
            perform_query(cursor, oblast=oblast, obcanstvi=obcanstvi, rok=rok, oblast_type=oblast_type)
        elif response == "6":
            break
        else:
            print("Neplatná možnost.")
    
        confirm_to_clear()

    





if __name__ == "__main__":
    connection = sqlite3.connect(constants.DATABASE_FILENAME)
    cursor = connection.cursor()

    user_interface(cursor)

    connection.rollback()
    connection.close()
    """
    perform_query(cursor, oblast=None, obcanstvi=None, rok=None)

    perform_query(cursor, oblast=3123, obcanstvi=380, rok=None, oblast_type="kraj")
    perform_query(cursor, oblast=40215, obcanstvi=None, rok=2005, oblast_type="uzemi")
    perform_query(cursor, oblast=None, obcanstvi=804, rok=2019)

    perform_query(cursor, oblast=40924, obcanstvi=None, rok=None, oblast_type="uzemi")
    perform_query(cursor, oblast=None, obcanstvi=834, rok=None)
    perform_query(cursor, oblast=None, obcanstvi=None, rok=2015)

    perform_query(cursor, oblast=3093, obcanstvi=380, rok=2020, oblast_type="kraj")
    """

    