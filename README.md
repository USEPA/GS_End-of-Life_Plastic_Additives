# GS_End-of-Life_Plastic_Additives
This repository contains the data supporting the development of a generic analysis of current U.S. End-of-Life (EoL) processing scenarios to track and estimate environmental releases of plastic additives throughout the plastic EoL stage.

Associated Manuscript Title: A Generic Scenario Analysis of End-of-Life Plastic Management: Chemical Additives 
Submitted to: Energy and Environmental Science Journal
https://pubs.rsc.org/en/journals/journalissues/ee#!recentarticles&adv


Summary of the Project:
The increase in demands for plastics and consequently an increase in global plastics production have considerably increased the quantity of spent plastics, out of which over 90% is either landfilled or incinerated. Both methods for handling spent plastics are susceptible to releasing toxic substances, greenhouse gases, that lead to detrimental effects on air, water, soil, organisms, and public health. Chemical additives may migrate out of the original plastic under certain conditions, contaminating its surroundings and causing unwanted hazards. Therefore, improvements to the existing infrastructure for plastics management are needed to limit chemical additive release and exposure resulting from the end-of-life (EoL) stage of plastics. This work aims to develop generic EoL management scenarios to track and estimate the potential migration and releases of plastic additives throughout the plastic EoL stage. A material flow analysis of the plastic life cycle was performed using available US municipal solid waste (MSW) data to track plastics and chemical additives movement from the manufacturing phase to the EoL stage, including mechanical recycling, waste-to-energy, and landfilling. Our analysis identified the mass flow intensity, greenhouse emissions, chemical additive migration, and subsequent releases from post-consumer plastics materials under the current and hypothetical scenarios involving enhanced recycling methods such as chemical routes. The potential hazards and risks identified in this research create an opportunity to design a safer closed-loop plastic recycling infrastructure to handle chemical additives strategically and support implementing sustainable materials management efforts to transform the US plastic economy from linear to circular.


This repository contains Excel spreadsheets used to calculate material flow throughout the plastics life cycle, with strong emphasis on chemical additives in the end-of-life stages. Three major scenarios were presented with the manuscript: 1) Current plastic waste management infrastructure, 2) implementing chemical recycling to the existing plastics recycling, and 3) extracting chemical additives prior to the manufacturing stage. 

General guideline for each spreadsheet: The user would primarily modify values on the yellow tab, titled "US 2018 Facts - Sensitivity". Values highlighted in yellow may be changed for sensitivity analysis purposes. Please note that the values shown for MSW generated, recycled, incinerated, landfilled, composted, imported, exported, re-exported, and other categories in this tab were based on 2018 data. Analysis for other years can be made possible with a replicate version of this spreadsheet and the necessary data to replace those of 2018.

There are many other tabs present in all three spreadsheets, which makes first time navigation relatively confusing. However, most of the tabs, especially those that contains "Stream # - Description", do not require user interaction. They are intermediate calculations that change according to the user inputs. It is available for the user to see so that the calculation/method is transparent. The major results of these individual stream tabs are ultimately compiled into one summary tab. All streams throughout the plastics life cycle, for each respective scenario (1, 2, and 3), is shown in the "US Mat Flow Analysis 2018" tab. For each stream, we acounted the approximate mass of plastics found in MSW, additives that may be present, and nonplastics. Each spreadsheet contains a representative diagram that matches the stream label. This illustration is placed to aid the user with unnderstanding the connection between each stage in the plastics life cycle.


_____________________________________
Scenario 1 - Mechanical Recycling (Existing Recycling Infrastructure)

This hypothetical scenario predicts the effects of increasing the mechanical recycling rate on the global warming potentials, chemical additive releases, and energy footprint.109 The maximum technical feasibility of plastic recovery from the collection, sorting, and mechanical can theoretically reach a maximum recovery of 72%, as reported by Brouwer et al.113 Therefore, the recovery rate of the plastics sent for recycling could theoretically be between 0 – 72%. Plastic waste exports value was held constant at 4.5% regardless of the increase in recycling efficiency.114 Incineration and landfilling are selected as the secondary method for processing nonrecyclable plastic and were held at a constant ratio of 17.2:82.8. 

Scenario 1 spreadsheet uniquely contains Material Flow Analysis Summary, in addition the LCI. In the "Material Flow Analysis Summary" tab, we represented the input, output, releases, exposures, and greenhouse gas emissions based on the amount of materials inputted into a specific stage in the plastics life cycle. 

The "Life Cycle Inventory" tab contributes additional calculations to estimate the releases to land, air, and water. 

_____________________________________
Scenario 2 - Chemical Recycling

This hypothetical scenario examines the effects of implementing pyrolysis to treat all plastic materials that were not successfully recycled through the mechanical route on the global warming potentials, additive release into the environment, and energy footprint. Mechanical recycling remains as the primary chosen method for recycling municipal plastic waste.  All untreatable waste and solid residues resulted as a byproduct of mechanical and chemical recycling are sent to incineration and landfilling at constant ratio of 17.2:82.8. International plastic waste export remains constant  at 4.5%. 

Pyrolysis was chosen to represent the chemical recycling, with an conversion efficiency range between 60 - 95%. 
The life cycle inventory for pyrolysis process was estimated based on the values reported by Jeswani et al. 2021. The mechanical recycling efficiency was held constant at 66.7%. The pyrolysis conversion efficiency was held at 95%.

_____________________________________
Scenario 3 - Chemical additives are extracted from mechanically recycled plastics

This hypothetical scenario examines the effects of implementing an extraction technique post-mechanical recycling on global warming potentials, chemical additive releases, and energy footprint. Chemical additive extraction is promising when performed as a solid-liquid extraction with dissolution-precipitation.48 Common extraction types may include shake-flask extraction, Soxhlet extraction, ultrasonic extraction, microwave-assisted extraction, supercritical fluid extraction, accelerated solvent extraction, and dissolution-precipitation.48 The success rate of these methods is highly dependent on the additives, plastics, and extraction conditions. 

______________________________________
Figures and Data - A gs analysis on eol plastic management

This word document contains the raw data used to create all the figures in the main manuscript. The major references used to obtain the data are also included where appropriate.
