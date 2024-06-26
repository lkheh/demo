import re, binascii
from capstone import *
from unicorn import *
from unicorn.x86_const import *

def unicorn_block(block):
    # init unicorn
    mu = Uc(UC_ARCH_X86, UC_MODE_32)
    # setup memory and write code to memory
    ADDRESS = 0x1000000
    mu.mem_map(ADDRESS, 4 * 1024 * 1024)
    mu.mem_write(ADDRESS, block)
    # set these registers to 0x7f 
    mu.reg_write(UC_X86_REG_ESI, 0x7f)
    mu.reg_write(UC_X86_REG_EDI, 0x7f)
    mu.reg_write(UC_X86_REG_EBX, 0x7f)
    mu.reg_write(UC_X86_REG_ECX, 0x7f)
    # setup stack and base pointer
    mu.reg_write(UC_X86_REG_ESP, ADDRESS + 0x100000)
    mu.reg_write(UC_X86_REG_EBP, ADDRESS + 0x200000)
    # emulate machine code in infinite time
    try:
        mu.emu_start(ADDRESS, ADDRESS + len(block))
    except Exception as E:
        print (E)
    # read value in EBP (pointer to base)
    ebp = mu.reg_read(UC_X86_REG_EBP)
    # read memory from EBP - 0x100000, and strip \x00 bytes by decoding
    data = mu.mem_read(ebp - 0x100000, 0x100000).decode("utf-8")
    print (data)
    return


md = Cs(CS_ARCH_X86, CS_MODE_32) 
md.detail = True
md.skipdata = True
data=open("1.bin", "rb").read()
rule = re.compile(b"\x8A\x44.{2,3}|\x8A\x84.{2,6}") 
matches = rule.finditer(data) 

for m in matches:
    string = data[m.start():m.end()]
    disasm = list(md.disasm(string, 0, len(string)))
    offset = disasm[0].operands[1].value.mem.disp
    data_block = data[m.start()-500:m.end()]
    disasm_list = list(md.disasm(data_block, 0, len(data_block)))
    for i in reversed(disasm_list):
            if i.mnemonic == "mov" and i.operands[0].type == 3:
                if i.operands[0].value.mem.disp == offset:
                    print ("found stack string creation address > %08x, offset > %08x" % (i.address, offset))
                    smaller_block = data[((m.start()-500) + i.address ) : m.end() + 75]
                    for y in md.disasm(smaller_block, 0, len(smaller_block)):
                        if y.mnemonic == "jb":            
                            print ("found end of loop > %08x" % y.address)
                            smaller_block = smaller_block[:y.address+y.size]
                            print (binascii.hexlify(smaller_block))
                            break

