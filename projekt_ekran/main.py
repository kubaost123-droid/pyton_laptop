import time
import network
import socket
import json
from machine import Pin

# Przed uruchomieniem czegokolwiek, upewniamy się, że stare interfejsy są wyłączone
stary_ap = network.WLAN(network.AP_IF)
stary_ap.active(False)
 
stara_sta = network.WLAN(network.STA_IF)
stara_sta.active(False)
 
time.sleep(0.5) # Dajemy chipowi Wi-Fi pół sekundy na pełny reset wewnętrzny


try:
    from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
except ImportError:
    print("Brak biblioteki picographics!")

#--- 1. KONFIGURACJA EKRANU --
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
display.set_backlight(1.0)

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)

display.set_pen(BLACK)
display.clear()
display.set_pen(WHITE)

import jpegdec
j = jpegdec.JPEG(display)
j.open_file("franek2.jpg")
    
# Dekodowanie i rysowanie
j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    
display.update()

display.text("Laczenie z Wi-Fi...", 10, 50, 170, 4)
display.update()

# --- 2. ŁĄCZENIE Z SIECIĄ NADAJNIKA ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('PicoSensorNet', 'PicoPassword123') # Te same dane co u nadajnika

while not wlan.isconnected():
    time.sleep(0.5)
    print("Łączenie...")

print("Połączono! IP Odbiornika:", wlan.ifconfig()[0])

# --- 3. KONFIGURACJA ODBIORU UDP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', DEST_PORT := 5005))
sock.setblocking(False) # Ważne: nie blokujemy pętli, gdy nie ma nowych danych

print("Oczekuję na dane...")

# Zmienne przechowujące ostatnie odczyty
last_temp, last_hum, last_lux = 0, 0, 0
last_update = time.ticks_ms()

przycisk_a = Pin(12, Pin.IN, Pin.PULL_UP)
przycisk_b = Pin(13, Pin.IN, Pin.PULL_UP)
aktualne_okno = 0
MAKSYMALNA_LICZBA_OKIEN = 7

wilgotnosc_tab = []
temp_tab = []
lux_tab = []
max_liczba_danych = 30

#USTAWIENIA DO WYKRESU
X_START, X_END = 70, 300
Y_TOP, Y_BOTTOM = 50, 200

BG_COLOR = display.create_pen(20, 20, 20)
GRID_COLOR = display.create_pen(0, 150, 0)
LINE_COLOR = display.create_pen(0, 255, 255) # Cyjan dla linii wykresu
TEXT_COLOR = display.create_pen(255, 255, 255)

def temp_to_y(temp,TEMP_MIN,TEMP_MAX):
    # Skalowanie temperatury na piksele (z uwzględnieniem odwróconej osi Y)
    proporcja = (temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)
    wysokosc_wykresu = Y_BOTTOM - Y_TOP
    return int(Y_BOTTOM - (proporcja * wysokosc_wykresu))

