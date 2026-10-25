"""Independent readonly type identity and locomotor snapshots."""
from run_batch_v68 import *
source=(R/'make_bridge_catalog_v68.py').read_text(encoding='utf-8')
marker="q=S/'bridge_catalog_observer.c'";assert source.count(marker)==1
block=r'''
    for(uint32_t i=0;i<U32(0xA40C30);++i) {
        uint32_t actor=U32(U32(0xA40C24)+i*4),kind=U32(actor);
        if(kind!=0x7A3540 && kind!=0x7ADDF8)continue;
        uint32_t type=U32(actor+(kind==0x7A3540?0x5A8:0x5AC)),active=U32(actor+0x564);
        fprintf(state_file,"{\"kind\":\"fixture-other-locomotor\",\"frame\":%u,\"id\":%u,\"type\":\"%.24s\",\"locomotor\":%u}\n",frame,U32(actor+0x10),(char *)(uintptr_t)(type+0x24),active?U32(active):0);
    }
'''
source=source.replace(marker,"t=t.replace('    write_cell_catalog(frame);','    write_cell_catalog(frame);'+"+repr(block)+")\n"+marker)
source=source.replace('bridge_catalog_observer','other_movement_observer').replace('bridge-catalog-observer','other-movement-observer').replace('bridge-catalog-build-arguments','other-movement-build-arguments')
exec(compile(source,str(Path(__file__)),'exec'),dict(__name__='__main__',__file__=str(Path(__file__)),sys=sys))
