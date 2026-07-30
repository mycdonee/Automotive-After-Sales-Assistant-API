from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REVIEW_DATE = "2026-07-30"
DATA_DIR = Path("data/regulations")
RECORDS_PATH = DATA_DIR / "regulation_records.jsonl"
PAIRS_PATH = DATA_DIR / "regulation_comparison_pairs.json"


def unece_record(
    regulation_id: str,
    number: str,
    aliases: list[str],
    title: str,
    regulatory_system: str,
    regulated_object: str,
    scope_summary: str,
    vehicle_applicability: list[str],
    requirement_topics: list[str],
    reviewed_version: str,
    source_documents: list[str],
    special_status_notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "regulation_id": regulation_id,
        "jurisdiction": "UNECE",
        "authority": (
            "United Nations Economic Commission for Europe "
            "(UNECE)"
        ),
        "official_identifier": f"UN Regulation No. {number}",
        "aliases": aliases,
        "title": title,
        "citation": f"UN Regulation No. {number}",
        "regulatory_system": regulatory_system,
        "regulated_object": regulated_object,
        "scope_summary": scope_summary,
        "vehicle_applicability": vehicle_applicability,
        "requirement_topics": requirement_topics,
        "reviewed_version": reviewed_version,
        "reviewed_source_documents": source_documents,
        "source_format": "pdf",
        "source_content_date": None,
        "source_reviewed_on": REVIEW_DATE,
        "special_status_notes": special_status_notes or [],
        "verification_status": "verified",
    }


def fmvss_record(
    regulation_id: str,
    number: str,
    aliases: list[str],
    title: str,
    regulatory_system: str,
    regulated_object: str,
    scope_summary: str,
    vehicle_applicability: list[str],
    requirement_topics: list[str],
    special_status_notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "regulation_id": regulation_id,
        "jurisdiction": "United States",
        "authority": (
            "National Highway Traffic Safety Administration "
            "(NHTSA)"
        ),
        "official_identifier": f"FMVSS No. {number}",
        "aliases": aliases,
        "title": title,
        "citation": f"49 CFR 571.{number}",
        "regulatory_system": regulatory_system,
        "regulated_object": regulated_object,
        "scope_summary": scope_summary,
        "vehicle_applicability": vehicle_applicability,
        "requirement_topics": requirement_topics,
        "reviewed_version": (
            "eCFR version dated 2026-07-27"
        ),
        "reviewed_source_documents": [
            (
                "data/raw/regulations/fmvss/"
                f"FMVSS_{number}_eCFR_2026-07-27.xml"
            ),
            (
                "Source review documented in "
                "data/regulations/"
                "comparability_verification.md"
            ),
        ],
        "source_format": "xml",
        "source_content_date": "2026-07-27",
        "source_reviewed_on": REVIEW_DATE,
        "special_status_notes": special_status_notes or [],
        "verification_status": "verified",
    }


