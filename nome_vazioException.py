class NomeVazio(Exception):

    def __init__(self):
        super().__init__("O nome não pode ser um valor vazio!")
