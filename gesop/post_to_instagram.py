#!/usr/bin/env python3
"""
Post gesop slides to Instagram locally.
Usage: python3 post_to_instagram.py "Your caption here" slide1.jpg slide2.jpg ...
       OR just run it with no args to pick the latest downloaded slides automatically.
"""

import sys, os, time, json, glob
from pathlib import Path

try:
    import requests
    import rookiepy
except ImportError:
    print("Installing dependencies...")
    os.system("pip3 install requests rookiepy pillow")
    import requests
    import rookiepy

from PIL import Image
import io

def get_session():
    cookies = rookiepy.chrome(['instagram.com'])
    cookie_dict = {c['name']: c['value'] for c in cookies}
    csrf = cookie_dict.get('csrftoken', '')
    if not csrf:
        print("❌ Not logged in to Instagram in Chrome. Open instagram.com and log in first.")
        sys.exit(1)

    session = requests.Session()
    for c in cookies:
        session.cookies.set(c['name'], c['value'], domain='.instagram.com')
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-CSRFToken': csrf,
        'X-IG-App-ID': '936619743392459',
        'X-IG-WWW-Claim': '0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    })
    return session, csrf

def upload_image(session, img_path):
    img = Image.open(img_path).convert('RGB')
    # Resize to square if needed
    w, h = img.size
    if w != h:
        side = min(w, h)
        img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    img = img.resize((1080, 1080), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=92)
    img_bytes = buf.getvalue()

    upload_id = str(int(time.time() * 1000))
    upload_name = f"{upload_id}_0_-{upload_id}"

    r = session.post(
        f'https://www.instagram.com/rupload_igphoto/{upload_name}',
        data=img_bytes,
        headers={
            'Content-Type': 'image/jpeg',
            'X-Entity-Type': 'image/jpeg',
            'X-Entity-Name': upload_name,
            'X-Entity-Length': str(len(img_bytes)),
            'Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps({
                'upload_id': upload_id,
                'xsharing_user_ids': '[]',
                'image_compression': json.dumps({'lib_name': 'moz', 'lib_version': '3.1.m', 'quality': '80'}),
            }),
        }
    )
    r.raise_for_status()
    uid = r.json().get('upload_id', upload_id)
    print(f"  ✓ Uploaded {Path(img_path).name} → {uid}")
    return uid

def post(image_paths, caption):
    print(f"\n📸 Posting {len(image_paths)} slide(s) to Instagram...")
    session, csrf = get_session()

    upload_ids = []
    for i, path in enumerate(image_paths):
        print(f"  Uploading slide {i+1}/{len(image_paths)}...")
        uid = upload_image(session, path)
        upload_ids.append(uid)
        time.sleep(0.8)

    print("  Publishing...")
    if len(upload_ids) == 1:
        r = session.post(
            'https://www.instagram.com/api/v1/media/configure/',
            data={
                'upload_id': upload_ids[0],
                'caption': caption,
                'usertags': '{"in":[]}',
                'source_type': '4',
                'like_and_view_counts_disabled': '0',
                'disable_comments': '0',
            }
        )
    else:
        client_sidecar_id = str(int(time.time() * 1000))
        children = [{'upload_id': uid, 'source_type': '4'} for uid in upload_ids]
        r = session.post(
            'https://www.instagram.com/api/v1/media/configure_sidecar/',
            json={
                'caption': caption,
                'children_metadata': children,
                'source_type': '4',
                'client_sidecar_id': client_sidecar_id,
            },
            headers={'Content-Type': 'application/json'},
        )

    result = r.json()
    if result.get('media') or result.get('status') == 'ok':
        media_id = result.get('media', {}).get('pk', '')
        print(f"\n✅ Posted! https://www.instagram.com/p/{result.get('media', {}).get('code', '')}/")
    else:
        print(f"\n❌ Error: {result.get('message', result)}")

if __name__ == '__main__':
    args = sys.argv[1:]

    # Find image files from args, or auto-detect latest gesop download
    image_files = [a for a in args if a.lower().endswith(('.jpg', '.jpeg', '.png'))]
    caption_args = [a for a in args if not a.lower().endswith(('.jpg', '.jpeg', '.png'))]
    caption = caption_args[0] if caption_args else ""

    if not image_files:
        # Auto-detect: look for gesop slides in Downloads
        downloads = Path.home() / 'Downloads'
        candidates = sorted(glob.glob(str(downloads / 'gesop_slides*.zip'))) + \
                     sorted(glob.glob(str(downloads / 'slide_*.jpg'))) + \
                     sorted(glob.glob(str(downloads / 'slide_*.png')))
        if candidates:
            print(f"Auto-detected: {candidates}")
            # If zip, extract
            if candidates[0].endswith('.zip'):
                import zipfile, tempfile
                tmp = tempfile.mkdtemp()
                with zipfile.ZipFile(candidates[-1]) as z:
                    z.extractall(tmp)
                image_files = sorted(glob.glob(os.path.join(tmp, '*.jpg')) + glob.glob(os.path.join(tmp, '*.png')))
            else:
                image_files = candidates
        else:
            print("Usage: python3 post_to_instagram.py 'Your caption' slide1.jpg slide2.jpg ...")
            print("       OR: python3 post_to_instagram.py  (auto-detects latest downloaded slides)")
            sys.exit(1)

    if not caption:
        caption = input("Caption (leave blank to skip): ").strip()

    post(image_files, caption)
