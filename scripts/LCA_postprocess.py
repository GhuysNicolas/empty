import pandas as pd
import os
import numpy as np

lcia_file = r"C:\Users\ghuysn\Documents\PhD\EcoInvent_DBs\LCIA\LCIA_2040.xlsx"

#Path = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\CS_2\output"

#input_file = Path+'\lca_cstr_breakdown_sorted.txt'
#mult_file = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\CS_1\output\lca_res_breakdown_sorted_mult.txt"
def sort_BD(input_file) :
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_sorted{ext}"
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Séparer l'en-tête et les données
    header = lines[0]
    data = lines[1:]

    # Trier les données par ordre alphabétique selon la colonne "Name"
    sorted_data = sorted(data, key=lambda x: x.split("\t")[0])

    # Écrire le résultat dans un nouveau fichier
    with open(output_file, "w") as file:
        file.write(header)
        file.writelines(sorted_data)

    return output_file;
def extract_mult(input_file, lcia_file, sheet_name, acronym):
    # Charger les données du fichier Excel
    txt_file_path = input_file
    txt_data = pd.read_csv(txt_file_path, sep="\t")
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_mult{ext}"
    with open(input_file, "r") as file:
        lines = file.readlines()
    excel_file_path = lcia_file
    excel_data = pd.read_excel(excel_file_path, sheet_name)

    # Vérifier si la colonne nécessaire existe
    if 'LCA_CO2' not in excel_data.columns:
        raise ValueError("La colonne 'LCA_CO2' est absente dans la feuille 'resources'.")

    # Diviser les valeurs de LCA_res par les valeurs correspondantes de LCA_CO2
    # En supposant que les colonnes 'Name' des deux fichiers permettent de faire la correspondance
    merged_data = pd.merge(txt_data, excel_data[['Name', 'LCA_CO2']], on='Name', how='left')

    # Vérifier les valeurs nulles dans la colonne LCA_CO2
    if merged_data['LCA_CO2'].isnull().any():
        raise ValueError("Certaines valeurs de 'Name' dans le fichier texte n'ont pas de correspondance dans le fichier Excel.")

    merged_data['Result'] = merged_data.apply(
        lambda row: 0 if row['LCA_CO2'] == 0 else row['LCA_' + acronym] / row['LCA_CO2'],
        axis=1
    )

    # Garder uniquement les colonnes Name et Result
    final_data = merged_data[['Name', 'Result']]

    # Sauvegarder le résultat dans un nouveau fichier
    final_data.to_csv(output_file, index=False)

    return output_file
def multiply_operation_with_mult(lcia_file, mult_file, sheet_name):
    # Charger les données de la feuille "Operation" du fichier Excel
    excel_data = pd.read_excel(lcia_file, sheet_name=sheet_name)

    # Charger les données du fichier mult
    mult_data = pd.read_csv(mult_file)

    # Générer automatiquement le nom du fichier d'output
    mult_file_dir = os.path.dirname(mult_file)
    output_file = os.path.join(mult_file_dir, f"LCA_{sheet_name}_final.xlsx")  # Ajout de l'extension .xlsx

    # Vérifier la présence des colonnes nécessaires
    if 'Name' not in excel_data.columns or 'Name' not in mult_data.columns:
        raise ValueError("La colonne 'Name' est absente dans l'un des fichiers.")
    if 'Result' not in mult_data.columns:
        raise ValueError("La colonne 'Result' est absente dans le fichier mult.")

    # Fusionner les deux DataFrames sur la colonne 'Name'
    merged_data = pd.merge(excel_data, mult_data[['Name', 'Result']], on='Name', how='inner')

    # Multiplier les valeurs des colonnes de la feuille "Operation" par 'Result'
    numeric_columns = merged_data.select_dtypes(include='number').columns
    for col in numeric_columns:
        if col != 'Result':  # Ne pas multiplier la colonne 'Result' elle-même
            merged_data[col] = merged_data[col] * merged_data['Result']

    # Supprimer la colonne 'Result' après calcul
    final_data = merged_data.drop(columns=['Result'])

    # Sauvegarder le résultat dans un nouveau fichier Excel
    final_data.to_excel(output_file, index=False)

    return output_file
