import os
import tkinter
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import xlsxwriter

# Defining a class to represent a schedule in list data strucuture
class ScheduleList:
    def __init__(self, name, description, date, days, start_time, end_time, duration, location, staff_name):
        self.name = name
        self.description = description
        self.date = date
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.location = location
        self.staff_name = staff_name

    def __str__(self):
        return f"Date: {self.date}, Day: {self.days}, Start Time: {self.start_time}, End Time: {self.end_time}, " \
               f"Module Name: {self.name}, Session Name: {self.description}, Location: {self.location}, " \
               f"Duration: {self.duration}, Staff Name: {self.staff_name}"

# Function to load & preprocess data from CSV files in a folder 
def load_data(folder_path):
    schedules = []  
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(csv_file_path)
                for _, row in df.iterrows():
                    if (row['Scheduled Days'] != "unchecked" and
                        row['Scheduled Start Time'] != "unchecked" and
                        row['Scheduled End Time'] != "unchecked"):
                        schedule = ScheduleList(
                            row["Name"],
                            row["Description"],
                            row["Activity Dates (Individual)"],
                            row["Scheduled Days"],
                            row["Scheduled Start Time"],
                            row["Scheduled End Time"],
                            row["Duration"],
                            row["Allocated Location Name"],
                            row["Allocated Staff Name"],
                        )
                        schedules.append(schedule)
            except Exception as e:
                print("Error processing", filename, ":", str(e))
    return schedules

# Function to sort schedules based on date and time
def sort_schedules(schedules, ascending=True):
    # Define a sorting function that combines date and time
    def custom_sort_key(schedule):
        date_time_str = f"{schedule.date} {schedule.start_time}"
        
        # Adjust the format string to include the extra :00
        date_time = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')
        
        return date_time

    # Sort schedules based on the custom_sort_key using the key parameter
    sorted_schedules = sorted(schedules, key=custom_sort_key, reverse=not ascending)

    return sorted_schedules

# Function to search schedules based on keywords
def search_schedules(schedules, keywords):
    results = []
    for schedule in schedules:
        schedule_str = str(schedule).lower()
        if all(keyword.lower() in schedule_str for keyword in keywords):
            results.append(schedule)
    return results

# Function to search schedules based on Lecturer Name
def search_schedules_by_lecturer(schedules, lecturer_name):
    return [schedule for schedule in schedules if schedule.staff_name == lecturer_name]

# Function to search schedules based on Lecturer Name
def search_schedules_by_classroom(schedules, classroom_name):
    return [schedule for schedule in schedules if schedule.location == classroom_name]

def search_schedules_by_module(schedules, module_name):
    return [schedule for schedule in schedules if schedule.name == module_name]

# Function to filter schedules by date range
def search_by_date_range(schedules, start_date, end_date):
    if not start_date and not end_date:
        return schedules

    filtered_schedules = []
    for schedule in schedules:
        if start_date and end_date:
            schedule_date = datetime.strptime(schedule.date, '%d/%m/%Y')
            if start_date <= schedule_date <= end_date:
                filtered_schedules.append(schedule)
        elif start_date:
            schedule_date = datetime.strptime(schedule.date, '%d/%m/%Y')
            if schedule_date >= start_date:
                filtered_schedules.append(schedule)
        elif end_date:
            schedule_date = datetime.strptime(schedule.date, '%d/%m/%Y')
            if schedule_date <= end_date:
                filtered_schedules.append(schedule)
    return filtered_schedules

# Function to filter schedules by time range
def search_by_time_range(schedules, start_time, end_time):
    if not start_time and not end_time:
        return schedules

    filtered_schedules = []
    for schedule in schedules:
        if start_time and end_time:
            if start_time <= schedule.start_time <= end_time:
                filtered_schedules.append(schedule)
        elif start_time:
            if schedule.start_time >= start_time:
                filtered_schedules.append(schedule)
        elif end_time:
            if schedule.end_time <= end_time:
                filtered_schedules.append(schedule)
    return filtered_schedules

