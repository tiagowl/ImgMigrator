# Decisões Arquiteturais (ADRs) - Sistema de Migração iCloud para Google Drive

## ADR-001: Uso de FastAPI como Framework Web

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

Precisávamos escolher um framework web Python para o backend da aplicação. As opções principais eram Flask, Django e FastAPI.

### Decisão

Escolhemos **FastAPI** como framework principal.

### Justificativa

1. **Performance:** FastAPI é baseado em Starlette e Pydantic, oferecendo performance superior ao Flask/Django
2. **Async Nativo:** Suporte completo a async/await, essencial para operações I/O intensivas (APIs externas)
3. **Validação Automática:** Pydantic integrado para validação de dados e serialização
4. **Documentação Automática:** Gera OpenAPI/Swagger automaticamente
5. **Type Hints:** Suporte completo a type hints, melhorando DX e manutenibilidade
6. **Curva de Aprendizado:** Similar ao Flask, fácil para a equipe

### Consequências

**Positivas:**
- Melhor performance em operações assíncronas
- Menos código boilerplate
- Documentação sempre atualizada
- Melhor suporte a type checking

**Negativas:**
- Ecossistema menor que Django
- Menos recursos "batteries included" que Django
- Alguns pacotes podem não ter suporte async completo

### Alternativas Consideradas

- **Flask:** Mais maduro, mas síncrono e menos performático
- **Django:** Muito completo, mas pesado e menos adequado para APIs
- **Tornado:** Bom para async, mas menos popular e documentação limitada

---

## ADR-002: SQLite como Banco de Dados Inicial

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

Precisávamos escolher um banco de dados para armazenar usuários, credenciais e histórico de migrações. Considerações: MVP, simplicidade de deploy, custos.

### Decisão

Usar **SQLite** como banco de dados inicial, com plano de migração para PostgreSQL quando necessário.

### Justificativa

1. **Simplicidade:** Não requer servidor separado, facilita deploy
2. **Adequado para MVP:** Volume inicial esperado é baixo (< 1000 usuários)
3. **Zero Configuração:** Funciona out-of-the-box
4. **Custos:** Sem custos de infraestrutura adicional
5. **WAL Mode:** Suporta concorrência razoável
6. **Migração Futura:** SQLAlchemy facilita migração para PostgreSQL

### Consequências

**Positivas:**
- Deploy mais simples
- Sem necessidade de gerenciar servidor de banco
- Ideal para desenvolvimento e testes
- Baixo overhead

**Negativas:**
- Limitações de concorrência (máximo ~100 conexões simultâneas)
- Não suporta múltiplos servidores de aplicação facilmente
- Sem recursos avançados (replicação, sharding)
- Limite de tamanho de banco (~140TB, mas performance degrada antes)

### Plano de Migração

Quando atingir:
- > 1000 usuários ativos
- > 10 migrações simultâneas
- Necessidade de alta disponibilidade

Migrar para PostgreSQL mantendo compatibilidade com SQLAlchemy.

### Alternativas Consideradas

- **PostgreSQL:** Mais robusto, mas requer servidor dedicado
- **MySQL:** Similar ao PostgreSQL, mas menos features
- **MongoDB:** Não relacional, não adequado para este caso

---

## ADR-003: Processamento Assíncrono com Celery

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

Migrações de fotos são operações longas (minutos a horas). Não podemos bloquear a API durante o processamento.

### Decisão

Usar **Celery** com **Redis** para processamento assíncrono de migrações.

### Justificativa

1. **Não Bloqueante:** API responde imediatamente, migração roda em background
2. **Escalável:** Múltiplos workers podem processar migrações em paralelo
3. **Confiável:** Retry automático, persistência de tarefas
4. **Monitoramento:** Flower para monitorar workers e tarefas
5. **Maturidade:** Solução comprovada e amplamente usada
6. **Integração:** Fácil integração com FastAPI

### Consequências

**Positivas:**
- API responsiva
- Pode escalar workers independentemente
- Retry automático em falhas
- Monitoramento integrado

**Negativas:**
- Complexidade adicional (Redis + Celery)
- Mais componentes para gerenciar
- Debugging mais complexo (tarefas assíncronas)

### Alternativas Consideradas

- **RQ (Redis Queue):** Mais simples, mas menos features
- **Threading nativo:** Mais simples, mas menos controle e escalabilidade
- **asyncio tasks:** Não persiste entre reinicializações

---

## ADR-004: Criptografia AES-256-GCM para Credenciais

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura, Security

### Contexto

Precisamos armazenar credenciais do iCloud (Apple ID e senha) de forma segura. Essas são informações sensíveis que devem ser protegidas mesmo se o banco for comprometido.

### Decisão

