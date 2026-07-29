import re

from core.browser import Browser
from core.models import CarListing
from scrapers.base import BaseScraper


def safe_int(text):
    if not text:
        return 0

    text = re.sub(r"[^\d]", "", text)

    if text == "":
        return 0

    return int(text)


class SakaScraper(BaseScraper):

    URL = "https://saka.fi/fi/vaihtoautot?vehicle_type=Henkil%C3%B6auto&make=BMW&model=330&body_type=Sedan,Coupe&fuel=Bensiini%252C+Plug-in-hybridi&transmission=Automaatti&price={%22max%22:20000}&year_model={%22min%22:2019}"

    def search(self):

        cars = []

        with Browser() as page:

            print("Opening Saka...")

            page.goto(self.URL, wait_until="domcontentloaded")

            page.wait_for_load_state("networkidle")

            try:
                page.wait_for_selector(
                    '[data-test-id="vehicle-card"]',
                    timeout=5000
                )
            except:
                print("No matching Saka listings.")
                return []

            cards = page.locator('[data-test-id="vehicle-card"]')

            count = cards.count()

            print(f"Found {count} listings")

            if count == 0:
                return []

            for i in range(count):

                card = cards.nth(i)

                try:

                    href = card.locator("a").first.get_attribute("href")

                    if not href:
                        continue

                    url = "https://saka.fi" + href

                    title = (
                        card.locator("a")
                        .first
                        .get_attribute("aria-label")
                    )

                    subtitle = (
                        card.locator("p.mb-1")
                        .first
                        .inner_text()
                        .strip()
                    )

                    description = (
                        card.locator('[data-slot="card-description"]')
                        .first
                        .inner_text()
                        .strip()
                    )

                    badges = card.locator("div.inline-flex")

                    year = 0
                    mileage = 0
                    transmission = ""

                    if badges.count() >= 3:

                        year = safe_int(
                            badges.nth(0).inner_text()
                        )

                        mileage = safe_int(
                            badges.nth(1).inner_text()
                        )

                        transmission = (
                            badges.nth(2)
                            .inner_text()
                            .strip()
                        )

                    fuel = ""

                    fuel_icon = card.locator("span[title]")

                    if fuel_icon.count() > 0:
                        fuel = fuel_icon.first.get_attribute("title")

                    price = safe_int(
                        card.locator("p.text-base.font-bold")
                        .first
                        .inner_text()
                    )

                    listing_id = href.split("-")[-1]

                    cars.append(

                        CarListing(

                            website="Saka",

                            listing_id="saka_" + listing_id,

                            title=title,

                            subtitle=subtitle,

                            price=price,

                            year=year,

                            mileage=mileage,

                            fuel=fuel,

                            transmission=transmission,

                            body_type="Sedan",

                            location="Saka",

                            url=url,
                        )

                    )

                except Exception as e:
                    print(f"Skipped listing {i}: {e}")

        return cars