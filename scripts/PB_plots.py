import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

output_path_bar = str(r'C:\Users\ghuysn\Documents\PhD\MY_ARTICLES\PB-LCIA\PBs_bar_log.svg')
output_path_spyder_PB = str(r'C:\Users\ghuysn\Documents\PhD\MY_ARTICLES\PB-LCIA\PBs_spyder.svg')
output_path_spyder_LCA = str(r'C:\Users\ghuysn\Documents\PhD\MY_ARTICLES\PB-LCIA\LCA_spyder.svg')
def extract_years_PB(base_path):
    # Lister les années présentes dans le dossier START
    years = [year for year in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, year))]

    # Initialiser des DataFrames pour stocker les résultats finaux
    final_df_result = pd.DataFrame()
    final_df_overall = pd.DataFrame()

    for year in years:
        # Chemin vers le fichier PB_final.csv
        file_path = os.path.join(base_path, year, "output", "PB_final.csv")

        if os.path.exists(file_path):
            # Charger le fichier CSV pour l'année en cours
            data = pd.read_csv(file_path)

            # Vérifier si les colonnes nécessaires sont présentes pour 'Result'
            if 'Label' in data.columns and 'Result' in data.columns:
                extracted_data_result = data[['Label', 'Result']].copy()
                extracted_data_result.rename(columns={'Result': year}, inplace=True)

                # Fusionner avec le DataFrame final pour 'Result'
                if final_df_result.empty:
                    final_df_result = extracted_data_result
                    label_order_result = extracted_data_result['Label'].tolist()
                else:
                    final_df_result = pd.merge(final_df_result, extracted_data_result, on='Label', how='outer')
                final_df_result = final_df_result.set_index('Label').reindex(label_order_result).reset_index()

            # Vérifier si les colonnes nécessaires sont présentes pour 'Overall_total'
            if 'Label' in data.columns and 'Overall_Total' in data.columns:
                extracted_data_overall = data[['Label', 'Overall_Total']].copy()
                extracted_data_overall.rename(columns={'Overall_Total': year}, inplace=True)

                # Fusionner avec le DataFrame final pour 'Overall_total'
                if final_df_overall.empty:
                    final_df_overall = extracted_data_overall
                    label_order_overall = extracted_data_overall['Label'].tolist()
                else:
                    final_df_overall = pd.merge(final_df_overall, extracted_data_overall, on='Label', how='outer')
                final_df_overall = final_df_overall.set_index('Label').reindex(label_order_overall).reset_index()

        else:
            print(f"Fichier non trouvé pour l'année {year}: {file_path}")

    # Sauvegarder les DataFrames finaux dans des fichiers CSV
    output_file_result = os.path.join(base_path, "PB_final_combined.csv")
    final_df_result.to_csv(output_file_result, index=False)
    print(f"Fichier combiné pour 'Result' sauvegardé sous {output_file_result}.")

    output_file_overall = os.path.join(base_path, "LCA_final_combined.csv")
    final_df_overall.to_csv(output_file_overall, index=False)
    print(f"Fichier combiné pour 'Overall_total' sauvegardé sous {output_file_overall}.")

    return output_file_result
def plot_PBs_chart(file_path):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Recharger le fichier CSV
    data = pd.read_csv(file_path)

    # Extraire les années (colonnes sauf la première qui contient les labels)
    years = data.columns[1:]

    # Créer une figure et des barres empilées avec une couleur différente par année
    x = np.arange(len(data['Label']))  # Indices pour les labels
    width = 0.8 / len(years)  # Largeur des barres individuelles

    plt.figure(figsize=(15, 7))
    for i, year in enumerate(years):
        plt.bar(x + i * width, data[year], width, label=year, log=True)  # Ajouter log=True pour une échelle logarithmique

    # Ajouter une ligne horizontale à la valeur 1
    plt.axhline(y=3, color='red', linestyle='--', linewidth=1, label='High risk zone')
    plt.axhline(y=2, color='yellow', linestyle='--', linewidth=1, label='Uncertain zone')
    plt.axhline(y=1, color='green', linestyle='--', linewidth=1, label='Safe zone')

    # Ajouter les labels des axes et personnaliser le graphique
    plt.xticks(x + (len(years) - 1) * width / 2, data['Label'], rotation=90)
    #plt.ylabel('I')
    plt.xlabel('Labels')
    plt.title('Energy system impact on PBs through transition ')
    plt.legend()

    # Afficher le graphique
    plt.tight_layout()
    plt.savefig(output_path_bar)
    plt.show()
    return