Usar **AES-256-GCM** para criptografar credenciais antes de armazenar no banco.

### Justificativa

1. **Segurança:** AES-256 é considerado seguro para dados sensíveis
2. **GCM Mode:** Fornece autenticação além de criptografia (detecta modificações)
3. **Padrão da Indústria:** Amplamente usado e auditado
4. **Performance:** Eficiente em software
5. **Biblioteca Confiável:** `cryptography` é bem mantida e auditada

### Implementação

- Chave mestra armazenada em variável de ambiente
- Salt único por credencial (32 bytes)
- IV gerado aleatoriamente para cada criptografia
- Key derivation com PBKDF2 (100.000 iterações)

### Consequências

**Positivas:**
- Credenciais protegidas mesmo com acesso ao banco
- Conformidade com boas práticas de segurança
- Detecta tentativas de modificação

**Negativas:**
- Overhead de processamento (mínimo)
- Se chave mestra for perdida, credenciais não podem ser recuperadas
- Necessidade de gerenciar chave mestra com segurança

### Alternativas Consideradas

- **AES-256-CBC:** Menos seguro (sem autenticação)
- **ChaCha20-Poly1305:** Alternativa moderna, mas menos suporte
- **Sem criptografia:** Inaceitável para dados sensíveis

---

## ADR-005: WebSocket para Atualização de Progresso

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

Usuários precisam ver progresso de migração em tempo real. Polling HTTP é ineficiente e pode causar delay.

### Decisão

Usar **WebSocket** (via Socket.io) para atualização de progresso em tempo real, com fallback para polling HTTP.

### Justificativa

1. **Tempo Real:** Atualizações instantâneas sem polling
2. **Eficiência:** Menos overhead que polling HTTP
3. **Bidirecional:** Permite comunicação em ambas direções
4. **Fallback:** Socket.io tem fallback automático para polling
5. **Suporte:** Bem suportado em browsers modernos

### Implementação

- Socket.io no backend (python-socketio)
- Socket.io-client no frontend
- Eventos: `migration_progress`, `migration_complete`, `migration_error`
- Fallback: Endpoint HTTP `/api/migrations/{id}/progress` para polling

### Consequências

**Positivas:**
- Experiência de usuário melhor (atualizações instantâneas)
- Menos carga no servidor (vs polling frequente)
- Mais eficiente em termos de rede

**Negativas:**
- Complexidade adicional (gerenciar conexões WebSocket)
- Pode requerer mais recursos (muitas conexões simultâneas)
- Debugging mais complexo

### Alternativas Consideradas

- **Polling HTTP:** Mais simples, mas menos eficiente
- **Server-Sent Events (SSE):** Unidirecional, não atende todos os casos
- **Long Polling:** Complexo e ineficiente

---

## ADR-006: React como Framework Frontend

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura, Frontend

### Contexto

Precisávamos escolher um framework frontend moderno para a interface web. Opções: React, Vue.js, Angular, ou vanilla JS.

### Decisão

Usar **React** com **TypeScript** como framework frontend.

### Justificativa

1. **Ecossistema:** Maior ecossistema de bibliotecas
2. **Familiaridade:** Equipe já tem experiência com React
3. **Comunidade:** Grande comunidade e suporte
4. **TypeScript:** Type safety melhora qualidade do código
5. **Flexibilidade:** Não impõe muitas decisões arquiteturais
6. **Performance:** Virtual DOM eficiente

### Consequências

**Positivas:**
- Desenvolvimento mais rápido (equipe familiarizada)
- Grande quantidade de componentes e bibliotecas disponíveis
- Boa performance
- Type safety com TypeScript

**Negativas:**
- Curva de aprendizado para novos membros
- Pode ser "overkill" para aplicações simples
- Bundle size maior que alternativas

### Alternativas Consideradas

- **Vue.js:** Mais simples, mas ecossistema menor
- **Angular:** Muito completo, mas mais pesado e complexo
- **Vanilla JS:** Muito trabalho manual, menos produtivo

---

## ADR-007: Docker para Containerização

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura, DevOps

### Contexto

Precisamos de uma forma consistente de empacotar e deployar a aplicação em diferentes ambientes.

### Decisão

Usar **Docker** e **Docker Compose** para containerização e orquestração local.

### Justificativa

1. **Consistência:** Mesmo ambiente em dev, staging e produção
2. **Isolamento:** Dependências isoladas, sem conflitos
3. **Portabilidade:** Funciona em qualquer sistema com Docker
4. **Simplicidade:** Docker Compose facilita orquestração de múltiplos serviços
5. **Padrão da Indústria:** Amplamente adotado
6. **CI/CD:** Facilita integração com pipelines

### Consequências

