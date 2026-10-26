#pragma once
#include <stdint.h>
/* 返回0表示已经完成原ABI收尾；否则返回同一原函数内的后继地址。 */
uint32_t ra2_unit_death_handoff_bridge(void);
uint32_t ra2_infantry_death_handoff_bridge(void);
void ra2_unit_death_finish_bridge(void);
void ra2_infantry_death_finish_bridge(void);
void ra2_foot_uninit_bridge(void);
void ra2_object_uninit_bridge(void);
void ra2_object_delete_drain_bridge(void);
