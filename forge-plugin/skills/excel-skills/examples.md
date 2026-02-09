# Excel Skills Examples

This file contains example scenarios demonstrating how to use the excel-skills skill to solve common spreadsheet manipulation tasks.

---

## Example 1: VLOOKUP vs INDEX-MATCH for Product Pricing

### Scenario
User has a product catalog in Sheet1 with Product ID in column A and Price in column D. They need to look up prices in Sheet2 based on Product ID.

### User Prompt
```
I need to look up product prices from my catalog sheet. Product IDs are in column A of the catalog, prices in column D. In my order sheet, I have product IDs in column B and need prices in column E.
```

### Skill Execution

**Step 1 - Understand Context**:
- **Platform**: Excel (unspecified version, assume 2016+)
- **Structure**: 
  - Sheet1 (Catalog): Column A = Product ID, Column D = Price
  - Sheet2 (Orders): Column B = Product ID, Column E = needs Price
- **Objective**: Lookup formula to retrieve prices
- **User skill**: Intermediate (familiar with VLOOKUP)

**Step 2 - Analyze Requirements**:
- **Data structure**: Lookup column (A) is left of return column (D), so VLOOKUP works
- **Approach**: Provide both VLOOKUP (familiar) and INDEX-MATCH (better practice)
- **Constraints**: Should handle missing products gracefully

**Step 3 - Generate Solution**:

### Generated Solutions

#### Solution A: VLOOKUP (Traditional Approach)

**Formula for cell E2 in Orders sheet:**
```excel
=IFERROR(VLOOKUP(B2,Sheet1!$A:$D,4,FALSE),"Not Found")
```

**Explanation:**
- `B2`: Product ID to look up
- `Sheet1!$A:$D`: Range containing lookup table (A = lookup column, D = 4th column)
- `4`: Return value from 4th column (D)
- `FALSE`: Exact match required
- `IFERROR(...,"Not Found")`: Display "Not Found" if product doesn't exist

**Implementation:**
1. Click cell E2 in Orders sheet
2. Enter the formula above
3. Press Enter
4. Drag the formula down to apply to all order rows

**Pros**: Simple, widely understood
**Cons**: Breaks if columns are inserted between A and D; always searches from left to right

---

#### Solution B: INDEX-MATCH (Recommended)

**Formula for cell E2 in Orders sheet:**
```excel
=IFERROR(INDEX(Sheet1!$D:$D,MATCH(B2,Sheet1!$A:$A,0)),"Not Found")
```

**Explanation:**
- `MATCH(B2,Sheet1!$A:$A,0)`: Find the row number where B2 appears in column A
- `INDEX(Sheet1!$D:$D,...)`: Return the value from column D at that row number
- `IFERROR(...,"Not Found")`: Handle missing products

**Implementation:**
1. Click cell E2 in Orders sheet
2. Enter the formula above
3. Press Enter
4. Drag the formula down to apply to all order rows

**Pros**: More flexible (can lookup left), won't break if columns are inserted, often faster
**Cons**: Slightly more complex syntax

---

**Step 4 - Validate**:
- ✅ Both formulas handle missing products with "Not Found"
- ✅ Absolute references ($) prevent column references from shifting when copied
- ✅ MATCH with 0 ensures exact match (not approximate)
- ✅ Works with any dataset size

---

## Example 2: Conditional Sum with Multiple Criteria

### Scenario
User has a sales data table with Date (column A), Region (column B), Product (column C), and Amount (column D). They need to sum sales for a specific region and product combination.

### User Prompt
```
Sum all sales amounts where Region is "West" and Product is "Widget A"
```

### Skill Execution

**Step 1 - Understand Context**:
- **Platform**: Excel or Google Sheets (formula works in both)
- **Structure**: Columns A-D with sales data
- **Objective**: Conditional sum with two criteria
- **User skill**: Beginner (needs explanation)

**Step 2 - Analyze Requirements**:
- **Approach**: Use SUMIFS function (multiple criteria sum)
- **Constraints**: None mentioned

**Step 3 - Generate Solution**:

### Generated Solution

**Formula:**
```excel
=SUMIFS(D:D, B:B, "West", C:C, "Widget A")
```

**Explanation:**
- `D:D`: Sum range (Amount column)
- `B:B, "West"`: First criterion - Region must be "West"
- `C:C, "Widget A"`: Second criterion - Product must be "Widget A"

