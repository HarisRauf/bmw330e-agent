import re

from core.browser import Browser
from core.models import CarListing
from scrapers.base import BaseScraper


def safe_int(text):
    if not text:
        return 0

    text = re.sub(r"[^\d]", "", text)

    return int(text) if text else 0


class RintaJouppiScraper(BaseScraper):

    URL = (
        "https://www.rintajouppi.fi/kampanjat/6kk-koroton-ja-kuluton/"
        "?search_type=henkiloautot"
        "&sales_type[]=usedCar"
        "&manufacturer[]=bmw"
        "&model[]=bmw_330"
        "&korimalli[]=sedan-hatchback"
        "&fuel_type[]=hybrid"
        "&gear_type[]=A"
        "&price_max=20000"
        "&manufacture_year_min=2019"
    )

    def search(self):

        print("Opening Rinta-Jouppi...")

        cars = []

        with Browser() as page:

            page.goto(self.URL)

            page.wait_for_timeout(5000)

            wrappers = page.locator(".card__wrapper")

            print(f"Found {wrappers.count()} wrappers")

            for i in range(wrappers.count()):

                card = wrappers.nth(i)

                try:

                    # Skip anything that isn't a real vehicle card
                    if card.locator(".card__title").count() == 0:
                        continue

                    title = card.locator(".card__title").first.inner_text().strip()

                    href = card.locator("a").first.get_attribute("href")

                    if not href:
                        continue

                    url = "https://www.rintajouppi.fi" + href

                    subtitle = ""

                    spans = card.locator("span.font--md")

                    if spans.count() > 0:
                        subtitle = spans.first.inner_text().strip()

                    info = card.locator("p").first.inner_text()

                    year_match = re.search(r"\b(20\d{2})\b", info)

                    mileage_match = re.search(r"([\d,\s]+)\s*km", info)

                    year = int(year_match.group(1)) if year_match else 0

                    mileage = (
                        safe_int(mileage_match.group(1))
                        if mileage_match
                        else 0
                    )

                    transmission = ""

                    if "Automatic" in info:
                        transmission = "Automatic"

                    fuel = ""

                    if "Plug-in hybrid" in info:
                        fuel = "Plug-in hybrid"
                    elif "Hybrid" in info:
                        fuel = "Hybrid"

                    price = safe_int(
                        card.locator(".card__price--main").inner_text()
                    )

                    location = ""

                    if card.locator(".card__info-location").count() > 0:
                        location = (
                            card.locator(".card__info-location")
                            .inner_text()
                            .strip()
                        )

                    listing_id = href.strip("/").split("/")[-1]

                    print(title, year, price)

                    cars.append(
                        CarListing(
                            website="Rinta-Jouppi",
                            listing_id=listing_id,
                            title=title,
                            subtitle=subtitle,
                            price=price,
                            year=year,
                            mileage=mileage,
                            fuel=fuel,
                            transmission=transmission,
                            body_type="Sedan",
                            location=location,
                            url=url,
                        )
                    )

                except Exception as e:

                    print(f"Skipping wrapper {i}: {e}")

                    continue

        print(f"Rinta-Jouppi: {len(cars)} cars found")

        return cars