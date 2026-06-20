import csv
import os

csv_file = 'saitama6_result.csv'
output_file = 'ganbaweb/09074074605.html'

html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ガンバWeb 営業用ダッシュボード（秘密）</title>
<style>
body { font-family: sans-serif; padding: 20px; background: #f0f2f5; }
h1 { color: #333; font-size: 20px; text-align: center; margin-bottom: 20px; }
.list-group { display: flex; flex-direction: column; gap: 15px; max-width: 600px; margin: 0 auto; }
.list-item { background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.company { font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 5px; }
.phone { font-size: 14px; color: #7f8c8d; margin-bottom: 10px; }
.link-btn { display: block; text-align: center; background: #3498db; color: #fff; text-decoration: none; padding: 10px; border-radius: 5px; font-weight: bold; }
.mobile-badge { display: inline-block; background: #e74c3c; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-left: 10px; }
</style>
</head>
<body>
<h1>🎯 営業用ターゲット一覧 (埼玉56件)</h1>
<div class="list-group">
"""

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company_name = row.get('業者名', '名称不明').strip()
        phone = row.get('電話番号', '').strip()
        if not phone:
            continue
            
        safe_phone = phone.replace('-', '')
        url = f"https://ganbaweb.com/{safe_phone}"
        
        # 090, 080, 070 には SMSバッジをつける
        badge = ""
        if safe_phone.startswith("090") or safe_phone.startswith("080") or safe_phone.startswith("070"):
            badge = "<span class='mobile-badge'>📱 SMS送信可</span>"
            
        html_content += f"""
        <div class="list-item">
            <div class="company">{company_name} {badge}</div>
            <div class="phone">📞 {phone}</div>
            <a href="{url}" class="link-btn" target="_blank">デモサイトを開く</a>
        </div>
        """

html_content += """
</div>
</body>
</html>
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Dashboard generated at {output_file}")
