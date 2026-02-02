# papo

Papo é um chat app desenvolvido com o intuito de explorar as possibilidades de WebSockets com entrega de mensagens em tempo real e monitoramento de status online, utilizando código assíncrono em seus consumidores através do Django Channels e Redis como Pub/Sub. O foco é o desenvolvimento do back-end, enquanto o front-end possui uma interface simples construída utilizando Tailwind.

## Tech Stack
- [Django](https://github.com/django) - Web Framework
- [Channels](https://github.com/django/channels) - Extensão do Django para código assíncrono e WebSockets
- [Daphne](https://github.com/django/daphne) - Servidor HTTPS/Websocket
- [PostgreSQL](https://www.postgresql.org) - Banco de Dados SQL
- [Redis](https://redis.io/) - Channel Layer
- [Tailwind](https://tailwindcss.com/) - CSS Framework
- [Docker Compose](https://docs.docker.com/compose/) - Multi-container

## Configuração
1. Clone o repositório:
```bash
git clone https://github.com/ma-alves/papo.git
```
2. Ajuste as variáveis de ambiente:
```bash
cp .env.example .env
```
3. Utilize o Docker Compose para iniciar os serviços:
```bash
docker compose up --build
```
4. A aplicação estará disponível em 0.0.0.0:8000

## Acesso
A aplicação também está disponível em [papo](https://papo-uexb.onrender.com), fique a vontade para me enviar uma mensagem! Meu usuário: [matheus](https://papo-uexb.onrender.com/chat/profile/matheus/)

## Arquitetura

### Fluxo de Comunicação
O projeto utiliza Django Channels para gerenciar conexões WebSocket através de consumidores assíncronos. Cada cliente estabelece uma conexão persistente que é mantida ativa durante toda a sessão do usuário. O Redis funciona como canal de pub/sub, permitindo que múltiplos usuários se comuniquem entre canais dedicados.

### Autenticação e Autorização
- Sistema de autenticação baseado em JWT
- Validação de sessão para conexões WebSocket
- Validação de sessão nos endpoints diferenciando usuários logados

### Gerenciamento de Status Online
- Rastreamento de status de usuários em tempo real
- Atualização automática de presença ao conectar/desconectar
- Broadcasting de mudanças de status para todos os clientes conectados

## Detalhes Técnicos

### Consumidores WebSocket
O módulo `consumers.py` implementa consumidores assíncronos que lidam com:
- Estabelecimento e encerramento de conexões
- Recebimento e armazenamento de mensagens
- Broadcast de mensagens para o chat privado
- Mostra mudanças de status de usuários

### Modelo de Dados
- **User**: Usuários do sistema com informações de perfil
- **Message**: Mensagens armazenadas com timestamps e referências a remetente/destinatário
- **Conversation**: Agrupamento de mensagens entre pares de usuários
- Relacionamentos com índices otimizados para queries de chat history

### Camada de Persistência
- PostgreSQL para dados estruturados (usuários, mensagens, conversas)
- Índices em timestamps para ordenação eficiente de mensagens
- Transações ACID para garantir consistência de dados

### Camada de Frontend
- JavaScript vanilla para gerenciar conexão WebSocket
- Listeners para recebimento de mensagens
- DOM updates utilizando Tailwind para estilização

## Fluxo de Mensagens

1. Usuário A envia uma mensagem através do WebSocket
2. Consumer recebe e valida a mensagem
3. Mensagem é persistida no banco de dados
4. Consumer publica no Redis para todos os subscribers
5. Usuário B recebe a mensagem em tempo real via WebSocket
6. UI atualiza automaticamente com a nova mensagem

## Estrutura de Diretórios

```
papo/
├── accounts/           # Autenticação e gerenciamento de usuários
├── chat/               # Lógica principal do chat (consumers, models, views)
├── papo/               # Configurações do projeto
├── templates/          # Templates HTML (login, cadastro)
├── manage.py           # CLI do Django
└── docker-compose.yaml # Orquestração de serviços
```

## Testes

O projeto inclui testes unitários nos módulos de `tests.py` para validar:
- Funcionalidade de autenticação
- Comportamento dos consumers WebSocket
- Persistência e recuperação de mensagens
*Observação*: a cobertura de testes ainda não está 100%