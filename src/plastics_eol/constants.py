# Constant values from assumptions to be used in calculations.
ASSUMED_VALUES = {
    "Plastic waste lost to littering": 0.02,
    "Plastic waste leak after landfill": 0.1,
    "Plastic content in compost": 0.01,
    "Total compost stream mass multiplier": 1.01,
    "Total mass of plastic in compost stream (Tons):": 426000,
    "Additive migration Fraction": 0.02,
    "Incineration Efficiency Fraction": 0.9999,
}

# Low additive Fractions
# key = type of additive (Excel F6:F21)
# value = low value for bulk mass proportion (Excel G6:G21)
LOW_ADD_FRACTIONS = {
    "Plasticizer": 0.1,
    "Flame Retardant": 0.007,
    "UV Stabilizer": 0.005,
    "Heat Stabilizer": 0.005,
    "Antioxidant": 0.005,
    "Slip Agent": 0.001,
    "Lubricant": 0.001,
    "Antistatic": 0.001,
    "Curing Agent": 0.001,
    "Blowing Agent": 0.005,
    "Biocide": 0.00001,
    "Colorant": 0.0025,
    "Organic Pigment": 0.00001,
    "Clarifier/Toner": 0.00015,
    "Inorganic Pigment": 0.0001,
    "Filler": 0.00001,
    "Reinforcement": 0.15,
}

# Categories to be paired with data for each year
CONDITION_CATEGORIES = [
    "Total MSW (Tons)",
    "Total Plastic waste (Tons)",
    "Plastic Recycled (Total, domestic and export)",
    "Plastic Domestically Recycled Fraction",
    "Efficiency of Domestic Recycling",
    "Plastic Export Fraction",
    "Plastic Re-Export Fraction",
    "Plastic Incinerated Fraction",
    "Plastic Landfilled Fraction",
    "Waste Facility Emissions",
]

WASTE_TYPES = [
    "Misc. Inorganic Waste",
    "Other",
    "Yard Trimmings",
    "Food",
    "Rubber, Leather and Textiles",
    "Wood",
    "Metals",
    "Glass",
    "Paper and Paperboard",
    "Plastics",
]

# Note: This is the same as the one above without a plastics string
CALC_WASTE_TYPES = WASTE_TYPES[:len(WASTE_TYPES)-1]

# Types of plastics in international calculations
INTERNATIONAL_PLASTICS = [
  "Ethylene",
  "Vinyl Chloride",
  "Styrene",
  "Other"
]

# Categories for life cycle inventory
# (formerly known as material flow analysis)
INVENTORY_CATEGORIES = [
    "PET",
    "HDPE",
    "PVC",
    "LDPE",
    "PLA",
    "PP",
    "PS",
    "Other Resin",
    "Chemical Additives",
]

# Densities of plastics for later calculations
# polymerWasteDensity = {
DOMESTIC_PLASTICS_DENSITIES = {
    "PET": 1.365,
    "HDPE": 952.5,
    "PVC": 1.455,
    "LDPE": 0.925,
    "PLA": 1.26,
    "PP": 905,
    "PS": 1.055,
    "Other Resin": 1.29,
}

# TODO: Remove this commented code once the app is functioning.
# Types of plastics in domestic calculations
# NOTE: This list is redundant based on the densities dictionary.
# To get this list of domestic plastic types simply retrieve the list of keys
# from DOMESTIC_PLASTIC_DENSITIES.
# typesOfPlasticDomestic = [
#     "PET",
#     "HDPE",
#     "PVC",
#     "LDPE",
#     "PLA",
#     "PP",
#     "PS",
#     "Other Resin",
# ]
