# -*- coding: utf-8 -*-
"""Variasi pembuka paragraf lapis kedua.

Lapisan pendalaman menambahkan banyak paragraf baru, dan sebagian di antaranya
membuka dengan kalimat yang bentuknya sama seperti paragraf di atasnya
(terutama di studi kasus, yang diawali "The ..." berulang kali). Modul ini
mengganti pembuka itu dengan rumusan yang setara maknanya tetapi berbeda
bentuknya.

Setiap entri adalah pasangan (lama, baru) yang sudah diberi jangkar berupa
kalimat berikutnya, sehingga hanya kemunculan yang dimaksud yang berubah.
Modul ini idempoten: kalau teks lama tidak ada, tidak terjadi apa-apa.
"""

EN = [
    # --- "The lessons are ..." / "The case ..." di studi kasus ---
    ("The lessons are specific. First, importing countries should hold",
     "The lessons for importers are specific. First, they should hold"),
    ("The lessons are specific. Warnings must arrive",
     "For warning systems the lesson is specific. Warnings must arrive"),
    ("The lessons are specific. Mental health services must be",
     "For services, the lesson is specific. Mental health services must be"),
    ("The lessons are specific. Principles matter",
     "For negotiations the lesson is specific. Principles matter"),
    ("The lessons are specific. Heat plans must be designed",
     "For heat planning the lesson is specific. Heat plans must be designed"),
    ("The lessons are practical. First, vector control",
     "For health systems the lessons are practical. First, vector control"),
    ("The lessons are clear. Heat is a mass casualty event",
     "For public health, the lessons are clear. Heat is a mass casualty event"),
    ("The lessons are transferable. Warning must reach the last mile",
     "For any country building a warning system, the lessons are transferable. "
     "Warning must reach the last mile"),
    ("The case has wider lessons. First, repeated disturbances",
     "The lessons reach beyond the reef itself. First, repeated disturbances"),
    ("The case illustrates three lessons. First, infrastructure failures",
     "The Texas case yields three lessons. First, infrastructure failures"),
    ("The case shows that food security is a systems problem.",
     "Food security is a systems problem, and the rice shock shows why."),
    ("The case shows that restoration is a governance problem, not a planting problem.",
     "The restoration record shows governance to be the binding constraint, "
     "not planting."),
    ("The case illustrates the connection between climate and health systems. The weather created",
     "The connection between climate and health systems runs through capacity. "
     "The weather created"),
    ("The case illustrates the central argument of this chapter: slow emergencies are political. The rainfall was",
     "Slow emergencies are political, and this one shows why. The rainfall was"),
    ("The health system response varied. Brazil deployed",
     "The response varied by health system. Brazil deployed"),
    ("The lessons are financial as well as physical. First, insurance penetration",
     "What followed was financial as well as physical. First, insurance penetration"),
    ("The fund's significance is partly symbolic. It recognises",
     "Its significance is partly symbolic. It recognises"),
    ("The comparison with Pakistan is instructive. Both events",
     "The comparison with Pakistan is the instructive part. Both events"),
    ("The comparison is not a story of complete success.", "Success was not complete."),
    ("The disaster shaped the institutions that followed. After independence in 1971",
     "The institutions that followed were shaped by it. After independence in 1971"),
    ("The results were measurable. Kerosene use fell",
     "The results showed up in household budgets. Kerosene use fell"),
    ("The reef is also affected by other pressures. Runoff",
     "Other pressures compound the heat. Runoff"),
    ("The immediate response was overwhelmed. Evacuation routes were blocked",
     "The immediate response was overwhelmed within hours. "
     "Evacuation routes were blocked"),
    ("The warning system had worked. The Famine Early Warning Systems Network",
     "The warning system had in fact worked. "
     "The Famine Early Warning Systems Network"),
    ("The famine was also a failure of livelihoods. Pastoralists depend",
     "Livelihoods failed before the rains did. Pastoralists depend"),
    ("The response, when it came, was large but late. Food aid",
     "Relief, when it came, was large but late. Food aid"),
    ("The reef has bleached five times since 2016: in 2016, 2017, 2020, 2022 and 2024.",
     "Five bleaching events have hit the reef since 2016: in 2016, 2017, 2020, "
     "2022 and 2024."),
    # --- studi kasus lain: satu tahun, satu angka, satu peristiwa ---
    ("The 2017 Atlantic season is a study in how a single year of disasters is absorbed.",
     "What the 2017 season documents is how a single year of disasters is absorbed."),
    ("The 2017 season also demonstrated the insurance gap that defines climate economics.",
     "It also demonstrated the insurance gap that defines climate economics."),
    ("The economic effects persisted for years.",
     "Its economic effects persisted for years."),
    ("The total damage was about US$300 billion, of which only about a third was insured.",
     "Total damage came to about US$300 billion, of which only about a third "
     "was insured."),
    ("The 2017 Atlantic hurricane season was one of the most destructive on record.",
     "Few Atlantic seasons have been as destructive as 2017."),
    # --- makroekonomi ---
    ("The macroeconomics of a warming world are shaped by three forces that pull in different directions.",
     "Three forces pull the macroeconomics of a warming world in different "
     "directions."),
    ("The macroeconomics of a warming world is largely about productivity, capital and uncertainty.",
     "Productivity, capital and uncertainty are what the macroeconomics of a "
     "warming world is largely about."),
    ("The macroeconomics of a warming world is less about the cost of a disaster than about the drag on growth, and the drag is the number that compounds.",
     "What matters is less the cost of a disaster than the drag on growth, and "
     "the drag is the number that compounds."),
    ("The policy response has three pillars.", "Three pillars make up the policy response."),
    ("The fiscal exposure of small and low-income states is the part of the economic story that the macro models handle worst.",
     "Fiscal exposure of small and low-income states is the part of the economic "
     "story that the macro models handle worst."),
    ("The effect is not uniform across countries.",
     "Its effect is not uniform across countries."),
    # --- iklim dan konflik ---
    ("The research on climate and conflict has moved through three phases and the third is the most useful.",
     "Three phases have marked the research, and the third is the most useful."),
    ("The research on climate and conflict has moved from a claim that the climate causes wars to a more careful account of how it shifts probabilities.",
     "The field has moved from a claim that the climate causes wars to a more "
     "careful account of how it shifts probabilities."),
    ("The quantitative literature has three strands. One finds",
     "Three strands run through the quantitative literature. One finds"),
    ("The finding was influential and contested. Critics, notably",
     "It was influential and contested in equal measure. Critics, notably"),
    ("The pathways are easier to describe than to measure.",
     "They are easier to describe than to measure."),
    ("The pathways run through livelihoods, prices and movement, and each has an observable signature.",
     "Livelihoods, prices and movement are the channels, and each has an "
     "observable signature."),
    ("The first pathway is economic.", "Economics is the first pathway."),
    ("The second pathway is food prices.", "Food prices are the second pathway."),
    ("The third pathway is migration.", "Migration is the third pathway."),
    ("The conflict in Mali, Burkina Faso and Niger has killed thousands and displaced millions.",
     "Conflict in Mali, Burkina Faso and Niger has killed thousands and "
     "displaced millions."),
    ("The Lake Chad basin is a similar case. The lake's shrinkage",
     "The Lake Chad basin repeats the pattern with a different mechanism. "
     "The lake's shrinkage"),
    ("The Lake Chad Basin is the most cited case, and it is more complicated than the shorthand suggests. The lake shrank",
     "The lake shrank"),
    ("The Lake Chad basin illustrates how a slow environmental change becomes a security problem through livelihoods rather than through scarcity alone.",
     "What the basin illustrates is how a slow environmental change becomes a "
     "security problem through livelihoods rather than through scarcity alone."),
    ("The Lake Chad basin is often cited as a climate-conflict case and the citation is usually oversimplified.",
     "It is often cited as a climate-conflict case, and the citation is usually "
     "oversimplified."),
    # --- Sahel dan kelaparan ---
    ("The Sahel famines of the 1970s and 1980s produced one of the most influential and most contested narratives in environmental history",
     "Famines in the Sahel during the 1970s and 1980s produced one of the most "
     "influential and most contested narratives in environmental history"),
    ("The Sahel famines of the 1970s and 1980s killed an estimated hundred thousand people in the drought of 1968 to 1974,",
     "An estimated hundred thousand people died in the Sahel drought of 1968 to "
     "1974,"),
    ("The Sahel is the region where the argument about land, rainfall and conflict has been fought most intensely, and the argument has moved on.",
     "No region has fought the argument about land, rainfall and conflict more "
     "intensely than the Sahel, and the argument has moved on."),
    ("The Great Green Wall is the most ambitious attempt to reverse Sahelian land degradation, and its evolution is instructive.",
     "The most ambitious attempt to reverse Sahelian land degradation is the "
     "Great Green Wall, and its evolution is instructive."),
    ("The causes were not simply rainfall. Colonial and post-colonial",
     "Rainfall was not the whole cause. Colonial and post-colonial"),
    ("The Sahel also shows that adaptation is possible. Since the 1980s",
     "Adaptation has been possible there too. Since the 1980s"),
    ("The Ethiopian famine of 1984–85 is the case that made famine visible to the world, and its legacy is double-edged",
     "Famine became visible to the world through Ethiopia in 1984–85, and its "
     "legacy is double-edged"),
    ("The 2011 Somali famine is the clearest case in the modern record of a disaster that was predicted and not prevented.",
     "No disaster in the modern record was more clearly predicted and less "
     "clearly prevented than the Somali famine of 2011."),
    ("The Somali famine of 2011 is often described as a failure of early warning, and the description is only partly right.",
     "It is often described as a failure of early warning, and the description is "
     "only partly right."),
    # --- harga pangan ---
    ("The 2007–2008 food price crisis demonstrated that a climate shock can become a global event through markets rather than through harvests.",
     "What the 2007–2008 crisis demonstrated is that a climate shock can become a "
     "global event through markets rather than through harvests."),
    ("The 2022 food crisis repeated the 2008 pattern with a different trigger.",
     "In 2022 the pattern repeated with a different trigger."),
    ("The 2007–2008 crisis produced a set of reforms that are still the basis of food security policy.",
     "It produced a set of reforms that are still the basis of food security policy."),
    ("The food price crisis of 2007 and 2008 was the moment when the world discovered that its food system had less slack than it thought.",
     "In 2007 and 2008 the world discovered that its food system had less slack "
     "than it thought."),
    ("The 2007 and 2008 crisis produced a set of rules that were supposed to prevent a repetition, and the rules were tested in 2022 and partly failed.",
     "That crisis also produced rules that were supposed to prevent a repetition, "
     "and the rules were tested in 2022 and partly failed."),
    # --- panas ---
    ("The 1995 Chicago heatwave remains the canonical case because the mortality was so clearly social",
     "Chicago in 1995 remains the canonical case because the mortality was so "
     "clearly social"),
    ("The European heatwave of 2003 is the founding case of heat-health planning, and it is still the clearest demonstration of what a health system can and cannot absorb",
     "Europe in 2003 is the founding case of heat-health planning, and it is still "
     "the clearest demonstration of what a health system can and cannot do."),
    ("The European heatwave of 2003 produced about seventy thousand deaths and a reform that has been copied across the world",
     "Europe in 2003 produced about seventy thousand deaths and a reform that has "
     "been copied across the world"),
    ("The deaths were concentrated among older people living alone, often in flats with poor insulation and no air conditioning.",
     "Death was concentrated among older people living alone, often in flats with "
     "poor insulation and no cooling."),
    ("The political reaction was severe.", "Political reaction was severe."),
    ("The systems appear to have worked. When Europe experienced",
     "The systems appear to have worked after 2003. When Europe experienced"),
    ("The 2021 Pacific Northwest heat dome was unprecedented in the instrumental record",
     "In the instrumental record, the 2021 Pacific Northwest heat dome was "
     "unprecedented"),
    ("The human toll was concentrated among people who had no experience of such heat and no means to escape it.",
     "Those who died had no experience of such heat and no means to escape it."),
    ("The event exposed a planning gap.", "It exposed a planning gap."),
    ("The Pacific Northwest heat dome exposed a form of vulnerability that climate planning had largely ignored",
     "A form of vulnerability that climate planning had largely ignored was "
     "exposed by the Pacific Northwest heat dome"),
    ("The Pacific Northwest heat dome of June 2021 was a different kind of event and it changed the way scientists think about extremes",
     "June 2021 in the Pacific Northwest was a different kind of event, and it "
     "changed the way scientists think about extremes"),
    ("The Pacific Northwest heat dome exposed the infrastructure assumptions of a temperate region, and the exposure was not mainly about hospitals.",
     "Temperate-region infrastructure assumptions were exposed by the Pacific "
     "Northwest heat dome, and the exposure was not mainly about hospitals."),
    # --- api dan banjir ---
    ("The Canadian case also illustrates the limits of suppression.",
     "It also illustrates the limits of suppression."),
    ("The Canadian fires of 2023 produced a health event that extended far beyond the burn zone.",
     "In 2023 the Canadian fires produced a health event that extended far beyond "
     "the burn zone."),
    ("The smoke problem has changed how fire is understood in public health, and the change is recent.",
     "How fire is understood in public health has changed, and the change is recent."),
    ("The Canadian wildfires of 2023 produced a hazard that is new in its reach",
     "What the Canadian wildfires of 2023 produced was a hazard that is new in "
     "its reach"),
    ("The Canadian smoke of 2023 turned air quality into a transboundary issue that no single jurisdiction could manage, and the management was improvised.",
     "Smoke from Canada in 2023 turned air quality into a transboundary issue that "
     "no single jurisdiction could manage, and the management was improvised."),
    ("The case is notable because it occurred in a wealthy region with strong institutions and modern forecasting.",
     "What makes the case notable is that it occurred in a wealthy region with "
     "strong institutions and modern forecasting."),
    ("The 2021 floods in Germany and Belgium became a case study in warning failure rather than in rainfall.",
     "Germany and Belgium in 2021 became a case study in warning failure rather "
     "than in rainfall."),
    ("The Ahr valley flood produced a policy reform that is unusually specific.",
     "It produced a policy reform that is unusually specific."),
    ("The Ahr valley flood of July 2021 is the case that most clearly separates a warning from an action",
     "No case separates a warning from an action more clearly than the Ahr valley "
     "flood of July 2021"),
    ("The Ahr valley flood led to a reform of the European flood directive and to a change in the way warnings are delivered, and the change is instructive.",
     "It led to a reform of the European flood directive and to a change in the "
     "way warnings are delivered, and the change is instructive."),
    # --- kebakaran Camp ---
    ("The Camp Fire began on 8 November 2018 near Pulga, California, and spread rapidly",
     "On 8 November 2018 a fire began near Pulga, California, and spread rapidly"),
    ("The Camp Fire destroyed the town of Paradise in a few hours on 8 November 2018, killing eighty-five people",
     "In a few hours on 8 November 2018 the Camp Fire destroyed the town of "
     "Paradise, killing eighty-five people"),
    ("The mental health consequences were severe and persistent.",
     "Mental health consequences were severe and persistent."),
    ("The COVID-19 pandemic arrived while many survivors were still displaced",
     "COVID-19 arrived while many survivors were still displaced"),
    ("The aftermath of the 2018 Kerala floods produced an instructive natural experiment in community mental health.",
     "Kerala's 2018 floods produced an instructive natural experiment in "
     "community mental health."),
    # --- keadilan dan dana kerugian ---
    ("The issue gained momentum after a series of disasters.",
     "Momentum came after a series of disasters."),
    ("The agreement was historic but limited.",
     "Historic and limited, the agreement was both."),
    ("The case that best illustrates the justice dimension is the dispute over the atmosphere's remaining carbon budget.",
     "What best illustrates the justice dimension is the dispute over the "
     "atmosphere's remaining carbon budget."),
    ("The Loss and Damage Fund is a case study in how a justice demand becomes an institution and how much of the demand survives the process.",
     "How a justice demand becomes an institution, and how much of the demand "
     "survives the process, is what the Loss and Damage Fund documents."),
    ("The Loss and Damage Fund became operational with a board that is balanced between the contributors and the recipients",
     "It became operational with a board that is balanced between the "
     "contributors and the recipients"),
    # --- Bhola ---
    ("The Bhola cyclone of November 1970 killed an estimated 300,000 to 500,000 people in the low-lying delta of East Pakistan",
     "In November 1970 the Bhola cyclone killed an estimated 300,000 to 500,000 "
     "people in the low-lying delta of East Pakistan"),
    ("The most useful case for a reader who wants to act is not a catastrophe but a city that prepared before one arrived.",
     "For a reader who wants to act, the useful case is not a catastrophe but a "
     "city that prepared before one arrived."),
    ("The fifty years between the Bhola cyclone of 1970 and Cyclone Amphan of 2020 are the clearest record of what preparedness can achieve.",
     "Between the Bhola cyclone of 1970 and Cyclone Amphan of 2020 lie fifty "
     "years, the clearest record of what preparedness can achieve."),
    ("The Bangladeshi cyclone programme is the clearest demonstration in the record that preparedness can be built at scale",
     "Nowhere is it clearer that preparedness can be built at scale than in the "
     "Bangladeshi cyclone programme"),
]

