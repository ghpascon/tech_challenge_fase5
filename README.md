# Tech Challenge Fase 5 — Previsão de Defasagem Escolar

Projeto acadêmico **FIAP — Engenharia de Machine Learning** que prevê o grau de defasagem escolar de alunos a partir de indicadores educacionais anonimizados.  
O pipeline cobre desde o pré-processamento dos dados brutos até a exposição do modelo treinado via API REST, com interface web interativa.

---

## Sumário

- [Tech Challenge Fase 5 — Previsão de Defasagem Escolar](#tech-challenge-fase-5--previsão-de-defasagem-escolar)
  - [Sumário](#sumário)
  - [Visão Geral](#visão-geral)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação com Poetry](#instalação-com-poetry)
  - [Configuração](#configuração)
  - [Executando a Aplicação](#executando-a-aplicação)
  - [Notebooks](#notebooks)
    - [`notebooks/1_data_processing.ipynb` — Processamento de Dados](#notebooks1_data_processingipynb--processamento-de-dados)
    - [`notebooks/2_model_train.ipynb` — Treinamento do Modelo](#notebooks2_model_trainipynb--treinamento-do-modelo)
  - [MLflow — Rastreamento de Experimentos](#mlflow--rastreamento-de-experimentos)
  - [API REST](#api-rest)
    - [`GET /api/v1/ml/get_model_info`](#get-apiv1mlget_model_info)
    - [`POST /api/v1/ml/predict`](#post-apiv1mlpredict)
    - [`GET /api/v1/application/get_version`](#get-apiv1applicationget_version)
    - [`GET /api/v1/application/get_alerts`](#get-apiv1applicationget_alerts)
  - [Interface Web](#interface-web)
  - [Interpretando o Resultado](#interpretando-o-resultado)
  - [Testes](#testes)

---

## Visão Geral

| Etapa | Descrição |
|---|---|
| Processamento de dados | Limpeza, encoding e normalização dos CSVs brutos |
| Treinamento | Comparação de modelos com GridSearchCV + validação cruzada |
| Rastreamento | MLflow para log de parâmetros, métricas e artefatos |
| Serviço | FastAPI servindo o modelo e uma interface HTML/Alpine.js |

---

## Estrutura do Projeto

```
tech_challenge_fase5/
├── app/                    # Aplicação FastAPI
│   ├── routers/
│   │   ├── api/v1/         # Endpoints REST (/api/v1/...)
│   │   └── pages/          # Rotas de páginas HTML
│   ├── schemas/ml.py       # Schema Pydantic de entrada do modelo
│   ├── services/ml_service.py  # Lógica de predição
│   └── templates/          # Templates Jinja2 (Tailwind + Alpine.js)
├── config/config.json      # Configurações da aplicação
├── data/                   # Dados brutos (CSV) e processados
├── docs/                   # Documentação do pipeline
├── ml_models/              # Modelo, scaler e feature names salvos
├── mlruns/                 # Experimentos MLflow
├── notebooks/
│   ├── 1_data_processing.ipynb
│   └── 2_model_train.ipynb
├── src/fiap/               # Utilitários internos (logger, path, etc.)
├── tests/                  # Testes unitários (pytest)
├── main.py                 # Entry point da aplicação
└── pyproject.toml          # Dependências e configuração Poetry
```

---

## Pré-requisitos

- **Python 3.11** (versão exata exigida pelo projeto)
- **Poetry** — gerenciador de dependências e ambientes virtuais

Instale o Poetry caso não tenha:

```bash
pip install poetry
```

---

## Instalação com Poetry

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd tech_challenge_fase5

# Instala todas as dependências (cria o virtualenv automaticamente)
poetry install

# Ativa o shell do ambiente virtual (opcional)
poetry shell
```

> **Dependências principais:** FastAPI, Uvicorn, MLflow, scikit-learn, pandas, joblib, Pydantic v2, SQLAlchemy, Prometheus FastAPI Instrumentator.

---

## Configuração

Edite `config/config.json` conforme necessário:

```json
{
  "TITLE": "FIAP Tech Challenge - Fase 5",
  "LOG_PATH": "<caminho absoluto para salvar os logs>",
  "DATABASE_URL": null,
  "PORT": 5000
}
```

| Chave | Descrição |
|---|---|
| `TITLE` | Título exibido na interface e no Swagger |
| `LOG_PATH` | Diretório onde os arquivos de log serão gravados |
| `PORT` | Porta HTTP da aplicação (padrão `5000`) |
| `DATABASE_URL` | Conexão com banco de dados (opcional, `null` desabilita) |

---

## Executando a Aplicação

```bash
poetry run python main.py
```

A aplicação sobe em `http://localhost:5000` e, se configurado, abre o navegador automaticamente.

| URL | Descrição |
|---|---|
| `http://localhost:5000/` | Interface web de predição |
| `http://localhost:5000/docs` | Swagger UI interativo |
| `http://localhost:5000/logs` | Visualizador de logs da aplicação |
| `http://localhost:5000/metrics` | Métricas Prometheus |

---

## Notebooks

> ⚠️ **Atenção:** Ao abrir um notebook no VS Code, selecione o kernel do Poetry como interpretador Python.  
> No VS Code: clique no seletor de kernel (canto superior direito do notebook) → **Select Another Kernel** → **Python Environments** → escolha o ambiente `.venv` criado pelo Poetry (geralmente em `C:\Users\<user>\AppData\Local\pypoetry\Cache\...` ou dentro da pasta do projeto se `virtualenvs.in-project = true`).

### `notebooks/1_data_processing.ipynb` — Processamento de Dados

Responsável por transformar os CSVs brutos em um dataset limpo e pronto para modelagem.

**Etapas principais:**

1. **Carregamento** dos dados `PEDE2024.csv` com padronização de colunas.
2. **Exploração inicial** — shape, tipos, nulos e estatísticas descritivas.
3. **Limpeza** — remoção de identificadores, datas, nomes e colunas de status.
4. **Filtragem de nulos** — descarte de colunas com > 30% de valores ausentes.
5. **Encoding** — fase → numérico; gênero → variáveis binárias; instituição de ensino → one-hot manual com mapeamento salvo em `docs/map_instituicao_ensino.json`.
6. **Remoção de leakage** — colunas `pedra_2024` e `inde_2024` removidas por serem derivadas do alvo.
7. **Imputação** — valores nulos em indicadores numéricos preenchidos com a média da coluna.
8. **Salvamento** do dataset final em `data/processed_data.csv`.

📄 Documentação detalhada: `docs/data_processing.md`

---

### `notebooks/2_model_train.ipynb` — Treinamento do Modelo

Treina, avalia e seleciona o melhor modelo de regressão para prever `defasagem`.

**Etapas principais:**

1. **Preparação** — carrega `processed_data.csv`, separa `X` / `y (defasagem)` e normaliza com `MinMaxScaler` (salvo em `ml_models/scaler.joblib`).
2. **Split** — 80% treino / 20% teste com `random_state` fixo.
3. **Modelos avaliados:**
   - Regressão Linear
   - Árvore de Decisão
   - **Random Forest** ✅ *(melhor desempenho)*
   - HistGradientBoosting
4. **GridSearchCV** com validação cruzada 5-fold (métrica MAE) para busca de hiperparâmetros.
5. **Métricas** reportadas: MAE, RMSE, R² e CV_MAE.
6. **Seleção automática** do melhor modelo pelo maior R² e salvamento em `ml_models/best_model.joblib`.
7. **Rastreamento MLflow** — parâmetros, métricas e artefatos logados por experimento.
8. **Validação final** com exemplos extremos de defasagem (-2 e +2) para checagem de coerência.

📄 Documentação detalhada: `docs/model_training.md`

---

## MLflow — Rastreamento de Experimentos

O projeto usa **MLflow** para registrar cada execução de treinamento de forma auditável.

```bash
# Iniciar a UI do MLflow (na raiz do projeto)
poetry run mlflow ui

# Acesse em: http://localhost:5001
```

Cada run registra:
- Hiperparâmetros de cada modelo testado
- Métricas de avaliação (MAE, RMSE, R², CV_MAE)
- O artefato do modelo treinado
- Comparativo entre runs para facilitar a escolha do melhor modelo

Os experimentos ficam armazenados localmente em `mlruns/`.

---

## API REST

A API é servida sob o prefixo `/api/v1/` e documentada automaticamente pelo Swagger em `/docs`.

### `GET /api/v1/ml/get_model_info`

Retorna informações sobre os artefatos carregados.

```json
{
  "model_type": "RandomForestRegressor",
  "scaler_type": "MinMaxScaler",
  "feature_names": ["fase", "idade", "iaa", ...],
  "institutions_data": { "pública": 1, "privada": 3, ... }
}
```

### `POST /api/v1/ml/predict`

Realiza uma predição de defasagem escolar.

**Body (JSON):**

```json
{
  "fase": 7,
  "idade": 16,
  "iaa": 8.5,
  "ieg": 9.0,
  "ips": 8.0,
  "ipp": 8.5,
  "ida": 9.0,
  "mat": 8.5,
  "por": 9.0,
  "ipv": 8.0,
  "ian": 9.0,
  "genero": "f",
  "instituicao_tipo": 1
}
```

**Resposta:**

```json
{ "prediction": 0.8712 }
```

**Validações aplicadas (Pydantic + backend):**

| Campo | Restrição |
|---|---|
| `idade` | `>= 0` |
| `iaa`, `ieg`, `ips`, `ipp`, `ida`, `mat`, `por`, `ipv`, `ian` | `>= 0` e `<= 10` |
| `genero` | `"f"` ou `"m"` |
| `instituicao_tipo` | inteiro entre `1` e `7` |

O serviço internamente monta o DataFrame com as features na **exata ordem** que o modelo foi treinado, aplica o `MinMaxScaler` e retorna a predição do `RandomForestRegressor`.

### `GET /api/v1/application/get_version`

Retorna a versão atual da aplicação.

### `GET /api/v1/application/get_alerts`

Retorna alertas ativos do sistema.

---

## Interface Web

A rota `/` exibe um formulário completo construído com **Tailwind CSS** e **Alpine.js**:

- **Indicadores acadêmicos** (IAA, IEG, IPS, IPP, IDA, MAT, POR, IPV, IAN) com tooltips `?` explicativos e validação `min=0 / max=10` no navegador.
- **Dados pessoais:** gênero e tipo de instituição de ensino (select com os 7 tipos mapeados).
- **Botões de exemplo:** *Exemplo bom* e *Exemplo ruim* preenchem o formulário automaticamente para demonstração rápida.
- **Modal de resultado** com classificação visual por nível:

| Resultado | Nível | Estilo |
|---|---|---|
| `< -1` | Alto Negativo | 🔴 Vermelho |
| `-1` a `-0.5` | Médio Negativo | 🟠 Laranja |
| `-0.5` a `0` | Leve Negativo | 🟡 Âmbar |
| `0` a `0.5` | Leve | 🩵 Teal |
| `0.5` a `1` | Médio | 🟢 Verde |
| `> 1` | Alto | ✅ Esmeralda |

---

## Interpretando o Resultado

O modelo prevê um valor contínuo de **defasagem escolar**:

- **Valores positivos** indicam que o aluno está à frente do esperado para seu nível.
- **Valores negativos** indicam defasagem — quanto mais negativo, maior a necessidade de atenção.
- **Faixa de referência:** os intervalos de 0,5 foram definidos com base na distribuição do target no conjunto de treinamento.

---

## Testes

```bash
# Rodar todos os testes
poetry run pytest

# Com saída detalhada
poetry run pytest -v
```

Os testes cobrem: processamento de dados, transformação de arquivos, logger manager e treinamento do modelo.

---

*Projeto acadêmico FIAP — Engenharia de Machine Learning • Python 3.11 • FastAPI • scikit-learn • MLflow*