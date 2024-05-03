from datetime import date


class DomainBookmark:
    """
    Bookmark domain model. Note, this is much simpler than P&G's domain model.
    This could be imporved by adding type annotations so python and django know what should be coming
    it works great this way provided that the correct input is given.
    """

    def __init__(self, id, title, url, notes, date_added):
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.date_added = date_added

    def __str__(self):
        return f"{self.title}"