while True:
    try:
        # Próba odbioru danych (max 1024 bajty)
        msg, addr = sock.recvfrom(1024)
        
        # Odkodowanie JSON'a
        dane = json.loads(msg.decode('utf-8'))
        last_temp = dane.get("temp", 0)
        last_hum = dane.get("hum", 0)
        last_lux = dane.get("lux", 0)
        last_update = time.ticks_ms() # Czas ostatniej pomyślnej wiadomości
        wilgotnosc_tab.append(last_hum)
        if len(wilgotnosc_tab)>30:
            wilgotnosc_tab.pop(0)

        temp_tab.append(last_temp)
        if len(temp_tab)>30:
            temp_tab.pop(0)

        lux_tab.append(last_lux)
        if len(lux_tab)>30:
            lux_tab.pop(0)

        print("Odebrano od", addr[0], ":", dane)

    except OSError:
        # Błąd OSError w trybie non-blocking oznacza po prostu brak nowej paczki
        pass

    if przycisk_a.value() == 0:
        aktualne_okno += 1
        if aktualne_okno >= MAKSYMALNA_LICZBA_OKIEN:
            aktualne_okno = 0  # Zapętlenie z okna 2 z powrotem do 0
        time.sleep(0.3) # WAŻNE: Debouncing (opóźnienie)
        
    if przycisk_b.value() == 0:
        aktualne_okno -= 1
        if aktualne_okno < 0:
            aktualne_okno = MAKSYMALNA_LICZBA_OKIEN - 1 # Zapętlenie z 0 do 2
        time.sleep(0.3)
                
            # --- RYSOWANIE EKRANU ---
    display.set_pen(BLACK)
    display.clear()
 


            
    if aktualne_okno == 0:
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
        display.set_pen(GREEN)
        display.text("TEMPERATURA", 20, 20, 300, 3)
        display.set_pen(BLACK)
        display.text(f'{last_temp} C', 20, 80, 300, 6)
                
    elif aktualne_okno == 1:
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
        display.set_pen(GREEN)
        display.text("NASWIETLENIE", 20, 20, 300, 3)
        display.set_pen(BLACK)
        display.text(f'{last_lux} Lx', 20, 80, 300, 6)
                
    elif aktualne_okno == 2:
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
        display.set_pen(GREEN)
        display.text("WILGOTNOSC", 20, 20, 300, 3)
        display.set_pen(BLACK)
        display.text(f'{last_hum} %', 20, 80, 300, 6)
            
    elif aktualne_okno == 3:                    ####################           WILGOTNOSC
        hum_min = min(wilgotnosc_tab) 
        hum_max = max(wilgotnosc_tab)
        display.set_pen(BG_COLOR)
        display.clear()
        # Rysowanie osi i ramki wykresu
        display.set_pen(GRID_COLOR)
        display.line(X_START, Y_BOTTOM, X_END, Y_BOTTOM) # Oś X
        display.line(X_START, Y_BOTTOM+1, X_END, Y_BOTTOM+1) # Oś X
        display.line(X_START, Y_TOP-20, X_START, Y_BOTTOM)  # Oś Y
        display.line(X_START+1, Y_TOP-20, X_START+1, Y_BOTTOM)  # Oś Y
        
        # Rysowanie podpisów osi (tekst)
        display.set_pen(TEXT_COLOR)
        display.text(f"{hum_max}%", 10, Y_TOP - 5, 40, 2)
        display.text(f"{hum_min}%", 10, Y_BOTTOM - 5, 40, 2)
        
        # Obliczanie odległości w poziomie między punktami wykresu
        liczba_punktów = len(wilgotnosc_tab)
        krok_x = (X_END - X_START) / (liczba_punktów - 1)
        
        # Rysowanie linii wykresu łączącej punkty
        display.set_pen(LINE_COLOR)
        
        for i in range(liczba_punktów - 1):
            # Punkt bieżący (1)
            x1 = int(X_START + (i * krok_x))
            y1 = temp_to_y(wilgotnosc_tab[i],hum_min-1,hum_max+1)
            
            # Punkt następny (2)
            x2 = int(X_START + ((i + 1) * krok_x))
            y2 = temp_to_y(wilgotnosc_tab[i + 1],hum_min-1,hum_max+1)
            
            # Łączymy punkt 1 z punktem 2
            display.line(x1, y1, x2, y2)
        display.set_pen(GRID_COLOR)
        display.text(f'WILGOTNOSC',140,30,300,3)

    elif aktualne_okno == 4:            ####################           TEMPERATURA
        temp_min = min(temp_tab) 
        temp_max = max(temp_tab)
        display.set_pen(BG_COLOR)
        display.clear()
        # Rysowanie osi i ramki wykresu
        display.set_pen(GRID_COLOR)
        display.line(X_START, Y_BOTTOM, X_END, Y_BOTTOM) # Oś X
        display.line(X_START, Y_BOTTOM+1, X_END, Y_BOTTOM+1) # Oś X
        display.line(X_START, Y_TOP-20, X_START, Y_BOTTOM)  # Oś Y
        display.line(X_START+1, Y_TOP-20, X_START+1, Y_BOTTOM)  # Oś Y
        
        # Rysowanie podpisów osi (tekst)
        display.set_pen(TEXT_COLOR)
        display.text(f"{temp_max} C", 10, Y_TOP - 5, 40, 2)
        display.text(f"{temp_min} C", 10, Y_BOTTOM - 5, 40, 2)
        
        # Obliczanie odległości w poziomie między punktami wykresu
        liczba_punktów = len(temp_tab)
        krok_x = (X_END - X_START) / (liczba_punktów - 1)
        
        # Rysowanie linii wykresu łączącej punkty
        display.set_pen(LINE_COLOR)
        
        for i in range(liczba_punktów - 1):
            # Punkt bieżący (1)
            x1 = int(X_START + (i * krok_x))
            y1 = temp_to_y(temp_tab[i],temp_min-1,temp_max+1)
            
            # Punkt następny (2)
            x2 = int(X_START + ((i + 1) * krok_x))
            y2 = temp_to_y(temp_tab[i + 1],temp_min-1,temp_max+1)
            
            # Łączymy punkt 1 z punktem 2
            display.line(x1, y1, x2, y2)
        display.set_pen(GRID_COLOR)
        display.text(f'TEMPERATURA',140,30,300,3)

    elif aktualne_okno == 5:                            ####################           NASWIETLENIE
        lux_min = min(lux_tab) 
        lux_max = max(lux_tab)
        display.set_pen(BG_COLOR)
        display.clear()
        # Rysowanie osi i ramki wykresu
        display.set_pen(GRID_COLOR)
        display.line(X_START, Y_BOTTOM, X_END, Y_BOTTOM) # Oś X
        display.line(X_START, Y_BOTTOM+1, X_END, Y_BOTTOM+1) # Oś X
        display.line(X_START, Y_TOP-20, X_START, Y_BOTTOM)  # Oś Y
        display.line(X_START+1, Y_TOP-20, X_START+1, Y_BOTTOM)  # Oś Y
        
        # Rysowanie podpisów osi (tekst)
        display.set_pen(TEXT_COLOR)
        display.text(f"{lux_max} Lx", 10, Y_TOP - 5, 40, 2)
        display.text(f"{lux_min} Lx", 10, Y_BOTTOM - 5, 40, 2)
        
        # Obliczanie odległości w poziomie między punktami wykresu
        liczba_punktów = len(lux_tab)
        krok_x = (X_END - X_START) / (liczba_punktów - 1)
        
        # Rysowanie linii wykresu łączącej punkty
        display.set_pen(LINE_COLOR)
        
        for i in range(liczba_punktów - 1):
            # Punkt bieżący (1)
            x1 = int(X_START + (i * krok_x))
            y1 = temp_to_y(lux_tab[i],lux_min-1,lux_max+1)
            
            # Punkt następny (2)
            x2 = int(X_START + ((i + 1) * krok_x))
            y2 = temp_to_y(lux_tab[i + 1],lux_min-1,lux_max+1)
            
            # Łączymy punkt 1 z punktem 2
            display.line(x1, y1, x2, y2)
        display.set_pen(GRID_COLOR)
        display.text(f'NASWIETLENIE',120,30,300,3)

    elif aktualne_okno == 6:                           ##############zbirocze                    
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
        display.set_pen(RED)
        display.text(f"Sr_wilg: {(sum(wilgotnosc_tab)/len(wilgotnosc_tab)):.2f}",10,10,300,3)
        display.set_pen(BLACK)
        display.text(f"Temp: {last_temp} C", 10, 60, 300, 3)
        display.text(f"Wilg: {last_hum} %", 10, 110, 300, 3)
        display.text(f"Lux: {last_lux} Lx", 10, 160, 300, 3)
    

    display.set_pen(WHITE)
    display.text(f"Strona: {aktualne_okno + 1}/{MAKSYMALNA_LICZBA_OKIEN}", 20, 220, 300, 2)
    display.update()

