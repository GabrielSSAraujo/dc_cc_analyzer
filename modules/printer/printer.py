import pandas as pd
import json
from fpdf import FPDF, Align

# REQ-8: A Ferramenta deve produzir como saída um relatório de cobertura DC/CC, em formato PDF, 
# do SUT considerando como casos de teste os Test Vectors presentes na planilha de entrada.
class Printer:
    def __init__(self, path, sut_path, test_vector_path, df_list, dc_coverage, pass_fail_coverage, pass_fail_data):
        # Set path to directory
        self.path = path
        self.website = "https://github.com/GabrielSSAraujo/dc_cc_analyzer.git"

        # Read each CSV file into a DataFrame
        self.outputs_df = pd.read_csv(self.path + "outputs.csv")
        self.results_df = pd.read_csv(self.path + "results_sut.csv")
        self.sut_path = sut_path
        self.test_vector_path = test_vector_path
        self.df_list = df_list
        self.dc_coverage = dc_coverage
        self.pass_fail_coverage = pass_fail_coverage
        self.pass_fail_data = pass_fail_data

        self.pdf = FPDF("P", "mm", "A3")
        self.pdf.set_title("DC/CC Analyzer Report")
        self.pdf.set_author(
            "Aline Andreotti, Bruno Alvarenga, Gabriel Santos, Gustavo Pinheiro, Moacir Galdino"
        )

    # Fill up document
    def generate_report(self):
        # Add first page
        self.pdf.add_page()
        self.pdf.set_font("Times", "", 16)
        # First section
        self.pdf.cell(0, 16, "Data Coupling/Control Coupling Report", border=False, align="C")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Github location: {self.website}", link=self.website)
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Project: {self.sut_path}")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Test Vector: {self.test_vector_path}")
        self.pdf.ln()
        self.pdf.cell(0, 10, f"Pass/Fail: {self.pass_fail_coverage}%")
        self.pdf.ln(10)
        self.pdf.cell(0, 10, f"DC/CC Coverage: {self.dc_coverage}%")
        self.pdf.ln(10)
        
        # Set auto page break
        self.pdf.set_auto_page_break(auto = True, margin = 15)

        # Second section - Functions DC/CC report
        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 14, f"Functions DC/CC report")

        for df in self.df_list:
            # Calculate columns width
            col_width = 30

            self.pdf.ln()
            # Header
            self.pdf.set_font("Times", "B", 12)
            self.pdf.cell(col_width, 10, txt=df.name, border=1, align="C")
            for col in df.columns:
                self.pdf.cell(col_width, 10, txt=col, border=1, align="C")
            self.pdf.ln()

            # Body
            self.pdf.set_font("Times", "", 12)
            for index, row in df.iterrows():
                self.pdf.cell(col_width, 10, text=str(index), border=1, align="C")
                for col in df.columns:
                    text = ""
                    if row[col] == "0":
                        text = "NC"
                        self.pdf.set_fill_color("#ea9999")
                    else:
                        text = "C (" + row[col] + ")"
                        self.pdf.set_fill_color("#b6d7a8")
                    self.pdf.cell(col_width, 10, text=text, border=1, align="C", fill = True)
                self.pdf.ln()
        
        # Legend
        self.pdf.ln()
        self.pdf.cell(0, 8, f"Caption: C: Covered (time of coverage), NC: Not Covered.")
        self.pdf.ln()
        self.pdf.cell(0, 8, f"Note: The rows represent the identified inputs of each function, and the columns represent the outputs.")
        self.pdf.ln()

        # Third section - Pass/Fail report
        self.pdf.add_page()
        self.pdf.set_font("Times", "B", size=14)
        self.pdf.cell(0, 14, f"Pass/Fail report", )

        # Create DataFrame structure
        cols = ["Time", "Generated", "Expected", "Pass/Fail"]
        df_pass_fail = pd.DataFrame(columns=cols)

        time = []
        generated = {}
        for i in range(len(self.results_df)):
            for col in self.results_df.columns:
                if col == "Time":
                    time.insert(i, self.outputs_df.iloc[i][col])
                    generated[i] = []
                    continue
                generated[i].append(str(col) + "=" + str(round(self.outputs_df.iloc[i][col], 3)))
        
        df_pass_fail["Time"] = time

        expected = {}
        for i in range(len(self.outputs_df)):
            for col in self.outputs_df.columns:
                if col == "Time":
                    expected[i] = []
                    continue
                expected[i].append(str(col) + "=" + str(round(self.outputs_df.iloc[i][col], 3)))
        
        pass_fail = []
        for time in self.pass_fail_data:
            pass_fail.append(self.pass_fail_data[time])
        
        df_pass_fail["Pass/Fail"] = pass_fail

        # Print to PDF
        # Calculate columns width
        col_width = (self.pdf.w - 2 * self.pdf.l_margin) / len(df_pass_fail.columns)

        # Header
        self.pdf.ln()
        self.pdf.set_font("Times", "B", 12)
        for col in df_pass_fail.columns:
            self.pdf.cell(col_width, 10, txt=col, border=1, align="C")
        self.pdf.ln()

        # Body
        self.pdf.set_font("Times", "", 12)
        for index, row in df_pass_fail.iterrows():
            for col in df_pass_fail.columns:
                if df_pass_fail["Pass/Fail"][index]:
                    self.pdf.set_fill_color("#b6d7a8")
                else:
                    self.pdf.set_fill_color("#ea9999")
                
                if col == "Generated":
                    width = col_width/len(generated[index])
                    for output in generated[index]:
                        self.pdf.cell(width, 10, text=str(output), border=1, fill=True, align="C")
                elif col == "Expected":
                    width = col_width/len(expected[index])
                    for output in expected[index]:
                        self.pdf.cell(width, 10, text=str(output), border=1, fill=True, align="C")
                else:
                    self.pdf.cell(col_width, 10, text=str(row[col]), border=1, fill=True, align="C")
            self.pdf.ln()

        # Close document
        self.pdf.output("report.pdf")