def join_excel_files(file1, file2, file3, sheet_names,Path):

    # Générer automatiquement le nom du fichier d'output
    output_file = Path+"\LCA_final.xlsx"

    # Charger les fichiers Excel
    data1 = pd.read_excel(file1)
    data2 = pd.read_excel(file2)
    data3 = pd.read_excel(file3)

    # Écrire les données dans un fichier Excel avec plusieurs feuilles
    with pd.ExcelWriter(output_file) as writer:
        data1.to_excel(writer, sheet_name=sheet_names[0], index=False)
        data2.to_excel(writer, sheet_name=sheet_names[1], index=False)
        data3.to_excel(writer, sheet_name=sheet_names[2], index=False)

    return  output_file
def add_summary_sheet(input_file):

    # Charger toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(input_file, sheet_name=None)
    summary_sheet_name = 'Total'
    # Dictionnaire pour stocker les sommes par feuille
    sheet_sums = {}

    # Calculer la somme des colonnes pour chaque feuille
    for sheet_name, data in excel_data.items():
        # Sélectionner uniquement les colonnes numériques
        numeric_data = data.select_dtypes(include='number')
        sheet_sums[sheet_name] = numeric_data.sum(axis=0)

    # Créer un DataFrame pour la feuille de résumé
    summary_data = pd.DataFrame(sheet_sums).T  # Transposer pour avoir les colonnes en lignes
    summary_data.loc['Overall Total'] = summary_data.sum(axis=0)  # Ajouter une ligne pour la somme totale

    # Écrire dans le fichier Excel existant
    with pd.ExcelWriter(input_file, mode='a', if_sheet_exists='replace') as writer:
        summary_data.to_excel(writer, sheet_name=summary_sheet_name)

    return input_file
def PB_postprocess_run(file_path, path) :
    output_file_csv = path + "\PB_final.csv"
    # Charger la feuille "Total"
    data = pd.read_excel(file_path, sheet_name='Total')
    # Extraire la ligne contenant "overall total"
    overall_total_row = data[data.apply(lambda row: row.astype(str).str.contains('overall total', case=False).any(), axis=1)]
    # Vérifiez que la ligne a été extraite correctement
    if overall_total_row.empty:
        print("La ligne 'overall total' n'a pas été trouvée.")
    else:
        # Définir les labels et les valeurs PB_world
        Labels = [
            'LCA_ACIDIFICATION', 'LCA_CO2', 'LCA_ECOTOXICITY', 'LCA_FRESHWATER_EUT',
            'LCA_MARINE_EUT', 'LCA_TERRESTRIAL_EUT', 'LCA_HUMAN_TOXICITY_CARC',
            'LCA_HUMAN_TOXICITY_NOCARC', 'LCA_IONIZING_RADIATION', 'LCA_LANDUSE',
            'LCA_MINERAL_DEPLETION', 'LCA_PARTICULATE_MATTER', 'LCA_OZONE_TROPOS',
            'LCA_WATER_DEPLETION', 'LCA_ABIOTIC_DEPLETION', 'LCA_OZONE_DEPLETION'
        ]
        PB_world = [
            1.00E+12, 6.81E+12, 1.31E+14, 5.81E+09, 2.01E+11, 6.13E+12,
            9.62E+05, 4.10E+06, 5.27E+14, 1.27E+13, 2.19E+08, 5.16E+05,
            4.07E+11, 1.82E+14, 2.24E+14, 5.39E+08
        ]

        PIB_BE = 583
        POP_BE = 11
        POP_WO = 8000
        PIB_WO = 101000
        SHARE_BE_PIB = (PIB_BE/PIB_WO)/1000000
        SHARE_BE = (POP_BE / POP_WO) / 1000000
        PB_BE = [value * SHARE_BE for value in PB_world]

        # Extraire les valeurs de la ligne 'overall total' (assume labels in first column)
        overall_total_values = overall_total_row.iloc[0, 1:].to_numpy(dtype=float)  # Convertir en tableau numpy

        # Convertir PB_world en tableau numpy
        PB_BE_array = np.array(PB_BE, dtype=float)

        # Effectuer la division élément par élément
        division_result = overall_total_values / PB_BE_array

        # Créer un DataFrame pour afficher les résultats avec les labels
        result_df = pd.DataFrame({
            'Label': Labels,
            'Overall_Total': overall_total_values,
            'PB_BE': PB_BE_array,
            'Result': division_result
        })
        result_df.to_csv(output_file_csv, index=False)
    return result_df
