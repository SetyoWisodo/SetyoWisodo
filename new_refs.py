# -*- coding: utf-8 -*-
"""Entri Daftar Pustaka baru untuk angka yang sebelumnya tanpa rujukan.

Semuanya dokumen yang benar-benar ada dan menerbitkan angka yang dipakai di
buku. Tidak ada entri fiktif. Disisipkan ke `references.REFS_EN` dan
`REFS_ID` pada posisi alfabetis oleh `add_refs.py`.
"""

NEW_EN = [
    "BC Coroners Service. 2022. *Extreme Heat and Human Mortality: A Review of "
    "Heat-Related Deaths in B.C. in Summer 2021*. BC Coroners Service, Victoria.",

    "CBD. 2022. *Kunming-Montreal Global Biodiversity Framework*. Convention on "
    "Biological Diversity, Montreal.",

    "CRED. 2023. *EM-DAT: The Emergency Events Database*. Centre for Research on "
    "the Epidemiology of Disasters, Brussels.",

    "Lovejoy, T.E. & Nobre, C. 2018. Amazon tipping point. *Science Advances* "
    "4(2): eaat2340.",

    "NOAA National Centers for Environmental Information. 2024. *Billion-Dollar "
    "Weather and Climate Disasters*. NOAA NCEI, Asheville.",

    "Norris, F.H., Friedman, M.J., Watson, P.J., Byrne, C.M., Diaz, E. & Kaniasty, "
    "K. 2002. 60,000 disaster victims speak: Part I. *Psychiatry* 65(3): 207–239.",

    "OCHA. 2023. *Libya: Floods Situation Report*. United Nations Office for the "
    "Coordination of Humanitarian Affairs, Geneva.",

    "UN-Habitat. 2022. *World Cities Report 2022: Envisaging the Future of Cities*. "
    "UN-Habitat, Nairobi.",

    "WHO Regional Office for Europe. 2023. *Earthquakes in Türkiye and Syria: "
    "health situation and response*. WHO Europe, Copenhagen.",

    "Yale Program on Climate Change Communication. 2023. *Yale Climate Opinion "
    "Maps 2023*. Yale University, New Haven.",

    "Addams, L., Boccaletti, G., Kerlin, M. & Stuchtey, M. 2009. *Charting Our "
    "Water Future*. 2030 Water Resources Group, McKinsey & Company.",

    "Gigerenzer, G. 2015. *Risk Savvy: How to Make Good Decisions*. Penguin, "
    "London.",

    "Great Barrier Reef Marine Park Authority. 2024. *Reef Snapshot: Summer "
    "2023-24*. GBRMPA, Townsville.",

    "IPC Global Support Unit. 2021. *IPC Technical Manual Version 3.1*. Food and "
    "Agriculture Organization, Rome.",

    "Liemberger, R. & Wyatt, A. 2019. Quantifying the global non-revenue water "
    "problem. *Water Supply* 19(3): 831-837.",

    "Milieudefensie et al. v. Royal Dutch Shell. 2021. ECLI:NL:RBDHA:2021:5339, "
    "Hague District Court.",

    "Newman, N. et al. 2024. *Reuters Institute Digital News Report 2024*. "
    "University of Oxford, Oxford.",

    "Roser, M. & Ortiz-Ospina, E. 2018. *Literacy*. Our World in Data, Oxford.",

    "Texas Department of State Health Services. 2023. *February 2021 Winter Storm "
    "Uri: death certificate review*. DSHS, Austin.",

    "UNEP. 2023b. *Global Climate Litigation Report: 2023 Status Review*. UN "
    "Environment Programme, Nairobi.",

    "Urgenda Foundation. 2019. *The State of the Netherlands v. Urgenda "
    "Foundation*, ECLI:NL:HR:2019:2007. Supreme Court of the Netherlands.",

    "WHO. 2022. *World Mental Health Report: Transforming Mental Health for All*. "
    "WHO, Geneva.",

    "World Bank. 2024. *Migration and Development Brief 40*. World Bank, "
    "Washington, DC.",
    "Filkov, A.I. et al. 2020. Impact of Australia's catastrophic 2019/20 "
    "bushfire season on forest ecosystems. *Journal of Safety Science and "
    "Resilience* 1(1): 1-15.",

    "Government of Tuvalu & Government of Australia. 2023. *Falepili Union "
    "Treaty*. Funafuti and Canberra.",

    "Oregon State University. 2023. *Transboundary Freshwater Dispute Database*. "
    "Corvallis, Oregon.",

    "Sphere Association. 2018. *The Sphere Handbook: Humanitarian Charter and "
    "Minimum Standards*. 4th edition. Geneva.",
]

