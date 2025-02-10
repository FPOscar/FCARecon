import os
import pandas as pd
import xml.etree.ElementTree as ET
import xlsxwriter

def combine_csv_files(folder_path):
    # List to hold DataFrames
    all_data = []
    
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Read the CSV file with specific dtype for Transaction Reference Number
            df = pd.read_csv(
                file_path,
                dtype={
                    'Transaction Reference Number': str,  # Force string type
                },
                float_precision='round_trip'
            )
            
            # Additional cleaning for Transaction Reference Number
            if 'Transaction Reference Number' in df.columns:
                # Remove any whitespace
                df['Transaction Reference Number'] = df['Transaction Reference Number'].str.strip()
                
                # If there are any decimal points, truncate to integer
                df['Transaction Reference Number'] = df['Transaction Reference Number'].apply(
                    lambda x: str(x).split('.')[0] if isinstance(x, str) and '.' in x else str(x)
                )
            
            # Validate the transaction references
            validate_transaction_references(df, filename)
            
            all_data.append(df)
    
    # Combine all DataFrames into one
    combined_df = pd.concat(all_data, ignore_index=True)
    
    return combined_df

def validate_transaction_references(df, original_file):
    """
    Validate transaction references to catch any potential import issues
    """
    import logging
    
    logging.basicConfig(filename='transaction_reference_validation.log', level=logging.WARNING)
    
    issues = []
    
    # Check for any transaction references that look suspicious
    for idx, ref in enumerate(df['Transaction Reference Number']):
        # Check for scientific notation
        if 'e' in str(ref).lower():
            issues.append(f"Row {idx+2}: Scientific notation detected: {ref}")
        
        # Check for decimal points
        if '.' in str(ref):
            issues.append(f"Row {idx+2}: Decimal point detected: {ref}")
        
        # Check for unexpected characters
        if not str(ref).strip().isalnum():
            issues.append(f"Row {idx+2}: Non-alphanumeric characters detected: {ref}")
    
    # Log any issues found
    if issues:
        logging.warning(f"\nIssues found in {original_file}:")
        for issue in issues:
            logging.warning(issue)
        
    return len(issues) == 0  # Returns True if no issues found

