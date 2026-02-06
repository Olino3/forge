---
name: excel-skills
description: Masters spreadsheet manipulation across Excel, Google Sheets, and LibreOffice Calc. Analyzes spreadsheet structure, generates formulas, creates pivot tables, performs data transformations, and automates workflows with VBA/Apps Script/Python (openpyxl/pandas). Like Hephaestus crafting precision instruments, this skill transforms raw data into organized, actionable insights through the power of spreadsheet mastery.
---

# Spreadsheet Manipulation Master

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 4-step workflow outlined in this document MUST be followed in exact order for EVERY spreadsheet task. Skipping steps or deviating from the procedure will result in ineffective or incorrect spreadsheet solutions. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different spreadsheet tasks and generated solutions
- **../../memory/skills/excel-skills/**: Project-specific memory storage
  - `{project-name}/`: Per-project spreadsheet patterns and conventions
- **templates/**:
  - `formula_template.md`: Standard formula output format template
  - `macro_template.md`: VBA/Apps Script macro template
  - `analysis_template.md`: Data analysis report template

## Focus Areas

Spreadsheet manipulation evaluates 7 critical dimensions:

1. **Formula Engineering**: Create robust formulas using appropriate functions (VLOOKUP, INDEX-MATCH, SUMIFS, array formulas, etc.)
2. **Data Structure Analysis**: Understand existing spreadsheet layouts, identify data patterns, and detect inconsistencies
3. **Automation Design**: Generate VBA macros, Google Apps Script, or Python scripts (openpyxl, pandas, xlwings) for repetitive tasks
4. **Data Transformation**: Clean, reshape, and normalize data for analysis or reporting
5. **Visualization**: Design charts, conditional formatting, and dashboards for data presentation
6. **Performance Optimization**: Avoid volatile functions, minimize array formula complexity, and optimize calculation speed
7. **Cross-Platform Compatibility**: Ensure solutions work across Excel, Google Sheets, and LibreOffice when required

**Note**: The skill generates formulas, macros, and automation scripts for the user to implement. It does not directly manipulate spreadsheet files unless integrated with appropriate tools.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Understand the Spreadsheet Context (REQUIRED)

**YOU MUST:**
1. Determine the **spreadsheet platform**: Excel (Windows/Mac), Google Sheets, LibreOffice Calc, or platform-agnostic
2. Identify the **current data structure**: column headers, data types, table dimensions, named ranges
3. Clarify the **task objective**: formula creation, data transformation, automation, analysis, visualization
4. Assess **skill level** of the user: beginner (needs explanations), intermediate (familiar with formulas), advanced (VBA/scripting capable)
5. Ask clarifying questions if context is incomplete:
   - What does your current spreadsheet look like? (Column headers, sample data)
   - What specific result are you trying to achieve?
   - Are there any existing formulas or macros in the workbook?
   - Should this work in a specific version of Excel or be Google Sheets compatible?
   - Do you prefer formulas or would you like a macro/script solution?

**DO NOT PROCEED WITHOUT UNDERSTANDING THE SPREADSHEET STRUCTURE AND OBJECTIVE**

### ⚠️ STEP 2: Analyze Data and Requirements (REQUIRED)

**YOU MUST:**
1. **Map the data structure**: Identify source columns, lookup tables, calculation dependencies
2. **Determine the approach**:
   - **Formula-based**: Use built-in functions for one-time calculations or dynamic references
   - **Macro-based**: Use VBA/Apps Script for repetitive tasks, batch operations, or UI automation
   - **Python-based**: Use openpyxl/pandas for complex data transformations, large datasets, or integration with other tools
3. **Identify constraints**:
   - Performance: Will this run on large datasets? (>10,000 rows)
   - Compatibility: Must it work across platforms or specific versions?
   - Maintenance: Will non-technical users need to modify this?
4. **Check project memory**: Look in `../../memory/skills/excel-skills/{project-name}/` for project-specific conventions, naming patterns, or existing formulas
5. **Plan the solution structure**: Break complex tasks into steps, identify helper columns if needed

**DO NOT PROCEED WITHOUT A CLEAR SOLUTION APPROACH**

### ⚠️ STEP 3: Generate the Solution (REQUIRED)

**YOU MUST:**
1. **For Formulas**:
   - Use absolute references (`$A$1`) where appropriate for fixed cells
   - Use relative references (`A1`) for cells that should adjust when copied
   - Prefer INDEX-MATCH over VLOOKUP for flexibility and performance
   - Use structured references (Table[@Column]) when working with Excel Tables
   - Add error handling with IFERROR or IFNA where appropriate
   - Break complex formulas into intermediate columns for readability
   - Add comments explaining the logic

2. **For Macros/Scripts**:
   - VBA (Excel): Use Option Explicit, declare variable types, add error handling
   - Apps Script (Google Sheets): Use modern JavaScript syntax, handle permissions
   - Python (openpyxl/pandas): Use virtual environments, handle file paths properly
   - Include comments explaining each section
   - Add user prompts or confirmation dialogs for destructive operations

3. **For Data Transformations**:
   - Document before/after structure clearly
   - Preserve original data or create a backup
   - Validate transformations with test data
   - Handle edge cases (empty cells, duplicates, invalid data)

4. **Use templates** from `templates/` for consistent output formatting

**DO NOT USE DEPRECATED FUNCTIONS OR UNSAFE PRACTICES**

### ⚠️ STEP 4: Validate and Document (REQUIRED)

**YOU MUST validate the solution against these criteria:**
1. **Correctness check**:
   - [ ] Formula produces expected results for sample data
   - [ ] Edge cases handled (empty cells, zeros, errors, text in numeric fields)
   - [ ] No circular references introduced
   - [ ] Array formulas entered correctly (Ctrl+Shift+Enter in older Excel)

2. **Performance check**:
   - [ ] No volatile functions (NOW, TODAY, RAND, OFFSET) unless necessary
   - [ ] Formulas calculate efficiently for expected dataset size
   - [ ] Macros don't cause screen flicker (Application.ScreenUpdating = False in VBA)

3. **Compatibility check**:
   - [ ] Functions are available in target platform/version
   - [ ] No platform-specific behavior (e.g., Google Sheets QUERY vs Excel Power Query)

4. **Documentation**:
   - [ ] Provide step-by-step implementation instructions
   - [ ] Explain what the formula/macro does and why
   - [ ] Include example use cases and expected output
   - [ ] Note any prerequisites (enable macros, install libraries)

5. **Present the solution** to the user with clear implementation steps
6. **Offer alternatives**: Provide 2-3 alternative approaches when applicable (e.g., formula vs. macro, VLOOKUP vs. INDEX-MATCH)

**DO NOT SKIP VALIDATION**

**OPTIONAL: Update Project Memory**

If project-specific patterns are discovered during the process, store insights in `../../memory/skills/excel-skills/{project-name}/`:
- Common column naming conventions
- Recurring formula patterns
- Standard data validation rules
- Preferred automation approaches

---

## Compliance Checklist

Before completing ANY spreadsheet task, verify:
- [ ] Step 1: Spreadsheet context understood — platform, structure, objective, user skill level
- [ ] Step 2: Data and requirements analyzed — approach determined, constraints identified
- [ ] Step 3: Solution generated — formula/macro/script created with proper syntax and error handling
- [ ] Step 4: Solution validated — correctness, performance, compatibility checked; documentation provided

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SOLUTION**

---

## Common Spreadsheet Tasks

### Formula Generation
- **Lookup operations**: VLOOKUP, INDEX-MATCH, XLOOKUP (Excel 365)
- **Conditional calculations**: SUMIF(S), COUNTIF(S), AVERAGEIF(S)
- **Text manipulation**: CONCATENATE/TEXTJOIN, LEFT/RIGHT/MID, TRIM, UPPER/LOWER
- **Date/Time**: DATE, DATEDIF, EOMONTH, NETWORKDAYS, TEXT formatting
- **Array formulas**: SUMPRODUCT, array constants, dynamic arrays (Excel 365)
- **Statistical**: STDEV, CORREL, PERCENTILE, MEDIAN

### Data Transformation
- **Cleaning**: Remove duplicates, trim whitespace, fix data types, split/merge columns
- **Reshaping**: Transpose, unpivot (Power Query), pivot, stack/unstack
- **Filtering**: Advanced filters, dynamic filtering (Excel 365), FILTER function
- **Sorting**: Multi-level sorts, custom sort orders, dynamic sorting

### Automation
- **VBA Macros**: Batch operations, form controls, custom functions (UDFs), workbook events
- **Google Apps Script**: Triggers, custom menus, data import from APIs, email notifications
- **Python Integration**: openpyxl (read/write), pandas (analysis), xlwings (live Excel connection)

### Visualization
- **Charts**: Line, bar, scatter, combo charts, sparklines
- **Conditional formatting**: Color scales, data bars, icon sets, formula-based rules
- **Dashboards**: Slicers, pivot tables, named ranges, dynamic charts

---

## Platform-Specific Considerations

### Excel (Windows/Mac)
- **Strengths**: VBA automation, Power Query, Power Pivot, rich charting, Excel Tables
- **Limitations**: License cost, file size limits, desktop-only (unless Excel Online)
- **Version differences**: Excel 365 has dynamic arrays, XLOOKUP; older versions need array formula syntax

### Google Sheets
- **Strengths**: Free, cloud-based, real-time collaboration, Apps Script automation, Google API integration
- **Limitations**: 10M cell limit per spreadsheet, slower performance for complex formulas, no VBA
- **Unique functions**: QUERY (SQL-like), IMPORTRANGE, GOOGLEFINANCE, GOOGLETRANSLATE

### LibreOffice Calc
- **Strengths**: Free, open-source, cross-platform, supports Excel file formats
- **Limitations**: Smaller user community, fewer advanced features, Basic macros instead of VBA
- **Compatibility**: Most Excel formulas work, but VBA macros require conversion to LibreOffice Basic

---

## Further Reading

Refer to official documentation:
- **Excel**:
  - Excel Functions Reference: https://support.microsoft.com/en-us/excel
  - VBA Documentation: https://docs.microsoft.com/en-us/office/vba/api/overview/excel
- **Google Sheets**:
  - Function List: https://support.google.com/docs/table/25273
  - Apps Script: https://developers.google.com/apps-script
- **Python Libraries**:
  - openpyxl: https://openpyxl.readthedocs.io/
  - pandas: https://pandas.pydata.org/docs/
  - xlwings: https://docs.xlwings.org/
- **Best Practices**:
  - Chandoo's Excel Tips: https://chandoo.org/
  - Contextures Excel Tips: https://www.contextures.com/

---

## Version History

- v1.0.0 (2026-02-06): Initial release
  - Mandatory 4-step workflow for spreadsheet tasks
  - Support for Excel, Google Sheets, LibreOffice Calc
  - Formula generation, macro creation, data transformation
  - Project memory integration for pattern persistence
  - Template-based output formatting
