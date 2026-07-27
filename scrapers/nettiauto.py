import json
import html
import re

from core.browser import Browser
from core.models import CarListing
from scrapers.base import BaseScraper


def safe_int(value, default=0):
    if value is None:
        return default

    value = str(value).strip()

    if value == "":
        return default

    value = value.replace(" ", "").replace(",", "")

    try:
        return int(value)
    except ValueError:
        return default


class NettiautoScraper(BaseScraper):

    URL = "https://www.nettiauto.com/en/bmw/330/hybridi?haku=P3759872182"

    def search(self):

        cars = []

        with Browser() as page:

            print("Opening Nettiauto...")

            page.goto(
                self.URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(3000)

            page.wait_for_selector(
                'div[data-testid="normal_ad_listing_wrapper"]',
                timeout=30000
            )

            cards = page.locator(
                'div[data-testid="normal_ad_listing_wrapper"]'
            )

            count = cards.count()

            print(f"Found {count} listings")

            for i in range(count):

                card = cards.nth(i)

                raw = card.get_attribute("data-datalayer")

                if raw is None:
                    continue

                raw = html.unescape(raw)

                raw = re.sub(
                    r'([,{])([a-zA-Z0-9_]+):',
                    r'\1"\2":',
                    raw
                )

                data = json.loads(raw)

                href = card.locator(
                    'a[data-testid="favourite-list-ads-title"]'
                ).get_attribute("href")

                url = "https://www.nettiauto.com" + href

                # Extract subtitle (contains 330e / 330d / 330i)
                try:
                    subtitle = card.locator(
                        ".product-card__sub-title"
                    ).inner_text().strip()
                except:
                    subtitle = ""

                print(subtitle)

                year = safe_int(data.get("item_year_model"))
                mileage = safe_int(data.get("item_mileage"))
                price = safe_int(data.get("item_vehicle_price"))

                cars.append(
                    CarListing(
                        website="Nettiauto",
                        listing_id=str(data.get("item_id")),
                        title=data.get("item_name", ""),
                        subtitle=subtitle,
                        price=price,
                        year=year,
                        mileage=mileage,
                        fuel=data.get("item_power_type", ""),
                        transmission="Automatic",
                        body_type="Sedan",
                        location=data.get("item_seller", ""),
                        url=url,
                    )
                )

        return cars