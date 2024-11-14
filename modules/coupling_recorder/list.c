#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "list.h"

List* list_create(int size) {
    List *list = (List*)malloc(sizeof(List));
    list->nodes = (Node*)malloc(size*sizeof(Node));
    list->size = size;

    for (int i = 0; i < list->size; i++) {
        list->nodes[i].data = NULL;
    }

    return list;
}

void list_delete(List *list) {
    for (int i = 0; i < list->size; i++) {
        if (list->nodes[i].data != NULL) {
            free(list->nodes[i].data);
        }
    }
    free(list->nodes);
    free(list);
}

void list_setNodeName(List *list, int id, const char *name) {
    if (id >= list->size) {
        return;
    }
    list->nodes[id].name = name;
}

void list_setNodeData(List *list, int id, void *data, const char *type) {
    if (id >= list->size) {
        return;
    }

    if (!strcmp(type, "int")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(int));
        }
        list->nodes[id].type = INT;
        memcpy(list->nodes[id].data, data, sizeof(int));
    }
    else if (!strcmp(type, "char")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(char));
        }
        list->nodes[id].type = CHAR;
        memcpy(list->nodes[id].data, data, sizeof(char));
    }
    else if (!strcmp(type, "float")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(float));
        }
        list->nodes[id].type = FLOAT;
        memcpy(list->nodes[id].data, data, sizeof(float));
    }
    else if (!strcmp(type, "double")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(double));
        }
        list->nodes[id].type = DOUBLE;
        memcpy(list->nodes[id].data, data, sizeof(double));
    }
    else if (!strcmp(type, "long")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(long));
        }
        list->nodes[id].type = LONG;
        memcpy(list->nodes[id].data, data, sizeof(long));
    }
    else if (!strcmp(type, "short")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(short));
        }
        list->nodes[id].type = SHORT;
        memcpy(list->nodes[id].data, data, sizeof(short));
    }
    else if (!strcmp(type, "unsigned int")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(unsigned int));
        }
        list->nodes[id].type = UNSIGNED_INT;
        memcpy(list->nodes[id].data, data, sizeof(unsigned int));
    }
    else if (!strcmp(type, "unsigned char")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(unsigned char));
        }
        list->nodes[id].type = UNSIGNED_CHAR;
        memcpy(list->nodes[id].data, data, sizeof(unsigned char));
    }
    else if (!strcmp(type, "unsigned long")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(unsigned long));
        }
        list->nodes[id].type = UNSIGNED_LONG;
        memcpy(list->nodes[id].data, data, sizeof(unsigned long));
    }
    else if (!strcmp(type, "unsigned short")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(unsigned short));
        }
        list->nodes[id].type = UNSIGNED_SHORT;
        memcpy(list->nodes[id].data, data, sizeof(unsigned short));
    }
    else if (!strcmp(type, "long long")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(long long));
        }
        list->nodes[id].type = LONG_LONG;
        memcpy(list->nodes[id].data, data, sizeof(long long));
    }
    else if (!strcmp(type, "long double")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(long double));
        }
        list->nodes[id].type = LONG_DOUBLE;
        memcpy(list->nodes[id].data, data, sizeof(long double));
    }
    else if (!strcmp(type, "bool")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(bool));
        }
        list->nodes[id].type = BOOL;
        memcpy(list->nodes[id].data, data, sizeof(bool));
    }
    else if (!strcmp(type, "size_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(size_t));
        }
        list->nodes[id].type = SIZE_T;
        memcpy(list->nodes[id].data, data, sizeof(size_t));
    }
    else if (!strcmp(type, "int8_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(int8_t));
        }
        list->nodes[id].type = INT8_T;
        memcpy(list->nodes[id].data, data, sizeof(int8_t));
    }
    else if (!strcmp(type, "int16_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(int16_t));
        }
        list->nodes[id].type = INT16_T;
        memcpy(list->nodes[id].data, data, sizeof(int16_t));
    }
    else if (!strcmp(type, "int32_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(int32_t));
        }
        list->nodes[id].type = INT32_T;
        memcpy(list->nodes[id].data, data, sizeof(int32_t));
    }
    else if (!strcmp(type, "int64_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(int64_t));
        }
        list->nodes[id].type = INT64_T;
        memcpy(list->nodes[id].data, data, sizeof(int64_t));
    }
    else if (!strcmp(type, "uint8_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(uint8_t));
        }
        list->nodes[id].type = UINT8_T;
        memcpy(list->nodes[id].data, data, sizeof(uint8_t));
    }
    else if (!strcmp(type, "uint16_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(uint16_t));
        }
        list->nodes[id].type = UINT16_T;
        memcpy(list->nodes[id].data, data, sizeof(uint16_t));
    }
    else if (!strcmp(type, "uint32_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(uint32_t));
        }
        list->nodes[id].type = UINT32_T;
        memcpy(list->nodes[id].data, data, sizeof(uint32_t));
    }
    else if (!strcmp(type, "uint64_t")) {
        if (list->nodes[id].data == NULL) {
            list->nodes[id].data = malloc(sizeof(uint64_t));
        }
        list->nodes[id].type = UINT64_T;
        memcpy(list->nodes[id].data, data, sizeof(uint64_t));
    }
}

