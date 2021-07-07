import openpyxl
 
workbook = openpyxl.load_workbook('torihiki.xlsx')
sheet = workbook["Sheet1"]
suppliers = []
 
for i in range(3,9):
    cell_value = sheet.cell(row=i, column=2).value
 
    if cell_value not in suppliers:
        suppliers.append(cell_value)
 
 
print(suppliers)
