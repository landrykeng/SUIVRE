import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from Authentification import *
from Fonction import *

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord collecte FOSA",
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
                <span style='font-size: 40px;'>FOSA</span>
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
    fosa = st.multiselect("Statut FOSA", data_rejet["Statut FOSA"].unique(),default=data_rejet["Statut FOSA"].unique())
    annee = st.multiselect("Année", data_rejet["annee"].unique(),default=data_rejet["annee"].unique())
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
st.markdown("# 📊 Tableau de bord de l'enquête- FOSA 2025")

#afficher_toutes_les_10_secondes()


#st.success(f"Dernière mise à jour effectuée avec succès à {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")
#st.session_state.last_update=datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
update=st.button("Mettre à jour le tableau de bord")
if update:
    upgrade_data()
    
st.info("Si vous êtes sur PC, ajuster le zoom de votre navigateur à 80% pour une meilleure expérience visuelle. (ctrl + -)", icon="ℹ️")
tab_=st.tabs(["**Données**","**Dashboard**", "**Personnel**"])


#==============ONGLET DONNEES==========================
with tab_[0]:   
    st.write("### Données sur les chèque rejetés et acceptés")
    st.dataframe(data_rejet)
    st.write("### Données de synthèse")
    st.dataframe(data_synthese)
    st.write("### Données initiales")
    st.dataframe(data_initial)
#==============ONGLET GENERAL===================
with tab_[1]:

    kpi_col=st.columns(3)
    #initial_to_use["Nombre de chèque à saisir"]=initial_to_use["Nombre de chèque à saisir"].astype('Int64')
    total_cheque_a_saisir=initial_to_use["Nombre de chèque à saisir"].sum()
    total_cheq_saisie=rejet_to_use.shape[0]
    with kpi_col[0]:
        
        display_single_metric_advanced("Nombre Total de chèque à Saisir",total_cheque_a_saisir, delta=0, color_scheme="green")
        
    with kpi_col[1]:
        
        display_single_metric_advanced("Nombre de chèque saisie",total_cheq_saisie, delta=0,color_scheme="red")

    with kpi_col[2]:
        
        display_single_metric_advanced("Taux de réalisation",round(100*total_cheq_saisie/total_cheque_a_saisir,2), delta=0,color_scheme="orange", unit="%")

    st.write("")
    
    
    cheq_init_par_district=initial_to_use.groupby("NOM DISTRICT")["Nombre de chèque à saisir"].sum().reset_index().rename(columns={"Nombre de chèque à saisir":"Chèque à saisir"})
    cheq_par_district=rejet_to_use.groupby("NOM DISTRICT")["Numéro de chèque"].count().reset_index().rename(columns={"Numéro de chèque":"Chèque saisi"})
    tab_cheq_district=pd.merge(cheq_init_par_district,cheq_par_district,left_on="NOM DISTRICT", right_on="NOM DISTRICT", how="left")
    tab_cheq_district=tab_cheq_district.set_index("NOM DISTRICT")
    col_= st.columns(2)

    with col_[0]:
        #
        create_bar_chart_from_contingency(tab_cheq_district, var1_name="NOM DISTRICT", title="Chèque à saisir vs Chèque saisi par district", height="400px" )
        #create_crossed_bar_chart(good_data,var1="Region",var2="Statut_cheque",title="Répartition des chèques par région",height="350px" ) 

    with col_[1]:
        taux_realisation_district=tab_cheq_district.copy()
        taux_realisation_district["Taux de réalisation"]=round(taux_realisation_district["Chèque saisi"]/taux_realisation_district["Chèque à saisir"],2)
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
    district=st.multiselect("Sélectionnez le(s) district(s)", options=rejet_to_use["NOM DISTRICT"].unique(), default=rejet_to_use["NOM DISTRICT"].unique())
    rejet_district_choosed=rejet_to_use[rejet_to_use["NOM DISTRICT"].isin(district)] if len(district)!=0 else rejet_to_use
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
    col1, col2 = st.columns(2)

    with col1:
        pass
        #display_confusion_matrix(good_data, var1="Statut_facture", var2="Statut_cheque",keys="SKJBDCBNKJFN")

    with col2:
        pass
        #display_confusion_matrix(good_data, var1="Statut_facture", var2="Statut_cheque", value="Montant_mensuel",color_scheme="Oranges", keys="bdkjsndkjbk")

#==============ONGLET PERSONNEL==========================
with tab_[2]:
    def main():
    #st.write("Autre approche: Au cas ou la première approche ne marche pas, inscrivez vous dans l'onglet connexion ci contre et utiliser vos identifiants pour vous connecter")
        is_authenticated = authentication_system("Enqueteur")
        if is_authenticated:
            user=st.session_state.username
            good_data_user=good_data
            data_facture_user=data_facture
            
            kpi_col_user=st.columns(3)

            acept_facture_user=good_data_user["Statut_facture"].value_counts().to_dict()
            with kpi_col_user[0]:
                df_accepted_user=good_data_user[good_data_user["Statut_facture"]=="Acceptée"]
                coherence_user=df_accepted_user["Coherence"].value_counts().to_dict()
                display_single_metric_advanced("Chèque validé par le médecin",acept_facture_user["Acceptée"], delta=round(100*coherence_user["Coherent"]/acept_facture_user["Acceptée"],2),delta_label="Coherence", color_scheme="green")
                
            with kpi_col_user[1]:    
                df_accepted_user=good_data_user[good_data_user["Statut_facture"]=="Rejetée"]
                coherence_user=df_accepted_user["Coherence"].value_counts().to_dict()
                display_single_metric_advanced("Chèque invalidé par le médecin",acept_facture_user["Rejetée"], delta=round(100*coherence_user["Coherent"]/acept_facture_user["Rejetée"],2),delta_label="Coherence",color_scheme="red")

            with kpi_col_user[2]:
                df_coherent=good_data_user[good_data_user["Coherence"]=="Coherent"]
                coherence_user=df_accepted_user["Coherence"].value_counts().to_dict()
                display_single_metric_advanced("Total chèque",good_data_user.shape[0], delta=round(100*df_coherent.shape[0]/good_data_user.shape[0],2),delta_label="Coherence",color_scheme="orange")


            st.write("")
            # Deuxième ligne avec calendrier et tranches de facturation
            col_= st.columns([2, 1])
            
            with col_[0]:
                create_crossed_bar_chart(good_data,var1="Region",var2="Statut_cheque",title="Répartition des chèques par région",height="350px", keys="skjdkjnkjfvns" )

        
            
            with col_[1]:
                create_pie_chart_from_df(data_facture_user,column="Statut de Facture selon le Médecin Conseil", colors=["green","red"],height="300px", title="Proportion",cle="jbcjhbsdjch")
                col_1=st.columns(2)
                with col_1[0]:
                    st.markdown("Graph1")
                with col_1[1]:
                    st.markdown("Graph2")

            # Troisième ligne avec Top 5 clients et Revenus par commerciaux
            col1, col2 = st.columns(2)

            with col1:
                display_confusion_matrix(good_data_user, var1="Statut_facture", var2="Statut_cheque", keys="jffkjnj")

            with col2:
                display_confusion_matrix(good_data_user, var1="Statut_facture", var2="Statut_cheque", value="Montant_mensuel",color_scheme="Oranges", keys="dsbcducvh")
            
            st.write(f"Bienvenue **{user}** dans votre section Personnel")
            st.write("Ici vous pouvez consulter les informations relatives au personnel de FOSA.")

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