# Dashboard IXC - Ordens de Servico

Plataforma para coletar dados do IXC Software e montar um painel com:

- Quantidade de OS efetuadas hora a hora
- Contador de OS abertas por assunto
- Tecnicos em execucao
- SLA das ordens (dentro e fora do prazo)
- Tempos por tecnico (resposta, execucao e total)
- Filtros por filial, periodo e assunto
- Filtro por grupo de assuntos configuravel

Manual passo a passo de inicializacao: [MANUAL_INICIO.md](./MANUAL_INICIO.md)

## 1. Requisitos

- Python 3.11+
- Acesso ao IXC com token de API

## 2. Instalacao

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configuracao

1. Copie `.env.example` para `.env`
2. Ajuste principalmente:
   - `IXC_BASE_URL`
   - `IXC_TOKEN`
   - Campos da tabela de OS (`IXC_OS_*`)
   - Tabelas/campos de assunto e tecnico
   - Campos de filial (`IXC_OS_BRANCH_ID_FIELD` e `IXC_OS_BRANCH_NAME_FIELD`)

Exemplo rapido:

```env
IXC_BASE_URL=https://seu-servidor-ixc.com.br
IXC_TOKEN=Basic xxxxxxxxxxxxxxxxxxxxx
IXC_OS_TABLE=su_oss_chamado
IXC_OS_STATUS_FIELD=status
IXC_OS_CLOSED_AT_FIELD=data_fechamento
```

Observacao: em `IXC_BASE_URL` use apenas a base do servidor (ex.: `https://seu-servidor-ixc.com.br`), sem `/adm.php`, sem `/webservice/v1` e sem `/su_oss_chamado`.

## 4. Rodando

```bash
uvicorn app.main:app --reload
```

Abra:

- `http://127.0.0.1:8000/` para o dashboard
- `http://127.0.0.1:8000/docs` para Swagger
- Na aba **Configuracoes** do painel voce consegue editar e salvar o `.env` sem abrir arquivo manualmente.

Se estiver no Windows e aparecer erro de timezone (`ZoneInfoNotFoundError`), rode:

```bash
pip install tzdata
```

## 5. Endpoints principais

- `POST /api/sync` -> executa sincronizacao imediata
- `POST /api/sync?full=true` -> forca sincronizacao completa
- `GET /api/metrics/overview?date=YYYY-MM-DD` -> retorna metricas do dashboard
- `GET /api/metrics/overview?date=YYYY-MM-DD&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&subject=...&branch=...` -> metricas com filtros
- `GET /api/metrics/filter-options` -> retorna opcoes de filtros (assuntos/filiais)
- `GET /api/health` -> health check
- `GET /api/settings` -> leitura das configuracoes atuais
- `PUT /api/settings` -> salva configuracoes no `.env` e aplica em runtime
- `POST /api/settings/test-connection` -> valida conexao IXC
- `GET /api/discovery/os-fields` -> analisa tabela de OS e sugere `IXC_OS_*`
- `GET /api/discovery/subject-fields` -> sugere campos de assunto
- `GET /api/discovery/tech-fields` -> sugere campos de tecnico

## 6. Descoberta automatica dos campos da sua base

Depois de preencher `IXC_BASE_URL` e `IXC_TOKEN` no `.env`, rode:

```bash
curl http://127.0.0.1:8000/api/discovery/os-fields
curl http://127.0.0.1:8000/api/discovery/subject-fields
curl http://127.0.0.1:8000/api/discovery/tech-fields
```

Copie os campos sugeridos (`env_suggestions`) para o `.env`.

## 7. Como o SLA e calculado

- Ordem ativa: status nao fechado (config `IXC_STATUS_CLOSED`)
- Em execucao: status configurado em `IXC_STATUS_EXECUTION` ou campo de inicio de execucao preenchido
- Dentro do SLA: `due_at` vazio ou maior/igual ao horario atual
- Fora do SLA: `due_at` menor que o horario atual

## 8. Observacoes importantes

- Estruturas de campo podem mudar por versao/customizacao do IXC.
- Se os nomes de campos forem diferentes na sua base, ajuste no `.env` sem alterar codigo.
- O cliente usa o padrao IXC de consulta via `POST /webservice/v1/{tabela}` com header `ixcsoft: listar`.
- Sincronizacao incremental:
  - `IXC_INCREMENTAL_SYNC=true`: busca apenas novos `os_id` nas execucoes incrementais.
  - `IXC_FULL_SYNC_EVERY_N_RUNS=12`: a cada N execucoes incrementais, roda uma sincronizacao completa para reconciliacao.
- Atualizacao automatica do frontend:
  - `APP_DASHBOARD_REFRESH_SECONDS`: intervalo do auto refresh de metricas.
  - `APP_FILTER_OPTIONS_REFRESH_SECONDS`: intervalo do refresh das opcoes de filtros.
