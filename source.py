class Source:
    # will hold all the source objects
    # this variable is the same for all instances and the class
    all_sources = []

    def __init__(self, ident, name, url, query):
        self.ident = ident
        self.name = name
        self.url = url
        self.query = query

        # when a source object is initialized
        # it appends itself to all_sources
        Source.all_sources.append(self)

    def GetIdent(self):
        return self.ident

    def GetName(self):
        return self.name

    def GetUrl(self):
        return self.url

    def GetQuery(self, term):
        return f'{self.query}{term}'

    # static method can be called without creating an instance
    # can also be called from the Source class
    @staticmethod
    def GetSources():
        return Source.all_sources

    def __str__(self):
        return f'{self.name}'

    __repr__ = __str__
