#include <stdio.h>
#include <wchar.h>
#include <string.h>
#include <stdint.h>

#define ROR32(value, bits) ((value >> bits) | (value << (32 - bits)))

int calc_dll_hash(const wchar_t* name)
{
    uint32_t running_hash = 0;
    size_t length = (wcslen(name) +1 )* 2;
    uint32_t rot = 0;
    char c;

    for (size_t i = 0; i < length; ++i)
    {
        rot = ROR32(running_hash, 13); // ROT13
         c =*(char*)((char*)name + i);

        if (c < 0x61)
            running_hash = c + rot;
        else
            running_hash = c - 0x20 + rot;
    }

    return running_hash;
}


int main(int argc , char** argv[])
{

        int hash = calc_dll_hash(L"ntdll.dll");
        printf("0x%x\n",hash);

}
