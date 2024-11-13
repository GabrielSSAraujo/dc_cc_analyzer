#ifndef COUPLING_RECORDER_H
#define COUPLING_RECORDER_H

void recorder_start(const char* file_name);
void recorder_setCouplings(int size, ...);
void recorder_record(const char* name, void *data, const char *type);
void recorder_save(float time);
void recorder_stop();

#endif