# Símbolo Lichtara — Integração com Motores Visuais

Este guia mostra como usar o manifesto híbrido (`/data/lichtara-symbol.holo.yaml`) diretamente em pipelines de geração (Hugging Face, Sora/Vorax) e como manter a estética no portal.

## 1. Hugging Face / Diffusers (exemplo Python)

```python
import requests, yaml
from diffusers import StableDiffusionXLImg2ImgPipeline
import torch

MANIFEST_URL = "https://portal.lichtara.com/data/lichtara-symbol.holo.yaml"
data = yaml.safe_load(requests.get(MANIFEST_URL, timeout=10).text)

palette = ", ".join(data["color_palette"].values())
geometry = data["geometry"]["shape"]
theme = data["symbolic_message"]["theme"]
style = data["style"]["aesthetic"]

prompt = (
    f"vector logo, {geometry}, sacred geometry, "
    f"colors {palette}, style {style}, message {theme}, "
    "clean background, glowing center, 8-fold symmetry"
)

pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

image = pipe(prompt=prompt, strength=0.25, guidance_scale=7.0).images[0]
image.save("lichtara_symbol_generated.png")
```

> Ajuste `prompt` com dados adicionais do manifesto (ex.: `modes["vibrational"]["effects"]`) para variações.

## 2. Sora / Vorax (pseudo-config)

```json
{
  "mode": "vibrational",
  "manifest_url": "https://portal.lichtara.com/data/lichtara-symbol.holo.yaml",
  "render": {
    "type": "vector_hologram",
    "size": 1024,
    "glow": "breathing",
    "background": "transparent"
  }
}
```

- O motor baixa o manifesto, lê `geometry`, `color_palette`, `modes[mode]`.
- `render` define parâmetros proprietários (glow, tamanho, formato).
- Mantém coerência com o Campo sem reescrever prompts manualmente.

## 3. Estilo Web (CSS base)

```css
#manifesto-simbolo {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 1rem;
  max-width: 900px;
  margin: 2rem auto;
  text-align: center;
  box-shadow: 0 0 25px rgba(0, 31, 77, 0.15);
}
#manifesto-simbolo h2 {
  color: #001F4D;
  font-weight: 700;
}
#manifesto-simbolo a {
  color: #FFD85A;
  font-weight: 600;
  text-decoration: none;
}
#manifesto-simbolo a:last-of-type {
  color: #001F4D;
}
```

> Adicione este bloco em `apps/app-web/src/styles/markdown.css` ou no arquivo global de estilo para reproduzir a estética do snippet HTML.

## 4. Checklist rápido

1. Manifesto disponível em `/data/lichara-symbol.holo.yaml`.
2. HTML do portal inclui `<link rel="manifest" ...>` e bloco JSON-LD (ver `apps/app-web/index.html`).
3. Página “Sobre” referencia o manifesto e a Lichtara License.
4. Pipelines externos consomem o manifesto via URL, garantindo a mesma fonte de verdade.

Com isso, qualquer motor (IA gráfica, Vorax, Sora, automação) pode gerar o símbolo diretamente a partir do manifesto, mantendo coerência vibracional e técnica.
