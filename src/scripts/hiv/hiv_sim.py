import datetime
import logging
import os
import pandas as pd

from tlo import Date, Simulation
from tlo.analysis.utils import parse_log_file
from tlo.methods import demography, healthsystem, lifestyle, healthburden, hiv, \
    male_circumcision, tb

# Where will output go
outputpath = './src/scripts/outputLogs/'

# date-stamp to label log files and any other outputs
datestamp = datetime.date.today().strftime("__%Y_%m_%d")

# The resource files
resourcefilepath = './resources/'

start_date = Date(2010, 1, 1)
end_date = Date(2019, 1, 1)
popsize = 2000

# Establish the simulation object
sim = Simulation(start_date=start_date)

# Establish the logger
logfile = outputpath + 'LogFile' + datestamp + '.log'

if os.path.exists(logfile):
    os.remove(logfile)
fh = logging.FileHandler(logfile)
fr = logging.Formatter("%(levelname)s|%(name)s|%(message)s")
fh.setFormatter(fr)
logging.getLogger().addHandler(fh)

# ----- Control over the types of intervention that can occur -----
# Make a list that contains the treatment_id that will be allowed. Empty list means nothing allowed.
# '*' means everything. It will allow any treatment_id that begins with a stub (e.g. Mockitis*)
service_availability = ['*']

logging.getLogger('tlo.methods.demography').setLevel(logging.INFO)
logging.getLogger('tlo.methods.lifestyle').setLevel(logging.WARNING)
logging.getLogger('tlo.methods.healthburden').setLevel(logging.INFO)
logging.getLogger('tlo.methods.hiv').setLevel(logging.INFO)
logging.getLogger('tlo.methods.tb').setLevel(logging.WARNING)
logging.getLogger('tlo.methods.male_circumcision').setLevel(logging.INFO)

# Register the appropriate modules
sim.register(demography.Demography(resourcefilepath=resourcefilepath))
sim.register(healthsystem.HealthSystem(resourcefilepath=resourcefilepath))
sim.register(healthburden.HealthBurden(resourcefilepath=resourcefilepath))
sim.register(lifestyle.Lifestyle())
sim.register(hiv.hiv(resourcefilepath=resourcefilepath))
sim.register(tb.tb(resourcefilepath=resourcefilepath))
sim.register(male_circumcision.male_circumcision(resourcefilepath=resourcefilepath))

# Run the simulation and flush the logger
sim.seed_rngs(0)
sim.make_initial_population(n=popsize)
sim.simulate(end_date=end_date)
fh.flush()
# fh.close()


# %% read the results
import datetime
import pandas as pd
from tlo.analysis.utils import parse_log_file
import matplotlib.pyplot as plt

outputpath = './src/scripts/outputLogs/'

# date-stamp to label log files and any other outputs
datestamp = datetime.date.today().strftime("__%Y_%m_%d")
logfile = outputpath + 'LogFile' + datestamp + '.log'
output = parse_log_file(logfile)

deaths_df = output['tlo.methods.demography']['death']
deaths_df['date'] = pd.to_datetime(deaths_df['date'])
deaths_df['year'] = deaths_df['date'].dt.year
death_by_cause = deaths_df.groupby(['year','cause'])['person_id'].size()