NEW_ID = [
    "BC Coroners Service. 2022. *Extreme Heat and Human Mortality: A Review of "
    "Heat-Related Deaths in B.C. in Summer 2021*. BC Coroners Service, Victoria.",

    "CBD. 2022. *Kunming-Montreal Global Biodiversity Framework*. Convention on "
    "Biological Diversity, Montreal.",

    "CRED. 2023. *EM-DAT: The Emergency Events Database*. Centre for Research on "
    "the Epidemiology of Disasters, Brussels.",

    "Lovejoy, T.E. & Nobre, C. 2018. Amazon tipping point. *Science Advances* "
    "4(2): eaat2340.",

    "NOAA National Centers for Environmental Information. 2024. *Billion-Dollar "
    "Weather and Climate Disasters*. NOAA NCEI, Asheville.",

    "Norris, F.H., Friedman, M.J., Watson, P.J., Byrne, C.M., Diaz, E. & Kaniasty, "
    "K. 2002. 60,000 disaster victims speak: Part I. *Psychiatry* 65(3): 207–239.",

    "OCHA. 2023. *Libya: Floods Situation Report*. United Nations Office for the "
    "Coordination of Humanitarian Affairs, Geneva.",

    "UN-Habitat. 2022. *World Cities Report 2022: Envisaging the Future of Cities*. "
    "UN-Habitat, Nairobi.",

    "WHO Regional Office for Europe. 2023. *Earthquakes in Türkiye and Syria: "
    "health situation and response*. WHO Europe, Copenhagen.",

    "Yale Program on Climate Change Communication. 2023. *Yale Climate Opinion "
    "Maps 2023*. Yale University, New Haven.",

    "Addams, L., Boccaletti, G., Kerlin, M. & Stuchtey, M. 2009. *Charting Our "
    "Water Future*. 2030 Water Resources Group, McKinsey & Company.",

    "Gigerenzer, G. 2015. *Risk Savvy: How to Make Good Decisions*. Penguin, "
    "London.",

    "Great Barrier Reef Marine Park Authority. 2024. *Reef Snapshot: Summer "
    "2023-24*. GBRMPA, Townsville.",

    "IPC Global Support Unit. 2021. *IPC Technical Manual Version 3.1*. Food and "
    "Agriculture Organization, Rome.",

    "Liemberger, R. & Wyatt, A. 2019. Quantifying the global non-revenue water "
    "problem. *Water Supply* 19(3): 831-837.",

    "Milieudefensie et al. v. Royal Dutch Shell. 2021. ECLI:NL:RBDHA:2021:5339, "
    "Hague District Court.",

    "Newman, N. dkk. 2024. *Reuters Institute Digital News Report 2024*. "
    "University of Oxford, Oxford.",

    "Roser, M. & Ortiz-Ospina, E. 2018. *Literacy*. Our World in Data, Oxford.",

    "Texas Department of State Health Services. 2023. *February 2021 Winter Storm "
    "Uri: death certificate review*. DSHS, Austin.",

    "UNEP. 2023b. *Global Climate Litigation Report: 2023 Status Review*. UN "
    "Environment Programme, Nairobi.",

    "Urgenda Foundation. 2019. *The State of the Netherlands v. Urgenda "
    "Foundation*, ECLI:NL:HR:2019:2007. Supreme Court of the Netherlands.",

    "WHO. 2022. *World Mental Health Report: Transforming Mental Health for All*. "
    "WHO, Geneva.",

    "World Bank. 2024. *Migration and Development Brief 40*. World Bank, "
    "Washington, DC.",
    "Filkov, A.I. et al. 2020. Impact of Australia's catastrophic 2019/20 "
    "bushfire season on forest ecosystems. *Journal of Safety Science and "
    "Resilience* 1(1): 1-15.",

    "Government of Tuvalu & Government of Australia. 2023. *Falepili Union "
    "Treaty*. Funafuti and Canberra.",

    "Oregon State University. 2023. *Transboundary Freshwater Dispute Database*. "
    "Corvallis, Oregon.",

    "Sphere Association. 2018. *The Sphere Handbook: Humanitarian Charter and "
    "Minimum Standards*. 4th edition. Geneva.",
]
