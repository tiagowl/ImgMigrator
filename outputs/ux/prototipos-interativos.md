# Protótipos Interativos - Sistema de Migração iCloud para Google Drive

## 1. Especificação de Interações

### 1.1 Estados da Interface

#### Estados de Botões

**Estado Normal:**
- Cor: Azul primário (#0066CC)
- Hover: Azul escuro (#0052A3)
- Cursor: pointer
- Transição: 0.2s ease

**Estado Desabilitado:**
- Cor: Cinza (#CCCCCC)
- Cursor: not-allowed
- Opacidade: 0.6

**Estado Loading:**
- Spinner animado
- Texto: "Processando..."
- Desabilitado durante ação

**Estado Sucesso:**
- Ícone de check verde
- Feedback visual: 2s
- Retorna ao estado normal

**Estado Erro:**
- Ícone de alerta vermelho
- Mensagem de erro abaixo
- Permanece até correção

---

### 1.2 Transições e Animações

#### Barra de Progresso

```css
/* Animação suave da barra de progresso */
.progress-bar {
  transition: width 0.5s ease-in-out;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}
```

**Comportamento:**
- Atualiza a cada 1 segundo
- Animação suave de preenchimento
- Pulso sutil para indicar atividade

#### Cards e Modais

```css
/* Entrada de modais */
.modal-enter {
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Comportamento:**
- Fade in + slide up
- Duração: 300ms
- Backdrop com fade simultâneo

#### Notificações Toast

```css
/* Notificações deslizam da direita */
.toast-enter {
  animation: slideInRight 0.4s ease;
}

.toast-exit {
  animation: slideOutRight 0.3s ease;
}
```

**Comportamento:**
- Entram da direita
- Permanecem 5 segundos
- Saem automaticamente ou ao clicar em X

---

## 2. Protótipo: Dashboard Interativo

### 2.1 Interações Principais

#### Card de Status do Google Drive

**Estado Inicial:**
```
┌─────────────────────────────┐
│ ✅ Google Drive Conectado   │
│ Conta: usuario@gmail.com    │
│ [Desconectar]               │
└─────────────────────────────┘
```

**Hover sobre "Desconectar":**
- Botão muda para vermelho
- Tooltip: "Desconectar sua conta Google Drive"

**Click em "Desconectar":**
1. Modal de confirmação aparece
2. Backdrop escurece
3. Modal com animação fadeInUp
4. Opções: [Cancelar] [Confirmar]

**Click em "Confirmar":**
1. Loading no botão (2s)
2. Card atualiza para estado "Não conectado"
3. Toast de sucesso aparece
4. Botão muda para "Conectar Google Drive"

---

#### Formulário de Credenciais iCloud

**Interações de Campo:**

**Campo Apple ID:**
- Foco: Borda azul, label sobe
- Digitação: Validação em tempo real
- Erro: Borda vermelha + mensagem abaixo
- Sucesso: Borda verde + ícone check

**Campo Senha:**
- Foco: Borda azul, label sobe
- Digitação: Mostra força da senha (barra)
- Toggle visibilidade: Ícone olho alterna
- Erro: Borda vermelha + mensagem

**Botão "Salvar e Validar":**
- Hover: Escurece, escala 1.02
- Click: 
  1. Loading spinner
  2. Desabilita campos
  3. Valida credenciais (3-5s)
  4. Sucesso: Card atualiza
  5. Erro: Mensagem de erro aparece

---

### 2.2 Feedback Visual em Tempo Real

#### Indicadores de Status

**Status: Conectado**
```
┌─────────────────────────────┐
│ 🟢 Online                    │
│ Última verificação: agora   │
└─────────────────────────────┘
```

**Status: Verificando**
```
┌─────────────────────────────┐
│ 🟡 Verificando...            │
│ [Spinner animado]           │
└─────────────────────────────┘
```

**Status: Erro**
```
┌─────────────────────────────┐
│ 🔴 Erro de conexão           │
│ [Tentar Novamente]          │
└─────────────────────────────┘
```

---

## 3. Protótipo: Migração em Progresso

### 3.1 Barra de Progresso Interativa

**Componente:**
```
┌─────────────────────────────────────────┐
│ ████████████████░░░░░░░░░░░░░░ 65%     │
└─────────────────────────────────────────┘
```

**Comportamento:**
- Atualiza a cada foto processada
- Animação suave de preenchimento
- Cores:
  - 0-50%: Azul
  - 50-90%: Amarelo
  - 90-100%: Verde

**Hover sobre barra:**
- Tooltip mostra: "3.402 de 5.234 fotos"

---

### 3.2 Atualização em Tempo Real

**Mecanismo:**
- WebSocket ou Polling a cada 2 segundos
- Atualiza sem recarregar página
- Transições suaves entre estados

**Elementos que atualizam:**
1. Barra de progresso
2. Contador de fotos
3. Velocidade de transferência
4. Tempo restante
5. Lista de atividade recente

**Exemplo de Atualização:**
```
Antes: 3.400 de 5.234 fotos
       Velocidade: 2.5 MB/s
       Tempo: ~18 minutos

[2 segundos depois]

Depois: 3.402 de 5.234 fotos
        Velocidade: 2.6 MB/s
        Tempo: ~17 minutos
```

**Animação:**
- Números fazem fade out/in
- Valores antigos desvanecem
- Novos valores aparecem

---

### 3.3 Controles de Migração

#### Botão Pausar

**Estado Normal:**
```
[⏸️ Pausar]
```

**Hover:**
- Escala 1.05
- Tooltip: "Pausar migração temporariamente"

**Click:**
1. Confirmação rápida (toast)
2. Migração pausa
3. Botão muda para "▶️ Retomar"
4. Progresso congela

**Estado Pausado:**
```
┌─────────────────────────────┐
│ ⏸️ Migração Pausada          │
│                              │
│ [▶️ Retomar] [❌ Cancelar]   │
└─────────────────────────────┘
```

---

#### Botão Cancelar

**Click:**
1. Modal de confirmação aparece
2. Aviso sobre perda de progresso
3. Opções: [Manter Migração] [Cancelar Migração]

**Confirmação de Cancelamento:**
1. Loading (1s)
2. Migração para
3. Toast: "Migração cancelada"
4. Redireciona para dashboard

---

## 4. Protótipo: Notificações e Feedback

### 4.1 Sistema de Notificações

#### Toast de Sucesso

**Aparição:**
```
                    ┌──────────────┐
                    │ ✅ Sucesso!  │
                    │              │
                    │ Migração     │
                    │ concluída.   │
                    │              │
                    │ [Ver] [✕]   │
                    └──────────────┘
```

**Comportamento:**
- Desliza da direita (400ms)
- Permanece 5 segundos
- Auto-fecha ou manual
- Stack de múltiplas notificações

**Interações:**
- Hover: Pausa timer
- Click em "Ver": Abre detalhes
- Click em "✕": Fecha imediatamente

---

#### Toast de Erro

**Aparição:**
```
                    ┌──────────────┐
                    │ ❌ Erro       │
                    │              │
                    │ Falha na     │
                    │ conexão.     │
                    │              │
                    │ [Tentar] [✕] │
                    └──────────────┘
```

**Comportamento:**
- Cor vermelha
- Permanece até ação do usuário
- Botão de ação destacado

---

### 4.2 Modais Interativos

#### Modal de Confirmação

**Estrutura:**
```
┌─────────────────────────────────┐
│  ⚠️  Confirmar Ação             │
│                                 │
│  Deseja realmente cancelar a   │
│  migração?                      │
│                                 │
│  O progresso atual será perdido.│
│                                 │
│  [Cancelar]  [Confirmar]       │
└─────────────────────────────────┘
```

**Interações:**
- Backdrop: Click fecha modal
- ESC: Fecha modal
- Tab: Navega entre botões
- Enter no "Confirmar": Executa ação
- Enter no "Cancelar": Fecha modal

**Animações:**
- Entrada: fadeInUp (300ms)
- Saída: fadeOutDown (200ms)
- Backdrop: fade in/out simultâneo

---

## 5. Protótipo: Formulários Interativos

### 5.1 Validação em Tempo Real

#### Campo Apple ID

**Estados:**

**Vazio:**
```
┌─────────────────────────────┐
│ Apple ID                    │
│ [________________]          │
└─────────────────────────────┘
```

**Digitando (inválido):**
```
┌─────────────────────────────┐
│ Apple ID                    │
│ [user@invalid]     ❌        │
│ Email inválido              │
└─────────────────────────────┘
```

**Válido:**
```
┌─────────────────────────────┐
│ Apple ID                    │
│ [user@icloud.com]  ✅        │
└─────────────────────────────┘
```

**Comportamento:**
- Validação após 500ms de inatividade
- Feedback imediato visual
- Mensagens claras e acionáveis

---

#### Campo Senha

**Indicador de Força:**
```
┌─────────────────────────────┐
│ Senha                       │
│ [••••••••]        [👁️]      │
│ ▓▓▓░░░░░░  Fraca            │
└─────────────────────────────┘
```

**Níveis:**
- Fraca: Vermelho, 1-2 barras
- Média: Amarelo, 3 barras
- Forte: Verde, 4-5 barras

---

### 5.2 Autocomplete e Sugestões

#### Sugestões de Email

**Comportamento:**
- Ao digitar "@", mostra sugestões:
  - @icloud.com
  - @me.com
  - @mac.com

**Interação:**
- Setas ↑↓: Navega sugestões
- Enter: Seleciona
- ESC: Fecha sugestões

---

## 6. Protótipo: Histórico Interativo

### 6.1 Filtros e Busca

#### Filtros

**Componente:**
```
┌─────────────────────────────┐
│ [Todos ▼] [Data ▼] [Status▼]│
└─────────────────────────────┘
```

**Interações:**
- Click abre dropdown
- Seleção atualiza lista instantaneamente
- Múltiplos filtros combináveis
- Botão "Limpar Filtros"

---

#### Busca

**Componente:**
```
┌─────────────────────────────┐
│ 🔍 [Buscar migrações...]    │
└─────────────────────────────┘
```

**Comportamento:**
- Busca em tempo real
- Filtra por:
  - Data
  - Status
  - Número de fotos
- Resultados destacados

---

### 6.2 Cards de Migração

#### Hover State

**Normal:**
```
┌─────────────────────────────┐
│ ✅ Migração Concluída        │
│ 15/12/2023                  │
│ 5.234 fotos                 │
└─────────────────────────────┘
```

**Hover:**
```
┌─────────────────────────────┐
│ ✅ Migração Concluída        │
│ 15/12/2023                  │
│ 5.234 fotos                 │
│ [Ver Detalhes] [Google]    │ ← Aparece
└─────────────────────────────┘
   ↑ Sombra aumenta
   ↑ Escala 1.02
```

**Click:**
- Navega para detalhes
- Transição suave
- Histórico mantido (breadcrumb)

---

## 7. Protótipo: Estados de Loading

### 7.1 Skeleton Screens

**Dashboard Carregando:**
```
┌─────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ← Animação shimmer
│ ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░ │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
└─────────────────────────────┘
```

**Vantagens:**
- Percepção de velocidade
- Menos ansiedade
- Melhor UX que spinner

---

### 7.2 Spinners Contextuais

#### Spinner Pequeno (Inline)
```
[⏳ Processando...]
```

#### Spinner Médio (Botão)
```
┌─────────────────┐
│ [⏳ Validando...]│
└─────────────────┘
```

#### Spinner Grande (Tela)
```
        ┌─────┐
        │ ⏳  │
        │     │
        │ Carregando... │
        └─────┘
```

---

## 8. Protótipo: Responsividade Interativa

### 8.1 Breakpoints

**Mobile (< 768px):**
- Menu hamburger
- Cards em coluna única
- Botões full-width
- Swipe gestures

**Tablet (768px - 1024px):**
- Menu lateral colapsável
- Cards em grid 2 colunas
- Touch-friendly

**Desktop (> 1024px):**
- Menu horizontal
- Cards em grid 3 colunas
- Hover states ativos

---

### 8.2 Gestos Mobile

**Swipe para Atualizar:**
- Pull to refresh no histórico
- Feedback visual durante swipe

**Swipe para Ações:**
- Swipe left: Ver detalhes
- Swipe right: Ações rápidas

**Pinch to Zoom:**
- Gráficos e imagens
- Detalhes de progresso

---

## 9. Protótipo: Microinterações

### 9.1 Feedback Tátil

**Cliques:**
- Vibração sutil (mobile)
- Som de clique (opcional, configurável)

**Sucesso:**
- Animação de confetti (opcional)
- Som de sucesso

**Erro:**
- Shake animation
- Som de erro

---

### 9.2 Animações de Transição

**Navegação entre Páginas:**
- Slide left/right
- Fade cross-fade
- Duração: 300ms

**Expansão de Cards:**
- Accordion animation
- Smooth height transition
- Duração: 400ms

---

## 10. Protótipo: Acessibilidade Interativa

### 10.1 Navegação por Teclado

**Atalhos:**
- `Tab`: Navega elementos
- `Enter`: Ativa botão focado
- `ESC`: Fecha modais
- `?`: Mostra atalhos

**Indicador de Foco:**
- Outline azul brilhante
- Contraste alto
- Visível sempre

---

### 10.2 Screen Reader

**Anúncios:**
- "Migração iniciada"
- "65% completo"
- "Migração concluída com sucesso"
- "Erro: credenciais inválidas"

**Labels:**
- Todos os botões têm aria-label
- Campos têm labels descritivos
- Estados anunciados

---

## 11. Ferramentas de Prototipagem Recomendadas

### Alta Fidelidade
- **Figma:** Protótipos interativos completos
- **Adobe XD:** Animações e transições
- **Sketch + InVision:** Prototipagem rápida

### Baixa/Média Fidelidade
- **Balsamiq:** Wireframes interativos
- **Axure:** Protótipos complexos
- **Framer:** Código + design

### Testes
- **Maze:** Testes de usabilidade
- **UserTesting:** Testes com usuários reais
- **Hotjar:** Heatmaps e gravações

---

## 12. Checklist de Interatividade

### Funcionalidades Obrigatórias
- [ ] Todos os botões têm estados (normal, hover, active, disabled)
- [ ] Formulários validam em tempo real
- [ ] Feedback visual em todas as ações
- [ ] Loading states em operações assíncronas
- [ ] Mensagens de erro claras e acionáveis
- [ ] Transições suaves entre estados
- [ ] Responsividade em todos os breakpoints
- [ ] Acessibilidade (teclado, screen reader)

### Funcionalidades Desejáveis
- [ ] Animações de microinteração
- [ ] Gestos mobile (swipe, pinch)
- [ ] Feedback tátil
- [ ] Sons de interface (opcional)
- [ ] Modo escuro
- [ ] Personalizações

---

**Documento gerado em:** [Data atual]  
**Versão:** 1.0  
**Status:** Pronto para implementação






