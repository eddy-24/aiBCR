import json
import os

PUNCTE_FILE = "puncte.json"

def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_puncte():
    return load_json_file(PUNCTE_FILE)

def save_puncte(data):
    save_json_file(PUNCTE_FILE, data)

def economie(data):
    venit = data.get("GPI_LST_SALARY_ND", 0)
    print(f"📌 Sugestie: economisește 10% din venit = {venit * 0.10:.2f} lei/lună.")

def plan_personalizat(data):
    if data.get("MCC_CLOTHING_AMT", 0) > 1000:
        print("🛍️ Cheltuieli mari pe haine. Sugestie: buget + cashback.")
    if data.get("MCC_FOOD_AMT", 0) > 1200:
        print("🍕 Cheltuieli mari pe mâncare. Sugestie: listă de cumpărături.")
    print("✅ Recomandări bazate pe comportamentul tău.")

def simulare_decizie():
    print("📊 Simulare decizie:")
    print("1. Animal de companie (~300 lei/lună)")
    print("2. Credit (~350 lei/lună)")
    print("3. Abonament (~50 lei/lună)")
    opt = input("Alege: ").strip()
    if opt == "1":
        print("🐶 Cost estimat: 300 lei/lună.")
    elif opt == "2":
        print("💳 Rată estimată: 350 lei/lună.")
    elif opt == "3":
        print("📺 Cost total anual: ~600 lei.")

def obiectiv(puncte_data):
    obj = input("🎯 Obiectiv (ex: vacanță): ")
    suma = float(input("Sumă dorită: "))
    luni = int(input("Luni până la obiectiv: "))
    lunar = suma / luni
    print(f"✔️ Economisește {lunar:.2f} lei/lună pentru {obj}")
    puncte_data["puncte"] += 10
    save_puncte(puncte_data)
    print("🎁 +10 puncte primite!")

def evenimente_viitoare():
    tip = input("📅 Eveniment (ex: vacanță): ")
    suma = input("Cost estimat: ")
    data = input("Data: ")
    print(f"🔔 Reține: {tip} pe {data}, estimat {suma} lei")

def scenariu_viata():
    tip = input("🎓 Scenariu (ex: pensie): ")
    cost = float(input("Cost estimat total: "))
    ani = int(input("În câți ani?: "))
    print(f"🧠 Economisește ~{cost / (ani * 12):.2f} lei/lună pentru {tip}")

def provocare(puncte_data):
    rasp = input("🎯 Ai economisit 200 lei săptămâna aceasta? (da/nu): ").lower()
    if rasp == "da":
        puncte_data["puncte"] += 20
        print("✅ +20 puncte câștigate!")
    else:
        print("❌ Mai încearcă săptămâna viitoare.")
    save_puncte(puncte_data)

def magazin(puncte_data):
    print(f"🪙 Ai {puncte_data['puncte']} puncte.")
    print("1. Voucher 10 lei - 50p")
    alegere = input("Răscumperi ceva? (1/nu): ")
    if alegere == "1" and puncte_data["puncte"] >= 50:
        puncte_data["puncte"] -= 50
        print("🎁 Voucher acordat!")
    else:
        print("❗ Puncte insuficiente.")
    save_puncte(puncte_data)

def asistent_menu(data_client):
    puncte = load_puncte()
    while True:
        print("\n🤖 Asistent Financiar Inteligent:")
        print("1. Vreau să economisesc")
        print("2. Fă-mi un plan personalizat")
        print("3. Simulează o decizie financiară")
        print("4. Setează un obiectiv 🎯")
        print("5. Evenimente viitoare 📆")
        print("6. Scenarii de viață 📚")
        print("7. Provocare adaptivă 🔁")
        print("8. Magazin de puncte 🛍️")
        print("0. Înapoi")

        opt = input("Alege: ").strip()
        if opt == "1":
            economie(data_client)
        elif opt == "2":
            plan_personalizat(data_client)
        elif opt == "3":
            simulare_decizie()
        elif opt == "4":
            obiectiv(puncte)
        elif opt == "5":
            evenimente_viitoare()
        elif opt == "6":
            scenariu_viata()
        elif opt == "7":
            provocare(puncte)
        elif opt == "8":
            magazin(puncte)
        elif opt == "0":
            break
        else:
            print("❗ Opțiune invalidă.")

def main():
    data_client = {
        "GPI_LST_SALARY_ND": 4000.0,
        "SAV_TOTAL_BALANCE_AMT": 1200.0,
        "MCC_CLOTHING_AMT": 1300.0,
        "MCC_FOOD_AMT": 1100.0
    }
    asistent_menu(data_client)

if __name__ == "__main__":
    main()
