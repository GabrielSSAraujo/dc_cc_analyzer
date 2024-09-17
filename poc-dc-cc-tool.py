from stsatic_analyzer import StaticAnalyzer

if __name__ == "__main__":
    file_path = './SUT/sut.c'
    analyzer = StaticAnalyzer(file_path)
    analyzer.start_analysis()