**Positivas:**
- Deploy mais simples e consistente
- Facilita onboarding de novos desenvolvedores
- Isolamento de dependências
- Preparado para Kubernetes (futuro)

**Negativas:**
- Overhead de recursos (mínimo)
- Curva de aprendizado inicial
- Requer Docker instalado

### Alternativas Consideradas

- **Virtualenv + requirements.txt:** Mais simples, mas menos isolamento
- **Vagrant:** Mais pesado, menos usado atualmente
- **Kubernetes direto:** Muito complexo para MVP

---

## ADR-008: Estrutura de Código em Camadas

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

Precisávamos definir uma estrutura de código que facilite manutenção, testes e escalabilidade.

### Decisão

Adotar arquitetura em camadas: **Routes → Controllers → Services → Repositories → Database**.

### Justificativa

1. **Separação de Responsabilidades:** Cada camada tem responsabilidade clara
2. **Testabilidade:** Fácil mockar dependências para testes
3. **Manutenibilidade:** Mudanças isoladas em uma camada
4. **Reusabilidade:** Services podem ser reutilizados
5. **Padrão Conhecido:** Arquitetura familiar para desenvolvedores

### Estrutura

```
Routes (API endpoints)
  ↓
Controllers (Request/Response handling)
  ↓
Services (Business logic)
  ↓
Repositories (Data access)
  ↓
Database
```

### Consequências

**Positivas:**
- Código organizado e fácil de navegar
- Testes unitários mais simples
- Mudanças isoladas
- Facilita onboarding

**Negativas:**
- Mais arquivos e estrutura
- Pode ser "over-engineering" para features simples
- Requer disciplina para manter separação

### Alternativas Consideradas

- **MVC simples:** Menos camadas, mas menos organização
- **Domain-Driven Design:** Muito complexo para este projeto
- **Monolítico sem camadas:** Mais rápido, mas difícil de manter

---

## ADR-009: Retry Automático com Backoff Exponencial

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

APIs externas (iCloud, Google Drive) podem falhar temporariamente. Precisamos de estratégia de retry robusta.

### Decisão

Implementar retry automático com **backoff exponencial** para todas as chamadas a APIs externas.

### Justificativa

1. **Resiliência:** Lida com falhas temporárias automaticamente
2. **Backoff Exponencial:** Evita sobrecarregar APIs já sobrecarregadas
3. **Padrão da Indústria:** Estratégia comprovada
4. **Melhor UX:** Usuário não precisa reiniciar manualmente

### Implementação

- Máximo 3 tentativas
- Backoff: 1s, 2s, 4s
- Apenas para erros temporários (5xx, timeouts, rate limits)
- Não retry para erros permanentes (4xx, exceto 429)

### Consequências

**Positivas:**
- Maior taxa de sucesso em migrações
- Menos intervenção manual
- Melhor experiência do usuário

**Negativas:**
- Pode aumentar tempo total de migração
- Pode mascarar problemas reais se não configurado corretamente

### Alternativas Consideradas

- **Retry linear:** Mais simples, mas menos eficiente
- **Sem retry:** Usuário precisa reiniciar manualmente
- **Retry infinito:** Pode travar indefinidamente

---

## ADR-010: Checkpointing para Recuperação de Migrações

**Status:** Aceito  
**Data:** 2023-12-15  
**Decisores:** Equipe de Arquitetura

### Contexto

Migrações podem falhar no meio do processo. Não queremos que usuário perca todo o progresso.

### Decisão

Implementar **checkpointing**: salvar progresso a cada 10 fotos processadas, permitindo retomar de onde parou.

### Justificativa

1. **Resiliência:** Migrações podem ser retomadas após falhas
2. **Melhor UX:** Usuário não perde progresso
3. **Eficiência:** Não reprocessa fotos já migradas
4. **Confiabilidade:** Sistema mais robusto

### Implementação

- Tabela `migration_logs` armazena status de cada foto
- Status: pending, downloading, uploading, completed, failed
- Ao retomar: pula fotos com status "completed"
- Checkpoint a cada 10 fotos ou a cada 30 segundos

### Consequências

**Positivas:**
- Migrações podem ser retomadas
- Melhor experiência do usuário
- Mais confiável

**Negativas:**
- Overhead de escrita no banco
- Lógica adicional para verificar checkpoints
- Pode processar algumas fotos duplicadas se falhar entre checkpoints

### Alternativas Consideradas

- **Sem checkpointing:** Mais simples, mas perde progresso em falhas
- **Checkpoint por foto:** Mais overhead, mas mais granular
- **Checkpoint apenas no final:** Não ajuda em falhas intermediárias

---

**Documento gerado em:** [Data atual]  
**Versão:** 1.0  
**Status:** Decisões arquiteturais documentadas



