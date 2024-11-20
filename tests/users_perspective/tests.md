# Tests done to cover REQ-1, REQ-2, REQ-8 and REQ-9

## Test 1
1. Download the project to your Windows machine.
2. Install the necessary libraries.
3. Download the `sut_final` project and place it in the same directory as the `dc_cc_analyzer` project.
4. Navigate to the `dc_cc_analyzer` project directory.
5. Execute the following command: 

```
python dc-cc-analyzer.py ..\sut_final\sut.c ..\sut_final\TestVec.xls
```

6. Verify that the software runs without errors. (REQ-1, REQ-2)
7. Verify that the software produces the message "Check the report.pdf file in \<path> directory", where path is the `dc_cc_analyzer` folder path. (REQ-9)
8. Verify that the `report.pdf` file is a Data and Control Coupling report and that the report indicates that the test vectors used are those in the `TestVec.xls` file. (REQ-8)

### Results

Passed. Check the `windows_execution.png` and `windows_report.pdf` files.

## Test 2
1. Download the project to your Linux machine.
2. Install the necessary libraries.
3. Download the `sut_final` project and place it in the same directory as the `dc_cc_analyzer` project.
4. Navigate to the `dc_cc_analyzer` project directory.
5. Execute the following command: 

```
python3 dc-cc-analyzer.py ../sut_final/sut.c ../sut_final/TestVec.xls
```

6. Verify that the software runs without errors. (REQ-1, REQ-2)
7. Verify that the software produces the message "Check the report.pdf file in \<path> directory", where path is the `dc_cc_analyzer` folder path. (REQ-9)
8. Verify that the `report.pdf` file is a Data and Control Coupling report and that the report indicates that the test vectors used are those in the `TestVec.xls` file. (REQ-8)

### Results

Passed. Check the `linux_execution.png` and `linux_report.pdf` files.