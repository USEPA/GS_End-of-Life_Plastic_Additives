# constants.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Constant value declarations."""


ALL_SCENARIO_FIELDS = [
    'conditions', 'msw_composition', 'msw_recycling', 'msw_incineration',
    'msw_landfill', 'msw_compost', 'plastic_recycling', 'incinerated_plastic',
    'landfilled_plastic', 'reported_recycled_masses', 'imported_plastic',
    'exported_plastic', 're_exported_plastic']

COMPLETE_CSS = 'usa-step-indicator__segment--complete'
CURRENT_CSS = 'usa-step-indicator__segment--current'
COMPLETE_SPAN = 'completed'
INCOMPLETE_SPAN = 'not completed'


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
    # "Total MSW (Tons)",
    # "Total Plastic waste (Tons)",
    # "Plastic Recycled (Total, domestic and export)",
    # "Plastic Domestically Recycled Fraction",
    # "Efficiency of Domestic Recycling",
    # "Plastic Export Fraction",
    # "Plastic Re-Export Fraction",
    # "Plastic Incinerated Fraction",
    # "Plastic Landfilled Fraction",
    # "Waste Facility Emissions",
    "total_msw",
    "total_waste",
    "total_recyc",
    "domestic_recyc",
    "export",
    "re_export",
    "recyc_efficiency",
    "incinerated",
    "landfilled",
    "waste_facility_emissions"
]

WASTE_TYPES = [
    # "Misc. Inorganic Waste",
    # "Other",
    # "Yard Trimmings",
    # "Food",
    # "Rubber, Leather and Textiles",
    # "Wood",
    # "Metals",
    # "Glass",
    # "Paper and Paperboard",
    # "Plastics",
    "inorganic",
    "other",
    "yard_trimmings",
    "food",
    "rubber_leather_textiles",
    "wood",
    "metals",
    "glass",
    "paper",
    "plastics"
]



# Note: This is the same as the one above without a plastics string
CALC_WASTE_TYPES = WASTE_TYPES[:len(WASTE_TYPES) - 1]


# Types of plastics in international calculations
INTERNATIONAL_PLASTICS = [
    # "Ethylene",
    # "Vinyl Chloride",
    # "Styrene",
    # "Other",
    "ethylene",
    "vinyl_chloride",
    "styrene",
    "other"
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
    "pet": 1.365,
    "hdpe": 952.5,
    "pvc": 1.455,
    "ldpe": 0.925,
    "pla": 1.26,
    "pp": 905,
    "ps": 1.055,
    "other": 1.29,
}

MAPPER_FRM_DB_TO_APP = {
    "pet": "PET",
    "hdpe": "HDPE",
    "pvc": "PVC",
    "ldpe": "LDPE",
    "pla": "PLA",
    "pp": "PP",
    "ps": "PS",
    "other": "Other Resin",
}

MAPPER_FRM_APP_TO_DB = {
    "PET": "pet",
    "HDPE": "hdpe",
    "PVC": "pvc",
    "LDPE": "ldpe",
    "PLA": "pla",
    "PP": "pp",
    "PS": "ps",
    "Other Resin": "other",
}

