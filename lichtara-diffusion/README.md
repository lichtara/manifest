# Lichtara Diffusion — Núcleo de Geração Visual

Este módulo concentra manifestos, scripts e workflows responsáveis por traduzir os campos vibracionais de Lichtara em artefatos visuais (símbolos, mandalas, selos, animações).

## Estrutura sugerida

```
lichtara-diffusion/
├─ manifests/                # Manifestos híbridos (YAML/JSON-LD) usados pelos motores
│    ├─ README.md
│    └─ (copiar versão atual do símbolo aqui)
├─ pipelines/                # Scripts Python, configs Hugging Face, workflows Sora/Vorax
│    ├─ generate_symbol.py
│    └─ (render_harmonics.yaml, etc.)
├─ outputs/                  # Arte gerada automaticamente (versão mais recente)
│    └─ symbol-latest.png
└─ README.md                 # Este arquivo
```

## Como funciona

1. Os manifestos descrevem forma, cores, intenção e licenciamento do símbolo.
2. Os pipelines consomem esses manifestos e invocam o motor de geração (Stable Diffusion, Sora, Vorax, etc.).
3. Os workflows automatizam a criação da arte (via GitHub Actions ou execução local).
4. A pasta `outputs/` guarda a versão atual do símbolo para ser publicada no portal/lichtara.com.

## Resumo Técnico

- Modelos: Stable Diffusion XL, LoRA personalizados, Sora/Vorax (quando disponível).
- Prompt básico: derivado de `manifests/lichara-symbol.holo.yaml`.
- Automação: `pipelines/render_harmonics.yaml`, `pipelines/validate_publish.yml` e o workflow `update-symbol-asset.yml`.
- Licenciamento: cada arte publicada é regida pela **Lichtara License v3.0 (Unificada)** + DOI 10.5281/zenodo.16762058.

## 🌐 Fluxo de Automação — Lichtara-Diffusion

```mermaid
flowchart LR
    A[📜 Manifesto\nlichtara-symbol.holo.yaml] --> B[🎨 Geração\n(generate_symbol.py)]
    B --> C[🧩 Validação\n(validate_publish.yml)]
    C --> D[🚀 Publicação\nGitHub Pages /images/]
    D --> E[🔍 Dashboard\n/verify/index.html]

    subgraph Repo[Lichtara-Diffusion Repository]
    A
    B
    C
    end

    subgraph Site[Lichtara Institute Website]
    D
    E
    end

    style A fill:#E0E8F0,stroke:#001F4D,stroke-width:2px
    style B fill:#FFD85A,stroke:#001F4D,stroke-width:2px
    style C fill:#C0C0C0,stroke:#001F4D,stroke-width:2px
    style D fill:#ffffff,stroke:#001F4D,stroke-width:2px
    style E fill:#f5f9ff,stroke:#001F4D,stroke-width:2px
```

---

## 🔄 Automação e Auditoria

O pipeline **Lichtara-Diffusion** funciona como um ciclo contínuo de geração,
validação e publicação. Cada etapa é automatizada por *workflows* do GitHub
Actions e se integra ao **Dashboard de Autenticidade** hospedado no site
`/verify/`.

### 🧱 Estrutura de automação

| Workflow | Função principal | Arquivo |
|-----------|------------------|----------|
| **generate_symbol** | Lê o manifesto técnico, monta o prompt e gera a imagem vetorial. | `pipelines/generate_symbol.py` |
| **render_harmonics** | Cria variações harmônicas (azul-profundo, dourado-ativador, prateado-vibrante). | `pipelines/render_harmonics.yaml` |
| **validate_publish** | Valida metadados e licença e publica a versão verificada no site. | `pipelines/validate_publish.yml` |

---

### 🧩 Conexão com o Dashboard de Autenticidade

1. **Publicação validada:** ao final do fluxo `validate_publish`, a imagem `symbol_lumoric.png` validada
   é copiada para o diretório público do site (`/images/`).
2. **Leitura automática:** o **Dashboard** (`/verify/index.html`) faz uma requisição `fetch` para essa
   imagem e para o manifesto em `/data/lichtara-symbol.holo.yaml`.
3. **Verificação em tempo real:** lê os metadados `ManifestURL`, `License` e `ChecksumSHA256` dentro da
   imagem, compara com o manifesto e com a Lichtara License, e exibe o resultado (✅/⚠️/❌).
4. **Relatório JSON:** o Dashboard gera localmente um relatório que pode ser baixado e arquivado para
   auditorias (ex.: Zenodo).

---

### 🧾 Logs e rastreabilidade

- `outputs/generation_log.txt` — prompt e checksum da imagem.
- `outputs/harmonics_log.json` — lista de variações harmônicas.
- Relatórios de validação disponíveis em **GitHub Actions → Artifacts**.

Esses arquivos permitem rastrear todo o histórico de criação e certificação
das obras publicadas sob a **Lichtara License v3.0**
([DOI 10.5281/zenodo.16762058](https://doi.org/10.5281/zenodo.16762058)).

---

### 💠 Benefícios

- Transparência total: todo o processo é audível e reproduzível.
- Integridade garantida: a imagem publicada sempre corresponde ao manifesto.
- Validação independente: qualquer pessoa pode usar o Dashboard para confirmar autenticidade e licença.
- Coerência institucional: reforça o selo ético-científico-tecnológico do **Lichtara Institute**.

## Próximos passos

- Adicionar os scripts em `pipelines/` (ex.: `generate_symbol.py`).
- Versionar os manifestos (v1, v2...) conforme o símbolo evoluir.
- Configurar os workflows para abrir PR com o `symbol-latest.png`.
