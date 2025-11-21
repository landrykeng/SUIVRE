import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from Authentification import *
from Fonction import *
from streamlit_echarts import st_echarts

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord collecte CHEQUE SANTE",
    layout="wide",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/6/6b/Bitmap_Icon_FOSA.png"
)


st.session_state.df_rejet=pd.read_excel("Data_collected.xlsx",sheet_name="Rejet")
st.session_state.df_synthese=pd.read_excel("Data_collected.xlsx",sheet_name="Synthese")
st.session_state.df_initial=pd.read_excel("Data_collected.xlsx",sheet_name="Initial")

#===========================IMPORTATION DES DONNEES=====================================
# IMPORTATION DES DONNES


data_rejet=st.session_state.df_rejet
data_synthese=st.session_state.df_synthese
data_initial=st.session_state.df_initial

data_initial["Mois"]=data_initial["Mois"].replace({"Fervrier":"Février"})
data_synthese["Mois"]=data_synthese["Mois"].replace({"Fervrier":"Février"})
data_rejet["Mois"]=data_rejet["Mois"].replace({"Fervrier":"Février"})

data_rejet=data_rejet[data_rejet['Numéro de chèque'].notna()]
#
echantillon=pd.read_excel("Echantillon.xlsx")
echantillon["District"]=echantillon["District"].replace(VALUE_SETS["s0q02"])
echantillon["Région"]=echantillon["Région"].replace(VALUE_SETS["s0q01"])

for col in data_rejet.select_dtypes(include='number').columns:
    data_rejet[col] = data_rejet[col].astype('Int64')   # garde les NaN
    
for col in data_synthese.select_dtypes(include='number').columns:
    data_synthese[col] = data_synthese[col].astype('Int64')   # garde les NaN
    
for col in data_initial.select_dtypes(include='number').columns:
    data_initial[col] = data_initial[col].astype('Int64')   # garde les NaN

