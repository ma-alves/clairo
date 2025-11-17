# clairo
Batizado em homenagem a cantora indie, clairo é um chat app desenvolvido com o intuito de explorar as possibilidades de WebSockets com entrega de mensagens em tempo real e monitoramento de status online, utilizando código assíncrono em seus consumidores através do Django Channels e Redis como Message Broker. O foco é o desenvolvimento do backend, enquanto o frontend possui uma interface simples e intuitiva construída utilizando Tailwind.

## Tech Stack
- [Django](https://github.com/django) - Web Framework
- [Channels](https://github.com/django/channels) - Extensão do Django para código assíncrono
- [Daphne](https://github.com/django/daphne) - Servidor HTTP/Websocket
- [SQLite3](https://www.sqlite.org/index.html) - Banco de Dados SQL
- [Redis](https://redis.io/) - Message Broker
- [Tailwind](https://tailwindcss.com/) - CSS Framework
- [Docker](https://www.docker.com/) - Containers

## Uso
1. Clone este repositório:\
`git clone https://github.com/ma-alves/clairo.git`
2. Crie o banco de dados e faça as migrações:\
`touch database.db`\
`uv run python3 manage.py makemigrations`\
`uv run python3 manage.py migrate`\
3. Inicie o container Redis:\
`docker run --rm -p 6379:6379 -e TZ=America/Sao_Paulo redis:7`
4. Inicie o servidor:\
`uv run python3 manage.py runserver`