def parse_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespace
    ns = {'ns': 'http://mdp.fca.org.uk/gb_extra'}

    # Define the column structure
    columns = [
        'TxId', 'ExctgPty', 'InvstmtPtyInd', 'SubmitgPty', 'LEI', 'CtryOfBrnch', 'LEI2', 'LEI3',
        'TrnsmssnInd', 'TradDt', 'TradgCpcty', 'QtyUnit', 'Amt', 'Ccy', 'NmnlVal', 'NmnlValCcy',
        'Pctg', 'NetAmt', 'TradVn', 'FinInstrmId', 'InvstmtDcsnPrsnCtryOfBrnch', 'InvstmtDcsnPrsnId',
        'InvstmtDcsnPrsnCd', 'InvstmtDcsnPrsnPrtry',  # <- also add InvstmtDcsnPrsnPrtry
        'ExctgPrsnCtryOfBrnch', 'ExctgPrsnId', 'ExctgPrsnCd', 'SctiesFincgTxInd', 'Sts', 'SubmDt'
    ]


    # Helper function to extract text with default value
    def get_text(element, path):
        return element.findtext(path, default="", namespaces=ns)

    # Store records
    records = []

    # Iterate through each transaction (Tx) in the XML
    for tx in root.findall(".//ns:Tx", namespaces=ns):
        amt_element = tx.find(".//ns:Tx/ns:Pric/ns:Pric/ns:MntryVal/ns:Amt", namespaces=ns)
        nmnl_val_element = tx.find(".//ns:Tx/ns:Qty/ns:NmnlVal", namespaces=ns)
        pctg_element = tx.find(".//ns:Tx/ns:Pric/ns:Pric/ns:Pctg", namespaces=ns)
        net_amt_element = tx.find(".//ns:Tx/ns:NetAmt", namespaces=ns)
        prtry_element = tx.find(".//ns:InvstmtDcsnPrsn/ns:Prsn/ns:Othr/ns:SchmeNm/ns:Prtry", namespaces=ns)

        record = {
            'TxId': get_text(tx, ".//ns:TxId"),
            'ExctgPty': get_text(tx, ".//ns:ExctgPty"),
            'InvstmtPtyInd': get_text(tx, ".//ns:InvstmtPtyInd"),
            'SubmitgPty': get_text(tx, ".//ns:SubmitgPty"),
            'LEI': get_text(tx, ".//ns:Buyr/ns:AcctOwnr/ns:Id/ns:LEI"),
            'CtryOfBrnch': get_text(tx, ".//ns:Buyr/ns:AcctOwnr/ns:CtryOfBrnch"),
            'LEI2': get_text(tx, ".//ns:Buyr/ns:DcsnMakr/ns:LEI"),
            'LEI3': get_text(tx, ".//ns:Sellr/ns:AcctOwnr/ns:Id/ns:LEI"),
            'TrnsmssnInd': get_text(tx, ".//ns:OrdrTrnsmssn/ns:TrnsmssnInd"),
            'TradDt': get_text(tx, ".//ns:Tx/ns:TradDt"),
            'TradgCpcty': get_text(tx, ".//ns:Tx/ns:TradgCpcty"),
            'QtyUnit': get_text(tx, ".//ns:Tx/ns:Qty/ns:Unit"),
            'Amt': get_text(tx, ".//ns:Tx/ns:Pric/ns:Pric/ns:MntryVal/ns:Amt"),
            'Ccy': amt_element.attrib.get("Ccy", "") if amt_element is not None else "",
            'NmnlVal': nmnl_val_element.text if nmnl_val_element is not None else "",
            'NmnlValCcy': nmnl_val_element.attrib.get("Ccy", "") if nmnl_val_element is not None else "",
            'Pctg': pctg_element.text if pctg_element is not None else "",
            'NetAmt': net_amt_element.text if net_amt_element is not None else "",
            'TradVn': get_text(tx, ".//ns:Tx/ns:TradVn"),
            'FinInstrmId': get_text(tx, ".//ns:FinInstrm/ns:Id"),
            'InvstmtDcsnPrsnCtryOfBrnch': get_text(tx, ".//ns:InvstmtDcsnPrsn/ns:Prsn/ns:CtryOfBrnch"),
            'InvstmtDcsnPrsnId': get_text(tx, ".//ns:InvstmtDcsnPrsn/ns:Prsn/ns:Othr/ns:Id"),
            'InvstmtDcsnPrsnCd': get_text(tx, ".//ns:InvstmtDcsnPrsn/ns:Prsn/ns:Othr/ns:SchmeNm/ns:Cd"),
            'InvstmtDcsnPrsnPrtry': prtry_element.text if prtry_element is not None else "",
            'ExctgPrsnCtryOfBrnch': get_text(tx, ".//ns:ExctgPrsn/ns:Prsn/ns:CtryOfBrnch"),
            'ExctgPrsnId': get_text(tx, ".//ns:ExctgPrsn/ns:Prsn/ns:Othr/ns:Id"),
            'ExctgPrsnCd': get_text(tx, ".//ns:ExctgPrsn/ns:Prsn/ns:Othr/ns:SchmeNm/ns:Cd"),
            'SctiesFincgTxInd': get_text(tx, ".//ns:AddtlAttrbts/ns:SctiesFincgTxInd"),
            'Sts': get_text(tx, ".//ns:Feedback/ns:Sts"),
            'SubmDt': get_text(tx, ".//ns:SubmDt")
        }
        records.append(record)


    # Convert records to DataFrame and remove empty rows
    df = pd.DataFrame(records, columns=columns)
    df_cleaned = df[df['TxId'].notna() & df['TxId'].str.strip().astype(bool)]

    return df_cleaned


