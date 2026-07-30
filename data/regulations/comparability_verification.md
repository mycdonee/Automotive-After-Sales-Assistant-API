# Regulation Comparability Verification

## Purpose

This document records the source-based verification used to decide whether candidate UNECE and United States vehicle regulations can be included in structured comparison workflows.

A comparison relationship does not imply that two regulations are legally equivalent.

Each candidate pair is reviewed for overlap in:

- regulated system
- regulated object or function
- vehicle applicability
- requirement topics
- performance dimensions
- test dimensions

The verification was last reviewed on 2026-07-29.

## Comparison Levels

### `direct`

The regulations address substantially the same regulated object and have closely aligned vehicle applicability and requirement dimensions.

### `partial`

The regulations address the same regulated object and contain several directly comparable requirements, but their vehicle scope, exclusions, terminology, regulatory structure, or test provisions are not fully aligned.

### `system_level`

The regulations concern the same broad vehicle system, but regulate different objects or divide the requirements differently across documents.

## Source Version Notes

### UNECE

The local research set currently reviewed contains:

- UN Regulation No. 13-H, Revision 4
- UN Regulation No. 13-H, Revision 4, Amendments 1–6
- UN Regulation No. 140, original regulation
- UN Regulation No. 140, Amendments 1–6
- UN Regulation No. 14, Revision 7
- UN Regulation No. 14, Revision 7, Amendments 1–4
- UN Regulation No. 16, Revision 10
- UN Regulation No. 16, Revision 10, Corrigendum 1
- UN Regulation No. 16, Revision 10, Amendments 1–6
- UN Regulation No. 16, Revision 11, Amendments 1–2
- UN Regulation No. 145, original regulation
- UN Regulation No. 145, Amendments 1–4
- UN Regulation No. 48, Revision 13
- UN Regulation No. 48, Revision 13, Amendments 1–3
- UN Regulation No. 48, Revision 14, Amendments 1–6
- UN Regulation No. 48, Revision 14, Amendment 6, Corrigendum 1
- UN Regulation No. 148, original regulation
- UN Regulation No. 148, Amendments 1–5
- UN Regulation No. 148, Revision 1, Amendments 1–2
- UN Regulation No. 149, original regulation
- UN Regulation No. 149, Amendments 1–6
- UN Regulation No. 149, Revision 1, Amendments 1–3
- UN Regulation No. 150, original regulation
- UN Regulation No. 150, Amendments 1–5
- UN Regulation No. 150, Revision 1, Amendments 1–2
- UN Regulation No. 150, Revision 1, Amendment 2, Corrigendum 1
- UN Regulation No. 104, Revision 1
- UN Regulation No. 104, Revision 1, Corrigenda 1–2
- UN Regulation No. 104, Revision 1, Amendments 1–4
- UN Regulation No. 27, Revision 3, 05 series

The UNECE PDF files are retained as ignored local research artifacts and are not committed to the repository.

### United States

The local research set currently reviewed contains:

- 49 CFR § 571.135 XML, eCFR version dated 2026-07-27
- 49 CFR § 571.126 XML, eCFR version dated 2026-07-27
- 49 CFR § 571.210 XML, eCFR version dated 2026-07-27
- 49 CFR § 571.209 XML, eCFR version dated 2026-07-27
- 49 CFR § 571.225 XML, eCFR version dated 2026-07-27
- 49 CFR § 571.108 XML, eCFR version dated 2026-07-27
- 49 CFR § 571.125 XML, eCFR version dated 2026-07-27

The XML files were downloaded from the official eCFR Versioner API and are retained as ignored local research artifacts.

The eCFR content-version date and the project verification date are separate values.

## Pair 1 — UN R13-H and FMVSS 135

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `braking_and_vehicle_stability`
- Comparison focus: `light_vehicle_braking`

### UNECE Regulation

- Official identifier: UN Regulation No. 13-H
- Title: Uniform provisions concerning the approval of passenger cars with regard to braking
- Reviewed version: Revision 4 with Amendments 1–6
- Official vehicle categories:
  - M1
  - N1

The reviewed scope applies to the braking of vehicles in categories M1 and N1.

The reviewed exclusions include:

- vehicles with a design speed not exceeding 25 km/h
- vehicles fitted for disabled drivers
- approval of vehicle ESC and brake-assist systems
- vehicles without manual braking controls intended for normal operation

The fourth exclusion was introduced by Revision 4, Amendment 5.

The reference to paragraph 1.2.11 in Amendment 6 belongs to Annex 3 test provisions and does not modify the top-level scope.

### United States Standard

- Official identifier: FMVSS No. 135
- Citation: 49 CFR 571.135
- Title: Light vehicle brake systems
- Reviewed eCFR version: 2026-07-27

The standard specifies requirements for service brake and associated parking brake systems.

It applies to:

- passenger cars
- multipurpose passenger vehicles
- trucks
- buses

For multipurpose passenger vehicles, trucks, and buses, the stated GVWR limit is 3,500 kilograms or less.

### Comparable Requirement Topics

The reviewed documents support comparison of:

