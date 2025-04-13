# Study group

- Sovelluksessa käyttäjät pystyvät luomaan tai liittymään mukaan valmiiksi perustettuun opiskeluryhmään. Ryhmän ilmoituksessa lukee jäsenten määrä ja ryhmän haluttu maksimikoko.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen opiskeluryhmiä. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään opiskeluryhmiä.
- Käyttäjä näkee sovellukseen lisätyt opiskeluryhmät. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät opiskeluryhmät.
- Käyttäjä pystyy etsimään opiskeluryhmiä hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä opiskeluryhmiä.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja hänen ryhmänsä.
- Käyttäjä pystyy valitsemaan ryhmälle yhden tai useamman luokittelun (esim. tietokannat, algoritmit, lineaarialgebra).
- Käyttäjä pystyy liittymään opiskeluryhmiin. Ryhmän ilmoituksessa näytetään ryhmän jäsenet.

## Toiminnallisuus - Välipalautus 3

Tavoitteena on, että sovelluksessa on ainakin seuraavat toiminnot:

:white_check_mark: Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

:white_check_mark: Käyttäjä pystyy lisäämään tietokohteita

:white_check_mark: Käyttäjä pystyy muokkaamaan ja poistamaan tietokohteita.

:white_check_mark: Käyttäjä näkee sovellukseen lisätyt tietokohteet.

:white_check_mark: Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.

:white_check_mark: Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tietokohteet.

:white_check_mark: Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.

:white_square_button: Käyttäjä pystyy lähettämään toisen käyttäjän tietokohteeseen liittyen jotain lisätietoa, joka tulee näkyviin sovelluksessa.

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
