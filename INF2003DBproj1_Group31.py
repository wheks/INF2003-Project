import sys
import mariadb
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import ttkbootstrap as ttkb


#Global connection settings
conn = None
cur = None

def connect_to_mariadb():
    global conn, cur
    try:
        conn = mariadb.connect(
            host='localhost',
            user='Username',
            password='Password',
            database='INF2003DBproj1',
            port=3306
        )
        cur = conn.cursor()
        print("Successfully connected to MariaDB")
    except mariadb.Error as e:
        print(f'Error connecting to MariaDB Platform: {e}')
        messagebox.showerror("Database Error", f"Failed to connect: {e}")
        sys.exit(1)

#SQLAlchemy connection for pandas
db_connection_str = 'mysql+pymysql://Username:Password@localhost:3306/INF2003DBproj1'
engine = create_engine(db_connection_str)

def analyse_airline_popularity():
    global conn, cur
    try:
        #First, let's check the structure of the Airlines table
        cur.execute("DESCRIBE Airlines")
        columns = [column[0] for column in cur.fetchall()]
        print("Airlines table columns:", columns)

        #Modify the query based on the actual column names
        query = """
        SELECT a.aid AS Airline_ID, COUNT(p.pid) AS Passenger_Count
        FROM Airlines a
        LEFT JOIN Passenger p ON a.aid = p.aid
        GROUP BY a.aid
        ORDER BY Passenger_Count DESC
        """
        #Execute the query using the existing cursor
        cur.execute(query)
        results = cur.fetchall()

        #Convert results to a pandas DataFrame
        airline_pop_df = pd.DataFrame(results, columns=['Airline_ID', 'Passenger_Count'])

        #Sort the DataFrame by Passenger_Count in descending order
        airline_pop_df = airline_pop_df.sort_values('Passenger_Count', ascending=False)

        #Output the DataFrame to console for debugging
        print(airline_pop_df)

        #Plot the horizontal bar chart for airline popularity
        plt.figure(figsize=(8, 5))  
        plt.barh(airline_pop_df['Airline_ID'].astype(str),
                 airline_pop_df['Passenger_Count'],
                 color='skyblue')
        plt.title('Airline Popularity Based on Passenger Count')
        plt.xlabel('Number of Passengers')
        plt.ylabel('Airline ID')
        plt.gca().invert_yaxis()  
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        
        #Find the most popular airline
        if not airline_pop_df.empty:
            most_popular_airline = airline_pop_df.iloc[0]
            messagebox.showinfo("Most Popular Airline",
                                f"The most popular airline (ID: {most_popular_airline['Airline_ID']}) "
                                f"has {most_popular_airline['Passenger_Count']} passengers.")
        else:
            messagebox.showinfo("No Data", "No airline popularity data available.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while analyzing airline popularity: {e}")
        print(f"Detailed error: {e}")  

def analyse_tourism_duration():
    global conn, cur
    try:
        #SQL query to get length of stay (lid) and passenger count
        query = """
        SELECT p.lid, COUNT(p.pid) AS passenger_count
        FROM Passenger AS p
        JOIN Length_Of_Stay AS l ON p.lid = l.lid
        GROUP BY p.lid
        ORDER BY passenger_count DESC;
        """

        #Execute the query
        cur.execute(query)
        results = cur.fetchall()

        if not results:
            messagebox.showinfo("No Data", "No tourism duration data available.")
            return

        #Extract data for plotting
        lids = [row[0] for row in results]
        passenger_counts = [row[1] for row in results]

        #Plotting a horizontal bar chart
        plt.figure(figsize=(8, 5))
        plt.barh(lids, passenger_counts, color='skyblue')
        plt.xlabel("Number of Passengers")
        plt.ylabel("Length of Stay (LID)")
        plt.title("Number of Passengers per Length of Stay")
        plt.gca().invert_yaxis()  
        plt.tight_layout()

        #Find the most common length of stay
        most_common_lid = lids[0]
        most_common_count = passenger_counts[0]

        #Show the plot
        plt.show()

        #Display a message box with the most common length of stay
        messagebox.showinfo("Tourism Duration Analysis",
                            f"The most common length of stay (LID: {most_common_lid}) "
                            f"has {most_common_count} passengers.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while analyzing tourism duration: {e}")
        print(f"Detailed error: {e}")  

