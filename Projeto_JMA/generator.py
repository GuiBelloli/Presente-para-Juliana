import json
import os
import base64
import qrcode
from jinja2 import Template
from PIL import Image

def encode_image_to_base64(filepath):
    """Converte imagem para base64 (para embutir no HTML)"""
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def generate_romantic_caption(hint, your_name, partner_name):
    """
    Retorna apenas a legenda que você escreveu
    """
    return hint

def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def process_photos(photos_list, assets_dir, config):
    """Processa fotos: converte para base64 e gera legendas"""
    processed = []
    for photo in photos_list:
        filepath = os.path.join(assets_dir, "photos", photo["filename"])
        if not os.path.exists(filepath):
            print(f"⚠️ Foto não encontrada: {filepath}")
            continue
        img_base64 = encode_image_to_base64(filepath)
        caption = generate_romantic_caption(
            photo.get("caption_hint", ""),
            config["couple"]["your_name"],
            config["couple"]["partner_name"]
        )
        processed.append({
            "src": f"data:image/jpeg;base64,{img_base64}",
            "caption": caption,
            "date": photo.get("date", "")
        })
    return processed

def generate_qr_code(url, output_path):
    """Gera QR Code apontando para a página hospedada"""
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"✅ QR Code salvo em: {output_path}")

def generate_html(config, photos_processed, template_path="templates/page.html"):
    """Gera o HTML final usando Jinja2"""
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    
    html = template.render(
        config=config,
        photos=photos_processed,
        spotify_embed=config["spotify"]["embed_url"]
    )
    return html

def main():
    print("🐼 Iniciando Gerador de Páginas Românticas...")
    
    # Carrega configurações
    config = load_config()
    
    # Processa fotos
    photos_processed = process_photos(
        config["photos"], 
        assets_dir="assets", 
        config=config
    )
    
    # Gera HTML
    html_content = generate_html(config, photos_processed)
    
    # Salva arquivo final
    os.makedirs("assets/output", exist_ok=True)
    output_path = "assets/output/index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Página gerada: {output_path}")
    
    # Gera QR Code (aponta para localhost por enquanto)
    # Após hospedar, atualize a URL abaixo
    generate_qr_code("https://seunome.netlify.app", "assets/output/qr_code.png")
    
    print("\n🎉 Pronto! Agora:")
    print("1. Abra 'assets/output/index.html' no navegador para testar")
    print("2. Para compartilhar: hospede em Netlify/GitHub Pages (veja README)")
    print("3. Use o QR Code gerado para presentear de forma física ou digital")

if __name__ == "__main__":
    main()