**Implementation:**
1. Click any empty cell where you want the result
2. Type the formula above
3. Press Enter

**Making it Dynamic:**
If you want to change the region and product without editing the formula, put "West" in cell F1 and "Widget A" in cell G1, then use:

```excel
=SUMIFS(D:D, B:B, F1, C:C, G1)
```

Now changing F1 or G1 will update the sum automatically.

**Step 4 - Validate**:
- ✅ SUMIFS handles any number of matching rows (0 to thousands)
- ✅ Criteria are case-sensitive in Excel, case-insensitive in Google Sheets
- ✅ Returns 0 if no matches found (not an error)
- ✅ Full column references (D:D) auto-expand as data grows

---

## Example 3: Remove Duplicates and Clean Data with VBA

### Scenario
User has a large customer database with 50,000 rows containing duplicate entries, extra spaces in names, and inconsistent capitalization. They need to clean this data regularly.

### User Prompt
```
I have a huge customer list with duplicates and messy data. Names have extra spaces, some are all caps, some lowercase. I need to clean this up weekly. Columns are: A=Customer ID, B=Name, C=Email, D=Phone
```

### Skill Execution

**Step 1 - Understand Context**:
- **Platform**: Excel (VBA mentioned as preferred for automation)
- **Structure**: 4 columns, 50,000+ rows
- **Objective**: Automated data cleaning
- **User skill**: Intermediate (comfortable running macros)

**Step 2 - Analyze Requirements**:
- **Approach**: VBA macro for batch operations (faster than formulas for 50K rows)
- **Tasks**: Remove duplicates, trim spaces, normalize capitalization
- **Constraints**: Performance matters with large dataset

**Step 3 - Generate Solution**:

### Generated VBA Macro

```vba
Sub CleanCustomerData()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    
    ' Disable screen updating for better performance
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    ' Set the worksheet (change "Sheet1" to your actual sheet name)
    Set ws = ThisWorkbook.Sheets("Sheet1")
    
    ' Find the last row with data
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    ' Clean Name column (B): Trim spaces and proper case
    For i = 2 To lastRow ' Start at 2 to skip header row
        If ws.Cells(i, 2).Value <> "" Then
            ws.Cells(i, 2).Value = Application.WorksheetFunction.Proper(Trim(ws.Cells(i, 2).Value))
        End If
    Next i
    
    ' Clean Email column (C): Trim and lowercase
    For i = 2 To lastRow
        If ws.Cells(i, 3).Value <> "" Then
            ws.Cells(i, 3).Value = LCase(Trim(ws.Cells(i, 3).Value))
        End If
    Next i
    
    ' Clean Phone column (D): Trim only
    For i = 2 To lastRow
        If ws.Cells(i, 4).Value <> "" Then
            ws.Cells(i, 4).Value = Trim(ws.Cells(i, 4).Value)
        End If
    Next i
    
    ' Remove duplicates based on Customer ID (column A)
    ws.Range("A1:D" & lastRow).RemoveDuplicates Columns:=1, Header:=xlYes
    
    ' Re-enable screen updating
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    
    MsgBox "Data cleaned successfully! Duplicates removed based on Customer ID.", vbInformation
End Sub
```

**Implementation Steps:**

1. **Open VBA Editor**: Press `Alt + F11` in Excel
2. **Insert Module**: Click Insert → Module
3. **Paste Code**: Copy the macro above into the module window
4. **Modify Sheet Name**: Change "Sheet1" to match your actual sheet name (line 12)
5. **Close VBA Editor**: Press `Alt + Q` or click the X
6. **Run the Macro**:
   - Press `Alt + F8`
   - Select `CleanCustomerData`
   - Click Run

**What It Does:**
1. Turns off screen updating for speed
2. Finds the last row with data automatically
3. Applies Proper Case to names (John Smith instead of JOHN SMITH or john smith)
4. Converts emails to lowercase and trims spaces
5. Trims spaces from phone numbers
6. Removes duplicate rows based on Customer ID
7. Shows a completion message

**Safety Note**: This modifies data in place. **Always save a backup before running** or test on a copy first.

**Step 4 - Validate**:
- ✅ Screen updating disabled = much faster on large datasets
- ✅ Handles empty cells without errors
- ✅ Uses Excel's built-in RemoveDuplicates (fast and reliable)
- ✅ User gets confirmation when complete
- ⚠️ **Important**: User should test on a copy first

---

