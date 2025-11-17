#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detailed Translation Quality Analysis
Identifies translation errors, missing phrases, UI element formatting issues
"""
import json
import re
from collections import defaultdict
from typing import List, Dict, Tuple

# Color palette for phrase highlighting
COLORS = [
    '#FFB6C1', '#FFD700', '#98FB98', '#87CEEB', '#DDA0DD',
    '#F0E68C', '#FFE4B5', '#B0E0E6', '#FFB6E1', '#D8BFD8',
    '#FFDAB9', '#E0BBE4', '#C7CEEA', '#FFDFD3', '#B4F8C8'
]

class TranslationAnalyzer:
    def __init__(self, segments):
        self.segments = segments
        self.issues = []
        self.term_usage = defaultdict(lambda: defaultdict(set))

    def analyze_segment(self, seg):
        """Analyze a single segment for issues"""
        segment_issues = []

        source = seg['source']
        target = seg['target']
        seg_id = seg['id']

        # 1. Check for UI element formatting
        ui_issues = self.check_ui_elements(source, target, seg_id)
        segment_issues.extend(ui_issues)

        # 2. Check for untranslated phrases
        untranslated = self.check_untranslated(source, target, seg_id)
        segment_issues.extend(untranslated)

        # 3. Check for missing content
        missing = self.check_missing_content(source, target, seg_id)
        segment_issues.extend(missing)

        # 4. Collect term usage for consistency check
        self.collect_terms(source, target, seg_id)

        return segment_issues

    def check_ui_elements(self, source, target, seg_id):
        """Check if UI elements are properly formatted as EN (Tulkojums)"""
        issues = []

        # Common UI elements patterns
        ui_patterns = [
            r'\b(button|mode|menu|tab|page|field|option|setting|panel|window|dialog|checkbox|radio)\b',
            r'\b(Full|Plus|Standard|Advanced|Normal|High|Low)\s+(mode|Mode)',
            r'(Series|Scan|Recon|Image)\s+(Text|Mode|Type|Page)',
        ]

        for pattern in ui_patterns:
            matches = re.finditer(pattern, source, re.IGNORECASE)
            for match in matches:
                ui_element = match.group(0)

                # Check if it's properly formatted in target
                # Should be: UI_Element (Tulkojums) or fully translated with object type first

                # Look for English text in parentheses
                if ui_element in target and not re.search(rf'{re.escape(ui_element)}\s*\([^)]+\)', target):
                    # UI element exists but not in (EN) format
                    if not self.is_properly_translated_ui(ui_element, target):
                        issues.append({
                            'type': 'UI_FORMAT',
                            'segment_id': seg_id,
                            'element': ui_element,
                            'source': source,
                            'target': target,
                            'message': f'UI elements "{ui_element}" nav pareizi formatēts kā EN (Tulkojums) vai objekta tips nav pirms nosaukuma'
                        })

        return issues

    def is_properly_translated_ui(self, ui_element, target):
        """Check if UI element is properly translated"""
        # Check if the element appears with Latvian translation in proper format
        # This is a simplified check
        latvian_ui_terms = {
            'button': ['poga', 'pogas'],
            'mode': ['režīms', 'režīmu', 'režīmā'],
            'menu': ['izvēlne', 'izvēlni'],
            'tab': ['cilne', 'cilni'],
            'page': ['lapa', 'lapā', 'lapu'],
            'field': ['lauks', 'lauku', 'laukā'],
            'option': ['opcija', 'opciju'],
            'setting': ['iestatījums', 'iestatījumu'],
        }

        for eng, lv_variants in latvian_ui_terms.items():
            if eng.lower() in ui_element.lower():
                for lv in lv_variants:
                    if lv in target.lower():
                        return True
        return False

    def check_untranslated(self, source, target, seg_id):
        """Check for potentially untranslated English phrases"""
        issues = []

        # Look for English words in target (excluding technical terms)
        # Common English words that shouldn't appear in Latvian text
        common_words = [
            r'\bthe\b', r'\bto\b', r'\band\b', r'\bor\b', r'\bof\b',
            r'\bin\b', r'\bon\b', r'\bat\b', r'\bfor\b', r'\bwith\b',
            r'\bis\b', r'\bare\b', r'\bcan\b', r'\bmay\b', r'\bwill\b',
            r'\bshould\b', r'\busing\b', r'\bselect\b', r'\bclick\b'
        ]

        for pattern in common_words:
            if re.search(pattern, target, re.IGNORECASE):
                issues.append({
                    'type': 'UNTRANSLATED',
                    'segment_id': seg_id,
                    'source': source,
                    'target': target,
                    'message': f'Tulkojumā atrasti neiztulkoti angļu vārdi: {pattern}'
                })
                break

        return issues

    def check_missing_content(self, source, target, seg_id):
        """Check if target might be missing some source content"""
        issues = []

        # Count numbers, they should match
        source_numbers = re.findall(r'\d+\.?\d*', source)
        target_numbers = re.findall(r'\d+\.?\d*', target)

        # Convert comma decimals to dot decimals for comparison
        target_numbers_normalized = [n.replace(',', '.') for n in target_numbers]

        if len(source_numbers) != len(target_numbers_normalized):
            issues.append({
                'type': 'MISSING_NUMBERS',
                'segment_id': seg_id,
                'source': source,
                'target': target,
                'message': f'Skaitļu skaits nesakrīt: avotā {len(source_numbers)}, tulkojumā {len(target_numbers)}'
            })

        # Check if target is significantly shorter (might indicate truncation)
        if len(target) < len(source) * 0.6 and len(source) > 50:
            issues.append({
                'type': 'POTENTIALLY_TRUNCATED',
                'segment_id': seg_id,
                'source': source,
                'target': target,
                'message': f'Tulkojums var būt saīsināts (avots: {len(source)} rakstzīmes, tulkojums: {len(target)} rakstzīmes)'
            })

        return issues

    def collect_terms(self, source, target, seg_id):
        """Collect term usage for consistency analysis"""
        # Common terms to track
        terms = {
            'reconstruction': r'\breconstruction\b',
            'mode': r'\bmode\b',
            'scan': r'\bscan\b',
            'image': r'\bimage\b',
            'series': r'\bseries\b',
            'resolution': r'\bresolution\b',
            'slice': r'\bslice\b',
            'thickness': r'\bthickness\b',
        }

        for term_name, pattern in terms.items():
            if re.search(pattern, source, re.IGNORECASE):
                # Extract how it's translated
                self.term_usage[term_name]['source'].add(seg_id)

                # Try to find corresponding Latvian term
                latvian_patterns = {
                    'reconstruction': r'\b(rekonstrukcij\w+)\b',
                    'mode': r'\b(režīm\w+)\b',
                    'scan': r'\b(skenēšan\w+|izmeklēj\w+)\b',
                    'image': r'\b(attēl\w+)\b',
                    'series': r'\b(sērij\w+)\b',
                    'resolution': r'\b(izšķirtspēj\w+)\b',
                    'slice': r'\b(slāņ\w+|griezum\w+)\b',
                    'thickness': r'\b(biezum\w+)\b',
                }

                if term_name in latvian_patterns:
                    lv_matches = re.findall(latvian_patterns[term_name], target, re.IGNORECASE)
                    for match in lv_matches:
                        self.term_usage[term_name][match.lower()].add(seg_id)

    def check_term_consistency(self):
        """Check if terms are translated consistently"""
        issues = []

        for term, translations in self.term_usage.items():
            latvian_translations = {k: v for k, v in translations.items() if k != 'source'}

            if len(latvian_translations) > 1:
                # Multiple translations for the same term
                translation_list = [(trans, len(segs)) for trans, segs in latvian_translations.items()]
                translation_list.sort(key=lambda x: x[1], reverse=True)

                if len(translation_list) > 1 and translation_list[1][1] > 2:  # More than 2 occurrences of alternate
                    issues.append({
                        'type': 'INCONSISTENT_TERM',
                        'term': term,
                        'translations': translation_list,
                        'message': f'Termins "{term}" tulkots nekonsekventi: {translation_list}'
                    })

        return issues

    def analyze_all(self):
        """Analyze all segments"""
        print("Analyzing translation quality...")

        for seg in self.segments:
            seg_issues = self.analyze_segment(seg)
            if seg_issues:
                self.issues.append({
                    'segment': seg,
                    'issues': seg_issues
                })

        # Check term consistency
        term_issues = self.check_term_consistency()

        print(f"\nFound {len(self.issues)} segments with issues")
        print(f"Found {len(term_issues)} term consistency issues")

        return self.issues, term_issues

def main():
    # Load segments
    with open('translation_segments.json', 'r', encoding='utf-8') as f:
        segments = json.load(f)

    analyzer = TranslationAnalyzer(segments)
    segment_issues, term_issues = analyzer.analyze_all()

    # Save results
    results = {
        'segment_issues': segment_issues,
        'term_issues': term_issues,
        'total_segments': len(segments),
        'problematic_segments': len(segment_issues)
    }

    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to analysis_results.json")

    # Show summary
    issue_types = defaultdict(int)
    for seg_issue in segment_issues:
        for issue in seg_issue['issues']:
            issue_types[issue['type']] += 1

    print("\n=== Issue Summary ===")
    for issue_type, count in sorted(issue_types.items()):
        print(f"{issue_type}: {count}")

if __name__ == "__main__":
    main()
