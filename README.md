# Printbox - zadanie rekrutacyjne Obiadomat 
![Obiadomat Thumbnail](static/obiadomat_thumb.png)

<div style="
  color: #333; 
  background-color: #21b573; 
  padding: 15px; 
  border-radius: 8px; 
  font-size: 1.2em; 
  line-height: 1.5em; 
  font-weight: bold; 
  text-align: center;
">
  ℹ️ Na wstępie zaznaczam, że nie wykorzystamy tego kodu w firmie. Chcemy, żeby przykład był życiowy, aby przyjemniej rozwiązywało się zadanie, a nie jakąś totalną abstrakcję.
</div>

## Wskazówki 📋
Projekt może wydawać się duży, szczególnie że można dodawać własne elementy. Jest to celowe, ponieważ zostawiona jest przestrzeń na wykazanie się. 

W wymaganiach znajdziesz:

- **Wersja MVP:** Powinna być zakodowana w całości oraz wystawiona w sieci.
- **Wersja V2:** Sugerowane rozszerzenia.
- **Wersja V3:** Zależy od Ciebie 🙂

Jeśli zastanawiasz się, z czego możesz skorzystać przy pracy nad projektem, to są tylko dwa wymagania:

- Użyty framework to **Django**.
- Prosimy o samodzielną pracę, tj. nie proszenie osób trzecich o **kodowanie** zadania.

Nie stawiamy ograniczeń co do wykorzystywania bibliotek zewnętrznych, innych technologii (np. JavaScript) czy narzędzi wspomagających pracę dewelopera.

Pamiętaj, że jakość pisanej aplikacji powinna pozwolić w przyszłości na bezpieczne dodawanie kolejnych funkcji, bez ryzyka zepsucia istniejących.


## Jak złożyć projekt?

> **⚠️ Uwaga!** Dodawaj commity w tym repozytorium, nie musisz tworzyć nowego. Pamiętaj o dodawaniu commitów w czasie pracy nad projektem. Jeden wielki commit na koniec pracy nie wystarczy.

**Dokumentacja**  
Dołącz do repozytorium dodatkową dokumentację z opisem, jeśli dodajesz coś od siebie do aplikacji.

**Wymagania MVP/V2**  
Jeśli nie spełniłaś/spełniłeś wszystkich wymagań z MVP lub V2 w wymaganym czasie, ale masz coś działającego, również prosimy o przesłanie.

