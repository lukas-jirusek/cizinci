DROP TABLE IF EXISTS pohlavi;
DROP TABLE IF EXISTS obcanstvi;
DROP TABLE IF EXISTS vek;
DROP TABLE IF EXISTS kraj;
DROP TABLE IF EXISTS uzemi;
DROP TABLE IF EXISTS zaznam;

CREATE TABLE pohlavi(
    pohlavi_kod INTEGER PRIMARY KEY,
    pohlavi_txt TEXT NOT NULL    
);

CREATE TABLE obcanstvi(
    stobcan_kod INTEGER PRIMARY KEY,
    stobcan_txt TEXT NOT NULL    
);

CREATE TABLE vek(
    vek_kod INTEGER PRIMARY KEY,
    vek_txt TEXT NOT NULL    
);

-- creation_script.sql (cast kodu)
CREATE TABLE kraj(
    kraj_kod INTEGER PRIMARY KEY,
    kraj_txt TEXT NOT NULL
);

CREATE TABLE uzemi(
    uzemi_kod INTEGER PRIMARY KEY,
    uzemi_txt TEXT NOT NULL,
    kraj_kod INTEGER NOT NULL
);

CREATE TABLE zaznam(
    id INTEGER PRIMARY KEY,
    hodnota INTEGER NOT NULL,
    rok INTEGER NOT NULL,
    pohlavi_kod INTEGER NOT NULL,
    obcanstvi_kod INTEGER NOT NULL,
    vek_kod INTEGER NOT NULL,
    uzemi_kod INTEGER NOT NULL
);