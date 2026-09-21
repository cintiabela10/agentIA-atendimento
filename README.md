# strands-agents-ollama
Strands Agents usando Ollama baseado no workshop "Criação de agentes de IA com o SDK Strands: de loops simples a enxames de vários agentes" do AWS Builder Center.
Todo código e organização foi basicamente criado seguindo o workshop disponível [aqui](https://catalog.us-east-1.prod.workshops.aws/workshops/083b80d7-5a90-402b-9bb4-19fb53092808/en-US), com adaptações em português e usando o modelo Ollama para rodar o agente localmente sem precisar de credenciais AWS.

# Visão Geral
Construir um agente de atendimento ao cliente com o Strands Agents que pesquisa clientes, verifica pedidos e processa reembolsos.
Inspecionar o loop do agente em ação (User → LLM → Tool Call → Tool Result → LLM → Response)
O loop do agente alterna entre o LLM e suas ferramentas até que o modelo tenha informações suficientes para responder. A solicitação do usuário é enviada ao LLM, que decide chamar uma ferramenta, lê o resultado e chama outra ferramenta ou retorna a resposta final.
