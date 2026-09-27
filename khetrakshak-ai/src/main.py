"""
main.py

End-to-end CLI demo of the KhetRakshak AI pipeline:

    photo -> diagnosis -> dosage plan -> matching schemes -> regional output -> local log

Usage:
    python src/main.py --image data/sample_images/sample_leaf.png --crop tomato --area 2 --language hi
"""

import argparse

from classifier import diagnose
from dosage_engine import get_treatment_plan
from scheme_matcher import matching_schemes
from language import translate, speak
from sync_log import log_diagnosis, sync_pending


def run(image_path: str, crop: str, field_area_acres: float, language: str, block: str) -> None:
    result = diagnose(image_path)

    print("=" * 60)
    print(f"{translate('diagnosis_header', language)} / Diagnosis")
    print("=" * 60)
    print(f"Crop: {crop}")
    print(f"Result: {result.label}  (confidence: {result.confidence:.0%}, method: {result.method})")
    print()

    if result.label == "healthy":
        message = translate("no_disease", language)
        print(message)
        speak(message, language)
    else:
        plan = get_treatment_plan(result.label, field_area_acres)
        print(f"{translate('treatment_header', language)} / Recommended Treatment")
        print(f"  Disease: {plan.display_name}")
        if plan.organic_product:
            print(f"  Organic option:  {plan.organic_product}")
            print(f"                   {plan.organic_total_dose}  |  {plan.organic_frequency}")
        if plan.chemical_product:
            print(f"  Chemical option: {plan.chemical_product}")
            print(f"                   {plan.chemical_total_dose}  |  {plan.chemical_frequency}")
        print(f"  Notes: {plan.notes}")
        print()

        speak(f"{plan.display_name}. {plan.notes}", language)

        schemes = matching_schemes(result.label)
        if schemes:
            print(f"{translate('schemes_header', language)} / Matching Schemes")
            for s in schemes:
                print(f"  - {s['name']}: {s['description']}")
                print(f"    How to apply: {s['how_to_apply']}")
        print()

    entry = log_diagnosis(crop=crop, disease_label=result.label, block=block)
    pending = sync_pending(connectivity_available=False)
    print(f"Logged locally: {entry['disease_label']} @ {entry['block']} "
          f"({pending} entries queued for next opportunistic sync)")


def main():
    parser = argparse.ArgumentParser(description="KhetRakshak AI - offline crop disease diagnosis prototype")
    parser.add_argument("--image", required=True, help="Path to a crop leaf image")
    parser.add_argument("--crop", default="tomato", help="Crop name (e.g. tomato, wheat)")
    parser.add_argument("--area", type=float, default=1.0, help="Field area in acres")
    parser.add_argument("--language", default="en", choices=["en", "hi"], help="Output language")
    parser.add_argument("--block", default="unspecified", help="Coarse location label for the outbreak log")
    args = parser.parse_args()

    run(args.image, args.crop, args.area, args.language, args.block)


if __name__ == "__main__":
    main()
