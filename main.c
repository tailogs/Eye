#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAXMEM 5

typedef enum {
    PUSH = 0x00d00201,
    POP = 0x00d00205,
    ADD = 0x00d00202,
    SUB = 0x00d00206,
    DIV = 0x00d00203,
    MUL = 0x00d00204,
    ENTER = 0x00d00211,
    TEST = 0x00d00209,
    PRINT = 0x00d00210,
    RAM = 0x00d00208,
    EXIT = 0x00d00207
} mnemonics;

const int code[] = {
    PUSH, 22,
    PUSH, 45,
    RAM,
    SUB,
    POP,
    PUSH, 23,
    PUSH, 9,
    PUSH, 5,
    RAM,
    PRINT,
    ADD,
    POP,
    PUSH, 7,
    PUSH, 7,
    RAM,
    ADD,
    POP,
    POP,
    ENTER,
    PRINT,
    TEST,
    EXIT
};


int stack[MAXMEM];
int sp = -1;
int ip = 0;
bool VM = true;

void decoder(int instr);

int main() {
    while (VM) {
        decoder(code[ip]);
        ip++;
    }
    system("pause");
    return 0;
}

int empty_sp() {
    return sp == -1 ? 1 : 0;
}

int full_sp() {
    return sp == MAXMEM ? 1 : 0;
}

void decoder(int instr) {
    switch (instr) {
        case PUSH: {
            if (full_sp()) {
                printf("Memory is full\n");
                break;
            }
            sp++;
            stack[sp] = code[++ip];
            break;
        }
        case POP: {
            if (empty_sp()) {
                printf("Memory is empty\n");
                break;
            }
            int pop_value = stack[sp--];
            printf("Result: %d \n", pop_value);
            break;
        }
        case ADD: {
            int a = stack[sp--];
            int b = stack[sp--];
            sp++;
            stack[sp] = b + a;
            printf("ADD->");
            break;
        }
        case SUB: {
            int a = stack[sp--];
            int b = stack[sp--];
            sp++;
            stack[sp] = a - b;
            printf("SUB->");
            break;
        }
        case DIV: {
            int a = stack[sp--];
            int b = stack[sp--];
            sp++;
            stack[sp] = a / b;
            printf("DIV->");
            break;
        }
        case MUL: {
            int a = stack[sp--];
            int b = stack[sp--];
            sp++;
            stack[sp] = a * b;
            printf("MUL->");
            break;
        }
        case RAM: {
            int x = sp;
            for (; x >= 0; --x) {
                printf("RAM[%u]: %u\n", x, stack[x]);
            }
            break;
        }
        case TEST: {
            stack[sp--] == 0x31337 ? printf("Good Pass!\n") : printf("Bad Pass!\n");
            break;
        }
        case PRINT: {
            printf("PRINT Stack[%u]: %u\n", sp, stack[sp]);
            break;
        }
        case ENTER: {
            printf("ENTER Password: ");
            sp++;
            scanf("%d", &stack[sp]);
            break;
        }
        case EXIT: {
            VM = false;
            printf("Exit VM\n");
            break;
        }
    }
}
