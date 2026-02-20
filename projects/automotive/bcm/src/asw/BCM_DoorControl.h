/*
 * BCM_DoorControl.h
 * 车门控制模块 - 头文件
 */

#ifndef BCM_DOOR_CONTROL_H
#define BCM_DOOR_CONTROL_H

/* ============================================
 * Includes
 * ============================================ */
#include "Std_Types.h"
#include "Dio.h"
#include "Dcm.h"

/* ============================================
 * API Services
 * ============================================ */

/* 初始化 */
void DoorControl_Init(void);

/* 10ms 周期性任务 */
void DoorControl_Runnable_10ms(void);

/* 100ms 周期性任务 */
void DoorControl_Runnable_100ms(void);

/* 外部调用 API */
Std_ReturnType BCM_UnlockAllDoors(void);
Std_ReturnType BCM_LockAllDoors(void);
Std_ReturnType BCM_GetDoorStatus(DoorStateType* fl, DoorStateType* fr, 
                                  DoorStateType* rl, DoorStateType* rr);

/* 版本信息 */
void DoorControl_GetVersionInfo(Std_VersionInfoType* versioninfo);

/* ============================================
 * 类型定义 (供外部使用)
 * ============================================ */

typedef enum {
    DOOR_STATE_CLOSED = 0,
    DOOR_STATE_OPEN = 1,
    DOOR_STATE_UNDEFINED = 2
} DoorStateType;

typedef enum {
    DOOR_CMD_NONE = 0,
    DOOR_CMD_UNLOCK = 1,
    DOOR_CMD_LOCK = 2,
    DOOR_CMD_OPEN = 3
} DoorCommandType;

/* ============================================
 * DTC 定义
 * ============================================ */
#define DTC_DOOR_MOTOR_OVERCURRENT    0x01
#define DTC_DOOR_SENSOR_FAULT         0x02
#define DTC_DOOR_ACTUATOR_FAULT       0x03
#define DTC_WINDOW_PINCH_PROTECTION   0x10

#endif /* BCM_DOOR_CONTROL_H */
