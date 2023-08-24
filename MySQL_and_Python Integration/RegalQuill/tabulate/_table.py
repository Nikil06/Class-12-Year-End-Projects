import csv

class Table:
    def __init__(self, columns):
        self.columns = columns
        self.data = []

    def add_row(self, row_data):
        if len(row_data) != len(self.columns):
            print("Error: Number of columns in the row does not match the table.")
            return
        self.data.append(row_data)

    def display(self):
        header = " | ".join(self.columns)
        print(header)
        print("-" * len(header))
        for row in self.data:
            row_str = " | ".join(map(str, row))
            print(row_str)

    def get_data(self, row_index, column_index=None, column_name=None):
        if column_index is not None:
            return self.data[row_index][column_index]
        elif column_name in self.columns:
            return self.data[row_index][self.columns.index(column_name)]
        else:
            print("Error: Column not found.")
            return None

    def update_data(self, row_index, column_index=None, column_name=None, new_value=None):
        if column_index is not None:
            self.data[row_index][column_index] = new_value
        elif column_name in self.columns:
            self.data[row_index][self.columns.index(column_name)] = new_value
        else:
            print("Error: Column not found.")

    def sort_by_column(self, column_name):
        if column_name in self.columns:
            index = self.columns.index(column_name)
            self.data.sort(key=lambda x: x[index])

    def filter_by_column(self, column_name, condition):
        if column_name in self.columns:
            index = self.columns.index(column_name)
            self.data = [row for row in self.data if condition(row[index])]

    def remove_row(self, row_index):
        if 0 <= row_index < len(self.data):
            del self.data[row_index]
        else:
            print("Error: Invalid row index.")

    def save_to_csv(self, file_name):
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.columns)
            writer.writerows(self.data)

    def load_from_csv(self, file_name):
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.columns = next(reader)
            self.data = [row for row in reader]

# Example usage:
my_table = Table(["Name", "Age", "City"])

my_table.add_row(["Alice", 25, "New York"])
my_table.add_row(["Bob", 30, "San Francisco"])
my_table.add_row(["Charlie", 22, "Los Angeles"])

my_table.display()
print()

my_table.sort_by_column("Age")
my_table.display()
print()

my_table.filter_by_column("City", lambda x: x == "New York")
my_table.display()
print()

my_table.display()
print()

my_table.save_to_csv("my_table.csv")
my_table.load_from_csv("my_table.csv")
my_table.display()
