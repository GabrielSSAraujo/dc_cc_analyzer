/*Author: Aline Andreotti Urna
Data: 03/10/2024
Teste de Driver para o SUT
*/

//limitações conhecidas: 
//1) não é feito o reconhecimento do tipo de dado. Para simplificar, primeiramente
//estamos trabalhando com tipos primitivos - no caso específico - dos inteiros
//mas a ideia é que seja possível trabalhar com qualquer tipo de dado primitivo.
//para isso precisaremo usar resultados da análise estática.
//2) não é feito o tratamento de erros. Por exemplo, se o arquivo de entrada não existe, o programa irá quebrar.
//3) não é feito o tratamento de memória. Por exemplo, se o arquivo de entrada for muito grande e ultrapassar o limite de memória disponível [256]
//4) não ha garantias da existencia do SUT.h e SUT.c (premissa?)

//comando para executar no code terminal: quando abro o terminal integrado em dc_cc_analzer
/*
gcc SUT/teste_driver.c SUT/SUT.c -o teste_driver
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//include SutFileName.h

//define ROWS
//define COLS
//define OUT_COLS



int main() {
    /*init data*/
    int input_data[COLS];
    int output_data[OUT_COLS];
    //int outx

    // Criar arquivos CSV
    FILE *input_file = fopen("input.csv", "r");
    FILE *output_file = fopen("output.csv", "r");
    FILE *results_file = fopen("results.csv", "w"); //arquivo de saída final (original "output.csv" + resultados após executar o SUT)

    if (input_file == NULL || output_file == NULL || results_file == NULL) {
        printf("Erro ao abrir os arquivos.\n");
        return 1;
    }

    char input_line[256]; //variável para armazenar a linha lida do arquivo de entrada
    char output_line[256]; //variável para armazenar a linha lida do arquivo de saída
    char aux_output_line[256]; // Variável auxiliar para armazenar a cópia de output_line

    // Ler e escrever a primeira linha (cabeçalho)
    if (fgets(output_line, sizeof(output_line), output_file) != NULL) {
        output_line[strcspn(output_line, "\n")] = '\0';
        //HeaderPlaceholder
    }

    for (int i = 1; i < ROWS; i++) {
        // Ler uma linha por vez do input.csv
        if (fgets(input_line, sizeof(input_line), input_file) != NULL) {
            char *token = strtok(input_line, ",");
            int j = 0;
            while (token != NULL && j < COLS) {
                input_data[j] = atoi(token);
                token = strtok(NULL, ",");
                j++;
            }
        }

        // Ler uma linha por vez do output.csv
        if (fgets(output_line, sizeof(output_line), output_file) != NULL) {
            strcpy(aux_output_line, output_line);
            aux_output_line[strcspn(aux_output_line, "\n")] = '\0';
            char *token = strtok(output_line, ",");
            int j = 0;
            while (token != NULL && j < OUT_COLS) {
                output_data[j] = atoi(token);
                token = strtok(NULL, ",");
                j++;
            }
        }

        // Chamar a função SUT com os dados lidos
        //SUT()

        // Verificar os resultados e escrever no arquivo output.csv
        //printf("Debug: out0=%d, out1=%d, out2=%d, out3=%d, out4=%d, out5=%d\n", out0, out1, out2, out3, out4, out5);
        //printf("Debug: output_data[0]=%d, output_data[1]=%d, output_data[2]=%d, output_data[3]=%d, output_data[4]=%d, output_data[5]=%d\n", output_data[0], output_data[1], output_data[2], output_data[3], output_data[4], output_data[5]);

        //PassFailComparison

        //printf("Debug: test_result=%d\n", test_result);
        //printf("Debug: output_line=%s\n", output_line);

        output_line[strcspn(output_line, "\n")] = '\0'; //remove o lineFeed para não pular a linha. Quero concatenar com o resultado
        
        // Escrever no arquivo
        //LineConcat
            perror("Erro ao escrever no arquivo");
            fclose(results_file);
            return 1;
        }


}

        // Fechar arquivos
        fclose(input_file);
        fclose(output_file);
        fclose(results_file);

         return 0;
}

//comando para executar no code terminal: quando abro o terminal integrado dc_cc_analyzer
/*
gcc SUT/teste_driver.c SUT/SUT.c -o teste_driver
*/


//auxilios:
//atalhos VSCODE
//comentarios
//bloco de comentarios = Alt + shift + A
// comentar linha = ctrl + ;