- service brake system requirements
- parking brake system requirements
- stopping performance
- brake warning functions
- brake-system failure performance
- cold braking effectiveness
- hot braking performance
- wheel-lock and stability-related braking conditions
- test loads and test conditions
- electrically actuated and regenerative braking provisions

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UNECE categories M1 and N1 do not map one-to-one to the United States vehicle classes.
- FMVSS 135 also names multipurpose passenger vehicles, trucks, and buses within its stated mass limit.
- UN R13-H contains explicit scope exclusions that are not expressed in the same form in FMVSS 135.
- FMVSS 135 includes manufacturing-date provisions in its application section.
- The two frameworks organize approval, performance requirements, testing, and transitional provisions differently.

### Conclusion

The regulations are directly comparable for several braking requirements within their overlapping light-vehicle scope.

The complete regulations do not have identical applicability. The pair is therefore approved with a `partial` comparison level.

## Pair 2 — UN R140 and FMVSS 126

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `braking_and_vehicle_stability`
- Comparison focus: `electronic_stability_control`

### UNECE Regulation

- Official identifier: UN Regulation No. 140
- Title: Uniform provisions concerning the approval of passenger cars with regard to Electronic Stability Control systems
- Reviewed version: Original regulation with Amendments 1–6
- Official vehicle categories:
  - M1
  - N1

The reviewed scope applies to the approval of vehicles in categories M1 and N1 with regard to their electronic stability control systems.

The reviewed exclusions include:

- vehicles with a design speed not exceeding 25 km/h
- vehicles fitted for disabled drivers

No amendment to the top-level scope was identified in Amendments 1–6 during the current review.

### United States Standard

- Official identifier: FMVSS No. 126
- Citation: 49 CFR 571.126
- Title: Electronic stability control systems for light vehicles
- Reviewed eCFR version: 2026-07-27

The standard establishes performance and equipment requirements for electronic stability control systems.

It applies to:

- passenger cars
- multipurpose passenger vehicles
- trucks
- buses

The stated GVWR limit is 4,536 kilograms or less.

### Comparable Requirement Topics

The reviewed documents support comparison of:

- ESC equipment requirements
- individual-wheel braking intervention
- vehicle yaw response
- lateral vehicle response
- steering-input monitoring
- oversteer and understeer control
- engine-torque intervention
- ESC malfunction warning
- ESC control and default-mode behaviour
- dynamic stability test procedures
- Sine with Dwell testing

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UNECE categories M1 and N1 do not map one-to-one to the United States vehicle classes.
- FMVSS 126 includes buses and vehicles up to a stated GVWR of 4,536 kilograms.
- The two frameworks use different approval structures and legal terminology.
- Detailed equipment, test, timing, measurement, and transitional provisions must be compared field by field.
- Similar technical objectives do not establish legal equivalence.

### Conclusion

The regulations address the same regulated function and contain multiple directly comparable ESC requirement dimensions.

Their complete vehicle applicability and regulatory structures are not identical. The pair is therefore approved with a `partial` comparison level.

## Pair 3 — UN R14 and FMVSS 210

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `occupant_restraint`
- Comparison focus: `seat_belt_anchorages`

### UNECE Regulation

- Official identifier: UN Regulation No. 14
- Title: Safety-belt anchorages
- Reviewed version: Revision 7 with Amendments 1–4
- Official vehicle categories:
  - M
  - N1

The reviewed scope applies to vehicles in categories M and N1 with regard to anchorages for safety-belts intended for adult occupants of forward-facing, rearward-facing, or side-facing seats.

No amendment to the top-level scope was identified in Revision 7, Amendments 1–4 during the current review.

### United States Standard

- Official identifier: FMVSS No. 210
- Citation: 49 CFR 571.210
- Title: Seat belt assembly anchorages
- Reviewed eCFR version: 2026-07-27

The standard establishes requirements for seat belt assembly anchorages to support effective occupant restraint, ensure proper anchorage location, and reduce the likelihood of anchorage failure.

It applies to:

- passenger cars
- multipurpose passenger vehicles
- trucks
- buses
- school buses

### Comparable Requirement Topics

The reviewed documents support comparison of:

- seat-belt anchorage requirements
- anchorage types
- designated seating positions
- pelvic restraint anchorages
- upper-torso restraint anchorages
- anchorage strength
- anchorage location
- force-application direction
- test loads
- force duration
- test procedures
- attachment to the vehicle or seat structure

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UNECE categories M and N1 do not map one-to-one to the United States vehicle classes.
- FMVSS 210 explicitly includes school buses and contains school-bus-specific provisions.
- UN R14 describes its scope through UNECE vehicle categories and adult-occupant seat orientations.
- FMVSS 210 connects several requirements to designated seating positions and other FMVSS standards.
- The two frameworks use different anchorage classifications, test devices, force values, approval structures, and legal terminology.
- Detailed strength, geometry, force, and test requirements must be compared field by field.

### Conclusion

The regulations address the same regulated object and contain multiple directly comparable anchorage requirement dimensions.

Their complete vehicle applicability, requirement structure, and test provisions are not identical. The pair is therefore approved with a `partial` comparison level.

## Pair 4 — UN R16 and FMVSS 209

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `occupant_restraint`
- Comparison focus: `seat_belt_assemblies`

### UNECE Regulation