records = [
    unece_record(
        regulation_id="unece_r13h",
        number="13-H",
        aliases=[
            "UN R13-H",
            "UNECE R13-H",
        ],
        title="Passenger cars with regard to braking",
        regulatory_system="braking_and_stability",
        regulated_object="Passenger-car braking systems",
        scope_summary=(
            "Requirements for braking-system performance and "
            "behavior for passenger cars within the reviewed "
            "UN R13-H scope."
        ),
        vehicle_applicability=[
            "Passenger cars within the reviewed UNECE category scope",
        ],
        requirement_topics=[
            "service braking",
            "secondary braking",
            "parking braking",
            "stopping performance",
            "brake-system integrity",
            "anti-lock braking",
            "warning signals",
            "test procedures",
        ],
        reviewed_version=(
            "Verified UNECE source chain documented for Pair 1"
        ),
        source_documents=[
            (
                "data/regulations/"
                "comparability_verification.md — Pair 1 source review"
            ),
            (
                "data/raw/regulations/unece/r13h/ — "
                "ignored official UNECE research artifacts"
            ),
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_135",
        number="135",
        aliases=[
            "FMVSS 135",
            "49 CFR 571.135",
        ],
        title="Light vehicle brake systems",
        regulatory_system="braking_and_stability",
        regulated_object="Light-vehicle brake systems",
        scope_summary=(
            "Federal requirements for service, parking, and "
            "related braking performance on vehicles covered "
            "by FMVSS 135."
        ),
        vehicle_applicability=[
            (
                "Light vehicles covered by FMVSS 135, subject "
                "to its stated inclusions and exclusions"
            ),
        ],
        requirement_topics=[
            "service braking",
            "parking braking",
            "stopping distance",
            "brake-system failure",
            "anti-lock braking",
            "warning indicators",
            "vehicle loading conditions",
            "test procedures",
        ],
    ),
    unece_record(
        regulation_id="unece_r140",
        number="140",
        aliases=[
            "UN R140",
            "UNECE R140",
        ],
        title="Electronic Stability Control Systems",
        regulatory_system="braking_and_stability",
        regulated_object=(
            "Electronic stability control systems"
        ),
        scope_summary=(
            "Functional and performance requirements for "
            "electronic stability control systems on vehicles "
            "within the reviewed UN R140 scope."
        ),
        vehicle_applicability=[
            (
                "Vehicles within the M1 and N1 categories "
                "covered by the reviewed UN R140 scope"
            ),
        ],
        requirement_topics=[
            "electronic stability control",
            "yaw stability",
            "lateral responsiveness",
            "system activation",
            "malfunction detection",
            "driver telltales",
            "test maneuvers",
            "performance thresholds",
        ],
        reviewed_version=(
            "Verified UNECE source chain documented for Pair 2"
        ),
        source_documents=[
            (
                "data/regulations/"
                "comparability_verification.md — Pair 2 source review"
            ),
            (
                "data/raw/regulations/unece/r140/ — "
                "ignored official UNECE research artifacts"
            ),
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_126",
        number="126",
        aliases=[
            "FMVSS 126",
            "49 CFR 571.126",
        ],
        title=(
            "Electronic stability control systems "
            "for light vehicles"
        ),
        regulatory_system="braking_and_stability",
        regulated_object=(
            "Electronic stability control systems "
            "for light vehicles"
        ),
        scope_summary=(
            "Federal functional and performance requirements "
            "for electronic stability control systems on "
            "covered light vehicles."
        ),
        vehicle_applicability=[
            (
                "Light vehicles covered by FMVSS 126, subject "
                "to its stated weight limits and exclusions"
            ),
        ],
        requirement_topics=[
            "electronic stability control",
            "yaw stability",
            "lateral responsiveness",
            "system activation",
            "malfunction detection",
            "driver telltales",
            "sine-with-dwell testing",
            "performance thresholds",
        ],
    ),
    unece_record(
        regulation_id="unece_r14",
        number="14",
        aliases=[
            "UN R14",
            "UNECE R14",
        ],
        title=(
            "Safety-belt anchorages, ISOFIX anchorage systems "
            "and ISOFIX top tether anchorages"
        ),
        regulatory_system="occupant_restraint",
        regulated_object=(
            "Seat-belt and child-restraint anchorages"
        ),
        scope_summary=(
            "Requirements for the location, geometry, strength, "
            "and testing of safety-belt and associated "
            "child-restraint anchorages."
        ),
        vehicle_applicability=[
            (
                "Vehicles in the M and N categories covered "
                "by the reviewed UN R14 scope"
            ),
        ],
        requirement_topics=[
            "seat-belt anchorages",
            "anchorage location",
            "anchorage geometry",
            "anchorage strength",
            "load testing",
            "ISOFIX anchorages",
            "top tether anchorages",
            "vehicle structure",
        ],
        reviewed_version=(
            "Verified UNECE source chain documented for Pair 3"
        ),
        source_documents=[
            (
                "data/regulations/"
                "comparability_verification.md — Pair 3 source review"
            ),
            (
                "data/raw/regulations/unece/r14/ — "
                "ignored official UNECE research artifacts"
            ),
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_210",
        number="210",
        aliases=[
            "FMVSS 210",
            "49 CFR 571.210",
        ],
        title="Seat belt assembly anchorages",
        regulatory_system="occupant_restraint",
        regulated_object="Seat-belt assembly anchorages",
        scope_summary=(
            "Federal requirements for seat-belt anchorage "
            "installation, location, strength, and load testing "
            "on covered vehicles."
        ),
        vehicle_applicability=[
            (
                "Vehicles and seating positions covered by "
                "FMVSS 210"
            ),
        ],
        requirement_topics=[
            "seat-belt anchorages",
            "anchorage location",
            "anchorage strength",
            "load application",
            "seating positions",
            "vehicle structure",
            "attachment hardware",
            "test procedures",
        ],
    ),
    unece_record(
        regulation_id="unece_r16",
        number="16",
        aliases=[
            "UN R16",
            "UNECE R16",
        ],
        title=(
            "Safety-belts, restraint systems, child restraint "
            "systems and ISOFIX child restraint systems"
        ),
        regulatory_system="occupant_restraint",
        regulated_object=(
            "Safety belts and occupant-restraint systems"
        ),
        scope_summary=(
            "Requirements for safety-belt assemblies, restraint "
            "systems, their components, installation, and "
            "associated vehicle provisions."
        ),
        vehicle_applicability=[
            (
                "Vehicles, seating positions, and restraint "
                "systems covered by the reviewed UN R16 scope"
            ),
        ],
        requirement_topics=[
            "seat-belt assemblies",
            "webbing",
            "buckles",
            "retractors",
            "strength",
            "durability",
            "restraint-system installation",
            "occupant protection",
        ],
        reviewed_version=(
            "Verified UNECE source chain documented for Pair 4"
        ),
        source_documents=[
            (
                "data/regulations/"
                "comparability_verification.md — Pair 4 source review"
            ),
            (
                "data/raw/regulations/unece/r16/ — "
                "ignored official UNECE research artifacts"
            ),
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_209",
        number="209",
        aliases=[
            "FMVSS 209",
            "49 CFR 571.209",
        ],
        title="Seat belt assemblies",
        regulatory_system="occupant_restraint",
        regulated_object="Seat-belt assemblies",
        scope_summary=(
            "Federal requirements for seat-belt assembly "
            "components, strength, operation, durability, "
            "marking, and testing."
        ),
        vehicle_applicability=[
            (
                "Seat-belt assemblies designed for use in "
                "motor vehicles covered by the standard"
            ),
        ],
        requirement_topics=[
            "seat-belt assemblies",
            "webbing",
            "buckles",
            "retractors",
            "attachment hardware",
            "strength",
            "durability",
            "marking and instructions",
        ],
    ),
    unece_record(
        regulation_id="unece_r145",
        number="145",
        aliases=[
            "UN R145",
            "UNECE R145",
        ],
        title=(
            "ISOFIX anchorage systems, ISOFIX top tether "
            "anchorages and i-Size seating positions"
        ),
        regulatory_system="occupant_restraint",
        regulated_object=(
            "Child-restraint anchorage systems"
        ),
        scope_summary=(
            "Requirements for ISOFIX anchorage systems, top "
            "tether anchorages, and i-Size seating positions."
        ),
        vehicle_applicability=[
            (
                "Vehicles and seating positions equipped with "
                "covered ISOFIX or i-Size anchorage systems"
            ),
        ],
        requirement_topics=[
            "ISOFIX anchorages",
            "top tether anchorages",
            "i-Size seating positions",
            "anchorage geometry",
            "anchorage strength",
            "marking",
            "accessibility",
            "load testing",
        ],
        reviewed_version=(
            "Verified UNECE source chain documented for Pair 5"
        ),
        source_documents=[
            (
                "data/regulations/"
                "comparability_verification.md — Pair 5 source review"
            ),
            (
                "data/raw/regulations/unece/r145/ — "
                "ignored official UNECE research artifacts"
            ),
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_225",
        number="225",
        aliases=[
            "FMVSS 225",
            "49 CFR 571.225",
            "LATCH anchorage standard",
        ],
        title="Child restraint anchorage systems",
        regulatory_system="occupant_restraint",
        regulated_object=(
            "Child-restraint anchorage systems"
        ),
        scope_summary=(
            "Federal requirements for lower anchorages, tether "
            "anchorages, their location, strength, marking, and "
            "installation on covered vehicles."
        ),
        vehicle_applicability=[
            (
                "Vehicles and designated seating positions "
                "covered by FMVSS 225"
            ),
        ],
        requirement_topics=[
            "lower anchorages",
            "tether anchorages",
            "LATCH systems",
            "anchorage geometry",
            "anchorage strength",
            "marking",
            "accessibility",
            "load testing",
        ],
    ),
    unece_record(
        regulation_id="unece_r48",
        number="48",
        aliases=[
            "UN R48",
            "UNECE R48",
        ],
        title=(
            "Installation of lighting and "
            "light-signalling devices"
        ),
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Vehicle-level installation of lighting and "
            "light-signalling devices"
        ),
        scope_summary=(
            "Vehicle-level requirements governing the number, "
            "position, orientation, visibility, activation, and "
            "installation of lighting and light-signalling "
            "devices."
        ),
        vehicle_applicability=[
            "Vehicles of categories M and N",
            "Trailers of category O",
        ],
        requirement_topics=[
            "lamp installation",
            "number of lamps",
            "mounting position",
            "mounting height",
            "geometric visibility",
            "orientation",
            "activation",
            "tell-tales",
            "lighting functions",
            "conspicuity",
        ],
        reviewed_version=(
            "Revision 14 through Amendment 6, Corrigendum 1"
        ),
        source_documents=[
            "UN Regulation No. 48, Revision 13",
            "Revision 13, Amendments 1–3",
            "Revision 14, Amendments 1–6",
            "Revision 14, Amendment 6, Corrigendum 1",
        ],
    ),
    unece_record(
        regulation_id="unece_r148",
        number="148",
        aliases=[
            "UN R148",
            "UNECE R148",
        ],
        title=(
            "Light-signalling devices for power-driven "
            "vehicles and their trailers"
        ),
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Individual light-signalling devices and lamps"
        ),
        scope_summary=(
            "Type-approval and performance requirements for "
            "registration-plate lamps, indicators, position "
            "lamps, stop lamps, reversing lamps, fog lamps, "
            "daytime running lamps, and related signalling "
            "devices."
        ),
        vehicle_applicability=[
            (
                "Power-driven vehicles and trailers using "
                "covered light-signalling devices"
            ),
        ],
        requirement_topics=[
            "light-signalling lamps",
            "luminous intensity",
            "light distribution",
            "color",
            "photometric performance",
            "light sources",
            "variable intensity",
            "sequential activation",
            "heat resistance",
            "test procedures",
        ],
        reviewed_version=(
            "Amendment 5, 01 series, with Revision 1 "
            "Amendments 1–2 reviewed"
        ),
        source_documents=[
            "UN Regulation No. 148, original regulation",
            "Amendments 1–5",
            "Revision 1, Amendments 1–2",
        ],
        special_status_notes=[
            (
                "Amendment 5 introduced the 01 series on "
                "4 January 2023."
            ),
            (
                "No later top-level Scope change was identified "
                "in Revision 1 Amendments 1–2."
            ),
        ],
    ),
    unece_record(
        regulation_id="unece_r149",
        number="149",
        aliases=[
            "UN R149",
            "UNECE R149",
        ],
        title=(
            "Road illumination devices and systems for "
            "power-driven vehicles"
        ),
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Road-illumination devices, lamps, beams, "
            "and associated systems"
        ),
        scope_summary=(
            "Performance requirements for driving and passing "
            "beams, adaptive front-lighting systems, adaptive "
            "driving beams, front fog lamps, and cornering lamps."
        ),
        vehicle_applicability=[
            (
                "Vehicles of categories L, M, N, and T as "
                "specified for each covered lighting function"
            ),
        ],
        requirement_topics=[
            "driving beams",
            "passing beams",
            "adaptive driving beams",
            "adaptive front-lighting systems",
            "beam cutoff",
            "headlamp aiming",
            "photometric test points",
            "light sources",
            "plastic lenses",
            "durability testing",
        ],
        reviewed_version=(
            "Amendment 6, 01 series, with Revision 1 "
            "Amendments 1–3 reviewed"
        ),
        source_documents=[
            "UN Regulation No. 149, original regulation",
            "Amendments 1–6",
            "Revision 1, Amendments 1–3",
        ],
        special_status_notes=[
            (
                "Revision 1 Amendment 3 is the latest reviewed "
                "top-level Scope amendment."
            ),
            (
                "The separately listed Revision 1 consolidated "
                "document was forthcoming when reviewed."
            ),
        ],
    ),
    unece_record(
        regulation_id="unece_r150",
        number="150",
        aliases=[
            "UN R150",
            "UNECE R150",
        ],
        title=(
            "Retro-reflective devices and markings for "
            "power-driven vehicles and their trailers"
        ),
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Retro-reflective devices, materials, markings, "
            "plates, and warning triangles"
        ),
        scope_summary=(
            "Performance and type-approval requirements for "
            "retro-reflectors, marking materials, heavy- and "
            "long-vehicle plates, slow-moving-vehicle plates, "
            "and advance warning triangles."
        ),
        vehicle_applicability=[
            (
                "Power-driven vehicles and trailers using "
                "covered retro-reflective devices or markings"
            ),
        ],
        requirement_topics=[
            "retro-reflectors",
            "retro-reflective materials",
            "marking plates",
            "observation angles",
            "entrance angles",
            "coefficient of retro-reflection",
            "colorimetric performance",
            "environmental testing",
            "chemical resistance",
            "mechanical resistance",
        ],
        reviewed_version=(
            "Amendment 5, 01 series, with Revision 1 "
            "Amendments 1–2 and Corrigendum 1 reviewed"
        ),
        source_documents=[
            "UN Regulation No. 150, original regulation",
            "Amendments 1–5",
            "Revision 1, Amendments 1–2",
            "Revision 1, Amendment 2, Corrigendum 1",
        ],
        special_status_notes=[
            (
                "Amendment 5 introduced the 01 series on "
                "4 January 2023."
            ),
            (
                "No later top-level Scope change was identified "
                "in the reviewed Revision 1 documents."
            ),
        ],
    ),
    unece_record(
        regulation_id="unece_r104",
        number="104",
        aliases=[
            "UN R104",
            "UNECE R104",
        ],
        title=(
            "Retro-reflective markings for heavy and long "
            "vehicles and their trailers"
        ),
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Vehicle conspicuity marking materials"
        ),
        scope_summary=(
            "Requirements for retro-reflective markings used "
            "on specified buses, goods vehicles, and trailers."
        ),
        vehicle_applicability=[
            "Category M2",
            "Category M3",
            "Category N",
            "Category O2",
            "Category O3",
            "Category O4",
        ],
        requirement_topics=[
            "retro-reflective markings",
            "side markings",
            "rear markings",
            "strip dimensions",
            "colorimetric performance",
            "photometric performance",
            "coefficient of retro-reflection",
            "observation angles",
            "entrance angles",
            "resistance to external agents",
        ],
        reviewed_version=(
            "Revision 1 with Corrigenda 1–2 and "
            "Amendments 1–4 reviewed"
        ),
        source_documents=[
            "UN Regulation No. 104, Revision 1",
            "Revision 1, Corrigenda 1–2",
            "Revision 1, Amendments 1–4",
        ],
        special_status_notes=[
            (
                "No later top-level Scope change was identified "
                "in the reviewed corrigenda and amendments."
            ),
        ],
    ),
    unece_record(
        regulation_id="unece_r27",
        number="27",
        aliases=[
            "UN R27",
            "UNECE R27",
        ],
        title="Advance warning triangles",
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Portable advance warning triangles"
        ),
        scope_summary=(
            "Requirements for portable warning triangles "
            "carried on vehicles and placed on the carriageway "
            "to warn of a halted vehicle by day and night."
        ),
        vehicle_applicability=[
            (
                "Vehicles carrying covered portable advance "
                "warning devices"
            ),
        ],
        requirement_topics=[
            "advance warning triangles",
            "equilateral-triangle shape",
            "retro-reflecting material",
            "fluorescent material",
            "coefficient of luminous intensity",
            "luminance factor",
            "shape and dimensions",
            "road-surface stability",
            "weathering",
            "instructions for use",
        ],
        reviewed_version="Revision 3, 05 series",
        source_documents=[
            "UN Regulation No. 27, Revision 3",
            (
                "Supplement 1 to the 04 series incorporated "
                "into Revision 3"
            ),
            (
                "05 series of amendments incorporated into "
                "Revision 3"
            ),
        ],
        special_status_notes=[
            (
                "The 05 series entered into force on "
                "15 October 2019."
            ),
            (
                "The transitional provisions require "
                "Contracting Parties to cease granting new "
                "R27 approvals 24 months after UN R150 enters "
                "into force, while specified extensions and "
                "replacement-device approvals may continue."
            ),
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_108",
        number="108",
        aliases=[
            "FMVSS 108",
            "49 CFR 571.108",
        ],
        title=(
            "Lamps, reflective devices, and "
            "associated equipment"
        ),
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Vehicle lighting, reflective devices, "
            "and associated equipment"
        ),
        scope_summary=(
            "Federal requirements covering vehicle lighting "
            "installation, lamp performance, reflective devices, "
            "conspicuity treatment, original equipment, and "
            "replacement equipment."
        ),
        vehicle_applicability=[
            "Passenger cars",
            "Multipurpose passenger vehicles",
            "Trucks",
            "Buses",
            "Trailers, subject to specified exclusions",
            "Motorcycles",
            "Specified replacement equipment",
        ],
        requirement_topics=[
            "lighting installation",
            "headlamps",
            "signal lamps",
            "adaptive driving beams",
            "photometric performance",
            "lamp aiming",
            "reflex reflectors",
            "retroreflective sheeting",
            "vehicle conspicuity",
            "physical and environmental testing",
        ],
    ),
    fmvss_record(
        regulation_id="fmvss_125",
        number="125",
        aliases=[
            "FMVSS 125",
            "49 CFR 571.125",
        ],
        title="Warning devices",
        regulatory_system=(
            "lighting_and_light_signalling"
        ),
        regulated_object=(
            "Portable warning devices without "
            "self-contained energy sources"
        ),
        scope_summary=(
            "Requirements for portable warning devices carried "
            "in specified buses and trucks and used to warn "
            "approaching traffic of a stopped vehicle."
        ),
        vehicle_applicability=[
            (
                "Buses with a GVWR greater than "
                "10,000 pounds"
            ),
            (
                "Trucks with a GVWR greater than "
                "10,000 pounds"
            ),
        ],
        requirement_topics=[
            "warning triangles",
            "equilateral-triangle configuration",
            "red reflex reflective material",
            "orange fluorescent material",
            "dual-purpose material",
            "entrance angles",
            "observation angles",
            "reflectivity testing",
            "luminance testing",
            "environmental conditioning",
            "protective storage",
            "DOT marking",
        ],
    ),
]


