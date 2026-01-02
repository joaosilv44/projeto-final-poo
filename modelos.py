class Produto:
    def __init__(self, nome, quantidade, preco, dataValidade):
        self.__name = nome
        self.__menge = quantidade
        self.__price = preco
        self.__validDate = dataValidade

    def __str__(self):
        return (
            f"{self.__nome} | Qauntidade:{self.__quantidade} | Preço: {self.__preco} | Val.:{self.__dataValidade}"
        )
    

class Estoque:
    def __init__(self):
        self.produtos = ["1", "2", "3"]

    def adicionar_pallet(self, pallet):
        self.produtos.append(pallet)
        return "Pallet cadastrado!"
    
    def search_product_name(self, id):
        for p in self.products:
            if id == p.id:
                return f"{p}"
            else:
                return "Pallet não encontrado!"
            
    def remover_pallet(self, pallet):
        for p in self.produtos:
            if p == pallet:
                self.produtos.remove(p)
                return "Pallet removido!"
            