- Official identifier: UN Regulation No. 16
- Title: Safety-belts
- Reviewed source chain:
  - Revision 10
  - Revision 10, Corrigendum 1
  - Revision 10, Amendments 1–6
  - Revision 11, Amendments 1–2
- Latest reviewed top-level scope: Revision 11, Amendment 2
- Official vehicle categories:
  - M
  - N
  - O
  - L2
  - L4
  - L5
  - L6
  - L7
  - T

The latest reviewed scope applies to safety-belts and restraint systems intended for separate use as individual fittings by adult occupants of forward-facing, rearward-facing, and side-facing seats.

At the request of the manufacturer, it also applies to safety-belts intended for side-facing seats in specified category M3 vehicles.

Revision 11, Amendment 2 narrows the reviewed top-level scope to safety-belt and restraint-system components.

Vehicle-installation requirements, child-restraint installation, ISOFIX and i-Size installation, and safety-belt-reminder requirements are described in the amendment as having been moved to separate UN Regulations.

The paragraph 1 amendment identified in Revision 10, Amendment 6 belongs to Annex 18 and does not modify the top-level scope.

The Revision 11 consolidated version was not available in the reviewed official catalogue. The local research chain therefore retains Revision 10 and its corrigendum and amendments together with the formally published Revision 11 Amendments 1–2.

### United States Standard

- Official identifier: FMVSS No. 209
- Citation: 49 CFR 571.209
- Title: Seat belt assemblies
- Reviewed eCFR version: 2026-07-27

The standard specifies requirements for seat belt assemblies used in:

- passenger cars
- multipurpose passenger vehicles
- trucks
- buses

### Comparable Requirement Topics

The reviewed documents support comparison of:

- seat-belt assembly construction
- belt types
- pelvic and upper-torso restraints
- webbing width
- webbing breaking strength
- webbing elongation
- abrasion resistance
- environmental resistance
- buckles
- buckle release
- adjustment hardware
- attachment hardware
- retractors
- load-limiting features
- corrosion resistance
- temperature resistance
- component strength
- conditioning and test procedures
- usage and installation instructions

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UNECE vehicle categories do not map one-to-one to the United States vehicle classes.
- UN R16 covers a wider set of vehicle categories, including categories not directly represented in FMVSS 209 application terminology.
- UN R16 includes an optional application concerning safety-belts for specified side-facing seats in category M3 vehicles.
- Belt classifications, component definitions, approval procedures, test forces, conditioning methods, and acceptance criteria differ between the frameworks.
- FMVSS 209 connects some requirements and exemptions to other United States standards, including FMVSS 208.
- Detailed numerical and procedural requirements must be compared field by field.

### Conclusion

The regulations directly overlap at the seat-belt assembly component level and contain multiple comparable construction, strength, durability, hardware, and test requirements.

Their complete vehicle applicability and detailed technical provisions are not identical. The pair is therefore approved with a `partial` comparison level.

## Pair 5 — UN R145 and FMVSS 225

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `occupant_restraint`
- Comparison focus: `child_restraint_anchorages`

### UNECE Regulation

- Official identifier: UN Regulation No. 145
- Title: ISOFIX anchorage systems, ISOFIX top tether anchorages and i-Size seating positions
- Reviewed source chain:
  - Original regulation
  - Amendments 1–4
- Latest reviewed top-level scope: Amendment 4, 01 series
- Primary vehicle category:
  - M1

The latest reviewed scope applies to category M1 vehicles with regard to:

- ISOFIX anchorage systems
- ISOFIX top-tether anchorages
- lower-tether anchorages intended for child restraint systems

Other vehicle categories fitted with ISOFIX anchorages or lower-tether anchorages must also comply with the applicable provisions.

The regulation also applies to vehicles of any category with regard to i-Size seating positions when such positions are defined by the vehicle manufacturer.

Amendment 4 introduces the 01 series of amendments and adds lower-tether anchorage definitions, positioning zones, design provisions, strength requirements, test procedures, and transitional provisions.

### United States Standard

- Official identifier: FMVSS No. 225
- Citation: 49 CFR 571.225
- Title: Child restraint anchorage systems
- Reviewed eCFR version: 2026-07-27

The standard establishes location and strength requirements for child-restraint anchorage systems.

It applies to:

- passenger cars
- trucks and multipurpose passenger vehicles with a GVWR of 3,855 kilograms or less
- buses, including school buses, with a GVWR of 4,536 kilograms or less

The reviewed exclusions include:

- walk-in van-type vehicles
- vehicles manufactured exclusively for the United States Postal Service
- shuttle buses
- funeral coaches

A child-restraint anchorage system under FMVSS 225 consists of:

- two lower anchorages
- one tether anchorage

### Comparable Requirement Topics

The reviewed documents support comparison of:

