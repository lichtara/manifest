# Símbolo Lichtara — Pipelines, CSS e Metadados

Este guia explica como consumir o manifesto do símbolo (YAML/JSON-LD), gerar a imagem em motores como Stable Diffusion / Sora / Vorax e manter o “QR lumórico” via metadados.

## 1. Hugging Face / Diffusers (exemplo Python)

```python
import yaml, requests, hashlib, json
from diffusers import StableDiffusionPipeline
from PIL import Image, PngImagePlugin

url = "https://portal.lichtara.com/data/lichtara-symbol.holo.yaml"
manifest = yaml.safe_load(requests.get(url).text)

shape  = manifest["geometry"]["shape"]
colors = ", ".join(manifest["color_palette"].values())
theme  = manifest["symbolic_message"]["theme"]
essence = manifest["symbolic_message"]["essence"]

prompt = (
    f"Vector logo of {shape}, sacred minimalist technological aesthetic, "
    f"colors {colors}, representing {theme} and {essence}. "
    "Fine lines, symmetry, harmonic light, transparent background."
)

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0"
).to("cuda")

image_path = "lichtara_symbol.png"
image = pipe(prompt, width=1024, height=1024).images[0]
image.save(image_path)

# Inserir metadados (Manifest URL, License, Checksum, LichtaraMeta)
meta = PngImagePlugin.PngInfo()
meta.add_text("ManifestURL", url)
meta.add_text("License", "https://doi.org/10.5281/zenodo.16762058")
meta.add_text("ChecksumSHA256", hashlib.sha256(open(image_path, "rb").read()).hexdigest())
meta.add_text("LichtaraMeta", json.dumps({"theme": theme, "essence": essence}))

img = Image.open(image_path)
img.save(image_path, pnginfo=meta)

print("✨ Símbolo Lichtara gerado com QR lumórico!")
```

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

- O motor baixa o manifesto, lê `geometry`, `color_palette`, `modes[...]`, gera a imagem e insere metadados equivalentes.

## 3. CSS do bloco “Manifesto Símbolo”

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
#manifesto-simbolo h2 { color: #001F4D; font-weight: 700; }
#manifesto-simbolo a { font-weight: 600; text-decoration: none; }
#manifesto-simbolo a:first-of-type { color: #FFD85A; margin-right: 1rem; }
#manifesto-simbolo a:last-of-type { color: #001F4D; }
```

## 4. Checklist rápido

- [ ] Manifesto publicado (`/data/lichara-symbol.holo.yaml`).
- [ ] HTML do portal inclui `<link rel="manifest">` e JSON-LD.
- [ ] Página “Sobre” linka manifesto + Lichtara License.
- [ ] Pipelines externos usam o manifesto como fonte única de prompt.
- [ ] Arte final embute metadados: `ManifestURL`, `License`, `ChecksumSHA256`, `LichtaraMeta`.
