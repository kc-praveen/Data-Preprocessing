import tkinter as tk
import numpy as np
import pandas as pd 
from tkinter import filedialog,messagebox
from tkinter import Frame,Listbox,Scrollbar,RIGHT, BOTH, MULTIPLE
from sklearn.impute import SimpleImputer
from tkinter import ttk
from sklearn.impute import KNNImputer

class Preprocess:  
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Selection")
        self.window.geometry("800x400")
        self.window.configure(bg="#68838B") 	
        
        label = tk.Label(self.window, text="DATA PREPROCESSING", font=("Californian FB", 22, "bold"), fg="white",bg="#68838B")
        label.place(x=250, y=30)
        label_1 = tk.Label(self.window, text="SELECT FILE: ", font=("italic", 15, "bold"),bg="#68838B",fg="black")
        label_1.place(x=133, y=165)
        
        self.e1 = tk.Entry(self.window, width=50)
        self.e1.place(x=280, y=170)
        
        button_1 = tk.Button(self.window, text='choose', command=self.choose, font=("Cascadia Code SemiBold", 12), bg="white")
        button_1.place(x=600, y=165)
        button_2 = tk.Button(self.window, text='ENTER', command=self.window_2, font=("Century", 16), bg="white", fg="red")
        button_2.place(x=340, y=270)
        
        self.file = None
        
        self.window.mainloop()
    
    def choose(self):
        self.file = filedialog.askopenfile(filetypes=[("CSV", "*.csv")])

        self.data = self.file.name
        self.e1.delete(0, tk.END)  
        self.e1.insert(0, self.data)  

    def cfile(self):
        self.f_path=self.e1.get()
        self.csv_file = pd.read_csv(self.f_path)
        self.csv_list = list(self.csv_file)
       
    def window_2(self):
        if not self.file:  
            messagebox.showerror("Error", "No file selected. Please choose a file.")
            return
       
        self.cfile()
        self.window2 = tk.Tk()
        self.window2.title("COLUMN SELECTION")
        self.window2.geometry("1000x600")
        self.window2.configure(bg="#68838B")
        label = tk.Label(self.window2, text="COLUMN SELECTION", font=("Constantia", 22, "bold"), bg="#68838B", fg="white")
        label.place(x=250, y=30)
        scrollbar1 = Scrollbar(self.window2)
        scrollbar1.pack(side=RIGHT,fill=BOTH)
                    
        self.listbox1 = Listbox(self.window2, selectmode=MULTIPLE)
        self.listbox1.config(yscrollcommand=scrollbar1.set)
        self.listbox1.place(x=250, y=100,width=605, height=350)
                
        button_3=tk.Button(self.window2,text="ENTER",command=self.window_3,font=("Century",16),bg="white",fg="black")
        button_3.place(x=400,y=500)
                
        button_data=tk.Button(self.window2, text="VIEW Dataset",command=self.dataset_window, font=("Century",16),bg="white",fg="black")
        button_data.place(x=550,y=500)
                
        for row in self.csv_list:
            self.listbox1.insert(tk.END, row) 
            
     
    def dataset_window(self): 
        self.cfile()
        self.windowds=tk.Tk()
        self.windowds.title("VIEW DATASET")
        self.windowds.geometry("1100x550")
        self.windowds.configure(bg="#68838B")
    
        bd=tk.Button(self.windowds, text="EXIT",command=self.__del__, font=("Century",16),bg="white",fg="red")
        bd.place(x=400,y=450)
        
        label = tk.Label(self.windowds, text="CHECK DATASET", font=("italic", 20, "bold"), bg="#68838B", fg="white")
        label.place(x=350, y=30)
            
        frame = Frame(self.windowds)
        frame.place(x=180,y=100,width=800, height=300)
        
        scroll1 = Scrollbar(frame, orient='vertical')
        scroll1.pack(side=RIGHT,fill=tk.Y)
        
        scroll2 = tk.Scrollbar(frame, orient='horizontal')
        scroll2.pack(side=tk.BOTTOM, fill=tk.X)
        
        global tview
        #tview
        tview = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
        tview.pack()
        
        scroll1.config(command=tview.yview)
        scroll2.config(command=tview.xview)
        
        
        tview["columns"] = list(self.csv_file)
        tview["show"] = "headings"
        
        for column in tview["columns"]:
            tview.heading(column, text=column)
            
        df_rows = self.csv_file.to_numpy().tolist()
        
        for row in df_rows:
            tview.insert("", "end", values=row)
        tview.pack()
            

    def __del__(self):
        self.windowds.destroy()
        
        
    
    def get_selected_values(self): 
        self.selected_columns = []
        self.selected_indices = self.listbox1.curselection()
        
        if self.selected_indices:
            self.selected_columns = [self.csv_list[int(index)] for index in self.selected_indices]
            return self.selected_columns
        
    def window_3(self):
        self.window3=tk.Tk()
        self.window3.title("PROCESSING_ANALYTICS")
        self.window3.geometry("1200x600")
        self.window3.configure(bg="#68838B")
        labe13=tk.Label(self.window3,text="ANALYTICS",font=("italic",24,"bold"),bg="#68838B",fg="white").place(x=450,y=30)
        label4=tk.Label(self.window3,text="For selected index",font=("italic",12,"bold"),bg="#68838B",fg="white").place(x=80,y=75)
        
        b4=tk.Button(self.window3,command=self.check_null_index,text="CHECK NULL",font=("Century",14),bg="white",fg="red").place(x=80,y=100)
        b5=tk.Button(self.window3,command=self.check_null_dataset,text="CHECK NULL ALL",font=("Century",14),bg="white",fg="red").place(x=500,y=500)
        
        b6=tk.Button(self.window3,command=self.window_4,text="NEXT",font=("Century",16),bg="white",fg="red").place(x=800,y=500)
        b7=tk.Button(self.window3,command=self.back,text="BACK",font=("Century",16),bg="white",fg="red").place(x=350,y=500)
      
        scrollbar2 = Scrollbar(self.window3)
        scrollbar2.pack(side=RIGHT,fill=BOTH)
        self.textbox1 = tk.Text(self.window3,wrap=tk.NONE)
        self.textbox1.config(yscrollcommand=scrollbar2)
        self.textbox1.place(x=250,y=80,width=750, height=350)
       
    def back(self):
        self.window3.destroy()
        self.window2.destroy()
        self.window_2()
        
    def check_null_index(self):
        selected_columns = self.get_selected_values()
    
        if not selected_columns:
            messagebox.showwarning("Warning", "No columns selected for analysis.")
            return
    
        null_count = self.csv_file[selected_columns].isnull().sum()
        count = self.csv_file[selected_columns].count()
    
        result = pd.DataFrame({
            "Column": selected_columns,
            "Null Count": null_count,
            "Non-null Count": count
        })
    
        self.textbox1.delete(1.0, tk.END)
    
        column_widths = result.applymap(lambda x: len(str(x))).max() + 5
        
        header_str = f"{'Column':<{column_widths['Column']}} {'Null Count':<{column_widths['Null Count']}}   {'Non-null Count':<{column_widths['Non-null Count']}}"
        self.textbox1.insert(tk.END, header_str + "\n")
    
        for _, row in result.iterrows():      
            row_str = f"{row['Column']:<{column_widths['Column']}} {row['Null Count']:<{column_widths['Null Count']}}       {row['Non-null Count']:<{column_widths['Non-null Count']}}"
            self.textbox1.insert(tk.END, row_str + "\n")


    def check_null_dataset(self):
        messagebox.showinfo("NULL CHECK","Null Checked For All Columns")
        self.window_null = tk.Tk()
        self.window_null.title("NULL CHECK")
        self.window_null.geometry("1200x600")
        self.window_null.configure(bg="#68838B")
        
        label13 = tk.Label(self.window_null, text="CHECK NULL FOR ALL COLUMNS", font=("italic", 20, "bold"), bg="#68838B" , fg="white").place(x=250, y=30)
        
        btn_exit = tk.Button(self.window_null, text="EXIT", command=self.null_del, font=("Century", 16), bg="white", fg="red")
        btn_exit.place(x=400, y=500)
    
        scrollbar2 = Scrollbar(self.window_null)
        scrollbar2.pack(side=RIGHT, fill=BOTH)
    
        self.textbox2 = tk.Text(self.window_null, wrap=tk.NONE)
        self.textbox2.config(yscrollcommand=scrollbar2.set)
        self.textbox2.place(x=250, y=120, width=750, height=350)
    
        null_count = self.csv_file.isnull().sum()
        count = self.csv_file.count()
    
        result2 = pd.DataFrame({
            "Column": self.csv_list,
            "Null Count": null_count,
            "Non-null Count": count
        })
    
        self.textbox2.delete(1.0, tk.END)

        column_widths = result2.applymap(lambda x: len(str(x))).max() + 5

        header_str = f"{'Column':<{column_widths['Column']}} {'Null Count':<{column_widths['Null Count']}} {'Non-null Count':<{column_widths['Non-null Count']}}"
        self.textbox2.insert(tk.END, header_str + "\n")
    
        for _, row in result2.iterrows():
            row_str = f"{row['Column']:<{column_widths['Column']}} {row['Null Count']:<{column_widths['Null Count']}} {row['Non-null Count']:<{column_widths['Non-null Count']}}"
            self.textbox2.insert(tk.END, row_str + "\n")
        
    def null_del(self):
        self.window_null.destroy()
           
        
        
    def window_4(self):
        self.window4 = tk.Tk()
        self.window4.title("CLEAN DATA")
        self.window4.geometry("1000x600")
        self.window4.configure(bg="#68838B")
    
        label13 = tk.Label(self.window4, text="SELECT METHOD", font=("italic", 24, "bold"), bg="#68838B", fg="white")
        label13.place(x=400, y=30)
    
        bw4_ffill = tk.Button(self.window4, command=self.ffill_window, text="Forward Fill", font=("Century", 20), bg="white", fg="black")
        bw4_ffill.place(x=700, y=150)
    
        bw4_bfill = tk.Button(self.window4, command=self.bfill_window, text="Backward Fill", font=("Century", 20), bg="white", fg="black")
        bw4_bfill.place(x=700, y=250)
    
        bw4_mean = tk.Button(self.window4, command=self.mean_window, text="Mean", font=("Century", 20), bg="white", fg="black")
        bw4_mean.place(x=150, y=150)
    
        bw4_median = tk.Button(self.window4, command=self.median_window, text="Median", font=("Century", 20), bg="white", fg="black")
        bw4_median.place(x=150, y=250)
    
        bw4_drop = tk.Button(self.window4, command=self.drop_window, text="Drop", font=("Century", 20), bg="white", fg="black")
        bw4_drop.place(x=150, y=350)
    
        bw4_knn = tk.Button(self.window4, command=self.KNN_window, text="KNN", font=("Century", 20), bg="white", fg="black")
        bw4_knn.place(x=700, y=350)

        self.window4.mainloop()

        

    def ffill_del(self):
        self.window_ffill.destroy()
        
    def bfill_del(self):
        self.window_bfill.destroy()
        
    def mean_del(self):
        self.window_mean.destroy()
        
    def median_del(self):
        self.window_median.destroy()
        
    def drop_del(self):
        self.window_drop.destroy()
        
    def KNN_del(self):
        self.window_KNN.destroy()
        

    def ffill_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.ffill_csv.to_csv(file_path, index=False)
        messagebox.showinfo("FORWARD FILLING", "Saved Sucessfully" )

    def bfill_save(self):  
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.bfill_csv.to_csv(file_path, index=False)
        messagebox.showinfo("BACKWARD FILLING", "Saved Sucessfully" )


    def mean_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.mean_csv.to_csv(file_path, index=False)
        messagebox.showinfo("MEAN METHOD", "Saved Sucessfully" )

            
    def median_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.median_csv.to_csv(file_path, index=False)
        messagebox.showinfo("MEDIAN METHOD", "Saved Sucessfully" )
            
    def drop_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.drop_csv.to_csv(file_path, index=False)
        messagebox.showinfo("DROP METHOD", "Saved Sucessfully" )
        
    def KNN_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.KNN_csv.to_csv(file_path, index=False)
        messagebox.showinfo("KNN METHOD", "Saved Sucessfully" )

    def ffill_window(self):
        self.window_ffill = tk.Tk()
        self.window_ffill.title("FORWARD FILLING")
        self.window_ffill.geometry("1100x550")
        self.window_ffill.configure(bg="#68838B")
    
        labe13 = tk.Label(self.window_ffill, text="FORWARD FILLING METHOD", font=("italic", 20, "bold"), bg="#68838B", fg="white").place(x=250, y=30)
    
        exit_ffill = tk.Button(self.window_ffill, command=self.ffill_del, text=" EXIT ", font=("Century", 18), bg="white", fg="red")
        exit_ffill.place(x=250, y=450)
    
        save_ffill = tk.Button(self.window_ffill, command=self.ffill_save, text="SAVE", font=("Century", 18), bg="white", fg="black")
        save_ffill.place(x=350, y=450)

        self.selected_columns2 = self.get_selected_values()
        if self.selected_columns2:
            self.ffill_csv = self.csv_file.copy()
            self.ffill_csv[self.selected_columns2] = self.ffill_csv[self.selected_columns2].fillna(method="ffill")

            frame = Frame(self.window_ffill)
            frame.place(x=200, y=100, width=800, height=300)
            
            scroll1 = Scrollbar(frame, orient='vertical')
            scroll1.pack(side=RIGHT, fill=tk.Y)

            scroll2 = tk.Scrollbar(frame, orient='horizontal')
            scroll2.pack(side=tk.BOTTOM, fill=tk.X)

            global tview
            tview = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
            tview.pack()

            scroll1.config(command=tview.yview)
            scroll2.config(command=tview.xview)

            tview["columns"] = list(self.ffill_csv)
            tview["show"] = "headings"

            for column in tview["columns"]:
                tview.heading(column, text=column)

            df_rows = self.ffill_csv.to_numpy().tolist()

            for row in df_rows:
                tview.insert("", "end", values=row)
                tview.pack()
        messagebox.showinfo("FORWARD FILLING", "Forward Filling Applied" )

    def bfill_window(self):
        self.window_bfill = tk.Tk()
        self.window_bfill.title("BACKWARD FILLING")
        self.window_bfill.geometry("1100x550")
        self.window_bfill.configure(bg="#68838B")
    
        labe13 = tk.Label(self.window_bfill, text="BACKWARD FILLING METHOD", font=("italic", 20, "bold"), bg="#68838B", fg="white").place(x=250, y=30)
    
        exit_b = tk.Button(self.window_bfill, command=self.bfill_del, text=" EXIT ", font=("Century", 18), bg="white", fg="red")
        exit_b.place(x=150, y=450)
    
        save_b = tk.Button(self.window_bfill, command=self.bfill_save, text="SAVE", font=("Century", 18), bg="white", fg="black")
        save_b.place(x=250, y=450)

        self.selected_columns2 = self.get_selected_values()
        if self.selected_columns2:
            self.bfill_csv = self.csv_file.copy()
            self.bfill_csv[self.selected_columns2] = self.bfill_csv[self.selected_columns2].fillna(method="bfill")

            frame = Frame(self.window_bfill)
            frame.place(x=200, y=100, width=800, height=300)

            scroll1 = Scrollbar(frame, orient='vertical')
            scroll1.pack(side=RIGHT, fill=tk.Y)

            scroll2 = tk.Scrollbar(frame, orient='horizontal')
            scroll2.pack(side=tk.BOTTOM, fill=tk.X)

            global tview
            tview = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
            tview.pack()

            scroll1.config(command=tview.yview)
            scroll2.config(command=tview.xview)

            tview["columns"] = list(self.bfill_csv)
            tview["show"] = "headings"

            for column in tview["columns"]:
                tview.heading(column, text=column)

            df_rows = self.bfill_csv.to_numpy().tolist()

            for row in df_rows:
                tview.insert("", "end", values=row)
                tview.pack()
        messagebox.showinfo("BACKWARD FILLING", "Backward Filling Applied" )               

    def KNN_window(self):
        self.window_KNN = tk.Tk()
        self.window_KNN.title("KNN METHOD")
        self.window_KNN.geometry("1100x550")
        self.window_KNN.configure(bg="#68838B")

        label = tk.Label(self.window_KNN, text="KNN METHOD", font=("italic", 20, "bold"), bg="#68838B", fg="white").place(x=250, y=30)

        exit_KNN = tk.Button(self.window_KNN, command=self.KNN_del, text=" EXIT ", font=("Century", 18), bg="white", fg="red")
        exit_KNN.place(x=150, y=450)

        save_KNN = tk.Button(self.window_KNN, command=self.KNN_save, text="SAVE", font=("Century", 18), bg="white", fg="black")
        save_KNN.place(x=250, y=450)

        selected_columns = self.get_selected_values()

        if not selected_columns:
            print("No columns selected for analysis.")
            return

        numeric_columns = self.csv_file[selected_columns].select_dtypes(include=[np.number])

        if numeric_columns.empty:
            print("No numeric columns selected for KNN imputation.")
            return

    # Use KNNImputer on the selected numeric columns
        kn_imputer = KNNImputer(n_neighbors=2, weights='distance')
        data = kn_imputer.fit_transform(numeric_columns)

    # Replace the missing values in the original DataFrame with the imputed values
        self.KNN_csv = self.csv_file.copy()
        self.KNN_csv[selected_columns] = data

        print("KNN imputation applied to selected columns.")
        print(self.KNN_csv)

        frame = Frame(self.window_KNN)
        frame.place(x=200, y=100, width=800, height=300)

        scroll1 = Scrollbar(frame, orient='vertical')
        scroll1.pack(side=RIGHT, fill=tk.Y)

        scroll2 = tk.Scrollbar(frame, orient='horizontal')
        scroll2.pack(side=tk.BOTTOM, fill=tk.X)

        tview_KNN = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
        tview_KNN.pack()

        scroll1.config(command=tview_KNN.yview)
        scroll2.config(command=tview_KNN.xview)

        tview_KNN["columns"] = list(self.KNN_csv)
        tview_KNN["show"] = "headings"

        for column in tview_KNN["columns"]:
            tview_KNN.heading(column, text=column)

        df_rows_KNN = self.KNN_csv.to_numpy().tolist()

        for row in df_rows_KNN:
            tview_KNN.insert("", "end", values=row)
        messagebox.showinfo("KNN", "KNN Method Applied" )
                
    def drop_window(self):
        self.window_drop = tk.Tk()
        self.window_drop.title("DROP METHOD")
        self.window_drop.geometry("1100x550")
        self.window_drop.configure(bg="#68838B")

        label = tk.Label(self.window_drop, text="DROP METHOD", font=("italic", 20, "bold"), bg="#68838B", fg="white").place(x=250, y=30)

        exit_drop = tk.Button(self.window_drop, command=self.drop_del, text=" EXIT ", font=("Century", 18), bg="white", fg="red")
        exit_drop.place(x=150, y=450)

        save_drop = tk.Button(self.window_drop, command=self.drop_save, text="SAVE", font=("Century", 18), bg="white", fg="black")
        save_drop.place(x=250, y=450)

        selected_columns = self.get_selected_values()

        if not selected_columns:
            print("No columns selected for analysis.")
            return

        numeric_columns = self.csv_file[selected_columns].select_dtypes(include=[np.number])

        if numeric_columns.empty:
            print("No numeric columns selected for drop.")
            return

        self.drop_csv = self.csv_file.copy()
        self.drop_csv = self.drop_csv.dropna(subset=numeric_columns.columns)

        frame = Frame(self.window_drop)
        frame.place(x=200, y=100, width=800, height=300)

        scroll1 = Scrollbar(frame, orient='vertical')
        scroll1.pack(side=RIGHT, fill=tk.Y)

        scroll2 = tk.Scrollbar(frame, orient='horizontal')
        scroll2.pack(side=tk.BOTTOM, fill=tk.X)

        tview_drop = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
        tview_drop.pack()

        scroll1.config(command=tview_drop.yview)
        scroll2.config(command=tview_drop.xview)

        tview_drop["columns"] = list(self.drop_csv)
        tview_drop["show"] = "headings"

        for column in tview_drop["columns"]:
            tview_drop.heading(column, text=column)

        df_rows_drop = self.drop_csv.to_numpy().tolist()

        for row in df_rows_drop:
            tview_drop.insert("", "end", values=row)
        messagebox.showinfo("DROP", "Drop Method Applied" )

    def mean_window(self):
        self.window_mean = tk.Tk()
        self.window_mean.title("MEAN")
        self.window_mean.geometry("1100x550")
        self.window_mean.configure(bg="#68838B")
    
        label13 = tk.Label(self.window_mean, text="MEAN METHOD", font=("italic", 20, "bold"), bg="#68838B", fg="white").place(x=250, y=30)
    
        exit_mean = tk.Button(self.window_mean, command=self.mean_del, text=" EXIT ", font=("Century", 18), bg="white", fg="red")
        exit_mean.place(x=150, y=450)
    
        save_mean = tk.Button(self.window_mean, command=self.mean_save, text="SAVE", font=("Century", 18), bg="white", fg="black")
        save_mean.place(x=250, y=450)
    
        selected_columns = self.get_selected_values()
        if not selected_columns:
            print("No columns selected for analysis.")
            return
    
        mean_csv = self.csv_file.copy()
        numeric_columns = mean_csv[selected_columns].select_dtypes(include=[np.number])
    
        if numeric_columns.empty:
            print("No numeric columns selected for mean imputation.")
            return
    
        mean_values = SimpleImputer(strategy='mean')
        data = mean_values.fit_transform(numeric_columns)
    
        mean_csv[selected_columns] = data
    
        frame = Frame(self.window_mean)
        frame.place(x=200, y=100, width=800, height=300)
    
        scroll1 = Scrollbar(frame, orient='vertical')
        scroll1.pack(side=RIGHT, fill=tk.Y)
    
        scroll2 = tk.Scrollbar(frame, orient='horizontal')
        scroll2.pack(side=tk.BOTTOM, fill=tk.X)
    
        tview = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
        tview.pack()
    
        scroll1.config(command=tview.yview)
        scroll2.config(command=tview.xview)
    
        tview["columns"] = list(mean_csv)
        tview["show"] = "headings"
    
        for column in tview["columns"]:
            tview.heading(column, text=column)
    
        df_rows = mean_csv.to_numpy().tolist()
    
        for row in df_rows:
            tview.insert("", "end", values=row)
            tview.pack()
        messagebox.showinfo("MEAN", "Mean Method Applied" )
        self.window_mean.mainloop()



    def median_window(self):
        self.window_median = tk.Tk()
        self.window_median.title("MEDIAN")
        self.window_median.geometry("1100x550")
        self.window_median.configure(bg="#68838B")
        
        labe13 = tk.Label(self.window_median, text="MEDIAN METHOD", font=("italic", 20, "bold"), bg="#68838B", fg="white").place(x=250, y=30)
    
        exit_b = tk.Button(self.window_median, command=self.median_del, text=" EXIT ", font=("Century", 18), bg="white", fg="red")
        exit_b.place(x=150, y=450)
    
        save_b = tk.Button(self.window_median, command=self.median_save, text="SAVE", font=("Century", 18), bg="white", fg="black")
        save_b.place(x=250, y=450)

        selected_columns = self.get_selected_values()
        if not selected_columns:
            print("No columns selected for analysis.")
            return

        self.median_csv = self.csv_file.copy()
        numeric_columns = self.median_csv[selected_columns].select_dtypes(include=[np.number])

        if numeric_columns.empty:
            print("No numeric columns selected for median imputation.")
            return

        median_values = SimpleImputer(strategy='median')
        data = median_values.fit_transform(numeric_columns)

        self.median_csv[selected_columns] = data


        frame = Frame(self.window_median)
        frame.place(x=200, y=100, width=800, height=300)

        scroll1 = Scrollbar(frame, orient='vertical')
        scroll1.pack(side=RIGHT, fill=tk.Y)

        scroll2 = tk.Scrollbar(frame, orient='horizontal')
        scroll2.pack(side=tk.BOTTOM, fill=tk.X)

        global tview
        tview = ttk.Treeview(frame, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set)
        tview.pack()

        scroll1.config(command=tview.yview)
        scroll2.config(command=tview.xview)

        tview["columns"] = list(self.median_csv)
        tview["show"] = "headings"

        for column in tview["columns"]:
            tview.heading(column, text=column)

        df_rows = self.median_csv.to_numpy().tolist()

        for row in df_rows:
            tview.insert("", "end", values=row)
        messagebox.showinfo("MEDIAN", "Median Method Applied" )
        # Move the pack() method outside the loop
        tview.pack()

        self.window_median.mainloop()
        
    

proce = Preprocess()
