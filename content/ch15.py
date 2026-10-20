# -*- coding: utf-8 -*-
"""Chapter 15 — Data, Statistics and Misinformation."""

CH = {
    "num": 15,
    "title": "Data, Statistics and Misinformation",
    "theme": "climate data, statistical reasoning and the contest over evidence",
    "nsec": 10,

    "opening": [
        "On 26 September 2024, Hurricane Helene made landfall in Florida's Big Bend as a Category 4 "
        "storm and then travelled inland for hundreds of kilometres, dropping extreme rainfall across "
        "Georgia, South Carolina, North Carolina and Tennessee. The flooding in the southern "
        "Appalachians was catastrophic: whole towns were cut off, the French Broad River in Asheville "
        "reached a level not seen in more than a century, and at least 230 people died across six "
        "states. Damage was estimated at more than US$78 billion.",

        "Within hours of landfall, a second event was unfolding online. Posts claimed that the federal "
        "government had engineered the storm, that relief agencies were confiscating donations, that "
        "rescue teams were refusing to help people with certain political views, and that officials "
        "were seizing land for lithium mining. None of it was true. The Federal Emergency Management "
        "Agency set up a page to rebut the rumours; local officials pleaded for people to stop "
        "sharing them; and meteorologists reported threats against their staff.",

        "The misinformation did not stay online. It affected whether people evacuated, whether they "
        "applied for aid, and whether they trusted the warnings that arrived before the next storm. In "
        "a disaster, information is infrastructure: it determines whether people move, whether they "
        "shelter, and whether they accept help. When it fails, the physical response fails with it.",

        "This chapter is about how climate knowledge is produced, how it is misread, and how it is "
        "deliberately distorted. It explains what climate data actually are, how scientists measure "
        "consensus and attribute extreme events, and which statistical mistakes recur most often. It "
        "then turns to the mechanics of misinformation and to what actually works against it. The aim "
        "is not to make every reader a statistician but to make every reader harder to fool.",
    ],

    "sections": [
        {
            "num": "15.1",
            "title": "What a Climate Number Actually Means",
            "paras": [
                "The statement that 2024 was the first calendar year more than 1.5 °C above "
                "pre-industrial levels is precise only in relation to a baseline, and the baseline is "
                "a choice. Pre-industrial usually means 1850–1900, the period when instrument "
                "coverage became global enough to estimate a planetary average. Change the baseline "
                "and the number changes: relative to 1981–2010, 2024 was about 1.2 °C warmer; relative "
                "to the last glacial maximum it is a different quantity altogether.",

                "Climate numbers are usually expressed as anomalies rather than absolute "
                "temperatures, because anomalies are more comparable across space and time. A station "
                "in Siberia and one in Indonesia have very different absolute temperatures, but their "
                "year-to-year changes can be averaged meaningfully. The convention avoids being "
                "distorted by the uneven distribution of weather stations, but it also makes the "
                "numbers abstract, which is one reason they are easy to misrepresent.",

                "Every climate number also carries an uncertainty range, and the range is not a sign "
                "of weakness. It reflects incomplete coverage, instrument error, and the choice of "
                "method. The global mean surface temperature estimated by NASA, NOAA, the Met Office "
                "and Berkeley Earth agree within a few hundredths of a degree, which is a remarkable "
                "convergence given that they use different station networks and different "
                "interpolation methods. Convergence of independent methods is the strongest evidence "
                "a reader can ask for.",
            ],
        },
        {
            "num": "15.2",
            "title": "Where the Data Come From",
            "paras": [
                "The instrumental record is assembled from land stations, ocean buoys and ships, "
                "weather balloons, aircraft, and satellites. Each has strengths and weaknesses. Land "
                "stations give long records but are unevenly distributed, with dense coverage in "
                "Europe and North America and sparse coverage in parts of Africa and South America. "
                "Ocean measurements cover two-thirds of the planet but were historically taken by "
                "merchant ships along trade routes, leaving gaps that models must fill.",

                "Satellites provide global coverage but only since the late 1970s, and they measure "
                "different things: microwave sounders estimate lower-troposphere temperature, radar "
                "altimeters measure sea level, and radiometers measure sea-surface temperature. "
                "Satellite records must be calibrated across successive instruments, and small "
                "differences in calibration can produce apparent trends that are artefacts rather "
                "than signals — a fact that has been exploited by campaigns against the data.",

                "Reanalysis products such as ERA5 combine observations with a weather model to "
                "produce a physically consistent reconstruction of the atmosphere going back to "
                "1940, and proxy records — tree rings, ice cores, corals, sediments — extend the "
                "picture back thousands of years. The proxies are less precise but they establish "
                "the context: the current warming is far faster than anything in the Holocene, and "
                "the concentration of carbon dioxide is higher than at any point in at least 800,000 "
                "years, and probably three million.",
            ],
        },
        {
            "num": "15.3",
            "title": "Measuring Scientific Consensus",
            "paras": [
                "The claim that about 97 per cent of climate scientists agree that human activity is "
                "warming the planet comes from several independent studies. Doran and Zimmerman "
                "(2009) surveyed Earth scientists and found that 97 per cent of those who actively "
                "publish climate research agreed that human activity is a significant contributing "
                "factor. Cook et al. (2013) examined nearly 12,000 abstracts and found that among "
                "those expressing a position, 97.1 per cent endorsed the consensus, a figure later "
                "revised upward when the sample was corrected.",

                "Lynas et al. (2021) reviewed 88,125 climate-related papers published between 2012 "
                "and 2020 and found that more than 99.9 per cent of them endorsed the consensus. "
                "That is an extraordinary level of agreement for any scientific question, comparable "
                "to the consensus on plate tectonics or the germ theory of disease. It does not mean "
                "that the science is settled in every detail; it means that the central claim is not "
                "seriously disputed by specialists.",

                "The gap between scientific consensus and public perception is itself measured. "
                "Surveys in the United States find that the public estimates the share of scientists "
                "who agree at around 70 per cent, well below the actual figure, and that this "
                "underestimate is associated with lower support for policy. The gap is sometimes "
                "called the consensus gap, and it is produced by the same mechanisms that produce "
                "other misconceptions: repetition, selective exposure and the prominence of dissenting "
                "voices disproportionate to their number.",
            ],
        },
        {
            "num": "15.4",
            "title": "Attribution Science",
            "paras": [
                "Event attribution asks a counterfactual question: how likely would this heatwave, "
                "flood or drought have been in a world without human influence? The method compares "
                "large ensembles of climate model simulations with and without historical greenhouse "
                "gas emissions, and sometimes combines them with observed trends. It does not say "
                "that climate change caused a specific storm, because weather always has multiple "
                "causes; it says that the probability or intensity of the event has shifted.",

                "The field has matured quickly. World Weather Attribution, a collaboration of "
                "scientists in Europe and the United States, now produces rapid analyses within days "
                "or weeks of an event. Studies have found that the 2021 Pacific Northwest heatwave "
                "was made at least 150 times more likely by climate change, that the 2022 Pakistan "
                "flooding was made more intense by warming, and that the 2024 European heat was made "
                "substantially more likely and hotter.",

                "Attribution is powerful because it connects global statistics to local experience, "
                "but it is also easy to misrepresent. A finding that an event was made twice as "
                "likely does not mean it was twice as severe, and a finding that no human signal was "
                "detected in a particular event does not mean climate change is not happening. "
                "Absence of attribution for one event is not evidence against the broader trend, just "
                "as a single cold week is not evidence against a warming climate.",
            ],
        },
        {
            "num": "15.5",
            "title": "The Statistical Fallacies That Recur",
            "paras": [
                "The most common fallacy is cherry-picking the baseline. A widely repeated claim that "
                "warming stopped in 1998 depends on choosing a year with an exceptionally strong El "
                "Niño as the starting point. Begin the analysis three years earlier or later and the "
                "trend is clear. The same technique is used to argue that sea ice is recovering, that "
                "the 1930s were hotter, or that a particular glacier is growing: select the window "
                "that produces the desired slope.",

                "A second fallacy is confusing weather with climate. A cold snap in one region does "
                "not disprove a global trend any more than a hot day proves it. The relevant question "
                "is whether the frequency and intensity of events are changing over decades and "
                "across regions, which requires aggregating data rather than selecting anecdotes. "
                "Anecdotes are vivid and statistics are abstract, which is why the fallacy persists.",

                "A third is misreading correlation and causation, usually in the claim that carbon "
                "dioxide follows temperature rather than causing it. In the ice-core record, carbon "
                "dioxide does rise after temperature at the onset of glacial terminations, because "
                "the initial warming is driven by orbital cycles and the ocean then releases carbon "
                "dioxide, which amplifies the warming. That is a feedback, not a refutation; the "
                "physics of carbon dioxide absorbing infrared radiation was established in the "
                "nineteenth century and is not in dispute.",
            ],
        },
        {
            "num": "15.6",
            "title": "Misinformation in Disasters",
            "paras": [
                "Disasters create ideal conditions for misinformation: uncertainty is high, official "
                "information is slow, emotions are strong, and people are desperate for explanations. "
                "Rumours fill the vacuum. After Hurricane Katrina in 2005, reports of widespread "
                "violence and hundreds of deaths in the Superdome circulated widely and were later "
                "found to be largely false; after the 2011 Tōhoku earthquake, false claims about "
                "radiation spread faster than official advisories.",

                "The pattern has intensified with social media. During Hurricane Helene in 2024, "
                "false claims about weather modification, land seizure and diverted aid reached "
                "millions of people, and officials reported that they interfered with relief. FEMA "
                "created a rumour-response page, and the North Carolina authorities warned that "
                "misinformation was deterring people from applying for assistance. The effect is "
                "measurable: trust in warnings falls, and evacuation and aid uptake decline.",

                "Artificial intelligence has made the problem harder. Generated images of flooded "
                "streets or destroyed neighbourhoods can be produced in minutes and are difficult to "
                "distinguish from real photographs, especially on a phone screen during an emergency. "
                "Detection tools lag behind generation, and the platforms that distribute the content "
                "have limited incentive to slow it. The result is that the evidentiary value of a "
                "photograph has fallen, which is a problem for journalists, insurers and courts as "
                "well as for emergency managers.",
            ],
        },
        {
            "num": "15.7",
            "title": "Reading a Graph and Spotting a Trick",
            "paras": [
                "Many misleading climate claims are made through graphs rather than words, because a "
                "graph appears objective. The common tricks are simple: truncating the vertical axis "
                "so that a small change looks dramatic, or extending it so that a large change looks "
                "small; choosing a start date that flatters a trend; plotting a short window and "
                "drawing a long conclusion; and comparing datasets that measure different things.",

                "A reader can apply four checks. First, what is the baseline or reference period, and "
                "why was it chosen? Second, what is the vertical axis, and does it start at zero or at "
                "a value that exaggerates the change? Third, what is the time window, and is it long "
                "enough to distinguish a trend from noise? Fourth, who produced the data, and is the "
                "underlying dataset available? The last question is the most powerful, because "
                "manipulated graphs rarely come with accessible data.",

                "Legitimate scientific communication has its own conventions that can look like "
                "weakness. Error bars, ranges and conditional language are marks of care, not "
                "evasion. A scientist who says an outcome is likely under a scenario is being precise; "
                "a commentator who says it is certain is being careless or dishonest. Learning to read "
                "hedged language as a sign of rigour is one of the most useful skills a citizen can "
                "acquire.",
            ],
        },
        {
            "num": "15.8",
            "title": "Prebunking, Debunking and Inoculation",
            "paras": [
                "The evidence on correcting misinformation is mixed but not hopeless. Debunking after "
                "the fact works partially: it reduces belief among people who see the correction, but "
                "it rarely reaches everyone who saw the original claim, and repeating the falsehood "
                "can strengthen it among some audiences. The practical implication is to lead with the "
                "fact, explain the technique rather than dwell on the claim, and avoid repeating the "
                "falsehood more than necessary.",

                "Prebunking — warning people about manipulation techniques before they encounter them "
                "— has stronger evidence. Inoculation theory, developed by William McGuire in the "
                "1960s, holds that exposing people to a weakened form of a misleading argument builds "
                "resistance to the full version. Field experiments by van der Linden and colleagues "
                "found that short videos explaining techniques such as emotional manipulation, false "
                "dichotomies and scapegoating improved people's ability to identify misinformation "
                "across topics.",

                "The most durable defence is structural: reduce the supply of misinformation, increase "
                "the salience of reliable sources, and make accurate information easy to find and act "
                "upon. That means funding public broadcasting, requiring platforms to disclose how "
                "their algorithms amplify content, supporting local journalism, and ensuring that "
                "official warnings are timely, specific and consistent. Individual literacy matters, "
                "but it cannot compensate for an information environment designed to confuse.",
            ],
        },
        {
            "num": "15.9",
            "title": "Open Data, Reproducibility and Data Gaps",
            "paras": [
                "Climate science is unusually open. The major temperature records are published with "
                "their methods and code; satellite data are archived and distributed; model outputs "
                "are contributed to the Coupled Model Intercomparison Project and made available to "
                "researchers worldwide; and the Intergovernmental Panel on Climate Change reports are "
                "reviewed by hundreds of scientists and published in full. This openness is the best "
                "available answer to claims of conspiracy, because anyone with the skills can "
                "reproduce the analysis.",

                "But the data are not evenly distributed. Station coverage is sparse in parts of "
                "Africa, South America and Southeast Asia, which means that the regions most "
                "vulnerable to climate change often have the weakest observational records. The "
                "result is greater uncertainty in local projections precisely where adaptation "
                "decisions are most urgent. Programmes to digitise historical records, expand "
                "automatic weather stations and support national meteorological services are "
                "therefore a form of climate resilience.",

                "Reproducibility is also a social practice. A dataset that is published but "
                "undocumented is not usable; a method that is described but not coded is not "
                "replicable. The most valuable institutions in this space are those that maintain "
                "long records, document their methods and respond to criticism in public. Their "
                "reputation is built on being checkable, which is exactly what a conspiracy theory "
                "cannot be.",
            ],
        },
        {
            "num": "15.10",
            "title": "Communicating Numbers Honestly",
            "paras": [
                "Numbers are persuasive but easily misread, so communication requires care. A "
                "temperature rise of 1.5 °C sounds small to people who experience 1.5 °C as the "
                "difference between a cool and a warm day; the same change in a planetary average is "
                "enormous, because it represents a shift in the distribution of heat, not a uniform "
                "increase. Explaining the difference between a local temperature and a global average "
                "is one of the most useful things a communicator can do.",

                "Uncertainty language matters too. The IPCC uses calibrated terms: virtually certain "
                "means 99–100 per cent probability, very likely 90–100 per cent, likely 66–100 per "
                "cent, about as likely as not 33–66 per cent. These terms are defined so that readers "
                "can interpret them consistently, but they are often read as vague hedging. Translating "
                "them into plain probabilities, without stripping the uncertainty, is a skill worth "
                "teaching.",

                "Finally, communication should respect the audience. People are not empty vessels into "
                "which facts are poured; they have experience, values and trusted sources. A message "
                "that begins with local experience, acknowledges what is uncertain, and offers "
                "concrete action is more likely to be heard than one that begins with a global "
                "statistic and a moral instruction. Honesty about uncertainty is not a weakness in "
                "persuasion; it is the foundation of trust, and trust is the resource that matters "
                "most when the next warning arrives.",
            ],
        },
    ],

    "case": {
        "title": "Case Study: Hurricane Helene and the Information Emergency",
        "paras": [
            "Hurricane Helene made landfall on 26 September 2024 as a Category 4 storm near Perry, "
            "Florida, then moved rapidly inland. Its wind field was unusually large, and its moisture "
            "was drawn from an exceptionally warm Gulf of Mexico. The result was extreme rainfall over "
            "the southern Appalachians, a region where steep terrain funnels water into narrow "
            "valleys and where communities are often accessible by a single road.",

            "The physical damage was severe. At least 230 people died across six states, making "
            "Helene the deadliest mainland hurricane since Katrina in 2005. Asheville and surrounding "
            "counties were cut off; the region's water system was destroyed; and damage estimates "
            "exceeded US$78 billion. Power and communications failed across a wide area, which meant "
            "that many people relied on social media for information precisely when it was least "
            "reliable.",

            "The information environment collapsed faster than the roads. Claims that the federal "
            "government had created or steered the storm, that relief workers were confiscating "
            "supplies, and that officials were seizing land for mining spread across platforms and "
            "were amplified by political figures. FEMA published a rumour-response page; state "
            "officials urged residents to verify before sharing; and meteorologists reported threats. "
            "Surveys later found that belief in the false claims was concentrated among people who "
            "distrusted government generally.",

            "The practical consequences were measurable. Officials reported that some residents did "
            "not apply for assistance because they believed the aid would be taken or would obligate "
            "them; others delayed evacuation before subsequent storms. Aid organisations found that "
            "they had to spend time rebutting rumours instead of delivering supplies. The episode "
            "showed that trust is not a soft variable: it determines whether warnings are obeyed and "
            "whether help is accepted.",

            "The lessons are specific. Warnings must arrive through trusted local messengers, not only "
            "through national agencies. Correction must be fast, concrete and repeated, because "
            "rumours spread in the gap between the event and the official response. And platforms "
            "must be treated as part of the emergency infrastructure, with obligations that match "
            "their influence. A community that has accurate information and trusts it recovers faster "
            "than one that has the same physical damage and does not.",
        ],
    },

    "future": {
        "title": "Future Scenarios and Predictions: The Information Environment in 2050",
        "paras": [
            "The historical record shows that misinformation is not new; what is new is its speed and "
            "scale. Rumours spread by word of mouth during the Lisbon earthquake of 1755; radio "
            "amplified propaganda in the twentieth century; and social media compressed the cycle from "
            "days to minutes. Each transition increased reach and reduced the time available for "
            "verification.",

            "Present conditions define the starting point. Around 5 billion people use social media, "
            "and surveys in many countries find that a majority get at least some news from it. "
            "Generative artificial intelligence has made synthetic text, images and audio cheap; "
            "research by Reuters Institute and others finds that audiences struggle to distinguish "
            "them from authentic material. Trust in news media has declined in most wealthy "
            "democracies, while trust in scientists remains comparatively high, which creates an "
            "opening for scientists who communicate directly.",

            "The assumptions that drive the projections are the pace of regulation, the cost of "
            "detection, and the resilience of local institutions. A world that invests in verification "
            "infrastructure, media literacy and trusted local reporting can limit the damage; a world "
            "that does not will face disasters in which the information environment fails alongside "
            "the physical one. The table summarises the range.",
        ],
        "table": {
            "caption": "Table 15.1 Information environment indicators, 2050",
            "head": ["Indicator", "Fragmented", "Current trends", "Resilient", "Consequence"],
            "rows": [
                ["Share of news from social platforms", "70%", "55%", "35%", "Speed vs verification"],
                ["Synthetic media detection", "Poor", "Moderate", "Good", "Evidentiary trust"],
                ["Local news outlets", "Few", "Declining", "Stable", "Accountability"],
                ["Trust in official warnings", "Low", "Moderate", "High", "Evacuation compliance"],
                ["Media literacy in schools", "20%", "45%", "80%", "Resistance to manipulation"],
                ["Platform disclosure rules", "None", "Partial", "Strong", "Algorithmic transparency"],
            ],
        },
        "after_table": [
            "Two conclusions follow. First, misinformation is a disaster-risk multiplier: it does not "
            "create the flood, but it determines whether people escape it. Second, the defences that "
            "work are local and structural — trusted messengers, funded journalism, open data and "
            "literate citizens — rather than a single technological fix.",

            "What would change these conclusions? Regulation that requires platforms to disclose how "
            "they rank content could reduce the amplification of falsehood, though enforcement across "
            "borders is difficult. Cheap and reliable provenance systems — cryptographic signatures on "
            "images and video — could restore part of the evidentiary value of a photograph. And a "
            "sustained investment in local journalism could rebuild the institutions that once "
            "filtered rumour. The most important variable remains the same as elsewhere: the pace of "
            "climate change determines how often the information system will be tested, and the "
            "quality of that system determines how many people survive the test.",
        ],
    },
}
