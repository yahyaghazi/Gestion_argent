import tkinter as tk
from GestionnaireFinancier import GestionnaireFinancier
from IntegrationBancaire import IntegrationBancaireUI

def test_integration_bancaire():
    # Interface simple pour tester l'intégration bancaire
    root = tk.Tk()
    root.title("Test d'intégration bancaire")
    root.geometry("400x300")
    
    # Créer une instance du gestionnaire financier
    gestionnaire = GestionnaireFinancier()
    
    # Bouton pour ouvrir l'interface d'intégration bancaire
    def ouvrir_integration():
        ui = IntegrationBancaireUI(root, gestionnaire)
        ui.afficher_menu_integration()
    
    label = tk.Label(root, text="Test de l'intégration bancaire", font=("Arial", 14))
    label.pack(pady=20)
    
    explications = tk.Label(root, text="Cette interface permet de tester l'intégration\n"
                              "avec les APIs bancaires pour synchroniser\n"
                              "automatiquement les transactions financières.")
    explications.pack(pady=10)
    
    bouton = tk.Button(root, text="Ouvrir l'intégration bancaire", 
                     command=ouvrir_integration, bg="#ffccff", padx=10, pady=5)
    bouton.pack(pady=20)
    
    # Bouton pour fermer l'application
    tk.Button(root, text="Quitter", command=root.destroy, padx=10, pady=5).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_integration_bancaire()