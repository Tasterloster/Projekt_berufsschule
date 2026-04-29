# BlitzBoard – Understanding Session

A grill-me session to build full understanding of the BlitzBoard codebase.

---

## Q1 – Startup Sequence

**Question:** When a user runs `python main.py`, what are the first 5 things that happen before the window becomes interactive — and why does auto-installing Pillow happen *before* the database is initialized rather than after?

**Answer:** `_ensure_dependencies()` runs first to install Pillow, then `database.init_db()` creates the SQLite schema, then the tkinter window is created, then the GIF background is loaded (which requires Pillow), then either the login screen or main menu is shown based on `session.json`. Pillow comes before the database because the GIF loader would crash immediately if Pillow wasn't present — the visual layer needs to be ready before anything is drawn.

---

## Q2 – Minimax Callback Design

**Question:** `minimax.py` knows nothing about Pawn Chess or Tic-Tac-Toe — it receives four callback functions instead. What are those four callbacks, what does each one return, and why is this design better than writing a separate minimax for each game?

**Answer:** The four callbacks are:
- `get_moves_fn` — returns a list of legal moves for a given board state
- `apply_move_fn` — returns a new board after a move is applied (never mutates the original)
- `evaluate_fn` — returns a numeric score for a non-terminal board state
- `is_terminal_fn` — returns a `(bool, score)` tuple indicating if the game is over and the final score

This is better than duplicating minimax per game because the algorithm logic — recursive search, alpha-beta pruning, score propagation — is identical regardless of game; only the rules differ. One correct implementation beats two that could diverge.

---

## Q3 – Alpha-Beta Pruning

**Question:** What does alpha-beta pruning actually *do* in `minimax.py`, and what would happen to the AI's difficulty levels if you removed it?

**Answer:** Alpha-beta pruning cuts off branches of the search tree that can't possibly affect the final decision — if the maximizing player already has a guaranteed score better than what the minimizing player would allow, there's no point exploring further. Without it, minimax would still return the *same* best move, but would evaluate exponentially more board states to get there. At higher difficulty levels (depth 4–5), removing pruning would likely make the AI's move calculation take several seconds instead of milliseconds, making the game feel broken or frozen — even though the AI would still play just as well.

---

## Q5 – Pawn Chess Evaluation Heuristic

**Question:** `pawn_chess.py`'s `evaluate` function scores board states using three factors. What are they, and — more importantly — why does piece count alone make a weak heuristic for Pawn Chess specifically?

