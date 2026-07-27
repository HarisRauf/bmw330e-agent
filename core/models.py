from dataclasses import dataclass

@dataclass
class CarListing:
    website: str
    listing_id: str
    title: str
    subtitle: str
    price: int
    year: int
    mileage: int
    fuel: str
    transmission: str
    body_type: str
    location: str
    url: str