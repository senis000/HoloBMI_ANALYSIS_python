# HoloBMI Analysis in python
 Bunch of analysis in python for the HoloBMI paper. 
 Follows similar structure than the python monorepo. 
 However the files will be stored locally (to be shared in globus) 

### Starting with the data
Ideally the data would be store remote so the paths to access it would be the same for 
everyone, but this is not the case. In a perfect world (remote_storage) we would never touched
general_constants, alas....
we need to change in utils/general_constants the local dir

`local_dir = Path("C:/your_local_dir_where_data_is_stored/") `

The data has to keep the following structure:
* raw_data folder: with the original raw files and the following subfolders: 
`raw_data/session_date/mice_name/day`
* curated_data folder: containing the parquet and excel file with info of the sessions. 
The session_filenames.parquet can be retrieved as:
```
from utils.loader import load_sessions_filename
df = load_sessions_filename()
```
df will have the following structure:
* index -> session_date
* columns multiindex: 
    * level 1: _____ Day ________________               Mice_name
    * level 2: 1_round, 2_round,______  file_names, number_files, type of experiment



### Retrieving the data
The loader helps to retrieve information from each session by indicating date and mice:
```   
from utils.loader import SessionLoader 
session_date = '191007' 
mice_name = 'NVI12'
loader = SessionLoader(session_date, mice_name)
```

From loader you can retrieve:

```
# loader.day --> the day (independently of 1st or 2nd round)
# loader.file_baseline --> the name of the mat file retrieved. 
#    (similar for training, pretraining, target_calibration, target_info and holostim)
# loader.pretraining --> type of pre-training experiment
# loader.training --> type of training experiment
# loader.mice_name, loader.session_date --> input values
# loader.session_name --> combination of session and mice_name for storage of analysis
# loader.learning() --> learning results
# loader.results_target_info_dict() --> numpy dictionary with the mat file variables.
#    (similar for baseline, training, pretraining, target_calibration, and holostim)

>> training_dict = loader.experiment_variables.dict_training() 
>> training_dict['data']['selfHits']
  array([0., 0., 0., ..., 0., 0., 0.], dtype=float32)
```









 
 
