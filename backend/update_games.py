"""Populate the local games table with top 20,000 games from RAWG"""
import os
import logging
from datetime import date

import requests
from sqlalchemy.orm import Session

from .database import SessionLocal
from .schema import Games

LOGGER  = logging.getLogger(__name__)
RAWG_GAMES_URL = "https://api.rawg.io/api/games"


def _api_key() -> str:
    key = os.getenv("RAWG_API_KEY")
    if not key:
        raise RuntimeError("RAWG_API_KEY not found.")
    return key

def game_data(game):
    return {
        "rawg_id": game.get("id"),
        "slug": game.get("slug"),
        "name": game.get("name"),
        "description": game.get("description"),
        "genres": ",".join(genre["name"] for genre in game.get("genres",[])),
        "platforms": ",".join(p["platform"]["name"]
                              for p in game.get("platforms", [])
                              if p.get("platform") and p["platform"].get("name")),
         "released": game.get("released"),
        "rating": game.get("rating"),
        "metacritic_rating": game.get("metacritic"),

    }

def get_page(url, api_key, page, page_size, ordering, released_after=None):
    params = {
        "key": api_key,
        "page": page,
        "page_size": page_size,
        "ordering": ordering,
    }
    if released_after:
        params["dates"] = f"{released_after},{date.today().isoformat()}"
    response = requests.get(url = url, params = params, timeout = 30)
    response.raise_for_status()
    return response.json().get("results",[])

def upsert_games(session: Session, payload: dict):
    check = session.query(Games).filter_by(rawg_id = payload["rawg_id"]).one_or_none()
    if check:
        for k,v in payload.items():
            setattr(check, k, v)
    else:
        session.add(Games(**payload))

def populate_games(api_key, limit = 20, page_size = 40, ordering = "-rating", released_after="2016-01-01"):
    saved = 0
    page = 1
    with SessionLocal() as session:
        while saved<limit:
            games = get_page(
                RAWG_GAMES_URL,
                api_key=api_key,
                page=page,
                page_size=page_size,
                ordering = ordering,
                released_after=released_after,
            )
            if not games:
                break
            for game in games:
                if saved>=limit:
                    break
                upsert_games(session, game_data(game))
                saved+=1
            session.commit()
            page+=1
        print(f"Saved {saved} games.")




