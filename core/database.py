import sqlite3
from pathlib import Path

from core.models import CarListing


class Database:

    def __init__(self, path: str):

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(path)

        self.create()

    def create(self):

        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS listings(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            listing_id TEXT UNIQUE,

            website TEXT,

            title TEXT,

            price INTEGER,

            year INTEGER,

            mileage INTEGER,

            fuel TEXT,

            location TEXT,

            url TEXT,

            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def exists(self, listing_id):

        cur = self.conn.cursor()

        cur.execute(
            "SELECT 1 FROM listings WHERE listing_id=?",
            (listing_id,)
        )

        return cur.fetchone() is not None

    def insert(self, car: CarListing):

        cur = self.conn.cursor()

        cur.execute("""
        INSERT OR IGNORE INTO listings(
            listing_id,
            website,
            title,
            price,
            year,
            mileage,
            fuel,
            location,
            url
        )
        VALUES(?,?,?,?,?,?,?,?,?)
        """,(
            car.listing_id,
            car.website,
            car.title,
            car.price,
            car.year,
            car.mileage,
            car.fuel,
            car.location,
            car.url
        ))

        self.conn.commit()