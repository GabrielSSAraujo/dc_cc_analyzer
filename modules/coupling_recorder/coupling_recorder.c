#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

#include "coupling_recorder.h"
#include "list.h"

// Internal modules variables
FILE *_file = NULL;
List *_list = NULL;
int _header_written = 0;
int _couplings_set = 0;

void recorder_start(const char* file_name) {
    if (_file != NULL) {
        return;
    }
    
    _file = fopen(file_name, "w+");
    if (_file == NULL) {
        printf("ERROR: Could not open %s file!", file_name);
    }
}

void recorder_setCouplings(int size, ...) {
    if (!_couplings_set) {
        _list = list_create(size);
        
        // Init each coupling
        va_list args;
        va_start(args, size);

        for (int i = 0; i < size; i++) {
            list_setNodeName(_list, i, va_arg(args, const char*));
        }

        va_end(args);
        _couplings_set = 1;
    }
}

void recorder_record(const char* name, void *data, const char *type) {
    if (!_couplings_set) {
        printf("Error: No coupling was set!\n");
        return;
    }

    int id = list_getNodeId(_list, name);
    if (id < 0) {
        printf("ERROR: Could not find coupling named %s!\n", name);
        return;
    }

    list_setNodeData(_list, id, data, type);
}

void recorder_save(float time) {
    if (!_couplings_set) {
        return;
    }

    // Check if header of csv was written
    if (!_header_written) {
        fprintf(_file, "Time, ");

        // Write csv header
        for (int i = 0; i < _list->size; i++) {
            list_printNodeNameToFile(_list, i, _file);      

            // Write separator
            if (i < _list->size - 1) {
                fprintf(_file, ", ");
            } else {
                fprintf(_file, "\n");
            }
        }
        _header_written = 1;
    }

    // Print time
    fprintf(_file, "%f, ", time);

    // Print values
    for (int i = 0; i < _list->size; i++) {
        list_printNodeDataToFile(_list, i, _file);      

        // Write separator
        if (i < _list->size - 1) {
            fprintf(_file, ", ");
        } else {
            fprintf(_file, "\n");
        }
    }
}

void recorder_stop() {
    _header_written = 0;
    _couplings_set = 0;
    if (!_couplings_set) {
        list_delete(_list);
    }
    fclose(_file);
}