def comparison_pair(
    pair_number: int,
    left_regulation_id: str,
    right_regulation_id: str,
    regulatory_system: str,
    comparison_focus: str,
    overlap_summary: str,
    comparable_topics: list[str],
    scope_differences: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "pair_number": pair_number,
        "pair_id": (
            f"{left_regulation_id}__{right_regulation_id}"
        ),
        "left_regulation_id": left_regulation_id,
        "right_regulation_id": right_regulation_id,
        "status": "approved",
        "comparison_level": "partial",
        "regulatory_system": regulatory_system,
        "comparison_focus": comparison_focus,
        "overlap_summary": overlap_summary,
        "comparable_topics": comparable_topics,
        "scope_differences": scope_differences,
        "legal_equivalence": False,
        "verification_reference": (
            "data/regulations/comparability_verification.md "
            f"— Pair {pair_number}"
        ),
        "source_reviewed_on": REVIEW_DATE,
    }


pairs = [
    comparison_pair(
        1,
        "unece_r13h",
        "fmvss_135",
        "braking_and_stability",
        "light_vehicle_braking",
        (
            "Both frameworks regulate light-vehicle braking "
            "performance, system behavior, warning functions, "
            "and defined test procedures."
        ),
        [
            "service braking",
            "parking braking",
            "stopping performance",
            "brake-system failure",
            "anti-lock braking",
            "warning signals",
            "vehicle loading conditions",
            "test procedures",
        ],
        [
            (
                "Vehicle categories and applicability rules "
                "do not map one-to-one."
            ),
            (
                "Stopping tests, loading conditions, thresholds, "
                "and measurement procedures differ."
            ),
            (
                "UNECE type approval and United States "
                "self-certification use different frameworks."
            ),
        ],
    ),
    comparison_pair(
        2,
        "unece_r140",
        "fmvss_126",
        "braking_and_stability",
        "electronic_stability_control",
        (
            "Both frameworks regulate electronic stability "
            "control functionality, vehicle response, "
            "malfunction detection, and performance testing."
        ),
        [
            "electronic stability control",
            "yaw stability",
            "lateral responsiveness",
            "system activation",
            "malfunction detection",
            "driver telltales",
            "dynamic test maneuvers",
            "performance thresholds",
        ],
        [
            (
                "Vehicle categories and United States weight "
                "limits differ."
            ),
            (
                "Test maneuvers, instrumentation, thresholds, "
                "and calculation methods are not identical."
            ),
            (
                "Approval and certification systems differ."
            ),
        ],
    ),
    comparison_pair(
        3,
        "unece_r14",
        "fmvss_210",
        "occupant_restraint",
        "seat_belt_anchorages",
        (
            "Both frameworks regulate seat-belt anchorage "
            "location, structural strength, load application, "
            "and anchorage testing."
        ),
        [
            "seat-belt anchorages",
            "anchorage location",
            "anchorage geometry",
            "anchorage strength",
            "load application",
            "seating positions",
            "vehicle structure",
            "test procedures",
        ],
        [
            (
                "UN R14 includes additional ISOFIX-related "
                "anchorage provisions beyond the core Pair 3 focus."
            ),
            (
                "Vehicle categories, loads, force directions, "
                "and test fixtures differ."
            ),
            (
                "Type-approval and self-certification systems differ."
            ),
        ],
    ),
    comparison_pair(
        4,
        "unece_r16",
        "fmvss_209",
        "occupant_restraint",
        "seat_belt_assemblies",
        (
            "Both frameworks regulate seat-belt assembly "
            "components, strength, operation, durability, "
            "and testing."
        ),
        [
            "seat-belt assemblies",
            "webbing",
            "buckles",
            "retractors",
            "attachment hardware",
            "strength",
            "durability",
            "marking and instructions",
        ],
        [
            (
                "UN R16 has a broader vehicle and restraint-system "
                "scope than FMVSS 209."
            ),
            (
                "Assembly classifications, conditioning, test "
                "loads, and acceptance criteria differ."
            ),
            (
                "Installation and certification structures differ."
            ),
        ],
    ),
    comparison_pair(
        5,
        "unece_r145",
        "fmvss_225",
        "occupant_restraint",
        "child_restraint_anchorages",
        (
            "Both frameworks regulate standardized child-restraint "
            "anchorages, geometry, strength, accessibility, "
            "marking, and testing."
        ),
        [
            "lower anchorages",
            "ISOFIX and LATCH systems",
            "top tether anchorages",
            "anchorage geometry",
            "anchorage strength",
            "marking",
            "accessibility",
            "load testing",
        ],
        [
            (
                "ISOFIX, i-Size, and LATCH terminology and "
                "classifications do not map one-to-one."
            ),
            (
                "Vehicle applicability and required seating "
                "positions differ."
            ),
            (
                "Geometry, loads, fixtures, and approval systems differ."
            ),
        ],
    ),
    comparison_pair(
        6,
        "unece_r48",
        "fmvss_108",
        "lighting_and_light_signalling",
        "vehicle_lighting_installation",
        (
            "Both frameworks regulate vehicle-level installation "
            "of lighting and light-signalling functions."
        ),
        [
            "number of lamps",
            "mounting location",
            "mounting height",
            "geometric visibility",
            "orientation",
            "activation",
            "tell-tales",
            "headlighting",
            "turn and stop signals",
            "side markers and conspicuity",
        ],
        [
            (
                "UNECE and United States vehicle categories "
                "do not map one-to-one."
            ),
            (
                "Permitted lamp functions, installation geometry, "
                "activation rules, and numerical limits differ."
            ),
            (
                "R48 is primarily an installation regulation, "
                "while FMVSS 108 combines installation and "
                "equipment-performance requirements."
            ),
        ],
    ),
    comparison_pair(
        7,
        "unece_r148",
        "fmvss_108",
        "lighting_and_light_signalling",
        "light_signalling_device_performance",
        (
            "Both frameworks regulate multiple corresponding "
            "light-signalling lamp categories and their optical, "
            "photometric, color, and light-source performance."
        ),
        [
            "registration-plate lamps",
            "direction indicators and turn signals",
            "position and tail lamps",
            "stop lamps",
            "clearance and end-outline lamps",
            "reversing and backup lamps",
            "daytime running lamps",
            "side-marker lamps",
            "luminous intensity",
            "photometric performance",
        ],
        [
            (
                "UN R148 includes manoeuvring lamps and rear fog "
                "lamps without identified direct FMVSS 108 matches."
            ),
            (
                "Device names, classifications, numerical limits, "
                "test grids, and light-source rules differ."
            ),
            (
                "UN type approval and United States "
                "self-certification differ."
            ),
        ],
    ),
    comparison_pair(
        8,
        "unece_r149",
        "fmvss_108",
        "lighting_and_light_signalling",
        "road_illumination_device_performance",
        (
            "Both frameworks regulate headlamp beam functions, "
            "adaptive driving beams, aiming, cutoff, photometric "
            "performance, light sources, and durability."
        ),
        [
            "driving and upper beams",
            "passing and lower beams",
            "adaptive driving beams",
            "beam cutoff",
            "headlamp aiming",
            "photometric test points",
            "luminous intensity",
            "light sources",
            "plastic lenses",
            "environmental testing",
        ],
        [
            (
                "Adaptive front-lighting systems, front fog lamps, "
                "and cornering lamps were not matched one-to-one."
            ),
            (
                "Beam terminology, patterns, test grids, aiming "
                "methods, and numerical criteria differ."
            ),
            (
                "Vehicle applicability and certification "
                "frameworks differ."
            ),
        ],
    ),
    comparison_pair(
        9,
        "unece_r150",
        "fmvss_108",
        "lighting_and_light_signalling",
        "retro_reflective_device_performance",
        (
            "Both frameworks regulate reflex reflectors, "
            "retroreflective materials, conspicuity products, "
            "photometric geometry, color, and physical testing."
        ),
        [
            "retro-reflectors and reflex reflectors",
            "retro-reflective materials and sheeting",
            "vehicle conspicuity",
            "photometric measurements",
            "observation angles",
            "entrance angles",
            "colorimetric performance",
            "dimensions",
            "environmental durability",
            "product marking",
        ],
        [
            (
                "UN R150 additionally covers heavy-vehicle plates, "
                "slow-moving-vehicle plates, and warning triangles."
            ),
            (
                "UNECE classes do not map one-to-one to FMVSS "
                "reflector and sheeting classifications."
            ),
            (
                "Measurement geometry, material requirements, "
                "physical tests, and certification systems differ."
            ),
        ],
    ),
    comparison_pair(
        10,
        "unece_r104",
        "fmvss_108",
        "lighting_and_light_signalling",
        "vehicle_conspicuity_marking_requirements",
        (
            "Both frameworks regulate conspicuity markings for "
            "specified heavy vehicles using retro-reflective "
            "materials on vehicle sides and rears."
        ),
        [
            "heavy-vehicle conspicuity",
            "retro-reflective marking materials",
            "side markings",
            "rear markings",
            "strip and sheeting dimensions",
            "placement and spacing",
            "color",
            "photometric performance",
            "observation and entrance angles",
            "durability and identification",
        ],
        [
            (
                "R104 uses UNECE vehicle categories, while FMVSS "
                "108 uses vehicle definitions, width, and GVWR."
            ),
            (
                "Strip patterns, coverage, colors, placement, "
                "and certification grades differ."
            ),
            (
                "R104 type approval and FMVSS self-certification "
                "use different systems."
            ),
        ],
    ),
    comparison_pair(
        11,
        "unece_r27",
        "fmvss_125",
        "lighting_and_light_signalling",
        "portable_advance_warning_triangle_performance",
        (
            "Both frameworks regulate portable equilateral "
            "warning triangles using reflective and fluorescent "
            "materials to warn approaching traffic of a stopped "
            "vehicle."
        ),
        [
            "portable warning triangles",
            "daytime and nighttime visibility",
            "equilateral-triangle configuration",
            "reflective material",
            "fluorescent material",
            "combined-purpose material",
            "luminance and reflectivity",
            "entrance and observation angles",
            "structural stability",
            "environmental durability",
            "storage and instructions",
            "marking and testing",
        ],
        [
            (
                "FMVSS 125 applies specifically to devices for "
                "buses and trucks over 10,000 pounds GVWR."
            ),
            (
                "UNECE Type 1 and Type 2 classifications do not "
                "map one-to-one to FMVSS material options."
            ),
            (
                "Dimensions, optical geometry, test methods, "
                "numerical limits, and certification systems differ."
            ),
            (
                "UN R27 has transitional status linked to "
                "the entry into force of UN R150."
            ),
        ],
    ),
]


