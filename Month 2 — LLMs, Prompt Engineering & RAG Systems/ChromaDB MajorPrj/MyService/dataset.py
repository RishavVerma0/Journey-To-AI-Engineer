# using this amazing script i have generated my new dataset for my custom chatbot application

import csv
import random
from datetime import date, timedelta

random.seed(42)

vehicles = [
    # Maruti Suzuki
    "Maruti Alto K10",
    "Maruti Alto 800",
    "Maruti WagonR",
    "Maruti Swift",
    "Maruti Dzire",
    "Maruti Baleno",
    "Maruti Brezza",
    "Maruti Fronx",
    "Maruti Ertiga",
    "Maruti XL6",
    "Maruti Celerio",
    "Maruti Ignis",
    "Maruti S-Presso",
    "Maruti Eeco",

    # Tata Motors
    "Tata Tiago",
    "Tata Tigor",
    "Tata Altroz",
    "Tata Punch",
    "Tata Nexon",
    "Tata Curvv",
    "Tata Harrier",
    "Tata Safari",

    # Hyundai
    "Hyundai Grand i10 Nios",
    "Hyundai i20",
    "Hyundai Exter",
    "Hyundai Venue",
    "Hyundai Creta",
    "Hyundai Verna",
    "Hyundai Alcazar",

    # Mahindra
    "Mahindra Bolero",
    "Mahindra Bolero Neo",
    "Mahindra Thar",
    "Mahindra Scorpio",
    "Mahindra Scorpio N",
    "Mahindra XUV 3XO",
    "Mahindra XUV700",

    # Honda
    "Honda Amaze",
    "Honda City",
    "Honda Elevate",

    # Toyota
    "Toyota Glanza",
    "Toyota Urban Cruiser Hyryder",
    "Toyota Innova Crysta",
    "Toyota Innova Hycross",
    "Toyota Fortuner",

    # Kia
    "Kia Sonet",
    "Kia Seltos",
    "Kia Carens",
    "Kia Syros",

    # Renault
    "Renault Kwid",
    "Renault Kiger",
    "Renault Triber",

    # Nissan
    "Nissan Magnite",

    # Volkswagen
    "Volkswagen Virtus",
    "Volkswagen Taigun",

    # Skoda
    "Skoda Slavia",
    "Skoda Kushaq",

    # MG
    "MG Comet EV",
    "MG Astor",
    "MG Windsor EV",
    "MG Hector",

    # Citroen
    "Citroen C3",
    "Citroen Basalt",

    # Jeep
    "Jeep Compass",

    # Generic
    "Generic"
]

categories = ["FAQ", "Repair", "Service", "Troubleshooting"]
severities = ["Low", "Medium", "High"]
sources = ["Workshop Manual", "Technician", "FAQ", "Customer Feedback", "Service Bulletin"]

