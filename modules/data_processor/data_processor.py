import pandas as pd
import logging

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
        
        # Load tolerances as a dictionary
        tolerances_df = pd.read_csv(files_dir + 'tolerances.csv', index_col=0, header=None)
        self.tolerances = tolerances_df[1].to_dict()  # Column 1 contains tolerance values
        
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
                    tolerance = float(self.tolerances.get(column, 0))

                    # Check if the actual value is within tolerance
                    if abs(expected_value - actual_value) > tolerance:
                        pass_case = False
                        break
            
            # Count passes/fails
            if pass_case:
                passed_tests += 1
        
        # Calculate and log pass rate
        pass_rate = (passed_tests / total_tests) * 100
        print(f"Percentage of passed test cases: {pass_rate:.2f}%")
        
        # Perform couplings analysis
        self.analyze_couplings()
        
        return pass_rate

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
            for _, value in self.couplings[coupling].items():
                if previous_value is not None:
                    # Calculate the difference between consecutive values
                    if abs(value - previous_value) > tolerance:
                        coupling_exercised = True
                        break
                previous_value = value  # Update previous value for the next comparison
            
            if coupling_exercised:
                exercised_couplings += 1
        
        # Calculate and print the percentage of exercised couplings
        exercised_percentage = (exercised_couplings / total_couplings) * 100
        print(f"Percentage of exercised couplings: {exercised_percentage:.2f}%")
        