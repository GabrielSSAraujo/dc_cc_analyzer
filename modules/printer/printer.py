import pandas as pd
from fpdf import FPDF

# REQ-13: A Ferramenta deve produzir como saída um relatório de cobertura DC/CC, em formato PDF, 
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

    def get_generated_outputs(self):
        generated = {}
        for i in range(len(self.results_df)):
            for col in self.results_df.columns:
                if col == "Time":
                    generated[i] = []
                    continue
                generated[i].append(str(col) + "=" + str(round(self.results_df.iloc[i][col], 3)))
        
        return generated
    
    def get_expected_outputs(self):
        expected = {}
        for i in range(len(self.outputs_df)):
            for col in self.outputs_df.columns:
                if col == "Time":
                    expected[i] = []
                    continue
                expected[i].append(str(col) + "=" + str(round(self.outputs_df.iloc[i][col], 3)))
        return expected
    
    def get_time(self):
        return [el for el in self.pass_fail_data]
    
    def get_pass_fail(self):
        pass_fail = []
        for time in self.pass_fail_data:
            pass_fail.append(self.pass_fail_data[time])
        return pass_fail
        
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

        # REQ-15: A Ferramenta deve registrar no relatório o caminho (path) para o arquivo "sut.c" analisado.
        self.pdf.cell(0, 10, f"Project: {self.sut_path}")
        self.pdf.ln()

        #REQ-16: A Ferramenta deve registrar no relatório o caminho (path) para a planilha de Test Vectors utilizada para a análise.
        self.pdf.cell(0, 10, f"Test Vector: {self.test_vector_path}")
        self.pdf.ln()

        # REQ-17: A Ferramenta deve registrar no relatório a porcentagem de Test Vectors que, após serem executados pelo SUT, produziram as saídas esperadas.
        self.pdf.cell(0, 10, f"Pass/Fail: {self.pass_fail_coverage}%")
        self.pdf.ln(10)

        #REQ-18: A Ferramenta deve registrar no relatório a porcentagem de cobertura DC/CC obtida.
        self.pdf.cell(0, 10, f"DC/CC Coverage: {self.dc_coverage}%")
        self.pdf.ln(10)

        # Set auto page break
        self.pdf.set_auto_page_break(auto=True, margin=15)

        # Second section - Functions DC/CC report
        # REQ-19: Para cada função do SUT, a Ferramenta deve registrar no relatório suas entradas e saídas, além de identificar quais entradas, individualmente, foram capazes de influenciar as saídas da função e quais foram as saídas influenciadas.
        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 14, f"Functions DC/CC report")

        for df in self.df_list:
            # Calculate columns width
            col_width = 30

            self.pdf.ln()
            # Header
            self.pdf.set_font("Times", "B", 12)
            self.pdf.cell(col_width, 10, text=df.name, border=1, align="C")
            for col in df.columns:
                self.pdf.cell(col_width, 10, text=col, border=1, align="C")
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
        # REQ-20: A ferramenta deve registrar no relatório o valor esperado e o valor produzido pelo SUT para cada Test Vector, indicando também se o valor produzido correspondeu ao esperado (resultado do teste: aprovado ou reprovado).
        self.pdf.add_page()
        self.pdf.set_font("Times", "B", size=14)
        self.pdf.cell(0, 14, f"Pass/Fail report", )

        # Create DataFrame structure
        cols = ["Time", "Generated", "Expected", "Pass/Fail"]
        df_pass_fail = pd.DataFrame(columns=cols)

        # Get required data
        df_pass_fail["Time"] = self.get_time()
        generated = self.get_generated_outputs()
        expected = self.get_expected_outputs()
        df_pass_fail["Pass/Fail"] = self.get_pass_fail()

        # Print to PDF
        # Calculate columns width
        col_width = (self.pdf.w - 2 * self.pdf.l_margin) / len(df_pass_fail.columns)

        # Header
        self.pdf.ln()
        self.pdf.set_font("Times", "B", 12)
        for col in df_pass_fail.columns:
            self.pdf.cell(col_width, 10, text=col, border=1, align="C")
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
