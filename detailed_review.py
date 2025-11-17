#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detailed Manual Review - comprehensive translation quality check
"""
import json
import re
from collections import defaultdict

def load_segments():
    with open('translation_segments.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def deep_analysis(segments):
    """Perform deep analysis focusing on real issues"""
    issues = []

    for seg in segments:
        seg_id = seg['id']
        source = seg['source']
        target = seg['target']
        seg_issues = []

        # === 1. CHECK FOR TRUNCATED/INCOMPLETE TRANSLATIONS ===
        if len(target) < len(source) * 0.65 and len(source) > 100:
            seg_issues.append({
                'type': 'TRUNCATED',
                'severity': 'HIGH',
                'message': f'Tulkojums iespējami saīsināts: avots {len(source)} simboli, tulkojums {len(target)} simboli'
            })

        # === 2. CHECK NUMBER CONSISTENCY ===
        src_numbers = re.findall(r'\d+\.?\d*', source)
        tgt_numbers = re.findall(r'\d+[.,]?\d*', target)

        # Normalize for comparison
        tgt_normalized = [n.replace(',', '.') for n in tgt_numbers]

        if len(src_numbers) > 0 and len(src_numbers) != len(tgt_normalized):
            # More detailed check - some numbers might be spelled out
            seg_issues.append({
                'type': 'NUMBER_MISMATCH',
                'severity': 'MEDIUM',
                'message': f'Skaitļu skaits atšķiras: EN={src_numbers}, LV={tgt_numbers}',
                'src_numbers': src_numbers,
                'tgt_numbers': tgt_numbers
            })

        # === 3. CHECK UI ELEMENT FORMATTING ===
        # Look for patterns like: "From the X menu" or "Click the Y button"
        ui_patterns = {
            'button': (r'(?:the\s+)?([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\s+button', 'poga'),
            'field': (r'(?:the\s+)?([A-Z][A-Za-z\s]+?)\s+field', 'lauks'),
            'menu': (r'(?:the\s+)?([A-Z][A-Za-z\s]+?)\s+menu', 'izvēlne'),
            'panel': (r'(?:the\s+)?([A-Z][A-Za-z\s]+?)\s+panel', 'panelis'),
            'page': (r'(?:the\s+)?([A-Z][A-Za-z\s]+?)\s+page', 'lapa'),
            'tab': (r'(?:the\s+)?([A-Z][A-Za-z\s]+?)\s+tab', 'cilne'),
            'window': (r'(?:the\s+)?([A-Z][A-Za-z\s]+?)\s+window', 'logs'),
            'mode': (r'([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\s+mode', 'režīms'),
        }

        for ui_type, (pattern, lv_type) in ui_patterns.items():
            matches = re.finditer(pattern, source, re.IGNORECASE)
            for match in matches:
                ui_name = match.group(1).strip()

                # Skip very generic terms
                if ui_name.lower() in ['the', 'this', 'that', 'a', 'an']:
                    continue

                # Check if UI element appears in target
                if ui_name in target:
                    # Check formatting:
                    # CORRECT: "lauks Window Width (Loga platums)"
                    # CORRECT: "Window Width (Loga platums) lauks"
                    # WRONG: "Window Width lauks" (no translation)
                    # WRONG: Just "Window Width" (no translation at all)

                    # Check if it has translation in parentheses
                    has_translation = re.search(rf'{re.escape(ui_name)}\s*\([^)]+\)', target)

                    if not has_translation:
                        # UI element without translation in parentheses
                        seg_issues.append({
                            'type': 'UI_NO_TRANSLATION',
                            'severity': 'MEDIUM',
                            'message': f'UI elements "{ui_name}" ({ui_type}) nav pievienots tulkojums iekavās',
                            'ui_name': ui_name,
                            'ui_type': ui_type
                        })

                    # Check order: UI type should typically be before or after, but check consistency
                    # Pattern: EN_Name (LV_Trans) lv_type - might be wrong
                    wrong_order_pattern = rf'{re.escape(ui_name)}\s*\([^)]+\)\s+{lv_type}\b'
                    if re.search(wrong_order_pattern, target, re.IGNORECASE):
                        seg_issues.append({
                            'type': 'UI_WRONG_ORDER',
                            'severity': 'LOW',
                            'message': f'UI objekta tips "{lv_type}" ir pēc nosaukuma, iespējams pareizāk būtu: "{lv_type} {ui_name} (tulkojums)"',
                            'ui_name': ui_name,
                            'ui_type': lv_type
                        })

        # === 4. CHECK FOR UNTRANSLATED SELECT/CHOOSE OPTIONS ===
        # Pattern: "select Full or Plus" - these should be formatted
        select_patterns = [
            r'select\s+((?:[A-Z][a-z]+)(?:\s+or\s+(?:[A-Z][a-z]+))+)',
            r'choose\s+((?:[A-Z][a-z]+)(?:\s+or\s+(?:[A-Z][a-z]+))+)',
        ]

        for pattern in select_patterns:
            match = re.search(pattern, source, re.IGNORECASE)
            if match:
                options = match.group(1)
                # Extract individual options
                option_list = re.findall(r'[A-Z][a-z]+', options)

                # Check if these options are formatted in target
                for opt in option_list:
                    if opt in target:
                        # Check if formatted as Opt (Tulkojums)
                        if not re.search(rf'{re.escape(opt)}\s*\([^)]+\)', target):
                            # Not formatted - might be an issue
                            if len(opt) > 3:  # Skip very short words
                                seg_issues.append({
                                    'type': 'OPTION_NO_FORMAT',
                                    'severity': 'MEDIUM',
                                    'message': f'Opcija "{opt}" nav formatēta kā EN (Tulkojums)',
                                    'option': opt
                                })

        # === 5. CHECK FOR COMMON UNTRANSLATED WORDS ===
        # These shouldn't appear in Latvian text unless in (EN) format
        untranslated_indicators = [
            (r'\bthe\s+\w+\s+button\b', 'Neiztulkots "the ... button"'),
            (r'\bclick\s+\w+', 'Neiztulkots "click"'),
            (r'\bselect\s+\w+', 'Neiztulkots "select"'),
            (r'\bpress\s+\w+', 'Neiztulkots "press"'),
            (r'\benter\s+\w+', 'Neiztulkots "enter"'),
        ]

        for pattern, desc in untranslated_indicators:
            if re.search(pattern, target, re.IGNORECASE):
                # Make sure it's not in (EN) format
                match = re.search(pattern, target, re.IGNORECASE)
                if match:
                    context_start = max(0, match.start() - 30)
                    context_end = min(len(target), match.end() + 30)
                    context = target[context_start:context_end]

                    # Check if it's in parentheses (which would be correct)
                    if not re.search(r'\([^)]*' + re.escape(match.group(0)) + r'[^)]*\)', context):
                        seg_issues.append({
                            'type': 'UNTRANSLATED',
                            'severity': 'HIGH',
                            'message': desc,
                            'context': context
                        })
                        break  # Only report once per segment

        # === 6. CHECK TERM CONSISTENCY (track for later analysis) ===
        # This will be done in aggregate

        if seg_issues:
            issues.append({
                'segment': seg,
                'issues': seg_issues
            })

    return issues

def generate_issues_report(issues):
    """Generate detailed report"""
    print(f"=== DETAILED REVIEW RESULTS ===\n")
    print(f"Total segments with issues: {len(issues)}\n")

    # Group by severity
    high_severity = [i for i in issues if any(iss['severity'] == 'HIGH' for iss in i['issues'])]
    medium_severity = [i for i in issues if any(iss['severity'] == 'MEDIUM' for iss in i['issues']) and i not in high_severity]
    low_severity = [i for i in issues if any(iss['severity'] == 'LOW' for iss in i['issues']) and i not in high_severity and i not in medium_severity]

    print(f"HIGH severity: {len(high_severity)}")
    print(f"MEDIUM severity: {len(medium_severity)}")
    print(f"LOW severity: {len(low_severity)}\n")

    # Count issue types
    issue_type_count = defaultdict(int)
    for issue_seg in issues:
        for iss in issue_seg['issues']:
            issue_type_count[iss['type']] += 1

    print("=== Issue Types ===")
    for issue_type, count in sorted(issue_type_count.items(), key=lambda x: -x[1]):
        print(f"{issue_type}: {count}")

    return high_severity, medium_severity, low_severity

def save_results(issues, filename='detailed_issues.json'):
    """Save detailed issues to JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed results saved to {filename}")

def show_examples(issues, issue_type, limit=5):
    """Show examples of specific issue type"""
    examples = [i for i in issues if any(iss['type'] == issue_type for iss in i['issues'])]
    print(f"\n=== Examples of {issue_type} (showing {min(limit, len(examples))}) ===")

    for i, item in enumerate(examples[:limit]):
        seg = item['segment']
        print(f"\n{i+1}. Segment #{seg['id']}")
        print(f"   EN: {seg['source']}")
        print(f"   LV: {seg['target']}")

        # Show relevant issues
        relevant_issues = [iss for iss in item['issues'] if iss['type'] == issue_type]
        for iss in relevant_issues:
            print(f"   ⚠️  {iss['message']}")

def main():
    segments = load_segments()
    print(f"Analyzing {len(segments)} segments...\n")

    issues = deep_analysis(segments)

    high, medium, low = generate_issues_report(issues)

    save_results(issues, 'detailed_issues.json')

    # Show examples of each major issue type
    major_types = ['TRUNCATED', 'UNTRANSLATED', 'NUMBER_MISMATCH', 'UI_NO_TRANSLATION', 'OPTION_NO_FORMAT']
    for issue_type in major_types:
        show_examples(issues, issue_type, limit=3)

if __name__ == "__main__":
    main()
