# Design System - Sistema de Migração iCloud para Google Drive

## 1. Princípios de Design

### 1.1 Valores Fundamentais

**Clareza:**
- Comunicação direta e objetiva
- Sem jargões técnicos desnecessários
- Feedback imediato em todas as ações

**Confiança:**
- Transparência total no processo
- Segurança visível e comunicada
- Controle ao usuário

**Simplicidade:**
- Interface limpa e focada
- Fluxos intuitivos
- Informações progressivas

**Acessibilidade:**
- Design inclusivo
- Conformidade WCAG 2.1 AA
- Suporte a múltiplos dispositivos

---

## 2. Paleta de Cores

### 2.1 Cores Primárias

**Azul Primário:**
- `#0066CC` - Principal (botões, links)
- `#0052A3` - Hover
- `#003D7A` - Active/Pressed
- `#E6F2FF` - Background suave

**Verde Sucesso:**
- `#00AA44` - Sucesso
- `#008833` - Hover
- `#E6F9ED` - Background

**Vermelho Erro:**
- `#CC0000` - Erro
- `#AA0000` - Hover
- `#FFE6E6` - Background

**Amarelo Aviso:**
- `#FFAA00` - Aviso
- `#CC8800` - Hover
- `#FFF4E6` - Background

### 2.2 Cores Neutras

**Cinzas:**
- `#1A1A1A` - Texto primário
- `#4A4A4A` - Texto secundário
- `#8A8A8A` - Texto terciário
- `#CCCCCC` - Bordas
- `#F5F5F5` - Background
- `#FFFFFF` - Fundo branco

### 2.3 Uso de Cores

**Status:**
- 🟢 Verde: Conectado, Sucesso, Completo
- 🟡 Amarelo: Processando, Aviso, Pausado
- 🔴 Vermelho: Erro, Falha, Desconectado
- ⚪ Cinza: Inativo, Não configurado

---

## 3. Tipografia

### 3.1 Família de Fontes

**Primária:** Inter ou System Font Stack
- `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`

**Monospace (códigos):**
- `"SF Mono", Monaco, "Courier New", monospace`

### 3.2 Escala Tipográfica

**Títulos:**
- H1: 32px / 40px line-height / Bold
- H2: 24px / 32px line-height / Bold
- H3: 20px / 28px line-height / SemiBold
- H4: 18px / 24px line-height / SemiBold

**Corpo:**
- Body Large: 16px / 24px line-height / Regular
- Body: 14px / 20px line-height / Regular
- Body Small: 12px / 16px line-height / Regular

**Especial:**
- Caption: 11px / 16px line-height / Regular
- Button: 14px / 20px line-height / SemiBold

### 3.3 Hierarquia

**Peso:**
- Bold (700): Títulos principais
- SemiBold (600): Subtítulos, botões
- Regular (400): Corpo de texto
- Light (300): Texto secundário

---

## 4. Componentes

### 4.1 Botões

#### Botão Primário
```
┌─────────────────────┐
│  [Texto do Botão]   │
└─────────────────────┘
```
- Background: #0066CC
- Texto: Branco
- Padding: 12px 24px
- Border-radius: 6px
- Hover: #0052A3
- Active: #003D7A

#### Botão Secundário
```
┌─────────────────────┐
│  [Texto do Botão]   │
└─────────────────────┘
```
- Background: Transparente
- Texto: #0066CC
- Borda: 1px solid #0066CC
- Hover: Background #E6F2FF

#### Botão Desabilitado
- Opacidade: 0.6
- Cursor: not-allowed
- Background: #CCCCCC

### 4.2 Formulários

#### Campo de Input
```
┌─────────────────────────────┐
│ Label                        │
│ ┌─────────────────────────┐ │
│ │ [Texto digitado]        │ │
│ └─────────────────────────┘ │
│ Mensagem de ajuda/erro       │
└─────────────────────────────┘
```

**Estados:**
- Normal: Borda #CCCCCC
- Foco: Borda #0066CC, sombra sutil
- Erro: Borda #CC0000, ícone ❌
- Sucesso: Borda #00AA44, ícone ✅

**Especificações:**
- Altura: 44px (mínimo para touch)
- Padding: 12px 16px
- Border-radius: 6px
- Font-size: 14px

### 4.3 Cards

#### Card Padrão
```
┌─────────────────────────────┐
│  [Ícone] Título              │
│                              │
│  Conteúdo do card            │
│                              │
│  [Ações]                     │
└─────────────────────────────┘
```

**Especificações:**
- Background: #FFFFFF
- Border: 1px solid #CCCCCC
- Border-radius: 8px
- Padding: 20px
- Sombra: 0 2px 4px rgba(0,0,0,0.1)
- Hover: Sombra aumenta, escala 1.02

### 4.4 Barras de Progresso

#### Barra de Progresso
```
┌─────────────────────────────────┐
│████████████░░░░░░░░░░░░ 65%     │
└─────────────────────────────────┘
```

**Especificações:**
- Altura: 8px
- Border-radius: 4px
- Background: #F5F5F5
- Fill: Gradiente azul
- Animação: Transição suave 0.5s

### 4.5 Notificações

#### Toast de Sucesso
```
┌─────────────────────────────┐
│ ✅ Sucesso!                  │
│ Mensagem de sucesso          │
│ [Ação] [✕]                  │
└─────────────────────────────┘
```

