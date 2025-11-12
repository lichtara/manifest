"""
Pipeline: Leia o manifesto Lichtara e gere a arte do símbolo.
Uso local:
    python pipelines/generate_symbol.py \
        --manifest manifests/lichtara-symbol.holo.yaml \
        --output outputs/symbol-latest.png
"""

import argparse
import hashlib
import json
import yaml
from pathlib import Path

from diffusers import StableDiffusionPipeline
from PIL import Image, PngImagePlugin
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


def embed_metadata(image_path: Path, manifest: dict, manifest_url: str, license_url: str):
    """Insere metadados 'lumóricos' (manifesto, licença, checksum) no PNG."""
    png = Image.open(image_path)
    meta = PngImagePlugin.PngInfo()

    with open(image_path, "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()

    mini_manifest = {
        "name": manifest.get("name"),
        "geometry": manifest.get("geometry", {}).get("shape"),
        "theme": manifest.get("symbolic_message", {}).get("theme"),
        "essence": manifest.get("symbolic_message", {}).get("essence"),
    }

    meta.add_text("ManifestURL", manifest_url)
    meta.add_text("License", license_url)
    meta.add_text("ChecksumSHA256", checksum)
    meta.add_text("LichtaraMeta", json.dumps(mini_manifest, ensure_ascii=False))

    png.save(image_path, pnginfo=meta)
    print(f"Metadados inseridos em {image_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="Caminho para o manifesto YAML/JSON")
    parser.add_argument("--output", required=True, help="Arquivo de saída (PNG)")
    parser.add_argument("--model", default="stabilityai/stable-diffusion-xl-base-1.0")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument(
        "--manifest-url",
        default="https://portal.lichtara.com/data/lichtara-symbol.holo.yaml",
        help="URL pública do manifesto para referência futura.",
    )
    parser.add_argument(
        "--license-url",
        default="https://doi.org/10.5281/zenodo.16762058",
        help="URL da Lichtara License v3.0 ou licença complementar.",
    )
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    prompt = build_prompt(manifest)

    pipe = StableDiffusionPipeline.from_pretrained(args.model).to("cuda")
    image = pipe(prompt, width=args.width, height=args.height).images[0]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    embed_metadata(output_path, manifest, args.manifest_url, args.license_url)
    print(f"Imagem salva em {output_path}")


if __name__ == "__main__":
    main()