- child-restraint anchorage systems
- paired lower-anchor concepts
- tether and top-tether anchorages
- designated seating positions
- anchorage positioning
- anchorage spacing
- anchorage strength
- structural load transfer
- force-application direction
- force-application devices
- test loads
- displacement and deformation criteria
- anchorage marking and identification
- accessibility and clearance
- attachment to vehicle or seat structures

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UNECE vehicle categories do not map one-to-one to the United States vehicle classes.
- FMVSS 225 uses vehicle-class, GVWR, manufacturing-date, and exclusion provisions that are not structured in the same way as UN R145.
- UN R145 includes i-Size seating-position and vehicle-floor support-leg requirements.
- UN R145 Amendment 4 introduces lower-tether anchorages for anti-rotation devices used with certain rear-facing child restraints.
- A UN R145 lower-tether anchorage is not equivalent to an FMVSS 225 lower anchorage.
- The frameworks use different anchorage terminology, fixtures, positioning zones, force values, deformation criteria, markings, and approval procedures.
- Detailed numerical and procedural requirements must be compared field by field.

### Conclusion

The regulations address the same broad regulated object and contain multiple directly comparable requirements for child-restraint anchorage location, strength, tethering, identification, and testing.

Their complete vehicle applicability and technical architecture are not identical. In particular, similarly named lower-anchor concepts must not be treated as equivalent without field-level verification.

The pair is therefore approved with a `partial` comparison level.

## Pair 6 — UN R48 and FMVSS 108

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `lighting_and_light_signalling`
- Comparison focus: `vehicle_lighting_installation`

### UNECE Regulation

- Official identifier: UN Regulation No. 48
- Title: Installation of lighting and light-signalling devices
- Reviewed source chain:
  - Revision 13
  - Revision 13, Amendments 1–3
  - Revision 14, Amendments 1–6
  - Revision 14, Amendment 6, Corrigendum 1
- Latest reviewed top-level scope: Revision 13 consolidated scope
- Official vehicle categories:
  - M
  - N
  - O

The regulation applies to vehicles of categories M and N and their category O trailers with regard to the installation of lighting and light-signalling devices.

The reviewed scope concerns vehicle-level installation rather than only the approval of an individual lamp or reflective device.

The reviewed 08-series source chain begins with Revision 13, Amendment 3. No change to the top-level Paragraph 1 Scope was identified in that amendment, in Revision 14 Amendments 1–6, or in Revision 14 Amendment 6 Corrigendum 1.

The Revision 14 consolidated text was listed as forthcoming in the reviewed official catalogue. The local research chain therefore retains the Revision 13 consolidated text together with the formally published 08-series amendments and corrigendum.

### United States Standard

- Official identifier: FMVSS No. 108
- Citation: 49 CFR 571.108
- Title: Lamps, reflective devices, and associated equipment
- Reviewed eCFR version: 2026-07-27

The standard specifies requirements for original and replacement lamps, reflective devices, and associated equipment.

It applies to:

- passenger cars
- multipurpose passenger vehicles
- trucks
- buses
- trailers, except pole trailers and trailer converter dollies
- motorcycles
- specified retroreflective sheeting and reflex reflectors
- replacement lamps, reflective devices, and associated equipment

### Comparable Requirement Topics

The reviewed documents support vehicle-installation comparison of:

- required lighting and light-signalling devices
- mandatory and optional lamps
- lamp quantity
- lamp color
- mounting location
- mounting height
- longitudinal and lateral positioning
- symmetry and separation
- geometric visibility
- obstruction and clearance
- device activation
- electrical connections
- headlighting installation
- dipped-beam and upper-beam operation
- turn-signal lamps
- stop lamps
- position lamps
- side-marker lamps
- reflex reflectors
- conspicuity markings and treatments
- driver indications and tell-tales

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UNECE vehicle categories do not map one-to-one to the United States vehicle classes.
- UN R48 primarily regulates vehicle-level installation and type approval.
- FMVSS 108 also includes device-performance requirements and replacement equipment.
- FMVSS 108 includes motorcycles, while the reviewed UN R48 scope covers categories M, N, and O.
- FMVSS 108 contains specific trailer exclusions that are not expressed through the same structure as UN R48.
- UNECE distributes device requirements across UN Regulations Nos. 148, 149, and 150, while FMVSS 108 consolidates many installation and device requirements in one standard.
- The frameworks use different lamp classifications, required-device tables, colors, mounting limits, activation rules, photometric references, testing structures, and approval procedures.
- Detailed numerical and procedural requirements must be compared field by field.

### Conclusion

The regulations contain substantial overlap in vehicle-level requirements concerning which lighting and light-signalling devices must be installed and how those devices are positioned, made visible, activated, and integrated into the vehicle.

Their complete regulatory scope and technical architecture are not identical. The pair is therefore approved with a `partial` comparison level.

## Pair 7 — UN R148 and FMVSS 108

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `lighting_and_light_signalling`
- Comparison focus: `light_signalling_device_performance`

### UNECE Regulation

- Official identifier: UN Regulation No. 148
- Title: Light Signalling Devices
- Reviewed source chain:
  - Original regulation
  - Amendments 1–5
  - Revision 1, Amendments 1–2
- Latest reviewed top-level scope: Amendment 5, 01 series
- Date of entry into force of the 01 series: 4 January 2023
- Regulated object: individual light-signalling devices and lamps

The reviewed 01-series scope applies to:

- rear-registration plate illuminating lamps
- direction indicator lamps
- position lamps
- stop lamps
- end-outline marker lamps
- reversing lamps
- manoeuvring lamps
- rear fog lamps
- parking lamps
- daytime running lamps
- side marker lamps

Amendment 5 introduces the 01 series and contains a complete regulation text.

