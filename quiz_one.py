import streamlit as st

# Configuration de la page
st.set_page_config(page_title="QCM Désancrage packer", page_icon="✅")

# --- CONSTANTES ET DONNÉES ---
PASS_MARK = 70
QUESTIONS = [
    (
        "Quel est le fluide généralement utilisé lors des opérations de sand-jetting ?",
        {
            "A": "Eau douce",
            "B": "Brine d’injection 1.12 Sg",
            "C": "Huile légère",
            "D": "Boue de forage",
        },
        "B",
        "On utilise généralement de la brine d’injection 1.12 Sg pour les opérations de sand-jetting."
    ),
    (
        "Pourquoi faut-il prévoir les effets des changements dans le puits avant de désancrer le packer ?",
        {
            "A": "Pour réduire le temps d’opération",
            "B": "Pour anticiper les variations de densité et de pression",
            "C": "Pour éviter la corrosion du tubing",
            "D": "Pour améliorer la qualité du fluide",
        },
        "B",
        "Les variations de densité et de pression peuvent créer des déséquilibres importants au moment du désancrage."
    ),
    (
        "Quel risque peut apparaître après le nettoyage des perforations ?",
        {
            "A": "Effet Venturi",
            "B": "Effet de tube en « U »",
            "C": "Effet siphon inversé",
            "D": "Effet vortex",
        },
        "B",
        "Après nettoyage, la différence de colonne de fluide peut engendrer un effet de tube en « U »."
    ),
    (
        "Que doit-on faire avant de commencer le désancrage du packer ?",
        {
            "A": "Installer une pompe centrifuge",
            "B": "Tenir un pré-job meeting",
            "C": "Purger le tubing avec air comprimé",
            "D": "Fermer toutes les vannes",
        },
        "B",
        "Le pré-job meeting permet d’aligner les équipes sur les risques, les responsabilités et la procédure."
    ),
    (
        "Quel est le rôle de la Kelly valve dans cette opération ?",
        {
            "A": "Contrôler la pression dans l’annulaire",
            "B": "Servir de vanne de sécurité en position ouverte",
            "C": "Isoler le tubing du casing",
            "D": "Réguler le débit de sand-jetting",
        },
        "B",
        "La Kelly valve est utilisée comme barrière de sécurité et est laissée en position ouverte en fonctionnement normal."
    ),
    (
        "Combien de temps faut-il attendre après la rétraction des garnitures du PKR ?",
        {
            "A": "5 min",
            "B": "10 min",
            "C": "15 min (selon type PKR)",
            "D": "30 min",
        },
        "C",
        "On attend environ 15 minutes (selon le type de packer) pour assurer la rétraction complète des garnitures."
    ),
    (
        "Que faire si un retour de fluide ou gaz est constaté par l’annulaire et/ou le tubing ?",
        {
            "A": "Continuer l’opération",
            "B": "Fermer immédiatement le BOP",
            "C": "Augmenter la vitesse de remontée",
            "D": "Injecter de l’air comprimé",
        },
        "B",
        "Un retour non contrôlé indique un risque de kick : il faut fermer immédiatement le BOP."
    ),
    (
        "Quel est le débit recommandé pour remplir le tubing pendant le POOH des Macaronis ?",
        {
            "A": "0.22 l/m",
            "B": "0.44 l/m",
            "C": "1.12 l/m",
            "D": "2.00 l/m",
        },
        "B",
        "Le débit recommandé est d’environ 0,44 l/m pour garder la colonne pleine sans surcharger le puits."
    ),
    (
        "Que doit faire l’opérateur au plancher pendant le flow check ?",
        {
            "A": "Observer le comportement dans l’annulaire via le BOP",
            "B": "Vérifier la densité du fluide",
            "C": "Installer la Kelly valve",
            "D": "Purger le tubing",
        },
        "A",
        "Lors du flow check, l’opérateur observe le comportement du fluide dans l’annulaire via le BOP."
    ),
    (
        "Si le retour de fluide ne se calme pas après fermeture du BOP, quelle action est requise ?",
        {
            "A": "Ouvrir toutes les vannes",
            "B": "Fermer les vannes 2 et 4 et préparer la circulation avec brine",
            "C": "Injecter du gaz pour équilibrer",
            "D": "Continuer le désancrage",
        },
        "B",
        "Si le retour persiste, il faut fermer les vannes 2 et 4 et préparer une circulation avec brine."
    ),
]

# --- GESTION DE L'ÉTAT (Session State) ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False

# --- FONCTIONS ---
def submit_answer(user_choice, correct_response):
    is_correct = (user_choice == correct_response)
    if is_correct:
        st.session_state.score += 1

    st.session_state.user_answers.append(
        {
            "q_index": st.session_state.current_question,
            "user": user_choice,
            "correct": correct_response,
            "is_correct": is_correct,
        }
    )

    if st.session_state.current_question < len(QUESTIONS) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.quiz_finished = True


def restart_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.user_answers = []
    st.session_state.quiz_finished = False

# --- INTERFACE UTILISATEUR ---
st.title("QCM – Désancrage packer")

if not st.session_state.quiz_finished:
    q_idx = st.session_state.current_question
    question_text, options, correct_resp, explanation = QUESTIONS[q_idx]

    st.progress(q_idx / len(QUESTIONS))
    st.subheader(f"Question {q_idx + 1}/{len(QUESTIONS)}")
    st.write(f"**{question_text}**")

    choice_label = st.radio(
        "Choisissez une réponse :",
        list(options.keys()),
        format_func=lambda x: f"{x}) {options[x]}",
        key=f"radio_{q_idx}",
    )

    if st.button("Valider", type="primary"):
        submit_answer(choice_label, correct_resp)
        st.rerun()

else:
    st.balloons()
    total = len(QUESTIONS)
    score_pct = round(st.session_state.score * 100.0 / total, 2)

    st.write("---")
    st.header(f"Résultat : {st.session_state.score}/{total} ({score_pct}%)")

    if score_pct >= PASS_MARK:
        st.success("🎉 Félicitations : Test réussi !")
    else:
        st.error("⚠️ Échec : Vous n'avez pas atteint le seuil requis.")

    with st.expander("Voir le détail des corrections"):
        for i, ans in enumerate(st.session_state.user_answers):
            q_data = QUESTIONS[i]
            status = "✅" if ans["is_correct"] else "❌"
            st.markdown(f"**Q{i+1} {status}** : {q_data[0]}")
            st.markdown(f"Votre réponse : {ans['user']}")
            st.markdown(f"Bonne réponse : **{ans['correct']}**")
            st.info(f"Note : {q_data[3]}")
            st.markdown("---")

    st.button("Recommencer le QCM", on_click=restart_quiz)
