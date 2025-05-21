import subprocess
import sys

def main():
    while True:
        print("\n🧠 Lansează platforma BCR Banking")
        print("1. Educație financiară & Întrebări despre cont")
        print("2. Asistent Financiar Inteligent")
        print("0. Ieșire")

        opt = input("Alege opțiunea: ").strip()
        if opt == "1":
            subprocess.run([sys.executable, "edu_cont.py"])
        elif opt == "2":
            subprocess.run([sys.executable, "asistent_inteligent.py"])
        elif opt == "0":
            print("👋 Închidere launcher. La revedere!")
            break
        else:
            print("❗ Opțiune invalidă. Încearcă din nou.")

if __name__ == "__main__":
    main()
