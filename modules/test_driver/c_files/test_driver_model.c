#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../coupling_recorder/coupling_recorder.h"

// include SutFileName.h

int main()
{
    /*init data*/
// init_var
    float time_id;
    // Criar arquivos CSV
    // inputFile_path
    // resultFile_path

    if (input_file == NULL || results_file == NULL)
    {
        printf("Erro ao abrir os arquivos.\n");
        return 1;
    }

    char line[256];      // variável para armazenar a linha lida do arquivo de entrada

    // Escrever a primeira linha (cabeçalho)
    // HeaderPlaceholder

    recorder_start("./data/couplings.csv");

    // Ignore header
    fgets(line, sizeof(line), input_file);

    // Ler o arquivo de entrada
    while (fgets(line, sizeof(line), input_file)) {
        // Remover o caractere de nova linha, se presente
        line[strcspn(line, "\n")] = '\0';

        // Dividir a linha em tokens
        char *token = strtok(line, ",");

        // leitura dos valores do input.csv e atribuição a variáveis.
        //primeira coluna: convencionado que é o time_id
        if (token != NULL) time_id= atof(token);
// TokenAssignment
        
        // sut()
        recorder_save(time_id);

        //vamos escrever no arquivo de resultados
        // RESULTS.CSV
        perror("Erro ao escrever no arquivo");
        fclose(results_file);
        return 1;
        }
    }

    recorder_stop();
    fclose(input_file);
    fclose(results_file);

    return 0;
}
