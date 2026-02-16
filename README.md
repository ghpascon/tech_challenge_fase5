# Tech Challenge Fase 5 - Previsão de Defasagem Escolar

Este projeto tem como objetivo prever a defasagem escolar de alunos utilizando dados educacionais anonimizados. O pipeline inclui:

- Processamento e limpeza de dados (notebook 1_data_processing.ipynb)
- Engenharia de variáveis e normalização
- Treinamento, validação e comparação de modelos de regressão (notebook 2_model_train.ipynb)
- Busca de hiperparâmetros com GridSearchCV
- Validação cruzada (cross-validation)
- Rastreamento de experimentos com MLflow
- Salvamento de modelos e scaler para uso futuro

## Estrutura
- `data/` — Dados brutos e processados
- `notebooks/` — Jupyter Notebooks do projeto
- `src/` — Utilitários e módulos auxiliares
- `docs/` — Documentação detalhada do pipeline e modelagem
- `ml_models/` — Modelos e scaler salvos
- `logs/` — Logs de execução

## Como executar
1. Instale as dependências (requirements.txt)
2. Execute os notebooks na ordem:
   - 1_data_processing.ipynb
   - 2_model_train.ipynb
3. Os resultados e modelos serão salvos nas pastas apropriadas.

## Documentação
- Veja a pasta `docs/` para detalhes sobre o processamento de dados e treinamento dos modelos.

---

Projeto acadêmico FIAP - Engenharia de Machine Learning