# Agente de atendimento para loja online

🚀 **[Clique aqui para testar a demonstração ao vivo no Hugging Face Spaces](https://huggingface.co/spaces/cintiabela10/agentIA)** 🚀

## O que é o projeto?

Este projeto é um agente de atendimento para uma loja online. Ele pode consultar dados de clientes, verificar histórico de pedidos, avaliar regras de reembolso, atualizar status de contas e abrir chamados de suporte.

O agente foi construído em Python e usa a API compatível com OpenAI da [Groq](https://groq.com/), com o modelo configurado em `config.py`. Os dados (mock) são armazenados em `data_base.json`.

O projeto conta com duas formas de uso:
- **Interface Web (`app.py`)**: Uma interface de chat moderna usando Gradio, ideal para demonstração no Hugging Face Spaces.
- **Terminal (`agent.py`)**: Um loop de conversa interativo no terminal para testes locais.

## Como rodar localmente

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

### 3. Inicie a aplicação
Para abrir a interface web (Gradio):
```bash
python app.py
```
Para rodar no terminal (modo texto):
```bash
python agent.py
```
Para encerrar, digite `sair`.

## Ferramentas(tools) disponíveis

O agente possui as seguintes ferramentas:

- **`get_customer`**: Busca os dados de um cliente pelo ID.
- **`update_account_status`**: Atualiza o status da conta de um cliente.
- **`get_order_history`**: Consulta o histórico de pedidos de um cliente, incluindo informações como status, datas e código de rastreio.
- **`check_refund_eligibility`**: Verifica se um cliente pode pedir reembolso de um produto.
- **`open_support_ticket`**: Abre um chamado de suporte para um cliente, registra a descrição do problema e gera um protocolo.
- **`list_open_tickets`**: Lista os chamados abertos de um cliente específico.

## Fluxo de uma solicitação

```text
Usuário -> modelo de linguagem -> chamada de tool (opcional)
         -> resultado da tool -> modelo de linguagem -> resposta
```

O modelo decide quando usar uma tool. O programa executa a função correspondente, envia o resultado de volta ao modelo e exibe a resposta final no terminal.

## Estrutura do projeto

```text
.
├── app.py
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
- `app.py`: monta a interface Gradio, converte o histórico de mensagens e chama o run_agent.
- `agent.py`: executa o loop de conversa e processa as chamadas de tools.
- `config.py`: carrega a variável `GROQ_API_KEY`, configura o cliente da Groq e define o prompt do sistema (`SYSTEM_PROMPT`).
- `data_base.json`: banco de dados local de clientes, pedidos e chamados.
- `db.py`: fornece as funções para ler e salvar o banco de dados local.
- `requirements.txt`: lista as dependências Python do projeto.
- `.env.example`: exemplo das variáveis de ambiente necessárias.
- `tools/`: contém a lógica de negócios dividida por domínio (clientes, pedidos e suporte).
