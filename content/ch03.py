# -*- coding: utf-8 -*-
"""Bab 3 — Sistem Iklim, Umpan Balik dan Pemantauan (versi dalam, bahasa Inggris)."""

CH = {
    "num": 3,
    "title": "Climate Systems, Feedbacks and Monitoring",
    "theme": "climate systems, feedback mechanisms and monitoring",
    "nsec": 10,

    "opening": [
        "A climate is not a temperature. It is a machine with several moving parts — an "
        "atmosphere, an ocean, a cryosphere, a biosphere and a land surface — coupled so tightly "
        "that a change in one is felt in all the others, usually after a delay. The atmosphere "
        "responds in days, the ocean in decades, the ice sheets in centuries. This difference in "
        "response time is the single most important fact for anyone trying to understand why the "
        "consequences of emissions arrive long after the emissions themselves, and why some of "
        "those consequences cannot be reversed on any timetable that matters to the people "
        "experiencing them.",

        "The couplings also explain why the climate does not warm smoothly. Heat stored in the "
        "ocean can be released years later; a shift in wind patterns can cool a continent for a "
        "decade while the planet as a whole warms; a volcanic eruption can suppress global "
        "temperature for two or three years. These internal variations are not noise in the sense "
        "of meaningless — they are the weather of the climate system, and they determine whether "
        "a particular harvest fails or survives, whether a particular city floods this year or "
        "next.",

        "Feedback is the mechanism that turns a small push into a large response, or a large push "
        "into a small one. Warming increases atmospheric water vapour, which is itself a "
        "greenhouse gas, which produces more warming; that is a positive feedback, and it roughly "
        "doubles the effect of carbon dioxide alone. Warming melts reflective ice, exposing dark "
        "ocean that absorbs more sunlight; another positive feedback. But warming also increases "
        "the radiation the planet emits to space, which is a negative feedback and the reason the "
        "system has not run away. The balance between these effects, not the strength of any one "
        "of them, determines how sensitive the climate is.",

        "This chapter is about that balance, about the thresholds where it can change abruptly, "
        "and about the instruments that allow us to watch it happen. It closes with the least "
        "glamorous and most consequential subject in climate science: data quality, and the "
        "question of what a measurement can and cannot tell you.",
    ],

    "sections": [
        {
            "num": "3.1",
            "title": "The Climate System",
            "paras": [
                "The Earth receives about 340 watts of solar energy for every square metre of its "
                "surface, averaged over day and night and over the seasons. Roughly thirty per "
                "cent of that is reflected back to space by clouds, ice and bright surfaces — the "
                "albedo — and the remainder is absorbed by the atmosphere, the ocean and the land. "
                "Because the planet is neither heating nor cooling catastrophically on human "
                "timescales, the energy leaving must roughly equal the energy arriving. The "
                "greenhouse effect works by slowing the departure, not by adding energy; the "
                "system compensates by warming until the outgoing radiation again balances the "
                "incoming sunlight (Trenberth, Fasullo and Kiehl, 2009).",

                "What makes the system complicated is that its components have different memories. "
                "The atmosphere forgets a temperature anomaly within weeks; the surface ocean "
                "remembers it for months to years; the deep ocean for centuries; an ice sheet for "
                "millennia. A pulse of heat injected into the atmosphere is therefore partitioned: "
                "some escapes to space immediately, some is absorbed by the ocean and returned "
                "decades later, and some is consumed melting ice. The same is true of carbon "
                "dioxide, which is exchanged continuously among the atmosphere, the biosphere and "
                "the ocean, with a small fraction remaining airborne for thousands of years.",

                "The practical consequence is that the climate responds to a change in forcing with "
                "a lag that depends on the component being observed. Surface temperature responds "
                "within a few years, sea level over centuries, and ice sheets over millennia. "
                "Policymakers who expect a rapid visible response to emission cuts are therefore "
                "looking at the wrong variable; the response is real but it arrives first in the "
                "ocean and only later at the coast.",
            ],
        },
        {
            "num": "3.2",
            "title": "Atmosphere and Ocean Circulation",
            "paras": [
                "The atmosphere moves heat from the tropics toward the poles through three great "
                "cells in each hemisphere: the Hadley cell, which lifts moist air at the equator "
                "and brings it down over the subtropics; the Ferrel cell, which drives the "
                "mid-latitude westerlies; and the polar cell. The boundaries between these cells "
                "are where the jet streams run, and the position of the jets determines whether a "
                "winter storm reaches Lisbon or stalls over the North Sea. As the tropics warm "
                "faster than the poles, the temperature gradient weakens and the jets tend to shift "
                "poleward, though the effect is uneven and remains an active research question "
                "(IPCC, 2021, Chapter 4).",

                "The ocean moves heat in parallel, and more slowly. The Atlantic Meridional "
                "Overturning Circulation carries warm surface water northward, cools it in the "
                "Nordic seas, and returns it southward as cold, dense deep water; the Gulf Stream "
                "is its most visible surface expression. The circulation transports roughly "
                "eighteen million cubic metres of water per second — about a hundred times the "
                "flow of the Amazon — and delivers heat to Europe that helps keep its winters "
                "milder than those of comparable latitudes in Canada. It is driven by differences "
                "in temperature and salinity, which is why added freshwater from Greenland's "
                "melting ice is watched so closely.",

                "Superimposed on these steady circulations are oscillations: the El Niño–Southern "
                "Oscillation, which shifts heat across the tropical Pacific every two to seven "
                "years and alters rainfall from Peru to Indonesia; the North Atlantic Oscillation, "
                "which governs European winter weather; the Indian Ocean Dipole; the Southern "
                "Annular Mode. These patterns do not create the long-term trend, but they "
                "determine which years are hot, which are wet, and where the damage falls.",
            ],
        },
        {
            "num": "3.3",
            "title": "Positive and Negative Feedback Loops",
            "paras": [
                "The largest feedback is also the least visible. Warmer air holds more water "
                "vapour — about seven per cent more for each degree of warming, following the "
                "Clausius–Clapeyron relation — and water vapour is a powerful greenhouse gas. The "
                "increase in water vapour roughly doubles the warming that carbon dioxide would "
                "produce on its own, which is why the climate sensitivity to a doubling of CO2 is "
                "about three degrees rather than one and a half. This is not a speculative "
                "mechanism; it is measured, and it is the reason the same physics that gives a "
                "modest direct effect gives a large total one (IPCC, 2021, Chapter 7).",

                "Ice and snow provide a second positive feedback. White surfaces reflect sunlight; "
                "dark ocean and dark land absorb it. When ice retreats, the newly exposed surface "
                "absorbs more energy, which warms the region, which melts more ice. The feedback is "
                "strongest in the Arctic, where it contributes to the three- to fourfold "
                "amplification of warming relative to the global mean. A third comes from the "
                "carbon cycle: warming increases the respiration of soil microbes and the "
                "frequency of fire, releasing carbon that had been stored, which produces further "
                "warming.",

                "Against these stand the negative feedbacks that keep the system stable. The "
                "planet radiates more energy as it warms, following the Stefan–Boltzmann law; the "
                "lapse rate — the rate at which temperature falls with altitude — adjusts in a way "
                "that damps the response in the tropics; and increased weathering of silicate "
                "rocks removes carbon dioxide from the atmosphere over geological time. Clouds are "
                "the great uncertainty: low clouds reflect sunlight and cool, high clouds trap heat "
                "and warm, and how their balance changes with warming remains the largest single "
                "source of spread among climate models.",
            ],
        },
        {
            "num": "3.4",
            "title": "Tipping Points and Abrupt Change",
            "paras": [
                "Some parts of the climate system do not respond gradually. They behave like a "
                "see-saw held just past its balance point: a small additional push produces a "
                "large, rapid and often irreversible change. Researchers call these tipping "
                "elements, and a 2022 assessment identified sixteen of them, including the "
                "Greenland and West Antarctic ice sheets, the Atlantic overturning circulation, "
                "the Amazon rainforest, boreal permafrost and warm-water coral reefs (Armstrong "
                "McKay et al., 2022). The assessment found that several would be at risk at "
                "warming levels between 1.5 and 2°C, which is to say within the range that current "
                "policies are likely to produce.",

                "The concept is easy to misunderstand. A tipping point is not a cliff edge at a "
                "precise temperature; it is a region of the parameter space in which the system "
                "loses stability, and the exact location is uncertain because the systems are "
                "complex and poorly observed. Nor does crossing a threshold always produce an "
                "instantaneous change: the Greenland ice sheet may take centuries to disappear "
                "once committed, and the Amazon may degrade over decades through fire and "
                "drought. What changes at the threshold is not the speed of the change but its "
                "reversibility.",

                "The policy implication is asymmetric. If the system were linear, overshooting a "
                "target and returning later would be an acceptable strategy. If it contains "
                "thresholds, overshoot becomes a gamble with a permanent loss on the other side. "
                "That asymmetry, rather than any single temperature number, is the strongest "
                "argument for treating 1.5°C as a limit to be approached with caution rather than "
                "a target to be traded against other priorities.",
            ],
        },
        {
            "num": "3.5",
            "title": "Temperature and Satellite Monitoring",
            "paras": [
                "The global temperature record is assembled from about thirty thousand land "
                "stations, several thousand ships and buoys, and a handful of satellite "
                "instruments, all processed by four independent groups using different methods. "
                "Satellites have measured the temperature of the lower troposphere since 1979, "
                "first with microwave sounders and later with infrared interferometers; they "
                "provide global coverage but suffer from orbital drift, calibration changes and "
                "the difficulty of separating the signal of the lower atmosphere from that of the "
                "surface. Reanalysis products, which combine observations with a weather model, "
                "fill the gaps and provide consistent fields of temperature, wind and humidity "
                "over the whole planet (Hersbach et al., 2020).",

                "Each system has a characteristic error. Surface stations are precise but unevenly "
                "distributed, with dense coverage in Europe and North America and sparse coverage "
                "in parts of Africa and South America. Satellites are uniform but indirect, "
                "measuring radiance rather than temperature and requiring a radiative transfer "
                "model to convert one into the other. Reanalyses are complete but inherit the "
                "biases of their models. The skill of the system comes from the disagreement: when "
                "independent methods converge, the result is robust; when they diverge, the "
                "divergence points to a problem worth investigating.",

                "The architecture of that system is itself a policy achievement. The Global "
                "Climate Observing System, established in 1992, sets standards for instruments, "
                "data exchange and continuity, and the Paris Agreement's transparency framework "
                "depends on it. When a country reports its emissions or its progress, it relies on "
                "measurements that are only credible because they are comparable across borders. "
                "Monitoring, in other words, is not a technical appendix to climate policy; it is "
                "the infrastructure that makes policy verifiable.",
            ],
        },
        {
            "num": "3.6",
            "title": "Ocean and Ice Monitoring",
            "paras": [
                "The ocean was, until recently, the least observed part of the climate system — a "
                "gap that mattered because it stores more than ninety per cent of the excess heat. "
                "That changed with Argo, an international programme that began deploying "
                "autonomous profiling floats in 2000 and now maintains roughly four thousand of "
                "them. Each float sinks to two thousand metres, measures temperature and salinity "
                "as it rises, transmits its data by satellite and repeats the cycle every ten "
                "days. The result is a three-dimensional picture of the ocean's heat content, "
                "updated continuously, available to anyone with an internet connection.",

                "Ice is observed by a different combination of instruments. Satellite altimetry, "
                "which has measured sea surface height since 1992, also measures the height of ice "
                "sheets; the GRACE mission, launched in 2002, weighs them by detecting tiny changes "
                "in the Earth's gravity field. Radar and laser altimeters measure thinning, and "
                "microwave sensors map the extent of sea ice every day. Each method has blind "
                "spots — altimetry struggles at the steep margins of ice sheets, gravity missions "
                "have coarse spatial resolution — but together they have produced a consistent "
                "picture of accelerating loss (Shepherd et al., 2020).",

                "The data from these systems are open, which is unusual for expensive "
                "infrastructure and essential for credibility. A government that disputes a "
                "sea-level projection can download the altimetry, the tide-gauge record and the "
                "gravity data and check the arithmetic itself. That openness does not settle "
                "political disputes, but it narrows the space in which they can be conducted by "
                "assertion rather than evidence.",
            ],
        },
        {
            "num": "3.7",
            "title": "Extreme Event Attribution",
            "paras": [
                "Attribution began with a question about a single heatwave. After the European "
                "summer of 2003 killed tens of thousands of people, a team led by Peter Stott "
                "asked whether the probability of such an event had changed because of human "
                "influence, and answered by comparing model simulations with and without "
                "greenhouse gases (Stott, Stone and Allen, 2004). The answer — that the risk had "
                "roughly doubled — established a method that has since been applied to hundreds of "
                "events, from the Russian heatwave of 2010 to the floods of 2022 in Pakistan.",

                "The method has become faster and more standardised. The World Weather "
                "Attribution group, founded in 2014, now produces rapid analyses within weeks of "
                "an event, using peer-reviewed protocols and large ensembles of model runs. Its "
                "findings are stated as changes in probability or intensity rather than as "
                "certainties: the 2021 Pacific Northwest heat dome was judged to be virtually "
                "impossible without climate change; the 2022 Pakistan floods were made more "
                "likely by warming, though vulnerability and land management determined the "
                "scale of the disaster; the 2023 Derna flood in Libya was linked to "
                "warmer-than-usual Mediterranean waters.",

                "Attribution has limits that are easy to forget. It is more reliable for heat than "
                "for rainfall, more reliable at continental than at local scales, and weakest "
                "where observations are sparse — which is usually where the most vulnerable "
                "populations live. It also says nothing about who is responsible or who should "
                "pay; those are political questions that attribution can inform but cannot "
                "answer. Used carefully, it converts a diffuse sense of injustice into a "
                "defensible claim; used carelessly, it invites the expectation that every "
                "disaster has a single attributable cause.",
            ],
        },
        {
            "num": "3.8",
            "title": "Early Warning Systems",
            "paras": [
                "Early warning is the most cost-effective adaptation measure available, and it is "
                "still missing where it is needed most. The United Nations' Early Warnings for All "
                "initiative, launched in 2022, estimated that about half of the world's countries "
                "lack a multi-hazard early warning system, and that where systems exist they often "
                "fail at the last mile — the warning reaches a capital city but not a village, or "
                "arrives in a language and format that the people at risk cannot use (UNDRR and "
                "WMO, 2023). The same reports estimate that a twenty-four-hour warning of a "
                "coming storm can reduce damage by about thirty per cent.",

                "Bangladesh is the standard example of what is possible. After the Bhola cyclone "
                "of 1970 killed an estimated three hundred thousand people, the country built a "
                "system of cyclone shelters, volunteer networks and mobile-phone alerts that has "
                "cut fatalities dramatically: Cyclone Amphan in 2020, a storm of comparable "
                "strength, killed roughly a hundred people. The improvement was not primarily "
                "technological. It came from shelters placed where people live, warnings issued in "
                "local languages, and drills that made evacuation routine.",

                "Heat is the harder case, because heat kills quietly and without a visible "
                "landfall. Ahmedabad's heat action plan, adopted after a 2010 heatwave killed more "
                "than a thousand people, combines colour-coded forecasts, cooling centres, altered "
                "working hours and outreach to vulnerable groups; evaluations suggest it has "
                "reduced mortality substantially. The lesson generalises: a warning is only an "
                "early warning if it arrives with the capacity to act on it.",
            ],
        },
        {
            "num": "3.9",
            "title": "Data Quality and Uncertainty",
            "paras": [
                "Uncertainty is not the same as ignorance, and the distinction matters for how "
                "scientific statements should be read. A measurement can be uncertain in a way "
                "that is precisely quantified — plus or minus a tenth of a degree, with a stated "
                "confidence interval — and a projection can be uncertain in a way that reflects "
                "genuine disagreement among plausible models. The first kind of uncertainty "
                "shrinks with better instruments; the second shrinks with better understanding, "
                "and sometimes not at all. Confusing the two leads either to false confidence or "
                "to unwarranted paralysis.",

                "Climate science distinguishes between internal variability, which is the "
                "unpredictable component generated by the system itself; model uncertainty, which "
                "is the spread produced by different representations of the same physics; and "
                "scenario uncertainty, which reflects the fact that future emissions depend on "
                "choices not yet made. Only the first is reduced by more data, and only the third "
                "is reduced by policy. When a projection is presented as a range, the width of "
                "that range is usually dominated by scenario uncertainty at the end of the century "
                "and by model uncertainty in the near term.",

                "There is also a discipline problem that the field has only recently begun to "
                "address. A dataset that is used to make a political argument will be scrutinised "
                "in a way that a dataset used only for research is not, and the scrutiny often "
                "targets the processing rather than the physics. The defence is transparency: "
                "open code, documented adjustments, published uncertainty ranges, and an "
                "explicit account of what would change the conclusion. Those practices are now "
                "standard in the major temperature and sea-level products, and they are the reason "
                "the records have survived decades of political attack.",
            ],
        },
        {
            "num": "3.10",
            "title": "Using Data for Decisions",
            "paras": [
                "The final step is the one most often skipped: converting a probabilistic "
                "projection into a decision. The standard approach in engineering is to design for "
                "a return period — a flood defence built for the one-in-a-hundred-year event — but "
                "that approach assumes a stationary climate, which is precisely what no longer "
                "holds. A defence designed for the statistics of the twentieth century will be "
                "overtopped more often than its designers intended, not because it was badly "
                "built but because the statistics it was built against have moved.",

                "The alternative is robust decision-making: rather than optimising for a single "
                "best estimate, identify the options that perform acceptably across a wide range "
                "of futures, and prefer those that can be adjusted as information arrives. The "
                "Netherlands' Delta Programme, which plans for sea-level rise up to several metres "
                "while building in stages that can be accelerated or paused, is the clearest "
                "example. The Thames Barrier, designed in the 1970s for a scenario that now looks "
                "optimistic, is another: its closure rate has risen from a few times a year to "
                "several times a year, and the decision to raise it further is taken on the basis "
                "of monitoring rather than prediction.",

                "What these examples share is a willingness to treat uncertainty as a design "
                "parameter rather than an obstacle. That requires institutions capable of "
                "revisiting decisions, budgets that can be reallocated, and a public that "
                "understands why a plan might change. The technical tools are available; the "
                "constraint is almost always institutional, which is why the chapters that follow "
                "devote as much attention to governance as to physics.",
            ],
        },
    ],

    "case": {
        "title": "Case Study: Argo and the Ocean That Was Hiding",
        "paras": [
            "Before 2000, the ocean's interior was sampled the way a continent might be mapped by "
            "a few dozen travellers: ships lowered instruments at chosen points, took a reading, "
            "and moved on. The coverage was sparse, biased toward shipping lanes, and concentrated "
            "in the northern hemisphere. Estimates of ocean heat content therefore carried "
            "uncertainties large enough to obscure the trend for a decade at a time, which meant "
            "that the largest reservoir of the climate system was also the least measured.",

            "Argo changed that with a design of remarkable simplicity. A float is dropped from a "
            "ship; it sinks to a programmed depth, drifts with the current, then rises while "
            "measuring temperature and salinity. At the surface it transmits its data and its "
            "position by satellite, then sinks again. Each cycle takes about ten days, each float "
            "lasts about four years, and the international programme maintains roughly four "
            "thousand of them, distributed across every ocean basin. The data are released within "
            "a day and are free to use.",

            "The scientific consequences were immediate. Ocean heat content became measurable with "
            "an uncertainty small enough to detect the annual increase; the seasonal cycle of the "
            "upper ocean became visible; and the deep ocean's role in absorbing heat could be "
            "quantified rather than inferred. When the record was extended backward with older "
            "ship data and forward with Argo, it showed a steady accumulation of heat that has "
            "continued every year since, with the last decade the warmest in the record (Cheng et "
            "al., 2024).",

            "Argo also demonstrates a governance lesson. The programme works because countries "
            "contribute floats, share data and accept common standards without a central "
            "authority that can compel them. It is coordinated by a small international secretariat "
            "and sustained by the self-interest of the participants, each of whom gets access to "
            "the whole dataset in exchange for contributing a share. That model — voluntary, "
            "standardised, open — has proved more durable than many formal treaties.",

            "The gaps that remain are instructive. Ice-covered seas, marginal seas and the deep "
            "ocean below two thousand metres are still poorly sampled, and the floats themselves "
            "are biased toward regions where deployment is easy. The next generation of "
            "instruments, including deep Argo and under-ice floats, is being deployed to close "
            "those gaps. The lesson for other domains is that a monitoring system is never "
            "finished; it is a commitment to keep looking, renewed each time the technology "
            "changes.",
        ],
    },

    "future": {
        "title": "Future Scenarios and Predictions: Systems, Feedbacks and Thresholds",
        "paras": [
            "The future of the climate system is not a single number but a set of conditional "
            "paths, and the condition is the same one that governs the previous chapter: the "
            "cumulative carbon emitted. What this chapter adds is the possibility of abruptness. "
            "The historical record shows that the system has changed gradually for most of the "
            "last ten thousand years, and that it has also changed abruptly in the more distant "
            "past — the Younger Dryas cold snap, the collapse of ice sheets at the end of the last "
            "glaciation — when a threshold was crossed. The question for the next century is "
            "whether the thresholds now being approached will be crossed slowly or quickly.",

            "The present position is that several of the slower variables have already begun to "
            "move. The Atlantic overturning circulation is weaker than at any time in the last "
            "millennium according to proxy reconstructions, though the size and significance of "
            "the decline remain contested (Caesar et al., 2021). Arctic sea ice is on a trajectory "
            "to be essentially absent in September before mid-century under all but the lowest "
            "emission scenarios. Warm-water coral reefs have already suffered four global "
            "bleaching events, and the interval between them has shortened.",

            "The assumptions that drive the scenarios are therefore not only about emissions but "
            "about the response of these slow variables. If the overturning circulation weakens "
            "moderately, European winters cool slightly while the tropics warm faster; if it "
            "collapses, the regional consequences are severe and the global consequences are still "
            "debated. If the Greenland ice sheet is committed to long-term loss, sea level rises "
            "for centuries regardless of what happens to emissions after mid-century. These are "
            "not alternative theories; they are different positions on a continuum of "
            "probability, and the monitoring systems described above are what allow the "
            "probabilities to be updated.",
        ],
        "table": {
            "caption": "Table 3.1 System thresholds and what to watch for",
            "head": ["Element", "Threshold of concern", "Time to observe change", "Signal to monitor"],
            "rows": [
                ["Atlantic overturning", "Weakening beyond ~15% of baseline",
                 "Decades", "Florida Strait transport; Labrador Sea density"],
                ["Arctic summer sea ice", "Below 1 million km² in September",
                 "Years", "NSIDC extent; ice thickness from CryoSat"],
                ["Greenland ice sheet", "Committed loss above ~1.5°C",
                 "Centuries", "GRACE gravity; surface melt days"],
                ["Amazon rainforest", "Dieback beyond ~20–25% forest loss",
                 "Decades", "Fire counts; dry-season length; carbon flux"],
                ["Coral reefs", "Frequent bleaching at 1.5°C; collapse at 2°C",
                 "Years", "Degree-heating weeks; reef surveys"],
            ],
        },
        "after_table": [
            "Two conclusions follow for decisions. The first is that monitoring is not a "
            "scientific luxury but an early-warning system for the planet: the sooner a threshold "
            "is detected, the more options remain. The second is that the standard tools of "
            "cost-benefit analysis are poorly suited to a system with thresholds, because they "
            "average over outcomes that are not interchangeable. A small probability of an "
            "irreversible change is not equivalent to a larger probability of a recoverable one, "
            "and any appraisal that treats them as equivalent will systematically underinvest in "
            "prevention.",

            "What would change these conclusions? A clear, sustained weakening of the overturning "
            "circulation would raise the urgency of every adaptation decision in Europe and West "
            "Africa. A decade without further Arctic sea-ice decline would suggest that the "
            "system is more resilient than the models assume. Neither is likely to be decisive on "
            "its own, and that is the nature of a system observed at the pace of decades: the "
            "evidence arrives slowly, and the decisions cannot wait for it.",
        ],
    },
}
