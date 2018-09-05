import r2pipe
import json
import sys

r = r2pipe.open(sys.argv[1])

r.cmd('aaa')
func_start_addr = '0x804d680'
# to load the appropriate value of data structure of in the register 
addr_of_halt = '0x804d694'
func_end_addr = '0x0804d6f0'

config_addr_start = '0x0804d700'
config_addr_end = '0x0804e080'

def emu_decrypt(str_offset, str_len=100):
    r.cmd('s '+ func_start_addr)
    r.cmd('y {} @ {}'.format(str_len, str_offset))
    r.cmd('aei')
    r.cmd('aeim')
    r.cmd('aeip')
    r.cmd('aer')
    r.cmd('yy @ 0x100000')
    r.cmd('wx 0x00001000 @ 0x100064')
    r.cmd('wv {} @ 0x100068'.format(str_len))
    #r.cmd('wv `fl @ {}` @ 0x100018'.format(dcrypt_offset))
    r.cmd('aecu '+addr_of_halt)
    r.cmd('ar ecx=0x100064')
    r.cmd('aecu '+func_end_addr)
    return r.cmd('ps @ 0x100000)')


print('============>[String method]<=================')

for str_obj in r.cmd('psj 1 @@ str.*').split('\n'):
    str_obj = json.loads(str_obj)
    dcrypt_offset = str(str_obj['offset'])
    print(emu_decrypt(dcrypt_offset))

print('=============>[Reference method]<===============')
r.cmd('s '+config_addr_start)
data_refs = r.cmdj('agaj')
data_refs = list(map(lambda y : y['title'], data_refs['nodes']))
#print('reference data ', data_refs)
for str_obj in data_refs:
    dcrypt_offset = str_obj
    print(emu_decrypt(dcrypt_offset))


print('============>[Assembly search method]<===========')

r.cmd('e search.from = '+config_addr_start)
r.cmd('e search.to = '+config_addr_end)
push_list = r.cmdj('/atj push')
conf_cnt = 0
for inst in push_list:
    data_offset = inst['opstr'].replace('push ','')
    inst_addr = str(inst['addr'])

    if inst['size'] == 5 :
        dis = r.cmdj('pdj 5 @ '+inst_addr)
        conf_val = emu_decrypt(data_offset)
        print(conf_val)
