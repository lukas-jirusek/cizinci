# Tento soubor obsahuje konstanty pro dalsi vyuziti
# napriklad jsou zde ulozeny cesty ke zdrovojym datum ale i k souboru s databazi

# prvni a posledni rok s daty
START_YEAR = 2004
END_YEAR = 2020

# nazvy pro nexpracovane i zpracovane csv soubory
SOURCE_FILENAME = "source/CIZ01_{year}.csv"
EDITED_FILENAME = "edited/{year}.csv"

# nazev pro vyslednou databazi
DATABASE_FILENAME = "cizinci.db"

# nazvy creation a insertion scriptu
SQL_CREATION_SCRIPT = "sql/creation_script.sql"
SQL_INSERTION_SCRIPT = "sql/insertion_script.sql"

# kolik obcanstvi vypsat v tabulce
ROW_LIMIT = 10