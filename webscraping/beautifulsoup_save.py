from bs4 import BeautifulSoup
import requests
import time
import mysql.connector
from SQL_Daten import zugang as anbin
ort = 'lap'
database = 'numbeo'
mydb = mysql.connector.connect(
        host=anbin.host(ort),
        user=anbin.user(ort),
        passwd=anbin.passwd(ort),
        database=anbin.database(database),
        auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

my_cursor = mydb.cursor()
selection = ['Dresden','Frankfurt','Berlin','Hamburg','Nuremberg','Munich','Stuttgart','Dusseldorf','Heidelberg','Prague','Warsaw','Luxembourg']
#selection = ['Aachen','Cologne','Hanover','Karlsruhe']
#zeit = time.strftime("%Y-%m-%d %H:%M:%S")
#,'Mannheim'Mannheim
x = 1
def feching():
    for city in selection:

        url = f'https://www.numbeo.com/cost-of-living/in/{city}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', attrs={'class': 'data_wide_table new_bar_table'})
        rows = table.find_all('tr')
        """""""""
        --------------------------------------Meal, Inexpensive Restaurant--------------------------------------------------
        """""""""
        data = rows[1].text.split()
        fail = data.pop()
        if fail == '?':
            snack_price_raw = None
            snack_price_min = None
            snack_price_max = None
        else:
            snack_price_raw = data[3].replace(",", "")
            price_range = fail
            price_3 = price_range.split("-")
            snack_price_min = float(price_3[0])
            snack_price_max = float(price_3[1])

        """""""""
        --------------------------------------Meal for 2 People, Mid-range Restaurant, Three-course-------------------------
        """""""""
        data = rows[2].text.split()
        fail = data.pop()
        if fail == '?':
            meal_price_raw = None
            meal_price_max = None
            meal_price_min = None
        else:
            meal_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            meal_price_min = float(price_3[0])
            meal_price_max = float(price_3[1])

        """""""""
        --------------------------------------McMeal at McDonalds (or Equivalent Combo Meal)--------------------------------
        """""""""
        data = rows[3].text.split()
        fail = data.pop()
        if fail == '?':
            mcmeal_price_raw = None
            mcmeal_price_min = None
            mcmeal_price_max = None
        else:
            mcmeal_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            mcmeal_price_min = float(price_3[0])
            mcmeal_price_max = float(price_3[1])

        """""""""
        --------------------------------------Domestic Beer (0.5 liter draught)---------------------------------------------
        """""""""
        data = rows[4].text.split()
        fail = data.pop()
        if fail == '?':
            beer_home_price_raw = None
            beer_home_price_min = None
            beer_home_price_max = None
        else:
            beer_home_price_raw = data[5].replace(",", "")
            price_range = data[7].replace(",", "")
            price_3 = price_range.split("-")
            beer_home_price_min = float(price_3[0])
            beer_home_price_max = float(price_3[1])

        """""""""
        --------------------------------------Imported Beer (0.33 liter bottle)---------------------------------------------
        """""""""
        data = rows[5].text.split()
        fail = data.pop()
        if fail == '?':
            beer_import_price_raw = None
            beer_import_price_min = None
            beer_import_price_max = None
        else:
            beer_import_price_raw = data[5].replace(",", "")
            price_range = data[7].replace(",", "")
            price_3 = price_range.split("-")
            beer_import_price_min = float(price_3[0])
            beer_import_price_max = float(price_3[1])

        """""""""
        --------------------------------------Cappuccino (regular)----------------------------------------------------------
        """""""""
        data = rows[6].text.split()
        fail = data.pop()
        if fail == '?':
            cappuccino_price_raw = None
            cappuccino_price_min = None
            cappuccino_price_max = None
        else:
            cappuccino_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            cappuccino_price_min = float(price_3[0])
            cappuccino_price_max = float(price_3[1])

        """""""""
        --------------------------------------Coke/Pepsi (0.33 liter bottle)------------------------------------------------
        """""""""
        data = rows[7].text.split()
        fail = data.pop()
        if fail == '?':
            cola_price_raw = None
            cola_price_min = None
            cola_price_max = None
        else:
            cola_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            cola_price_min = float(price_3[0])
            cola_price_max = float(price_3[1])

        """""""""
        --------------------------------------Water (0.33 liter bottle) ----------------------------------------------------
        """""""""
        data = rows[8].text.split()
        fail = data.pop()
        if fail == '?':
            water_price_raw = None
            water_price_min = None
            water_price_max = None
        else:
            water_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            water_price_min = float(price_3[0])
            water_price_max = float(price_3[1])

        """""""""
        print(f'Snackpreis ist {snack_price_raw} mit einer Range von {snack_price_min} - {snack_price_max}')
        print(f'Mealpreis ist {meal_price_raw} mit einer Range von {meal_price_min} - {meal_price_max}')
        print(f'Mcpreis ist {mcmeal_price_raw} mit einer Range von {mcmeal_price_min} - {mcmeal_price_max}')
        print(f'Homebeerpreis ist {beer_home_price_raw} mit einer Range von {beer_home_price_min} - {beer_home_price_max}')
        print(f'Homebeerpreis ist {beer_import_price_raw} mit einer Range von {beer_import_price_min} - {beer_import_price_max}')
        print(f'Kaffepreis ist {cappuccino_price_raw} mit einer Range von {cappuccino_price_min} - {cappuccino_price_max}')
        print(f'Colapreis ist {cola_price_raw} mit einer Range von {cola_price_min} - {cola_price_max}')
        print(f'Mealpreis ist {water_price_raw} mit einer Range von {water_price_min} - {water_price_max}')
        """""""""

        """""""""
        --------------------------------------Milk (regular), (1 liter) ----------------------------------------------------
        """""""""
        data = rows[10].text.split()
        fail = data.pop()
        if fail == '?':
            milk_price_raw = None
            milk_price_min = None
            milk_price_max = None
        else:
            milk_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            milk_price_min = float(price_3[0])
            milk_price_max = float(price_3[1])

        """""""""
        --------------------------------------Loaf of Fresh White Bread (500g)  --------------------------------------------
        """""""""
        data = rows[11].text.split()
        fail = data.pop()
        if fail == '?':
            bread_price_raw = None
            bread_price_min = None
            bread_price_max = None
        else:
            bread_price_raw = data[6].replace(",", "")
            price_range = data[8].replace(",", "")
            price_3 = price_range.split("-")
            bread_price_min = float(price_3[0])
            bread_price_max = float(price_3[1])

        """""""""
        --------------------------------------Rice (white), (1kg)-----------------------------------------------------------
        """""""""
        data = rows[12].text.split()
        fail = data.pop()
        if fail == '?':
            rice_price_raw = None
            rice_price_min = None
            rice_price_max = None
        else:
            rice_price_raw = data[3].replace(",", "")
            price_range = data[5].replace(",", "")
            price_3 = price_range.split("-")
            rice_price_min = float(price_3[0])
            rice_price_max = float(price_3[1])

        """""""""
        --------------------------------------Eggs (regular) (12) ----------------------------------------------------------
        """""""""
        data = rows[13].text.split()
        fail = data.pop()
        if fail == '?':
            eggs_price_raw = None
            eggs_price_min = None
            eggs_price_max = None
        else:
            eggs_price_raw = data[3].replace(",", "")
            price_range = data[5].replace(",", "")
            price_3 = price_range.split("-")
            eggs_price_min = float(price_3[0])
            eggs_price_max = float(price_3[1])

        """""""""
        --------------------------------------Local Cheese (1kg)------------------------------------------------------------
        """""""""
        data = rows[14].text.split()
        fail = data.pop()
        if fail == '?':
            cheese_price_raw = None
            cheese_price_min = None
            cheese_price_max = None
        else:
            cheese_price_raw = data[3].replace(",", "")
            price_range = data[5].replace(",", "")
            price_3 = price_range.split("-")
            cheese_price_min = float(price_3[0])
            cheese_price_max = float(price_3[1])

        """""""""
        --------------------------------------Chicken Fillets (1kg) --------------------------------------------------------
        """""""""
        data = rows[15].text.split()
        fail = data.pop()
        if fail == '?':
            chicken_fillets_price_raw = None
            chicken_fillets_price_min = None
            chicken_fillets_price_max = None
        else:
            chicken_fillets_price_raw = data[3].replace(",", "")
            price_range = data[5].replace(",", "")
            price_3 = price_range.split("-")
            chicken_fillets_price_min = float(price_3[0])
            chicken_fillets_price_max = float(price_3[1])

        """""""""
        --------------------------------------Beef Round (1kg) (or Equivalent Back Leg Red Meat) ---------------------------
        """""""""
        data = rows[16].text.split()
        fail = data.pop()
        if fail == '?':
            beef_price_raw = None
            beef_price_min = None
            beef_price_max = None
        else:
            beef_price_raw = data[9].replace(",", "")
            price_range = data[11].replace(",", "")
            price_3 = price_range.split("-")
            beef_price_min = float(price_3[0])
            beef_price_max = float(price_3[1])

        """""""""
        --------------------------------------Apples (1kg) -----------------------------------------------------------------
        """""""""
        data = rows[17].text.split()
        fail = data.pop()
        if fail == '?':
            apples_price_raw = None
            apples_price_min = None
            apples_price_max = None
        else:
            apples_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            apples_price_min = float(price_3[0])
            apples_price_max = float(price_3[1])

        """""""""
        --------------------------------------Banana (1kg) -----------------------------------------------------------------
        """""""""
        data = rows[18].text.split()
        fail = data.pop()
        if fail == '?':
            banana_price_raw = None
            banana_price_min = None
            banana_price_max = None
        else:
            banana_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            banana_price_min = float(price_3[0])
            banana_price_max = float(price_3[1])

        """""""""
        --------------------------------------Oranges (1kg) ----------------------------------------------------------------
        """""""""
        data = rows[19].text.split()
        fail = data.pop()
        if fail == '?':
            oranges_price_raw = None
            oranges_price_min = None
            oranges_price_max = None
        else:
            oranges_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            oranges_price_min = float(price_3[0])
            oranges_price_max = float(price_3[1])

        """""""""
        --------------------------------------Tomato (1kg) -----------------------------------------------------------------
        """""""""
        data = rows[20].text.split()
        fail = data.pop()
        if fail == '?':
            tomato_price_raw = None
            tomato_price_min = None
            tomato_price_max = None
        else:
            tomato_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            tomato_price_min = float(price_3[0])
            tomato_price_max = float(price_3[1])

        """""""""
        --------------------------------------Potato (1kg) -----------------------------------------------------------------
        """""""""
        data = rows[21].text.split()
        fail = data.pop()
        if fail == '?':
            potato_price_raw = None
            potato_price_min = None
            potato_price_max = None
        else:
            potato_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            potato_price_min = float(price_3[0])
            potato_price_max = float(price_3[1])

        """""""""
        --------------------------------------Onion (1kg)-------------------------------------------------------------------
        """""""""
        data = rows[22].text.split()
        fail = data.pop()
        if fail == '?':
            onion_price_raw = None
            onion_price_min = None
            onion_price_max = None
        else:
            onion_price_raw = data[2].replace(",", "")
            price_range = data[4].replace(",", "")
            price_3 = price_range.split("-")
            onion_price_min = float(price_3[0])
            onion_price_max = float(price_3[1])

        """""""""
        --------------------------------------Lettuce (1 head) -------------------------------------------------------------
        """""""""
        data = rows[23].text.split()
        fail = data.pop()
        if fail == '?':
            lettuce_price_raw = None
            lettuce_price_min = None
            lettuce_price_max = None
        else:
            lettuce_price_raw = data[3].replace(",", "")
            price_range = data[5].replace(",", "")
            price_3 = price_range.split("-")
            lettuce_price_min = float(price_3[0])
            lettuce_price_max = float(price_3[1])

        """""""""
        --------------------------------------Water (1.5 liter bottle)------------------------------------------------------
        """""""""
        data = rows[24].text.split()
        fail = data.pop()
        if fail == '?':
            waterbottle_price_raw = None
            waterbottle_price_min = None
            waterbottle_price_max = None
        else:
            waterbottle_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            waterbottle_price_min = float(price_3[0])
            waterbottle_price_max = float(price_3[1])

        """""""""
        --------------------------------------Bottle of Wine (Mid-Range) ---------------------------------------------------
        """""""""
        data = rows[25].text.split()
        fail = data.pop()
        if fail == '?':
            wine_price_raw = None
            wine_price_min = None
            wine_price_max = None
        else:
            wine_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            wine_price_min = float(price_3[0])
            wine_price_max = float(price_3[1])

        """""""""
        --------------------------------------Domestic Beer (0.5 liter bottle)----------------------------------------------
        """""""""
        data = rows[26].text.split()
        fail = data.pop()
        if fail == '?':
            heimatbier_price_raw = None
            heimatbier_price_min = None
            heimatbier_price_max = None
        else:
            heimatbier_price_raw = data[5].replace(",", "")
            price_range = data[7].replace(",", "")
            price_3 = price_range.split("-")
            heimatbier_price_min = float(price_3[0])
            heimatbier_price_max = float(price_3[1])

        """""""""
        --------------------------------------Imported Beer (0.33 liter bottle) --------------------------------------------
        """""""""
        data = rows[27].text.split()
        fail = data.pop()
        if fail == '?':
            auslandsbier_price_raw = None
            auslandsbier_price_min = None
            auslandsbier_price_max = None
        else:
            auslandsbier_price_raw = data[5].replace(",", "")
            price_range = data[7].replace(",", "")
            price_3 = price_range.split("-")
            auslandsbier_price_min = float(price_3[0])
            auslandsbier_price_max = float(price_3[1])

        """""""""
        --------------------------------------Cigarettes 20 Pack (Marlboro) ------------------------------------------------
        """""""""
        data = rows[28].text.split()
        fail = data.pop()
        if fail == '?':
            cigarettes_price_raw = None
            cigarettes_price_min = None
            cigarettes_price_max = None
        else:
            cigarettes_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            cigarettes_price_min = float(price_3[0])
            cigarettes_price_max = float(price_3[1])

        """""""""
        print(f'Milchpreis ist {milk_price_raw} mit einer Range von {milk_price_min} - {milk_price_max}')
        print(f'Brotpreis ist {bread_price_raw} mit einer Range von {bread_price_min} - {bread_price_max}')
        print(f'Reispreis ist {rice_price_raw} mit einer Range von {rice_price_min} - {rice_price_max}')
        print(f'Eierpreis ist {eggs_price_raw} mit einer Range von {eggs_price_min} - {eggs_price_max}')
        print(f'Käsepreis ist {cheese_price_raw} mit einer Range von {cheese_price_min} - {cheese_price_max}')
        print(f'Hünchenpreis ist {chicken_fillets_price_raw} mit einer Range von {chicken_fillets_price_min} - {chicken_fillets_price_max}')
        print(f'Fleischpreis ist {beef_price_raw} mit einer Range von {beef_price_min} - {beef_price_max}')
        print(f'Äpfelpreis ist {apples_price_raw} mit einer Range von {apples_price_min} - {apples_price_max}')
        print(f'Bananenpreis ist {banana_price_raw} mit einer Range von {banana_price_min} - {banana_price_max}')
        print(f'Orangenpreis ist {oranges_price_raw} mit einer Range von {oranges_price_min} - {oranges_price_max}')
        print(f'Tomatenpreis ist {tomato_price_raw} mit einer Range von {tomato_price_min} - {tomato_price_max}')
        print(f'Kartoffelnpreis ist {potato_price_raw} mit einer Range von {potato_price_min} - {potato_price_max}')
        print(f'Zwiebelnpreis ist {onion_price_raw} mit einer Range von {onion_price_min} - {onion_price_max}')
        print(f'Lettucepreis ist {lettuce_price_raw} mit einer Range von {lettuce_price_min} - {lettuce_price_max}')
        print(f'Wasserpreis ist {waterbottle_price_raw} mit einer Range von {waterbottle_price_min} - {waterbottle_price_max}')
        print(f'Winepreis ist {wine_price_raw} mit einer Range von {wine_price_min} - {wine_price_max}')
        print(f'Heimatbierpreis ist {heimatbier_price_raw} mit einer Range von {heimatbier_price_min} - {heimatbier_price_max}')
        print(f'Auslandsbierpreis ist {auslandsbier_price_raw} mit einer Range von {auslandsbier_price_min} - {auslandsbier_price_max}')
        print(f'Zigarettenpreis ist {cigarettes_price_raw} mit einer Range von {cigarettes_price_min} - {cigarettes_price_max}')
        """""""""

        """""""""
        --------------------------------------One-way Ticket (Local Transport)----------------------------------------------
        """""""""
        data = rows[30].text.split()
        fail = data.pop()
        if fail == '?':
            ticket_price_raw = None
            ticket_price_min = None
            ticket_price_max = None
        else:
            ticket_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            ticket_price_min = float(price_3[0])
            ticket_price_max = float(price_3[1])

        """""""""
        --------------------------------------Monthly Pass (Regular Price) -------------------------------------------------
        """""""""
        data = rows[31].text.split()
        fail = data.pop()
        if fail == '?':
            monatskarte_price_raw = None
            monatskarte_price_min = None
            monatskarte_price_max = None
        else:
            monatskarte_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            monatskarte_price_min = float(price_3[0])
            monatskarte_price_max = float(price_3[1])

        """""""""
        --------------------------------------Taxi Start (Normal Tariff) ---------------------------------------------------
        """""""""
        data = rows[32].text.split()
        fail = data.pop()
        if fail == '?':
            taxi_start_price_raw = None
            taxi_start_price_min = None
            taxi_start_price_max = None
        else:
            taxi_start_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            taxi_start_price_min = float(price_3[0])
            taxi_start_price_max = float(price_3[1])

        """""""""
        --------------------------------------Taxi 1km (Normal Tariff) -----------------------------------------------------
        """""""""
        data = rows[33].text.split()
        fail = data.pop()
        if fail == '?':
            taxi_1km_price_raw = None
            taxi_1km_price_min = None
            taxi_1km_price_max = None
        else:
            taxi_1km_price_raw = data[4].replace(",", "")
            price_range = data[6].replace(",", "")
            price_3 = price_range.split("-")
            taxi_1km_price_min = float(price_3[0])
            taxi_1km_price_max = float(price_3[1])

        """""""""
        --------------------------------------Taxi 1hour Waiting (Normal Tariff) -------------------------------------------
        """""""""
        data = rows[34].text.split()
        fail = data.pop()
        if fail == '?':
            taxi_1h_price_raw = None
            taxi_1h_price_min = None
            taxi_1h_price_max = None
        else:
            taxi_1h_price_raw = data[5].replace(",", "")
            price_range = data[7].replace(",", "")
            price_3 = price_range.split("-")
            taxi_1h_price_min = float(price_3[0])
            taxi_1h_price_max = float(price_3[1])

        """""""""
        --------------------------------------Gasoline (1 liter)------------------------------------------------------------
        """""""""
        data = rows[35].text.split()
        fail = data.pop()
        if fail == '?':
            gasoline_price_raw = None
            gasoline_price_min = None
            gasoline_price_max = None
        else:
            gasoline_price_raw = data[3].replace(",", "")
            price_range = data[5].replace(",", "")
            price_3 = price_range.split("-")
            gasoline_price_min = float(price_3[0])
            gasoline_price_max = float(price_3[1])

        """""""""
        --------------------------------------Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car) ------------------
        """""""""
        data = rows[36].text.split()
        fail = data.pop()
        if fail == '?':
            vw_price_raw = None
            vw_price_min = None
            vw_price_max = None
        else:
            vw_price_raw = data[10].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            vw_price_min = float(price_3[0])
            vw_price_max = float(price_3[1])

        """""""""
        --------------------------------------Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car) ---------------
        """""""""
        data = rows[37].text.split()
        fail = data.pop()
        if fail == '?':
            toyota_price_raw = None
            toyota_price_min = None
            toyota_price_max = None
        else:
            toyota_price_raw = data[10].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            toyota_price_min = float(price_3[0])
            toyota_price_max = float(price_3[1])

        """""""""
        print(f'Ticketpreis ist {ticket_price_raw} mit einer Range von {ticket_price_min} - {ticket_price_max}')
        print(f'Monatskartepreis ist {monatskarte_price_raw} mit einer Range von {monatskarte_price_min} - {monatskarte_price_max}')
        print(f'Taxistartpreis ist {taxi_start_price_raw} mit einer Range von {taxi_start_price_min} - {taxi_start_price_max}')
        print(f'Taxi 1km preis ist {taxi_1km_price_raw} mit einer Range von {taxi_1km_price_min} - {taxi_1km_price_max}')
        print(f'Taxi 1h preis ist {taxi_1h_price_raw} mit einer Range von {taxi_1h_price_min} - {taxi_1h_price_max}')
        print(f'Benzinpreis ist {gasoline_price_raw} mit einer Range von {gasoline_price_min} - {gasoline_price_max}')
        print(f'VW preis ist {vw_price_raw} mit einer Range von {vw_price_min} - {vw_price_max}')
        print(f'Toyota preis ist {toyota_price_raw} mit einer Range von {toyota_price_min} - {toyota_price_max}')
        """""""""

        """""""""
        ----------------------Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment 	--------------------
        """""""""
        data = rows[39].text.split()
        fail = data.pop()
        if fail == '?':
            basic_price_raw = None
            basic_price_min = None
            basic_price_max = None
        else:
            basic_price_raw = data[9].replace(",", "")
            price_range = data[11].replace(",", "")
            price_3 = price_range.split("-")
            basic_price_min = float(price_3[0])
            basic_price_max = float(price_3[1])

        """""""""
        --------------------1 min. of Prepaid Mobile Tariff Local (No Discounts or Plans) ----------------------------------
        """""""""
        data = rows[40].text.split()
        fail = data.pop()
        if fail == '?':
            tarif_1min_price_raw = None
            tarif_1min_price_min = None
            tarif_1min_price_max = None
        else:
            tarif_1min_price_raw = data[11].replace(",", "")
            price_range = data[13].replace(",", "")
            price_3 = price_range.split("-")
            tarif_1min_price_min = float(price_3[0])
            tarif_1min_price_max = float(price_3[1])

        """""""""
        -----------------------Internet (60 Mbps or More, Unlimited Data, Cable/ADSL) --------------------------------------
        """""""""
        data = rows[41].text.split()
        fail = data.pop()
        if fail == '?':
            internet_price_raw = None
            internet_price_min = None
            internet_price_max = None
        else:
            internet_price_raw = data[8].replace(",", "")
            price_range = data[10].replace(",", "")
            price_3 = price_range.split("-")
            internet_price_min = float(price_3[0])
            internet_price_max = float(price_3[1])

        """""""""
        print(f'Basispreis ist {basic_price_raw} mit einer Range von {basic_price_min} - {basic_price_max}')
        print(f'1min Telen ist {tarif_1min_price_raw} mit einer Range von {tarif_1min_price_min} - {tarif_1min_price_max}')
        print(f'Internet preis ist {internet_price_raw} mit einer Range von {internet_price_min} - {internet_price_max}')
        """""""""

        """""""""
        --------------------------Fitness Club, Monthly Fee for 1 Adult ----------------------------------------------------
        """""""""
        data = rows[43].text.split()
        fail = data.pop()
        if fail == '?':
            fitness_price_raw = None
            fitness_price_min = None
            fitness_price_max = None
        else:
            fitness_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            fitness_price_min = float(price_3[0])
            fitness_price_max = float(price_3[1])

        """""""""
        --------------------------------------Tennis Court Rent (1 Hour on Weekend) ----------------------------------------
        """""""""
        data = rows[44].text.split()
        fail = data.pop()
        if fail == '?':
            tennis_court_price_raw = None
            tennis_court_price_min = None
            tennis_court_price_max = None
        else:
            tennis_court_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            tennis_court_price_min = float(price_3[0])
            tennis_court_price_max = float(price_3[1])

        """""""""
        --------------------------------------Cinema, International Release, 1 Seat ----------------------------------------
        """""""""
        data = rows[45].text.split()
        fail = data.pop()
        if fail == '?':
            cinema_price_raw = None
            cinema_price_min = None
            cinema_price_max = None
        else:
            cinema_price_raw = data[5].replace(",", "")
            price_range = data[7].replace(",", "")
            price_3 = price_range.split("-")
            cinema_price_min = float(price_3[0])
            cinema_price_max = float(price_3[1])

        """""""""
        print(f'Fittnespreis ist {fitness_price_raw} mit einer Range von {fitness_price_min} - {fitness_price_max}')
        print(f'Tennispreis ist {tennis_court_price_raw} mit einer Range von {tennis_court_price_min} - {tennis_court_price_max}')
        print(f'Kinopreis ist {cinema_price_raw} mit einer Range von {cinema_price_min} - {cinema_price_max}')
        """""""""

        """""""""
        --------------Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child  ---------------------------------
        """""""""
        data = rows[47].text.split()
        fail = data.pop()
        if fail == '?':
            preschool_price_raw = None
            preschool_price_min = None
            preschool_price_max = None
        else:
            preschool_price_raw = data[10].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            preschool_price_min = float(price_3[0])
            preschool_price_max = float(price_3[1])

        """""""""
        ------------------------International Primary School, Yearly for 1 Child -------------------------------------------
        """""""""
        data = rows[48].text.split()
        fail = data.pop()
        if fail == '?':
            school_price_raw = None
            school_price_min = None
            school_price_max = None
        else:
            school_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            school_price_min = float(price_3[0])
            school_price_max = float(price_3[1])

        """""""""
        print(f'Vorschule ist {preschool_price_raw} mit einer Range von {preschool_price_min} - {preschool_price_max}')
        print(f'Schule ist {school_price_raw} mit einer Range von {school_price_min} - {school_price_max}')
        """""""""

        """""""""
        ----------------------1 Pair of Jeans (Levis 501 Or Similar) -------------------------------------------------------
        """""""""
        data = rows[50].text.split()
        fail = data.pop()
        if fail == '?':
            jeans_price_raw = None
            jeans_price_min = None
            jeans_price_max = None
        else:
            jeans_price_raw = data[8].replace(",", "")
            price_range = data[10].replace(",", "")
            price_3 = price_range.split("-")
            jeans_price_min = float(price_3[0])
            jeans_price_max = float(price_3[1])

        """""""""
        -------------------1 Summer Dress in a Chain Store (Zara, H&M, ...) ------------------------------------------------
        """""""""
        data = rows[51].text.split()
        fail = data.pop()
        if fail == '?':
            dress_price_raw = None
            dress_price_min = None
            dress_price_max = None
        else:
            dress_price_raw = data[10].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            dress_price_min = float(price_3[0])
            dress_price_max = float(price_3[1])

        """""""""
        --------------------------------------1 Pair of Nike Running Shoes (Mid-Range) -------------------------------------
        """""""""
        data = rows[52].text.split()
        fail = data.pop()
        if fail == '?':
            running_shoes_price_raw = None
            running_shoes_price_min = None
            running_shoes_price_max = None
        else:
            running_shoes_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            running_shoes_price_min = float(price_3[0])
            running_shoes_price_max = float(price_3[1])

        """""""""
        --------------------------------------1 Pair of Men Leather Business Shoes -----------------------------------------
        """""""""
        data = rows[53].text.split()
        fail = data.pop()
        if fail == '?':
            business_shoes_price_raw = None
            business_shoes_price_min = None
            business_shoes_price_max = None
        else:
            business_shoes_price_raw = data[7].replace(",", "")
            price_range = data[9].replace(",", "")
            price_3 = price_range.split("-")
            business_shoes_price_min = float(price_3[0])
            business_shoes_price_max = float(price_3[1])

        """""""""
        print(f'Jeans ist {jeans_price_raw} mit einer Range von {jeans_price_min} - {jeans_price_max}')
        print(f'Dress ist {dress_price_raw} mit einer Range von {dress_price_min} - {dress_price_max}')
        print(f'Running shoes ist {running_shoes_price_raw} mit einer Range von {running_shoes_price_min} - {running_shoes_price_max}')
        print(f'business ist {business_shoes_price_raw} mit einer Range von {business_shoes_price_min} - {business_shoes_price_max}')
        """""""""

        """""""""
        ----------------------Apartment (1 bedroom) in City Centre ---------------------------------------------------------
        """""""""
        data = rows[55].text.split()
        fail = data.pop()
        if fail == '?':
            rent_1bedroom_center_price_raw = None
            rent_1bedroom_center_price_min = None
            rent_1bedroom_center_price_max = None
        else:
            rent_1bedroom_center_price_raw = data[6].replace(",", "")
            price_range = data[8].replace(",", "")
            price_3 = price_range.split("-")
            rent_1bedroom_center_price_min = float(price_3[0])
            rent_1bedroom_center_price_max = float(price_3[1])

        """""""""
        --------------------------------------Apartment (1 bedroom) Outside of Centre --------------------------------------
        """""""""
        data = rows[56].text.split()
        fail = data.pop()
        if fail == '?':
            rent_1bedroom_outside_price_raw = None
            rent_1bedroom_outside_price_min = None
            rent_1bedroom_outside_price_max = None
        else:
            rent_1bedroom_outside_price_raw = data[6].replace(",", "")
            price_range = data[8].replace(",", "")
            price_3 = price_range.split("-")
            rent_1bedroom_outside_price_min = float(price_3[0])
            rent_1bedroom_outside_price_max = float(price_3[1])

        """""""""
        --------------------------------------Apartment (3 bedrooms) in City Centre-----------------------------------------
        """""""""
        data = rows[57].text.split()
        fail = data.pop()
        if fail == '?':
            rent_3bedroom_center_price_raw = None
            rent_3bedroom_center_price_min = None
            rent_3bedroom_center_price_max = None
        else:
            rent_3bedroom_center_price_raw = data[6].replace(",", "")
            price_range = data[8].replace(",", "")
            price_3 = price_range.split("-")
            rent_3bedroom_center_price_min = float(price_3[0])
            rent_3bedroom_center_price_max = float(price_3[1])

        """""""""
        --------------------------------------Apartment (3 bedrooms) Outside of Centre -------------------------------------
        """""""""
        data = rows[58].text.split()
        fail = data.pop()
        if fail == '?':
            rent_3bedroom_outside_price_raw = None
            rent_3bedroom_outside_price_min = None
            rent_3bedroom_outside_price_max = None
        else:
            rent_3bedroom_outside_price_raw = data[6].replace(",", "")
            price_range = data[8].replace(",", "")
            price_3 = price_range.split("-")
            rent_3bedroom_outside_price_min = float(price_3[0])
            rent_3bedroom_outside_price_max = float(price_3[1])

        """""""""
        print(f'1 bedroom center ist {rent_1bedroom_center_price_raw} mit einer Range von {rent_1bedroom_center_price_min} - {rent_1bedroom_center_price_max}')
        print(f'1 bedroom outside ist {rent_1bedroom_outside_price_raw} mit einer Range von {rent_1bedroom_outside_price_min} - {rent_1bedroom_outside_price_max}')
        print(f'3 bedroom center ist {rent_3bedroom_center_price_raw} mit einer Range von {rent_3bedroom_center_price_min} - {rent_3bedroom_center_price_max}')
        print(f'3 bedroom outside ist {rent_3bedroom_outside_price_raw} mit einer Range von {rent_3bedroom_outside_price_min} - {rent_3bedroom_outside_price_max}')
        """""""""
        """""""""
        --------------------------------------Price per Square Meter to Buy Apartment in City Centre -----------------------
        """""""""
        data = rows[60].text.split()
        fail = data.pop()
        if fail == '?':
            buyapart_sqaremeter_center_price_raw = None
            buyapart_sqaremeter_center_price_min = None
            buyapart_sqaremeter_center_price_max = None
        else:
            buyapart_sqaremeter_center_price_raw = data[10].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            buyapart_sqaremeter_center_price_min = float(price_3[0])
            buyapart_sqaremeter_center_price_max = float(price_3[1])

        """""""""
        ----------------------------Price per Square Meter to Buy Apartment Outside of Centre  -----------------------------
        """""""""
        data = rows[61].text.split()
        fail = data.pop()
        if fail == '?':
            buyapart_sqaremeter_outside_price_raw = None
            buyapart_sqaremeter_outside_price_min = None
            buyapart_sqaremeter_outside_price_max = None
        else:
            buyapart_sqaremeter_outside_price_raw = data[10].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            buyapart_sqaremeter_outside_price_min = float(price_3[0])
            buyapart_sqaremeter_outside_price_max = float(price_3[1])

        """""""""
        print(f'buycenter ist {buyapart_sqaremeter_center_price_raw} mit einer Range von {buyapart_sqaremeter_center_price_min} - {buyapart_sqaremeter_center_price_max}')
        print(f'buy outside ist {buyapart_sqaremeter_outside_price_raw} mit einer Range von {buyapart_sqaremeter_outside_price_min} - {buyapart_sqaremeter_outside_price_max}')
        """""""""

        """""""""
        -----------------------------------Average Monthly Net Salary (After Tax) ------------------------------------------
        """""""""
        data = rows[63].text.split()
        fail = data.pop()
        if fail == '?':
            salary_raw = None
        else:
            salary_raw = data[6].replace(",", "")
        """""""""
        ----------Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate -------------------------------
        """""""""
        data = rows[64].text.split()
        fail = data.pop()
        if fail == '?':
            intrest_raw = None
            intrest_min = None
            intrest_max = None
        else:
            intrest_raw = data[11].replace(",", "")
            price_range = data[12].replace(",", "")
            price_3 = price_range.split("-")
            intrest_min = float(price_3[0])
            intrest_max = float(price_3[1])

        """""""""
        print(f'Einkommen ist {salary_raw} ')
        print(f'Zinsen ist {intrest_raw} mit einer Range von {intrest_min} - {intrest_max}')
        """""""""

        if city == "Dresden":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`dresden` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Frankfurt":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`frankfurt` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Berlin":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`berlin` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Aachen":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`aachen` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Cologne":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`cologne` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Hamburg":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`hamburg` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Nuremberg":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`nuremberg` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Munich":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`munich` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Stuttgart":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`stuttgart` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Hanover":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`hanover` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Mannheim":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`mannheim` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Karlsruhe":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`karlsruhe` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Dusseldorf":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`dusseldorf` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Heidelberg":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`heidelberg` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Prague":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`prague` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Warsaw":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`warsaw` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        elif city == "Luxembourg":
            print(city)
            sqlStuff = "INSERT INTO `numbeo`.`luxembourg` (`Zeit`,`Snack`,`Snack(min)`,`Snack(max)`,`Meal`,`Meal(min)`," \
                       "`Meal(max)`,`Mcmeal`,`Mcmeal(min)`,`Mcmeal(max)`,`Domestic Beer`,`Domestic Beer(min)`," \
                       "`Domestic Beer(max)`,`Imported Beer`,`Imported Beer(min)`,`Imported Beer(max)`,`Cappuccino`," \
                       "`Cappuccino(min)`,`Cappuccino(max)`,`Cola`,`Cola(min)`,`Cola(max)`,`Wasser`,`Wasser(min)`," \
                       "`Wasser(max)`,`Milk`,`Milk(min)`,`Milk(max)`,`Bread`,`Bread(min)`,`Bread(max)`,`Rice`," \
                       "`Rice(min)`,`Rice(max)`,`Eggs`,`Eggs(min)`,`Eggs(max)`,`Cheese`,`Cheese(min)`,`Cheese(max)`," \
                       "`Chicken`,`Chicken(min)`,`Chicken(max)`,`Beef`,`Beef(min)`,`Beef(max)`,`Apples`,`Apples(min)`," \
                       "`Apples(max)`,`Banana`,`Banana(min)`,`Banana(max)`,`Oranges`,`Oranges(min)`,`Oranges(max)`," \
                       "`Tomato`,`Tomato(min)`,`Tomato(max)`,`Potato`,`Potato(min)`,`Potato(max)`,`Onion`,`Onion(min)`," \
                       "`Onion(max)`,`Lettuce`,`Lettuce(min)`,`Lettuce(max)`,`Waterbottle`,`Waterbottle(min)`," \
                       "`Waterbottle(max)`,`Heimatbier`,`Heimatbier(min)`,`Heimatbier(max)`,`Auslandsbier`," \
                       "`Auslandsbier(min)`,`Auslandsbier(max)`,`Cigarettes`,`Cigarettes(min)`,`Cigarettes(max)`," \
                       "`Ticket`,`Ticket(min)`,`Ticket(max)`,`Monatskarte`,`Monatskarte(min)`,`Monatskarte(max)`," \
                       "`Taxi-Startpreis`,`Taxi-Startpreis(min)`,`Taxi-Startpreis(max)`,`Taxi-Kilometerpreis`," \
                       "`Taxi-Kilometerpreis(min)`,`Taxi-Kilometerpreis(max)`,`Taxi-1h-wartenpreis`," \
                       "`Taxi-1h-wartenpreis(min)`,`Taxi-1h-wartenpreis(max)`,`Gasoline`,`Gasoline(min)`,`Gasoline(max)`," \
                       "`VW`,`VW(min)`,`VW(max)`,`Toyota`,`Toyota(min)`,`Toyota(max)`,`Basic`,`Basic(min)`,`Basic(max)`," \
                       "`Tarif-1min`,`Tarif-1min(min)`,`Tarif-1min(max)`,`Internet`,`Internet(min)`,`Internet(max)`," \
                       "`Fitness`,`Fitness(min)`,`Fitness(max)`,`Tennis`,`Tennis(min)`,`Tennis(max)`,`Cinema`,`Cinema(min)`," \
                       "`Cinema(max)`,`Preschool`,`Preschool(min)`,`Preschool(max)`,`Primary School`,`Primary School(min)`," \
                       "`Primary School(max)`,`Jeans`,`Jeans(min)`,`Jeans(max)`,`Dress`,`Dress(min)`,`Dress(max)`," \
                       "`Running-Shoes`,`Running-Shoes(min)`,`Running-Shoes(max)`, `Business-Shoes`,`Business-Shoes(min)`," \
                       "`Business-Shoes(max)`,`Rent-1-Bedroom-Center`,`Rent-1-Bedroom-Center(min)`," \
                       "`Rent-1-Bedroom-Center(max)`,`Rent-1-Bedroom-Outside`,`Rent-1-Bedroom-Outside(min)`," \
                       "`Rent-1-Bedroom-Outside(max)`,`Rent-3-Bedroom-Center`,`Rent-3-Bedroom-Center(min)`," \
                       "`Rent-3-Bedroom-Center(max)`,`Rent-3-Bedroom-Outside`,`Rent-3-Bedroom-Outside(min)`," \
                       "`Rent-3-Bedroom-Outside(max)`,`Square-Meter-in-City-Centre`,`Square-Meter-in-City-Centre(min)`," \
                       "`Square-Meter-in-City-Centre(max)`,`Square-Meter-in-City-Outside`," \
                       "`Square-Meter-in-City-Outside(min)`,`Square-Meter-in-City-Outside(max)`,`Salary`,`Intrest`," \
                       "`Intrest(min)`,`Intrest(max)` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                       " %s,%s,%s);"
            record1 = (
                zeit, snack_price_raw, snack_price_min, snack_price_max, meal_price_raw, meal_price_min, meal_price_max,
                mcmeal_price_raw, mcmeal_price_min, mcmeal_price_max, beer_home_price_raw, beer_home_price_min,
                beer_home_price_max, beer_import_price_raw, beer_import_price_min, beer_import_price_max,
                cappuccino_price_raw, cappuccino_price_min, cappuccino_price_max, cola_price_raw, cola_price_min,
                cola_price_max, water_price_raw, water_price_min, water_price_max, milk_price_raw, milk_price_min,
                milk_price_max, bread_price_raw, bread_price_min, bread_price_max, rice_price_raw, rice_price_min,
                rice_price_max, eggs_price_raw, eggs_price_min, eggs_price_max, cheese_price_raw, cheese_price_min,
                cheese_price_max, chicken_fillets_price_raw, chicken_fillets_price_min, chicken_fillets_price_max,
                beef_price_raw, beef_price_min, beef_price_max, apples_price_raw, apples_price_min, apples_price_max,
                banana_price_raw, banana_price_min, banana_price_max, oranges_price_raw, oranges_price_min,
                oranges_price_max, tomato_price_raw, tomato_price_min, tomato_price_max, potato_price_raw, potato_price_min,
                potato_price_max, onion_price_raw, onion_price_min, onion_price_max, lettuce_price_raw, lettuce_price_min,
                lettuce_price_max, waterbottle_price_raw, waterbottle_price_min, waterbottle_price_max,
                heimatbier_price_raw, heimatbier_price_min, heimatbier_price_max, auslandsbier_price_raw,
                auslandsbier_price_min, auslandsbier_price_max, cigarettes_price_raw, cigarettes_price_min,
                cigarettes_price_max, ticket_price_raw, ticket_price_min, ticket_price_max, monatskarte_price_raw,
                monatskarte_price_min, monatskarte_price_max, taxi_start_price_raw, taxi_start_price_min,
                taxi_start_price_max, taxi_1km_price_raw, taxi_1km_price_min, taxi_1km_price_max, taxi_1h_price_raw,
                taxi_1h_price_min, taxi_1h_price_max, gasoline_price_raw, gasoline_price_min, gasoline_price_max,
                vw_price_raw, vw_price_min, vw_price_max, toyota_price_raw, toyota_price_min, toyota_price_max,
                basic_price_raw, basic_price_min, basic_price_max, tarif_1min_price_raw, tarif_1min_price_min,
                tarif_1min_price_max, internet_price_raw, internet_price_min, internet_price_max, fitness_price_raw,
                fitness_price_min, fitness_price_max, tennis_court_price_raw, tennis_court_price_min,
                tennis_court_price_max, cinema_price_raw, cinema_price_min, cinema_price_max, preschool_price_raw,
                preschool_price_min, preschool_price_max, school_price_raw, school_price_min, school_price_max,
                jeans_price_raw, jeans_price_min, jeans_price_max, dress_price_raw, dress_price_min, dress_price_max,
                running_shoes_price_raw, running_shoes_price_min, running_shoes_price_max, business_shoes_price_raw,
                business_shoes_price_min, business_shoes_price_max, rent_1bedroom_center_price_raw,
                rent_1bedroom_center_price_min, rent_1bedroom_center_price_max, rent_1bedroom_outside_price_raw,
                rent_1bedroom_outside_price_min, rent_1bedroom_outside_price_max, rent_3bedroom_center_price_raw,
                rent_3bedroom_center_price_min, rent_3bedroom_center_price_max, rent_3bedroom_outside_price_raw,
                rent_3bedroom_outside_price_min, rent_3bedroom_outside_price_max, buyapart_sqaremeter_center_price_raw,
                buyapart_sqaremeter_center_price_min, buyapart_sqaremeter_center_price_max,
                buyapart_sqaremeter_outside_price_raw, buyapart_sqaremeter_outside_price_min,
                buyapart_sqaremeter_outside_price_max, salary_raw, intrest_raw, intrest_min, intrest_max)
            my_cursor.execute(sqlStuff, record1)
            mydb.commit()

        else:
            print("Fehlschlag")

        print("Erfolg")
        #time.sleep(30)

while x == 1:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    trigger = time.gmtime()
    print(trigger.tm_min)
    print(trigger.tm_min%2)
    if trigger.tm_min%1 == 0:
        feching()
        time.sleep(120)
    else:
        print(f'nicht richtige zeit')

    time.sleep(10)
"""""""""
selection = ['Dresden','Frankfurt','Berlin','Aachen','Cologne','Hamburg','Nuremberg','Munich','Stuttgart','Hanover',
             'Mannheim','Karlsruhe','Dusseldorf','Heidelberg','Prague','Warsaw','Luxembourg']
"""""""""