# -*- coding: utf-8 -*-
"""Chapter 10 — Economic Impacts and Financial Resilience."""

CH = {
    "num": 10,
    "title": "Economic Impacts and Financial Resilience",
    "theme": "the economics of climate damage, insurance and the cost of delay",
    "nsec": 10,

    "opening": [
        "In August 2017, Hurricane Harvey stalled over Houston and dropped more than 1,500 "
        "millimetres of rain in five days. The damage was estimated at US$125 billion, most of it "
        "from flooding rather than wind. A few weeks later, Hurricane Irma struck the Caribbean and "
        "Florida, and Hurricane Maria struck Puerto Rico, with losses of US$77 billion "
        "and US$90 billion respectively. The three storms together produced losses of about US$300 "
        "billion, of which only about a third was insured.",

        "The 2017 season illustrates a pattern that is becoming more common. The physical damage "
        "is only the first layer of economic loss. Businesses that close do not pay wages; workers "
        "who lose wages spend less; local governments that lose tax revenue cut services; insurers "
        "that pay claims raise premiums; and households that lose their savings reduce consumption "
        "for years. The indirect losses can exceed the direct damage, and they fall hardest on the "
        "people with the least cushion.",

        "Climate economics has moved from the margins of the discipline to its centre because the "
        "damage is no longer hypothetical. The estimates vary widely, but they converge on a "
        "conclusion: the cost of inaction is larger than the cost of action, and the difference "
        "grows with every year of delay. The debate is no longer about whether to act but about how "
        "to allocate the cost, who bears the risk, and how to finance the transition.",

        "This chapter examines the economic channels through which climate change affects "
        "households, firms and states. It distinguishes between direct damage and indirect loss, "
        "between stock and flow, and between the risks that can be insured and those that cannot. "
        "It closes with the financial instruments that can build resilience — reserve funds, "
        "parametric insurance, catastrophe bonds, and the public balance sheets that ultimately "
        "backstop them.",
    ],

    "sections": [
        {
            "num": "10.1",
            "title": "Direct Damage and Indirect Loss",
            "paras": [
                "Disaster economics distinguishes between damage, which is the cost of repairing or "
                "replacing physical assets, and loss, which is the cost of lost economic activity. "
                "A factory that is destroyed represents damage; the production that the factory "
                "would have generated during the months it is rebuilt represents loss. The two are "
                "often reported together, but they behave differently: damage is a one-time cost, "
                "while loss can persist until the factory is rebuilt and the market recovers.",

                "The distinction matters for policy. Compensation that covers damage but not loss "
                "leaves businesses unable to pay wages and households unable to replace income, "
                "which prolongs the disruption. The 2011 Thailand floods damaged industrial estates "
                "that produced a large share of the world's hard drives; the damage was repaired in "
                "months, but the global production shortfall lasted longer and raised computer "
                "prices for a year. The loss was transmitted through supply chains to firms and "
                "consumers who never saw the flood.",

                "Indirect losses are difficult to measure because they are counterfactual: they "
                "describe what would have happened without the disaster. Economists estimate them "
                "using input-output models, computable general equilibrium models, or econometric "
                "comparisons of affected and unaffected regions. The estimates vary, but they "
                "consistently find that indirect losses are larger in economies with tighter "
                "linkages, weaker social protection and less fiscal space to respond.",
            ],
        },
        {
            "num": "10.2",
            "title": "Productivity, Labour and Heat",
            "paras": [
                "Heat reduces economic output through labour productivity. The International Labour "
                "Organization estimates that heat stress already reduces global working hours by "
                "about 2.2 per cent, equivalent to 80 million full-time jobs, and that the loss "
                "could reach 2.4 per cent by 2030. Agriculture accounts for about 60 per cent of the "
                "lost hours, followed by construction, manufacturing and transport.",

                "The mechanism is physiological and behavioural. Above a certain wet-bulb "
                "temperature, workers must slow down, take breaks and drink water; in the absence "
                "of those adaptations, heat exhaustion and heatstroke occur. Firms respond by "
                "shifting hours, installing cooling, or automating tasks, but each response has a "
                "cost. For workers paid by output, the cost is borne directly as lost income; for "
                "firms, it appears as lower productivity and higher capital expenditure.",

                "The distributional effect is important. Outdoor workers, agricultural labourers and "
                "construction workers are the most exposed, and they are often the least able to "
                "insure against lost income. In countries where a large share of employment is "
                "informal, heat does not appear in official productivity statistics, because the "
                "work is not measured in the first place. The result is that the economic cost of "
                "heat is systematically underestimated in the places where it is highest.",
            ],
        },
        {
            "num": "10.3",
            "title": "Food Prices and Inflation",
            "paras": [
                "Climate shocks to food production are transmitted to the wider economy through "
                "prices. When a major producer loses a harvest, global prices rise, and the effect "
                "reaches consumers through retail prices and, in poor countries, through the cost "
                "of the food basket that dominates household budgets. Central banks have begun to "
                "include climate shocks in their inflation models, because food and energy price "
                "spikes can destabilise expectations even when core inflation is stable.",

                "The 2022 food price crisis is an example. The war in Ukraine was the immediate "
                "trigger, but it arrived on top of a series of climate-related harvest failures in "
                "Europe, South Asia and the Horn of Africa. Food prices rose by more than 20 per "
                "cent globally, and the increase was largest in countries that import a high share "
                "of their calories. The result was a rise in poverty and a decline in dietary "
                "quality that persisted after prices fell.",

                "The inflationary effect is not only a problem for households; it is a problem for "
                "governments. Food and energy subsidies are politically difficult to remove and "
                "fiscally expensive to maintain, and they tend to expand precisely when revenues "
                "are falling because the economy is contracting. The result is a pro-cyclical "
                "fiscal burden that can turn a climate shock into a debt crisis, particularly in "
                "countries with limited access to international capital markets.",
            ],
        },
        {
            "num": "10.4",
            "title": "Sovereign Risk and the Cost of Capital",
            "paras": [
                "Climate change affects the cost at which governments and firms borrow. Credit rating "
                "agencies have begun to incorporate climate vulnerability into sovereign ratings, "
                "and the effect is already visible in the spreads that some countries pay on their "
                "debt. A country that is exposed to repeated disasters, dependent on climate-sensitive "
                "exports and lacking fiscal buffers is a riskier borrower than one that is not, even "
                "if its current debt level is the same.",

                "The mechanism operates through several channels. Disasters reduce tax revenue and "
                "increase expenditure at the same time, which worsens the fiscal balance. Repeated "
                "disasters can reduce potential growth by destroying capital and discouraging "
                "investment. And the expectation of future losses can raise the risk premium that "
                "investors demand, which increases the cost of servicing debt and reduces the "
                "resources available for adaptation.",

                "The result is a vicious circle for the most vulnerable countries. They face the "
                "highest adaptation costs, the highest cost of capital and the least fiscal space, "
                "and the combination can make adaptation unaffordable even when the returns are "
                "high. International financial institutions have begun to address the problem "
                "through concessional finance, debt swaps and pre-arranged emergency lending, but "
                "the scale remains small relative to the need.",
            ],
        },
        {
            "num": "10.5",
            "title": "Insurance and the Limits of Risk Transfer",
            "paras": [
                "Insurance is the mechanism that allows losses to be spread across many policyholders "
                "and over time. It works when the risk is measurable, the events are independent, "
                "and the premiums cover the expected losses plus a margin. Climate change violates "
                "all three conditions: the risk is changing, the events are becoming correlated "
                "across regions, and the losses are rising faster than premiums can adjust.",

                "The result is retreat. Insurers have withdrawn from parts of California and Florida, "
                "where wildfire and hurricane risk have increased; they have raised premiums in "
                "coastal areas; and they have reduced coverage for floods and storm surge. In the "
                "United States, the National Flood Insurance Program has been insolvent for years "
                "and has been forced to raise premiums, which has made insurance unaffordable for "
                "some homeowners and reduced property values.",

                "When insurance fails, the cost shifts to governments and households. Governments "
                "provide disaster relief, which is often untargeted and slow; households draw down "
                "savings, borrow at high interest, or abandon property. The shift is regressive, "
                "because wealthy households can self-insure and poor households cannot. The result "
                "is that climate risk becomes a mechanism for transferring wealth from those who "
                "cannot bear it to those who can.",
            ],
        },
        {
            "num": "10.6",
            "title": "Stranded Assets and Transition Risk",
            "paras": [
                "The transition away from fossil fuels creates a different kind of financial risk: "
                "assets that were expected to produce revenue may become uneconomic before they are "
                "fully depreciated. Coal plants, oil fields, gas pipelines and the infrastructure "
                "that supports them could be stranded if demand falls faster than expected or if "
                "policy restricts their use. The value of those assets is reflected in the balance "
                "sheets of companies, banks and pension funds, which means that a rapid transition "
                "could create losses across the financial system.",

                "The risk is not hypothetical. Coal companies in the United States and Europe have "
                "written down assets as gas and renewables have displaced coal; oil majors have "
                "faced pressure from investors to disclose their climate assumptions; and central "
                "banks have begun to stress-test banks against transition scenarios. The magnitude "
                "of the risk depends on the speed of the transition and on whether it is orderly or "
                "disorderly.",

                "The policy implication is that transition risk and physical risk must be managed "
                "together. A disorderly transition, in which policy changes abruptly and assets are "
                "written down suddenly, can destabilise financial institutions; a delayed "
                "transition, in which physical risk continues to accumulate, can destabilise them "
                "even more. The goal is an orderly transition that signals policy direction early, "
                "phases out the most exposed assets gradually and protects the workers and "
                "communities that depend on them.",
            ],
        },
        {
            "num": "10.7",
            "title": "The Cost of Inaction",
            "paras": [
                "Estimating the cost of inaction requires comparing a future with climate change to "
                "a future without it, and the comparison depends on assumptions about growth, "
                "adaptation and discounting. Early integrated assessment models, such as the "
                "DICE model developed by William Nordhaus, produced estimates of a few per cent of "
                "global GDP by the end of the century, and those estimates were criticised for "
                "understating the risk of catastrophic and irreversible impacts.",

                "More recent estimates are larger. A 2024 study in Nature found that a high-emission "
                "pathway would reduce global income by about 19 per cent by 2050 relative to a "
                "no-climate baseline, with damages of about US$38 trillion a year, and that the "
                "losses would fall disproportionately on countries with low historical emissions "
                "(Kotz, Levermann and Wenz, 2024). The Swiss Re Institute estimated that climate "
                "change could reduce global GDP by 10 per cent by 2050 in a severe scenario, and the "
                "World Bank has estimated that poor countries could lose 1.2 to 3.3 per cent of GDP "
                "by 2030.",

                "The estimates differ because they use different assumptions, but they share a "
                "conclusion: the cost of inaction is larger than the cost of action, and the "
                "difference is growing. The economics of climate change is therefore not primarily "
                "about whether to act but about how quickly, how fairly and how effectively. The "
                "longer the delay, the larger the physical risk and the more abrupt the transition "
                "that will be required to avoid it.",
            ],
        },
        {
            "num": "10.8",
            "title": "Who Bears the Loss",
            "paras": [
                "The economic burden of climate change is distributed unevenly across countries, "
                "sectors and households. Low-income countries are more exposed because their "
                "economies depend on agriculture, their infrastructure is less resilient, and their "
                "fiscal capacity to respond is smaller. Within countries, poor households are more "
                "exposed because they live in more hazardous places, work outdoors, and have fewer "
                "savings and less insurance.",

                "The distributional effect is compounded by the fact that the countries and "
                "households that contributed least to emissions are often the most exposed. This is "
                "the basis of the loss and damage debate in international climate negotiations, "
                "which led to the creation of a fund at COP27 in 2022. The fund is small relative "
                "to the need, and its governance and disbursement remain contested, but it "
                "establishes the principle that climate losses are a matter of justice, not only of "
                "charity.",

                "The household-level distribution is equally important. A disaster that destroys a "
                "poor household's home can push it into poverty permanently, because it has no "
                "savings, no insurance and no access to credit. A wealthier household can absorb "
                "the same loss and rebuild. The result is that a single event can widen inequality "
                "for a generation, and that social protection is as important as physical "
                "infrastructure in determining who recovers.",
            ],
        },
        {
            "num": "10.9",
            "title": "Financial Instruments for Resilience",
            "paras": [
                "Several instruments can transfer or finance climate risk. Sovereign catastrophe "
                "bonds pay out when a predefined event occurs, providing rapid liquidity after a "
                "disaster. Parametric insurance does the same at a smaller scale, using rainfall or "
                "wind speed as a proxy for loss. Contingent credit lines allow governments to borrow "
                "quickly when a disaster is declared. Reserve funds accumulate savings in good years "
                "for use in bad ones.",

                "Each instrument has strengths and weaknesses. Catastrophe bonds are expensive and "
                "require sophisticated legal and financial infrastructure; parametric insurance "
                "suffers from basis risk, because the index may not match the actual loss; "
                "contingent credit depends on the government's creditworthiness; and reserve funds "
                "require fiscal discipline that is difficult to maintain. The most effective "
                "approach combines several instruments and layers them so that small events are "
                "covered by reserves, medium events by insurance and large events by sovereign or "
                "international support.",

                "The deeper issue is that risk transfer does not reduce risk; it only spreads it. "
                "A country that insures against floods still experiences the flood, and the premium "
                "it pays reduces the resources available for prevention. The most cost-effective "
                "financial strategy is therefore to invest in reducing risk first, and to use "
                "insurance for the residual risk that cannot be eliminated. That sequencing — "
                "prevention before transfer — is the core principle of financial resilience.",
            ],
        },
        {
            "num": "10.10",
            "title": "The Macroeconomics of a Warming World",
            "paras": [
                "At the macroeconomic level, climate change affects growth through several channels: "
                "it destroys capital, reduces productivity, diverts investment from productive uses "
                "to reconstruction, and increases uncertainty, which discourages long-term "
                "investment. The combined effect is a reduction in potential output that persists "
                "long after the event that caused it.",

                "The effect is not uniform across countries. Economies that depend on agriculture, "
                "tourism or outdoor labour are more exposed; economies with diversified production "
                "and strong institutions are more resilient. The result is that climate change is "
                "likely to widen the gap between rich and poor countries, reversing some of the "
                "convergence that globalisation produced in the late twentieth century.",

                "The policy response has three pillars. The first is mitigation, which reduces the "
                "magnitude of future damage. The second is adaptation, which reduces vulnerability "
                "to the damage that is already committed. The third is financial resilience, which "
                "ensures that households, firms and governments can absorb the shocks that cannot "
                "be prevented. The three are complementary: mitigation without adaptation leaves "
                "people exposed to unavoidable impacts; adaptation without mitigation eventually "
                "exceeds its limits; and both without financial resilience leave the poorest to bear "
                "the cost.",
            ],
        },
    ],

    "case": {
        "title": "Case Study: The 2017 Atlantic Hurricane Season",
        "paras": [
            "The 2017 Atlantic hurricane season was one of the most destructive on record. Hurricane "
            "Harvey made landfall in Texas in August and stalled, dropping more than 1,500 "
            "millimetres of rain over Houston, with losses put at US$125 billion. "
            "Hurricane Irma followed in September, devastating several Caribbean islands and inflicting "
            "losses of US$77 billion. Hurricane Maria struck Puerto Rico two weeks later, "
            "destroying the electricity grid and inflicting damage of about US$90 billion.",

            "The total damage was about US$300 billion, of which only about a third was insured. The "
            "gap was concentrated in Puerto Rico and the smaller Caribbean islands, where insurance "
            "penetration is low and where the losses were largest relative to the size of the "
            "economy. In Puerto Rico, the storm caused an estimated 2,975 excess deaths in the "
            "months after landfall, most of them from the failure of the electricity and health "
            "systems rather than from the storm itself.",

            "The economic effects persisted for years. In Puerto Rico, the population declined by "
            "several per cent as residents moved to the mainland; businesses closed; and the "
            "reconstruction of the grid took more than a year and cost billions of dollars. In "
            "Texas, the recovery was faster because the state had resources, insurance and access "
            "to federal assistance, but the damage to housing was concentrated in low-income "
            "neighbourhoods that lacked flood insurance.",

            "The season illustrates the difference between insured and uninsured loss, and between "
            "the capacity of rich and poor jurisdictions to recover. It also illustrates the "
            "importance of infrastructure: the failure of the Puerto Rican grid turned a hurricane "
            "into a public health emergency, and the failure of the Texas power system during a "
            "winter storm four years later showed the same pattern in a different season. In both "
            "cases, the physical hazard was within the range of what the infrastructure was "
            "supposed to withstand; the failure was in the design, maintenance and governance of "
            "the system.",

            "The lessons are financial as well as physical. First, insurance penetration is a "
            "determinant of recovery, and it is lowest where the need is greatest. Second, "
            "infrastructure resilience is a form of financial protection, because it reduces the "
            "liability that governments and households must bear after an event. Third, the "
            "poorest households need grants and social protection, not loans, because a loan "
            "against future income is not a recovery strategy for someone who has lost their "
            "livelihood. Fourth, the cost of reconstruction is rising, and the willingness of "
            "donors and insurers to pay is not.",
        ],
    },

    "future": {
        "title": "Future Scenarios and Predictions: The Economic Cost to 2050",
        "paras": [
            "The historical record shows that economic losses from climate-related disasters have "
            "increased. The total damage from weather-related disasters, adjusted for inflation, "
            "has grown by about 5 to 7 per cent a year since the 1970s, faster than exposure alone "
            "would predict. Insured losses have grown even faster, because more assets are "
            "concentrated in exposed areas and because insurance has expanded into new markets.",

            "Present conditions give the baseline. Global losses from weather-related disasters are "
            "estimated at US$200 to US$300 billion a year, of which about half is insured. The "
            "uninsured half falls on households, firms and governments, and it is concentrated in "
            "low- and middle-income countries. The cost of adaptation is estimated at US$100 to "
            "US$300 billion a year by 2030 for developing countries, and the finance available is a "
            "fraction of that.",

            "The assumptions that drive the projections are the emission path, the rate of "
            "adaptation, and the discount rate used to compare present and future costs. A low "
            "discount rate makes future damages look larger and justifies more spending now; a high "
            "discount rate makes them look smaller and justifies delay. The choice of discount rate "
            "is therefore an ethical choice as much as an economic one, because it determines how "
            "much weight is given to people who are not yet born.",
        ],
        "table": {
            "caption": "Table 10.1 Economic losses under three pathways, 2050",
            "head": ["Indicator", "Low emissions", "Current policies", "High emissions", "Main driver"],
            "rows": [
                ["Global GDP loss vs no-climate baseline", "−3 to −5%", "−8 to −12%", "−15 to −20%", "Labour; agriculture; capital"],
                ["Annual damage (US$ trillion)", "1.5–2.5", "4–6", "7–10", "Extreme events; slow onset"],
                ["Uninsured losses (share)", "40%", "50%", "60%", "Insurance retreat"],
                ["People pushed into poverty (million)", "50–100", "100–200", "200–400", "Food prices; displacement"],
                ["Adaptation finance needed (US$ bn/yr)", "100", "200", "300+", "Infrastructure; social protection"],
            ],
        },
        "after_table": [
            "Two conclusions follow. First, the difference between the low and high pathways is "
            "measured in percentage points of global GDP, which is to say in trillions of dollars "
            "and in hundreds of millions of people pushed into poverty. Second, the losses are not "
            "a future that arrives in 2050; they accumulate year by year, and the countries that "
            "are least able to adapt are already paying the highest share.",

            "What would change these conclusions? A rapid diffusion of cheap clean energy would "
            "reduce both the physical damage and the transition risk, and it is already happening "
            "faster than most models assumed. A breakthrough in adaptation finance — through "
            "reform of multilateral institutions, debt relief or new levies — would reduce the "
            "burden on the poorest countries. And a change in the discount rate used by "
            "governments would make long-term damages look larger and justify more investment now. "
            "None of these is certain, but the direction of the economics is: delay costs more than "
            "action.",
        ],
    },
}
