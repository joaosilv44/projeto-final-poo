from datetime import datetime

# DATA DA ATUALIZAÇÃO: 07.01.2026 as 21:00 da noite
class AbstractEmployee(ABC): 
    """
    A classe abstrata Employee é tida como base comum para todo tipo de funcionário.
    Logo, garante todas as regras de funcionamento, estrutura e comportamento. Onde, funciona sem a necessidade de instâncias diretas. 
    """
    
    @abstractmethod
    def register_entry(self):
        pass
    
    """
    Regra de registro da saída do funcionário
    """
    @abstractmethod
    
    def register_exit(self):
        pass
    
    """
    Regra do cálculo matemático das horas extras do funcionário, é levada em conta a atual jornada trabalhista de oito horas (8).
    """
    @abstractmethod
    def calculate_overtime(self, day_type="Normal"):
        pass 
    
    @abstractmethod
    def request_vacation(self):
        pass
    
    @abstractmethod
    def request_raise(self,percentage):
        pass
    
    @abstractmethod
    def employee_stattus(self):
        pass
    
class ClockMixin:
    """
    O Mixin acima encapsula o controle de ponto, onde permite o reuso em diferentes tipos de funcionários.
    O mesmo não é acoplado ao modelo final da classe.
    """
    
    def register_entry(self):
        if self.__entry_time is not None:
            return "Sua entrada já foi registrada..."

        self.__entry_time = datetime.now()
        return "A entrada foi regiistrada com sucesso!."
    
    
    def register_exit(self):
        if not self.__entry_time:
            return "A entrada não foi registrada"
        
        exit_time = datetime.now()
        worked_hours = (exit_time - self.__entry_time).seconds / 3600
        
        self.__hours_worked += worked_hours
        
        if worked_hours > 8:
            self.__overtime += worked_hours - 8
            
        self.__entry_time = None
        return "A Saída foi registrada"
    
    
#! classe abstrata de Client -> serve de base para o desenvolvimento da mesma.
class AbstractClient(ABC):
    
    @abstractmethod
    def buy(self, product, quantity_pallets, unit_value_pallet):
        pass

    @abstractmethod
    def client_category(self):
        pass
    
    @abstractmethod
    def summary_client(self):
        pass
    
    @abstractmethod
    def volume_discount(self, quantity_pallets):
        pass

    @abstractmethod
    def add_loyalty_points(self, buy_value):
        pass
    
    @abstractmethod
    def claim_points(self):
        pass
    
    @abstractmethod
    def check_promotion(self, buy_value):
        pass
    
    @abstractmethod
    def rate_service(self, stars):
        pass
    
    @abstractmethod 
    def client_status(self):
        pass

#!interface class client
class LoyaltySistem(ABC):
    
    @abstractmethod
    def claim_points(self):
        pass
    
    @abstractmethod
    def add_loyalty_points(self, buy_value):
        pass
    
#! mixin class client
class ReviewMixin:
    def rate_service(self, stars):
        
        descriptions = {
            5: "Atendimento Excelente",
            4: "Atendimento Bom",
            3: "Bem Razoável",
            2: "Atendimento Ruim",
            1: "Péssimo"
        }
        
        if stars not in descriptions:
            return "Avaliação Inválida, ultilize a escala de 1 a 5 para a avaliação do atendimento."
        
        self.__reviews.append(stars)
        return f"Obrigado, a sua avaliação foi: {stars} estrelas ({descriptions[stars]})"
        

#  DATA DA ATUALIZAÇÃO: 02.01.2026 as 22:30 da noite
class Client: 
    def __init__(self, name, cnpj, id_client, credit_limit, costumer_preferences, status_client, registration_date, address, phone, client_type, loyalty_points=0):
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
        self.__purchase_history = []
        self.__reviews = []


# método de compra de pallets
    def buy(self, product, quantity_pallets, unit_value_pallet):
        
        #valor bruto
        gross_value = quantity_pallets * unit_value_pallet
       
       #desconto acerca do volume 
        discount_rate = self.volume_discount(quantity_pallets)
        discount_value = gross_value * discount_rate
        
        #valor final com o desconto.
        final_value = gross_value - discount_value

        self.__purchase_history.append({
        "Product": product, 
        "Quantity Pallets": quantity_pallets, 
        "Unit Value": unit_value_pallet,
        "Gross Value": gross_value,
        "Discount": int(discount_rate * 100),
        "Final Value": final_value,
        "Date": datetime.now()
        })
        
        if quantity_pallets > 1:
            self.add_loyalty_points(final_value)
        return final_value
    
    def volume_discount(self, quantity_pallets):
        if quantity_pallets >= 75:
            return 0.30
    
        elif quantity_pallets >= 50:
            return 0.25
    
        elif quantity_pallets >= 20:
            return 0.15
        
        elif quantity_pallets >= 10:
            return 0.05
        
        else: 
            return 0
    