def write_large_df_in_chunks(df, writer, sheet_name, chunk_size=10000):
    for i in range(0, len(df), chunk_size):
        df_chunk = df.iloc[i:i + chunk_size]
        df_chunk.to_excel(writer, sheet_name=sheet_name, startrow=i+1, index=False, header=i == 0)

def perform_column_checks(nex_data, fca_data):
    """Perform vectorized checks to see if specific columns in NEX data match those in FCA data, 
    with special handling for 'Trading Date Time' and treasury bills (Quantity/Price check)."""
    
    # Ensure the necessary columns are present
    required_columns_nex = [
        'Transaction Reference Number', 'Executing Entity Identification Code', 'Trading Date Time',
        'Quantity', 'Price', 'Instrument Identification Code', 'Trading Venue', 'Transmission of Order Indicator',
        'Buyer Code', 'Seller Code'
    ]
    
    required_columns_fca = [
        'TxId', 'ExctgPty', 'TradDt', 'QtyUnit', 'Amt', 'FinInstrmId', 'TradVn', 'TrnsmssnInd', 'LEI', 'LEI3',
        # Note: FCA data also has 'NmnlVal' and 'NetAmt' for treasury bills.
    ]
    
    for col in required_columns_nex:
        if col not in nex_data.columns:
            raise KeyError(f"'{col}' column not found in NEX data.")
    
    for col in required_columns_fca:
        if col not in fca_data.columns:
            raise KeyError(f"'{col}' column not found in FCA data.")
    
    # Merge the NEX and FCA data on 'Transaction Reference Number' (NEX) and 'TxId' (FCA)
    merged_data = pd.merge(nex_data, fca_data, left_on='Transaction Reference Number', right_on='TxId', how='left')
    
    # Create a DataFrame to hold the results
    results = pd.DataFrame()
    
    # Define the columns to compare
    columns_to_check = [
        ('Transaction Reference Number', 'TxId'),
        ('Executing Entity Identification Code', 'ExctgPty'),
        ('Trading Date Time', 'TradDt'),  # Special handling for this column
        ('Quantity', 'QtyUnit'),          # Will add treasury bill logic here
        ('Price', 'Amt'),                 # Will add treasury bill logic here
        ('Instrument Identification Code', 'FinInstrmId'),
        ('Trading Venue', 'TradVn'),
        ('Transmission of Order Indicator', 'TrnsmssnInd'),
        ('Buyer Code', 'LEI'),
        ('Seller Code', 'LEI3')
    ]
    
    for nex_col, fca_col in columns_to_check:
        if nex_col == 'Trading Date Time':
            # Ignore any trailing 'Z' in FCA’s date
            results[f'{nex_col} Check'] = merged_data[nex_col] == merged_data[fca_col].str.rstrip('Z')
        
        elif nex_col == 'Quantity':
            # For treasury bills, FCA's QtyUnit will be empty.
            # In that case, compare NEX's Quantity to FCA's NmnlVal instead.
            fca_qty = merged_data[fca_col]
            # Define a boolean series where QtyUnit is missing or empty (treasury bill indicator)
            is_tbill = fca_qty.isna() | (fca_qty.astype(str).str.strip() == '')
            # Use QtyUnit if available; otherwise use NmnlVal
            fca_qty_final = fca_qty.where(~is_tbill, merged_data['NmnlVal'])
            
            # Convert both sides to numeric and round to 0 decimals before comparing.
            results[f'{nex_col} Check'] = (
                pd.to_numeric(merged_data[nex_col], errors='coerce').round(0) ==
                pd.to_numeric(fca_qty_final, errors='coerce').round(0)
            )
        
        elif nex_col == 'Price':
            # For treasury bills, if FCA's Amt is empty, use Pctg instead.
            fca_amt = merged_data[fca_col]
            is_tbill = fca_amt.isna() | (fca_amt.astype(str).str.strip() == '')
            fca_amt_final = fca_amt.where(~is_tbill, merged_data['Pctg'])
            
            # Convert both sides to numeric and round to 2 decimals before comparing.
            results[f'{nex_col} Check'] = (
                pd.to_numeric(merged_data[nex_col], errors='coerce').round(2) ==
                pd.to_numeric(fca_amt_final, errors='coerce').round(2)
            )
        
        elif nex_col == 'Transmission of Order Indicator':
            # Convert both sides to boolean for the comparison
            results[f'{nex_col} Check'] = merged_data[nex_col].astype(bool) == merged_data[fca_col].astype(bool)
        
        else:
            # Standard comparison for other columns
            results[f'{nex_col} Check'] = merged_data[nex_col] == merged_data[fca_col]
    
    # Replace the boolean values with "OK" or "CHECK"
    for column in results.columns:
        results[column] = results[column].map(lambda x: "OK" if x else "CHECK")
    
    # Include additional columns for cross-referencing
    results['Actual Transaction Reference Number'] = merged_data['Transaction Reference Number']
    # If you have an Instrument Full Name field, include it; otherwise, you can remove the next line.
    if 'Instrument Full Name' in merged_data.columns:
        results['Instrument Full Name'] = merged_data['Instrument Full Name']
    
    return results


