"""
knowledge_base.py
------------------
Curated sustainability knowledge base for GreenSahayak.

Each entry is an ORIGINAL, paraphrased summary of publicly known guidance
(CPCB waste rules, standard water/energy conservation practice) - not a
verbatim copy of any single source. Each entry lists which general
guidance it's adapted from, for transparency, without quoting it directly.

To extend: add more entries in the same shape. More entries = better
retrieval coverage = a more convincing demo.
"""

KNOWLEDGE_BASE = [
    {
        "id": "waste_wet_dry",
        "topic": "Waste Segregation",
        "source": "CPCB Solid Waste Management Rules (general guidance)",
        "content": (
            "Indian municipal waste rules require separating waste at the source into "
            "at least three streams: wet/biodegradable (food scraps, peels, garden waste), "
            "dry/recyclable (paper, plastic, metal, glass), and domestic hazardous waste "
            "(batteries, expired medicines, chemical containers, CFL bulbs). Mixing these "
            "makes downstream recycling and composting far less effective, since contaminated "
            "recyclables are often rejected entirely."
        ),
    },
    {
        "id": "ewaste_disposal",
        "topic": "E-Waste Disposal",
        "source": "E-Waste (Management) Rules - general guidance",
        "content": (
            "Electronic waste (old phones, chargers, batteries, laptops) should never go into "
            "regular household waste, since it contains heavy metals and toxic materials that "
            "leach into soil and water in landfills. It should instead be handed to an authorized "
            "e-waste collection point or a manufacturer take-back program, many of which are free. "
            "Most Indian cities and city corporations have designated e-waste drop points, and "
            "several electronics retailers accept old devices for safe recycling."
        ),
    },
    {
        "id": "composting_home",
        "topic": "Home Composting",
        "source": "Standard composting practice",
        "content": (
            "Wet kitchen waste like vegetable peels, fruit scraps, tea leaves, and eggshells can "
            "be composted at home in a simple bin or pot, ideally layered with dry material like "
            "dried leaves or shredded paper to control moisture and odor. Cooked food, oily items, "
            "meat, and dairy are best avoided in small home setups since they attract pests and "
            "smell more as they break down. A well-maintained compost pile typically takes 6-8 "
            "weeks to turn into usable soil for plants."
        ),
    },
    {
        "id": "water_scarcity_signs",
        "topic": "Water Conservation",
        "source": "General water conservation guidance",
        "content": (
            "Household water use can often be cut significantly with simple changes: fixing "
            "leaking taps (a slow drip can waste over 15 liters a day), using a bucket instead of "
            "a running shower or hose, reusing RO-reject water for cleaning or plants, and "
            "installing aerators on taps to reduce flow without reducing usability. During declared "
            "water-scarcity periods, many municipalities also restrict non-essential outdoor water "
            "use like car washing and lawn watering."
        ),
    },
    {
        "id": "plastic_categories",
        "topic": "Plastic Recycling",
        "source": "General recycling guidance",
        "content": (
            "Not all plastics are recycled the same way. Rigid plastics like water bottles (PET) "
            "and milk containers (HDPE) are widely accepted by recyclers and should be rinsed and "
            "flattened before disposal. Multi-layered plastic packaging (like chip packets and "
            "sachets) is much harder to recycle in most local systems and is better avoided when "
            "there's a choice, or collected separately for specialized recycling programs where "
            "they exist."
        ),
    },
    {
        "id": "energy_appliance_tips",
        "topic": "Energy Conservation",
        "source": "General energy-efficiency guidance",
        "content": (
            "Common household energy savings include switching to BEE 5-star rated appliances, "
            "unplugging chargers and devices on standby (which draw power even when off), setting "
            "air conditioners to 24-26°C instead of lower, and using natural light and ventilation "
            "during the day where possible. Ceiling fans use a small fraction of the electricity an "
            "AC does and can often reduce reliance on cooling appliances significantly."
        ),
    },
    {
        "id": "battery_disposal",
        "topic": "Battery Disposal",
        "source": "Hazardous waste handling guidance",
        "content": (
            "Household batteries (AA, AAA, button cells, power banks) should never be thrown in "
            "regular trash or burned, as they can leak corrosive and toxic materials. They should "
            "be stored separately in a sealed container at home and dropped off at a battery "
            "collection point, which are increasingly available at electronics stores and some "
            "municipal collection centers."
        ),
    },
    {
        "id": "sdg_alignment_note",
        "topic": "Sustainable Development Goals",
        "source": "UN SDG framework",
        "content": (
            "Responsible waste segregation and resource conservation at the household and campus "
            "level directly support SDG 12 (Responsible Consumption and Production) by reducing "
            "landfill burden and enabling effective recycling, and indirectly support SDG 11 "
            "(Sustainable Cities and Communities) by easing pressure on municipal waste systems."
        ),
    },
]
