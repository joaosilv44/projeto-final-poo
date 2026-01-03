from datetime import datetime

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
        
        #v. bruto
        gross_value = quantity_pallets * unit_value_pallet
       
       #desconto acerca do volume 
        discount_rate = self.volume_discount(quantity_pallets)
        discount_value = gross_value * discount_rate
        
        #v. final c desconto add.
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
    
#adiciona pontos acumulativos de acordo com o valor da conta; neste quesito é creditado pontos uando o cliente faz compras acima de 1 pallet de produtos.
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
            

