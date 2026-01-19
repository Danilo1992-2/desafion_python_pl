# 🧪 Desafio Técnico — Desenvolvedor(a) Python Pleno (Healthtech & IA)

## 📌 Contexto

Você está trabalhando em uma **healthtech** que utiliza **LLMs integrados a pipelines backend** para apoiar profissionais de saúde.

Antes de qualquer uso de IA, o sistema precisa **estruturar, validar e controlar dados clínicos**, garantindo previsibilidade, auditoria e segurança.

Este desafio simula esse cenário com **dados fictícios**.

---

## 🎯 Objetivo

Avaliar sua capacidade de:

- Projetar APIs backend em Python
- Modelar e validar dados
- Tomar decisões arquiteturais
- Integrar LLMs de forma **controlada**
- Explicar trade-offs técnicos

---

## 🧩 Desafio

Implemente uma **API em Python (FastAPI)** que receba dados de uma consulta médica fictícia e gere um resumo clínico estruturado.

A API deve oferecer **duas estratégias de resumo**:

1. **Rule-based (obrigatória)**
2. **LLM-based (opcional, diferencial)**

---

## 🌐 Endpoint esperado

```
POST /consultations
```

---

## ✅ Requisitos obrigatórios

- Validação de dados com **Pydantic**
- Organização do projeto em módulos
- Estratégia `rule_based` totalmente funcional
- Tratamento de erros consistente
- README explicando decisões técnicas

### Resumo rule-based

O resumo determinístico deve ser gerado **sem uso de IA**, apenas com regras claras.

---

## ⭐ Diferencial: uso de LLM com libs (opcional)

Se optar por implementar o modo `llm_based`:

- Utilize bibliotecas para o consumo de LLMs
- O LLM deve ser **encapsulado**
- Deve existir fallback para `rule_based`
- Não é permitido inferir diagnósticos
---

## 🧪 Avaliação

Será avaliado:

- Clareza arquitetural
- Separação de responsabilidades
- Uso consciente (ou não uso) de LLMs
- Capacidade de explicar decisões
- Qualidade geral do código

> Não avaliamos “prompt bonito”.  
> Avaliamos **engenharia de sistemas com IA**.

---

## 📦 Entrega

- Repositório GitHub
- Código + README
- Instruções para rodar localmente

---

## 📝 Observações finais

- Use apenas dados fictícios
- Priorize clareza e responsabilidade
- O desafio deve funcionar perfeitamente **sem IA**
