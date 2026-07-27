from core.database import Database
from core.filters import matches
from core.telegram import notify
from scrapers.nettiauto import NettiautoScraper


def main():

    db = Database("data/cars.db")

    scraper = NettiautoScraper()

    cars = scraper.search()

    print(f"\nTotal scraped: {len(cars)}")

    matching = 0
    new = 0

    for car in cars:

        print("\n-------------------------")
        print(f"Checking: {car.title}")
        print(f"Price: €{car.price}")
        print(f"Year: {car.year}")
        print(f"Mileage: {car.mileage} km")
        print(f"Fuel: {car.fuel}")

        if not matches(car):
            print("❌ Does not match filter")
            continue

        matching += 1
        print("✅ Matches filter")

        if db.exists(car.listing_id):
            print("⚠ Already in database")
            continue

        print("🆕 New listing!")

        new += 1

        db.insert(car)

        message = f"""
🚗 New BMW 330e Found!

💶 Price: €{car.price:,}

📅 Year: {car.year}

🛣 Mileage: {car.mileage:,} km

⛽ Fuel: {car.fuel}

📍 Dealer: {car.location}

📝 Description:
{car.subtitle}

🌐 Website: {car.website}

🔗 <a href="{car.url}">Open Listing</a>
"""

        notify(message)

    print("\n=========================")
    print(f"Total scraped : {len(cars)}")
    print(f"Passed filter : {matching}")
    print(f"New listings  : {new}")


if __name__ == "__main__":
    main()