# Configuração do QStash para Background Workers

Este guia explica como configurar o QStash como alternativa ao Celery para processamento de tarefas em background.

## O que é QStash?

QStash é um serviço de fila de mensagens serverless da Upstash que permite processar tarefas em background sem precisar de workers dedicados. É uma excelente alternativa ao Celery para projetos que não querem gerenciar workers separados.

## Vantagens do QStash

- ✅ **Gratuito**: 10.000 requisições/dia no plano gratuito
- ✅ **Serverless**: Não precisa de workers dedicados
- ✅ **Simples**: Usa HTTP, sem necessidade de Redis ou RabbitMQ
- ✅ **Confiável**: Retry automático e garantia de entrega
- ✅ **Escalável**: Escala automaticamente

## Passo a Passo

### 1. Criar Conta no Upstash

1. Acesse: https://console.upstash.com/
2. Crie uma conta (gratuita)
3. Crie um novo projeto

### 2. Criar QStash

1. No dashboard do Upstash, vá para **QStash**
2. Clique em **Create QStash**
3. Anote as seguintes informações:
   - **Token**: Token de autenticação
   - **Current Signing Key**: Chave para verificar assinaturas
   - **Next Signing Key**: Chave de rotação (opcional)

### 3. Configurar Variáveis de Ambiente

Adicione as seguintes variáveis ao seu arquivo `.env`:

```env
# QStash
QSTASH_TOKEN=seu-token-aqui
QSTASH_CURRENT_SIGNING_KEY=seu-signing-key-aqui
QSTASH_NEXT_SIGNING_KEY=seu-next-signing-key-opcional
BASE_URL=https://seu-backend.onrender.com
```

**Para Render:**
1. Vá para o dashboard do seu serviço
2. Vá em **Environment**
3. Adicione as variáveis:
   - `QSTASH_TOKEN`
   - `QSTASH_CURRENT_SIGNING_KEY`
   - `QSTASH_NEXT_SIGNING_KEY` (opcional)
   - `BASE_URL` (URL do seu serviço, ex: `https://imgmigrator.onrender.com`)

### 4. Verificar Configuração

O backend detecta automaticamente se o QStash está configurado. Se `QSTASH_TOKEN` estiver presente, ele usará QStash. Caso contrário, tentará usar Celery como fallback.

### 5. Testar

1. Crie uma nova migração através da API
2. Verifique os logs do backend para confirmar que a tarefa foi publicada no QStash
3. Verifique o dashboard do QStash para ver as mensagens processadas

## Como Funciona

1. **Publicação**: Quando uma migração é criada, o backend publica uma mensagem no QStash
2. **Webhook**: O QStash envia uma requisição HTTP para o endpoint `/api/v1/webhooks/qstash`
3. **Processamento**: O endpoint processa a migração de forma assíncrona
4. **Retry**: Se houver erro, o QStash tenta novamente automaticamente

## Endpoint do Webhook

O endpoint do webhook é:
```
POST /api/v1/webhooks/qstash
```

Este endpoint:
- Verifica a assinatura do QStash (segurança)
- Extrai `migration_id` e `user_id` do payload
- Processa a migração usando a função `process_migration_async`

## Payload

O payload enviado pelo QStash é:
```json
{
  "migration_id": 123,
  "user_id": 1
}
```

## Limites do Plano Gratuito

- **10.000 requisições/dia**
- **Rate limit**: 100 requisições/segundo
- **Timeout**: 30 segundos por requisição

Para projetos maiores, considere o plano pago.

## Troubleshooting

### Erro: "QSTASH_TOKEN não está configurado"

- Verifique se a variável `QSTASH_TOKEN` está definida no `.env` ou nas variáveis de ambiente do Render

### Erro: "Webhook URL não configurado"

- Verifique se a variável `BASE_URL` está definida
- O `BASE_URL` deve ser a URL completa do seu backend (ex: `https://imgmigrator.onrender.com`)

### Erro: "Invalid signature"

- Verifique se `QSTASH_CURRENT_SIGNING_KEY` está correto
- Se você rotacionou as chaves, atualize `QSTASH_CURRENT_SIGNING_KEY` e `QSTASH_NEXT_SIGNING_KEY`

### Tarefas não estão sendo processadas

1. Verifique os logs do backend
2. Verifique o dashboard do QStash para ver se as mensagens estão sendo enviadas
3. Verifique se o endpoint `/api/v1/webhooks/qstash` está acessível publicamente
4. Verifique se o `BASE_URL` está correto e acessível

## Migração do Celery para QStash

Se você já está usando Celery:

1. Configure o QStash (passos acima)
2. O sistema automaticamente usará QStash se `QSTASH_TOKEN` estiver configurado
3. Você pode manter o Celery como fallback removendo `QSTASH_TOKEN` se necessário
4. Não é necessário remover o Celery, ele será usado apenas se QStash não estiver disponível

## Comparação: QStash vs Celery

| Recurso | QStash | Celery |
|---------|--------|--------|
| Setup | Simples (apenas HTTP) | Complexo (Redis/RabbitMQ + Workers) |
| Custo | Gratuito até 10k/dia | Requer infraestrutura |
| Escalabilidade | Automática | Manual |
| Workers | Não precisa | Precisa gerenciar |
| Retry | Automático | Configurável |
| Melhor para | Projetos pequenos/médios | Projetos grandes/complexos |

## Recursos Adicionais

- [Documentação do QStash](https://docs.upstash.com/qstash)
- [Dashboard do Upstash](https://console.upstash.com/)
- [Exemplos de uso](https://github.com/upstash/qstash-examples)