**Especificações:**
- Background: #FFFFFF
- Borda esquerda: 4px solid #00AA44
- Sombra: 0 4px 12px rgba(0,0,0,0.15)
- Posição: Canto superior direito
- Animação: Slide in da direita

---

## 5. Espaçamento

### 5.1 Sistema de Grid

**Base:** 4px

**Espaçamentos:**
- XS: 4px
- SM: 8px
- MD: 16px
- LG: 24px
- XL: 32px
- XXL: 48px

### 5.2 Layout

**Container:**
- Max-width: 1200px
- Padding lateral: 24px (mobile: 16px)
- Gutter: 24px

**Grid:**
- 12 colunas (desktop)
- 8 colunas (tablet)
- 4 colunas (mobile)

---

## 6. Ícones

### 6.1 Biblioteca

**Fonte de Ícones:** Feather Icons ou Material Icons

**Tamanhos:**
- Small: 16px
- Medium: 24px
- Large: 32px
- XLarge: 48px

### 6.2 Ícones Principais

- ✅ Check (sucesso)
- ❌ X (erro, fechar)
- ⚠️ Alert (aviso)
- ⏳ Loading (processando)
- 🔒 Lock (segurança)
- 📸 Camera (fotos)
- ⚙️ Settings (configurações)
- 📊 Chart (estatísticas)
- 🔄 Refresh (atualizar)
- ▶️ Play (iniciar)
- ⏸️ Pause (pausar)

---

## 7. Sombras e Elevação

### 7.1 Níveis de Elevação

**Level 0 (Flat):**
- Sem sombra

**Level 1 (Card):**
- `0 2px 4px rgba(0,0,0,0.1)`

**Level 2 (Hover):**
- `0 4px 8px rgba(0,0,0,0.12)`

**Level 3 (Modal):**
- `0 8px 24px rgba(0,0,0,0.15)`

**Level 4 (Dropdown):**
- `0 12px 32px rgba(0,0,0,0.18)`

---

## 8. Animações

### 8.1 Durações Padrão

- Rápida: 150ms (hover, focus)
- Média: 300ms (transições)
- Lenta: 500ms (animações complexas)

### 8.2 Easing

- Ease-in-out: Padrão para transições
- Ease-out: Entrada de elementos
- Ease-in: Saída de elementos

### 8.3 Animações Principais

**Fade:**
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

**Slide:**
```css
@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}
```

**Pulse:**
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

---

## 9. Responsividade

### 9.1 Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px
- Large Desktop: > 1440px

### 9.2 Adaptações

**Mobile:**
- Menu hamburger
- Cards full-width
- Botões full-width
- Font-size reduzido em 10%

**Tablet:**
- Menu lateral colapsável
- Cards em grid 2 colunas
- Tamanhos padrão mantidos

**Desktop:**
- Menu horizontal
- Cards em grid 3+ colunas
- Espaçamentos maiores

---

## 10. Acessibilidade

### 10.1 Contraste

**WCAG AA:**
- Texto normal: Mínimo 4.5:1
- Texto grande: Mínimo 3:1
- Componentes: Mínimo 3:1

### 10.2 Navegação por Teclado

- Tab order lógico
- Foco visível (outline azul)
- Atalhos de teclado
- Skip links

### 10.3 Screen Readers

- Labels descritivos
- ARIA labels
- Landmarks
- Estados anunciados

### 10.4 Touch Targets

- Mínimo: 44x44px
- Espaçamento entre: 8px mínimo

---

## 11. Tokens de Design

### 11.1 Variáveis CSS

```css
:root {
  /* Cores */
  --color-primary: #0066CC;
  --color-success: #00AA44;
  --color-error: #CC0000;
  --color-warning: #FFAA00;
  
  /* Espaçamento */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  
  /* Tipografia */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-size-base: 14px;
  
  /* Bordas */
  --border-radius: 6px;
  --border-radius-lg: 8px;
  
  /* Sombras */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 8px rgba(0,0,0,0.12);
  
  /* Transições */
  --transition-fast: 150ms;
  --transition-base: 300ms;
}
```

---

## 12. Guia de Uso

### 12.1 Quando Usar Cada Componente

**Botão Primário:**
- Ação principal da tela
- Confirmação de ações importantes
- Máximo 1 por tela

**Botão Secundário:**
- Ações secundárias
- Cancelamento
- Múltiplos permitidos

**Cards:**
- Agrupamento de informações relacionadas
- Status e resumos
- Listas de itens

**Modais:**
- Confirmações importantes
- Formulários complexos
- Informações detalhadas

---

## 13. Checklist de Implementação

### Componentes Base
- [ ] Botões (primário, secundário, desabilitado)
- [ ] Inputs (text, password, email)
- [ ] Cards
- [ ] Modais
- [ ] Notificações (toast)
- [ ] Barras de progresso
- [ ] Ícones

### Layout
- [ ] Grid system
- [ ] Container
- [ ] Header
- [ ] Footer
- [ ] Sidebar (se aplicável)

### Estados
- [ ] Loading
- [ ] Erro
- [ ] Sucesso
- [ ] Vazio
- [ ] Hover
- [ ] Focus
- [ ] Active

### Responsividade
- [ ] Mobile (< 768px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (> 1024px)

### Acessibilidade
- [ ] Contraste WCAG AA
- [ ] Navegação por teclado
- [ ] Screen reader support
- [ ] Touch targets adequados

---

**Documento gerado em:** [Data atual]  
**Versão:** 1.0  
**Status:** Pronto para implementação






