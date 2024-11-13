#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#include "coupling_recorder.h"

int main() {
    recorder_start("../../data/couplings.csv");
    recorder_setCouplings(22, "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L11", "L12", "L13", "L14", "L15", "L16", "L17", "L18", "L19", "L20", "L21", "L22");

    int L1 = 1;
    char L2 = 2;
    float L3 = 3;
    double L4 = 4.44;
    long L5 = 5;
    short L6 = 6;
    unsigned int L7 = 7;
    unsigned char L8 = 8;
    unsigned long L9 = 9;
    unsigned short L10 = 10;
    long long L11 = 11;
    long double L12 = 12.2222;
    bool L13 = true;
    size_t L14 = 14;
    int8_t L15 = 15;
    int16_t L16 = 16;
    int32_t L17 = 17;
    int64_t L18 = 18;
    uint8_t L19 = 19;
    uint16_t L20 = 20;
    uint32_t L21 = 21;
    uint64_t L22 = 22;

    recorder_record("L1", &L1, "int");
    recorder_record("L2", &L2, "char");
    recorder_record("L3", &L3, "float");
    recorder_record("L4", &L4, "double");
    recorder_record("L5", &L5, "long");
    recorder_record("L6", &L6, "short");
    recorder_record("L7", &L7, "unsigned int");
    recorder_record("L8", &L8, "unsigned char");
    recorder_record("L9", &L9, "unsigned long");
    recorder_record("L10", &L10, "unsigned short");
    recorder_record("L11", &L11, "long long");
    recorder_record("L12", &L12, "long double");
    recorder_record("L13", &L13, "bool");
    recorder_record("L14", &L14, "size_t");
    recorder_record("L15", &L15, "int8_t");
    recorder_record("L16", &L16, "int16_t");
    recorder_record("L17", &L17, "int32_t");
    recorder_record("L18", &L18, "int64_t");
    recorder_record("L19", &L19, "uint8_t");
    recorder_record("L20", &L20, "uint16_t");
    recorder_record("L21", &L21, "uint32_t");
    recorder_record("L22", &L22, "uint64_t");

    recorder_save();

    L1 = 10;
    L2 = 20;
    L3 = 30;
    L4 = 40.44;
    L5 = 50;
    L6 = 60;
    L7 = 70;
    L8 = 80;
    L9 = 90;
    L10 = 100;
    L11 = 110;
    L12 = 120.2222;
    L13 = false;
    L14 = 140;
    L15 = 100;
    L16 = 160;
    L17 = 170;
    L18 = 180;
    L19 = 190;
    L20 = 200;
    L21 = 210;
    L22 = 220;

    recorder_record("L1", &L1, "int");
    recorder_record("L2", &L2, "char");
    recorder_record("L3", &L3, "float");
    recorder_record("L4", &L4, "double");
    recorder_record("L5", &L5, "long");
    recorder_record("L6", &L6, "short");
    recorder_record("L7", &L7, "unsigned int");
    recorder_record("L8", &L8, "unsigned char");
    recorder_record("L9", &L9, "unsigned long");
    recorder_record("L10", &L10, "unsigned short");
    recorder_record("L11", &L11, "long long");
    recorder_record("L12", &L12, "long double");
    recorder_record("L13", &L13, "bool");
    recorder_record("L14", &L14, "size_t");
    recorder_record("L15", &L15, "int8_t");
    recorder_record("L16", &L16, "int16_t");
    recorder_record("L17", &L17, "int32_t");
    recorder_record("L18", &L18, "int64_t");
    recorder_record("L19", &L19, "uint8_t");
    recorder_record("L20", &L20, "uint16_t");
    recorder_record("L21", &L21, "uint32_t");
    recorder_record("L22", &L22, "uint64_t");

    recorder_save();
    recorder_stop();
    
    return 0;
}