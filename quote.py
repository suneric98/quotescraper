class Quote:
    def __init__(self, author, quotes):
        self.__author = author
        self.__quote = quotes

    def get_quote(self):
        return self.__quote

    def get_author(self):
        return self.__author
    
    def set_quote(self, quote):
        self.__quote = quote