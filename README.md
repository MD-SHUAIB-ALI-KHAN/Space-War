# 🚀 Space War — "Termination"

A top-down space shooter built with Python's `turtle` module and `pygame` sound.
Steer your ship, shoot the red enemies, and avoid hitting your blue allies.
This was **my first game ever coded** — it started in Python 2.7, and this repo
shows its full journey: the original, a debugged Python 3 port, and a version
with a player leaderboard stored in MySQL.

&#x20;  !\[Gameplay](Screenshots/Space\_War3\_Gameplay\_Demo\_1.png)

&#x20;  !\[Leaderboard](Screenshots/New%20Leaderboard%20img.png)

## Versions

|Folder|Python|What it is|
|-|-|-|
|`v1-python2-original/`|2.7 + pygame 1.9.6|The game exactly as I first wrote it (kept untouched for the record)|
|`v2-python3-bugfixed/`|3.12 + pygame 2|Ported to Python 3, collision bug and other bugs fixed|
|`v3-python3-leaderboard/`|3.12 + pygame 2 + MySQL|v2 + player names, lives, game-over screen, top-5 leaderboard|

## Controls

|Key|Action|
|-|-|
|← / →|Turn the ship|
|↑ / ↓|Speed up / slow down|
|Space|Fire missile|
|Enter *(game-over screen)*|Play again|
|N *(game-over screen)*|New player|

## Scoring

|Event|Score|Lives|
|-|-|-|
|Missile hits an enemy (red)|+55|—|
|Missile hits an ally (blue)|−5|—|
|An enemy crashes into you|−10|−1 *(v3 only)*|

In v3 you start with 3 lives. When they run out the game ends, your score is saved
to the database and the top 5 players are shown.

## Run it

### v2 (no database)

```
py -3.12 -m pip install pygame
cd v2-python3-bugfixed
py -3.12 BATTLE\_IN\_SPACE\_py3.py
```

### v3 (with leaderboard)

1. Install the requirements: `py -3.12 -m pip install -r requirements.txt`
2. Open **XAMPP Control Panel** and click **Start** next to **MySQL**.
3. Run the game: `py -3.12 BATTLE\_IN\_SPACE\_v3.py`

The database (`space\_war`) and its `scores` table are created automatically on
first run. To look at the data, open **phpMyAdmin → space\_war → scores**.

> XAMPP's default login (`root`, empty password, port 3306) is used. If yours is
> different, edit `DB\_CONFIG` at the top of `db.py`.
> If MySQL isn't running, the game still works — it just shows "Leaderboard offline".

### v1 (original, Python 2.7)

```
py -2.7 -m pip install pygame==1.9.6
py -2.7 BATTLE\_IN\_SPACE.py
```

## What changed from v1 → v2 (bug fixes)

|#|Problem in v1|Symptom|Fix in v2|
|-|-|-|-|
|1|`is\_collision` compared the sprite's **Y** position with the other sprite's **X** position (`other.xcor()`)|Missiles passed through enemies, while enemies and allies "died" with sound effects when nothing touched them|Compare X with X and Y with Y|
|2|After a hit the missile stayed at the hit spot until the next frame|One missile could kill two enemies or also hit an ally, causing extra sounds and score changes|The missile is removed (`park()`) the moment it hits|
|3|Missile status was written as both `"ready"` and `"Ready"`|Only worked by accident|One `park()` method sets the status|
|4|`self.speed = 1` overwrote turtle's built-in `speed()` method|Fragile, confusing code|Renamed to `velocity`|
|5|Explosion particles moved forever, even hidden ones|Wasted work every frame|Particles live 25 frames, then hide|
|6|Score text relied on `pen.undo()` undoing the right step|Fragile|Dedicated score pen using `clear()`|
|7|Laser sound file was reloaded on every shot|Small hitch when firing|Loaded once as a `Sound` object|
|8|Respawned enemies could appear on top of the player|Instant unfair hits|Respawn at a safe distance|
|9|`raw\_input(...)` after an infinite loop (never reached); closing the window printed an error|Dead code, ugly exit|Removed; window close handled cleanly|
|10|Images/sounds were found only if launched from the game folder|Double-click could fail|Game switches to its own folder at start|

**Python 3 port:** `raw\_input` removed, `super()` modernised, pygame 2 used.

## What's new in v3 (leaderboard)

* Player name prompt at start (trimmed, max 20 characters)
* Lives system and a proper game-over state (my original code had unused `lives`/`state` fields — v3 finishes that idea)
* Scores saved to **MySQL** (XAMPP) with a top-5 leaderboard on the game-over screen
* Restart without closing the window; switch player with **N**
* All SQL lives in its own file, `db.py`, using **parameterised queries** (safe against SQL injection)
* The game never crashes because of the database: if MySQL or the connector is missing, it plays on without a leaderboard

### Database schema

```sql
CREATE TABLE scores (
    id          INT AUTO\_INCREMENT PRIMARY KEY,
    player\_name VARCHAR(30) NOT NULL,
    score       INT         NOT NULL,
    played\_at   TIMESTAMP   NOT NULL DEFAULT CURRENT\_TIMESTAMP
);
```

## Project structure

```
Space-War/
├── README.md
├── screenshots/
├── v1-python2-original/        BATTLE\_IN\_SPACE.py + assets
├── v2-python3-bugfixed/        BATTLE\_IN\_SPACE\_py3.py + assets
└── v3-python3-leaderboard/     BATTLE\_IN\_SPACE\_v3.py, db.py, requirements.txt + assets
```

*(Each folder also needs the game's `realspace.gif`, `explosion.ogg`, `sniper rifle.ogg`, `windows error sound effect.ogg` and `laser shot.mp3`.)*

## Tech used

Python · turtle · pygame (mixer) · MySQL / MariaDB (XAMPP) · mysql-connector-python

## What I learned

* How a game loop works: update → move → check collisions → draw, every frame
* Object-oriented design: one `Sprite` base class, with `Player`, `Enemy`, `Ally`, `Missile` and `Particle` inheriting from it
* How a one-word typo (`xcor` instead of `ycor`) can cause bugs that look random
* Keeping database code separate from game code, and handling failures gracefully
* Moving a project from Python 2 to Python 3

## Acknowledgements

Game design and original code: **Md Shuaib Ali Khan** (my first coded game).
The bug hunt, Python 3 port and leaderboard were done as a learning exercise with help from
Claude (AI assistant by Anthropic), and I went through every change to understand it.

## Author

**Md Shuaib Ali Khan** — [LinkedIn](https://www.linkedin.com/in/mdshuaibkhan04) · [GitHub](https://github.com/MD-SHUAIB-ALI-KHAN)

