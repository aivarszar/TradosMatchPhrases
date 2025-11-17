#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate final HTML report with phrase highlighting and corrections
"""
import json
import re
from typing import List, Tuple

# Color palette for phrase highlighting
COLORS = [
    '#FFB6C1', '#87CEEB', '#98FB98', '#FFD700', '#DDA0DD',
    '#F0E68C', '#FFE4B5', '#B0E0E6', '#FFDAB9', '#E0BBE4',
    '#C7CEEA', '#FFDFD3', '#B4F8C8', '#FBE7C6', '#A0CED9',
    '#FAD7A0', '#D5F4E6', '#F8B9D4', '#AED6F1', '#F9E79F'
]

def extract_key_phrases(text: str) -> List[str]:
    """Extract key phrases for highlighting"""
    phrases = []

    # 1. Numbers with units
    numbers = re.findall(r'\d+[.,:/]?\d*\s*(?:mm|cm|m|s|ms|Hz|%|mAs|kV|mGy|Sec)?', text)
    phrases.extend(numbers)

    # 2. Parenthetical content: Term (Translation)
    parenthetical = re.findall(r'([A-Z][A-Za-z\s&-]+?)\s*\(([^)]+)\)', text)
    for eng, lv in parenthetical:
        phrases.append(eng.strip())

    # 3. Capitalized terms (likely UI elements or modes)
    cap_terms = re.findall(r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3})\b', text)
    phrases.extend([t for t in cap_terms if len(t) > 3])

    # 4. Technical terms in ALL CAPS
    all_caps = re.findall(r'\b[A-Z]{2,}\b', text)
    phrases.extend(all_caps)

    # Remove duplicates while preserving order
    seen = set()
    unique_phrases = []
    for p in phrases:
        if p and p not in seen and len(p.strip()) > 1:
            seen.add(p)
            unique_phrases.append(p)

    return unique_phrases

def highlight_phrases(source: str, target: str) -> Tuple[str, str]:
    """Highlight matching phrases in source and target"""
    # Extract phrases from source
    source_phrases = extract_key_phrases(source)

    # Create highlighted versions
    source_highlighted = source
    target_highlighted = target

    # Track which phrases are found in target
    phrase_colors = {}
    color_idx = 0

    for phrase in source_phrases:
        # Check if phrase or its translation is in target
        # This is a simplified check - in reality, we'd need proper translation mapping
        if phrase in target or re.search(re.escape(phrase), target, re.IGNORECASE):
            color = COLORS[color_idx % len(COLORS)]
            phrase_colors[phrase] = color
            color_idx += 1

            # Highlight in source
            source_highlighted = re.sub(
                rf'\b({re.escape(phrase)})\b',
                rf'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px;">\1</span>',
                source_highlighted,
                flags=re.IGNORECASE
            )

            # Highlight in target (if exact match exists)
            if phrase in target:
                target_highlighted = re.sub(
                    rf'\b({re.escape(phrase)})\b',
                    rf'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px;">\1</span>',
                    target_highlighted,
                    flags=re.IGNORECASE
                )

    return source_highlighted, target_highlighted

def generate_html_report():
    """Generate comprehensive HTML report"""

    # Load corrections
    with open('translation_corrections.json', 'r', encoding='utf-8') as f:
        corrections = json.load(f)

    # Generate HTML for each correction
    corrections_html = ""

    for i, corr in enumerate(corrections, 1):
        severity_colors = {
            'HIGH': '#e74c3c',
            'MEDIUM': '#f39c12',
            'LOW': '#3498db'
        }
        severity_color = severity_colors.get(corr['severity'], '#95a5a6')

        severity_labels = {
            'HIGH': 'Augsta prioritāte',
            'MEDIUM': 'Vidēja prioritāte',
            'LOW': 'Zema prioritāte'
        }
        severity_label = severity_labels.get(corr['severity'], corr['severity'])

        # Highlight phrases
        source_hl, original_target_hl = highlight_phrases(
            corr['original_source'],
            corr['original_target']
        )
        _, corrected_target_hl = highlight_phrases(
            corr['original_source'],
            corr['corrected_target']
        )

        corrections_html += f'''
        <div class="correction-item" style="border-left: 4px solid {severity_color};">
            <div class="correction-header">
                <div class="correction-number">Labojums #{i}</div>
                <div class="segment-badge">Segments #{corr['segment_id']}</div>
                <div class="severity-badge" style="background-color: {severity_color}20; color: {severity_color};">
                    {severity_label}
                </div>
                <div class="issue-type">{corr['issue_type']}</div>
            </div>

            <div class="text-block source-block">
                <div class="block-label">📄 Avotteksts (EN)</div>
                <div class="block-content">{source_hl}</div>
            </div>

            <div class="text-block original-block">
                <div class="block-label">❌ Oriģinālais tulkojums (LV)</div>
                <div class="block-content">{original_target_hl}</div>
            </div>

            <div class="text-block corrected-block">
                <div class="block-label">✅ Labotais tulkojums (LV)</div>
                <div class="block-content corrected">{corrected_target_hl}</div>
            </div>

            <div class="explanation-block">
                <div class="block-label">💡 Paskaidrojums</div>
                <div class="block-content">{corr['explanation']}</div>
            </div>
        </div>
        '''

    # Generate full HTML document
    html_content = f'''
<!DOCTYPE html>
<html lang="lv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tulkojuma kvalitātes pārbaude - Galīgais ziņojums</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .header .subtitle {{
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 20px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 25px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}

        .stat-card .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }}

        .stat-card .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
            display: block;
            margin-top: 5px;
        }}

        .corrections-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .section-title {{
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}

        .correction-item {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .correction-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .correction-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .correction-number {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
        }}

        .segment-badge {{
            background: #3498db;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}

        .severity-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}

        .issue-type {{
            background: #ecf0f1;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #7f8c8d;
            font-family: 'Courier New', monospace;
        }}

        .text-block {{
            margin-bottom: 15px;
            background: white;
            border-radius: 8px;
            padding: 15px;
        }}

        .block-label {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #2c3e50;
        }}

        .block-content {{
            line-height: 1.8;
            font-size: 1.05em;
            color: #34495e;
        }}

        .source-block {{
            border-left: 4px solid #3498db;
        }}

        .original-block {{
            border-left: 4px solid #e74c3c;
        }}

        .corrected-block {{
            border-left: 4px solid #2ecc71;
        }}

        .corrected {{
            font-weight: 500;
            color: #27ae60;
        }}

        .explanation-block {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }}

        .explanation-block .block-label {{
            color: #856404;
        }}

        .explanation-block .block-content {{
            color: #856404;
        }}

        .summary-box {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-top: 30px;
        }}

        .summary-box h3 {{
            font-size: 1.5em;
            margin-bottom: 15px;
        }}

        .summary-box ul {{
            list-style: none;
            padding-left: 20px;
        }}

        .summary-box li {{
            margin-bottom: 10px;
            position: relative;
            padding-left: 25px;
        }}

        .summary-box li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            margin-top: 30px;
        }}

        @media print {{
            body {{
                background: white;
            }}

            .header, .corrections-container {{
                box-shadow: none;
            }}

            .correction-item {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Tulkojuma Kvalitātes Pārbaude</h1>
            <div class="subtitle">Translation Quality Review - LB17-11 viss tulkojums</div>
            <div class="subtitle" style="font-size: 0.95em; color: #95a5a6; margin-top: 5px;">
                Dokuments: UM_6789320-1EN_r1_for_RevolutionVibe_Apex5.0-1107
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">2662</span>
                    <span class="stat-label">Kopā segmenti</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">30</span>
                    <span class="stat-label">Potenciāli problemātiski</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">8</span>
                    <span class="stat-label">Veikti labojumi</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">99.7%</span>
                    <span class="stat-label">Kvalitātes līmenis</span>
                </div>
            </div>
        </div>

        <div class="corrections-container">
            <h2 class="section-title">Detalizēti Labojumi</h2>

            {corrections_html}

            <div class="summary-box">
                <h3>📊 Kopsavilkums</h3>
                <ul>
                    <li><strong>Kopā analizēti:</strong> 2662 tulkojuma segmenti</li>
                    <li><strong>Identificētas problēmas:</strong> 30 segmentos (1.1%)</li>
                    <li><strong>Veikti labojumi:</strong> 8 segmentos (0.3%)</li>
                    <li><strong>False positives:</strong> 22 segmenti (automātiskās analīzes brīdinājumi, bet tulkojums pareizs)</li>
                </ul>

                <h3 style="margin-top: 25px;">🎯 Galvenās problēmu kategorijas</h3>
                <ul>
                    <li><strong>UI elementi bez tulkojuma:</strong> 5 segmenti - režīmu un pogu nosaukumi nav formatēti kā EN (Tulkojums)</li>
                    <li><strong>Skaitļu/faktu neatbilstība:</strong> 2 segmenti - programmatūras versija un skaitļa formāts</li>
                    <li><strong>Konsekven ces jautājumi:</strong> 1 segments - terminu lietojuma konsekvence</li>
                </ul>

                <h3 style="margin-top: 25px;">✅ Vispārējais novērtējums</h3>
                <p style="margin-top: 10px; line-height: 1.8;">
                    Tulkojuma kvalitāte kopumā ir <strong>ļoti augsta (99.7%)</strong>. Lielākā daļa segmentu ir iztulkoti precīzi,
                    ievērojot terminoloģijas konsekvenci un tehniskā dokumenta prasības. Identificētās problēmas
                    ir galvenokārt saistītas ar UI elementu formatēšanu, kur angļu nosaukumi nav papildināti ar
                    latviešu tulkojumiem iekavās. Šie labojumi uzlabos dokumenta lietojamību un atbilstību
                    lokalizācijas standartiem.
                </p>
            </div>
        </div>

        <div class="footer">
            <p>Ģenerēts: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px;">Translation Quality Review Tool v1.0</p>
        </div>
    </div>
</body>
</html>
    '''

    # Save HTML report
    with open('tulkojuma_labojumi_final.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ Galīgais HTML ziņojums izveidots: tulkojuma_labojumi_final.html")
    print(f"   Faila atrašanās vieta: /home/user/TradosMatchPhrases/tulkojuma_labojumi_final.html")

def main():
    generate_html_report()

if __name__ == "__main__":
    main()
