# clairo
Batizado em homenagem a cantora indie, clairo é um chat app desenvolvido com o intuito de explorar as possibilidades de WebSockets com entrega de mensagens em tempo real e monitoramento de status online, utilizando código assíncrono em seus consumidores através do Django Channels e Redis como Message Broker. O foco é o desenvolvimento do backend, enquanto o frontend possui uma interface simples e intuitiva construída utilizando Tailwind.

## Tech Stack
- [Django](https://github.com/django) - Web Framework
- [Channels](https://github.com/django/channels) - Extensão do Django para código assíncrono
- [Daphne](https://github.com/django/daphne) - Servidor HTTP/Websocket
- [PostgreSQL](https://www.postgresql.org) - Banco de Dados SQL
- [Redis](https://redis.io/) - Message Broker
- [Docker](https://www.docker.com/) - Containers
- [Tailwind](https://tailwindcss.com/) - CSS Framework

## Uso
1. Clone o repositório:\
`git clone https://github.com/ma-alves/clairo.git`
2. Por enquanto .env não está disponível, mas as configurações são as seguintes:\
`DJANGO_SECRET_KEY=your_secret_key`\
`DEBUG=True`\
`DJANGO_LOGLEVEL=info`\
`DJANGO_ALLOWED_HOSTS=localhost`\
`DATABASE_ENGINE=postgresql_psycopg2`\
`DATABASE_NAME=dockerdjango`\
`DATABASE_USERNAME=dbuser`\
`DATABASE_PASSWORD=dbpassword`\
`DATABASE_HOST=db`\
`DATABASE_PORT=5432`
3. Utilize o Docker Compose para iniciar os serviços:\
`docker compose up --build`
