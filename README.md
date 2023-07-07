# REDAMP
## Zprovoznění 
- execute `pip install -r requirements.txt`
- execute `python3 main.py`

### Údaje k databázi:
- user: postgres
- pw: redamp  
Ve funkci `connect_to_database()` se nachází údaje o připojení k databázi, v případě potřeby lze změnit proměnné k připojení do databáze.

## Teoretický test
Cesta k testu teorie se nachází v složce `doc`, která zároveň i postupuje úvodní brainstorming.

## Závěr
Z důvodů, kdy mi bylo na pohovoru řečeno, že při zhotovení tohoto testu bych se měl doučit databáze,
rozhodl jsem se využít bodu "Everything else depends on your imagination" ze zadání a vytvořil jsem komplexnější strukturu než jen tři tabulky.

Následující kód jsem vytvořil tak, aby se choval univerzálně pro urlhaus, alienvault a openphish, kde se využívají stejné funkce pro stahování a aktualizaci.
Tabulky `urlhaus`, `alienvault` a `openphish` jsou propojeny s tabulkou `base` pomocí foreign klíčů. Tabulka `base` je řídící (nadřazená) tabulka,
ze které následně získávám další informace na základě `base_id` a `source` z ostatních tabulek.

Průběh mého brainstormingu mi poskytl základní představu o tom, jak by tento projekt měl vypadat, ale během vývoje jsem ho musel několikrát přepracovat, abych dosáhl co největší efektivity.
Naštěstí mi znalosti knihovny pandas velmi usnadnily práci a pomohly mi optimalizovat kód.
Pro prevenci SQL injection jsem preventivně využil parametrizaci, i když to není nejefektivnější forma ochrany.
Pro prevenci Brute Force jsem také preventivně přidal autentizaci uživatele.


