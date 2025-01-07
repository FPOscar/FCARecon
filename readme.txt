NEX-FCA Data Comparison Tool
===========================

Description
-----------
This tool processes and compares financial transaction data from NEX CSV files against FCA XML data. It performs automated checks on key fields, generates detailed comparison reports, and outputs the results in an Excel workbook.

Features
--------
- Combines multiple NEX CSV files into a single dataset
- Parses FCA XML files with specified schema
- Performs automated validation of transaction references
- Compares key fields between NEX and FCA data
- Generates comprehensive Excel report with:
  * Combined NEX data
  * Parsed FCA data
  * Detailed check results
  * Summary statistics

Requirements
------------
- Python 3.x
- Required packages:
  * pandas
  * xlsxwriter
  * xml.etree.ElementTree (built-in)

Input File Requirements
---------------------
1. NEX Data:
   - CSV files in specified folder
   - Must contain required columns including:
     * Transaction Reference Number
     * Executing Entity Identification Code
     * Trading Date Time
     * Quantity
     * Price
     * Instrument Identification Code
     * Trading Venue
     * Transmission of Order Indicator
     * Buyer Code
     * Seller Code

2. FCA Data:
   - XML file following FCA schema
   - Must contain corresponding transaction data with matching IDs

Usage
-----
1. Place your NEX CSV files in a folder
2. Have your FCA XML file ready
3. Update the following variables in the script:
   ```python
   csv_folder = "Abide CSV files"
   xml_file = "FCA XML file/FCA.xml"
   output_file = "output_file_with_checks_and_summary.xlsx"
   ```
4. Run the script:
   ```python
   python script_name.py
   ```

Output
------
The script generates an Excel workbook with four sheets:
1. NEX data: Combined data from all CSV files
2. FCA data: Parsed data from the XML file
3. Check Results: Field-by-field comparison results
4. Summary: Statistical overview of the comparison

Error Handling
-------------
- Transaction reference validation issues are logged to 'transaction_reference_validation.log'
- Missing required columns will raise KeyError with specific column information
- Data type mismatches are handled automatically with appropriate conversions

Notes
-----
- The script uses vectorized operations for improved performance with large datasets
- Decimal precision is maintained for financial calculations
- Special handling is implemented for date/time fields and numerical comparisons
```