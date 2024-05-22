//inline assembly
#include <stdio.h>

void other_function();
void other_function_2();

void (*backup)();                            // backup address


int main() {
    int i = 0x13;                            // we expect this to be on the stack
    int j = 0;

    __asm(".intel_syntax noprefix;"           // intel is my preference
            "mov ecx, eax;"                   // move i from eax into ecx
            "inc ecx;"
	    ".att_syntax prefix"                                                         
            :"=c"(j)                          // outputs "c" -> ecx into j
            :"a"(i)                           // the "a" -> i into eax
                                              // clobbered registers, none
            );
            
    printf("Our i value is: %d\n", i);        // we expect decimal 19
    printf("Our j value is: %d\n\n", j);      // we expect decimal 20
    
    printf("Calling other_function...\n");
    printf("-------------------------\n");
    
    other_function();                         // call other_function
    
    printf("-------------------------\n");
    return 0;                                 
}

void other_function_2(){                       // this will NOT execute
                                               // we'll set our return 
                                               // here with inline assembly
    
    printf("THIS IS other_function_2!\n");


}



void other_function(){
    
    void (*p)();
    p = other_function_2;                     // address of other_function_2
    
    __asm(".intel_syntax noprefix;"           // spoof stack frame
            "mov %0, [rbp+0x8];"
            "mov [rbp+0x8], %1;"
            ".att_syntax prefix"			// ..._2 stack frame
            :"=c"(backup)
            :"a"(p)
            
            );
    
    printf("THIS IS other_function!\n");       // frame has other_function_2
    
    
    __asm(".intel_syntax noprefix;"            // restore old address
            "mov [rbp+0x8], %0;"
	    ".att_syntax prefix"
            :
            :"r"(backup)
            
            );
                        
    return;                                    
}

//from:https://blog.malicious.group/inline-assembly/
