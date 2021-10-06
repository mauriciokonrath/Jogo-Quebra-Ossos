from DAO.DAO import DAO

# DAO do ranking HERENÇAO do DAO
class PontuacoesDAO(DAO):

    def __init__(self):
        super().__init__('versao_final/src/pontuacoes.json')

    def add(self, key=None, value=None, ranks=None):
        if isinstance(key, str) and isinstance(value, float) and ranks is None:
            super().add(key, value)

        # elif isinstance(ranks, dict):
        #     for nome, pontuacao in ranks.items():
        #         self.add(nome, pontuacao)
