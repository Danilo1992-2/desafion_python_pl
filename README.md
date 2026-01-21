# 🏥 Healthtech API — Resumo de Consultas Médicas (Rule-based + LLM)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-⚡-green.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)
![AI](https://img.shields.io/badge/AI-LLM%20Optional-purple.svg)
![Status](https://img.shields.io/badge/status-challenge%20ready-success.svg)

API backend em Python que recebe dados estruturados de consultas médicas fictícias e gera um **resumo clínico estruturado**, utilizando **regras determinísticas (obrigatórias)** e **LLM (opcional)** com fallback automático.

> 🎯 Foco: engenharia de software para sistemas com IA — previsibilidade, validação, arquitetura limpa e uso responsável de LLMs.

---

## 📑 Sumário

- [📌 Contexto](#-contexto)
- [🎯 Objetivo técnico](#-objetivo-técnico)
- [🧩 Funcionalidades](#-funcionalidades)
- [🧠 Estratégias de resumo](#-estratégias-de-resumo)
- [🏗️ Arquitetura do projeto](#️-arquitetura-do-projeto)
- [🔐 Princípios adotados](#-princípios-adotados)
- [📡 Exemplo de uso da API](#-exemplo-de-uso-da-api)
- [🐳 Como rodar o projeto](#-como-rodar-o-projeto-docker--recomendado)

---

## 📌 Contexto

Este projeto simula o backend de uma healthtech que recebe dados estruturados de consultas médicas fictícias e gera um resumo clínico estruturado para apoio a profissionais de saúde.

O foco principal **não é “fazer um prompt bonito”**, mas sim demonstrar **engenharia de software aplicada a sistemas com IA**, priorizando:

- Estruturação e validação de dados clínicos  
- Previsibilidade e auditabilidade  
- Separação de responsabilidades  
- Uso responsável de LLMs  
- Fallback determinístico obrigatório  

O sistema funciona **100% sem IA**. O uso de LLM é apenas um **diferencial arquitetural**.

---

## 🎯 Objetivo técnico

Avaliar a capacidade de:

- Projetar APIs backend em Python (FastAPI)  
- Modelar e validar dados com Pydantic  
- Organizar um projeto de forma modular  
- Implementar regras determinísticas (rule-based)  
- Integrar LLMs de forma encapsulada  
- Implementar fallback seguro  
- Explicar decisões técnicas e trade-offs  

---

## 🧩 Funcionalidades

### Endpoint principal (core do desafio)

`POST /consultations`

Recebe dados estruturados de uma consulta médica e retorna:

- Identificação da consulta  
- Nome do paciente  
- Nome do médico  
- Resumo clínico  
- Estratégia utilizada (`llm_based` ou `rule_based`)  

---

## 🧠 Estratégias de resumo

### ✅ 1. Rule-based (obrigatória)

Implementada em:

app/services/rule_based.py


**Características:**

- Totalmente determinística  
- Não usa IA  
- Não infere diagnósticos  
- Não sugere tratamentos  
- Apenas organiza e resume os dados fornecidos  
- Garante previsibilidade e auditabilidade  

👉 Base funcional obrigatória do sistema.

---

### ⭐ 2. LLM-based (diferencial)

Implementada em:

app/services/llm_based.py


**Características:**

- Usa Ollama local com modelo Mistral  
- Totalmente encapsulada em client dedicado  
- Prompt restritivo:
  - Não inventar fatos  
  - Não inferir diagnósticos  
  - Não prescrever tratamentos  
  - Usar apenas dados fornecidos  

**Fluxo:**

API → tenta IA → se falhar → fallback rule-based


**Fallback ocorre em caso de:**

- Timeout  
- Erro de rede  
- LLM indisponível  
- Resposta vazia  

👉 O sistema **nunca depende da IA para funcionar**.

---

## 🏗️ Arquitetura do projeto

app/
├── api/             # Camada de API (rotas FastAPI)
│   ├── models/      # Camada de persistência (SQLAlchemy ORM)
│   ├── schemas/     # Camada de contrato (Pydantic)
│   ├── services/    # Camada de regras de negócio (rule-based e LLM)
│   ├── db/          # Conexão, inicialização e seeds do banco
│   └── main.py      # Ponto de entrada da aplicação


**Responsabilidades:**

- `api` → orquestra fluxo HTTP  
- `schemas` → valida dados  
- `models` → persistência  
- `services` → regras de negócio  
- `db` → infraestrutura  

---

## 🔐 Princípios adotados

- LLM não é fonte de verdade  
- LLM não gera diagnósticos  
- LLM não toma decisões clínicas  
- Dados sempre estruturados e validados antes de qualquer IA  
- Fallback determinístico obrigatório  
- IA usada apenas como camada auxiliar de linguagem  

---

## 📡 Exemplo de uso da API

### 🔹 Request

```http
POST /consultations
Content-Type: application/json
    {
    "patient_id": 1,
    "doctor_id": 1,
    "care_unit_id": 1,
    "symptoms": "dor de cabeça, fadiga",
    "patient_notes": "paciente informa dor no peito",
    "medical_notes": "",
    "appointment_datetime": "2026-01-20T21:37:32.570Z"
    }

    🔹 Response (exemplo)
    llm:
        {
            "consultation_id": 12,
            "patient_name": "Carlos Silva",
            "doctor_name": "Dra. Ana Lima",
            "summary": "1. The patient presents with symptoms of a headache and fatigue.\n2. Additionally, the patient reports chest pain.\n3. No further medical observations are provided in the information given.\n4. A comprehensive evaluation is necessary to determine potential causes for these symptoms and the chest pain.\n5. Further diagnostic tests may be required to confirm any underlying conditions or diseases.",
            "strategy": "llm_based",
            "created_at": "2026-01-20T23:10:34.889004"
        }
    rule:
       {
            "consultation_id": 13,
            "patient_name": "Carlos Silva",
            "doctor_name": "Dra. Ana Lima",
            "summary": "Consulta agendada em 2026-01-20 21:37. Sintomas relatados: dor de cabeça, fadiga. Relato do paciente: paciente informa dor no peito.",
            "strategy": "rule_based",
            "created_at": "2026-01-20T23:12:17.575785"
        }
```

### 🐳 Como rodar o projeto (Docker — recomendado)
Pré-requisitos
    Docker
    Docker Compose

Subir o ambiente
    docker compose up -d --build

Acessos
    API: http://localhost:8000
    Docs (Swagger): http://localhost:8000/docs

