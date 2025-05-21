import json
import unicodedata
import Levenshtein
from answers import *
from topics import *
import spacy

nlp = spacy.load("ro_core_news_sm")

def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

synonyms = load_json_file("synonyms.json")
synonyms = {k: [remove_accents(s.lower().replace("?", "")) for s in v] for k, v in synonyms.items()}
intents_dict = load_json_file("raspunsuri.json")

def parse_question_levenshtein(text, threshold=0.6):
    text = remove_accents(text.lower().strip())
    best_intent, best_score = None, 0.0
    for intent, phrases in synonyms.items():
        for phrase in phrases:
            score = Levenshtein.ratio(text, phrase)
            if score > best_score:
                best_score, best_intent = score, intent
    return (best_intent, None, None) if best_score >= threshold else (None, None, None)

def education_menu():
    while True:
        print("\n📚 Categorii disponibile:")
        print("1. Educație financiară de bază")
        print("2. Educație financiară avansată")
        print("3. Securitate cibernetică")
        print("4. Educație pentru adolescenți")
        print("5. Educație în funcție de vârstă")
        print("0. Înapoi la meniul principal")
        cat_choice = input("Alege o categorie: ").strip()

        if cat_choice == "0":
            return

        categories = {
            "1": basic_finance_education,
            "2": advanced_finance_education,
            "3": security_education,
            "4": adolescent_finance_education,
            "5": parent_age_education
        }

        selected_cat = categories.get(cat_choice)
        if not selected_cat:
            print("❗ Selecție invalidă.")
            continue

        while True:
            keys = list(selected_cat.keys())
            print("\n📖 Lecții disponibile:")
            for i, key in enumerate(keys, 1):
                print(f"{i}. {selected_cat[key]['intrebare']}")
            print("0. Înapoi la categorii")

            lesson_choice = input("Alege lecția dorită: ").strip()
            if lesson_choice == "0":
                break
            if lesson_choice.isdigit() and 1 <= int(lesson_choice) <= len(keys):
                lec = selected_cat[keys[int(lesson_choice)-1]]
                print(f"\n{lec['raspuns']}\n")
                input("🔙 Apasă Enter pentru a reveni la lista de lecții...")
            else:
                print("❗ Selecție invalidă.")

def get_financial_answer(data):
    print("\n💬 Modul întrebări despre cont. Tastează 'exit' pentru a reveni.")
    while True:
        text = input("Întrebarea ta: ").strip()
        if text.lower() == "exit":
            break
        intent, _, _ = parse_question_levenshtein(text)
        response_func = intents_dict.get(intent)
        if response_func:
            response = globals()[response_func](data)
        else:
            response = "Îmi pare rău, nu am înțeles întrebarea."
        print(f"Răspuns: {response}\n")

def main():
    data_client = {
        "TRX_IN_ALL_AMT": 10000.0,
        "TRX_OUT_ALL_AMT": 8000.0,
        "DEP_TOTAL_BALANCE_AMT": 5000.0,
        "CRT_TOTAL_BALANCE_AMT": 3000.0,
        "GPI_LST_SALARY_ND": 4000.0,
        "SAV_TOTAL_BALANCE_AMT": 1500.0,
        "MCC_FOOD_AMT": 1100.0
    }

    while True:
        print("\n🎓 Bun venit în platforma BCR Banking")
        print("1. Educație financiară")
        print("2. Întrebări despre cont")
        print("0. Ieșire")

        opt = input("Alege opțiunea: ").strip()
        if opt == "1":
            education_menu()
        elif opt == "2":
            get_financial_answer(data_client)
        elif opt == "0":
            print("👋 La revedere!")
            break
        else:
            print("❗ Opțiune invalidă.")

if __name__ == "__main__":
    main()
