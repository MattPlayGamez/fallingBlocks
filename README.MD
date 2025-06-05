
# Catching the Falling Blocks

## Beschrijving
Dit is een eenvoudig spel gemaakt door Mathys Penson waarbij de speler een blok opvangt dat naar beneden valt. Het spel is geschreven in Python met behulp van de Pygame-bibliotheek.

## Inhoud
- [Vereisten](#vereisten)
- [Installatie](#installatie)
- [Gebruik](#gebruik)
- [Argumenten](#argumenten)
- [Begrippen](#begrippen)
  - Paddle
  - Block
  - Colors
- [Spelregels en Spelmechanica](#spelregels-en-spelmechanica)
- [Besturing](#besturing)
- [Geschiedenis en Versies](#geschiedenis-en-versies)
- [Licentie](#licentie)

## Vereisten
- Python 3.x
- Pygame

## Installatie
- Installeer Python 3.x als dit nog niet is gebeurd.
- Installeer Pygame via pip:
  ```
  pip install pygame
  ```

## Gebruik
- Sla de code op in een bestand, bijvoorbeeld `falling_blocks.py`.
- Voer het spel uit met:
  ```
  python falling_blocks.py [opties]
  ```

## Argumenten
- `-fs`, `--fullscreen`
  - Schakelt volledige schermmodus in (standaard).
- `-w`, `--windowed`
  - Schakelt venstermodus in.
- `-r WIDTH:HEIGHT`, `--resolution WIDTH:HEIGHT`
  - Stelt de schermresolutie in in het formaat WIDTH:HEIGHT (bijv. 1920:1080).
- `-l LIMIT`, `--limit LIMIT`
  - Bepaalt de maximale valsnelheid van het blok (standaard 18).

## Begrippen
### Paddle
- **Beschrijving**: De paddle is de balk onderaan het scherm die de speler bestuurt om het blok op te vangen.
- **Eigenschappen**:
  - `x`, `y`: Coördinaten van de paddle.
  - `width`, `height`: Afmetingen van de paddle.
  - `sprite`: De grafische representatie (rechthoek).
- **Methodes**:
  - `centerPaddle()`: Plaatst de paddle in het midden onderaan het scherm.
  - `draw()`: Tekent de paddle op het scherm.
  - `moveLeft()`: Verplaatst de paddle naar links.
  - `moveRight()`: Verplaatst de paddle naar rechts.

### Block
- **Beschrijving**: Het blok dat van boven naar beneden valt en door de paddle moet worden opgevangen.
- **Eigenschappen**:
  - `x`, `y`: Coördinaten van het blok.
  - `width`, `height`: Afmetingen van het blok.
  - `velocity`: Snelheidsvector die de richting en snelheid bepaalt (in combinatie met `fallspeed`).
  - `fallspeed`: Huidige valsnelheid van het blok.
  - `angle`: Hoek waarin het blok beweegt.
- **Methodes**:
  - `draw()`: Tekent het blok op het scherm.
  - `fall()`: Verplaatst het blok afhankelijk van zijn snelheid en controleert of het schermrand is bereikt.
  - `updateFallSpeed()`: Verhoogt de valsnelheid totdat de limiet (`maxFallSpeed`) is bereikt.
  - `changeSpeed(direction)`: Past de valsnelheid aan omhoog of omlaag.
  - `checkCollision(collisionItem)`: Controleert botsing met een ander object (bijvoorbeeld de paddle).
  - `reset()`: Reset het blok naar de startpositie en initiële valsnelheid.
  - `rebounce(distanceFromMiddle)`: Laat het blok terugkaatsen wanneer het de paddle raakt, met een afwijking gebaseerd op de impactpositie.
  - `rebounceFromScreen(axis)`: Laat het blok terugkaatsen bij botsing met de schermranden.

### Colors
- **Beschrijving**: Een klasse die kleurdefinities (RGB) bevat die in het spel worden gebruikt.
- **Eigenschappen**:
  - `white`, `black`, `blue`, `green`, `red`: Tuple met RGB-waarden.

## Spelregels en Spelmechanica
- Het blok valt van boven naar beneden met een initiële snelheid.
- Zodra het blok de paddle raakt, kaatst het weg en versnelt het een beetje.
- De speler verdient 1 punt per succesvolle vangst.
- Bij botsing met zij- of bovenzijde van het scherm kaatst het blok ook weg.
- Als het blok de onderkant van het scherm bereikt zonder opgevangen te worden, is het spel voorbij.

## Besturing
- **Pijltjestoetsen Links/Rechts**: Beweeg de paddle naar links of rechts.
- **Pijltjestoetsen Omhoog/Omlaag**: Verhoog of verlaag de valsnelheid van het blok tijdens het spel.
- **F**: Schakel tussen volledige schermmodus en venstermodus.
- **Enter**: Herstart het spel na een game over.
- **Escape**: Sluit het spel af.
- **Rechter Alt (RALT)**: Verhoog de score (voor testdoeleinden).

## Geschiedenis en Versies
| Versie | Datum       | Beschrijving                         |
|--------|-------------|--------------------------------------|
| 1.0    | 05-06-2025  | Eerste release met basisfunctionaliteit |

## Licentie
Dit project is gelicentieerd onder de Eclipse Public License - v 2.0. Zie het `LICENSE`-bestand voor details.