No later change to the top-level Scope was identified in Revision 1 Amendments 1–2.

### United States Standard

- Official identifier: FMVSS No. 108
- Citation: 49 CFR 571.108
- Title: Lamps, reflective devices, and associated equipment
- Reviewed eCFR version: 2026-07-27

FMVSS 108 combines vehicle-level requirements with requirements for original and replacement lamps, reflective devices, and associated equipment.

The reviewed text contains corresponding or closely related device categories including:

- license-plate lamps
- turn-signal lamps
- taillamps and position-lighting functions
- stop lamps
- clearance lamps
- backup lamps
- parking lamps
- daytime running lamps
- side-marker lamps

### Comparable Requirement Topics

The reviewed documents support comparison of:

- registration-plate illumination
- direction-indicator and turn-signal lamps
- position and tail lamps
- stop lamps
- end-outline and clearance lamps
- reversing and backup lamps
- parking lamps
- daytime running lamps
- side-marker lamps
- lamp categories and classifications
- color requirements
- luminous intensity
- candela limits
- photometric performance
- light-source requirements
- variable-intensity functions
- optical characteristics
- test procedures
- environmental and durability requirements
- approval and identification markings

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UN R148 is primarily an individual-device type-approval regulation.
- FMVSS 108 combines device requirements, vehicle installation requirements, original equipment, and replacement equipment in one standard.
- UN R148 includes manoeuvring lamps and rear fog lamps for which no direct FMVSS 108 textual equivalent was identified in the reviewed search.
- Sequential activation was explicitly identified in UN R148 but not through the reviewed FMVSS 108 phrase search.
- The exact phrase `light distribution` was identified in UN R148 but not in the reviewed FMVSS 108 search; photometric and luminous-intensity requirements nevertheless occur in both frameworks.
- Environmental and durability test structures differ between the frameworks.
- Lamp names and classifications do not map one-to-one.
- Numerical intensity limits, color definitions, test grids, reference axes, light-source rules, and acceptance criteria must be compared field by field.
- UNECE type approval and United States self-certification use different regulatory and administrative structures.

### Conclusion

The regulations contain substantial overlap at the light-signalling-device level, including multiple corresponding lamp categories and comparable requirements concerning color, luminous intensity, photometric performance, light sources, variable intensity, and testing.

Their complete regulated scope, terminology, test structures, and approval systems are not identical.

The pair is therefore approved with a `partial` comparison level.

## Pair 8 — UN R149 and FMVSS 108

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `lighting_and_light_signalling`
- Comparison focus: `road_illumination_device_performance`

### UNECE Regulation

- Official identifier: UN Regulation No. 149
- Title: Road illumination devices (lamps) and systems for power-driven vehicles
- Reviewed source chain:
  - Original regulation
  - Amendments 1–6
  - Revision 1, Amendments 1–3
- Current reviewed series: 01 series
- 01-series entry into force: 4 January 2023
- Latest reviewed top-level Scope: Revision 1, Amendment 3
- Latest reviewed Scope amendment entry into force: 22 September 2024
- Regulated object: individual road-illumination devices, lamps, beams, and associated systems

Amendment 6 introduces the 01 series and contains a complete regulation text.

Revision 1 Amendments 1–3 are Supplements 1–3 to the 01 series.

The separately listed Revision 1 consolidated document was still marked as forthcoming when reviewed and was therefore not used as regulatory source text.

Amendments 7–9 belong to the continuing 00-series branch and were intentionally excluded from the current 01-series research chain.

The latest reviewed Scope applies to:

- headlamps emitting a driving-beam and/or an asymmetrical passing-beam for vehicles of categories L, M, N, and T
- adaptive front-lighting systems for vehicles of categories M, N, and L3
- adaptive driving-beam systems for vehicles of category L3
- headlamps emitting a driving-beam and/or a symmetrical passing-beam for vehicles of categories L and T
- front fog lamps for vehicles of categories L3, L4, L5, L7, M, N, and T
- cornering lamps for vehicles of categories M, N, and T

Revision 1 Amendment 3 changes the adaptive front-lighting system Scope from categories M and N to categories M, N, and L3.

### United States Standard

- Official identifier: FMVSS No. 108
- Citation: 49 CFR 571.108
- Title: Lamps, reflective devices, and associated equipment
- Reviewed eCFR version: 2026-07-27

FMVSS 108 combines requirements for vehicle lighting installation, original equipment, replacement equipment, lamps, reflective devices, and associated equipment.

The reviewed text includes requirements and definitions concerning:

- headlamps
- upper beams
- lower beams
- adaptive driving beams
- headlamp aiming
- visual and optical aiming features
- beam cutoffs
- photometric measurements
- luminous intensity
- illuminance and candela values
- reference and optical axes
- light sources and replaceable light sources
- plastic lenses
- color
- environmental and durability testing
- lamp marking and identification

### Comparable Requirement Topics

The reviewed documents support comparison of:

