class Client: 
    def __init__(self, name, cnpj, id_client, credit_limit, costumer_preferences, status_client, registration_date, address, phone, client_type, loyalty_points):
        self.__name = name 
        self.__cnpj = cnpj
        self.__id_client = id_client
        self.__credit_limit = credit_limit
        self.__costumer_preferences = costumer_preferences
        self.__status_client = status_client
        self.__registration_date = registration_date
        self.__address = address
        self.__phone = phone
        self.__client_type = client_type
        self.__loyalty_points = loyalty_points

    def get_name(self):
        return self.__name
    
class Product:
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
            

