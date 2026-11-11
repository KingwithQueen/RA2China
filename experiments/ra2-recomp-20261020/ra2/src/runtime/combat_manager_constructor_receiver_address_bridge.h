#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_RECEIVER_ADDRESS_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_RECEIVER_ADDRESS_BRIDGE_H
#include <stdint.h>

/* 以32位无符号算术计算接收者地址，不访问该地址。 */
uint32_t ra2_manager_constructor_receiver_address_bridge(uint32_t base);
#endif
