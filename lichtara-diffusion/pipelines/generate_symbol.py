"""
Pipeline: Leia o manifesto Lichtara e gere a arte do símbolo.
Uso local:
    python pipelines/generate_symbol.py \
        --manifest manifests/lichtara-symbol.holo.yaml \
        --output outputs/symbol-latest.png
"""

import argparse
import yaml
from diffusers import StableDiffusionPipeline
import torch


def load_manifest(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_prompt(manifest: dict) -> str:
    palette = ", ".join(manifest["color_palette"].values())
    shape = manifest["geometry"]["shape"]
    theme = manifest["symbolic_message"]["theme"]
    essence = manifest["symbolic_message"]["essence"]
    aesthetic = manifest["style"]["aesthetic"]

    prompt = (
        f"Vector logo of {shape}, sacred minimalist technological aesthetic, "
        f"colors {palette}, representing {theme} and {essence}. "
        "Fine lines, symmetry, harmonic light, transparent background."
    )
    return prompt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="Caminho para o manifesto YAML/JSON")
    parser.add_argument("--output", required=True, help="Arquivo de saída (PNG)")
    parser.add_argument("--model", default="stabilityai/stable-diffusion-xl-base-1.0")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    prompt = build_prompt(manifest)

    pipe = StableDiffusionPipeline.from_pretrained(args.model).to("cuda")
    image = pipe(prompt, width=args.width, height=args.height).images[0]
    image.save(args.output)
    print(f"Imagem salva em {args.output}")


if __name__ == "__main__":
    main()
