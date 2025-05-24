from tkinter import *
from tkinter import messagebox
from abc import ABC , abstractmethod
import re
from tkinter import ttk
from datetime import datetime
import csv
from  PIL import Image, ImageTk

root = Tk()
root.geometry("800x500")
root.configure(bg='white')
root.iconbitmap('bul.ico')
root.resizable(False, False)
root.title('COMPANY MANAGEMENT')

#classs
class Personne(ABC) :
    def __init__(self,nom,prenom,date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.datenaissance = date_naissance
        
    @abstractmethod
    def calculerSalaire (self) :
        pass

    def calculerAge(self) :
        dd = datetime.strptime(self.datenaissance, "%d/%m/%Y").date()
        today = datetime.now().date()  # Get today's date
        age = today.year - dd.year
        return age
    
    
    @classmethod
    def calculer_salaire_totale(cls):
        total = 0
        for i in Employe.listemploye:
            total += i.calculer_salaire()
        for i in Chef.listchef:
            total += i.calculer_salaire()
        return f"Total salaire: {total}"

    @staticmethod
    def afficher_par_departement(dep):
        for i in Chef.listchef:
            if i.departement == dep:
                print(i.afficher_info())
        print("----------------------------")
        for i in Employe.listemploye:
            if i.departement == dep:
                print(i.afficher_info())
        print("----------------------------")
class Employe(Personne):
    listemploye = []
    id = 0

    def __init__(self, nom, prenom, date_naissance, departement, hours_travail, salaire=0):
        super().__init__(nom, prenom, date_naissance)
        self.salaire = salaire
        self.departement = departement
        self.hours_travail = hours_travail
        if not isinstance(self, Chef):
            Employe.listemploye.append(self)
        Employe.id += 1
        self._id_emp = Employe.id

    def calculerSalaire(self):
        if self.hours_travail > 90:
            return self.salaire + ((self.hours_travail - 90) * (self.salaire // 90))
        return self.salaire
    
    

    def set_changer_departement(self, new_dep):
        self.departement = new_dep

    def afficher_info(self):
        return f"id: {self._id_emp} | nom: {self.nom} {self.prenom} | age: {Personne.calculerAge(self)} salaire: {self.salaire} | departement: {self.departement} | heures: {self.hours_travail} \n"

    @classmethod
    def augmenter_salaire(cls, salaire_ajouter):
        for employe in cls.listemploye:
            employe.salaire += salaire_ajouter

                

    def changer_deparetememnt(self, newdep):
        self.departement = newdep

    @classmethod
    def supprimer_employe(cls, employe):
        emp_id = int(input("donner id : "))
        for i in Personne.listemploye:
            if i._id_emp == emp_id:
                Personne.listemploye.remove(i)
            else:
                return "No employe"

    
    @classmethod
    def save_csv(cls):
        with open("employes.csv", "w") as emp:
            emp.write("id  \t  nom  \t  prenom \t age \t departement \t HeurTv \t salaire \n")
            for i in Employe.listemploye:
                i:Employe
                emp.write(f"{i._id_emp} \t {i.nom} \t {i.prenom} \t {i.datenaissance} \t {i.departement} \t {i.hours_travail} \t {i.salaire} \n")
        emp.close()
class Chef(Employe):
    listchef = []
    def __init__(self, nom, prenom, date_naissance, departement, hours_travail, prime,salaire=0):
        self.prime = prime
        Chef.listchef.append(self)
        super().__init__(nom, prenom, date_naissance, departement, hours_travail, salaire)

    def calculersalaire(self) :
        sal = super().calculer_salaire() + self.prime
        return sal

    def afficher_info(self):
        return f"{super().afficher_info()} | prime: {self.prime} \n -----------------------------------------"


    @classmethod
    def save_csv_chefs(cls):
        with open("chefs.csv", "w") as emp:
            emp.write("id \t nom \t prenom \t dateNaissance \t departement \t heursTravail \t prime \t salaire \n")
            i:Chef
            for i in Chef.listchef:
                emp.write(f"{i._id_emp} \t {i.nom} \t {i.prenom} \t {i.datenaissance} \t {i.departement} \t {i.hours_travail} \t {i.prime} \t {i.salaire} \n")

#GUI
def app():
    global image322
#afficher
    def aff():
        def back():
            title1.destroy()
            eemp.destroy()
            cchef.destroy()
            backk.destroy()
            app()
        def affemp():
            def backk2():
                title2.destroy()
                idd.destroy()
                affich.destroy()
                backkk.destroy()
                tree.destroy()
                aff()
            def empp_aff():
                iid = idd.get().strip()
                with open('employes.csv', 'r') as file:
                    filelines = file.readlines()
                    for i in filelines[1:]:
                        fields = i.strip().split('\t')
                        if fields[0].strip() == iid:
                            #emp_info = f"ID: {fields[0]} | Name: {fields[1]} {fields[2]} | Age: {fields[3]} | Department: {fields[4]} | Hours: {fields[5]} | Salary: {fields[6]}"
                            tree.insert('', 'end', values=(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6]))
                            break
                        else:
                            continue
            
            title1.destroy()
            eemp.destroy()
            cchef.destroy()
            backk.destroy()

            title2 = Label(root, text='Afficher employe', bg='white', font=['serif',18])
            title2.place(x=75, y=30)

            idd = Entry(root,
                width=24,
                bg='#95CAFE')
            idd.place(x=80, y=100)
            affich = Button(root, 
                text='afficher', 
                width=20,
                command=empp_aff,
                height=2,
                bg='#5189DC', 
                fg='black')
            affich.place(x=80, y=180)

            backkk = Button(root, 
                text='back', 
                width=20,
                command=backk2,
                height=2,
                bg='#5189DC', 
                fg='black')
            backkk.place(x=80, y=260)
            
            tree = ttk.Treeview(root, height=1, columns=("id", "name", "prenom", "date", "deparetement", "hoursTR", "salaire"), show="headings")
            tree.heading('id', text='ID')
            tree.heading('name', text='Nom')
            tree.heading('prenom', text='prenom')
            tree.heading('date', text='date')
            tree.heading('deparetement', text='depar')
            tree.heading('hoursTR', text='hoursTR')
            tree.heading('salaire', text='salaire')

            tree.column("id", width=10) 
            tree.column("name", width=50)     
            tree.column("prenom", width=50)
            tree.column("date", width=40)
            tree.column("deparetement", width=100)
            tree.column("hoursTR", width=80)
            tree.column("salaire", width=80)
            tree.place(x=80, y=360)
        def affchf():
            def backk2():
                title2.destroy()
                idd.destroy()
                affich.destroy()
                backkk.destroy()
                tree.destroy()
                aff()
            def chf_aff():
                iid = idd.get().strip()
                with open('chefs.csv', 'r') as file:
                    filelines = file.readlines()
                    for i in filelines[1:]:
                        fields = i.strip().split('\t')
                        if fields[0].strip() == iid:
                            #emp_info = f"ID: {fields[0]} | Name: {fields[1]} {fields[2]} | Age: {fields[3]} | Department: {fields[4]} | Hours: {fields[5]} | Salary: {fields[6]}"
                            tree.insert('', 'end', values=(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7]))
                            break
                        else:
                            continue

            title1.destroy()
            eemp.destroy()
            cchef.destroy()
            backk.destroy()

            title2 = Label(root, text='Afficher chef', bg='white', font=['serif',18])
            title2.place(x=85, y=30)

            idd = Entry(root,
                width=24,
                bg='#95CAFE')
            idd.place(x=80, y=100)
            affich = Button(root, 
                text='afficher', 
                width=20,
                command=chf_aff,
                height=2,
                bg='#5189DC', 
                fg='black')
            affich.place(x=80, y=180)

            backkk = Button(root, 
                text='back', 
                width=20,
                command=backk2,
                height=2,
                bg='#5189DC', 
                fg='black')
            backkk.place(x=80, y=260)
            
            tree = ttk.Treeview(root, height=1, columns=("id", "name", "prenom", "date", "deparetement", "hoursTR", "prime", "salaire"), show="headings")
            tree.heading('id', text='ID')
            tree.heading('name', text='Nom')
            tree.heading('prenom', text='prenom')
            tree.heading('date', text='date')
            tree.heading('deparetement', text='depar')
            tree.heading('hoursTR', text='hoursTR')
            tree.heading('prime', text='prime')
            tree.heading('salaire', text='salaire')

            tree.column("id", width=10) 
            tree.column("name", width=50)     
            tree.column("prenom", width=50)
            tree.column("date", width=40)
            tree.column("deparetement", width=100)
            tree.column("hoursTR", width=80)
            tree.column("prime", width=80)
            tree.column("salaire", width=80)
            tree.place(x=30, y=360)

        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()

        title1 = Label(root, text='Afficher', bg='white', font=['serif',18])
        title1.place(x=115, y=30)
        
        eemp = Button(root, 
                text='employe', 
                width=20,
                command=affemp,
                height=2,
                bg='#5189DC', 
                fg='black')
        eemp.place(x=80, y=100)
        cchef = Button(root, 
                text='chef', 
                width=20,
                command=affchf,
                height=2,
                bg='#5189DC', 
                fg='black')
        cchef.place(x=80, y=180)
        backk = Button(root, 
                text='back', 
                width=20,
                command=back,
                height=2,
                bg='#5189DC', 
                fg='black')
        backk.place(x=80, y=260)

#ajouter
    def ajou():
        def back():
            title1.destroy()
            add_emp.destroy()
            add_chef.destroy()
            backk.destroy()
            app()
        def empl():
            def backkemp():
                title2.destroy()
                nom_label.destroy()
                prenom_label.destroy()
                datenaissance_label.destroy()
                departement_label.destroy()
                hasattr_label.destroy()
                salaire_label.destroy()

                nom.destroy()
                prenom.destroy()
                datenaissance.destroy()
                departement.destroy()
                heurstravail.destroy()
                salaire.destroy()
                add.destroy()
                backkem.destroy()

                label1.destroy()
                ajou()

            def addempl():
                f = True
                n = nom.get()
                if not bool(re.match(r'^[a-zA-Z]{4,8}$',n)):
                    messagebox.showinfo("error","nom invalide")
                    f = False
                    
                p = prenom.get()
                if not bool(re.match(r'^[a-zA-Z]{4,8}$',p)):
                    messagebox.showinfo("error","prenom invalide")
                    f = False

                d = datenaissance.get()
                if not bool(re.match(r'^[0-9]{2}+/[0-9]{2}+/[0-9]{4}$',d)):
                    messagebox.showinfo("error","date invalide")
                    f = False

                dp = departement.get()
                if not bool(re.match(r'^[a-zA-Z]{4,8}$',dp)):
                    messagebox.showinfo("error","departement invalide")
                    f = False

                h = heurstravail.get()
                if not bool(re.match(r'^[0-9]{0,}$',h)):
                    messagebox.showinfo("error","heur invalide")
                    f = False

                s = salaire.get()
                if not bool(re.match(r'^[0-9]{0,}$',s)):
                    messagebox.showinfo("error","salaire invalide")
                    f = False

                if f == True:
                    Emp1 = Employe(n, p, d, dp, h, s)
                    Employe.save_csv()
                    label1.configure(text='data saved', fg='green')
                else:
                    label1.configure(text='something wrong')

            title1.destroy()
            add_emp.destroy()
            add_chef.destroy()
            backk.destroy()

            title2 = Label(root, text='Ajouter employe', bg='white', font=['serif',18])
            title2.place(x=80, y=10)

            label1 = Label(root, width=20, bg='white', fg='red')
            label1.place(x=80, y=280)
            
            nom_label = Label(root, text='nom : ', fg='black', bg='white')
            nom_label.place(x=20, y=60)
            nom = Entry(root, text='nom', width=24, bg='#95CAFE')
            nom.place(x=100, y=60)

            prenom_label = Label(root, text='prenom : ', fg='black', bg='white')
            prenom_label.place(x=20, y=100)
            prenom = Entry(root, text='prenom', width=24, bg='#95CAFE')
            prenom.place(x=100, y=100)
            
            datenaissance_label = Label(root, text='date naiss : ', fg='black', bg='white')
            datenaissance_label.place(x=20, y=140)
            datenaissance = Entry(root, text='date', width=24, bg='#95CAFE')
            datenaissance.place(x=100, y=140)

            departement_label = Label(root, text='departement : ', fg='black', bg='white')
            departement_label.place(x=20, y=180)
            departement = Entry(root, text='departement', width=24, bg='#95CAFE')
            departement.place(x=100, y=180)

            hasattr_label = Label(root, text='heur travail : ', fg='black', bg='white')
            hasattr_label.place(x=20, y=220)
            heurstravail = Entry(root, text='heurs travail', width=24, bg='#95CAFE')
            heurstravail.place(x=100, y=220)

            salaire_label = Label(root, text='salaire : ', fg='black', bg='white')
            salaire_label.place(x=20, y=260)
            salaire = Entry(root, text='salaire', width=24, bg='#95CAFE')
            salaire.place(x=100, y=260)
            add = Button(root, 
                text='add and save',
                height=2,
                bg='#5189DC', 
                fg='black',
                width=20, 
                command=addempl)
            add.place(x=80, y=300)
            backkem = Button(root, 
                text='back', 
                height=2,
                bg='#5189DC', 
                fg='black',
                width=20,
                command=backkemp)
            backkem.place(x=80, y=360)
        def chef():
            def backkchef():
                title2.destroy()
                nom_label.destroy()
                prenom_label.destroy()
                datenaissance_label.destroy()
                departement_label.destroy()
                hasattr_label.destroy()
                prime_label.destroy()
                salaire_label.destroy()

                nom.destroy()
                prenom.destroy()
                datenaissance.destroy()
                departement.destroy()
                heurstravail.destroy()
                prime.destroy()
                salaire.destroy()
                add.destroy()
                backkch.destroy()
                label1.destroy()
                ajou()
            def addchef():
                f = True
                n = nom.get()
                if not bool(re.match(r'^[a-zA-Z]{4,8}$',n)):
                    messagebox.showinfo("error","nom invalide")
                    f = False
                    
                p = prenom.get()
                if not bool(re.match(r'^[a-zA-Z]{4,8}$',p)):
                    messagebox.showinfo("error","prenom invalide")
                    f = False

                d = datenaissance.get()
                if not bool(re.match(r'^[0-9]{2}+/[0-9]{2}+/[0-9]{4}$',d)):
                    messagebox.showinfo("error","date invalide")
                    f = False

                dp = departement.get()
                if not bool(re.match(r'^[a-zA-Z]{4,8}$',dp)):
                    messagebox.showinfo("error","departement invalide")
                    f = False

                h = heurstravail.get()
                if not bool(re.match(r'^[0-9]{0,}$',h)):
                    messagebox.showinfo("error","heur invalide")
                    f = False

                pr = prime.get()
                if not bool(re.match(r'^[0-9]{0,}$',pr)):
                    messagebox.showinfo("error","prime invalide")
                    f = False

                s = salaire.get()
                if not bool(re.match(r'^[0-9]{0,}$',s)):
                    messagebox.showinfo("error","salaire invalide")
                    f = False

                if f == True:
                    ch1 = Chef(n, p, d, dp, h, pr, s)
                    Chef.save_csv_chefs()
                    label1.configure(text='data saved', fg='green')
                else:
                    label1.configure(text='something wrong')

            title1.destroy()
            add_emp.destroy()
            add_chef.destroy()
            backk.destroy()

            title2 = Label(root, text='Ajouter employe', bg='white', font=['serif',18])
            title2.place(x=80, y=10)

            label1 = Label(root, width=20, bg='white', fg='red')
            label1.place(x=80, y=280)

            nom_label = Label(root, text='nom : ', fg='black', bg='white')
            nom_label.place(x=20, y=60)
            nom = Entry(root, text='nom', width=24, bg='#95CAFE')
            nom.place(x=100, y=60)

            prenom_label = Label(root, text='prenom : ', fg='black', bg='white')
            prenom_label.place(x=20, y=100)
            prenom = Entry(root, text='prenom', width=24, bg='#95CAFE')
            prenom.place(x=100, y=100)
            
            datenaissance_label = Label(root, text='date naiss : ', fg='black', bg='white')
            datenaissance_label.place(x=20, y=140)
            datenaissance = Entry(root, text='date', width=24, bg='#95CAFE')
            datenaissance.place(x=100, y=140)

            departement_label = Label(root, text='departement : ', fg='black', bg='white')
            departement_label.place(x=20, y=180)
            departement = Entry(root, text='departement', width=24, bg='#95CAFE')
            departement.place(x=100, y=180)

            hasattr_label = Label(root, text='heur travail : ', fg='black', bg='white')
            hasattr_label.place(x=20, y=220)
            heurstravail = Entry(root, text='heurs travail', width=24, bg='#95CAFE')
            heurstravail.place(x=100, y=220)


            prime_label = Label(root, text='prime : ', fg='black', bg='white')
            prime_label.place(x=20, y=260)
            prime = Entry(root, text='prime', width=24, bg='#95CAFE')
            prime.place(x=100, y=260)

            salaire_label = Label(root, text='salaire : ', fg='black', bg='white')
            salaire_label.place(x=20, y=300)
            salaire = Entry(root, text='salaire', width=24, bg='#95CAFE')
            salaire.place(x=100, y=300)

            add = Button(root, text='add and save',
                height=2,
                bg='#5189DC', 
                fg='black',
                width=20, command=addchef)
            add.place(x=80, y=340)
            backkch = Button(root, 
                text='back', 
                height=2,
                bg='#5189DC', 
                fg='black',
                width=20,
                command=backkchef)
            backkch.place(x=80, y=400)
            

        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()

        title1 = Label(root, text='Ajouter', bg='white', font=['serif',18])
        title1.place(x=115, y=30)

        add_emp = Button(root, 
                text='employe',
                height=2,
                bg='#5189DC', 
                fg='black', 
                width=20, 
                command=empl)
        add_emp.place(x=80, y=100)
        add_chef = Button(root, 
                text='chef',
                height=2,
                bg='#5189DC', 
                fg='black', 
                width=20, 
                command=chef)
        add_chef.place(x=80, y=180)
        backk = Button(root, 
                text='back', 
                height=2,
                bg='#5189DC', 
                fg='black',
                width=20, 
                command=back)
        backk.place(x=80, y=260)

#afficher par deparetement
    def affich_depar():
        def back():
            dep_name.destroy()
            title1.destroy()
            label_dep.destroy()
            aff_dep.destroy()
            back_dep.destroy()
            tree.destroy()
            tree2.destroy()
            app()

        def aff_par_dep():
            iid = label_dep.get().strip()
            with open('employes.csv', 'r') as file:
                filelines = file.readlines()
                for i in filelines[1:]:
                    fields = i.strip().split('\t')
                    if fields[4].strip() == iid:
                        #emp_info = f"ID: {fields[0]} | Name: {fields[1]} {fields[2]} | Age: {fields[3]} | Department: {fields[4]} | Hours: {fields[5]} | Salary: {fields[6]}"
                        tree.insert('', 'end', values=(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6]))
                    else:
                        continue
            with open('chefs.csv', 'r') as fil:
                lines = fil.readlines()
                for i in lines[1:]:
                    field = i.strip().split('\t')
                    if field[4].strip() == iid:
                        #emp_info = f"ID: {fields[0]} | Name: {fields[1]} {fields[2]} | Age: {fields[3]} | Department: {fields[4]} | Hours: {fields[5]} | Salary: {fields[6]}"
                        tree2.insert('', 'end', values=(field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7]))
                    else:
                        continue   
            
        title.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()

        title1 = Label(root, text='Afficher par departement', bg='white', font=['serif',18])
        title1.place(x=250, y=30)

        dep_name = Label(root, text='departement', width=24, bg='white')
        dep_name.place(x=30, y=100)

        label_dep = Entry(root, width=24, bg='#95CAFE')
        label_dep.place(x=40, y=130)

        aff_dep = Button(root, width=20, text="afficher", 
                height=2,
                bg='#5189DC', 
                fg='black', command=aff_par_dep)
        aff_dep.place(x=40, y=180)

        back_dep = Button(root, text='back', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black', command=back)
        back_dep.place(x=40, y=240)

        #tree chef
        tree2 = ttk.Treeview(root,height=2, columns=("id", "name", "prenom", "age", "deparetement", "hoursTR", "prime", "salaire"), show="headings")
        tree2.heading('id', text='ID')
        tree2.heading('name', text='Nom')
        tree2.heading('prenom', text='prenom')
        tree2.heading('age', text='age')
        tree2.heading('deparetement', text='depar')
        tree2.heading('hoursTR', text='hoursTR')
        tree2.heading('prime', text='prime')
        tree2.heading('salaire', text='salaire')
        tree2.column("id", width=10) 
        tree2.column("name", width=50)     
        tree2.column("prenom", width=50)
        tree2.column("age", width=80)
        tree2.column("deparetement", width=100)
        tree2.column("hoursTR", width=80)
        tree2.column("prime", width=80)
        tree2.column("salaire", width=80)
        tree2.place(x=260, y=100)

        #tree employe
        tree = ttk.Treeview(root, columns=("id", "name", "prenom", "age", "deparetement", "hoursTR", "salaire"), show="headings")
        tree.heading('id', text='ID')
        tree.heading('name', text='Nom')
        tree.heading('prenom', text='prenom')
        tree.heading('age', text='age')
        tree.heading('deparetement', text='depar')
        tree.heading('hoursTR', text='hoursTR')
        tree.heading('salaire', text='salaire')
        tree.column("id", width=20) 
        tree.column("name", width=60)     
        tree.column("prenom", width=60)
        tree.column("age", width=90)
        tree.column("deparetement", width=110)
        tree.column("hoursTR", width=95)
        tree.column("salaire", width=95)
        tree.place(x=260, y=180)

#calculer salaire
    def calculer():
        def back():
            title1.destroy()
            eemp.destroy()
            cchef.destroy()
            backk.destroy()
            app()
        def claculer_sal_emp():
            def back():
                employe_id.destroy()
                title2.destroy()
                idd.destroy()
                aff.destroy()
                sall.destroy()
                back_dep.destroy()
                calculer()

            def calcul():
                id = idd.get().strip()
                with open('employes.csv', 'r') as fil:
                    lines = fil.readlines()
                    for i in lines[1:]:
                        field = i.strip().split('\t')
                        if field[0].strip() == id:
                            if int(field[5]) > 90:
                                sall.configure(text=f" {int(field[6]) + ((int(field[5]) - 90) * (int(field[6]) // 90))}")
                            else:
                                sall.configure(text=f"{int(field[6])}")

            title1.destroy()                
            eemp.destroy()
            cchef.destroy()
            backk.destroy()
        
            title2 = Label(root, text='calculer salaire \n employe', bg='white', font=['serif',18])
            title2.place(x=80, y=30)

            employe_id = Label(root, text='employe id', bg='white')
            employe_id.place(x=120, y=115)

            idd = Entry(root, 
                        width=24, 
                        bg='#95CAFE')
            idd.place(x=80, y=140)

            aff = Button(root, width=20, text="calculer", 
                height=2,
                bg='#5189DC', 
                fg='black', 
                command=calcul)
            aff.place(x=80, y=180)

            back_dep = Button(root, text='back', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black', 
                command=back)
            back_dep.place(x=80, y=240)

            sall = Label(root, width=20, height=5, bg='#95CAFE')
            sall.place(x=80, y=320)

        def claculer_sal_chf():
            def back():
                title2.destroy()
                employe_id.destroy()
                idd.destroy()
                aff.destroy()
                sall.destroy()
                back_dep.destroy()
                calculer()

            def calcul2():
                id = idd.get().strip()
                with open('chefs.csv', 'r') as fil:
                    lines = fil.readlines()
                    for i in lines[1:]:
                        field = i.strip().split('\t')
                        if field[0].strip() == id:
                            if int(field[5]) > 90:
                                sall.configure(text=f" {int(field[7]) + ((int(field[5]) - 90) * (int(field[7]) // 90)) + int(field[6])}")
                            else:
                                sall.configure(text=f"{int(field[7]) + int(field[6])}")
                            
            title1.destroy()                
            eemp.destroy()
            cchef.destroy()
            backk.destroy()
        
            title2 = Label(root, text='calculer salaire \n chef', bg='white', font=['serif',18])
            title2.place(x=80, y=30)

            employe_id = Label(root, text='chef id', bg='white')
            employe_id.place(x=125, y=115)

            idd = Entry(root, width=24, bg='#95CAFE')
            idd.place(x=80, y=140)

            aff = Button(root, width=20, text="calculer", 
                height=2,
                bg='#5189DC', 
                fg='black', 
                command=calcul2)
            aff.place(x=80, y=180)

            back_dep = Button(root, text='back', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black', 
                command=back)
            back_dep.place(x=80, y=220)

            sall = Label(root, width=20, height=5, bg='#95CAFE')
            sall.place(x=80, y=320)
            

        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()

        title1 = Label(root, text='calculer salaire', bg='white', font=['serif',18])
        title1.place(x=75, y=30)

        eemp = Button(root, 
                text='employe', 
                width=20,
                command=claculer_sal_emp,
                height=2,
                bg='#5189DC', 
                fg='black')
        eemp.place(x=80, y=100)
        cchef = Button(root, 
                text='chef', 
                width=20,
                command=claculer_sal_chf,
                height=2,
                bg='#5189DC', 
                fg='black')
        cchef.place(x=80, y=180)

        backk = Button(root, 
                text='back', 
                width=20,
                command=back,
                height=2,
                bg='#5189DC', 
                fg='black')
        backk.place(x=80, y=260)

#calculer slaire totale
    def calculer_totale():
        def back():
            title2.destroy()
            call_lab.destroy()
            call.destroy()
            backk.destroy()
            app()
        def claculer_tt():
            total = 0
            with open('employes.csv', 'r') as fil:
                lines = fil.readlines()
                for i in lines[1:]:
                    field = i.strip().split('\t')
                    total += int(field[6])
            call_lab.config(text=f"salaire tatle : {total} $")
                    

        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        button5.destroy()
        button6.destroy()

        title2 = Label(root, text='calculer totale', bg='white', font=['serif',18])
        title2.place(x=80, y=50)

        call = Button(root, 
                text='calculer', 
                width=20,
                height=2,
                bg='#5189DC', 
                fg='black',
                command=claculer_tt)
        call.place(x=80, y=160)

        call_lab = Label(root,
                width=20,
                height=2,
                bg='#95CAFE', 
                fg='black')
        call_lab.place(x=80, y=100)

        backk = Button(root, 
                text='back', 
                width=20,
                command=back,
                height=2,
                bg='#5189DC', 
                fg='black')
        backk.place(x=80, y=220)

#main menu       
    button1 = Button(root,
                border=0, 
                text='afficher', 
                width=20, 
                command=aff, 
                height=2,
                bg='#5189DC', 
                fg='black')
    button1.place(x=80, y=70)
    button2 = Button(root,
                border=0, text='ajouter', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black',
                command=ajou)
    button2.place(x=80, y=120)
    button3 = Button(root,
                border=0, text='afficher par departement', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black', command=affich_depar)
    button3.place(x=80, y=170)
    button4 = Button(root,
                border=0, text='calculer salaire', 
                height=2,
                width=20,
                bg='#5189DC', 
                fg='black', command=calculer)
    button4.place(x=80, y=220)
    button5 = Button(root,
                border=0, text='calculer totale', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black', command=calculer_totale)
    button5.place(x=80, y=270)
    button6 = Button(root,
                border=0, text='exit', width=20, 
                height=2,
                bg='#5189DC', 
                fg='black', command=exit)
    button6.place(x=80, y=320)
    
    image2 = Image.open("image1.jpg").resize((600,450))
    image322 = ImageTk.PhotoImage(image2)

    lab2 = Label(root, image=image322, border=0)
    lab2.place(x=230, y=50)

    title = Label(root, text='COMPANY MANAGEMENT', bg='white', font=['fantasy',28])
    title.place(x=300, y=20)
app()
root.mainloop()