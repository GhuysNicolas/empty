import os
# Charger le fichier
input_file_1 = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\CS_1\output\lca_cstr_breakdown.txt"
input_file_2 = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\CS_1\output\lca_op_breakdown.txt"
input_file_3 = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\CS_1\output\lca_res_breakdown.txt"

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

sort_BD(input_file_1)
sort_BD(input_file_2)
sort_BD(input_file_3)

