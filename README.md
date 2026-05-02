# Pull, Otimização e Avaliação de Prompts

## Objetivo

Este projeto otimiza prompts de baixa qualidade publicados no LangSmith Prompt Hub para converter relatos de bugs em user stories e avaliá-los com métricas automáticas.

## Funcionalidades

- Faz pull do prompt inicial do LangSmith
- Mantém um prompt otimizado em `prompts/bug_to_user_story_v2.yml`
- Faz push do prompt otimizado para o LangSmith Hub
- Avalia o prompt com métricas de `Helpfulness`, `Correctness`, `F1-Score`, `Clarity` e `Precision`
- Usa um script alternativo com controle de taxa para executar avaliações com Gemini free

## Estrutura Principal

```text
mba-ia-pull-evaluation-prompt/
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── datasets/
│   └── bug_to_user_story.jsonl
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   ├── evaluate.py
│   ├── metrics.py
│   └── utils.py
├── run_with_rate_limit.py
└── README.md
```

## Tecnologias

- Python 3.9+
- LangChain
- LangSmith
- YAML
- OpenAI ou Google Gemini

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração

Configure as variáveis do `.env` com base no `.env.example`.

Exemplo mínimo:

```env
LANGSMITH_API_KEY=...
USERNAME_LANGSMITH_HUB=...
LLM_PROVIDER=google
GOOGLE_API_KEY=...
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

Para OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=...
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o
```

## Prompt Otimizado

O arquivo `prompts/bug_to_user_story_v2.yml` contém a versão otimizada do prompt. A abordagem usada prioriza:

- persona bem definida
- estrutura BDD consistente
- raciocínio interno guiado
- cobertura factual do bug
- critérios testáveis e objetivos

## Técnicas Utilizadas no Prompt

As principais estratégias aplicadas em `prompts/bug_to_user_story_v2.yml` são:

- **Role Prompting**: define uma persona especializada para orientar o tom da resposta e manter foco em valor de negócio, clareza e testabilidade.
- **Por que foi usada**: para evitar respostas genéricas e fazer o modelo escrever como alguém com visão de produto, arquitetura e qualidade.
- **Chain of Thought silencioso**: orienta o modelo a organizar o raciocínio internamente antes de responder, ajudando a reduzir omissões importantes sem poluir a saída final.
- **Por que foi usada**: para melhorar a análise do bug antes da escrita, identificar fatos obrigatórios e preservar detalhes importantes sem perder objetividade na resposta final.
- **Tree of Thought silencioso**: faz o modelo considerar diferentes perspectivas do problema, como valor para o usuário, critérios testáveis e riscos técnicos, melhorando a cobertura do bug.
- **Por que foi usada**: para aumentar a cobertura em bugs com mais de um problema e evitar que o modelo foque apenas no primeiro ponto identificado.
- **Skeleton of Thought**: estrutura internamente a resposta antes da escrita, definindo um esqueleto curto ou expandido conforme a complexidade do bug.
- **Por que foi usada**: para manter um padrão estável de saída e reduzir respostas incompletas, desorganizadas ou curtas demais em casos complexos.
- **ReAct silencioso**: reforça um fluxo interno de analisar, decidir, revisar e então responder, ajudando o modelo a escolher a estrutura mais adequada e revisar a cobertura factual antes de responder.
- **Por que foi usada**: para melhorar a tomada de decisão do modelo sobre formato, prioridade e revisão final do conteúdo.

Em conjunto, essas técnicas ajudam o prompt a transformar bugs em histórias de usuário mais claras, completas e alinhadas ao padrão de avaliação do projeto.

## Fluxo de Uso

### 1. Fazer pull do prompt inicial

```bash
python src/pull_prompts.py
```

### 2. Editar o prompt otimizado

Edite:

```text
prompts/bug_to_user_story_v2.yml
```

### 3. Fazer push do prompt para o LangSmith

```bash
python src/push_prompts.py
```

### 4. Executar a avaliação

Para ambientes sem restrição forte de taxa:

```bash
python src/evaluate.py
```

Para uso com Gemini free e controle de taxa:

```bash
python run_with_rate_limit.py
```

## Avaliação com `run_with_rate_limit.py`

O arquivo `run_with_rate_limit.py` foi criado como alternativa ao `src/evaluate.py`.

- Ele foi derivado do `src/evaluate.py`
- Foi usado para coletar as avaliações do projeto
- A coleta de métricas e scores apresentados durante a otimização foi feita por ele
- O motivo foi a necessidade de contornar limites de taxa do provider sem modificar o `src/evaluate.py`, que deve permanecer preservado para fins da avaliação

Em termos práticos, o script:

- lê o dataset linha a linha
- aplica pausas entre chamadas ao modelo
- faz retry em erros de cota (`429` e `RESOURCE_EXHAUSTED`)
- evita interrupções frequentes em execuções com Gemini no plano free

## Critério de Aprovação

O projeto é aprovado quando todas as métricas ficam em pelo menos `0.9`:

- Helpfulness
- Correctness
- F1-Score
- Clarity
- Precision

## Observações

- O prompt avaliado é sempre puxado do LangSmith Hub, não do arquivo local diretamente
- Depois de editar `prompts/bug_to_user_story_v2.yml`, é obrigatório executar o push novamente
- O dataset de avaliação não deve ser alterado

## Comandos Úteis

```bash
python src/pull_prompts.py
python src/push_prompts.py
python src/evaluate.py
python run_with_rate_limit.py
pytest tests/test_prompts.py
```