- driving-beam and upper-beam functions
- passing-beam and lower-beam functions
- adaptive driving-beam systems
- forward-road illumination
- beam shape and distribution
- beam cutoff
- visual and instrumental aiming
- horizontal and vertical aim
- photometric test points
- reference axes and optical axes
- luminous-intensity requirements
- illuminance and candela requirements
- glare reduction
- light sources
- replaceable light sources
- LED modules and LED systems
- light color
- plastic lenses
- stability of photometric performance
- dust and contamination testing
- moisture, corrosion, heat, and vibration requirements
- device marking and identification
- test procedures and acceptance criteria

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UN R149 is primarily an individual-device and lighting-system type-approval regulation.
- FMVSS 108 combines device-performance, vehicle-installation, original-equipment, and replacement-equipment provisions.
- UNECE vehicle categories L, M, N, and T do not map one-to-one to United States vehicle classes.
- Adaptive front-lighting systems were identified in UN R149 but not through the reviewed FMVSS 108 phrase search.
- Front fog lamps and cornering lamps were identified in UN R149 but no direct textual counterpart was identified through the reviewed FMVSS 108 search.
- The two frameworks use different terminology for driving and passing beams versus upper and lower beams.
- Their beam patterns, photometric grids, test points, cutoff definitions, aiming procedures, intensity limits, light-source rules, and acceptance criteria differ.
- Their environmental and durability testing structures are not identical.
- UNECE type approval and United States self-certification use different regulatory and administrative structures.
- Detailed numerical and procedural requirements must be compared field by field.

### Conclusion

The regulations contain substantial overlap in road-illumination-device performance, particularly for driving and passing beams, upper and lower beams, adaptive driving beams, aiming, cutoff control, photometric performance, light sources, color, lens requirements, durability, and testing.

Their complete device coverage, vehicle applicability, terminology, technical requirements, and regulatory structures are not identical.

The pair is therefore approved with a `partial` comparison level.

## Pair 9 — UN R150 and FMVSS 108

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `lighting_and_light_signalling`
- Comparison focus: `retro_reflective_device_performance`

### UNECE Regulation

- Official identifier: UN Regulation No. 150
- Title: Retro-reflective devices and markings for power-driven vehicles and their trailers
- Reviewed source chain:
  - Original regulation
  - Amendments 1–5
  - Revision 1, Amendments 1–2
  - Revision 1, Amendment 2, Corrigendum 1
- Current reviewed series: 01 series
- 01-series entry into force: 4 January 2023
- Latest reviewed top-level Scope: Amendment 5
- Regulated object: retro-reflective devices, materials, markings, plates, and advance warning triangles

Amendment 5 introduces the 01 series and contains a complete regulation text.

Revision 1 Amendment 1 is Supplement 1 to the 01 series.

Revision 1 Amendment 2 is Supplement 2 to the 01 series.

Revision 1 Amendment 2 Corrigendum 1 corrects Supplement 2 and belongs to the same 01-series branch.

The separately listed Revision 1 consolidated document was still marked as forthcoming when reviewed and was therefore not used as regulatory source text.

No later change to the top-level Scope was identified in the reviewed Revision 1 amendments or corrigendum.

The latest reviewed Scope applies to:

- retro-reflectors of Classes IA, IB, IIIA, IIIB, and IVA
- retro-reflective marking materials of Classes C, D, E, F, and D/E
- retro-reflective marking plates for heavy and long vehicles of Classes 1–5
- retro-reflective marking plates for slow-moving vehicles of Classes 1 and 2
- advance warning triangles of Types 1 and 2

### United States Standard

- Official identifier: FMVSS No. 108
- Citation: 49 CFR 571.108
- Title: Lamps, reflective devices, and associated equipment
- Reviewed eCFR version: 2026-07-27

FMVSS 108 applies to specified vehicles, replacement lighting equipment, retroreflective sheeting, reflex reflectors, reflective devices, and associated equipment.

The reviewed text includes requirements and definitions concerning:

- reflex reflectors
- retroreflective sheeting
- vehicle conspicuity treatment
- reflective devices
- observation angles
- entrance angles
- luminous-intensity measurements
- photometric test procedures
- color
- dimensions
- optical axes
- marking and identification
- applicable physical test performance requirements

### Comparable Requirement Topics

The reviewed documents support comparison of:

- retro-reflectors and reflex reflectors
- retro-reflective marking materials and retroreflective sheeting
- vehicle conspicuity markings and conspicuity treatment
- photometric measurements
- coefficient of luminous intensity
- retro-reflective performance
- observation angles
- entrance angles
- illumination, observation, reference, and optical axes
- device dimensions
- color and colorimetric requirements
- reflective materials
- applicable physical and durability tests
- marking and identification
- test procedures and acceptance criteria

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UN R150 is primarily a type-approval regulation for several classes of retro-reflective devices, materials, plates, and warning devices.
- FMVSS 108 combines vehicle-installation, equipment-performance, replacement-equipment, reflective-device, and conspicuity provisions.
- UN R150 classes do not map one-to-one to FMVSS device classifications.
- Heavy and long vehicle marking plates were identified in UN R150, but that exact classification was not identified in the reviewed FMVSS 108 text.
- Slow-moving vehicle marking plates were identified in UN R150, but no direct FMVSS 108 textual counterpart was identified.
- Advance warning triangles were identified in UN R150, but no direct FMVSS 108 textual counterpart was identified.
- FMVSS 108 vehicle conspicuity treatment is comparable to only part of the broader UN R150 marking-device Scope.
- The measurement geometries, observation angles, entrance angles, intensity values, color limits, dimensions, material classifications, and test procedures differ.
- The presence of environmental-test terminology in FMVSS 108 does not establish that every listed test applies to every reflex reflector or retroreflective-sheeting category.
- Detailed physical, environmental, numerical, and procedural requirements must be compared field by field.
- UNECE type approval and United States self-certification use different regulatory and administrative structures.

