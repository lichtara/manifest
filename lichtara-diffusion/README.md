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
- Automação: workflow `generate-symbol.yml` (GitHub Actions) + `update-symbol-asset.yml`.
- Licenciamento: cada arte publicada é regida pela **Lichtara License v3.0 (Unificada)** + DOI 10.5281/zenodo.16762058.

## Próximos passos

- Adicionar os scripts em `pipelines/` (ex.: `generate_symbol.py`).
- Versionar os manifestos (v1, v2...) conforme o símbolo evoluir.
- Configurar os workflows para abrir PR com o `symbol-latest.png`.
