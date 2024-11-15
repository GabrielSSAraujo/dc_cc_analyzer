import pandas as pd
import logging
import decimal
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataProcessor:
    def __init__(self, files_dir):
        # Load CSV files
        self.inputs = pd.read_csv(files_dir + 'inputs.csv')
        self.expected_outputs = pd.read_csv(files_dir + 'outputs.csv')
        self.actual_results = pd.read_csv(files_dir + 'results_sut.csv')
        self.suti_results = pd.read_csv(files_dir + 'results_suti.csv')
        self.couplings = pd.read_csv(files_dir + 'couplings.csv')
        self.pass_rate = 0.0
        self.exercised_percentage = 0.0
        self.compromised_suti = False
        self.exercised_couplings = [] # STILL NOT BEING FILLED
        self.couplings_outputs = self.load_couplings_outputs(files_dir + 'couplings_outputs.json')

        # Load tolerances as a dictionary
        tolerances_df = pd.read_csv(files_dir + 'tolerances.csv', index_col=0, header=None)
        self.tolerances = tolerances_df[1].to_dict()  # Column 1 contains tolerance values

    def load_couplings_outputs(self, json_file_path):
        """Load the couplings outputs JSON file and return it as a dictionary."""
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            #logging.info("Couplings outputs JSON file loaded successfully.")
            return data
        except Exception as e:
            logging.error(f"Error loading couplings outputs JSON file: {e}")
            return {}

    def analyze(self):
        # Initialize pass/fail counters
        total_tests = 0
        passed_tests = 0
        
        # Perform pass/fail analysis for each row
        for index, row in self.expected_outputs.iterrows():
            total_tests += 1
            pass_case = True
            
            for column in row.index:
                if column != "Time":
                    expected_value = row[column]
                    actual_value = self.actual_results.at[index, column]
                    suti_value = self.suti_results.at[index, column]
                    tolerance = float(self.tolerances.get(column, 0))

                    # Check if the actual value is within tolerance of the expected output
                    difference = abs(expected_value - actual_value)
                    rounded_difference = round_to_match_decimals(difference, tolerance)
                    if rounded_difference > tolerance:
                        pass_case = False

                    # Check if the difference between actual result and SUTI result exceeds tolerance
                    tolerance = 0.00001
                    difference = abs(actual_value - suti_value)
                    rounded_difference = round_to_match_decimals(difference, tolerance)
                    if rounded_difference > tolerance:
                        logging.warning(
                            f"Warning: Difference between actual result ({actual_value}) and "
                            f"SUTI result ({suti_value}) for '{column}' at index {index} exceeds tolerance ({tolerance})."
                            f"Instrumented SUT may be compromised."
                        )
                        self.compromised_suti = True
            
            # Count passes/fails
            if pass_case:
                passed_tests += 1
        
        # Calculate and log pass rate
        self.pass_rate = (passed_tests / total_tests) * 100
        print(f"Percentage of passed test cases: {self.pass_rate:.2f}%")
        
        # Perform couplings analysis
        self.analyze_couplings()

    def analyze_couplings(self):
        total_couplings = 0
        exercised_couplings = 0
        tolerance = 0.01
        
        # Check each coupling's values against the tolerances by examining all pairs of values
        for coupling in self.couplings.columns[1:]:  # Skip the "Time" column
            total_couplings += 1
            coupling_exercised = False
            
            # Iterate through values in the column, comparing each with the previous value
            previous_value = None
            for index, value in self.couplings[coupling].items():
                if previous_value is not None:
                    # Calculate the difference between consecutive values in the coupling
                    if abs(value - previous_value) > tolerance:
                        # Check if the corresponding output vector has also changed beyond tolerance
                        output_changed = False
                        for output_column in self.actual_results.columns:
                            if output_column != "Time":
                                previous_output_value = self.actual_results.at[index - 1, output_column]
                                current_output_value = self.actual_results.at[index, output_column]
                                output_tolerance = float(self.tolerances.get(output_column, 0))

                                # Check if output change exceeds tolerance
                                if abs(current_output_value - previous_output_value) > output_tolerance:
                                    output_changed = True
                                    break  # Stop if any output value has changed beyond tolerance
                        
                        if output_changed:
                            coupling_exercised = True
                            break
                previous_value = value  # Update previous value for the next comparison
            
            if coupling_exercised:
                exercised_couplings += 1
        
        # Calculate and print the percentage of exercised couplings
        self.exercised_percentage = (exercised_couplings / total_couplings) * 100
        print(f"Percentage of exercised couplings: {self.exercised_percentage:.2f}%")

def round_to_match_decimals(number, reference):
    # Determine the number of decimal places in the reference number
    decimal_places = abs(decimal.Decimal(str(reference)).as_tuple().exponent)
    # Round the number to match the decimal places of the reference
    return round(number, decimal_places)