import streamlit as st
from instagrapi import Client
from deepface import DeepFace
import ollama
import requests
import os
import random

st.set_page_config(page_title="Insta Prospect IA", layout="wide")
st.title("🧠 Insta Prospect IA - Récupération Followers")

if 'client' not in st.session_state:
    st.session_state.client = None
if 'prospects' not in st.session_state:
    st.session_state.prospects = []

# ===================== CONNEXION =====================
st.sidebar.subheader("Connexion Instagram")
if st.session_state.client is None:
    username = st.sidebar.text_input("Ton username (compte secondaire)")
    password = st.sidebar.text_input("Mot de passe", type="password")
    if st.sidebar.button("Se connecter"):
        if username and password:
            with st.spinner("Connexion..."):
                try:
                    cl = Client()
                    cl.login(username, password)
                    st.session_state.client = cl
                    st.sidebar.success("✅ Connecté")
                except Exception as e:
                    st.sidebar.error(f"Erreur: {e}")
else:
    st.sidebar.success("✅ Connecté")

# ===================== RÉCUPÉRATION FOLLOWERS =====================
st.subheader("1. Récupérer des followers")
celebrity_username = st.text_input("Username du gros compte (ex: neymarjr, kimkardashian)", placeholder="groscompte")

if st.button("Récupérer des followers"):
    if st.session_state.client is None:
        st.error("Connecte-toi d'abord")
    else:
        with st.spinner("Récupération des followers en cours (ça peut prendre du temps)..."):
            try:
                cl = st.session_state.client
                user_id = cl.user_id_from_username(celebrity_username)
                followers = cl.user_followers(user_id, amount=30)  # max 30 pour limiter le risque
                
                new_prospects = []
                for user_id, user in list(followers.items())[:20]:  # limite à 20
                    try:
                        u = cl.user_info(user_id)
                        if u.is_private:
                            continue
                        
                        first_name = u.full_name.split()[0] if u.full_name else u.username
                        bio = u.biography or ""
                        
                        # Face detection
                        has_face = False
                        try:
                            img_data = requests.get(u.profile_pic_url).content
                            with open("temp.jpg", "wb") as f:
                                f.write(img_data)
                            faces = DeepFace.extract_faces("temp.jpg", detector_backend="retinaface")
                            has_face = len(faces) > 0
                            os.remove("temp.jpg")
                        except:
                            pass
                        
                        if not has_face:
                            continue
                        
                        # Message IA
                        prompt = f"Message Instagram court, sympa et naturel pour {first_name}. Bio: {bio[:130]}"
                        resp = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
                        message = resp['message']['content'].strip()
                        
                        new_prospects.append({
                            "username": u.username,
                            "name": u.full_name,
                            "has_face": has_face,
                            "message": message
                        })
                    except:
                        continue
                
                st.session_state.prospects.extend(new_prospects)
                st.success(f"{len(new_prospects)} profils qualifiés ajoutés !")
            except Exception as e:
                st.error(f"Erreur récupération : {e}")

# ===================== DASHBOARD =====================
st.subheader("2. Profils qualifiés - Validation manuelle")
for i, p in enumerate(st.session_state.prospects):
    with st.expander(f"@{p['username']} - {p.get('name','')}"):
        st.write(f"**Visage détecté :** {'✅ Oui' if p['has_face'] else '❌ Non'}")
        
        edited_message = st.text_area("Modifie le message si besoin :", p['message'], height=140, key=f"msg{i}")
        
        col1, col2 = st.columns(2)
        if col1.button("✅ Envoyer tel quel", key=f"send{i}"):
            try:
                cl = st.session_state.client
                user = cl.user_info_by_username(p['username'])
                cl.direct_send(edited_message, [user.pk])
                st.success(f"Message envoyé à @{p['username']} !")
            except Exception as e:
                st.error(f"Échec envoi : {e}")
        
        if col2.button("❌ Skip ce profil", key=f"skip{i}"):
            st.info("Profil ignoré")

st.caption("⚠️ Utilise avec modération (10-20 max par jour). Risque de ban élevé.")