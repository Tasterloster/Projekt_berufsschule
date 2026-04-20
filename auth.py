"""
auth.py - Authentifizierungsfunktionen für HHBKTendo Spielesammlung
Passwörter werden gehasht gespeichert (LN5030)
"""

import hashlib
import os
import database

# Aktuell eingeloggter Benutzer (None = Gast)
current_user = None


def hash_password(password):
    """
    Hasht ein Passwort mit SHA-256 und einem zufälligen Salt (LN5030).
    Gibt 'salt:hash' zurück.
    """
    salt = os.urandom(16).hex()
    pw_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{pw_hash}"


def verify_password(password, stored_hash):
    """
    Überprüft ein Passwort gegen den gespeicherten Hash.
    Gibt True zurück wenn korrekt.
    """
    parts = stored_hash.split(":")
    if len(parts) != 2:
        return False
    salt, pw_hash = parts
    check_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return check_hash == pw_hash


def register(username, password):
    """
    Registriert einen neuen Benutzer.
    Gibt (True, user_id) bei Erfolg zurück, (False, Fehlermeldung) bei Fehler.
    """
    if not username or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters."
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters."

    username = username.strip()
    pw_hash = hash_password(password)
    user_id = database.register_user(username, pw_hash)

    if user_id is None:
        return False, "Username already taken."

    return True, user_id


def login(username, password):
    """
    Meldet einen Benutzer an.
    Gibt (True, user_dict) bei Erfolg zurück, (False, Fehlermeldung) bei Fehler.
    """
    if not username or not password:
        return False, "Please enter username and password."

    user = database.get_user_by_username(username.strip())
    if user is None:
        return False, "User not found."

    if not verify_password(password, user["password_hash"]):
        return False, "Incorrect password."

    return True, user


def set_current_user(user):
    """Setzt den aktuell eingeloggten Benutzer."""
    global current_user
    current_user = user


def logout():
    """Meldet den aktuellen Benutzer ab."""
    global current_user
    current_user = None


def get_current_user():
    """Gibt den aktuell eingeloggten Benutzer zurück (None = Gast)."""
    return current_user


def is_logged_in():
    """Gibt True zurück wenn ein Benutzer eingeloggt ist."""
    return current_user is not None


def is_guest():
    """Gibt True zurück wenn als Gast gespielt wird."""
    return current_user is None
