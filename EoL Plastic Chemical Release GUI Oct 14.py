import PySimpleGUI as sg
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import pandas as pd



EoLPlasticgui = tk.Tk()
EoLPlasticgui.title("Generic Scenario of End-of-Life Plastics - Chemical Additives")

my_program= ttk.Notebook(EoLPlasticgui)
my_program.pack(fill="both",expand=1)

w = 1500 # width for the Tk root
h = 800 # height for the Tk root
#get screen width and height
ws = EoLPlasticgui.winfo_screenwidth() # width of the screen
hs = EoLPlasticgui.winfo_screenheight() # height of the screen
#calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
#set the dimensions of the screen  and where it is placed
EoLPlasticgui.geometry('%dx%d+%d+%d' % (w, h, x, y-25))

    
#Create frames for GUI
my_frame1 = Frame(my_program, width=300, height=300, bg="white") #Home frame
userSpecificationsFrame = Frame(my_program, width = 300, height = 300, bg = 'white') #User specs frame
userSpecificationsCanvas = Canvas(userSpecificationsFrame, bg = 'white') #Canvas within user specs frame to allow for scrollbar
my_frame2 = Frame(userSpecificationsCanvas, width=300, height=300, bg="white") #Frame to put widgets on for user specs frame
my_frame3 = Frame(my_program, width=300, height=300, bg="white") #Material Data tab
my_frame4 = Frame(my_program, width=300, height=300, bg="white") #Will be for assumptions tab, but for now has been removed until assumptions tab is ready
my_frame5 = Frame(my_program, width=300, height = 300, bg = 'white') #For LCI Tab
my_frame6 = Frame(my_program, width = 300, height = 300, bg = 'white', bd=5) #Will be for Chemical Additives Database
dataAnalysisFrame = Frame(my_program, width = 300, height = 300, bg ='white') #Added to program for canvas on next line
dataAnalysisCanvas = Canvas(dataAnalysisFrame, bg = 'white') #Added to frame above so a scrollbar can be created
my_frame7 = Frame(dataAnalysisCanvas, width = 300, height = 300, bg = 'white', bd = 5) #Will contain widgets to display input and graphs
streamFrame = Frame(my_program, width = 300, height = 300, bg = 'white') #Will be for pop-up


#Adds tabs to top
my_program.add(my_frame1, text="Home")
my_program.add(userSpecificationsFrame, text="User Specifications")
my_program.add(streamFrame, text = 'Stream Calculations')
my_program.add(dataAnalysisFrame, text = 'Material Flow Results')
my_program.add(my_frame5, text = 'Life Cycle Inventory')
my_program.add(my_frame3, text="Material Data")
#my_program.add(my_frame4, text="Assumptions") Removed for now
my_program.add(my_frame6, text = "Chemical Additives Database")


##########################################################################################################
##########################################################################################################
#Sensitivity Analysis Sheet


#Create dictionaries of constant values that are from assumptions and will be used in calculations
assumedValues={"Plastic waste lost to littering":0.02, "Plastic waste leak after landfill":0.1, "Plastic content in compost":0.01, 
               "Total compost stream mass multiplier":1.01, "Total mass of plastic in compost stream(Tons):":426_000, 
               "Additive migration Fraction":0.02, "Incineration Efficiency Fraction":0.9999}

#Creates dictionary of low additive Fractions. key = type of additive F6:F21; value = low value for bulk mass proportion G6:G21
lowAdditiveFractions = {"Plasticizer":0.1, "Flame Retardant":0.007, "UV Stabilizer": 0.005, "Heat Stabilizer":0.005, "Antioxidant":0.005, "Slip Agent":0.001, "Lubricant":0.001, 
                        "Antistatic":0.001, "Curing Agent":0.001, "Blowing Agent":0.005, "Biocide":0.00001, "Colorant": 0.0025, "Organic Pigment":0.00001, 
                        "Clarifier/Toner": 0.00015, "Inorganic Pigment": 0.0001, "Filler": 0.00001, "Reinforcement": 0.15}

#Create lists of categories to be paired with data for each year
conditionsCategories = ["Total MSW (Tons):", "Total Plastic waste (Tons):", "Plastic Recycled (Total, domestic and export)", 
                        "Plastic Domestically Recycled Fraction", "Efficiency of Domestic Recycling", "Plastic Export Fraction", 
                        "Plastic Re-Export Fraction", "Plastic Incinerated Fraction", "Plastic Landfilled Fraction", "Waste Facility Emissions"]

typesOfWastes = ["Misc. Inorganic Waste", "Other", "Yard Trimmings", "Food", "Rubber, Leather and Textiles", "Wood", "Metals", "Glass", 
                 "Paper and Paperboard", "Plastics"]

typesOfWastesForCalculations = ["Misc. Inorganic Waste", "Other", "Yard Trimmings", "Food", "Rubber, Leather and Textiles", "Wood", "Metals", "Glass", 
                 "Paper and Paperboard"] #Note: This is the same as the one above without a plastics string

#Creates list of strings of types of plastics in domestic calculations
typesOfPlasticDomestic = ["PET", "HDPE", "PVC", "LDPE", "PLA", "PP", "PS", "Other Resin"]

#Creates list of strings of types of plastics in international calculations
typesOfPlasticsInternational = ["Ethylene", "Vinyl Chloride", "Styrene", "Other"]

#Categories for life cycle inventory (formerly known as material flow analysis)
matFlowAnalSumCategories = ["PET", "HDPE", "PVC", "LDPE", "PLA", "PP", "PS", "Other Resin", "Chemical Additives"]

#Dictionary of densities of plastics for later calculations
polymerWasteDensity = {"PET":1.365, "HDPE":952.5, "PVC":1.455, "LDPE":0.925, "PLA":1.26, "PP":905, "PS":1.055, "Other Resin":1.29}

#Creates empty lists that will be filled by user input before calculations are made
plasticRecycled = 0

conditions = []

mswCompProp = []

mswRecyc = []

mswIncin = []

mswLand = []

mswCompost =[]

repRecPlastics = []

repPlasticImport = []

repPlasticsExport = []

repPlasticsReExport = []

plasticLandFractionsList = []

plasticRecycledFractionsList = []

plasticIncinFractionsList = []


#Create 2018 data which will be added to the lists above as input by user:


conditions2018 = [292_360_000.0, 35_680_000.0, 0.084, (0.084-0.0456706), 0.6670, 0.0456706, 0.0002, 0.172271*(1-0.084), 1-0.084-0.172271*(1-0.084), 109_000_000, 630_000_000] #B2:B10

mswCompProp2018 = [0.0139, 0.0156, 0.121, 0.2159, 0.0896, 0.0619, 0.0876, 0.0419, 0.2305, 0.122] #B21:B30

mswRecyc2018 = [69_000_000.0, 0, 0.014, 0, 0, 0.0606, 0.0449, 0.1263, 0.0443, 0.666, 0.0438] #B32:B42

mswIncin2018 = [34_560_000.0, 0.023, 0.019, 0.074, 0.218, 0.166, 0.082, 0.085, 0.047, 0.122, 0.163] #B44:B54

mswLand2018 = [146_180_000.0, 0.022, 0.02, 0.072, 0.241, 0.111, 0.083, 0.095, 0.052, 0.118, 0.185] #B56:B66

mswCompost2018 =[42_600_000.0, 0, 0, 0.523, 0.477, 0, 0, 0, 0, 0, 0] #B68:B78

repRecPlastics2018 = [980000.0, 560000.0, 0, 370000.0, 0, 50000.0, 20000.0, 1110000.0] #F9:F16

repPlasticImport2018 = [139791.0, 36647.0, 19841.0, 778806.0] #E22:#25

repPlasticsExport2018 = [920477.0, 137493.0, 28071.0, 543487.0] #F22:F25

repPlasticsReExport2018 = [7246.0, 34.0, 27.0, 1038.0] #G22:G25

plasticLandFractionsList2018 = [0.13410900183711, 0.175750153092468, 0.0257195345988977, 0.251684017146356, 0.00275566442131047, 0.248009797917942, 0.0685854255970606, 0.0933864053888549]

plasticRecycledFractionsList2018 = [0.148179271708683, 0.176470588235294, 0.0235294117647059, 0.240616246498599, 0.00252100840336134, 0.228291316526611, 0.0633053221288515, 0.116526610644258]

plasticIncinFractionsList2018 = [0.13410900183711, 0.175750153092468, 0.0257195345988977, 0.251684017146356, 0.00275566442131047, 0.248009797917942, 0.0685854255970606, 0.0933864053888549]
 


#Creates list of each kind of additive added to each type of plastic based on stream 6 additive categories
PETadditiveTypes = ["UV Stabilizer", "Flame Retardant", "Antistatic", "Clarifier/Toner", "Organic Pigment"]

HDPEadditiveTypes = ["Antioxidant", "UV Stabilizer", "Colorant", "Flame Retardant", "Heat Stabilizer", "Organic Pigment"]

PVCadditiveTypes = ["Plasticizer", "Antioxidant", "Slip Agent", "Heat Stabilizer", "Lubricant", "Colorant", "Organic Pigment"]

PPadditiveTypes = ["Antioxidant", "Slip Agent", "UV Stabilizer", "Flame Retardant", "Clarifier/Toner", "Organic Pigment"]

PSadditiveTypes = ["Antioxidant", "Slip Agent", "UV Stabilizer", "Antistatic", "Colorant", "Organic Pigment"]

LDPEadditiveTypes = ["Antioxidant", "Slip Agent", "UV Stabilizer", "Flame Retardant", "Heat Stabilizer", "Colorant", "Organic Pigment"]

PLAadditiveTypes = ["Plasticizer", "Heat Stabilizer", "Filler", "Reinforcement", "Biocide", "Antioxidant", "Colorant"]

otherResinAdditives = ["Plasticizer", "Antioxidant", "UV Stabilizer", "Colorant", "Flame Retardant", "Curing Agent", "Blowing Agent", "Biocide", "Clarifier/Toner", 
                       "Inorganic Pigment", "Heat Stabilizer", "Organic Pigment", "Filler", "Reinforcement", "Lubricant", "Slip Agent", "Antistatic"]

#Creates list of 8 preceding lists
additivesListList = [PETadditiveTypes, HDPEadditiveTypes, PVCadditiveTypes, PPadditiveTypes, PSadditiveTypes, LDPEadditiveTypes, PLAadditiveTypes, otherResinAdditives]

#Will calculate amount of each kind of additive in each kind of plastic based on low additive Fractions and bulk mass; key = types of additives, value = amount of each additive
def additiveMassCalculator(additiveList, plasticType, massDict): #Takes argument of LIST of types of additives going into type of plastic, STRING of type of plastic, then DICT of bulk masses
    newDict = dict(zip(additiveList, [massDict[plasticType]*lowAdditiveFractions[i] for i in additiveList])) #takes bulk mass and multiplies by low additive Fraction for each kind of additive
    return newDict

#Sums mass of additive type in specified stream
def totalOfAdditiveType(typeOfAdditive, listOfAdditiveLists): #Takes argument for STRING of type of additive, and LIST of dicts of additives
    additiveAmount = 0
    for i in listOfAdditiveLists:
        if typeOfAdditive in i: #Checks whether additive is in each list of additives, then adds to total of that additive
            additiveAmount += i[typeOfAdditive]
    return additiveAmount

#Calculates total mass of plastic resin in specific stream
def totalResinCalculator(plasticType, plasticMassDict, additiveMassList): #Takes argument for STRING of plastic type; DICT of bulk masses; DICT of additive masses for specific plastic
    resinMass = plasticMassDict[plasticType]-sum(additiveMassList.values()) #sums additives in plastic's bulk mass, then subtracts to find resin mass
    return resinMass

#Calculates bulk plastic masses in reverse of total resin calculator, based on resin masses
def backwardsLumpPlasticCalculator(resinMassList, typeOfResin, additiveList):
    additiveFraction = sum([lowAdditiveFractions[i] for i in additiveList]) #Finds total Fraction of bulk mass that is resin
    lumpSum = resinMassList[typeOfResin]/(1-additiveFraction) #Divides to find bulk mass
    return lumpSum
        

def trvwListMaker(listOfDicts): #Creates lists that will be eventually added to LCI TRVW tables. Takes argument of list of dictionaries that are to be examined
    newList = []
    for i in matFlowAnalSumCategories: #iterates over list of categories in LCI tables
        subList = []
        q=0
        subList.append(i)
        for d in listOfDicts:
            q = d[i] #Takes value from dict
            try:
                q= float(q) #if value is a number, will and round to three decimal places and add to the TRVW list
                subList.append(round(q,3))
            except ValueError:
                subList.append(d[i]) #if value is not a number (if it is 'Unavaible'), it will be added 
        for b in range(len(subList)):
            if subList[b] == 0:
                subList[b] = "Negligible" #Changes 0's to negligible
        newList.append(subList)
    return newList

def streamSummaryTRVWLister(listOfDicts, category): #creates lists that will be added to stream summary TRVW tables. Takes argument of list of dictionaries that are to be examined, along with string for category that will make up the row of the table
    trvwList = []
    trvwList.append(category) #adds category/row name
    for i in listOfDicts:
        if category in i:
            trvwList.append(i[category]) #adds values corresponding to category from dictionary to this list if there is one, otherwise adds 0
        else: 
            trvwList.append(0)
    return trvwList
#Will accomplish recycling scaling calculations (Sensitivty Facts G9:G16)
def recycleScaler(reportedList, plasticTotal, recycledFraction): #takes input of types of plastics, total plastic mass, and Fraction of plastic that is recycled 
    newScaledDict = dict(zip(typesOfPlasticDomestic,[plasticTotal*recycledFraction/sum(reportedList)*i for i in reportedList])) #creates dictionary from above list
    return newScaledDict

def trvwRounder(num): #rounds numbers in stream summary trvw based on its magnitude
    value = 0
    if isinstance(num, str):
        value = num
    elif num<1:
        if num<0.5:
            if num<0.1:
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

def checkEntry(check): #will be used to make sure all data has an input
    if check == []:
        return True

def makeCalculations():
    assignValues() #will be removed before distribution. This is a programming shortcut
    
    #creates list of lists of input data
    listOfDataLists = [conditions, mswCompProp, mswRecyc, mswIncin, mswLand, mswCompost, repRecPlastics, repPlasticImport, repPlasticsExport,
                   repPlasticsReExport, plasticLandFractionsList, plasticRecycledFractionsList, plasticIncinFractionsList] 

    #Checks entry data lists to make sure they have data in there and returns error if necesssary
    for i in listOfDataLists:
        if checkEntry(i):
            gapLabel1.config(text = 'Not all data has been input.')
            return

    #clears LCI tables if they already had data inside
    matFlowManufactureTRVW.delete(*matFlowManufactureTRVW.get_children())
    matFlowUseTRVW.delete(*matFlowUseTRVW.get_children())
    matFlowCSPTRVW.delete(*matFlowCSPTRVW.get_children())
    matFlowMechRecycTRVW.delete(*matFlowMechRecycTRVW.get_children())
    matFlowIncinTRVW.delete(*matFlowIncinTRVW.get_children())
    matFlowLandTRVW.delete(*matFlowLandTRVW.get_children())
    
    
    
    
    #Creates dict of Fractions of total plastic landfilled are associated with each type of plastic
    plasticLandFractions = dict(zip(typesOfPlasticDomestic, plasticLandFractionsList))

    
    #Creates dictionary of proportion of each type of plastic that has been recycled. key = type of plastic A5:A12; value = proportion of each type of plastic in MSW stream B5:B12
    plasticFractionsRecycled = dict(zip(typesOfPlasticDomestic, plasticRecycledFractionsList))
    
    #Creates dict of incineration Fractions for each kind of plastic. Key = type of plastic, value = proportion of incineration make up
    plasticIncinFractionsDict = dict(zip(typesOfPlasticDomestic, plasticIncinFractionsList))
    
    #Create dictionaries of data, associating category with value
    mswGeneratedProps = dict(zip(typesOfWastes, mswCompProp)) #key = MSW waste, value = proportion of MSW 
    
    mswConditions = dict(zip(conditionsCategories, conditions)) #key = conditions (total MSW, total plastic, plastic recycled, etc.)
    
    
    #Creates dictionary of international recycling values
    repPlasticImportDict = dict(zip(typesOfPlasticsInternational, repPlasticImport))
    
    repPlasticsExportDict = dict(zip(typesOfPlasticsInternational, repPlasticsExport))
    
    repPlasticsReExportDict = dict(zip(typesOfPlasticsInternational, repPlasticsReExport))
    
    
    
    
    
    #Creates dictionary of scaled recycled masses (key = type of plastic, value = bulk mass of plastic and additives)
    scaledRec = recycleScaler(repRecPlastics, conditions[1], conditions[2]) #G9:G16
    
    
    
    ##########################################################################################################
    ##########################################################################################################
    #Stream 6 Calculations
    #Sheet = Stream 6 - PWaste Generated
    #Creates dictionary with total mass of each total type of plastic generated (total mass of plastics generated * Fraction of each kind of plastic). key = type of plastic A5:A12; value = bulk mass including additives C5:C12
    plasticsMassDict = dict(zip(typesOfPlasticDomestic, [plasticFractionsRecycled[i] * conditions[1] for i in typesOfPlasticDomestic]))
    
    
    
    #Creates dicts of additive masses in each kind of plastic in 
    PETAdditiveMasses = additiveMassCalculator(PETadditiveTypes, "PET", plasticsMassDict)
    HDPEAdditiveMasses = additiveMassCalculator(HDPEadditiveTypes, "HDPE", plasticsMassDict)
    PVCAdditiveMasses = additiveMassCalculator(PVCadditiveTypes, "PVC", plasticsMassDict)
    PPAdditiveMasses = additiveMassCalculator(PPadditiveTypes, "PP", plasticsMassDict)
    PSAdditiveMasses = additiveMassCalculator(PSadditiveTypes, "PS", plasticsMassDict)
    LDPEAdditiveMasses = additiveMassCalculator(LDPEadditiveTypes, "LDPE", plasticsMassDict)
    PLAAdditiveMasses = additiveMassCalculator(PLAadditiveTypes, "PLA", plasticsMassDict)
    otherResinAdditivesMasses = additiveMassCalculator(otherResinAdditives, "Other Resin", plasticsMassDict)
    
    #Creates list of preceding 8 dicts
    listOfStream6Additives_ = [PETAdditiveMasses, HDPEAdditiveMasses, PVCAdditiveMasses, LDPEAdditiveMasses,   PLAAdditiveMasses,
                                   PPAdditiveMasses, PSAdditiveMasses, otherResinAdditivesMasses]
    
    averageDensityCalculation = sum([polymerWasteDensity[i]*plasticFractionsRecycled[i] for i in typesOfPlasticDomestic])* 0.00000110231
    ##########################################################################################################################
    #Stream 16 Calculations
    #Sheet = Stream 16 - MechRecyc
    
    #Creates dictionary of bulk masses by multiplying scaled recycling values by the ratio of domestic recycled plastic to total recycled plastic
    stream16PlasticCalcMasses = dict(zip(typesOfPlasticDomestic, [conditions[3]/conditions[2]*scaledRec[i] for i in typesOfPlasticDomestic]))
    
    #Creates dictionary of masses of each kind of additive in each kind of plastic
    stream16PET = additiveMassCalculator(PETadditiveTypes, "PET", stream16PlasticCalcMasses)
    stream16HDPE = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream16PlasticCalcMasses)
    stream16PVC = additiveMassCalculator(PVCadditiveTypes, "PVC", stream16PlasticCalcMasses)
    stream16PP = additiveMassCalculator(PPadditiveTypes, "PP", stream16PlasticCalcMasses)
    stream16PS = additiveMassCalculator(PSadditiveTypes, "PS", stream16PlasticCalcMasses)   
    stream16LDPE = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream16PlasticCalcMasses)
    stream16PLA = additiveMassCalculator(PLAadditiveTypes, "PLA", stream16PlasticCalcMasses)
    stream16Other = additiveMassCalculator(otherResinAdditives, "Other Resin", stream16PlasticCalcMasses)
    
    #Creates dict of emissions factors per M24:M31. Key = type of additive, value = emission factor
    emissionFactors = {"PET":-1.13, "HDPE":-.88, "PVC":0, "LDPE":0, "PLA": 0, "PP":0, "PS":0, "Other Resin":-1.03}
    
    #Creates list of additive dicts in stream 16 
    listOfstream16Additives = [stream16PET, stream16HDPE, stream16PVC, stream16LDPE, stream16PLA, stream16PP, stream16PS,  stream16Other]
    
    #Calculates total amount of each kind of additive in stream 16; key = type of additive, value = total mass of additive
    totalAdditivesStream16_ = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfstream16Additives) for i in otherResinAdditives])) #Dict of additive in stream 16
    
    #Calculates Fraction of each additive of total mass of additives in stream 16; key = type of additive, value = Fraction of total 
    additiveFractionsStream16_ = dict(zip(otherResinAdditives, [totalAdditivesStream16_[i]/sum(totalAdditivesStream16_.values()) for i in otherResinAdditives]))
    
    #Calculates total amount of each resin in stream 16; key = type of plastic, value = mass of resin
    stream16ResinMasses_ = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream16PlasticCalcMasses, listOfstream16Additives[i]) for i in range(8)]))
    
    
    
    ############################################################################################
    #Stream 17
    
    #Creates dict by calculating emissions from stream 16 per emissions factors and converts to Tons of CO2. 
    #Multiplies bulk mass of each plastic by emission factor and then converts to Tons. Key = type of plastic, value = emissions in Tons of CO2
    emissionStream16 = dict(zip(typesOfPlasticDomestic, [emissionFactors[i]*stream16PlasticCalcMasses[i]*1.10231 for i in typesOfPlasticDomestic]))
    
    
    #############################################################################################
    #Stream 19
    #Sheet = Stream 19 - Contamination
    #Creates dict of additive contaminations. Key = type of additive; value = contamination 
    additiveContaminationConstant = 0.0415 #C11
    
    #Multiplies Fraction of each kind of additive by the total of plastic bulk masses in stream 16 and by the contamination constant
    stream19AdditivesTotals = dict(zip(otherResinAdditives, [additiveFractionsStream16_[i]*sum(stream16PlasticCalcMasses.values())*(additiveContaminationConstant) for i in otherResinAdditives]))
    
    
    #Calculates additives and degradation products in stream 19
    stream19Contaminants = sum(stream16PlasticCalcMasses.values())*0.0065
    stream19DegradationProducts = sum(stream16PlasticCalcMasses.values())*0.0515
    
    
    
    #################################################################################################
    #Stream 4 Calculations
    #Sheet = US Mat Flow Analysis 
    #Creates dict of total resin in stream 4, based on stream 6 and bulk plastic manufacturing for . Key = type of plastic, value = mass of resin
    stream4ResinMasses_ = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], plasticsMassDict, listOfStream6Additives_[i]) for i in range(8)]))
    
    #Creates dict of total additives in stream 4, based on stream 6 and bulk plastic manufacturing for . Key = type of additive, value = mass of additive
    stream4AdditiveMasses_ = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfStream6Additives_) for i in otherResinAdditives]))
    
    
    ##############################################################################################
    #Stream 18 Calculations
    #Sheet = US Mat Flow Analysis 
    #Creates dict of additive migration occuring in stream 18 by multiplying the mass of each kind of additive in stream 16 by the additive migration constant (0.02)
    stream18AdditiveMigration = dict(zip(otherResinAdditives, [0.02*totalAdditivesStream16_[i] for i in otherResinAdditives]))
    
    
    ###################################################################################################
    #Stream 21 Calculations
    #Sheet = Stream 21 - Import
    
    #Creates dict with key = type of plastic and value = amount of type of plastic imported based on reported Imported plastics in 
    stream21PlasticMasses = {"PET":repPlasticImportDict["Other"]*0.4, "HDPE": repPlasticImportDict["Ethylene"]/2, "PVC":repPlasticImportDict["Vinyl Chloride"], 
                             "LDPE":repPlasticImportDict["Ethylene"]/2, "PLA":0, "PP":0, "PS":repPlasticImportDict["Styrene"], "Other Resin": repPlasticImportDict["Other"]*0.6} #includes resin and additives lumped together
    
    
    #Creates dict of each kind of additive in each kind of plastic. Key = additive, value = mass of that additive
    stream21PET = additiveMassCalculator(PETadditiveTypes, "PET", stream21PlasticMasses)
    stream21HDPE = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream21PlasticMasses)
    stream21PVC = additiveMassCalculator(PVCadditiveTypes, "PVC", stream21PlasticMasses)
    stream21PP = additiveMassCalculator(PPadditiveTypes, "PP", stream21PlasticMasses)
    stream21PS = additiveMassCalculator(PSadditiveTypes, "PS", stream21PlasticMasses)   
    stream21LDPE = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream21PlasticMasses)
    stream21PLA = additiveMassCalculator(PLAadditiveTypes, "PLA", stream21PlasticMasses)
    stream21Other = additiveMassCalculator(otherResinAdditives, "Other Resin", stream21PlasticMasses)
    
    #Creates list of preceding dicts
    listOfStream21Additives_ = [stream21PET, stream21HDPE, stream21PVC, stream21LDPE, stream21PLA, stream21PP, 
                                    stream21PS,  stream21Other]
    
    #Totals each kind of additive in stream 21. Key = type of additive, value = amount of additive
    stream21AdditivesTotals = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfStream21Additives_) for i in otherResinAdditives]))
    
    #Calculates total amount of each kind of resin in stream 21. Key = type of plastic, value = amount of resin
    stream21ResinMasses_ = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream21PlasticMasses, listOfStream21Additives_[i]) for i in range(8)]))
    
    #Calculates emissions in this stream by multiplying bulk mass by 0.04 (the emissions factor) then converting into Tons of CO2
    stream21Emissions = dict(zip(typesOfPlasticDomestic, [0.04 * 1.10231* stream21PlasticMasses[i] for i in typesOfPlasticDomestic]))
    
    
    ################################################################################
    #Stream 22 Calculations
    #Sheet = Stream 22- Re-Export
    
    #Creates dict with key = type of plastic and value = amount of type of plastic reexported based on reported reexported plastics in 
    
    stream22PlasticMasses = {"PET":repPlasticsReExportDict["Other"]*0.4, "HDPE": repPlasticsReExportDict["Ethylene"]/2, "PVC":repPlasticsReExportDict["Vinyl Chloride"], 
                             "LDPE":repPlasticsReExportDict["Ethylene"]/2, "PLA":0, "PP":0, "PS":repPlasticsReExportDict["Styrene"], "Other Resin": repPlasticsReExportDict["Other"]*0.6}
    
    
    #Calculates amount of each additive in each type of plastic in stream 22. Key = type of additive, value = mass of that additive in stream 22
    stream22PET = additiveMassCalculator(PETadditiveTypes, "PET", stream22PlasticMasses)
    stream22HDPE = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream22PlasticMasses)
    stream22PVC = additiveMassCalculator(PVCadditiveTypes, "PVC", stream22PlasticMasses)
    stream22PP = additiveMassCalculator(PPadditiveTypes, "PP", stream22PlasticMasses)
    stream22PS = additiveMassCalculator(PSadditiveTypes, "PS", stream22PlasticMasses)   
    stream22LDPE = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream22PlasticMasses)
    stream22PLA = additiveMassCalculator(PLAadditiveTypes, "PLA", stream22PlasticMasses)
    stream22Other = additiveMassCalculator(otherResinAdditives, "Other Resin", stream22PlasticMasses)
    
    #Creates list of above dictionaries
    listOfStream22Additives_ = [stream22PET, stream22HDPE, stream22PVC, stream22LDPE, stream22PLA, stream22PP, 
                                    stream22PS,  stream22Other]
    
    
    #Dict: Calculates total mass of each kind of resin in stream 22. Key = type of plastic, value = mass of resin
    stream22ResinMasses_ = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream22PlasticMasses, listOfStream22Additives_[i]) for i in range(8)]))
    
    #Dict: Calculates total of each kind of additive in stream 22. Key = type of additive, value = mass of additive
    stream22AdditivesTotals = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfStream22Additives_) for i in otherResinAdditives]))
    
    #Dict: Calculates emissions in stream 22. Emission factor 0.04*bulk mass of plastic in stream 22 and then converted into Tons of CO2
    stream22Emissions = dict(zip(typesOfPlasticDomestic, [0.04 * 1.10231* stream22PlasticMasses[i] for i in typesOfPlasticDomestic]))
    
    
    
    ###############################################################################################################
    #Stream 23 Calculations
    #Sheet = Stream 23MechRec-Incin
    
    #Dictionary of resin masses in stream 23, based on efficiency of domestic recycling (1-conditions208[4])/2, then multiplied by resin mass. key = type of plastic resin, value = mass of resin
    stream23ResinMasses_ = dict(zip(typesOfPlasticDomestic, [(1-conditions[4])/2*stream16ResinMasses_[i] for i in typesOfPlasticDomestic])) #Resin alone
    
    #Dictionary of additive masses in stream 23, based on efficiency of domestic recycling (1-conditions208[4])/2, then multiplied by additive mass. key = type of plastic additive, value = mass of additive
    stream23AdditiveMasses_ = dict(zip(otherResinAdditives, [totalAdditivesStream16_[i]*(1-conditions[4])/2 for i in otherResinAdditives]))
    stream23PlasticMasses = dict(zip(typesOfPlasticDomestic, [backwardsLumpPlasticCalculator(stream23ResinMasses_, typesOfPlasticDomestic[i], additivesListList[i]) for i in range(8)]))
    #stream 23 Emissions calculations dictionary. Bulk plastic weight in stream * 0.04 * conversion factor to make units Tons of CO2. Key = type of plastic, value = emissions associated with that type
    stream23Emissions = dict(zip(typesOfPlasticDomestic, [0.04*1.10231*stream23PlasticMasses[i] for i in typesOfPlasticDomestic]))
    
    
    ###########################################################################################################
    
    #Stream28 Calculations unnecessary because they are the same as stream 23- as per sheet US Mat Flow Analysis 
    
    
    ##########################################################################################################
    #Stream 20 Calculations
    #Sheet = Stream 20 Domestic Recyc
    
    
    #Creates dictionary of stream 20 resin masses. Key = type of plastic resin, value = mass of resin: stream16+stream21-stream22-stream23-stream28 (but stream28=stream23, so stream23 is subtracted twice)
    stream20ResinMasses = dict(zip(typesOfPlasticDomestic, [stream16ResinMasses_[i]+stream21ResinMasses_[i]-stream22ResinMasses_[i]-2*stream23ResinMasses_[i] for i in typesOfPlasticDomestic]))
    
    #Creates dictionary of stream 20 additive masses. Key = type of additive, value = mass of additive: stream16-stream18+stream19+stream21-stream22-stream23-stream28 (stream28=stream23, so stream23 is substracted twice)
    stream20TotalAdditives = dict(zip(otherResinAdditives, [totalAdditivesStream16_[i]-stream18AdditiveMigration[i]+stream19AdditivesTotals[i]+stream21AdditivesTotals[i]-stream22AdditivesTotals[i]-2*stream23AdditiveMasses_[i] for i in otherResinAdditives]))
    
    #Not given bulk masses, so bulk masses calculated here. Key = type of plastic, value = bulk mass of each type of plastic
    stream20PlasticCalcMasses = dict(zip(typesOfPlasticDomestic, [backwardsLumpPlasticCalculator(stream20ResinMasses, typesOfPlasticDomestic[i], additivesListList[i]) for i in range(8)]))
    
    stream20Emissions = dict(zip(typesOfPlasticDomestic, [stream20PlasticCalcMasses[i] * emissionFactors[i] for i in typesOfPlasticDomestic]))    

    
    ###################################################################################################################################
    #Stream 1 Calculations
    #Sheet =US Mat Flow Analysis 
    #Dictionary of stream1 resin masses. Key = type of resin, value = mass of resin: stream4- stream 20
    stream1PlasticMasses = dict(zip(typesOfPlasticDomestic, [stream4ResinMasses_[i] - stream20ResinMasses[i] for i in typesOfPlasticDomestic]))
    
    
    ###########################################################################################################
    #Stream 2 Calculations
    #Sheet= US Mat Flow Analysis 
    #Dictionary of additive masses. Key = type of additive, value = mass of additive
    stream2AdditiveMasses = dict(zip(otherResinAdditives, [stream4AdditiveMasses_[i] - stream20TotalAdditives[i] for i in otherResinAdditives]))
    
    
    ##################################################################################
    #Stream 3 Calculations
    #Sheet = Stream 3 - Emissions
    
    #Sum to create mass basis for stream 3
    stream1_stream2_total = sum(stream1PlasticMasses.values())+sum(stream2AdditiveMasses.values())
    
    
    #Creats dict of Fraction of each kind of plastic in stream 3 based on total resin. Key = type of plastic, value = Fraction of total 
    stream3PlasticFractions = dict(zip(typesOfPlasticDomestic, [stream1PlasticMasses[i]/sum(stream1PlasticMasses.values()) for i in typesOfPlasticDomestic]))
    
    #Creates dict of bulk plastic masses of each kind of plastic based on Fraction determined above and mass basis. Key = type of plastic, value = bulk mass
    stream3PlasticMasses = dict(zip(typesOfPlasticDomestic, [stream3PlasticFractions[i]*stream1_stream2_total for i in typesOfPlasticDomestic])) #Lump sum
    
    #Creates dictionary of additives for each type for each kind of plastic based on bulk mass
    stream3PETAdditives = additiveMassCalculator(PETadditiveTypes, "PET", stream3PlasticMasses)
    stream3HDPEAdditives = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream3PlasticMasses)
    stream3PVCAdditives = additiveMassCalculator(PVCadditiveTypes, "PVC", stream3PlasticMasses)
    stream3LDPEAdditives = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream3PlasticMasses)
    stream3PLAAdditives = additiveMassCalculator(PLAadditiveTypes, "PLA", stream3PlasticMasses)
    stream3PPAdditives = additiveMassCalculator(PPadditiveTypes, "PP", stream3PlasticMasses)
    stream3PSAdditives = additiveMassCalculator(PSadditiveTypes, "PS", stream3PlasticMasses)
    stream3OtherAdditives = additiveMassCalculator(otherResinAdditives, "Other Resin", stream3PlasticMasses)
    
    #Creates dictionary of emisions factors for each kind of plastic. Key = type of plastic, value = emission factor
    stream3EmissionFactor = {"PET":2.2, "HDPE":1.53, "PVC":1.9, "LDPE":1.76, "PLA":2.09, "PP":1.51, "PS":2.46, "Other Resin":1.92}
    
    #Creates dictionary of emissions for stream 3. Key = type of plastic, value = emissions for that (bulk mass*emission factor*conversion factor)
    stream3Emissions = dict(zip(typesOfPlasticDomestic, [stream3EmissionFactor[i] * stream3PlasticMasses[i]*1.10231 for i in typesOfPlasticDomestic]))
    
    
    #################################################################################################################
    #Stream 5 Calculations
    #Sheet = US Mat Flow Analysis 
    polymerMigrationConstant = 4.71538E-06
    additiveMigrationConstant = 0.019945732
    
    #Creates dict of resin masses in stream 5 by multiplying by polymer migration constant defined above. Key = type of resin, value = mass of migration
    stream5ResinMasses = dict(zip(typesOfPlasticDomestic, [polymerMigrationConstant*stream4ResinMasses_[i] for i in typesOfPlasticDomestic]))
    
    #Creates dict of additive masses in stream 5 by multiplying by additive migration constant defined above. Key = type of resin, value = mass of migration
    stream5AdditiveMasses = dict(zip(otherResinAdditives, [additiveMigrationConstant*stream4AdditiveMasses_[i] for i in otherResinAdditives]))
    
    #####################################################################################################################
    #Stream 27 Calculations
    #Sheet = Stream 27 - Export
    
    #Dictionary defining mass of each kind of plastic for this stream based on Export definitions in US  Sensitivity facts. Key = type of plastic, value = bulk mass of that plastic
    stream27PlasticMasses = {"PET":repPlasticsExportDict["Other"]*0.4, "HDPE":repPlasticsExportDict["Ethylene"]/2, 
                                 "PVC":repPlasticsExportDict["Vinyl Chloride"], "LDPE":repPlasticsExportDict["Ethylene"]/2,
                                 "PLA":0, "PP": 0, "PS":repPlasticsExportDict["Styrene"], "Other Resin":repPlasticsExportDict["Other"]*0.6}
    
    #Dictionary defining mass of each kind of additive in each kind of plastic. Key = type of additive, value = mass of that additive
    stream27PETAdditives = additiveMassCalculator(PETadditiveTypes, "PET", stream27PlasticMasses)
    stream27HDPEAdditives = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream27PlasticMasses)
    stream27PVCAdditives = additiveMassCalculator(PVCadditiveTypes, "PVC", stream27PlasticMasses)
    stream27LDPEAdditives = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream27PlasticMasses)
    stream27PLAAdditives = additiveMassCalculator(PLAadditiveTypes, "PLA", stream27PlasticMasses)
    stream27PPAdditives = additiveMassCalculator(PPadditiveTypes, "PP", stream27PlasticMasses)
    stream27PSAdditives = additiveMassCalculator(PETadditiveTypes, "PS", stream27PlasticMasses)
    stream27OtherAdditives = additiveMassCalculator(otherResinAdditives, "Other Resin", stream27PlasticMasses)
    
    #List of above dictionaries
    listOfstream27Additives = [stream27PETAdditives, stream27HDPEAdditives, stream27PVCAdditives, stream27LDPEAdditives, stream27PLAAdditives,
                               stream27PPAdditives, stream27PSAdditives, stream27OtherAdditives]
    
    #Dictionary of resin masses in this stream. Key = type of resin, value = mass of resin
    stream27ResinMasses = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream27PlasticMasses, listOfstream27Additives[i]) for i in range(8)]))
    
    
    #Dictionary of additive masses in this stream. Key = type of additive, value = mass of additive
    stream27TotalAdditivesMasses = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfstream27Additives) for i in otherResinAdditives]))
    
    #Dictionary of emissions in this stream, key = type of plastic, value = emissions associated with that plastic (bulk mass *0.04 * conversion factor to make units Tons CO2))
    stream27Emissions = dict(zip(typesOfPlasticDomestic, [0.04*1.10231*stream27PlasticMasses[i] for i in typesOfPlasticDomestic]))
    
    ######################################################################################
    #Stream 8 Calculations
    #Note: stream8 plastic resins and additives are the same as stream 27 as per US Mat FLow Analysis 
    #Creates dictionary of types of MSW waste (without plastic), takes total MSW and multiplies that by their respective proportions. Key = type of MSW, value = mass of that MSW
    stream8MSWMasses_ = dict(zip(typesOfWastesForCalculations, [mswCompProp[i]*conditions[0] for i in range(len(typesOfWastesForCalculations))]))
    
    
    ####################################################################################################
    #Stream 9 Calculations
    #Sheet = Stream 9 - Litter
    #Determines total mass of stream 4, then multiplies it by littering constant to determine mass of littered plastic
    stream4TotalMass_ = sum(stream4AdditiveMasses_.values())+sum(stream4ResinMasses_.values())
    stream9TotalMass_ = 0.02*stream4TotalMass_
    
    #Creates dictionary of bulk plastic masses based on proportions of plastic generated and mass basis for stream. Key = type of plastic, value = bulk mass littered 
    stream9PlasticMasses_ = dict(zip(typesOfPlasticDomestic, [stream9TotalMass_*plasticFractionsRecycled[i] for i in typesOfPlasticDomestic]))
    
    
    #Creates dictionary of additives in littered plastic based on bulk masses determined above. Key = type of additive, value = mass of additive
    stream9PETAdditives = additiveMassCalculator(PETadditiveTypes, "PET", stream9PlasticMasses_)
    stream9HDPEAdditives = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream9PlasticMasses_)
    stream9PVCAdditives = additiveMassCalculator(PVCadditiveTypes, "PVC", stream9PlasticMasses_)
    stream9LDPEAdditives = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream9PlasticMasses_)
    stream9PLAAdditives = additiveMassCalculator(PLAadditiveTypes, "PLA", stream9PlasticMasses_)
    stream9PPAdditives = additiveMassCalculator(PPadditiveTypes, "PP", stream9PlasticMasses_)
    stream9PSAdditives = additiveMassCalculator(PSadditiveTypes, "PS", stream9PlasticMasses_)
    stream9OtherAdditives = additiveMassCalculator(otherResinAdditives, "Other Resin", stream9PlasticMasses_)
    
    #Creates list of above dicts
    listOfstream9Additives = [stream9PETAdditives, stream9HDPEAdditives, stream9PVCAdditives, stream9LDPEAdditives, stream9PLAAdditives,
                               stream9PPAdditives, stream9PSAdditives, stream9OtherAdditives]
    
    #Creates dictionary of total of each kind of additive in this stream. Key = type of additive, value = total mass of additive in this stream
    stream9TotalAdditives = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfstream9Additives) for i in otherResinAdditives]))
    
    #Creates dict of total resin in this stream. Key= type of resin, value = mass of resin in this stream
    stream9ResinTotals = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream9PlasticMasses_, listOfstream9Additives[i]) for i in range(8)]))
    
    ###############################################################################################################
    #Stream 6 Pt. 2
    
    #Dict of resin values in this stream
    stream6ResinTotals = dict(zip(typesOfPlasticDomestic, [stream4ResinMasses_[i] - stream5ResinMasses[i] for i in typesOfPlasticDomestic]))
    
    #Dict of additive values in this stream
    stream6AdditiveTotals = dict(zip(otherResinAdditives, [stream4AdditiveMasses_[i] - stream5AdditiveMasses[i] for i in otherResinAdditives]))
    
    ########################################################################################
    #Stream 10 Calculations
    #Sheet = US Mat Flow Analysis 
    
    #Creates dict of resin totals in this stream. Key = type of resin, value = mass of resin (stream6-stream9+stream27)
    stream10ResinTotals = dict(zip(typesOfPlasticDomestic, [stream6ResinTotals[i] - stream9ResinTotals[i] + stream27ResinMasses[i] for i in typesOfPlasticDomestic]))
    
    
    #Creates dict of additive totals in this stream. Key = type of additive, value = mass of additive (stream6-stream9+stream27)
    stream10AdditiveTotals = dict(zip(otherResinAdditives, [stream6AdditiveTotals[i] - stream9TotalAdditives[i]+stream27TotalAdditivesMasses[i] for i in otherResinAdditives]))
    #Note: stream 10 MSW data (rows 27:35) is the same as stream 8 so will be omitted for concision purposes
    totalStream10Waste = sum(stream10AdditiveTotals.values())+sum(stream10ResinTotals.values())+sum(stream8MSWMasses_.values()) #Cell K39
    
    
    ############################################################################################################
    #Stream 7 Calculations
    #Sheet = US Mat Flow Analysis 
    stream7EmissionFactor = 230
    
    #Calculates stream 7 emissions based on total stream 10 mass, emission factor, and conversion factor to Tons of CO2
    stream7TotalEmissions = totalStream10Waste*stream7EmissionFactor*0.00110231
    
    
    ############################################################################
    #Stream 11 Calculations
    #Sheet = US Mat Flow Analysis 
    
    #Creates dictionary of key = types of MSW (except plastic); value = mass of MSW incinerated (total mass incinerated*proportion incinerated)
    stream11MSWValues = dict(zip(typesOfWastesForCalculations, [mswIncin[0]*mswIncin[i] for i in range(1,len(typesOfWastesForCalculations)+1)]))
    
    
    ##############################################################################
    #Stream 12 Calculations
    #Sheet = US Mat FLow Analysis 
    
    #Creates dict of key = types of MSW (except plastic); value = mass of MSW landfilled (total mass landfilled*proportion landfilled)
    stream12MSWValues = dict(zip(typesOfWastesForCalculations, [mswLand[0]*mswLand[i] for i in range(1, len(typesOfWastesForCalculations)+1)]))
    
    
    ############################################################################
    #Stream 13 Calculations
    #Sheet = Stream 13-Plastic Compost
    
    #Creates dict of key = type of plastic, value = mass*0.01Fraction*Fraction of each kind of plastic. 
    stream13PlasticMasses = dict(zip(typesOfPlasticDomestic, [mswCompost[0]*0.0001*plasticFractionsRecycled[i] for i in typesOfPlasticDomestic]))
    
    #Creates dict of key = type of additive, value = mass of additive in this stream
    stream13PETAdditives = additiveMassCalculator(PETadditiveTypes, "PET", stream13PlasticMasses)
    stream13HDPEAdditives = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream13PlasticMasses)
    stream13PVCAdditives = additiveMassCalculator(PVCadditiveTypes, "PVC", stream13PlasticMasses)
    stream13LDPEAdditives = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream13PlasticMasses)
    stream13PLAAdditives = additiveMassCalculator(PLAadditiveTypes, "PLA", stream13PlasticMasses)
    stream13PPAdditives = additiveMassCalculator(PPadditiveTypes, "PP", stream13PlasticMasses)
    stream13PSAdditives = additiveMassCalculator(PSadditiveTypes, "PS", stream13PlasticMasses)
    stream13OtherAdditives = additiveMassCalculator(otherResinAdditives, "Other Resin", stream13PlasticMasses)
    
    #List of above dicts
    listOfStream13Additives = [stream13PETAdditives, stream13HDPEAdditives, stream13PVCAdditives, stream13LDPEAdditives, stream13PLAAdditives,
                                   stream13PPAdditives, stream13PSAdditives, stream13OtherAdditives]
    
    #Totals additives and resins for this stream
    stream13AdditiveTotals = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfStream13Additives) for i in otherResinAdditives]))
    stream13ResinMasses = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream13PlasticMasses, listOfStream13Additives[i]) for i in range(8)]))
    
    #MSW for this stream
    stream13MSW = dict(zip(typesOfWastesForCalculations, [mswCompost[i+1]*mswCompost[0] for i in range(10)]))
    #######################################################################################################################
    #Stream 14 Calculations
    #Sheet = US Mat Flow Analysis 
    #Creates dict of key = types of MSW except plastic, value = mass recycled(total mass recycled*proportion of each kind of plastic recycled)
    stream14MSWValues = dict(zip(typesOfWastesForCalculations, [mswRecyc[0]*mswRecyc[i] for i in range(1, len(typesOfWastesForCalculations)+1)]))
    
    ######################################################################
    #Stream 15 Input
    #Sheet = US Mat Flow Analysis 
    
    wasteFacilityEmissions = conditions[9]*1.10231 #CellP43
    
    
    #########################################################################
    #Stream 24 Calculations
    #Sheet = Stream 24 - Incineration
    
    
    
    
    #Calculates mass basis, total plastic*Fraction incinerated
    stream24MassBasis = conditions[1]*conditions[7]
    
    #Creates dict of bulk masses of each kind of plastic based on mass basis and proportions of each plastic incinerated. Key = type of plastic, value = bulk mass
    stream24PlasticMasses = dict(zip(typesOfPlasticDomestic, [stream24MassBasis*plasticIncinFractionsDict[i] for i in typesOfPlasticDomestic]))
    
    #Creates dict of additives based on bulk masses. Key= type of additive, value = mass of additive
    stream24PETAdditives = additiveMassCalculator(PETadditiveTypes, "PET", stream24PlasticMasses)
    stream24HDPEAdditives = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream24PlasticMasses)
    stream24PVCAdditives = additiveMassCalculator(PVCadditiveTypes, "PVC", stream24PlasticMasses)
    stream24LDPEAdditives = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream24PlasticMasses)
    stream24PLAAdditives = additiveMassCalculator(PLAadditiveTypes, "PLA", stream24PlasticMasses)
    stream24PPAdditives = additiveMassCalculator(PPadditiveTypes, "PP", stream24PlasticMasses)
    stream24PSAdditives = additiveMassCalculator(PSadditiveTypes, "PS", stream24PlasticMasses)
    stream24OtherAdditives = additiveMassCalculator(otherResinAdditives, "Other Resin", stream24PlasticMasses)
    
    #List of above dicts
    listOfStream24Additives = [stream24PETAdditives, stream24HDPEAdditives, stream24PVCAdditives, stream24LDPEAdditives, stream24PLAAdditives,
                                   stream24PPAdditives, stream24PSAdditives, stream24OtherAdditives]
    
    #Creates dict of total additives and resins in the straem
    stream24AdditiveTotals = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfStream24Additives) for i in otherResinAdditives]))
    stream24ResinMasses = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream24PlasticMasses, listOfStream24Additives[i]) for i in range(8)]))
    
    
    #Creates dict of emissions factors, then creates dict of emissions associated with each type of plastic's bulk masses
    stream24EmissionsFactors = {"PET": 1.24, "HDPE":1.27, "PVC":0.67, "LDPE": 1.27, "PLA":1.25, "PP":1.27, "PS":1.64, "Other Resin":2.33}
    stream24Emissions = dict(zip(typesOfPlasticDomestic, [stream24EmissionsFactors[i]*stream24PlasticMasses[i] *1.10231 for i in typesOfPlasticDomestic]))
    
    ##########################################################################################
    #Stream 25 Calculations
    #Sheet = US Mat Flow Analysis 
    #Creates dict of amount of resin, additive, and non-plastic MSW not incincerated (value = type of resin/additive/MSW, value = mass not incinerated)
    stream25ResinMasses = dict(zip(typesOfPlasticDomestic, [(stream24ResinMasses[i]+stream23ResinMasses_[i])*(1-assumedValues["Incineration Efficiency Fraction"]) for i in typesOfPlasticDomestic]))
    stream25AdditiveMasses = dict(zip(otherResinAdditives, [(stream24AdditiveTotals[i]+stream23AdditiveMasses_[i])*(1-assumedValues["Incineration Efficiency Fraction"]) for i in otherResinAdditives]))
    
    stream25MSWValues = dict(zip(typesOfWastesForCalculations, [(stream11MSWValues[i])*(1-assumedValues["Incineration Efficiency Fraction"]) for i in typesOfWastesForCalculations]))
    
    stream25AshMass = (sum(stream24AdditiveTotals.values())+sum(stream24ResinMasses.values()))/averageDensityCalculation * 0.01 * 2.05*0.0000011023
    #############################################################################################
    #Stream 26 Calculations
    #Sheet = Stream 26 Landfilled Plastic
    
    
    #Creates dict of total plastic landfilled
    stream26MassBasis = conditions[1]*conditions[8]
    
    #Creates dict of key = type of plastic, value = bulk mass of type of plastic (mass basis for stream *proportion for each kind of plastic)
    stream26PlasticMasses = dict(zip(typesOfPlasticDomestic, [stream26MassBasis*plasticLandFractions[i] for i in typesOfPlasticDomestic]))
    
    
    #Creates dict of additives for each kind of plastic. Key = type of additive, value = mass
    stream26PETAdditives = additiveMassCalculator(PETadditiveTypes, "PET", stream26PlasticMasses)
    stream26HDPEAdditives = additiveMassCalculator(HDPEadditiveTypes, "HDPE", stream26PlasticMasses)
    stream26PVCAdditives = additiveMassCalculator(PVCadditiveTypes, "PVC", stream26PlasticMasses)
    stream26LDPEAdditives = additiveMassCalculator(LDPEadditiveTypes, "LDPE", stream26PlasticMasses)
    stream26PLAAdditives = additiveMassCalculator(PLAadditiveTypes, "PLA", stream26PlasticMasses)
    stream26PPAdditives = additiveMassCalculator(PPadditiveTypes, "PP", stream26PlasticMasses)
    stream26PSAdditives = additiveMassCalculator(PSadditiveTypes, "PS", stream26PlasticMasses)
    stream26OtherAdditives = additiveMassCalculator(otherResinAdditives, "Other Resin", stream26PlasticMasses)
    
    #List of above created dicts
    listOfStream26Additives = [stream26PETAdditives, stream26HDPEAdditives, stream26PVCAdditives, stream26LDPEAdditives, stream26PLAAdditives,
                                   stream26PPAdditives, stream26PSAdditives, stream26OtherAdditives]
    
    #Creates dict of Sums of additives and resins in this stream
    stream26AdditiveTotals = dict(zip(otherResinAdditives, [totalOfAdditiveType(i, listOfStream26Additives) for i in otherResinAdditives]))
    stream26ResinMasses = dict(zip(typesOfPlasticDomestic, [totalResinCalculator(typesOfPlasticDomestic[i], stream26PlasticMasses, listOfStream26Additives[i]) for i in range(8)]))
    
    #Creates dict of emissions in this stream based on bulk masses in this stream
    stream26Emissions = dict(zip(typesOfPlasticDomestic, [0.04*stream26PlasticMasses[i] *1.10231 for i in typesOfPlasticDomestic]))
    
    
    #########################################################################
    #Stream 29 Calculations
    #Sheet = Stream 29 - Plastic Release
    #Creates dict of resins and additives in this stream based on leak constant. key = type of resin or additive, value = mass
    stream29ResinMasses = dict(zip(typesOfPlasticDomestic, [stream4ResinMasses_[i] * assumedValues["Plastic waste leak after landfill"] for i in typesOfPlasticDomestic]))
    stream29AdditiveMasses = dict(zip(otherResinAdditives, [stream4AdditiveMasses_[i]*assumedValues["Plastic waste leak after landfill"]+(stream26AdditiveTotals[i]+stream23AdditiveMasses_[i])*0.00001 for i in otherResinAdditives]))
    
    #Creates dict of key = type of plastic, value = emissions associated with release (mass*0.04 for emission factor *conversion factor)
    stream29Emissions = dict(zip(typesOfPlasticDomestic, [stream29ResinMasses[i]*0.04*1.10231 for i in typesOfPlasticDomestic]))
    
    ##########################################################################
    #Stream 30 Calculations
    #Sheet = US Mat Flow Analysis 
    #Sums emissions in stream 26
    stream26totalEmissions = sum(stream26Emissions.values())
    
    #Inputs landfill emissions in 
    FractionOfMSWEmissionLandfill = 0.15
    combinedLandfillEmissions = conditions[10]*FractionOfMSWEmissionLandfill
    
    #Sums stream 30 emissions
    stream30Emissions = stream26totalEmissions+combinedLandfillEmissions
    
    ###########################################################################
    #Total Incineration Calculations
    #Sheet = US Mat Flow Analysis 
    
    #Creates dict of total incineration for each kind of plastic and additive (stream 23 +stream 24).
    totalIncinerationPlasticResin = dict(zip(typesOfPlasticDomestic, [stream23ResinMasses_[i] + stream24ResinMasses[i] for i in typesOfPlasticDomestic]))
    totalIncinerationAdditives = dict(zip(otherResinAdditives, [stream23AdditiveMasses_[i]+stream23AdditiveMasses_[i] for i in otherResinAdditives]))
    
    #Creates dict of total incineration for each kind of MSW (stream 11).
    totalIncinerationMSW = stream11MSWValues
    
    #Total Landfill Calculations: sums stream 9, 23, 26 and subtracts stream 29 resins, additive, MSW masses
    totalLandfillPlasticResin = dict(zip(typesOfPlasticDomestic, [stream9ResinTotals[i]+stream23ResinMasses_[i]+stream26ResinMasses[i]-stream29ResinMasses[i] for i in typesOfPlasticDomestic]))
    totalLandfillAdditives = dict(zip(otherResinAdditives, [stream9TotalAdditives[i]+stream23AdditiveMasses_[i]+stream26AdditiveTotals[i]-stream29AdditiveMasses[i] for i in otherResinAdditives]))
    totalLandfilledOtherMSW = stream12MSWValues
    
    
    
    
    
    ################################################################################
    ################################################################################
    #LCI Summary
    #Sheet= Material Flow Analysis Summary
    #Creates list of categories for following dicts
    
    #Manufacturing Phase
    #Used as divisor in following input calculations:
    matFlowManufactureDivisor = stream1_stream2_total+sum(stream20PlasticCalcMasses.values())
    
    #Sums each kind of resin from streams 1 and 20 and divides by total mass in streams1,2, and 20; then does same for total chemical additives in those same streams
    matFlowManufactureInput = dict(zip(typesOfPlasticDomestic, [(stream1PlasticMasses[i]+stream20ResinMasses[i])/matFlowManufactureDivisor for i in typesOfPlasticDomestic]))
    matFlowManufactureInput['Chemical Additives'] = (sum(stream2AdditiveMasses.values())+sum(stream20TotalAdditives.values()))/matFlowManufactureDivisor
    
    #Sums each kind of resin and additive (additives all grouped together) from stream4 and divides by total mass in stream 4
    matFlowManufactureOutput = dict(zip(typesOfPlasticDomestic, [stream4ResinMasses_[i]/stream4TotalMass_ for i in typesOfPlasticDomestic]))
    matFlowManufactureOutput['Chemical Additives'] = sum(stream4AdditiveMasses_.values())/stream4TotalMass_
    
    
    #Littering, Inhalation, and derm expos unavailable
    matFlowManufactureLitter = dict(zip(matFlowAnalSumCategories, ["Unavailable" for i in matFlowAnalSumCategories]))
    matFlowManufactureInhal = matFlowManufactureLitter
    matFlowManufactureDerm = matFlowManufactureLitter
    
    #Greenhouse gas emissions from manufacturing= stream3 Emission factor*conversion factor +0.0025: 
    matFlowManufactureGHG = dict(zip(typesOfPlasticDomestic, [stream3EmissionFactor[i]*1.10231+0.0025 for i in typesOfPlasticDomestic]))
    matFlowManufactureGHG['Chemical Additives'] = matFlowManufactureGHG['Other Resin']
    
    
    #TRVW (table) lists
    global manufactureDictList
    manufactureDictList = []
    manufactureDictList = [matFlowManufactureInput, matFlowManufactureOutput, matFlowManufactureLitter, matFlowManufactureInhal, 
                               matFlowManufactureDerm, matFlowManufactureGHG]
    
    
    
    #####################################################
    #Use Phase
    
    #Input same as output of manufacture
    matFlowUseInput = matFlowManufactureOutput
    
    #Output determined based on stream 6 resins, total additives, and total mass
    matFlowUseOutput = dict(zip(typesOfPlasticDomestic, [stream6ResinTotals[i]/(sum(plasticsMassDict.values())) for i in typesOfPlasticDomestic]))
    matFlowUseOutput['Chemical Additives'] = sum(stream6AdditiveTotals.values())/(sum(plasticsMassDict.values()))
    
    
    #Littering Calculations: stream 5/(total of stream 4)
    matFlowUseLittering = dict(zip(typesOfPlasticDomestic, [(stream5ResinMasses[i]/stream4TotalMass_) for i in typesOfPlasticDomestic]))
    matFlowUseLittering['Chemical Additives'] = sum(stream5AdditiveMasses.values())/stream4TotalMass_
    
    #Inhalation, dermal and GHG unavailable
    matFlowUseInhal = matFlowManufactureDerm
    matFlowUseDerm = matFlowManufactureDerm
    matFlowUseGHG = matFlowManufactureDerm
    
    
    global useDictList #creates list of above dicts
    useDictList = []
    useDictList = [matFlowUseInput, matFlowUseOutput, matFlowUseLittering, matFlowUseInhal, matFlowUseDerm, 
                       matFlowUseGHG]
    
    ############################################################
    #Collection and Sorting Phase (CSP)
    
    #Input: divisor is total plastic and additive mass in stream 6, 27
    #Creates dict, key = category, value = proportion of total mass. stream6+27
    matFlowCSPInputDivisor = sum(stream6AdditiveTotals.values())+sum(stream6ResinTotals.values())+sum(stream27ResinMasses.values())+sum(stream27TotalAdditivesMasses.values())
    matFlowCSPInput = dict(zip(typesOfPlasticDomestic, [(stream6ResinTotals[i]+stream27ResinMasses[i])/matFlowCSPInputDivisor for i in typesOfPlasticDomestic]))
    matFlowCSPInput['Chemical Additives'] = (sum(stream6AdditiveTotals.values())+sum(stream27TotalAdditivesMasses.values()))/matFlowCSPInputDivisor
    
    
    #Output: stream27+16+24+26
    matFlowCSPOutput = dict(zip(typesOfPlasticDomestic, [(stream27ResinMasses[i]+stream16ResinMasses_[i]+stream24ResinMasses[i]+stream26ResinMasses[i])/matFlowCSPInputDivisor for i in typesOfPlasticDomestic]))
    matFlowCSPOutput['Chemical Additives'] = (sum(stream27TotalAdditivesMasses.values())+sum(totalAdditivesStream16_.values())+sum(stream24AdditiveTotals.values())+sum(stream26AdditiveTotals.values()))/matFlowCSPInputDivisor
    
    #Littering: Input-Output
    matFlowCSPLittering = dict(zip(matFlowCSPOutput.keys(), [matFlowCSPInput[i]-matFlowCSPOutput[i] for i in matFlowCSPOutput.keys()]))
    
    #Emissions: 
    matFlowCSPGHG = dict(zip(matFlowAnalSumCategories, [wasteFacilityEmissions/totalStream10Waste for i in matFlowAnalSumCategories]))
        
    #Inhalation and dermal exposure unavailable
    matFlowCSPInhal = matFlowUseInhal
    matFlowCSPDerm = matFlowUseInhal
    
    #creates list of above dicts
    global cspDictList
    cspDictList = []
    cspDictList = [matFlowCSPInput, matFlowCSPOutput, matFlowCSPLittering, matFlowCSPInhal, matFlowCSPDerm,
                       matFlowCSPGHG]
    
    ############################################################
    #Mechanical Recycling
    
    #Input: (stream16+19+21)/combined total of those streams
    matFlowMechRecycInputDivisor = sum(stream16PlasticCalcMasses.values())+sum(stream19AdditivesTotals.values())+sum(stream21PlasticMasses.values())+stream19DegradationProducts+stream19Contaminants
    matFlowMechRecycInput = dict(zip(typesOfPlasticDomestic, [(stream16ResinMasses_[i]+stream21ResinMasses_[i])/matFlowMechRecycInputDivisor for i in typesOfPlasticDomestic]))
    matFlowMechRecycInput['Chemical Additives']=(sum(totalAdditivesStream16_.values())+sum(stream19AdditivesTotals.values())+sum(stream21AdditivesTotals.values())+stream19Contaminants+stream19DegradationProducts)/matFlowMechRecycInputDivisor
    
    #Output: (stream20+28+23+22)/sum of all three
    matFlowMechRecycOutDivisor = 2*(sum(stream23AdditiveMasses_.values())+sum(stream23ResinMasses_.values()))+sum(stream22PlasticMasses.values())+sum(stream20ResinMasses.values())+sum(stream20TotalAdditives.values())
    matFlowMechRecycOutput = dict(zip(typesOfPlasticDomestic, [(stream20ResinMasses[i]+2*stream23ResinMasses_[i]+stream22ResinMasses_[i])/matFlowMechRecycOutDivisor for i in typesOfPlasticDomestic]))
    matFlowMechRecycOutput['Chemical Additives'] = (sum(stream20TotalAdditives.values())+2*sum(stream23AdditiveMasses_.values())+sum(stream22AdditivesTotals.values()))/matFlowMechRecycOutDivisor
    
    #Releases/littering (input*0.0001)
    matFlowMechRecycLittering = dict(zip(matFlowAnalSumCategories, [matFlowMechRecycInput[i]*0.0001 for i in matFlowAnalSumCategories]))
    
    #Inhalation Exposure (105/(9.072*10^8)*21834*250)/matFlowInputDivisor*Input
    matFlowMechRecycInhal = dict(zip(matFlowAnalSumCategories, [matFlowMechRecycInput[i]*(105/(9.072*10**8)*21834*250)/matFlowMechRecycInputDivisor for i in matFlowAnalSumCategories]))
    
    #Dermal Exposure (2170/(9.072*10^8))*21834*250*Input/matFlowInputDivisor
    matFlowMechRecycDermExp = dict(zip(matFlowAnalSumCategories, [matFlowMechRecycInput[i]*(2170/(9.072*10**8))*21834*250/matFlowMechRecycInputDivisor for i in matFlowAnalSumCategories]))
    
    #GHG Emissions stream16 emissions factors
    matFlowMechRecycGHG = dict(zip(typesOfPlasticDomestic, [emissionFactors[i]*1.10231 for i in typesOfPlasticDomestic]))
    matFlowMechRecycGHG['Chemical Additives']=matFlowMechRecycGHG['Other Resin']
    
    #creates list of above dicts
    global mechRecycDictList
    mechRecycDictList = []
    mechRecycDictList = [matFlowMechRecycInput, matFlowMechRecycOutput, matFlowMechRecycLittering, 
                             matFlowMechRecycInhal, matFlowMechRecycDermExp, matFlowMechRecycGHG]
   
    
    ###############################################################
    #Incineration
    #Input: (stream23+24)/sum of stream totals
    matFlowIncinInputDivisor = sum(stream23AdditiveMasses_.values())+sum(stream23ResinMasses_.values())+sum(stream24PlasticMasses.values())
    matFlowIncinInput = dict(zip(typesOfPlasticDomestic, [(stream23ResinMasses_[i]+stream24ResinMasses[i])/matFlowIncinInputDivisor for i in typesOfPlasticDomestic]))
    matFlowIncinInput['Chemical Additives'] = (sum(stream23AdditiveMasses_.values())+sum(stream24AdditiveTotals.values()))/matFlowIncinInputDivisor
    
    #Output: 0
    matFlowIncinOutput = dict(zip(matFlowAnalSumCategories, [0 for i in matFlowAnalSumCategories]))
    
    #Littering: stream25/sum of stream 23, 24
    matFlowIncinLitter = dict(zip(typesOfPlasticDomestic, [stream25ResinMasses[i]/matFlowIncinInputDivisor for i in typesOfPlasticDomestic]))
    matFlowIncinLitter['Chemical Additives']=sum(stream25AdditiveMasses.values())/matFlowIncinInputDivisor
    
    #Inhalataion and dermal exposure: 0
    matFlowIncinInhal = dict(zip(matFlowAnalSumCategories, [0 for i in matFlowAnalSumCategories]))
    matFlowIncinDerm = matFlowIncinInhal
    
    #GHG: stream24 emission factors
    matFlowIncinGHG = dict(zip(typesOfPlasticDomestic, [stream24EmissionsFactors[i]*1.10231 for i in typesOfPlasticDomestic]))
    matFlowIncinGHG['Chemical Additives'] = matFlowIncinGHG['Other Resin']
    
    
    global incinDictList
    incinDictList = []
    incinDictList = [matFlowIncinInput, matFlowIncinOutput, matFlowIncinLitter, matFlowIncinInhal, matFlowIncinDerm,
                         matFlowIncinGHG]
    
    ################################################################
    #Landfilling: 
    
    #Input: stream26+28/sum of the two
    matFlowLandInputDivisor = sum(stream26PlasticMasses.values())+sum(stream23ResinMasses_.values())+sum(stream23AdditiveMasses_.values())
    matFlowLandInput = dict(zip(typesOfPlasticDomestic, [(stream26ResinMasses[i]+stream23ResinMasses_[i])/matFlowLandInputDivisor for i in typesOfPlasticDomestic]))
    matFlowLandInput['Chemical Additives'] = (sum(stream26AdditiveTotals.values())+sum(stream23AdditiveMasses_.values()))/matFlowLandInputDivisor 
    
    
    #Output = 0
    matFlowLandOutput = matFlowIncinInhal
    
    #Littering: stream29/sum of stream26,28
    matFlowLandLitter = dict(zip(typesOfPlasticDomestic, [stream29ResinMasses[i]/matFlowLandInputDivisor for i in typesOfPlasticDomestic]))
    matFlowLandLitter['Chemical Additives'] = (sum(stream29AdditiveMasses.values())/matFlowLandInputDivisor)
    
    
    #Dermal and Inhalation Exposure = 0
    matFlowLandInhal = matFlowIncinInhal
    matFlowLandDerm = matFlowIncinInhal
    
    #GHG: emission factor = 0.04*1.10231
    matFlowLandGHG = dict(zip(matFlowAnalSumCategories, [0.04*1.10231 for i in matFlowAnalSumCategories]))
    
    #Creates list of above dicts
    global landDictList
    landDictList = []
    landDictList = [matFlowLandInput, matFlowLandOutput, matFlowLandLitter, matFlowLandInhal, matFlowLandDerm,
                        matFlowLandGHG]
    
    #############################################################################
    #Stream Summary TRVW shtuff
    #creates dictionary that data will be extracted from to create stream summary trvw
    dummyDictionary = {}  #to serve in place of streams where no data is (e.g. no additive data in resin lists) to make sure no inappropriate numbers are added to table
    
    #These dicts will be iterated over to look for data. (e.g. will be searched for "PET", "HDPE", etc.)
    listOfStreamsForResinTRVW = [stream1PlasticMasses, dummyDictionary, dummyDictionary, stream4ResinMasses_, stream5ResinMasses,
                                 stream6ResinTotals, dummyDictionary, stream27ResinMasses, stream9ResinTotals, stream10ResinTotals,
                                 dummyDictionary, dummyDictionary, stream13ResinMasses, dummyDictionary, dummyDictionary, stream16ResinMasses_,
                                 dummyDictionary, dummyDictionary, dummyDictionary, stream20ResinMasses, stream21ResinMasses_, stream22ResinMasses_,
                                 stream23ResinMasses_, stream24ResinMasses, stream25ResinMasses, stream26ResinMasses, stream27ResinMasses,
                                 stream23ResinMasses_, stream29ResinMasses, dummyDictionary, totalIncinerationPlasticResin, totalLandfillPlasticResin]
    
    listOfStreamforAdditivesTRVW = [dummyDictionary, stream2AdditiveMasses, dummyDictionary, stream4AdditiveMasses_, stream5AdditiveMasses, 
                                    stream6AdditiveTotals, dummyDictionary, stream27TotalAdditivesMasses, stream9TotalAdditives, stream10AdditiveTotals,
                                    dummyDictionary, dummyDictionary, stream13AdditiveTotals, dummyDictionary, dummyDictionary, totalAdditivesStream16_,
                                    dummyDictionary, stream18AdditiveMigration, stream19AdditivesTotals, stream20TotalAdditives, stream21AdditivesTotals,
                                    stream22AdditivesTotals, stream23AdditiveMasses_, stream24AdditiveTotals, stream25AdditiveMasses, stream26AdditiveTotals,
                                    stream27TotalAdditivesMasses, stream23AdditiveMasses_, stream29AdditiveMasses, dummyDictionary, totalIncinerationAdditives,
                                    totalLandfillAdditives]
    
    listOfStreamMSWTRVW = [dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, 
                           stream8MSWMasses_, dummyDictionary, stream8MSWMasses_, stream11MSWValues, stream12MSWValues, stream13MSW, stream14MSWValues,
                           dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary,
                           dummyDictionary, dummyDictionary, stream25MSWValues, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary, dummyDictionary,
                          totalIncinerationMSW, totalLandfilledOtherMSW]
    
    #creates single list to be iterated over for filling stream summary trvw
    
    global streamTRVWLists
    streamTRVWLists = []
    streamTRVWLists.clear() #clears to make sure that when new data is input, old data is erased
    
    #list comprehension that will create list of lists for addition to stream summary table. streamSummaryTRVWLister defined above
    streamTRVWLists = [streamSummaryTRVWLister(listOfStreamsForResinTRVW, i) for i in typesOfPlasticDomestic]+[streamSummaryTRVWLister(listOfStreamforAdditivesTRVW, i) for i in otherResinAdditives]+[streamSummaryTRVWLister(listOfStreamMSWTRVW, i) for i in typesOfWastesForCalculations]
   
    #following list will be used to make other calculations easier later on by removing row title, which can then be added later on
    listsWithoutTitles = [streamSummaryTRVWLister(listOfStreamsForResinTRVW, i) for i in typesOfPlasticDomestic]+[streamSummaryTRVWLister(listOfStreamforAdditivesTRVW, i) for i in otherResinAdditives]+[streamSummaryTRVWLister(listOfStreamMSWTRVW, i) for i in typesOfWastesForCalculations]
    for i in listsWithoutTitles:
        del i[0]
    
    #Creates ash row list for addition to TRVW
    ashTRVWList = ['Ash', 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,stream25AshMass, 0,0,0,0,0,0,0,]
    
    #Creates list for column sums at bottom of table, then Creates list of data lists that will be tacked on to the end of the stream summary TRVW
    totalStreamMassesList = ['Total Mass excluding emissions']+[sum([i[b] for i in listsWithoutTitles]) for b in range(32)]
    
    listsToAdd =[ashTRVWList, totalStreamMassesList]
    
    totalPlasticsStreamSummaryList = ['Total Plastics'] + [sum(i.values()) for i in listOfStreamsForResinTRVW]
    listsToAdd.append(totalPlasticsStreamSummaryList)
    
    totalAdditivesStreamSummaryList = ['Total Additives'] + [sum(i.values()) for i in listOfStreamforAdditivesTRVW]
    listsToAdd.append(totalAdditivesStreamSummaryList)
    
    actualMassEmissionTotalTRVWList = ['Actual mass of emission (Tons):'] + [0, 0, '-', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, stream25AshMass, 0, 0, 0, 0, 0, 0, 0]
    listsToAdd.append(actualMassEmissionTotalTRVWList)
    
    totalEmissionsTRVWList = ['Total Emissions', 0,0, (sum(stream4AdditiveMasses_.values())+sum(stream4ResinMasses_.values()))*0.0025+sum(stream3Emissions.values()), 0,0,0, totalStream10Waste*230*0.00110231, 0,0,0,0,0,0,0, conditions[9]*1.10231131, 0, sum(emissionStream16.values()), 0, 0, sum(stream20Emissions.values()), 0, 0, sum(stream23Emissions.values()), 0, sum(stream24Emissions.values())+1.05*sum(stream11MSWValues.values()), sum(stream27Emissions.values()), sum(stream23Emissions.values()), sum(stream29Emissions.values()), stream30Emissions, 0, 0]
    listsToAdd.append(totalEmissionsTRVWList)
    
    emissionsFromPlasticList = ['Emissions from plastic', 0,0, (sum(stream4AdditiveMasses_.values())+sum(stream4ResinMasses_.values()))*0.0025+sum(stream3Emissions.values()), 0,0,0, totalStream10Waste*230*0.00110231, 0,0,0,0,0,0,0, conditions[9]*1.10231131, 0, sum(emissionStream16.values()), 0, 0, sum(stream20Emissions.values()), 0, 0, sum(stream23Emissions.values()), 0, sum(stream24Emissions.values()),0, sum(stream27Emissions.values()), sum(stream23Emissions.values()), sum(stream29Emissions.values()), sum(stream26Emissions.values()), 0, 0]
    listsToAdd.append(emissionsFromPlasticList)
    
    
    streamTRVWLists = streamTRVWLists+listsToAdd
    #streamSummaryTRVW.insert(parent ='', index ='end', iid = 0, text = '', values = tuple([streamTitleRows[b] for b in range(len(streamTitleRows))]))

    
    #Changes text on user specs page to confirm calcualtions are complete
    gapLabel1.config(text = 'Calculations Complete')

  #Creates pie chart for data analysis stream. Shows msw composition
  #PIE CHART
    piecharttest=np.array(mswCompProp)
    plasticexplode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5] #make the plastic section wedge out from the center of the pie.
    plt.rcParams["figure.figsize"] = (10, 7) #adjusts the whitespace to show the entirety of the figure
    
    fig1, ax1=plt.subplots()
    ax1.pie(piecharttest, labels=typesOfWastes, explode=plasticexplode, autopct='%1.1f%%', pctdistance=0.9, labeldistance=1.05,
            shadow=True, startangle=180)
    ax1.set_title('MSW Composition', fontsize=18) #adjust the title of the figure. pad = distance from the figure
    ax1.plot(label=typesOfWastes)

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    canvasPieChart = FigureCanvasTkAgg(fig1, master=plotFrame) # Convert the Figure to the data frame (tab)
    canvasPieChart.get_tk_widget().grid(column = 0, row = 0) # Show the widget on the screen
    canvasPieChart.draw() # Draw the graph on the canvas?    
    
    
    ### Bar Chart
    #Creates dictionary showing amount of each kind of plastic recycled, then creates list of values from that dict
    amountOfPlasticRecycled = dict(zip(typesOfPlasticDomestic, [stream16ResinMasses_[i]+stream27ResinMasses[i] for i in typesOfPlasticDomestic]))
    barData1 = list(amountOfPlasticRecycled.values())
   
    #creates list of generated plastic masses from earlier dict
    barData2 = list(plasticsMassDict.values())
    
    
    #Comparison bar graph creation
    index = np.arange(len(typesOfPlasticDomestic)) #Creates x-axis categories
    bar_width = 0.35 #width of each bar
    
    barChart, ax = plt.subplots() #defines graph
    
    barRecyc = ax.bar(index, barData1, bar_width, label = "Amount Of Plastic Recycled") #creates data one data set for graph
    barCollected = ax.bar(index+bar_width, barData2, bar_width, label = "Amount of Plastic Collected") #creates second data set for graph
    
    #Creates labels for axes and graph
    ax.set_xlabel("Type Of Plastic")
    ax.set_ylabel("Amount (tons)")
    ax.set_title("Amount of Plastic Collected and Recycled")
    ax.set_xticks(index+bar_width/2)
    ax.set_xticklabels(typesOfPlasticDomestic)
    ax.legend()
    
    #creates canvas for placement in GUI
    barCanvas = FigureCanvasTkAgg(barChart, master = plotFrame)
    barCanvas.draw()
    barCanvas.get_tk_widget().grid(column = 1, row = 0)
    
    
    

##################################################################
#Abstract Tab

#Adding text boxes to Frame 1 
#note: this information is no longer the abstract but the instructions
#old widget names remain though sorry bout it
abstract_frame1 = tk.Text(my_frame1, bd = 0, highlightthickness= 0, bg = "white",  height = 25, width = 90)
title_frame1 = tk.Text(my_frame1, bd = 0, highlightthickness= 0, bg = "white", height = 4, width = 50)
subtitle_frame1 = tk.Text(my_frame1, bd = 0, highlightthickness = 0, bg = "white", height = 1, width =50)

#Adding text to instructions textbox (formerly the abstract)
abstract_frame1.insert(tk.INSERT, "1. Municipal solid waste (MSW) data can be input under the “User Specifications” tab. Click on this tab, then begin\nfilling in the data in the entry boxes provided. To autofill all boxes at once, click the year at the top, then “Select Year.” Alternatively, you can fill each category individually.") #abstract
abstract_frame1.insert(tk.INSERT, "\n\n2. Once a set of data is input, click “Enter Above Dataset” to submit that data and move on to the next set. At any time, you may return to previously entered data sets by clicking on the appropriate category on the left. Submitting will also\ncheck the data, ensuring all proportions sum to 1 as necessary. At any time, you may check the proportions yourself by clicking “Check Proportions.” This button will NOT submit data.") #abstract
abstract_frame1.insert(tk.INSERT, "\n\n3. Once all data has been submitted, press “Calculate Streams.” If not all data has been entered, an error message\nwill appear prompting you to go back and check that every box is filled with a number. ") #abstract
abstract_frame1.insert(tk.INSERT, "\n\n4. At this point, all calculations have been completed and you may analyze the data. In the “Stream Calculations” tab, a flow chart shows the MSW lifecycle and stream numbers and titles for the processes within.") #abstract
abstract_frame1.insert(tk.INSERT, "\n\n5. On this same page, the mass calculations for each stream are generated by clicking “Show Stream Calculations.”\nThis will generate a spreadsheet of stream data in a pop-up window that can then be exported to an Excel\nspreadsheet by clicking “Export to Excel.” ") #abstract
abstract_frame1.insert(tk.INSERT, "\n\n6. Under the “Material Flow Results” tab, various plots are shown, and clicking “Display User Input” will show the data\nvalues input by the user.") #abstract
abstract_frame1.insert(tk.INSERT, "\n\n7. The “LCI” tab shows a lifecycle inventory, giving information about each plastic resin and a lump category of plastic additives in each major step of the plastic lifecycle.") #abstract



#Add text to title
title_frame1.insert(tk.INSERT, "\nA Generic Scenario Analysis of End-of-Life Plastic\nManagement: Chemical Additives") #title for frame

#Configure title text boxes, fonts, etc.
title_frame1.tag_configure("center", justify = 'center') 
title_frame1.tag_add("center", 1.0, 'end')
title_frame1.configure(font = ("Helvetica", 24, "bold"))
subtitle_frame1.insert(tk.INSERT, "Instructions")
subtitle_frame1.tag_configure("center", justify = "center")
subtitle_frame1.tag_add("center", 1.0, 'end')
subtitle_frame1.configure(font = ("Helvetica 20 bold"))
abstract_frame1.configure(font = ("Helvetica 14"))

#disables editing of text boxes
title_frame1.config(state="disabled")
subtitle_frame1.config(state="disabled")
abstract_frame1.config(state="disabled")

#places text boxes on screen
title_frame1.pack()
subtitle_frame1.pack()
abstract_frame1.pack()


########################################################################
#LCI Tab

#Create and place canvas inside my_frame5 so that a scrollbar can be added
#Note: material flow is name carried over from older versions. This is all part of LCI Tab
#note2: material flow is an old name. this now refers to LCI, but names have been preserved
materialFlowCanvas = Canvas(my_frame5, bg = 'white')
materialFlowCanvas.pack(side = LEFT, fill = BOTH, expand = 1)

#Create and configure scrollbar
matFlowScrollbar = Scrollbar(my_frame5, orient = 'vertical', command = materialFlowCanvas.yview)
matFlowScrollbar.pack(side = 'right', fill = 'y')
matFlowScrollbar.config(command=materialFlowCanvas.yview)
materialFlowCanvas.configure(yscrollcommand=matFlowScrollbar.set)
materialFlowCanvas.bind('<Configure>', lambda e: materialFlowCanvas.configure(scrollregion = materialFlowCanvas.bbox('all')))


#Creates frame for tables that will show life cycle inventory tables and places inside canvas
materialFlowFrame = Frame(materialFlowCanvas, bg = 'white')
materialFlowCanvas.create_window((0,0), window = materialFlowFrame, anchor = 'nw')


#Creates and configures title and subtitle for LCI Frame
fontChoice = 'Helvetica 12 bold'
materialFlowTitle = tk.Text(materialFlowFrame, bd = 0, highlightthickness = 0, bg = 'white', height = 2, width = 50)
materialFlowTitle.insert(tk.INSERT, "\nLife Cycle Inventory")
materialFlowTitle.tag_configure("center", justify = 'center') 
materialFlowTitle.tag_add("center", 1.0, 'end')
materialFlowTitle.configure(font = ("Helvetica 20 bold"))
materialFlowTitle.config(state = 'disabled')

materialFlowSubtitle = tk.Text(materialFlowFrame, bd = 0, highlightthickness = 0, bg = 'white', height = 1, width = 75)
materialFlowSubtitle.insert(tk.INSERT, 'Select year or custom in "User Specifications" tab to populate table.')
materialFlowSubtitle.tag_configure("center", justify = 'center') 
materialFlowSubtitle.tag_add("center", 1.0, 'end')
materialFlowSubtitle.configure(font = ("Helvetica 16 bold"))
materialFlowSubtitle.config(state = 'disabled')

#places title and subtitle
materialFlowTitle.pack()
materialFlowSubtitle.pack()


#Creates  tables (TRVWs) that will contain LCI information
matFlowManufactureTRVW = ttk.Treeview(materialFlowFrame)
matFlowUseTRVW = ttk.Treeview(materialFlowFrame)
matFlowCSPTRVW = ttk.Treeview(materialFlowFrame)
matFlowMechRecycTRVW = ttk.Treeview(materialFlowFrame)
matFlowIncinTRVW = ttk.Treeview(materialFlowFrame)
matFlowLandTRVW = ttk.Treeview(materialFlowFrame)

#Creates title for each TRVW
matFlowManufactureText = Text(materialFlowFrame, bd=0, highlightthickness = 0, bg = "white", height = 3, width = 125)
matFlowUseText = Text(materialFlowFrame, bd=0, highlightthickness = 0, bg = "white", height = 3, width = 125)
matFlowCSPText = Text(materialFlowFrame, bd=0, highlightthickness = 0, bg = "white", height = 3, width = 125)
matFlowMechRecycText = Text(materialFlowFrame, bd=0, highlightthickness = 0, bg = "white", height = 3, width = 125)
matFlowIncinText = Text(materialFlowFrame, bd=0, highlightthickness = 0, bg = "white", height = 3, width = 125)
matFlowLandText = Text(materialFlowFrame, bd=0, highlightthickness = 0, bg = "white", height = 3, width = 125)

#Creates lists of rows to be added to each LCI table
matFlowColumnHeadings = ('Materials', 'Input (ton/total ton input)', 'Output (ton/total ton input)', 'Releases/Littering (ton/total ton input)', 'Inhalation Exposure (Tons/total ton input)', 'Dermal Exposure (Tons/total ton input)', 'Greenhouse Gas Emissions (Tons CO2-eq/ton input)')
matFlowCategories = ['\nManufacture', "\nUse", '\nCollection and Sorting', '\nMechanical Recycling', '\nIncineration', '\nLandfill']
matFlowTRVWList = [matFlowManufactureText, matFlowManufactureTRVW, matFlowUseText, matFlowUseTRVW, matFlowCSPText, matFlowCSPTRVW, matFlowMechRecycText, 
                   matFlowMechRecycTRVW, matFlowIncinText, matFlowIncinTRVW, matFlowLandText, matFlowLandTRVW]



for i in range(len(matFlowTRVWList)):
    if i%2 == 1:
        matFlowTRVWList[i]['columns'] = matFlowColumnHeadings #adds headers to tables and packs
        matFlowTRVWList[i].column('#0', width = 0, stretch = NO)
        for name in matFlowColumnHeadings:
            matFlowTRVWList[i].heading(name, text = name)
        matFlowTRVWList[i].pack(fill = BOTH)
    if i%2 ==0:
        matFlowTRVWList[i].insert(tk.INSERT, matFlowCategories[i//2]) #adds in between titles for each trvw
        matFlowTRVWList[i].tag_configure("center", justify = 'center')
        matFlowTRVWList[i].tag_add("center", 1.0, 'end')
        matFlowTRVWList[i].configure(font = ("Helvetica 16 bold"))
        matFlowTRVWList[i].config(state="disabled")
        matFlowTRVWList[i].pack()
    
def fillMatFlowAnalSumTRVW(): #will be used to fill each LCI trvw table
    
    try:
        manufactureList = trvwListMaker(manufactureDictList) #in case of error won't crash code
    except: 
        return
    
    #creates list for each trvw and its row
    useList = trvwListMaker(useDictList)
    cspList = trvwListMaker(cspDictList)
    mechRecycList = trvwListMaker(mechRecycDictList)
    incinList = trvwListMaker(incinDictList)
    landList = trvwListMaker(landDictList)
    count = 0
    
    #inserts above data into trvw tables
    for record in manufactureList:
        matFlowManufactureTRVW.insert(parent ='', index ='end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        count +=1
    
    count = 0
    for record in useList:
        matFlowUseTRVW.insert(parent ='', index ='end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        count +=1
        
    count = 0
    for record in cspList:
        matFlowCSPTRVW.insert(parent ='', index ='end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        count +=1
        
    count = 0
    for record in mechRecycList:
        matFlowMechRecycTRVW.insert(parent ='', index ='end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        count +=1    
        
    count = 0
    for record in incinList:
        matFlowIncinTRVW.insert(parent ='', index ='end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        count +=1    
        
    count = 0
    for record in landList:
        matFlowLandTRVW.insert(parent ='', index ='end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
        count +=1    
        
        
        
        
###################################################
### Entries tab


#makes sure that all proportions sum to within 1% of appropriate total. works for every category but conditions
def checkProportions(listOfEntries, finalSum):
    g = 0
    for i in listOfEntries:
        try:
            g += float(i.get()) #makes sure input is numbers only
        except:
            gapLabel1.config(text = 'Error: Please enter a number into each box to continue.', fg = 'red')
            return
    if  0.99*finalSum<g<1.01*finalSum: #checks to be within 1%
        gapLabel1.config(text = 'Check successful.') #indicates success
        return True
    else:
        gapLabel1.config(text = 'Proportions do not sum to 1.', fg = 'red') #indicates failure
        return False

#Above check function does not work for conditions category, so this function is used instead
def conditionsCheckProp(): 
    g = 0 
    for i in conditionsPropCheckList:
        try: #makes sure input is numbers only
            g += float(i.get())
        except:
            gapLabel1.config(text = 'Error: Please enter a number into each box to continue.')
            return
    
    h = 0
    for b in conditionsPropCheckList2:
        h+= float(b.get())
    
    standard = float(plasticRecycledPropEntry.get())  #ensures plastic recycled domestically and exported sum to total recycled
    if 0.99<g<1.01: #makes sure total waste proportions (incinerated, landfilled, recycled) sum to 1
        if 0.99*standard<h<1.01*standard:
            gapLabel1.config(text = 'Check successful.')
            return True
        else:
            gapLabel1.config(text = 'Domestic and exported recycling do not sum to total recycled Fraction.') #for if
            gapLabel1.config(fg = 'red')
    else: 
        if 0.99*standard<h<1.01*standard:
            gapLabel1.config(fg = 'red')
            gapLabel1.config(text = "Plastic recycled proportion, landfill proportion, and incineration proportion do not sum to 1.")
        else:
            gapLabel1.config(text = "Plastic recycled proportion, landfill proportion, and incineration proportion do not sum to 1. Domestic and exported recycling do not sum to total recycled Fraction.")
            gapLabel1.config(fg = 'red')
            
    return False

#Packs canvas that will have data input section on it. Canvas allows for scroll bar to be added if necessary
userSpecificationsCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
userSpecificationsCanvas.create_window((0,0), window = my_frame2, anchor = 'nw')


#Creates scrollbar for above canvas
userSpecScrollbar = Scrollbar(userSpecificationsFrame, orient = 'vertical', command = userSpecificationsCanvas.yview)
userSpecScrollbar.config(command=userSpecificationsCanvas.yview)

userSpecificationsCanvas.configure(yscrollcommand=userSpecScrollbar.set)

#Creates and configures title/subtitle for user specs tab
#Text to frame 2
title_frame2 = tk.Text(my_frame2, bd=0, highlightthickness = 0, bg = "white", height=1, width=125)
title_frame2.insert(tk.INSERT,"User Specifications")
title_frame2.tag_configure("center", justify = 'center')
title_frame2.tag_add("center", 1.0, 'end')
title_frame2.configure(font = ("Helvetica 16 bold"))
title_frame2.config(state="disabled")
title_frame2.grid(column=0,row=0,columnspan=3)

subtitle_frame2 = tk.Text(my_frame2, bd=0, highlightthickness = 0, bg = "white", height=2, width = 75)
subtitle_frame2.insert(tk.INSERT,"Please select the simulated year for default MSW composition.\nYou may adjust these values accordingly.") #" #Note: Please fill all boxes, entering 0 where applicable.")
subtitle_frame2.configure(font = ("Helvetica 10 bold"))
subtitle_frame2.tag_configure("center", justify="center")
subtitle_frame2.tag_add('center', 1.0, 'end')
subtitle_frame2.config(state="disabled")
subtitle_frame2.grid(column =0, row=1, columnspan=3)



# Dictionary to create multiple radio buttons
values = {"2016" : "2016",
          "2017" : "2017",
          "2018" : "2018",
          "2019" : "2019",
          "Custom" : "Custom"}

#Variable for those radio buttons
selectYear = StringVar()

 
# Loop is used to create multiple RadiobutTons
# rather than creating each button separately
fontChoice = 'Helvetica 9 bold' #Assign font choices

frame2Row = 2
#create radiobuttons and grid them
for (text, value) in values.items():
    Radiobutton(my_frame2, text = text, variable = selectYear,
                value = value, indicator = 0,
                background = "gray81", font = fontChoice).grid(column = 0, row = frame2Row, columnspan=3, sticky=EW, ipady=5)
    frame2Row +=1
    
#Creates functions associated with radio buttons that will auto fill the entry boxes on the input tab
def select2018():
    for i in customEntryList:
        for b in i:
            b.delete(0, END)
    for i in range(10):
        typesOfWasteEntry[i].insert(END, mswCompProp2018[i])
    for i in range(11):
        conditionsentryList[i].insert(END, conditions2018[i])
    for i in range(11):
        IncinMSWPropsEntry[i].insert(END, mswIncin2018[i])
    for i in range(11):
        recycMSWPropsEntry[i].insert(END, mswRecyc2018[i])
    for i in range(11):
        LandMSWPropsEntry[i].insert(END, mswLand2018[i])
    for i in range(11):
        CompostMSWPropsEntry[i].insert(END, mswCompost2018[i])
    for i in range(8):
        recycPlasticEntry[i].insert(END, plasticRecycledFractionsList2018[i]) 
    for i in range(8):
        LandPlasticEntry[i].insert(END, plasticLandFractionsList2018[i])
    for i in range(8):
        IncinPlasticEntry[i].insert(END, plasticIncinFractionsList2018[i])
    for i in range(8):
        RepRecycPlasticEntry[i].insert(END, repRecPlastics2018[i])
    for i in range(4):
        ImportPlasticEntry[i].insert(END, repPlasticImport2018[i])
    for i in range(4):
        ExportPlasticEntry[i].insert(END, repPlasticsExport2018[i])
    for i in range(4):
        ReExportPlasticEntry[i].insert(END, repPlasticsReExport2018[i])
    
#When custom is selected via radio button, the entry boxes will be cleared
def selectCustom():
    for i in customEntryList:
        for b in i:
            b.delete(0, END)

#When enter button below will autofill data appropriately
def clicked(value):
    totalMSWEntry.delete(0, END)
    for i in range(10):
        typesOfWasteEntry[i].delete(0,END) #Clears entry boxes
    if value == "2018":
        select2018()
    if value == 'Custom':
        selectCustom()
    if value == '2016':
        selectCustom()
    if value == '2017':
        selectCustom()
    if value == '2019':
        selectCustom()

#Create button to set year and autofill data
myButtonyear = Button(my_frame2, bg =  "grey", text="Select Year", fg = 'white', font = fontChoice, command=lambda: clicked(selectYear.get()))
myButtonyear.grid(column=0, row=8, columnspan=3, sticky=EW, ipady=5)

#Is currently a programmer's shortcut to take all values in entry boxes. This will be removed before distribution, forcing user to enter each individual category of data 
def assignValues():
    enter(typesOfWasteEntry, mswCompProp, typesOfWasteValueLabels, recycMSWPropsLabels, recycMSWPropsEntry, recycMSWButtonChecker, recycMSWAutoButton, recycMSWEnterButton)    
    enter(conditionsentryList, conditions, conditionsValueValueLabelsList, typesOfWasteLabels, typesOfWasteEntry, mswCompButtonCheck, mswCompAuto, mswCompEnter)    
    enter(IncinMSWPropsEntry, mswIncin, IncinMSWPropsValueLabels, LandMSWPropsLabels, LandMSWPropsEntry, landMSWButtonChecker, landMSWAutoButton, landMSWEnterButton)
    enter(recycMSWPropsEntry, mswRecyc, recycMSWPropsValueLabels, IncinMSWPropsLabels, IncinMSWPropsEntry, incinMSWButtonChecker, incinMSWAutoButton, incinMSWEnterButton)
    enter(LandMSWPropsEntry, mswLand, LandMSWPropsValueLabels, CompostMSWPropsLabels, CompostMSWPropsEntry, compostMSWCheckerButton, compostMSWAutoButton, compostMSWEnterButton)
    enter(CompostMSWPropsEntry, mswCompost, CompostMSWPropsValueLabels, recycPlasticLabels, recycPlasticEntry, plasticRecycButtonChecker, plasticRecycAutoButton, plasticRecycEnterButton)
    enter(recycPlasticEntry, plasticRecycledFractionsList, plasticRecycValueLabels, IncinPlasticLabels, IncinPlasticEntry, plasticIncinButtonChecker, plasticIncinAutoButton, plasticIncinEnterButton)
    enter(IncinPlasticEntry, plasticIncinFractionsList, IncinPlasticValueLabels, LandPlasticLabels, LandPlasticEntry, plasticLandButtonChecker, plasticLandAutoButton, plasticLandEnterButton)    
    enter(LandPlasticEntry, plasticLandFractionsList, LandPlasticValueLabels, RepRecycPlasticLabels, RepRecycPlasticEntry, NONE, plasticRepRecycAutoButton, plasticRepRecycEnterButton)
    enter(RepRecycPlasticEntry, repRecPlastics, RepRecycPlasticValueLabel, ImportPlasticLabels, ImportPlasticEntry, NONE, plasticImportAutoButton, plasticImportEnterButton)
    enter(ImportPlasticEntry, repPlasticImport, ImportPlasticValueLabels, ExportPlasticLabels, ExportPlasticEntry, NONE, plasticExportAutoButton, plasticExportEnterButton)
    enter(ExportPlasticEntry, repPlasticsExport, ExportPlasticValueLabels, ReExportPlasticLabels, ReExportPlasticEntry, NONE, plasticReExportAutoButton, plasticReExportEnterButton)
    enter(ReExportPlasticEntry, repPlasticsReExport, ReExportPlasticValueLabels, conditionsLabelsListForPlacement, conditionsEntryListForPlacement, conditionsButtonChecker, conditionsAutoButton, conditionsEnterButton)

#will enter data currently shown on screen
def enter(entry, appList, valueLabel, nextLabel, nextEntry, nextCheck, nextAuto, nextEnter):
    value = 0
    appList.clear()
    for i in entry:
        try:
            value = float(i.get()) #in case user doesn't enter a number
        except:
            gapLabel1.config(text = 'Error, please enter a number in each box.')
            return
        if float(entry[0].get()) >1: #this will create list that can be checked later on for correct proportions
            newList = [entry[i] for i in range(1, len(entry))]
        else:
            newList = entry
        #Below is condition that will subject data to checks unless it is a set that doesn't need to be checked
        if entry !=conditionsentryList and entry != RepRecycPlasticEntry and entry != ImportPlasticEntry and entry != ExportPlasticEntry and entry != ReExportPlasticEntry:
            if checkProportions(newList, 1):
                appList.append(value) #if check is successful, will append data
            else:
                checkProportions(newList, 1) #if check is unsuccessful, will give error message
                return
        elif entry == conditionsentryList: #will complete conditions check if conditions category is shown
            if conditionsCheckProp():
                appList.append(value)
            else:
                conditionsCheckProp()
                return
        else:
            appList.append(value) #if data doesn't need to be checked, data will be automatically appended
    for v in range(len(valueLabel)):
        valueLabel[v].config(text = str(appList[v]), fg = 'saddlebrown') #will insert data into data analysis tab so user can look at plots and see data input at the same time
    
        
    gapLabel1.config(text = 'Previous data Entered') #will give confirmation message to user that data has been entered
    
    try:
        showSection(nextLabel, nextEntry, nextCheck, nextAuto, nextEnter)
        gapLabel1.config(text = listOfEntryCategories[str(entry)])

    except:
        makeCalculations()
        
#autofills data for each category as necessary
def autofill(entry, data):
    for i in range(len(entry)):
        entry[i].delete(0, END)
        entry[i].insert(0, data[i])

#section subtitle
mswLabel = Label(my_frame2, bg = 'white', text = "Municipal Solid Waste Composition in the United States", font = 'Helvetica 12 bold')

#Creating labels for types of waste to go next to entry boxes MJC
miscInOrgWasteLabel = Label(my_frame2, text = "Misc. Inorganic Waste (Fraction): ", font = fontChoice, bg="white")
otherWasteLabel = Label(my_frame2, text = "Other (Fraction): ", font = fontChoice, bg="white")
yardTrimmingsLabel = Label(my_frame2, text = "Yard Trimmings (Fraction): ", font = fontChoice, bg="white")
foodWasteLabel = Label(my_frame2, text = "Food (Fraction): ", font = fontChoice, bg="white")
rltWasteLabel = Label(my_frame2, text = "Rubber, Leather, Textiles (Fraction): ", font = fontChoice, bg="white")
woodWasteLabel = Label(my_frame2, text = "Wood (Fraction): ", font = fontChoice, bg="white")
metalsWasteLabel = Label(my_frame2, text = "Metals (Fraction): ", font = fontChoice, bg="white")
glassWasteLabel = Label(my_frame2, text = "Glass (Fraction): ", font = fontChoice, bg="white")
paperAndBoardLabel = Label(my_frame2, text = "Paper and Paperboard (Fraction): ", font = fontChoice, bg="white")
plasticsLabel = Label(my_frame2, text = "Plastics (Fraction): ", font = fontChoice, bg="white")

#Creating list of labels MJC
typesOfWasteLabels = [mswLabel, miscInOrgWasteLabel, otherWasteLabel, yardTrimmingsLabel, foodWasteLabel, rltWasteLabel, woodWasteLabel, metalsWasteLabel, glassWasteLabel, paperAndBoardLabel, plasticsLabel]

#Entry boxes for custom waste stream creation MJC
miscInOrgWasteEntry = Entry(my_frame2, width=50)
otherWasteEntry = Entry(my_frame2, width=50)
yardTrimmingsEntry = Entry(my_frame2, width=50)
foodWasteEntry = Entry(my_frame2, width=50)
rltWasteEntry = Entry(my_frame2, width=50)
woodWasteEntry = Entry(my_frame2, width=50)
metalsWasteEntry = Entry(my_frame2, width=50)
glassWasteEntry = Entry(my_frame2, width=50)
paperAndBoardEntry = Entry(my_frame2, width=50)
plasticsEntry = Entry(my_frame2, width=50)


#Creates buttons using check, enter, and autofill functions
mswCompButtonCheck = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(typesOfWasteEntry, 1))
mswCompEnter = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(typesOfWasteEntry, mswCompProp, typesOfWasteValueLabels, recycMSWPropsLabels, recycMSWPropsEntry, recycMSWButtonChecker, recycMSWAutoButton, recycMSWEnterButton))
mswCompAuto = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(typesOfWasteEntry, mswCompProp2018))

#Create list of entry boxes to be placed MJC
typesOfWasteEntry = [miscInOrgWasteEntry, otherWasteEntry, yardTrimmingsEntry, foodWasteEntry, rltWasteEntry, woodWasteEntry, metalsWasteEntry, glassWasteEntry, paperAndBoardEntry, plasticsEntry]
 

#Creates conditions labels and entries
conditionsTitleLabel = Label(my_frame2, text = "Conditions", bg = 'white', font = 'Helvetica 12 bold')
totalMSWLabel = Label(my_frame2, text = 'Total MSW (Tons):', bg = 'white', font = fontChoice)
totalPlasticLabel = Label(my_frame2, text = 'Total Plastic Waste (Tons):', bg = 'white', font = fontChoice)
plasticRecycledPropLabel = Label(my_frame2, text = 'Total Plastic Recycled (Fraction, Domestic and Export):', bg = 'white', font = fontChoice)
plasticDomesticLabel = Label(my_frame2, text = 'Plastic Recycled Domestically (Fraction):', bg = 'white', font = fontChoice)
plasticRecycEfficiencyLabel = Label(my_frame2, text = 'Plastic Recycling Efficiency (Fraction):', bg = 'white', font = fontChoice)
plasticExportPropLabel = Label(my_frame2, text = 'Plastic Export Fraction (Fraction):', bg = 'white', font = fontChoice)
plasticReExportPropLabel = Label(my_frame2, text = "Plastic Re-Export (Fraction):", bg = 'white', font = fontChoice)
plasticIncineratedPropLabel = Label(my_frame2, text = 'Plastic Incinerated (Fraction):', bg = 'white', font = fontChoice)
plasticLandfillPropLabel = Label(my_frame2, text = "Plastic Landfilled (Fraction):", bg = 'white', font = fontChoice)
wasteFacilityEmissionsLabel = Label(my_frame2, text = 'Waste Facility Emissions (Tons):', bg = 'white', font = fontChoice)
landfillEmissionsLabel = Label(my_frame2, text = 'Emissions from Landfill (Tons):', bg = 'white', font = fontChoice)

totalMSWEntry = Entry(my_frame2, width = 50)
totalPlasticEntry = Entry(my_frame2, width = 50)
plasticRecycledPropEntry = Entry(my_frame2, width = 50)
plasticDomesticEntry = Entry(my_frame2, width = 50)
plasticRecycEfficiencyEntry = Entry(my_frame2, width = 50)
plasticExportPropEntry = Entry(my_frame2, width = 50)
plasticReExportPropEntry = Entry(my_frame2, width = 50)
plasticIncineratedPropEntry = Entry(my_frame2, width = 50)
plasticLandfillPropEntry = Entry(my_frame2, width = 50)
wasteFacilityEmissionsEntry = Entry(my_frame2, width = 50)
landfillEmissionsEntry = Entry(my_frame2, width = 50)


#creates lists of widgets for placement
conditionsLabelsListForPlacement = [conditionsTitleLabel, totalMSWLabel, totalPlasticLabel, plasticRecycledPropLabel, plasticDomesticLabel, plasticExportPropLabel, plasticReExportPropLabel,
                                    plasticRecycEfficiencyLabel, plasticIncineratedPropLabel, plasticLandfillPropLabel, wasteFacilityEmissionsLabel, landfillEmissionsLabel]

conditionsEntryListForPlacement = [totalMSWEntry, totalPlasticEntry, plasticRecycledPropEntry, plasticDomesticEntry, plasticExportPropEntry, plasticReExportPropEntry, 
                                   plasticRecycEfficiencyEntry, plasticIncineratedPropEntry, plasticLandfillPropEntry, wasteFacilityEmissionsEntry, landfillEmissionsEntry]

conditionsLabelsList = [conditionsTitleLabel, totalMSWLabel, totalPlasticLabel, plasticRecycledPropLabel, plasticDomesticLabel, plasticRecycEfficiencyLabel, plasticExportPropLabel,
                        plasticReExportPropLabel, plasticIncineratedPropLabel, plasticLandfillPropLabel, wasteFacilityEmissionsLabel, landfillEmissionsLabel]

conditionsentryList = [totalMSWEntry, totalPlasticEntry, plasticRecycledPropEntry, plasticDomesticEntry, plasticRecycEfficiencyEntry, plasticExportPropEntry,
                       plasticReExportPropEntry, plasticIncineratedPropEntry, plasticLandfillPropEntry, wasteFacilityEmissionsEntry, landfillEmissionsEntry]


#Creates list of conditions entries that will be used for checking
conditionsPropCheckList = [plasticRecycledPropEntry, plasticIncineratedPropEntry, plasticLandfillPropEntry]
conditionsPropCheckList2 = [plasticDomesticEntry, plasticExportPropEntry, plasticReExportPropEntry]

#Creates buttons for checking, autofilling, and entering
conditionsButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = conditionsCheckProp)
conditionsAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(conditionsentryList, conditions2018))
conditionsEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(conditionsentryList, conditions, conditionsValueValueLabelsList, typesOfWasteLabels, typesOfWasteEntry, mswCompButtonCheck, mswCompAuto, mswCompEnter))



#Recycling data input labels and entry boxes
totalRecycLabel = Label(my_frame2, text = "Recycling Data", bg = 'white', font = 'Helvetica 12 bold')
totalRecycMassLabel = Label(my_frame2, text = "Total Recycled Mass:", bg = 'white', font = fontChoice)
miscInOrgRecycLabel = Label(my_frame2, text = "Misc. Inorg Waste (Fraction): ", bg = 'white', font = fontChoice)
otherWasteRecycLabel = Label(my_frame2, text = "Other (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsRecycLabel = Label(my_frame2, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodRecycLabel = Label(my_frame2, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltRecycLabel = Label(my_frame2, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodRecycLabel = Label(my_frame2, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalRecycLabel = Label(my_frame2, text = "Metals (Fraction):", bg = 'white', font = fontChoice)
glassRecycLabel = Label(my_frame2, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperRecycLabel = Label(my_frame2, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticRecycLabel = Label(my_frame2, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)

totalRecycMassEntry = Entry(my_frame2, width = 50)
miscInOrgRecycEntry = Entry(my_frame2, width = 50)
otherWasteRecycEntry = Entry(my_frame2, width = 50)
yardTrimmingsRecycEntry = Entry(my_frame2, width = 50)
foodRecycEntry = Entry(my_frame2, width = 50)
rltRecycEntry = Entry(my_frame2, width = 50)
woodRecycEntry = Entry(my_frame2, width = 50)
metalRecycEntry = Entry(my_frame2, width = 50)
glassRecycEntry = Entry(my_frame2, width = 50)
paperRecycEntry = Entry(my_frame2, width = 50)
plasticRecycEntry = Entry(my_frame2, width = 50)

#Creates lists of labels and entries for placement 
recycMSWPropsLabels= [totalRecycLabel, totalRecycMassLabel, miscInOrgRecycLabel, otherWasteRecycLabel, yardTrimmingsRecycLabel, foodRecycLabel,
                      rltRecycLabel, woodRecycLabel, metalRecycLabel, glassRecycLabel, paperRecycLabel, plasticRecycLabel]

recycMSWPropsEntry = [totalRecycMassEntry, miscInOrgRecycEntry, otherWasteRecycEntry, yardTrimmingsRecycEntry, foodRecycEntry, rltRecycEntry,
                      woodRecycEntry, metalRecycEntry, glassRecycEntry, paperRecycEntry, plasticRecycEntry]

recycMSWCheckList = [miscInOrgRecycEntry, otherWasteRecycEntry, yardTrimmingsRecycEntry, foodRecycEntry, rltRecycEntry,
                      woodRecycEntry, metalRecycEntry, glassRecycEntry, paperRecycEntry, plasticRecycEntry]


#Creates buttons for checking, autofilling, and entering
recycMSWButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(recycMSWCheckList, 1))
recycMSWAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(recycMSWPropsEntry, mswRecyc2018))
recycMSWEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(recycMSWPropsEntry, mswRecyc, recycMSWPropsValueLabels, IncinMSWPropsLabels, IncinMSWPropsEntry, incinMSWButtonChecker, incinMSWAutoButton, incinMSWEnterButton))



#Incineration data input labels and entry boxes
totalIncinLabel = Label(my_frame2, text = "Incineration Data", bg = 'white', font = 'Helvetica 12 bold')
totalIncinMassLabel = Label(my_frame2, text = "Total Mass Incinerated: ", bg = 'white', font = fontChoice)
miscInOrgIncinLabel = Label(my_frame2, text = "Misc. Inorganic Wastes (Fraction):", bg = 'white', font = fontChoice)
otherWasteIncinLabel = Label(my_frame2, text = "Other Wastes (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsIncinLabel = Label(my_frame2, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodIncinLabel = Label(my_frame2, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltIncinLabel = Label(my_frame2, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodIncinLabel = Label(my_frame2, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalIncinLabel = Label(my_frame2, text = "Metal (Fraction):", bg = 'white', font = fontChoice)
glassIncinLabel = Label(my_frame2, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperIncinLabel = Label(my_frame2, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticIncinLabel = Label(my_frame2, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)

totalIncinMassEntry = Entry(my_frame2, width = 50)
miscInOrgIncinEntry = Entry(my_frame2, width = 50)
otherWasteIncinEntry = Entry(my_frame2, width = 50)
yardTrimmingsIncinEntry = Entry(my_frame2, width = 50)
foodIncinEntry = Entry(my_frame2, width = 50)
rltIncinEntry = Entry(my_frame2, width = 50)
woodIncinEntry = Entry(my_frame2, width = 50)
metalIncinEntry = Entry(my_frame2, width = 50)
glassIncinEntry = Entry(my_frame2, width = 50)
paperIncinEntry = Entry(my_frame2, width = 50)
plasticIncinEntry = Entry(my_frame2, width = 50)


#Creates lists for widget placement
IncinMSWPropsLabels= [totalIncinLabel, totalIncinMassLabel, miscInOrgIncinLabel, otherWasteIncinLabel, yardTrimmingsIncinLabel, foodIncinLabel,
                      rltIncinLabel, woodIncinLabel, metalIncinLabel, glassIncinLabel, paperIncinLabel, plasticIncinLabel]

IncinMSWPropsEntry = [totalIncinMassEntry, miscInOrgIncinEntry, otherWasteIncinEntry, yardTrimmingsIncinEntry, foodIncinEntry, rltIncinEntry,
                      woodIncinEntry, metalIncinEntry, glassIncinEntry, paperIncinEntry, plasticIncinEntry]

IncinMSWCheckList = [miscInOrgIncinEntry, otherWasteIncinEntry, yardTrimmingsIncinEntry, foodIncinEntry, rltIncinEntry,
                      woodIncinEntry, metalIncinEntry, glassIncinEntry, paperIncinEntry, plasticIncinEntry]


#Creates buttons for checking, autofilling, and entering data
incinMSWButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(IncinMSWCheckList, 1))
incinMSWAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(IncinMSWPropsEntry, mswIncin2018))
incinMSWEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(IncinMSWPropsEntry, mswIncin, IncinMSWPropsValueLabels, LandMSWPropsLabels, LandMSWPropsEntry, landMSWButtonChecker, landMSWAutoButton, landMSWEnterButton))



#Compost data input labels and entry boxes
totalCompostLabel = Label(my_frame2, text = "Compost Data", bg = 'white', font = 'Helvetica 12 bold')
totalCompostMassLabel = Label(my_frame2, text = "Total Mass Compost: ", bg = 'white', font = fontChoice)
miscInOrgCompostLabel = Label(my_frame2, text = "Misc. Inorganic Wastes (Fraction):", bg = 'white', font = fontChoice)
otherWasteCompostLabel = Label(my_frame2, text = "Other Wastes (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsCompostLabel = Label(my_frame2, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodCompostLabel = Label(my_frame2, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltCompostLabel = Label(my_frame2, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodCompostLabel = Label(my_frame2, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalCompostLabel = Label(my_frame2, text = "Metal (Fraction):", bg = 'white', font = fontChoice)
glassCompostLabel = Label(my_frame2, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperCompostLabel = Label(my_frame2, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticCompostLabel = Label(my_frame2, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)

totalCompostMassEntry = Entry(my_frame2, width = 50)
miscInOrgCompostEntry = Entry(my_frame2, width = 50)
otherWasteCompostEntry = Entry(my_frame2, width = 50)
yardTrimmingsCompostEntry = Entry(my_frame2, width = 50)
foodCompostEntry = Entry(my_frame2, width = 50)
rltCompostEntry = Entry(my_frame2, width = 50)
woodCompostEntry = Entry(my_frame2, width = 50)
metalCompostEntry = Entry(my_frame2, width = 50)
glassCompostEntry = Entry(my_frame2, width = 50)
paperCompostEntry = Entry(my_frame2, width = 50)
plasticCompostEntry = Entry(my_frame2, width = 50)

#creates lists for widget placement
CompostMSWPropsLabels= [totalCompostLabel, totalCompostMassLabel, miscInOrgCompostLabel, otherWasteCompostLabel, yardTrimmingsCompostLabel, foodCompostLabel,
                      rltCompostLabel, woodCompostLabel, metalCompostLabel, glassCompostLabel, paperCompostLabel, plasticCompostLabel]

CompostMSWPropsEntry = [totalCompostMassEntry, miscInOrgCompostEntry, otherWasteCompostEntry, yardTrimmingsCompostEntry, foodCompostEntry, rltCompostEntry,
                      woodCompostEntry, metalCompostEntry, glassCompostEntry, paperCompostEntry, plasticCompostEntry]

compostMSWCheckList = [miscInOrgCompostEntry, otherWasteCompostEntry, yardTrimmingsCompostEntry, foodCompostEntry, rltCompostEntry,
                      woodCompostEntry, metalCompostEntry, glassCompostEntry, paperCompostEntry, plasticCompostEntry]

#Creates buttons for checking proportions, autofilling, and entering data
compostMSWCheckerButton = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(compostMSWCheckList, 1))
compostMSWAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(CompostMSWPropsEntry, mswCompost2018))
compostMSWEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(CompostMSWPropsEntry, mswCompost, CompostMSWPropsValueLabels, recycPlasticLabels, recycPlasticEntry, plasticRecycButtonChecker, plasticRecycAutoButton, plasticRecycEnterButton))


#Landfill Data input labels and entries
totalLandLabel = Label(my_frame2, text = "Landfill Data", bg = 'white', font = 'Helvetica 12 bold')
totalLandMassLabel = Label(my_frame2, text = "Total Mass Landfilled: ", bg = 'white', font = fontChoice)
miscInOrgLandLabel = Label(my_frame2, text = "Misc. Inorganic Wastes (Fraction):", bg = 'white', font = fontChoice)
otherWasteLandLabel = Label(my_frame2, text = "Other Wastes (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsLandLabel = Label(my_frame2, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodLandLabel = Label(my_frame2, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltLandLabel = Label(my_frame2, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodLandLabel = Label(my_frame2, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalLandLabel = Label(my_frame2, text = "Metal (Fraction):", bg = 'white', font = fontChoice)
glassLandLabel = Label(my_frame2, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperLandLabel = Label(my_frame2, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticLandLabel = Label(my_frame2, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)

totalLandMassEntry = Entry(my_frame2, width = 50)
miscInOrgLandEntry = Entry(my_frame2, width = 50)
otherWasteLandEntry = Entry(my_frame2, width = 50)
yardTrimmingsLandEntry = Entry(my_frame2, width = 50)
foodLandEntry = Entry(my_frame2, width = 50)
rltLandEntry = Entry(my_frame2, width = 50)
woodLandEntry = Entry(my_frame2, width = 50)
metalLandEntry = Entry(my_frame2, width = 50)
glassLandEntry = Entry(my_frame2, width = 50)
paperLandEntry = Entry(my_frame2, width = 50)
plasticLandEntry = Entry(my_frame2, width = 50)


#Creates lists for widget placement
LandMSWPropsLabels= [totalLandLabel, totalLandMassLabel, miscInOrgLandLabel, otherWasteLandLabel, yardTrimmingsLandLabel, foodLandLabel,
                      rltLandLabel, woodLandLabel, metalLandLabel, glassLandLabel, paperLandLabel, plasticLandLabel]

LandMSWPropsEntry = [totalLandMassEntry, miscInOrgLandEntry, otherWasteLandEntry, yardTrimmingsLandEntry, foodLandEntry, rltLandEntry,
                      woodLandEntry, metalLandEntry, glassLandEntry, paperLandEntry, plasticLandEntry]

LandMSWChecker = [miscInOrgLandEntry, otherWasteLandEntry, yardTrimmingsLandEntry, foodLandEntry, rltLandEntry,
                      woodLandEntry, metalLandEntry, glassLandEntry, paperLandEntry, plasticLandEntry]


#Creates buttons for checking, autofilling, and entering data
landMSWButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(LandMSWChecker, 1))
landMSWAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(LandMSWPropsEntry, mswLand2018))
landMSWEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(LandMSWPropsEntry, mswLand, LandMSWPropsValueLabels, CompostMSWPropsLabels, CompostMSWPropsEntry, compostMSWCheckerButton, compostMSWAutoButton, compostMSWEnterButton))



#Types of plastics entry boxes and labels for recycled list
plasticRecycProportionsLabel = Label(my_frame2, text = "Plastic Recycled Proportions", bg = 'white', font = 'Helvetica 12 bold')

petRecycLabel = Label(my_frame2, text = "PET Proportion (Fraction):", bg = 'white', font = fontChoice)
hdpeRecycLabel = Label(my_frame2, text = "HDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
pvcRecycLabel = Label(my_frame2, text = "PVC Proportion (Fraction):", bg = 'white', font = fontChoice)
ldpeRecycLabel = Label(my_frame2, text = "LDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
ppRecycLabel = Label(my_frame2, text = "PP Proportion (Fraction):", bg = 'white', font = fontChoice)
psRecycLabel = Label(my_frame2, text = "PS Proportion (Fraction):", bg = 'white', font = fontChoice)
otherRecycPlasticsLabel = Label(my_frame2, text = "Other Plastics Proportion (Fraction):", bg = 'white', font = fontChoice)
plaRecycLabel = Label(my_frame2, text = "PLA Proportion (Fraction):", bg = 'white', font = fontChoice)


petRecycEntry = Entry(my_frame2, width=50)
hdpeRecycEntry = Entry(my_frame2, width=50)
pvcRecycEntry = Entry(my_frame2, width=50)
ldpeRecycEntry = Entry(my_frame2, width=50)
ppRecycEntry = Entry(my_frame2, width=50)
psRecycEntry = Entry(my_frame2, width=50)
otherRecycPlasticsEntry = Entry(my_frame2, width=50)
plaRecycEntry = Entry(my_frame2, width=50)


#Creates lists for widget placement 
recycPlasticLabels = [plasticRecycProportionsLabel, petRecycLabel, hdpeRecycLabel, pvcRecycLabel, ldpeRecycLabel, plaRecycLabel, ppRecycLabel, psRecycLabel, otherRecycPlasticsLabel]
recycPlasticEntry = [petRecycEntry, hdpeRecycEntry, pvcRecycEntry, ldpeRecycEntry, plaRecycEntry, ppRecycEntry, psRecycEntry, otherRecycPlasticsEntry]

#Creates buttons for checking, autofilling, and entering data
plasticRecycButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(recycPlasticEntry, 1))
plasticRecycAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(recycPlasticEntry, plasticRecycledFractionsList2018))
plasticRecycEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(recycPlasticEntry, plasticRecycledFractionsList, plasticRecycValueLabels, IncinPlasticLabels, IncinPlasticEntry, plasticIncinButtonChecker, plasticIncinAutoButton, plasticIncinEnterButton))






#Types of plastics entry boxes and labels for landfilled list
plasticLandProportionsLabel = Label(my_frame2, text = "Plastic Landfilled Proportions", bg = 'white', font = 'Helvetica 12 bold')

petLandLabel = Label(my_frame2, text = "PET Proportion (Fraction):", bg = 'white', font = fontChoice)
hdpeLandLabel = Label(my_frame2, text = "HDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
pvcLandLabel = Label(my_frame2, text = "PVC Proportion (Fraction):", bg = 'white', font = fontChoice)
ldpeLandLabel = Label(my_frame2, text = "LDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
ppLandLabel = Label(my_frame2, text = "PP Proportion (Fraction):", bg = 'white', font = fontChoice)
psLandLabel = Label(my_frame2, text = "PS Proportion (Fraction):", bg = 'white', font = fontChoice)
otherLandPlasticsLabel = Label(my_frame2, text = "Other Plastics Proportion (Fraction):", bg = 'white', font = fontChoice)
plaLandLabel = Label(my_frame2, text = "PLA Proportion (Fraction):", bg = 'white', font = fontChoice)


petLandEntry = Entry(my_frame2, width=50)
hdpeLandEntry = Entry(my_frame2, width=50)
pvcLandEntry = Entry(my_frame2, width=50)
ldpeLandEntry = Entry(my_frame2, width=50)
ppLandEntry = Entry(my_frame2, width=50)
psLandEntry = Entry(my_frame2, width=50)
otherLandPlasticsEntry = Entry(my_frame2, width=50)
plaLandEntry = Entry(my_frame2, width=50)


#Creates lists for widget placement
LandPlasticLabels = [plasticLandProportionsLabel, petLandLabel, hdpeLandLabel, pvcLandLabel, ldpeLandLabel, plaLandLabel, ppLandLabel, psLandLabel, otherLandPlasticsLabel]
LandPlasticEntry = [petLandEntry, hdpeLandEntry, pvcLandEntry, ldpeLandEntry, plaLandEntry, ppLandEntry, psLandEntry, otherLandPlasticsEntry]


#Creates buttons for checking, autofilling, and entering data
plasticLandButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(LandPlasticEntry, 1))
plasticLandAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(LandPlasticEntry, plasticLandFractionsList))
plasticLandEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(LandPlasticEntry, plasticLandFractionsList, LandPlasticValueLabels, RepRecycPlasticLabels, RepRecycPlasticEntry, NONE, plasticRepRecycAutoButton, plasticRepRecycEnterButton))




#Types of plastics entry boxes and labels for Incinerated list
plasticIncinProportionsLabel = Label(my_frame2, text = "Plastic Incinerated Proportions", bg = 'white', font = 'Helvetica 12 bold')

petIncinLabel = Label(my_frame2, text = "PET Proportion (Fraction):", bg = 'white', font = fontChoice)
hdpeIncinLabel = Label(my_frame2, text = "HDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
pvcIncinLabel = Label(my_frame2, text = "PVC Proportion (Fraction):", bg = 'white', font = fontChoice)
ldpeIncinLabel = Label(my_frame2, text = "LDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
ppIncinLabel = Label(my_frame2, text = "PP Proportion (Fraction):", bg = 'white', font = fontChoice)
psIncinLabel = Label(my_frame2, text = "PS Proportion (Fraction):", bg = 'white', font = fontChoice)
otherIncinPlasticsLabel = Label(my_frame2, text = "Other Plastics Proportion (Fraction):", bg = 'white', font = fontChoice)
plaIncinLabel = Label(my_frame2, text = "PLA Proportion (Fraction):", bg = 'white', font = fontChoice)


petIncinEntry = Entry(my_frame2, width=50)
hdpeIncinEntry = Entry(my_frame2, width=50)
pvcIncinEntry = Entry(my_frame2, width=50)
ldpeIncinEntry = Entry(my_frame2, width=50)
ppIncinEntry = Entry(my_frame2, width=50)
psIncinEntry = Entry(my_frame2, width=50)
otherIncinPlasticsEntry = Entry(my_frame2, width=50)
plaIncinEntry = Entry(my_frame2, width=50)


#Creates lists for placement of widgets
IncinPlasticLabels = [plasticIncinProportionsLabel, petIncinLabel, hdpeIncinLabel, pvcIncinLabel, ldpeIncinLabel, plaIncinLabel, ppIncinLabel, psIncinLabel, otherIncinPlasticsLabel]
IncinPlasticEntry = [petIncinEntry, hdpeIncinEntry, pvcIncinEntry, ldpeIncinEntry, plaIncinEntry, ppIncinEntry, psIncinEntry, otherIncinPlasticsEntry]

#Creates buttons for checking, autofilling, and entering data
plasticIncinButtonChecker = Button(my_frame2, text = ' Check Proportions ', command = lambda:checkProportions(IncinPlasticEntry, 1))
plasticIncinAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(IncinPlasticEntry, plasticIncinFractionsList2018))
plasticIncinEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(IncinPlasticEntry, plasticIncinFractionsList, IncinPlasticValueLabels, LandPlasticLabels, LandPlasticEntry, plasticLandButtonChecker, plasticLandAutoButton, plasticLandEnterButton))


#Types of plastics entry boxes and labels for reported recycled list
plasticRepRecycProportionsLabel = Label(my_frame2, text = "Plastic Reported Recycled Masses", bg = 'white', font = 'Helvetica 12 bold')

petRepRecycLabel = Label(my_frame2, text = "PET Proportion (Tons):", bg = 'white', font = fontChoice)
hdpeRepRecycLabel = Label(my_frame2, text = "HDPE Proportion (Tons):", bg = 'white', font = fontChoice)
pvcRepRecycLabel = Label(my_frame2, text = "PVC Proportion (Tons):", bg = 'white', font = fontChoice)
ldpeRepRecycLabel = Label(my_frame2, text = "LDPE Proportion (Tons):", bg = 'white', font = fontChoice)
ppRepRecycLabel = Label(my_frame2, text = "PP Proportion (Tons):", bg = 'white', font = fontChoice)
psRepRecycLabel = Label(my_frame2, text = "PS Proportion (Tons):", bg = 'white', font = fontChoice)
otherRepRecycPlasticsLabel = Label(my_frame2, text = "Other Plastics Proportion (Tons):", bg = 'white', font = fontChoice)
plaRepRecycLabel = Label(my_frame2, text = "PLA Proportion (Tons):", bg = 'white', font = fontChoice)


petRepRecycEntry = Entry(my_frame2, width=50)
hdpeRepRecycEntry = Entry(my_frame2, width=50)
pvcRepRecycEntry = Entry(my_frame2, width=50)
ldpeRepRecycEntry = Entry(my_frame2, width=50)
ppRepRecycEntry = Entry(my_frame2, width=50)
psRepRecycEntry = Entry(my_frame2, width=50)
otherRepRecycPlasticsEntry = Entry(my_frame2, width=50)
plaRepRecycEntry = Entry(my_frame2, width=50)

#Creates lists for widget placement
RepRecycPlasticLabels = [plasticRepRecycProportionsLabel, petRepRecycLabel, hdpeRepRecycLabel, pvcRepRecycLabel, ldpeRepRecycLabel, plaRepRecycLabel, ppRepRecycLabel, psRepRecycLabel, otherRepRecycPlasticsLabel]
RepRecycPlasticEntry = [petRepRecycEntry, hdpeRepRecycEntry, pvcRepRecycEntry, ldpeRepRecycEntry, plaRepRecycEntry, ppRepRecycEntry, psRepRecycEntry, otherRepRecycPlasticsEntry]


#Creates buttons for autofilling and entering the data
plasticRepRecycAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(RepRecycPlasticEntry, repRecPlastics2018))
plasticRepRecycEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(RepRecycPlasticEntry, repRecPlastics, RepRecycPlasticValueLabel, ImportPlasticLabels, ImportPlasticEntry, NONE, plasticImportAutoButton, plasticImportEnterButton))



#Types of plastics entry boxes and labels for import list
plasticImportProportionsLabel = Label(my_frame2, text = "Plastic Imported Mass", bg = 'white', font = 'Helvetica 12 bold')

ethyleneImportLabel = Label(my_frame2, text = "Ethylene Mass (Tons):", bg = 'white', font = fontChoice)
vinylChlorideImportLabel = Label(my_frame2, text = "Vinyl Chloride Mass (Tons):", bg = 'white', font = fontChoice)
styreneImportLabel = Label(my_frame2, text = "Styrene Mass (Tons):", bg = 'white', font = fontChoice)
otherImportLabel = Label(my_frame2, text = "Other Plastics (Tons):", bg = 'white', font = fontChoice)


ethyleneImportEntry = Entry(my_frame2, width=50)
vinylChlorideImportEntry = Entry(my_frame2, width=50)
styreneImportEntry = Entry(my_frame2, width=50)
otherImportEntry = Entry(my_frame2, width=50)


#Creates lists for widget placement
ImportPlasticLabels = [plasticImportProportionsLabel, ethyleneImportLabel, vinylChlorideImportLabel, styreneImportLabel, otherImportLabel]
ImportPlasticEntry = [ethyleneImportEntry, vinylChlorideImportEntry, styreneImportEntry, otherImportEntry]

#Creates button for autofilling and entering the data
plasticImportAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(ImportPlasticEntry, repPlasticImport2018))
plasticImportEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(ImportPlasticEntry, repPlasticImport, ImportPlasticValueLabels, ExportPlasticLabels, ExportPlasticEntry, NONE, plasticExportAutoButton, plasticExportEnterButton))


#Types of plastics entry boxes and labels for Export list
plasticExportProportionsLabel = Label(my_frame2, text = "Plastic Exported Mass", bg = 'white', font = 'Helvetica 12 bold')

ethyleneExportLabel = Label(my_frame2, text = "Ethylene Mass (Tons):", bg = 'white', font = fontChoice)
vinylChlorideExportLabel = Label(my_frame2, text = "Vinyl Chloride Mass (Tons):", bg = 'white', font = fontChoice)
styreneExportLabel = Label(my_frame2, text = "Styrene Mass (Tons):", bg = 'white', font = fontChoice)
otherExportLabel = Label(my_frame2, text = "Other Plastics (Tons):", bg = 'white', font = fontChoice)


ethyleneExportEntry = Entry(my_frame2, width=50)
vinylChlorideExportEntry = Entry(my_frame2, width=50)
styreneExportEntry = Entry(my_frame2, width=50)
otherExportEntry = Entry(my_frame2, width=50)

#Creates lists for widget placement
ExportPlasticLabels = [plasticExportProportionsLabel, ethyleneExportLabel, vinylChlorideExportLabel, styreneExportLabel, otherExportLabel]
ExportPlasticEntry = [ethyleneExportEntry, vinylChlorideExportEntry, styreneExportEntry, otherExportEntry]

#Creates buttons for autofilling and entering data
plasticExportAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(ExportPlasticEntry, repPlasticsExport2018))
plasticExportEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(ExportPlasticEntry, repPlasticsExport, ExportPlasticValueLabels, ReExportPlasticLabels, ReExportPlasticEntry, NONE, plasticReExportAutoButton, plasticReExportEnterButton))


#Types of plastics entry boxes and labels for ReExport list
plasticReExportProportionsLabel = Label(my_frame2, text = "Plastic ReExported Mass", bg = 'white', font = 'Helvetica 12 bold')

ethyleneReExportLabel = Label(my_frame2, text = "Ethylene Mass (Tons):", bg = 'white', font = fontChoice)
vinylChlorideReExportLabel = Label(my_frame2, text = "Vinyl Chloride Mass (Tons):", bg = 'white', font = fontChoice)
styreneReExportLabel = Label(my_frame2, text = "Styrene Mass (Tons):", bg = 'white', font = fontChoice)
otherReExportLabel = Label(my_frame2, text = "Other Plastics (Tons):", bg = 'white', font = fontChoice)


ethyleneReExportEntry = Entry(my_frame2, width=50)
vinylChlorideReExportEntry = Entry(my_frame2, width=50)
styreneReExportEntry = Entry(my_frame2, width=50)
otherReExportEntry = Entry(my_frame2, width=50)

#Creates lists for widget placement
ReExportPlasticLabels = [plasticReExportProportionsLabel, ethyleneReExportLabel, vinylChlorideReExportLabel, styreneReExportLabel, otherReExportLabel]
ReExportPlasticEntry = [ethyleneReExportEntry, vinylChlorideReExportEntry, styreneReExportEntry, otherReExportEntry]

#Creates buttons for autofilling and entering data
plasticReExportAutoButton = Button(my_frame2, text = ' Autofill 2018 Data', command = lambda: autofill(ReExportPlasticEntry, repPlasticsReExport2018))
plasticReExportEnterButton = Button(my_frame2, text = 'Enter Above Dataset', command = lambda: enter(ReExportPlasticEntry, repPlasticsReExport, ReExportPlasticValueLabels, conditionsLabelsListForPlacement, conditionsEntryListForPlacement, conditionsButtonChecker, conditionsAutoButton, conditionsEnterButton))


#Creates lists of labels and entries to allow for a loop to place them on screen
customLabelsList = [conditionsLabelsListForPlacement, typesOfWasteLabels, recycMSWPropsLabels, IncinMSWPropsLabels, LandMSWPropsLabels, 
                    CompostMSWPropsLabels, recycPlasticLabels, IncinPlasticLabels, LandPlasticLabels, RepRecycPlasticLabels, ImportPlasticLabels, 
                    ExportPlasticLabels, ReExportPlasticLabels]


customEntryList = [conditionsEntryListForPlacement, typesOfWasteEntry, recycMSWPropsEntry, IncinMSWPropsEntry, LandMSWPropsEntry, CompostMSWPropsEntry,
                   recycPlasticEntry,IncinPlasticEntry, LandPlasticEntry, RepRecycPlasticEntry, ImportPlasticEntry, ExportPlasticEntry,
                   ReExportPlasticEntry]

#Gap labels to appropriately space widgets on screen
gapLabel1 = Label(my_frame2, bg = 'white')
gapLabel2 = Label(my_frame2, bg = 'white')
gapLabel3 = Label(my_frame2, bg = 'white', text = 'Status:', font = fontChoice)
gapLabel4 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel5 = Label(my_frame7, bg = 'white', text = '________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________')
gapLabel6 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel7 = Label(my_frame7, bg = 'white', text = '________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________')
gapLabel8 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel9 = Label(my_frame7, bg = 'white', text = '________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________')
gapLabel10 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel11 = Label(my_frame7, bg = 'white', text = '________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________')
gapLabel12 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel13 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel14 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel15 = Label(my_frame7, bg = 'white', text = '                     ')
gapLabel16 = Label(my_frame2, bg = 'white', text = '                     ')
gapLabel17 = Label(my_frame7, bg = 'white', text = '                     ')


innerGap1 = Label(my_frame2, bg = 'white')
innerGap2 = Label(my_frame2, bg = 'white')
innerGap3 = Label(my_frame2, bg = 'white')
innerGap4 = Label(my_frame2, bg = 'white')
innerGap5 = Label(my_frame2, bg = 'white')
innerGap6 = Label(my_frame2, bg = 'white')
innerGap7 = Label(my_frame2, bg = 'white')
innerGap8 = Label(my_frame2, bg = 'white')
innerGap9 = Label(my_frame2, bg = 'white')
innerGap10 = Label(my_frame2, bg = 'white')
innerGap11 = Label(my_frame2, bg = 'white')
innerGap12 = Label(my_frame2, bg = 'white')
innerGap13 = Label(my_frame2, bg = 'white')
innerGap14 = Label(my_frame2, bg = 'white')

#Creates more lists of widgets for easier placement on screen
gapLabelsList = [gapLabel4, gapLabel5, gapLabel6, gapLabel7, gapLabel8, gapLabel9, gapLabel10, gapLabel11,
                 gapLabel12, gapLabel13, gapLabel14, gapLabel15]

innerGapLabelsList = [innerGap1, innerGap2, innerGap3, innerGap4, innerGap5, innerGap6, innerGap7, innerGap8, innerGap9, innerGap10, 
                      innerGap11, innerGap12, innerGap13, innerGap14]

checkButtonList = [conditionsButtonChecker, mswCompButtonCheck, recycMSWButtonChecker, incinMSWButtonChecker,  landMSWButtonChecker, 
                   compostMSWCheckerButton, plasticRecycButtonChecker, plasticIncinButtonChecker, plasticLandButtonChecker]

extraButTonsList = [conditionsAutoButton, conditionsEnterButton, mswCompAuto, mswCompEnter, recycMSWAutoButton, recycMSWEnterButton,
                    incinMSWAutoButton, incinMSWEnterButton, landMSWAutoButton, landMSWEnterButton, compostMSWAutoButton, compostMSWEnterButton,
                    plasticRecycAutoButton, plasticRecycEnterButton, plasticIncinAutoButton, plasticIncinEnterButton, plasticLandAutoButton,
                    plasticLandEnterButton, plasticRepRecycAutoButton, plasticRepRecycEnterButton, plasticImportAutoButton, plasticImportEnterButton,
                    plasticExportAutoButton, plasticExportEnterButton, plasticReExportAutoButton, plasticReExportEnterButton]

# title label and placement
userSpecificationsLabel = Label(my_frame2, text = "User Specifications", bg = 'white', font = 'Helvetica 14 bold')
userSpecificationsLabel.grid(column = 1, row = 10, columnspan = 2)

#Function connected to calculate button to extract values from entry boxes, append to list
    # and complete appropriate calculations MJC
def calculateWasteProportions():
   makeCalculations()
   fillMatFlowAnalSumTRVW()

#Create Button that will assign values and make calculations based on input 
calculateButton = Button(my_frame2, text=" Calculate Streams ", command=calculateWasteProportions)

#Grids conditions widgets at boot up
conditionsLabelsList[0].grid(column = 1, row = 11, columnspan = 2)
gapLabel1.grid(column = 2, row = 12, sticky = W)
gapLabel3.grid(column = 1, row = 12, sticky = E)
frameRow = 13
for i in range(len(conditionsLabelsListForPlacement)-1):
    conditionsLabelsListForPlacement[i+1].grid(column = 1, row = frameRow, sticky = E)
    conditionsEntryListForPlacement[i].grid(column = 2, row = frameRow, sticky = W)
    frameRow+=1
gapLabel2.grid(column = 1, row = frameRow, columnspan = 2)
frameRow +=1
conditionsButtonChecker.grid(column = 1, row = frameRow, columnspan = 2)
frameRow +=1
conditionsAutoButton.grid(column = 1, row = frameRow, columnspan = 2)
frameRow +=1
conditionsEnterButton.grid(column = 1, row = frameRow, columnspan = 2)
frameRow +=1
calculateButton.grid(column=1, row=frameRow, columnspan = 2)


#Function that will remove category widgets from screen 
def removeLabels():
    for i in customLabelsList:
        for b in i:
            b.grid_remove()
    for c in customEntryList:
        for q in c:
            q.grid_remove()
    for v in checkButtonList:
        v.grid_remove()
    gapLabel2.grid_remove()
    calculateButton.grid_remove()
    for i in extraButTonsList:
        i.grid_remove()
            
#function that will add next set of widgets to stream
def showSection(label, entry, checkButton, autofill, enter):
    removeLabels()
    gapLabel1.config(text = '')
    frameRow = 13
    label[0].grid(column = 1, row = 11, columnspan = 2)
    for i in range(len(label)-1):
        label[i+1].grid(column = 1, row = frameRow, sticky = E)
        frameRow += 1
    frameRow = 13
    for i in entry:
        i.grid(column = 2, row = frameRow, sticky = W)
        frameRow += 1
    gapLabel2.grid(column = 1, row = frameRow, columnspan = 2)
    frameRow+=1
    if checkButton != NONE:
        checkButton.grid(column = 1, row = frameRow, columnspan = 2)
        frameRow+=1
   
    autofill.grid(column = 1, row = frameRow, columnspan = 2)
    frameRow+=1
    enter.grid(column = 1, row = frameRow, columnspan = 2)
    frameRow+=1
    calculateButton.grid(column = 1, row = frameRow, columnspan = 2)
    

#Menu at left of buttons that will change list of available entries
showConditionsButton = Button(my_frame2, text = 'Conditions', command = lambda:showSection(conditionsLabelsListForPlacement, conditionsEntryListForPlacement, conditionsButtonChecker, conditionsAutoButton, conditionsEnterButton))
showMSWCompButton = Button(my_frame2, text = 'MSW Composition', command = lambda: showSection(typesOfWasteLabels, typesOfWasteEntry, mswCompButtonCheck, mswCompAuto, mswCompEnter))
showrecycMSWButton = Button(my_frame2, text = 'MSW Recycling', command = lambda:showSection(recycMSWPropsLabels, recycMSWPropsEntry, recycMSWButtonChecker, recycMSWAutoButton, recycMSWEnterButton))
showincinMSWButton = Button(my_frame2, text = 'MSW Incineration', command = lambda: showSection(IncinMSWPropsLabels, IncinMSWPropsEntry, incinMSWButtonChecker, incinMSWAutoButton, incinMSWEnterButton))
showlandMSWButton = Button(my_frame2, text = 'MSW Landfill', command = lambda:showSection(LandMSWPropsLabels, LandMSWPropsEntry, landMSWButtonChecker, landMSWAutoButton, landMSWEnterButton))
showcompostMSWButton = Button(my_frame2, text = "MSW Compost", command = lambda: showSection(CompostMSWPropsLabels, CompostMSWPropsEntry, compostMSWCheckerButton, compostMSWAutoButton, compostMSWEnterButton))
showPlasticRecycButton = Button(my_frame2, text = 'Plastic Recycling', command = lambda: showSection(recycPlasticLabels, recycPlasticEntry, plasticRecycButtonChecker, plasticRecycAutoButton, plasticRecycEnterButton))
showIncinPlasticButton = Button(my_frame2, text = 'Incinerated Plastic', command = lambda: showSection(IncinPlasticLabels, IncinPlasticEntry, plasticIncinButtonChecker, plasticIncinAutoButton, plasticIncinEnterButton))
showLandPlasticButton = Button(my_frame2, text = 'Landfilled Plastic', command = lambda: showSection(LandPlasticLabels, LandPlasticEntry, plasticLandButtonChecker, plasticLandAutoButton, plasticLandEnterButton))
showRepRecycButton = Button(my_frame2, text = 'Reported Recycled Masses', command = lambda: showSection(RepRecycPlasticLabels, RepRecycPlasticEntry, NONE, plasticRepRecycAutoButton, plasticRepRecycEnterButton))
showImportButton = Button(my_frame2, text = 'Imported Plastic', command = lambda: showSection(ImportPlasticLabels, ImportPlasticEntry, NONE, plasticImportAutoButton, plasticImportEnterButton))
showExportButton = Button(my_frame2, text = 'Exported Plastics', command = lambda: showSection(ExportPlasticLabels, ExportPlasticEntry, NONE, plasticExportAutoButton, plasticExportEnterButton))
showReExportButton = Button(my_frame2, text = 'Re-Exported Plastics', command = lambda: showSection(ReExportPlasticLabels, ReExportPlasticEntry, NONE, plasticReExportAutoButton, plasticReExportEnterButton))

#Creates list of these buttons above
showButtonLists = [showConditionsButton, showMSWCompButton, showrecycMSWButton, showincinMSWButton, showlandMSWButton, showcompostMSWButton, 
                   showPlasticRecycButton, showIncinPlasticButton, showLandPlasticButton, showRepRecycButton, showImportButton, showExportButton,
                   showReExportButton]
frameRow =11

#loop that places these buttons
for i in showButtonLists:
    i.grid(column = 0, row = frameRow, sticky = EW)
    frameRow +=1

#List of strings that will be used as confirmation after each set of data is entered
listOfEntryCategories = {str(conditionsentryList):"Conditions Data Entered", str(typesOfWasteEntry): "Municipal Solid Waste Composition Data Entered", str(recycMSWPropsEntry): "MSW Recycling Data Entered", 
                         str(LandMSWPropsEntry): "MSW Landfill Data Entered", str(IncinMSWPropsEntry): "MSW Incineration Data Entered", str(CompostMSWPropsEntry): "MSW Compost Data Entered", 
                         str(recycPlasticEntry): "Plastic Recycled Data Entered", str(IncinPlasticEntry): "Plastic Incinerated Data Entered", str(LandPlasticEntry): "Plastic Landfill Data Entered",
                         str(RepRecycPlasticEntry): "Reported Recycling Data Entered", str(ImportPlasticEntry): "Import Data Entered", str(ExportPlasticEntry): "Export Data Entered", 
                         str(ReExportPlasticEntry): "Re-Export Data Entered"}
        

####################################################
### Stream Summary Tab

#creates and adds canvas that will hold frame for plots (canvas created to allow for scrollbar)
plotCanvas = Canvas(dataAnalysisFrame, bg = 'white')
plotFrame = Frame(plotCanvas, bg = 'white')
plotScrollBar = Scrollbar(dataAnalysisFrame, orient = 'vertical', command = plotCanvas.yview)
plotScrollBar.pack(side = RIGHT, fill = Y)
plotCanvas.pack(fill = BOTH, expand = 1)

#creates and configures scrollbar for plot frame
plotScrollBar.config(command = plotCanvas.yview)
plotCanvas['yscrollcommand'] = plotScrollBar.set
plotCanvas.bind('<Configure>', lambda e: plotCanvas.configure(scrollregion = plotCanvas.bbox('all')))
plotCanvas.create_window((0,0), window = plotFrame, anchor = 'nw')


#Function that will be used to display frame that contains labels of user input
def displayInput():
    dataAnalysisCanvas.pack(fill = BOTH, expand = 1)
    my_frame7.pack(side = LEFT, fill = BOTH, expand = 1)
    dataAnalysisScrollBar.config(command=dataAnalysisCanvas.yview)

    dataAnalysisCanvas['yscrollcommand']=dataAnalysisScrollBar.set
    
    dataAnalysisCanvas.bind('<Configure>', lambda e: dataAnalysisCanvas.configure(scrollregion = dataAnalysisCanvas.bbox('all')))

    dataAnalysisCanvas.create_window((0,0), window = my_frame7, anchor = 'nw')
    my_program.bind_all('<MouseWheel>', lambda event: dataAnalysisCanvas.yview_scroll(int(-1*(event.delta/120)), "units"))

#Function that will be used to hide frame that contains labels of user input
def hideInput():
    dataAnalysisCanvas.pack_forget()
    my_frame7.pack_forget()

#Creates and places buttons for above two functions
displayInputButton = Button(dataAnalysisFrame, text = 'Display User Input', command = displayInput)
hideInputButton = Button(dataAnalysisFrame, text = 'Hide User Input', command = hideInput)

displayInputButton.pack()
hideInputButton.pack()



#Creates and configures titles for data analysis frames
dataAnalTitle = tk.Text(my_frame7, bd=0, highlightthickness = 0, bg = "white", height=1, width=125)
dataAnalTitle.insert(tk.INSERT,"User Specifications")
dataAnalTitle.tag_configure("center", justify = 'center')
dataAnalTitle.tag_add("center", 1.0, 'end')
dataAnalTitle.configure(font = ("Helvetica 16 bold"))
dataAnalTitle.config(state="disabled")
dataAnalTitle.grid(column=0,row=0,columnspan=6)
gapLabel17.grid(column = 0, row = 1, columnspan = 6)

#Creates category titles for each section of data
mswStreamLabel = Label(my_frame7, text = "MSW Composition", font = 'Helvetica 14 bold', bg = 'white')
miscInOrgWasteStreamLabel = Label(my_frame7, text = "Misc. Inorganic Waste (Fraction): ", font = fontChoice, bg="white")
otherWasteStreamLabel = Label(my_frame7, text = "Other (Fraction): ", font = fontChoice, bg="white")
yardTrimmingsStreamLabel = Label(my_frame7, text = "Yard Trimmings (Fraction): ", font = fontChoice, bg="white")
foodWasteStreamLabel = Label(my_frame7, text = "Food (Fraction): ", font = fontChoice, bg="white")
rltWasteStreamLabel = Label(my_frame7, text = "Rubber, Leather, Textiles (Fraction): ", font = fontChoice, bg="white")
woodWasteStreamLabel = Label(my_frame7, text = "Wood (Fraction): ", font = fontChoice, bg="white")
metalsWasteStreamLabel = Label(my_frame7, text = "Metals (Fraction): ", font = fontChoice, bg="white")
glassWasteStreamLabel = Label(my_frame7, text = "Glass (Fraction): ", font = fontChoice, bg="white")
paperAndBoardStreamLabel = Label(my_frame7, text = "Paper and Paperboard (Fraction): ", font = fontChoice, bg="white")
plasticsStreamLabel = Label(my_frame7, text = "Plastics (Fraction): ", font = fontChoice, bg="white")

#Creating list of input data labels (not values) MJC
typesOfWasteStreamStreamLabels = [mswStreamLabel, miscInOrgWasteStreamLabel, otherWasteStreamLabel, yardTrimmingsStreamLabel, foodWasteStreamLabel, rltWasteStreamLabel, woodWasteStreamLabel, metalsWasteStreamLabel, glassWasteStreamLabel, paperAndBoardStreamLabel, plasticsStreamLabel]



#Creates conditions StreamLabels and entries
conditionsTitleStreamLabel = Label(my_frame7, text = "Conditions", bg = 'white', font = 'Helvetica 12 bold')
totalMSWStreamLabel = Label(my_frame7, text = 'Total MSW (Tons):', bg = 'white', font = fontChoice)
totalPlasticStreamLabel = Label(my_frame7, text = 'Total Plastic Waste (Tons):', bg = 'white', font = fontChoice)
plasticRecycledPropStreamLabel = Label(my_frame7, text = 'Total Plastic Recycled (Fraction, Domestic and Export):', bg = 'white', font = fontChoice)
plasticDomesticStreamLabel = Label(my_frame7, text = 'Plastic Recycled Domestically (Fraction):', bg = 'white', font = fontChoice)
plasticRecycEfficiencyStreamLabel = Label(my_frame7, text = 'Plastic Recycling Efficiency (Fraction):', bg = 'white', font = fontChoice)
plasticExportPropStreamLabel = Label(my_frame7, text = 'Plastic Export Fraction (Fraction):', bg = 'white', font = fontChoice)
plasticReExportPropStreamLabel = Label(my_frame7, text = "Plastic Re-Export (Fraction):", bg = 'white', font = fontChoice)
plasticIncineratedPropStreamLabel = Label(my_frame7, text = 'Plastic Incinerated (Fraction):', bg = 'white', font = fontChoice)
plasticLandfillPropStreamLabel = Label(my_frame7, text = "Plastic Landfilled (Fraction):", bg = 'white', font = fontChoice)
wasteFacilityEmissionsStreamLabel = Label(my_frame7, text = 'Waste Facility Emissions (Tons):', bg = 'white', font = fontChoice)
landfillEmissionsStreamLabel = Label(my_frame7, text = 'Emissions from Landfill (Tons):', bg = 'white', font = fontChoice)



conditionsStreamStreamLabelsList = [conditionsTitleStreamLabel, totalMSWStreamLabel, totalPlasticStreamLabel, plasticRecycledPropStreamLabel, plasticDomesticStreamLabel, plasticRecycEfficiencyStreamLabel, plasticExportPropStreamLabel,
                        plasticReExportPropStreamLabel, plasticIncineratedPropStreamLabel, plasticLandfillPropStreamLabel, wasteFacilityEmissionsStreamLabel, landfillEmissionsStreamLabel]

conditionsStreamStreamLabelsListForPlacement = [conditionsTitleStreamLabel, totalMSWStreamLabel, totalPlasticStreamLabel, plasticRecycledPropStreamLabel, plasticDomesticStreamLabel, plasticExportPropStreamLabel, plasticReExportPropStreamLabel,
                                                plasticRecycEfficiencyStreamLabel, plasticIncineratedPropStreamLabel,  plasticLandfillPropStreamLabel, wasteFacilityEmissionsStreamLabel, landfillEmissionsStreamLabel]



#Recycling data input StreamLabels and entry boxes
totalRecycStreamLabel = Label(my_frame7, text = "Recycling Data", bg = 'white', font = 'Helvetica 12 bold')
totalRecycMassStreamLabel = Label(my_frame7, text = "Total Recycled Mass:", bg = 'white', font = fontChoice)
miscInOrgRecycStreamLabel = Label(my_frame7, text = "Misc. Inorg Waste (Fraction): ", bg = 'white', font = fontChoice)
otherWasteRecycStreamLabel = Label(my_frame7, text = "Other (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsRecycStreamLabel = Label(my_frame7, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodRecycStreamLabel = Label(my_frame7, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltRecycStreamLabel = Label(my_frame7, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodRecycStreamLabel = Label(my_frame7, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalRecycStreamLabel = Label(my_frame7, text = "Metals (Fraction):", bg = 'white', font = fontChoice)
glassRecycStreamLabel = Label(my_frame7, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperRecycStreamLabel = Label(my_frame7, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticRecycStreamLabel = Label(my_frame7, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)


recycMSWPropsStreamStreamLabels= [totalRecycStreamLabel, totalRecycMassStreamLabel, miscInOrgRecycStreamLabel, otherWasteRecycStreamLabel, yardTrimmingsRecycStreamLabel, foodRecycStreamLabel,
                      rltRecycStreamLabel, woodRecycStreamLabel, metalRecycStreamLabel, glassRecycStreamLabel, paperRecycStreamLabel, plasticRecycStreamLabel]



#Incineration data input StreamLabels and entry boxes
totalIncinStreamLabel = Label(my_frame7, text = "Incineration Data", bg = 'white', font = 'Helvetica 12 bold')
totalIncinMassStreamLabel = Label(my_frame7, text = "Total Mass Incinerated: ", bg = 'white', font = fontChoice)
miscInOrgIncinStreamLabel = Label(my_frame7, text = "Misc. Inorganic Wastes (Fraction):", bg = 'white', font = fontChoice)
otherWasteIncinStreamLabel = Label(my_frame7, text = "Other Wastes (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsIncinStreamLabel = Label(my_frame7, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodIncinStreamLabel = Label(my_frame7, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltIncinStreamLabel = Label(my_frame7, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodIncinStreamLabel = Label(my_frame7, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalIncinStreamLabel = Label(my_frame7, text = "Metal (Fraction):", bg = 'white', font = fontChoice)
glassIncinStreamLabel = Label(my_frame7, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperIncinStreamLabel = Label(my_frame7, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticIncinStreamLabel = Label(my_frame7, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)


IncinMSWPropsStreamStreamLabels= [totalIncinStreamLabel, totalIncinMassStreamLabel, miscInOrgIncinStreamLabel, otherWasteIncinStreamLabel, yardTrimmingsIncinStreamLabel, foodIncinStreamLabel,
                                  rltIncinStreamLabel, woodIncinStreamLabel, metalIncinStreamLabel, glassIncinStreamLabel, paperIncinStreamLabel, plasticIncinStreamLabel]


#Compost data input StreamLabels and entry boxes
totalCompostStreamLabel = Label(my_frame7, text = "Compost Data", bg = 'white', font = 'Helvetica 12 bold')
totalCompostMassStreamLabel = Label(my_frame7, text = "Total Mass Compost: ", bg = 'white', font = fontChoice)
miscInOrgCompostStreamLabel = Label(my_frame7, text = "Misc. Inorganic Wastes (Fraction):", bg = 'white', font = fontChoice)
otherWasteCompostStreamLabel = Label(my_frame7, text = "Other Wastes (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsCompostStreamLabel = Label(my_frame7, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodCompostStreamLabel = Label(my_frame7, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltCompostStreamLabel = Label(my_frame7, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodCompostStreamLabel = Label(my_frame7, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalCompostStreamLabel = Label(my_frame7, text = "Metal (Fraction):", bg = 'white', font = fontChoice)
glassCompostStreamLabel = Label(my_frame7, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperCompostStreamLabel = Label(my_frame7, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticCompostStreamLabel = Label(my_frame7, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)



CompostMSWPropsStreamStreamLabels= [totalCompostStreamLabel, totalCompostMassStreamLabel, miscInOrgCompostStreamLabel, otherWasteCompostStreamLabel, yardTrimmingsCompostStreamLabel, foodCompostStreamLabel,
                      rltCompostStreamLabel, woodCompostStreamLabel, metalCompostStreamLabel, glassCompostStreamLabel, paperCompostStreamLabel, plasticCompostStreamLabel]



#Landfill Data input StreamLabels and entries
totalLandStreamLabel = Label(my_frame7, text = "Landfill Data", bg = 'white', font = 'Helvetica 12 bold')
totalLandMassStreamLabel = Label(my_frame7, text = "Total Mass Landfilled: ", bg = 'white', font = fontChoice)
miscInOrgLandStreamLabel = Label(my_frame7, text = "Misc. Inorganic Wastes (Fraction):", bg = 'white', font = fontChoice)
otherWasteLandStreamLabel = Label(my_frame7, text = "Other Wastes (Fraction):", bg = 'white', font = fontChoice)
yardTrimmingsLandStreamLabel = Label(my_frame7, text = "Yard Trimmings (Fraction):", bg = 'white', font = fontChoice)
foodLandStreamLabel = Label(my_frame7, text = "Food (Fraction):", bg = 'white', font = fontChoice)
rltLandStreamLabel = Label(my_frame7, text = "Rubber, Leather, Textiles (Fraction):", bg = 'white', font = fontChoice)
woodLandStreamLabel = Label(my_frame7, text = "Wood (Fraction):", bg = 'white', font = fontChoice)
metalLandStreamLabel = Label(my_frame7, text = "Metal (Fraction):", bg = 'white', font = fontChoice)
glassLandStreamLabel = Label(my_frame7, text = "Glass (Fraction):", bg = 'white', font = fontChoice)
paperLandStreamLabel = Label(my_frame7, text = "Paper and Paperboard (Fraction):", bg = 'white', font = fontChoice)
plasticLandStreamLabel = Label(my_frame7, text = "Plastic (Fraction):", bg = 'white', font = fontChoice)


LandMSWPropsStreamStreamLabels= [totalLandStreamLabel, totalLandMassStreamLabel, miscInOrgLandStreamLabel, otherWasteLandStreamLabel, yardTrimmingsLandStreamLabel, foodLandStreamLabel,
                      rltLandStreamLabel, woodLandStreamLabel, metalLandStreamLabel, glassLandStreamLabel, paperLandStreamLabel, plasticLandStreamLabel]



#Types of plastics entry boxes and StreamLabels for recycled list
plasticRecycProportionsStreamLabel = Label(my_frame7, text = "Plastic Recycled Proportions", bg = 'white', font = 'Helvetica 12 bold')

petRecycStreamLabel = Label(my_frame7, text = "PET Proportion (Fraction):", bg = 'white', font = fontChoice)
hdpeRecycStreamLabel = Label(my_frame7, text = "HDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
pvcRecycStreamLabel = Label(my_frame7, text = "PVC Proportion (Fraction):", bg = 'white', font = fontChoice)
ldpeRecycStreamLabel = Label(my_frame7, text = "LDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
ppRecycStreamLabel = Label(my_frame7, text = "PP Proportion (Fraction):", bg = 'white', font = fontChoice)
psRecycStreamLabel = Label(my_frame7, text = "PS Proportion (Fraction):", bg = 'white', font = fontChoice)
otherRecycPlasticsStreamLabel = Label(my_frame7, text = "Other Plastics Proportion (Fraction):", bg = 'white', font = fontChoice)
plaRecycStreamLabel = Label(my_frame7, text = "PLA Proportion (Fraction):", bg = 'white', font = fontChoice)

plasticRecycPropsStreamsLabels = [plasticRecycProportionsStreamLabel, petRecycStreamLabel, hdpeRecycStreamLabel, pvcRecycStreamLabel, ldpeRecycStreamLabel, plaRecycStreamLabel, ppRecycStreamLabel, 
                           psRecycStreamLabel, otherRecycPlasticsStreamLabel]

#Types of plastics entry boxes and StreamLabels for landfilled list
plasticLandProportionsStreamLabel = Label(my_frame7, text = "Plastic Landfilled Proportions", bg = 'white', font = 'Helvetica 12 bold')

petLandStreamLabel = Label(my_frame7, text = "PET Proportion (Fraction):", bg = 'white', font = fontChoice)
hdpeLandStreamLabel = Label(my_frame7, text = "HDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
pvcLandStreamLabel = Label(my_frame7, text = "PVC Proportion (Fraction):", bg = 'white', font = fontChoice)
ldpeLandStreamLabel = Label(my_frame7, text = "LDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
ppLandStreamLabel = Label(my_frame7, text = "PP Proportion (Fraction):", bg = 'white', font = fontChoice)
psLandStreamLabel = Label(my_frame7, text = "PS Proportion (Fraction):", bg = 'white', font = fontChoice)
otherLandPlasticsStreamLabel = Label(my_frame7, text = "Other Plastics Proportion (Fraction):", bg = 'white', font = fontChoice)
plaLandStreamLabel = Label(my_frame7, text = "PLA Proportion (Fraction):", bg = 'white', font = fontChoice)



LandPlasticStreamStreamLabels = [plasticLandProportionsStreamLabel, petLandStreamLabel, hdpeLandStreamLabel, pvcLandStreamLabel, ldpeLandStreamLabel, plaLandStreamLabel, ppLandStreamLabel, psLandStreamLabel, otherLandPlasticsStreamLabel]


#Types of plastics entry boxes and StreamLabels for Incinerated list
plasticIncinProportionsStreamLabel = Label(my_frame7, text = "Plastic Incinerated Proportions", bg = 'white', font = 'Helvetica 12 bold')

petIncinStreamLabel = Label(my_frame7, text = "PET Proportion (Fraction):", bg = 'white', font = fontChoice)
hdpeIncinStreamLabel = Label(my_frame7, text = "HDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
pvcIncinStreamLabel = Label(my_frame7, text = "PVC Proportion (Fraction):", bg = 'white', font = fontChoice)
ldpeIncinStreamLabel = Label(my_frame7, text = "LDPE Proportion (Fraction):", bg = 'white', font = fontChoice)
ppIncinStreamLabel = Label(my_frame7, text = "PP Proportion (Fraction):", bg = 'white', font = fontChoice)
psIncinStreamLabel = Label(my_frame7, text = "PS Proportion (Fraction):", bg = 'white', font = fontChoice)
otherIncinPlasticsStreamLabel = Label(my_frame7, text = "Other Plastics Proportion (Fraction):", bg = 'white', font = fontChoice)
plaIncinStreamLabel = Label(my_frame7, text = "PLA Proportion (Fraction):", bg = 'white', font = fontChoice)


IncinPlasticStreamStreamLabels = [plasticIncinProportionsStreamLabel, petIncinStreamLabel, hdpeIncinStreamLabel, pvcIncinStreamLabel, ldpeIncinStreamLabel, plaIncinStreamLabel, ppIncinStreamLabel, psIncinStreamLabel, otherIncinPlasticsStreamLabel]

#Types of plastics entry boxes and StreamLabels for reported recycled list
plasticRepRecycProportionsStreamLabel = Label(my_frame7, text = "Plastic Reported Recycled Masses", bg = 'white', font = 'Helvetica 12 bold')

petRepRecycStreamLabel = Label(my_frame7, text = "PET Proportion (Tons):", bg = 'white', font = fontChoice)
hdpeRepRecycStreamLabel = Label(my_frame7, text = "HDPE Proportion (Tons):", bg = 'white', font = fontChoice)
pvcRepRecycStreamLabel = Label(my_frame7, text = "PVC Proportion (Tons):", bg = 'white', font = fontChoice)
ldpeRepRecycStreamLabel = Label(my_frame7, text = "LDPE Proportion (Tons):", bg = 'white', font = fontChoice)
ppRepRecycStreamLabel = Label(my_frame7, text = "PP Proportion (Tons):", bg = 'white', font = fontChoice)
psRepRecycStreamLabel = Label(my_frame7, text = "PS Proportion (Tons):", bg = 'white', font = fontChoice)
otherRepRecycPlasticsStreamLabel = Label(my_frame7, text = "Other Plastics Proportion (Tons):", bg = 'white', font = fontChoice)
plaRepRecycStreamLabel = Label(my_frame7, text = "PLA Proportion (Tons):", bg = 'white', font = fontChoice)


RepRecycPlasticStreamStreamLabels = [plasticRepRecycProportionsStreamLabel, petRepRecycStreamLabel, hdpeRepRecycStreamLabel, pvcRepRecycStreamLabel, ldpeRepRecycStreamLabel, plaRepRecycStreamLabel, ppRepRecycStreamLabel, psRepRecycStreamLabel, otherRepRecycPlasticsStreamLabel]

#Types of plastics entry boxes and StreamLabels for import list
plasticImportProportionsStreamLabel = Label(my_frame7, text = "Plastic Imported Mass", bg = 'white', font = 'Helvetica 12 bold')

ethyleneImportStreamLabel = Label(my_frame7, text = "Ethylene Mass (Tons):", bg = 'white', font = fontChoice)
vinylChlorideImportStreamLabel = Label(my_frame7, text = "Vinyl Chloride Mass (Tons):", bg = 'white', font = fontChoice)
styreneImportStreamLabel = Label(my_frame7, text = "Styrene Mass (Tons):", bg = 'white', font = fontChoice)
otherImportStreamLabel = Label(my_frame7, text = "Other Plastics (Tons):", bg = 'white', font = fontChoice)



ImportPlasticStreamStreamLabels = [plasticImportProportionsStreamLabel, ethyleneImportStreamLabel, vinylChlorideImportStreamLabel, styreneImportStreamLabel, otherImportStreamLabel]


#Types of plastics entry boxes and StreamLabels for Export list
plasticExportProportionsStreamLabel = Label(my_frame7, text = "Plastic Exported Mass", bg = 'white', font = 'Helvetica 12 bold')

ethyleneExportStreamLabel = Label(my_frame7, text = "Ethylene Mass (Tons):", bg = 'white', font = fontChoice)
vinylChlorideExportStreamLabel = Label(my_frame7, text = "Vinyl Chloride Mass (Tons):", bg = 'white', font = fontChoice)
styreneExportStreamLabel = Label(my_frame7, text = "Styrene Mass (Tons):", bg = 'white', font = fontChoice)
otherExportStreamLabel = Label(my_frame7, text = "Other Plastics (Tons):", bg = 'white', font = fontChoice)



ExportPlasticStreamStreamLabels = [plasticExportProportionsStreamLabel, ethyleneExportStreamLabel, vinylChlorideExportStreamLabel, styreneExportStreamLabel, otherExportStreamLabel]


#Types of plastics entry boxes and StreamLabels for ReExport list
plasticReExportProportionsStreamLabel = Label(my_frame7, text = "Plastic ReExported Mass", bg = 'white', font = 'Helvetica 12 bold')

ethyleneReExportStreamLabel = Label(my_frame7, text = "Ethylene Mass (Tons):", bg = 'white', font = fontChoice)
vinylChlorideReExportStreamLabel = Label(my_frame7, text = "Vinyl Chloride Mass (Tons):", bg = 'white', font = fontChoice)
styreneReExportStreamLabel = Label(my_frame7, text = "Styrene Mass (Tons):", bg = 'white', font = fontChoice)
otherReExportStreamLabel = Label(my_frame7, text = "Other Plastics (Tons):", bg = 'white', font = fontChoice)

ReExportPlasticStreamStreamLabels = [plasticReExportProportionsStreamLabel, ethyleneReExportStreamLabel, vinylChlorideReExportStreamLabel, styreneReExportStreamLabel, otherReExportStreamLabel]

#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
##################################################################################################################################################################
#Labels whose text will show Values
miscInOrgWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
otherWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
yardTrimmingsValueLabel = Label(my_frame7, font = fontChoice, bg="white")
foodWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
rltWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
woodWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
metalsWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
glassWasteValueLabel = Label(my_frame7, font = fontChoice, bg="white")
paperAndBoardValueLabel = Label(my_frame7, font = fontChoice, bg="white")
plasticsValueLabel = Label(my_frame7, font = fontChoice, bg="white")


#Creating list of value labels MJC
typesOfWasteValueLabels = [miscInOrgWasteValueLabel, otherWasteValueLabel, yardTrimmingsValueLabel, foodWasteValueLabel, rltWasteValueLabel, woodWasteValueLabel, metalsWasteValueLabel, glassWasteValueLabel, paperAndBoardValueLabel, plasticsValueLabel]



#Creates conditions StreamLabels and entries
totalMSWValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
totalPlasticValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticRecycledPropValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticDomesticValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticRecycEfficiencyValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticExportPropValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticReExportPropValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticIncineratedPropValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticLandfillPropValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
wasteFacilityEmissionsValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
landfillEmissionsValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)



conditionsValueValueLabelsList = [totalMSWValueLabel, totalPlasticValueLabel, plasticRecycledPropValueLabel, plasticDomesticValueLabel, plasticRecycEfficiencyValueLabel, plasticExportPropValueLabel,
                        plasticReExportPropValueLabel, plasticIncineratedPropValueLabel, plasticLandfillPropValueLabel, wasteFacilityEmissionsValueLabel, landfillEmissionsValueLabel]

conditionsValueValueLabelsListForPlacement = [totalMSWValueLabel, totalPlasticValueLabel, plasticRecycledPropValueLabel, plasticDomesticValueLabel, plasticExportPropValueLabel,
                                  plasticReExportPropValueLabel, plasticRecycEfficiencyValueLabel, plasticIncineratedPropValueLabel, plasticLandfillPropValueLabel, wasteFacilityEmissionsValueLabel, 
                                  landfillEmissionsValueLabel]


#Recycling data input StreamLabels and entry boxes
totalRecycMassValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
miscInOrgRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherWasteRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
yardTrimmingsRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
foodRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
rltRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
woodRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
metalRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
glassRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
paperRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)


recycMSWPropsValueLabels= [totalRecycMassValueLabel, miscInOrgRecycValueLabel, otherWasteRecycValueLabel, yardTrimmingsRecycValueLabel, foodRecycValueLabel,
                      rltRecycValueLabel, woodRecycValueLabel, metalRecycValueLabel, glassRecycValueLabel, paperRecycValueLabel, plasticRecycValueLabel]



#Incineration data input StreamLabels and entry boxes
totalIncinMassValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
miscInOrgIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherWasteIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
yardTrimmingsIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
foodIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
rltIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
woodIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
metalIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
glassIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
paperIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)


IncinMSWPropsValueLabels= [totalIncinMassValueLabel, miscInOrgIncinValueLabel, otherWasteIncinValueLabel, yardTrimmingsIncinValueLabel, foodIncinValueLabel,
                      rltIncinValueLabel, woodIncinValueLabel, metalIncinValueLabel, glassIncinValueLabel, paperIncinValueLabel, plasticIncinValueLabel]


#Compost data input StreamLabels and entry boxes
totalCompostMassValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
miscInOrgCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherWasteCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
yardTrimmingsCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
foodCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
rltCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
woodCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
metalCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
glassCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
paperCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticCompostValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)



CompostMSWPropsValueLabels= [totalCompostMassValueLabel, miscInOrgCompostValueLabel, otherWasteCompostValueLabel, yardTrimmingsCompostValueLabel, foodCompostValueLabel,
                      rltCompostValueLabel, woodCompostValueLabel, metalCompostValueLabel, glassCompostValueLabel, paperCompostValueLabel, plasticCompostValueLabel]



#Landfill Data input StreamLabels and entries
totalLandMassValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
miscInOrgLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherWasteLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
yardTrimmingsLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
foodLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
rltLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
woodLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
metalLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
glassLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
paperLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plasticLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)


LandMSWPropsValueLabels= [totalLandMassValueLabel, miscInOrgLandValueLabel, otherWasteLandValueLabel, yardTrimmingsLandValueLabel, foodLandValueLabel,
                      rltLandValueLabel, woodLandValueLabel, metalLandValueLabel, glassLandValueLabel, paperLandValueLabel, plasticLandValueLabel]



#Types of plastics entry boxes and StreamLabels for recycled list
petRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
hdpeRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
pvcRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ldpeRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ppRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
psRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherRecycPlasticsValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plaRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)

plasticRecycValueLabels = [petRecycValueLabel, hdpeRecycValueLabel, pvcRecycValueLabel, ldpeRecycValueLabel, plaRecycValueLabel, ppRecycValueLabel, psRecycValueLabel,
                           otherRecycPlasticsValueLabel]

#Types of plastics entry boxes and StreamLabels for landfilled list

petLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
hdpeLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
pvcLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ldpeLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ppLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
psLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherLandPlasticsValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plaLandValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)



LandPlasticValueLabels = [petLandValueLabel, hdpeLandValueLabel, pvcLandValueLabel, ldpeLandValueLabel, plaLandValueLabel, ppLandValueLabel, psLandValueLabel, otherLandPlasticsValueLabel]


#Types of plastics entry boxes and StreamLabels for Incinerated list
petIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
hdpeIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
pvcIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ldpeIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ppIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
psIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherIncinPlasticsValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plaIncinValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)


IncinPlasticValueLabels = [petIncinValueLabel, hdpeIncinValueLabel, pvcIncinValueLabel, ldpeIncinValueLabel, plaIncinValueLabel, ppIncinValueLabel, psIncinValueLabel, otherIncinPlasticsValueLabel]

#Types of plastics entry boxes and StreamLabels for reported recycled list
petRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
hdpeRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
pvcRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ldpeRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
ppRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
psRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherRepRecycPlasticsValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
plaRepRecycValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)


RepRecycPlasticValueLabel = [petRepRecycValueLabel, hdpeRepRecycValueLabel, pvcRepRecycValueLabel, ldpeRepRecycValueLabel, plaRepRecycValueLabel, ppRepRecycValueLabel, psRepRecycValueLabel, otherRepRecycPlasticsValueLabel]

#Types of plastics entry boxes and StreamLabels for import list
ethyleneImportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
vinylChlorideImportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
styreneImportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherImportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)



ImportPlasticValueLabels = [ethyleneImportValueLabel, vinylChlorideImportValueLabel, styreneImportValueLabel, otherImportValueLabel]


#Types of plastics entry boxes and StreamLabels for Export list
ethyleneExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
vinylChlorideExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
styreneExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)



ExportPlasticValueLabels = [ethyleneExportValueLabel, vinylChlorideExportValueLabel, styreneExportValueLabel, otherExportValueLabel]


#Types of plastics entry boxes and StreamLabels for ReExport list
ethyleneReExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
vinylChlorideReExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
styreneReExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)
otherReExportValueLabel = Label(my_frame7, bg = 'white', font = fontChoice)

ReExportPlasticValueLabels = [ethyleneReExportValueLabel, vinylChlorideReExportValueLabel, styreneReExportValueLabel, otherReExportValueLabel]


#list of each row's labels
rowStream1 = [conditionsStreamStreamLabelsListForPlacement, typesOfWasteStreamStreamLabels, recycMSWPropsStreamStreamLabels]

rowStream2 = [IncinMSWPropsStreamStreamLabels, LandMSWPropsStreamStreamLabels, CompostMSWPropsStreamStreamLabels]

rowStream3 = [plasticRecycPropsStreamsLabels, IncinPlasticStreamStreamLabels, LandPlasticStreamStreamLabels]

rowStream4 = [RepRecycPlasticStreamStreamLabels, ImportPlasticStreamStreamLabels, ExportPlasticStreamStreamLabels]

rowStream5 = [ReExportPlasticStreamStreamLabels]

rowValue1 = [conditionsValueValueLabelsListForPlacement, typesOfWasteValueLabels, recycMSWPropsValueLabels]

rowValue2 = [IncinMSWPropsValueLabels, LandMSWPropsValueLabels, CompostMSWPropsValueLabels]

rowValue3 = [plasticRecycValueLabels, IncinPlasticValueLabels, LandPlasticValueLabels]

rowValue4 = [RepRecycPlasticValueLabel, ImportPlasticValueLabels, ExportPlasticValueLabels]

rowValue5 = [ReExportPlasticValueLabels]

gapLabel13.grid(column = 0, row = 1, columnspan = 6)

#Function that will place each row of labels in the appropriate spot
def rowStreamPlacer(stream, value, gap, row):
    col = 0
    for i in range(len(stream)):
        frameNum = row
        for a in range(len(stream[i])):
            if a == 0:
                stream[i][a].grid(column = col, row = frameNum, columnspan = 2)
                frameNum +=1

                if i ==0:
                    gapLabelsList[gap].grid(column = 0, row = frameNum, columnspan = 6)
            else:
                stream[i][a].grid(column = col, row = frameNum, sticky = E)
                value[i][a-1].grid(column = col +1, row = frameNum, sticky = W)
            frameNum+=1
        col +=2
    
    
#places rows and appropriate gap labels
rowStreamPlacer(rowStream1, rowValue1, 0, 2)
gapLabelsList[1].grid(column = 0, row =15, columnspan = 6)
rowStreamPlacer(rowStream2, rowValue2, 2, 16)
gapLabelsList[3].grid(column = 0, row = 29, columnspan = 6)
rowStreamPlacer(rowStream3, rowValue3, 4, 30)
gapLabelsList[5].grid(column = 0, row = 40, columnspan = 6)
rowStreamPlacer(rowStream4, rowValue4, 6, 41)
gapLabelsList[7].grid(column = 0, row = 51, columnspan = 6)
rowStreamPlacer(rowStream5, rowValue5, 8, 52)
gapLabelsList[9].grid(column = 0, row = 58, columnspan = 6)

            

#Creates scrollbar for input data frame
dataAnalysisScrollBar = Scrollbar(my_frame7, orient = 'vertical', command = dataAnalysisCanvas.yview)
dataAnalysisScrollBar.grid(column = 6, row = 0, rowspan = 80, sticky = NS)


   

###################################################
#Creating flow diagram
#function that will open pop up window with stream trvw when button is pressed
def open_popup():
    
    #Creates pop up window with title
   top= Toplevel(streamFrame)
   top.geometry('%dx%d+%d+%d' % (w, h, x, y-25))
   top.title("Stream Calculations")
   
   #Creates and packs stream summary trvw (table)
   streamSummaryTRVW = ttk.Treeview(top)
   streamSummaryTRVW.pack(padx=5, pady=5, fill='both', expand=True,side='top')
   
   #Creates and configures x, then y scrollbar for trvw
   streamSummaryScrollBar = Scrollbar(top, orient = 'horizontal', command = streamSummaryTRVW.xview)
   streamSummaryScrollBar.config(command = streamSummaryTRVW.xview)
   streamSummaryTRVW.configure(xscrollcommand = streamSummaryScrollBar.set)
   
   streamSummaryYScrollBar = Scrollbar(top, orient = 'vertical', command = streamSummaryTRVW.yview)
   streamSummaryYScrollBar.config(command = streamSummaryTRVW.xview)
   streamSummaryTRVW.configure(yscrollcommand = streamSummaryYScrollBar.set)
   
   #packs y scrollbar -- there is some issue here I will return to MJC
   #streamSummaryYScrollBar.pack(side = RIGHT, fill = Y)
   
   #Creates and packs button that will eventually allow data to be exported to excel
   exportButton = Button(top, text = 'Export to Excel')
   exportButton.pack()
   
   #creates column headings in trvw
   streamSummaryColumns = tuple(['Stream'] + [str(i) for i in range(1,31)]+['Waste Incinerated 2018', 'Waste Accumulated in Landfill 2018'])
   streamSummaryTRVW['columns']=streamSummaryColumns
   streamSummaryTRVW.column('#0', width = 0, stretch = NO)
   for name in streamSummaryColumns:
       streamSummaryTRVW.column(name, width = 250, anchor = CENTER, stretch = NO)
       streamSummaryTRVW.heading(name, text = name)
       streamTitleRows = ['Stream Title', 'Monomer/Raw Materials', 'Additives', 'Manufacture GHG Releases', 'Manufacture to Use', 'Additives Migration', 'Use to Collection', 'Collection GHG Emissions', 'Other Waste into Collection', 
                          'Plastic Litter', 'Collection to Sort', 'Nonrecyclable Incinerate: Sort to Incineration', 'Sort to Landfill', 'Sort to Compost', 'Sort to Recycle: Recyclable Nonplastic Waste', 'Sort GHG Emissions', 'Sort to Mechanical Recycling', 'Mechanical Recycling Net GHG Emissions', 
                          'Mechanical Recycling Additive Migration', 'Mechanical Recycling Additive Contamination', 'Plastic: Mechanical Recycling to Manufacture', 'Plastic Import', 'Plastic Re-Export', 'Mechanical Recycling to Incineration', 'Plastic: Sort to Incineration', "Incineration GHG Emissions",
                          'Plastic: Sort to Landfill', 'Plastic Export from Sort', 'Mechanical Recycling to Landfill', 'Landfill Plastic Leak', 'Landfill GHG Emissions', '', '']
  
    #inserts titles into stream summary trvw

   streamSummaryTRVW.insert(parent ='', index ='end', iid = 0, text = '', values = tuple([streamTitleRows[b] for b in range(len(streamTitleRows))]))
   
   count = 1
   #inserts data into stream summary trvw
   for i in streamTRVWLists:
       streamSummaryTRVW.insert(parent ='', index ='end', iid = count, text = '', values = tuple([trvwRounder(i[b]) for b in range(len(i))]))
       count +=1
       
       
    #adds stream summary scroll bars
   streamSummaryScrollBar.pack(fill = X)

#Creates buttons that will create pop up buttons
popUpButton = Button(streamFrame, text = "Show Stream Calculations", command = open_popup)
popUpButton.pack() #places button

#Begins creation of flow diagram
flow = plt.figure(figsize = (40,45), dpi = 44) #Creates matplot figure


#Creates lists that will be used to note connections between nodes
From = ['Manufacture', "Stream 4:\nManufacture\nto Use",'Use', "Stream 6:\nUse to\nCollection",'Collection'] 

To = ["Stream 4:\nManufacture\nto Use", 'Use', "Stream 6:\nUse to\nCollection", "Collection", 'Stream 10:\nCollection\nto Sort']


From1 = ['Stream 10:\nCollection\nto Sort',"Sort", 'Stream 16:\nSort to\nMechanical\nRecycling', 'Sort', 'Stream 11:\nNonrecyclable\nSort to\nIncineration']
 
To1 = ["Sort",'Stream 16:\nSort to\nMechanical\nRecycling','Mechanical\nRecycling','Stream 11:\nNonrecyclable\nSort to\nIncineration', 'Energy\nRecovery\n(Incineration)']


From2 = ['Sort', 'Stream 13:\nSort to\nCompost', 'Sort', 'Stream 12:\nSort to\nLandfill','Mechanical\nRecycling', 'Stream 20:\nPlastic\nRecyclate\nto\nManufacture']

To2 = ['Stream 13:\nSort to\nCompost', 'Compost',
      'Stream 12:\nSort to\nLandfill', 'Landfilling and\nDegradation', 'Stream 20:\nPlastic\nRecyclate\nto\nManufacture', 'Manufacture']


From3 = ['Mechanical\nRecycling', 'Stream 23:\nRecycling\nto\nIncineration', 'Stream 1:\nMonomer\n and Raw\nMaterals',
        'Stream 2:\nAdditives', 'Manufacture']

To3 = ['Stream 23:\nRecycling\nto\nIncineration', 'Energy\nRecovery\n(Incineration)', 'Manufacture', 'Manufacture',
       "Stream 3:\nGHG\nReleases"]


From4 = ["Use", 'Collection', 'Stream 8:\nOther Waste', 'Collection', 'Sort']

To4 = ["Stream 5:\nAdditive\nMigration", 'Stream 7:\nGHG\nReleases', 'Collection', 'Stream 9:\nPlastic\nLitter', 'Stream 14:\nRecyclable\nNonplastics']


From5 = ["Sort", "Mechanical\nRecycling", 'Mechanical\nRecycling', "Stream 19:\nAdditive\nContamination", "Stream 21:\nPlastic Import", 
         "Mechanical\nRecycling", "Sort", "Stream 24:\nPlastic Sort\nto\nIncineration"]

To5 = ["Stream 15:\nGHG\nReleases","Stream 17:\nNet GHG\nReleases", "Stream 18:\nAdditive\nMigration", "Mechanical\nRecycling", "Mechanical\nRecycling",
       "Stream 22:\nPlastic\nRe-Export", "Stream 24:\nPlastic Sort\nto\nIncineration", 'Energy\nRecovery\n(Incineration)']


From6 = ['Energy\nRecovery\n(Incineration)', 'Sort', 'Stream 26:\nPlastic Sort\nto Landfill',
         'Sort', 'Mechanical\nRecycling', 'Stream 28:\nRecycling\nto Landfill', 'Landfilling and\nDegradation', 'Landfilling and\nDegradation']

To6 = ["Stream 25:\nGHG\nReleases", 'Stream 26:\nPlastic Sort\nto Landfill', 'Landfilling and\nDegradation',
       'Stream 27:\nPlastic Export', 'Stream 28:\nRecycling\nto Landfill', 'Landfilling and\nDegradation', 'Stream 29:\nPlastic Leak', 
       'Stream 30:\nGHG\nReleases']


#creates full list connecting appropriate nodes
Froms = [From1, From2, From3, From4, From5, From6]
Tos = [To1, To2, To3, To4, To5, To6]

for i in Froms:
    From +=i
    
for i in Tos:
    To +=i

#Creates data frame that shows connection of nodes
df = pd.DataFrame({ 'from':From,
                   'to':To})



# Define Node Positions
pos = {'Manufacture':(-1,36),
        'Sort':(47.5,33.5),
        'Collection':(30,44),
        'Use':(21.5,36),
        'Mechanical\nRecycling':(11,28),
        'Energy\nRecovery\n(Incineration)':(21.5,1),
        'Compost':(57,23),
        'Landfilling and\nDegradation': (57,15),
        'Stream 1:\nMonomer\n and Raw\nMaterals': (-1, 48),
        'Stream 2:\nAdditives': (5,48),
        "Stream 4:\nManufacture\nto Use": (11,36),
        "Stream 3:\nGHG\nReleases": (10,48),
        "Stream 5:\nAdditive\nMigration": (15,48),
        "Stream 6:\nUse to\nCollection":(20,48),
        'Stream 7:\nGHG\nReleases':(40,48),
        'Stream 8:\nOther Waste':(42,41),
        'Stream 9:\nPlastic\nLitter':(39, 38),
        'Stream 10:\nCollection\nto Sort':(34.5, 34.5),
        'Stream 11:\nNonrecyclable\nSort to\nIncineration': (40,6),
        'Stream 12:\nSort to\nLandfill':(47,23),
        'Stream 13:\nSort to\nCompost': (58, 34.5),
        'Stream 14:\nRecyclable\nNonplastics':(55,48),
        "Stream 15:\nGHG\nReleases": (58,42),
        'Stream 16:\nSort to\nMechanical\nRecycling':(21.5,28),
        "Stream 17:\nNet GHG\nReleases":(-1, 9),
        "Stream 18:\nAdditive\nMigration":(7,6),
        "Stream 19:\nAdditive\nContamination":(2, 7.5),
        'Stream 20:\nPlastic\nRecyclate\nto\nManufacture': (-1,24.5),
        "Stream 21:\nPlastic Import": (12,7.5),
        "Stream 22:\nPlastic\nRe-Export": (-1, 16),
        'Stream 23:\nRecycling\nto\nIncineration': (17,11.5),
        "Stream 24:\nPlastic Sort\nto\nIncineration":(21.5,12.5),
        "Stream 25:\nGHG\nReleases":(40,-1),
        'Stream 26:\nPlastic Sort\nto Landfill': (40,22),
        'Stream 27:\nPlastic Export':(48, 48),
        'Stream 28:\nRecycling\nto Landfill': (21.5, 20),
        'Stream 29:\nPlastic Leak':(53,-1),
        'Stream 30:\nGHG\nReleases': (57,-1)}


Labels = {}
i = 0
for a in From:
    Labels[a]=a
    i +=1
    

for i in To:
    if i not in list(Labels.values()):
        Labels[i] = i


# Build your graph. Note that we use the DiGraph function to create the graph! This adds arrows
G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph() )

# Define the colormap and set nodes to circles, but the last one to a triangle
Circles = []
Square = []

for n in G.nodes:
    if 'Stream' in n:
        Square.append(n)
    else:
        Circles.append(n)

# By making a white node that is larger, I can make the arrow "start" beyond the node


nodes = nx.draw_networkx_nodes(G, pos, 
                       nodelist = Circles,
                       node_size=8.5e3,
                       node_shape='o',
                       node_color= 'seagreen',
                       edgecolors='black',
                       alpha=0.5)

nodes = nx.draw_networkx_nodes(G, pos, 
                       nodelist = Square,
                       node_size=5.5e3,
                       node_shape='s',
                       node_color='white',
                       edgecolors='black',
                       alpha=0.5)


nx.draw_networkx_labels(G, pos, Labels, font_size=12)

# Again by making the node_size larer, I can have the arrows end before they actually hit the node
edges = nx.draw_networkx_edges(G, pos, node_size=1e4,
                               arrowstyle='->',width=2)


flowCanvas = FigureCanvasTkAgg(flow, master = streamFrame)
flowCanvas.draw()
flowCanvas.get_tk_widget().pack()



###################################################
### Material Data tab


#Adding Textbox to Material data tab for title, configuring and packing
text_frame3 = tk.Text(my_frame3, bg = "white", height=2, width=200)
text_frame3.config(font=("Helvetica 20 bold"))
text_frame3.insert(tk.INSERT,"\nMaterial Data")
text_frame3.tag_configure('center', justify = "center")
text_frame3.tag_add('center', 1.0, 'end')
text_frame3.config(state="disabled")
text_frame3.pack()

#Creating and packing table
trvw= ttk.Treeview(my_frame3,show='headings')
trvw.pack(padx=5, pady=5, fill='both', expand=True,side='top')



#Creates scoll bars in (x) directions        
#Creates scoll bars in (y) directions  
scrollbary2=ttk.Scrollbar(trvw, orient="vertical", command=trvw.yview) 
scrollbary2.pack(side="right", fill="y") 
# assign the scrollbars to the Treeview Widget
trvw.configure(yscrollcommand=scrollbary2.set) 

#Creates lists that will be added to the table
dataframe2_rows = [['Iron_Steel', 2.19, 0.44], ['Low Carbon steel', 1.8, 0.44], ['Low alloy steel (cranskshafts and tools)', 2.0, 0.52], ['Cast Iron', 10.5, 0.51], ['Stainless_Steel', 4.95, 0.73], ['Aluminum', 12.0, 2.1], ['Magnesium alloys', 24.5, 2.9], ['Titanium alloy', 46.5, 5.2], ['Copper alloys', 3.7, 0.83], ['Lead alloys', 2.0, 0.45], ['Zinc (die cast) alloys', 4.1, 0.67], ['Zinc alloys', 3.2, 0.67], ['Nickel-Chromium alloy', 11.5, 2.0], ['Nickel-based superalloys', 35.6, 4.3], ['Silver', 100.0, 9.3], ['Gold', 26500.0, 43.0], ['Platinum', 14750.0, 367.0], ['Nickel', 9.0, 0.7], ['Palladium', 425.5, 'nan'], ['Rhodium', 1100.0, 'nan'], ['Iridium', 165.0, 'nan'], ['PP', 3.05, 2.1], ['PE', 2.75, 2.85], ['PET', 3.9, 2.35], ['LDPE', 2.75, 2.85], ['HDPE', 3.26, 2.28], ['PVC', 2.5, 2.15], ['PES (polysulfone)', 3.0, 0.0], ['PUR (polyurethane)', 3.7, 1.26], ['PUR foam', 4.5, 0.0], ['ABS', 3.8, 2.8], ['PS', 3.8, 2.85], ['Polycarbonate', 6.0, 2.55], ['Polyamide_Nylon', 7.95, 2.56], ['Polyactide (PLA)', 3.6, 2.2], ['Polyester', 'nan', 'nan'], ['Phenolics', 3.6, 'nan'], ['Nat_Rubber', 2.1, 'nan'], ['Butyl_Rubber_Synthetics', 6.6, 'nan'], ['Ethylene Vinyl Acetate (EVA)', 2.1, 2.8], ['Paper_Cardboard', 19.5, 0.76], ['Eglass_Fiber', 3.52, 'nan'], ['Cotton', 2.55, 'nan'], ['Systems (unit as specified)', 'nan', 'nan'], ['Desktop computer, without screen', 274.0, 'nan'], ['Laptop Computer', 250.0, 'nan'], ['Small electronic devices (per kg)', 300.0, 'nan'], ['LCD displays (per m2)', 335.0, 'nan'], ['Laser jet printer', 68.0, 'nan'], ['Subsytems, per unit', 'nan', 'nan'], ['Printed wiring board, desktop PC motherboard', 162.0, 'nan'], ['Printed wiring board, laptop PC motherboard', 267.0, 'nan'], ['hard disk drive', 8.0, 'nan'], ['CD-ROM/DVD-ROM drive', 10.0, 'nan'], ['Power supply', 30.0, 'nan'], ['Fan', 12.0, 'nan'], ['Keyboard (per unit)', 27.0, 'nan'], ['Mouse devices, optical with cable, per unit', 6.0, 'nan'], ['Toner module, laser jet', 10.5, 'nan'], ['CPU', 'nan', 'nan'], ['CRT', 'nan', 'nan'], ['LCD', 'nan', 'nan'], ['notebook', 'nan', 'nan'], ['computer_average', 'nan', 'nan'], ['mobile_phone', 'nan', 'nan'], ['CRT_glass', 'nan', 'nan'], ['E_waste_copper', 'nan', 'nan'], ['E_waste_lead', 'nan', 'nan'], ['Printed circuit board', 1723.0, 'nan']]
column_names2=['Material', 'Primary (virgin)', 'Secondary (mechanically recycled)']  

#assigns and adds columns names to table
trvw.configure(columns=column_names2)
for column in trvw["columns"]:
    trvw.heading(column, text=column)# let the column heading = column name

#inserts data into table
for i,row in enumerate(dataframe2_rows):
    if i%2==0:
        trvw.insert("", "end", values=row,tags=('oddrow',))
    else:
        trvw.insert("", "end", values=row,tags=('evenrow',))
        




#######################################################

#Assumptions Tab MJC

#Creates and packs canvas to allow for scrollbar to be placed
assumptionsCanvas = Canvas(my_frame4, bg = 'white')
assumptionsCanvas.pack()

#Creates and packs frame for assumptions textboxes
assumptionsFrame = Frame(assumptionsCanvas)
assumptionsFrame.pack()

#creates and packs scrollbar for assumptions textboxes
assumpScrollbar = Scrollbar(assumptionsCanvas, orient = 'vertical', command = assumptionsCanvas.yview)
assumpScrollbar.pack(side = 'right', fill = 'y')
assumpScrollbar.config(command=assumptionsCanvas.yview)

#creating and placing title and subtitles for tab
title_frame4 = tk.Text(assumptionsFrame, bd = 0, highlightthickness = 0, bg = "white", height=4, width=100)
title_frame4.config(font=("Helvetica 20 bold"))
title_frame4.insert(tk.INSERT,"\nAssumptions and Justifications")
title_frame4.tag_configure('center', justify = "center")
title_frame4.tag_add('center', 1.0, 'end')
title_frame4.config(state="disabled")
title_frame4.grid(column = 0, row = 0, columnspan = 3)


#list of assumptions (list of lists, in each individual list the first str is the assumption, second str is the effect, third str is the justification)
assumptions = [['Accumulation during consumer use phase is 0', 'Stream 4 = 6', 'It is difficult to predict the use-time of a particular\nplastic product. Thus, in reality, this assumption is\nnot perfectly accurate. For example, in some\napplications such as food storage, people will use the container for years before discarding/recycling it.\nAlternatively, some plastics are used as single-use\nitems (food wrapping, utensils, plates). '], ['10Fraction of plastic produced ends up in the environment/ocean', 'Stream 24= 0.10*Stream 4', 'Realistically, plastics sent to landfills are likely to migrate to another environment. Plastic landfills do hold plastics within the containment barrier. However, a Fraction of plastics does not make it into the containment. Transportation between stages, collection, sorting, and littering are all factors that contribute to plastics release.'], ['Additives composition varies between a specific range based on types. To ensure that the general mass balance of all additive types are accounted for in a given stream, the lowest composition of additive was used for all material balances', 'Lowest additive composition used', 'Plastics manufactured do not necessarily always use every additive possible. In some cases, one plastic product may use fillers, while another type uses none. Using minimum composition lets us assume that, on average, the Fraction of added additives to omitted additives balances the minimum composition. This assumption was made because the average additive composition for "Other plastics" nets a negative polymer resin mass, which is not possible in reality. For instance, suppose that a plastic product is made out of base resin (A), additive B, and additive C. Additive B can range between 5 – 70Fraction of the total mass, while additive eC can range between 10  - 50Fraction of the total mass. The highest additive composition mixture in this situation would result in 120Fraction additives, an impossible scenario. The lowest additive composition equates to 15Fraction additives and 85Fraction base resin. \n\nOur work considers a longer list of additives that could be present. Using the compositions still the additive content to a value higher than 100Fraction. Instead, low composition for all chemical additives is chosen because we also considered the possibility that some additives may not be found in all plastics generated. \n'], ['2Fraction of total plastic waste generated becomes litter', 'Total mass of stream 9 = Stream 4*0.02', 'Jambeck et al 2015 reported a 2Fraction littering rate for plastic waste in their analysis'], ['Degradation of plastic waste in landfill is too slow for appreciable mass loss', 'Mass loss from degradation in landfilling is neglected from plastic ONLY', 'Plastic waste can take hundreds of years to degrade in the environment. When performing a material flow analysis on the basis of one year, the mass loss of plastic waste can be considered negligible. However, mass loss to the environment such as the ocean should be considered. This assumption is valid only for material flow analysis involving plastic components. If we factor in the rest of the MSW that ended up in the landfill, the degradation products cannot be neglected.'], ['Incineration of plastic waste results in ash content equal to 1Fraction of the original volume', 'Determines the exiting solid mass out of incineration', 'Using the average ash density of 2.05 g/cm3, average polymer density of 0.000413367 Tons/cm3, or 0.375 kg/cm3 (calculated in the generic polymer stream tab), we can calculate the ash content generated. The remaining mass has already been converted to a standardized unit of CO2-eq and thus will not appear balanced.'], ['2Fraction of additives migrated during the use phase', 'Stream 5 Additives = Stream 4 Additves * 0.02', 'See the "Migration Data - Use" tab. We have a very limited information on migrated chemicals during the use phase because it is difficult and time-consuming to do individual studies. However, in that tab, we have compiled what we were able to find and averaged/lumped the data into an estimation'], ['0.00047Fraction of polymer/plastic/monomer migrated during use phase', 'Stream 5 Plastic = Stream 4 Plastic * 0.0000047', 'Like the previous assumption, Crompton (2007)’s migration data was used. This value of 0.00047Fraction came from the possibility of PDMS dissolving in oily products. This value is the only contributing factor to polymer migration at this time. More available data will improve the accuracy.'], ['Emissions in unit of Tons CO2 equivalent is not considered part of the mass', 'Emission value excluded from material balance', 'The emissions calculated were based on average endpoint data. The specifics of the identity of the "emission" are unspecified. However, for this study, we assumed that the emissions come from running the process, using substances integral to the operation, and other releases that do not include plastics/additives. Note that Tons of CO2 equivalent are simply a way of standardizing the impacts of different released substances. A higher mass of CO2 equivalent signifies a high environmental impact. Therefore, different chemicals are assigned different values of CO2 equivalency. '], ["Microplastics/Plastic components make up 0.01Fraction of the compost's mass", 'Total plastic content in stream  11 compost = 0.01Fraction w/w compost from stream 11. These plastics joined the material balance on stream 8 (with other nonplastic waste)', 'Plastic-coated products have the potential to contaminate compost. Brinton et al. 2018 tested the content of microplastics in plastic-coated paper products (milk and juice carTons, hot and cold paper drinking cups, frozen food containers, take-out containers, paper plates, and plastic-lined paper bags). During composting, these plastic coatings break down into smaller components (microplastics) rather than succumbing to biodegradation. Unfortunately, these microplastics can produce persistent organic pollutants such as DDT, PCBs, and dioxins. Eventually, these toxic chemicals may find their way into wildlife and the food chain. '], ['The incineration of 1 MT (1.1 US Tons) of MSW releases approximately 0.95 MT CO2-eq (or 1.05 Tons CO2-eq)', 'Emission of nonplastic MSW = 1.05*Mass of nonplastic MSW into incineration', 'A background paper on "Good Practice Guidance and Uncertainty Management in National Greenhouse Gas Inventories" reported that the incineration of 1 MT of MSW releases between 0.7-1.2 MT of CO2. An average value of 0.95 MT was used. '], ['Polymer recovery rate = 66.7-94Fraction', 'Domestic Recycling efficiency = 0.667', 'van Velzen et al. 2017 performed a study on the polymer recovery efficiency via mechanical recycling and determined that the net polymer yields have varied between 66.7 – 94Fraction for a standard recycling process. Some contaminants are partially removed following the same process. Additionally, a recent material recycling facility constructed in Philadelphia has demonstrated a recycling efficiency of 64Fraction. We estimated a 66.7Fraction efficiency for this one iteration. Opportunities for sensitivity analysis are available for this parameter'], ['2Fraction of the additives subjected to mechanical recycling has migrated from the polymer matrix', 'Stream 18 additives = Stream 16 additives * 0.02', 'van Velzen et al. 2017 reported that approximately 1-3Fraction of the recovered polymer mass appeared as dissolved substances that were separated during the polymer wash. Although they were not specific about the identity of the dissolved substances, we can approximate that the dissolved substances are volatile/semi-volatile additives '], ['Additives added to help the polymer processability is lumped into the contamination stream (19). ', 'Contamination stream 19 represents additives from previous processing, the generated degradation products, and additional additives required for processing', 'Horodytska (2020) study focuses on determining chemicals found in recycled plastic after being subjected to mechanical recycling. During recycling, we know that more additives are added to improve processability. However, some of the same additives can migrate out. Therefore, the contamination stream is the "net" mass flow rate of chemicals into recycled plastics. '], ['The contamination/degradation products entering the manufacturing phase are neglected from Stream 4', 'Contaminants and Degradation products in Stream 20 does not get added to Stream 4', "If we account for the contamination/degradation of chemicals from stream 20 (recycled), we will enter a calculation loop. The contaminants/degradation from the plastic's previous life would get added to the next cycle. "], ['Plastic Waste Import/Export - Ethylene = HDPE/LDPE/PET and are evenly split', 'Ethylene values reported as import/export/reexport are divided into two for HDPE, LDPE  estimation. ', 'According to Ma et al. 2020, PET imports account for 40Fraction of the world’s total export. Although variation is expected between countries, using a global average to estimate an unknown Fraction should be reasonable. \n\nTherefore, based on the UN COMTRADE data regarding plastic waste import/export/re-export, we assume that 40Fraction of “Other plastics” are PET and 60Fraction contains other uncategorized plastic wastes. \n'], ['1/3 of Domestically Recycled Plastic is sent to incineration/landfill due to inefficiency problem', 'Stream 23 and Stream 28 contains 1/3 of the wasted plastics sent to domestic recycling. This value is split equally between the two streams for simplification', 'Only 3.9Fraction has been domestically recycled in the United States, while 4.5Fraction has been exported for recycling in 2018. State-of-the-art technology could realistically recover 2/3 of the plastics sent for recycling, leaving 1/3 as waste. This assumption is a "best-case scenario."'], ['Landfill leachate release additive at a 0.001Fraction rate', 'Stream 29 = Plastic Litter + 0.00001*Additive Input', 'Landfill sites in industrialized countries have been known to perform leachate treatments such as aerobic and membrane bioreactors to reduce the BPA concentration to 0.11 – 30 μg/L. Without proper leachate treatment, plastic additives and BPA could be released into the environment and contaminate the nearby water supply. The rate of leachate release has been estimated to vary between 20 – 30Fraction of the wastes placed in the landfill 23. Our generic scenario holds that over 146 million Tons of waste have been sent for landfilling in 2018, with each landfill receiving on average 55,000 Tons of MSW/day. The potential leachate generated from landfills may approach 29.2 – 43.8 million Tons/yr, or 11,000 – 16,500 Tons/(yr·site). For a given site, the estimated yearly chemical additive release through leachate equates to 0.11 – 0.165 Tons/(yr·site) (0.001Fraction additive in leachate).']]

#Creates list of textboxes for assumptions (1 assumption per box)
assumptionText1 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText2 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText3 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText4 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText5 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText6 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText7 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText8 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText9 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText10 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText11 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText12 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText13 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText14 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText15 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText16 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText17 = tk.Text(assumptionsFrame, bd = 0, width = 45)
assumptionText18 = tk.Text(assumptionsFrame, bd = 0, width = 45)

#Creates list of assumptions text boxes
assumptionTextList = [assumptionText1, assumptionText2, assumptionText3, assumptionText4, assumptionText5, assumptionText6,
                      assumptionText7, assumptionText8, assumptionText9, assumptionText10, assumptionText11, assumptionText12,
                      assumptionText13, assumptionText14, assumptionText15, assumptionText16, assumptionText17, assumptionText18]

#creates effect textboxes
effectText1 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText2 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText3 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText4 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText5 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText6 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText7 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText8 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText9 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText10 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText11 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText12 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText13 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText14 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText15 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText16 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText17 = tk.Text(assumptionsFrame, bd = 0, width = 45)
effectText18 = tk.Text(assumptionsFrame, bd = 0, width = 45)

#creates list of effect textboxes

effectTextList = [effectText1, effectText2, effectText3, effectText4, effectText5, effectText6,
                  effectText7, effectText8, effectText9, effectText10, effectText11, effectText12,
                  effectText13, effectText14, effectText15, effectText16, effectText17, effectText18]

#creates justification textboxes

justificationText1 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText2 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText3 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText4 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText5 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText6 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText7 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText8 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText9 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText10 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText11 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText12 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText13 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText14 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText15 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText16 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText17 = tk.Text(assumptionsFrame, bd = 0, width = 45)
justificationText18 = tk.Text(assumptionsFrame, bd = 0, width = 45)

#creates list of justification textboxes

justificationTextList = [justificationText1, justificationText2, justificationText3, justificationText4, justificationText5, justificationText6,
                         justificationText7, justificationText8, justificationText9, justificationText10, justificationText11, justificationText12,
                         justificationText13, justificationText14, justificationText15, justificationText16, justificationText17, justificationText18]

#Grids assumption, effect, and justification textboxes
assumpRow = 1
for i in range(18):
    assumptionTextList[i].grid(column = 0, row = assumpRow)
    assumptionTextList[i].config(font=("Helvetica 14 bold"))
    assumptionTextList[i].insert(tk.INSERT, assumptions[i][0])
    assumptionTextList[i].tag_configure('center', justify = "center")
    assumptionTextList[i].tag_add('center', 1.0, 'end')
    
    effectTextList[i].grid(column = 1, row = assumpRow)
    effectTextList[i].config(font=("Helvetica 14 bold"))
    effectTextList[i].insert(tk.INSERT, assumptions[i][1])
    effectTextList[i].tag_configure('center', justify = "center")
    effectTextList[i].tag_add('center', 1.0, 'end')
    
    justificationTextList[i].grid(column = 2, row = assumpRow)
    justificationTextList[i].config(font=("Helvetica 14 bold"))
    justificationTextList[i].insert(tk.INSERT, assumptions[i][2])
    justificationTextList[i].tag_configure('center', justify = "center")
    justificationTextList[i].tag_add('center', 1.0, 'end')
    
    assumpRow+=1
    
allAssumpTexts = justificationTextList + assumptionTextList + effectTextList

#Configures textboxes to prevent editing
for i in allAssumpTexts:
    i.config(state = 'disabled')
    
##### Chemical Additives data base

#Creates and configures title text box
chemicalAdditivesTitle = tk.Text(my_frame6, bd = 0, width = 45, height = 3)
chemicalAdditivesTitle.config(font = ('Helvetica 20 bold'))
chemicalAdditivesTitle.tag_configure('center', justify = CENTER)
chemicalAdditivesTitle.tag_add('center', 1.0, 'end')
chemicalAdditivesTitle.pack()
chemicalAdditivesTitle.insert(tk.INSERT, "Chemical Additives Database")
chemicalAdditivesTitle.config(state = 'disabled')

#Creates list of chemical additives, one list per row
chemicalAdditivesList = [['1 ', 'Boric acid', 'Hydrogen borate, boracic acid, orthoboric acid', 'Flame Retardant', '61.83', 'odorless white solid'], ['2 ', 'Brominated Flame Retardants', 'PBDE', 'Flame Retardant', '1366.9', 'Solids, liquid'], ['3 ', 'Tris(2-chloroethyl)phosphate', 'TCEP', 'Flame Retardant', '285.5', 'odorless clear liquid'], ['4 ', 'Tris(2-chlorisopropyl)phosphate', 'TCPP', 'Flame Retardant', '288.5', 'clear colorless viscous liquid'], ['5 ', 'Hexabromocyclohexane', 'HBCDD', 'Flame Retardant', '557.5', 'White, beige powder'], ['6 ', "4,4'-dioctyldiphenylamine", 'Vanox 1081', 'Antioxidant', '393.7', 'colorless solid'], ['7 ', 'Octylated diphenylamines', 'Permanax OD', 'Antioxidant', '393.7', 'beige sticks'], ['8 ', "N,N'-di-s-butyl-p-phenylenediamine", 'HiTEC 4720 (ethyl Antixodant PDA)', 'Antioxidant', '220.4', 'red, clear liquid'], ['9 ', "N,N'-di(1,4-dimethylpentyl)-p-phenylenediamine", 'Vulkanox 4030', 'Antioxidant', '304.5', 'dark-red, low viscous liquid'], ['10 ', "N,N'-di(i-octyl)-p-phenylenediamine", 'Antozite 1', 'Antioxidant', '332.6', 'liquid'], ['11 ', "N-2-propyl-N'phenyl-p-phenylenediamine", 'Permanax IPPD', 'Antioxidant', '226.2', 'brown rods'], ['12 ', "N-(1,3-dimethylbutyl)-N'-phenyl-p-phenylenediamine", 'Vulkanox 4020', 'Antioxidant', '268.4', 'brown to violet solid'], ['13 ', "N-(1,3-dimethylbutyl)-and N-(1,4-dimethylpentyl)-N'-phenyl-p-phenylenediamine (1:1)", 'Vulkanox 4022', 'Antioxidant', '304.5', 'Dark brown low-viscous iquid'], ['14 ', "N,N'diphenyl-p-phenylenediamine", 'Permanax DPPD', 'Antioxidant', '260.3', 'dark-grey solid'], ['15 ', 'N-phenyl-N-1-naphthylamine', 'Vulkanox P (ASM PAN)', 'Antioxidant', '219.2', 'violet solid'], ['16 ', 'N-phenyl-2-naphthylamine', 'Vulkanox PBN', 'Antioxidant', '219.2', 'violet to brown solid'], ['17 ', "N,N' -di(2-naphthyl)-p-phenylenediamine", 'Age Rite White', 'Antioxidant', '360.4', 'colorless solid'], ['18 ', 'polymer 2,2,4-trimethyl-l,2-dihydroquinoline', 'Vulkanox HS/Pulver', 'Antioxidant', '173.25', 'yellow to amber-colored solid'], ['19 ', 'acetone diphenylamine condensation product', 'Permanax BL', 'Antioxidant', '227.3', 'Black, clear, viscous liquid'], ['20 ', 'acetone-diphenylamine condensation product on Si02', 'Permanax BWL', 'Antioxidant', '227.3', 'Black solid'], ['21 ', '6-ethoxy-2,2,4-trimethyl-l,2-dihydroquinoline', 'Santoflex AW', 'Antioxidant', '217.3', 'Liquid'], ['22 ', 'bis(2,6-di-i-propylphenyl)carbodiimide', 'Stabaxol I', 'Antioxidant', '362.5', 'colorless solid'], ['23 ', 'N-dibutyldithiocarbamate', 'NBC', 'Antioxidant', '467.4', 'green solid'], ['24 ', 'Hydroquinone', 'Hydroquinone Inhibtor Grade', 'Antioxidant', '110.1', 'Colorless solid'], ['25 ', '2,6-di-t-butylphenol', 'Ethyl 701, HiTEC 4701', 'Antioxidant', '206.3', 'Pale-straw, crystalline solid'], ['26 ', '2,6-di-t-butyl-4-methylphenol', 'Lowinox BHT', 'Antioxidant', '220.4', 'colorless solid'], ['27 ', '2,6-di-t-butyl-4-s-butylphenol', 'Vanox 1320', 'Antioxidant', '262.4', 'straw to light-amber, clear liquid'], ['28 ', '2,4-dimethyl-6-(0-methylcyclohexyl)phenol', 'Permanax WSL', 'Antioxidant', '218.3', 'yellowish, clear liquid'], ['29 ', 'mixture of alkylated phenols', 'HiTEC 4733, Ethanox 733', 'Antioxidant', 'Unknown', 'liquid'], ['30 ', 'Styrenated phenol', 'Montaclere', 'Antioxidant', '322 - 367', 'yellowish to amber-colored liquid'], ['31 ', 't-butylhydroquinone', 'Eastman MTBHQ', 'Antioxidant', '166.2', 'colorless solid'], ['32 ', '2,5-di-t-butylhydroquinone', 'Eastman DTBHQ', 'Antioxidant', '222.3', 'colorless to tan crystal'], ['33 ', '2,5-di-t-pentylhydroquinone', 'Santovar A', 'Antioxidant', '250.4', 'yellowish to grey-white solid'], ['34 ', '2,6-di-t-pentylhydroquinone', 'Lowinox AH 25', 'Antioxidant', '250.4', 'grey solid'], ['35 ', "2,2'-methylene-bis(6-t-butyl-4-methylphenol)", 'Irganox 2246', 'Antioxidant', '340.5', 'colorless, crystalline solid'], ['36 ', "2,2' -ethylidene-bis( 4,6-di-t-butylphenol)", 'Vanox 1290', 'Antioxidant', '438.7', 'colorless solid'], ['37 ', "2,2'-methylene-bis( 4-methyl-6-cyclohexylphenol)", 'Vulkanox ZKF, ASM ZKF', 'Antioxidant', '392.4', 'white solid'], ['38 ', "2,2'-methylene-bis( 4-methyl-6-(0-methylcyclohexyl)phenol)", 'Permanax WSP', 'Antioxidant', '420.6', 'yellowish solid'], ['39 ', "4,4'-methylene-bis(2-t-butylphenol)", 'Vulkanox NKF', 'Antioxidant', '312.4', 'white solid'], ['40 ', "4,4'-methylene-bis(2,6-di-t-butylphenol)", 'Ethanox 702', 'Antioxidant', '424.7', 'light-straw, crystalline solid'], ['41 ', "4,4'-methylene-bis(2,6-di-t-butylphenol)", 'CeMox 02 NP, Antioxidant 702 ND', 'Antioxidant', '424.7', 'yellow solid'], ['42 ', "2,2'-i-butylidene-bis(4,6-dimethylphenol)", 'Lowinox 22 IB 46', 'Antioxidant', '298.4', 'colorless solid'], ['43 ', "4,4' -butylidene-bis( 6-t-butyl-3-methylphenol)", 'Santowhite Powder', 'Antioxidant', '382.6', 'colorless solid'], ['44 ', 'bis( 4-hydroxyphenyl) -2-propane', 'Bisphenol A', 'Antioxidant', '228.3', 'colorless crystal'], ['45 ', 'mixture of polybutylated bisphenol A', 'Agerite Superlite', 'Antioxidant', '340.5', 'liquid'], ['46 ', "2,2'-(octahydro-4,7-methano-1H-indenediyl)-bis( 6-t-butyl-4-methylphenol)", 'Lowinox CPL', 'Antioxidant', '456.7', 'colorless solid'], ['47 ', '1,1,3-tris(2-methyl-4-hydroxy-5-t-butylphenyl)butane', 'Topanol CA', 'Antioxidant', '544.7', 'colorless solid'], ['48 ', '1,3,5-trim ethyl-2,4,6- tris( 3,5-di -t-butyl-4-hydroxybenzyl) benzene', 'Ethanox 330', 'Antioxidant', '775.2', 'colorless crystalline solid'], ['49 ', '1,3,5-trimethyl-2,4,6-tris(3,5-di-t-butyl-4-hydroxybenzyl)benzene', 'Irganox 1330', 'Antioxidant', '775.2', 'colorless to yellowish, crystalline solid'], ['50 ', "4,4' -dihydroxybiphenyl, 4,4' -biphenol", 'ASM DOD', 'Antioxidant', '186.2', 'colorless solid'], ['51 ', 'hydroquinone monomethylether, 4-hydroxyanisole', 'Eastman HQMME', 'Antioxidant', '124.1', 'colorless flakes'], ['52 ', 'hydroquinone-bis(2-hydroxyethyl)ether', 'Eastman HQEE', 'Antioxidant', '198.2', 'colorless flakes'], ['53 ', 'β-(3,5-di-t-butyl-4-hydroxyphenyl)propionic octadecyl ester', 'Irganox 1076', 'Antioxidant', '530.9', 'colorless solid'], ['54 ', 'β-(3,5-di-t-butyl-4-hydroxyphenyl)propionic octadecyl ester', 'Lowinox PO 35', 'Antioxidant', '530.9', 'colorless solid'], ['55 ', '3,4,5-trihydroxybenzoic acid propyl ester (propyl gallate)', 'Tenox PG', 'Antioxidant', '212.2', 'colorless solid'], ['56 ', 'triethyleneglycol-bis-3-(3-t-butyl-4-hydroxy-5-methylphenyl)propionate', 'Irganox 245', 'Antioxidant', '586.8', 'colorless solid'], ['57 ', '3,3-bis( 4-hydroxy-3-t-butylphenyl)ethylene butyrate', 'Hostanox O 3', 'Antioxidant', '795.1', 'colorless solid'], ['58 ', 'pentaerythrityl-tetrakis(3-(3,5-di-t-butyl-4-hydroxyphenyl)propionate)', 'Lowinox PP 35', 'Antioxidant', '1178', 'slightly yellowish solid'], ['59 ', 'pentaerythrityl-tetrakis(3-(3,5-di-t-butyl-4-hydroxyphenyl)propionate)', 'Irganox 1010', 'Antioxidant', '1178', 'colorless solid'], ['60 ', '2,6-di-t-butyl-4-dimethylaminomethylphenol', 'Ethanox 703', 'Antioxidant', '263.4', 'pale-yellow, crystalline solid'], ['61 ', "N,N'-bis(3(3',5'-di-t-butyl-4'-hydroxyphenyl) propionyl)hydrazine", 'Irganox MD 1024', 'Antioxidant', '552.8', 'colorless solid'], ['62 ', "N ,N' -hexamethylene-bis( 3,5-di -t-butyl-4-hydroxyhydrocinnamide)", 'Irganox 1098', 'Antioxidant', '588.9', 'colorless solid'], ['63 ', 'tris( 3,5-di -t -butyl-4-hydroxybenzyl)isocyanurate', 'Irganox 3114', 'Antioxidant', '784.1', 'colorless to slightly yellowish solid'], ['64 ', '2-methyl-4,6-bis( octylthiomethyl)phenol', 'Irganox 1520', 'Antioxidant', '424.8', 'pale yellow, low-viscous, free-flowing liquid'], ['65 ', "2,2'-thio-bis(6-t-butyl-4-methylphenol)", 'Irganox 1081', 'Antioxidant', '358.5', 'colorless crystalline solid'], ['66 ', "4,4'-thio-bis(2-t-butyl-5-methylphenol)", 'Irganox 415', 'Antioxidant', '358.5', 'colorless solid'], ['67 ', "4,4'-thio-bis(6-t-butyl-2-methylphenol)", 'Ethanox 322 Antioxidant', 'Antioxidant', '358.5', 'white to yellow-straw, crystalline solid'], ['68 ', "2,2' -thiodiethyl-bis(3-(3,5-di-t-butyl-4-hydroxyphenyl)propionate", 'Irganox 1035', 'Antioxidant', '642.9', 'colorless solid'], ['69 ', 'Nonylphenoldisulfide oligomer', 'Ethanox 323', 'Antioxidant', 'Unknown', 'liquid'], ['70 ', '2,4-bis(octylthio)-6-(4-hydroxy-3,5-di-t-butylanilino)-1,3,5-triazine', 'Irganox 565', 'Antioxidant', '588.9', 'colorless solid'], ['71 ', '3,5-di-t-butyl-4-hydroxybenzylphosphonic acid diethylester', 'Irganox 1222', 'Antioxidant', '356.4', 'colorless solid'], ['72 ', "tris( 4,4' -thio-bis( 2- t-butyl-5-methylphenol) )phosphite", 'Hostanox VP OSP 1', 'Antioxidant', '1105', 'colorless solid'], ['73 ', 'dioctadecyldisulfide', 'Hostanox SE 10', 'Antioxidant', '571.1', 'colorless solid'], ['74 ', 'thiodistearylpropionate', 'Hostanox VP SE 2', 'Antioxidant', '683.2', 'colorless solid'], ['75 ', 'i-octyldiphenylphosphite', 'Weston ODPP', 'Antioxidant', '346.4', 'colorless, clear liquid'], ['76 ', 'tris(nonylphenyl)phosphite', 'Western TNPP', 'Antioxidant', '689', 'yellow, clear liquid'], ['77 ', 'bis(2,4-di -t-butylphenyl)pentaerythritoldiphosphite', 'Ultranox', 'Antioxidant', '604.7', 'colorless solid'], ['78 ', 'triphenylphosphite', 'Western TPP', 'Antioxidant', '310.3', 'colorless, clear liquid'], ['79 ', "β,β'-thiodilaurylpropionate", 'Hostanox SE 10', 'Antioxidant', '514.9', 'colorless solid'], ['80 ', "dimyristyl-3,3'-thiodipropionate", 'Irganox PS 801', 'Antioxidant', '571', 'colorless crystals'], ['81 ', "3,3'-thio-bis( stearyldipropionate)", 'Lowinox DSTDP', 'Antioxidant', '683.2', 'colorless flakes'], ['82 ', 'Zn 2-benzimidazole ethiolate', 'Vulkanox ZMB 2', 'Antioxidant', '363.6', 'colorless solid'], ['83 ', '4- or 5-methylmercaptobenzimidazole', 'Vulkanox MB2/MG', 'Antioxidant', '164.2', 'yellowish-white solid'], ['84 ', '2 basic Pb carbonate', '2-bas, Bleicarbonat', 'Stabilizer', '780', 'colorless solid'], ['85 ', '2-basic Pb phosphite', 'Zweibasisches Blei-Phosphit', 'Stabilizer', '289', 'colorless solid'], ['86 ', '2-basic Pb phosphite complex', 'Baerostab E 502 FP', 'Stabilizer', '1480', 'colorless granules'], ['87 ', '2-basic Pb phosphite -sulfite complex', 'Sulfofos C', 'Stabilizer', 'Unknown', 'Colorless solid'], ['88 ', 'coprecipitate based on Pb phosphite-carboxylate', 'Interstab LF 3638', 'Stabilizer', 'Unknown', 'cream-colored flakes'], ['89 ', 'Pb phosphite-sulfite-carbonate complex', 'Naftovin T 82', 'Stabilizer', 'Unknown', 'colorless solid'], ['90 ', 'coprecipitate based on Ba Ca complex and 2-basic lead phosphite (1:1)', 'Interstab LT 3631/3', 'Stabilizer', 'Unknown', 'cream-colored solid'], ['91 ', 'basic Pb phosphite carboxylate', 'Baeropan MC 380 FP', 'Stabilizer', 'Unknown', 'colorless solid'], ['92 ', '3-basic Pb sulfate', 'Baerostab V 220 MC', 'Stabilizer', '970', 'colorless solid'], ['93 ', '4-basic Pb sulfate', 'Interstab LP 3104', 'Stabilizer', '1200', 'colorless solid'], ['94 ', 'coprecipitate based on Pb sulfate-carboxylate', 'Interstab LP 3636', 'Stabilizer', 'Unknown', 'cream-colored solid'], ['95 ', 'coprecipitate based on Pb sulfate-carboxylate', 'Interstab LT 3679', 'Stabilizer', 'Unknown', 'cream-colored solid'], ['96 ', 'coprecipitate based on Pb sulfate-phosphite-carboxylate', 'Interstab LF 3734', 'Stabilizer', 'Unknown', 'cream-colored granules'], ['97 ', 'epoxidized octanoic ester', 'Plastepon 451', 'Stabilizer', 'Unknown', 'light-yellow, clear liquid'], ['98 ', 'epoxidized soybean oil', 'Baerostab LSU', 'Stabilizer', '975', 'colorless, clear liquid'], ['99 ', 'epoxidized soybean oil', 'Reoplast 39', 'Stabilizer', '975', 'yellowish, clear liquid'], ['100 ', 'dilaurylthiodipropionate', 'Dilaurylthiodipropionat', 'Stabilizer', '514.9', 'colorless solid'], ['101 ', 'di( tridecyl)thiopropionate', 'Ditridecylthiopropionat', 'Stabilizer', '542.9', 'colorless, clear liquid'], ['102 ', 'thiodiethyleneglycol-~-aminocrotonic acid ester with Ca and Zn stearate', 'Irgastab A 80', 'Stabilizer', 'Unknown', 'yellowish solid'], ['103 ', "N,N'-diphenylthiourea", 'Diphenylthioharnstoff', 'Stabilizer', '228.3', 'colorless solid'], ['104 ', 'Zn octoate', 'Baerostab L 230', 'Stabilizer', '351.8', 'slightly yellowish, clear liquid'], ['105 ', 'Zn complex', 'Interstab M 823', 'Stabilizer', 'Unknown', 'pale-yellowish, clear viscous liquid'], ['106 ', 'Ba laurate', 'Barium-Laurat', 'Stabilizer', '536', 'colorless solid'], ['107 ', 'Cd laurate', 'Cadmium-Laurat', 'Stabilizer', '511', 'colorless solid'], ['108 ', 'Li stearate', 'Lithium-stearat', 'Stabilizer', '291.4', 'colorless solid'], ['109 ', 'Na stearate', 'Natrium-Stearat', 'Stabilizer', '307.5', 'colorless solid'], ['110 ', 'Mg stearate', 'Magnesium-stearat', 'Stabilizer', '591.3', 'colorless solid'], ['111 ', 'Ca stearate', 'Calcium Stearate IT', 'Stabilizer', '607', 'colorless solid'], ['112 ', 'Ba stearate', 'Barium-stearat', 'Stabilizer', '704.2', 'colorless solid'], ['113 ', 'Zn stearate', 'Zink-stabilisator LF', 'Stabilizer', '623.2', 'colorless solid'], ['114 ', 'Cd stearate', 'Naftowin BM 16', 'Stabilizer', '679.4', 'colorless solid'], ['115 ', 'Pb stearate', 'Interstab LP 3155', 'Stabilizer', '774.2', 'cream-coloreed solid'], ['116 ', '2-basic Pb stearate', 'Zweibasisches Blei-Stearat', 'Stabilizer', '1221', 'colorless solid'], ['117 ', 'basic Pb carboxylate + CaC03', 'Baeropan SMS 314', 'Stabilizer', 'Unknown', 'light-brown flakes'], ['118 ', 'basic Pb complex with ester, carboxylate and phosphite groups', 'Baeropan MC 2567 SL', 'Stabilizer', 'Unknown', 'colorless solid'], ['119 ', 'coprecipitate Pb-carboxylate + PbS04+CaC03', 'Baeropan 2028 SP', 'Stabilizer', 'Unknown', 'colorless solid'], ['120 ', '2-basic Pb phthalate', 'Interstab PDP-E', 'Stabilizer', '817.8', 'colorless solid'], ['121 ', '2-basic Pb phthalate with fatty acid carboxylate', 'Baerostab E 503', 'Stabilizer', '817.8', 'colorless granules'], ['122 ', 'Pb salicylate', 'Nafovin T 50', 'Stabilizer', '343.3', 'colorless, fine-crystalline solid'], ['123 ', 'dibutyltin dilaurate', 'Meister Z 4101', 'Stabilizer', '631.6', 'slightly yellowish , clear liquid'], ['124 ', 'dibutyltin maleate', 'Meister DBTM', 'Stabilizer', '347', 'colorless solid'], ['125 ', 'dibutyltin maleic ester carboxylate', 'Stanclere T 85;', 'Stabilizer', '349.05', 'colorless, clear-liquid'], ['nan', 'nan', 'Stanclere T 57;', 'nan', 'nan', 'nan'], ['nan', 'nan', 'Stanclere T 85', 'nan', 'nan', 'nan'], ['126 ', 'dibutyltin thioglycolate', 'Hostastab Sn S 61', 'Stabilizer', '323.04', 'colorless, clear liquid'], ['127 ', 'dibutyItin thioglycoIic acid 2-ethylhexylester mercaptide', 'Stanclere T 160', 'Stabilizer', '607.5', 'colorless, clear liquid'], ['128 ', 'dibutyltin thioglycolic acid 2-ethylhexylester mercaptide', 'Stanclere T 161', 'Stabilizer', '607.5', 'colorless, clear liquid'], ['129 ', 'dioctyltin thioglycolic alkylester mercaptide', 'Hostastab Sn S 15', 'Stabilizer', '438.16', 'colorless, clear liquid'], ['nan', 'nan', 'Stanclere T 484', 'nan', 'nan', 'nan'], ['130 ', 'dibutyltin mercaptopropionate', 'Stanclere T 186', 'Stabilizer', '337.1', 'colorless solid'], ['131 ', 'K Zn complex', 'Interstab M 731', 'Stabilizer', 'Unknown', 'amber-colored, clear liquid'], ['132 ', 'Ca Zn complex', 'Baerostab NT 1 S', 'Stabilizer', 'Unknown', 'colorless solid'], ['133 ', 'Ca Sn complex', 'Baeropan SN 200', 'Stabilizer', 'Unknown', 'colorless solid'], ['134 ', 'Ba Zn complex', 'Baerostab OE 666', 'Stabilizer', 'Unknown', 'colorless solid'], ['135 ', 'Ba Zn complex', 'Swedstab 504', 'Stabilizer', 'Unknown', 'colorless, clear liquid'], ['136 ', 'Ba Zn complex', 'Naftovin BZ 580', 'Stabilizer', 'Unknown', 'yellow, clear liquid'], ['137 ', 'Ba Cd complex', 'Baerostab ZPS-F', 'Stabilizer', 'Unknown', 'colorless solid'], ['138 ', 'Ba Cd complex', 'Baerostab PC 52', 'Stabilizer', 'Unknown', 'colorless solid'], ['139 ', 'Zn Mg complex', 'Naftovin CKP 90030', 'Stabilizer', 'Unknown', 'colorless solid'], ['140 ', 'Zn Mg complex', 'Naftovin CKP 90172', 'Stabilizer', 'Unknown', 'colorless solid'], ['141 ', 'Pb Ba Cd-phosphite carboxylate', 'Baeropan 16435 FP', 'Stabilizer/Lubricant', 'Unknown', 'colorless solid'], ['142 ', 'Ca Zn ester carboxylate', 'Irgastab CZ 110', 'Stabilizer', 'Unknown', 'yellowish-white, high viscous paste'], ['143 ', 'Ca Zn ester carboxylate', 'Stabiol VCZ 1616', 'Stabilizer', 'Unknown', 'colorless solid'], ['144 ', 'Ca Zn ester carboxylate', 'Baeropan NT 328 FLA', 'Stabilizer/Lubricant', 'Unknown', 'colorless solid'], ['145 ', 'Ba Zn ester carboxylate', 'Swedstab 502', 'Stabilizer', 'Unknown', 'colorless, clear liquid'], ['146 ', 'Ba Ca soap complex', 'Reagens F/95', 'Stabilizer', 'Unknown', 'colorless solid'], ['147 ', 'Ba Cd soap complex with epoxester', 'Reagens G1/52', 'Stabilizer/Lubricant', 'Unknown', 'Brown, clear liquid'], ['148 ', 'Pb Ba Cd compound with phosphite and carboxylate groups', 'Baeropan 16511 FP', 'Stabilizer/Lubricant', 'Unknown', 'colorless solid'], ['149 ', 'tri-iso-decylphosphite', 'Weston TDP', 'Stabilizer', '502.8', 'colorless, clear liquid'], ['150 ', 'tri(tridecyl)phosphite', 'Tritridecylphosphit', 'Stabilizer/Antioxidant', '629', 'colorless, clear liquid'], ['151 ', 'distearylpentaerythrityldiphosphite', 'Weston 619 F', 'Stabilizer', '733.1', 'colorless solid'], ['152 ', 'tri( dipropyleneglycol)phosphite', 'Weston 430', 'Stabilizer', '396.5', 'colorless, clear liquid'], ['153 ', 'di-i-decylphenyl phosphite', 'Irgastab CH 300', 'Stabilizer', '438.6', 'colorless, clear liquid'], ['154 ', 'phenyldidecylphosphite', 'Weston PDDP', 'Stabilizer', '438.6', 'colorless, clear liquid'], ['155 ', 'i-decyldiphenyl phosphite', 'Irgastab CH 301', 'Stabilizer', '374.5', 'colorless, clear liquid'], ['156 ', "4,4' -i-propylidenediphenol-alkylphosphite", 'Weston 439', 'Stabilizer', 'Unknown', 'colorless, clear liquid'], ['157 ', "2,2'-ethylene-bis( 4,6-di-t-butylphenyl)fluorophosphite", 'Ethanox 398', 'Stabilizer/Antioxidant', '486.7', 'white, crystalline solid'], ['158 ', 'bis(2,4-di-t -butylphenyl)pentaerythrityldiphosphite', 'Ultranox  626', 'Stabilizer', '604.7', 'colorless solid'], ['159 ', 'tris(nonylphenyl)phosphite', 'Baerostab CWM 35', 'Stabilizer', '689', 'colorless, clear liquid'], ['160 ', 'Octylphenol', '4-Octylphenol', 'Stabilizer (antioxidant/UV)', '206.32', 'White flakes'], ['161 ', '1,3,5-Tris(oxiran-2-ylmethyl)-1,3,5-triazinane-2,4,6-trione', 'TGIC', 'Stabilizer (antioxidant/UV)', '297.3', 'White powder'], ['162 ', '1,3,5-tris[(2S and 2R)-2,3-epoxypropyl)-1,3,5-triazine-2,4,6-(1H,3H,5H)-trione', 'β-TGIC', 'Stabilizer (antioxidant/UV)', '297.26', 'White powder'], ['163 ', 'Butylated hydroxyltoluene', 'BHT', 'Stabilizer (antioxidant/UV)', '220.35', 'White to yellow powder'], ['164 ', '2- and 3-t-butyl-4 hydroxyanisole', 'BHA', 'Stabilizer (antioxidant/UV)', '180.24', 'White-yellow waxy solid'], ['165 ', 'Tris-nonyl-phenyl phosphate', 'TNPP', 'Stabilizer (antioxidant/UV)', '705', 'Colorless liquid'], ['166 ', 'Tris(2,4-di-tert-butylphenyl) phosphite', 'Irgasfos 168', 'Stabilizer (antioxidant/UV)', '646.92', 'White solid'], ['167 ', 'Cadmium compounds', 'Cadmium sulfide, cadmium sulfoselenide, cadmium ', 'Heat stabilizer/Pigments', 'Unknown', 'Unknown'], ['168 ', 'Lead compounds (Lead, Lead oxide)', 'nan', 'Heat stabilizer', 'Unknown', 'Unknown'], ['169 ', 'Barium and calcium salts', 'nan', 'Heat stabilizer', 'Unknown', 'Unknown'], ['170 ', 'tris(2,4-di-t-butylphenol)phosphite', 'Hostanox PAR 24', 'Stabilizer/Antioxidant', '646.9', 'colorless solid'], ['171 ', 'triphenylphosphite', 'Irgastab CH 55', 'Stabilizer', '310.3', 'colorless, clear liquid'], ['172 ', 'Pb phosphite-carboxylate on CaC03', 'Baeropan E-RL 25', 'Stabilizer/Lubricant', 'Unknown', 'colorless granules'], ['173 ', 'Pb phosphite-carboxylate with aliphatic ester', 'Baeropan E-RL 15', 'Stabilizer/Lubricant', 'Unknown', 'colorless granules'], ['174 ', 'vinyl-functional poly( dimethylsiloxane) with filler', 'Hitzestabilsator H1 Rot', 'Heat stabilizer', 'Unknown', 'red-brown paste'], ['175 ', 'sterically hindered amine, HALS', 'Hostavin  N 20', 'Light stabilizer', 'Unknown', 'colorless solid'], ['176 ', 'poly( bis(2,2,6,6-tetramethyl-4-piperidinylimino )-1,6-hexanediyl-alt-4-t-octylamino-l,3,5-triazine-2,4-diyl)', 'Chimassorb 944 FL', 'UV stabilizer', 'Unknown', 'light-yellow granules, low dusting'], ['nan', 'hexanediyl-alt-4-t-octylamino-l,3,5-triazine-2,4-diyl)', 'nan', 'nan', 'nan', 'nan'], ['177 ', '2-(2-hydroxy-5-methylphenyl)-2H-benzotriazole', 'Tinuvin P', 'Light Stabilizer', '225.2', 'slightly yellowish solid '], ['178 ', "2-(2' -hydroxy-3' -t-butyl-5'-methylphenyl)-5-chlorobenzotriazole", 'Tinuvin 326', 'UV stabilizer', '315.7', 'pale yellow solid'], ['179 ', "2-(2' -hydroxy-3' -dodecyl-5' -methylphenyl)b enzotriazole", 'Tinuvin 571', 'UV stabilizer', '393.6', 'pale yellow liquid'], ['180 ', ',6-hexanediol-bis-3-(3-benzotriazole-4-hydroxy-5-t-butyl)propionate', 'Tinuvin 840', 'UV stabilizer', '760.9', 'slightly yellowish solid'], ['181 ', 'alkylphenolic benzotriazole derivative', 'Tinuvin 234', 'Light stabilizer', 'Unknown', 'yellowish solid'], ['182 ', '2-hydroxy-4-methoxybenzophenone', 'UV 325', 'UV stabilizer', '228.3', 'yellowish solid'], ['183 ', '2-hydroxy-4-octoxybenzophenone', 'Hostavin ARO 8', 'Light stabilizer', '326.4', 'light-yellow , crystalline solid'], ['184 ', 'resorcinol monobenzoate', 'Eastman RMB', 'UV stabilizer', '214.2', 'colorless, crystalline solid'], ['185 ', 'cyanoacrylate derivative', 'UV 340', 'UV stabilizer', '438.7', 'Colorless solid'], ['186 ', "2-ethoxy-2' -ethyloxalyldianilide", 'Baerostab B 200 P', 'UV Stabilizer', '312.4', 'Colorless solid'], ['187 ', "2,2'-thio-bis(4-t-octylphenolato )butylamine, Ni-salt", 'Chimassorb N-705', 'UV stabilizer', '572.5', 'Light-green solid'], ['188 ', '3,5-di-t-butyl-4-hydroxybenzyl phosphonic acid monoethylester, Ni-salt', 'Irgastab 2002', 'Stabilizer', '713.5', 'pale-yellow to green solid'], ['189 ', 'mixture of higher paraffin hydrocarbons and microwaxes, contains some NH (fatty amine)', 'Antilux 610', 'Light stabilizer', 'Unknown', 'Yellowish wax'], ['190 ', 'poly( oxyalkylene)-polysiloxane blockcopolymer', 'Tegostab B 1048', 'Foam Stabilizer', 'Unknown', 'yellowish, clear liquid'], ['191 ', 'mixture of polyether-modified polysiloxane and surfactant', 'Tegostab B 5055', 'Foam Stabilizer', 'Unknown', 'yellowish, clear liquid'], ['192 ', 'poly( oxyalkylene)-polysiloxane blockcopolymer', 'Tegostab B 1400 A', 'Foam Stabilizer', 'Unknown', 'yellowish, clear liquid'], ['193 ', 'poly( oxypropylene)-b-poly( dimethylsiloxane)', 'Tegostab B 8680', 'Foam Stabilizer', 'Unknown', 'colorless, clear liquid'], ['194 ', 'poly( oxypropylene )-b-poly( dimethylsiloxane)', 'Tegostab B 1651', 'Stabilizer', 'Unknown', 'colorless, clear liquid'], ['195 ', 'poly(oxypropylene)-b-poly(oxyethylene)-bpoly(dimethylsiloxane)', 'Tegostab B 2219', 'Foam Stabilizer', 'Unknown', 'colorless, clear liquid'], ['196 ', 'po1y( oxyethylene)-b-poly( oxypropylene)-bpoly(dimethylsiloxane)', 'Tegostab B 8425', 'Foam Stabilizer', 'Unknown', 'Clear, amber liquid'], ['197 ', 'mixture ofhigh-MW paraffins, contains some NH (fatty amine)', 'Antilux 654', 'Antioxidant/Antiozonant', 'Unknown', 'White to light-yellow wax'], ['198 ', 'mixture of higher paraffin hydrocarbons and microwaxes, contains some ester and NH (fatty amine)', 'Antilux 750', 'Light stabilizer', 'Unknown', 'yellowish wax'], ['199 ', 'long-chain aliphatic hindered amine (HALS)', 'Antilux 550', 'UV Stabilizer', 'Unknown', 'Yellowish wax'], ['200 ', 'Antimony(III) Oxide', 'Antimontrioxid Typ Blue', 'Flame Retardant', '291.52', 'Solid'], ['201 ', 'antimony(III) chloride', 'Antimony butter', 'Flame Retardant', '228.1', 'soft, hygroscopic mass'], ['202 ', 'Ammonium polyphosphate', 'Exolit VP IFR 23', 'Flame Retardant', '97.01', 'White powder'], ['203 ', 'Sb2O 3 with mineral oil', 'Antiflamm 90/10', 'Flame Retardant', 'Unknown', 'Colorless solid'], ['204 ', 'Sb2O 3 with chlorinated phosphoric acid ester', 'Firex 5718', 'Flame Retardant', 'Unknown', 'white sediment (with dispersant)'], ['205 ', 'K antimonate', 'potassium antimony(III) oxide', 'Flame Retardant', '262.9', 'colorless solid'], ['206 ', 'chlorinated paraffin hydrocarbons', 'Cereclor S 52', 'Flame Retardant', 'Unknown', 'yellowish liquid'], ['207 ', "2,2'-bis( 4-(2,3-dibromopropoxy}-3,5-dibromophenyl}propane", 'Bromkal 66-8', 'Flame Retardant', '835.6', 'colorless solid'], ['208 ', "N,N'-ethylene-bis( tetrabromophthalimide}", 'Saytex BT 93', 'Flame Retardant', '951.5', 'colorless solid'], ['209 ', 'mixture of oligomeric, chlorinated phosphirc aicd ester', 'Tego Antiflamm N', 'Flame Retardant', 'Unknown', 'colorless, clear liquid'], ['210 ', 'oxalyl-bis(benzylidenehydrazide)', 'Eastman OABH-EF', 'Metal deactivator', '294.2', 'colorless, crystalline solid'], ['211 ', 'Phosphonic acid ester', 'Baerostab CW M 201', 'Metal deactivator', 'Unknown', 'colorless clear liquid'], ['212 ', 'Tributyltin hydride', 'XE 9503 (TBTH)', 'Biocide', '291.1', 'colorless, clear liquid'], ['213 ', 'Tributyltin fluoride', 'Eurecid 9260 (TBTF)', 'Biocide', '309.1', 'colorless solid'], ['214 ', 'Tributyltin oxide', 'Eurecid 9000', 'Biocide', '596.1', 'colorless, clear liquid'], ['215 ', 'Tributyltin linoleate', 'Eurecid 9220 (TBTL)', 'Biocide', '569.5', 'yellow, clear liquid'], ['216 ', 'tributyltin naphthenate', 'Eurecid 9240 (TBTN)', 'Biocide', 'Unknown', 'yellow-brown, clear liquid'], ['217 ', 'tributyltin benzoate', 'Eurecid 9200 (TBTB)', 'Biocide', '411.2', 'colorless, clear liquid'], ['218 ', 'tetraoctyltin', 'Tetra-n-octylzinn, dest. (TOT)', 'Biocide', '571.6', 'pale-yellow, clear liquid'], ['219 ', 'N-( dichlorofluoromethylthio )phthalimide', 'Preventol A3', 'Biocide', '280.1', 'colorless solid'], ['220 ', 'Arsenic and arsenic compounds', 'Arsenic trioxide, sodium arsenite, arsenic trichloride', 'Biocide', 'Unknown', 'Metalloid/semi-metal'], ['221 ', 'Triclosan', 'Irgasan DP-300', 'Biocide', '289.54', 'White solid'], ['222 ', 'Phenoxarsine', '10,10-oxybisphenoarsine', 'Biocide', '502.2', 'Clear, light yellow liquid'], ['223 ', 'Bis(tributyltin)oxide', 'TBTO', 'Biocide', '596.112', 'Viscous, colorless liquid'], ['224 ', 'Ba permanganate mixed crystals with Ba sulfate', 'Manganblan', 'Pigment', 'Unknown', 'Shining middle-blue solid'], ['225 ', 'Pb chromate', 'Sicomin Rot L 3130 S', 'Inorganic Pigment', '323.19', 'Red solid'], ['226 ', 'Mixed crystals of Pb chromate-sulfate', 'Sicomingelb LD E-55', 'Organic Pigment', 'Unknown', 'yellow solid'], ['227 ', 'mixed crystals of Pb chromate-sulfate', 'Sicomin Gelb L 1625', 'Inorganic Pigment', 'Unknown', 'yellow solid'], ['228 ', 'Pb chromate-molybdate mixed crystals', 'Sicomin Rot L 3030 S', 'Inorganic Pigment', 'Unknown', 'red solid'], ['229 ', 'S-containing Na Al silicate', 'Ultramarin Blau', 'Inorganic Pigment', 'Unknown', 'blue solid'], ['230 ', 'Co chromate-aluminate, spinell structure', 'Lichtblau 100 Standard 9515', 'Inorganic Pigment', 'Unknown', 'blue solid'], ['231 ', 'Co Ni Zn titanate aluminate, inverse spinell', 'Lichtgruen 5 G Standard 9270', 'Inorganic Pigment', 'Unknown', 'green solid'], ['232 ', 'Fe oxide', 'Sicotrans Rot I. 2915 D', 'Inorganic pigment', '165.87', 'red solid'], ['233 ', 'Fe oxide hydrate', 'Sicotrans Gelb L. 1916', 'Inorganic Pigment', '159.69', 'yellow solid'], ['234 ', 'Fe oxide hydrate', 'Sicotrans Orange L. 2416', 'Inorganic Pigment', 'Unknown', 'orange solid'], ['235 ', 'Fe oxide hydrate ', 'Bayferrox 920', 'Inorganic Pigment', 'Unknown', 'red solid'], ['236 ', 'iron(lI, III) oxide, magnetite structure', 'Bayferrox 318, Standard 86', 'Inorganic Pigment', '231.6', 'black solid'], ['237 ', 'chromium(III) oxide, corundum structure', 'Chromoxidgruen GN', 'Inorganic Pigment', '151.99', 'green solid'], ['238 ', 'Cr-Sb-Ti oxide mixed phase system', 'Sicotrans Gelb I. 1910', 'Inorganic Pigment', 'Unknown', 'yellow solid'], ['239 ', 'Sb Ni Ti oxide', 'Lichtgelb 7 G', 'Inorganic Pigment', 'Unknown', 'yellow solid'], ['240 ', 'Titanium dioxide', 'Tioxide R-CR-2', 'Inorganic Pigment', '79.88', 'white solid'], ['241 ', 'calcined coprecipitation of CdS and CdSe, extended with BaS04', 'Cadmium Red', 'Inorganic Pigment', 'Unknown', 'red solid'], ['242 ', '3-nitro-4-toluidine -> acetoacetic arylide-anilide', 'Hansa Gelb G', 'Organic Pigment', '340.3', 'yellow solid'], ['243 ', '4-methoxy-2-nitroaniline -> acetoacetic arylide-2-methylanilide', 'Hansa Gelb 3R', 'Organic Pigment', '370.4', 'yellow solid'], ['244 ', '2-methoxy-4-nitroaniline -> acetoacetic arylide-2-methoxyanilide', 'Monolite Yellow 2G', 'Organic Pigment', '386.4', 'yellow solid'], ['245 ', '4-methoxy-2-nitroaniline -> acetoacetic rylide-2-methoxyanilide', 'Hansa Gelb RN', 'Organic Pigment', '386.3', 'yellow solid'], ['246 ', '4-chloro-2-toluidine -> acetoacetic arylide-I-naphthylimide', 'Helio Echtgelb 8G', 'Organic Pigment', '379.8', 'yellow solid'], ['247 ', '4-chloro-2-nitroaniline -> acetoacetic arylide-6-chloro-2-methylanilide', 'Hansa Gelb 8G', 'Organic Pigment', '409.2', 'yellow solid'], ['248 ', '4-chloro-2-nitroaniline -> acetoacetic arylide-anilide', 'Hansa Gelb 3G', 'Organic Pigment', '360.7', 'yellow solid'], ['249 ', '4-chloro-2-nitroaniline -> acetoacetic rylide-2,4-dimethylanilide', 'Hansa Gelb GR', 'Organic Pigment', '388.8', 'yellow solid'], ['250 ', '4-chloro-2-nitroaniline -> acetoacetic arylide-2-chloroanilide', 'Monolite Yellow 10 GE', 'Organic Pigment', '395.2', 'yellow solid'], ['251 ', '4-chloro-2-nitroaniline -> acetoacetic arylide-4-chloro-2-methylanilide', 'Hansa Brillantgelb 10 GX', 'Organic Pigment', '409.2', 'yellow solid'], ['252 ', '4-chloro-2-nitroaniline -> acetoacetic arylide-2-methoxyanilide', 'Hansa Brillantgelb 4GX', 'Organic Pigment', '390.8', 'yellow solid'], ['253 ', '4-chloro-2-nitro aniline -> acetoacetic arylide-4-methoxyanilide', 'Symuler Fast Yellow 4119', 'Organic Pigment', '390.8', 'yellow solid'], ['254 ', '4-chloro-2-nitroaniline -> acetoacetic arylide-4-ethoxyanilide', 'Hansa Gelb XT', 'Organic Pigment', '392.8', 'yellow solid'], ['255 ', '4-amino-5-nitrobenzenesulfonic acid -> acetoacetic arylide-anilide, Ca-salt', 'Irgalite Yellow WSC', 'Organic Pigment', '848.7', 'yellow solid'], ['256 ', '4-amino-3-nitrobenzenesulfonic acid -> acetoacetic arylide-2-methylanilide, Ca-salt', 'Irgaplast Gelb R', 'Organic Pigment', '878.9', 'yellow solid'], ['257 ', '4-amino-3-nitrobenzenesulfonic acid -> acetoacetic arylide-2-methylanilide, Ba-salt', 'Irgalite Yellow WSR', 'Organic Pigment', '976.1', 'yellow solid'], ['258 ', '2,5-dimethoxy-4-N-phenylsulfonamidoaniline-> acetoacetic arylide-4-chloro-2,5-dimethoxyanilide', 'Novoperm Gelb FGL', 'Organic Pigment', '591', 'yellow solid'], ['259 ', '3-nitrosulfanilic acid -> acetoacetic arylide-anilide, Sr-salt', 'Symuler Lake Fast Yellow 6G', 'Organic Pigment', '896.3', 'yellow solid'], ['260 ', '3-nitrosulfanilic acid -> acetoacetic arylide-4-methoxyanilide', 'Symuler Yellow 3056', 'Organic Pigment', '910.9', 'yellow solid'], ['261 ', '2,4-dichloroaniline -> 2-hydroxynaphthoic arylide-2-methylanilide', 'Permanent Rot FGG', 'Organic Pigment', '450.3', 'red solid'], ['262 ', '2,5-dichloroaniline -> 2-hydroxynaphthoic arylide-4-methylanilide', 'Permanent Rot FRL', 'Organic Pigment', '450.3', 'red solid'], ['263 ', '4-chloro-2-toluidine -> 2-hydroxynaphthoic arylide-4-chloro-2-methylanilide', 'Monolite Red 4RH', 'Organic Pigment', '464.4', 'red solid'], ['264 ', '5-chloro-2-toluidine -> 2-hydroxynaphthoic arylide-4-chloroanilide', 'Helio Echtcarmin B', 'Organic Pigment', '450.3', 'red solid'], ['265 ', '5-chloro-2-toluidine -> 2-hydroxynaphthoic rylide-5-chloro-2-methylanilide', 'Permanent Rubin FBH', 'Organic Pigment', '498.8', 'dark-red solid'], ['266 ', '2,4,5-trichloroaniline -> 2-hydroxynaphthoic arylide-2-methylanilide', 'Permanent Rot FGR 70', 'Organic Pigment', '484.8', 'red solid'], ['267 ', '2,4-dinitroaniline -> 2-hydroxynaphthoic arylide-2-ethoxyanilide', 'Helio Echtbordo RR', 'Organic Pigment', '501.5', 'dark-red solid'], ['268 ', "3-amino-4-methoxy-N(4'-benzamide)benzamide -> 2-hydroxynaphthoic arylide-2,4-dimethoxy-5-chloranilide", 'PV-Echtrot HF4B', 'Organic Pigment', '654.1', 'red solid'], ['269 ', "3-amino-4-methyl-N-(2',4'-xylyl)benzamide -> 2-hydroxynaphthoic arylide-4-chloroanilide", 'Vulkan Echtrossa G', 'Organic Pigment', '563', 'pink solid'], ['270 ', '3-amino-4-chlorobenzamide -> 2-hydroxynaphthoic arylide-4-aminoacetylanilide', 'Novoperm Rot HFG', 'Organic Pigment', '501.9', 'red solid'], ['271 ', '4-aminobenzamide -> 2-hydroxynaphthoic arylide-2-ethoxyanilide', 'Novoperm Rot F5RK', 'Organic Pigment', '454.5', 'red solid'], ['272 ', '3-chloroaniline -> 2-hydroxynaphthoic arylide-2-methoxyanilide', 'Helio Echtorange G', 'Organic Pigment', '502.8', 'orange solid'], ['273 ', '2,5-dichloroaniline -> 2-hydroxynaphthoic arylide-2-methoxyanilide', 'Permanent Rot FRLL', 'Organic Pigment', '466.3', 'red solid'], ['274 ', '2,5-dichloroaniline -> 2-hydroxynaphthoic arylide-2,5-dimethoxyanilide', 'Permanent Braun FG', 'Organic Pigment', '496.4', 'brown solid'], ['275 ', '4-amino-2,5-diethoxybenzanilide -> 2-hydroxynaphthoic arylide-2-methylanilide', 'Helio Echtbrillantblau RR', 'Organic Pigment', '484.5', 'blue solid'], ['276 ', '3-amino-4-methoxybenzanilide -> 2-hydroxynaphthoic arylide-anilide', 'Vulkan Echtrubin B', 'Organic Pigment', '516.5', 'ruby solid'], ['277 ', '3-amino-4-methoxybenzanilide -> 2-hydroxynaphthoic arylide-4-chloro-2-methylanilide', 'Permanent Rosa F3B', 'Organic Pigment', '565', 'pink solid'], ['278 ', '3-amino-4-methoxybenzanilide -> 2-hydroxynaphthoic arylide-4-chloro-2,5-dimethoxyanilide', 'Permanent Carmin FBB02', 'Organic Pigment', '599', 'dark-red solid'], ['279 ', '2-amino-4-(2,5-dichloroanilido)benzoic methylester-> 2-hydroxynaphthoic arylide-2-anisidide', 'Novoperm Rot HF 3570', 'Organic Pigment', '643.5', 'Red solid'], ['280 ', '2-amino-4-(2,5-dichloroanilido)benzoic methylester-> 2-hydroxynaphthoic arylide-2-anisidide', 'Novoperm Rot HF3S', 'Organic Pigment', '643.5', 'Red solid'], ['281 ', '5-nitro-2-toluidine -> 2-hydroxynaphthoic arylide-anilide', 'Symuler Fast Scarlet BGT', 'Organic Pigment', '426.4', 'scarlet solid'], ['282 ', '4-nitro-2-toluidine -> 2-hydroxynaphthoic arylide-2-methylanilide', 'Pmernant Bordo FRR', 'Organic Pigment', '440.5', 'dark-red solid'], ['283 ', '5-nitro-2-toluidine -> 2-hydroxynaphthoic arylide-4-chloroanilide', 'Permanent Rot F4R', 'Organic Pigment', '460.9', 'red solid'], ['284 ', '2-methoxy-4-nitroaniline -> 2-hydroxynaphthoic arylide-2-methylanilide', 'Toluidine Maroon RT-530-D', 'Organic Pigment', '456.4', 'dark-red solid'], ['285 ', '3-amino-4-methoxybenzanilide -> 2-hydroxynaphthoic arylide-3-nitroanilide', 'Symuler Fast Red 4085', 'Organic Pigment', '561.6', 'red solid'], ['286 ', '2-methoxy-4-nitroaniline -> 2-hydroxynaphthoic arylide-l-naphthylamide', 'Permanent Bordo F3R', 'Organic Pigment', '477.5', 'dark-red solid'], ['287 ', '2,4-dinitroaniline -> 2-hydroxynaphthoic arylide-2-ethoxyanilide', 'Helio Echtbrillantrot 3B', 'Organic Pigment', '501.5', 'red solid'], ['288 ', '2-nitro-4-toluidine -> 2-hydroxynaphthoic arylide-3-nitroanilide', 'Sico Echtmaroon BMD dunkel', 'Organic Pigment', '471.4', 'red-brown solid'], ['289 ', '2-methoxy-5-nitroaniline -> 2-hydroxynaphthoic arylide-3-nitroanilide', 'Symuler Fast Red 4015', 'Organic Pigment', '487.4', 'red solid'], ['290 ', '3-amino-4-methoxyphenylbenzyl sulfone -> 2-hydroxynaphthoic arylide-2,3-dimethylanilide', 'Hansa Rottoner R', 'Organic Pigment', '579.7', 'red solid'], ['291 ', '2-methoxy-5-N,N-dimethylsulfonamidoaniline -> 2-hydroxynaphthoic arylide-5-chloro-2,4-dimethoxyanilide', 'Permanent Carmin FB01', 'Organic Pigment', '627.1', 'dark-red solid'], ['292 ', '3-amino-4-methoxybenzoanilide -> 2-hydroxynaphthoic acid-4-chloro-2-methylanilide', 'Permanent Rosa', 'Organic Pigment', '565', 'pink solid'], ['293 ', '5-nitro-2-toluidine -> 2-hydroxynaphthoic arylide-2-methylanilide', 'Montclair Red Medium 235-7700', 'Organic Pigment', '440.4', 'red solid'], ['294 ', '2-aminobenzenesulfonic acid -> 2-hydroxynaphthoic arylide-4-sulfonic acid anilide, Ba-salt', 'PV-Rot H4B 01', 'Organic Pigment', '662.9', 'red solid'], ['295 ', "4' -nitrophenyl(3-amino-4-methoxyphenyl)sulfonate -> 2-hydroxynaphthoic arylide-2-methylanilide", 'Helio Echtcarmin G', 'Organic Pigment', '612.6', 'red solid'], ['296 ', '2-amino-I,4-benzenedisulfonic acid -> 2-hydroxyna-phthoic', 'Irgaplast Rot HGL', 'Organic Pigment', '757.3', 'red solid'], ['nan', 'arylide-2, 4-dimethoxy-5-chloro-anilide, Ba salt', 'nan', 'nan', 'nan', 'nan'], ['297 ', '2-amino-I,4-benzenedisulfonic acid->2-hydroxynaphthoic arylide-2-naphthylamide, Ba salt', 'Irgaplast Rot HBL', 'Organic Pigment', '662.8', 'red solid'], ['298 ', '2-nitroaniline -> 2-naphthol', 'Ortho Nitranilinorange', 'Organic Pigment', '293.3', 'orange solid'], ['299 ', '4-nitroaniline -> 2-naphthol', 'Pigmentrot B', 'Organic Pigment', '290.3', 'red solid'], ['300 ', '4-nitroaniline -> 2-naphthol, Cu-complex', 'Tiefdruckbraun 30', 'Organic Pigment', '248.3', 'brown solid'], ['301 ', '4-methyl-2-nitroaniline -> 2-naphthol', 'Hansa Scharlach RNC', 'Organic Pigment', '307.3', 'scarlet solid'], ['302 ', '2,4-dinitroaniline -> 2-naphthol', 'Hansa Rot GG', 'Organic Pigment', '338.3', 'red solid'], ['303 ', '2-chloro-4-nitroaniline -> 2-naphthol', 'Hansa Rot R', 'Organic Pigment', '327.7', 'Red solid'], ['304 ', '2-naphthylamine-I-sulfonic acid -> 2-naphthol, Ba-salt', 'Tobithol Red B', 'Organic Pigment', '463.6', 'red solid'], ['305 ', '2-methylsulfanilic acid -> 2-naphthol, Ba-salt', 'Lithol Rot RMT', 'Organic Pigment', '443.6', 'red solid'], ['306 ', '4-chloro-3-toluidine-6-sulfonic acid -> 2-naphthol,Na-salt', 'Lackrot C', 'Organic Pigment', '420.8', 'red solid'], ['307 ', '4-chloro-3-toluidine-6-sulfonic acid -> 2-naphthol, Ba-salt', 'Permanent Lackrot LCLL', 'Organic Pigment', '824.8', 'Red solid'], ['308 ', '2-amino-4-ethyl-5-chlorobenzenesulfonic acid-> 2-naphthol, Ba-salt', 'Clarion Red 20-7155', 'Organic Pigment', '526.1', 'Red solid'], ['309 ', '1-(4-methyl-2-nitro-l-phenyl)azo-2-naphthol', 'Hansascharlach RNC', 'Organic Pigment', '307.3', 'dark-red solid'], ['310 ', '2-amino-5-chloro-4-i-propylbenzenesulfonic acid-> 2-naphthol, Ba-salt', 'Arcturus Red', 'Organic Pigment', '539.1', 'red solid'], ['311 ', '2-amino-4-carboxy-5-chlorobenzenesulfonic acid -> 2-naphthol, Ca-salt', 'PV-Rot NCR', 'Organic Pigment', '444.8', 'red solid'], ['312 ', 'aniline -> 2-naphthol-6-sulfonic acid, Ca-salt', 'Helio Orange CAG', 'Organic Pigment', '334.3', 'orange solid'], ['313 ', 'I-naphthylamine -> 2-naphthol-5-sulfonic acid, Ca-salt', 'Helio Bordo BL', 'Organic Pigment', '384.4', 'dark-red solid'], ['314 ', '3,4,5-trichloroaniline -> 2-naphthol-3,6-disulfonic acid, Ba-salt', 'Helio Echtrottoner R', 'Organic Pigment', '647', 'red solid'], ['315 ', '5-chloro-2-phenoxyaniline -> 2-naphthol-3,6-disulfonic acid, Ba-salt', 'Helio Echtrottoner 3B', 'Organic Pigment', '670.2', 'red solid'], ['316 ', '2-naphthylarnine-l-sulfonic acid -> 2-naphthol,Na-salt', 'Lithol Rot RS', 'Organic Pigment', '422.4', 'red solid'], ['317 ', '2-naphthylarnine-l-sulfonic acid -> 2-naphthol, Ca-Salt', 'Lithol Rot RBKX (Brillianttoner CS)', 'Organic Pigment', '416.5', 'red solid'], ['318 ', '2-amino-5-chlororbenzoic acid -> 2-hydroxynaphthoic arylide, Cu-salt', 'Newport Maroon RT-647-D', 'Organic Pigment', '420.3', 'brown solid'], ['319 ', '2-amino-5-chlororbenzoic acid -> 2-hydroxynaphthoic arylide, Mn-salt', 'Maroon Gold IRT-608-D', 'Organic Pigment', '411.7', 'brown solid'], ['320 ', '4-toluidine-3-sulfonic acid -> 2-hydroxynaphthoic arylide,Na-salt', 'Lithol Rubin BN', 'Organic Pigment', '430.4', 'ruby solid'], ['321 ', '4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Ca-salt', 'Irgalite Rubine 4BP', 'Organic Pigment', '412.4', 'dark-red solid'], ['322 ', '2-amino-l-naphthalenesulfonic acid -> 2-hydroxynaphthoic arylide, Na-salt', 'Lithol Bordeaux BNS', 'Organic Pigment', '466.4', 'dark-red solid'], ['323 ', '2-amino-l-naphthalenesulfonic acid -> 2-hydroxynaphthoic arylide, Ca-salt', 'Symuler Lake Bordeaux 10 B 310', 'Organic Pigment', '460.5', 'dark-red solid'], ['324 ', 'o-aminobenzoic acid -> 2-hydroxy-3,6-naphthalenedisulfonic acid, Ba-salt', 'Pigmentscharlach 3 B', 'Organic Pigment', '585.7', 'scarlet solid'], ['325 ', '2-amino-l-naphthalenesulfonic acid -> 2-hydroxynaphthoic acrylide, Mn-salt', 'Maroon Toner BB', 'Organic Pigment', '475.4', 'brown solid'], ['326 ', '2-methyl-5-methoxysulfanilic acid -> 2-hydroxynaphthoic arylide, Ba-salt', 'Permanent Bordo RN', 'Organic Pigment', '551.7', 'dark-red solid'], ['327 ', '3-amino-6-chlorobenzenesulfonic acid -> 2-hydroxynaphthoic arylide, Mn-salt', 'Sico Maroon BM hell', 'Organic Pigment', '459.7', 'dark-red solid'], ['328 ', '3-amino-5-chlorobenzenesulfonic acid -> 2-hydroxynaphthoic arylide, Ca-salt', 'Lithol Rubin GK', 'Organic Pigment', '444.9', 'ruby solid'], ['329 ', '5-chloro-4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Na-salt', 'Permanent Rot 2B', 'Organic Pigment', '464.8', 'red solid'], ['330 ', '5-chloro-4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Mg-salt', 'Irgalite Red MGP', 'Organic Pigment', '443.1', 'red solid'], ['331 ', '5-chloro-4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Ca-salt', 'Rubine Toner 2BO', 'Organic Pigment', '458.9', 'dark-red solid'], ['332 ', '5-chloro-4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Sr-salt', 'Irgalite Red 2BY', 'Organic Pigment', '506.4', 'red solid'], ['333 ', '5-chloro-4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Ba-salt', 'Irgalite Red NBSP', 'Organic Pigment', '556.1', 'red solid'], ['334 ', '5-chloro-4-toluidine-2-sulfonic acid -> 2-hydroxynaphthoic arylide, Mn-salt', 'Lithol Echtscharlach L 4260', 'Organic Pigment', '473.7', 'scarlet solid'], ['335 ', '6-chloro-3-toluidine-4-sulfonic acid -> 2-hydroxynaphthoic arylide, Ca-salt', 'Macatawa Red', 'Organic Pigment', '458.9', 'red solid'], ['336 ', '6-chloro-3-toluidine-4-sulfonic acid -> 2-hydroxynaphthoic arylide, Mn-salt', 'Sico Maroon 33 M', 'Organic Pigment', '473.7', 'dark-red solid'], ['337 ', '2-trifluoromethylaniline -> 5-N-acetoacetylaminobenzimidazolone', 'Hostaperm Gelb H3G', 'Organic Pigment', '405.3', 'yellow solid'], ['338 ', '2-carboxyaniline -> 5-N-acetoacetylaminobenzimidazolone', 'Hostaperm Gelb H4G', 'Organic Pigment', '381.3', 'yellow solid'], ['339 ', '3,5-dicarboxymethylaniline -> 5-N-acetoacetylaminobenzimidazolone', 'PV-Echt-Gelb-H2G01', 'Organic Pigment', '453.4', 'yellow solid'], ['340 ', '2,5-dimethoxycarbonylaniline -> 5-N-acetoacetylaminobenzimidazolone', 'Hostaperm Gelb H6G', 'Organic Pigment', '453.4', 'yellow solid'], ['341 ', '4-chloro-2-nitroaniline -> 5-N-acetoacetylaminobenzimidazolone', 'Novoperm Orange HL70', 'Organic Pigment', '416.8', 'orange solid'], ['342 ', '4-nitroaniline -> 5-N-acetoacetylaminobenzimidazolone', 'Novoperm Orange H5G70', 'Organic Pigment', '382.3', 'orange solid'], ['343 ', "2,5-dichloroaniline -> 2'-hydroxy-3'-naphthoyl-5-aminobenzimidazolone", 'Hostaperm Braun HFR', 'Organic Pigment', '492.3', 'brown solid'], ['344 ', "2-carboxymethylaniline -> 2'-hydroxy-3'-naphthoyl-5-aminobenzimidazolone", 'Novoperm Rot HFT', 'Organic Pigment', '481.5', 'red solid'], ['345 ', "2-aminobenzoic butylester -> 2'-hydroxy-3'-naphthoyl-5-aminobenzimidazolone", 'Permanent Rot HF2B', 'Organic Pigment', '523.5', 'red solid'], ['346 ', '4-nitro-2-anisidine -> 2-hydroxynaphthoic arylide-N-(2-oxo-5-benzimidazoline)', 'Novoperm Marron HFM01', 'Organic Pigment', '498.5', 'red-brown solid'], ['347 ', "3-amino-4-methoxybenzanilide -> 2'-hydroxy-3'-naphthoyl-5-amino-benzimidazolone", 'Novoperm Carmin HF3C', 'Organic Pigment', '572.6', 'dark-red solid'], ['348 ', '2-chloroaniline -> 3-methyl-l-phenyl-5-pyrazolone', 'Permanent Gelb 4R', 'Organic Pigment', '312.7', 'yellow solid'], ['349 ', '2,5-dichloroaniline -> 3-methyl-l-phenyl-5-pyrazolone', 'Hansa Gelb RN', 'Organic Pigment', '347.2', 'yellow solid'], ['350 ', 'anthranilic acid -> 3-methyl-l-phenyl-5-pyrazolone', 'Filamid Yellow R', 'Organic Pigment', '322.3', 'yellow solid'], ['351 ', 'I-naphthylamine -> N-benzoyl-8-amino-l-naphthol-3,5-disulfonic acid, Ba-salt', 'Vulcanosinviolett BB', 'Organic Pigment', '712.9', 'violet solid'], ['352 ', '3-toluidine -> N-benzoyl-8-amino-I-naphthol-3,5-disulfonic acid, Na-salt', 'Anthosin 3B', 'Organic Pigment', '585.5', 'red solid'], ['353 ', "2-methoxyaniline -> N-(2',4'-dichlorobenzoyl)-8-amino-I-naphthol-3,5-disulfonic acid, Ba-salt", 'Vulkanosinrot 5B', 'Organic Pigment', '761.7', 'red solid'], ['354 ', "5-chloro-2-methylaniline -> N,N'-diacetoacetyl-3,3'- (5) organic pigment dimethylbenzidine", 'Helio Echtbrilliant Gelb GR', 'Organic Pigment', '685.6', 'yellow solid'], ['355 ', "2,4-dichloroaniline -> N,N'-diacetoacetyl-3,3'-dimethylbenzidine", 'Permanent Gelb NCG', 'Organic Pigment', '726.4', 'yellow solid'], ['356 ', "3,3'-dimethoxybenzidine->acetoacetic anilide", 'Symuler Fast Orange K', 'Organic Pigment', '620.7', 'orange solid'], ['357 ', "3,3'-dimethoxybenzidine -> acetoacetic arylide-2,4-dimethylanilide", 'Vulcan Echtorange GG', 'Organic Pigment', '676.7', 'orange solid'], ['358 ', "3,3'-dichlorobenzidine -> acetoacetic arylide-anilide", 'Permanent Gelb DHG', 'Organic Pigment', '629.5', 'yellow solid'], ['359 ', "3,3'-dichlorobenzidine -> acetoacetic arylide-2-methylanilide", 'Irgalite Yellow BRM', 'Organic Pigment', '657.5', 'yellow solid'], ['360 ', "3,3'-dichlorobenzidine -> acetoacetic arylide-4-toluidide", 'Irgalite Yellow BAF', 'Organic Pigment', '657.5', 'yellow solid'], ['361 ', "3,3'-dichlorobenzidine -> acetoacetic arylide-2,4-dimethylanilide", 'Irgalite Yellow BAWP', 'Organic Pigment', '685.6', 'yellow solid'], ['362 ', "3,3'-dichlorobenzidine -> acetoacetic arylide-2-methoxyanilide", 'Irgalite Yellow 2GP', 'Organic Pigment', '685.5', 'yellow solid'], ['363 ', "3,3'-dichlorobenzidine -> acetoacetic arylide-4-chloro-2,5-dimethoxyanilide", 'Diacetanil Yellow 3RH', 'Organic Pigment', '818.5', 'yellow solid'], ['364 ', "2,2'-dichloro-S,S'-dimethoxybenzidine -> acetoacetic arylide-2,4-dimethylanilide", 'Vulcan Echtgelb 5G', 'Organic Pigment', '745.7', 'yellow solid'], ['365 ', ",2',5, S'-tetrachlorobenzidine->acetoacetic arylide-2,4-dimethylanilide", 'Novoperm Gelb H10G', 'Organic Pigment', '754.5', 'yellow solid'], ['366 ', "3-amino-4,5'-dichloro-2'-methylbenzanilide -> N,N'-(2,5-dimethyl-l,4-phenylene )-bis( acetoacetamide)", 'Cromophtal Gelb GR', 'Organic Pigment', '916.6', 'yellow solid'], ['367 ', "3-amino-4,5'-dichloro-2'-methylbenzanilide -> N,N'-(2,5-dichloro-l ,4-phenylene )-bis( acetoacetamide)", 'Cromophtal Gelb 6G', 'Organic Pigment', '957.4', 'yellow solid'], ['368 ', "3-amino-4-chloro-2'-(4-chlorophenoxy)-5'-trifluoromethylbenzanilide-> N,N'-(2-chloro-5-methyl-l,4-phenylene", 'Cromophtal Gelb 8G', 'Organic Pigment', '1229', 'yellow sollid'], ['nan', ')-bis( acetoacetamide)', 'nan', 'nan', 'nan', 'nan'], ['369 ', "3-amino-3,4'-dichloro-2'-methylbenzanilide-> 3-ketobutyrylchloride condensed with 2-chloro-5-methyl-p-phenylenediamine", 'Cromophtal Gelb 3G', 'Organic Pigment', '937', 'yellow solid'], ['370 ', "2,5-dichloroaniline -> N,N'-1,4-phenylenebis(3-hydroxy-2-naphthamide)", 'Cromophtal Scharlach RN', 'Organic Pigment', '794.4', 'scarlet solid'], ['371 ', "2,5-dichloroaniline-N,N' -(2-chloro-1 ,4-phenylene)-bis(3-hydroxy-2-naphthamide)", 'Cromophtal Rot BRN', 'Organic Pigment', '828.9', 'red solid'], ['372 ', "3-amino-p-toluic acid 2-chloroethyl ester -> N,N'(2,5-dimethyl-l,4-phenylene )-bis(3-hydroxy-2-naphthamide)", 'Cromophtal Rot G', 'Organic Pigment', '925.8', 'red solid'], ['373 ', "4-chloro-2-nitroaniline -> N,N'-(2-chloro-l,4-phenylene)-bis(3-hydroxy-2-naphthamide)", 'Cromophtal Braun 5R', 'Organic Pigment', '770.5', 'brown solid'], ['374 ', "3,3'-dichlorobenzidine -> 3-methyl-I-phenyl-5-pyrazolone", 'Irgalite Orange P', 'Organic Pigment', '623.5', 'orange solid'], ['375 ', "3,3'-dichlorobenzidine -> 3-methyl-l-(3'-tolyl)-5-pyrazolone", 'Permanent Orange RL 70', 'Organic Pigment', '651.6', 'orange solid'], ['376 ', "2,2'-dianisidine -> 3-methyl-l-phenyl-5-pyrazolone", 'Elektra Red', 'Organic Pigment', '614.7', 'red solid'], ['377 ', "3,3'-dimethoxybenzidine -> 3-methyl-l,4'-tolyl-5-pyrazolone", 'PV-Rot G 1', 'Organic Pigment', '614.6', 'red solid'], ['378 ', "3,3'-dichlorobenzidine -> ethoxycarbonyl-l-phenyl-5-pyrazolone", 'Sicoplast V Rot', 'Organic Pigment', '739.6', 'red solid'], ['379 ', '1,2-dihydroxy-9,lO-anthraquinone (alizarin), Al-Ca lake', 'Krapplack C', 'Organic Pigment', '240.2', 'red solid'], ['380 ', "4,4' -bis(I -amino-9, 1 O-anthraquinone)", 'Indofast Red R6340', 'Organic Pigment', '444.4', 'red solid'], ['381 ', '4,4-bis(I-amino-9,IO-anthraquinonediyl) on CaC03', 'Cromophtal Rot C20', 'Organic Pigment', '444.4', 'red solid'], ['382 ', 'I-methylamino-9,1O-anthraquinone', 'Oracet Red G', 'Organic Pigment', '237.3', 'red solid'], ['383 ', '1 ,8-bis( thiophenyl)-9,1 O-anthraquinone', 'Oracet Yellow GHS', 'Organic Pigment', '424.5', 'yellow solid'], ['384 ', '1-aminoanthraquinonebenzamide', 'Pigmosolgelb G', 'Organic Pigment', '295.3', 'yellow solid'], ['385 ', 'quinizarin-2-sulfonic acid, AI-salt', 'Violett 31372', 'Organic Pigment', '346.3', 'violet solid'], ['386 ', 'quinizarin-6-sulfonic acid, AI-lake', 'Violett 31372 R', 'Organic Pigment', '346.3', 'violet solid'], ['387 ', 'quinizarin-2,6-disulfonic acid AI-salt', 'Violett 31372 B', 'Organic Pigment', '425.3', 'violet solid'], ['388 ', 'N-l-anthraquinone-anthrapyrimidine-4-carboxylic amid', 'Paliogen Gelb 1560', 'Organic Pigment', '481.5', 'yellow solid'], ['389 ', "N,N'-{5-phenyl-l,3-triazine)-bis{1-amino-9,1 O-anthraquinone)", 'Cromophtal Gelb AGR', 'Organic Pigment', '599.6', 'yellow solid'], ['390 ', 'perylene-3,4,9,lO-tetracarboxylic acid anhydride', 'Irgazin Rot BPT', 'Organic Pigment', '392.3', 'red solid'], ['391 ', 'perylene-3,4,9,lO-tetracarboxylic acid diimide', 'Perindo Violet V4047', 'Organic Pigment', '390.3', 'violet solid'], ['392 ', 'perylene-3,4,9,I-tetracarboxylic acid diimide', 'PV-Echtbordo B', 'Organic Pigment', '390.3', 'dark-red solid'], ['393 ', "N ,N' -dimethylperylene-3,4,9,10-tetracarboxylic acid diimide", 'Paliogen Red L 4120', 'Organic Pigment', '418.4', 'red solid'], ['394 ', "N ,N' -di-4' -anisylperylene-3,4,9, 1 O-tetracarboxylic acid diimide", 'Indofast Brilliant Scarlet R-6500', 'Organic Pigment', '602.6', 'scarlet solid'], ['395 ', "N,N'-di-3',5'-xylylperylene-3,4,9,IO-tetracarboxylic acid diimide", 'Paliogen Rot K3580', 'Organic Pigment', '598.7', 'red solid'], ['396 ', 'perylene derivative', 'Indofast Brilliant Scarlet-Toner R-6300', 'Organic Pigment', '630.6', 'scarlet solid'], ['397 ', "N,N' -di-3' ,5' -xylylperylene-3,4,9, 1 0-tetracarboxylic acid diimide with poly( dimethylsiloxane)", 'Wacker HTV-Farbpaste', 'Organic Pigment', '598.7', 'red paste'], ['398 ', 'diimide of 3,4,9,10-perylenetetracarboxylic acid with 4-phenylazoaniline', 'Paliogen Rot L3910 HD', 'Organic Pigment', '750.8', 'red solid'], ['399 ', '2,7 -dibromoanthanthrone', 'Monolite Red Y', 'Organic Pigment', '464.1', 'light-red solid'], ['400 ', "dibenzimidazolo( 1,2-e,1 ',2'-m)-4,9-diaza-3,8-pyrenequinone", 'EPV-Echtorange GRL', 'Organic Pigment', '412.4', 'orange solid'], ['401 ', 'pyranthrone', 'Indanthren Goldorange G', 'Organic Pigment', '406.4', 'orange solid'], ['402 ', '6,14-dichloropyranthrone', 'Paliogen Orange L 2640', 'Organic Pigment', '475.3', 'orange solid'], ['403 ', '6, 14-dichloro-l ,9-dibromopyranthrone', 'Paliogen Rot L 3340', 'Organic Pigment', '633.1', 'red solid'], ['404 ', '7,9,12-tribromopyranthrone', 'Paliogen Orange 3GT', 'Organic Pigment', '643.1', 'orange solid'], ['405 ', '16,17 -dimethoxyviolanthrone', 'Indanthren Brilliant Gruen FFB', 'Organic Pigment', '492.5', 'green solid'], ['406 ', '5,14-dichloroisoviolanthrone', 'Indanthren Brilliant Violett RR', 'Organic Pigment', '525.4', 'violet solid'], ['407 ', '5,14-dibromoisoviolanthrone', 'Indanthren Brilliant Violett 3B', 'Organic Pigment', '614.3', 'violet solid'], ['408 ', '2,4-dinitro-l-naphthol-7 -sulfonic acid, Ba-lake on blanc fixe', 'Hellgelber Lack 1', 'Organic Pigment', '433.5', 'yellow solid'], ['409 ', "N,N' -di-4-chloro-2-nitrophenylmethylendiamine, methylen-bis( 4-chloro-2-nitrophenylamin)", 'Lithol Echtgelb GG', 'Organic Pigment', '355.1', 'yellow solid'], ['410 ', '4-(amino-3-tolyl)-4\'-N-phenylaminophenyl-4"-N-sulfophenylaminophenylmethane,', 'Arionblau 1', 'Organic Pigment', '521.6', 'blue solid'], ['nan', 'free acid', 'nan', 'nan', 'nan', 'nan'], ['411 ', 'bis(4-N-phenylaminophenyl)-4-N"-sulfophenylaminophenylmethane', 'Reflex Blau R51', 'Organic Pigment', '595.7', 'blue solid'], ['412 ', '4-N-phenylaminophenyl-4\'-N-(2"-tolylaminophenyl)-4"\'-N-(4""-sulfo-2""-tolylaminophenyl)methane', 'Reflex Blau RB', 'Organic Pigment', '611.7', 'blue solid'], ['413 ', 'bis(4-N-3\'-tolylaminophenyl)-4"-N-(4"\'-sulfo-3"\'-tolylaminophenyl)methane', 'Reflex Blau 2G', 'Organic Pigment', '623.8', 'blue solid'], ['414 ', 'bis(4-N-3\'-tolylaminophenyl)-4"-N-(4"\'-sulfo-3"\'-tolylaminophenyl)methane', 'Reflex Blau 3G 51', 'Organic Pigment', '637.8', 'blue solid'], ['415 ', "N,N' -1,3-phenylene-bis( 3-iminotetrachloroisoindolin-I-one)", 'Cromophtal Gelb 2RLTS', 'Organic Pigment', '641.9', 'yellow solid'], ['416 ', "N,N' -(2,6-toluenediyl)-bis(3-iminotetrachloroisoindolin-I-one), azomethine-type", 'Irgazin Gelb 2GLTN', 'Organic Pigment', '655.9', 'yellow solid'], ['417 ', 'isoindoline derivative', 'Fanchon Fast Yellow Y-5700', 'Organic Pigment', '367.2', 'yellow solid'], ['418 ', 'isoindolinone derivative, azomethine-type', 'Irgazin Orange 3GL', 'Organic Pigment', '569.2', 'orange solid'], ['419 ', "dibenzimidazolo(l,2-e,2',1 '-I)-4,9-diaza-3, 10-pyrenequinone", 'Permanent Rot TG', 'Organic Pigment', '412.4', 'red solid'], ['420 ', '7,14-dioxo-5,7,12,14-tetrahydroquinolino-[2,3-blacridine,β-form', 'Cinquasia Violet R RT-891-D', 'Organic Pigment', '312.3', 'violet solid'], ['421 ', '7,14-dioxo-5,7,12,14-tetrahydroquinolino(2,3-b ) acridine, β-form', 'Hostaperm Rotviolett ER02', 'Organic Pigment', '312.3', 'red-violet solid'], ['422 ', ',14-dioxo-5,7,12,14-tetrahydroquinoIino-[2,3-b]acridine, γ-form', 'Hostaperm Rot E2B 70', 'Organic Pigment', '312.3', 'red solid'], ['423 ', '2,9-dimethyl-7,14-dioxo-5,7,12,14,tetrahydroquinoIino[2,3-b ]acridine', 'Hostaperm Rosa E Transparent', 'Organic Pigment', '342.4', 'pink solid'], ['424 ', '2,9-dichloro-7,14-dioxo-5,7,12,14-tetrahydroquinolino[ 2,3-b ] acridine', 'Quindo Magenta RV 6843', 'Organic Pigment', '355.2', 'solid'], ['425 ', '3,1 0-dichloro-7 ,14-dioxo-5,7, 12,14-tetrahydroquinolino[2,3-b]acridine', 'Hostaperm Rot EG Transparent', 'Organic Pigment', '383.2', 'red solid'], ['426 ', '3,8,16-trioxo-3,8,9,16-tetrahydronaphthalinobenzo- [a]naphth-[2,3-H]acridine-5,8,13(14H)trione', 'Indanthren Rot RK', 'Organic Pigment', '375.4', 'red solid'], ['427 ', "N ,N' -diethyldipyrazoleanthronyl", 'Indanthren Rubin R', 'Organic Pigment', '494.6', 'ruby solid'], ['428 ', 'anthrapyrimidine derivative', 'Indanthren Yellow 20', 'Organic Pigment', '481.5', 'yellow solid'], ['429 ', 'N-phenyl-2-aminophenazoniumchloride derivative', 'Pigmentschwarz 1', 'Organic Pigment', '1102', 'black solid'], ['430 ', 'fiavanthrone', 'Monolite Yellow FR', 'Organic Pigment', '408.4', 'orange solid'], ['431 ', 'indanthrone', 'Cromophtal Blau A3R', 'Organic Pigment', '442.4', 'blue solid'], ['432 ', '7-chloroindanthrone', 'Indanthren Blau GCD', 'Organic Pigment', '476.9', 'blue solid'], ['433 ', '7,16-dichloroindanthrone', 'Indanthren Blau BC', 'Organic Pigment', '511.3', 'blue solid'], ['434 ', 'Cu-phthalocyanine,β-form', 'Irgalite Blue BLR/P', 'Organic Pigment', '576.1', 'blue solid'], ['435 ', 'Cu-phthalocyanine,α-form', 'Cromophtal Blau 4GNP', 'Organic Pigment', '576.1', 'blue solid'], ['436 ', 'Cu-hexadecachlorophthalocyanine', 'Bayplast Gruen HG', 'Organic Pigment', '1127', 'green solid'], ['437 ', 'Cu-hexabromodecachlorophthalocyanine', 'Bayplast Gruen 8HG', 'Organic Pigment', '1394', 'green solid'], ['438 ', 'Cu-hexabromodecachlorophthalocyanine', 'Bayplast Gruen 8GN', 'Organic Pigment', '1394', 'green solid'], ['439 ', 'phthalocyanine, halogenated, metalfree', 'Heliogen Blau LG', 'Organic Pigment', '1065', 'blue solid'], ['440 ', '2,4,5,7-tetrahromo6uorescein, Ph-salt', 'Eosin A salzfrei', 'Organic Pigment', '853.1', 'red solid'], ['441 ', 'oxazoloanthraquinone pigment', 'Indanthren Rot FBB', 'Organic Pigment', '420.4', 'red solid'], ['442 ', '2,6-dibenzamido-9,1 O-diacetamido-3,7 -diethoxytriphendioxazine', 'Cromophtal Violett B', 'Organic Pigment', '696.7', 'violet solid'], ['443 ', 'phenoxazine derivative', 'Hostaperm Violett RL Spezial', 'Organic Pigment', '589.5', 'violet solid'], ['444 ', "5,5'-dibromo-4,4'-dichloroindigo", 'Brilliant Indigo 4G', 'Organic Pigment', '490.9', 'blue solid'], ['445 ', 'di-Na fluorescein', 'Uranin A extra', 'Organic Pigment', '376.3', 'dark-red solid'], ['446 ', '2,4,5,7 -tetrabromofluorescein, Na-salt', 'Phloxinlack 1', 'Organic Pigment', '691.9', 'red solid'], ['447 ', 'thioindigo', 'Indigo', 'Organic Pigment', '296.4', 'blue solid'], ['448 ', "7,7' -dichlorothioindigo", 'Harmon', 'Organic Pigment', '365.3', 'red solid'], ['449 ', "5,5' -dichloro-7 ,7' -dimethylthioindigo", 'Indanthren Rotbiolett RH', 'Organic Pigment', '393.3', 'violet solid'], ['450 ', "5,5' -dichloro-4,4',7 ,7' -tetramethylthioindigo", 'Indanthren Brilliant Bordo RRL', 'Organic Pigment', '421.4', 'dark-red solid'], ['451 ', "6,6' -dichloro-4,4' -dimethylthioindigo", 'Oracet Pink RF', 'Organic Pigment', '393.3', 'pink solid'], ['452 ', "4,4' -dichloro-7 ,7' -dimethylthioindigo", 'Thiosa Fast Red MV-6604', 'Organic Pigment', '393.3', 'red solid'], ['453 ', "4,4',7,7'-tetrachlorothioindigo", 'Novoperm Rotviolett MRS', 'Organic Pigment', '434.1', 'red-violet solid'], ['454 ', "4,4',7,7'-tetrachlorothioindigo on CaC03", 'Cromophtal Bordo RN', 'Organic Pigment', '434.1', 'dark-red solid'], ['455 ', "2(4'-N,N-dimethylaminophenyl)-3,6-dimethylthiazolinium chloride", 'Fanalgelb G supra', 'Organic Pigment', '304.8', 'yellow solid'], ['456 ', "PW-molybdato-complex ofbis(4-N,N-diethylaminophenyl)-4'-N-ethylaminonaphthalenemethane", 'Lumiere Blue', 'Organic Pigment', 'Unknown', 'blue solid'], ['457 ', 'PW-molybdato complex ofbis(4-N-dimethylaminophenyl)-2"-chlorophenylmethane', 'Siegleblau-Extrakt D 449', 'Organic Pigment', 'Unknown', 'blue solid'], ['458 ', 'PW-molybdato complex ofbis(4-N-ethylamino-3-methylphenyl)-2" -chlorophenylmethane', 'Fanalbremer Blau B Supra', 'Organic Pigment', '355.4', 'blue solid'], ['459 ', 'PW-molybdato complex of bis(4-N-diethylaminophenyl)-PW-molybdato complex of bis(4-N-diethylaminophenyl)-', 'Sieglegruen-Extrakt D 454', 'Organic Pigment', 'Unknown', 'green solid'], ['nan', 'phenylmethane', 'nan', 'nan', 'nan', 'nan'], ['460 ', 'complex of Rhodamine 3 B', 'Fanalrot 5B supra', 'Organic Pigment', 'Unknown', 'red solid'], ['461 ', 'PW-molybdato-complex of Rhodamine 6 G', 'Sieglerosa Extrakt D 443', 'Organic Pigment', 'Unknown', 'pink solid'], ['462 ', 'PW-molybdato-complex of Rhodamine B', 'Sieglerotviolett D 445', 'Organic Pigment', 'Unknown', 'violet solid'], ['463 ', "4,4'-bis(2-methoxy)stilbene", 'Uvitex FP', 'Fluorescent brightening agent', '418.5', 'yellowish-green solid'], ['464 ', "2,2'-(2,5-thiophenediyl)-bis(5-t-butylbenzoxazole)", 'Uvitex OB', 'Fluorescent brightening agent', '430.6', 'yellowish solid'], ['465 ', 'Ca carbonate', 'Omya BSH', 'Filler', '100.1', 'colorless solid'], ['466 ', 'AI silicate, hydrated', 'Dixie Clay', 'Filler', '516.3', 'beige solid'], ['467 ', 'Na-Al silicate', 'Vulkasil A 1', 'Filler', 'Unknown', 'White powder'], ['468 ', 'Al hydroxysilicate', 'Kaolin Argirex', 'Filler', '516.3', 'light-grey solid'], ['469 ', 'calcinated Al silicate', 'Argirex B24', 'Inorganic Pigment/Filler', 'Unknown', 'greyish solid'], ['470 ', 'Al hydroxysilicate', 'China Clay Polewhite LM', 'Filler', '516.3', 'colorless solid'], ['471 ', 'amorphous Si02', 'Perkasil KS 404', 'Filler', '60.08', 'Transparent solid, white/yellow solid'], ['472 ', 'Active SiO2', 'Vulkasil N', 'Filler', '60.07', 'Colorless solid'], ['473 ', 'Si02 with Ca silicate', 'Vulkasil C', 'Filler', 'Unknown', 'White powder'], ['474 ', 'Al hydroxide', 'Apyral B 40 E', 'Fililler/Flame retardant', '78', 'colorless solid'], ['475 ', 'Chalk', 'Calcium carbonate', 'Fillers', '100.1', 'White powder'], ['476 ', 'Clay', 'Kaolinite', 'Fillers', 'Unknown', 'Grey solid'], ['477 ', 'Zinc oxide', 'Calamine', 'Fillers', '81.4', 'White powder'], ['478 ', 'Metal powder', 'nan', 'Fillers', 'Unknown', 'Grey powder'], ['479 ', 'Wood powder', 'nan', 'Fillers', 'Unknown', 'Brown powder'], ['480 ', 'Asbestos', 'Chrysotile, crocidolite, amosite, anthophyllite', 'Fillers', '277.11', 'Blue, brown, white fiber with low density'], ['481 ', 'Barium sulfate', 'Barite powder', 'Fillers', '233.38', 'Dense white powder'], ['482 ', 'Glass microspheres', 'nan', 'Fillers', 'Unknown', 'nan'], ['483 ', 'Siliceous earth', 'nan', 'Fillers', 'Unknown', 'White powder'], ['484 ', 'paraffinic mineral oil', 'Naftolen P 613 K', 'Plasticizer', 'Unknown', 'brown liquid'], ['485 ', 'mixture of predominantly aliphatic hydrocarbons', 'Naftolen V 4057', 'Plasticizer', 'Unknown', 'brown liquid'], ['486 ', 'naphthenic mineral oil', 'Naftolen N 400', 'Plasticizer', '315', 'brown liquid'], ['487 ', 'aromatic mineral oil', 'Naftolen NV', 'Plasticizer', 'Unknown', 'black liquid'], ['488 ', 'aliphatic C15,C16 chloroparaffin', 'Chlorparaffin Huels 40G', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['489 ', 'aliphatic C15,C16 chloroparaffin (40 ... 56% Cl)', 'Chlorparaffin Huels 45G', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['490 ', 'aliphatic C1S,C16-chloroparaffin', 'Chlorparaffin Huels 52G', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['491 ', '1,4-butanediol', '1,4-Butandiol', 'Plasticizer, Educt', '90.12', 'colorless, clear liquid'], ['492 ', 'di-butoxyethoxyethyl formal', 'Reomol BCF', 'Plasticizer', '336.5', 'colorless, clear liquid'], ['493 ', 'polyether with ester and alcoholic groups', 'Vulkanol FH', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['494 ', 'glyceroltriacetate', 'Triacetin', 'Plasticizer', '218.2', 'colorless, clear liquid'], ['495 ', 'glycerol mono acetate', 'Hallco C-918', 'Plasticizer', '134.1', 'colorless, clear liquid'], ['496 ', 'pentaerythritol(isostearate adipate)', 'Ester KE-23', 'Plasticizer', '566.8', 'colorless, viscous liquid'], ['497 ', 'trirnethylolpropane(isostearate adipate)', 'Ester KE-25', 'Plasticizer', '933.6', 'colorless, viscous liquid'], ['498 ', 'aliphatic mono carboxylic acid ester', 'Edenol 192', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['499 ', 'aliphatic carboxylic acid ester', 'Edenol 194', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['500 ', 'tri( ethyleneglycol)diacetate', 'Tegda', 'Plasticizer', '234.2', 'colorless, clear liquid'], ['501 ', 'triethyleneglycol caprate-caprylate', 'Plasthall 4141', 'Plasticizer', '430', 'colorless, clear liquid'], ['502 ', 'polyglycol ester of fatty acids', 'Witamol 460', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['503 ', 'dibutyladipate', 'Adimoll DB', 'Plasticizer', '258.4', 'colorless, clear liquid'], ['504 ', 'dihexyladipate', 'Adimoll PH', 'Plasticizer', '314.5', 'colorless, clear liquid'], ['505 ', 'dihexylazelate', 'Priplast 3013 DNHZ', 'Plasticizer', '356.6', 'pale-yellow liquid'], ['506 ', 'dioctylazelate', 'Priplast 3018 DOZ', 'Plasticizer', '412.7', 'pale-yellow liquid'], ['507 ', 'dibutylsebacate', 'Edenol DBS', 'Plasticizer', '314.5', 'colorless, clear liquid'], ['508 ', 'dioctylsebacate', 'Edenol 888', 'Plasticizer', '426.7', 'colorless, clear liquid'], ['509 ', 'di(C8···C10-alkyl)adipate', 'Linplast 810 XA', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['510 ', 'di-i-butyladipate', 'Freudenberg (Brunne collection)', 'Plasticizer', '258.4', 'colorless, clear liquid'], ['511 ', 'di(2-ethylhexyl)adipate', 'Hexaplas DOA', 'Plasticizer', '370.6', 'colorless, clear liquid'], ['512 ', 'di-i-nonyladipate', 'Adimoll DN', 'Plasticizer', '398.6', 'colorless, clear liquid'], ['513 ', 'di-i-nonyladipate, mixture of isomers with high amount of linear chains', 'Plastomoll DNA', 'Plasticizer', '398.6', 'colorless, clear liquid'], ['514 ', 'di-i-decyladipate', 'Jayflex DIDA', 'Plasticizer', '382.5', 'colorless, clear liquid'], ['515 ', 'di(i-octyl)dodecanedioate', 'Plasthall DIODD', 'Plasticizer', '454.7', 'colorless, clear liquid'], ['516 ', 'mixture of di-i-decyladipate and di-i-decylphthalate', 'Palatinol CE', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['517 ', 'di(butoxyethoxyethyl}glutarate', 'Plasthall DBEEG', 'Plasticizer', '420.6', 'colorless, clear liquid'], ['518 ', 'di(butoxyethoxyethyl}adipate', 'Plasthall DBEEA', 'Plasticizer', '434.6', 'colorless, clear liquid'], ['519 ', 'dibutoxyethoxyethylsebacate', 'Plasthall 83 SS', 'Plasticizer', '490.7', 'brown, clear liquid'], ['520 ', 'fatty acid polyglycol ester', 'Deplastol 00130344', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['521 ', 'poly(1,2-propanedioladipate)', 'Palamoll 636', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['522 ', 'poly( 1,2-propyleneadipate)', 'Witamol 615 MEK', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['523 ', 'poly(I,3-butanedioladipate)', 'Diolpate 150', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['524 ', 'poly(l,3-butylene-co-I,2-propylene adipate)', 'Diolpate 214', 'Plasticizer', '1150', 'colorless, clear liquid'], ['525 ', 'poly(butanedioladipate)', 'Palamoll 646', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['526 ', 'adipic acid polyester (based on butanediol)', 'Palamoll 652', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['527 ', 'azelaic polyester', 'Priplast 3142', 'Plasticizer', 'Unknown', 'colorless, viscous liquid'], ['528 ', 'sebacic acid polyester', 'Edenol 1800', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['529 ', 'polyester based on adipic and phthalic acids', 'Uraplast RA17', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['530 ', 'polyester based on adipic and phthalic acids', 'Uraplast RA5', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['531 ', 'benzyloctyl adipate', 'Adimoll BO', 'Plasticizer', '348.5', 'colorless, clear liquid'], ['532 ', 'fatty acid ester', 'Edenol W750', 'Plasticizer', 'Unknown', 'yellow, clear liquid'], ['533 ', 'special unsaturated fatty acid ester', 'Edenol W 1385', 'Plasticizer', 'Unknown', 'yellowish, clear liquid'], ['534 ', 'i-butyloleate', 'Edenol IBO', 'Plasticizer', '338.6', 'yellow, clear liquid'], ['535 ', 'tetra( oxyethylene )dimethacrylate', 'Weichmacher TEDMA', 'Plasticizer', '330.4', 'colorless, clear liquid'], ['536 ', 'octylepoxystearate', 'Reagens EP/3', 'Plasticizer', '383.6', 'colorless, clear liquid'], ['537 ', 'special epoxidised fatty acid ester', 'Edenol B 33', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['538 ', 'i-alkylepoxystearate', 'Edenol B35', 'Plasticizer', '380', 'colorless, clear liquid'], ['539 ', 'epoxidised oleic ester', 'Priplast 1431', 'Plasticizer', '600', 'pale-yellow liquid'], ['540 ', 'epoxidised soy bean oil', 'Edenol D82,ESBO', 'Plasticizer', '935', 'yellowish liquid'], ['541 ', 'epoxidised linseed oil', 'Edenol B316, Lankroflex L', 'Plasticizer', '960', 'yellow, clear liquid'], ['542 ', 'epoxidised vegetable oil', 'Drying oil epoxides', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['543 ', 'benzyloctyladipate', 'Adimoll BO', 'Plasticizer', '348.5', 'colorless, clear liquid'], ['544 ', 'methylene-bis(thioglycolic acid butyl ester)', 'Vulkanol 88', 'Plasticizer', '308.5', 'yellowish, clear liquid'], ['545 ', 'thiodi(glycolic acid-di-2-ethylhexyl ester)', 'Vulkanol 90', 'Plasticizer', '374.6', 'yellow to brownish, clear liquid'], ['546 ', 'mixture of thiocarboxylic and carboxylic acid esters', 'Vulkanol 81', 'Plasticizer', 'Unknown', 'pale yellow, clear liquid'], ['547 ', 'dimethylphthalate', 'Chrompack', 'Plasticizer', '194.2', 'colorless, clear liquid'], ['548 ', 'diethylphthalate', 'Chrompack', 'Plasticizer', '222.2', 'colorless, clear liquid'], ['549 ', 'dipropylphthalate', 'Chrompack', 'Plasticizer', '250.3', 'colorless, clear liquid'], ['550 ', 'dibutylphthalate', 'Chrompack', 'Plasticizer', '278.3', 'colorless, clear liquid'], ['551 ', 'dihexylphthalate', 'Chrompack', 'Plasticizer', '334.5', 'colorless, clear liquid'], ['552 ', 'diheptylphthalate', 'Witamol 107', 'Plasticizer', '362.5', 'colorless, clear liquid'], ['553 ', 'dinonylphthalate', 'Chrompack', 'Plasticizer', '418.6', 'colorless, clear liquid'], ['554 ', 'diundecylphthalate', 'Chrompack', 'Plasticizer', '474.7', 'colorless, clear liquid'], ['555 ', 'didodecylphthalate', 'Chrompack', 'Plasticizer', '502.8', 'colorless, clear liquid'], ['556 ', 'di-2-propylphthalate', 'Chrompack', 'Plasticizer', '250.3', 'colorless, clear liquid'], ['557 ', 'di-i-butylphthalate', 'Chrompack', 'Plasticizer', '278.3', 'colorless, clear liquid'], ['558 ', 'di-i-pentylphthalate', 'Palatinol CE 5539 (DIPP)', 'Plasticizer', '306.4', 'colorless, clear liquid'], ['559 ', 'di-i-heptylphthalate', 'DIHP J 77', 'Plasticizer', '362.5', 'colorless, clear liquid'], ['560 ', 'di(2-ethylhexyl)phthalate', 'Witamol 100', 'Plasticizer', '390.6', 'colorless, clear liquid'], ['561 ', 'di-i-octylphthalate', 'Jayflex DIOP', 'Plasticizer', '390.6', 'colorless, liquid'], ['562 ', 'di-i-nonylphthalate', 'Palatinol DINP', 'Plasticizer', '418.6', 'colorless, clear liquid'], ['563 ', 'di-i-decylphthalate', 'Genomoll 180', 'Plasticizer', '446.7', 'colorless, clear liquid'], ['564 ', 'di-i-undecylphthalate', 'Jayflex DIUP', 'Plasticizer', '474.7', 'colorless, clear liquid'], ['565 ', 'di-i-tridecylphthalate', 'Vestinol TD stab', 'Plasticizer', '530.8', 'colorless, clear liquid'], ['566 ', 'di-i-tridecylphthalate', 'Edenol W300S', 'Plasticizer', '530.8', 'yellow liquid'], ['567 ', 'dicyclohexylphthalate', 'Unimoll 66', 'Plasticizer', '330.4', 'colorless solid'], ['568 ', 'di(C6···C10 aIkyl)phthalate', 'Witamol 110', 'Plasticizer', '395', 'colorless, clear liquid'], ['569 ', 'nonylundecylphthalate', 'Jayflex 911P', 'Plasticizer', '446.7', 'colorless, clear liquid'], ['570 ', 'mixture of phthalic acid esters', 'Calibration Mixture 84C', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['571 ', 'benzylbutylphthalate', 'Unimoll BB', 'Plasticizer', '312.4', 'colorless, clear, low-viscous liquid'], ['572 ', 'dibenzylphthalate', 'Santicizer 278', 'Plasticizer', '346.4', 'colorless, clear, oily liquid'], ['573 ', 'dimethoxyethylphthalate', 'Palatinol O', 'Plasticizer', '282.3', 'colorless, clear liquid'], ['574 ', 'dibutoxyethylphthalate', 'Palatinol K (CE 5531)', 'Plasticizer', '366.5', 'colorless, clear liquid'], ['575 ', 'triheptyItrimellitate', 'Witamol 207 stab', 'Plasticizer', '504.7', 'colorless, clear liquid'], ['576 ', 'tri(C6 ... C8-alkyl)trimellitate', 'Linplast 68 TM', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['577 ', 'tri(C8···C10-alkyl)trimellitate', 'Witamol 218 stab', 'Plasticizer', '590', 'colorless, clear liquid'], ['578 ', 'tri(2-ethylhexyl)trimellitate', 'Hexaplas OTM', 'Plasticizer', '546.8', 'colorless, clear liquid'], ['579 ', 'mixture of trioctyl and tridecyl trimellitate', 'Hexaplas L810TM', 'Plasticizer', '592', 'colorless, clear liquid'], ['580 ', 'polymer, linear, saturated phthalate', 'Uraplast W4', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['581 ', 'phthalic acid polyester', 'Ultramoll PP', 'Plasticizer', 'Unknown', 'colorless, clear, low-viscous liquid'], ['582 ', 'phthalic polyester', 'Paraplex G31', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['583 ', 'tributylphosphate', 'Freudenberg (Brunne collection)', 'Plasticizer', '266.3', 'colorless, clear liquid'], ['584 ', 'trioctylphosphate', 'Disflamoll TOF', 'Plasticizer', '434.7', 'colorless, clear liquid'], ['585 ', 'tricresylphosphate', 'Disflamoll TKP', 'Plasticizer', '416.4', 'colorless, pale-yellow, clear liquid'], ['586 ', 'trixylenylphosphate', 'Reomol TXP', 'Plasticizer', '410.5', 'colorless, clear liquid'], ['587 ', '2-ethylhexyldiphenylphosphate', 'Santicizer 141', 'Plasticizer', '362.4', 'colorless, clear, oily liquid'], ['588 ', 'i-decyldiphenylphosphate', 'Santicizer 148', 'Plasticizer', '390.5', 'colorless, clear, oily liquid'], ['589 ', 'cresyldiphenylphosphate', 'Disflamoll DPK', 'Plasticizer', '340.3', 'colorless, clear liquid'], ['590 ', '2,4-xylyldiphenylphosphate', 'Reomol CDP', 'Plasticizer', '354.4', 'colorless, clear liquid'], ['591 ', 'triphenylphosphate', 'Disflamoll TP', 'Plasticizer', '326.3', 'colorless solid'], ['592 ', 'pentadecanesulfonic acid phenol and cresol esters', 'Mesamoll', 'Plasticizer', '368.4', 'colorless, clear liquid'], ['593 ', 'phenolic ester of aliphatic sulfonic acid', 'Weichmacher KL 3-3030', 'Plasticizer', 'Unknown', 'colorless, clear liquid'], ['594 ', 'N-butylbenzenesulfonamide', 'Cetamoll BMB', 'Plasticizer', '213.3', 'colorless, clear liquid'], ['595 ', 'mixture of 0- and p-N-ethyltoluenesulfonamide', 'Isaplast 5975', 'Plasticizer', '185.24', 'viscous liquid'], ['596 ', 'N -(2-hydroxypropyl)benzenesulfonamide', 'Isaplast', 'Plasticizer', '215.27', 'viscous, clear liquid'], ['597 ', 'N,N-disubstituted fatty acid amide', 'Hallcomid M-8-10', 'Plasticizer', 'Unknown', 'yellow, clear liquid'], ['598 ', 'fatty acid ester + mineral oil + dispersant', 'Struktol WB 700, extract', 'Plasticizer', 'Unknown', 'colorless, oily liquid'], ['599 ', 'hydrophilised fatty acid ester', 'Struktol WB 222', 'Plasticizer', 'Unknown', 'colorless, soft waxy material'], ['600 ', 'hydrophilised aliphatic ester on carrier', 'Struktol KW 400', 'Plasticizer', 'Unknown', 'colorless solid'], ['601 ', 'phthalic acid ester', 'Struktol KW 500', 'Plasticizer', 'Unknown', 'colorless liquid'], ['602 ', 'aliphatic-aromatic polyester based on phthalic acid', 'Struktol WB 300', 'Plasticizer', 'Unknown', 'colorless, viscous liquid'], ['603 ', 'Short chain chlorinated paraffins', 'SCCP', 'Plasticizer/Flame Retardant', 'Unknown', 'viscous liquid'], ['604 ', 'Medium chain chlorinated paraffins', 'MCCP', 'Plasticizer', 'Unknown', 'Viscous liquid'], ['605 ', 'Long chain chlorinated paraffins', 'LCCP', 'Plasticizer', 'Unknown', 'solid'], ['606 ', 'Diisoheptylphthalate', 'DIHP', 'Plasticizer', '362.5', 'nan'], ['607 ', '1,2-Benzenedicarboxylic acid, di-C7,11-branched and linear alkyl esters,', 'DHNUP', 'Plasticizer', '362-474', 'liquid'], ['608 ', 'Benzyl butyl phthalate', 'BBP', 'Plasticizer', '312.4', 'clear colorless liquid'], ['609 ', 'Bis(2-ethylhexyl)phthalate', 'DEHP', 'Plasticizer', '390.56', 'pale yellow oily liquid'], ['610 ', 'Bis(2-methoxyethyl)phthalate', 'DMEP', 'Plasticizer', '282.29', 'oily liquid'], ['611 ', 'Dibutyl phthalate', 'DBP', 'Plasticizer', '278.34', 'Colorless oil'], ['612 ', 'Dipentyl phthalate', 'DPP', 'Plasticizer', '306.4', 'Clear, colorless liquid'], ['613 ', 'Di-(2-ethylhexyl) adipate', 'DEHA', 'Plasticizer', '370.574', 'Colorless oily liquid'], ['614 ', 'Di-octyladipate', 'DOA', 'Plasticizer', '370.574', 'Colorless oily liquid'], ['615 ', 'Diethyl phthalate', 'DEP', 'Plasticizer', '222.24', 'Colorless liquid'], ['616 ', 'Diisobutylphthalate', 'DiBP', 'Plasticizer', '278.35', 'Oily, colorless liquid'], ['617 ', 'Tris(2 chloroethyl)phosphate', 'TCEP', 'Plasticizer', '285.48', 'Clear liquid'], ['618 ', 'Dicyclohexyl phthalate', 'DCHP', 'Plasticizer', '330.418', 'White granular solid'], ['619 ', 'Benzyl butyl phthalate', 'BBP', 'Plasticizer', '312.365', 'Clear, colorless liquid'], ['620 ', 'Diheptyl adipate', 'DHA', 'Plasticizer', '342.5', 'Clear, colorless liquid'], ['621 ', 'Dihexyl adipate', 'HAD', 'Plasticizer', '314.5', 'Colorless liquid'], ['622 ', 'Heptyl octyl adipate', 'HOA', 'Plasticizer', '356.6', 'Colorless liquif'], ['623 ', 'mixture of polyglycol ether and phthalate ester', 'Atepas U', 'Viscosity modifier/Plasticizer', 'Unknown', 'yellowish, clear, viscous liquid'], ['624 ', 'substituted fatty alcohol-ethyleneoxide adduct', 'Atepas K', 'Viscosity modifier/Plasticizer', 'Unknown', 'colorless, clear, viscous'], ['625 ', 'Glass fibers', 'fiberglass', 'Reinforcements', 'Unknown', 'Clear, glass pellets'], ['626 ', 'Carbon fibers', 'Graphite fiber', 'Reinforcements', '12.01', 'Black, string-like solid'], ['627 ', 'Aramide fibers', 'Kevlar, Nomex, Twaron', 'Reinforcements', 'Unknown', 'Yellow fibers'], ['628 ', 'higher paraffinic hydrocarbons', 'Irgawax 366', 'Lubricant', 'Unknown', 'colorless, clear liquid'], ['629 ', 'paraffin wax with low melting point', 'Naftolube SP 17', 'Lubricant', 'Unknown', 'colorless solid'], ['630 ', 'paraffin wax with high melting point', 'Naftolube SP 18', 'Lubricant', 'Unknown', 'colorless solid'], ['631 ', 'hydrocarbon wax with aliphatic ester groups', 'Baerolub L-KM', 'Lubricant', 'Unknown', 'colorless solid'], ['632 ', 'polyethylene wax', 'Naftolube PEF', 'Lubricant', 'Unknown', 'colorless solid'], ['633 ', 'polyethylene wax, non-polar', 'Hoechst-Wachs PE 520', 'Lubricant', 'Unknown', 'colorless granules'], ['634 ', 'hydrogenated castor oil', 'Loxiol EP 15', 'Lubricant', '939.5', 'colorless solid'], ['635 ', 'oxidized polyethylene wax', 'Naftolube OPE', 'Lubricant', 'Unknown', 'colorless solid'], ['636 ', 'polyethylene wax, polar', 'Hostalub H 12', 'Lubricant', 'Unknown', 'colorless solid'], ['637 ', 'oxidized hydrocarbon wax', 'Baerolub L-AX', 'Lubricant', 'Unknown', 'colorless solid '], ['638 ', 'partially oxidized, partially saponified polyethylene wax', 'Irgawax 372', 'Lubricant', 'Unknown', 'yellowish solid'], ['639 ', 'cetyl-stearyl alcohol', 'Realube C/18', 'Lubricant', '513', 'colorless solid'], ['640 ', 'saturated fatty alcohol', 'Naftolube SRL', 'Lubricant', 'Unknown', 'colorless solid'], ['641 ', 'saturated fatty alcohol', 'Loxiol EP 52', 'Lubricant', 'Unknown', 'colorless solid'], ['642 ', 'saturated fatty alcohol', 'Irgawax 365', 'Lubricant', 'Unknown', 'colorless solid'], ['643 ', 'etherified poly( oxyethylene)', 'Loxiol EP 304', 'Lubricant', 'Unknown', 'almost colorless flakes'], ['644 ', 'stearic acid', 'Naftozin N', 'Lubricant/plasticizer', '284.5', 'waxy solid'], ['645 ', 'spedal stearic add', 'Ligalub Se', 'Lubricant', '284.5', 'colorless solid'], ['646 ', 'mixture of fatty acids', 'Baerolub FTA', 'Lubricant', 'Unknown', 'colorless solid'], ['647 ', 'fatty acid', 'Realube PS', 'Lubricant', 'Unknown', 'colorless solid'], ['648 ', '12-hydroxystearic acid', 'Loxiol G 21', 'Lubricant', '300.5', 'colorless solid (beaded)'], ['649 ', 'mixture of hydroxyfatty acids', 'Baerolub FTO', 'Lubricant', 'Unknown', 'colorless solid'], ['650 ', 'stearylstearate', 'Ligalub 36 Fe', 'Lubricant', '537', 'colorless solid'], ['651 ', 'C16, C18 ester wax', 'Realube SS/16-18', 'Lubricant', 'Unknown', 'colorless solid'], ['652 ', 'fatty acid ester + acid', 'Baerolub L-PO-1', 'Lubricant', 'Unknown', 'colorless, clear liquid'], ['653 ', 'aliphatic ester wax', 'Loxiol G 47', 'Lubricant', 'Unknown', 'colorless solid'], ['654 ', 'fatty acid ester', 'Baerolub L-PK', 'Lubricant', 'Unknown', 'colorless, clear liquid'], ['655 ', 'long-chain aliphatic ester', 'Realube TR', 'Lubricant', 'Unknown', 'colorless, clear liquid'], ['656 ', 'glycerol ester of unsaturated fatty acids', 'Swedlub FG-4', 'Lubricant', 'Unknown', 'colorless, clear oily liquid'], ['657 ', 'unsaturated fatty acid ester', 'Ligalub 40/1', 'Lubricant', 'Unknown', 'yellow, clear liquid'], ['658 ', 'fatty acid triglycerol ester', 'Realube SI', 'Lubricant', 'Unknown', 'colorless solid'], ['659 ', 'pentaerythrol fatty ester', 'Loxiol EP 861', 'Lubricant', 'Unknown', 'colorless solid (beaded)'], ['660 ', 'montanic ester carboxylate', 'Hostalub We 4', 'Lubricant', 'Unknown', 'yellowish solid'], ['661 ', 'complex ester of saturated fatty acids', 'Baerolub A 275', 'Lubricant', 'Unknown', 'yellowish solid'], ['662 ', 'aliphatic ester wax with some phthalate ester', 'Naftolube ELP', 'Lubricant', 'Unknown', 'colorless solid'], ['663 ', 'aliphatic ester wax + phthalate ester', 'Realube SD', 'Lubricant', 'Unknown', 'colorless solid'], ['664 ', 'ester acid carboxylate', 'Baerolub GL 5 DO', 'Lubricant', 'Unknown', 'yellowish solid'], ['665 ', 'glycerolmonostearate', 'Swedlub HG 55', 'Lubricant', '358.6', 'slightly yellowish flakes'], ['666 ', 'wax esteralcohol, partial ester of glycerol', 'Realube GMS', 'Lubricant', 'Unknown', 'colorless solid'], ['667 ', 'glycerol partial ester of saturated fatty acids', 'Baerolub L-MS', 'Lubricant', 'Unknown', 'colorless solid'], ['668 ', 'fatty acid ester with OH groups', 'Baerolub LM 4', 'Lubricant', 'Unknown', 'colorless solid'], ['669 ', 'mixture of aliphatic esteralcohols', 'Tebestat HSE 81', 'Lubricant', 'Unknown', 'yellowish, clear liquid'], ['670 ', 'glycerol partial ester of oleic acid', 'Realube GMO', 'Lubricant', 'Unknown', 'light yellowish, clear liquid'], ['671 ', 'glycerol partial ester of unsaturated fatty acid', 'Baerolub L-PL', 'Lubricant', 'Unknown', 'yellowish, clear liquid'], ['672 ', 'glycerol partial ester of unsaturated fatty acids', 'Irgawax 361', 'Lubricant', 'Unknown', 'light yellowish, clear, oily liquid'], ['673 ', 'partially esterified poly(oxyethylene)', 'Baerostat 318 S', 'Lubricant', 'Unknown', 'colorless, clear liquid'], ['674 ', 'Li stearate', 'Liga Lithiumsterat', 'Lubricant', '290.4', 'colorless solid'], ['675 ', 'linear (C28-C32) carboxylic acid, Na-salt', 'Hostamont NaV 101', 'Lubricant', 'Unknown', 'pale-yellow solid'], ['676 ', 'K stearate', 'Liga Kaliumsterat R/D', 'Lubricant', '322.6', 'colorless to yellowish solid'], ['677 ', 'K oleate', 'Liga Kaliumoleat 90%', 'Lubricant', '320.6', 'yellowish solid'], ['678 ', 'K salts of unsaturated fatty acids (predominantly K oleate)', 'Rhenodiv LE', 'Lubricant', '320.6', 'yellowish, soft paste'], ['679 ', 'Mg stearate', 'Liga Magnesiumsterat MG tech', 'Lubricant', '591.3', 'colorless solid'], ['680 ', 'Ca stearate', 'Liga Calciumsterat CA 800', 'Lubricant/Stabilizer', '607', 'colorless solid'], ['681 ', 'Ba stearate', 'Liga Bariumsterat', 'Lubricant/Stabilizer', '704.3', 'colorless solid'], ['682 ', 'K stearate', 'Liga Kaliumsterat R/D', 'Lubricant', '322.6', 'colorless to yellowish solid'], ['683 ', 'Pb stearate', 'Liga Bleistearat B 28', 'Lubricant', '774.2', 'colorless solid'], ['684 ', 'Al tristearate', 'Liga Aluminiumsterat TR', 'Lubricant/Stabilizer', '877.4', 'colorless solid'], ['685 ', 'Al di-tri-stearate', 'Liga Aluminiumsterat DT', 'Lubricant/Stabilizer', '877.4', 'colorless solid'], ['686 ', 'Al distearate', 'Liga Aluminiumsterat D2', 'Lubricant/Stabilizer', '615', 'colorless solid'], ['687 ', 'fatty amine', 'Armeen HTD', 'Lubricant', 'Unknown', 'colorless flakes'], ['688 ', 'fatty amine', 'Armeen IOD', 'Lubricant', 'Unknown', 'colorless flakes'], ['689 ', 'erucamide', 'Armid E', 'Lubricant/Antiblocking agent', '337.6', 'slightly yellowish flakes'], ['690 ', 'hydrogenated tallowamide', 'Armid HT', 'Lubricant/Antiblocking agent', 'Unknown', 'colorless flakes'], ['691 ', 'oleylamide, partially isomerized to elaidic amide', 'Loxamid OA', 'Lubricant/Slip agent', '281.5', 'colorless solid'], ['692 ', 'secondary amide wax', 'Baerolub L-AK', 'Lubricant', 'Unknown', 'colorless solid'], ['693 ', 'hydrogenated tallowamide', 'Armid HT', 'Lubricant/Antiblocking agent', '251.52', 'colorless flakes'], ['694 ', 'Erucamide', '(Z)-docos-13-enamide', 'Slip agents', '337.6', 'White solid'], ['695 ', 'Oleamide', '(Z)-Octa-9-decenamide', 'Slip agents/lubricant/corrosion inhibitor', '281.477', 'Creamy solid'], ['696 ', 'Zinc stearate', 'Zinc octadecanoate', 'Slip agents ', '632.33', 'White solid'], ['697 ', '3-(2-aminoethylamino )propyltrimethoxysilane', 'Silane A 1100', 'Adhesion agent', '222.4', 'colorless, clear liquid'], ['698 ', 'hexamethylenetetramine,1,3,5,7-tetraazaadamantane', 'Cohedur H 30', 'Adhesion agent', '140.2', 'colorless solid'], ['699 ', 'isocyanate with ester groups', 'Desmodur RE', 'Adhesion agent', 'Unknown', 'yellowish, clear liquid'], ['700 ', '20% solution of thionophosphoric acid tris-', 'Desmodur RF/E', 'Adhesion agent', '465.4', 'pale brownish yellow, clear liquid'], ['nan', '(p-isocyanatophenyl)ester in CH2Cl2', 'nan', 'nan', 'nan', 'nan'], ['701 ', 'poly( acrylic ester-co-acrylonitrile)', 'Acralen AFR', 'Adhesion agent', 'Unknown', 'yellowish, clear liquid'], ['702 ', '3-mercaptopropyltrimethoxysilane', 'Silane A 189', 'Adhesion agent/Hydrophobing agent', '196.3', 'colorless, clear liquid'], ['703 ', '3-glycidyloxypropyltrimethoxysilane', 'Silane A 186', 'Adhesion agent/Hydrophobing agent', '236.3', 'colorless, clear liquid'], ['704 ', 'H -active mixture, phenol-formaldehyde resin (resol)', 'Vulcabond E', 'Adhesion agent', 'Unknown', 'black liquid, dried (solid residue)'], ['705 ', 'azodicarboxamide', 'Porofor ADC/M Pulver', 'Blowing agent', '116.1', 'colorless solid'], ['706 ', 'azodicarbamide and activator (9:1)', 'Porofor ADC/K', 'Blowing agent', 'Unknown', 'ochre-colored solid'], ['707 ', 'benzenesulfonohydrazide', 'Porofor BSH', 'Blowing agent', '172.2', 'colorless solid'], ['708 ', "3,3' -diphenylsulfonedisulfonohydrazide", 'Porofor D 33', 'Blowing agent', '406.4', 'colorless solid'], ['709 ', 'Azodicarbonamide', 'ADCA; ADA; azoformamide', 'Blowing agents', '116.08', 'Yellow/orange/red crystalline powder'], ['710 ', 'Benzene disulphonyl hydrazide (BSH)', 'BSH', 'Blowing agents', '172.21', 'White crystalline solid'], ['711 ', 'Pentane', 'nC5', 'Blowing agents', '72.15', 'Clear liquid'], ['712 ', 'Carbon dioxide', 'CO2', 'Blowing agents', '44.01', 'Colorless gas'], ['713 ', 'ethoxylated fatty alcohol', 'Meister H 9268', 'Antistatic', 'Unknown', 'colorless liquid'], ['714 ', 'ethoxylated fatty amine', 'Hostastat FA 14', 'Antistatic', 'Unknown', 'yellowish, clear, low viscosity liquid'], ['715 ', 'fatty alcohol-ethylene oxide adduct, poly( oxyethylene)etheralcohol', 'Dehydat 3204', 'Antistatic', 'Unknown', 'colorless, clear liquid'], ['716 ', 'fatty acid-ethyleneoxide adduct, poly(oxyethylene)ester', 'Dehydat 22', 'Antistatic', 'Unknown', 'colorless, clear oily liquid'], ['717 ', 'ethoxylated fatty amine', 'Hostastat FA 18', 'Antistatic', 'Unknown', 'yellowish solid'], ['718 ', 'alkane sulfonate', 'Hostastat HS 1', 'Antistatic', 'Unknown', 'colorless solid'], ['719 ', 'quaternary ammonium compound', 'Tebestat BK', 'Antistatic', 'Unknown', 'yellow, clear liquid'], ['720 ', 'modified quaternary ammonium compound with ethyleneoxide adduct', 'Tebestat IK 39', 'Antistatic', 'Unknown', 'darkyellow, clear liquid'], ['721 ', 'laurylpyridiniumchloride', 'Dehydat C krist', 'Antistatic', '283.9', 'colorless solid'], ['722 ', 'fatty alcohol-ethyleneoxide adduct', 'Tebestat PE 1', 'Antistatic', 'Unknown', 'yellowish wax'], ['723 ', 'triallylcyanurate', 'Perkalink 300', 'Crosslinking agent', '249.3', 'colorless solid'], ['724 ', 'triallylisocyanurate', 'TAIC DL 70', 'Crosslinking agent', '249.3', 'colorless, clear liquid'], ['725 ', 'ethyleneglycoldimethacrylate', 'Perkalink 401', 'Crosslinking agent', '198.2', 'colorless, clear liquid'], ['726 ', '2-ethyl-2-hydroxymethyl-l,3-propanedioltrimethacrylate, trimethylolpropanetrimethacrylate', 'Perkalink 400', 'Crosslinking agent', '338.4', 'colorless, clear liquid'], ['727 ', 'methacrylic acid 3-trimethoxysilylpropylester', 'Silane A 174, 3-trimethoxysilylpropylmethacrylate', 'Crosslinking agent/Adhesion agent', '248.4', 'colorless, clear liquid'], ['728 ', '2,5-dimethyl-2,5-di-t-butylperoxyhexyne-3', 'Trigonox 145', 'Crosslinking agent', '296.5', 'light-yellowish, clear liquid'], ['729 ', 't-butyicumylperoxide', 'Trigonox T', 'Crosslinking agent', '208.3', 'colorless, clear liquid'], ['730 ', '1,3-bis(t-butylperoxy-2-propyl)benzene', 'Perkadox-14 S', 'Crosslinking agent', '338.5', 'colorless solid'], ['731 ', 'dicumylperoxide', 'Perkadox BC', 'Crosslinking agent', '270.4', 'colorless granules'], ['732 ', 'isocyanate with carbodiimide', 'Desmodur TT', 'Crosslinking agent/Peptizer', '348.3', 'yellowish solid'], ['733 ', 'hexamethylenediamine carbamate', 'Diak 1', 'Crosslinking agent', '160.2', 'colorless solid'], ['734 ', 'N,N-dimethylethanolamine', 'Tegoamin DMEA', 'Curing agent/Activator', '89.13', 'colorless, clear liquid'], ['735 ', 'solution of triethylenediamine in dipropyleneglycol', 'Tegoamin 33', 'Curing agent/Activator, catalyst', '101.2', 'yellowish, clear liquid'], ['736 ', 'bis(2-dimethylaminoethyl)ether in dipropyleneglycol', 'Tegoamin BDE', 'Curing agent/Activator, catalyst', '160.3', 'colorless, clear liquid'], ['737 ', 'dibutyltin carboxylate', 'Kosmos 19', 'Curing agent/Activator, catalyst', '277.96', 'yellow, clear liquid'], ['738 ', 'Sn(II) octoate', 'Kosmos 29', 'Curing agent/Activator, catalyst', '405.1', 'pale yellowish, clear liquid'], ['739 ', 'condo product of a-ethyl-~-propylacrolein and aniline', 'Vulkacit 576', 'Accelerator', '201.3', 'red-brown liquid'], ['740 ', "N,N'-diphenylguanidine", 'Vulkasit DC', 'Accelerator', '211.2', 'colorless solid'], ['741 ', '1,3-di-o-tolylguanidine', 'Vulkacit DOTG', 'Accelerator', '239.3', 'greyish solid'], ['742 ', "N ,N' -diethylthiourea", 'Perkacit DETU', 'Accelerator', '132.2', 'colorless, crystalline solid'], ['743 ', '2-imidazolidinethione, ethylenethiourea', 'Perkacit ETU', 'Accelerator', '102.2', 'colorless solid'], ['744 ', "N,N'-diphenylthiourea", 'Thenocure CA', 'Accelerator/Antioxidant', '228.3', 'colorless solid'], ['745 ', 'Zn dimethyldithiocarbamate', 'Vulkacit L', 'Accelerator', '305.8', 'colorless solid'], ['746 ', 'Te diethyldithiocarbamate', 'Perkacit TDEC', 'Accelerator', '720.6', 'yellowish, soft granules'], ['747 ', 'Zn diethyldithiocarbamate', 'Vulkacit LDA', 'Accelerator', '361.9', 'colorless solid'], ['748 ', 'Zn-dibutyldithiocarbamate', 'Perkacit ZDBC', 'Accelerator', '474.1', 'colorless solid'], ['749 ', 'Zn N-dibutydithiocarbamate', 'Vulkacit LDB/C', 'Accelerator', '474.1', 'light-grey solid'], ['750 ', 'Ni dibutyldithiocarbamate', 'Perkacit NDBC', 'Accelerator', '467.4', 'green, soft, granules'], ['751 ', 'Zn pentamethylenedithiocarbamate', 'Vulkacit ZP', 'Accelerator', '385.9', 'colorless solid'], ['752 ', 'Zn ethylphenyldithiocarbamate', 'Desmorapid DA', 'Accelerator', '458', 'colorless solid'], ['753 ', 'Zn-dibenzyldithiocarbamate', 'Perkacit ZBEC', 'Accelerator', '610.2', 'colorless solid'], ['754 ', 'tetramethylthiurammonosulfide', 'Perkacit TMTM', 'Accelerator', '208.3', 'yellowish, soft granules'], ['755 ', 'tetramethylthiuramdisulfide', 'Perkacit TMTD', 'Accelerator', '240.4', 'colorless solid'], ['756 ', 'tetraethylthiuram disulfide', 'Perkacit TETD', 'Accelerator', '296.6', 'colorless solid'], ['757 ', 'dipentamethylenethiuram tetrasulfide', 'Perkacit DPTT', 'Accelerator', '384.6', 'colorless solid'], ['758 ', 'tetraallylthiuramdisulfide', 'Freudenberg (Brunne collection)', 'Accelerator/Vulcanization agent', '344.6', 'yellowish, clear liquid'], ['759 ', 'tetrabenzylthiuramdisulfide', 'Perkacit TBZTD', 'Accelerator', '544.8', 'colorless solid'], ['760 ', 'I-methylimidazol', 'Beschleuniger DY 070', 'Accelerator', '82.09', 'colorless liquid'], ['761 ', '2-mercaptoimidazoline', 'Vulkacit NP', 'Accelerator', '102.1', 'colorless solid'], ['762 ', '2-mercaptobenzothiazole', 'Perkacit MBT', 'Accelerator', '167.2', 'colorless solid'], ['763 ', 'Zn benzothiazolemercaptide', 'Vulkacit ZM', 'Accelerator', '319.7', 'colorless solid'], ['764 ', 'bis(2-benzothiazole)disulfide', 'Perkacit MBTS', 'Accelerator', '332.5', 'slightly yellowish solid'], ['765 ', '2-( thiomorpholino) benzothiazole', 'Perkacit MBS', 'Accelerator', '224.4', 'yellowish, soft granules'], ['766 ', 'Zn diethyldithiocarbamate + mercaptobenzothiazole', 'Vulkacit MDA/C', 'Accelerator', '519', 'greyish solid'], ['767 ', '2-mercaptobenzothiazole + tetramethylthiuramdisulfide', 'Vulkacit MT/C', 'Accelerator', '407.7', 'colorless solid'], ['768 ', 'N-t-butyl-2-benzothiazolesulfenamide', 'Perkacit TBBS', 'Accelerator', '238.3', 'colorless, soft granules'], ['769 ', 'N -cyclohexyl-2-benzothiazolsulfenamide', 'Vulkacit CZ/EG-C', 'Accelerator', '264.4', 'colorless solid'], ['770 ', 'N-cyclohexyl-2-benzothiazole sulfenamide', 'Perkacit CBS', 'Accelerator', '264.4', 'colorless granules'], ['771 ', "N ,N' -dicyclohexyl-2-benzothiazolesulfenamide", 'Perkacit DCBS', 'Accelerator', '346.6', 'colorless, soft granules'], ['772 ', 'dithiophosphoric acid ester, Zn salt, on Si02', 'Rhenocure TP/S', 'Accelerator', 'Unknown', 'colorless solid'], ['773 ', 'Zn oxide (93-95% ZnO, <10 ppm PbO)', 'Zinkoxid Aktiv', 'Vulcanization Activator/Filler', '81.38', 'colorless solid'], ['774 ', 'basic Zn carbonate (70-73% ZnO, <10 ppm PbO)', 'Zinkoxid transparent', 'Vulcanization Activator/Filler', '125.4', 'colorless solid'], ['775 ', 'amorphous silicium dioxide with active organic substance', 'Aflux S', 'Vulcanization Activator', '60.09', 'colorless solid'], ['776 ', 'mixture of amorphous siliciumdioxide with surfactants', 'Rhenofit 1987', 'Vulcanization Activator', 'Unknown', 'colorless solid'], ['777 ', '4-methyl-l-piperazinepropanol', 'Freudenberg (Brunne collection)', 'Vulcanization Activator', '158.2', 'colorless, clear liquid'], ['778 ', 'N-nitrosodiphenylamine', 'Vulkalent A', 'Vulcanization Retarder', '198.2', 'solid'], ['779 ', 'aromatic-aliphatic sulfonamide', 'Vulkalent E', 'Vulcanization Retarder', 'Unknown', 'colorless solid'], ['780 ', 'N -( cyc1ohexylthio )phthalimide', 'Santogard PVI DS', 'Vulcanization Retarder', '261.3', 'colorless solid'], ['781 ', 'acetone-aniline condensation product, polymeric', 'Flectol H', 'Aging Inhibitor/Antioxidant', 'Unknown', 'light-brown solid'], ['nan', '1, 2-dihydro-2, 2, 4-trimethylquinoline', 'nan', 'nan', 'nan', 'nan'], ['782 ', "2,2' -methylene-bis( 6-t-butyl-4-methylphenol)", 'Vulkadur RB', 'Reinforcing Resin', '340.5', 'red flakes'], ['783 ', 'phenol-formaldehyde novolac with 10% hexamethylenetetramine', 'Vulkadur A', 'Intensifier', 'Unknown', 'Ochre solid'], ['784 ', 'poly(butadiene-co-styrene-co-2-vinylpyridineco-', 'Pyratex 240', 'Adhesion agent, Adhesion Improver', 'Unknown', 'yellowish, clear liquid'], ['nan', 'amide/acid)', 'nan', 'nan', 'nan', 'nan'], ['785 ', '3-chloropropyltriethoxysilane', 'Dynasylan CPTEO', 'Adhesion agent', '240.8', 'colorless, clear liquid'], ['786 ', 'pentachlorothiophenol on kaolin', 'Renacit 7', 'Peptiser, Plastificator', '282.4', 'light-grey solid'], ['787 ', 'Zn pentachlorothiophenolate on kaolin with other ingredients', 'Renacit 9', 'Peptiser', '282.4', 'colorless solid'], ['788 ', 'poly( oxyethylene )dialkylether', 'Vulcastab LW', 'Stabilizer', 'Unknown', 'colorless solid'], ['789 ', 'pentachlorothiophenol on kaolin with other ingredients', 'Renacit 7/WG', 'Peptiser', '282.4', 'grey sticks'], ['790 ', 'methacrylate copolymer', 'Baerorapid 10 F', 'Acrylate-Modifier', 'Unknown', 'white powder, free flowing'], ['791 ', 'poly( oxyethylene )-b-poly( oxypropylene)b-', 'Tegostab B404', 'General additive', 'Unknown', 'colorless, clear, viscous liquid'], ['nan', 'poly( dimethylsiloxane)', 'nan', 'nan', 'nan', 'nan'], ['792 ', 'modified silicate complex', 'Antiblocking 7831', 'Antiblocking agent', 'Unknown', 'colorless solid'], ['793 ', 'modified silicate complex', 'Antiblocking 3780', 'Antiblocking agent', 'Unknown', 'grey-white solid'], ['794 ', 'Na oleate', 'Liga Natriumoleat', 'Emulsifying agent', '304.5', 'yellowish solid'], ['795 ', 'Na stearate', 'Liga Natriumsterat R/D', 'Emulsifying agent', '306.5', 'colorless to yellowish solid'], ['796 ', 'phosphoric acid ester and ethoxylated fatty alcohol', 'Ruco-Netzer VF', 'Wetting agent', 'Unknown', 'colorless, clear liquid'], ['797 ', 'alkylpolyglycoletber and ethoxylated fatty alcohol', 'Ruco-Egalisierer RF', 'Leveling agent', 'Unknown', 'yellowish, clear liquid'], ['798 ', 'aliphatic esteralcohol', 'Verolan GBK', 'Acid-producing component', 'Unknown', 'colorless, clear liquid'], ['799 ', 'stearylamide', 'Loxamid S', 'Separating agent', '283.5', 'colorless beads'], ['800 ', 'Na oleate', 'Liga Natriumoleat', 'Emulsifying agent', '304.5', 'yellowish solid'], ['801 ', 'Na stearate', 'Liga Natriumsterat R/D', 'Emulsifying agent', '306.5', 'colorless to yellowish solid'], ['802 ', 'Hexabromobiphenyls', 'Firemaster FF-1;', 'nan', '627.6', 'White solid/tan powder'], ['nan', 'nan', 'nan', 'Flame retardant', 'nan', 'nan'], ['803 ', 'Pentachlorobenzene', 'PeCB', 'Flame retardant', '250.3', 'White/colorless crystals'], ['804 ', 'Hexachlorobenzene (ISO and DDT)', 'nan', 'Fungicide', '284.8', 'White crystalline solid'], ['nan', 'nan', 'Perchlorobenzene', 'nan', 'nan', 'nan'], ['805 ', 'Dichlorodiphenyltichloroethane (DDT)', '1,1,1-trichloro-2,2-bis(p-chlorophenyl)ethane)', 'Biocide', '354.49', 'Colorless crystalline solid'], ['806 ', 'chlorodifluoromethane', 'HCFC-22;', 'Blowing agent', '86.47', 'Colorless gas'], ['nan', 'nan', 'R-22', 'nan', 'nan', 'nan'], ['807 ', 'dichlorotrifluoroethane', 'Freon 123', 'Blowing agent', '152.93', 'Colorless gas'], ['808 ', 'dichlorofluoroethanes', 'Freon 141', 'Blowing agent', '116.94', 'Colorless liquid'], ['809 ', 'dichloropentafluoropropanes', 'Freon 225', 'Blowing agent', '202.93', 'Colorless liquid'], ['810 ', 'bromochlorodifluoromethane', 'Freon 12B1;', 'Blowing agent', '165.36', 'Colorless gas'], ['nan', 'nan', 'Halon 1211', 'nan', 'nan', 'nan'], ['811 ', 'bromotrifluoromethane', 'Halon 1301;', 'Blowing agent', '148.91', 'Colorless gas'], ['nan', 'nan', 'R13B1;', 'nan', 'nan', 'nan'], ['nan', 'nan', 'Halon 13B1;', 'nan', 'nan', 'nan'], ['nan', 'nan', 'BTM', 'nan', 'nan', 'nan'], ['812 ', 'Dibromotetrafluoroethanes', 'R-114B2;', 'Blowing agent', '259.82', 'Colorless liquid'], ['nan', 'nan', 'Halon 2402', 'nan', 'nan', 'nan'], ['813 ', '1,2,3,4,5,6-hexachlorocyclohexane (HCH (ISO))', 'Lindane;', 'Flame retardant', '290.8', 'Colorless solid'], ['nan', 'nan', 'HCH', 'nan', 'nan', 'nan'], ['814 ', 'aldrin (ISO)', '(1R,4S,4aS,5S,8R,8aR)-1,2,3,4,10,10-Hexachloro-1,4,4a,5,8,8a-hexahydro-1,4:5,8-dimethanonaphthalene', 'Biocide', '364.9', 'Colorless solid'], ['815 ', 'chlordane (ISO)', '1,2,4,5,6,7,8,8-Octachloro-3a,4,7,7a-tetrahydro-4,7-methanoindane', 'Flame retardant', '409.76', 'Thick liquid ranging from colorless to amber'], ['816 ', 'heptachlor (ISO)', '1,4,5,6,7,8,8-Heptachloro-3a,4,7,7a-tetrahydro-1H-4,7-methanoindene', 'Biocide', '373.32', 'White to tan solid'], ['817 ', 'mirex (ISO)', 'Dodecachlorooctahydro-1H-1,3,4-(epimethanetriyl)cyclobuta[cd]pentalene', 'Flame retardant', '545.55', 'White crystalline solid'], ['818 ', 'benzyl alcohol', 'Phenylmethanol', 'Plasticizer', '108.14', 'Colorless liquid'], ['819 ', 'Hydroxybenzene', 'Phenol', 'Plasticizer', '94.11', 'White crystalline solid (commercial product is clear liquid)'], ['820 ', 'diethyl ether', 'Ether', 'Plasticizer', '74.12', 'Clear liquid'], ['821 ', '4-methylpentan-2-one', 'methyl isobutyl ketone (MIBK)', 'Plasticizer', '100.16', 'Colorless liquid'], ['822 ', 'n-butyl acetate', 'Butyl ethanoate', 'Plasticizer', '116.16', 'Clear liquid'], ['823 ', 'palmitic acid', 'Hexadecanoic acid', 'Plasticizer/lubricant', '256.4', 'White crystals'], ['824 ', 'dioctyl orthophthalates', 'Vinicizer 85', 'Plasticizer', '390.6', 'Clear oily liquid'], ['825 ', 'dinonyl orthophthalates', 'Bisoflex 91', 'Plasticizer', '418.6', 'Colorless liquid'], ['826 ', 'didecyl orthophthalates', 'Vinicizer 105', 'Plasticizer', '446.7', 'Clear viscous liquid'], ['827 ', 'phthlatic anhydride', 'Isobenzofuran-1,3-dione Phthalic', 'Plasticizer', '148.1', 'White solid powder'], ['828 ', 'terephthalic acid', 'Benzene-1,4-dicarboxylic acid', 'Plasticizer', '166.13', 'White solid'], ['829 ', 'dimethyl terephthalate', '1,4-Benzenedicarboxylic acid dimethyl ester', 'Plasticizer', '194.19', 'White solid'], ['830 ', 'tris(2,3-dibromopropyl) phosphate', 'Fyrol HB 32 Tris', 'Flame retardant', '697.61', 'Pale yellow solid'], ['831 ', '2-(N,N-Diethylamino)ethylchloride hydrochloride', '2-Chloro-N,N-diethylethanamine hydrochloride', 'Biocide', '172.09', 'White crystal solid'], ['832 ', '2-(N,N-Diethylamino)ethanethiol', 'Diethylcysteamine', 'Biocide', '133.26', 'Colorless to pale orange oil'], ['833 ', 'diethyl ethylphosphonate', 'Phosphonic acid, ethyl-, diethyl ester', 'Plasticizer/Antistatic agent', '166.16', 'Colorless liquid'], ['834 ', '2,4,6-tripropyl-1,3,5,2,4,6-trioxatriphosphinane 2,4,6-trioxide', 'Propylphosphonic anhydride', 'Flame retardant', '318.18', 'Exclusively sold in ethyl acetate solution'], ['835 ', '2,2,4-trimethyl-1,2-dihydroquinoline ', 'TMQ', 'Antioxidant', '173.25', 'Dark cloudy copper-yellow colored liquid'], ['836 ', 'polychlorinated biphenyls', 'PCBs', 'Flame retardant', 'Unknown', 'Clear-yellow liquid'], ['837 ', 'polychlorinated terphenyls', 'PCTs', 'Plasticizers; flame retardants; lubricants', 'Unknown', 'Clear-yellow liquids'], ['838 ', 'polybrominated biphenyls', 'PBBs', 'Flame retardants', 'Unknown', 'White solids'], ['839 ', 'tetra-, penta-, hexa-, hepta-, octobromodiphenyl ethers', 'PBDEs (polybrominated diphenyl ethers)', 'Flame retardants', 'Unknown', 'Clear/amber/pale solids (Unknown)']]

#Creates and packs table that will contain additives
chemicalAdditivesTRVW = ttk.Treeview(my_frame6)
chemicalAdditivesTRVW.pack(padx=5, pady=5, fill='both', expand=True,side='top')

#creates columns for table
chemicalAdditiveColumns = ['#', 'Name', 'Alternate Name', 'Type', 'Molecular Weight', 'State']
chemicalAdditivesTRVW.configure(columns=chemicalAdditiveColumns)

#gets rid of dummy first column
chemicalAdditivesTRVW.column('#0', width = 0, stretch = NO)

#adds headings for each column
for column in chemicalAdditivesTRVW["columns"]:
    chemicalAdditivesTRVW.heading(column, text=column)# let the column heading = column name

#inserts data into table
count = 0
for i in chemicalAdditivesList:
       chemicalAdditivesTRVW.insert(parent ='', index ='end', iid = count, text = '', values = tuple(i))
       count +=1
       
#Creates scoll bars in (y) direction 
additivesScrollbar=ttk.Scrollbar(chemicalAdditivesTRVW, orient="vertical", command=chemicalAdditivesTRVW.yview) 
additivesScrollbar.pack(side="right", fill="y") 
# assign the scrollbars to the Treeview Widget
chemicalAdditivesTRVW.configure(yscrollcommand=additivesScrollbar.set)

#xoxo, MJC
EoLPlasticgui.mainloop()
