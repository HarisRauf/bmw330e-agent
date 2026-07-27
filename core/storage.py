import json
import os


class Storage:

    def __init__(self, filename="listings.json"):
        self.filename = filename

        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump([], f)

    def load(self):
        with open(self.filename, "r") as f:
            return set(json.load(f))

    def save(self, ids):
        with open(self.filename, "w") as f:
            json.dump(sorted(list(ids)), f, indent=4)

    def exists(self, listing_id):

        ids = self.load()

        return listing_id in ids

    def add(self, listing_id):

        ids = self.load()

        ids.add(listing_id)

        self.save(ids)