def analyse_airline_trend():
    global conn, cur, engine  #Reuse existing connections and engine from your app
    
    try:
        #Define the SQL query
        query = """
        SELECT
            countries.cid AS country,
            airlines.aid AS airline,
            COUNT(passenger.pid) AS passenger_count
        FROM
            passenger
        JOIN
            countries ON passenger.cid = countries.cid
        JOIN
            airlines ON passenger.aid = airlines.aid
        GROUP BY
            countries.cid,
            airlines.aid
        ORDER BY
            countries.cid,
            airlines.aid;
        """
        
        #Execute the query and store results in a DataFrame using SQLAlchemy engine for pandas
        data = pd.read_sql(query, engine)  # Reuse SQLAlchemy engine

        #Check if data is empty
        if data.empty:
            messagebox.showinfo("No Data", "No trend data available for airline and country.")
            return

        #Print data to the console for debugging
        print(data.head())

        #Create the bar plot using matplotlib
        plt.figure(figsize=(8, 5))
        for airline in data['airline'].unique():
            subset = data[data['airline'] == airline]
            plt.bar(subset['country'], subset['passenger_count'], label=f'Airline {airline}')

        #Customize the plot
        plt.title('Passenger Count per Airline and Country')
        plt.xlabel('Country')
        plt.ylabel('Passenger Count')
        plt.xticks(rotation=45)
        plt.legend(framealpha=0.8,bbox_to_anchor=[1, 0.8])
        plt.tight_layout()

        #Show the plot
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while analyzing airline trends: {e}")
        print(f"Detailed error: {e}")

#Function to get existing tables
def get_existing_tables():
    cur.execute("SHOW TABLES")
    return [table[0] for table in cur.fetchall()]

#Utility functions
def get_valid_options(table, column):
    cur.execute(f"SELECT DISTINCT {column} FROM {table}")
    return [str(row[0]) for row in cur.fetchall()]

#Functions to get dropdown options
def get_gender_options():
    return ['M', 'F', 'NB']

def get_lid_options():
    return get_valid_options('length_of_stay', 'lid')

def get_aid_options():
    return get_valid_options('airlines', 'aid')

def get_cid_options():
    return get_valid_options('countries', 'cid')

def validate_foreign_key(table, column, value):
    cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} = ?", (value,))
    return cur.fetchone()[0] > 0

def get_valid_options(table, column):
    cur.execute(f"SELECT {column} FROM {table}")
    return [row[0] for row in cur.fetchall()]

def increment_counter(table, id_column, count_column, value):
    cur.execute(f"SELECT {count_column} FROM {table} WHERE {id_column} = ?", (value,))
    result = cur.fetchone()

    if result:
        cur.execute(f"UPDATE {table} SET {count_column} = {count_column} + 1 WHERE {id_column} = ?", (value,))
    else:
        cur.execute(f"INSERT INTO {table} ({id_column}, {count_column}) VALUES (?, 1)", (value,))

def decre_counter(table, id_column, count_column, value):
    cur.execute(f"UPDATE {table} SET {count_column} = GREATEST({count_column} - 1, 0) WHERE {id_column} = ?", (value,))

