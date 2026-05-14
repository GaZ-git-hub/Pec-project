# Snake Game – Projekt PEC

Jednoduchá implementace klasické hry Snake v Pythonu s využitím knihovny Pygame. Hráč ovládá hada, který sbírá jablka, roste a nesmí narazit do zdi nebo do sebe.

## 🐍 Funkce

- Ovládání pomocí kláves W, A, S, D
- Score systém s vizuálním zobrazením
- Detekce kolizí (se zdí i sebou samým)
- Náhodně generované jablka
- Herní smyčka s Game Over obrazovkou
- Možnost restartu
- Možnost přidání obtížnosti

## 🔧 Instalace

1. Naklonuj repozitář:
    ```bash
    git clone https://git.fai.utb.cz/v_jachim/project_pec.git
    cd project_pec
    ```

2. Nainstaluj požadované závislosti:
    ```bash
    pip install pygame
    ```

3. Spusť hru:
    ```bash
    python snakebase.py
    ```

## 🚦 Ovládání

- **W** – nahoru
- **S** – dolů
- **A** – doleva
- **D** – doprava
- **R** – restart hry po Game Over

## 🧪 Testování

Pro spuštění testů (např. test kolize):
```bash
pytest test.py
```

## 👤 Autoři
Václav Jáchim – autor

## 📄 Licence
Tento projekt je poskytován pod MIT licencí.