### Conclusion

The regulations contain substantial overlap for retro-reflective-device performance, particularly for reflex reflectors, retroreflective sheeting, conspicuity treatment, photometric measurements, observation and entrance angles, color, dimensions, marking, and applicable physical testing.

Their complete device coverage, classifications, vehicle applicability, numerical requirements, test structures, and regulatory systems are not identical.

The pair is therefore approved with a `partial` comparison level.

## Pair 10 — UN R104 and FMVSS 108

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `lighting_and_light_signalling`
- Comparison focus: `vehicle_conspicuity_marking_requirements`

### UNECE Regulation

- Official identifier: UN Regulation No. 104
- Title: Retro-reflective markings
- Reviewed source chain:
  - Revision 1
  - Revision 1, Corrigenda 1–2
  - Revision 1, Amendments 1–4
- Latest reviewed top-level Scope: Revision 1
- Later reviewed top-level Scope changes: none identified
- Regulated object: retro-reflective marking materials intended for specified vehicle categories

The reviewed Scope applies to retro-reflective markings for vehicles of categories:

- M2
- M3
- N
- O2
- O3
- O4

No later change to the top-level Scope was identified in Corrigenda 1–2 or Amendments 1–4.

The reviewed text contains requirements concerning:

- retro-reflective marking materials
- side and rear markings made with strips
- marking dimensions
- strip width
- approval markings
- colorimetric specifications
- photometric specifications
- coefficient of retro-reflection
- observation angles
- entrance angles
- resistance to external agents
- weathering, cleaning, fuel, and water exposure

The reviewed Revision 1 text specifies a nominal width of 50 mm, with a tolerance of +10/-0 mm, for side and rear marking material.

### United States Standard

- Official identifier: FMVSS No. 108
- Citation: 49 CFR 571.108
- Title: Lamps, reflective devices, and associated equipment
- Reviewed eCFR version: 2026-07-27

FMVSS 108 requires specified trailers and truck tractors to be equipped with a conspicuity system using:

- retroreflective sheeting
- reflex reflectors
- or a combination of sheeting and reflectors

The reviewed requirement applies to each trailer that:

- is at least 2032 mm in overall width
- has a GVWR greater than 10,000 pounds
- is not within the listed excluded trailer uses

It also applies to truck tractors.

The reviewed text includes requirements concerning:

- side and rear conspicuity treatment
- retroreflective sheeting
- reflex reflectors
- red-and-white application patterns
- sheeting width
- placement and spacing
- photometric performance
- observation and entrance angles
- color
- physical testing
- DOT-C2, DOT-C3, and DOT-C4 certification markings

### Comparable Requirement Topics

The reviewed documents support comparison of:

- heavy-vehicle conspicuity markings
- retro-reflective marking materials and retroreflective sheeting
- side markings
- rear markings
- strips and sheeting segments
- marking width and dimensions
- placement and spacing
- white, yellow, and red material requirements
- photometric performance
- coefficient of retro-reflection
- luminous-intensity measurements
- observation angles
- entrance angles
- reference and optical geometry
- resistance to environmental and external agents
- cleaning and weathering resistance
- product marking and identification
- test procedures and acceptance criteria

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UN R104 applies through UNECE vehicle categories M2, M3, N, O2, O3, and O4.
- FMVSS 108 uses United States vehicle definitions, dimensional thresholds, GVWR thresholds, and specified exclusions.
- UNECE vehicle categories do not map one-to-one to United States vehicle classes.
- UN R104 is primarily a type-approval regulation for retro-reflective marking materials.
- FMVSS 108 combines vehicle-installation requirements, material requirements, equipment performance, and self-certification.
- The reviewed R104 text uses side and rear markings made with strips and does not use the same terminology as the FMVSS conspicuity-treatment system.
- FMVSS 108 includes DOT-C2, DOT-C3, and DOT-C4 certification grades that have no one-to-one R104 equivalent.
- Color patterns, strip widths, coverage, spacing, installation positions, vehicle thresholds, and exclusions differ.
- Photometric tables, observation angles, entrance angles, material classifications, durability tests, and acceptance values must be compared field by field.
- UNECE type approval and United States self-certification use different regulatory and administrative structures.

### Conclusion

The regulations contain substantial overlap concerning heavy-vehicle conspicuity markings, retro-reflective materials, side and rear treatment, dimensions, color, photometric performance, observation and entrance angles, durability, and product identification.

Their vehicle applicability, material classifications, installation rules, numerical values, certification structures, and complete regulated scopes are not identical.

The pair is therefore approved with a `partial` comparison level.

## Pair 11 — UN R27 and FMVSS 125

### Decision

- Status: `approved`
- Comparison level: `partial`
- Regulated system: `lighting_and_light_signalling`
- Comparison focus: `portable_advance_warning_triangle_performance`