#CRUD operations
def create_passenger(name, age, gender, lid, aid, cid, window):
    #Validate foreign keys before proceeding with passenger creation
    if not validate_foreign_key("length_of_stay", "lid", lid):
        messagebox.showerror("Constraint Error", "Invalid Length of Stay ID. Please select a valid option.")
        return False
    if not validate_foreign_key("airlines", "aid", aid):
        messagebox.showerror("Constraint Error", "Invalid Airline ID. Please select a valid option.")
        return False
    if not validate_foreign_key("countries", "cid", cid):
        messagebox.showerror("Constraint Error", "Invalid Country ID. Please select a valid option.")
        return False

    #Retrieve the maximum PID value from the database
    cur.execute("SELECT COALESCE(MAX(pid), 0) + 1 FROM passenger")
    new_pid = cur.fetchone()[0]

    new_info = """INSERT INTO passenger (pid, name, lid, age, gender, aid, cid)
                  VALUES (?, ?, ?, ?, ?, ?, ?)"""

    try:
        cur.execute("START TRANSACTION")
        cur.execute(new_info, (new_pid, name, lid, int(age), gender, aid, cid))
        increment_counter("length_of_stay", "lid", "loscount", lid)
        increment_counter("airlines", "aid", "acount", aid)
        increment_counter("countries", "cid", "ccount", cid)
        conn.commit()
        print('Successfully created new passenger')

        #Close the window upon successful creation
        window.destroy()
        return True
    except mariadb.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        messagebox.showerror("Error", f"Failed to create new passenger")
        return False

def read_passenger(search_criteria=None):
    query = "SELECT * FROM passenger"
    params = []
    if search_criteria:
        conditions = []
        for key, value in search_criteria.items():
            if key == 'id':  
                key = 'pid'  
            conditions.append(f"{key} = ?")
            params.append(value)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    try:
        cur.execute(query, params)
        results = cur.fetchall()
        if not results:
            messagebox.showinfo("Info", "No passengers found matching the criteria.")
            return []
        columns = [column[0] for column in cur.description]
        return [dict(zip(columns, row)) for row in results]
    except mariadb.Error as e:
        messagebox.showerror("Error", f"Error reading passenger information: {e}")
        return []

def update_passenger(pid, updates):
    #First, retrieve the current passenger details
    cur.execute("SELECT lid, aid, cid FROM passenger WHERE pid = ?", (pid,))
    current_passenger = cur.fetchone()

    if not current_passenger:
        print(f"No passenger found with PID {pid}")
        return False

    current_lid, current_aid, current_cid = current_passenger

    #Start transaction
    cur.execute("START TRANSACTION")

    try:
        set_clauses = []
        values = []
        for key, value in updates.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)

        query = f"UPDATE passenger SET {', '.join(set_clauses)} WHERE pid = ?"
        values.append(pid)

        cur.execute(query, values)

        #Update counters
        if 'lid' in updates and updates['lid'] != current_lid:
            decre_counter("length_of_stay", "lid", "loscount", current_lid)
            increment_counter("length_of_stay", "lid", "loscount", updates['lid'])

        if 'aid' in updates and updates['aid'] != current_aid:
            decre_counter("airlines", "aid", "acount", current_aid)
            increment_counter("airlines", "aid", "acount", updates['aid'])

        if 'cid' in updates and updates['cid'] != current_cid:
            decre_counter("countries", "cid", "ccount", current_cid)
            increment_counter("countries", "cid", "ccount", updates['cid'])

        conn.commit()

        messagebox.showinfo("Success", f"Successfully updated passenger with ID {pid}")
        return True

    except mariadb.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error updating passenger: {e}")
        return False

def del_passenger(pid): #Delete passenger function
    try:
        #Fetch the passenger record first to check if it exists and retrieve its related information
        cur.execute("SELECT lid, aid, cid FROM passenger WHERE pid = ?", (pid,))
        passenger = cur.fetchone()
        
        if not passenger:
            print(f"No passenger found with PID {pid}")
            return False

        lid, aid, cid = passenger

        #Start transaction
        cur.execute("START TRANSACTION")

        #Delete the passenger
        cur.execute("DELETE FROM passenger WHERE pid = ?", (pid,))

        #Decrement counters
        decre_counter("length_of_stay", "lid", "loscount", lid)
        decre_counter("airlines", "aid", "acount", aid)
        decre_counter("countries", "cid", "ccount", cid)

        conn.commit()

        messagebox.showinfo("Success", f"Successfully deleted passenger with ID {pid}")
        return True

    except mariadb.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error deleting passenger: {e}")
        return False