def validate_before_write() -> None:
    record_schema_path = (
        DATA_DIR / "schemas/regulation_record.schema.json"
    )
    pair_schema_path = (
        DATA_DIR
        / "schemas/regulation_comparison_pair.schema.json"
    )

    record_schema = json.loads(
        record_schema_path.read_text(encoding="utf-8")
    )
    pair_schema = json.loads(
        pair_schema_path.read_text(encoding="utf-8")
    )

    record_fields = set(record_schema["properties"])
    pair_fields = set(pair_schema["properties"])

    if len(records) != 18:
        raise ValueError(
            f"Expected 18 records, found {len(records)}."
        )

    regulation_ids = [
        record["regulation_id"]
        for record in records
    ]

    if len(set(regulation_ids)) != 18:
        raise ValueError(
            "Regulation IDs are not unique."
        )

    for record in records:
        if set(record) != record_fields:
            missing = record_fields - set(record)
            extra = set(record) - record_fields

            raise ValueError(
                f"Invalid fields for "
                f"{record['regulation_id']}: "
                f"missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )

        if record["schema_version"] != "1.0":
            raise ValueError(
                "Invalid record schema version."
            )

        if not re.fullmatch(
            r"(unece|fmvss)_[a-z0-9]+",
            record["regulation_id"],
        ):
            raise ValueError(
                f"Invalid regulation ID: "
                f"{record['regulation_id']}"
            )

        if record["verification_status"] != "verified":
            raise ValueError(
                f"Unverified record: "
                f"{record['regulation_id']}"
            )

    if len(pairs) != 11:
        raise ValueError(
            f"Expected 11 pairs, found {len(pairs)}."
        )

    pair_ids = [
        pair["pair_id"]
        for pair in pairs
    ]

    if len(set(pair_ids)) != 11:
        raise ValueError(
            "Comparison-pair IDs are not unique."
        )

    expected_pair_numbers = list(range(1, 12))
    actual_pair_numbers = [
        pair["pair_number"]
        for pair in pairs
    ]

    if actual_pair_numbers != expected_pair_numbers:
        raise ValueError(
            "Pair numbers are not exactly 1 through 11."
        )

    known_ids = set(regulation_ids)

    for pair in pairs:
        if set(pair) != pair_fields:
            missing = pair_fields - set(pair)
            extra = set(pair) - pair_fields

            raise ValueError(
                f"Invalid fields for {pair['pair_id']}: "
                f"missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )

        if pair["left_regulation_id"] not in known_ids:
            raise ValueError(
                f"Unknown left regulation: "
                f"{pair['left_regulation_id']}"
            )

        if pair["right_regulation_id"] not in known_ids:
            raise ValueError(
                f"Unknown right regulation: "
                f"{pair['right_regulation_id']}"
            )

        expected_pair_id = (
            f"{pair['left_regulation_id']}__"
            f"{pair['right_regulation_id']}"
        )

        if pair["pair_id"] != expected_pair_id:
            raise ValueError(
                f"Pair ID mismatch: {pair['pair_id']}"
            )

        if pair["status"] != "approved":
            raise ValueError(
                f"Pair is not approved: {pair['pair_id']}"
            )

        if pair["comparison_level"] != "partial":
            raise ValueError(
                f"Unexpected comparison level: "
                f"{pair['pair_id']}"
            )

        if pair["legal_equivalence"] is not False:
            raise ValueError(
                f"Legal equivalence must be false: "
                f"{pair['pair_id']}"
            )


def write_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with RECORDS_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            )

    PAIRS_PATH.write_text(
        json.dumps(
            pairs,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    validate_before_write()
    write_data()

    print(
        f"Created {len(records)} regulation records."
    )
    print(
        f"Created {len(pairs)} comparison pairs."
    )
    print("Built-in validation passed.")
