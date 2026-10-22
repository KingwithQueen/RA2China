from pathlib import Path
ROOT=Path(__file__).resolve().parent;S=ROOT/'evidence/movement-state-v10'
old=(ROOT/'evidence/movement-state-v9/objects_probe.c').read_text(encoding='utf-8')
head=old[:old.index('enum Op')].replace('ground_objects_bridge.h','ground_collision_bridge.h')
traps=old[old.index('static void patch('):old.index('static void initialize(')].replace('        lea eax,object_type\n','')
body=r'''
static unsigned char unit[0x700],cell[0x200],type[0x700],stack_data[8192];
static uint32_t host_stack,native_esp,native_ebp,native_resume,native_control,native_esi,native_edi;
static uint32_t frame,entry_object,entry_address=0x703905;
recomp_func_t recomp_lookup_manual(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a;return NULL; }
void ra2_state_movement_audit(unsigned a,uint32_t b,uint32_t c,uint32_t d) {(void)a;(void)b;(void)c;(void)d;}
'''
rest=r'''
int main(int argc,char **argv) {
    if(argc!=2) return 2;hold_image();map_original_image(argv[1]);
    unsigned char *stubs=VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);if(!stubs) return 2;
    const uint32_t boundaries[]={0x703AA9,0x703940};
    for(unsigned i=0;i<2;++i) {
        unsigned char *s=stubs+i*16;s[0]=0xC7;s[1]=5;uint32_t dest=P(&native_resume);memcpy(s+2,&dest,4);
        memcpy(s+6,&boundaries[i],4);s[10]=0xE9;uint32_t rel=P(trap)-P(s+15);memcpy(s+11,&rel,4);patch(boundaries[i],P(s));
    }
    unsigned blocked=0,upper=0,unordered=0;
    for(unsigned n=0;n<65536;++n) {
        uint32_t edge[]={0,0x80000000,1,0x80000001,0x3F800000,0xBF800000,0x7F800000,0xFF800000,0x7FC00000,0x7F800001};
        uint32_t bits=n%3 ? edge[(n/3)%10] : n*1664525u+1013904223u;
        memset(stack_data,0xA5,sizeof(stack_data));frame=P(stack_data+4096);
        MEM8(frame+0x11)=(uint8_t)((n>>7)&1);MEM32(frame+0x8C)=n%8;MEM32(frame+0x7C)=P(cell);
        F(unit,0x5AC)=P(type);F(type,0x5A4)=n%9;F(cell,0xEC)=(n/9)%10;
        MEM32(0x850EA0+((n/9)%10*9+n%9)*4)=bits;
        run_original();g_esp=frame;g_ebp=P(unit);g_ebx=P(cell);g_edi=n%8;
        int result=ra2_ground_terrain_tail_bridge();
        if((native_resume==0x703940)!=result || g_esp!=native_esp) {printf("tail mismatch %u bits=%x result=%d resume=%x\n",n,bits,result,native_resume);return 1;}
        blocked+=result!=0;upper+=MEM8(frame+0x11)!=0;unordered+=(bits&0x7FFFFFFF)>0x7F800000;
    }
    printf("{\"passed\":true,\"terrain_tail_cases\":65536,\"blocked\":%u,\"upper_layer\":%u,\"unordered_inputs\":%u}\n",blocked,upper,unordered);return 0;
}
'''
(S/'tail_probe.c').write_text(head+body+traps+rest,encoding='utf-8')
t=(ROOT/'build-objects-probe-v9.ps1').read_text(encoding='utf-8').replace('movement-state-v9','movement-state-v10').replace('objects','tail').replace('Objects','Tail')
t=t.replace('ground_tail_bridge.c','ground_collision_bridge.c').replace('gameplay\\ground_tail.c','gameplay\\ground_collision.c ..\\..\\ra2\\src\\gameplay\\ground_terrain.c')
(ROOT/'build-tail-probe-v10.ps1').write_text(t,encoding='utf-8')
