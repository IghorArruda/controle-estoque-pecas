# Controle de Estoque de Pecas de Manutencao

Aplicacao web responsiva desenvolvida com Python + Streamlit + SQLite para controle de estoque pessoal de pecas de manutencao de maquinas de cafe comerciais. Rodavel diretamente no celular via navegador, com deploy gratuito na nuvem.

**Status:** Em desenvolvimento | **Deploy:** Streamlit Cloud (em breve)

---

## Problema Resolvido

Como tecnico de manutencao de maquinas de cafe, gerencio um estoque pessoal de pecas no veiculo corporativo. O controle era feito mentalmente ou em anotacoes dispersas, gerando:

- Ruptura de pecas criticas em campo
- Tempo perdido procurando pecas no carro
- Falta de previsao de reposicao

**Resultado:** App que elimina rupturas, otimiza reposicao e gera insights de consumo.

---

## Stack Tecnologica

| Tecnologia | Uso |
|-----------|-----|
| Python | Logica de negocio e manipulacao de dados |
| Streamlit | Interface web responsiva (mobile-first) |
| SQLite | Banco de dados relacional local (zero config) |
| Pandas | Processamento e analise de dados |
| Plotly | Dashboards interativos para portfolio |

---

## Funcionalidades

### Operacoes CRUD
- **Inserir produto** â€” nome, modelo da maquina, quantidade inicial, quantidade minima (alerta)
- **Excluir produto** â€” remocao completa do catalogo
- **Entrada de pecas** â€” adiciona N unidades ao estoque (ex: retirada do almoxarifado)
- **Saida rapida** â€” botao "-1" para uso imediato em campo (1 toque)
- **Consulta** â€” busca por nome do produto ou modelo da maquina

### Alertas Inteligentes
- Alerta visual quando quantidade <= minimo definido
- Minimos personalizados por produto (ex: placas = 2, o-rings = 50)

### Historico
- Registro de todas as movimentacoes (entrada/saida)
- Filtro por periodo (mensal) para consulta rapida
- Armazenamento otimizado (nao acumula dados antigos indefinidamente)

### Dashboard (Portfolio)
- Pecas mais consumidas por periodo
- Status do estoque (critico / ok)
- Previsao de reposicao baseada em historico de consumo

---

## Modelagem de Dados

### Tabela: produtos

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | INTEGER PK | Identificador unico |
| nome | TEXT | Nome da peca (ex: Placa CPU) |
| modelo_maquina | TEXT | Modelo que utiliza (ex: Maquina A, Maquina B) |
| quantidade | INTEGER | Estoque atual |
| quantidade_minima | INTEGER | Limite para alerta |
| categoria | TEXT | Tipo de peca |

### Tabela: movimentacoes

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | INTEGER PK | Identificador unico |
| produto_id | INTEGER FK | Referencia ao produto |
| tipo | TEXT | entrada ou saida |
| quantidade | INTEGER | Quantidade movimentada |
| data_hora | TIMESTAMP | Momento da operacao |

---

## Como Usar

### Localmente

```bash
git clone https://github.com/IghorArruda/controle-estoque-pecas.git
cd controle-estoque-pecas
pip install -r requirements.txt
streamlit run app.py
```

Acesse no navegador: http://localhost:8501

### Deploy na Nuvem

- Deploy automatico via Streamlit Cloud (gratuito)
- Link de acesso e QR code para instalacao como app no celular (Android/iOS)

---

## Dataset de Demonstracao

Dados ficticios para portfolio e testes, baseados em pecas reais de manutencao de maquinas de cafe:

| Nome | Modelo da Maquina | Quantidade | Minimo |
|------|-------------------|------------|--------|
| Placa CPU | Maquina A | 2 | 2 |
| Placa Fonte | Maquina A | 2 | 2 |
| Eletrovalvula | Maquina B | 3 | 2 |
| Mangueira | Maquina A | 5 | 3 |
| O-Ring | Maquina B | 50 | 30 |
| Guarnicao | Maquina C | 10 | 5 |
| Motor Produto | Maquina A | 2 | 2 |
| Motor Batedor | Maquina B | 2 | 2 |

**Nota:** Todos os dados sao ficticios e genericos, sem qualquer informacao sensivel da empresa.

---

## Habilidades Demonstradas

- Modelagem de dados relacional (SQLite, normalizacao)
- CRUD completo com validacao de dados
- Interface responsiva (mobile-first com Streamlit)
- Analise de dados (Pandas, estatistica descritiva)
- Dashboards interativos (Plotly)
- Previsao de demanda com base em historico
- Deploy em nuvem (Streamlit Cloud)
- Versionamento (Git, GitHub)

---

## Licenca

MIT License â€” projeto de portfolio pessoal.

---

**Desenvolvido por:** Ighor Arruda

**LinkedIn:** linkedin.com/in/ighor-arruda

**Portfolio:** ighorarruda.github.io
