from abc import ABC, abstractmethod

from core.models import CarListing


class BaseScraper(ABC):

    @abstractmethod
    def search(self) -> list[CarListing]:
        """Return a list of car listings."""
        pass