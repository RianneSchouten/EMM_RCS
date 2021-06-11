# Folder: data_input

This folder contains the scripts for reading and importing the public datasets.

The HBSC-DNSSSU data is unfortunately not publicly available.

The Mannheim Eurobarometer Trend file can be retrieved from [this](https://search.gesis.org/research_data/ZA3521), [this](https://dbk.gesis.org/dbksearch/sdesc2.asp?no=3521&db=e&notabs=1) or [this](https://www.gesis.org/en/eurobarometer-data-service/search-data-access/eb-trends-trend-files/mannheim-eb-trend-file) link. Script 'preprocess_eurobarometer_data.sps' is used to process the data.

The Brexit dataset is imported from [the UK Data Service](https://reshare.ukdataservice.ac.uk/854869/). Script 'preprocess_brexit_data.sps' is used to process the data.

The Brexit folder furthercontains a subfolder with scripts for the Missing Data Experiments. The datasets are created with generate_missing_data.R.

