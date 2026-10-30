# Agente de atendimento para loja online

## O que é o projeto?

Este projeto é um agente de atendimento para uma loja online. Ele conversa com o cliente pelo terminal, consulta dados locais de clientes e pedidos e pode abrir chamados de suporte.

O agente usa Python e a API compatível com OpenAI da [Groq](https://groq.com/), com o modelo configurado em `config.py`. As informações são armazenadas em `data_base.json`.

## Como rodar?

### 1. Instale as dependências

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
```

### 2. Configure a chave da Groq

Crie um arquivo `.env` na raiz do projeto com sua chave de API:

```env
GROQ_API_KEY=sua-chave-aqui
```

### 3. Inicie o agente

```bash
python agent.py
```

Digite sua solicitação no terminal. Para encerrar, digite `sair`.

## Quais ferramentas(tools) existem?

O agente possui as seguintes ferramentas:

- **`get_customer`**: busca os dados de um cliente pelo ID.
- **`get_order_history`**: consulta o histórico de pedidos de um cliente, incluindo informações como status, datas e código de rastreio.
- **`open_support_ticket`**: abre um chamado de suporte para um cliente, registra a descrição do problema e gera um protocolo.

## Fluxo de uma solicitação

```text
Usuário -> modelo de linguagem -> chamada de tool (opcional)
         -> resultado da tool -> modelo de linguagem -> resposta
```

O modelo decide quando usar uma tool. O programa executa a função correspondente, envia o resultado de volta ao modelo e exibe a resposta final no terminal.

## Estrutura do projeto

```text
.
├── agent.py
├── config.py
├── data_base.json
├── db.py
├── requirements.txt
├── .env.example
└── tools/
    ├── __init__.py
    ├── customers.py
    ├── orders.py
    └── support.py
```

- `agent.py`: executa o loop de conversa e processa as chamadas de tools.
- `config.py`: carrega a variável `GROQ_API_KEY`, configura o cliente da Groq e define o prompt do sistema.
- `data_base.json`: banco de dados local de clientes, pedidos e chamados.
- `db.py`: fornece as funções para ler e salvar o banco de dados local.
- `requirements.txt`: lista as dependências Python do projeto.
- `.env.example`: exemplo das variáveis de ambiente necessárias.
- `tools/customers.py`: implementa a tool `get_customer`.
- `tools/orders.py`: implementa a tool `get_order_history`.
- `tools/support.py`: implementa a tool `open_support_ticket`.
- `tools/__init__.py`: registra as tools disponíveis para o agente.
