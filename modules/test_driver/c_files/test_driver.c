/**
 * @file: test_driver_model.c
 * @brief [Teste Driver para o SUT]
 * @details [limitações conhecidas: Não ha garantias da existencia do SUT.h e SUT.c (premissa?)]
 * @version: 0.1
 * @date: 2024-11-12 17:22
 * @autor: Aline Andreotti Urna
 * @e-mail: aline.urna@gmail.com
 * @githubLink: https://github.com/aliandreur
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../../tests/data/SUT/SUT.h"

int main()
{
    /*init data*/
	int SUTI1;
	int SUTI2;
	int SUTI3;
	int SUTI4;
	int SUTI5;
	int SUTI6;
	int SUTI7;
	int SUTO6;
	int SUTO5;
	int SUTO4;
	int SUTO3;
	int SUTO2;
	int SUTO1;
    float time_id;
    // Criar arquivos CSV
    FILE *input_file = fopen("./tests/data/inputs.csv", "r");
    FILE *results_file = fopen("./tests/data/results_sut.csv", "w");

    if (input_file == NULL || results_file == NULL)
    {
        printf("Erro ao abrir os arquivos.\n");
        return 1;
    }

    char line[256];      // variável para armazenar a linha lida do arquivo de entrada

    // Escrever a primeira linha (cabeçalho)
    fprintf(results_file, "%s,%s\n","ID,SUTO6, SUTO5, SUTO4, SUTO3, SUTO2, SUTO1");
    
    
    // Ler o arquivo de entrada
    while (fgets(line, sizeof(line), input_file)) {
        // Remover o caractere de nova linha, se presente
        line[strcspn(line, "\n")] = '\0';

        // Dividir a linha em tokens
        char *token = strtok(line, ",");

        // leitura dos valores do input.csv e atribuição a variáveis.
        //primeira coluna: convencionado que é o time_id
        if (token != NULL) time_id= atof(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI1 = atoi(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI2 = atoi(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI3 = atoi(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI4 = atoi(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI5 = atoi(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI6 = atoi(token);
		token = strtok(NULL, ",");
		if (token != NULL) SUTI7 = atoi(token);
        
        SUT(SUTI1, SUTI2, SUTI3, SUTI4, SUTI5, SUTI6, SUTI7, &SUTO6, &SUTO5, &SUTO4, &SUTO3, &SUTO2, &SUTO1);

        //vamos escrever no arquivo de resultados
        if (fprintf(results_file, "%f,%d,%d,%d,%d,%d,%d\n", time_id,SUTO6,SUTO5,SUTO4,SUTO3,SUTO2,SUTO1) < 0) {
        perror("Erro ao escrever no arquivo");
        fclose(results_file);
        return 1;
        }
    }

    fclose(input_file);
    fclose(results_file);

    return 0;
}
