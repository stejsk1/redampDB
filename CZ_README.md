# REDAMP
## Zprovoznění 
- execute `pip install -r requirements.txt`
- execute `python3 main.py`

### Údaje k databázi:
- user: postgres
- pw: redamp  
    - V souboru `main.py` ve třídě DataCollector se nachází údaje o připojení k databázi, v případě potřeby lze změnit proměnné k připojení do databáze.  
`self.data_handler = DatabaseHandler(
            dbname="postgres",
            user="postgres",
            password="redamp",
            host="localhost",
            port="5432",
        )`

## Teoretický test
Cesta k testu teorie se nachází v složce `doc`, která zároveň i obsahuje úvodní brainstorming projektu.

## O projektu
Obecně projekt slouží jako systém sběru a zpracování dat s následujícími klíčovými vlastnostmi:

- Autentizace: Projekt obsahuje autentizační mechanismus, který zajišťuje bezpečný přístup k datům a manipulaci s nimi a umožňuje interakci se systémem pouze oprávněným uživatelům.

- Stahování souborů: Umožňuje stahování souborů CSV ze zadaných adres URL. Stávající soubory jsou kontrolovány a na základě nově stažených dat je provedeno porovnání, zda je nutná aktualizace.

- Efektivní porovnávání a aktualizace dat: Zapomocí využití knihoven `numpy` a `pandas` projekt optimalizuje operace porovnávání dat. Efektivně porovnává stažená data CSV s existujícími záznamy v databázi `PostgreSQL` a identifikuje nové nebo aktualizované záznamy pro přesné a zjednodušené aktualizace.

- Získávání dat: Projekt usnadňuje načítání dat z databáze `PostgreSQL` a umožňuje uživatelům získat konkrétní informace na základě jejich požadavků.

- Protokolování a zpracování chyb: V průběhu shromažďování a zpracování dat projekt udržuje soubor protokolu, který zachycuje důležité události a případné chyby. Tento mechanismus protokolování pomáhá při řešení problémů a sledování výkonu systému.

- Profilování výkonu: Projekt obsahuje funkce profilování pro měření a analýzu výkonu úloh sběru a zpracování dat. Výsledky profilování se zaznamenávají do samostatného souboru, což vývojářům umožňuje identifikovat potenciální úzká místa a optimalizovat kód pro zvýšení efektivity.

Celkově projekt nabízí komplexní řešení pro automatizovaný sběr dat, efektivní porovnávání a aktualizaci záznamů v databázi `PostgreSQL`, bezproblémové vyhledávání dat, zaznamenávání událostí a chyb a profilování výkonu pro průběžnou optimalizaci.

## Závěr
Z důvodů, kdy mi bylo na pohovoru řečeno, že při zhotovení tohoto testu bych se měl doučit databáze,
rozhodl jsem se využít bodu "Everything else depends on your imagination" ze zadání a vytvořil jsem komplexnější strukturu než pouze tři tabulky.

Následující kód jsem vytvořil tak, aby se choval univerzálně pro urlhaus, alienvault a openphish, kde se využívají stejné funkce pro stahování a aktualizaci.

Průběh mého brainstormingu mi poskytl základní představu o tom, jak by tento projekt měl vypadat, ale během vývoje jsem ho musel několikrát přepracovat, abych dosáhl co největší efektivity.
Naštěstí mi znalosti knihovny pandas velmi usnadnily práci a pomohly mi optimalizovat kód.
* Pro prevenci SQL injection jsem preventivně využil parametrizaci, i když to není nejefektivnější forma ochrany.
* Pro prevenci Brute Force jsem také preventivně přidal autentizaci uživatele.





