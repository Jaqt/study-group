# Study group

- Sovelluksessa käyttäjät pystyvät luomaan tai liittymään mukaan valmiiksi perustettuun opiskeluryhmään. Ryhmän ilmoituksessa lukee jäsenten määrä ja ryhmän haluttu maksimikoko.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen opiskeluryhmiä. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään opiskeluryhmiä.
- Käyttäjä näkee sovellukseen lisätyt opiskeluryhmät. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät opiskeluryhmät.
- Käyttäjä pystyy lähettämään viestejä ryhmänsä sivulle ja näkee muiden käyttäjien lähettämät viestit.
- Käyttäjä pystyy etsimään opiskeluryhmiä hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä opiskeluryhmiä.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja hänen ryhmänsä.
- Käyttäjä pystyy valitsemaan ryhmälle yhden tai useamman luokittelun (esim. tietokannat, algoritmit, lineaarialgebra).
- Käyttäjä pystyy liittymään opiskeluryhmiin. Ryhmän ilmoituksessa näytetään ryhmän jäsenet.

## Sovelluksen asennus

Luo paikallinen repo komennolla `git clone git@github.com:Jaqt/study-group.git` ja siirry sen jälkeen hakemistoon.

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## Suuri tietomäärä

- Sovellusta on testattu suurella tietomäärällä (seed.py) ja parannuksia sovelluksen tehokkuuteen on tehty seuraavasti:
  1. **Sivutus** - Ryhmiä näytetään 10 kappaletta kerrallaan yhdellä sivulla.
  2. **Skeema** - Luotu indeksit tehostamaan ryhmän omistajien, jäsenten ja viestien hakuja.
- Testit suoritettiin 10 000 000 ryhmällä ja 10 000 000 viestillä.
- Ryhmäsivujen latausaika nopeutui 2-3 sekunnista sekunnin sadasosiin.
