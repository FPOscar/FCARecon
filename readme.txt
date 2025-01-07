# NEX-FCA Data Comparison Tool

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
  - [Installation](#installation)
- [Input File Requirements](#input-file-requirements)
- [Usage](#usage)
- [Output](#output)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [License](#license)

## Description
This tool processes and compares financial transaction data from NEX CSV files against FCA XML data. It performs automated checks on key fields, generates detailed comparison reports, and outputs the results in an Excel workbook.

## Features
- Combines multiple NEX CSV files into a single dataset.
- Parses FCA XML files with a specified schema.
- Validates transaction references automatically.
- Compares key fields between NEX and FCA data.
- Generates a comprehensive Excel report with:
  - Combined NEX data.
  - Parsed FCA data.
  - Detailed check results.
  - Summary statistics.

## Requirements
- Python 3.x
- Required packages:
  - `pandas`
  - `xlsxwriter`
  - `xml.etree.ElementTree` (built-in)

### Installation
To install the required Python packages, run the following command:
```bash
pip install pandas xlsxwriter
```

## Input File Requirements
### 1. NEX Data:
- CSV files located in a specified folder.
- Must contain required columns, including:
  - Transaction Reference Number
  - Executing Entity Identification Code
  - Trading Date Time
  - Quantity
  - Price
  - Instrument Identification Code
  - Trading Venue
  - Transmission of Order Indicator
  - Buyer Code
  - Seller Code

### 2. FCA Data:
- XML file following the FCA schema.
- Must contain corresponding transaction data with matching IDs.

## Usage
1. Place your NEX CSV files in a folder.
2. Ensure your FCA XML file is ready.
3. Update the following variables in the script:
   ```python
   csv_folder = "Abide CSV files"
   xml_file = "FCA XML file/FCA.xml"
   output_file = "output_file_with_checks_and_summary.xlsx"
   ```
4. Run the script:
   ```bash
   python <script_name>.py
   ```

## Output
The script generates an Excel workbook with four sheets:
1. **NEX Data**: Combined data from all CSV files.
2. **FCA Data**: Parsed data from the XML file.
3. **Check Results**: Field-by-field comparison results.
4. **Summary**: Statistical overview of the comparison.

## Error Handling
- Transaction reference validation issues are logged to `transaction_reference_validation.log`.
- Missing required columns raise a `KeyError` with specific column information.
- Data type mismatches are handled automatically with appropriate conversions.

## Notes
- The script uses vectorized operations for improved performance with large datasets.
- Decimal precision is maintained for financial calculations.
- Special handling is implemented for date/time fields and numerical comparisons.

## License
This project is licensed under the [MIT License](LICENSE).