**Hosting aplikacji**🌐  
Wystaw aplikację w sieci za pomocą [Render](https://render.com/) i zamieść link w tym miejscu. Nazwą aplikacji niech będzie nazwa repo np `recr-py-24q4-RM-400` 
Link do aplikacji: https://app-yxxf.onrender.com

Tipy:
- Najprościej jest wykorzystać integrację z GitHub, tj. zalogować się do aplikacji render.com wykorzystując konto GitHub. Po zaakceptowaniu na githubie zaproszenia do tego projektu oraz dodaniu konfiguracji w render.com (poprowadzi Cię domyślnie) będzie on widoczny do wyboru przy wystawianiu nowego Web Service.
- Oczywiście wybierz darmowe rozwiązania. render.com po pewnym czasie braku aktywności usypia aplikacje, więc czasem potrzeba kilkudziesięciu sekund, aby wystartowała ponownie. W między czasie możesz widzieć błędy.
- Jest sporo dokumentacji oraz tutoriali jak to zrobić, więc nawet jeśli to Twoja pierwsza aplikacja w sieci, to powinno być łatwe 🙂


**Konto administratora**  
W aplikacji istnieją 2 konta administratora powiązane z mailami `bob@getprintbox.com`, `stefan@getprintbox.com`  
Hasło do obu: `printbox`

**Czas na wykonanie zadania**  
Zadanie powinno zająć kilka godzin pracy, nie dajemy górnego limitu. Czas na wykonanie zadania to 7 dni liczone od momentu wysłania zaproszenia.

Pamiętaj o spełnieniu wszystkich wymagań przed upływem wyznaczonego terminu. Zachęcamy do kreatywności i eksploracji różnych rozwiązań. Powodzenia! 🚀


<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>Obiadomat - opis oraz wymagania</h1>
    <div class="description">
        <h2>Jaki problem rozwiązuje?</h2>
        <p>Wyobraź sobie, że chcesz grupowo zamówić jedzenie (np. w pracy, na uczelni). Jak przebiega proces?</p>
        <ul>
            <li>Jest wybrana jedna osoba, która zorganizuje zamówienie (zwana dalej organizatorem)</li>
            <li>Ustalasz miejsce, z którego zamawiacie jedzenie</li>
            <li>Każdy musi wybrać co chce zamówić, po czym przekazać informacje do organizatora</li>
            <li>Organizator zwykle płaci za całe zamówienie (dla uproszczenia ewentualnych sytuacji brzegowych zakładamy, że organizator zawsze płaci za zamówienie)</li>
            <li>Grupa rozlicza się z organizatorem, trzeba policzyć wszystkie koszty (posiłek, opakowania, koszt dostawy) oraz puścić bliczka do organizatora</li>
        </ul>
        <p>Jest sporo niedogodności, które sprawiają, że za każdym razem tracony jest czas, szczególnie podczas rozliczeń. Zwykle przy większej ilości osób tworzą się podgrupki, które chcą zamówić jedzenie z różnych miejsc. Czasem dostawa jest też obostrzona minimalną wartością zamówienia, więc trzeba zebrać informacje o potencjalnych zamówieniach.</p>
        <h2>Jak Obiadomat upraszcza cały proces?</h2>
        <p>W aplikacji jest możliwość przez osobę z odpowiednimi uprawnieniami dodawać jadłodajnie, dania oraz ich ceny. Jedna osoba otwiera tzw sesję obiadową, do której zaprasza wybranych użytkowników. W takiej sesji jest określone miejsce zamówienia, czas dostawy obiadu oraz czas, do którego można wybierać posiłki. Zaproszeni użytkownicy wybierają swój posiłek oraz ilość porcji (tak, niektórzy jedzą 2 obiady 😛). Definiują również formę rozliczenia. Twórca sesji ma możliwość podglądu raportu, w którym jest podsumowanie zamówień wszystkich użytkowników oraz sumaryczny koszt. Pozostaje tylko złożyć zamówienie 🤤</p>
    </div>
    <table>
        <thead>
            <tr>
                <th>Numer</th>
                <th>Funkcjonalność</th>
                <th>Wersja</th>
                <th>Wymagania</th>
            </tr>
        </thead>
        <tbody>
            <!-- Rejestracja, logowanie, obsługa konta -->
            <tr>
                <td rowspan="11">1</td>
                <td rowspan="11">Rejestracja, logowanie, obsługa konta</td>
                <td>MVP</td>
                <td>istnieje formularz do rejestracji (imię, nazwisko, email, hasło)</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>jest możliwość zalogowania do aplikacji</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>wszystkie funkcje wymienione poniżej są dostępne po zalogowaniu w aplikacji</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>na głównej stronie przed zalogowaniem wyświetlany jest formularz do logowania</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>po zalogowaniu użytkownik jest przekierowany do listy sesji obiadowych</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>po wejściu na url widoku dostępnego po zalogowaniu, następuje przekierowanie na stronę logowania np chcesz wejść na liste sesji obiadowych bez zalogowania → przekierowanie do logowania</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>jest możliwość zmiany hasła oraz pozostałych danych użytkownika w profilu użytkownika</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>do profilu przechodzisz poprzez pasek zakładek (patrz punkt 3)</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>jest możliwość resetu hasła w widoku logowania za pomocą linku otrzymanego e-mail’em</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>na podany e-mail podczas rejestracji przychodzi link aktywacyjny, który użytkownik musi kliknąć żeby aktywować konto i móc się zalogować</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>administrator może dezaktywować konto wybranego użytkownika, nie jest możliwe logowanie kiedy konto jest dezaktywowane</td>
            </tr>
            <!-- Grupy i uprawnienia użytkowników -->
            <tr>
                <td rowspan="5">2</td>
                <td rowspan="5">Grupy i uprawnienia użytkowników</td>
                <td>MVP</td>
                <td>wykorzystaj adminkę django</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>istnieją 3 typy użytkowników: admin, manager, customer</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>administrator może definiować grupy użytkowników</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>administrator może nadawać uprawnienia managera innym użytkownikom</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>nowi użytkownicy otrzymują domyślnie typ: customer</td>
            </tr>
            <!-- Pasek zakładek -->
            <tr>
                <td rowspan="6">3</td>
                <td rowspan="6">Pasek zakładek</td>
                <td>MVP</td>
                <td>na każdej stronie (oprócz logowania/rejestracji) w aplikacji wyświetlany jest ten sam pasek zakładek</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>na pasku zakładek w zależności od uprawnień mogą pojawić się: Jadłodajnia, Sesje Obiadowe, Profil użytkownika</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>przejście do definiowania jadłodajni widoczne tylko dla administratora oraz managerów</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>przejście do listy sesji obiadowych, dostępne dla wszystkich użytkowników</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>przejście do profilu użytkownika, dostępne dla wszystkich użytkowników</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>Saldo kredytowe (patrz punkt 9)</td>
            </tr>
            <!-- Definiowanie jadłodajni -->
            <tr>
                <td rowspan="4">4</td>
                <td rowspan="4">Definiowanie jadłodajni</td>
                <td>MVP</td>
                <td>istnieje osobny widok na definiowanie jadłodajni</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>jadłodajnia zawiera swoją nazwe, adres oraz telefon kontaktowy</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>w jadłodajni definiowane są posiłki, które posiadają swoją nazwe oraz cenę</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>można dodawać/edytować/usuwać posiłki oraz ich cenę</td>
            </tr>
            <!-- Lista sesji obiadowych -->
            <tr>
                <td rowspan="8">5</td>
                <td rowspan="8">Lista sesji obiadowych</td>
                <td>MVP</td>
                <td>wyświetlone są tylko sesje obiadowe, do których użytkownik został zaproszony lub utworzone przez niego</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>na górze listy znajdują się aktywne sesje</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>aktywne sesje wyróżniają się wizualnie od pozostałych starszych (historycznych) sesji na liście oraz posiadają przycisk do składania zamówienia</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>na stronie z listą sesji znajduje się przycisk na dodanie nowej sesji obiadowej</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>na liście sesji jest wyświetlane ile pieniędzy wydał w danej sesji</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>na liście sesji użytkownik ma informacje, które sesje założył</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>na liście sesji użytkownik widzi, w których sesjach brał udział. Zaproszenie nie jest równoznaczne z braniem udziału, ponieważ mógł nie złożyć zamówienia</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>pod paskiem zakładek, a przed listą sesji obiadowej widnieje podsumowanie ile pieniędzy użytkownik wydał w ramach wszystkich zamówień</td>
            </tr>
            <!-- Tworzenie oraz edycja sesji obiadowej -->
            <tr>
                <td rowspan="6">6</td>
                <td rowspan="6">Tworzenie oraz edycja sesji obiadowej</td>
                <td>MVP</td>
                <td>dowolony użytkownik może utworzyć sesje obiadową, której definicja składa się z nazwy sesji obiadowej, wyboru spośród wcześniej zdefiniowanych jadłodajni przez administratora lub managera, czas dostawy obiadu, czas, do którego można składać oraz edytować zamówienia oraz definicji użytkowników/wyboru grup, którzy zostaną dołączeni do sesji obiadowej (tutaj wybór z zdefiniowanych grup przez administratora, np po wyborze zdefiniowanej wcześniej grupy “PY-dev”, wszyscy jej członkowie mają dostęp do sesji obiadowej)</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>twórca sesji ma możliwość edycji wszystkich wyżej wymienionych ustawień sesji</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>twórca sesji jest również uczestnikiem sesji i może złożyć swoje zamówienie</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>twórca sesji ma możliwości edycji zamówień innych użytkowników złożonych w ramach sesji obiadowej. Może zmienić posiłek oraz ilość porcji</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>przy zakładaniu sesji każdy z wybranych użytkowników lub należący do wybranych grup użytkowników otrzymuje maila z linkiem do utworzonej sesji obiadowej. Po otwarciu linku od razu może składać zamówienie (jeśli jest zalogowany)</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>wysyłane są powiadomienia o edycji w zamówieniu lub sesji obiadowej. Przy edycji sesji obiadowej przez twórcę, każdy z zaproszonych użytkowników sesji obiadowej dostaje powiadomienie mailem z szczegółami wprowadzonych zmian w sesji obiadowej. Przy zmianach zamówienia konkretnego zamówienia użytkownika, powiadomienie mailowe otrzymuje tylko dany użytkownik. W mailu wymienione są wszystkie poczynione zmiany przez twórcę sesji</td>
            </tr>
            <!-- Składanie oraz edycja zamówienia przez użytkownika -->
            <tr>
                <td rowspan="9">7</td>
                <td rowspan="9">Składanie oraz edycja zamówienia przez użytkownika</td>
                <td>MVP</td>
                <td>po przejściu do dowolnej (aktywnej lub historczynej) sesji obiadowej z listy pojawia się nowy widok. Widoczne są nazwa sesji, czas, do którego można wybrać/edytować swoje zamówienie, czas dostawy obiadu, nazwa jadłodajni, podsumowanie kosztów dla wybranych dań oraz ilości porcji oraz wybrana forma zapłaty</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>po przejściu do aktywnej sesji obiadowej dodatkowo można wybrać dania należące do wybranej jadłodajni oraz ilość porcji. Widoczne jest cena, można wybrać formę zapłaty. Po wprowadzeniu informacji użytkownik potwierdza zamówienie przyciskiem `Save`</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>zaproszony użytkownik może złożyć tylko jedno zamówienie w ramach sesji</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>zaproszony użytkownik może złożyć/edytować swoje zamówienie do czasu zdefiniowanego w sesji obiadowej</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>przejście do edycji zamówienia jest za pomocą tego samego przycisku do składania zamówienia na liście sesji przy konkretnej aktywnej sesji obiadowej</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>po przejściu do edycji wyświetlaną są wszystkie zdefiniowane wcześniej wartości: dania i ilość porcji, szczegóły sesji wymienione powyżej, podsumowanie aktualnych kosztów. Po wprowadzonych zmian, użytkownik potwierdza zmiany przyciskiem `Save`</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>po upływie czasu, do którego można składać/edytować zamówienia, tylko twórca sesji może edytować poszczególne zamówienia użytkowników</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>zaproszony uzytkownik może anulować swoje zamówienie, jeśli nie upłynął czas na składanie/edycje zamówień zdefiniowany w sesji obiadowej. W edycji zamówienia jest dodatkowy przycisk na anulowanie zamówienia. Po anulowaniu zamówienia następuje przekierowanie do listy sesji obiadowych</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>użytkownik podczas składania zamówienia ma dodatkowe pole na “uwagi do zamówienia” np uwaga do kebaba “sos mieszany, mięso mieszane”</td>
            </tr>
            <!-- Podsumowanie zamówień uzytkowników -->
            <tr>
                <td rowspan="9">8</td>
                <td rowspan="9">Podsumowanie zamówień uzytkowników</td>
                <td>MVP</td>
                <td>twórca sesji ma możliwość podglądnięcia raportu z sesji obiadowej</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>przycisk do przejście do raportu jest widoczny dla twórcy sesji na liście sesji przy konkretnej utworzonej przez niego sesji obiadowej</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>po naciśnięciu przycisku jest przejście do strony z podsumowaniem sesji obiadowej. Widać tutaj informacje: nazwa sesji, czas, do którego można wybrać/edytować swoje zamówienie, czas dostawy obiadu, nazwa jadłodajni, telefon kontaktowy</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>jest sekcja z zamówionymi posiłkami użytkowników, wylistowane są wszystkie zamówione posiłki oraz ich porcje per użytkownik. Dla każdego użytkownika podana jest podsumowana wartość jaką musi zapłacić za swoje zamówienie</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>w osobnej sekcji w podsumowaniu zaagregowane są te same posiłki oraz ilość zamówionych porcji. Np. jeśli 2 osoby zamówią pierogi po jednej porcji, to w tej sekcji pojawia się jeden wpis pierogi 2 porcje</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>na końcu jest podsumowanie z podaną wartością do zapłaty za wszystkie wybrane posiłki</td>
            </tr>
            <tr>
                <td>MVP</td>
                <td>wszystkie części raportu są widoczne na tej samej stronie</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>pojawiają sie w raporcie uwagi do zamówień od użytkowników, patrz punkt 7</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>po upłynięciu czasu pozwalającego na złożenie/edycje zamówienia na adres mailowy twórcy sesji przychodzi powiadomienie z linkiem do raportu z podsumowaniem</td>
            </tr>
            <!-- Nowa forma płatności: kredyt -->
            <tr>
                <td rowspan="5">9</td>
                <td rowspan="5">Nowa forma płatności: kredyt</td>
                <td>V2</td>
                <td>Jak działa kredyt? Kredyt to forma rozliczenia między użytkownikami polegająca na tym, że twórca sesji zamawia posiłki, ale koszty nie są zwracana do twórcy sesji, tj użytkownik zamawia posiłek na kredyt. Następnie zakredytowany użytkownik kolejnego dnia może utworzyć sesje obiadową, zaprosić organizatora poprzedniej sesji, u którego jest zakredytowany. Poprzedni organizator zamawiając posiłek również wybiera kredyt jako forme zapłaty. Płatności się znoszą (nie jest wymagane żeby były identyczne), saldo pomiędzy danymi użytkownikami jest wyliczane na podstawie historycznych sesji oraz zamówień. Zauważ, że saldo kredytu musi być w tej sytuacji wyliczane między twórcami sesji i wszystkimi użytkownikami, którzy byli zaproszeni do ich sesji i wybrali kredyt jako formę płatności</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>przy składaniu zamówienia jest dostępna nowa forma płatności: kredyt</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>w pasku zakładek jest nowa zakładka “Saldo kredytowe” dostępna dla wszystkich użytkowników</td>
            </tr>
            <tr>
                <td>V2</td>
                <td>w nowym widoku są wylistowani wszyscy użytkownicy, którzy mają względem zalogowanego użytkownika niezerowe saldo kredytowe. Dodatnie, jeśli ktoś ma kredyt u zalogowanego użytkownika, tzn nie zwrócił mu wcześniej pieniędzy. Ujemne, jeśli to zalogowany użytkownik nie zwrócił pieniędzy innemu twórcy sesji</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
