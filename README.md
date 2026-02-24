# Portfolio kart kolekcjonerskich (Django)

## Start 
1) Sklonuj repo:
   git clone <URL>
   cd srod

2) Utwórz i aktywuj venv:
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate

3) Zainstaluj zależności:
   pip install -r requirements.txt

4) Uruchom:
   python manage.py runserver

Wejdź w przeglądarce:
- http://127.0.0.1:8000/
- admin: http://127.0.0.1:8000/admin/

## Konto admina to: kuba1 hasło: a

## Naszym projektem jest portfolio kart kolekcjonerskich.
## Mamy możliwość rejestracji, oraz logowania użytkowników.
## Wykonaliśmy projekt korzystając z django + python 3.14.3
## trzeba zainstalować pillow do obsługi pól ze zdjęciami - python -m pip install Pillow
## http://127.0.0.1:8000/   - adres naszej strony
## http://127.0.0.1:8000/admin - panel admina

## Strona główna
## przyciski przekierowujące do mojego portfolio są na środku oraz w prawym górnym rogu
## mamy oczywiście w prawym górnym rogu też możliwość wylogowania ze strony
## Lewy górny róg przekierowuje na stronę główną

## Moje Porfolio
## Obliczanie wartości kolekcji oraz ilości kart
## Możliwość dodania karty z perspektywy użytkownika
## możliwość usuniecia oraz edycji kart
## klikając na zdjęcie karty, możemy zobaczyć ją w pełnej okazałości
## aby użytkownik mogl dodac konkretną kartę, najpierw musi zostać utworzona w "cards" w panelu admina

## Panel Admina
## posiada dodatkową funkcję transakcje, z których zrezygnowaliśmy