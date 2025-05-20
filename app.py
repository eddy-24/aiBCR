import re
import unicodedata
import json
from spellchecker import SpellChecker
import Levenshtein
from answers import *
import spacy
nlp = spacy.load("ro_core_news_sm")
from topics import security_education, basic_finance_education, advanced_finance_education, adolescent_finance_education, parent_age_education


# Funcție pentru eliminarea diacriticelor
def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

# Funcție pentru eliminarea semnului întrebării
def remove_question_mark(text):
    return text.replace("?", "").strip()

# Funcție pentru corectarea greșelilor de scriere
def correct_spelling(text):
    spell = SpellChecker(language='en')
    words = text.split()
    corrected_words = [spell.correction(word) if spell.correction(word) is not None else word for word in words]
    return " ".join(corrected_words)

# Funcție pentru curățarea textului
def clean_text(text):
    text = remove_question_mark(text)
    text = remove_accents(text.lower())  # Elimină diacriticele și face textul lowercase
    text = correct_spelling(text)  # Corectează greșelile de ortografie
    return text.strip()

# Încărcarea sinonimelor din fișier JSON
def load_synonyms(filename="synonyms.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

synonyms = load_synonyms()

# Funcție pentru calcularea similarității între două șiruri
def calculate_similarity(text1, text2):
    # Folosește Levenshtein Distance pentru a calcula diferența
    return Levenshtein.ratio(text1, text2)

def extract_keywords_from_synonyms(synonyms_dict):
    keywords_dict = {}
    for intent, phrases in synonyms_dict.items():
        keywords = set()
        for phrase in phrases:
            doc = nlp(phrase.lower())
            for token in doc:
                if token.pos_ in {"NOUN", "ADJ"}:
                    clean_token = token.lemma_.strip()
                    if clean_token.isalpha():
                        keywords.add(clean_token)
        keywords_dict[intent] = keywords
    return keywords_dict

keywords_dict = extract_keywords_from_synonyms(synonyms)


def parse_question(text):
    clean = clean_text(text)
    words = set(clean.split())

    direct_keywords = {
    "raport_financiar": ["raport", "financiar", "situatie", "finante"],
    "cheltuieli_mâncare": ["mancare", "alimentare", "supermarket", "restaurante", "mese", "mananci"],
    "cheltuieli_utilități": ["utilitati", "curent", "electricitate", "gaz", "apa", "facturi"],
    "cheltuieli_transport": ["transport", "combustibil", "naveta", "calatorii", "autobuz", "tren"],
    "sold_total_conturi": ["sold total", "conturi", "total", "banca", "balanta"],
    "sold_cont_curent": ["cont", "curent", "sold curent", "disponibil"],
    "sold_cont_depozit": ["depozit", "economii", "sold depozit", "cont economii"],
    "sold_credit": ["credit", "sold credit", "datorie", "imprumut"],
    "limita_card_credit": ["limita", "card", "credit", "disponibil"],
    "cheltuieli_digital_payments": ["apple pay", "google pay", "portofel digital", "plati digitale"],
    "tranzacții_atm": ["atm", "retrageri", "plati atm", "tranzactii atm"],
    "cheltuieli_retail": ["retail", "shopping", "magazine", "haine", "cumparaturi"],
    "limita_credit_utilizata": ["limita credit", "utilizat credit", "credit folosit"],
    "venit_luna_trecuta": ["venit", "salariu", "incasari", "luna trecuta"],
    "economisire_10_percent": ["economisire", "economii", "10%", "salariu", "pun peoparte"],
    "produse_active_banca": ["produse banca", "carduri", "conturi", "servicii bancare"],
    "durata_relatie_banca": ["durata relatie", "client banca", "de cat timp", "vechime cont"],
    "stare_cererilor_imprumut": ["cereri imprumut", "status imprumut", "cerere credit"],
    "cheltuieli_calatorii": ["calatorii", "vacante", "excursii", "transport international"],
    "cheltuieli_divertisment": ["divertisment", "distractie", "evenimente", "cluburi", "petreceri"],
    "sold_cont_economii": ["economii", "cont economii", "sold economii"],
    "intretinere_locuinta": ["intretinere", "reparatii", "locuinta", "renovare", "casa"],
    "cheltuieli_îmbrăcăminte": ["haine", "imbracaminte", "shopping", "articole vestimentare"],
    "servicii_profesionale": ["servicii profesionale", "consultanta", "avocat", "servicii juridice"],
    "cheltuieli_restaurante": ["restaurante", "mese in oras", "baruri", "cafenele", "mancare la restaurant"],
    "utilizare_overdraft": ["overdraft", "limita overdraft", "cont overdraft", "utilizare overdraft"],
    "sold_refinanțare": ["refinantare", "sold refinantare", "credit refinantare"],
    "tranzacții_international": ["tranzactii internationale", "plati internationale", "cheltuieli internationale"],
    "venituri_cheltuieli_anul": ["venituri anuale", "cheltuieli anuale", "raport anual", "balanta anuala"],
    "istoric_imprumuturi": ["istoric imprumuturi", "cereri credit", "status imprumuturi"],
    "produse_asigurare": ["asigurari", "produse asigurare", "polite asigurare"],
    "plăți_portofele_digitale": ["portofele digitale", "plati digitale", "apple pay", "google pay"],
    "servicii_afaceri": ["servicii afaceri", "consultanta afaceri", "servicii profesionale afaceri"],
    "comisioane_bancare": ["comisioane bancare", "taxe banca", "costuri bancare"],
    "sold_economii": ["sold economii", "cont economii", "economii"],
    "tranzacții_internet_banking": ["internet banking", "plati online", "tranzactii online"],
    "scor_credit": ["scor credit", "rating credit", "biroul de credit"],
    "utilizare_credit_ipotecar": ["credit ipotecar", "utilizare ipotecar", "sold credit ipotecar"],
    "sold_conturi_ultimele_3_luni": ["sold mediu", "media conturi", "ultimele 3 luni"],
    "evolutie_cheltuieli_ultimele_12_luni": ["evolutie cheltuieli", "cheltuieli 12 luni", "evolutie anuala"],
}


    # 1. Caută dacă vreun cuvânt din întrebarea curățată e în direct_keywords
    for word in words:
        if word in direct_keywords:
            return direct_keywords[word], None, None

    # 2. Altfel, folosește matching pe sinonime cu scor simplu
    max_score = 0
    best_intent = None
    for intent, synonyms_list in synonyms.items():
        for synonym in synonyms_list:
            syn_words = set(synonym.lower().split())
            score = len(words.intersection(syn_words))
            if score > max_score:
                max_score = score
                best_intent = intent

    if max_score > 0:
        return best_intent, None, None

    return None, None, None


def remove_question_mark_from_synonym(synonym):
    return synonym.replace("?", "").strip()

synonyms = {key: [remove_question_mark_from_synonym(remove_accents(synonym)) for synonym in synonyms_list] 
            for key, synonyms_list in synonyms.items()}


def load_intents(filename="raspunsuri.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Dicționarul de funcții
intents_dict = load_intents()

# Funcția de răspuns
def get_answer_live(data):
    while True:
        # Cere utilizatorului să introducă întrebarea
        text = input("Pune întrebarea: ")

        # Închide aplicația dacă utilizatorul scrie "exit"
        if text.lower() == "exit":
            print("Încetarea aplicației...")
            break

        # Curăță textul și corectează greșelile
        text = remove_accents(text)

        # Identifică intenția și entitățile din întrebarea utilizatorului
        intent, category, percent = parse_question(text)

        # Căutăm funcția corespunzătoare în dicționarul de răspunsuri
        response_function = intents_dict.get(intent)

        if response_function:
            # Verifică dacă `response_function` este un string (numele funcției)
            if isinstance(response_function, str):
                # Apelăm funcția din glob
                response = globals()[response_function](data)
            else:
                response = "Funcția nu este definită corect."
        else:
            response = "Îmi pare rău, nu am înțeles întrebarea. Te rog reformulează."

        print("Răspuns:", response)
        print("-" * 40)


# meniu ai cu lectii
def ai_welcome():
    print("Bună! Bine ai venit la BCR Banking. Cu ce te pot ajuta azi? 😊")
    print("Selectează o opțiune:")
    print("1. Vreau să învăț educație financiară cu Scoala de bani📚")
    print("2. Am întrebări despre contul meu 💼")

def education_menu():
    categories = {
        "1": ("Cunoștințe de bază în educația financiară", basic_finance_education),
        "2": ("Cunoștințe avansate în educația financiară", advanced_finance_education),
        "3": ("Securitate Cibernetică", security_education),
        "4": ("Conversații despre bani cu adolescenții", adolescent_finance_education),
        "5": ("Cum îți educi copiii în funcție de vârstă", parent_age_education),
    }

    print("\nPerfect! Alege o categorie de interes:")
    for k, (name, _) in categories.items():
        print(f"{k}. {name}")

    cat_choice = input("Introdu numărul categoriei: ").strip()
    if cat_choice not in categories:
        print("Te rog să introduci un număr valid.")
        return

    cat_name, lessons_dict = categories[cat_choice]
    print(f"\nAi ales categoria: {cat_name}")

    # Afișează lecțiile disponibile
    keys = list(lessons_dict.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {lessons_dict[key]['intrebare']}")

    lesson_choice = input("Alege numărul lecției dorite: ").strip()
    if not lesson_choice.isdigit() or not (1 <= int(lesson_choice) <= len(keys)):
        print("Selecție invalidă.")
        return

    selected_key = keys[int(lesson_choice) - 1]
    lesson = lessons_dict[selected_key]
    print(f"\n--- {lesson['intrebare']} ---\n")
    print(lesson['raspuns'])
    print("\n" + "-"*40 + "\n")

def financial_questions(data_client):
    print("\nHai să vedem ce informații am despre contul tău. Pune întrebarea sau tastează 'exit' pentru a ieși.")
    while True:
        question = input("Întrebarea ta: ").strip()
        if question.lower() == "exit":
            print("Mulțumim că ai folosit BCR Banking. O zi frumoasă! 👋")
            break
        # Aici apelezi funcția ta parse_question + get_answer_live (sau o variantă adaptată)
        intent, _, _ = parse_question(question)
        response_function = intents_dict.get(intent)
        if response_function and isinstance(response_function, str):
            answer = globals()[response_function](data_client)
        else:
            answer = "Îmi pare rău, nu am înțeles întrebarea. Te rog reformulează."
        print(f"Răspuns: {answer}")
        print("-" * 40)


def main():
    ai_welcome()
    while True:
        option = input("Alege opțiunea 1 sau 2 (sau 'exit' pentru a ieși): ").strip()
        if option.lower() == "exit":
            print("La revedere!")
            break
        elif option == "1":
            education_menu()
        elif option == "2":
            data_client = {
                "TRX_IN_ALL_AMT": 10000.0,
                "TRX_OUT_ALL_AMT": 8000.0,
                "DEP_TOTAL_BALANCE_AMT": 5000.0,
                "CRT_TOTAL_BALANCE_AMT": 3000.0,
                "GPI_LST_SALARY_ND": 4000.0,
                "MCC_FOOD_AMT": 1200.0,
                "MCC_UTILITY_SERV_AMT": 300.0,
                "MCC_TRANSPORTATION_AMT": 200.0,
                "CEC_TOTAL_BALANCE_AMT": 7000.0,
                "ICC_APPROVED_LIMIT": 1500.0,
                "ICC_REMAINING_LIMIT_AMT": 1000.0,
            }
            financial_questions(data_client)
        else:
            print("Opțiune invalidă. Te rog să alegi 1 sau 2.")

if __name__ == "__main__":
    main()