void list_printNodeDataToFile(List *list, int id, FILE *file) {
    if (id >= list->size) {
        return;
    }
    
    Node node = list->nodes[id];

    if (node.data == NULL) {
        fprintf(file, "NULL");
        return;        
    }

    switch (node.type) {
        case INT:
            fprintf(file, "%d", *(int*)node.data);
            break;
        case CHAR:
            fprintf(file, "%d", *(char*)node.data);
            break;
        case FLOAT:
            fprintf(file, "%f", *(float*)node.data);
            break;
        case DOUBLE:
            fprintf(file, "%lf", *(double*)node.data);
            break;
        case LONG:
            fprintf(file, "%ld", *(long*)node.data);
            break;
        case SHORT:
            fprintf(file, "%hd", *(short*)node.data);
            break;
        case UNSIGNED_INT:
            fprintf(file, "%u", *(unsigned int*)node.data);
            break;
        case UNSIGNED_CHAR:
            fprintf(file, "%u", *(unsigned char*)node.data);
            break;
        case UNSIGNED_LONG:
            fprintf(file, "%lu", *(unsigned long*)node.data);
            break;
        case UNSIGNED_SHORT:
            fprintf(file, "%hu", *(unsigned short*)node.data);
            break;
        case LONG_LONG:
            fprintf(file, "%lld", *(long long*)node.data);
            break;
        case LONG_DOUBLE:
            fprintf(file, "%Lf", *(long double*)node.data);
            break;
        case BOOL:
            fprintf(file, "%d", *(bool*)node.data);
            break;
        case SIZE_T:
            fprintf(file, "%zu", *(size_t*)node.data);
            break;
        case INT8_T:
            fprintf(file, "%d", *(int8_t*)node.data);
            break;
        case INT16_T:
            fprintf(file, "%d", *(int16_t*)node.data);
            break;
        case INT32_T:
            fprintf(file, "%d", *(int32_t*)node.data);
            break;
        case INT64_T:
            fprintf(file, "%ld", *(int64_t*)node.data);
            break;
        case UINT8_T:
            fprintf(file, "%u", *(uint8_t*)node.data);
            break;
        case UINT16_T:
            fprintf(file, "%u", *(uint16_t*)node.data);
            break;
        case UINT32_T:
            fprintf(file, "%u", *(uint32_t*)node.data);
            break;
        case UINT64_T:
            fprintf(file, "%lu", *(uint64_t*)node.data);
            break;
    }
}

void list_printNodeNameToFile(List *list, int id, FILE *file) {
    if (id >= list->size) {
        return;
    }
    
    Node node = list->nodes[id];
    if (node.name == NULL) {
        fprintf(file, "NULL");
        return;        
    }
    fprintf(file, "%s", node.name);
}

int list_getNodeId(List *list, const char *name) {
    for (int i = 0; i < list->size; i++) {
        if (!strcmp(name, list->nodes[i].name)) {
            return i;
        }
    }

    return -1;
}
