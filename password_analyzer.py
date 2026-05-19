"""
Password Strength Analyzer
A modern GUI application to analyze and generate strong passwords using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string


class PasswordStrengthAnalyzer:
    def __init__(self, root):
        """Initialize the Password Strength Analyzer application"""
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Set modern dark theme colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.card_color = "#313244"
        self.entry_bg = "#45475a"
        self.button_color = "#89b4fa"
        self.button_hover = "#b4befe"
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Create the main UI
        self.create_ui()
    
    def create_ui(self):
        """Create and arrange all UI elements"""
        
        # Main title
        title_label = tk.Label(
            self.root,
            text="🔐 Password Strength Analyzer",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Password input section
        input_frame = tk.Frame(main_frame, bg=self.card_color, padx=15, pady=15)
        input_frame.pack(fill="x", pady=10)
        
        tk.Label(
            input_frame,
            text="Enter Password:",
            font=("Helvetica", 11),
            bg=self.card_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        # Password entry with show/hide toggle
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            input_frame,
            textvariable=self.password_var,
            font=("Helvetica", 12),
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.accent_color,
            show="•",
            relief="flat"
        )
        self.password_entry.pack(fill="x", pady=5, ipadx=10, ipady=5)
        
        # Bind password entry to real-time analysis
        self.password_entry.bind("<KeyRelease>", self.analyze_password)
        
        # Show/Hide password button
        self.show_password = False
        self.toggle_button = tk.Button(
            input_frame,
            text="👁️ Show",
            command=self.toggle_password_visibility,
            font=("Helvetica", 9),
            bg=self.button_color,
            fg=self.bg_color,
            relief="flat",
            padx=10,
            pady=3,
            cursor="hand2"
        )
        self.toggle_button.pack(anchor="e", pady=5)
        
        # Strength indicator section
        strength_frame = tk.Frame(main_frame, bg=self.card_color, padx=15, pady=15)
        strength_frame.pack(fill="x", pady=10)
        
        tk.Label(
            strength_frame,
            text="Password Strength:",
            font=("Helvetica", 11),
            bg=self.card_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        # Strength label
        self.strength_label = tk.Label(
            strength_frame,
            text="Enter a password",
            font=("Helvetica", 14, "bold"),
            bg=self.card_color,
            fg="#f38ba8"  # Default red for weak
        )
        self.strength_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            strength_frame,
            style="Custom.Horizontal.TProgressbar",
            mode="determinate",
            length=400,
            maximum=100
        )
        self.progress.pack(fill="x", pady=10)
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=20,
            troughcolor=self.entry_bg,
            background="#f38ba8",
            bordercolor=self.card_color,
            lightcolor=self.card_color,
            darkcolor=self.card_color
        )
        
        # Criteria checklist
        criteria_frame = tk.Frame(main_frame, bg=self.card_color, padx=15, pady=15)
        criteria_frame.pack(fill="x", pady=10)
        
        tk.Label(
            criteria_frame,
            text="Password Criteria:",
            font=("Helvetica", 11, "bold"),
            bg=self.card_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 10))
        
        # Create criteria labels
        self.criteria_labels = {}
        self.criteria_texts = {}
        criteria = [
            ("length", "At least 8 characters"),
            ("uppercase", "Contains uppercase letters (A-Z)"),
            ("lowercase", "Contains lowercase letters (a-z)"),
            ("numbers", "Contains numbers (0-9)"),
            ("special", "Contains special characters (!@#$%^&*)")
        ]
        
        for key, text in criteria:
            label = tk.Label(
                criteria_frame,
                text=f"❌ {text}",
                font=("Helvetica", 9),
                bg=self.card_color,
                fg="#f38ba8",
                anchor="w"
            )
            label.pack(fill="x", pady=2)
            self.criteria_labels[key] = label
            self.criteria_texts[key] = text
        
        # Suggestions section
        self.suggestions_frame = tk.Frame(main_frame, bg=self.card_color, padx=15, pady=15)
        self.suggestions_frame.pack(fill="x", pady=10)
        
        tk.Label(
            self.suggestions_frame,
            text="Suggestions:",
            font=("Helvetica", 11, "bold"),
            bg=self.card_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 10))
        
        self.suggestions_label = tk.Label(
            self.suggestions_frame,
            text="Enter a password to see suggestions",
            font=("Helvetica", 9),
            bg=self.card_color,
            fg="#a6adc8",
            wraplength=400,
            justify="left",
            anchor="w"
        )
        self.suggestions_label.pack(fill="x")
        
        # Generate password button
        generate_button = tk.Button(
            main_frame,
            text="🎲 Generate Strong Password",
            command=self.generate_password,
            font=("Helvetica", 12, "bold"),
            bg=self.button_color,
            fg=self.bg_color,
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        generate_button.pack(pady=20)
        
        # Add hover effect to button
        generate_button.bind("<Enter>", lambda e: generate_button.configure(bg=self.button_hover))
        generate_button.bind("<Leave>", lambda e: generate_button.configure(bg=self.button_color))
    
    def toggle_password_visibility(self):
        """Toggle between showing and hiding the password"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_button.config(text="👁️ Hide")
        else:
            self.password_entry.config(show="•")
            self.toggle_button.config(text="👁️ Show")
    
    def analyze_password(self, event=None):
        """Analyze the password strength and update the UI"""
        password = self.password_var.get()
        
        if not password:
            self.reset_ui()
            return
        
        # Check criteria
        has_length = len(password) >= 8
        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_numbers = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*" for c in password)
        
        # Update criteria labels
        self.update_criteria("length", has_length)
        self.update_criteria("uppercase", has_uppercase)
        self.update_criteria("lowercase", has_lowercase)
        self.update_criteria("numbers", has_numbers)
        self.update_criteria("special", has_special)
        
        # Calculate strength score
        score = 0
        if has_length:
            score += 20
        if has_uppercase:
            score += 20
        if has_lowercase:
            score += 20
        if has_numbers:
            score += 20
        if has_special:
            score += 20
        
        # Bonus for longer passwords
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Cap score at 100
        score = min(score, 100)
        
        # Determine strength level and color
        if score < 40:
            strength = "Weak"
            color = "#f38ba8"  # Red
        elif score < 60:
            strength = "Medium"
            color = "#fab387"  # Orange
        elif score < 80:
            strength = "Strong"
            color = "#a6e3a1"  # Green
        else:
            strength = "Very Strong"
            color = "#94e2d5"  # Teal
        
        # Update strength label and progress bar
        self.strength_label.config(text=strength, fg=color)
        self.progress["value"] = score
        
        # Update progress bar color
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            background=color
        )
        
        # Generate suggestions
        self.generate_suggestions(password, has_length, has_uppercase, 
                                  has_lowercase, has_numbers, has_special)
    
    def update_criteria(self, key, met):
        """Update a criteria label based on whether it's met"""
        if met:
            self.criteria_labels[key].config(
                text=f"✅ {self.criteria_texts[key]}",
                fg="#a6e3a1"
            )
        else:
            self.criteria_labels[key].config(
                text=f"❌ {self.criteria_texts[key]}",
                fg="#f38ba8"
            )
    
    def generate_suggestions(self, password, has_length, has_uppercase, 
                            has_lowercase, has_numbers, has_special):
        """Generate suggestions to improve password strength"""
        suggestions = []
        
        if not has_length:
            suggestions.append("• Make your password at least 8 characters long")
        if not has_uppercase:
            suggestions.append("• Add uppercase letters (A-Z)")
        if not has_lowercase:
            suggestions.append("• Add lowercase letters (a-z)")
        if not has_numbers:
            suggestions.append("• Include numbers (0-9)")
        if not has_special:
            suggestions.append("• Add special characters (!@#$%^&*)")
        
        if len(password) < 12 and has_length:
            suggestions.append("• Consider using 12+ characters for better security")
        
        if suggestions:
            self.suggestions_label.config(text="\n".join(suggestions))
        else:
            self.suggestions_label.config(text="✅ Your password meets all criteria!")
    
    def reset_ui(self):
        """Reset the UI to initial state"""
        self.strength_label.config(text="Enter a password", fg="#f38ba8")
        self.progress["value"] = 0
        
        for key in self.criteria_labels:
            self.criteria_labels[key].config(
                text=f"❌ {self.criteria_texts[key]}",
                fg="#f38ba8"
            )
        
        self.suggestions_label.config(text="Enter a password to see suggestions")
    
    def generate_password(self):
        """Generate a strong random password"""
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        numbers = string.digits
        special = "!@#$%^&*"
        
        # Ensure at least one character from each set
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(numbers),
            random.choice(special)
        ]
        
        # Fill the rest with random characters from all sets
        all_chars = lowercase + uppercase + numbers + special
        length = 16  # Generate 16-character password
        
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
        
        # Shuffle the password
        random.shuffle(password)
        
        # Convert to string
        generated_password = "".join(password)
        
        # Set the password in the entry
        self.password_var.set(generated_password)
        self.password_entry.config(show="")  # Show the generated password
        self.show_password = True
        self.toggle_button.config(text="👁️ Hide")
        
        # Analyze the generated password
        self.analyze_password()
        
        # Show message
        messagebox.showinfo(
            "Password Generated",
            "A strong password has been generated!\n\n"
            "Make sure to save it in a secure location."
        )


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PasswordStrengthAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
