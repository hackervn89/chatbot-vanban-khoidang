import os
import sys
import zipfile
import json
import xml.etree.ElementTree as ET
import re
import shutil

# Reconfigure encoding for Windows console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Resolve paths
script_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(script_dir) # taovanban_khoidang
HDSD_DIR = os.path.join(PROJECT_ROOT, "references", "HDSD DHTN")
IMAGES_OUT_DIR = os.path.join(PROJECT_ROOT, "output", "images")

os.makedirs(IMAGES_OUT_DIR, exist_ok=True)

print(f"HDSD Source directory: {HDSD_DIR}")
print(f"Images Output directory: {IMAGES_OUT_DIR}")

def sanitize_folder_name(name):
    # Remove accent and replace special chars to make it URL friendly
    import unicodedata
    s = unicodedata.normalize('NFD', name)
    s = ''.join([c for c in s if not unicodedata.combining(c)])
    s = s.replace(" ", "_").replace("-", "_")
    return re.sub(r'[^a-zA-Z0-9__]', '', s)

def extract_images_from_docx(doc_path, rel_path):
    """
    Parses the docx XML, unzips referenced images, matches 'Hình' caption paragraphs to images
    and saves them to output directory.
    Returns a dict mapping: "Hình X" -> "images/folder_name/hinh_X.png"
    """
    doc_filename = os.path.basename(doc_path)
    folder_name = sanitize_folder_name(os.path.splitext(doc_filename)[0])
    dest_dir = os.path.join(IMAGES_OUT_DIR, folder_name)
    os.makedirs(dest_dir, exist_ok=True)

    rels = {}
    try:
        with zipfile.ZipFile(doc_path, 'r') as zip_ref:
            rels_xml = zip_ref.read('word/_rels/document.xml.rels')
            doc_xml = zip_ref.read('word/document.xml')
    except Exception as e:
        print(f"  [!] Lỗi khi đọc file zip {doc_filename}: {e}")
        return {}

    # Parse relationships to map rId -> target media file
    try:
        root_rels = ET.fromstring(rels_xml)
        namespaces_rels = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
        for r in root_rels.findall('.//rel:Relationship', namespaces_rels):
            r_id = r.get('Id')
            target = r.get('Target')
            if target and 'media' in target:
                rels[r_id] = target
    except Exception as e:
        print(f"  [!] Lỗi khi parse document.xml.rels cho {doc_filename}: {e}")
        return {}

    # Parse document structure in order of paragraphs
    paragraphs = []
    try:
        root_doc = ET.fromstring(doc_xml)
        namespaces_doc = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
        for p_el in root_doc.findall('.//w:p', namespaces_doc):
            text_runs = p_el.findall('.//w:t', namespaces_doc)
            text = "".join([t.text for t in text_runs]).strip()
            
            drawings = p_el.findall('.//w:drawing', namespaces_doc)
            images = []
            for drawing in drawings:
                embeds = drawing.findall('.//*[@r:embed]', namespaces_doc)
                for embed in embeds:
                    embed_id = embed.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                    if embed_id in rels:
                        images.append(rels[embed_id])
            paragraphs.append({'text': text, 'images': images})
    except Exception as e:
        print(f"  [!] Lỗi khi parse document.xml cho {doc_filename}: {e}")
        return {}

    mapping = {}
    extracted_count = 0

    # Look for 'Hình X' captions and map them to closest image in XML order
    for idx, p in enumerate(paragraphs):
        text = p['text']
        # Match 'Hình X', 'hình X:', 'HÌNH X -', etc.
        match = re.match(r'^(Hình\s+(\d+))\s*[:.-]?\s*(.*)', text, re.IGNORECASE)
        if match:
            hinh_label = f"Hình {match.group(2)}" # e.g. "Hình 1"
            
            # Find the closest paragraph containing an image within a window of 5 paragraphs
            found_image = None
            closest_dist = 999
            for offset in range(-5, 6):
                target_idx = idx + offset
                if 0 <= target_idx < len(paragraphs):
                    target_p = paragraphs[target_idx]
                    if target_p['images']:
                        dist = abs(offset)
                        if dist < closest_dist or (dist == closest_dist and offset < 0):
                            found_image = target_p['images'][0]
                            closest_dist = dist

            if found_image:
                # Extract this image from the zip and write to destination folder
                zip_path = f"word/{found_image}"
                # Keep file extension (.png, .jpg, etc.)
                _, ext = os.path.splitext(found_image)
                out_filename = f"hinh_{match.group(2)}{ext}".lower()
                out_path = os.path.join(dest_dir, out_filename)
                
                try:
                    with zipfile.ZipFile(doc_path, 'r') as zip_ref:
                        with zip_ref.open(zip_path) as source_img, open(out_path, 'wb') as dest_file:
                            shutil.copyfileobj(source_img, dest_file)
                    
                    # Store web URL path
                    mapping[hinh_label] = f"images/{folder_name}/{out_filename}"
                    extracted_count += 1
                except Exception as e:
                    print(f"    [!] Không thể giải nén {zip_path}: {e}")

    if extracted_count > 0:
         print(f"[+] {doc_filename}: Đã trích xuất {extracted_count} ảnh vào '{folder_name}/'")
    return mapping

def main():
    if not os.path.exists(HDSD_DIR):
        print(f"[!] Thư mục HDSD không tồn tại: {HDSD_DIR}")
        sys.exit(1)

    image_map = {}
    
    # Scan subdirectories: Web, Mobile, Tablet
    for category in ["Web", "Mobile", "Tablet"]:
        category_dir = os.path.join(HDSD_DIR, category)
        if not os.path.exists(category_dir):
            continue
            
        print(f"[*] Quét thư mục: {category}")
        for file in os.listdir(category_dir):
            if file.endswith(".docx") and not file.startswith("~$"):
                doc_path = os.path.join(category_dir, file)
                
                # Construct RAG source key: "HDSD/Category/Filename.docx"
                # To maintain compatibility, check file encoding/accents
                rag_source_key = f"HDSD/{category}/{file}"
                
                print(f"  - Đang xử lý: {file}...")
                mapping = extract_images_from_docx(doc_path, rag_source_key)
                if mapping:
                    image_map[rag_source_key] = mapping

    # Write mapping to image_map.json in the images output folder
    map_json_path = os.path.join(IMAGES_OUT_DIR, "image_map.json")
    with open(map_json_path, 'w', encoding='utf-8') as f:
        json.dump(image_map, f, ensure_ascii=False, indent=2)
        
    print("=" * 50)
    print(f"[Thành công] Đã lưu tệp bản đồ hình ảnh tại: {map_json_path}")
    print(f"Tổng số tài liệu được map: {len(image_map)}")

if __name__ == "__main__":
    main()