**Answer:** The three factors are piece count (+10 per piece), progress bonus (+2 per row advanced toward the opponent's baseline), and center control (+1 for columns 1–4). Piece count alone is weak because Pawn Chess can be won without capturing a single piece — you win by getting one pawn to the opponent's back rank. A board where you have 5 pawns but none have advanced is worse than a board where you have 3 pawns but one is one step from winning. Without progress and center bonuses, the AI would fight to preserve pieces rather than push forward, playing the wrong game entirely.

---

## Q6 – Password Security (Salt + SHA-256)

**Question:** `auth.py` stores passwords as `"salt:hash"` using SHA-256. Why is a random salt necessary — what specific attack does it prevent — and what would an attacker need to crack a password stored this way?

**Answer:** The salt prevents rainbow table attacks. Without a salt, an attacker with the database could precompute SHA-256 hashes for millions of common passwords and instantly look up matches. Because each password gets a unique random 16-byte salt, every hash is unique even if two users pick the same password — the attacker would need to brute-force each account individually. To crack a salted SHA-256 hash, they'd need the salt (stored alongside the hash), then run millions of guesses through `SHA-256(guess + salt)` until one matches. SHA-256 is fast though, which is its weakness — a production app would use bcrypt or Argon2 instead, which are deliberately slow.

---

## Q7 – Database Column Types (results table)

**Question:** The `results` table stores `difficulty` as an integer (1–5) and `won` as an integer (0 or 1) rather than booleans or text. Why does this matter when querying the leaderboard — what does `get_leaderboard` actually count, and how would storing `won` as `"yes"`/`"no"` break it?

**Answer:** `get_leaderboard` counts wins by summing the `won` column — `SUM(won)` works because `1 + 1 + 0 + 1 = 3` wins directly. If `won` were stored as `"yes"`/`"no"`, SQLite would sum strings, getting `0` for everything, and the leaderboard would show all players tied at zero. Storing difficulty as an integer also means you can filter with `WHERE difficulty = 3` cleanly — no string comparison, no case sensitivity issues, and it naturally sorts and groups correctly.

---

## Q8 – Threading & GUI Safety

**Question:** The AI move calculation runs in a separate `threading.Thread`. Why can't it just run directly on the main thread — and why does the AI thread use `root.after()` to update the board instead of updating tkinter widgets directly?

**Answer:** Tkinter's main loop is single-threaded — if the AI calculation runs on it, the entire GUI freezes until the calculation finishes. The window won't redraw, buttons won't respond, and on some systems the OS marks it as "not responding". Running the AI on a background thread keeps the GUI alive. The reason the AI thread uses `root.after()` to hand the result back is that tkinter is not thread-safe — calling widget methods from a non-main thread causes random crashes and corrupted state. `root.after()` schedules the board update to run on the main thread at the next event loop tick, which is the only safe way to touch the GUI from another thread.

---

## Q9 – Custom Label Buttons

**Question:** The app uses custom `tk.Label` widgets styled as buttons instead of native `tk.Button`. What specific problem does this solve, and what extra work does it require in the code to compensate for what native buttons give you for free?

**Answer:** Native `tk.Button` ignores background color on macOS — it renders with the system's native button style regardless of what color you set, breaking the Synthwave theme. Using `tk.Label` with mouse event bindings gives full color control on all platforms. The extra work required is manually implementing everything a button normally provides: `<Button-1>` binding for click, `<Enter>` and `<Leave>` bindings for hover color changes, and cursor changes to show the pointer. Native buttons handle all of that automatically.

---

## Q10 – Language / i18n Flow

**Question:** The app supports English and German via a `TEXTS` dict and a `t(key)` function. Trace the full journey of a language setting — from a user selecting German at registration, through to a translated string appearing on screen after they log back in the next day.

**Answer:** At registration, the chosen language is passed to `auth.register()`, which calls `database.register_user(username, password_hash, language)` and stores `"de"` in the `users.language` column. When the user logs back in, `auth.login()` fetches the full user row including `language`, sets it on the current user dict via `set_current_user()`, and `app_state["language"]` is updated to `"de"`. When any screen renders, `t("some_key")` looks up `TEXTS["de"]["some_key"]` and returns the German string, which gets passed directly into the widget's `text=` parameter. If a key is missing in German, it falls back to English silently.

---

## Q11 – Session File Security & Silent Bug

**Question:** `session.json` stores the user's ID so they're auto-logged in next time. What is the security risk of this approach, and under what circumstance would the session file cause a silent bug rather than a security problem?

**Answer:** The security risk is that anyone with filesystem access can read `session.json`, copy the user ID, and replay it to log in as that user — there's no token, expiry, or signature to validate. It's essentially an unprotected credential file. The silent bug scenario: if a user is deleted from the database (or the database is wiped/reset), `session.json` still contains their old ID. `auth.load_session()` reads that ID and calls `get_user_by_id()`, which returns `None` — and if that `None` isn't handled carefully, the app could proceed with a `None` user, causing attribute errors or showing a blank main menu with no username, rather than redirecting to the login screen.

---

## Q12 – Guest vs Logged-In User in end_game()

**Question:** A guest user can play games but their results are never saved. Trace exactly where in the code this decision is enforced — what check is made, at what point in the game flow, and what happens differently for a guest vs a logged-in user after `end_game()` is called?

**Answer:** The check happens inside `end_game()` in `main.py`. After the game concludes, the code calls `auth.is_guest()` (or checks `auth.get_current_user()` for `None`/guest flag). If the user is a guest, `database.save_result()` is never called — the result is simply discarded. For a logged-in user, `save_result(user_id, game, difficulty, won)` is called, writing the row to the `results` table. Both paths then show the result dialog and return to the main menu — the only difference is whether the database write happens. The leaderboard therefore never reflects guest play.

---

## Q13 – GIF Background Darkening

**Question:** The GIF background is darkened to 25% brightness before being displayed. Why is this done, and what would the UI look like without it?

**Answer:** The GIF is darkened so the Synthwave UI elements (neon text, buttons, labels) remain readable against the background. At full brightness, the background animation would compete visually with the foreground — text and buttons would be hard to read or completely lost against bright or busy frames. At 25% brightness, the background provides visual depth and motion without drawing the eye away from the interactive elements. Without the darkening, the app would look cluttered and unprofessional, and low-contrast text (like light cyan on a light background frame) could become illegible entirely.

---

## Q14 – Test Isolation with Temporary Database

**Question:** `test_all.py` uses a `DBTestCase` base class that sets up a temporary SQLite database for each test. Why is it critical that tests use a separate temporary database rather than the real `games.db`, and what would go wrong if you ran the test suite against the live database?

**Answer:** Tests insert, modify, and delete data as part of verifying behavior — running against `games.db` would pollute it with fake users and results, corrupt leaderboard data, and potentially break the app for real users. More subtly, tests depend on a known clean state: a test that checks "registering a duplicate username fails" only works reliably if that username doesn't already exist in the database. Against a live database with real data, tests could pass or fail depending on what's already there, making them non-deterministic. The temporary database is created fresh, tests run in isolation, and it's deleted on teardown — guaranteeing repeatability regardless of what's in `games.db`.

---

## Q15 – Procedural vs OOP Trade-offs

**Question:** The entire app uses no classes for game logic (procedural style, per school requirements). What are the concrete trade-offs — what does the procedural style make harder, and what does it make easier or cleaner in this specific codebase?

**Answer:** Harder: there's no natural place to encapsulate game state — the board, current turn, and move history are passed around as arguments or stored in the global `app_state` dict, which means any function can accidentally mutate shared state. Adding a third game would require threading more callbacks through `main.py` manually rather than just subclassing a `Game` base class. Easier/cleaner: the minimax callback design actually works better procedurally — pure functions with no `self` are simpler to pass as callbacks, and the lack of inheritance means there's no class hierarchy to understand before reading any single function. For a small two-game app, the procedural approach keeps the code flat and readable without the overhead of designing a class hierarchy that serves no real purpose at this scale.

---

## Q16 – tkinter pack() Geometry Manager

**Question:** `pack()` is used almost everywhere to position widgets. Looking at the header in `build_main_menu`, you see `pack(side="left")` and `pack(side="right")`. What does `pack` actually do, and why does `side="right"` on the logout button end up on the right even though it's packed after several `side="left"` widgets?

**Answer:** `pack()` is tkinter's flow-based geometry manager — it places each widget one at a time along an edge of its container, shrinking the remaining available space after each placement. `side="left"` stacks widgets left-to-right from the left edge; `side="right"` stacks from the right edge inward. They don't conflict because both sides consume from opposite ends of the same available space. The logout button ends up on the right because it claims the right edge of whatever space is left after the left-packed widgets have taken their share — order of packing determines who claims space first, and right-packed widgets claim from the right side regardless of when they were packed relative to left-packed ones.

---

## Q17 – Image Garbage Collection in tkinter

**Question:** In `build_login_screen`, the logo image is stored as `lbl_logo.image = login_logo_img`. Why is this line necessary — what would happen without it, and what does Python's garbage collector have to do with it?

**Answer:** tkinter uses Tcl/Tk under the hood, which manages image objects separately from Python. When you create an `ImageTk.PhotoImage` and assign it to a local variable, Python's garbage collector can delete the Python object once nothing in Python references it — even if Tcl/Tk is still using it to display the image. When the Python object is garbage collected, the underlying Tcl image is also destroyed, and the label renders as a blank grey box instead of the image. By assigning `lbl_logo.image = login_logo_img`, you attach a reference to the label widget itself, which survives as long as the screen is visible — keeping the image alive for as long as it's needed.

---

## Q18 – Screen Switching with destroy()

**Question:** `show_screen()` switches screens by destroying the old frame and creating a new one. What does `destroy()` actually do to all the widgets inside — and why is this approach used instead of hiding and showing screens?

**Answer:** `destroy()` recursively removes the frame and every widget inside it from memory — all labels, buttons, entries, canvases, and their event bindings are deleted. This is important because tkinter widgets are not lightweight objects; leaving old screens in memory would mean hundreds of invisible widgets accumulating as the user navigates. The hide/show alternative (`pack_forget()`) keeps widgets in memory but just makes them invisible — it would work but would leak memory over time and keep old event bindings active. Destroying and rebuilding is cleaner: each screen starts fresh with no leftover state, and memory is immediately freed.

---

## Q19 – tk.Canvas vs tk.Frame for the Game Board

**Question:** The game board is drawn on a `tk.Canvas` using `create_rectangle()` and `create_image()`. What makes `Canvas` fundamentally different from using `tk.Frame` with `tk.Label` widgets for each cell — and why is `Canvas` the right choice here?

**Answer:** A `tk.Frame` with `tk.Label` widgets creates actual widget objects for each cell — 36 separate Python/Tcl objects with their own event loops, backgrounds, and layout managers. A `tk.Canvas` is a single drawing surface where you issue draw commands that render directly as pixels — no child widgets at all. For a game board this is the right choice because: the entire board is redrawn from scratch on every move with `board_canvas.delete("all")`, which is one operation instead of 36 widget updates; pixel-precise highlighting and overlapping neon grid lines are trivial with canvas draw calls but impossible with Label grids; and mouse clicks are handled by one `<Button-1>` binding on the canvas, with the cell calculated from pixel coordinates (`event.x // CELL_SIZE`), rather than needing a binding on every cell widget.

---

## Q4 – Move Generation Optimization in Tic-Tac-Toe

**Question:** In `tictactoe.py`, when the board is empty, `get_valid_moves` only returns the 4 center squares instead of all 36. Why? And what would go wrong — not strategically but computationally — if it returned all 36 moves on the first turn?

**Answer:** The center squares are returned first because placing in the center is always the strongest opening. The computational reason is more critical: at depth 5 with 36 possible first moves, the search tree branches into 36 × 35 × 34... states — the branching factor explodes. By restricting to 4 center moves on the first turn (and only adjacent-to-occupied squares on subsequent turns), the tree stays tractable. If all 36 were returned, the AI's first move calculation could freeze the app entirely even with alpha-beta pruning.