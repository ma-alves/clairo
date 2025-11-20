# Imagem com uv instalado
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Variáveis para otimizar o uv e evitar downloads desnecessários
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Instalar projeto em `/app`
WORKDIR /app

# Instalar dependencias sem instalar o projeto
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copiar o código do projeto
COPY . /app

# Sincronizar as dependências e instalar o projeto
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Multistage: imagem final
FROM python:3.12-slim-bookworm

# Usuário non-root
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copiar a aplicação do estágio de build
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Váriaveis de ambiente para otimizar o python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# non-root para executar a aplicação
USER nonroot

# Usar `/app` como working directory
WORKDIR /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]