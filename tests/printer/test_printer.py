import unittest
import sys
import os
import pdfquery

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)  # Insere o diretório raiz no início do sys.path

from modules.analyzer.static_analyzer import StaticAnalyzer
from modules.data_processor.data_processor import DataProcessor
from modules.printer.printer import Printer

# Aux functions
def get_elements_between_texts(pdf, text1, text2):
    results = []
    elements = pdf.pq('LTTextBoxHorizontal')
    found_text1 = False

    for el in elements:
        text = el.text.strip()

        if text1 == text:
            found_text1 = True
            continue

        if text2 == text:
            break

        if found_text1:
            results.append(el.text.strip())
    return results

def get_elements_after_text(pdf, text):
    results = []
    elements = pdf.pq('LTTextBoxHorizontal')
    found_text = False

    for el in elements:
        t = el.text.strip()

        if t == text:
            found_text = True
            continue

        if found_text:
            results.append(el.text.strip())
    return results

class TestPrinter(unittest.TestCase):
    def custom_setUp(self, sut_dir_path, data_dir_path):
        # Set up StaticAnalyzer
        self.path_sut = os.path.abspath(os.path.join(os.path.dirname(__file__), f"./{sut_dir_path}/sut.c"))
        static_analyzer = StaticAnalyzer()
        ast = static_analyzer.get_ast(self.path_sut)
        function_interface_list = static_analyzer.get_coupled_data(ast)

        # Set up DataProcessor
        path_data = os.path.abspath(os.path.join(os.path.dirname(__file__),f"./{data_dir_path}")) + "/" 
        data_processor = DataProcessor(path_data)
        self.df_list = data_processor.analyze(function_interface_list)
        self.dc_coverage = data_processor.get_coverage(self.df_list)
        self.pass_fail_coverage, self.pass_fail_data = data_processor.get_pass_fail_coverage()

        # Set up Printer
        self.testvector_path = os.path.abspath(os.path.join(os.path.dirname(__file__),f"./{sut_dir_path}/TestVec.csv"))
        printer = Printer(os.path.join(os.path.dirname(__file__),f"./{data_dir_path}/"), self.path_sut, self.testvector_path, self.df_list, self.dc_coverage, self.pass_fail_coverage, self.pass_fail_data)
        self.expected_outputs = printer.get_expected_outputs()
        self.generated_outputs = printer.get_generated_outputs()
        self.times = printer.get_time()
        self.pass_fail_list = printer.get_pass_fail()

        printer.generate_report()

    # ----------- Tests -----------
    def test_req15_sut_path_01(self):
        self.custom_setUp("sut1", "data1")

        report_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("Project:")')[0]
        text = element.text
        self.assertEqual(text, f"Project: {self.path_sut} ")
        pdf.file.close()

    def test_req16_testvec_path_01(self):
        self.custom_setUp("sut1", "data1")

        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("Test Vector:")')[0]
        text = element.text
        self.assertEqual(text, f"Test Vector: {self.testvector_path} ")
        pdf.file.close()

    def test_req17_pass_fail_coverage_01(self):
        self.custom_setUp("sut1", "data1")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("Pass/Fail:")')[0]
        text = element.text
        self.assertEqual(text, f"Pass/Fail: {self.pass_fail_coverage}% ")
        pdf.file.close()

    def test_req18_dccc_coverage_01(self):
        self.custom_setUp("sut1", "data1")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("DC/CC Coverage:")')[0]
        text = element.text
        self.assertEqual(text, f"DC/CC Coverage: {self.dc_coverage}% ")
        pdf.file.close()

    def test_req19_dccc_tables_01(self):
        self.custom_setUp("sut1", "data1")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        texts = get_elements_between_texts(pdf, "Functions DC/CC report", "Pass/Fail report")
        self.assertGreater(len(texts), 0)
        texts = [t for t in texts if 'Caption:' not in t]
        texts = [t for t in texts if 'Note:' not in t]
        i = 0

        # Iterate over ever dataframe that is mapped to a table in the pdf
        for df in self.df_list:
            # Function name
            self.assertEqual(df.name, texts[i])
            i += 1

            # Table header
            for col in df.columns:
                self.assertEqual(col, texts[i])
                i += 1
            
            # Table content
            for index, row in df.iterrows():
                self.assertEqual(index, texts[i])
                i += 1
                for col in df.columns:
                    val = ""
                    if row[col] == "0":
                        val = "NC"
                    else:
                        val = "C (" + row[col] + ")"
                    self.assertEqual(val, texts[i])
                    i += 1
        pdf.file.close()

    def test_req20_pass_fail_tables_01(self):
        self.custom_setUp("sut1", "data1")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        texts = get_elements_after_text(pdf, "Pass/Fail report")
        self.assertGreater(len(texts), 0)
        i = 0

        # Check tabel header
        self.assertEqual("Time", texts[i]); i += 1
        self.assertEqual("Generated", texts[i]); i += 1
        self.assertEqual("Expected", texts[i]); i += 1
        self.assertEqual("Pass/Fail", texts[i]); i += 1

        # Check tabel content
        for index, time in enumerate(self.times):
            # Time
            self.assertEqual(time, texts[i]); i += 1

            # Generated
            for results in self.generated_outputs[index]:
                self.assertEqual(results, texts[i])
                i += 1

            # Expected
            for results in self.expected_outputs[index]:
                self.assertEqual(results, texts[i])
                i += 1

            # Pass/Fail
            self.assertEqual(str(self.pass_fail_list[index]), texts[i])
            i += 1

        pdf.file.close()

    def test_req15_sut_path_02(self):
        self.custom_setUp("sut2", "data2")

        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("Project:")')[0]
        text = element.text
        self.assertEqual(text, f"Project: {self.path_sut} ")
        pdf.file.close()

    def test_req16_testvec_path_02(self):
        self.custom_setUp("sut2", "data2")

        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("Test Vector:")')[0]
        text = element.text
        self.assertEqual(text, f"Test Vector: {self.testvector_path} ")
        pdf.file.close()

    def test_req17_pass_fail_coverage_02(self):
        self.custom_setUp("sut2", "data2")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("Pass/Fail:")')[0]
        text = element.text
        self.assertEqual(text, f"Pass/Fail: {self.pass_fail_coverage}% ")
        pdf.file.close()

    def test_req18_dccc_coverage_02(self):
        self.custom_setUp("sut2", "data2")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        element = pdf.pq('LTTextBoxHorizontal:contains("DC/CC Coverage:")')[0]
        text = element.text
        self.assertEqual(text, f"DC/CC Coverage: {self.dc_coverage}% ")
        pdf.file.close()

    def test_req19_dccc_tables_02(self):
        self.custom_setUp("sut2", "data2")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        texts = get_elements_between_texts(pdf, "Functions DC/CC report", "Pass/Fail report")
        self.assertGreater(len(texts), 0)
        texts = [t for t in texts if 'Caption:' not in t]
        texts = [t for t in texts if 'Note:' not in t]
        i = 0

        # Iterate over ever dataframe that is mapped to a table in the pdf
        for df in self.df_list:
            # Function name
            self.assertEqual(df.name, texts[i])
            i += 1

            # Table header
            for col in df.columns:
                self.assertEqual(col, texts[i])
                i += 1
            
            # Table content
            for index, row in df.iterrows():
                self.assertEqual(index, texts[i])
                i += 1
                for col in df.columns:
                    val = ""
                    if row[col] == "0":
                        val = "NC"
                    else:
                        val = "C (" + row[col] + ")"
                    self.assertEqual(val, texts[i])
                    i += 1
        pdf.file.close()

    def test_req20_pass_fail_tables_02(self):
        self.custom_setUp("sut2", "data2")
        
        report_path =os.path.abspath(os.path.join(os.path.dirname(__file__),"../../report.pdf"))
        pdf = pdfquery.PDFQuery(report_path)
        pdf.load()

        texts = get_elements_after_text(pdf, "Pass/Fail report")
        self.assertGreater(len(texts), 0)
        i = 0

        # Check tabel header
        self.assertEqual("Time", texts[i]); i += 1
        self.assertEqual("Generated", texts[i]); i += 1
        self.assertEqual("Expected", texts[i]); i += 1
        self.assertEqual("Pass/Fail", texts[i]); i += 1

        # Check tabel content
        for index, time in enumerate(self.times):
            # Time
            self.assertEqual(time, texts[i]); i += 1

            # Generated
            for results in self.generated_outputs[index]:
                self.assertEqual(results, texts[i])
                i += 1

            # Expected
            for results in self.expected_outputs[index]:
                self.assertEqual(results, texts[i])
                i += 1

            # Pass/Fail
            self.assertEqual(str(self.pass_fail_list[index]), texts[i])
            i += 1

        pdf.file.close()

# if __name__ == "__main__":
#     unittest.main(verbosity=2)