#===========================================================================================
# CSS personnalisé pour un design ultra-moderne
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Fond principal avec dégradé subtil */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        animation: gradientShift 15s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar stylisée */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        box-shadow: 4px 0 15px rgba(100,0,0,0.9);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Logo dans la sidebar */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 20px auto;
        transition: transform 0.3s ease;
    }
    
    /* Boutons dans la sidebar */
    .sidebar-button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px 20px;
        margin: 10px 0;
        color: white;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
        width: 100%;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .sidebar-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-button.active {
        background: rgba(255, 255, 255, 0.25);
        border-left: 4px solid #f39c12;
    }
    
    /* Titre principal avec animation */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 30px 0;
        font-weight: 700;
        font-size: 2.5em;
        animation: fadeInDown 1s ease;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Cartes métriques améliorées */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transition: all 1.3s ease;
        animation: fadeInUp 1.8s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .metric-label {
        font-size: 14px;
        opacity: 0.95;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    
    
    
    
    /* Alternative : cibler directement l'iframe */
    iframe[title*="echarts"] {
        border-radius: 20px;
    }
    
    /* Cibler le parent direct */
    .element-container:has(iframe[title*="echarts"]) {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,100,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.2s ease;
    }
    
    .element-container:has(iframe[title*="echarts"]):hover {
        box-shadow: 0 12px 40px rgba(0,0,150,0.5);
        transform: translateY(-2px);
    }
    
    /* Titres de sections */
    h3 {
        color: #2c3e50;
        font-weight: 600;
        padding: 15px 0;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-image-slice: 1;
        margin-bottom: 20px;
        animation: slideInLeft 0.8s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Ligne de séparation stylisée */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        margin: 30px 0;
    }
    
    /* Boutons Streamlit personnalisés */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Amélioration des selectbox et inputs */
    .stSelectbox, .stMultiSelect {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Footer stylisé */
    .footer {
        text-align: center;
        color: #666;
        padding: 30px;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin-top: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Animation de chargement */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Effets de brillance sur les cartes */
    @keyframes shine {
        0% {
            background-position: -200% center;
        }
        100% {
            background-position: 200% center;
        }
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        );
        transition: 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8em;
        }
        
        .metric-value {
            font-size: 24px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar élégante avec menu de navigation
with st.sidebar:
    # Logo/Icône en haut
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); 
                        width: 200px; height: 80px; margin: 0 auto; border-radius: 15px;
                        display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
                <span style='font-size: 30px;'>CHEQUE SANTE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Section filtres
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); 
                    border-radius: 10px; padding: 15px; margin: 20px 0;
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h4 style='color: white; margin: 0 0 15px 0; font-size: 16px;'>📅 Filtres</h4>
        </div>
    """, unsafe_allow_html=True)
    
    region=st.multiselect("Région", data_rejet["Région"].unique(),default=data_rejet["Région"].unique())
    fosa = st.multiselect("Statut FOSA", ["SONUC","SONUB"],default=["SONUC","SONUB"])
    annee = st.multiselect("Année", [2023,2024],default=[2023,2024])
    # Sélecteur de période
    mois = st.multiselect("Période", data_rejet["Mois"].unique(), default=data_rejet["Mois"].unique())
    
    st.markdown("<br>", unsafe_allow_html=True)

rejet_to_use=data_rejet[data_rejet['Région'].isin(region)] if len(region)!=0 else data_rejet
rejet_to_use=data_rejet[data_rejet['Statut FOSA'].isin(fosa)] if len(fosa)!=0 else data_rejet
rejet_to_use=rejet_to_use[rejet_to_use['annee'].isin(annee)] if len(annee)!=0 else rejet_to_use
rejet_to_use=rejet_to_use[rejet_to_use['Mois'].isin(mois)] if len(mois)!=0 else rejet_to_use

synthese_to_use=data_synthese[data_synthese['Région'].isin(region)] if len(region)!=0 else data_synthese
synthese_to_use=data_synthese[data_synthese['Statut FOSA'].isin(fosa)] if len(fosa)!=0 else data_synthese
synthese_to_use=synthese_to_use[synthese_to_use['annee'].isin(annee)] if len(annee)!=0 else synthese_to_use
synthese_to_use=synthese_to_use[synthese_to_use['Mois'].isin(mois)] if len(mois)!=0 else synthese_to_use

initial_to_use=data_initial[data_initial['Région'].isin(region)] if len(region)!=0 else data_initial
initial_to_use=data_initial[data_initial['Statut FOSA'].isin(fosa)] if len(fosa)!=0 else data_initial
#initial_to_use=initial_to_use[initial_to_use['annee'].isin(annee)] if len(annee)!=0 else initial_to_use
initial_to_use=initial_to_use[initial_to_use['Mois'].isin(mois)] if len(mois)!=0 else initial_to_use

# Titre principal
st.markdown("# 📊 Tableau de bord de l'enquête- CHEQUE SANTE 2025")

#afficher_toutes_les_10_secondes()

#st.success(f"Dernière mise à jour effectuée avec succès à {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")
#st.session_state.last_update=datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
update=st.button("Mettre à jour le tableau de bord")
if update:
    upgrade_data()
    
st.info("Si vous êtes sur PC, ajuster le zoom de votre navigateur à 80% pour une meilleure expérience visuelle. (ctrl + -)", icon="ℹ️")
tab_=st.tabs(["**Indicateurs**",
              "**Prestations Forfaitaires**",
              "**Prestations Plafonnées SONUB**",
              "**Prestations Plafonnées SONUC**",
              "**Non médicales**",
              "**Dashboard**", 
              "**Personnel**"])


#==============ONGLET DONNEES==========================
#with tab_[0]:   
  #  st.write("### Données sur les chèque rejetés et acceptés")
   # st.dataframe(data_rejet)
   # st.write("### Données de synthèse")
   # st.dataframe(data_synthese)
  #  valide=data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
  #  recu=data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()
   # st.write("### Données initiales")
   # st.dataframe(data_initial)
    

#==============ONGLET INDICATEURS==========================
with tab_[0]:
    cf=st.columns(2)
    with cf[0]:
        fosa2=st.multiselect("Choisir le statut de la FOSA", options=["SONUB","SONUC"], default=["SONUB","SONUC"])
    with cf[1]:
        region2=st.multiselect("Choisir la (les) régions(s)", options=data_rejet["Région"].unique(), default=data_rejet["Région"].unique())
    
    data_rejet=data_rejet[data_rejet["Région"].isin(region2)] if len(region2)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Statut FOSA"].isin(fosa2)] if len(fosa2)!=0 else data_rejet
    
    montant=data_rejet.groupby("statut du chèque").agg({"Montant rejeté par le CM":"sum"}).reset_index()
    
    
    # Tableau croisé : somme du "Montant rejeté par le CM" par "Catégorie" et "statut du chèque"
    montant_cat_statut = pd.pivot_table(
        data_rejet,
        index="Catégorie",
        columns="statut du chèque",
        values="Montant rejeté par le CM",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Convertir les colonnes de montants en Int64 pour garder les NaN si besoin
    for col in montant_cat_statut.columns[1:]:
        montant_cat_statut[col] = montant_cat_statut[col].astype("Int64")

    # Exposer le dataframe pour réutilisation éventuelle
    montant_cat_statut["Ordre de recette des FOSA"] = montant_cat_statut["Rejet TOTAL selon le CM"]+montant_cat_statut["Rejet PARTIEL selon le CM"]
    montant_cat_statut["A verser par l'Etat"]=montant_cat_statut["Validé BON A PAYER selon le CM"]  
    
    df_montant_cat_statut=montant_cat_statut[["Catégorie","Ordre de recette des FOSA", "A verser par l'Etat"]]
    st.caption("Analyse sur les montants")
    kpi_col3=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col3[0]:
        montant_associe = montant.loc[montant["statut du chèque"].isin(["Rejet TOTAL selon le CM","Rejet PARTIEL selon le CM"]) , "Montant rejeté par le CM"].sum()
        montant_to_reciev = int(montant_associe) if not pd.isna(montant_associe) else 0
        display_single_metric_advanced("Ordre de recette des FOSA",montant_to_reciev, delta=0, color_scheme="green", unit="XAF")
    
    with kpi_col3[1]:
        montant_associe2 = montant.loc[montant["statut du chèque"]=="Validé BON A PAYER selon le CM" , "Montant rejeté par le CM"].sum()
        montant_to_pay = int(montant_associe2) if not pd.isna(montant_associe2) else 0
        display_single_metric_advanced("Montant à reverser par l'Etat au FOSA",montant_to_pay, delta=0,color_scheme="red", unit="XAF")
    with kpi_col3[2]: 
        taux_global_NV=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()-synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Montant à net recevoir des FOSA",montant_to_reciev-montant_to_pay, delta=0,color_scheme="orange", unit="XAF")

    st.write(" ")
  
    cc=st.columns([4,2])
    with cc[0]:
        # Bar chart groupé (non empilé) avec étiquettes de données pour df_montant_cat_statut
        if df_montant_cat_statut is None or df_montant_cat_statut.empty:
            st.info("Aucune donnée disponible pour le graphique des montants.")
        else:
            # identifier colonne de catégorie et colonnes de valeurs
            cat_col = df_montant_cat_statut.columns[0]
            value_cols = [c for c in df_montant_cat_statut.columns if c != cat_col]

            df_plot = df_montant_cat_statut.fillna(0)
            labels = df_plot[cat_col].astype(str).tolist()

            # construire les séries (barres groupées) avec étiquettes visibles
            base_colors = ["#5470C6", "#91CC75", "#EE6666", "#FAC858", "#73C0DE", "#3BA272"]
            series = []
            for i, col in enumerate(value_cols):
                series.append({
                    "name": str(col),
                    "type": "bar",
                    "barWidth": "20%",
                    "data": df_plot[col].astype(float).tolist(),
                    "label": {"show": True, "position": "top", "formatter": "{c}"},
                    "itemStyle": {"color": base_colors[i % len(base_colors)]}
                })

            ymax = int(df_plot[value_cols].to_numpy().max() * 1.1) if len(value_cols) > 0 else 0

            options = {
                "backgroundColor": "transparent",
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "legend": {"data": [str(c) for c in value_cols], "top": "6%"},
                "grid": {"left": "6%", "right": "4%", "bottom": "12%", "containLabel": True},
                "xAxis": [{"type": "category", "data": labels, "axisLabel": {"rotate": 30, "interval": 0}}],
                "yAxis": [{"type": "value", "min": 0, "max": ymax}],
                "series": series
            }

            st_echarts(options=options, height="480px", key="montant_cat_statut_chart")
    
    with cc[1]:
        nb_fosa_to_audit=echantillon.shape[0]
        fosa_edited=len(data_initial["FOSA"].unique())
        taux_global_rejet=(round(100*data_rejet.shape[0]/data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum(),2))
        display_single_metric_advanced("Taux global de rejet",taux_global_rejet, delta=0, color_scheme="green", unit="%")
        st.write(" ")
        taux_global_V=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Validé selon MC"].shape[0])/data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum(),2))
        display_single_metric_advanced("Taux rejet factures valides",taux_global_V, delta=0,color_scheme="red", unit="%")

        st.write(" ")
        taux_global_NV=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()-data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Taux réhabilitation facture NV",taux_global_NV, delta=0,color_scheme="orange", unit="%")

    #============================================================================================================
    
        
    # Construction d'un dataframe par District avec les 3 taux demandés
    districts = sorted(list(data_rejet["District"].dropna().unique()))
    if "District" in data_synthese.columns:
        synth_districts = list(data_synthese["District"].dropna().unique())
        for d in synth_districts:
            if d not in districts:
                districts.append(d)

    rows = []
    for d in districts:
        # numérateurs
        rej_count = data_rejet[data_rejet["District"] == d].shape[0]
        valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Validé selon MC")].shape[0]
        non_valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Rejeté selon MC")].shape[0]

        # dénominateurs (par district si disponible sinon total)
        if "District" in data_synthese.columns:
            total_recu = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE RECU"].sum()
            total_valide_mc = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
        else:
            total_recu = data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()
            total_valide_mc = data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()

        denom_nv = total_recu - total_valide_mc

        taux_rejet = (100 * rej_count / total_recu) if total_recu and total_recu > 0 else np.nan
        taux_V = (100 * valid_count / total_valide_mc) if total_valide_mc and total_valide_mc > 0 else np.nan
        taux_NV = (100 * non_valid_count / denom_nv) if denom_nv and denom_nv > 0 else np.nan

        rows.append({
            "District": d,
            "taux_global_rejet": round(taux_rejet, 2) if not pd.isna(taux_rejet) else np.nan,
            "taux_global_V": round(taux_V, 2) if not pd.isna(taux_V) else np.nan,
            "taux_global_NV": round(taux_NV, 2) if not pd.isna(taux_NV) else np.nan,
        })

    df_taux_par_district = pd.DataFrame(rows).sort_values("District").reset_index(drop=True)
    st.caption("Taux de rejet, Taux rejet factures valides et Taux réhabilitation facture non validé (en %) — survolez les barres pour voir les valeurs.")
    col_tx=st.columns([10,1])
     
    with col_tx[0]:
        # Préparer les données (remplacer les NaN par 0 pour l'affichage)
        df_plot = df_taux_par_district.copy().fillna(0)
        labels = df_plot["District"].astype(str).tolist()
        rej = df_plot["taux_global_rejet"].tolist()
        val = df_plot["taux_global_V"].tolist()
        nonval = df_plot["taux_global_NV"].tolist()


        options = {
            "backgroundColor": "transparent",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b0}<br/>{a0}: {c0}%<br/>{a1}: {c1}%<br/>{a2}: {c2}%"
            },
            "legend": {
                "data": ["Taux rejet", "Taux rejet FV", "Taux  réhabilitation FNV"],
                "top": "6%",
                "textStyle": {"color": "#2c3e50"}
            },
            "grid": {"left": "6%", "right": "4%", "bottom": "8%", "containLabel": True},
            "xAxis": [
                {
                    "type": "category",
                    "data": labels,
                    "axisTick": {"alignWithLabel": True},
                    "axisLabel": {"rotate": 30, "interval": 0, "color": "#34495e"},
                    "axisLine": {"lineStyle": {"color": "#ecf0f1"}}
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "name": "%",
                    "min": 0,
                    "max": np.max([np.max(rej), np.max(val), np.max(nonval)])+5,
                    "axisLabel": {"formatter": "{value} %", "color": "#34495e"},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#ecf0f1"}}
                }
            ],
            "color": [
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#f73c42"}, {"offset": 1, "color": "#fad0c4"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#5512f1"}, {"offset": 1, "color": "#fbc2eb"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#16dbe9"}, {"offset": 1, "color": "#66a6ff"}]}
            ],
            "series": [
                {
                    "name": "Taux rejet",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": rej,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux rejet FV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": val,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux  réhabilitation FNV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": nonval,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                }
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "Enregistrer"},
                    "dataView": {"title": "Données", "readOnly": True}
                },
                "right": 10
            }
        }

        st_echarts(options=options, height="520px", key="tau")
    
    


#==============ONGLET FORFAITAIRES ===================
with tab_[1]:
    data_rejet=st.session_state.df_rejet
    data_synthese=st.session_state.df_synthese
    cf1=st.columns(2)
    with cf1[0]:
        fosa3=st.multiselect("Choisir le statut de la FOSA", options=["SONUB","SONUC"], default=["SONUB","SONUC"],key="fosa3")
    with cf1[1]:
        region3=st.multiselect("Choisir la (les) régions(s)", options=data_rejet["Région"].unique(), default=data_rejet["Région"].unique(), key="region3")
    
    data_rejet=data_rejet[data_rejet["Catégorie"]=="Forfaitaires"]
    data_synthese=data_synthese[data_synthese["Type de prestation"]=="Forfaitaires"]
    
    data_rejet=data_rejet[data_rejet["Région"].isin(region3)] if len(region3)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Statut FOSA"].isin(fosa3)] if len(fosa3)!=0 else data_rejet
    
    montant=data_rejet.groupby("statut du chèque").agg({"Montant rejeté par le CM":"sum"}).reset_index()
    
    
    # Tableau croisé : somme du "Montant rejeté par le CM" par "Catégorie" et "statut du chèque"
    montant_cat_statut = pd.pivot_table(
        data_rejet,
        index="Catégorie",
        columns="statut du chèque",
        values="Montant rejeté par le CM",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Convertir les colonnes de montants en Int64 pour garder les NaN si besoin
    for col in montant_cat_statut.columns[1:]:
        montant_cat_statut[col] = montant_cat_statut[col].astype("Int64")

    # Exposer le dataframe pour réutilisation éventuelle
    # S'assurer que les colonnes attendues existent; les créer avec 0 si elles manquent
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        if _col not in montant_cat_statut.columns:
            montant_cat_statut[_col] = 0
    # Convertir en numérique et remplacer NaN par 0, garder le type Int64
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        montant_cat_statut[_col] = pd.to_numeric(montant_cat_statut[_col], errors="coerce").fillna(0).astype("Int64")

    montant_cat_statut["Ordre de recette des FOSA"] = montant_cat_statut["Rejet TOTAL selon le CM"] + montant_cat_statut["Rejet PARTIEL selon le CM"]
    montant_cat_statut["A verser par l'Etat"]=montant_cat_statut["Validé BON A PAYER selon le CM"]  
    
    df_montant_cat_statut=montant_cat_statut[["Catégorie","Ordre de recette des FOSA", "A verser par l'Etat"]]
    st.caption("Analyse sur les montants")
    kpi_col4=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col4[0]:
        montant_associe = montant.loc[montant["statut du chèque"].isin(["Rejet TOTAL selon le CM","Rejet PARTIEL selon le CM"]) , "Montant rejeté par le CM"].sum()
        montant_to_reciev = int(montant_associe) if not pd.isna(montant_associe) else 0
        display_single_metric_advanced("Ordre de recette des FOSA",montant_to_reciev, delta=0, color_scheme="green", unit="XAF")
    
    with kpi_col4[1]:
        montant_associe2 = montant.loc[montant["statut du chèque"]=="Validé BON A PAYER selon le CM" , "Montant rejeté par le CM"].sum()
        montant_to_pay = int(montant_associe2) if not pd.isna(montant_associe2) else 0
        display_single_metric_advanced("Montant à reverser par l'Etat au FOSA",montant_to_pay, delta=0,color_scheme="red", unit="XAF")
    with kpi_col4[2]: 
        taux_global_NV=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()-synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Montant à net recevoir des FOSA",montant_to_reciev-montant_to_pay, delta=0,color_scheme="orange", unit="XAF")

    st.write(" ")
  
    cc1=st.columns([4,2])
    with cc1[0]:
        # Construction d'un dataframe par District avec les 3 taux demandés
        districts = sorted(list(data_rejet["District"].dropna().unique()))
        if "District" in data_synthese.columns:
            synth_districts = list(data_synthese["District"].dropna().unique())
            for d in synth_districts:
                if d not in districts:
                    districts.append(d)

        rows = []
        for d in districts:
            # numérateurs
            rej_count = data_rejet[data_rejet["District"] == d].shape[0]
            valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Validé selon MC")].shape[0]
            non_valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Rejeté selon MC")].shape[0]

            # dénominateurs (par district si disponible sinon total)
            if "District" in data_synthese.columns:
                total_recu = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
            else:
                total_recu = data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()

            denom_nv = total_recu - total_valide_mc

            taux_rejet = (100 * rej_count / total_recu) if total_recu and total_recu > 0 else np.nan
            taux_V = (100 * valid_count / total_valide_mc) if total_valide_mc and total_valide_mc > 0 else np.nan
            taux_NV = (100 * non_valid_count / denom_nv) if denom_nv and denom_nv > 0 else np.nan

            rows.append({
                "District": d,
                "taux_global_rejet": round(taux_rejet, 2) if not pd.isna(taux_rejet) else np.nan,
                "taux_global_V": round(taux_V, 2) if not pd.isna(taux_V) else np.nan,
                "taux_global_NV": round(taux_NV, 2) if not pd.isna(taux_NV) else np.nan,
            })

        if rows:
            df_taux_par_district = pd.DataFrame(rows).sort_values("District").reset_index(drop=True)
        else:
            df_taux_par_district = pd.DataFrame([{
            "District": "Aucune donnée",
            "taux_global_rejet": 0.0,
            "taux_global_V": 0.0,
            "taux_global_NV": 0.0
            }])
        st.caption("Taux de rejet, Taux rejet factures valides et Taux réhabilitation facture non validé (en %) — survolez les barres pour voir les valeurs.")
        # Préparer les données (remplacer les NaN par 0 pour l'affichage)
        df_plot = df_taux_par_district.copy().fillna(0)
        labels = df_plot["District"].astype(str).tolist()
        rej = df_plot["taux_global_rejet"].tolist()
        val = df_plot["taux_global_V"].tolist()
        nonval = df_plot["taux_global_NV"].tolist()


        options = {
            "backgroundColor": "transparent",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b0}<br/>{a0}: {c0}%<br/>{a1}: {c1}%<br/>{a2}: {c2}%"
            },
            "legend": {
                "data": ["Taux rejet", "Taux rejet FV", "Taux  réhabilitation FNV"],
                "top": "6%",
                "textStyle": {"color": "#2c3e50"}
            },
            "grid": {"left": "6%", "right": "4%", "bottom": "8%", "containLabel": True},
            "xAxis": [
                {
                    "type": "category",
                    "data": labels,
                    "axisTick": {"alignWithLabel": True},
                    "axisLabel": {"rotate": 30, "interval": 0, "color": "#34495e"},
                    "axisLine": {"lineStyle": {"color": "#ecf0f1"}}
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "name": "%",
                    "min": 0,
                    "max": np.max([np.max(rej), np.max(val), np.max(nonval)])+5,
                    "axisLabel": {"formatter": "{value} %", "color": "#34495e"},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#ecf0f1"}}
                }
            ],
            "color": [
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#f73c42"}, {"offset": 1, "color": "#fad0c4"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#5512f1"}, {"offset": 1, "color": "#fbc2eb"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#16dbe9"}, {"offset": 1, "color": "#66a6ff"}]}
            ],
            "series": [
                {
                    "name": "Taux rejet",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": rej,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux rejet FV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": val,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux  réhabilitation FNV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": nonval,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                }
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "Enregistrer"},
                    "dataView": {"title": "Données", "readOnly": True}
                },
                "right": 10
            }
        }

        st_echarts(options=options, height="520px", key="tajhu")
    
    with cc1[1]:
        nb_fosa_to_audit=echantillon.shape[0]
        fosa_edited=len(data_initial["FOSA"].unique())
        taux_global_rejet=(round(100*data_rejet.shape[0]/data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum(),2))
        display_single_metric_advanced("Taux global de rejet",taux_global_rejet, delta=0, color_scheme="green", unit="%")
        st.write(" ")
        taux_global_V=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Validé selon MC"].shape[0])/data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum(),2))
        display_single_metric_advanced("Taux rejet factures valides",taux_global_V, delta=0,color_scheme="red", unit="%")

        st.write(" ")
        taux_global_NV=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()-data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Taux réhabilitation facture NV",taux_global_NV, delta=0,color_scheme="orange", unit="%")

    #============================================================================================================
    

#==============ONGLET PLAFONNEE SONUB ===================
with tab_[2]:
    data_rejet=st.session_state.df_rejet
    data_synthese=st.session_state.df_synthese
    cf2=st.columns(2)
    with cf2[0]:
        fosa4=st.multiselect("Choisir le statut de la FOSA", options=["SONUB","SONUC"], default=["SONUB","SONUC"],key="fosa4")
    with cf2[1]:
        region4=st.multiselect("Choisir la (les) régions(s)", options=data_rejet["Région"].unique(), default=data_rejet["Région"].unique(), key="region4")
    
    data_rejet=data_rejet[data_rejet["Catégorie"]=="Plafonnées SONUB"]
    data_synthese=data_synthese[data_synthese["Type de prestation"]=="Plafonnées SONUB"]
    
    
    data_rejet=data_rejet[data_rejet["Région"].isin(region4)] if len(region4)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Statut FOSA"].isin(fosa4)] if len(fosa4)!=0 else data_rejet
    
    montant=data_rejet.groupby("statut du chèque").agg({"Montant rejeté par le CM":"sum"}).reset_index()
    
    
    # Tableau croisé : somme du "Montant rejeté par le CM" par "Catégorie" et "statut du chèque"
    montant_cat_statut = pd.pivot_table(
        data_rejet,
        index="Catégorie",
        columns="statut du chèque",
        values="Montant rejeté par le CM",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Convertir les colonnes de montants en Int64 pour garder les NaN si besoin
    for col in montant_cat_statut.columns[1:]:
        montant_cat_statut[col] = montant_cat_statut[col].astype("Int64")

    # Exposer le dataframe pour réutilisation éventuelle
    # S'assurer que les colonnes attendues existent; les créer avec 0 si elles manquent
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        if _col not in montant_cat_statut.columns:
            montant_cat_statut[_col] = 0
    # Convertir en numérique et remplacer NaN par 0, garder le type Int64
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        montant_cat_statut[_col] = pd.to_numeric(montant_cat_statut[_col], errors="coerce").fillna(0).astype("Int64")

    montant_cat_statut["Ordre de recette des FOSA"] = montant_cat_statut["Rejet TOTAL selon le CM"] + montant_cat_statut["Rejet PARTIEL selon le CM"]
    montant_cat_statut["A verser par l'Etat"]=montant_cat_statut["Validé BON A PAYER selon le CM"]  
    
    df_montant_cat_statut=montant_cat_statut[["Catégorie","Ordre de recette des FOSA", "A verser par l'Etat"]]
    st.caption("Analyse sur les montants")
    kpi_col3=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col3[0]:
        montant_associe = montant.loc[montant["statut du chèque"].isin(["Rejet TOTAL selon le CM","Rejet PARTIEL selon le CM"]) , "Montant rejeté par le CM"].sum()
        montant_to_reciev = int(montant_associe) if not pd.isna(montant_associe) else 0
        display_single_metric_advanced("Ordre de recette des FOSA",montant_to_reciev, delta=0, color_scheme="green", unit="XAF")
    
    with kpi_col3[1]:
        montant_associe2 = montant.loc[montant["statut du chèque"]=="Validé BON A PAYER selon le CM" , "Montant rejeté par le CM"].sum()
        montant_to_pay = int(montant_associe2) if not pd.isna(montant_associe2) else 0
        display_single_metric_advanced("Montant à reverser par l'Etat au FOSA",montant_to_pay, delta=0,color_scheme="red", unit="XAF")
    with kpi_col3[2]: 
        taux_global_NV=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()-synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Montant à net recevoir des FOSA",montant_to_reciev-montant_to_pay, delta=0,color_scheme="orange", unit="XAF")

    st.write(" ")
  
    cc2=st.columns([4,2])
    with cc2[0]:
        # Construction d'un dataframe par District avec les 3 taux demandés
        districts = sorted(list(data_rejet["District"].dropna().unique()))
        if "District" in data_synthese.columns:
            synth_districts = list(data_synthese["District"].dropna().unique())
            for d in synth_districts:
                if d not in districts:
                    districts.append(d)

        rows = []
        for d in districts:
            # numérateurs
            rej_count = data_rejet[data_rejet["District"] == d].shape[0]
            valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Validé selon MC")].shape[0]
            non_valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Rejeté selon MC")].shape[0]

            # dénominateurs (par district si disponible sinon total)
            if "District" in data_synthese.columns:
                total_recu = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
            else:
                total_recu = data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()

            denom_nv = total_recu - total_valide_mc

            taux_rejet = (100 * rej_count / total_recu) if total_recu and total_recu > 0 else np.nan
            taux_V = (100 * valid_count / total_valide_mc) if total_valide_mc and total_valide_mc > 0 else np.nan
            taux_NV = (100 * non_valid_count / denom_nv) if denom_nv and denom_nv > 0 else np.nan

            rows.append({
                "District": d,
                "taux_global_rejet": round(taux_rejet, 2) if not pd.isna(taux_rejet) else np.nan,
                "taux_global_V": round(taux_V, 2) if not pd.isna(taux_V) else np.nan,
                "taux_global_NV": round(taux_NV, 2) if not pd.isna(taux_NV) else np.nan,
            })

        
        # si 'rows' est vide, créer un dataframe par défaut pour éviter les erreurs en aval
        if rows:
            df_taux_par_district = pd.DataFrame(rows).sort_values("District").reset_index(drop=True)
        else:
            df_taux_par_district = pd.DataFrame([{
            "District": "Aucune donnée",
            "taux_global_rejet": 0.0,
            "taux_global_V": 0.0,
            "taux_global_NV": 0.0
            }])
        st.caption("Taux de rejet, Taux rejet factures valides et Taux réhabilitation facture non validé (en %) — survolez les barres pour voir les valeurs.")
        # Préparer les données (remplacer les NaN par 0 pour l'affichage)
        df_plot = df_taux_par_district.copy().fillna(0)
        labels = df_plot["District"].astype(str).tolist()
        rej = df_plot["taux_global_rejet"].tolist()
        val = df_plot["taux_global_V"].tolist()
        nonval = df_plot["taux_global_NV"].tolist()


        options = {
            "backgroundColor": "transparent",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b0}<br/>{a0}: {c0}%<br/>{a1}: {c1}%<br/>{a2}: {c2}%"
            },
            "legend": {
                "data": ["Taux rejet", "Taux rejet FV", "Taux  réhabilitation FNV"],
                "top": "6%",
                "textStyle": {"color": "#2c3e50"}
            },
            "grid": {"left": "6%", "right": "4%", "bottom": "8%", "containLabel": True},
            "xAxis": [
                {
                    "type": "category",
                    "data": labels,
                    "axisTick": {"alignWithLabel": True},
                    "axisLabel": {"rotate": 30, "interval": 0, "color": "#34495e"},
                    "axisLine": {"lineStyle": {"color": "#ecf0f1"}}
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "name": "%",
                    "min": 0,
                    "max": np.max([np.max(rej), np.max(val), np.max(nonval)])+5,
                    "axisLabel": {"formatter": "{value} %", "color": "#34495e"},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#ecf0f1"}}
                }
            ],
            "color": [
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#f73c42"}, {"offset": 1, "color": "#fad0c4"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#5512f1"}, {"offset": 1, "color": "#fbc2eb"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#16dbe9"}, {"offset": 1, "color": "#66a6ff"}]}
            ],
            "series": [
                {
                    "name": "Taux rejet",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": rej,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux rejet FV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": val,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux  réhabilitation FNV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": nonval,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                }
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "Enregistrer"},
                    "dataView": {"title": "Données", "readOnly": True}
                },
                "right": 10
            }
        }

        st_echarts(options=options, height="520px", key="tajnjipghhu")
    
    with cc2[1]:
        nb_fosa_to_audit=echantillon.shape[0]
        fosa_edited=len(data_initial["FOSA"].unique())
        taux_global_rejet=(round(100*data_rejet.shape[0]/data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum(),2))
        display_single_metric_advanced("Taux global de rejet",taux_global_rejet, delta=0, color_scheme="green", unit="%")
        st.write(" ")
        taux_global_V=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Validé selon MC"].shape[0])/data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum(),2))
        display_single_metric_advanced("Taux rejet factures valides",taux_global_V, delta=0,color_scheme="red", unit="%")

        st.write(" ")
        taux_global_NV=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()-data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Taux réhabilitation facture NV",taux_global_NV, delta=0,color_scheme="orange", unit="%")

    #============================================================================================================
    


#==============ONGLET PLAFONNEE SONUC ===================
with tab_[3]:
    data_rejet=st.session_state.df_rejet
    data_synthese=st.session_state.df_synthese
    cf3=st.columns(2)
    with cf3[0]:
        fosa6=st.multiselect("Choisir le statut de la FOSA", options=["SONUB","SONUC"], default=["SONUB","SONUC"],key="fosa6")
    with cf3[1]:
        region6=st.multiselect("Choisir la (les) régions(s)", options=data_rejet["Région"].unique(), default=data_rejet["Région"].unique(), key="region6")
    
    data_rejet=data_rejet[data_rejet["Catégorie"]=="Plafonnées SONUC"]
    data_synthese=data_synthese[data_synthese["Type de prestation"]=="Plafonnées SONUC"]
    
    data_rejet=data_rejet[data_rejet["Région"].isin(region6)] if len(region6)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Statut FOSA"].isin(fosa6)] if len(fosa6)!=0 else data_rejet
    
    montant=data_rejet.groupby("statut du chèque").agg({"Montant rejeté par le CM":"sum"}).reset_index()
    
    
    # Tableau croisé : somme du "Montant rejeté par le CM" par "Catégorie" et "statut du chèque"
    montant_cat_statut = pd.pivot_table(
        data_rejet,
        index="Catégorie",
        columns="statut du chèque",
        values="Montant rejeté par le CM",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Convertir les colonnes de montants en Int64 pour garder les NaN si besoin
    for col in montant_cat_statut.columns[1:]:
        montant_cat_statut[col] = montant_cat_statut[col].astype("Int64")

    # Exposer le dataframe pour réutilisation éventuelle
    # S'assurer que les colonnes attendues existent; les créer avec 0 si elles manquent
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        if _col not in montant_cat_statut.columns:
            montant_cat_statut[_col] = 0
    # Convertir en numérique et remplacer NaN par 0, garder le type Int64
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        montant_cat_statut[_col] = pd.to_numeric(montant_cat_statut[_col], errors="coerce").fillna(0).astype("Int64")

    montant_cat_statut["Ordre de recette des FOSA"] = montant_cat_statut["Rejet TOTAL selon le CM"] + montant_cat_statut["Rejet PARTIEL selon le CM"]
    montant_cat_statut["A verser par l'Etat"]=montant_cat_statut["Validé BON A PAYER selon le CM"]  
    
    df_montant_cat_statut=montant_cat_statut[["Catégorie","Ordre de recette des FOSA", "A verser par l'Etat"]]
    st.caption("Analyse sur les montants")
    kpi_col3=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col3[0]:
        montant_associe = montant.loc[montant["statut du chèque"].isin(["Rejet TOTAL selon le CM","Rejet PARTIEL selon le CM"]) , "Montant rejeté par le CM"].sum()
        montant_to_reciev = int(montant_associe) if not pd.isna(montant_associe) else 0
        display_single_metric_advanced("Ordre de recette des FOSA",montant_to_reciev, delta=0, color_scheme="green", unit="XAF")
    
    with kpi_col3[1]:
        montant_associe2 = montant.loc[montant["statut du chèque"]=="Validé BON A PAYER selon le CM" , "Montant rejeté par le CM"].sum()
        montant_to_pay = int(montant_associe2) if not pd.isna(montant_associe2) else 0
        display_single_metric_advanced("Montant à reverser par l'Etat au FOSA",montant_to_pay, delta=0,color_scheme="red", unit="XAF")
    with kpi_col3[2]: 
        taux_global_NV=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()-synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Montant à net recevoir des FOSA",montant_to_reciev-montant_to_pay, delta=0,color_scheme="orange", unit="XAF")

    st.write(" ")
  
    cc3=st.columns([4,2])
    with cc3[0]:
        # Construction d'un dataframe par District avec les 3 taux demandés
        districts = sorted(list(data_rejet["District"].dropna().unique()))
        if "District" in data_synthese.columns:
            synth_districts = list(data_synthese["District"].dropna().unique())
            for d in synth_districts:
                if d not in districts:
                    districts.append(d)

        rows = []
        for d in districts:
            # numérateurs
            rej_count = data_rejet[data_rejet["District"] == d].shape[0]
            valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Validé selon MC")].shape[0]
            non_valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Rejeté selon MC")].shape[0]

            # dénominateurs (par district si disponible sinon total)
            if "District" in data_synthese.columns:
                total_recu = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
            else:
                total_recu = data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()

            denom_nv = total_recu - total_valide_mc

            taux_rejet = (100 * rej_count / total_recu) if total_recu and total_recu > 0 else np.nan
            taux_V = (100 * valid_count / total_valide_mc) if total_valide_mc and total_valide_mc > 0 else np.nan
            taux_NV = (100 * non_valid_count / denom_nv) if denom_nv and denom_nv > 0 else np.nan

            rows.append({
                "District": d,
                "taux_global_rejet": round(taux_rejet, 2) if not pd.isna(taux_rejet) else np.nan,
                "taux_global_V": round(taux_V, 2) if not pd.isna(taux_V) else np.nan,
                "taux_global_NV": round(taux_NV, 2) if not pd.isna(taux_NV) else np.nan,
            })

        if rows:
            df_taux_par_district = pd.DataFrame(rows).sort_values("District").reset_index(drop=True)
        else:
            df_taux_par_district = pd.DataFrame([{
            "District": "Aucune donnée",
            "taux_global_rejet": 0.0,
            "taux_global_V": 0.0,
            "taux_global_NV": 0.0
            }])
        st.caption("Taux de rejet, Taux rejet factures valides et Taux réhabilitation facture non validé (en %) — survolez les barres pour voir les valeurs.")
        # Préparer les données (remplacer les NaN par 0 pour l'affichage)
        df_plot = df_taux_par_district.copy().fillna(0)
        labels = df_plot["District"].astype(str).tolist()
        rej = df_plot["taux_global_rejet"].tolist()
        val = df_plot["taux_global_V"].tolist()
        nonval = df_plot["taux_global_NV"].tolist()


        options = {
            "backgroundColor": "transparent",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b0}<br/>{a0}: {c0}%<br/>{a1}: {c1}%<br/>{a2}: {c2}%"
            },
            "legend": {
                "data": ["Taux rejet", "Taux rejet FV", "Taux  réhabilitation FNV"],
                "top": "6%",
                "textStyle": {"color": "#2c3e50"}
            },
            "grid": {"left": "6%", "right": "4%", "bottom": "8%", "containLabel": True},
            "xAxis": [
                {
                    "type": "category",
                    "data": labels,
                    "axisTick": {"alignWithLabel": True},
                    "axisLabel": {"rotate": 30, "interval": 0, "color": "#34495e"},
                    "axisLine": {"lineStyle": {"color": "#ecf0f1"}}
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "name": "%",
                    "min": 0,
                    "max": np.max([np.max(rej), np.max(val), np.max(nonval)])+5,
                    "axisLabel": {"formatter": "{value} %", "color": "#34495e"},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#ecf0f1"}}
                }
            ],
            "color": [
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#f73c42"}, {"offset": 1, "color": "#fad0c4"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#5512f1"}, {"offset": 1, "color": "#fbc2eb"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#16dbe9"}, {"offset": 1, "color": "#66a6ff"}]}
            ],
            "series": [
                {
                    "name": "Taux rejet",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": rej,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux rejet FV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": val,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux  réhabilitation FNV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": nonval,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                }
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "Enregistrer"},
                    "dataView": {"title": "Données", "readOnly": True}
                },
                "right": 10
            }
        }

        st_echarts(options=options, height="520px", key="tajbvfrn5hu")
    
    with cc3[1]:
        nb_fosa_to_audit=echantillon.shape[0]
        fosa_edited=len(data_initial["FOSA"].unique())
        taux_global_rejet=(round(100*data_rejet.shape[0]/data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum(),2))
        display_single_metric_advanced("Taux global de rejet",taux_global_rejet, delta=0, color_scheme="green", unit="%")
        st.write(" ")
        taux_global_V=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Validé selon MC"].shape[0])/data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum(),2))
        display_single_metric_advanced("Taux rejet factures valides",taux_global_V, delta=0,color_scheme="red", unit="%")

        st.write(" ")
        taux_global_NV=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()-data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Taux réhabilitation facture NV",taux_global_NV, delta=0,color_scheme="orange", unit="%")

    #============================================================================================================
    

#==============ONGLET NON MEDICALE ===================
with tab_[4]:
    data_rejet=st.session_state.df_rejet
    data_synthese=st.session_state.df_synthese
    cf8=st.columns(2)
    with cf8[0]:
        fosa7=st.multiselect("Choisir le statut de la FOSA", options=["SONUB","SONUC"], default=["SONUB","SONUC"],key="fosa7")
    with cf8[1]:
        region7=st.multiselect("Choisir la (les) régions(s)", options=data_rejet["Région"].unique(), default=data_rejet["Région"].unique(), key="region7")
    
    
    data_rejet=data_rejet[data_rejet["Catégorie"]=="Non médicales"]
    data_synthese=data_synthese[data_synthese["Type de prestation"]=="Non médicales"]
    
    data_rejet=data_rejet[data_rejet["Région"].isin(region7)] if len(region7)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Statut FOSA"].isin(fosa7)] if len(fosa7)!=0 else data_rejet
    
    montant=data_rejet.groupby("statut du chèque").agg({"Montant rejeté par le CM":"sum"}).reset_index()
    
    
    # Tableau croisé : somme du "Montant rejeté par le CM" par "Catégorie" et "statut du chèque"
    montant_cat_statut = pd.pivot_table(
        data_rejet,
        index="Catégorie",
        columns="statut du chèque",
        values="Montant rejeté par le CM",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Convertir les colonnes de montants en Int64 pour garder les NaN si besoin
    for col in montant_cat_statut.columns[1:]:
        montant_cat_statut[col] = montant_cat_statut[col].astype("Int64")

    # Exposer le dataframe pour réutilisation éventuelle
    # S'assurer que les colonnes attendues existent; les créer avec 0 si elles manquent
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        if _col not in montant_cat_statut.columns:
            montant_cat_statut[_col] = 0
    # Convertir en numérique et remplacer NaN par 0, garder le type Int64
    for _col in ["Rejet TOTAL selon le CM", "Rejet PARTIEL selon le CM", "Validé BON A PAYER selon le CM"]:
        montant_cat_statut[_col] = pd.to_numeric(montant_cat_statut[_col], errors="coerce").fillna(0).astype("Int64")

    montant_cat_statut["Ordre de recette des FOSA"] = montant_cat_statut["Rejet TOTAL selon le CM"] + montant_cat_statut["Rejet PARTIEL selon le CM"]
    montant_cat_statut["A verser par l'Etat"]=montant_cat_statut["Validé BON A PAYER selon le CM"]  
    
    df_montant_cat_statut=montant_cat_statut[["Catégorie","Ordre de recette des FOSA", "A verser par l'Etat"]]
    st.caption("Analyse sur les montants")
    kpi_col3=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col3[0]:
        montant_associe = montant.loc[montant["statut du chèque"].isin(["Rejet TOTAL selon le CM","Rejet PARTIEL selon le CM"]) , "Montant rejeté par le CM"].sum()
        montant_to_reciev = int(montant_associe) if not pd.isna(montant_associe) else 0
        display_single_metric_advanced("Ordre de recette des FOSA",montant_to_reciev, delta=0, color_scheme="green", unit="XAF")
    
    with kpi_col3[1]:
        montant_associe2 = montant.loc[montant["statut du chèque"]=="Validé BON A PAYER selon le CM" , "Montant rejeté par le CM"].sum()
        montant_to_pay = int(montant_associe2) if not pd.isna(montant_associe2) else 0
        display_single_metric_advanced("Montant à reverser par l'Etat au FOSA",montant_to_pay, delta=0,color_scheme="red", unit="XAF")
    with kpi_col3[2]: 
        taux_global_NV=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()-synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Montant à net recevoir des FOSA",montant_to_reciev-montant_to_pay, delta=0,color_scheme="orange", unit="XAF")

    st.write(" ")
  
    cc=st.columns([4,2])
    with cc[0]:
        # Construction d'un dataframe par District avec les 3 taux demandés
        districts = sorted(list(data_rejet["District"].dropna().unique()))
        if "District" in data_synthese.columns:
            synth_districts = list(data_synthese["District"].dropna().unique())
            for d in synth_districts:
                if d not in districts:
                    districts.append(d)

        rows = []
        for d in districts:
            # numérateurs
            rej_count = data_rejet[data_rejet["District"] == d].shape[0]
            valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Validé selon MC")].shape[0]
            non_valid_count = data_rejet[(data_rejet["District"] == d) & (data_rejet["Statut initial chèque"] == "Rejeté selon MC")].shape[0]

            # dénominateurs (par district si disponible sinon total)
            if "District" in data_synthese.columns:
                total_recu = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese[data_synthese["District"] == d]["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
            else:
                total_recu = data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()
                total_valide_mc = data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()

            denom_nv = total_recu - total_valide_mc

            taux_rejet = (100 * rej_count / total_recu) if total_recu and total_recu > 0 else np.nan
            taux_V = (100 * valid_count / total_valide_mc) if total_valide_mc and total_valide_mc > 0 else np.nan
            taux_NV = (100 * non_valid_count / denom_nv) if denom_nv and denom_nv > 0 else np.nan

            rows.append({
                "District": d,
                "taux_global_rejet": round(taux_rejet, 2) if not pd.isna(taux_rejet) else np.nan,
                "taux_global_V": round(taux_V, 2) if not pd.isna(taux_V) else np.nan,
                "taux_global_NV": round(taux_NV, 2) if not pd.isna(taux_NV) else np.nan,
            })

        if rows:
            df_taux_par_district = pd.DataFrame(rows).sort_values("District").reset_index(drop=True)
        else:
            df_taux_par_district = pd.DataFrame([{
            "District": "Aucune donnée",
            "taux_global_rejet": 0.0,
            "taux_global_V": 0.0,
            "taux_global_NV": 0.0
            }])
        st.caption("Taux de rejet, Taux rejet factures valides et Taux réhabilitation facture non validé (en %) — survolez les barres pour voir les valeurs.")
        # Préparer les données (remplacer les NaN par 0 pour l'affichage)
        df_plot = df_taux_par_district.copy().fillna(0)
        labels = df_plot["District"].astype(str).tolist()
        rej = df_plot["taux_global_rejet"].tolist()
        val = df_plot["taux_global_V"].tolist()
        nonval = df_plot["taux_global_NV"].tolist()


        options = {
            "backgroundColor": "transparent",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b0}<br/>{a0}: {c0}%<br/>{a1}: {c1}%<br/>{a2}: {c2}%"
            },
            "legend": {
                "data": ["Taux rejet", "Taux rejet FV", "Taux  réhabilitation FNV"],
                "top": "6%",
                "textStyle": {"color": "#2c3e50"}
            },
            "grid": {"left": "6%", "right": "4%", "bottom": "8%", "containLabel": True},
            "xAxis": [
                {
                    "type": "category",
                    "data": labels,
                    "axisTick": {"alignWithLabel": True},
                    "axisLabel": {"rotate": 30, "interval": 0, "color": "#34495e"},
                    "axisLine": {"lineStyle": {"color": "#ecf0f1"}}
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "name": "%",
                    "min": 0,
                    "max": np.max([np.max(rej), np.max(val), np.max(nonval)])+5,
                    "axisLabel": {"formatter": "{value} %", "color": "#34495e"},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#ecf0f1"}}
                }
            ],
            "color": [
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#f73c42"}, {"offset": 1, "color": "#fad0c4"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#5512f1"}, {"offset": 1, "color": "#fbc2eb"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#16dbe9"}, {"offset": 1, "color": "#66a6ff"}]}
            ],
            "series": [
                {
                    "name": "Taux rejet",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": rej,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux rejet FV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": val,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux  réhabilitation FNV",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": nonval,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                }
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "Enregistrer"},
                    "dataView": {"title": "Données", "readOnly": True}
                },
                "right": 10
            }
        }

        st_echarts(options=options, height="520px", key="tajvgt2hu")
    
    with cc[1]:
        nb_fosa_to_audit=echantillon.shape[0]
        fosa_edited=len(data_initial["FOSA"].unique())
        taux_global_rejet=(round(100*data_rejet.shape[0]/data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum(),2))
        display_single_metric_advanced("Taux global de rejet",taux_global_rejet, delta=0, color_scheme="green", unit="%")
        st.write(" ")
        taux_global_V=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Validé selon MC"].shape[0])/data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum(),2))
        display_single_metric_advanced("Taux rejet factures valides",taux_global_V, delta=0,color_scheme="red", unit="%")

        st.write(" ")
        taux_global_NV=(round(100*(data_rejet[data_rejet["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(data_synthese["NOMBRE TOTAL DE FACTURE RECU"].sum()-data_synthese["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Taux réhabilitation facture NV",taux_global_NV, delta=0,color_scheme="orange", unit="%")

    #============================================================================================================
    


#==============ONGLET DASHBOARD ===================
with tab_[5]:

    data_rejet=st.session_state.df_rejet
    data_synthese=st.session_state.df_synthese
    kpi_col=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col[0]:
        display_single_metric_advanced("Nombre FOSA à auditer",nb_fosa_to_audit, delta=0, color_scheme="green")
        
    with kpi_col[1]:
        display_single_metric_advanced("Nombre de FOSA audité",fosa_edited, delta=0,color_scheme="red")

    with kpi_col[2]: 
        display_single_metric_advanced("Taux de réalisation",round(100*fosa_edited/nb_fosa_to_audit,2), delta=0,color_scheme="orange", unit="%")

    st.write("")
    
    fosa_int_par_district=echantillon.groupby("District").agg({"FOSA":"count"}).rename(columns={"FOSA":"FOSA à auditer"})
    fosa_int_par_district = fosa_int_par_district.reset_index()
    
    fosa_par_district_audit=initial_to_use.drop_duplicates(subset=["FOSA"]).groupby("District").agg({"FOSA":"count"}).rename(columns={"FOSA":"FOSA audité"})
    fosa_par_district_audit=fosa_par_district_audit.reset_index()
    
    tab_fosa_district=fosa_par_district_audit.merge(fosa_int_par_district,on="District", how="left" )
    # remettre "District" en index et remplacer les éventuels NaN par 0
    tab_fosa_district = tab_fosa_district.set_index("District")
    tab_fosa_district[["FOSA à auditer", "FOSA audité"]] = tab_fosa_district[["FOSA à auditer", "FOSA audité"]].fillna(0).astype(int)
    
    col_= st.columns(2)

    with col_[0]:
        pass
        create_bar_chart_from_contingency(tab_fosa_district, var1_name="District", title="FOSA à auditer vs FOSA audité par district", height="400px" )
        #create_crossed_bar_chart(good_data,var1="Region",var2="Statut_cheque",title="Répartition des chèques par région",height="350px" ) 

    with col_[1]:
        taux_realisation_district=tab_fosa_district.copy()
        taux_realisation_district["Taux de réalisation"] = (taux_realisation_district["FOSA audité"] / taux_realisation_district["FOSA à auditer"]).round(2)
        # créer une liste de couleurs de la même taille que les données
        n = len(taux_realisation_district)
        palette = px.colors.qualitative.Plotly  # palette de base
        colors = [palette[i % len(palette)] for i in range(n)]
        
        make_multi_progress_bar_echart( labels=taux_realisation_district.index, values=taux_realisation_district["Taux de réalisation"],
            titre="Taux de réalisation par district",
            colors=colors,
            height="400px",
            width="100%",
        )
    
        #create_pie_chart_from_df(data_facture,column="Statut de Facture selon le Médecin Conseil", colors=["green","red"],height="300px", title="Proportion",cle="sjfhbjhc")
    col_f=st.columns([1,1,2])
    with col_f[0]:
        district=st.multiselect("Sélectionnez le(s) district(s)", options=rejet_to_use["District"].unique(), default=rejet_to_use["District"].unique())
        rejet_district_choosed=rejet_to_use[rejet_to_use["District"].isin(district)] if len(district)!=0 else rejet_to_use
    with col_f[1]:
        cat=st.multiselect("Catégorie de prestation ", options=rejet_district_choosed["Catégorie"].unique(), default=rejet_district_choosed["Catégorie"].unique())
        rejet_district_choosed=rejet_to_use[rejet_to_use["Catégorie"].isin(cat)] if len(cat)!=0 else rejet_district_choosed
    with col_f[2]:
        type_pres=st.multiselect("Type de prestation ", options=rejet_district_choosed["Type de prestation"].unique(), default=rejet_district_choosed["Type de prestation"].unique())
        rejet_district_choosed=rejet_to_use[rejet_to_use["Type de prestation"].isin(type_pres)] if len(type_pres)!=0 else rejet_district_choosed
    
    
    
    
    df_coherence=pd.crosstab(rejet_district_choosed["Statut initial chèque"], rejet_district_choosed["statut du chèque"])
    df_coherence["Total"]=df_coherence.sum(axis=1)
    col_1=st.columns([1,2])
    with col_1[0]:
        create_pie_chart_from_df(rejet_district_choosed,column="Statut initial chèque", title="Statut initial des chèques", height="200px")
        create_pie_chart_from_df(rejet_district_choosed,column="statut du chèque", title="Statut audité des chèques", height="200px", cle="khl")
        
        #create_bar_chart_from_contingency(df_coherence, var1_name="Statut initial chèque", title="Coherence entre statut initial et statut final du chèque", cle="jhbkl")
        
            
            
    with col_1[1]:
        display_confusion_from_crosstab(df_coherence,y_title="Statut initial",x_title="Satut audité", keys="jkbcnksdnkjs",title="Satatut des chèques avant et après audition", height="450px")
    # Troisième ligne avec Top 5 clients et Revenus par commerciaux
    
    kpi_col2=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    nb_fosa_to_audit=echantillon.shape[0]
    fosa_edited=len(initial_to_use["FOSA"].unique())
    
    with kpi_col2[0]:
        taux_global_rejet=(round(100*rejet_to_use.shape[0]/synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum(),2))
        display_single_metric_advanced("Taux global de rejet",taux_global_rejet, delta=0, color_scheme="green", unit="%")
        
    with kpi_col2[1]:
        taux_global_V=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Validé selon MC"].shape[0])/synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum(),2))
        display_single_metric_advanced("Taux rejet factures valides",taux_global_V, delta=0,color_scheme="red", unit="%")

    with kpi_col2[2]: 
        taux_global_NV=(round(100*(rejet_to_use[rejet_to_use["Statut initial chèque"]=="Rejeté selon MC"].shape[0])/(synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()-synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()),2))
        display_single_metric_advanced("Taux réhabilitation facture NV",taux_global_NV, delta=0,color_scheme="orange", unit="%")

    # Construction d'un dataframe par District avec les 3 taux demandés
    districts = sorted(list(rejet_to_use["District"].dropna().unique()))
    if "District" in synthese_to_use.columns:
        synth_districts = list(synthese_to_use["District"].dropna().unique())
        for d in synth_districts:
            if d not in districts:
                districts.append(d)

    rows = []
    for d in districts:
        # numérateurs
        rej_count = rejet_to_use[rejet_to_use["District"] == d].shape[0]
        valid_count = rejet_to_use[(rejet_to_use["District"] == d) & (rejet_to_use["Statut initial chèque"] == "Validé selon MC")].shape[0]
        non_valid_count = rejet_to_use[(rejet_to_use["District"] == d) & (rejet_to_use["Statut initial chèque"] == "Rejeté selon MC")].shape[0]

        # dénominateurs (par district si disponible sinon total)
        if "District" in synthese_to_use.columns:
            total_recu = synthese_to_use[synthese_to_use["District"] == d]["NOMBRE TOTAL DE FACTURE RECU"].sum()
            total_valide_mc = synthese_to_use[synthese_to_use["District"] == d]["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()
        else:
            total_recu = synthese_to_use["NOMBRE TOTAL DE FACTURE RECU"].sum()
            total_valide_mc = synthese_to_use["NOMBRE TOTAL DE FACTURE VALIDE MC"].sum()

        denom_nv = total_recu - total_valide_mc

        taux_rejet = (100 * rej_count / total_recu) if total_recu and total_recu > 0 else np.nan
        taux_V = (100 * valid_count / total_valide_mc) if total_valide_mc and total_valide_mc > 0 else np.nan
        taux_NV = (100 * non_valid_count / denom_nv) if denom_nv and denom_nv > 0 else np.nan

        rows.append({
            "District": d,
            "taux_global_rejet": round(taux_rejet, 2) if not pd.isna(taux_rejet) else np.nan,
            "taux_global_V": round(taux_V, 2) if not pd.isna(taux_V) else np.nan,
            "taux_global_NV": round(taux_NV, 2) if not pd.isna(taux_NV) else np.nan,
        })

    df_taux_par_district = pd.DataFrame(rows).sort_values("District").reset_index(drop=True)
    st.caption("Taux de rejet, taux validé et taux non validé par district (en %) — survolez les barres pour voir les valeurs.")
    col_tx=st.columns([3,1])
     
    with col_tx[0]:
        # Préparer les données (remplacer les NaN par 0 pour l'affichage)
        df_plot = df_taux_par_district.copy().fillna(0)
        labels = df_plot["District"].astype(str).tolist()
        rej = df_plot["taux_global_rejet"].tolist()
        val = df_plot["taux_global_V"].tolist()
        nonval = df_plot["taux_global_NV"].tolist()


        options = {
            "backgroundColor": "transparent",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": "{b0}<br/>{a0}: {c0}%<br/>{a1}: {c1}%<br/>{a2}: {c2}%"
            },
            "legend": {
                "data": ["Taux rejet", "Taux validé", "Taux non validé"],
                "top": "6%",
                "textStyle": {"color": "#2c3e50"}
            },
            "grid": {"left": "6%", "right": "4%", "bottom": "8%", "containLabel": True},
            "xAxis": [
                {
                    "type": "category",
                    "data": labels,
                    "axisTick": {"alignWithLabel": True},
                    "axisLabel": {"rotate": 30, "interval": 0, "color": "#34495e"},
                    "axisLine": {"lineStyle": {"color": "#ecf0f1"}}
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "name": "%",
                    "min": 0,
                    "max": np.max([np.max(rej), np.max(val), np.max(nonval)])+5,
                    "axisLabel": {"formatter": "{value} %", "color": "#34495e"},
                    "splitLine": {"lineStyle": {"type": "dashed", "color": "#ecf0f1"}}
                }
            ],
            "color": [
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#f73c42"}, {"offset": 1, "color": "#fad0c4"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#5512f1"}, {"offset": 1, "color": "#fbc2eb"}]},
                {"type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [{"offset": 0, "color": "#16dbe9"}, {"offset": 1, "color": "#66a6ff"}]}
            ],
            "series": [
                {
                    "name": "Taux rejet",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": rej,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux validé",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": val,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                },
                {
                    "name": "Taux non validé",
                    "type": "bar",
                    "barWidth": "28%",
                    "data": nonval,
                    "itemStyle": {"borderRadius": [6, 6, 0, 0]},
                    "label": {"show": True, "position": "top", "formatter": "{c}%"}
                }
            ],
            "toolbox": {
                "feature": {
                    "saveAsImage": {"title": "Enregistrer"},
                    "dataView": {"title": "Données", "readOnly": True}
                },
                "right": 10
            }
        }

        st_echarts(options=options, height="520px", key="taux_par_district_chart")
    
    with col_tx[1]:
        st.dataframe(df_taux_par_district)
        st.write("")
       
    st.markdown("## Tableaux des données")

    fosa_tab=st.multiselect("Choisisez une FOSA", options=data_initial["FOSA"].unique(), default=data_initial["FOSA"].unique())
    district_tab=st.multiselect("Choisisez un district", options=data_initial["District"].unique(), default=data_initial["District"].unique())
    prestation_tab=st.multiselect("Choisisez un type de prestation", options=data_synthese["Type de prestation"].unique(), default=data_synthese["Type de prestation"].unique())
    mois_tab=st.multiselect("Choisisez un mois", options=data_rejet["Mois"].unique(), default=data_rejet["Mois"].unique())
    
    data_rejet=data_rejet[data_rejet["FOSA"].isin(fosa_tab)] if len(fosa_tab)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["District"].isin(district_tab)] if len(district_tab)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Catégorie"].isin(prestation_tab)] if len(prestation_tab)!=0 else data_rejet
    data_rejet=data_rejet[data_rejet["Mois"].isin(mois_tab)] if len(mois_tab)!=0 else data_rejet
    
    data_synthese=data_synthese[data_synthese["FOSA"].isin(fosa_tab)] if len(fosa_tab)!=0 else data_synthese
    data_synthese=data_synthese[data_synthese["District"].isin(district_tab)] if len(district_tab)!=0 else data_synthese
    data_synthese=data_synthese[data_synthese["Type de prestation"].isin(prestation_tab)] if len(prestation_tab)!=0 else data_synthese
    data_synthese=data_synthese[data_synthese["Mois"].isin(mois_tab)] if len(mois_tab)!=0 else data_synthese
    
    data_initial=data_initial[data_initial["FOSA"].isin(fosa_tab)] if len(fosa_tab)!=0 else data_initial
    data_initial=data_initial[data_initial["District"].isin(district_tab)] if len(district_tab)!=0 else data_initial
    data_initial=data_initial[data_initial["Mois"].isin(mois_tab)] if len(mois_tab)!=0 else data_initial
    
    st.write("### Données sur les chèque rejetés et acceptés")
    st.dataframe(data_rejet)
    st.write("### Données de synthèse")
    st.dataframe(data_synthese)
    st.write("### FOSA auditées")
    st.dataframe(data_initial)

        
#++++++++++++++++++++ONGLET PERSONNEL++++++++++++++++++++++++
with tab_[6]:
    def main():
    #st.write("Autre approche: Au cas ou la première approche ne marche pas, inscrivez vous dans l'onglet connexion ci contre et utiliser vos identifiants pour vous connecter")
        is_authenticated = authentication_system("Enqueteur")
        if is_authenticated:
            user=st.session_state.username
            st.success(f"Bienvenue {user} ! Vous êtes connecté en tant qu'Enquêteur.", icon="✅")

    if __name__ == "__main__":
        main()

# Footer élégant
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <div style='display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <span style='font-size: 24px;'>📊</span>
                <span style='font-weight: 600; color: #2c3e50;'>Dashboard Analytics</span>
            </div>
            <span style='color: #bdc3c7;'>|</span>
            <div>
                <span style='color: #7f8c8d;'>Créé avec</span>
                <span style='color: #e74c3c; font-size: 16px;'>  </span>
                <span style='color: #7f8c8d;'>Streamlit</span>
            </div>
            <span style='color: #bdc3c7;'>|</span>
            <div style='color: #7f8c8d;'>
                © 2025 Tableau de Bord
            </div>
        </div>
        <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: center; gap: 20px; font-size: 15px; color: #95a5a6;'>
                <span>📧 landrykengne99@gmail.com</span>
                <span>📱 +237 6 98 28 05 37</span>
                <span>🌐 www.dashboard-analytics.fr</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

#afficher_heure()