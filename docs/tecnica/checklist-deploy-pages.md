# Checklist — Publicação do portal.lichtara.com

## 1. DNS e domínio
- [ ] Em Settings → Pages, definir o domínio customizado `portal.lichtara.com`.
- [ ] Configurar o DNS externamente com um registro **CNAME** apontando `portal.lichtara.com` → `lichtara.github.io`.
- [ ] Garantir que `apps/app-web/public/CNAME` contenha exatamente `portal.lichtara.com`.

## 2. Variáveis (Repository → Settings → Secrets and variables → Actions → *Variables*)
| Nome                     | Exemplo/descrição                                                       |
|--------------------------|--------------------------------------------------------------------------|
| `VITE_BASE_PATH`         | `/` (ou `/portal/` se usar subpath)                                     |
| `VITE_SYNTARIS_BASE_URL` | `https://api.<dominio>/syntaris` (backend público)                      |
| `VITE_SENTRY_DSN`        | DSN público do cliente (opcional)                                       |
| `SENTRY_URL`             | `https://de.sentry.io` (se usar Sentry)                                 |
| `SENTRY_ORG`             | `lichtara`                                                              |
| `SENTRY_PROJECT`         | `app-web`                                                               |

> Observação: `VITE_SENTRY_RELEASE` e `SENTRY_RELEASE` são preenchidos automaticamente (`app-web@${{ github.sha }}`).

## 3. Secrets (Repository → Settings → Secrets and variables → Actions → *Secrets*)
- `SENTRY_AUTH_TOKEN` (opcional; necessário apenas para upload automático de sourcemaps).

## 4. Workflow (Deploy Pages)
1. Confirmar que `main` está atualizado (`npm run build:release` já foi validado localmente).
2. Push para `main` ou executar manualmente o workflow “Deploy Pages”.
3. Aguardar os jobs:
   - `build`: instala dependências (`npm ci`), executa `npm run build:release`, envia artifact.
   - `deploy`: publica via `actions/deploy-pages@v4`.

> Workflow (no repositório `portal`): `portal/.github/workflows/deploy-pages.yml`

## 5. Pós-publicação
- [ ] Verificar o link exibido no ambiente `github-pages`.
- [ ] Testar rotas principais (`/`, `/mandalas`, `/ativar`, `/painel` etc.).
- [ ] Confirmar que o proxy/Syntaris responde (ver rede no navegador, chamadas `POST /api/syntaris/...`).
- [ ] Registrar na mandala (`docs/mapa-vibracional-status.md`) que a pétala “Vórtice de experiência” está em produção.

Manter este checklist junto ao time garante que qualquer nova publicação repita o ritual de forma consistente.
