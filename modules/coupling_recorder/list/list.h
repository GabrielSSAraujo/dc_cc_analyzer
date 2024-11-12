#ifndef LIST_H
#define LIST_H
#include <stdio.h>

typedef enum {
    INT,
    CHAR,
    FLOAT,
    DOUBLE,
    LONG,
    SHORT,
    UNSIGNED_INT,
    UNSIGNED_CHAR,
    UNSIGNED_LONG,
    UNSIGNED_SHORT,
    LONG_LONG,
    LONG_DOUBLE,
    BOOL,
    SIZE_T,
    INT8_T,
    INT16_T,
    INT32_T,
    INT64_T,
    UINT8_T,
    UINT16_T,
    UINT32_T,
    UINT64_T
} DataType;

typedef struct Node {
    const char *name;
    void *data;
    DataType type;
} Node;

typedef struct List {
    Node *nodes;
    int size;
} List;

List* list_create(int size);
void list_delete(List *list);
void list_setNodeName(List *list, int id, const char *name);
void list_setNodeData(List *list, int id, void *data, const char *type);
void list_printNodeDataToFile(List *list, int id, FILE *file);
void list_printNodeNameToFile(List *list, int id, FILE *file);
int list_getNodeId(List *list, const char *name);

#endif