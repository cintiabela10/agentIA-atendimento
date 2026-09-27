# agentIA

Protótipo de um agente de atendimento ao cliente para uma loja de eletrônicos. O projeto foi inspirado no workshop [Criação de agentes de IA com o SDK Strands: de loops simples a enxames de vários agentes](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US), mas a implementação atual **não utiliza o Strands Agents**.

O agente foi implementado em Python usando o cliente `openai` para acessar a API compatível com OpenAI da [Groq](https://groq.com/), com o modelo `qwen/qwen3.8-27b`. As informações de clientes e pedidos são lidas de `base_dados.json`, que também é usado para registrar chamados de suporte.

## O que o programa faz

- Recebe mensagens do usuário em um terminal interativo.
- Consulta o modelo de linguagem para decidir se precisa usar uma ferramenta.
- Busca dados de um cliente pelo ID.
- Consulta o histórico de pedidos de um cliente, incluindo status, datas e código de rastreio.
- Abre chamados de suporte técnico e gera um protocolo.
- Envia os resultados das ferramentas de volta ao modelo para produzir a resposta final.

As ferramentas disponíveis são definidas em `ferramentas.py`:

- `buscar_cliente`
- `obter_historico_pedido`
- `abrir_chamado_suporte`

## Fluxo de uma solicitação

```text
Usuário -> modelo de linguagem -> chamada de ferramenta (opcional)
		 -> resultado da ferramenta -> modelo de linguagem -> resposta
```

Na implementação atual, o programa faz uma chamada inicial ao modelo. Quando há chamadas de ferramentas, executa as funções correspondentes e faz uma segunda chamada ao modelo com os resultados. Não há uma arquitetura de múltiplos agentes nem um loop de ferramentas contínuo.

## Configuração

1. Instale as dependências:

	```bash
	pip install -r requirements.txt
	```

2. Crie um arquivo `.env` na raiz do projeto com uma chave da Groq:

	```env
	GROQ_API_KEY=sua-chave-aqui
	```

## Como executar

```bash
python agent.py
```

Digite uma solicitação no terminal. Para encerrar, use `sair`, `exit`, `quit` ou `fechar`.

## Estrutura do projeto

- `agent.py`: configura o cliente da Groq, define o prompt do sistema e executa o agente.
- `ferramentas.py`: implementa as ferramentas e seus schemas enviados ao modelo.
- `base_dados.json`: banco de dados local de clientes, pedidos e chamados.
- `requirements.txt`: dependências Python do projeto.
