# Criacao de um agente de IA
# API da OpenAI usando o maritaka como modelo de linguagem
# Importando as bibliotecas necessárias
import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


@tool
def info_restaurante(_: str = ""):
    """Retorna as informações do restaurante."""
    return "Pizzaria Maritaka, Rua dos Bobos, nº 0, São Paulo - SP, Brasil"

@tool
def horario_funcionamento(_: str = ""):
    """Retorna o horário de funcionamento do restaurante."""
    return """Segunda: 17:30 - 23:00
                Terça: Fechado
                Quarta: 17:30 - 23:00
                Quinta: 17:30 - 23:00
                Sexta: 17:30 - 23:00
                Sábado: 17:30 - 23:00
                Domingo: 17:30 - 23:00"""

@tool
def promocoes(_: str = ""):
    """Retorna as promoções do restaurante."""
    return """
            COMBO 1⃣
            Pizza G (8 fatias, 2 sabores) + Pizza P de Apaixonados + Guaraná antártica de 1L

            Combo 2⃣
            Duas Pizzas Grande (8 fatias, 2 sabores) + 1 Coca Cola de 2 litros
            """

@tool
def info_combo(combo: str = ""):
    """Retorna as informações detalhada de cada combo.
       Args:
            combo (str): O número do combo (1 ou 2).
    """
    if combo == "1":
        return """
            COMBO 1⃣
            Pizza G (8 fatias, 2 sabores) + Pizza P de Apaixonados + Guaraná antártica de 1L
            PREÇO RETIRADA:
            > 42,00 reais em espécie ou pix
            > 49,00 reais no cartão de crédito ou débito
            PREÇO ENTREGA:
            > 52,00 reais em espécie ou pix
            > 61,00 reais no cartão de crédito ou débito

            Observacao: os valores acima é com a pizza pequena de apaixonados, caso o cliente queira trocar
            por outro sabor doce, tem um acréscimo de 5,00 reais no valor total do pedido.
            """
    elif combo == "2":
        return """
            COMBO 2⃣
            Duas Pizzas Grande (8 fatias, 2 sabores) + 1 Coca Cola de 2 litros
            PREÇO RETIRADA
            > 77,00 reais em espécie ou Pix
            > 84,00 reais no cartão de crédito ou débito
            PREÇO ENTREGA
            > 86,00 reais em espécie ou Pix
            > 93,00 reais no cartão de crédito ou débito
            """

@tool
def sabores_pizzas(_: str = ""):
    """Retorna os sabores de pizzas disponíveis."""
    return """
            Sabores de Pizza:
            - Calabresa (pequena: 4 fatias, média: 6 fatias, grande: 8 fatias) (40 reais, 50 reais, 60 reais)
            - Frango com Catupiry (pequena: 4 fatias, média: 6 fatias, grande: 8 fatias) (40 reais, 50 reais, 60 reais)
            - Portuguesa (pequena: 4 fatias, média: 6 fatias, grande: 8 fatias) (40 reais, 50 reais, 60 reais)
            - Quatro Queijos (pequena: 4 fatias, média: 6 fatias, grande: 8 fatias) (40 reais, 50 reais, 60 reais)
            - Marguerita (pequena: 4 fatias, média: 6 fatias, grande: 8 fatias) (40 reais, 50 reais, 60 reais)
            """

@tool
def fluxo_pedido_retirada(_: str = ""):
    """Retorna o que é necessario para fazer um pedido para retirada."""
    return """
            O cleinte deve ter escolhido o combo a pizza individual.
            deve Informar o sabor da pizza
            nos casos das pizzas individuais deve informar o tamanho (P, M ou G).
            o método de pagamento (dinheiro, pix, cartão de crédito ou débito).
            voce deve calcular o preço de acordo com o combo e a forma de pagamento ou
            se for a pizza individual deve calcular o preço de acordo com o tamanho e o sabor.
            """


tool_list = [
    info_restaurante,
    horario_funcionamento,
    promocoes,
    info_combo,
    sabores_pizzas,
    fluxo_pedido_retirada
]


class PizzaBot:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0.0, max_tokens=150):
        # Carrega variáveis de ambiente
        load_dotenv()

        # Inicializa o modelo LLM com chave da API
        self.api_key = os.getenv("API_KEY_CHATGPT")
        if not self.api_key:
            raise ValueError("API_KEY_MARITAKA_BOT não encontrada no arquivo .env")

        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Cria o prompt do agente
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um atendente de uma pizzaria que ajuda os clientes a fazer pedidos 
                        e fornece informações sobre o restaurante, utilize as ferramentas
                        disponíveis para responder as perguntas dos clientes."""),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # Cria o agente
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tool_list,
            prompt=self.prompt,
        )

        # Cria o executor do agente
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=tool_list,
            verbose=True
        )

    def perguntar(self, mensagem: str):
        result = self.executor.invoke({"input": mensagem})
        return result