ID = [
    ("Pelajarannya spesifik. Pertama, negara pengimpor",
     "Bagi negara pengimpor pelajarannya spesifik. Pertama, mereka"),
    ("Pelajarannya spesifik. Peringatan harus datang",
     "Bagi sistem peringatan pelajarannya spesifik. Peringatan harus datang"),
    ("Pelajarannya spesifik. Layanan kesehatan mental",
     "Bagi layanan, pelajarannya spesifik. Layanan kesehatan mental"),
    ("Pelajarannya spesifik. Prinsip penting",
     "Bagi perundingan pelajarannya spesifik. Prinsip penting"),
    ("Pelajarannya spesifik. Rencana panas",
     "Bagi perencanaan panas pelajarannya spesifik. Rencana panas"),
    ("Pelajarannya jelas. Panas adalah peristiwa korban massal",
     "Bagi kesehatan publik, pelajarannya jelas. Panas adalah peristiwa korban massal"),
    ("Pelajarannya praktis. Pertama, pengendalian vektor",
     "Bagi sistem kesehatan pelajarannya praktis. Pertama, pengendalian vektor"),
    ("Pelajarannya dapat ditransfer. Peringatan harus menjangkau mil terakhir",
     "Bagi negara yang membangun sistem peringatan, pelajarannya dapat "
     "ditransfer. Peringatan harus menjangkau mil terakhir"),
    ("Pelajarannya finansial sekaligus fisik. Pertama, penetrasi asuransi",
     "Yang menyusul finansial sekaligus fisik. Pertama, penetrasi asuransi"),
    ("Kasus ini menunjukkan bahwa ketahanan pangan adalah masalah sistem.",
     "Ketahanan pangan adalah masalah sistem, dan guncangan beras menunjukkan "
     "mengapa."),
    ("Kasus ini menunjukkan restorasi adalah masalah tata kelola, bukan masalah menanam.",
     "Catatan restorasi menunjukkan tata kelola sebagai kendala pengikat, bukan "
     "penanaman."),
    ("Terumbu juga terpengaruh tekanan lain. Limpasan",
     "Tekanan lain memperberat panasnya. Limpasan"),
    ("Hasilnya terukur. Penggunaan minyak tanah turun",
     "Hasilnya terlihat pada anggaran rumah tangga. Penggunaan minyak tanah turun"),
    ("Bencana itu membentuk institusi yang menyusul. Setelah kemerdekaan 1971",
     "Institusi yang menyusul dibentuk olehnya. Setelah kemerdekaan 1971"),
    ("Cekungan Danau Chad adalah kasus serupa. Penyusutan danau",
     "Cekungan Danau Chad mengulang polanya dengan mekanisme berbeda. Penyusutan danau"),
    ("Temuan itu berpengaruh dan diperdebatkan. Kritikus, terutama",
     "Pengaruhnya besar dan perdebatannya sama besar. Kritikus, terutama"),
    ("Literatur kuantitatif memiliki tiga alur. Satu",
     "Tiga alur berjalan melalui literatur kuantitatif. Satu"),
    ("Perbandingan dengan Pakistan instruktif. Kedua peristiwa",
     "Bagian yang instruktif adalah perbandingan dengan Pakistan. Kedua peristiwa"),
    ("Penyebabnya bukan sekadar curah hujan. Kebijakan kolonial",
     "Curah hujan bukan satu-satunya penyebab. Kebijakan kolonial"),
    ("Sahel juga menunjukkan bahwa adaptasi mungkin. Sejak 1980-an",
     "Adaptasi juga mungkin di sana. Sejak 1980-an"),
    ("Sistem itu tampaknya bekerja. Ketika Eropa mengalami",
     "Sistemnya tampaknya bekerja setelah 2003. Ketika Eropa mengalami"),
    ("Makna dana itu sebagian simbolis. Ia mengakui",
     "Maknanya sebagian simbolis. Ia mengakui"),
]


def apply(text, lang):
    pairs = EN if lang == "en" else ID
    n = 0
    for old, new in pairs:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    return text, n
