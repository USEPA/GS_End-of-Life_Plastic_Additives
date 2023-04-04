# utils.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Utility methods."""
from plastics_eol import constants as CONST
from plastics_eol import utils
from plastics_eol.models import MSWCompost, MSWComposition, MSWIncineration, \
    MSWRecycling, MSWLandfill, PlasticLandfill, PlasticRecycling, \
    PlasticIncineration, Condition, ImportedPlastic, ExportedPlastic, \
    ReExportedPlastic, PlasticReportedRecycled, Result, Scenario


def run_calculator(scenario_id):
    # ########################################################################
    # User inputs, TODO move to forms:
    # plastic_land_fractions = []
    # plastic_recyc_fractions = []
    # plastic_incin_fractions = []
    # msw_comp_prop = []
    # conditions = []
    # rep_plastic_import = []
    # rep_plastic_export = []
    # rep_plastic_re_export = []
    # rep_rec_plastics = []
    # ########################################################################

    domestic_plastics = list(CONST.DOMESTIC_PLASTICS_DENSITIES.keys())
    # #  will be removed before distribution. This is a programming shortcut
    # assign_vals()

    # #  creates list of lists of input data
    # data_lists = [
    #     conditions, msw_comp_prop, mswRecyc, mswIncin, mswLand, mswCompost,
    #     rep_rec_plastics, rep_plastic_import, rep_plastic_export,
    #     rep_plastic_re_export, plastic_land_fractions,
    #     plastic_recyc_fractions, plastic_incin_fractions
    # ]

    # #  Checks entry data lists to make sure they have data
    # #  returns an error if necesssary
    # for i in data_lists:
    #     if check_entry(i):
    #         gap_label_1.config(text='Not all data has been input.')
    #         return

    # # clears LCI tables if they already had data inside
    # mat_flow_manuf_trvw.delete(*mat_flow_manuf_trvw.get_children())
    # mat_flow_use_trvw.delete(*mat_flow_use_trvw.get_children())
    # mat_flow_csp_trvw.delete(*mat_flow_csp_trvw.get_children())
    # mat_flow_mech_recyc_trvw.delete(*mat_flow_mech_recyc_trvw.get_children())
    # mat_flow_incin_trvw.delete(*mat_flow_incin_trvw.get_children())
    # mat_flow_land_trvw.delete(*mat_flow_land_trvw.get_children())

    # dict of Fractions of total plastic landfilled
    # associated with each type of plastic
    plastic_landfill = PlasticLandfill.objects.filter(scenario_id=scenario_id).first().__dict__
    plastic_land_fractions = {p: plastic_landfill[p] for p in domestic_plastics}


    # plastic_land_fractions_dict = {
    #     CONST.MAPPER_FRM_DB_TO_APP[member]: plastic_land_fractions[member] for member in members
    # }
    # dict of proportion of each type of plastic that has been recycled.
    # key = type of plastic A5:A12;
    # value = proportion of each type of plastic in MSW stream B5:B12
    plastic_recyc = PlasticRecycling.objects.filter(scenario_id=scenario_id).first().__dict__
    plasticFractionsRecycled = {p: plastic_recyc[p] for p in domestic_plastics}
    # plasticFractionsRecycled = dict(zip(domestic_plastics,
    #                                     plastic_recyc_fractions))

    # dict of incineration Fractions for each kind of plastic.
    # Key = type of plastic, value = proportion of incineration make up

    plastic_incin = PlasticIncineration.objects.filter(scenario_id=scenario_id).first().__dict__
    plasticIncinFractionsDict = {p: plastic_incin[p] for p in domestic_plastics}

    # plasticIncinFractionsDict = dict(zip(domestic_plastics,
    #                                      plastic_incin_fractions))

    # dicts of data, associating category with value
    # key = MSW waste, value = proportion of MSW
    msw_composition = MSWComposition.objects.filter(scenario_id=scenario_id).first().__dict__
    mswGeneratedProps = {w: msw_composition[w] for w in CONST.WASTE_TYPES}
    # mswGeneratedProps = dict(zip(CONST.WASTE_TYPES, msw_comp_prop))

    # key = conditions (total MSW, total plastic, plastic recycled, etc.)
    condition = Condition.objects.filter(scenario_id=scenario_id).first().__dict__
    mswConditions = {c: condition[c] for c in CONST.CONDITION_CATEGORIES}
    # mswConditions = dict(zip(CONST.CONDITION_CATEGORIES, conditions))

    # Create dictionaries of international recycling values
    plast_import = ImportedPlastic.objects.filter(scenario_id=scenario_id).first().__dict__
    rep_plastic_importDict = {p: plast_import[p] for p in CONST.INTERNATIONAL_PLASTICS}

    # rep_plastic_importDict = dict(zip(CONST.INTERNATIONAL_PLASTICS,
    #                                   rep_plastic_import))

    plast_export = ImportedPlastic.objects.filter(scenario_id=scenario_id).first().__dict__
    rep_plastic_exportDict = {p: plast_export[p] for p in CONST.INTERNATIONAL_PLASTICS}

    # rep_plastic_exportDict = dict(zip(CONST.INTERNATIONAL_PLASTICS,
                                    #   rep_plastic_export))

    plast_reexport = ReExportedPlastic.objects.filter(scenario_id=scenario_id).first().__dict__
    rep_plastic_re_exportDict = {p: plast_reexport[p] for p in CONST.INTERNATIONAL_PLASTICS}
    # rep_plastic_re_exportDict = dict(zip(CONST.INTERNATIONAL_PLASTICS,
    #                                      rep_plastic_re_export))

    # dict of scaled recycled masses
    # key = type of plastic, value = bulk mass of plastic and additives G9:G16
    rep_rec_plastics = PlasticReportedRecycled.objects.filter(scenario_id=scenario_id).first().__dict__
    rep_rec_plastics_values = [rep_rec_plastics[p] for p in CONST.DOMESTIC_PLASTICS_DENSITIES.keys()]
    scaledRec = utils.recycle_scaler(
        rep_rec_plastics_values, condition['total_waste'], condition['total_recyc'])

    ###########################################################################
    ###########################################################################
    # Stream 6 Calculations
    # Sheet = Stream 6 - PWaste Generated
    # Create dict with total mass of each total type of plastic generated
    # (total mass of plastics generated * Fraction of each kind of plastic).
    # key = plastic type A5:A12; value = bulk mass including additives C5:C12
    plasticsMassDict = dict(zip(
        domestic_plastics,
        [plasticFractionsRecycled[i] * condition['total_waste']
         for i in domestic_plastics]))

    # Create dicts of additive masses in each kind of plastic in
    PETAdditiveMasses = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", plasticsMassDict)
    HDPEAdditiveMasses = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", plasticsMassDict)
    PVCAdditiveMasses = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", plasticsMassDict)
    PPAdditiveMasses = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", plasticsMassDict)
    PSAdditiveMasses = utils.additiveMassCalculator(
        CONST.PSadditiveTypes, "ps", plasticsMassDict)
    LDPEAdditiveMasses = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", plasticsMassDict)
    PLAAdditiveMasses = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", plasticsMassDict)
    otherResinAdditivesMasses = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", plasticsMassDict)

    # Define list of preceding 8 dicts
    listOfStream6Additives_ = [
        PETAdditiveMasses, HDPEAdditiveMasses, PVCAdditiveMasses,
        LDPEAdditiveMasses, PLAAdditiveMasses, PPAdditiveMasses,
        PSAdditiveMasses, otherResinAdditivesMasses]

    averageDensityCalculation = sum([
        CONST.DOMESTIC_PLASTICS_DENSITIES[i] * plasticFractionsRecycled[i]
        for i in domestic_plastics]) * 0.00000110231

    ###########################################################################
    ###########################################################################
    ###########################################################################
    # Stream 16 Calculations
    # Sheet = Stream 16 - MechRecyc

    # Create dictionary of bulk masses by multiplying scaled recycling values
    # by the ratio of domestic recycled plastic to total recycled plastic
    stream16PlasticCalcMasses = dict(zip(
        domestic_plastics,
        [condition['domestic_recyc']/condition['total_recyc']*scaledRec[i]
         for i in domestic_plastics]))

    # Creates dictionary of masses of each kind of
    # additive in each kind of plastic
    stream16PET = utils.additiveMassCalculator(CONST.PETadditiveTypes, "pet",
                                               stream16PlasticCalcMasses)
    stream16HDPE = utils.additiveMassCalculator(CONST.HDPEadditiveTypes, "hdpe",
                                                stream16PlasticCalcMasses)
    stream16PVC = utils.additiveMassCalculator(CONST.PVCadditiveTypes, "pvc",
                                               stream16PlasticCalcMasses)
    stream16PP = utils.additiveMassCalculator(CONST.PPadditiveTypes, "pp",
                                              stream16PlasticCalcMasses)
    stream16PS = utils.additiveMassCalculator(CONST.PSadditiveTypes, "ps",
                                              stream16PlasticCalcMasses)
    stream16LDPE = utils.additiveMassCalculator(CONST.LDPEadditiveTypes, "ldpe",
                                                stream16PlasticCalcMasses)
    stream16PLA = utils.additiveMassCalculator(CONST.PLAadditiveTypes, "pla",
                                               stream16PlasticCalcMasses)
    stream16Other = utils.additiveMassCalculator(CONST.otherResinAdditives,
                                                 "other",
                                                 stream16PlasticCalcMasses)

    # Creates dict of emissions factors per M24:M31.
    # Key = type of additive, value = emission factor
    emissionFactors = {"pet": -1.13, "hdpe": -.88, "pvc": 0, "ldpe": 0,
                       "pla": 0, "pp": 0, "ps": 0, "other": -1.03}

    # Creates list of additive dicts in stream 16
    listOfstream16Additives = [
        stream16PET, stream16HDPE, stream16PVC, stream16LDPE, stream16PLA,
        stream16PP, stream16PS,  stream16Other]

    # Calculates total amount of each kind of additive in stream 16;
    # key = type of additive, value = total mass of additive
    totalAdditivesStream16_ = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfstream16Additives)
         for i in CONST.otherResinAdditives]))  # Dict of additive in stream 16

    # Calc Fraction of each additive of total mass of additives in stream 16
    # key = type of additive, value = Fraction of total
    additiveFractionsStream16_ = dict(zip(
        CONST.otherResinAdditives,
        [totalAdditivesStream16_[i] / sum(totalAdditivesStream16_.values())
         for i in CONST.otherResinAdditives]))

    # Calculates total amount of each resin in stream 16;
    # key = type of plastic, value = mass of resin
    stream16ResinMasses_ = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream16PlasticCalcMasses,
                              listOfstream16Additives[i])
         for i in range(8)]))

    ###########################################################################
    ###########################################################################
    # Stream 17
    # Create dict by calculating emissions from stream 16 per emissions
    # factors and converts to Tons of CO2.
    # Multiplies bulk mass of each plastic by emission factor and then
    # converts to Tons.
    # Key = type of plastic, value = emissions in Tons of CO2
    emissionStream16 = dict(zip(
        domestic_plastics,
        [emissionFactors[i] * stream16PlasticCalcMasses[i] * 1.10231
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 19
    # Sheet = Stream 19 - Contamination
    # Creates dict of additive contaminations.
    # Key = type of additive; value = contamination
    additiveContaminationConstant = 0.0415  # C11

    # Multiply Fraction of each kind of additive by the total of plastic
    # bulk masses in stream 16 and by the contamination constant
    stream19AdditivesTotals = dict(zip(
        CONST.otherResinAdditives,
        [additiveFractionsStream16_[i]
         * sum(stream16PlasticCalcMasses.values())
         * (additiveContaminationConstant) for i in CONST.otherResinAdditives]))

    # Calculate additives and degradation products in stream 19
    stream19Contaminants = sum(stream16PlasticCalcMasses.values()) * 0.0065
    stream19DegradationProducts = sum(
        stream16PlasticCalcMasses.values()) * 0.0515

    ###########################################################################
    ###########################################################################
    # Stream 4 Calculations
    # Sheet = US Mat Flow Analysis
    # Creates dict of total resin in stream 4,
    # based on stream 6 and bulk plastic manufacturing for .
    # Key = type of plastic, value = mass of resin
    stream4ResinMasses_ = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              plasticsMassDict, listOfStream6Additives_[i])
         for i in range(8)]))

    # Creates dict of total additives in stream 4, based on stream 6 and
    # bulk plastic manufacturing for .
    # Key = type of additive, value = mass of additive
    stream4AdditiveMasses_ = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfStream6Additives_)
         for i in CONST.otherResinAdditives]))

    ###########################################################################
    ###########################################################################
    # Stream 18 Calculations
    # Sheet = US Mat Flow Analysis
    # Create dict of additive migration occuring in stream 18 by multiplying
    # the mass of each kind of additive in stream 16
    # by the additive migration constant (0.02)
    stream18AdditiveMigration = dict(zip(
        CONST.otherResinAdditives, [0.02 * totalAdditivesStream16_[i]
                              for i in CONST.otherResinAdditives]))

    ###########################################################################
    ###########################################################################
    # Stream 21 Calculations
    # Sheet = Stream 21 - Import
    # Creates dict with key = type of plastic and value = amount of type
    # of plastic imported based on reported Imported plastics in
    # includes resin and additives lumped together
    stream21PlasticMasses = {
        "pet": rep_plastic_importDict["other"] * 0.4,
        "hdpe": rep_plastic_importDict["ethylene"] / 2,
        "pvc": rep_plastic_importDict["vinyl_chloride"],
        "ldpe": rep_plastic_importDict["ethylene"] / 2,
        "pla": 0, "pp": 0, "ps": rep_plastic_importDict["styrene"],
        "other": rep_plastic_importDict["other"] * 0.6}

    # Create dict of each kind of additive in each kind of plastic.
    # Key = additive, value = mass of that additive
    stream21PET = utils.additiveMassCalculator(CONST.PETadditiveTypes, "pet",
                                               stream21PlasticMasses)
    stream21HDPE = utils.additiveMassCalculator(CONST.HDPEadditiveTypes, "hdpe",
                                                stream21PlasticMasses)
    stream21PVC = utils.additiveMassCalculator(CONST.PVCadditiveTypes, "pvc",
                                               stream21PlasticMasses)
    stream21PP = utils.additiveMassCalculator(CONST.PPadditiveTypes, "pp",
                                              stream21PlasticMasses)
    stream21PS = utils.additiveMassCalculator(CONST.PSadditiveTypes, "ps",
                                              stream21PlasticMasses)
    stream21LDPE = utils.additiveMassCalculator(CONST.LDPEadditiveTypes, "ldpe",
                                                stream21PlasticMasses)
    stream21PLA = utils.additiveMassCalculator(CONST.PLAadditiveTypes, "pla",
                                               stream21PlasticMasses)
    stream21Other = utils.additiveMassCalculator(CONST.otherResinAdditives,
                                                 "other",
                                                 stream21PlasticMasses)

    # lists of preceding dicts
    listOfStream21Additives_ = [
        stream21PET, stream21HDPE, stream21PVC, stream21LDPE, stream21PLA,
        stream21PP, stream21PS,  stream21Other]

    # Totals each kind of additive in stream 21.
    # Key = type of additive, value = amount of additive
    stream21AdditivesTotals = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfStream21Additives_)
         for i in CONST.otherResinAdditives]))

    # Calculate total amount of each kind of resin in stream 21.
    # Key = type of plastic, value = amount of resin
    stream21ResinMasses_ = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(
            domestic_plastics[i],
            stream21PlasticMasses,
            listOfStream21Additives_[i])
         for i in range(8)]))

    # Calculate emissions in this stream by multiplying bulk mass by
    # 0.04 (the emissions factor) then converting into Tons of CO2
    stream21Emissions = dict(zip(
        domestic_plastics,
        [0.04 * 1.10231 * stream21PlasticMasses[i]
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 22 Calculations
    # Sheet = Stream 22- Re-Export
    # Create dict with key = type of plastic and value = amount of
    # type of plastic reexported based on reported reexported plastics in
    stream22PlasticMasses = {
        "pet": rep_plastic_re_exportDict["other"] * 0.4,
        "hdpe": rep_plastic_re_exportDict["ethylene"] / 2,
        "pvc": rep_plastic_re_exportDict["vinyl_chloride"],
        "ldpe": rep_plastic_re_exportDict["ethylene"] / 2,
        "pla": 0, "pp": 0, "ps": rep_plastic_re_exportDict["styrene"],
        "other": rep_plastic_re_exportDict["other"] * 0.6}

    # Calculate amount of each additive in each type of plastic in stream 22.
    # Key = type of additive, value = mass of that additive in stream 22
    stream22PET = utils.additiveMassCalculator(CONST.PETadditiveTypes, "pet",
                                               stream22PlasticMasses)
    stream22HDPE = utils.additiveMassCalculator(CONST.HDPEadditiveTypes, "hdpe",
                                                stream22PlasticMasses)
    stream22PVC = utils.additiveMassCalculator(CONST.PVCadditiveTypes, "pvc",
                                               stream22PlasticMasses)
    stream22PP = utils.additiveMassCalculator(CONST.PPadditiveTypes, "pp",
                                              stream22PlasticMasses)
    stream22PS = utils.additiveMassCalculator(CONST.PSadditiveTypes, "ps",
                                              stream22PlasticMasses)
    stream22LDPE = utils.additiveMassCalculator(CONST.LDPEadditiveTypes, "ldpe",
                                                stream22PlasticMasses)
    stream22PLA = utils.additiveMassCalculator(CONST.PLAadditiveTypes, "pla",
                                               stream22PlasticMasses)
    stream22Other = utils.additiveMassCalculator(CONST.otherResinAdditives,
                                                 "other",
                                                 stream22PlasticMasses)

    # Create list of above dictionaries
    listOfStream22Additives_ = [
        stream22PET, stream22HDPE, stream22PVC, stream22LDPE, stream22PLA,
        stream22PP, stream22PS,  stream22Other]

    # Dict: Calculate total mass of each kind of resin in stream 22.
    # Key = type of plastic, value = mass of resin
    stream22ResinMasses_ = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream22PlasticMasses,
                              listOfStream22Additives_[i])
         for i in range(8)]))

    # Dict: Calculate total of each kind of additive in stream 22.
    # Key = type of additive, value = mass of additive
    stream22AdditivesTotals = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfStream22Additives_)
         for i in CONST.otherResinAdditives]))

    # Dict: Calculate emissions in stream 22. Emission factor 0.04*bulk mass
    # of plastic in stream 22 and then converted into Tons of CO2
    stream22Emissions = dict(zip(
        domestic_plastics,
        [0.04 * 1.10231 * stream22PlasticMasses[i]
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 23 Calculations
    # Sheet = Stream 23MechRec-Incin
    # Dictionary of resin masses in stream 23, based on efficiency of
    # domestic recycling (1-conditions208[4])/2, then multiplied by resin mass.
    # key = type of plastic resin, value = mass of resin
    stream23ResinMasses_ = dict(zip(
        domestic_plastics,
        [(1 - condition['export']) / 2 * stream16ResinMasses_[i]
         for i in domestic_plastics]))  # Resin alone

    # Dictionary of additive masses in stream 23, based on efficiency of
    # domestic recycling (1-conditions208[4])/2,
    # then multiplied by additive mass.
    # key = type of plastic additive, value = mass of additive
    stream23AdditiveMasses_ = dict(zip(
        CONST.otherResinAdditives,
        [totalAdditivesStream16_[i] * (1 - condition['export']) / 2
         for i in CONST.otherResinAdditives]))
    stream23PlasticMasses = dict(zip(
        domestic_plastics,
        [utils.backwardsLumpPlasticCalculator(stream23ResinMasses_,
                                        domestic_plastics[i],
                                        CONST.additivesListList[i])
         for i in range(8)]))

    # stream 23 Emissions calculations dictionary.
    # Bulk plastic weight in stream * 0.04 * conversion factor to
    # make units Tons of CO2.
    # Key = type of plastic, value = emissions associated with that type
    stream23Emissions = dict(zip(
        domestic_plastics,
        [0.04 * 1.10231 * stream23PlasticMasses[i]
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################

    # Stream28 Calculations unnecessary because they are the same as
    # stream 23- as per sheet US Mat Flow Analysis

    ###########################################################################
    ###########################################################################
    # Stream 20 Calculations
    # Sheet = Stream 20 Domestic Recyc

    # Create dictionary of stream 20 resin masses.
    # Key = type of plastic resin, value = mass of resin:
    #   stream16+stream21-stream22-stream23-stream28
    #   (but stream28=stream23, so stream23 is subtracted twice)
    stream20ResinMasses = dict(zip(
        domestic_plastics,
        [stream16ResinMasses_[i] + stream21ResinMasses_[i] -
         stream22ResinMasses_[i]-2*stream23ResinMasses_[i]
         for i in domestic_plastics]))

    # Create dictionary of stream 20 additive masses.
    # Key = type of additive, value = mass of additive:
    #   stream16-stream18+stream19+stream21-stream22-stream23-stream28
    #   (stream28=stream23, so stream23 is substracted twice)
    stream20TotalAdditives = dict(zip(
        CONST.otherResinAdditives,
        [totalAdditivesStream16_[i] - stream18AdditiveMigration[i] +
         stream19AdditivesTotals[i] + stream21AdditivesTotals[i] -
         stream22AdditivesTotals[i] - 2 * stream23AdditiveMasses_[i]
         for i in CONST.otherResinAdditives]))

    # Not given bulk masses, so bulk masses calculated here.
    # Key = type of plastic, value = bulk mass of each type of plastic
    stream20PlasticCalcMasses = dict(zip(
        domestic_plastics,
        [utils.backwardsLumpPlasticCalculator(stream20ResinMasses,
                                        domestic_plastics[i],
                                        CONST.additivesListList[i])
         for i in range(8)]))

    stream20Emissions = dict(zip(
        domestic_plastics,
        [stream20PlasticCalcMasses[i] * emissionFactors[i]
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 1 Calculations
    # Sheet =US Mat Flow Analysis
    # Dictionary of stream1 resin masses.
    # Key = type of resin, value = mass of resin: stream4 - stream 20
    stream1PlasticMasses = dict(zip(
        domestic_plastics,
        [stream4ResinMasses_[i] - stream20ResinMasses[i]
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 2 Calculations
    # Sheet= US Mat Flow Analysis
    # Dictionary of additive masses.
    # Key = type of additive, value = mass of additive
    stream2AdditiveMasses = dict(zip(
        CONST.otherResinAdditives,
        [stream4AdditiveMasses_[i] - stream20TotalAdditives[i]
         for i in CONST.otherResinAdditives]))

    ###########################################################################
    ###########################################################################
    # Stream 3 Calculations
    # Sheet = Stream 3 - Emissions

    # Sum to create mass basis for stream 3
    stream1_stream2_total = sum(stream1PlasticMasses.values()) + \
        sum(stream2AdditiveMasses.values())

    # Create dict of Fraction of each kind of plastic in
    # stream 3 based on total resin.
    # Key = type of plastic, value = Fraction of total
    stream3PlasticFractions = dict(zip(
        domestic_plastics,
        [stream1PlasticMasses[i] / sum(stream1PlasticMasses.values())
         for i in domestic_plastics]))

    # Create dict of bulk plastic masses of each kind of plastic based on
    # Fraction determined above and mass basis.
    # Key = type of plastic, value = bulk mass
    stream3PlasticMasses = dict(zip(
        domestic_plastics,
        [stream3PlasticFractions[i] * stream1_stream2_total
         for i in domestic_plastics]))  # Lump sum

    # Create dictionary of additives for each type for each
    # kind of plastic based on bulk mass
    stream3PETAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", stream3PlasticMasses)
    stream3HDPEAdditives = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", stream3PlasticMasses)
    stream3PVCAdditives = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", stream3PlasticMasses)
    stream3LDPEAdditives = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", stream3PlasticMasses)
    stream3PLAAdditives = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", stream3PlasticMasses)
    stream3PPAdditives = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", stream3PlasticMasses)
    stream3PSAdditives = utils.additiveMassCalculator(
        CONST.PSadditiveTypes, "ps", stream3PlasticMasses)
    stream3OtherAdditives = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", stream3PlasticMasses)

    # Create dictionary of emisions factors for each kind of plastic.
    # Key = type of plastic, value = emission factor
    stream3EmissionFactor = {
        "pet": 2.2, "hdpe": 1.53, "pvc": 1.9, "ldpe": 1.76, "pla": 2.09,
        "pp": 1.51, "ps": 2.46, "other": 1.92}

    # Create dictionary of emissions for stream 3.
    # Key = type of plastic, value = emissions for that
    # (bulk mass*emission factor*conversion factor)
    stream3Emissions = dict(zip(
        domestic_plastics,
        [stream3EmissionFactor[i] * stream3PlasticMasses[i] * 1.10231
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 5 Calculations
    # Sheet = US Mat Flow Analysis
    polymerMigrationConstant = 4.71538E-06
    additiveMigrationConstant = 0.019945732

    # Create dict of resin masses in stream 5 by multiplying by
    # polymer migration constant defined above.
    # Key = type of resin, value = mass of migration
    stream5ResinMasses = dict(zip(
        domestic_plastics,
        [polymerMigrationConstant * stream4ResinMasses_[i]
         for i in domestic_plastics]))

    # Create dict of additive masses in stream 5 by multiplying by
    # additive migration constant defined above.
    # Key = type of resin, value = mass of migration
    stream5AdditiveMasses = dict(zip(
        CONST.otherResinAdditives,
        [additiveMigrationConstant * stream4AdditiveMasses_[i]
         for i in CONST.otherResinAdditives]))

    ###########################################################################
    ###########################################################################
    # Stream 27 Calculations
    # Sheet = Stream 27 - Export

    # Dictionary defining mass of each kind of plastic for this stream
    # based on Export definitions in US  Sensitivity facts.
    # Key = type of plastic, value = bulk mass of that plastic
    stream27PlasticMasses = {
        "pet": rep_plastic_exportDict["other"] * 0.4,
        "hdpe": rep_plastic_exportDict["ethylene"] / 2,
        "pvc": rep_plastic_exportDict["vinyl_chloride"],
        "ldpe": rep_plastic_exportDict["ethylene"] / 2,
        "pla": 0, "pp": 0, "ps": rep_plastic_exportDict["styrene"],
        "other": rep_plastic_exportDict["other"] * 0.6}

    # Dict defining mass of each kind of additive in each kind of plastic.
    # Key = type of additive, value = mass of that additive
    stream27PETAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", stream27PlasticMasses)
    stream27HDPEAdditives = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", stream27PlasticMasses)
    stream27PVCAdditives = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", stream27PlasticMasses)
    stream27LDPEAdditives = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", stream27PlasticMasses)
    stream27PLAAdditives = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", stream27PlasticMasses)
    stream27PPAdditives = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", stream27PlasticMasses)
    stream27PSAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "ps", stream27PlasticMasses)
    stream27OtherAdditives = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", stream27PlasticMasses)

    # List of above dictionaries
    listOfstream27Additives = [
        stream27PETAdditives, stream27HDPEAdditives, stream27PVCAdditives,
        stream27LDPEAdditives, stream27PLAAdditives, stream27PPAdditives,
        stream27PSAdditives, stream27OtherAdditives]

    # Dict of resin masses in this stream.
    # Key = type of resin, value = mass of resin
    stream27ResinMasses = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream27PlasticMasses,
                              listOfstream27Additives[i])
         for i in range(8)]))

    # Dictionary of additive masses in this stream.
    # Key = type of additive, value = mass of additive
    stream27TotalAdditivesMasses = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfstream27Additives)
         for i in CONST.otherResinAdditives]))

    # Dictionary of emissions in this stream,
    # key = type of plastic, value = emissions associated with that plastic
    # (bulk mass *0.04 * conversion factor to make units Tons CO2))
    stream27Emissions = dict(zip(
        domestic_plastics,
        [0.04 * 1.10231 * stream27PlasticMasses[i]
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 8 Calculations
    # Note: stream8 plastic resins and additives are the same as
    # stream 27 as per US Mat FLow Analysis
    # Creates dictionary of types of MSW waste (without plastic),
    # takes total MSW and multiplies that by their respective proportions.
    # Key = type of MSW, value = mass of that MSW
    msw_comp_prop = list(mswGeneratedProps.values())
    stream8MSWMasses_ = dict(zip(
        CONST.CALC_WASTE_TYPES,
        [msw_comp_prop[i] * condition['total_msw']
         for i in range(len(CONST.CALC_WASTE_TYPES))]))

    ###########################################################################
    ###########################################################################
    # Stream 9 Calculations
    # Sheet = Stream 9 - Litter
    # Determines total mass of stream 4, then multiplies it by
    # littering constant to determine mass of littered plastic
    stream4TotalMass_ = sum(stream4AdditiveMasses_.values()) + \
        sum(stream4ResinMasses_.values())
    stream9TotalMass_ = 0.02 * stream4TotalMass_

    # Create dictionary of bulk plastic masses based on proportions
    # of plastic generated and mass basis for stream.
    # Key = type of plastic, value = bulk mass littered
    stream9PlasticMasses_ = dict(zip(
        domestic_plastics,
        [stream9TotalMass_*plasticFractionsRecycled[i]
         for i in domestic_plastics]))

    # Create dictionary of additives in littered plastic based on
    # bulk masses determined above.
    # Key = type of additive, value = mass of additive
    stream9PETAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", stream9PlasticMasses_)
    stream9HDPEAdditives = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", stream9PlasticMasses_)
    stream9PVCAdditives = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", stream9PlasticMasses_)
    stream9LDPEAdditives = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", stream9PlasticMasses_)
    stream9PLAAdditives = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", stream9PlasticMasses_)
    stream9PPAdditives = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", stream9PlasticMasses_)
    stream9PSAdditives = utils.additiveMassCalculator(
        CONST.PSadditiveTypes, "ps", stream9PlasticMasses_)
    stream9OtherAdditives = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", stream9PlasticMasses_)

    # Create list of above dicts
    listOfstream9Additives = [
        stream9PETAdditives, stream9HDPEAdditives, stream9PVCAdditives,
        stream9LDPEAdditives, stream9PLAAdditives, stream9PPAdditives,
        stream9PSAdditives, stream9OtherAdditives]

    # Create dictionary of total of each kind of additive in this stream.
    # Key = type of additive, value = total mass of additive in this stream
    stream9TotalAdditives = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfstream9Additives)
         for i in CONST.otherResinAdditives]))

    # Create dict of total resin in this stream.
    # Key= type of resin, value = mass of resin in this stream
    stream9ResinTotals = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream9PlasticMasses_,
                              listOfstream9Additives[i])
         for i in range(8)]))

    ###########################################################################
    ###########################################################################
    # Stream 6 Pt. 2

    # Dict of resin values in this stream
    stream6ResinTotals = dict(zip(
        domestic_plastics,
        [stream4ResinMasses_[i] - stream5ResinMasses[i]
         for i in domestic_plastics]))

    # Dict of additive values in this stream
    stream6AdditiveTotals = dict(zip(
        CONST.otherResinAdditives,
        [stream4AdditiveMasses_[i] - stream5AdditiveMasses[i]
         for i in CONST.otherResinAdditives]))

    ###########################################################################
    ###########################################################################
    # Stream 10 Calculations
    # Sheet = US Mat Flow Analysis

    # Creates dict of resin totals in this stream.
    # Key = type of resin, value = mass of resin (stream6-stream9+stream27)
    stream10ResinTotals = dict(zip(
        domestic_plastics,
        [stream6ResinTotals[i] - stream9ResinTotals[i] + stream27ResinMasses[i]
         for i in domestic_plastics]))

    # Creates dict of additive totals in this stream.
    # Key = type of additive, value = mass of additive
    # (stream6-stream9+stream27)
    stream10AdditiveTotals = dict(zip(
        CONST.otherResinAdditives,
        [stream6AdditiveTotals[i] - stream9TotalAdditives[i] +
         stream27TotalAdditivesMasses[i] for i in CONST.otherResinAdditives]))

    # Note: stream 10 MSW data (rows 27:35) is the same as
    # stream 8 so will be omitted for concision purposes
    # Cell K39
    totalStream10Waste = sum(stream10AdditiveTotals.values()) + \
        sum(stream10ResinTotals.values()) + sum(stream8MSWMasses_.values())

    ###########################################################################
    ###########################################################################
    # Stream 7 Calculations
    # Sheet = US Mat Flow Analysis
    stream7EmissionFactor = 230

    # Calculates stream 7 emissions based on total stream 10 mass,
    # emission factor, and conversion factor to Tons of CO2
    stream7TotalEmissions = totalStream10Waste * stream7EmissionFactor * \
        0.00110231

    ###########################################################################
    ###########################################################################
    # Stream 11 Calculations
    # Sheet = US Mat Flow Analysis

    # Create dictionary of key = types of MSW (except plastic);
    # value = mass of MSW incinerated
    # (total mass incinerated * proportion incinerated)

    # .get throws an error if obj doesn't exist
    # mswIncin = MSWIncineration.objects.get(id=scenario_id)

    # .filter returns an empty set, calling .first() on the
    mswIncin = MSWIncineration.objects.filter(scenario_id=scenario_id).first()
    stream11MSWValues = mswIncin.fractions_to_mass()
    # stream11MSWValues = dict(zip(
    #     CONST.CALC_WASTE_TYPES,
    #     [mswIncin[0] * mswIncin[i]
    #      for i in range(1, len(CONST.CALC_WASTE_TYPES) + 1)]))

    ###########################################################################
    ###########################################################################
    # Stream 12 Calculations
    # Sheet = US Mat FLow Analysis

    # Creates dict of key = types of MSW (except plastic)
    # value = mass of MSW landfilled
    # (total mass landfilled*proportion landfilled)
    mswLand = MSWLandfill.objects.filter(scenario_id=scenario_id).first()
    stream12MSWValues = mswLand.fractions_to_mass()
    # stream12MSWValues = dict(zip(
    #     CONST.CALC_WASTE_TYPES,
    #     [mswLand[0] * mswLand[i]
    #      for i in range(1, len(CONST.CALC_WASTE_TYPES) + 1)]))

    ###########################################################################
    ###########################################################################
    # Stream 13 Calculations
    # Sheet = Stream 13-Plastic Compost

    # Creates dict of key = type of plastic,
    # value = mass*0.01Fraction*Fraction of each kind of plastic.
    # TODO: define a custom function in the class
    mswCompost = MSWCompost.objects.filter(scenario_id=scenario_id).first().__dict__
    # stream13PlasticMasses = mswCompost.fractions_to_mass()
    # mswCompost_values =
    stream13PlasticMasses = dict(zip(
        domestic_plastics,
        [mswCompost['total_mass'] * 0.0001 * plasticFractionsRecycled[i]
         for i in domestic_plastics]))

    # Creates dict of key = type of additive,
    # value = mass of additive in this stream
    stream13PETAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", stream13PlasticMasses)
    stream13HDPEAdditives = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", stream13PlasticMasses)
    stream13PVCAdditives = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", stream13PlasticMasses)
    stream13LDPEAdditives = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", stream13PlasticMasses)
    stream13PLAAdditives = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", stream13PlasticMasses)
    stream13PPAdditives = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", stream13PlasticMasses)
    stream13PSAdditives = utils.additiveMassCalculator(
        CONST.PSadditiveTypes, "ps", stream13PlasticMasses)
    stream13OtherAdditives = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", stream13PlasticMasses)

    # List of above dicts
    listOfStream13Additives = [
        stream13PETAdditives, stream13HDPEAdditives, stream13PVCAdditives,
        stream13LDPEAdditives, stream13PLAAdditives, stream13PPAdditives,
        stream13PSAdditives, stream13OtherAdditives]

    # Totals additives and resins for this stream
    stream13AdditiveTotals = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfStream13Additives)
         for i in CONST.otherResinAdditives]))

    stream13ResinMasses = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream13PlasticMasses,
                              listOfStream13Additives[i])
         for i in range(8)]))

    # MSW for this stream
    mswCompost = CONST.DEFAULTS['2018']['msw_compost']
    stream13MSW = dict(zip(
        CONST.CALC_WASTE_TYPES,
        [mswCompost[i + 1] * mswCompost[0] for i in range(10)]))

    ###########################################################################
    ###########################################################################
    # Stream 14 Calculations
    # Sheet = US Mat Flow Analysis
    # Creates dict of key = types of MSW except plastic,
    # value = mass recycled
    # (total mass recycled*proportion of each kind of plastic recycled)
    mswRecyc = MSWRecycling.objects.filter(scenario_id=scenario_id).first()
    stream14MSWValues = mswRecyc.fractions_to_mass()

    # stream14MSWValues = dict(zip(
    #     CONST.CALC_WASTE_TYPES,
    #     [mswRecyc[0] * mswRecyc[i]
    #      for i in range(1, len(CONST.CALC_WASTE_TYPES)+1)]))

    ###########################################################################
    ###########################################################################
    # Stream 15 Input
    # Sheet = US Mat Flow Analysis
    wasteFacilityEmissions = condition['waste_facility_emissions'] * 1.10231  # CellP43

    ###########################################################################
    ###########################################################################
    # Stream 24 Calculations
    # Sheet = Stream 24 - Incineration

    # Calculates mass basis, total plastic*Fraction incinerated
    stream24MassBasis = condition['total_waste'] * condition['incinerated']

    # Creates dict of bulk masses of each kind of plastic based on
    # mass basis and proportions of each plastic incinerated.
    # Key = type of plastic, value = bulk mass
    stream24PlasticMasses = dict(zip(
        domestic_plastics,
        [stream24MassBasis*plasticIncinFractionsDict[i]
         for i in domestic_plastics]))

    # Creates dict of additives based on bulk masses.
    # Key= type of additive, value = mass of additive
    stream24PETAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", stream24PlasticMasses)
    stream24HDPEAdditives = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", stream24PlasticMasses)
    stream24PVCAdditives = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", stream24PlasticMasses)
    stream24LDPEAdditives = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", stream24PlasticMasses)
    stream24PLAAdditives = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", stream24PlasticMasses)
    stream24PPAdditives = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", stream24PlasticMasses)
    stream24PSAdditives = utils.additiveMassCalculator(
        CONST.PSadditiveTypes, "ps", stream24PlasticMasses)
    stream24OtherAdditives = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", stream24PlasticMasses)

    # List of above dicts
    listOfStream24Additives = [
        stream24PETAdditives, stream24HDPEAdditives, stream24PVCAdditives,
        stream24LDPEAdditives, stream24PLAAdditives, stream24PPAdditives,
        stream24PSAdditives, stream24OtherAdditives]

    # Creates dict of total additives and resins in the stream
    stream24AdditiveTotals = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfStream24Additives)
         for i in CONST.otherResinAdditives]))
    stream24ResinMasses = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream24PlasticMasses,
                              listOfStream24Additives[i])
         for i in range(8)]))

    # Creates dict of emissions factors, then creates dict of
    # emissions associated with each type of plastic's bulk masses
    stream24EmissionsFactors = {
        "pet": 1.24, "hdpe": 1.27, "pvc": 0.67, "ldpe": 1.27, "pla": 1.25,
        "pp": 1.27, "ps": 1.64, "other": 2.33}
    stream24Emissions = dict(zip(
        domestic_plastics,
        [stream24EmissionsFactors[i] * stream24PlasticMasses[i] * 1.10231
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 25 Calculations
    # Sheet = US Mat Flow Analysis
    # Creates dict of amount of resin, additive, and non-plastic MSW
    # not incincerated
    # (value = type of resin/additive/MSW, value = mass not incinerated)
    stream25ResinMasses = dict(zip(
        domestic_plastics,
        [(stream24ResinMasses[i]+stream23ResinMasses_[i]) *
         (1-CONST.ASSUMED_VALUES["Incineration Efficiency Fraction"])
         for i in domestic_plastics]))
    stream25AdditiveMasses = dict(zip(
        CONST.otherResinAdditives,
        [(stream24AdditiveTotals[i] + stream23AdditiveMasses_[i]) *
         (1-CONST.ASSUMED_VALUES["Incineration Efficiency Fraction"])
         for i in CONST.otherResinAdditives]))

    stream25MSWValues = dict(zip(
        CONST.CALC_WASTE_TYPES,
        [(stream11MSWValues[i]) *
         (1 - CONST.ASSUMED_VALUES["Incineration Efficiency Fraction"])
         for i in CONST.CALC_WASTE_TYPES]))

    stream25AshMass = (
        sum(stream24AdditiveTotals.values()) +
        sum(stream24ResinMasses.values())) / (
            averageDensityCalculation * 0.01 * 2.05 * 0.0000011023)

    ###########################################################################
    ###########################################################################
    # Stream 26 Calculations
    # Sheet = Stream 26 Landfilled Plastic

    # Creates dict of total plastic landfilled
    stream26MassBasis = condition['total_waste'] * condition['landfilled']

    # Creates dict of
    # key = type of plastic, value = bulk mass of type of plastic
    # (mass basis for stream *proportion for each kind of plastic)
    stream26PlasticMasses = dict(zip(
        domestic_plastics,
        [stream26MassBasis*plastic_land_fractions[i]
         for i in domestic_plastics]))

    # Creates dict of additives for each kind of plastic.
    # Key = type of additive, value = mass
    stream26PETAdditives = utils.additiveMassCalculator(
        CONST.PETadditiveTypes, "pet", stream26PlasticMasses)
    stream26HDPEAdditives = utils.additiveMassCalculator(
        CONST.HDPEadditiveTypes, "hdpe", stream26PlasticMasses)
    stream26PVCAdditives = utils.additiveMassCalculator(
        CONST.PVCadditiveTypes, "pvc", stream26PlasticMasses)
    stream26LDPEAdditives = utils.additiveMassCalculator(
        CONST.LDPEadditiveTypes, "ldpe", stream26PlasticMasses)
    stream26PLAAdditives = utils.additiveMassCalculator(
        CONST.PLAadditiveTypes, "pla", stream26PlasticMasses)
    stream26PPAdditives = utils.additiveMassCalculator(
        CONST.PPadditiveTypes, "pp", stream26PlasticMasses)
    stream26PSAdditives = utils.additiveMassCalculator(
        CONST.PSadditiveTypes, "ps", stream26PlasticMasses)
    stream26OtherAdditives = utils.additiveMassCalculator(
        CONST.otherResinAdditives, "other", stream26PlasticMasses)

    # List of above created dicts
    listOfStream26Additives = [
        stream26PETAdditives, stream26HDPEAdditives, stream26PVCAdditives,
        stream26LDPEAdditives, stream26PLAAdditives, stream26PPAdditives,
        stream26PSAdditives, stream26OtherAdditives]

    # Creates dict of Sums of additives and resins in this stream
    stream26AdditiveTotals = dict(zip(
        CONST.otherResinAdditives,
        [utils.totalOfAdditiveType(i, listOfStream26Additives)
         for i in CONST.otherResinAdditives]))
    stream26ResinMasses = dict(zip(
        domestic_plastics,
        [utils.total_resin_calc(domestic_plastics[i],
                              stream26PlasticMasses,
                              listOfStream26Additives[i])
         for i in range(8)]))

    # Create dict of emissions in this stream based on bulk masses
    stream26Emissions = dict(zip(
        domestic_plastics,
        [0.04 * stream26PlasticMasses[i] * 1.10231
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 29 Calculations
    # Sheet = Stream 29 - Plastic Release
    # Create dict of resins and additives in this stream based on leak constant
    # key = type of resin or additive, value = mass
    stream29ResinMasses = dict(zip(
        domestic_plastics,
        [stream4ResinMasses_[i] *
         CONST.ASSUMED_VALUES["Plastic waste leak after landfill"]
         for i in domestic_plastics]))
    stream29AdditiveMasses = dict(zip(
        CONST.otherResinAdditives,
        [stream4AdditiveMasses_[i] *
         CONST.ASSUMED_VALUES["Plastic waste leak after landfill"] +
         (stream26AdditiveTotals[i] + stream23AdditiveMasses_[i]) * 0.00001
         for i in CONST.otherResinAdditives]))

    # key = type of plastic, value = emissions associated with release
    # (mass*0.04 for emission factor *conversion factor)
    stream29Emissions = dict(zip(
        domestic_plastics,
        [stream29ResinMasses[i] * 0.04 * 1.10231
         for i in domestic_plastics]))

    ###########################################################################
    ###########################################################################
    # Stream 30 Calculations
    # Sheet = US Mat Flow Analysis
    # Sums emissions in stream 26
    stream26totalEmissions = sum(stream26Emissions.values())

    # Inputs landfill emissions in
    FractionOfMSWEmissionLandfill = 0.15
    combinedLandfillEmissions = condition['landfill_emissions'] * FractionOfMSWEmissionLandfill

    # Sums stream 30 emissions
    stream30Emissions = stream26totalEmissions + combinedLandfillEmissions

    ###########################################################################
    ###########################################################################
    # Total Incineration Calculations
    # Sheet = US Mat Flow Analysis

    # Creates dict of total incineration for each kind of plastic and additive
    # (stream 23 + stream 24).
    totalIncinerationPlasticResin = dict(zip(
        domestic_plastics,
        [stream23ResinMasses_[i] + stream24ResinMasses[i]
         for i in domestic_plastics]))
    totalIncinerationAdditives = dict(zip(
        CONST.otherResinAdditives,
        [stream23AdditiveMasses_[i] + stream23AdditiveMasses_[i]
         for i in CONST.otherResinAdditives]))

    # Creates dict of total incineration for each kind of MSW (stream 11).
    totalIncinerationMSW = stream11MSWValues

    # Total Landfill Calculations:
    # sum stream 9, 23, 26 and subtract stream 29 resins, additive, MSW masses
    totalLandfillPlasticResin = dict(zip(
        domestic_plastics,
        [stream9ResinTotals[i] + stream23ResinMasses_[i] +
         stream26ResinMasses[i] - stream29ResinMasses[i]
         for i in domestic_plastics]))

    totalLandfillAdditives = dict(zip(
        CONST.otherResinAdditives,
        [stream9TotalAdditives[i] + stream23AdditiveMasses_[i] +
         stream26AdditiveTotals[i]-stream29AdditiveMasses[i]
         for i in CONST.otherResinAdditives]))

    totalLandfilledOtherMSW = stream12MSWValues

    ###########################################################################
    ###########################################################################
    # LCI Summary
    # Sheet= Material Flow Analysis Summary
    # Creates list of categories for following dicts

    # Manufacturing Phase
    # Used as divisor in following input calculations:
    matFlowManufactureDivisor = stream1_stream2_total + sum(
        stream20PlasticCalcMasses.values())

    # Sums each kind of resin from streams 1 and 20 and divides by
    # total mass in streams1,2, and 20; then does same for total
    # chemical additives in those same streams
    matFlowManufactureInput = dict(zip(
        domestic_plastics,
        [(stream1PlasticMasses[i] + stream20ResinMasses[i]) /
         matFlowManufactureDivisor for i in domestic_plastics]))

    matFlowManufactureInput['Chemical Additives'] = (
        sum(stream2AdditiveMasses.values()) +
        sum(stream20TotalAdditives.values())) / matFlowManufactureDivisor

    # Sums each kind of resin and additive (additives all grouped together)
    # from stream4 and divides by total mass in stream 4
    matFlowManufactureOutput = dict(zip(
        domestic_plastics,
        [stream4ResinMasses_[i] / stream4TotalMass_
         for i in domestic_plastics]))

    matFlowManufactureOutput['Chemical Additives'] = sum(
        stream4AdditiveMasses_.values()) / stream4TotalMass_

    # Littering, Inhalation, and derm expos unavailable
    matFlowManufactureLitter = dict(zip(
        CONST.INVENTORY_CATEGORIES,
        ["Unavailable" for i in CONST.INVENTORY_CATEGORIES]))

    matFlowManufactureInhal = matFlowManufactureLitter
    matFlowManufactureDerm = matFlowManufactureLitter

    # Greenhouse gas emissions from
    # manufacturing = stream3 Emission factor * conversion factor + 0.0025
    matFlowManufactureGHG = dict(zip(
        domestic_plastics,
        [stream3EmissionFactor[i] * 1.10231 + 0.0025
         for i in domestic_plastics]))
    matFlowManufactureGHG['Chemical Additives'] = matFlowManufactureGHG[
        'other']

    # TRVW (table) lists
    manufactureDictList = [
        matFlowManufactureInput, matFlowManufactureOutput,
        matFlowManufactureLitter, matFlowManufactureInhal,
        matFlowManufactureDerm, matFlowManufactureGHG]

    ###########################################################################
    ###########################################################################
    # Use Phase

    # Input same as output of manufacture
    matFlowUseInput = matFlowManufactureOutput

    # Output determined based on
    # stream 6 resins, total additives, and total mass
    matFlowUseOutput = dict(zip(
        domestic_plastics,
        [stream6ResinTotals[i] / (sum(plasticsMassDict.values()))
         for i in domestic_plastics]))
    matFlowUseOutput['Chemical Additives'] = sum(
        stream6AdditiveTotals.values()) / (sum(plasticsMassDict.values()))

    # Littering Calculations: stream 5/(total of stream 4)
    matFlowUseLittering = dict(zip(
        domestic_plastics, [(stream5ResinMasses[i]/stream4TotalMass_)
                            for i in domestic_plastics]))

    matFlowUseLittering['Chemical Additives'] = sum(
        stream5AdditiveMasses.values()) / stream4TotalMass_

    # Inhalation, dermal and GHG unavailable
    matFlowUseInhal = matFlowManufactureDerm
    matFlowUseDerm = matFlowManufactureDerm
    matFlowUseGHG = matFlowManufactureDerm

    useDictList = [
        matFlowUseInput, matFlowUseOutput, matFlowUseLittering,
        matFlowUseInhal, matFlowUseDerm, matFlowUseGHG]

    ###########################################################################
    ###########################################################################
    # Collection and Sorting Phase (CSP)

    # Input: divisor is total plastic and additive mass in stream 6, 27
    # Create dict, key = category, value = proportion of total mass. stream6+27
    matFlowCSPInputDivisor = sum(stream6AdditiveTotals.values()) + \
        sum(stream6ResinTotals.values()) + \
        sum(stream27ResinMasses.values()) + \
        sum(stream27TotalAdditivesMasses.values())

    matFlowCSPInput = dict(zip(
        domestic_plastics,
        [(stream6ResinTotals[i] + stream27ResinMasses[i])
         / matFlowCSPInputDivisor for i in domestic_plastics]))

    matFlowCSPInput['Chemical Additives'] = (
        sum(stream6AdditiveTotals.values()) +
        sum(stream27TotalAdditivesMasses.values())) / matFlowCSPInputDivisor

    # Output: stream27+16+24+26
    matFlowCSPOutput = dict(zip(
        domestic_plastics,
        [(stream27ResinMasses[i] + stream16ResinMasses_[i] +
          stream24ResinMasses[i] + stream26ResinMasses[i]) /
         matFlowCSPInputDivisor for i in domestic_plastics]))

    matFlowCSPOutput['Chemical Additives'] = (
        sum(stream27TotalAdditivesMasses.values()) +
        sum(totalAdditivesStream16_.values()) +
        sum(stream24AdditiveTotals.values()) +
        sum(stream26AdditiveTotals.values())) / matFlowCSPInputDivisor

    # Littering: Input-Output
    matFlowCSPLittering = dict(zip(
        matFlowCSPOutput.keys(),
        [matFlowCSPInput[i] - matFlowCSPOutput[i]
         for i in matFlowCSPOutput.keys()]))

    # Emissions:
    matFlowCSPGHG = dict(zip(
        CONST.INVENTORY_CATEGORIES,
        [wasteFacilityEmissions / totalStream10Waste
         for i in CONST.INVENTORY_CATEGORIES]))

    # Inhalation and dermal exposure unavailable
    matFlowCSPInhal = matFlowUseInhal
    matFlowCSPDerm = matFlowUseInhal

    # creates list of above dicts
    cspDictList = [
        matFlowCSPInput, matFlowCSPOutput, matFlowCSPLittering,
        matFlowCSPInhal, matFlowCSPDerm, matFlowCSPGHG]

    ###########################################################################
    ###########################################################################
    # Mechanical Recycling

    # Input: (stream16+19+21)/combined total of those streams
    matFlowMechRecycInputDivisor = sum(stream16PlasticCalcMasses.values()) + \
        sum(stream19AdditivesTotals.values()) + \
        sum(stream21PlasticMasses.values()) + \
        stream19DegradationProducts + stream19Contaminants

    matFlowMechRecycInput = dict(zip(
        domestic_plastics,
        [(stream16ResinMasses_[i] + stream21ResinMasses_[i]) /
         matFlowMechRecycInputDivisor for i in domestic_plastics]))

    matFlowMechRecycInput['Chemical Additives'] = (
        sum(totalAdditivesStream16_.values()) +
        sum(stream19AdditivesTotals.values()) +
        sum(stream21AdditivesTotals.values()) +
        stream19Contaminants +
        stream19DegradationProducts) / matFlowMechRecycInputDivisor

    # Output: (stream20+28+23+22)/sum of all three
    matFlowMechRecycOutDivisor = 2 * (
        sum(stream23AdditiveMasses_.values()) +
        sum(stream23ResinMasses_.values())) + \
        sum(stream22PlasticMasses.values()) + \
        sum(stream20ResinMasses.values()) + \
        sum(stream20TotalAdditives.values())

    matFlowMechRecycOutput = dict(zip(
        domestic_plastics,
        [(stream20ResinMasses[i] + 2 * stream23ResinMasses_[i] +
          stream22ResinMasses_[i]) / matFlowMechRecycOutDivisor
         for i in domestic_plastics]))

    matFlowMechRecycOutput['Chemical Additives'] = (
        sum(stream20TotalAdditives.values()) + 2 *
        sum(stream23AdditiveMasses_.values()) +
        sum(stream22AdditivesTotals.values())) / matFlowMechRecycOutDivisor

    # Releases/littering (input*0.0001)
    matFlowMechRecycLittering = dict(zip(
        CONST.INVENTORY_CATEGORIES,
        [matFlowMechRecycInput[i] * 0.0001
         for i in CONST.INVENTORY_CATEGORIES]))

    # Inhalation Exposure (105/(9.072*10^8)*21834*250)/matFlowInputDivisor*Inp
    matFlowMechRecycInhal = dict(zip(
        CONST.INVENTORY_CATEGORIES,
        [matFlowMechRecycInput[i] * (105 / (9.072 * 10**8) * 21834 * 250) /
         matFlowMechRecycInputDivisor for i in CONST.INVENTORY_CATEGORIES]))

    # Dermal Exposure (2170/(9.072*10^8))*21834*250*Input/matFlowInputDivisor
    matFlowMechRecycDermExp = dict(zip(
        CONST.INVENTORY_CATEGORIES,
        [matFlowMechRecycInput[i] * (2170 / (9.072 * 10**8)) * 21834 * 250 /
         matFlowMechRecycInputDivisor for i in CONST.INVENTORY_CATEGORIES]))

    # GHG Emissions stream16 emissions factors
    matFlowMechRecycGHG = dict(zip(
        domestic_plastics,
        [emissionFactors[i] * 1.10231 for i in domestic_plastics]))

    matFlowMechRecycGHG['Chemical Additives'] = \
        matFlowMechRecycGHG['other']

    # creates list of above dicts
    mechRecycDictList = [
        matFlowMechRecycInput, matFlowMechRecycOutput,
        matFlowMechRecycLittering, matFlowMechRecycInhal,
        matFlowMechRecycDermExp, matFlowMechRecycGHG]

    ###########################################################################
    ###########################################################################
    # Incineration
    # Input: (stream23+24)/sum of stream totals
    matFlowIncinInputDivisor = sum(stream23AdditiveMasses_.values()) + \
        sum(stream23ResinMasses_.values()) + \
        sum(stream24PlasticMasses.values())

    matFlowIncinInput = dict(zip(
        domestic_plastics,
        [(stream23ResinMasses_[i] + stream24ResinMasses[i]) /
         matFlowIncinInputDivisor for i in domestic_plastics]))

    matFlowIncinInput['Chemical Additives'] = (
        sum(stream23AdditiveMasses_.values()) +
        sum(stream24AdditiveTotals.values()))/matFlowIncinInputDivisor

    # Output: 0
    matFlowIncinOutput = dict(zip(CONST.INVENTORY_CATEGORIES,
                                  [0 for i in CONST.INVENTORY_CATEGORIES]))

    # Littering: stream25/sum of stream 23, 24
    matFlowIncinLitter = dict(zip(
        domestic_plastics,
        [stream25ResinMasses[i] / matFlowIncinInputDivisor
         for i in domestic_plastics]))

    matFlowIncinLitter['Chemical Additives'] = sum(
        stream25AdditiveMasses.values()) / matFlowIncinInputDivisor

    # Inhalataion and dermal exposure: 0
    matFlowIncinInhal = dict(zip(CONST.INVENTORY_CATEGORIES,
                                 [0 for i in CONST.INVENTORY_CATEGORIES]))
    matFlowIncinDerm = matFlowIncinInhal

    # GHG: stream24 emission factors
    matFlowIncinGHG = dict(zip(
        domestic_plastics,
        [stream24EmissionsFactors[i] * 1.10231
         for i in domestic_plastics]))

    matFlowIncinGHG['Chemical Additives'] = matFlowIncinGHG['other']

    incinDictList = [
        matFlowIncinInput, matFlowIncinOutput, matFlowIncinLitter,
        matFlowIncinInhal, matFlowIncinDerm, matFlowIncinGHG]

    ###########################################################################
    ###########################################################################
    # Landfilling:

    # Input: stream26+28/sum of the two
    matFlowLandInputDivisor = sum(stream26PlasticMasses.values()) + \
        sum(stream23ResinMasses_.values()) + \
        sum(stream23AdditiveMasses_.values())

    matFlowLandInput = dict(zip(
        domestic_plastics,
        [(stream26ResinMasses[i] + stream23ResinMasses_[i]) /
         matFlowLandInputDivisor for i in domestic_plastics]))

    matFlowLandInput['Chemical Additives'] = (
        sum(stream26AdditiveTotals.values()) +
        sum(stream23AdditiveMasses_.values())) / matFlowLandInputDivisor

    # Output = 0
    matFlowLandOutput = matFlowIncinInhal

    # Littering: stream29/sum of stream26,28
    matFlowLandLitter = dict(zip(
        domestic_plastics,
        [stream29ResinMasses[i] / matFlowLandInputDivisor
         for i in domestic_plastics]))

    matFlowLandLitter['Chemical Additives'] = (
        sum(stream29AdditiveMasses.values())/matFlowLandInputDivisor)

    # Dermal and Inhalation Exposure = 0
    matFlowLandInhal = matFlowIncinInhal
    matFlowLandDerm = matFlowIncinInhal

    # GHG: emission factor = 0.04*1.10231
    matFlowLandGHG = dict(zip(
        CONST.INVENTORY_CATEGORIES,
        [0.04 * 1.10231 for i in CONST.INVENTORY_CATEGORIES]))

    # Creates list of above dicts
    landDictList = [
        matFlowLandInput, matFlowLandOutput, matFlowLandLitter,
        matFlowLandInhal, matFlowLandDerm, matFlowLandGHG]

    ###########################################################################
    ###########################################################################
    # Stream Summary TRVW stuff
    # creates dictionary that data will be extracted from to
    # create stream summary trvw
    dummyDictionary = {}
    # to serve in place of streams where no data is
    # (e.g. no additive data in resin lists) to make sure no
    # inappropriate numbers are added to table

    # These dicts will be iterated over to look for data.
    # (e.g. will be searched for "pet", "hdpe", etc.)
    listOfStreamsForResinTRVW = [
        stream1PlasticMasses, dummyDictionary, dummyDictionary,
        stream4ResinMasses_, stream5ResinMasses, stream6ResinTotals,
        dummyDictionary, stream27ResinMasses, stream9ResinTotals,
        stream10ResinTotals, dummyDictionary, dummyDictionary,
        stream13ResinMasses, dummyDictionary, dummyDictionary,
        stream16ResinMasses_, dummyDictionary, dummyDictionary,
        dummyDictionary, stream20ResinMasses, stream21ResinMasses_,
        stream22ResinMasses_, stream23ResinMasses_, stream24ResinMasses,
        stream25ResinMasses, stream26ResinMasses, stream27ResinMasses,
        stream23ResinMasses_, stream29ResinMasses, dummyDictionary,
        totalIncinerationPlasticResin, totalLandfillPlasticResin]

    listOfStreamforAdditivesTRVW = [
        dummyDictionary, stream2AdditiveMasses, dummyDictionary,
        stream4AdditiveMasses_, stream5AdditiveMasses, stream6AdditiveTotals,
        dummyDictionary, stream27TotalAdditivesMasses, stream9TotalAdditives,
        stream10AdditiveTotals, dummyDictionary, dummyDictionary,
        stream13AdditiveTotals, dummyDictionary, dummyDictionary,
        totalAdditivesStream16_, dummyDictionary, stream18AdditiveMigration,
        stream19AdditivesTotals, stream20TotalAdditives,
        stream21AdditivesTotals, stream22AdditivesTotals,
        stream23AdditiveMasses_, stream24AdditiveTotals,
        stream25AdditiveMasses, stream26AdditiveTotals,
        stream27TotalAdditivesMasses, stream23AdditiveMasses_,
        stream29AdditiveMasses, dummyDictionary, totalIncinerationAdditives,
        totalLandfillAdditives]

    listOfStreamMSWTRVW = [
        dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary,
        dummyDictionary, dummyDictionary, dummyDictionary, stream8MSWMasses_,
        dummyDictionary, stream8MSWMasses_, stream11MSWValues,
        stream12MSWValues, stream13MSW, stream14MSWValues, dummyDictionary,
        dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary,
        dummyDictionary, dummyDictionary, dummyDictionary,
        dummyDictionary, dummyDictionary, stream25MSWValues, dummyDictionary,
        dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary,
        totalIncinerationMSW, totalLandfilledOtherMSW]

    # creates single list to be iterated over for filling stream summary trvw
    streamTRVWLists = []

    # list comprehension that will create list of lists for
    # addition to stream summary table. streamSummaryTRVWLister defined above
    streamTRVWLists = [
        utils.streamSummaryTRVWLister(listOfStreamsForResinTRVW, i)
        for i in domestic_plastics] + \
        [utils.streamSummaryTRVWLister(listOfStreamforAdditivesTRVW, i)
         for i in CONST.otherResinAdditives] + \
        [utils.streamSummaryTRVWLister(listOfStreamMSWTRVW, i)
         for i in CONST.CALC_WASTE_TYPES]

    # following list will be used to make other calculations easier later
    # on by removing row title, which can then be added later on
    listsWithoutTitles = [
        utils.streamSummaryTRVWLister(listOfStreamsForResinTRVW, i)
        for i in domestic_plastics] + \
        [utils.streamSummaryTRVWLister(listOfStreamforAdditivesTRVW, i)
         for i in CONST.otherResinAdditives] + \
        [utils.streamSummaryTRVWLister(listOfStreamMSWTRVW, i)
         for i in CONST.CALC_WASTE_TYPES]

    for i in listsWithoutTitles:
        del i[0]

    # Creates ash row list for addition to TRVW
    ashTRVWList = ['Ash', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, stream25AshMass, 0, 0, 0, 0, 0, 0, 0]

    # Creates list for column sums at bottom of table, then Creates list of
    # data lists that will be tacked on to the end of the stream summary TRVW
    totalStreamMassesList = ['Total Mass excluding emissions'] + \
        [sum([i[b] for i in listsWithoutTitles]) for b in range(32)]

    listsToAdd = [ashTRVWList, totalStreamMassesList]

    totalPlasticsStreamSummaryList = ['Total Plastics'] + [
        sum(i.values()) for i in listOfStreamsForResinTRVW]
    listsToAdd.append(totalPlasticsStreamSummaryList)

    totalAdditivesStreamSummaryList = ['Total Additives'] + [
        sum(i.values()) for i in listOfStreamforAdditivesTRVW]
    listsToAdd.append(totalAdditivesStreamSummaryList)

    actualMassEmissionTotalTRVWList = ['Actual mass of emission (Tons):'] + [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # 0, 0, '-', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, stream25AshMass, 0, 0, 0, 0, 0, 0, 0]
    listsToAdd.append(actualMassEmissionTotalTRVWList)

    totalEmissionsTRVWList = [
        'Total Emissions', 0, 0,
        (sum(stream4AdditiveMasses_.values()) +
         sum(stream4ResinMasses_.values())) * 0.0025 +
        sum(stream3Emissions.values()), 0, 0, 0,
        totalStream10Waste * 230 * 0.00110231, 0, 0, 0, 0, 0, 0, 0,
        condition['waste_facility_emissions'] * 1.10231131, 0, sum(emissionStream16.values()), 0, 0,
        sum(stream20Emissions.values()), 0, 0, sum(stream23Emissions.values()),
        0, sum(stream24Emissions.values()) +
        1.05*sum(stream11MSWValues.values()),
        sum(stream27Emissions.values()), sum(stream23Emissions.values()),
        sum(stream29Emissions.values()), stream30Emissions, 0, 0]

    listsToAdd.append(totalEmissionsTRVWList)

    emissionsFromPlasticList = [
        'Emissions from plastic', 0, 0,
        (sum(stream4AdditiveMasses_.values()) +
         sum(stream4ResinMasses_.values())) * 0.0025 +
        sum(stream3Emissions.values()), 0, 0, 0,
        totalStream10Waste * 230 * 0.00110231, 0, 0, 0, 0, 0, 0, 0,
        condition['waste_facility_emissions'] * 1.10231131, 0, sum(emissionStream16.values()), 0, 0,
        sum(stream20Emissions.values()), 0, 0, sum(stream23Emissions.values()),
        0, sum(stream24Emissions.values()), 0, sum(stream27Emissions.values()),
        sum(stream23Emissions.values()), sum(stream29Emissions.values()),
        sum(stream26Emissions.values()), 0, 0]

    listsToAdd.append(emissionsFromPlasticList)

    finalTRVWList = streamTRVWLists + listsToAdd
    # f = np.asarray(finalTRVWList, dtype=object)
    # print(f.shape)
    # scenario = Scenario.objects.filter(id=scenario_id).first()
    for values in finalTRVWList:
        key = values[0]
        for index, val in enumerate(values[1:]):
            try:
                _ = float(val)
                res = Result(scenario_id=scenario_id, stream_id=index + 1,
                             key=key, value=val)
                res.save()
            except:
                print(key, val, type(val))

    # TODO: Save the results to database.
    return True

    # streamSummaryTRVW.insert(parent ='', index ='end', iid = 0, text = '',
    # values = tuple([streamTitleRows[b]
    #                 for b in range(len(streamTitleRows))]))

    # Changes text on user specs page to confirm calcualtions are complete
    # gap_label_1.config(text='Calculations Complete')

    # Creates pie chart for data analysis stream. Shows msw composition
    # PIE CHART
    # piecharttest = np.array(msw_comp_prop)

    # make the plastic section wedge out from the center of the pie.
    # plasticexplode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5]

    ####################################################################
    ## From here, to below, all code is related to graphing
    ####################################################################

    # adjusts the whitespace to show the entirety of the figure
    # plt.rcParams["figure.figsize"] = (10, 7)

    # fig1, ax1 = plt.subplots()
    # ax1.pie(
    #     piecharttest, labels=CONST.WASTE_TYPES, explode=plasticexplode,
    #     autopct='%1.1f%%', pctdistance=0.9, labeldistance=1.05,
    #     shadow=True, startangle=180)

    # # adjust the title of the figure. pad = distance from the figure
    # ax1.set_title('MSW Composition', fontsize=18)
    # ax1.plot(label=CONST.WASTE_TYPES)

    # # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax1.axis('equal')

    # # Convert the Figure to the data frame (tab)
    # canvasPieChart = FigureCanvasTkAgg(fig1, master=plotFrame)
    # # Show the widget on the screen
    # canvasPieChart.get_tk_widget().grid(column=0, row=0)
    # # Draw the graph on the canvas?
    # canvasPieChart.draw()

    # # ### Bar Chart
    # # Creates dictionary showing amount of each kind of plastic recycled,
    # # then creates list of values from that dict
    # amountOfPlasticRecycled = dict(zip(
    #     domestic_plastics,
    #     [stream16ResinMasses_[i] + stream27ResinMasses[i]
    #      for i in domestic_plastics]))
    # barData1 = list(amountOfPlasticRecycled.values())

    # # creates list of generated plastic masses from earlier dict
    # barData2 = list(plasticsMassDict.values())

    # # ### Comparison bar graph creation
    # # Creates x-axis categories
    # index = np.arange(len(domestic_plastics))
    # bar_width = 0.35  # width of each bar

    # barChart, ax = plt.subplots()  # defines graph

    # # creates data one data set for graph
    # barRecyc = ax.bar(index, barData1, bar_width,
    #                   label="Amount Of Plastic Recycled")
    # # creates second data set for graph
    # barCollected = ax.bar(index+bar_width, barData2, bar_width,
    #                       label="Amount of Plastic Collected")
