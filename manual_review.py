#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual Review Tool - generates HTML with phrase highlighting for detailed review
"""
import json
import re
from typing import List, Tuple, Dict

# Color palette for phrase matching
COLORS = [
    '#FFB6C1', '#87CEEB', '#98FB98', '#FFD700', '#DDA0DD',
    '#F0E68C', '#FFE4B5', '#B0E0E6', '#FFDAB9', '#E0BBE4',
    '#C7CEEA', '#FFDFD3', '#B4F8C8', '#FBE7C6', '#A0CED9'
]

class PhraseExtractor:
    """Extract meaningful phrases from sentences"""

    @staticmethod
    def extract_phrases(text: str) -> List[str]:
        """Extract phrases from text"""
        phrases = []

        # 1. Extract parenthetical content: EN (LV)
        parenthetical = re.findall(r'([^(]+)\s*\(([^)]+)\)', text)
        for eng, lv in parenthetical:
            phrases.append(eng.strip())
            phrases.append(lv.strip())

        # 2. Extract key technical terms and UI elements
        # Capital words/phrases
        capital_phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        phrases.extend(capital_phrases)

        # 3. Extract numbers with units
        numbers_with_units = re.findall(r'\d+[.,]?\d*\s*(?:mm|cm|s|ms|Hz|%|mAs|kV|:1)?', text)
        phrases.extend(numbers_with_units)

        # 4. Extract comma-separated lists
        # lists = re.findall(r'\b\w+\s*,\s*\w+\s*,\s*\w+', text)
        # phrases.extend(lists)

        return phrases

class ManualReviewGenerator:
    """Generate HTML for manual review with phrase highlighting"""

    def __init__(self, segments):
        self.segments = segments

    def identify_issues_simple(self, seg) -> List[Dict]:
        """Simple heuristic issue identification for prioritization"""
        issues = []
        source = seg['source']
        target = seg['target']

        # 1. Check if target is much shorter
        if len(target) < len(source) * 0.7 and len(source) > 80:
            issues.append({'type': 'SHORT', 'severity': 'high'})

        # 2. Check for English words that look like they should be translated
        # Only check for common English words that shouldn't be in parentheses
        common_english = ['button', 'click', 'select', 'press', 'enter', 'type', 'menu', 'field']
        for word in common_english:
            # Check if word appears standalone (not in parentheses)
            if re.search(rf'\b{word}\b(?![^(]*\))', target, re.IGNORECASE):
                issues.append({'type': 'ENGLISH_WORD', 'word': word, 'severity': 'medium'})

        # 3. Check numbers
        source_nums = re.findall(r'\d+[.,]?\d*', source)
        target_nums = re.findall(r'\d+[.,]?\d*', target)
        if len(source_nums) > 0 and len(source_nums) != len(target_nums):
            issues.append({'type': 'NUMBER_MISMATCH', 'severity': 'medium'})

        # 4. Check if English term appears without (LV) translation
        # Pattern: capital English word not followed by (...)
        english_terms = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b(?!\s*\()', target)
        # Filter out likely Latvian words and very short words
        english_terms = [t for t in english_terms if len(t) > 5 and
                         not any(lv in t.lower() for lv in ['režīms', 'lapa', 'poga', 'izvēlne'])]
        if english_terms:
            issues.append({'type': 'TERM_NO_TRANSLATION', 'terms': english_terms, 'severity': 'low'})

        return issues

    def split_into_phrases(self, text: str) -> List[Tuple[str, int]]:
        """Split text into phrases for matching"""
        # Split by common delimiters but keep them
        parts = []
        current = ""
        delimiters = [',', '.', ';', ':', '(', ')']

        for char in text:
            if char in delimiters:
                if current.strip():
                    parts.append((current.strip(), 0))  # phrase, color_idx
                parts.append((char, -1))  # delimiter, no color
                current = ""
            else:
                current += char

        if current.strip():
            parts.append((current.strip(), 0))

        return parts

    def highlight_phrase(self, phrase: str, color_idx: int) -> str:
        """Wrap phrase in HTML span with color"""
        if color_idx < 0:  # delimiter
            return phrase

        color = COLORS[color_idx % len(COLORS)]
        return f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px; margin: 1px;">{phrase}</span>'

    def generate_segment_html(self, seg, issues) -> str:
        """Generate HTML for a single segment"""
        seg_id = seg['id']
        source = seg['source']
        target = seg['target']

        # Determine severity
        severity_class = 'low'
        if issues:
            severities = [i.get('severity', 'low') for i in issues]
            if 'high' in severities:
                severity_class = 'high'
            elif 'medium' in severities:
                severity_class = 'medium'

        # Generate issue badges
        issue_badges = ""
        if issues:
            for issue in issues:
                issue_type = issue['type']
                issue_badges += f'<span class="badge badge-{issue["severity"]}">{issue_type}</span> '

        html = f'''
        <div class="segment {severity_class}" id="seg-{seg_id}">
            <div class="segment-header">
                <span class="segment-id">Segment #{seg_id}</span>
                {issue_badges}
            </div>
            <div class="segment-content">
                <div class="source-row">
                    <div class="label">EN:</div>
                    <div class="text">{source}</div>
                </div>
                <div class="target-row">
                    <div class="label">LV:</div>
                    <div class="text">{target}</div>
                </div>
            </div>
            <div class="segment-review">
                <label>Labojums:</label>
                <textarea class="correction" placeholder="Ievadiet laboto tulkojumu..."></textarea>
                <label>Paskaidrojums:</label>
                <textarea class="explanation" placeholder="Kļūdas apraksts un paskaidrojums..."></textarea>
            </div>
        </div>
        '''
        return html

    def generate_html_report(self, output_file='translation_review.html', limit=None):
        """Generate full HTML report"""
        print("Generating HTML review document...")

        # Identify segments with potential issues
        segments_with_issues = []
        segments_clean = []

        for seg in self.segments:
            issues = self.identify_issues_simple(seg)
            if issues:
                segments_with_issues.append((seg, issues))
            else:
                segments_clean.append(seg)

        print(f"Segments with potential issues: {len(segments_with_issues)}")
        print(f"Clean segments: {len(segments_clean)}")

        # Generate HTML for segments with issues
        segments_html = ""

        # Prioritize by severity
        segments_with_issues.sort(key=lambda x: (
            -max([{'high': 3, 'medium': 2, 'low': 1}.get(i['severity'], 0) for i in x[1]]),
            x[0]['id']
        ))

        # Limit if specified
        if limit:
            segments_with_issues = segments_with_issues[:limit]

        for seg, issues in segments_with_issues:
            segments_html += self.generate_segment_html(seg, issues)

        # Generate CSS and HTML structure
        html_template = f'''
<!DOCTYPE html>
<html lang="lv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tulkojuma pārbaude - Translation Review</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            margin: 0 0 10px 0;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}

        .stat {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 5px;
        }}

        .segment {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #ddd;
        }}

        .segment.high {{
            border-left-color: #e74c3c;
        }}

        .segment.medium {{
            border-left-color: #f39c12;
        }}

        .segment.low {{
            border-left-color: #3498db;
        }}

        .segment-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}

        .segment-id {{
            font-weight: bold;
            color: #666;
        }}

        .badge {{
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: 500;
        }}

        .badge-high {{
            background: #fee;
            color: #e74c3c;
        }}

        .badge-medium {{
            background: #fef5e7;
            color: #f39c12;
        }}

        .badge-low {{
            background: #ebf5fb;
            color: #3498db;
        }}

        .segment-content {{
            margin-bottom: 15px;
        }}

        .source-row, .target-row {{
            display: grid;
            grid-template-columns: 40px 1fr;
            gap: 10px;
            margin-bottom: 10px;
        }}

        .label {{
            font-weight: bold;
            color: #666;
        }}

        .text {{
            line-height: 1.6;
        }}

        .source-row .text {{
            color: #2c3e50;
        }}

        .target-row .text {{
            color: #16a085;
        }}

        .segment-review {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }}

        .segment-review label {{
            display: block;
            font-weight: bold;
            margin: 10px 0 5px 0;
            color: #555;
        }}

        .segment-review textarea {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            min-height: 60px;
        }}

        .correction {{
            background: #fffef5;
        }}

        .explanation {{
            background: #f0f8ff;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            margin-top: 40px;
        }}

        .export-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }}

        .export-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Tulkojuma kvalitātes pārbaude</h1>
        <p>Translation Quality Review - LB17-11</p>
        <div class="stats">
            <div class="stat">
                <strong>Kopā segmenti:</strong> {len(self.segments)}
            </div>
            <div class="stat">
                <strong>Ar problēmām:</strong> {len(segments_with_issues)}
            </div>
            <div class="stat">
                <strong>Tīri:</strong> {len(segments_clean)}
            </div>
        </div>
    </div>

    <div class="segments-container">
        {segments_html}
    </div>

    <div class="footer">
        Generated by Translation Review Tool | {len(segments_with_issues)} segments reviewed
    </div>

    <button class="export-btn" onclick="exportCorrections()">💾 Eksportēt labojumus</button>

    <script>
        function exportCorrections() {{
            const segments = document.querySelectorAll('.segment');
            const corrections = [];

            segments.forEach(seg => {{
                const segId = seg.id.replace('seg-', '');
                const correction = seg.querySelector('.correction').value;
                const explanation = seg.querySelector('.explanation').value;

                if (correction.trim() || explanation.trim()) {{
                    corrections.push({{
                        id: segId,
                        correction: correction,
                        explanation: explanation,
                        original_source: seg.querySelector('.source-row .text').textContent,
                        original_target: seg.querySelector('.target-row .text').textContent
                    }});
                }}
            }});

            // Download as JSON
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(corrections, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", "translation_corrections.json");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();

            alert('Eksportēti ' + corrections.length + ' labojumi!');
        }}

        // Auto-save to localStorage
        document.querySelectorAll('textarea').forEach(textarea => {{
            const segId = textarea.closest('.segment').id;
            const field = textarea.classList.contains('correction') ? 'correction' : 'explanation';

            // Load saved value
            const saved = localStorage.getItem(`${{segId}}-${{field}}`);
            if (saved) {{
                textarea.value = saved;
            }}

            // Save on change
            textarea.addEventListener('input', () => {{
                localStorage.setItem(`${{segId}}-${{field}}`, textarea.value);
            }});
        }});
    </script>
</body>
</html>
        '''

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)

        print(f"HTML report generated: {output_file}")
        print(f"Open in browser to review: file://{output_file}")

def main():
    with open('translation_segments.json', 'r', encoding='utf-8') as f:
        segments = json.load(f)

    generator = ManualReviewGenerator(segments)
    generator.generate_html_report('translation_review.html')

if __name__ == "__main__":
    main()
