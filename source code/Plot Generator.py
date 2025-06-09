import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.figure import Figure
import seaborn as sns
import openai
import json
import numpy as np
from pathlib import Path
import io
import sys
import warnings
warnings.filterwarnings('ignore')

class PlotIQ:
    def __init__(self, root):
        self.root = root
        self.root.title("PlotIQ - AI-Powered Data Visualization")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3a3a3a',
            'accent': '#00d4aa',
            'accent_hover': '#00b894',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'error': '#ff6b6b',
            'success': '#51cf66'
        }
        
        self.data = None
        self.api_key = None
        self.client = None
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['accent'],
                       font=('Helvetica', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('Helvetica', 12))
        
        style.configure('Modern.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_hover'])])
        
    def create_widgets(self):
        """Create and layout all GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="PlotIQ", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="AI-Powered Data Visualization Tool", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Content area with notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Setup tab
        self.create_setup_tab()
        
        # Data tab
        self.create_data_tab()
        
        # Visualization tab
        self.create_viz_tab()
        
    def create_setup_tab(self):
        """Create the setup and configuration tab"""
        setup_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(setup_frame, text="Setup")
        
        # API Key section
        api_frame = ttk.LabelFrame(setup_frame, text="OpenAI Configuration", 
                                  style='Modern.TFrame')
        api_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(api_frame, text="OpenAI API Key:", 
                bg=self.colors['bg_secondary'], 
                fg=self.colors['text_primary'],
                font=('Helvetica', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.api_key_entry = tk.Entry(api_frame, show="*", width=50,
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_primary'],
                                     insertbackground=self.colors['text_primary'],
                                     relief='flat', bd=5)
        self.api_key_entry.pack(padx=10, pady=(0, 10), fill='x')
        
        ttk.Button(api_frame, text="Set API Key", 
                  command=self.set_api_key,
                  style='Modern.TButton').pack(pady=10)
        
        # Data loading section
        data_frame = ttk.LabelFrame(setup_frame, text="Data Loading", 
                                   style='Modern.TFrame')
        data_frame.pack(fill='x', padx=20, pady=20)
        
        self.file_label = tk.Label(data_frame, text="No file selected", 
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_secondary'],
                                  font=('Helvetica', 10))
        self.file_label.pack(padx=10, pady=10)
        
        ttk.Button(data_frame, text="Load Dataset", 
                  command=self.load_data,
                  style='Modern.TButton').pack(pady=10)
        
        # Status section
        self.status_label = tk.Label(setup_frame, text="Ready", 
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['success'],
                                    font=('Helvetica', 10, 'bold'))
        self.status_label.pack(side='bottom', pady=20)
        
    def create_data_tab(self):
        """Create the data preview tab"""
        data_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(data_frame, text="Data Preview")
        
        # Data info frame
        info_frame = ttk.Frame(data_frame, style='Modern.TFrame')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        self.data_info_label = tk.Label(info_frame, text="Load a dataset to see preview", 
                                       bg=self.colors['bg_secondary'],
                                       fg=self.colors['text_secondary'],
                                       font=('Helvetica', 10))
        self.data_info_label.pack()
        
        # Data preview with scrollbars
        preview_frame = ttk.Frame(data_frame, style='Modern.TFrame')
        preview_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.data_text = scrolledtext.ScrolledText(preview_frame, 
                                                  bg=self.colors['bg_tertiary'],
                                                  fg=self.colors['text_primary'],
                                                  font=('Courier', 9),
                                                  state='disabled')
        self.data_text.pack(fill='both', expand=True)
        
    def create_viz_tab(self):
        """Create the visualization tab"""
        viz_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(viz_frame, text="Visualization")
        
        # Control panel
        control_frame = ttk.Frame(viz_frame, style='Modern.TFrame')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(control_frame, text="Describe the plot you want:", 
                bg=self.colors['bg_secondary'], 
                fg=self.colors['text_primary'],
                font=('Helvetica', 10, 'bold')).pack(anchor='w')
        
        self.prompt_text = scrolledtext.ScrolledText(control_frame, height=4,
                                                    bg=self.colors['bg_tertiary'],
                                                    fg=self.colors['text_primary'],
                                                    font=('Helvetica', 10))
        self.prompt_text.pack(fill='x', pady=5)
        
        button_frame = ttk.Frame(control_frame, style='Modern.TFrame')
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Generate Plot", 
                  command=self.generate_plot,
                  style='Modern.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear Plot", 
                  command=self.clear_plot,
                  style='Modern.TButton').pack(side='left')
        
        # Plot area
        self.plot_frame = ttk.Frame(viz_frame, style='Modern.TFrame')
        self.plot_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.fig = Figure(figsize=(10, 6), facecolor='#2d2d2d')
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def set_api_key(self):
        """Set and validate OpenAI API key"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            self.update_status("Please enter an API key", "error")
            return
            
        try:
            self.client = openai.OpenAI(api_key=api_key)
            # Test the API key with a simple request
            self.client.models.list()
            self.api_key = api_key
            self.update_status("API key set successfully", "success")
        except Exception as e:
            self.update_status(f"Invalid API key: {str(e)}", "error")
            self.client = None
            
    def load_data(self):
        """Load dataset from various file formats"""
        file_path = filedialog.askopenfilename(
            title="Select Dataset",
            filetypes=[
                ("All Supported", "*.csv;*.xlsx;*.xls;*.json;*.parquet;*.tsv"),
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx;*.xls"),
                ("JSON files", "*.json"),
                ("Parquet files", "*.parquet"),
                ("TSV files", "*.tsv"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                self.data = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            elif file_ext == '.json':
                self.data = pd.read_json(file_path)
            elif file_ext == '.parquet':
                self.data = pd.read_parquet(file_path)
            elif file_ext == '.tsv':
                self.data = pd.read_csv(file_path, sep='\t')
            else:
                # Try to read as CSV by default
                self.data = pd.read_csv(file_path)
                
            self.file_label.config(text=f"Loaded: {Path(file_path).name}")
            self.update_data_preview()
            self.update_status(f"Dataset loaded successfully: {self.data.shape[0]} rows, {self.data.shape[1]} columns", "success")
            
        except Exception as e:
            self.update_status(f"Error loading file: {str(e)}", "error")
            
    def update_data_preview(self):
        """Update the data preview tab"""
        if self.data is None:
            return
            
        # Update info label
        info_text = f"Shape: {self.data.shape} | Columns: {list(self.data.columns)}"
        self.data_info_label.config(text=info_text)
        
        # Update preview text
        self.data_text.config(state='normal')
        self.data_text.delete(1.0, tk.END)
        
        # Show basic info
        buffer = io.StringIO()
        self.data.info(buf=buffer)
        info_str = buffer.getvalue()
        
        preview = f"DATASET INFO:\n{info_str}\n\n"
        preview += f"FIRST 10 ROWS:\n{self.data.head(10).to_string()}\n\n"
        preview += f"BASIC STATISTICS:\n{self.data.describe().to_string()}"
        
        self.data_text.insert(1.0, preview)
        self.data_text.config(state='disabled')
        
    def generate_plot(self):
        """Generate plot using OpenAI"""
        if not self.client:
            self.update_status("Please set a valid OpenAI API key first", "error")
            return
            
        if self.data is None:
            self.update_status("Please load a dataset first", "error")
            return
            
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        if not prompt:
            self.update_status("Please enter a description for the plot", "error")
            return
            
        try:
            self.update_status("Generating plot...", "info")
            
            # Prepare data summary for OpenAI
            data_summary = {
                'columns': list(self.data.columns),
                'shape': self.data.shape,
                'dtypes': self.data.dtypes.to_dict(),
                'sample_data': self.data.head().to_dict()
            }
            
            # Create the prompt for OpenAI
            system_prompt = """You are a data visualization expert. Given a dataset description and user request, generate Python code using matplotlib and seaborn to create the requested plot. 

Rules:
1. Use 'df' as the dataframe variable name
2. Use plt and sns for plotting (already imported)
3. Set figure size to (10, 6)
4. Use dark theme colors that work well on dark backgrounds
5. Include proper labels and titles
6. Return only the plotting code, no explanations
7. Don't include plt.show() or plt.savefig()
8. Make the plot visually appealing with good styling"""

            user_prompt = f"""Dataset info:
Columns: {data_summary['columns']}
Shape: {data_summary['shape']}
Data types: {data_summary['dtypes']}
Sample data: {data_summary['sample_data']}

User request: {prompt}

Generate the Python plotting code:"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            plot_code = response.choices[0].message.content.strip()
            
            # Clean up the code (remove code block markers if present)
            if plot_code.startswith('```python'):
                plot_code = plot_code[9:]
            if plot_code.startswith('```'):
                plot_code = plot_code[3:]
            if plot_code.endswith('```'):
                plot_code = plot_code[:-3]
                
            self.execute_plot_code(plot_code)
            
        except Exception as e:
            self.update_status(f"Error generating plot: {str(e)}", "error")
            
    def execute_plot_code(self, code):
        """Execute the generated plotting code"""
        try:
            # Clear previous plot
            self.fig.clear()
            
            # Create new subplot
            ax = self.fig.add_subplot(111)
            
            # Set dark style
            plt.style.use('dark_background')
            self.fig.patch.set_facecolor('#2d2d2d')
            ax.set_facecolor('#2d2d2d')
            
            # Prepare execution environment
            exec_globals = {
                'df': self.data,
                'plt': plt,
                'sns': sns,
                'np': np,
                'pd': pd,
                'ax': ax,
                'fig': self.fig
            }
            
            # Execute the code
            exec(code, exec_globals)
            
            # Refresh canvas
            self.canvas.draw()
            self.update_status("Plot generated successfully", "success")
            
        except Exception as e:
            self.update_status(f"Error executing plot code: {str(e)}", "error")
            
    def clear_plot(self):
        """Clear the current plot"""
        self.fig.clear()
        self.canvas.draw()
        self.update_status("Plot cleared", "info")
        
    def update_status(self, message, status_type="info"):
        """Update status label with colored messages"""
        colors = {
            "success": self.colors['success'],
            "error": self.colors['error'],
            "info": self.colors['text_secondary']
        }
        
        self.status_label.config(text=message, fg=colors.get(status_type, colors["info"]))
        self.root.update()


def main():
    """Main function to run PlotIQ"""
    root = tk.Tk()
    app = PlotIQ(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()