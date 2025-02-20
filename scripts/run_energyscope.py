# -*- coding: utf-8 -*-
"""
This script modifies the input data and runs the EnergyScope model

@author: Paolo Thiran, Matija Pavičević, Xavier Rixhon, Gauthier Limpens
"""

import os
from pathlib import Path
import energyscope as es
import matplotlib.pyplot as plt
from LCA_postprocess import LCA_postprocess_run
from LCA_postprocess import plot_solo_spider
if __name__ == '__main__':
    analysis_only = False
    compute_TDs = True

    # define project path
    project_path = Path(__file__).parents[1]

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
    Path_output = str(config['cs_path'] / config['case_study'] / 'output')
    config['Working_directory'] = os.getcwd() # keeping current working directory into config

   # Reading the data of the csv
    es.import_data(config)

    if compute_TDs:
        es.build_td_of_days(config)

    if not analysis_only:
        # Printing the .dat files for the optimisation problem       
        es.print_data(config)

        # Running EnergyScope
        es.run_es(config)
    if config['LCA_postprocess']:
        test = LCA_postprocess_run(Path_output)
        plot_PB = plot_solo_spider(str(Path_output) + '\PB_final.csv',1,1) #c=4.2 for GDP share
    # Example to print the sankey from this script
    if config['print_sankey']:
        sankey_path = config['cs_path']/ config['case_study'] / 'output' / 'sankey'
        es.drawSankey(path=sankey_path)

    # Reading outputs
    outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN'])
    elec_assets = es.get_assets_l(layer='ELECTRICITY', eff_tech=config['all_data']['Layers_in_out'],
                                  assets=outputs['assets'])
    # Plots (examples)
    # primary resources used
    if config['print_barh']:
        fig2, ax2 = es.plot_barh(outputs['resources_breakdown'][['Used']], title='Primary energy [GWh/y]')
        fig3, ax3 = es.plot_barh(elec_assets[['f']], title='Electricity assets [GW_e]',
                                 x_label='Installed capacity [GW_e]')
        path_to_fig_1 = str(Path_output + "\Cluster_1.png")
        path_to_fig_2 = str(Path_output + "\Cluster_2.png")
        print("clusters save")
        # Save the figures to the specified paths
        fig2.savefig(path_to_fig_1, dpi=300, bbox_inches='tight')
        plt.close(fig2)  # Ensure the figure is closed after saving
        fig3.savefig(path_to_fig_2, dpi=300, bbox_inches='tight')
        plt.close(fig3)

    # layer_HEAT_LOW_T_DECEN for the 12 tds
    if config['print_hourly_data']:
        fig, ax = es.hourly_plot(plotdata=outputs['layer_HEAT_LOW_T_DECEN'], nbr_tds=12, show_plot=True)
        plt.close(fig)
        elec_layer_plot = es.plot_layer_elec_td(outputs['layer_ELECTRICITY'])
        plt.close(elec_layer_plot)



    
    