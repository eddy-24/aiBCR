import json
import unicodedata
from answers import *
from topics import *
import Levenshtein
import spacy
import os

nlp = spacy.load("ro_core_news_sm")
PUNCTE_FILE = "puncte.json"

# ---------------------------- UTILITARE ----------------------------
def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_puncte():
    if os.path.exists(PUNCTE_FILE):
        return json.load(open(PUNCTE_FILE))
    return {"puncte": 0}

def save_puncte(puncte):
    save_json_file(PUNCTE_FILE, puncte)

# ---------------------------- PARSARE ----------------------------
synonyms = load_json_file("synonyms.json")
synonyms = {k: [remove_accents(s.lower().replace("?", "")) for s in v] for k, v in synonyms.items()}

def parse_question_levenshtein(text, threshold=0.6):
    text = remove_accents(text.lower().strip())
    best_intent, best_score = None, 0.0
    for intent, phrases in synonyms.items():
        for phrase in phrases:
            score = Levenshtein.ratio(text, phrase)
            if score > best_score:
                best_score, best_intent = score, intent
    return (best_intent, None, None) if best_score >= threshold else (None, None, None)

# ---------------------------- RĂSPUNSURI ----------------------------
intents_dict = load_json_file("raspunsuri.json")

def get_financial_answer(data):
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

# ---------------------------- FUNCȚII INTELIGENTE ----------------------------

def economie(data):
    venit = data.get("GPI_LST_SALARY_ND", 0)
    suma = venit * 0.1
    print(f"📌 Sugestie: economisește 10% din venit = {suma:.2f} lei/lună.")

def plan_personalizat(data):
    if data.get("MCC_CLOTHING_AMT", 0) > 1000:
        print("🛍️ Cheltuieli mari pe haine. Sugestie: setare buget și cashback la magazine.")
    if data.get("MCC_FOOD_AMT", 0) > 1200:
        print("🍕 Cheltuieli mari pe mâncare. Sugestie: cumpărături planificate.")
    print("✅ Plan generat pe baza cheltuielilor dominante.")

def predictii(data):
    economii = data.get("SAV_TOTAL_BALANCE_AMT", 0)
    venit = data.get("GPI_LST_SALARY_ND", 0)
    if economii < 3 * venit:
        print("🔮 Fond de urgență insuficient. Țintă: 3x venit lunar.")
    else:
        print("🔮 Fondul tău de urgență este stabil. Bravo!")

def simulare_decizie():
    print("📊 Ce vrei să simulezi?")
    print("1. Animal de companie 🐶 (~300 lei/lună)")
    print("2. Credit nou (10.000 lei -> ~350 lei/lună)")
    print("3. Abonament lunar (Netflix, sport etc.)")
    opt = input("Alege: ").strip()
    if opt == "1":
        print("Cost estimat: 300 lei/lună")
    elif opt == "2":
        print("Rată estimată: 350 lei/lună x 36 luni")
    elif opt == "3":
        print("Abonamente lunare pot consuma 600-1000 lei/an")

def obiectiv_financiar(puncte_data):
    obiectiv = input("🎯 Obiectiv (ex: vacanță, gadget): ").strip()
    suma = float(input("Suma dorită (lei): ").strip())
    luni = int(input("Luni pentru atingere: ").strip())
    lunar = suma / luni
    print(f"✔️ Economisește {lunar:.2f} lei/lună pentru '{obiectiv}'")
    puncte_data["puncte"] += 10
    print("🎁 +10 puncte pentru obiectiv setat!")
    save_puncte(puncte_data)

def evenimente_viitoare():
    print("📆 Adaugă evenimente planificate:")
    tip = input("Eveniment (ex: vacanță, factură, aniversare): ")
    suma = input("Cost estimat (lei): ")
    data = input("Data evenimentului (ex: 15.06.2025): ")
    print(f"🔔 Reține: {tip} pe {data}, buget estimat {suma} lei")

def scenariu_viata():
    print("📅 Simulare eveniment major (căsătorie, copil, pensie...)")
    tip = input("Eveniment: ")
    cost = input("Estimare cost total: ")
    ani = input("În câți ani va avea loc?: ")
    print(f"🧠 Estimare: ai nevoie de {cost} lei în {ani} ani => ~{float(cost)/int(ani)/12:.2f} lei/lună")

