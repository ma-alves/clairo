# papo

Papo é um chat app em tempo real desenvolvido com Django Channels que utiliza WebSockets como protocolo de comunicação, Redis como Pub/Sub nas channel layers nativas e PostgreSQL para persistência. A aplicação não coleta informações pessoais priorizando a privacidade dos usuários em um ambiente designado para interações rápidas e casuais, e nesse cenário a recuperação de senhas é feita através de um PAT (Personal Access Token) disponibilizado ao usuário após o seu cadastro.

## Tech Stack
- [Django](https://github.com/django) - Web Framework
- [Channels](https://github.com/django/channels) - Extensão do Django para código assíncrono e WebSockets
- [Daphne](https://github.com/django/daphne) - Servidor ASGI/WebSocket
- [PostgreSQL](https://www.postgresql.org) - Banco de Dados SQL
- [Redis](https://redis.io/) - Channel Layer (Pub/Sub)
- [Tailwind](https://tailwindcss.com/) - CSS Framework
- [Docker Compose](https://docs.docker.com/compose/) - Orquestração multi-container
- [GitHub Actions](https://github.com/features/actions) - CI/CD

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
- Cadastro com username e senha via formulário Django
- Geração automática de token criptografado (Fernet) via signal `post_save`
- Validação de token no primeiro acesso
- Recuperação de senha utilizando Personal Access Token criado no cadastro do usuário
- Autenticação de sessão para conexões WebSocket via `AuthMiddlewareStack`
- Proteção de views com `@login_required` e `LoginRequiredMixin`

## Detalhes Técnicos

### Consumidores WebSocket
O módulo `consumers.py` implementa dois consumidores assíncronos:

**ChatConsumer** (`ws/chat/<chat_uuid>/`)
- Estabelecimento e encerramento de conexões em chats UUID
- Recebimento, validação e persistência de mensagens

**OnlineConsumer** (`ws/online-status/`)
- Rastreamento de presença (conexão/desconexão)
- Atualização do status no banco via `UserOnlineStatus`
- Broadcasting de mudanças de status para todos os clientes

### Modelo de Dados
- **User**: Usuários do sistema (modelo padrão do Django)
- **Chat**: Sala de conversa identificada por UUID, com controle de usuários online
- **ChatMessage**: Mensagens com autor, corpo do texto, timestamp e FK para Chat
- **UserOnlineStatus**: One-to-one com User, rastreia presença online/offline
- **UserToken**: Token criptografado (Fernet) para validação de primeiro acesso

### Camada de Persistência
- PostgreSQL para dados estruturados (usuários, mensagens, conversas)
- Índices em timestamps para ordenação eficiente de mensagens
- Transações ACID para garantir consistência de dados

### Camada de Frontend
- JavaScript vanilla com três módulos WebSocket:
  - `chat.js` — gerencia a sala de chat, envio/recebimento de mensagens e renderização no DOM
  - `online.js` — broadcast de status online na página inicial (lista de chats)
  - `online-profile.js` — indicador de status online na página de perfil do usuário
- DOM updates com Tailwind CSS para estilização

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
├── accounts/              # Autenticação e gerenciamento de usuários
│   ├── forms.py           # Formulários de cadastro, token e senha
│   ├── models.py          # UserToken (token criptografado)
│   ├── signals.py         # Geração automática de token no post_save
│   ├── utils.py           # Criptografia Fernet
│   └── views.py           # Signup, token validation, reset de senha
├── chat/                  # Lógica principal do chat
│   ├── consumers.py       # ChatConsumer e OnlineConsumer (WebSocket)
│   ├── exceptions.py      # ClientError customizada
│   ├── models.py          # Chat, ChatMessage, UserOnlineStatus
│   ├── routing.py         # Rotas WebSocket (/ws/chat/, /ws/online-status/)
│   ├── static/js/         # chat.js, online.js, online-profile.js
│   ├── templates/chat/    # Templates HTML do chat
│   └── views.py           # Home, chat, search, profile, delete
├── papo/                  # Configurações do projeto
│   ├── asgi.py            # ASGI com ProtocolTypeRouter
│   ├── settings.py        # Configurações Django + Channels + Redis
│   └── urls.py            # Rotas HTTP
├── templates/             # Templates base (login, signup, 404, 500)
├── .github/workflows/     # CI/CD (test, deploy)
├── compose.yaml           # Orquestração Docker (PostgreSQL + Redis + web)
├── Dockerfile             # Multi-stage build com uv
├── pyproject.toml         # Dependências e configuração Ruff
└── manage.py              # CLI do Django
```

## CI/CD com GitHub Actions

O projeto utiliza **GitHub Actions** para automação de testes e deploy. A pipeline é executada em pushes para `main`/`dev` e pull requests, além de poder ser acionada manualmente.

### Pipeline (`deploy.yaml`)

**Job: test** (executado em todos os pushes/PRs)
1. **Setup**: Python via `.python-version`, pacotes com `uv sync --locked --all-extras --dev`
2. **Serviços**: PostgreSQL 17 e Redis 7 com health checks
3. **Migrações**: `python manage.py migrate`
4. **Testes**: `python manage.py test`

**Job: deploy** (executado apenas no merge em `main`, após testes)
1. **Deploy no Render**: via webhook (`RENDER_DEPLOY_HOOK_URL`)

### Variáveis de Ambiente
- Configuradas via GitHub Secrets: `DJANGO_SECRET_KEY`, `FERNET_KEY`, `RENDER_DEPLOY_HOOK_URL`
- Hosts de banco e Redis configurados para o runner

### Benefícios

- **Validação Automática**: Cada commit é testado automaticamente
- **Detecção de Regressões**: Falhas impedem o deploy
- **Consistência**: Ambiente de teste reproduzível e isolado
- **Segurança**: Secrets gerenciados via GitHub Secrets

## Testes

O projeto inclui testes unitários nos módulos de `tests.py` para validar:
- Funcionalidade de autenticação
- Comportamento dos consumers WebSocket
- Persistência e recuperação de mensagens

*Observação*: a cobertura de testes ainda não está 100%

*Documento parcialmente gerado por IA, revisado e mantido por ma-alves.*