## Example 4: Dynamic Dashboard with Named Ranges and Charts

### Scenario
User wants to create a sales dashboard that updates automatically when data changes. They have monthly sales data and want dropdown filters for Year and Region.

### User Prompt
```
Create a dashboard where I can select a year and region from dropdowns, and the charts update automatically to show sales for that selection.
```

### Skill Execution

**Step 1 - Understand Context**:
- **Platform**: Excel (assuming 2016+)
- **Structure**: Sales data in a table, need dropdown filters
- **Objective**: Interactive dashboard with dynamic charts
- **User skill**: Intermediate

**Step 2 - Analyze Requirements**:
- **Approach**: Excel Tables + slicers (or data validation dropdowns) + formulas + charts
- **Components**: Dropdown cells, filtered data range, charts linked to filtered data
- **Constraints**: Must update automatically when selection changes

**Step 3 - Generate Solution**:

### Generated Solution: Multi-Step Dashboard Setup

#### Part 1: Set Up the Data Table

1. **Convert your data range to an Excel Table**:
   - Select your sales data (including headers)
   - Press `Ctrl + T` or go to Insert → Table
   - Check "My table has headers"
   - Click OK
   - Name the table "SalesData" (Table Design → Table Name)

#### Part 2: Create Dropdown Controls

2. **Create dropdown cells**:
   - Cell G2: Year selector
   - Cell G4: Region selector

3. **Add data validation dropdowns**:
   - For Year (G2):
     - Select cell G2
     - Go to Data → Data Validation
     - Allow: List
     - Source: =UNIQUE(SalesData[Year]) **(Excel 365)** or manually type: 2022,2023,2024,2025
     - Click OK
   
   - For Region (G4):
     - Select cell G4
     - Data → Data Validation
     - Allow: List
     - Source: =UNIQUE(SalesData[Region]) **(Excel 365)** or manually type: North,South,East,West
     - Click OK

#### Part 3: Create Filtered Summary Table

4. **Build a summary table that responds to dropdowns**:

| Cell | Formula | Purpose |
|------|---------|---------|
| I2   | `=G2`   | Display selected year |
| I3   | `=G4`   | Display selected region |
| I5   | `=SUMIFS(SalesData[Amount], SalesData[Year], G2, SalesData[Region], G4)` | Total Sales |
| I6   | `=COUNTIFS(SalesData[Year], G2, SalesData[Region], G4)` | Number of Transactions |
| I7   | `=AVERAGEIFS(SalesData[Amount], SalesData[Year], G2, SalesData[Region], G4)` | Average Sale |

#### Part 4: Create Dynamic Chart

5. **Create a chart linked to filtered data**:
   - If you want a monthly breakdown, create a helper table:
   
```excel
Month | Sales
------|------
Jan   | =SUMIFS(SalesData[Amount], SalesData[Year], $G$2, SalesData[Region], $G$4, SalesData[Month], "Jan")
Feb   | =SUMIFS(SalesData[Amount], SalesData[Year], $G$2, SalesData[Region], $G$4, SalesData[Month], "Feb")
...
```

6. **Insert a column or line chart**:
   - Select your month/sales helper table
   - Insert → Chart → Column Chart
   - The chart will automatically update when you change the dropdown selections

#### Part 5: Add Visual Polish

7. **Format the dashboard**:
   - Add labels: "Select Year:", "Select Region:"
   - Use bold fonts and borders for dropdown cells
   - Color-code the summary metrics
   - Add a title: "Sales Dashboard"

**Step 4 - Validate**:
- ✅ Dropdowns update summary metrics automatically
- ✅ Chart responds to dropdown changes
- ✅ Formulas handle cases where no data matches selection (returns 0, not error)
- ✅ Excel Tables auto-expand when new data is added

**Alternative (Excel 365)**: Use FILTER function for more advanced scenarios:
```excel
=FILTER(SalesData, (SalesData[Year]=G2)*(SalesData[Region]=G4))
```

---

## Example 5: Batch File Processing with Python (openpyxl)

### Scenario
User has 100 Excel files from different departments, all with the same structure. They need to combine all files into a single master spreadsheet and add a "Department" column indicating the source file.

### User Prompt
```
I have 100 Excel files in a folder, each named like "Sales_Marketing.xlsx", "Sales_Engineering.xlsx", etc. Each has the same columns: Date, Product, Amount. I need to combine them all into one file with an extra column showing which department each row came from.
```

