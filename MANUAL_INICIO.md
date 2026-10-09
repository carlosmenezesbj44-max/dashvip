# Manual de Inicio do App

Este manual mostra como subir o `Dashboard IXC` pela primeira vez no Windows com PowerShell.

## 1. Pre-requisitos

- Python `3.11` ou superior instalado
- Acesso ao IXC com `base_url` e token/API
- PowerShell aberto na pasta do projeto

## 2. Abrir a pasta do projeto

No PowerShell:

```powershell
cd C:\caminho\para\dashboard-ixc
```

## 3. Criar e ativar o ambiente virtual

Crie o ambiente:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativacao do script:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativo, o terminal passa a mostrar `(.venv)` no inicio da linha.

## 4. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Criar o arquivo `.env`

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` e preencha pelo menos:

- `IXC_BASE_URL`
- `IXC_TOKEN`
- `IXC_OS_TABLE`
- `IXC_OS_ID_FIELD`
- `IXC_OS_STATUS_FIELD`
- `IXC_OS_OPENED_AT_FIELD`
- `IXC_OS_EXECUTION_AT_FIELD`
- `IXC_OS_CLOSED_AT_FIELD`
- `IXC_SUBJECT_TABLE`
- `IXC_TECH_TABLE`

Exemplo minimo:

```env
IXC_BASE_URL=https://seu-servidor-ixc.com.br
IXC_TOKEN=Basic seu_token_aqui
IXC_OS_TABLE=su_oss_chamado
IXC_OS_ID_FIELD=id
IXC_OS_STATUS_FIELD=status
IXC_OS_OPENED_AT_FIELD=data_abertura
IXC_OS_EXECUTION_AT_FIELD=data_hora_execucao
IXC_OS_CLOSED_AT_FIELD=data_fechamento
IXC_SUBJECT_TABLE=su_oss_assunto
IXC_TECH_TABLE=funcionarios
```

Observacao importante:

- Em `IXC_BASE_URL`, use apenas a base do servidor.
- Nao inclua `/adm.php`, `/webservice/v1` ou o nome da tabela.

## 6. Iniciar a aplicacao

Com o ambiente virtual ativo:

```powershell
python -m uvicorn app.main:app --reload
```

Se tudo subir corretamente, abra:

- `http://127.0.0.1:8000/` para o dashboard
- `http://127.0.0.1:8000/docs` para a documentacao Swagger

## 7. Validar conexao com o IXC

Voce pode validar de duas formas.

Pelo navegador:

- Abra o dashboard
- Va na aba `Configuracoes`
- Use o teste de conexao

Pelo PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/settings/test-connection"
```

## 8. Descobrir os campos corretos da sua base

Se sua base IXC usa nomes de campos diferentes, rode:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/discovery/os-fields"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/discovery/subject-fields"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/discovery/tech-fields"
```

Use os campos sugeridos para ajustar o `.env`.

## 9. Fazer a primeira sincronizacao

Para carregar a base pela primeira vez, execute uma sincronizacao completa:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/sync?full=true"
```

Depois disso:

- volte ao dashboard
- atualize a pagina
- confira metricas, filtros e detalhes das OS

## 10. Fluxo recomendado de primeira subida

Use esta ordem:

1. Criar e ativar `.venv`
2. Instalar dependencias
3. Copiar `.env.example` para `.env`
4. Preencher `IXC_BASE_URL` e `IXC_TOKEN`
5. Iniciar o app
6. Testar conexao
7. Rodar descoberta de campos
8. Ajustar `.env` se necessario
9. Executar `sync?full=true`
10. Abrir o dashboard e validar os dados

## 11. Comandos uteis do dia a dia

Subir o app:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Rodar sync incremental:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/sync"
```

Rodar sync completa:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/sync?full=true"
```

## 12. Problemas comuns

### PowerShell nao deixa ativar o `.venv`

Use:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

### Erro de timezone no Windows

Instale:

```powershell
pip install tzdata
```

### App sobe, mas nao traz dados

Revise:

- `IXC_BASE_URL`
- `IXC_TOKEN`
- nomes dos campos `IXC_OS_*`
- nomes das tabelas de assunto e tecnico

Depois rode novamente:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/sync?full=true"
```

### Dados de execucao ainda parecem incompletos

Nesse caso o mais importante e validar:

- se `IXC_OS_EXECUTION_AT_FIELD` aponta para o campo certo na sua base
- se a descoberta sugere `data_hora_execucao`, `data_inicio` ou outro campo melhor
- se o IXC realmente registra esses eventos na tabela principal da OS

## 13. Encerrar o app

No terminal onde o `uvicorn` estiver rodando:

```powershell
Ctrl + C
```
