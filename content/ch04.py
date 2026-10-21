# -*- coding: utf-8 -*-
"""Chapter 4 — Extreme Heat and Urban Health."""

CH = {
    "num": 4,
    "title": "Extreme Heat and Urban Health",
    "theme": "extreme heat, urban heat islands and the physiology of heat death",
    "nsec": 10,

    "opening": [
        "Heat is the deadliest climate hazard in most years, and the least visible. A flood leaves "
        "debris, a fire leaves ash, a hurricane leaves a coastline that can be photographed from "
        "space. A heatwave leaves bodies in apartments, morgues that fill quietly, and death "
        "certificates that list cardiac arrest rather than exposure. The number of people killed "
        "by heat is therefore almost always discovered later, by epidemiologists comparing the "
        "deaths that occurred with the deaths that would have been expected, rather than by "
        "officials counting at the scene.",

        "The physical basis is simple. The human body produces heat continuously and must lose it "
        "to the environment. It does so by radiation, convection, evaporation of sweat and, to a "
        "small extent, by breathing. When air temperature approaches skin temperature, radiation "
        "and convection stop working and evaporation becomes the only route. When humidity is also "
        "high, evaporation slows, and the body's core temperature begins to rise. At a wet-bulb "
        "temperature near 35°C — the theoretical limit at which sweat can no longer cool the body "
        "— even a healthy adult at rest will overheat within hours.",

        "Cities make this worse in ways that are measurable. Concrete and asphalt absorb solar "
        "radiation during the day and release it at night, so the urban heat island is strongest "
        "after sunset, when the body most needs relief. Buildings block wind, traffic adds waste "
        "heat, and the loss of trees removes shade and transpiration. The result is that a "
        "heatwave of the same meteorological magnitude can be survivable in a village and lethal "
        "in a city, and that the difference is concentrated in the neighbourhoods with the least "
        "green cover and the oldest housing.",

        "This chapter examines heat as a physical hazard, as a physiological stress, as an urban "
        "design problem and as a public health emergency. It pays particular attention to the "
        "question that determines whether a heatwave becomes a disaster: who is exposed, who is "
        "warned, and who has somewhere cooler to go.",
    ],

    "sections": [
        {
            "num": "4.1",
            "title": "Measuring Heat: Temperature, Humidity and Wet-Bulb",
            "paras": [
                "A thermometer in the shade measures air temperature, but the body responds to a "
                "combination of temperature, humidity, wind and radiation. The heat index, familiar "
                "from weather forecasts, approximates the apparent temperature by combining "
                "temperature and relative humidity. Wet-bulb temperature goes further: it is the "
                "lowest temperature to which a surface can be cooled by evaporation, and it is the "
                "variable most closely tied to the body's ability to shed heat. A dry 45°C is "
                "dangerous; a humid 35°C wet-bulb is close to unsurvivable for more than a few "
                "hours.",

                "The theoretical limit of 35°C wet-bulb was proposed by Sherwood and Huber (2010) "
                "on the basis of a resting metabolic rate. Laboratory work since then has found "
                "that the critical wet-bulb temperature for healthy young adults at rest is closer "
                "to 31°C, and lower still during light activity (Vecellio, Wolf, Cottle and "
                "Kenney, 2022). Older people, people with cardiovascular disease, pregnant women "
                "and children reach their limits earlier. The practical implication is that "
                "conditions once considered rare are already occurring in South Asia and the "
                "Persian Gulf, and that the margin between discomfort and death is narrower than "
                "the 35°C figure suggests.",

                "Heat is also cumulative. A single hot day is survivable; a week of hot nights is "
                "not, because sleep is when the body recovers. Public health agencies therefore "
                "increasingly report heat in terms of consecutive days above a threshold, or "
                "degree-days, rather than daily maxima. The distinction matters for warnings: a "
                "forecast of 40°C for one afternoon is a different emergency from a forecast of "
                "35°C for seven consecutive days with nights above 28°C.",
            ],
        },
        {
            "num": "4.2",
            "title": "The Physiology of Heat Illness",
            "paras": [
                "Heat illness progresses along a continuum. Heat cramps are painful muscle spasms "
                "caused by salt loss; heat exhaustion produces weakness, dizziness, headache and "
                "nausea as blood pools in the skin and the heart struggles to maintain blood "
                "pressure; heatstroke occurs when the core temperature exceeds about 40°C and the "
                "body's thermoregulation fails. Heatstroke is a medical emergency with a mortality "
                "rate that can exceed 50 per cent if cooling is delayed, and it can leave survivors "
                "with permanent neurological damage.",

                "The pathway to death is often cardiovascular rather than thermal. During a "
                "heatwave, the heart works harder to pump blood to the skin for cooling, while "
                "sweating reduces blood volume. People with narrowed coronary arteries, heart "
                "failure or kidney disease can die of a heart attack or kidney failure without "
                "ever reaching the temperature that defines heatstroke. This is why excess "
                "mortality during heatwaves is dominated by cardiovascular and respiratory causes, "
                "and why death certificates rarely mention heat.",

                "Certain medications increase risk. Diuretics reduce blood volume; beta-blockers "
                "limit the heart's ability to increase output; anticholinergics reduce sweating; "
                "some antidepressants impair the perception of thirst. People who live alone may "
                "not notice the onset of symptoms, and people with dementia may not be able to "
                "seek help. The physiological and the social therefore combine: the same "
                "temperature that causes discomfort in a healthy adult can be lethal to an "
                "isolated elderly person on the top floor of a building without shade.",
            ],
        },
        {
            "num": "4.3",
            "title": "The Urban Heat Island",
            "paras": [
                "The urban heat island is one of the best-documented effects of human settlement. "
                "Cities are typically 3 to 7°C warmer than their rural surroundings during the "
                "day and can be more than 10°C warmer at night. The causes are well understood: "
                "dark surfaces absorb more solar radiation, buildings have a high thermal mass and "
                "release heat slowly, the geometry of streets traps radiation, vehicles and "
                "air-conditioning units release waste heat, and vegetation that would otherwise "
                "cool the air through transpiration is scarce.",

                "The intensity varies enormously within a single city. Satellite measurements of "
                "land surface temperature in Jakarta, Delhi, Manila and São Paulo show differences "
                "of 5 to 10°C between neighbourhoods a few kilometres apart, with the hottest "
                "areas corresponding to dense informal settlements, industrial zones and bare "
                "ground, and the coolest to parks, tree-lined streets and water bodies. Because "
                "these differences track income, the urban heat island is also a map of "
                "inequality: the people with the least capacity to buy cooling live in the "
                "hottest places.",

                "Urban form determines how the heat island will change. A city that grows through "
                "sprawl with dark roofs and wide asphalt roads will intensify it; a city that "
                "protects green space, plants street trees, uses reflective materials and preserves "
                "ventilation corridors can keep it in check even as the climate warms. The "
                "decisions are made in building codes, zoning rules and investment plans, which is "
                "why heat policy is inseparable from urban planning.",
            ],
        },
        {
            "num": "4.4",
            "title": "Who Dies in a Heatwave",
            "paras": [
                "The epidemiology of heat mortality is remarkably consistent across countries. The "
                "elderly account for the majority of deaths, particularly those over 75 and those "
                "living alone. People with pre-existing cardiovascular, respiratory, renal or "
                "psychiatric conditions are at elevated risk. Outdoor workers, construction "
                "labourers, agricultural workers and delivery riders are exposed to the highest "
                "temperatures for the longest periods. Homeless people, prisoners, refugees and "
                "people in informal settlements are exposed both to heat and to the absence of "
                "cooling.",

                "The Chicago heatwave of July 1995 is the canonical study. More than 700 people "
                "died in five days, most of them in their homes, and the distribution was not "
                "explained by temperature alone. Eric Klinenberg's social autopsy found that "
                "neighbourhoods with similar demographics and similar temperatures had very "
                "different death rates, and that the difference was associated with social "
                "isolation, fear of crime, and the quality of the local social infrastructure — "
                "whether people knew their neighbours, whether they trusted the city, whether they "
                "were willing to leave their apartments (Klinenberg, 2002).",

                "The European heatwave of August 2003 killed an estimated 70,000 people, with "
                "France alone accounting for nearly 15,000. The deaths were concentrated among the "
                "elderly, many of whom were left in apartments without air conditioning while "
                "their families were on holiday, and the crisis exposed the absence of a public "
                "health plan for heat. The 2022 European summer, by contrast, killed about 61,700 "
                "people despite a much better warning system, which suggests that warnings alone "
                "are insufficient when the underlying vulnerability remains (Ballester et al., "
                "2023).",
            ],
        },
        {
            "num": "4.5",
            "title": "Counting the Dead: Excess Mortality",
            "paras": [
                "Heat deaths are counted by comparing the number of deaths observed during a "
                "heatwave with the number expected from historical averages for the same period. "
                "The difference is excess mortality. The method is robust to the misclassification "
                "of individual death certificates, because it does not require the certifier to "
                "recognise heat as a cause; it only requires that the total number of deaths be "
                "counted accurately. This is why epidemiological estimates of heat deaths are "
                "usually much higher than official counts.",

                "The method has limitations. Heat can displace deaths that would have occurred "
                "within weeks — a phenomenon known as mortality displacement, or harvesting — which "
                "means that a heatwave may accelerate deaths rather than cause them. Studies "
                "generally find that displacement accounts for a minority of excess deaths, "
                "especially for severe heatwaves, but the size of the effect is contested. "
                "Excess mortality also captures deaths from other causes that rise during "
                "heatwaves, such as heart attacks and kidney failure, which may not be recorded as "
                "heat-related.",

                "The global burden is large. The Lancet Countdown estimates that heat-related "
                "mortality among people over 65 has increased by about 70 per cent since the early "
                "1990s, and that more than 500,000 deaths a year are associated with heat. The "
                "figure is an estimate, not a count, and it depends on assumptions about "
                "temperature-mortality relationships that vary by location. But the direction is "
                "unambiguous, and the trend is one of the clearest signals that climate change is "
                "already affecting human health.",
            ],
        },
        {
            "num": "4.6",
            "title": "Heat Action Plans and Early Warning",
            "paras": [
                "Ahmedabad, India, adopted one of the first heat action plans in South Asia after a "
                "2010 heatwave killed more than 1,300 people. The plan combines a colour-coded "
                "forecast system, cooling centres in public buildings, adjusted working hours for "
                "outdoor labourers, water distribution, and outreach to slum communities through "
                "community health workers. An evaluation published in 2018 estimated that the plan "
                "had prevented about 1,190 deaths a year, though the authors cautioned that the "
                "estimate depended on assumptions about the counterfactual (Hess et al., 2018).",

                "The components of an effective plan are now fairly standard. A warning system "
                "that triggers specific actions at specific thresholds; a communication strategy "
                "that reaches people in their own languages through channels they trust; a "
                "registry of vulnerable people, particularly the elderly living alone; designated "
                "cooling spaces that are open, accessible and free; and a protocol for hospitals "
                "and emergency services to prepare for surges. The weakest link is usually the "
                "last mile: the warning exists, but the person at risk does not hear it, cannot "
                "act on it, or has nowhere to go.",

                "Plans also fail when they are designed for the wrong hazard. A plan built around "
                "daily maximum temperature will miss a heatwave with moderate daytime temperatures "
                "and very hot nights, which is precisely the pattern that kills in humid cities. "
                "Plans built around a single city will miss rural workers and informal settlements "
                "outside the administrative boundary. And plans that are not rehearsed will not be "
                "implemented when the emergency arrives, because the agencies involved will be "
                "learning their roles in real time.",
            ],
        },
        {
            "num": "4.7",
            "title": "Heat at Work: Productivity and Labour",
            "paras": [
                "Heat affects economies through labour as well as through death. The International "
                "Labour Organization estimates that heat stress already reduces global working "
                "hours by about 2.2 per cent, equivalent to 80 million full-time jobs, and that "
                "the loss could rise to 2.4 per cent by 2030 under a high-emission scenario. "
                "Agriculture accounts for about 60 per cent of the lost hours, followed by "
                "construction and industry. The losses are concentrated in South Asia, Sub-Saharan "
                "Africa and Southeast Asia, where outdoor work is common and cooling is scarce.",

                "The mechanism is physiological. Above about 26°C wet-bulb, the body must divert "
                "blood to the skin to dissipate heat, which reduces the blood available to "
                "muscles and the brain. Physical capacity declines, error rates rise, and the risk "
                "of accidents increases. Workers adapt by taking breaks, shifting hours to early "
                "morning or night, and drinking more water, but these adaptations have limits, and "
                "they are often unavailable to workers paid by output rather than by time.",

                "The economic consequence is not only lost output but lost income. A construction "
                "worker who cannot work during the hottest hours loses a fraction of daily wages; "
                "a farmer whose crop fails loses a season. Because informal workers rarely have "
                "heat insurance or sick leave, the cost is transferred to the household. Heat "
                "policy is therefore also labour policy, and the most effective interventions "
                "often involve collective bargaining, enforceable rest breaks and access to "
                "shade and water on site.",
            ],
        },
        {
            "num": "4.8",
            "title": "Cooling, Energy and Equity",
            "paras": [
                "Air conditioning saves lives, and its spread is one of the reasons heat mortality "
                "has fallen in high-income countries even as heatwaves have become more severe. "
                "The International Energy Agency counted about 1.6 billion air-conditioning units "
                "in 2016 and projected that the number could reach 5.6 billion by 2050, with most "
                "of the growth in developing countries. Cooling already accounts for about a tenth "
                "of global electricity consumption, and demand peaks during exactly the hours when "
                "the grid is most stressed.",

                "The equity problem is that the people who most need cooling are least able to "
                "afford it. In many cities, electricity is unreliable, the upfront cost of an air "
                "conditioner is prohibitive, and landlords do not pay for efficiency improvements. "
                "Passive cooling — shade, insulation, reflective roofs, cross-ventilation, "
                "courtyards, trees — is cheaper and does not increase emissions, but it requires "
                "design decisions that are locked in for decades and is difficult to retrofit into "
                "informal housing.",

                "There is also a feedback loop. Air conditioning releases waste heat into the "
                "street, raising the outdoor temperature and increasing the demand for cooling in "
                "neighbouring buildings. The effect is small relative to the heat island but "
                "measurable in dense districts. The solution is not to discourage cooling but to "
                "combine it with efficiency standards, building codes, urban greening and "
                "protection for people who cannot pay — a package that treats cooling as "
                "infrastructure rather than as a consumer good.",
            ],
        },
        {
            "num": "4.9",
            "title": "Designing Cooler Cities",
            "paras": [
                "Urban heat can be reduced by design, and the interventions are well understood. "
                "Street trees are the most effective single measure: a mature canopy can lower "
                "surface temperature by 10 to 15°C and air temperature by 2 to 4°C within its "
                "shade. Reflective roofs and pavements raise albedo and reduce heat absorption. "
                "Green roofs and walls insulate buildings and cool the air through transpiration. "
                "Water features, parks and ventilation corridors allow cool air to move through "
                "the city.",

                "The evidence base has improved. A study of 601 European cities estimated that "
                "increasing tree cover to 30 per cent could have prevented about 2,600 heat deaths "
                "a year, roughly a third of the total, and that the benefit was largest in "
                "southern and eastern Europe (Iungman et al., 2023). Modelling of US cities found "
                "that reflective roofs and street trees could reduce afternoon temperatures by "
                "1.5 to 3°C in dense neighbourhoods. The interventions pay for themselves through "
                "reduced cooling demand, improved air quality and lower mortality.",

                "The obstacle is not knowledge but implementation. Trees take decades to mature, "
                "compete for space with utilities and parking, and require maintenance that "
                "municipal budgets often lack. Reflective roofs need building codes that are "
                "enforced. Ventilation corridors need planning rules that resist the pressure to "
                "build on every open space. The cities that succeed tend to have a dedicated heat "
                "office, a long-term budget and a political constituency that treats heat as a "
                "public health issue rather than an inconvenience.",
            ],
        },
        {
            "num": "4.10",
            "title": "The Limits of Adaptation",
            "paras": [
                "Adaptation to heat has real limits. Once wet-bulb temperatures approach the "
                "physiological threshold, no amount of shading, cooling or behaviour change can "
                "make outdoor work safe, and even indoor spaces without mechanical cooling become "
                "lethal. The regions most exposed — the Indus Valley, the Persian Gulf, the North "
                "China Plain, parts of West Africa — are also regions with large populations, "
                "limited air conditioning and fragile grids. In those places, adaptation buys time "
                "but does not remove the hazard.",

                "The second limit is economic. Cooling for everyone would require a massive "
                "expansion of electricity generation, much of which would need to be low-carbon to "
                "avoid worsening the problem it addresses. The International Energy Agency "
                "estimates that efficient cooling could halve the growth in demand relative to a "
                "business-as-usual path, but efficiency requires standards, financing and "
                "enforcement that many countries lack. The third limit is behavioural: people "
                "underestimate their own vulnerability, especially if they have survived previous "
                "heatwaves, and warnings that are repeated without visible consequences lose "
                "credibility.",

                "These limits do not make adaptation pointless. They define the boundary between "
                "what can be managed and what must be prevented. A city that plants trees, "
                "insulates homes, protects outdoor workers and opens cooling centres can prevent "
                "most heat deaths at 1.5°C or 2°C of warming. At 3°C or 4°C, the same city will "
                "face conditions that no amount of planning can fully offset. That is why heat "
                "policy must be paired with emission reduction: adaptation and mitigation are not "
                "alternatives but two halves of the same decision.",
            ],
        },
    ],

    "case": {
        "title": "Case Study: The European Summer of 2022",
        "paras": [
            "The summer of 2022 was the hottest in Europe since records began, and it was "
            "preceded by a spring drought that had already lowered rivers and dried soils. "
            "Temperatures exceeded 40°C in Britain for the first time, reached 47°C in Portugal, "
            "and persisted across the Mediterranean for weeks. Wildfires burned more than 800,000 "
            "hectares across the continent, the largest area in the European record, and the "
            "combined effect of heat and drought reduced maize and sunflower harvests by "
            "double-digit percentages.",

            "The mortality estimate published in Nature Medicine attributed about 61,700 deaths to "
            "the summer, with the highest numbers in Italy, Spain, Germany and France (Ballester "
            "et al., 2023). The figure was lower than the 70,000 of 2003 in absolute terms, but the "
            "summer was hotter, which suggests that adaptation had reduced the death rate per "
            "degree even as the absolute burden remained enormous. The authors noted that the "
            "estimate depended on the choice of temperature-mortality model and that the true "
            "figure could be higher.",

            "The pattern of deaths revealed the limits of adaptation. Most deaths occurred among "
            "people over 75, many with cardiovascular or respiratory disease, and many in "
            "households without air conditioning. Southern European countries with older housing "
            "stock and less air conditioning had higher death rates than northern countries with "
            "cooler climates but better building standards. The lesson is that vulnerability is "
            "not simply a function of latitude: it is a function of housing, income, age structure "
            "and the presence of a plan.",

            "The policy response varied. France, which had built a national heat plan after 2003, "
            "activated a colour-coded alert system, opened cooling centres and sent text messages "
            "to vulnerable households. Spain and Italy introduced restrictions on outdoor work "
            "during the hottest hours. Britain, which had no comparable plan, declared a national "
            "emergency for the first time and cancelled appointments at hospitals that were "
            "already under pressure. The differences in outcome are difficult to isolate because "
            "many factors changed at once, but the comparison suggests that plans reduce deaths "
            "when they are specific, funded and rehearsed.",

            "The summer also exposed the interaction between heat and other systems. Railways "
            "buckled in Britain, nuclear plants in France reduced output because river water was "
            "too warm for cooling, and hospitals cancelled surgeries because operating theatres "
            "could not be kept cool. These failures were not caused by the temperature itself but "
            "by infrastructure designed for a cooler climate. They illustrate the central point of "
            "this chapter: heat becomes a disaster when it encounters systems that were not built "
            "to tolerate it.",

            "For planners, the case suggests three priorities. The first is to treat heat as a "
            "health emergency with a dedicated budget, not as a weather inconvenience. The second "
            "is to identify the people at risk before the heatwave, through registries of elderly "
            "and isolated residents, rather than trying to find them during it. The third is to "
            "protect the infrastructure that heat disables — power, water, transport, hospitals — "
            "because a heatwave that shuts down the grid becomes a different and much larger "
            "emergency.",
        ],
    },

    "future": {
        "title": "Future Scenarios and Predictions: Heat in a Warmer World",
        "paras": [
            "The historical record shows a clear trend. The number of days with extreme heat has "
            "increased on every continent, the frequency of heatwaves has risen by a factor of "
            "roughly three since the 1950s, and the hottest year on record has been exceeded "
            "repeatedly in the past decade. Heat mortality has risen with it: the Lancet Countdown "
            "estimates that heat deaths among people over 65 have increased by about 70 per cent "
            "since the 1990s, and that the trend is accelerating in Europe and South Asia.",

            "Present conditions vary enormously by place. In Delhi, the summer of 2024 produced "
            "weeks of temperatures above 45°C and a record electricity demand; in Jakarta, the "
            "combination of high humidity and a strong urban heat island produces wet-bulb "
            "conditions that are already dangerous for outdoor workers; in Karachi, the 2015 "
            "heatwave killed more than 1,200 people in a city where many neighbourhoods lack "
            "reliable water and power. These are not future scenarios. They are the baseline from "
            "which the projections begin.",

            "The assumptions that drive the projections are therefore about adaptation as much as "
            "about emissions. If cities invest in shade, cooling, warning systems and housing, "
            "mortality can fall even as temperatures rise. If they do not, mortality will rise "
            "faster than the temperature because exposure is growing with urbanisation and ageing. "
            "The scenarios below combine the two: they show what happens to heat risk under "
            "different emission paths and different levels of adaptive investment.",
        ],
        "table": {
            "caption": "Table 4.1 Heat exposure in selected cities, present and 2050",
            "head": ["City", "Days above 35°C now", "Days above 35°C in 2050 (SSP2-4.5)", "Wet-bulb risk", "Critical adaptation"],
            "rows": [
                ["Delhi", "~100", "~140", "High in monsoon", "Cooling centres; outdoor work bans"],
                ["Karachi", "~60", "~100", "Very high", "Water supply; power reliability"],
                ["Jakarta", "~30", "~70", "Very high", "Shade; drainage; social housing"],
                ["Lagos", "~20", "~60", "High", "Grid; informal settlement upgrading"],
                ["Athens", "~30", "~55", "Moderate", "Building codes; tree canopy"],
                ["Phoenix", "~110", "~150", "Low but extreme", "Cooling for homeless; grid capacity"],
            ],
        },
        "after_table": [
            "Two conclusions follow. The first is that heat risk is not determined by temperature "
            "alone: the same number of hot days produces very different mortality depending on "
            "housing, water, power and social protection. The second is that the largest gains "
            "come from interventions that are boring and cheap — shade, water, warnings, "
            "check-ins on elderly neighbours — rather than from technologies that are expensive "
            "and unproven. A city that does the boring things well can save thousands of lives at "
            "1.5°C and still save many at 2.5°C, though the margin narrows.",

            "What would change these conclusions? A breakthrough in cheap, efficient cooling would "
            "reduce mortality in hot countries but would increase electricity demand and "
            "emissions unless it were paired with clean generation. A collapse of the power grid "
            "during a heatwave would turn a manageable event into a catastrophe, as happened in "
            "Texas in 2021 and in India in 2012. And a wet-bulb event above the physiological "
            "threshold would create a situation in which adaptation is impossible and only "
            "evacuation remains.",
        ],
    },
}