def create_summary(results, nex_data, fca_data):
    """Create a summary showing the number of 'CHECK' for each comparison, and overall statistics."""
    
    summary = pd.DataFrame(columns=['Check', 'CHECK Count'])
    
    # Count the number of 'CHECK' in each column
    for col in results.columns[1:]:  # Skipping the first column (Transaction Reference Number)
        check_count = (results[col] == 'CHECK').sum()
        summary = pd.concat([summary, pd.DataFrame({'Check': [col], 'CHECK Count': [check_count]})], ignore_index=True)
    
    # Add additional summary information
    summary = pd.concat([summary, pd.DataFrame({'Check': ['Total Rows in NEX'], 'CHECK Count': [len(nex_data)]})], ignore_index=True)
    summary = pd.concat([summary, pd.DataFrame({'Check': ['Total Rows in FCA'], 'CHECK Count': [len(fca_data)]})], ignore_index=True)
    
    # Get the date range from the 'Trading Date Time' columns
    nex_date_range = f"{nex_data['Trading Date Time'].min()} to {nex_data['Trading Date Time'].max()}"
    fca_date_range = f"{fca_data['TradDt'].min()} to {fca_data['TradDt'].max()}"
    
    summary = pd.concat([summary, pd.DataFrame({'Check': ['Date Range in NEX'], 'CHECK Count': [nex_date_range]})], ignore_index=True)
    summary = pd.concat([summary, pd.DataFrame({'Check': ['Date Range in FCA'], 'CHECK Count': [fca_date_range]})], ignore_index=True)
    
    return summary


def create_excel(output_file, csv_folder, xml_file):
    # Combine CSV files and parse XML
    nex_data = combine_csv_files(csv_folder)
    print("Combined CSV")
    
    fca_data = parse_xml(xml_file)
    print("Parsed XML")
    
    # Perform checks
    check_results = perform_column_checks(nex_data, fca_data)
    print("Performed checks")
    
    # Create the summary
    summary = create_summary(check_results, nex_data, fca_data)
    print("Created summary")

    # Write everything to Excel
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        nex_data.to_excel(writer, sheet_name='NEX data', index=False)
        fca_data.to_excel(writer, sheet_name='FCA data', index=False)
        check_results.to_excel(writer, sheet_name='Check Results', index=False)
        summary.to_excel(writer, sheet_name='Summary', index=False)

    print(f"Excel file '{output_file}' created with checks and summary.")

# Example usage:
csv_folder = "Abide CSV files"
xml_file = "FCA XML file/FCA.xml"
output_file = "output_file_with_checks_and_summary.xlsx"

create_excel(output_file, csv_folder, xml_file)