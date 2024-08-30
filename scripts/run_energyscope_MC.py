import datetime
import os
from pathlib import Path
import energyscope as es
import csv

# MODIFY

output_filename = r"C:/Users/ghuysn/GIT_Projects/EnergyScope_LCA/case_studies/MC_outputs/MC_values.csv"

# Output from 1st Algorithm
input_weights = [
    [1.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0],
    [0.2, 0.2, 0.2, 0.2, 0.2]
]

# DO NOT MODIFY
def modify_weights(config, input_weights, j):
    new_weights = input_weights [j]
    if 'Weight_Cost' in config:
        config['Weight_Cost'] = new_weights[0]
    if 'Weight_LCA' in config:
        config['Weight_LCA'] = new_weights[1]
    if 'Weight_Crit1' in config:
        config['Weight_Crit1'] = new_weights[2]
    if 'Weight_Crit2' in config:
        config['Weight_Crit2'] = new_weights[3]
    if 'Weight_Crit3' in config:
        config['Weight_Crit3'] = new_weights[4]
    else:
        raise KeyError("The key 'Weights' does not exist in the config file.")
    return config

if __name__ == '__main__':
    analysis_only = False
    compute_TDs = True

    # define project path
    project_path = Path(__file__).parents[1]

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn='config_ref_MC.yaml', project_path=project_path)
    config['Working_directory'] = os.getcwd()  # keeping current working directory into config
    start_time = datetime.datetime.now()

    for k in range(len(input_weights)):
        config = modify_weights(config, input_weights, k)
        # Reading the data of the csv
        es.import_data(config)

        if compute_TDs:
            es.build_td_of_days(config)

        if not analysis_only:
            # Printing the .dat files for the optimisation problem
            es.print_data(config)
            es.run_es(config)
            print(f"Line {k}")

        if config.get('save_MC_outputs', False):
            try:
                # Read the log file
                log_file_path = config['ampl_options']['log_file']
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r') as log_file:
                        log_contents = log_file.readlines()

                    # Get the last 10 lines
                    last_10_lines = log_contents[-17:-12]
                    # Append the last 10 lines to the output file
                    with open(output_filename, 'a') as f:
                        f.write(''.join(last_10_lines) + '\n')  # Add a newline for separation
                else:
                    print(f"Log file {log_file_path} does not exist.")
            except Exception as e:
                print(f"Error processing log file {log_file_path}: {e}")

    end_time = datetime.datetime.now()
    print(f"Start time: {start_time}")
    print(f"End time: {end_time}")
    duration = end_time - start_time
    print(f"Duration: {duration}")

