import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
import threading
import re
from datetime import datetime
import requests

class DatasetCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Mr. CleanData")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Color scheme
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3d3d3d',
            'accent': '#007acc',
            'accent_hover': '#005a9e',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0'
        }
        
        # Variables
        self.api_key = tk.StringVar()
        self.file_path = tk.StringVar()
        self.df = None
        self.cleaned_df = None
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Header.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Normal.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 10))
        
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover'])])
        
        style.configure('Secondary.TButton',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       borderwidth=0)
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧽 Mr. CleanData", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # API Key Section
        api_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief='raised', bd=1)
        api_frame.pack(fill='x', pady=(0, 20))
        
        api_inner = tk.Frame(api_frame, bg=self.colors['bg_secondary'])
        api_inner.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(api_inner, text="OpenAI API Key", style='Header.TLabel').pack(anchor='w')
        
        api_entry_frame = tk.Frame(api_inner, bg=self.colors['bg_secondary'])
        api_entry_frame.pack(fill='x', pady=(5, 0))
        
        self.api_entry = tk.Entry(api_entry_frame, textvariable=self.api_key, 
                                 font=('Segoe UI', 11), show='*',
                                 bg=self.colors['bg_tertiary'], 
                                 fg=self.colors['text_primary'],
                                 insertbackground=self.colors['text_primary'],
                                 relief='flat', bd=5)
        self.api_entry.pack(side='left', fill='x', expand=True, ipady=5)
        
        # File Selection Section
        file_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief='raised', bd=1)
        file_frame.pack(fill='x', pady=(0, 20))
        
        file_inner = tk.Frame(file_frame, bg=self.colors['bg_secondary'])
        file_inner.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(file_inner, text="Dataset File", style='Header.TLabel').pack(anchor='w')
        
        file_select_frame = tk.Frame(file_inner, bg=self.colors['bg_secondary'])
        file_select_frame.pack(fill='x', pady=(5, 0))
        
        self.file_label = tk.Label(file_select_frame, textvariable=self.file_path,
                                  bg=self.colors['bg_tertiary'], 
                                  fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 10), anchor='w',
                                  relief='flat', padx=10, pady=8)
        self.file_label.pack(side='left', fill='x', expand=True)
        
        select_btn = ttk.Button(file_select_frame, text="Browse", 
                               command=self.select_file, style='Accent.TButton')
        select_btn.pack(side='right', padx=(10, 0))
        
        # Control Buttons
        control_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        control_frame.pack(fill='x', pady=(0, 20))
        
        self.analyze_btn = ttk.Button(control_frame, text="🔍 Analyze & Clean Dataset", 
                                     command=self.start_analysis, style='Accent.TButton')
        self.analyze_btn.pack(side='left', padx=(0, 10))
        
        self.export_btn = ttk.Button(control_frame, text="💾 Export Cleaned Data", 
                                    command=self.export_data, style='Secondary.TButton',
                                    state='disabled')
        self.export_btn.pack(side='left')
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 20))
        
        # Results Area
        results_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief='raised', bd=1)
        results_frame.pack(fill='both', expand=True)
        
        results_inner = tk.Frame(results_frame, bg=self.colors['bg_secondary'])
        results_inner.pack(fill='both', expand=True, padx=20, pady=15)
        
        ttk.Label(results_inner, text="Analysis Results & Cleaning Log", 
                 style='Header.TLabel').pack(anchor='w', pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(results_inner,
                                                     bg=self.colors['bg_tertiary'],
                                                     fg=self.colors['text_primary'],
                                                     font=('Consolas', 10),
                                                     insertbackground=self.colors['text_primary'],
                                                     relief='flat', bd=0)
        self.results_text.pack(fill='both', expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready to analyze datasets")
        status_bar = tk.Label(main_frame, textvariable=self.status_var,
                             bg=self.colors['bg_tertiary'], 
                             fg=self.colors['text_secondary'],
                             font=('Segoe UI', 9), anchor='w', padx=10, pady=5)
        status_bar.pack(fill='x', pady=(10, 0))
        
    def select_file(self):
        file_types = [
            ("All Supported", "*.csv;*.xlsx;*.xls;*.json;*.tsv"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx;*.xls"),
            ("JSON files", "*.json"),
            ("TSV files", "*.tsv"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Dataset File",
            filetypes=file_types
        )
        
        if filename:
            self.file_path.set(filename)
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
            
    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.results_text.insert(tk.END, formatted_message)
        self.results_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_analysis(self):
        if not self.api_key.get().strip():
            messagebox.showerror("Error", "Please enter your OpenAI API key")
            return
            
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a dataset file")
            return
            
        # Start analysis in separate thread
        self.analyze_btn.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.analyze_dataset)
        thread.daemon = True
        thread.start()
        
    def analyze_dataset(self):
        try:
            self.log_message("Starting dataset analysis...")
            self.status_var.set("Loading dataset...")
            
            # Load dataset
            file_path = self.file_path.get()
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                self.df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                self.df = pd.read_excel(file_path)
            elif file_ext == '.json':
                self.df = pd.read_json(file_path)
            elif file_ext == '.tsv':
                self.df = pd.read_csv(file_path, sep='\t')
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
                
            self.log_message(f"Loaded dataset: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            
            # Analyze with AI
            self.status_var.set("Analyzing with AI...")
            analysis_result = self.analyze_with_ai()
            
            # Perform cleaning
            self.status_var.set("Cleaning dataset...")
            self.clean_dataset(analysis_result)
            
            self.log_message("Dataset cleaning completed successfully!", "SUCCESS")
            self.status_var.set("Analysis and cleaning completed")
            
            # Enable export button
            self.export_btn.config(state='normal')
            
        except Exception as e:
            self.log_message(f"Error during analysis: {str(e)}", "ERROR")
            self.status_var.set("Analysis failed")
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            
        finally:
            self.progress.stop()
            self.analyze_btn.config(state='normal')
            
    def analyze_with_ai(self):
        # Prepare dataset summary for AI analysis
        summary = self.generate_dataset_summary()
        
        prompt = f"""
        Analyze this dataset and provide cleaning recommendations in JSON format.
        
        Dataset Summary:
        {summary}
        
        Please provide a JSON response with the following structure:
        {{
            "recommendations": [
                {{
                    "column": "column_name",
                    "issues": ["issue1", "issue2"],
                    "actions": ["action1", "action2"],
                    "priority": "high|medium|low"
                }}
            ],
            "general_issues": ["issue1", "issue2"],
            "general_actions": ["action1", "action2"]
        }}
        
        Focus on common data quality issues like:
        - Missing values
        - Duplicates
        - Inconsistent formatting
        - Outliers
        - Data type mismatches
        - Leading/trailing whitespace
        - Inconsistent categorical values
        """
        
        try:
            # Make API call to OpenAI
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key.get().strip()}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a data cleaning expert. Provide practical, actionable recommendations in JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in AI response")
            else:
                raise ValueError(f"API request failed: {response.status_code}")
                
        except Exception as e:
            self.log_message(f"AI analysis failed: {str(e)}", "WARNING")
            # Return basic analysis if AI fails
            return self.basic_analysis()
            
    def generate_dataset_summary(self):
        summary = []
        summary.append(f"Shape: {self.df.shape}")
        summary.append(f"Columns: {list(self.df.columns)}")
        summary.append(f"Data types: {dict(self.df.dtypes)}")
        summary.append(f"Missing values: {dict(self.df.isnull().sum())}")
        summary.append(f"Duplicate rows: {self.df.duplicated().sum()}")
        
        # Sample data for first few rows
        summary.append("Sample data:")
        summary.append(str(self.df.head(3).to_dict()))
        
        return "\n".join(summary)
        
    def basic_analysis(self):
        """Fallback analysis if AI fails"""
        recommendations = []
        
        for col in self.df.columns:
            issues = []
            actions = []
            
            # Check for missing values
            if self.df[col].isnull().sum() > 0:
                issues.append("Missing values")
                actions.append("Fill or remove missing values")
                
            # Check for string columns with whitespace
            if self.df[col].dtype == 'object':
                sample_values = self.df[col].dropna().astype(str).head(100)
                if any(val != val.strip() for val in sample_values):
                    issues.append("Leading/trailing whitespace")
                    actions.append("Strip whitespace")
                    
            if issues:
                recommendations.append({
                    "column": col,
                    "issues": issues,
                    "actions": actions,
                    "priority": "medium"
                })
                
        return {
            "recommendations": recommendations,
            "general_issues": ["Check for duplicates"],
            "general_actions": ["Remove duplicate rows"]
        }
        
    def clean_dataset(self, analysis_result):
        self.cleaned_df = self.df.copy()
        
        self.log_message("Applying cleaning operations...")
        
        # Apply general cleaning
        initial_rows = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.drop_duplicates()
        removed_duplicates = initial_rows - len(self.cleaned_df)
        if removed_duplicates > 0:
            self.log_message(f"Removed {removed_duplicates} duplicate rows")
            
        # Apply column-specific cleaning
        for rec in analysis_result.get("recommendations", []):
            column = rec["column"]
            if column not in self.cleaned_df.columns:
                continue
                
            self.log_message(f"Cleaning column '{column}'...")
            
            for action in rec["actions"]:
                if "missing" in action.lower():
                    if self.cleaned_df[column].dtype in ['int64', 'float64']:
                        # Fill numeric missing values with median
                        median_val = self.cleaned_df[column].median()
                        self.cleaned_df[column].fillna(median_val, inplace=True)
                        self.log_message(f"  - Filled missing values with median: {median_val}")
                    else:
                        # Fill categorical missing values with mode
                        mode_val = self.cleaned_df[column].mode()
                        if len(mode_val) > 0:
                            self.cleaned_df[column].fillna(mode_val[0], inplace=True)
                            self.log_message(f"  - Filled missing values with mode: {mode_val[0]}")
                        
                elif "whitespace" in action.lower():
                    if self.cleaned_df[column].dtype == 'object':
                        self.cleaned_df[column] = self.cleaned_df[column].astype(str).str.strip()
                        self.log_message("  - Removed leading/trailing whitespace")
                        
                elif "outlier" in action.lower():
                    if self.cleaned_df[column].dtype in ['int64', 'float64']:
                        Q1 = self.cleaned_df[column].quantile(0.25)
                        Q3 = self.cleaned_df[column].quantile(0.75)
                        IQR = Q3 - Q1
                        lower = Q1 - 1.5 * IQR
                        upper = Q3 + 1.5 * IQR
                        outliers_before = len(self.cleaned_df)
                        self.cleaned_df = self.cleaned_df[
                            (self.cleaned_df[column] >= lower) & 
                            (self.cleaned_df[column] <= upper)
                        ]
                        outliers_removed = outliers_before - len(self.cleaned_df)
                        if outliers_removed > 0:
                            self.log_message(f"  - Removed {outliers_removed} outlier rows")
                            
        # Final summary
        self.log_message(f"Cleaning summary:")
        self.log_message(f"  Original shape: {self.df.shape}")
        self.log_message(f"  Cleaned shape: {self.cleaned_df.shape}")
        self.log_message(f"  Rows removed: {self.df.shape[0] - self.cleaned_df.shape[0]}")
        
    def export_data(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No cleaned data to export")
            return
            
        try:
            original_path = Path(self.file_path.get())
            output_path = original_path.parent / f"{original_path.stem}_cleaned{original_path.suffix}"
            
            # Export based on original file format
            if original_path.suffix.lower() == '.csv':
                self.cleaned_df.to_csv(output_path, index=False)
            elif original_path.suffix.lower() in ['.xlsx', '.xls']:
                self.cleaned_df.to_excel(output_path, index=False)
            elif original_path.suffix.lower() == '.json':
                self.cleaned_df.to_json(output_path, orient='records', indent=2)
            elif original_path.suffix.lower() == '.tsv':
                self.cleaned_df.to_csv(output_path, sep='\t', index=False)
                
            self.log_message(f"Exported cleaned dataset to: {output_path}", "SUCCESS")
            self.status_var.set(f"Exported to: {output_path.name}")
            
            messagebox.showinfo("Success", f"Cleaned dataset exported to:\n{output_path}")
            
        except Exception as e:
            self.log_message(f"Export failed: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Export failed: {str(e)}")

def main():
    root = tk.Tk()
    app = DatasetCleaner(root)
    root.mainloop()

if __name__ == "__main__":
    main()