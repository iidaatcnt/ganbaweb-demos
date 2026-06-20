import csv
import os
import re
import urllib.parse

csv_file = "saitama6_result.csv"
output_dir = "ganbaweb_demos"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{city}で{category}の専門業者をお探しなら{company_name}へ。職人直営の適正価格と高品質な施工をお約束します。ご相談・お見積り無料。">
    <title>{company_name} | {city}の{category}・専門工事</title>
    <style>
        :root {{
            --primary: #2C3E50;
            --secondary: #3498DB;
            --accent: #E67E22;
            --text: #333333;
            --bg: #F8F9FA;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif; color: var(--text); background: var(--bg); line-height: 1.6; }}
        
        /* Header */
        header {{ background: #fff; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 100; }}
        .logo {{ font-size: 24px; font-weight: bold; color: var(--primary); letter-spacing: 1px; }}
        .header-tel {{ font-size: 16px; font-weight: bold; color: var(--primary); }}
        .header-tel span {{ color: var(--secondary); font-size: 20px; }}
        .nav-links {{ display: flex; gap: 20px; list-style: none; }}
        .nav-links a {{ text-decoration: none; color: var(--primary); font-weight: bold; }}
        .menu-btn {{ display: none; background: none; border: none; font-size: 28px; cursor: pointer; color: var(--primary); }}
        
        /* Hero Section Slider */
        .hero {{ position: relative; color: #fff; text-align: center; padding: 100px 5%; overflow: hidden; }}
        .slider-bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; z-index: 1; opacity: 0; animation: fade 15s infinite; }}
        .slider-bg::after {{ content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(44, 62, 80, 0.7); }}
        .bg1 {{ background-image: url('https://images.unsplash.com/photo-1504307651254-35680f356dfd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'); animation-delay: 0s; }}
        .bg2 {{ background-image: url('https://images.unsplash.com/photo-1589939705384-5185137a7f0f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'); animation-delay: 5s; }}
        .bg3 {{ background-image: url('https://images.unsplash.com/photo-1503387762-592deb58ef4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'); animation-delay: 10s; }}
        @keyframes fade {{ 0% {{ opacity: 1; transform: scale(1); }} 25% {{ opacity: 1; transform: scale(1.05); }} 33% {{ opacity: 0; transform: scale(1.06); }} 92% {{ opacity: 0; transform: scale(1); }} 100% {{ opacity: 1; transform: scale(1); }} }}
        .hero-content {{ position: relative; z-index: 2; }}
        .hero h1 {{ font-size: 36px; margin-bottom: 20px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }}
        .hero p {{ font-size: 18px; margin-bottom: 40px; }}
        .btn-cta {{ display: inline-block; background: var(--accent); color: #fff; text-decoration: none; padding: 15px 40px; font-size: 18px; font-weight: bold; border-radius: 5px; transition: background 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .btn-cta:hover {{ background: #d35400; }}

        /* Trust Section (Strengths) */
        .trust {{ padding: 60px 5%; text-align: center; background: #fff; }}
        .trust h2 {{ font-size: 28px; color: var(--primary); margin-bottom: 30px; }}
        .trust-grid {{ display: flex; flex-wrap: wrap; gap: 20px; max-width: 800px; margin: 0 auto; justify-content: center; }}
        .review-card {{ background: var(--bg); padding: 30px; border-radius: 8px; flex: 1; min-width: 250px; border-left: 5px solid var(--secondary); box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: left; }}
        .review-card h3 {{ color: var(--primary); margin-bottom: 10px; font-size: 20px; }}

        /* Services */
        .services {{ padding: 60px 5%; background: var(--primary); color: #fff; }}
        .services h2 {{ text-align: center; font-size: 28px; margin-bottom: 40px; }}
        .service-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; max-width: 1000px; margin: 0 auto; }}
        .service-card {{ background: rgba(255,255,255,0.1); padding: 30px; border-radius: 8px; text-align: center; }}
        .service-card h3 {{ color: var(--secondary); margin-bottom: 15px; font-size: 20px; }}

        /* Contact Section */
        .contact {{ padding: 80px 5%; text-align: center; background: #fff; }}
        .contact h2 {{ font-size: 28px; color: var(--primary); margin-bottom: 20px; }}
        .contact p {{ font-size: 18px; margin-bottom: 30px; }}
        .tel-large {{ font-size: 36px; font-weight: bold; color: var(--secondary); margin-bottom: 20px; display: block; text-decoration: none; }}
        .map-container {{ margin: 30px auto; max-width: 800px; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .map-btn {{ display: inline-block; margin-top: 10px; padding: 10px 20px; background: #4285F4; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }}

        /* Footer & Banner */
        footer {{ background: #1A252F; color: #fff; text-align: center; padding: 30px 5%; font-size: 14px; }}
        .disclaimer {{ margin-top: 20px; font-size: 12px; color: #aaa; text-align: left; max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.4; }}
        .global-banner {{ background: #FFD700; color: #333; text-align: center; padding: 12px 5%; font-weight: bold; font-size: 14px; z-index: 1000; position: relative; border-bottom: 2px solid #E67E22; }}
        .global-banner a {{ color: #E67E22; text-decoration: underline; margin-left: 10px; }}
        
        /* Mobile Sticky Footer CTA */
        .mobile-cta {{ display: none; }}
        @media (max-width: 768px) {{
            .header-tel {{ display: none; }}
            .menu-btn {{ display: block; }}
            .nav-links {{ display: none; position: absolute; top: 100%; left: 0; width: 100%; background: #fff; flex-direction: column; text-align: center; padding: 15px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .nav-links.active {{ display: flex; }}
            .hero {{ padding: 60px 5%; }}
            .hero h1 {{ font-size: 24px; }}
            .tel-large {{ font-size: 24px; }}
            .trust-grid {{ flex-direction: column; }}
            .mobile-cta {{
                display: block;
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background: var(--accent);
                color: #fff;
                text-align: center;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                text-decoration: none;
                z-index: 1000;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            }}
            body {{ padding-bottom: 60px; }}
        }}
    </style>
</head>
<body>
    <div class="global-banner">
        【事業者様へ】このページはガンバWebが自動生成したデモサイトです。このデザインで公式Webサイトを持ちませんか？
        <a href="https://ganbaweb.com/" target="_blank">詳細・お問い合わせはこちら</a>
    </div>
    <header>
        <div class="logo">{company_name}</div>
        <nav>
            <ul class="nav-links" id="navLinks">
                <li><a href="#trust" onclick="toggleMenu()">当社の強み</a></li>
                <li><a href="#services" onclick="toggleMenu()">事業内容</a></li>
                <li><a href="#contact" onclick="toggleMenu()">お問い合わせ</a></li>
            </ul>
        </nav>
        <button class="menu-btn" onclick="toggleMenu()">☰</button>
        <div class="header-tel">お見積り・ご相談 <span>{phone}</span></div>
    </header>
    <a href="tel:{phone}" class="mobile-cta">📞 電話で無料相談</a>

    <section class="hero">
        <div class="slider-bg bg1"></div>
        <div class="slider-bg bg2"></div>
        <div class="slider-bg bg3"></div>
        <div class="hero-content">
            <h1>{city}で選ばれる確かな技術。<br>{category}のことなら{company_name}。</h1>
            <p>職人直営だからできる「適正価格」と「高品質」をお約束します。<br>地域の皆様の安心と安全を第一に施工いたします。</p>
            <a href="#contact" class="btn-cta">無料お見積り・お問い合わせ</a>
        </div>
    </section>

    <section class="trust" id="trust">
        <h2>当社の強み</h2>
        <div class="trust-grid">
            <div class="review-card">
                <h3>職人直営の適正価格</h3>
                <p>中間の営業マンを挟まないため、無駄なマージンがかかりません。高品質な施工を適正価格でお届けします。</p>
            </div>
            <div class="review-card">
                <h3>{city}密着のスピード対応</h3>
                <p>地元・{city}エリアを中心に絞ることで、フットワーク軽く迅速な対応が可能です。小さな修繕からお任せください。</p>
            </div>
        </div>
    </section>

    <section class="services" id="services">
        <h2>事業内容</h2>
        <div class="service-grid">
            <div class="service-card">
                <h3>{category}・専門施工</h3>
                <p>長年の実績と確かな技術で、お客様のご要望にお応えする高品質な施工を提供いたします。</p>
            </div>
            <div class="service-card">
                <h3>定期メンテナンス・修繕</h3>
                <p>施工後のアフターフォローも万全です。定期的な点検や小さな修繕も迅速に対応します。</p>
            </div>
            <div class="service-card">
                <h3>無料お見積り・現地調査</h3>
                <p>まずは現場の状況をしっかり確認させていただき、最適なプランと明朗な見積もりをご提示します。</p>
            </div>
        </div>
    </section>

    <section class="contact" id="contact">
        <h2>まずはお気軽にご相談ください</h2>
        <p>些細なご相談からでも喜んで対応いたします。<br>ご相談・お見積りは無料です。</p>
        <a href="tel:{phone}" class="tel-large">📞 {phone}</a>
        <p>【営業時間】 9:00 〜 18:00（日曜定休）</p>
        
        <div class="map-container">
            <iframe src="https://maps.google.com/maps?q={encoded_address}&t=&z=15&ie=UTF8&iwloc=&output=embed" width="100%" height="300" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
        </div>
        <a href="{map_url}" target="_blank" class="map-btn">📍 Googleマップで見る</a>
    </section>

    <footer>
        <p>&copy; 2026 {company_name} All Rights Reserved.</p>
        <p>{address}</p>
        <div class="disclaimer">
            ※免責事項：このページはインターネット上の公開情報に基づいて自動生成された「応援デモページ」であり、{company_name}様の公式Webサイトではありません。内容の修正・削除をご希望の事業者様、またはこのデザインでの公式Webサイト制作をご希望の事業者様はガンバWebまでご連絡ください。
        </div>
    </footer>

    <script>
        function toggleMenu() {{
            document.getElementById('navLinks').classList.toggle('active');
        }}
    </script>
</body>
</html>"""

def extract_city(address):
    # 埼玉県〇〇市を取り出す
    match = re.search(r'(埼玉県)(.+?[市区町村])', address)
    if match:
        return match.group(2)
    return "埼玉県"

count = 0
sitemap_urls = []
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company_name = row.get('業者名', '業者名未定').strip()
        phone = row.get('電話番号', '').strip()
        address = row.get('住所', '').strip()
        category = row.get('業種', '建設・工事').strip()
        map_url = row.get('GoogleマップURL', '').strip()
        
        city = extract_city(address)
        encoded_address = urllib.parse.quote(address)
        
        if not phone:
            continue
            
        html_content = HTML_TEMPLATE.format(
            company_name=company_name,
            phone=phone,
            address=address,
            category=category,
            city=city,
            encoded_address=encoded_address,
            map_url=map_url
        )
        
        # SMS用のURLをすっきりさせるため、ファイル名は電話番号のみにする
        safe_phone = phone.replace('-', '')
        safe_filename = f"{safe_phone}.html"
        sitemap_urls.append(f"https://ganbaweb.com/{safe_phone}")
        filepath = os.path.join(output_dir, safe_filename)
        
        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(html_content)
        count += 1

sitemap_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n"
sitemap_content += "</urlset>"

with open(os.path.join(output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

with open(os.path.join(output_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write("User-agent: *\nAllow: /\nSitemap: https://ganbaweb.com/sitemap.xml\n")

print(f"✅ 成功: {output_dir} フォルダに {count} 件のデモサイトとSEO用ファイル（sitemap.xml, robots.txt）を自動生成しました！")