def provocare_saptamanala(puncte_data):
    print("🎯 Provocare: Economisește 200 lei în 7 zile.")
    rasp = input("Ai reușit? (da/nu): ").lower()
    if rasp == "da":
        puncte_data["puncte"] += 20
        print("✅ Felicitări! +20 puncte adăugate.")
    else:
        print("❌ Nu-i nimic. Mai încearcă săptămâna viitoare.")
    save_puncte(puncte_data)

def magazin_puncte(puncte_data):
    print(f"🪙 Ai {puncte_data['puncte']} puncte.")
    print("1. Voucher 10 lei = 50 puncte")
    print("2. Acces extra lecție = 30 puncte")
    alegere = input("Vrei să răscumperi ceva? (1/2/nimic): ").strip()
    if alegere == "1" and puncte_data["puncte"] >= 50:
        puncte_data["puncte"] -= 50
        print("🎁 Ai primit un voucher de 10 lei!")
    elif alegere == "2" and puncte_data["puncte"] >= 30:
        puncte_data["puncte"] -= 30
        print("🎁 Acces deblocat la o lecție avansată!")
    else:
        print("❗ Puncte insuficiente sau opțiune invalidă.")
    save_puncte(puncte_data)

# ---------------------------- MENIU PRINCIPAL ----------------------------
def asistent_financiar(data_client):
    puncte_data = load_puncte()
    while True:
        print("\n🤖 Asistent Financiar Inteligent:")
        print("1. Vreau să economisesc")
        print("2. Fă-mi un plan personalizat")
        print("3. Oferă-mi predicții")
        print("4. Simulează o decizie financiară")
        print("5. Setează un obiectiv 🎯")
        print("6. Evenimente viitoare 📆")
        print("7. Scenarii de viață 📚")
        print("8. Provocare adaptivă 🔁")
        print("9. Magazin de puncte 🛍️")
        print("0. Înapoi")
        opt = input("Alege opțiunea: ").strip()
        if opt == "1":
            economie(data_client)
        elif opt == "2":
            plan_personalizat(data_client)
        elif opt == "3":
            predictii(data_client)
        elif opt == "4":
            simulare_decizie()
        elif opt == "5":
            obiectiv_financiar(puncte_data)
        elif opt == "6":
            evenimente_viitoare()
        elif opt == "7":
            scenariu_viata()
        elif opt == "8":
            provocare_saptamanala(puncte_data)
        elif opt == "9":
            magazin_puncte(puncte_data)
        elif opt == "0":
            break

# ---------------------------- MAIN ----------------------------
def main():
    print("🎓 Bun venit în platforma BCR Banking")
    print("1. Educație financiară")
    print("2. Întrebări despre cont")
    print("3. Asistent financiar inteligent 💡")
    print("0. Ieșire")

    while True:
        opt = input("Alege o opțiune: ").strip()
        if opt == "0":
            break
        elif opt == "1":
            print("🔜 Lecții educație financiară (vechi meniu)")
        elif opt == "2":
            data_client = {
                "TRX_IN_ALL_AMT": 10000.0,
                "TRX_OUT_ALL_AMT": 8200.0,
                "DEP_TOTAL_BALANCE_AMT": 3000.0,
                "CRT_TOTAL_BALANCE_AMT": 2000.0,
                "GPI_LST_SALARY_ND": 4000.0,
                "SAV_TOTAL_BALANCE_AMT": 1500.0,
                "MCC_CLOTHING_AMT": 1400.0,
                "MCC_FOOD_AMT": 1300.0
            }
            get_financial_answer(data_client)
        elif opt == "3":
            data_client = {
                "GPI_LST_SALARY_ND": 4000.0,
                "SAV_TOTAL_BALANCE_AMT": 1500.0,
                "MCC_CLOTHING_AMT": 1400.0,
                "MCC_FOOD_AMT": 1300.0
            }
            asistent_financiar(data_client)
        else:
            print("❗ Opțiune invalidă.")

if __name__ == "__main__":
    main()
