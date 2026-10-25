"""Add readonly Tube route/waypoint snapshots to the established isolated recorder."""
from run_batch_v66 import *
source=(R/'make_bridge_catalog_v66.py').read_text(encoding='utf-8')
marker="q=S/'bridge_catalog_observer.c'";assert source.count(marker)==1
# Keep the generated C string separate from the Python template to avoid escaping ambiguity.
block='''
    for (uint32_t index=0; index<U32(0xA40C30); ++index)
    {
        uint32_t object=U32(U32(0xA40C24)+index*4);
        if(U32(object)!=0x7ADDF8 || !U32(object+0x564) || U32(U32(object+0x564))!=0x7A04CC) continue;
        uint32_t count=U32(0x8661D8), route=U8(object+0x574), waypoint=U8(object+0x575);
        uint32_t tube=route<count ? U32(U32(0x8661CC)+route*4):0;
        fprintf(state_file,"{\\"kind\\":\\"fixture-tube-snapshot\\",\\"frame\\":%u,\\"id\\":%u,\\"route\\":%u,\\"waypoint\\":%u,\\"tube_count\\":%u,\\"steps\\":%u,\\"entrance\\":[%d,%d],\\"exit\\":[%d,%d],\\"approach\\":[%d,%d,%d]}\\n",
            frame,U32(object+0x10),route,waypoint,count,tube?U32(tube+0x1C0):0,
            tube?(int16_t)U16(tube+0x24):0,tube?(int16_t)U16(tube+0x26):0,
            tube?(int16_t)U16(tube+0x28):0,tube?(int16_t)U16(tube+0x2A):0,
            I32(object+0x45C),I32(object+0x460),I32(object+0x464));
    }
'''
source=source.replace(marker,"t=t.replace('    write_cell_catalog(frame);','    write_cell_catalog(frame);'+"+repr(block)+")\n"+marker)
source=source.replace('bridge_catalog_observer','channel_observer').replace('bridge-catalog-observer','channel-observer').replace('bridge-catalog-build-arguments','channel-observer-build-arguments')
exec(compile(source,str(Path(__file__)), 'exec'),dict(__name__='__main__',__file__=str(Path(__file__)),sys=sys))