### Skill Execution

**Step 1 - Understand Context**:
- **Platform**: Python (openpyxl + pandas) - Excel has limits for this task
- **Structure**: 100 files, same column structure
- **Objective**: Merge files with source tracking
- **User skill**: Advanced (comfortable with Python)

**Step 2 - Analyze Requirements**:
- **Approach**: Python script using pandas (best for merging CSVs/Excel files)
- **Constraints**: Files must have consistent structure

**Step 3 - Generate Solution**:

### Generated Python Script

```python
import pandas as pd
import os
from pathlib import Path

# Configuration
input_folder = r"C:\path\to\your\sales_files"  # Change this to your folder path
output_file = r"C:\path\to\output\combined_sales.xlsx"  # Change this to desired output path

# Initialize empty list to store dataframes
all_data = []

# Loop through all Excel files in the folder
for file_path in Path(input_folder).glob("*.xlsx"):
    # Extract department name from filename (e.g., "Sales_Marketing.xlsx" -> "Marketing")
    department = file_path.stem.replace("Sales_", "")
    
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Add a Department column
    df['Department'] = department
    
    # Append to our list
    all_data.append(df)
    
    print(f"Processed: {file_path.name} ({len(df)} rows)")

# Combine all dataframes
combined_df = pd.concat(all_data, ignore_index=True)

# Save to Excel
combined_df.to_excel(output_file, index=False)

print(f"\nSuccess! Combined {len(all_data)} files into {output_file}")
print(f"Total rows: {len(combined_df)}")
```

**Implementation Steps:**

1. **Install Required Libraries** (if not already installed):
   ```bash
   pip install pandas openpyxl
   ```

2. **Save the Script**:
   - Copy the code above into a file named `combine_sales.py`

3. **Modify Paths**:
   - Line 5: Set `input_folder` to the folder containing your 100 Excel files
   - Line 6: Set `output_file` to where you want the combined file saved

4. **Run the Script**:
   ```bash
   python combine_sales.py
   ```

5. **Verify**:
   - Open the generated `combined_sales.xlsx`
   - Check that all data is present
   - Verify the Department column correctly identifies each row's source

**What It Does:**
1. Scans the input folder for all `.xlsx` files
2. For each file:
   - Extracts the department name from the filename
   - Reads all data
   - Adds a "Department" column with the extracted name
3. Combines all data into a single dataframe
4. Saves the result to a new Excel file

**Optional Enhancements:**

**Add Error Handling:**
```python
try:
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"Error reading {file_path.name}: {e}")
    continue
```

**Filter by Date Range:**
```python
# After reading the file:
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'] >= '2024-01-01']
```

**Add Summary Statistics:**
```python
# After combining:
summary = combined_df.groupby('Department')['Amount'].agg(['sum', 'mean', 'count'])
print("\nSummary by Department:")
print(summary)
```

**Step 4 - Validate**:
- ✅ Handles any number of files in the folder
- ✅ Department name extraction is flexible
- ✅ Uses `ignore_index=True` to avoid duplicate index values
- ✅ Reports progress so user knows it's working
- ⚠️ **Note**: Very large files (>1M rows total) may need chunking

---

## Summary of Spreadsheet Task Types

1. **Lookup Formula** (`VLOOKUP` / `INDEX-MATCH`) — Retrieve related data from lookup tables
2. **Conditional Sum** (`SUMIFS`) — Aggregate data with multiple criteria
3. **VBA Automation** — Batch data cleaning and transformation
4. **Interactive Dashboard** — Dropdowns, dynamic formulas, and charts
5. **Python Batch Processing** — Combine multiple files programmatically

## Best Practices

- **Formulas**: Use INDEX-MATCH over VLOOKUP for flexibility and performance
- **Error Handling**: Always wrap formulas in IFERROR to handle missing data gracefully
- **References**: Use $ for absolute references when you don't want them to shift when copied
- **Macros**: Disable screen updating (`Application.ScreenUpdating = False`) for performance
- **Python**: Use pandas for data manipulation and openpyxl for Excel file I/O
- **Testing**: Always test on a copy of your data before running destructive operations
- **Documentation**: Comment complex formulas and macros so you remember what they do
- **Performance**: Avoid entire column references (A:A) in formulas if your dataset is small and fixed
- **Compatibility**: Check if functions are available in your Excel version or platform (Google Sheets vs Excel)
