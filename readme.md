# NEX-FCA Data Comparison Tool

A Python tool for processing and comparing financial transaction data from NEX CSV files against FCA XML data. The tool performs automated validation checks, generates detailed comparison reports, and outputs results in a comprehensive Excel workbook.

## Features

- **Multi-file Processing**: Combines multiple NEX CSV files into a single dataset
- **XML Schema Parsing**: Parses FCA XML files with specified schema validation
- **Automated Validation**: Performs transaction reference validation and field comparison
- **Comprehensive Reporting**: Generates detailed Excel reports with multiple worksheets
- **Error Handling**: Robust logging and error management for data processing issues

## Requirements

### System Requirements
- Python 3.x

### Dependencies
```bash
pip install pandas xlsxwriter
```

**Note**: `xml.etree.ElementTree` is included with Python's standard library.

## Input File Requirements

### NEX Data (CSV Format)
- **Location**: CSV files in a specified folder
- **Required Columns**:
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

### FCA Data (XML Format)
- **Format**: XML file following FCA schema
- **Content**: Transaction data with matching IDs corresponding to NEX data

## Installation & Setup

1. **Clone or download** the script to your local machine
2. **Install dependencies**:
   ```bash
   pip install pandas xlsxwriter
   ```
3. **Prepare your data files**:
   - Place NEX CSV files in a designated folder
   - Ensure FCA XML file is accessible

## Usage

### Configuration
Update the following variables in the script before running:

```python
csv_folder = "Abide CSV files"           # Path to NEX CSV files
xml_file = "FCA XML file/FCA.xml"        # Path to FCA XML file
output_file = "output_file_with_checks_and_summary.xlsx"  # Output file name
```

### Execution
Run the script from your terminal or command prompt:

```bash
python script_name.py
```

## Output

The tool generates an Excel workbook containing four worksheets:

| Worksheet | Description |
|-----------|-------------|
| **NEX Data** | Combined data from all CSV files |
| **FCA Data** | Parsed data from the XML file |
| **Check Results** | Field-by-field comparison results |
| **Summary** | Statistical overview of the comparison |

## Error Handling & Logging

- **Transaction Validation**: Issues logged to `transaction_reference_validation.log`
- **Missing Columns**: KeyError exceptions with specific column information
- **Data Type Handling**: Automatic conversions for mismatched data types
- **Performance Optimization**: Vectorized operations for large datasets

## Technical Notes

### Performance
- Uses vectorized pandas operations for optimal performance with large datasets
- Memory-efficient processing of multiple CSV files

### Data Handling
- Maintains decimal precision for financial calculations
- Special handling for date/time fields and numerical comparisons
- Robust data type conversion and validation

### File Processing
- Supports multiple CSV file formats
- XML schema validation and parsing
- Excel output with formatting and multiple worksheets

## Troubleshooting

### Common Issues

**Missing Required Columns**
- Ensure all required columns are present in NEX CSV files
- Check column name spelling and formatting

**XML Parsing Errors**
- Verify FCA XML file follows the expected schema
- Check file encoding and structure

**Memory Issues**
- For very large datasets, consider processing files in chunks
- Monitor system memory usage during execution# NEX-FCA Data Comparison Tool

A Python tool for processing and comparing financial transaction data from NEX CSV files against FCA XML data. The tool performs automated validation checks, generates detailed comparison reports, and outputs results in a comprehensive Excel workbook.

## Features

- **Multi-file Processing**: Combines multiple NEX CSV files into a single dataset
- **XML Schema Parsing**: Parses FCA XML files with specified schema validation
- **Automated Validation**: Performs transaction reference validation and field comparison
- **Comprehensive Reporting**: Generates detailed Excel reports with multiple worksheets
- **Error Handling**: Robust logging and error management for data processing issues

## Requirements

### System Requirements
- Python 3.x

### Dependencies
```bash
pip install pandas xlsxwriter
```

**Note**: `xml.etree.ElementTree` is included with Python's standard library.

## Input File Requirements

### NEX Data (CSV Format)
- **Location**: CSV files in a specified folder
- **Required Columns**:
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

### FCA Data (XML Format)
- **Format**: XML file following FCA schema
- **Content**: Transaction data with matching IDs corresponding to NEX data

## Installation & Setup

1. **Clone or download** the script to your local machine
2. **Install dependencies**:
   ```bash
   pip install pandas xlsxwriter
   ```
3. **Prepare your data files**:
   - Place NEX CSV files in a designated folder
   - Ensure FCA XML file is accessible

## Usage

### Configuration
Update the following variables in the script before running:

```python
csv_folder = "Abide CSV files"           # Path to NEX CSV files
xml_file = "FCA XML file/FCA.xml"        # Path to FCA XML file
output_file = "output_file_with_checks_and_summary.xlsx"  # Output file name
```

### Execution
Run the script from your terminal or command prompt:

```bash
python script_name.py
```

## Output

The tool generates an Excel workbook containing four worksheets:

| Worksheet | Description |
|-----------|-------------|
| **NEX Data** | Combined data from all CSV files |
| **FCA Data** | Parsed data from the XML file |
| **Check Results** | Field-by-field comparison results |
| **Summary** | Statistical overview of the comparison |

## Error Handling & Logging

- **Transaction Validation**: Issues logged to `transaction_reference_validation.log`
- **Missing Columns**: KeyError exceptions with specific column information
- **Data Type Handling**: Automatic conversions for mismatched data types
- **Performance Optimization**: Vectorized operations for large datasets

## Technical Notes

### Performance
- Uses vectorized pandas operations for optimal performance with large datasets
- Memory-efficient processing of multiple CSV files

### Data Handling
- Maintains decimal precision for financial calculations
- Special handling for date/time fields and numerical comparisons
- Robust data type conversion and validation

### File Processing
- Supports multiple CSV file formats
- XML schema validation and parsing
- Excel output with formatting and multiple worksheets

## Troubleshooting

### Common Issues

**Missing Required Columns**
- Ensure all required columns are present in NEX CSV files
- Check column name spelling and formatting

**XML Parsing Errors**
- Verify FCA XML file follows the expected schema
- Check file encoding and structure

**Memory Issues**
- For very large datasets, consider processing files in chunks
- Monitor system memory usage during execution