# utils.py (plastics_eol)
# !/usr/bin/env python3
# coding=utf-8

"""Utility methods."""

from plastics_eol import constants as CONST


def get_steps(ctx, current_step):
    """
    Add Scenario creation step statuses to the provided context.

    Args:
        ctx (dict): the view's context which is modified and returned
        current_step (int): the current step's index in ALL_SCENARIO_FIELDS

    Returns:
        dict: ctx, the view's context
    """

    for idx, field in enumerate(CONST.ALL_SCENARIO_FIELDS):
        if idx is current_step:  # idx == current
            ctx[f'{field}_status_css'] = CONST.CURRENT_CSS

        elif idx > current_step:  # idx > current
            ctx[f'{field}_status_span'] = CONST.INCOMPLETE_SPAN

        else:  # idx < current
            ctx[f'{field}_status_css'] = CONST.COMPLETE_CSS
            ctx[f'{field}_status_span'] = CONST.COMPLETE_SPAN

    return ctx


def additive_mass_calc(additive_list, plastic_type, mass_dict):
    """
    Will calculate amount of each kind of additive in each kind of plastic
    based on low additive Fractions and bulk mass.

    Args:
        additive_list (list): types of additives going into type of plastic
        plastic_type (str): type of plastic
        mass_dict (dict): bulk masses

    Returns:
        _type_: _description_
    """
    # multiply bulk mass by low additive Fraction for each kind of additive
    return dict(zip(
        additive_list,
        [mass_dict[plastic_type] * CONST.LOW_ADD_FRACTIONS[i]
         for i in additive_list]
    ))


def total_resin_calc(plastic_type, plastic_mass_dict, additive_mass_list):
    """
    Calculates total mass of plastic resin in specific stream

    Args:
        plastic_type (str): plastic type
        plastic_mass_dict (dict): bulk masses
        additive_mass_list (dict): additive masses for specific plastics

    Returns:
        _type_: _description_
    """

    # sums additives in plastic's bulk mass, then subtracts to find resin mass
    return plastic_mass_dict[plastic_type] - sum(additive_mass_list.values())


