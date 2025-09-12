class NotaAssente(Exception):
    def __init__(self):
        super().__init__("La nota e' None")