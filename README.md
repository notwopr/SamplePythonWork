# SamplePythonWork
For the past year, I have been developing and researching algorithms that would improve investment decisions in US Based equities.  I have chosen Python and its libraries to write the code.  Included here is a sample of one part of my project to give you an idea of my Python competency.

The program here is composed of several files.  When you run the program, the host machine calls an API, pulls data, wrangles and cleans it, and saves it to the local disk.  Specifically it pulls all price histories for all US stocks from the NYSE and NASDAQ exchanges, as well as price histories of the US stock exchange indexes (Dow, S&P 500, and NASDAQ) into separate files for each ticker as well as creating an archiving a master dataframe that combines all currently traded ticker histories into one large dataframe for certain functions to reduce runtime.  Due to the large size and number of data points involved, the program harnesses the host machine's multiprocessing capabilities.

Not only does it run a price history pull, it also creates a database of the ticker, their full name, their age, starting date of history and ending dates of history.

INSTRUCTIONS HOW TO RUN
The script will not run without the API keys to access the API data source.  I removed the keys from the code for security reasons.  Please contact me if you wish to run this script in full.
To run the script, you would run the 'MASTERSCRIPT' file.  However, you need to modify the settings in the 'computersettings' file so that it reflects the host machine being used to run the script, in particular, setting the directory location to which the download will save the data, and the number of processors you wish to use for the multiprocessor.

WARNING: You'll notice that the price data for the US exchange indexes will be blank.  That is because the data vendor shut down.  The individual stock tickers should still be available and up to date.

EXTRA MATERIAL
To provide you with a sample that contrasts from an API data pull, I also included a statistical research bot that graphs and visualizes how many samples it would take for an additional sample to move the average of the population an amount less than a specified threshold.

I also included a function that graphs all data points of a set and highlights the outliers based on how strongly you would want to define an outlier to be (e.g. 1.4 standard deviations, 1.6, 2.1, etc.).



