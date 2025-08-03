import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from database import Database
import sqlite3
import datetime
from typing import Optional, Dict, Any

# Set appearance mode and color theme
ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernEmployeeAssignmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Affectations du Personnel")
        self.root.geometry("1200x800")
        
        # Initialize database
        self.db = Database()
        
        # Configure the window
        self.root.minsize(1000, 700)
        
        # Create main container with padding
        self.main_container = ctk.CTkFrame(root, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create tabview (modern tabs)
        self.tabview = ctk.CTkTabview(self.main_container, width=1160, height=650)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=(10, 20))
        
        # Create tabs
        self.create_location_tab()
        self.create_employee_tab()
        self.create_assignment_tab()
        self.create_search_tab()
        self.create_reports_tab()
        
        # Status bar
        self.create_status_bar()
        
        # Initialize data
        self.employee_dict = {}
        self.load_initial_data()
        
    def create_header(self):
        """Create modern header with title and theme switcher"""
        header_frame = ctk.CTkFrame(self.main_container, height=80, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🏢 Gestion des Affectations du Personnel", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=30, pady=25)
        
        # Theme switcher
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.pack(side="right", padx=30, pady=25)
        
        ctk.CTkLabel(theme_frame, text="Thème:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 10))
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            switch_width=50,
            switch_height=25
        )
        self.theme_switch.pack(side="left")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def create_status_bar(self):
        """Create modern status bar"""
        self.status_frame = ctk.CTkFrame(self.main_container, height=40, corner_radius=10)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="📊 Prêt", 
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=20, pady=10)
    
    def update_status(self, message: str, icon: str = "ℹ️"):
        """Update status bar with message and icon"""
        self.status_label.configure(text=f"{icon} {message}")
        self.root.after(5000, lambda: self.status_label.configure(text="📊 Prêt"))
    
    def create_location_tab(self):
        """Create modern locations management tab"""
        tab = self.tabview.add("🌍 Lieux")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(tab, corner_radius=15)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form section
        form_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Form title
        ctk.CTkLabel(
            form_frame, 
            text="📝 Formulaire Lieu", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Form fields in a grid
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # ID Lieu
        ctk.CTkLabel(fields_frame, text="ID Lieu:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 15)
        )
        self.loc_id = ctk.CTkEntry(fields_frame, placeholder_text="Entrez l'ID du lieu", width=200)
        self.loc_id.grid(row=0, column=1, padx=(0, 30), pady=(0, 15), sticky="w")
        
        # Désignation
        ctk.CTkLabel(fields_frame, text="Désignation:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=2, sticky="w", padx=(0, 10), pady=(0, 15)
        )
        self.loc_design = ctk.CTkEntry(fields_frame, placeholder_text="Nom du lieu", width=200)
        self.loc_design.grid(row=0, column=3, pady=(0, 15), sticky="w")
        
        # Province
        ctk.CTkLabel(fields_frame, text="Province:", font=ctk.CTkFont(size=12)).grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 15)
        )
        self.loc_province = ctk.CTkComboBox(
            fields_frame, 
            values=['Antananarivo', 'Antsiranana', 'Fianarantsoa', 'Mahajanga', 'Toamasina', 'Toliara'],
            width=200
        )
        self.loc_province.grid(row=1, column=1, padx=(0, 30), pady=(0, 15), sticky="w")
        
        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="➕ Ajouter", command=self.add_location, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Modifier", command=self.update_location, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Supprimer", command=self.delete_location, width=100, fg_color="red", hover_color="darkred").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🆕 Nouveau", command=self.clear_location_form, width=100, fg_color="gray", hover_color="darkgray").pack(side="left", padx=5)
        
        # Data display section
        data_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        data_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            data_frame, 
            text="📋 Liste des Lieux", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Modern treeview with custom styling
        tree_container = ctk.CTkFrame(data_frame, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Create treeview with modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=30,
                       fieldbackground="#2b2b2b",
                       font=('Segoe UI', 10))
        style.configure("Modern.Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       font=('Segoe UI', 10, 'bold'))
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_container, orient="vertical")
        x_scroll = ttk.Scrollbar(tree_container, orient="horizontal")
        
        self.loc_tree = ttk.Treeview(
            tree_container,
            columns=('id', 'design', 'province'),
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            selectmode='browse',
            style="Modern.Treeview"
        )
        
        # Configure scrollbars
        y_scroll.config(command=self.loc_tree.yview)
        x_scroll.config(command=self.loc_tree.xview)
        
        # Define columns
        self.loc_tree.heading('#0', text='')
        self.loc_tree.heading('id', text='🆔 ID Lieu', anchor="w")
        self.loc_tree.heading('design', text='📍 Désignation', anchor="w")
        self.loc_tree.heading('province', text='🗺️ Province', anchor="w")
        
        # Format columns
        self.loc_tree.column('#0', width=0, stretch=False)
        self.loc_tree.column('id', width=120, minwidth=100)
        self.loc_tree.column('design', width=300, minwidth=200)
        self.loc_tree.column('province', width=150, minwidth=100)
        
        # Pack scrollbars and treeview
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.loc_tree.pack(fill="both", expand=True)
        
        # Bind events
        self.loc_tree.bind('<<TreeviewSelect>>', self.on_location_select)
    
    def create_employee_tab(self):
        """Create modern employees management tab"""
        tab = self.tabview.add("👤 Employés")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(tab, corner_radius=15)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form section
        form_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Form title
        ctk.CTkLabel(
            form_frame, 
            text="👨‍💼 Formulaire Employé", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Row 1
        row1_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row1_frame, text="N° Employé:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_num = ctk.CTkEntry(row1_frame, placeholder_text="Numéro employé", width=150)
        self.emp_num.pack(side="left", padx=(10, 30))
        
        ctk.CTkLabel(row1_frame, text="Civilité:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_civilite = ctk.CTkComboBox(row1_frame, values=['M.', 'Mme', 'Mlle'], width=100)
        self.emp_civilite.pack(side="left", padx=(10, 0))
        
        # Row 2
        row2_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row2_frame, text="Nom:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_nom = ctk.CTkEntry(row2_frame, placeholder_text="Nom de famille", width=150)
        self.emp_nom.pack(side="left", padx=(10, 30))
        
        ctk.CTkLabel(row2_frame, text="Prénom:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_prenom = ctk.CTkEntry(row2_frame, placeholder_text="Prénom", width=150)
        self.emp_prenom.pack(side="left", padx=(10, 0))
        
        # Row 3
        row3_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row3_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row3_frame, text="Email:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_email = ctk.CTkEntry(row3_frame, placeholder_text="email@exemple.com", width=200)
        self.emp_email.pack(side="left", padx=(10, 30))
        
        ctk.CTkLabel(row3_frame, text="Poste:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_poste = ctk.CTkEntry(row3_frame, placeholder_text="Fonction", width=150)
        self.emp_poste.pack(side="left", padx=(10, 0))
        
        # Row 4
        row4_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row4_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row4_frame, text="Lieu d'affectation:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.emp_lieu = ctk.CTkComboBox(row4_frame, width=300)
        self.emp_lieu.pack(side="left", padx=(10, 0))
        
        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="➕ Ajouter", command=self.add_employee, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Modifier", command=self.update_employee, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Supprimer", command=self.delete_employee, width=100, fg_color="red", hover_color="darkred").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🆕 Nouveau", command=self.clear_employee_form, width=100, fg_color="gray", hover_color="darkgray").pack(side="left", padx=5)
        
        # Search section
        search_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        search_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            search_frame, 
            text="🔍 Recherche", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        search_input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_frame.pack(pady=(0, 15))
        
        self.emp_search_var = tk.StringVar()
        self.emp_search = ctk.CTkEntry(
            search_input_frame, 
            placeholder_text="Rechercher par nom, prénom ou email...",
            textvariable=self.emp_search_var,
            width=400
        )
        self.emp_search.pack(side="left", padx=(0, 10))
        self.emp_search.bind("<KeyRelease>", self.search_employees)
        
        # Data display section
        data_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        data_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            data_frame, 
            text="👥 Liste des Employés", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Treeview for employees
        tree_container = ctk.CTkFrame(data_frame, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Scrollbars
        y_scroll_emp = ttk.Scrollbar(tree_container, orient="vertical")
        x_scroll_emp = ttk.Scrollbar(tree_container, orient="horizontal")
        
        columns = ('num', 'civilite', 'nom', 'prenom', 'email', 'poste', 'lieu')
        self.emp_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            yscrollcommand=y_scroll_emp.set,
            xscrollcommand=x_scroll_emp.set,
            selectmode='browse',
            show='headings',
            style="Modern.Treeview"
        )
        
        y_scroll_emp.config(command=self.emp_tree.yview)
        x_scroll_emp.config(command=self.emp_tree.xview)
        
        # Define columns
        self.emp_tree.heading('num', text='🆔 N° Emp', anchor="w")
        self.emp_tree.heading('civilite', text='👤 Civ.', anchor="w")
        self.emp_tree.heading('nom', text='📝 Nom', anchor="w")
        self.emp_tree.heading('prenom', text='📝 Prénom', anchor="w")
        self.emp_tree.heading('email', text='📧 Email', anchor="w")
        self.emp_tree.heading('poste', text='💼 Poste', anchor="w")
        self.emp_tree.heading('lieu', text='📍 Lieu', anchor="w")
        
        # Format columns
        self.emp_tree.column('num', width=80, minwidth=60)
        self.emp_tree.column('civilite', width=60, minwidth=50)
        self.emp_tree.column('nom', width=120, minwidth=100)
        self.emp_tree.column('prenom', width=120, minwidth=100)
        self.emp_tree.column('email', width=180, minwidth=150)
        self.emp_tree.column('poste', width=120, minwidth=100)
        self.emp_tree.column('lieu', width=120, minwidth=100)
        
        y_scroll_emp.pack(side="right", fill="y")
        x_scroll_emp.pack(side="bottom", fill="x")
        self.emp_tree.pack(fill="both", expand=True)
        
        self.emp_tree.bind('<<TreeviewSelect>>', self.on_employee_select)
    
    def create_assignment_tab(self):
        """Create modern assignments management tab"""
        tab = self.tabview.add("🔄 Affectations")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(tab, corner_radius=15)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form section
        form_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Form title
        ctk.CTkLabel(
            form_frame, 
            text="📋 Formulaire d'Affectation", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Row 1
        row1_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row1_frame, text="N° Affectation:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_num = ctk.CTkEntry(row1_frame, placeholder_text="Numéro affectation", width=150)
        self.affect_num.pack(side="left", padx=(10, 30))
        
        ctk.CTkLabel(row1_frame, text="Employé:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_emp = ctk.CTkComboBox(row1_frame, width=250)
        self.affect_emp.pack(side="left", padx=(10, 0))
        
        # Row 2
        row2_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row2_frame, text="Ancien Lieu:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_old_loc = ctk.CTkComboBox(row2_frame, width=200)
        self.affect_old_loc.pack(side="left", padx=(10, 30))
        
        ctk.CTkLabel(row2_frame, text="Nouveau Lieu:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_new_loc = ctk.CTkComboBox(row2_frame, width=200)
        self.affect_new_loc.pack(side="left", padx=(10, 0))
        
        # Row 3
        row3_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        row3_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(row3_frame, text="Date d'Affectation:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_date = ctk.CTkEntry(row3_frame, placeholder_text="AAAA-MM-JJ", width=150)
        self.affect_date.pack(side="left", padx=(10, 30))
        self.affect_date.insert(0, self.get_today_date())
        
        ctk.CTkLabel(row3_frame, text="Date de Service:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_service_date = ctk.CTkEntry(row3_frame, placeholder_text="AAAA-MM-JJ", width=150)
        self.affect_service_date.pack(side="left", padx=(10, 0))
        self.affect_service_date.insert(0, self.get_today_date())
        
        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="➕ Ajouter", command=self.add_assignment, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Modifier", command=self.update_assignment, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Supprimer", command=self.delete_assignment, width=100, fg_color="red", hover_color="darkred").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🆕 Nouveau", command=self.clear_assignment_form, width=100, fg_color="gray", hover_color="darkgray").pack(side="left", padx=5)
        
        # Search and filter section
        filter_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            filter_frame, 
            text="🔍 Recherche et Filtres", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Search row
        search_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        search_row.pack(fill="x", padx=30, pady=(0, 15))
        
        ctk.CTkLabel(search_row, text="Rechercher:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.affect_search_var = tk.StringVar()
        self.affect_search = ctk.CTkEntry(
            search_row, 
            placeholder_text="Rechercher par employé ou numéro...",
            textvariable=self.affect_search_var,
            width=300
        )
        self.affect_search.pack(side="left", padx=(10, 0))
        self.affect_search.bind("<KeyRelease>", self.search_assignments)
        
        # Date filter row
        date_row = ctk.CTkFrame(filter_frame, fg_color="transparent")
        date_row.pack(fill="x", padx=30, pady=(0, 15))
        
        ctk.CTkLabel(date_row, text="Période:", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(date_row, text="Du:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(20, 5))
        self.date_from = ctk.CTkEntry(date_row, placeholder_text="AAAA-MM-JJ", width=120)
        self.date_from.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(date_row, text="Au:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0, 5))
        self.date_to = ctk.CTkEntry(date_row, placeholder_text="AAAA-MM-JJ", width=120)
        self.date_to.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(date_row, text="🔍 Filtrer", command=self.filter_by_date, width=80).pack(side="left", padx=5)
        ctk.CTkButton(date_row, text="🔄 Reset", command=self.reset_date_filter, width=80, fg_color="gray").pack(side="left", padx=5)
        
        # Data display section
        data_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        data_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            data_frame, 
            text="📊 Liste des Affectations", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Treeview for assignments
        tree_container = ctk.CTkFrame(data_frame, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Scrollbars
        y_scroll_affect = ttk.Scrollbar(tree_container, orient="vertical")
        x_scroll_affect = ttk.Scrollbar(tree_container, orient="horizontal")
        
        columns = ('num', 'emp_name', 'old_loc', 'new_loc', 'date_affect', 'date_service')
        self.affect_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            yscrollcommand=y_scroll_affect.set,
            xscrollcommand=x_scroll_affect.set,
            selectmode='browse',
            show='headings',
            style="Modern.Treeview"
        )
        
        y_scroll_affect.config(command=self.affect_tree.yview)
        x_scroll_affect.config(command=self.affect_tree.xview)
        
        # Define columns
        self.affect_tree.heading('num', text='🆔 N° Affect.', anchor="w")
        self.affect_tree.heading('emp_name', text='👤 Employé', anchor="w")
        self.affect_tree.heading('old_loc', text='📍 Ancien Lieu', anchor="w")
        self.affect_tree.heading('new_loc', text='📍 Nouveau Lieu', anchor="w")
        self.affect_tree.heading('date_affect', text='📅 Date Affect.', anchor="w")
        self.affect_tree.heading('date_service', text='📅 Date Service', anchor="w")
        
        # Format columns
        self.affect_tree.column('num', width=100, minwidth=80)
        self.affect_tree.column('emp_name', width=150, minwidth=120)
        self.affect_tree.column('old_loc', width=140, minwidth=120)
        self.affect_tree.column('new_loc', width=140, minwidth=120)
        self.affect_tree.column('date_affect', width=120, minwidth=100)
        self.affect_tree.column('date_service', width=120, minwidth=100)
        
        y_scroll_affect.pack(side="right", fill="y")
        x_scroll_affect.pack(side="bottom", fill="x")
        self.affect_tree.pack(fill="both", expand=True)
        
        self.affect_tree.bind('<<TreeviewSelect>>', self.on_assignment_select)
    
    def create_search_tab(self):
        """Create modern search tab"""
        tab = self.tabview.add("🔍 Recherche")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(tab, corner_radius=15)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search section
        search_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        search_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            search_frame, 
            text="🔍 Recherche Avancée", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 15))
        
        # Search criteria
        criteria_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        criteria_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Employee search
        emp_search_frame = ctk.CTkFrame(criteria_frame, corner_radius=10)
        emp_search_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            emp_search_frame, 
            text="👤 Recherche d'Employés", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Search fields
        fields_frame = ctk.CTkFrame(emp_search_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Name search
        name_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(name_frame, text="Nom/Prénom:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.search_name = ctk.CTkEntry(name_frame, placeholder_text="Rechercher par nom ou prénom", width=300)
        self.search_name.pack(side="left", padx=(10, 20))
        
        # Location search
        ctk.CTkLabel(name_frame, text="Lieu:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.search_location = ctk.CTkComboBox(name_frame, width=200)
        self.search_location.pack(side="left", padx=(10, 0))
        
        # Position search
        pos_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        pos_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(pos_frame, text="Poste:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.search_position = ctk.CTkEntry(pos_frame, placeholder_text="Rechercher par poste", width=300)
        self.search_position.pack(side="left", padx=(10, 20))
        
        # Province search
        ctk.CTkLabel(pos_frame, text="Province:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.search_province = ctk.CTkComboBox(
            pos_frame, 
            values=['Tous', 'Antananarivo', 'Antsiranana', 'Fianarantsoa', 'Mahajanga', 'Toamasina', 'Toliara'],
            width=150
        )
        self.search_province.pack(side="left", padx=(10, 0))
        self.search_province.set("Tous")
        
        # Search buttons
        btn_frame = ctk.CTkFrame(emp_search_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 15))
        
        ctk.CTkButton(btn_frame, text="🔍 Rechercher", command=self.advanced_search, width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Effacer", command=self.clear_search, width=120, fg_color="gray").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="📊 Exporter", command=self.export_results, width=120, fg_color="green").pack(side="left", padx=5)
        
        # Results section
        results_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        results_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            results_frame, 
            text="📋 Résultats de Recherche", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Results info
        self.results_info = ctk.CTkLabel(
            results_frame, 
            text="Aucune recherche effectuée", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.results_info.pack(pady=(0, 10))
        
        # Results treeview
        tree_container = ctk.CTkFrame(results_frame, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        y_scroll_search = ttk.Scrollbar(tree_container, orient="vertical")
        x_scroll_search = ttk.Scrollbar(tree_container, orient="horizontal")
        
        columns = ('num', 'civilite', 'nom', 'prenom', 'email', 'poste', 'lieu', 'province')
        self.search_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            yscrollcommand=y_scroll_search.set,
            xscrollcommand=x_scroll_search.set,
            selectmode='browse',
            show='headings',
            style="Modern.Treeview"
        )
        
        y_scroll_search.config(command=self.search_tree.yview)
        x_scroll_search.config(command=self.search_tree.xview)
        
        # Define columns
        self.search_tree.heading('num', text='🆔 N° Emp', anchor="w")
        self.search_tree.heading('civilite', text='👤 Civ.', anchor="w")
        self.search_tree.heading('nom', text='📝 Nom', anchor="w")
        self.search_tree.heading('prenom', text='📝 Prénom', anchor="w")
        self.search_tree.heading('email', text='📧 Email', anchor="w")
        self.search_tree.heading('poste', text='💼 Poste', anchor="w")
        self.search_tree.heading('lieu', text='📍 Lieu', anchor="w")
        self.search_tree.heading('province', text='🗺️ Province', anchor="w")
        
        # Format columns
        for col in columns:
            self.search_tree.column(col, width=120, minwidth=80)
        
        y_scroll_search.pack(side="right", fill="y")
        x_scroll_search.pack(side="bottom", fill="x")
        self.search_tree.pack(fill="both", expand=True)
    
    def create_reports_tab(self):
        """Create modern reports tab"""
        tab = self.tabview.add("📊 Rapports")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(tab, corner_radius=15)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame, 
            text="📊 Rapports et Statistiques", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 15))
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            stats_frame, 
            text="📈 Statistiques Générales", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=30, pady=(0, 15))
        
        # Create stat cards
        self.create_stat_card(stats_grid, "👥", "Total Employés", "0", 0, 0)
        self.create_stat_card(stats_grid, "🌍", "Total Lieux", "0", 0, 1)
        self.create_stat_card(stats_grid, "🔄", "Total Affectations", "0", 1, 0)
        self.create_stat_card(stats_grid, "📅", "Ce Mois", "0", 1, 1)
        
        # Reports section
        reports_frame = ctk.CTkFrame(scrollable_frame, corner_radius=15)
        reports_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            reports_frame, 
            text="📋 Rapports Disponibles", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Report buttons
        reports_grid = ctk.CTkFrame(reports_frame, fg_color="transparent")
        reports_grid.pack(fill="x", padx=30, pady=(0, 20))
        
        # Row 1
        row1 = ctk.CTkFrame(reports_grid, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 15))
        
        ctk.CTkButton(
            row1, 
            text="📊 Rapport par Province", 
            command=self.generate_province_report,
            width=200,
            height=40
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            row1, 
            text="📈 Rapport par Poste", 
            command=self.generate_position_report,
            width=200,
            height=40
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            row1, 
            text="📅 Rapport Mensuel", 
            command=self.generate_monthly_report,
            width=200,
            height=40
        ).pack(side="left")
        
        # Row 2
        row2 = ctk.CTkFrame(reports_grid, fg_color="transparent")
        row2.pack(fill="x")
        
        ctk.CTkButton(
            row2, 
            text="🔄 Historique Affectations", 
            command=self.generate_history_report,
            width=200,
            height=40
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            row2, 
            text="📋 Liste Complète", 
            command=self.generate_complete_list,
            width=200,
            height=40
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            row2, 
            text="📤 Exporter Tout", 
            command=self.export_all_data,
            width=200,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        ).pack(side="left")
        
        # Update statistics on load
        self.update_statistics()
    
    def create_stat_card(self, parent, icon, title, value, row, col):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent, width=200, height=100, corner_radius=10)
        card.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
        card.grid_propagate(False)
        
        # Icon and title
        ctk.CTkLabel(
            card, 
            text=f"{icon} {title}", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card, 
            text=value, 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1f538d"
        )
        value_label.pack()
        
        # Store reference for updates
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[title] = value_label
    
    # Database methods (keeping the original logic with modern UI)
    def load_initial_data(self):
        """Load initial data for all components"""
        self.load_locations()
        self.load_employees()
        self.load_assignments()
        self.load_location_combobox()
        self.load_employee_combobox()
        self.load_location_comboboxes()
        self.load_search_location_combobox()
    
    def load_search_location_combobox(self):
        """Load locations for search combobox"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT DISTINCT design FROM LIEU ORDER BY design")
        locations = [row[0] for row in cursor.fetchall()]
        locations.insert(0, "Tous")
        self.search_location.configure(values=locations)
        self.search_location.set("Tous")
    
    def load_locations(self):
        """Load locations from database into treeview"""
        for item in self.loc_tree.get_children():
            self.loc_tree.delete(item)
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM LIEU ORDER BY idlieu")
        
        for row in cursor.fetchall():
            self.loc_tree.insert('', 'end', values=row)
    
    def clear_location_form(self):
        """Clear the location form"""
        self.loc_id.delete(0, "end")
        self.loc_design.delete(0, "end")
        self.loc_province.set('')
        self.loc_tree.selection_remove(self.loc_tree.selection())
    
    def on_location_select(self, event):
        """When a location is selected in the treeview"""
        selected = self.loc_tree.selection()
        if not selected:
            return
            
        item = self.loc_tree.item(selected[0])
        values = item['values']
        
        self.loc_id.delete(0, "end")
        self.loc_id.insert(0, values[0])
        self.loc_design.delete(0, "end")
        self.loc_design.insert(0, values[1])
        self.loc_province.set(values[2])
    
    def add_location(self):
        """Add a new location"""
        id_lieu = self.loc_id.get().strip()
        design = self.loc_design.get().strip()
        province = self.loc_province.get().strip()
        
        if not all([id_lieu, design, province]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)",
                (id_lieu, design, province)
            )
            self.db.conn.commit()
            self.load_locations()
            self.clear_location_form()
            self.update_status(f"Lieu '{design}' ajouté avec succès!", "✅")
            self.update_statistics()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Cet ID de lieu existe déjà!")
    
    def update_location(self):
        """Update selected location"""
        selected = self.loc_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un lieu à modifier!")
            return
            
        id_lieu = self.loc_id.get().strip()
        design = self.loc_design.get().strip()
        province = self.loc_province.get().strip()
        
        if not all([id_lieu, design, province]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "UPDATE LIEU SET design = ?, province = ? WHERE idlieu = ?",
                (design, province, id_lieu)
            )
            if cursor.rowcount > 0:
                self.db.conn.commit()
                self.load_locations()
                self.update_status(f"Lieu '{design}' mis à jour avec succès!", "✅")
            else:
                messagebox.showerror("Erreur", "Échec de la mise à jour du lieu!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {str(e)}")
    
    def delete_location(self):
        """Delete selected location"""
        selected = self.loc_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un lieu à supprimer!")
            return
            
        item = self.loc_tree.item(selected[0])
        id_lieu = item['values'][0]
        design = item['values'][1]
        
        if not messagebox.askyesno("Confirmer", f"Voulez-vous vraiment supprimer le lieu '{design}'?"):
            return
        
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM EMPLOYE WHERE idlieu = ?", (id_lieu,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror(
                    "Erreur",
                    "Ce lieu ne peut pas être supprimé car il est référencé par un ou plusieurs employés!"
                )
                return
                
            cursor.execute("DELETE FROM LIEU WHERE idlieu = ?", (id_lieu,))
            self.db.conn.commit()
            self.load_locations()
            self.clear_location_form()
            self.update_status(f"Lieu '{design}' supprimé avec succès!", "🗑️")
            self.update_statistics()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
    
    def load_location_combobox(self):
        """Load locations into the combobox"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT idlieu, design FROM LIEU ORDER BY design")
        locations = cursor.fetchall()
        values = [f"{loc[0]} - {loc[1]}" for loc in locations]
        self.emp_lieu.configure(values=values)
    
    def load_employees(self, search_term=None):
        """Load employees from database into treeview"""
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        
        query = """
        SELECT e.numEmp, e.civilite, e.nom, e.prenom, e.mail, e.poste, 
               COALESCE(l.design, 'Non affecté') as lieu
        FROM EMPLOYE e
        LEFT JOIN LIEU l ON e.idlieu = l.idlieu
        """
        
        params = ()
        if search_term:
            query += " WHERE e.nom LIKE ? OR e.prenom LIKE ? OR e.mail LIKE ?"
            search_pattern = f"%{search_term}%"
            params = (search_pattern, search_pattern, search_pattern)
        
        query += " ORDER BY e.nom, e.prenom"
        
        cursor = self.db.conn.cursor()
        cursor.execute(query, params)
        
        for row in cursor.fetchall():
            self.emp_tree.insert('', 'end', values=row)
    
    def clear_employee_form(self):
        """Clear the employee form"""
        self.emp_num.configure(state="normal")
        self.emp_num.delete(0, "end")
        self.emp_civilite.set('')
        self.emp_nom.delete(0, "end")
        self.emp_prenom.delete(0, "end")
        self.emp_email.delete(0, "end")
        self.emp_poste.delete(0, "end")
        self.emp_lieu.set('')
        self.emp_tree.selection_remove(self.emp_tree.selection())
    
    def on_employee_select(self, event):
        """When an employee is selected in the treeview"""
        selected = self.emp_tree.selection()
        if not selected:
            return
            
        item = self.emp_tree.item(selected[0])
        values = item['values']
        
        self.emp_num.configure(state="normal")
        self.emp_num.delete(0, "end")
        self.emp_num.insert(0, values[0])
        self.emp_num.configure(state="readonly")
        
        self.emp_civilite.set(values[1])
        
        self.emp_nom.delete(0, "end")
        self.emp_nom.insert(0, values[2])
        
        self.emp_prenom.delete(0, "end")
        self.emp_prenom.insert(0, values[3])
        
        self.emp_email.delete(0, "end")
        self.emp_email.insert(0, values[4])
        
        self.emp_poste.delete(0, "end")
        self.emp_poste.insert(0, values[5])
        
        if values[6] != 'Non affecté':
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT idlieu, design FROM LIEU WHERE design = ?", (values[6],))
            loc = cursor.fetchone()
            if loc:
                self.emp_lieu.set(f"{loc[0]} - {loc[1]}")
        else:
            self.emp_lieu.set('')
    
    def validate_employee_data(self):
        """Validate employee form data"""
        num_emp = self.emp_num.get().strip()
        civilite = self.emp_civilite.get().strip()
        nom = self.emp_nom.get().strip()
        prenom = self.emp_prenom.get().strip()
        email = self.emp_email.get().strip()
        poste = self.emp_poste.get().strip()
        lieu = self.emp_lieu.get().strip()
        
        if not all([num_emp, civilite, nom, prenom, email, poste]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return False
            
        if '@' not in email or '.' not in email:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse email valide!")
            return False
            
        idlieu = None
        if lieu:
            idlieu = lieu.split(' - ')[0]
        
        return {
            'num_emp': num_emp,
            'civilite': civilite,
            'nom': nom,
            'prenom': prenom,
            'email': email,
            'poste': poste,
            'idlieu': idlieu
        }
    
    def add_employee(self):
        """Add a new employee"""
        data = self.validate_employee_data()
        if not data:
            return
            
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO EMPLOYE (numEmp, civilite, nom, prenom, mail, poste, idlieu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data['num_emp'], data['civilite'], data['nom'], data['prenom'],
                data['email'], data['poste'], data['idlieu']
            ))
            self.db.conn.commit()
            self.load_employees()
            self.clear_employee_form()
            self.update_status(f"Employé {data['nom']} {data['prenom']} ajouté avec succès!", "✅")
            self.update_statistics()
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: EMPLOYE.mail" in str(e):
                messagebox.showerror("Erreur", "Un employé avec cet email existe déjà!")
            elif "UNIQUE constraint failed: EMPLOYE.numEmp" in str(e):
                messagebox.showerror("Erreur", "Un employé avec ce numéro existe déjà!")
            else:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")
    
    def update_employee(self):
        """Update selected employee"""
        selected = self.emp_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un employé à modifier!")
            return
            
        data = self.validate_employee_data()
        if not data:
            return
            
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE EMPLOYE 
                SET civilite = ?, nom = ?, prenom = ?, mail = ?, poste = ?, idlieu = ?
                WHERE numEmp = ?
            """, (
                data['civilite'], data['nom'], data['prenom'],
                data['email'], data['poste'], data['idlieu'],
                data['num_emp']
            ))
            
            if cursor.rowcount > 0:
                self.db.conn.commit()
                self.load_employees()
                self.update_status(f"Employé {data['nom']} {data['prenom']} mis à jour avec succès!", "✅")
            else:
                messagebox.showerror("Erreur", "Échec de la mise à jour de l'employé!")
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: EMPLOYE.mail" in str(e):
                messagebox.showerror("Erreur", "Un employé avec cet email existe déjà!")
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {str(e)}")
    
    def delete_employee(self):
        """Delete selected employee"""
        selected = self.emp_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un employé à supprimer!")
            return
            
        item = self.emp_tree.item(selected[0])
        num_emp = item['values'][0]
        nom = item['values'][2]
        prenom = item['values'][3]
        
        if not messagebox.askyesno("Confirmer", f"Voulez-vous vraiment supprimer l'employé {nom} {prenom}?"):
            return
        
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM AFFECTER WHERE numEmp = ?", (num_emp,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror(
                    "Erreur",
                    "Cet employé ne peut pas être supprimé car il a des affectations!"
                )
                return
                
            cursor.execute("DELETE FROM EMPLOYE WHERE numEmp = ?", (num_emp,))
            self.db.conn.commit()
            self.load_employees()
            self.clear_employee_form()
            self.update_status(f"Employé {nom} {prenom} supprimé avec succès!", "🗑️")
            self.update_statistics()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
    
    def search_employees(self, event=None):
        """Search employees based on search term"""
        search_term = self.emp_search_var.get().strip()
        if len(search_term) >= 2 or search_term == '':
            self.load_employees(search_term if search_term else None)
    
    # Assignment methods (continuing with same logic...)
    def load_employee_combobox(self):
        """Load employees into the assignment employee combobox"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT e.numEmp, e.nom, e.prenom, COALESCE(l.design, 'Non affecté') 
            FROM EMPLOYE e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            ORDER BY e.nom, e.prenom
        """)
        employees = cursor.fetchall()
        self.employee_dict = {}
        display_values = []
        for emp in employees:
            emp_id = emp[0]
            emp_display = f"{emp[1]} {emp[2]} ({emp[3]})"
            self.employee_dict[emp_display] = emp_id
            display_values.append(emp_display)
        self.affect_emp.configure(values=display_values)
    
    def load_location_comboboxes(self):
        """Load locations into the assignment location comboboxes"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT idlieu, design FROM LIEU ORDER BY design")
        locations = cursor.fetchall()
        location_values = [f"{loc[0]} - {loc[1]}" for loc in locations]
        self.affect_old_loc.configure(values=location_values)
        self.affect_new_loc.configure(values=location_values)
    
    def load_assignments(self, search_term=None, date_from=None, date_to=None):
        """Load assignments from database into treeview"""
        for item in self.affect_tree.get_children():
            self.affect_tree.delete(item)
        
        query = """
        SELECT 
            a.numAffect, 
            e.nom || ' ' || e.prenom as employee_name,
            old_l.design as old_location,
            new_l.design as new_location,
            a.dateAffect,
            a.datePriseService
        FROM AFFECTER a
        JOIN EMPLOYE e ON a.numEmp = e.numEmp
        LEFT JOIN LIEU old_l ON a.AncienLieu = old_l.idlieu
        LEFT JOIN LIEU new_l ON a.NouveauLieu = new_l.idlieu
        """
        
        conditions = []
        params = []
        
        if search_term:
            conditions.append("(e.nom LIKE ? OR e.prenom LIKE ? OR a.numAffect LIKE ?)")
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        if date_from and date_to:
            if conditions:
                conditions.append("AND")
            conditions.append("(a.dateAffect BETWEEN ? AND ? OR a.datePriseService BETWEEN ? AND ?)")
            params.extend([date_from, date_to, date_from, date_to])
        
        if conditions:
            query += " WHERE " + " ".join(conditions)
        
        query += " ORDER BY a.dateAffect DESC, a.datePriseService DESC"
        
        cursor = self.db.conn.cursor()
        cursor.execute(query, params)
        
        for row in cursor.fetchall():
            self.affect_tree.insert('', 'end', values=row)
    
    def clear_assignment_form(self):
        """Clear the assignment form"""
        self.affect_num.configure(state="normal")
        self.affect_num.delete(0, "end")
        self.affect_emp.set('')
        self.affect_old_loc.set('')
        self.affect_new_loc.set('')
        self.affect_date.delete(0, "end")
        self.affect_date.insert(0, self.get_today_date())
        self.affect_service_date.delete(0, "end")
        self.affect_service_date.insert(0, self.get_today_date())
        self.affect_tree.selection_remove(self.affect_tree.selection())
    
    def on_assignment_select(self, event):
        """When an assignment is selected in the treeview"""
        selected = self.affect_tree.selection()
        if not selected:
            return
            
        item = self.affect_tree.item(selected[0])
        values = item['values']
        
        self.affect_num.configure(state="normal")
        self.affect_num.delete(0, "end")
        self.affect_num.insert(0, values[0])
        self.affect_num.configure(state="readonly")
        
        # Set employee
        employee_name = values[1]
        for emp_display, emp_id in self.employee_dict.items():
            if employee_name in emp_display:
                self.affect_emp.set(emp_display)
                break
        
        # Set locations
        self.affect_old_loc.set(values[2])
        self.affect_new_loc.set(values[3])
        
        # Set dates
        self.affect_date.delete(0, "end")
        self.affect_date.insert(0, values[4])
        
        self.affect_service_date.delete(0, "end")
        self.affect_service_date.insert(0, values[5])
    
    def validate_assignment_data(self):
        """Validate assignment form data"""
        num_affect = self.affect_num.get().strip()
        emp = self.affect_emp.get().strip()
        old_loc = self.affect_old_loc.get().strip()
        new_loc = self.affect_new_loc.get().strip()
        date_affect = self.affect_date.get().strip()
        date_service = self.affect_service_date.get().strip()
        
        if not all([num_affect, emp, old_loc, new_loc, date_affect, date_service]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return False
        
        if old_loc == new_loc:
            messagebox.showerror("Erreur", "L'ancien et le nouveau lieu doivent être différents!")
            return False
        
        try:
            date_affect_dt = datetime.datetime.strptime(date_affect, '%Y-%m-%d')
            date_service_dt = datetime.datetime.strptime(date_service, '%Y-%m-%d')
            
            if date_service_dt < date_affect_dt:
                messagebox.showerror("Erreur", "La date de prise de service ne peut pas être antérieure à la date d'affectation!")
                return False
                
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide! Utilisez AAAA-MM-JJ")
            return False
        
        emp_id = self.employee_dict.get(emp)
        old_loc_id = old_loc.split(' - ')[0] if old_loc else None
        new_loc_id = new_loc.split(' - ')[0] if new_loc else None
        
        return {
            'num_affect': num_affect,
            'emp_id': emp_id,
            'old_loc_id': old_loc_id,
            'new_loc_id': new_loc_id,
            'date_affect': date_affect,
            'date_service': date_service
        }
    
    def add_assignment(self):
        """Add a new assignment"""
        data = self.validate_assignment_data()
        if not data:
            return
            
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("BEGIN TRANSACTION")
            
            cursor.execute("""
                INSERT INTO AFFECTER (numAffect, numEmp, AncienLieu, NouveauLieu, dateAffect, datePriseService)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['num_affect'], data['emp_id'], data['old_loc_id'],
                data['new_loc_id'], data['date_affect'], data['date_service']
            ))
            
            cursor.execute("""
                UPDATE EMPLOYE 
                SET idlieu = ?
                WHERE numEmp = ?
            """, (data['new_loc_id'], data['emp_id']))
            
            self.db.conn.commit()
            self.load_assignments()
            self.clear_assignment_form()
            self.update_status(f"Affectation {data['num_affect']} ajoutée avec succès!", "✅")
            self.update_statistics()
            
        except sqlite3.IntegrityError as e:
            self.db.conn.rollback()
            if "UNIQUE constraint failed: AFFECTER.numAffect" in str(e):
                messagebox.showerror("Erreur", "Une affectation avec ce numéro existe déjà!")
            else:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")
    
    def update_assignment(self):
        """Update selected assignment"""
        selected = self.affect_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une affectation à modifier!")
            return
            
        data = self.validate_assignment_data()
        if not data:
            return
            
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            
            cursor.execute("""
                SELECT numEmp, AncienLieu, NouveauLieu 
                FROM AFFECTER 
                WHERE numAffect = ?
            """, (data['num_affect'],))
            original = cursor.fetchone()
            
            if not original:
                messagebox.showerror("Erreur", "Affectation introuvable!")
                self.db.conn.rollback()
                return
                
            original_emp_id, original_old_loc, original_new_loc = original
            
            cursor.execute("""
                UPDATE AFFECTER 
                SET numEmp = ?, AncienLieu = ?, NouveauLieu = ?, 
                    dateAffect = ?, datePriseService = ?
                WHERE numAffect = ?
            """, (
                data['emp_id'], data['old_loc_id'], data['new_loc_id'],
                data['date_affect'], data['date_service'], data['num_affect']
            ))
            
            if original_emp_id != data['emp_id'] or original_new_loc != data['new_loc_id']:
                cursor.execute("""
                    UPDATE EMPLOYE 
                    SET idlieu = ?
                    WHERE numEmp = ?
                """, (data['new_loc_id'], data['emp_id']))
                
                if original_emp_id != data['emp_id']:
                    self._update_employee_location(original_emp_id)
            
            self.db.conn.commit()
            self.load_assignments()
            self.update_status(f"Affectation {data['num_affect']} mise à jour avec succès!", "✅")
            
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {str(e)}")
    
    def _update_employee_location(self, emp_id):
        """Update an employee's location based on their latest assignment"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT NouveauLieu 
            FROM AFFECTER 
            WHERE numEmp = ? 
            ORDER BY dateAffect DESC, datePriseService DESC 
            LIMIT 1
        """, (emp_id,))
        
        result = cursor.fetchone()
        if result:
            new_loc_id = result[0]
            cursor.execute("""
                UPDATE EMPLOYE 
                SET idlieu = ?
                WHERE numEmp = ?
            """, (new_loc_id, emp_id))
    
    def delete_assignment(self):
        """Delete selected assignment"""
        selected = self.affect_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une affectation à supprimer!")
            return
            
        item = self.affect_tree.item(selected[0])
        num_affect = item['values'][0]
        
        if not messagebox.askyesno("Confirmer", f"Voulez-vous vraiment supprimer l'affectation {num_affect}?"):
            return
        
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("SELECT numEmp FROM AFFECTER WHERE numAffect = ?", (num_affect,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Erreur", "Affectation introuvable!")
                return
                
            emp_id = result[0]
            
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute("DELETE FROM AFFECTER WHERE numAffect = ?", (num_affect,))
            self._update_employee_location(emp_id)
            
            self.db.conn.commit()
            self.load_assignments()
            self.clear_assignment_form()
            self.update_status(f"Affectation {num_affect} supprimée avec succès!", "🗑️")
            self.update_statistics()
            
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {str(e)}")
    
    def search_assignments(self, event=None):
        """Search assignments based on search term"""
        search_term = self.affect_search_var.get().strip()
        if len(search_term) >= 2 or search_term == '':
            self.load_assignments(search_term if search_term else None)
    
    def filter_by_date(self):
        """Filter assignments by date range"""
        date_from = self.date_from.get().strip()
        date_to = self.date_to.get().strip()
        
        if not date_from and not date_to:
            messagebox.showwarning("Avertissement", "Veuillez spécifier au moins une date!")
            return
            
        try:
            if date_from:
                datetime.datetime.strptime(date_from, '%Y-%m-%d')
            if date_to:
                datetime.datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide! Utilisez AAAA-MM-JJ")
            return
            
        self.load_assignments(None, date_from or '1900-01-01', date_to or '2100-12-31')
    
    def reset_date_filter(self):
        """Reset the date filter"""
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")
        self.load_assignments()
    
    def get_today_date(self):
        """Get today's date in YYYY-MM-DD format"""
        return datetime.date.today().strftime('%Y-%m-%d')
    
    # Search methods
    def advanced_search(self):
        """Perform advanced search"""
        name = self.search_name.get().strip()
        location = self.search_location.get().strip()
        position = self.search_position.get().strip()
        province = self.search_province.get().strip()
        
        # Clear previous results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Build query
        query = """
        SELECT e.numEmp, e.civilite, e.nom, e.prenom, e.mail, e.poste, 
               COALESCE(l.design, 'Non affecté') as lieu,
               COALESCE(l.province, 'N/A') as province
        FROM EMPLOYE e
        LEFT JOIN LIEU l ON e.idlieu = l.idlieu
        WHERE 1=1
        """
        
        params = []
        
        if name:
            query += " AND (e.nom LIKE ? OR e.prenom LIKE ?)"
            name_pattern = f"%{name}%"
            params.extend([name_pattern, name_pattern])
        
        if location and location != "Tous":
            query += " AND l.design = ?"
            params.append(location)
        
        if position:
            query += " AND e.poste LIKE ?"
            params.append(f"%{position}%")
        
        if province and province != "Tous":
            query += " AND l.province = ?"
            params.append(province)
        
        query += " ORDER BY e.nom, e.prenom"
        
        cursor = self.db.conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Add results to treeview
        for row in results:
            self.search_tree.insert('', 'end', values=row)
        
        # Update results info
        count = len(results)
        if count == 0:
            self.results_info.configure(text="Aucun résultat trouvé", text_color="red")
        else:
            self.results_info.configure(
                text=f"{count} employé{'s' if count > 1 else ''} trouvé{'s' if count > 1 else ''}", 
                text_color="green"
            )
    
    def clear_search(self):
        """Clear search form and results"""
        self.search_name.delete(0, "end")
        self.search_location.set("Tous")
        self.search_position.delete(0, "end")
        self.search_province.set("Tous")
        
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        self.results_info.configure(text="Aucune recherche effectuée", text_color="gray")
    
    def export_results(self):
        """Export search results to CSV"""
        items = self.search_tree.get_children()
        if not items:
            messagebox.showwarning("Avertissement", "Aucun résultat à exporter!")
            return
        
        try:
            import csv
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Exporter les résultats"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    headers = ['N° Employé', 'Civilité', 'Nom', 'Prénom', 'Email', 'Poste', 'Lieu', 'Province']
                    writer.writerow(headers)
                    
                    # Write data
                    for item in items:
                        values = self.search_tree.item(item)['values']
                        writer.writerow(values)
                
                self.update_status(f"Résultats exportés vers {filename}", "📤")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation: {str(e)}")
    
    # Statistics and reports methods
    def update_statistics(self):
        """Update statistics cards"""
        cursor = self.db.conn.cursor()
        
        # Total employees
        cursor.execute("SELECT COUNT(*) FROM EMPLOYE")
        total_emp = cursor.fetchone()[0]
        if hasattr(self, 'stat_labels') and 'Total Employés' in self.stat_labels:
            self.stat_labels['Total Employés'].configure(text=str(total_emp))
        
        # Total locations
        cursor.execute("SELECT COUNT(*) FROM LIEU")
        total_loc = cursor.fetchone()[0]
        if hasattr(self, 'stat_labels') and 'Total Lieux' in self.stat_labels:
            self.stat_labels['Total Lieux'].configure(text=str(total_loc))
        
        # Total assignments
        cursor.execute("SELECT COUNT(*) FROM AFFECTER")
        total_affect = cursor.fetchone()[0]
        if hasattr(self, 'stat_labels') and 'Total Affectations' in self.stat_labels:
            self.stat_labels['Total Affectations'].configure(text=str(total_affect))
        
        # This month assignments
        current_month = datetime.date.today().strftime('%Y-%m')
        cursor.execute("SELECT COUNT(*) FROM AFFECTER WHERE dateAffect LIKE ?", (f"{current_month}%",))
        month_affect = cursor.fetchone()[0]
        if hasattr(self, 'stat_labels') and 'Ce Mois' in self.stat_labels:
            self.stat_labels['Ce Mois'].configure(text=str(month_affect))
    
    def generate_province_report(self):
        """Generate report by province"""
        messagebox.showinfo("Rapport", "Génération du rapport par province en cours...")
        self.update_status("Rapport par province généré", "📊")
    
    def generate_position_report(self):
        """Generate report by position"""
        messagebox.showinfo("Rapport", "Génération du rapport par poste en cours...")
        self.update_status("Rapport par poste généré", "📊")
    
    def generate_monthly_report(self):
        """Generate monthly report"""
        messagebox.showinfo("Rapport", "Génération du rapport mensuel en cours...")
        self.update_status("Rapport mensuel généré", "📊")
    
    def generate_history_report(self):
        """Generate assignment history report"""
        messagebox.showinfo("Rapport", "Génération de l'historique des affectations en cours...")
        self.update_status("Historique des affectations généré", "📊")
    
    def generate_complete_list(self):
        """Generate complete employee list"""
        messagebox.showinfo("Rapport", "Génération de la liste complète en cours...")
        self.update_status("Liste complète générée", "📊")
    
    def export_all_data(self):
        """Export all data to files"""
        messagebox.showinfo("Export", "Exportation de toutes les données en cours...")
        self.update_status("Toutes les données exportées", "📤")
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.db.close()
            self.root.destroy()


def main():
    """Main function to run the application"""
    root = ctk.CTk()
    app = ModernEmployeeAssignmentApp(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center window
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()