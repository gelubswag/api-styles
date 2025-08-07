from spyne import Integer, Unicode, ComplexModel


class BookSOAP(ComplexModel):
    __namespace__ = 'books'
    id = Integer
    title = Unicode

