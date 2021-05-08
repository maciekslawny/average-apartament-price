from webscrape import *

city = ''
loaded = 'Nie'
data = 0
def menu():
    global city
    global data
    global loaded
    print(f'Wybrane miasto to: {city} | Wczytane dane: {loaded}')


    wybor = int(input("""
    1 - Wybierz miasto                        3 - Oblicz średnie ceny mieszkań
    2 - Pobierz dane mieszkań dla miasta      4 - Zakończ program 
    Wybór: """))

    if (wybor == 1):
        city = input('Nazwa miasta: ')
        print(f'Miasto {city} zostało wybrane')
        loaded = 'Nie'
        data = 0
        menu()
        
    elif(wybor == 2):
        print('Trwa pobieranie danych..')
        data = import_data(city)
        print('Dane zostały pobrane!')
        loaded = 'Tak'
        menu()
    elif(wybor == 3):
        print('Obliczanie średniej ceny za metr. Podaj wartości:')
        min_meters = int(input('Minimalna ilość metrów: '))
        max_meters = int(input('Max ilość metrów: '))
        average_price = count_medium_price(data, min_meters, max_meters)
        print(f'Średnia cena za metr kwadratowy w przedziale od {min_meters}m2 do {max_meters}m2 w mieście {city} wynosi = {average_price}PLN/m2')
        menu()
    elif(wybor == 4):
        print('Zamykanie programu..')
        return 0



    
menu()