#
def backwards_lump_plastic_calc(resin_mass_list, resin_type, additive_list):
    """
    Calculates bulk plastic masses in reverse of total resin calculator
    based on resin masses.

    Args:
        resin_mass_list (_type_): _description_
        resin_type (_type_): _description_
        additive_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Finds total Fraction of bulk mass that is resin
    additiveFraction = sum([CONST.LOW_ADD_FRACTIONS[i] for i in additive_list])

    # Divides to find bulk mass (lump sum)
    return resin_mass_list[resin_type] / (1 - additiveFraction)


def trvw_list_maker(list_of_dicts):
    """
    Creates lists that will be eventually added to LCI TRVW tables.
    Takes argument of list of dictionaries that are to be examined.

    Args:
        listOfDicts (_type_): _description_

    Returns:
        _type_: _description_
    """
    new_list = []
    # iterates over list of categories in LCI tables
    for i in CONST.INVENTORY_CATEGORIES:
        sub_list = []
        q = 0
        sub_list.append(i)
        for d in list_of_dicts:
            q = d[i]
            try:
                # if value is a number, will and round to three decimal
                # places and add to the TRVW list
                q = float(q)
                sub_list.append(round(q, 3))
            except ValueError:
                # if value is not a number ('Unavaible'), it will be added
                sub_list.append(d[i])
        for b in range(len(sub_list)):
            if sub_list[b] == 0:
                # Changes 0's to negligible
                sub_list[b] = "Negligible"
        new_list.append(sub_list)
    return new_list


def stream_summary_trvw_lister(list_of_dicts, category):
    """
    Create lists that will be added to stream summary TRVW tables.

    Args:
        list_of_dicts (list): list of dictionaries to be examined
        category (string): category representing the row of the table

    Returns:
        _type_: _description_
    """
    trvw_list = []
    # adds category/row name
    trvw_list.append(category)
    for i in list_of_dicts:
        if category in i:
            # add values corresponding to category from dictionary if exists
            trvw_list.append(i[category])
        else:
            # otherwise adds 0
            trvw_list.append(0)
    return trvw_list


def recycle_scaler(reported_list, plastic_total, recycled_fraction):
    """
    Perform recycling scaling calculations (Sensitivty Facts G9:G16)

    Args:
        reported_list (list): types of plastics
        plastic_total (float): total plastic mass
        recycled_fraction (float): Fraction of plastic that is recycled

    Returns:
        _type_: _description_
    """
    # TODO: Look into this logic. Can probably be simplified since domestic
    # plastic types is already a dictionary instead of a list by default.
    return dict(zip(
        CONST.DOMESTIC_PLASTICS_DENSITIES.keys(),
        # creates dictionary from above list
        [plastic_total * recycled_fraction / sum(reported_list) * i
         for i in reported_list]))


def trvw_rounder(num):
    """
    ounds numbers in stream summary trvw based on its magnitude

    Args:
        num (float): _description_

    Returns:
        _type_: _description_
    """
    value = 0
    if isinstance(num, str):
        value = num
    elif num < 1:
        if num < 0.5:
            if num < 0.1:
                if num == 0:
                    value = 0
                else:
                    value = '<0.1'
            else:
                value = '<0.5'
        else:
            value = '<1'
    else:
        value = '{:,}'.format(round(num))
    return value


def check_entry(check):
    """
    Used to make sure all data has an input.

    Args:
        check (list): _description_

    Returns:
        boolean: _description_
    """
    if check == []:
        return True
    return False


def totalOfAdditiveType(typeOfAdditive, listOfAdditiveLists):
    """Takes argument for STRING of type of additive, and LIST of dicts of
    additives

    Sums mass of additive type in specified stream

    Args:
        typeOfAdditive (_type_): _description_
        listOfAdditiveLists (_type_): _description_

    Returns:
        _type_: _description_
    """

    additiveAmount = 0
    for i in listOfAdditiveLists:
        if (typeOfAdditive in i):
            # Checks whether additive is in each list of additives, then adds
            # to total of that additive
            additiveAmount += i[typeOfAdditive]
    return additiveAmount


def backwardsLumpPlasticCalculator(resinMassList, typeOfResin, additiveList):
    """Calculates bulk plastic masses in reverse of total resin calculator,
    based on resin masses

    Args:
        resinMassList (_type_): _description_
        typeOfResin (_type_): _description_
        additiveList (_type_): _description_

    Returns:
        _type_: _description_
    """
    additiveFraction = sum(
        [CONST.lowAdditiveFractions[i] for i in additiveList]
    )  # Finds total Fraction of bulk mass that is resin
    lumpSum = resinMassList[typeOfResin] / (
        1 - additiveFraction
    )  # Divides to find bulk mass
    return lumpSum



def additiveMassCalculator(additiveList, plasticType, massDict):
    """Will calculate amount of each kind of additive in each kind of plastic
    based on low additive Fractions and bulk mass;
    key = types of additives,
    value = amount of each additive

    Args:
        additiveList (_type_): _description_
        plasticType (_type_): _description_
        massDict (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Takes argument of LIST of types of additives going into type of plastic,
    # STRING of type of plastic, then DICT of bulk masses
    newDict = dict(zip(additiveList,
                       [massDict[plasticType] * CONST.lowAdditiveFractions[i]
                        for i in additiveList])
                   )
    # takes bulk mass and multiplies by low additive Fraction for each kind
    # of additive
    return newDict


def streamSummaryTRVWLister(listOfDicts, category):
    """creates lists that will be added to stream summary TRVW tables.
    Takes argument of list of dictionaries that are to be examined,
    along with string for category that will make up the row of the table

    Args:
        listOfDicts (_type_): _description_
        category (_type_): _description_

    Returns:
        _type_: _description_
    """

    trvwList = []
    trvwList.append(category)  # adds category/row name
    for i in listOfDicts:
        if category in i:
            # adds values corresponding to category from dictionary to this
            # list if there is one, otherwise adds 0
            trvwList.append(i[category])
        else:
            trvwList.append(0)
    return trvwList