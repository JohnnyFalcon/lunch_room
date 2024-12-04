# Dodatkowe funkcjonalności

## Funkcje dodatkowe (V2)
- Reset hasła w widoku logowania za pomocą linku otrzymanego e-mail'em
- Link aktywacyjny wysyłany na podany e-mail podczas rejestracji - użytkownik musi kliknąć żeby aktywować konto i móc się zalogować
- Przy zakładaniu sesji każdy z wybranych użytkowników lub należący do wybranych grup użytkowników otrzymuje maila z linkiem do utworzonej sesji obiadowej. Po otwarciu linku od razu może składać zamówienie (jeśli jest zalogowany)

## Własne rozszerzenia i usprawnienia

### System uprawnień dla widoków
Przygotowanie i zdefiniowanie customowych uprawnień dla każdego widoku (permissions.py)

### Zaawansowany system uprawnień dla sesji obiadowych
Wprowadzono zaawansowany system uprawnień pozwalający na elastyczne zarządzanie dostępem do sesji. Kreator sesji automatycznie otrzymuje uprawnienia managera. Dodatkowo zaimplementowano możliwość przypisania roli managera dla wybranych użytkowników poprzez konfigurację w bazie danych, co pozwala im na wykonywanie wszystkich operacji kreatora w ramach danej sesji.

### Automatyzacja zadań przy użyciu Celery
Cykliczne odpytywanie i aktualizacja statusu sesji w bazie danych