#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refined Translation Quality Analysis with Manual Review Focus
"""
import json
import re
from collections import defaultdict

class RefinedAnalyzer:
    def __init__(self, segments):
        self.segments = segments
        self.issues = []

    def check_proper_english_in_parentheses(self, text):
        """Check if English text in parentheses follows EN (LV) format"""
        # Pattern: English term (Latvian translation)
        # This is CORRECT format, should not be flagged
        pattern = r'([A-Z][A-Za-z\s&]+)\s*\(([^)]+)\)'
        return re.findall(pattern, text)

    def analyze_segment_detailed(self, seg):
        """Detailed analysis of a single segment"""
        issues = []
        source = seg['source']
        target = seg['target']
        seg_id = seg['id']

        # 1. Check if English text appears WITHOUT translation in parentheses
        # Find English words/phrases in target that are NOT in (EN) format
        english_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        english_in_target = re.findall(english_pattern, target)

        # Filter out those that are properly in (EN) format
        proper_format = self.check_proper_english_in_parentheses(target)
        proper_english = {eng for eng, lv in proper_format}

        # Check for standalone English phrases
        problematic_english = []
        for eng_phrase in english_in_target:
            # Skip technical terms (all caps, or known terms)
            if eng_phrase.isupper() or len(eng_phrase) < 4:
                continue

            # Check if it's in proper (EN) format
            if eng_phrase not in proper_english:
                # Check if it's followed by parentheses
                if not re.search(rf'{re.escape(eng_phrase)}\s*\([^)]+\)', target):
                    problematic_english.append(eng_phrase)

        if problematic_english:
            issues.append({
                'type': 'MISSING_TRANSLATION_FORMAT',
                'elements': problematic_english,
                'message': f'Angļu frāzes nav formatētas kā EN (Tulkojums): {", ".join(problematic_english)}'
            })

        # 2. Check for common untranslated phrases (not in proper format)
        common_untranslated_patterns = [
            (r'\b(select|click|press|enter|type)\b', 'Nederīgi angļu verbi'),
            (r'\b(button|field|menu|panel)\b(?!\s*\()', 'UI elementi bez tulkojuma'),
        ]

        for pattern, desc in common_untranslated_patterns:
            # Make sure they're not in proper (EN) format
            matches = re.finditer(pattern, target, re.IGNORECASE)
            for match in matches:
                word = match.group(0)
                # Check context - is it in (EN) format?
                context_start = max(0, match.start() - 20)
                context_end = min(len(target), match.end() + 20)
                context = target[context_start:context_end]

                if not re.search(r'\([^)]*' + re.escape(word) + r'[^)]*\)', context, re.IGNORECASE):
                    issues.append({
                        'type': 'UNTRANSLATED_WORD',
                        'word': word,
                        'context': context,
                        'message': f'{desc}: "{word}"'
                    })
                    break  # Only report once per segment

        # 3. Check numbers
        source_numbers = re.findall(r'\d+[.,]?\d*', source)
        target_numbers = re.findall(r'\d+[.,]?\d*', target)

        # Normalize for comparison
        source_normalized = [n.replace(',', '.') for n in source_numbers]
        target_normalized = [n.replace(',', '.') for n in target_numbers]

        if len(source_normalized) > 0 and len(source_normalized) != len(target_normalized):
            issues.append({
                'type': 'NUMBER_MISMATCH',
                'source_numbers': source_numbers,
                'target_numbers': target_numbers,
                'message': f'Skaitļu skaits nesakrīt: avotā {len(source_numbers)}, tulkojumā {len(target_numbers)}'
            })

        # 4. Check for truncation (target significantly shorter)
        if len(target) < len(source) * 0.7 and len(source) > 100:
            issues.append({
                'type': 'POSSIBLE_TRUNCATION',
                'source_len': len(source),
                'target_len': len(target),
                'message': f'Iespējama saīsināšana: avots {len(source)} rakstzīmes, tulkojums {len(target)} rakstzīmes'
            })

        # 5. Check for UI element format: should be "objekta_tips EN (LV)"
        # Example: "poga Start (Sākt)" not "Start (Sākt) poga"
        ui_patterns = {
            'button': r'poga',
            'mode': r'režīms',
            'field': r'lauks',
            'menu': r'izvēlne',
            'panel': r'panelis',
            'window': r'logs',
            'tab': r'cilne',
            'page': r'lapa',
            'option': r'opcija',
        }

        # Check if English UI term appears with translation but wrong order
        for eng_ui, lv_ui in ui_patterns.items():
            if eng_ui in source.lower():
                # Check if Latvian UI term appears AFTER the English term
                # Pattern: EN_Term (LV translation) lv_ui_type - WRONG
                # Should be: lv_ui_type EN_Term (LV translation) - CORRECT
                wrong_pattern = rf'([A-Z][a-z]+)\s*\([^)]+\)\s+{lv_ui}'
                if re.search(wrong_pattern, target, re.IGNORECASE):
                    issues.append({
                        'type': 'UI_WRONG_ORDER',
                        'ui_type': eng_ui,
                        'message': f'UI elements tips "{lv_ui}" ir pēc nosaukuma, bet vajadzētu būt pirms'
                    })

        return issues

    def analyze_all(self):
        """Analyze all segments"""
        print("Performing refined analysis...")

        for seg in self.segments:
            seg_issues = self.analyze_segment_detailed(seg)

            if seg_issues:
                self.issues.append({
                    'segment': seg,
                    'issues': seg_issues
                })

        print(f"\nFound {len(self.issues)} segments with potential issues")
        return self.issues

def main():
    with open('translation_segments.json', 'r', encoding='utf-8') as f:
        segments = json.load(f)

    analyzer = RefinedAnalyzer(segments)
    issues = analyzer.analyze_all()

    # Save results
    with open('refined_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to refined_analysis.json")

    # Show summary
    issue_types = defaultdict(int)
    for seg_issue in issues:
        for issue in seg_issue['issues']:
            issue_types[issue['type']] += 1

    print("\n=== Issue Summary ===")
    for issue_type, count in sorted(issue_types.items()):
        print(f"{issue_type}: {count}")

    # Show examples
    print("\n=== Examples of Issues ===")
    for issue_type in ['NUMBER_MISMATCH', 'POSSIBLE_TRUNCATION', 'UI_WRONG_ORDER']:
        examples = [s for s in issues if any(i['type'] == issue_type for i in s['issues'])]
        if examples:
            print(f"\n{issue_type} (first 3):")
            for i, seg in enumerate(examples[:3]):
                print(f"  {i+1}. Segment {seg['segment']['id']}:")
                print(f"     EN: {seg['segment']['source'][:80]}...")
                print(f"     LV: {seg['segment']['target'][:80]}...")
                issue_details = [iss for iss in seg['issues'] if iss['type'] == issue_type]
                for iss in issue_details:
                    print(f"     >> {iss['message']}")

if __name__ == "__main__":
    main()