ADDITIVE_TYPES = {
    'PET': ["UV Stabilizer", "Flame Retardant", "Antistatic",
            "Clarifier/Toner", "Organic Pigment"],
    'HDPE': ["Antioxidant", "UV Stabilizer", "Colorant", "Flame Retardant",
             "Heat Stabilizer", "Organic Pigment"],
    'PVC': ["Plasticizer", "Antioxidant", "Slip Agent", "Heat Stabilizer",
            "Lubricant", "Colorant", "Organic Pigment"],
    'PP': ["Antioxidant", "Slip Agent", "UV Stabilizer", "Flame Retardant",
           "Clarifier/Toner", "Organic Pigment"],
    'PS': ["Antioxidant", "Slip Agent", "UV Stabilizer", "Antistatic",
           "Colorant", "Organic Pigment"],
    'LDPE': ["Antioxidant", "Slip Agent", "UV Stabilizer", "Flame Retardant",
             "Heat Stabilizer", "Colorant", "Organic Pigment"],
    'PLA': ["Plasticizer", "Heat Stabilizer", "Filler", "Reinforcement",
            "Biocide", "Antioxidant", "Colorant"],
    'other': ["Plasticizer", "Antioxidant", "UV Stabilizer", "Colorant",
              "Flame Retardant", "Curing Agent", "Blowing Agent", "Biocide",
              "Clarifier/Toner", "Inorganic Pigment", "Heat Stabilizer",
              "Organic Pigment", "Filler", "Reinforcement", "Lubricant",
              "Slip Agent", "Antistatic"],
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

# TODO: Proposed table layout
# 4 cols: year, page, field_name, field_value
#         2018, conditions, condition_field_1, 292360000
#         2018, conditions, condition_field_2, 35_680_000
#         2018, msw_comp_prop, msw_comp_prop_field_1, 0.0139

DEFAULT_YEAR = '2018'

DEFAULTS = {
    '2018': {
        'conditions': [292360000.0, 35_680_000.0, 0.084, (0.084 - 0.0456706),
                       0.6670, 0.0456706, 0.0002, 0.172271 * (1 - 0.084),
                       1 - 0.084 - 0.172271 * (1 - 0.084), 109_000_000,
                       630_000_000],
        'msw_comp_prop': [0.0139, 0.0156, 0.121, 0.2159, 0.0896, 0.0619,
                          0.0876, 0.0419, 0.2305, 0.122],
        'msw_recyc': [69_000_000.0, 0, 0.014, 0, 0, 0.0606, 0.0449, 0.1263,
                      0.0443, 0.666, 0.0438],
        'msw_incin': [34_560_000.0, 0.023, 0.019, 0.074, 0.218, 0.166, 0.082,
                      0.085, 0.047, 0.122, 0.163],
        'msw_land': [146_180_000.0, 0.022, 0.02, 0.072, 0.241, 0.111, 0.083,
                     0.095, 0.052, 0.118, 0.185],
        'msw_compost': [42_600_000.0, 0, 0, 0.523, 0.477, 0, 0, 0, 0, 0, 0],
        'rep_rec_plastics': [980000.0, 560000.0, 0, 370000.0, 0, 50000.0,
                             20000.0, 1110000.0],
        'rep_plastics_import': [139791.0, 36647.0, 19841.0, 778806.0],
        'rep_plastics_export': [920477.0, 137493.0, 28071.0, 543487.0],
        'rep_plastics_re_export': [7246.0, 34.0, 27.0, 1038.0],
        'plastics_land_fractions': [
            0.13410900183711, 0.175750153092468, 0.0257195345988977,
            0.251684017146356, 0.00275566442131047, 0.248009797917942,
            0.0685854255970606, 0.0933864053888549],
        'plastics_recyc_fractions': [
            0.148179271708683, 0.176470588235294, 0.0235294117647059,
            0.240616246498599, 0.00252100840336134, 0.228291316526611,
            0.0633053221288515, 0.116526610644258],
        'plastic_incin_fractions': [
            0.13410900183711, 0.175750153092468, 0.0257195345988977,
            0.251684017146356, 0.00275566442131047, 0.248009797917942,
            0.0685854255970606, 0.0933864053888549],
    }
}

PETadditiveTypes = [
    "UV Stabilizer",
    "Flame Retardant",
    "Antistatic",
    "Clarifier/Toner",
    "Organic Pigment",
]

HDPEadditiveTypes = [
    "Antioxidant",
    "UV Stabilizer",
    "Colorant",
    "Flame Retardant",
    "Heat Stabilizer",
    "Organic Pigment",
]

PVCadditiveTypes = [
    "Plasticizer",
    "Antioxidant",
    "Slip Agent",
    "Heat Stabilizer",
    "Lubricant",
    "Colorant",
    "Organic Pigment",
]

PPadditiveTypes = [
    "Antioxidant",
    "Slip Agent",
    "UV Stabilizer",
    "Flame Retardant",
    "Clarifier/Toner",
    "Organic Pigment",
]

PSadditiveTypes = [
    "Antioxidant",
    "Slip Agent",
    "UV Stabilizer",
    "Antistatic",
    "Colorant",
    "Organic Pigment",
]

LDPEadditiveTypes = [
    "Antioxidant",
    "Slip Agent",
    "UV Stabilizer",
    "Flame Retardant",
    "Heat Stabilizer",
    "Colorant",
    "Organic Pigment",
]

PLAadditiveTypes = [
    "Plasticizer",
    "Heat Stabilizer",
    "Filler",
    "Reinforcement",
    "Biocide",
    "Antioxidant",
    "Colorant",
]

otherResinAdditives = [
    "Plasticizer",
    "Antioxidant",
    "UV Stabilizer",
    "Colorant",
    "Flame Retardant",
    "Curing Agent",
    "Blowing Agent",
    "Biocide",
    "Clarifier/Toner",
    "Inorganic Pigment",
    "Heat Stabilizer",
    "Organic Pigment",
    "Filler",
    "Reinforcement",
    "Lubricant",
    "Slip Agent",
    "Antistatic",
]

lowAdditiveFractions = {
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

additivesListList = [
    PETadditiveTypes,
    HDPEadditiveTypes,
    PVCadditiveTypes,
    PPadditiveTypes,
    PSadditiveTypes,
    LDPEadditiveTypes,
    PLAadditiveTypes,
    otherResinAdditives,
]

mswIncin = []