### UNECE Regulation

- Official identifier: UN Regulation No. 27
- Title: Advance warning triangles
- Reviewed source: Revision 3
- Current reviewed series: 05 series
- 05-series entry into force: 15 October 2019
- Regulated object: portable advance warning triangles intended to be carried on vehicles and placed on the carriageway

Revision 3 incorporates all valid text through:

- Supplement 1 to the 04 series of amendments
- the 05 series of amendments

The reviewed Scope applies to advance warning devices intended:

- to be carried on board vehicles
- to be placed on the carriageway
- to signal the presence of a halted vehicle
- to provide warning during both day and night

The Regulation defines:

- Type 1 advance warning triangles, using separate retro-reflecting and fluorescent components
- Type 2 advance warning triangles, using a single fluorescent retro-reflecting material

The reviewed text includes requirements concerning:

- equilateral-triangle configuration
- shape and dimensions
- optical characteristics
- retro-reflecting devices
- fluorescent materials
- fluorescent retro-reflecting materials
- luminance factor
- coefficient of luminous intensity
- illumination, observation, divergence, and rotation geometry
- structural and mechanical characteristics
- resistance to weathering
- color fastness
- road-surface stability
- protective covers
- instructions for assembly and use
- approval markings
- test procedures
- conformity of production

The transitional provisions state that Contracting Parties applying the Regulation shall cease granting new approvals 24 months after the official entry into force of UN Regulation No. 150.

Extensions of existing approvals and approvals for replacement devices may continue under the specified conditions.

### United States Standard

- Official identifier: FMVSS No. 125
- Citation: 49 CFR 571.125
- Title: Warning devices
- Reviewed eCFR version: 2026-07-27
- Regulated object: portable warning devices without self-contained energy sources

The standard establishes requirements for devices that:

- do not have self-contained energy sources
- are designed to be carried in motor vehicles
- warn approaching traffic of a stopped vehicle
- are not designed to be permanently affixed to the vehicle

Its Application section covers devices designed to be carried in:

- buses with a GVWR greater than 10,000 pounds
- trucks with a GVWR greater than 10,000 pounds

The reviewed requirements include:

- red reflex reflective material
- orange fluorescent material
- dual-purpose orange fluorescent and red reflective material
- application of required material to both faces
- an equilateral-triangle configuration
- erection and storage without tools
- protection against damage and deterioration
- reusable protective containers or protected vehicle compartments
- manufacturer identification
- month and year of manufacture
- DOT marking or an equivalent compliance statement
- instructions for erection and display
- recommended positioning
- stability and durability requirements
- entrance-angle and observation-angle definitions
- reflectivity testing
- luminance testing
- temperature conditioning
- humidity conditioning
- salt-spray testing
- water-immersion testing

### Comparable Requirement Topics

The reviewed documents support comparison of:

- portable roadside warning triangles
- warning of halted or stopped vehicles
- daytime and nighttime visibility
- equilateral-triangle configuration
- triangle shape and dimensions
- red retro-reflective or reflex-reflective material
- fluorescent warning material
- combined fluorescent and reflective material
- application of optical material to the warning device
- coefficient of luminous intensity
- reflectivity
- luminance and luminance factor
- entrance and observation angles
- illumination and measurement geometry
- optical performance
- structural stability
- resistance to wind or movement
- temperature resistance
- moisture and water resistance
- corrosion or salt-spray exposure
- weathering and color-fastness requirements
- protective storage
- device erection and use instructions
- manufacturer and compliance markings
- test procedures and acceptance criteria

### Scope Differences

The regulations must not be treated as fully equivalent because:

- UN R27 applies to specified portable advance warning devices intended to be carried on vehicles without using the same United States GVWR threshold.
- FMVSS 125 specifically applies to devices designed for buses and trucks with a GVWR greater than 10,000 pounds.
- The vehicle applicability of the two frameworks therefore does not map one-to-one.
- UN R27 distinguishes Type 1 and Type 2 warning triangles.
- FMVSS 125 permits separate reflective and fluorescent materials or a specified dual-purpose material but does not use the same UNECE type classification.
- Material definitions, colors, dimensions, optical geometry, measurement units, test distances, test angles, durability procedures, and numerical limits differ.
- Marking and certification requirements differ.
- UN R27 contains transitional provisions connected to the entry into force of UN Regulation No. 150.
- FMVSS 125 does not use the same transitional type-approval structure.
- UNECE type approval and United States self-certification use different regulatory and administrative systems.
- Detailed numerical and procedural requirements must be compared field by field.

### Conclusion

The regulations contain strong functional and technical overlap for portable advance warning triangles, including their intended roadside use, equilateral configuration, reflective and fluorescent materials, optical performance, luminance, measurement angles, stability, durability, instructions, markings, and test procedures.

Their vehicle applicability, material classifications, numerical requirements, test methods, certification systems, and current regulatory status are not identical.

The pair is therefore approved with a `partial` comparison level.

## Verification Boundary

This document records project research decisions for a proof-of-concept regulatory-information system.

It does not provide:

- legal advice
- an authoritative legal interpretation
- a homologation decision
- a compliance determination
- evidence that the compared regulations are interchangeable
