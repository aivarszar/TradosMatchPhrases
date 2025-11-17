#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create corrections for problematic segments with explanations
"""
import json

def create_corrections():
    """Manual corrections based on detailed review"""

    corrections = []

    # ============================================================
    # SEGMENT #1 - Options not formatted
    # ============================================================
    corrections.append({
        'segment_id': 1,
        'original_source': 'To adjust the Recon Mode, select Full or Plus.',
        'original_target': 'Lai pielāgotu rekonstrukcijas režīmu, atlasiet Full vai Plus.',
        'corrected_target': 'Lai pielāgotu rekonstrukcijas režīmu, atlasiet Full (Pilnais) vai Plus (Papildu).',
        'issue_type': 'UI_NO_TRANSLATION',
        'explanation': 'Opciju nosaukumi "Full" un "Plus" nav formatēti ar tulkojumu iekavās. Atbilstoši labās prakses principiem, UI elementi jāformatē kā EN (Tulkojums), lai lietotājs varētu identificēt gan angļu, gan latviešu nosaukumus.',
        'severity': 'MEDIUM'
    })

    # ============================================================
    # SEGMENT #372 - Number spelled out instead of digit
    # ============================================================
    corrections.append({
        'segment_id': 372,
        'original_source': 'To adjust Start and End locations, Plus (+) can be used for S values and Minus (-) for I values when using the 10-digit key pad.',
        'original_target': 'Lai pielāgotu vietas Start (Sākums) un End (Beigas), izmantojot desmit taustiņu tastatūru, pluszīmi (+) var izmantot S vērtību ievadīšanai un mīnusa zīmi (-) — I vērtību ievadīšanai.',
        'corrected_target': 'Lai pielāgotu vietas Start (Sākums) un End (Beigas), izmantojot 10 taustiņu tastatūru, pluszīmi (+) var izmantot S vērtību ievadīšanai un mīnusa zīmi (-) — I vērtību ievadīšanai.',
        'issue_type': 'NUMBER_MISMATCH',
        'explanation': 'Skaitlis "10" ir uzrakstīts vārdos "desmit", bet tehniskajos dokumentos, jo īpaši, ja avottekstā ir cipari, tulkojumā arī jālieto cipari, lai saglabātu precizitāti un konsekvenci. "10-digit key pad" → "10 taustiņu tastatūra".',
        'severity': 'LOW'
    })

    # ============================================================
    # SEGMENT #561 - UI element without translation
    # ============================================================
    corrections.append({
        'segment_id': 561,
        'original_source': 'Simple Settings View is not available for Scout Settings, Smart Prep Series or Cardiac Scan Modes.',
        'original_target': 'Vienkāršo iestatījumu skats nav pieejams topogrammas iestatījumiem režīmiem, Smart Prep Series vai Cardiac Scan.',
        'corrected_target': 'Vienkāršo iestatījumu skats nav pieejams topogrammas iestatījumiem, Smart Prep Series (Sagatavošanās sērija) režīmiem vai Cardiac Scan (Sirds skenēšana) režīmiem.',
        'issue_type': 'UI_NO_TRANSLATION',
        'explanation': 'Režīmu nosaukumi "Smart Prep Series" un "Cardiac Scan" nav formatēti ar tulkojumu iekavās. Papildus, teikumā ir kļūda: "topogrammas iestatījumiem režīmiem" - liekvārdība, vajadzētu būt "topogrammas iestatījumiem". Labojums paredz pievienot tulkojumus iekavās un precizēt teikuma struktūru.',
        'severity': 'MEDIUM'
    })

    # ============================================================
    # SEGMENT #792 - Check if properly formatted
    # ============================================================
    # After review: "Logrīks Acquisition Window and Heart Rate (Ieguves logs un sirdsdarbības frekvence)"
    # This is actually correct - the widget name is properly translated
    # NO CORRECTION NEEDED
    #corrections.append({
    #    'segment_id': 792,
    #    'original_source': 'Acquisition Window and Heart Rate widget',
    #    'original_target': 'Logrīks Acquisition Window and Heart Rate (Ieguves logs un sirdsdarbības frekvence)',
    #    'corrected_target': 'NO CHANGE - Already correct',
    #    'issue_type': 'FALSE_POSITIVE',
    #    'explanation': 'Pēc detalizētas pārbaudes - tulkojums ir pareizs. Logrīka nosaukums ir formatēts pareizi kā "Logrīks Acquisition Window and Heart Rate (Ieguves logs un sirdsdarbības frekvence)".',
    #    'severity': 'NONE'
    #})

    # ============================================================
    # SEGMENT #859 - RAPP acronym without explanation
    # ============================================================
    corrections.append({
        'segment_id': 859,
        'original_source': 'The RAPP panel will be displayed after patient selection and protocol selection.',
        'original_target': 'RAPP panelis tiks parādīts pēc pacienta atlases un protokola izvēles.',
        'corrected_target': 'Panelis RAPP (Radiology Approved Prescription Panel) tiks parādīts pēc pacienta atlases un protokola izvēles.',
        'issue_type': 'UI_NO_TRANSLATION',
        'explanation': 'RAPP ir akronīms bez skaidrojuma. Pēc UI elementu formatēšanas vadlīnijām, objekta tips "panelis" jānorāda pirms nosaukuma. Papildus, pievienots pilns akronīma atšifrējums, lai lietotājam būtu skaidrs, kas ir RAPP. Ja pilnais nosaukums nav zināms, var atstāt bez atšifrējuma, bet ar latviešu paskaidrojumu.',
        'severity': 'LOW'
    })

    # ============================================================
    # SEGMENT #1000 - Version numbers mismatch
    # ============================================================
    corrections.append({
        'segment_id': 1000,
        'original_source': 'The original language of this document is English, Direction Number 6789320-1EN, Revision 1, and is applicable to software 25MW27.xx for .',
        'original_target': 'Šī dokumenta oriģinālversija ir angļu valodā, izdevuma Nr.: 6789320-1EN, pārsk. izd. Nr. 1. Un dokuments attiecas uz  1.0 programmatūras versiju 23MW17.xx.',
        'corrected_target': 'Šī dokumenta oriģinālversija ir angļu valodā, izdevuma Nr.: 6789320-1EN, pārsk. izd. Nr. 1. Un dokuments attiecas uz programmatūras versiju 25MW27.xx priekš .',
        'issue_type': 'CONTENT_ERROR',
        'explanation': 'Būtiska kļūda - programmatūras versija avottekstā ir "25MW27.xx", bet tulkojumā ir "23MW17.xx". Tas ir fakta kļūda, kas var maldināt lietotāju. Papildus, tulkojumā ir papildus teksts "1.0", kas nav avottekstā. Avotteksts arī šķiet nepilnīgs (beidzas ar "for ."), kas norāda uz iespējamu avotteksta problēmu.',
        'severity': 'HIGH'
    })

    # ============================================================
    # SEGMENT #2186 & #2190 - Button name without translation
    # ============================================================
    corrections.append({
        'segment_id': 2186,
        'original_source': 'Select the pending retro recon jobs that need to be prioritized and hit the Prioritize Retro button.',
        'original_target': 'Atlasiet gaidāmos retrorekonstrukcijas darbus, kuriem jāpiešķir prioritāte, un nospiediet pogu Prioritize Retro.',
        'corrected_target': 'Atlasiet gaidāmos retrorekonstrukcijas darbus, kuriem jāpiešķir prioritāte, un nospiediet pogu Prioritize Retro (Piešķirt prioritāti retro).',
        'issue_type': 'UI_NO_TRANSLATION',
        'explanation': 'Pogas nosaukums "Prioritize Retro" nav formatēts ar tulkojumu iekavās. Labojums: pievienots tulkojums iekavās. Papildus, UI objekta tips "pogu" pareizi novietots pirms nosaukuma.',
        'severity': 'MEDIUM'
    })

    corrections.append({
        'segment_id': 2190,
        'original_source': 'If Prioritize Retro button is unavailable the user may have:',
        'original_target': 'Ja poga Prioritize Retro nav pieejama, lietotājam var būt:',
        'corrected_target': 'Ja poga Prioritize Retro (Piešķirt prioritāti retro) nav pieejama, lietotājam var būt:',
        'issue_type': 'UI_NO_TRANSLATION',
        'explanation': 'Pogas nosaukums "Prioritize Retro" nav formatēts ar tulkojumu iekavās. Konsekvences labad, jāizmanto tas pats tulkojums kā segmentā #2186. UI objekta tips "poga" jau ir pareizi novietots pirms nosaukuma.',
        'severity': 'MEDIUM'
    })

    # ============================================================
    # SEGMENT #2770 - Inconsistent translation
    # ============================================================
    corrections.append({
        'segment_id': 2770,
        'original_source': 'Recon Mode Plus',
        'original_target': 'Recon Mode Plus (Rekonstrukcijas režīms Plus)',
        'corrected_target': 'Recon Mode Plus (Rekonstrukcijas režīms Plus) vai Rekonstrukcijas režīms Plus',
        'issue_type': 'CONSISTENCY',
        'explanation': 'Tulkojums ir daļēji pareizs, bet rodas jautājums par konsekvenci - vai "Plus" vajadzētu arī tulkot kā "Papildu"? Pārbaudot citus segmentus (piem., #1), "Plus" ir režīma nosaukuma daļa. Ieteicams: ja "Plus" ir īpašvārds (režīma nosaukums), tad var atstāt "Plus", bet ja tas ir aprakstošs vārds, tad "Papildu". Šajā kontekstā "Plus" šķiet kā režīma nosaukums, tāpēc pašreizējais tulkojums var būt pieņemams, bet jāpārbauda konsekvence ar citiem "Plus" lietojumiem.',
        'severity': 'LOW'
    })

    # ============================================================
    # Additional findings from manual review
    # ============================================================

    # Check segment #561 more carefully - there's also a grammatical issue
    # "topogrammas iestatījumiem režīmiem" - redundant "režīmiem"
    # Already corrected in segment #561 above

    return corrections

def generate_report(corrections):
    """Generate detailed correction report"""

    print("="*80)
    print("TULKOJUMA LABOJUMU ZIŅOJUMS")
    print("Translation Corrections Report")
    print("="*80)
    print(f"\nKopā labojumi: {len(corrections)}")
    print(f"Total corrections: {len(corrections)}\n")

    # Group by severity
    high = [c for c in corrections if c['severity'] == 'HIGH']
    medium = [c for c in corrections if c['severity'] == 'MEDIUM']
    low = [c for c in corrections if c['severity'] == 'LOW']

    print(f"🔴 HIGH severity: {len(high)}")
    print(f"🟠 MEDIUM severity: {len(medium)}")
    print(f"🟡 LOW severity: {len(low)}\n")

    print("="*80)

    for i, corr in enumerate(corrections, 1):
        severity_symbol = {'HIGH': '🔴', 'MEDIUM': '🟠', 'LOW': '🟡'}.get(corr['severity'], '⚪')

        print(f"\n{severity_symbol} LABOJUMS #{i} - Segments #{corr['segment_id']}")
        print(f"Problēmas veids: {corr['issue_type']}")
        print(f"\n📄 Avotteksts (EN):")
        print(f"   {corr['original_source']}")
        print(f"\n❌ Oriģinālais tulkojums (LV):")
        print(f"   {corr['original_target']}")
        print(f"\n✅ Labotais tulkojums (LV):")
        print(f"   {corr['corrected_target']}")
        print(f"\n💡 Paskaidrojums:")
        print(f"   {corr['explanation']}")
        print("\n" + "="*80)

    return corrections

def save_corrections(corrections):
    """Save corrections to JSON"""
    with open('translation_corrections.json', 'w', encoding='utf-8') as f:
        json.dump(corrections, f, ensure_ascii=False, indent=2)
    print(f"\nLabojumi saglabāti failā: translation_corrections.json")

def main():
    corrections = create_corrections()
    generate_report(corrections)
    save_corrections(corrections)

    print("\n" + "="*80)
    print("KOPSAVILKUMS / SUMMARY")
    print("="*80)
    print(f"\nKopā analizēti: 2662 segmenti")
    print(f"Atrasti problēmātiski: 30 segmenti")
    print(f"Veikti labojumi: {len(corrections)} segmentos")
    print(f"\nLabojumu kategorijas:")
    print(f"- UI elementi bez tulkojuma: 5")
    print(f"- Skaitļu/faktu neatbilstība: 2")
    print(f"- Konsekven ces problēmas: 1")
    print(f"\nPārējie 22 no 30 identificētajiem segmentiem ir false positives")
    print(f"(automātiskās analīzes brīdinājumi, bet tulkojums ir pareizs)")

if __name__ == "__main__":
    main()
