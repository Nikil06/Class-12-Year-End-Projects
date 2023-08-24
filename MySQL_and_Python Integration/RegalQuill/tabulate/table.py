from enum import Enum, auto


class TableStyles(Enum):
    Simple = auto()
    SQL_Style = auto()


class Table:
    def __init__(self, rows, headers=None):
        self.headers = headers
        self.rows = rows

        self.number_of_columns = 0
        self.column_widths = []
        self.table_data = []

        self._update_table_info()

    def _get_column_index(self, column_name: str):
        if self.headers is None:
            raise ValueError("cant index from column name for undefined header.")

        if column_name in self.headers:
            return self.headers.index(column_name)
        else:
            raise ValueError(f"column of name : {column_name} does not exist.")

    def _update_table_info(self):
        if self.headers is None:
            num_of_cols = len(self.rows[0])
            data = [*self.rows]
        else:
            num_of_cols = len(self.headers)
            data = [self.headers, *self.rows]

        self.number_of_columns = num_of_cols
        self.table_data = data

    def add_row(self, row):
        if len(row) != self.number_of_columns:
            raise ValueError("Number of columns in the row does not match the table.")
        else:
            self.rows.append(row)
            self._update_table_info()

    def get_cell(self, row_idx, col_idx=None, col_name=None):
        if col_idx is not None:
            return self.rows[row_idx][col_idx]
        elif col_name is not None:
            return self.rows[row_idx][self._get_column_index(col_name)]
        else:
            raise ValueError("cant get cell from unknown column.")

    def update_cell(self, row_idx, col_idx=None, col_name=None, new_value=None):
        if col_idx is not None:
            self.rows[row_idx][col_idx] = new_value
            self._update_table_info()
        elif col_name is not None:
            self.rows[row_idx][col_idx] = new_value
            self._update_table_info()
        else:
            raise ValueError("cant get cell from unknown column.")

    def remove_row(self, row_idx):
        if 0 <= row_idx < len(self.rows):
            del self.rows[row_idx]
            self._update_table_info()
        else:
            raise ValueError("Error: Invalid row index.")

    def get_render(self, style: TableStyles):
        return RenderTable(self, style).get_render()


class RenderTable:
    def __init__(self, table: Table, style: TableStyles):
        self.rows = table.rows
        self.headers = table.headers
        self.style = style

        self.number_of_columns = table.number_of_columns
        self.column_widths = table.column_widths

        self._map_to_str()

    def _map_to_str(self):

        self.headers = list(map(str, self.headers))

        for i, row in enumerate(self.rows):
            self.rows[i] = list(map(str, row))

        col_widths = [0] * self.number_of_columns

        if self.headers is not None:
            data = [self.headers, *self.rows]
        else:
            data = [*self.rows]

        for row in data:
            for j, cell in enumerate(row):
                if len(cell) > col_widths[j]:
                    col_widths[j] = len(cell)

        self.column_widths = col_widths

    def get_render(self):
        if self.style == TableStyles.Simple:
            return self.render_simple()
        elif self.style == TableStyles.SQL_Style:
            return self.render_sql_style()

    def render_simple(self):
        col_sep = ['| ', ' | ', ' |']
        row_sep = [' ', '=', ' ']
        rows = []
        seperator = row_sep[0] + (sum(self.column_widths) + len(col_sep[1]) * self.number_of_columns - 1) * row_sep[1] + \
                    row_sep[2]
        if self.headers:
            header_row = [f"{self.headers[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            header = col_sep[0] + col_sep[1].join(header_row) + col_sep[2]
            rows += [seperator, header, seperator]
        else:
            rows += [seperator]

        for row in self.rows:
            row_data = [f"{row[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            rows.append(col_sep[0] + col_sep[1].join(row_data) + col_sep[2])

        rows += [seperator]

        return "\n".join(rows)

    def render_sql_style(self):
        col_sep = ['| ', ' | ', ' |']
        row_sep = ['+-', '-', '-+']
        rows = []
        seperator = row_sep[0] + (sum(self.column_widths) + len(col_sep[1]) * self.number_of_columns - 3) * row_sep[1] + \
                    row_sep[2]
        if self.headers:
            header_row = [f"{self.headers[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            header = col_sep[0] + col_sep[1].join(header_row) + col_sep[2]
            rows += [seperator, header, seperator]
        else:
            rows += [seperator]

        for row in self.rows:
            row_data = [f"{row[i]:<{self.column_widths[i]}}" for i in range(self.number_of_columns)]
            rows.append(col_sep[0] + col_sep[1].join(row_data) + col_sep[2])

        rows += [seperator]

        return "\n".join(rows)


if __name__ == "__main__":
    my_table = Table(headers=["Name", "Target IIT", "Target Branch"], rows=[
        ["Nikil", "Madras", "C.S."],
        ["Deepak", "Delhi", "Mech."],
        ["Karthik", "Bombay", "Chem"],
        ["ShriRam", "Madras", "AeroSpace"]
    ])

    render = RenderTable(my_table, style=TableStyles.Simple)
    print(render.render_simple())
    print()
    print(render.render_sql_style())