#adiciona pontos acumulativos de acordo com o valor da conta; neste quesito é creditado pontos quando o cliente faz compras acima de 1 pallet de produtos.
    def add_loyalty_points(self, buy_value):
        points = int(buy_value // 10)
        self.__loyalty_points += points
    
#método de resgate de pontos acumulativos; acima de 0; mostra a quantidade de pontos arrecadados/ou não pelo cliente 
    def claim_points(self):
        if self.__loyalty_points <= 0:
            return "O Cliente não possui pontos para resgatar"
        
        points_redeemed = self.__loyalty_points
        self.__loyalty_points = 0
        
        return f"O cliente arrecadou {points_redeemed} pontos com sucesso!"
    
    
 #cliente checa se recebe/aplica preco promocional no valor da compra; caso possua desconto ou frete grátis ele é informado automaticamente.
    def check_promotion(self, buy_value):
        
        discount = 0
        
        if self.__loyalty_points >= 500:
            discount = 0.20  
        elif self.__loyalty_points >= 200:
            discount = 0.10
        
        value_with_discount = buy_value - (buy_value * discount)
        
        return{
            "Desconto Aplicado": f"{int(discount * 100)}%",
            "Valor Final": value_with_discount
        }
        
    ##avaliação do servico -->  o cliente que avalia o serviço da distribuidora
    def rate_service(self, stars):
        
        descriptions = {
            5: "Atendimento Excelente",
            4: "Atendimento Bom",
            3: "Bem Razoável",
            2: "Atendimento Ruim",
            1: "Péssimo"
        }
        
        if stars not in descriptions:
            return "Avaliação Inválida, ultilize a escala de 1 a 5 para a avaliação do atendimento."
        
        self.__reviews.append(stars)
        return f"Obrigado, a sua avaliação foi: {stars} estrelas ({descriptions[stars]})"

#mecanização de categoria do cliente; é levado em conta o valor que ele deixa no caixa da distribuidora
# (criado com dicionários)
    def client_category(self):
        
        DIAMOND = 1000000
        GOLD = 300000
        SILVER = 100000
        
        total_revenue = sum(p["Final Value"] for p in self.__purchase_history)
        
        if total_revenue >= DIAMOND:
            return {
                "Categoria Atual": "Diamante",
                "Nivel Comercial": "Top Account",
                "Descrição da Categoria": "Este cliente possui visão estratégica e altos valores em faturamento",
                "Benefícios": [
                    "Possui desconto exclusivo",
                    "Atendimento prioritário",
                    "Crédito Estendido",
                    "Negociação personalizada com a distribuidora"
                ]
                
            }
            
        elif total_revenue >= GOLD:
            return {
                "Categoria Atual": "Ouro",
                "Nivel Comercial": "Alta performance",
                "Descrição da Categoria": "Cliente com excelente volume de compras",
                "Benefícios": [
                    "Desconto Diferenciado",
                    "Crédito Facilitado pela distribuidora"
                ]
            }
            
        elif total_revenue >= SILVER:
            return {
                "Categoria Atual": "Prata",
                "Nivel Comercial": "Em crescimento",
                "Descrição da Categoria": "Este cliente com ótimo potencial de crescimento",
                "Benefícios": [
                    "Programa de fidelidade padrão"
                ]
            }
            
        else:
            return {
                "Categoria Atual": "Bronze",
                "Nivel Comercial": "Ainda iniciando",
                "Descrição da Categoria": "Este cliente está em fase inicial de relacionamento",
                "Benefícios": [
                    "Condições comerciais básicas"
                ]
            }
             
#sumario simples do cliente (criado com um dicionário):
    def summary_client(self):
        return {
            "Name": self.__name,
            "Tipo de Cliente": self.__client_type,
            "Categoria": self.client_category(),
            "Pontos de Fidelidade": self.__loyalty_points,
            "Total de Compras" : self.__purchase_history
        }
        
#verifica se o clinete está ativoo conforme a data presebte na lista de compras:
    def client_status(self):
        
        if not self.__purchase_history:
            return "Cliente Inativo no Sistema"
        
        last_purchase_date = self.__purchase_history[-1].get("Date")
        
        if not last_purchase_date:
            return "Cliente Ativo no Sistema"
        
        days = (datetime.now() - last_purchase_date).days
        return "Cliente Ativo" if days <= 90 else "Cliente Inativo"

#  DATA DA ATUALIZAÇÃO: 03.01.2026 as 17:17 da tarde 
class Employee:
    def __init__(self, name, shift, cpf, salary, id_employee, departament, status_employee, admission_date, contract_type, position, meta_monthly, overtime, hours_worked):
        self.__name = name 
        self.__shift = shift
        self.__id_employee = id_employee
        self.__departament = departament
        self.__salary = salary 
        self.__cpf = cpf
        self.__status_employee = status_employee
        self.__admission_date = admission_date
        self.__contract_type = contract_type
        self.__position = position
        self.__meta_monthly = meta_monthly
        self.__overtime = overtime
        self.__hours_worked = hours_worked
        self.__entry_time = None


    def rehister_entry(self):
        if self.__entry_time is not None:
            return "Sua entrada já foi registrada..."

        self.__entry_time = datetime.now()
        return "A entrada foi regiistrada com sucesso!."
    

    def register_exit(self):
        if not self.__entry_time:
            return "A entrada não foi registrada"
        
        exit_time = datetime.now()
        worked_hours = (exit_time - self.__entry_time).seconds / 3600
        
        self.__hours_worked += worked_hours
        
        if worked_hours > 8:
            self.__overtime += worked_hours - 8
            
        self.__entry_time = None
        return "A Saída foi registrada"
        
         
    def review_stock(self, stock):

        reviewed_stock  = []
        
        for item in stock:
            reviewed_stock.append({
                
                "product": item["product"],
                "pallet_quantity": item["pallet_quantity"],
                "storage_type": item["storage_type"],
                "condition": item["condition"]
            })
                    
        return reviewed_stock
               
#calculo da hora extra com base no tipo de dia trabalhado - normal, domingo o feriado:
#é considerado aspenas as horas que passam da jornada de 8 horas e aplica o adicional de 50 ou 100

    def calculate_overtime(self, day_type = "Normal"):
        standard_daily_hours = 8
        
        if self.__hours_worked <= standard_daily_hours:
            return 0.0
    
        extra_hours = self.__hours_worked - standard_daily_hours
        hourly_value = self.__salary / 200
        
        if day_type == "feriado" or day_type == "domingo":
            overtime_rate = 2.0 # 100 por cento 
            
        else: 
            overtime_rate = 1.5
        
        overtime_value = extra_hours * hourly_value * overtime_rate
        return round(overtime_value, 2)
            
#? deve ter um método do GERENTE p aprovar as ferias:

    def request_vacation(self):
        if self.__status_employee == "Ferias":
            return "O funcionário se encontra em recesso."
  
        vacation_request = {
            "employee": self.__name,
            "employee_id": self.__id_employee,
            "departament": self.__departament,
            "request_date": datetime.now(),
            "status": "Aguardando a avaliação do Gerente"
        }
        
        return {
            "mensagem": "Olá, a sua solicitação de férias foi registrada com sucesso!",
            "despacho": "O pedido se encontra na análise do Gerente",
            "detalhes": vacation_request
        }
    
    
    def request_raise(self, percentage):
        if percentage <= 0:
            return "Este percentual de aumento é inválido."
        
        request_raise = {
            "employee": self.__name,
            "employee_id": self.__id_employee,
            "current_salary": self.__salary,
            "request_percentage": percentage,
            "request_date": datetime.now(),
            "status": "Aguardando a avaliação do Gerente"
        }
        
    #regra: acima de 15% precisa de aprovaçãoo do gerente:
        if percentage > 15:
            request_raise["Observação"] = "Aumentos acima de 15% necessitam da análise da Gerência"
        
        return {
            "mensagem": "Olá, o seu pedido de aumento salarial foi registrada com sucesso!",
            "despacho": "O pedido se encontra na análise do Gerente",
            "detalhes": request_raise
        }

# DATA DA ATUALIZAÇÃO: 08.01.2026 as 14:33 da tarde
class Seller(Employee): 
    def __init__(self, name, shift, cpf, salary,id_employee,departament,status_employee,admission_date,contract_type,position,overtime, hours_worked, meta_monthly, commision_percentual):
        
        super().__init__(name, commision_percentual,shift, cpf, salary, position, id_employee, departament, status_employee, admission_date, contract_type, position, meta_monthly, overtime, hours_worked)
        
        self.__costumers_served = []
        self.__pallets_sold = 0
        self.__quantity_invites = []
        self.__comission_percentual = commision_percentual
        self.__sales_made = []
        
    @property
    def meta_monthly(self):
        return self.__meta_monthly
    
    @meta_monthly.setter
    def meta_monthly(self, value):
        if value <= 0:
            raise ValueError("A meta deve ser maior do que zero")
        self.__meta_monthly = value
        
    @property
    def pallets_sold(self):
        return self.__pallets_sold
        
    
    def attend_costumer(self, costumer):
        self.__costumers_served.appen(costumer)
        
        
    def make_sale(self, costumer, product, quantity):
        
        sale = {
            "costumer":costumer,
            "product":product,
            "quantity":quantity
        }
        
        self.__sales_made.append(sale)
        
    def follow_customer(self, client):
        return f"Acompanhamento realizado com o cliente {client}"
    
    def apply_customer_benefi(self, client):
        return f"O benefício de fidelidade foi aplicado ao cliente {client}"
    
    def negotiate_price(self, discount):
        if discount < 0 or discount > 0.15:
            raise ValueError("O desconto deve encontrar-se entre 0% e 15%")
        return f"Desconto de {discount * 100}% aprovado!"
    
    def verify_meta_monthly(self):
        return self._Employee__meta_monthly <= self.__pallets_sold
    
        
    def calculate_comissions(self):
        return self.__pallets_sold * self.__comission_percentual
    
    def register_service(self, client):
        self.__quantity_invites.append(client)
        
    def request_evaluation(self, note):
        if note < 1 or note > 5:
            raise ValueError(" A nota se encontra em uma escala de 1 a 5.")
        
    def respond_to_complaint(self, client):
        return f"Reclamação do cliente {client} foi respondida"
    
    def sumary_sales(self):
        return {
        "clientes_atendidos": len(self.__customers_served),
        "vendas_realizadas": len(self.__sales_made),
        "paletes_vendidos": self.__pallets_sold,
        "comissao": self.calculate_comissions()
    }

#!ver isso ainda
    def see_costumer_credit(self, client):
        if client
        
        


        
class Product:
    def __init__(self, name,promotional_price, category, barr_code, valid_date, brand,quantity, price, dimensions):
        self.__name = name
        self.__promotional_price = promotional_price
        self.__category = category
        self.__barr_code = barr_code
        self.__valid_date = valid_date
        self.__brand = brand
        self.__menge = quantity
        self.__price = price
        self.__dimensions = dimensions

    def __str__(self): #Manipulação de como será impresso na tela o objeto Produto
        return (
            f"{self.__nome} | Qauntidade:{self.__quantidade} | Preço: {self.__preco} | Val.:{self.__dataValidade}"
        )

class Estoque:
    def __init__(self,status, responsible, capacity):
        self.status = status
        self.responsible = responsible
        self.pallet_list = ["1", "2", "3"] #usei ppara testar a lista
        self.historic_mov = ""
        self.capacity = capacity

    def add_pallet(self, pallet):
        """
        Método que adiciona um novo pallet na lista de pallet do estoque que estamos trabalhando no momento.
        Utiliza o método append para adicionar um objeto 'pallet' em 'pallet_list'.
        """
        self.pallet_list.append(pallet)
        return "Pallet cadastrado!"
    
    def search_product_id(self, id):
        """ 
        Método de busca, procura por objetos que existam dentro de pallet_list de acordo com seu id.
        """
        for p in self.pallet_list:
            if id == p.id:
                return f"{p}"
            else:
                return "Pallet não encontrado!"
            
    def delete_pallet(self, pallet):
        """ 
        Remove da lista objetos pallet que correspondem ao pallet passado como atributo. Usa o método remove.
        """
        for p in self.pallet_list:
            if p == pallet:
                self.pallet_list.remove(p)
                return "Pallet removido!"