def normalize_by_first_column(file_path, output_path):
    # Vérifier que la colonne '2020' existe
    data = pd.read_csv(file_path)
    if '2020' not in data.columns:
        raise ValueError("La colonne '2020' est absente du fichier.")

    # Stocker la colonne '2020' comme référence
    reference_column = data['2020']

    # Normaliser toutes les colonnes sauf 'Label' par la colonne '2020'
    for col in data.columns[1:]:  # Exclure 'Label' mais inclure '2020'
        data[col] = data[col] / reference_column

    # Sauvegarder le DataFrame normalisé
    data.to_csv(output_path, index=False)
    return output_path

    # Sauvegarder le résultat dans un nouveau fichier CSV
    data.to_csv(output_path, index=False)
    return output_path
def plot_LCA_spider(file_path):
    data = pd.read_csv(file_path)
    years = data.columns[1:]
    labels = data['Label']

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    for year in years:
        values = data[year].tolist()
        values += values[:1]  # Close the loop

        if year in ['2050', '2020']:
            ax.plot(angles, values, label=year, linewidth=2)
            ax.fill(angles, values, alpha=0.25)
        else:
            ax.plot(angles, values, label=year, linewidth=2)


    ax.set_yticks([1, 2, 3])  # Normal scale tick positions
    ax.set_yticklabels(["1", "2", "3"])  # Corresponding normal scale labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, rotation=45, ha='right')
    ax.set_title("Spider Plot: PB Impact Through Transition", va='bottom')

    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.savefig(output_path_spyder_LCA)
    plt.tight_layout()
    plt.show()
def plot_PBs_spider(file_path):
    data = pd.read_csv(file_path)
    years = data.columns[1:]
    labels = data['Label']

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    for year in years:
        values = data[year].tolist()
        values = [np.log10(value) if value > 0 else -2 for value in values]  # Convert to log scale
        values += values[:1]  # Close the loop

        if year in ['2050', '2020']:
            ax.plot(angles, values, label=year, linewidth=2)
            ax.fill(angles, values, alpha=0.25)
        else:
            ax.plot(angles, values, label=year, linewidth=2)

    # Add reference lines for risk zones
    ax.plot(angles, [np.log10(1)] * len(angles), color='green', linestyle='--', linewidth=1, label='Safe zone')
    ax.plot(angles, [np.log10(2)] * len(angles), color='yellow', linestyle='--', linewidth=1, label='Uncertain zone')
    ax.plot(angles, [np.log10(3)] * len(angles), color='red', linestyle='--', linewidth=1, label='High risk zone')

    ax.set_yticks([-2, -1, 0, 1, 2])  # Log scale tick positions
    ax.set_yticklabels(["0.01", "0.1", "1", "10","100"])  # Corresponding log scale labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, rotation=45, ha='right')
    ax.set_title("Log-Scaled Spider Plot: PB Impact Through Transition", va='bottom')

    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(output_path_spyder_PB)
    plt.show()
def plot_solo_spider(file_path,k):
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
    results = [np.log10(value*k) if value > 0 else -2 for value in results]
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
    output_path = os.path.join(os.path.dirname(file_path), "Spider_Plot_Results_Log_Scale.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

    print(f"Spider plot saved to: {output_path}")


#extract_years_PB(path)

PBs_path = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\PB_final_combined.csv"
LCA_path = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\LCA_final_combined.csv"
LCA_path_normalised = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\START\LCA_final_combined_normalised.csv"
Solo_PBs_path = r"C:\Users\ghuysn\GIT_Projects\EnergyScope_LCA\case_studies\ARTICLE_PB-LCA\MC\MC_1\output\PB_final.csv"
#plot_PBs_chart(path)
#LCA_path_normalized = normalize_by_first_column(LCA_path,LCA_path_normalised)
#plot_LCA_spider(LCA_path_normalized)
plot_PBs_spider(PBs_path)
plot_solo_spider(Solo_PBs_path,10)