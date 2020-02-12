class Advertisement(object):
    """
    The Advertisement object contains information about parsed ad
    """

    def __init__(self):
        self.title = None
        self.location = None
        self.details = None
        self.contacts = None
        self.description = None
        self.url = None

    def __str__(self):
        description = self.description
        if len(description) > 128:
            description = self.description[:128] + '...'

        string = (
            f'Title:\t\t{self.title}\n'
            f'Location:\t{self.location}\n'
            f'Ad details:\t{self.details}\n'
            f'Contacts:\t{self.contacts}\n'
            f'Description:\t{description}\n'
            f'URL:\t\t{self.url}\n'
        )
        return string

    def to_dict(self):
        ad = {
            'title': self.title,
            'location': self.location,
            'details': self.details,
            'contacts': self.contacts,
            'description': self.description,
            'url': self.url,
        }
        return ad