#GUI functions
def open_create_passen_window(): #Open Create passenger window
    create_window = ttkb.Toplevel(root)
    create_window.title("Create New Passenger")
    create_window.geometry("400x400")

    frame = ttkb.Frame(create_window, padding=20)
    frame.pack(expand=True, fill='both')

    ttkb.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    name_entry = ttkb.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttkb.Label(frame, text="Age:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    age_entry = ttkb.Entry(frame)
    age_entry.grid(row=1, column=1, padx=5, pady=5)

    ttkb.Label(frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    gender_combobox = ttkb.Combobox(frame, values=get_gender_options())
    gender_combobox.grid(row=2, column=1, padx=5, pady=5)

    ttkb.Label(frame, text="Length of Stay ID:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    lid_combobox = ttkb.Combobox(frame, values=get_lid_options())
    lid_combobox.grid(row=3, column=1, padx=5, pady=5)

    ttkb.Label(frame, text="Airline ID:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    aid_combobox = ttkb.Combobox(frame, values=get_aid_options())
    aid_combobox.grid(row=4, column=1, padx=5, pady=5)

    ttkb.Label(frame, text="Country ID:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
    cid_combobox = ttkb.Combobox(frame, values=get_cid_options())
    cid_combobox.grid(row=5, column=1, padx=5, pady=5)

    ttkb.Button(frame, text="Create Passenger", style='primary.TButton',
                command=lambda: create_passenger(
                    name_entry.get(), age_entry.get(), gender_combobox.get(),
                    lid_combobox.get(), aid_combobox.get(), cid_combobox.get(),
                    create_window 
                )).grid(row=6, column=0, columnspan=2, pady=20)

def open_read_passen_window(): #Open read passenger window
    read_window = tk.Toplevel(root)
    read_window.title("Read Passenger Details")
    read_window.geometry("500x400")

    tk.Label(read_window, text="Search by:").pack()
    search_by = tk.StringVar(read_window)
    search_by.set("All")

    #Function to handle the visibility of the search bar and drop-downs based on the selection
    def update_search_options(*args):
        search_entry.pack_forget()
        lid_combobox.pack_forget()
        aid_combobox.pack_forget()
        cid_combobox.pack_forget()

        if search_by.get() == "PID" or search_by.get() == "Name":
            search_entry.pack()
        elif search_by.get() == "LID":
            lid_combobox.pack()
        elif search_by.get() == "AID":
            aid_combobox.pack()
        elif search_by.get() == "CID":
            cid_combobox.pack()

    search_by.trace('w', update_search_options)
    tk.OptionMenu(read_window, search_by, "All", "PID", "Name", "LID", "AID", "CID").pack()

    #Widgets for input based on search type
    search_entry = tk.Entry(read_window)
    lid_combobox = ttk.Combobox(read_window, values=get_lid_options())
    aid_combobox = ttk.Combobox(read_window, values=get_aid_options())
    cid_combobox = ttk.Combobox(read_window, values=get_cid_options())

    #Frame to contain the Text widget and scrollbar
    frame = tk.Frame(read_window)
    frame.pack(fill='both', expand=True)

    #Text widget with scrollbar for displaying results
    result_text = tk.Text(frame, wrap='word', height=10, width=50)
    scrollbar = tk.Scrollbar(frame, command=result_text.yview)
    result_text.configure(yscrollcommand=scrollbar.set)
    result_text.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    def perfrm_search(): #Perform search function
        search_criteria = {}
        if search_by.get() == "PID":
            search_criteria['pid'] = search_entry.get()
        elif search_by.get() == "Name":
            search_criteria['name'] = search_entry.get()
        elif search_by.get() == "LID":
            search_criteria['lid'] = lid_combobox.get()
        elif search_by.get() == "AID":
            search_criteria['aid'] = aid_combobox.get()
        elif search_by.get() == "CID":
            search_criteria['cid'] = cid_combobox.get()

        results = read_passenger(search_criteria if search_by.get() != "All" else None)

        #Display the results
        result_text.delete('1.0', tk.END)
        for passenger in results:
            result_text.insert(tk.END, f"\nPassenger Information:\n")
            for key, value in passenger.items():
                result_text.insert(tk.END, f"{key}: {value}\n")
            result_text.insert(tk.END, "-" * 30 + "\n")

    tk.Button(read_window, text="Search", command=perfrm_search).pack()

def open_update_passen_window():
    update_window = tk.Toplevel(root)
    update_window.title("Update Passenger")

    tk.Label(update_window, text="Passenger ID:").grid(row=0, column=0, padx=5, pady=5)
    pid_entry = tk.Entry(update_window)
    pid_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Name:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = tk.Entry(update_window)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Age:").grid(row=2, column=0, padx=5, pady=5)
    age_entry = tk.Entry(update_window)
    age_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Gender:").grid(row=3, column=0, padx=5, pady=5)
    gender_combobox = ttk.Combobox(update_window, values=get_gender_options())
    gender_combobox.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Length of Stay ID:").grid(row=4, column=0, padx=5, pady=5)
    lid_combobox = ttk.Combobox(update_window, values=get_lid_options())
    lid_combobox.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Airline ID:").grid(row=5, column=0, padx=5, pady=5)
    aid_combobox = ttk.Combobox(update_window, values=get_aid_options())
    aid_combobox.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Country ID:").grid(row=6, column=0, padx=5, pady=5)
    cid_combobox = ttk.Combobox(update_window, values=get_cid_options())
    cid_combobox.grid(row=6, column=1, padx=5, pady=5)

    def perfrm_update(): #Performs updates
        updates = {}
        if name_entry.get(): updates['name'] = name_entry.get()
        if age_entry.get(): updates['age'] = int(age_entry.get())
        if gender_combobox.get(): updates['gender'] = gender_combobox.get()
        if lid_combobox.get(): updates['lid'] = lid_combobox.get()
        if aid_combobox.get(): updates['aid'] = aid_combobox.get()
        if cid_combobox.get(): updates['cid'] = cid_combobox.get()

        if updates:
            update_passenger(pid_entry.get(), updates)
        else:
            messagebox.showinfo("Info", "No updates provided.")

    tk.Button(update_window, text="Update Passenger", command=perfrm_update).grid(row=7, column=0, columnspan=2,
                                                                                   pady=10)

def open_del_passen_window(): #Opens delete window
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Passenger")

    tk.Label(delete_window, text="Passenger ID:").pack()
    pid_entry = tk.Entry(delete_window)
    pid_entry.pack()

    def perfrm_delete(): #Perform delete function
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete passenger with ID {pid_entry.get()}?"):
            del_passenger(pid_entry.get())

    tk.Button(delete_window, text="Delete Passenger", command=perfrm_delete).pack()

#Main menu function
def op_main_menu():
    clear_frame(root)

    tk.Label(root, text="Passenger Management System").pack(pady=10)

    tk.Button(root, text="Create New Passenger", command=open_create_passen_window).pack(pady=5)
    tk.Button(root, text="Read Passenger Details", command=open_read_passen_window).pack(pady=5)
    tk.Button(root, text="Update Passenger", command=open_update_passen_window).pack(pady=5)
    tk.Button(root, text="Delete Passenger", command=open_del_passen_window).pack(pady=5)

    #Aalysis buttons
    tk.Button(root, text="Analyse Airline Popularity", command=analyse_airline_popularity).pack(pady=5)
    tk.Button(root, text="Analyse Tourism Duration", command=analyse_tourism_duration).pack(pady=5)
    tk.Button(root, text="Analyse Airline Trend", command=analyse_airline_trend).pack(pady=5)

#Function to clear all widgets in a given frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#Initialize GUI
root = tk.Tk()
root.title("Passenger Management System")

#Establish the connection
connect_to_mariadb()

#Print existing tables
print("Existing tables:", get_existing_tables())

#Start with the main menu
op_main_menu()

#Start main loop
root.geometry("400x400")
root.mainloop()