def LCA_postprocess_run (Path) :
    op_file = Path + '\lca_op_breakdown.txt'
    cstr_file = Path + '\lca_cstr_breakdown.txt'
    res_file = Path + '\lca_res_breakdown.txt'

    op_file_sorted = sort_BD(op_file)
    cstr_file_sorted = sort_BD(cstr_file)
    res_file_sorted = sort_BD(res_file)

    op_file_mult = extract_mult(op_file_sorted, lcia_file, "Operation", 'op')
    cstr_file_mult = extract_mult(cstr_file_sorted, lcia_file, "Construction", 'tech')
    res_file_mult = extract_mult(res_file_sorted, lcia_file, "Resources", 'res')

    op_file_lca = multiply_operation_with_mult(lcia_file, op_file_mult, "Operation")
    cstr_file_lca = multiply_operation_with_mult(lcia_file, cstr_file_mult, "Construction")
    res_file_lca = multiply_operation_with_mult(lcia_file, res_file_mult, "Resources")

    lca_all = join_excel_files(op_file_lca, cstr_file_lca, res_file_lca, ['Operation', 'Construction', 'Resources'],Path)

    lca_final = add_summary_sheet(lca_all)

    output_final = PB_postprocess_run(lca_final,Path)

    print(f"Le fichier résultant a été sauvegardé dans : {Path}"+r"\LCA_final.xlsx")

    return output_final
def plot_solo_spider(file_path,c,k):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    # Load the data
    data = pd.read_csv(file_path)

    # Extract labels and results
    labels = data['Label']
    results = data['Result']

    # Prepare angles for the spider plot
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    # Apply log scale to results
    results = [np.log10(value/c) if value > 0 else -2 for value in results]
    results += results[:1]  # Close the loop

    # Create the spider plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    # Plot the results
    ax.plot(angles, results, label="Results", linewidth=2)
    ax.fill(angles, results, alpha=0.25)

    # Add reference lines for risk zones
    ax.plot(angles, [np.log10(1)] * len(angles), color='green', linestyle='--', linewidth=1, label='Safe zone')
    ax.plot(angles, [np.log10(2)] * len(angles), color='yellow', linestyle='--', linewidth=1, label='Uncertain zone')
    ax.plot(angles, [np.log10(3)] * len(angles), color='red', linestyle='--', linewidth=1, label='High risk zone')

    # Customize y-axis for log scale
    ax.set_yticks([-2, -1, 0, 1, 2])  # Log scale tick positions
    ax.set_yticklabels(["0.01", "0.1", "1", "10", "100"])  # Corresponding log scale labels

    # Add labels and title
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, rotation=45, ha='right')
    ax.set_title("Log-Scaled Spider Plot: Results Overview", va='bottom')

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    # Save the plot in the same directory as the input file
    output_path = os.path.join(os.path.dirname(file_path))
    plt.savefig(str(output_path) + f'\\PB_final_figure_{k}.svg', format='svg', bbox_inches='tight')
    plt.close()

    print(f"Spider plot saved to: {output_path}")

LCA_postprocess_run(r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\2020\output")
#Solo_PBs_path = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\MC\MC_1\output\PB_final.csv"

#plot_solo_spider(Solo_PBs_path,10)