# Function to export schedules to an Excel file
def export_timetable_to_excel(schedules, output_filename):
    workbook = xlsxwriter.Workbook(output_filename)
    worksheet = workbook.add_worksheet()

    # Write column headings
    headings = ["Module Name", "Session Name", "Date", "Day", "Start Time", "End Time", "Duration", "Location", "Staff Name"]
    for col, heading in enumerate(headings):
        worksheet.write(0, col, heading)

    # Write schedule data
    for row, schedule in enumerate(schedules, start=1):
        worksheet.write(row, 0, schedule.name)
        worksheet.write(row, 1, schedule.description)
        worksheet.write(row, 2, schedule.date)
        worksheet.write(row, 3, schedule.days)
        worksheet.write(row, 4, schedule.start_time)
        worksheet.write(row, 5, schedule.end_time)
        worksheet.write(row, 6, schedule.duration)
        worksheet.write(row, 7, schedule.location)
        worksheet.write(row, 8, schedule.staff_name)

    workbook.close()
    
    tkinter.messagebox.showinfo("Success", "Exported to Excel successfully.")

def create_gui():
    def handle_search():
        keywords = []

        try:
            # Get keywords from the entry fields
            lecturer_name = lecturer_entry.get()
            keywords.extend(lecturer_name.split())

            module_name = module_entry.get()
            keywords.extend(module_name.split())

            location = location_entry.get()
            keywords.extend(location.split())

            day = day_entry.get()
            keywords.extend(day.split())

            ascending = sort_order_var.get() == 1

            # Process start and end dates
            start_date_str = start_date_entry.get()
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y') if start_date_str else None

            end_date_str = end_date_entry.get()
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y') if end_date_str else None

            # Process start and end times
            start_time_range = start_time_range_entry.get()
            if start_time_range:
                start_time = datetime.strptime(start_time_range, '%H:%M').time()
            else:
                start_time = None

            end_time_range = end_time_range_entry.get()
            if end_time_range:
                end_time = datetime.strptime(end_time_range, '%H:%M').time()
            else:
                end_time = None

            if start_date and end_date and start_date > end_date:
                raise ValueError("Start Date cannot be greater than End Date")

            # Filter schedules by date range
            filtered_by_date = search_by_date_range(schedules, start_date, end_date)

            # Filter schedules by time range
            filtered_by_time = search_by_time_range(filtered_by_date, start_time, end_time)

            # Search and filter schedules based on keywords
            results = search_schedules(filtered_by_time, keywords)

            # Clear the existing treeview items
            for item in result_tree.get_children():
                result_tree.delete(item)

            if results:
                results = sort_schedules(results, ascending)
                for result in results:
                    result_tree.insert("", "end", values=(result.name, result.description, result.date, result.days,
                                                        result.start_time, result.end_time, result.duration,
                                                        result.location, result.staff_name))
            else:
                result_text.set("No schedules found.")

            # Export to Excel if specified
            if export_excel_var.get():
                export_timetable_to_excel(results, "c:\\Coventry University\Algorithms and Data Structures\\Project App\\timetable.xlsx")

        except ValueError as e:
            # Display an error message to the user
            result_text.set(f"Error: {str(e)}")

        except Exception as e:
            # Handle other exceptions and display a general error message
            result_text.set(f"An error occurred: {str(e)}")

    window = tk.Tk()
    window.title("Timetable Application")

    style = ttk.Style()
    style.configure("TButton", foreground="white", background="black")
    style.configure("TLabel", foreground="white", background="black")
    style.configure("Treeview", background="black", fieldbackground="black", foreground="white")

    export_excel_var = tk.IntVar()

    # Create labels and entry fields for each search field
    lecturer_label = tk.Label(window, text="Enter Lecturer Name:")
    lecturer_label.pack()
    lecturer_entry = tk.Entry(window)
    lecturer_entry.pack()

    module_label = tk.Label(window, text="Enter Module Name:")
    module_label.pack()
    module_entry = tk.Entry(window)
    module_entry.pack()

    location_label = tk.Label(window, text="Enter Location/Room Name:")
    location_label.pack()
    location_entry = tk.Entry(window)
    location_entry.pack()

    start_date_label = tk.Label(window, text="Enter Start Date (dd/mm/yyyy):")
    start_date_label.pack()
    start_date_entry = tk.Entry(window)
    start_date_entry.pack()

    end_date_label = tk.Label(window, text="Enter End Date (dd/mm/yyyy):")
    end_date_label.pack()
    end_date_entry = tk.Entry(window)
    end_date_entry.pack()

    start_time_range_label = tk.Label(window, text="Enter Start Time (hh:mm):")
    start_time_range_label.pack()
    start_time_range_entry = tk.Entry(window)
    start_time_range_entry.pack()

    end_time_range_label = tk.Label(window, text="Enter End Time (hh:mm):")
    end_time_range_label.pack()
    end_time_range_entry = tk.Entry(window)
    end_time_range_entry.pack()

    day_label = tk.Label(window, text="Enter Day (e.g., Monday):")
    day_label.pack()
    day_entry = tk.Entry(window)
    day_entry.pack()

    sort_order_var = tk.IntVar()
    ascending_radio = tk.Radiobutton(window, text="Earliest First", variable=sort_order_var, value=1)
    descending_radio = tk.Radiobutton(window, text="Latest First", variable=sort_order_var, value=0)

    ascending_radio.pack()
    descending_radio.pack()

    search_button = tk.Button(window, text="Search/Sort", command=handle_search)
    search_button.pack(pady=12)

    # Checkbuttons for exporting to Excel
    export_excel_var = tk.IntVar()
    export_excel_checkbutton = tk.Checkbutton(window, text="Export to Excel", variable=export_excel_var)
    export_excel_checkbutton.pack()


    # Create a widget to display the results in a table-like format
    result_tree = ttk.Treeview(window, columns=("Module Name", "Session Name", "Date", "Day", "Start Time",
                                                "End Time", "Duration", "Location", "Staff Name"), show="headings")

    # Define column headings
    result_tree.heading("Module Name", text="Module Name")
    result_tree.heading("Session Name", text="Session Name")
    result_tree.heading("Date", text="Date")
    result_tree.heading("Day", text="Day")
    result_tree.heading("Start Time", text="Start Time")
    result_tree.heading("End Time", text="End Time")
    result_tree.heading("Duration", text="Duration")
    result_tree.heading("Location", text="Location")
    result_tree.heading("Staff Name", text="Staff Name")

    # Define column widths
    result_tree.column("Module Name", width=150)
    result_tree.column("Session Name", width=150)
    result_tree.column("Date", width=150)
    result_tree.column("Day", width=150)
    result_tree.column("Start Time", width=150)
    result_tree.column("End Time", width=150)
    result_tree.column("Duration", width=150)
    result_tree.column("Location", width=150)
    result_tree.column("Staff Name", width=150)

    result_tree.pack()

    result_text = tk.StringVar()
    result_label = tk.Label(window, textvariable=result_text)
    result_label.pack()

    window.mainloop()

if __name__ == "__main__":
    folder_path_1 = "C:\Datasets\dataset"  # Path to the first dataset folder
    folder_path_2 = "C:\Datasets\dataset 2020"  # Path to the second dataset folder

    print("Loading data from dataset 1:", folder_path_1)
    schedules_1 = load_data(folder_path_1)
    print("Data loaded from dataset 1:", len(schedules_1), "schedules")

    print("Loading data from dataset 2:", folder_path_2)
    schedules_2 = load_data(folder_path_2)
    print("Data loaded from dataset 2:", len(schedules_2), "schedules")

    # Combine schedules from both datasets
    schedules = schedules_1 + schedules_2

    create_gui()