problems = [
    ("Engine overheating", "engine,coolant,radiator,temperature",
     "Check coolant level and top up if low. Inspect radiator for blockages or leaks. "
     "Verify the cooling fan is operating correctly and check the thermostat for proper function. "
     "If overheating persists, inspect the water pump and radiator hoses for damage."),
    ("Battery draining quickly", "battery,electrical,alternator,charging",
     "Test battery voltage using a multimeter; a healthy battery should read around 12.6V. "
     "Check alternator output while the engine is running. Inspect for parasitic drains caused "
     "by aftermarket accessories or faulty wiring. Replace battery if it fails a load test."),
    ("Brake pads squeaking", "brakes,pads,noise,rotor",
     "Inspect brake pads for wear and replace if thickness is below 3mm. Check rotor surface "
     "for grooves or glazing. Apply brake grease to contact points and ensure caliper slides "
     "freely. Test drive to confirm noise is resolved."),
    ("AC not cooling properly", "ac,air conditioning,compressor,refrigerant",
     "Check refrigerant level and recharge if low. Inspect AC compressor clutch engagement. "
     "Clean condenser fins of debris. Check cabin air filter for clogging and replace if dirty."),
    ("Unusual noise from suspension", "suspension,noise,bushings,shock absorber",
     "Inspect shock absorbers and struts for leaks or damage. Check suspension bushings for wear. "
     "Test sway bar links for looseness. Road test over bumps to isolate the source of noise."),
    ("Check engine light on", "engine,warning light,diagnostics,sensor",
     "Connect an OBD-II scanner to retrieve fault codes. Common causes include a faulty oxygen "
     "sensor, loose fuel cap, or catalytic converter issue. Clear codes after repair and re-test."),
    ("Steering wheel vibration", "steering,vibration,tires,alignment",
     "Check tire balance and rotate if uneven wear is present. Inspect wheel alignment "
     "and correct if out of specification. Examine steering rack and tie rod ends for play."),
    ("Fuel efficiency dropped", "fuel,mileage,filter,injector",
     "Inspect air filter and replace if clogged. Check fuel injectors for proper spray pattern. "
     "Verify tire pressure is at recommended levels. Check for dragging brakes affecting mileage."),
    ("Transmission shifting harshly", "transmission,gearbox,fluid,shift",
     "Check transmission fluid level and condition, replace if burnt or low. Inspect for "
     "software updates to the transmission control module. Test drive to confirm smooth shifting."),
    ("Infotainment system freezing", "infotainment,software,touchscreen,update",
     "Perform a soft reset of the infotainment unit. Check for available software updates "
     "and install the latest version. If issue persists, reset to factory settings."),
    ("Clutch feels heavy", "clutch,pedal,hydraulic,cable",
     "Inspect clutch master and slave cylinder for hydraulic fluid leaks. Check clutch cable "
     "for fraying if cable-operated. Bleed the hydraulic system if air is present."),
    ("Windows not working", "windows,electrical,motor,switch",
     "Check window switch for continuity. Inspect window regulator motor for failure. "
     "Verify fuse related to power windows is intact and replace if blown."),
    ("Power steering noise", "steering,power steering,pump,fluid",
     "Check power steering fluid level and top up with recommended fluid. Inspect for "
     "air in the system and bleed if necessary. Examine pump belt tension."),
    ("Oil leak under vehicle", "oil,leak,gasket,seal",
     "Inspect oil pan gasket and valve cover gasket for leaks. Check drain plug torque "
     "and washer condition. Clean area and monitor for new leak sources after repair."),
    ("Wipers not clearing properly", "wipers,washer,blades,streaks",
     "Replace worn wiper blades. Check washer fluid nozzle alignment and clear any blockages. "
     "Inspect wiper motor linkage for wear causing uneven sweep."),
    ("Warning light for tire pressure", "tpms,tires,sensor,pressure",
     "Check all tire pressures against recommended specification and adjust. Inspect TPMS "
     "sensors for battery failure. Reset TPMS system after correcting pressures."),
    ("Car pulling to one side", "alignment,tires,brakes,steering",
     "Check wheel alignment and adjust to specification. Inspect for uneven tire wear. "
     "Verify brake calipers are not sticking on one side."),
    ("Starter motor clicking but not starting", "starter,battery,ignition,electrical",
     "Test battery charge and terminal connections for corrosion. Inspect starter motor "
     "solenoid for failure. Check ignition switch and starter relay."),
    ("Exhaust smoke on startup", "exhaust,smoke,valve seals,piston rings",
     "Blue smoke suggests worn valve seals or piston rings; inspect and replace as needed. "
     "White smoke may indicate coolant entering combustion chamber; check head gasket."),
    ("Service reminder light on", "service,maintenance,reminder,reset",
     "Perform scheduled maintenance including oil and filter change. Reset the service "
     "reminder light using the vehicle's menu or diagnostic tool."),
]

faq_extra = [
    ("What is the recommended service interval?", "service,interval,maintenance,schedule",
     "Most vehicles recommend service every 10,000 km or 12 months, whichever comes first. "
     "Refer to the owner's manual for model-specific intervals and check severe usage schedules "
     "if driven in dusty or stop-and-go conditions."),
    ("How do I check tire pressure correctly?", "tires,pressure,maintenance,safety",
     "Check tire pressure when tires are cold, ideally before driving. Use a reliable gauge "
     "and compare against the value listed on the door jamb sticker, not the tire sidewall."),
    ("What warranty coverage applies to my vehicle?", "warranty,coverage,policy,claim",
     "Standard warranty typically covers manufacturing defects for a specified period or mileage. "
     "Extended warranty options may be available for purchase. Consult the dealership for exact terms."),
    ("How often should brake fluid be replaced?", "brakes,fluid,maintenance,safety",
     "Brake fluid should generally be replaced every 2 years as it absorbs moisture over time, "
     "reducing braking performance. Check owner's manual for exact recommendation."),
    ("What is the correct engine oil grade?", "engine,oil,grade,maintenance",
     "Refer to the owner's manual for the manufacturer-recommended oil viscosity grade, "
     "commonly 5W-30 or 0W-20 depending on engine type and climate conditions."),
]

all_problems = problems + faq_extra

def random_date():
    start = date(2024, 1, 1)
    end = date(2026, 7, 7)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

rows = []
for i in range(1, 2001):
    prob, kw, sol = random.choice(all_problems)
    category = random.choice(categories)
    vehicle = random.choice(vehicles)
    severity = random.choice(severities)
    source = random.choice(sources)
    last_updated = random_date().isoformat()
    rows.append({
        "id": 100 + i,
        "category": category,
        "vehicle": vehicle,
        "problem": prob,
        "solution": sol,
        "keywords": kw,
        "severity": severity,
        "source": source,
        "last_updated": last_updated
    })

with open("customer_support_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["id","category","vehicle","problem","solution",
                    "keywords","severity","source","last_updated"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Done — wrote {len(rows)} rows to customer_support_dataset.csv")