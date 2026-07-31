"""
pages/about.py: Static markdown page for context about Campi Flegrei.
"""
from dash import register_page, html, dcc

register_page(__name__, path='/about')

markdown_text_1 = '''## Campi Flegrei 

The Campi Flegrei, or Phlegraean Fields, is a massive caldera near Naples, Italy, and one of the most closely monitored volcanic systems in the world. This interactive dashboard, built with [Dash](https://dash.plotly.com/), tracks earthquake activity in the region using live data from [INGV](https://www.ingv.it/) (the National Institute of Geophysics and Volcanology).

#### The Volcano

Spanning approximately 13 kilometers, the caldera is part of an active volcanic complex formed around 39,000 years ago following a colossal eruption. Today, the Phlegrean Fields consist of 24 craters and volcanic edifices, some of which are submerged in the Gulf of Naples. 

The area is defined by its intense geothermal activity—most visibly at the Solfatara crater, where jets of steam and sulfurous gases serve as a constant reminder of the region's volatile nature. It belongs to the Campanian volcanic arc, which includes the infamous Mount Vesuvius (responsible for destroying Pompeii in 79 AD) situated just 9 km east of Naples. The caldera's last major eruption occurred in 1538, lasting eight days and depositing enough material to create an entirely new 132-meter hill, Monte Nuovo. '''


markdown_text_2 = '''Because of the sheer scale of its past eruptions and the dense population surrounding it, Campi Flegrei is considered one of Europe's most hazardous volcanoes. 

Over half a million people live inside the caldera's "Red Zone"—the area at highest risk of pyroclastic flows, which would require preemptive evacuation in the event of an eruption. Another 840,000 people reside in the "Yellow Zone," which could be subjected to heavy ashfall and forced evacuations. An eruption larger than what current models anticipate could impact an even wider area.

#### Bradyseism

The defining geological characteristic of Campi Flegrei is **bradyseism**. Deriving from the ancient Greek words *bradús* ("slow") and *seismós* ("movement"), bradyseism is the gradual uplift or subsidence of the Earth's surface. 

This deformation is driven by the movement of magma and hydrothermal fluids deep beneath the crust. During phases of positive bradyseism, pressure builds and the ground swells upward; during negative bradyseism, the ground slowly sinks. These cycles can persist for millennia between actual eruptions, and upward swelling phases are almost always accompanied by swarms of small to moderate earthquakes as the crust fractures under stress. In recent history, severe bradyseismic crises in the 1970s and 1980s caused the ground in the port town of Pozzuoli to rise by several meters, forcing mass relocations. '''


markdown_text_3 = '''The historical inflation and deflation of this caldera are exceptionally well documented, thanks to its seaside location and thousands of years of continuous human habitation. 

The most famous evidence is the Roman Macellum of Pozzuoli. Three of its standing marble columns feature distinct bands of holes bored by marine molluscs up to 7 meters above the base. This proves that negative bradyseism once lowered the Roman ruins deep beneath the sea, before a subsequent phase of uplift pushed them back above the water line. Similarly, extensive archaeological ruins, including paved roads and statues, now sit completely submerged off the coast of nearby Baia due to these shifting ground levels.

This dashboard tracks the seismic tremors associated with this ongoing uplift cycle, pulling data from INGV (updated every hour) to provide a clear view of the volcano's current activity. '''


# Layout assembles markdown text blocks and reference images in a centered layout
layout = [
    html.Div(
        dcc.Markdown(markdown_text_1),
        className='about',
    ), 
    html.Img(src='assets/map.png', className='image_centered'),
    html.Div(
        dcc.Markdown(markdown_text_2),
        className='about',
    ), 
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/5/52/Serapeum_%28Pozzuoli%29_-2.jpg', className='image_centered'),
    html.Div(
        dcc.Markdown(markdown_text_3),
        className='about',
    )
]