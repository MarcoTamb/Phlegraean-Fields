# Phlegraean Fields Earthquakes dashboard

The Phlegrean Fields, also known as Campi Flegrei, is a large volcanic area situated near Naples, Italy. Which is also close to where I grew up. This interactive dashboard, built with [Dash](https://dash.plotly.com/), tracks the earthquakes in the area, automatically scraping data from [INGV](https://www.ingv.it/), the Italian research institute monitoring the activity of the Volcano. 

## Tech Stack
* **Framework:** Built entirely in Python using [Plotly Dash](https://dash.plotly.com/).
* **Data Retrieval:** Live API scraping from INGV web services using `requests` and processed with `pandas`.
* **Performance:** Server-side caching using `Flask-Caching` to avoid API rate limits

## Instructions 

You can also access the live app deployed on Plotly Cloud **[here](https://faa06204-3bfd-4de8-bdac-24d810199848.plotly.app/)**. *(Note: The application runs on a free cloud tier and will enter hibernation after periods of inactivity. It may take 30–60 seconds to wake up and fetch fresh data from INGV on your first visit.)*

You can access the app, deployed on Heroku, [here](https://campiflegrei-644a6eb36dd0.herokuapp.com/). *(similar limitations)*

## Local Installation

To run this application locally on your machine, clone the repository, install all the dependencies in *requirements.txt*, and run *main.py*. 
You have two options for setting up your environment:


### Standard Python (pip)
```bash
# Create and activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Mamba/Conda

If using [Mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html)/[Conda](https://docs.conda.io/en/latest/), to set env variables and install packages I suggest to create a separate environment and use the following commands, assuming you are in the project folder: 

    mamba create -n phlegrean
    mamba activate phlegrean 
    mamba install --yes --file requirements.txt
    python main.py
    
From the second time onwards you only need to run:

    mamba activate phlegrean
    python main.py
(replace ``mamba`` with ``conda`` if using Conda)

### Accessing the dashboard
Once running, you can access the dashboard in your browser at *[localhost:8050](http://localhost:8050)*. 

*(Note: For some outdated Dash versions, it may be necessary to add the environment variable `REACT_VERSION=18.2.0` for dash-mantine-components to render correctly, though this should no longer be required on modern setups.)*

## Screenshots

#### 3D map

![3D-view](https://raw.githubusercontent.com/MarcoTamb/Phlegrean-Fields/main/screenshots/3d-view.png)

#### Heatmap

![Heatmap](https://raw.githubusercontent.com/MarcoTamb/Phlegrean-Fields/main/screenshots/heatmap.png)

#### About 

![About](https://raw.githubusercontent.com/MarcoTamb/Phlegrean-Fields/main/screenshots/about.png)

## The Volcano

Spanning approximately 13 kilometers, the caldera is part of an active volcanic complex formed around 39,000 years ago following a colossal eruption. Today, the Phlegrean Fields consist of 24 craters and volcanic edifices, some of which are submerged in the Gulf of Naples. 

The area is defined by its intense geothermal activity—most visibly at the Solfatara crater, where jets of steam and sulfurous gases serve as a constant reminder of the region's volatile nature. It belongs to the Campanian volcanic arc, which includes the infamous Mount Vesuvius (responsible for destroying Pompeii in 79 AD) situated just 9 km east of Naples. The caldera's last major eruption occurred in 1538, lasting eight days and depositing enough material to create an entirely new 132-meter hill, Monte Nuovo.

Because of the sheer scale of its past eruptions and the dense population surrounding it, Campi Flegrei is considered one of Europe's most hazardous volcanoes. 

Over half a million people live inside the caldera's "Red Zone"—the area at highest risk of pyroclastic flows, which would require preemptive evacuation in the event of an eruption. Another 840,000 people reside in the "Yellow Zone," which could be subjected to heavy ashfall and forced evacuations. An eruption larger than what current models anticipate could impact an even wider area.

## Bradyseism

The defining geological characteristic of Campi Flegrei is **bradyseism**. Deriving from the ancient Greek words *bradús* ("slow") and *seismós* ("movement"), bradyseism is the gradual uplift or subsidence of the Earth's surface. 

This deformation is driven by the movement of magma and hydrothermal fluids deep beneath the crust. During phases of positive bradyseism, pressure builds and the ground swells upward; during negative bradyseism, the ground slowly sinks. These cycles can persist for millennia between actual eruptions, and upward swelling phases are almost always accompanied by swarms of small to moderate earthquakes as the crust fractures under stress. In recent history, severe bradyseismic crises in the 1970s and 1980s caused the ground in the port town of Pozzuoli to rise by several meters, forcing mass relocations.

The historical inflation and deflation of this caldera are exceptionally well documented, thanks to its seaside location and thousands of years of continuous human habitation. 

![Macellum of Pozzuoli](https://upload.wikimedia.org/wikipedia/commons/5/52/Serapeum_%28Pozzuoli%29_-2.jpg)

The most famous evidence is the Roman Macellum of Pozzuoli. Three of its standing marble columns feature distinct bands of holes bored by marine molluscs up to 7 meters above the base. This proves that negative bradyseism once lowered the Roman ruins deep beneath the sea, before a subsequent phase of uplift pushed them back above the water line. Similarly, extensive archaeological ruins, including paved roads and statues, now sit completely submerged off the coast of nearby Baia due to these shifting ground levels.

This dashboard tracks the seismic tremors associated with this ongoing uplift cycle, pulling data from INGV (updated every hour) to provide a clear view of the volcano's current activity.
