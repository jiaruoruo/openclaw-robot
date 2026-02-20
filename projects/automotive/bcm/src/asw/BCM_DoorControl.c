/*
 * BCM_DoorControl.c
 * 车门控制模块 - 应用层软件组件 (SWC)
 * 符合 AUTOSAR 标准
 * 
 * 生成者: asw-engineer Agent
 * 日期: 2026-02-20
 */

#include "BCM_DoorControl.h"
#include "Rte_BCM.h"
#include "Std_Types.h"

/* ============================================
 * 模块配置
 * ============================================ */
#define DOOR_CONTROL_MODULE_ID         0x01
#define DOOR_CONTROL_VENDOR_ID       0x01
#define DOOR_CONTROL_SW_MAJOR_VERSION 1
#define DOOR_CONTROL_SW_MINOR_VERSION 0
#define DOOR_CONTROL_SW_PATCH_VERSION 0

/* ============================================
 * 类型定义
 * ============================================ */

/* 车门状态 */
typedef enum {
    DOOR_STATE_CLOSED = 0,
    DOOR_STATE_OPEN = 1,
    DOOR_STATE_UNDEFINED = 2
} DoorStateType;

/* 车窗状态 */
typedef enum {
    WINDOW_STATE_CLOSED = 0,
    WINDOW_STATE_OPEN = 1,
    WINDOW_STATE_MOVING_UP = 2,
    WINDOW_STATE_MOVING_DOWN = 3,
    WINDOW_STATE_PINCH_PROTECTION = 4
} WindowStateType;

/* 车门控制命令 */
typedef enum {
    DOOR_CMD_NONE = 0,
    DOOR_CMD_UNLOCK = 1,
    DOOR_CMD_LOCK = 2,
    DOOR_CMD_OPEN = 3
} DoorCommandType;

/* 车窗命令 */
typedef enum {
    WINDOW_CMD_NONE = 0,
    WINDOW_CMD_UP = 1,
    WINDOW_CMD_DOWN = 2,
    WINDOW_CMD_STOP = 3,
    WINDOW_CMD_AUTO = 4
} WindowCommandType;

/* 内部数据结构 */
typedef struct {
    DoorStateType     frontLeft;
    DoorStateType     frontRight;
    DoorStateType     rearLeft;
    DoorStateType     rearRight;
    DoorCommandType  cmd;
    boolean          lockButtonPressed;
    boolean          unlockButtonPressed;
} DoorControlInternalType;

/* ============================================
 * 静态变量 (SWC 内部状态)
 * ============================================ */
static DoorControlInternalType DoorControl_Data;
static uint32 DoorControl_TimeoutCounter = 0;
static boolean DoorControl_InitFlag = FALSE;

/* ============================================
 * 接口定义 (AUTOSAR RTE)
 * ============================================ */

/* 接收接口 - 来自 HMI 的命令 */
Std_ReturnType Rte_Read_DoorControl_Command(DoorCommandType* data)
{
    if (data == NULL_PTR) {
        return E_NOT_OK;
    }
    *data = DoorControl_Data.cmd;
    return E_OK;
}

Std_ReturnType Rte_Read_DoorControl_LockButton(boolean* pressed)
{
    if (pressed == NULL_PTR) {
        return E_NOT_OK;
    }
    *pressed = DoorControl_Data.lockButtonPressed;
    return E_OK;
}

Std_ReturnType Rte_Read_DoorControl_UnlockButton(boolean* pressed)
{
    if (pressed == NULL_PTR) {
        return E_NOT_OK;
    }
    *pressed = DoorControl_Data.unlockButtonPressed;
    return E_OK;
}

/* 发送接口 - 发送到 BSW 层 */
Std_ReturnType Rte_Write_DoorControl_DoorState(DoorStateType state)
{
    /* 调用 BSW Dio 驱动 */
    return Dio_WriteChannel(DIO_CHANNEL_DOOR_STATE, (boolean)state);
}

Std_ReturnType Rte_Write_DoorControl_LockActuator(boolean lock)
{
    /* 驱动门锁执行器 */
    return Dio_WriteChannel(DIO_CHANNEL_LOCK_ACTUATOR, lock);
}

Std_ReturnType Rte_Write_DoorControl_WindowActuator(WindowCommandType cmd)
{
    /* 驱动车窗电机 */
    switch (cmd) {
        case WINDOW_CMD_UP:
            Dio_WriteChannel(DIO_CHANNEL_WINDOW_UP, TRUE);
            Dio_WriteChannel(DIO_CHANNEL_WINDOW_DOWN, FALSE);
            break;
        case WINDOW_CMD_DOWN:
            Dio_WriteChannel(DIO_CHANNEL_WINDOW_UP, FALSE);
            Dio_WriteChannel(DIO_CHANNEL_WINDOW_DOWN, TRUE);
            break;
        case WINDOW_CMD_STOP:
            Dio_WriteChannel(DIO_CHANNEL_WINDOW_UP, FALSE);
            Dio_WriteChannel(DIO_CHANNEL_WINDOW_DOWN, FALSE);
            break;
        default:
            break;
    }
    return E_OK;
}

/* ============================================
 * 状态机实现
 * ============================================ */

/* 状态机状态 */
typedef enum {
    DOOR_SM_IDLE,
    DOOR_SM_LOCKING,
    DOOR_SM_UNLOCKING,
    DOOR_SM_ERROR
} DoorStateMachineType;

static DoorStateMachineType Door_SM_State = DOOR_SM_IDLE;

/* 状态机处理函数 */
static void DoorControl_StateMachine(void)
{
    switch (Door_SM_State) {
        case DOOR_SM_IDLE:
            /* 等待命令 */
            if (DoorControl_Data.cmd == DOOR_CMD_LOCK) {
                Door_SM_State = DOOR_SM_LOCKING;
            } else if (DoorControl_Data.cmd == DOOR_CMD_UNLOCK) {
                Door_SM_State = DOOR_SM_UNLOCKING;
            }
            break;
            
        case DOOR_SM_LOCKING:
            /* 执行锁门动作 */
            (void)Rte_Write_DoorControl_LockActuator(TRUE);
            DoorControl_Data.frontLeft = DOOR_STATE_CLOSED;
            DoorControl_Data.frontRight = DOOR_STATE_CLOSED;
            DoorControl_Data.rearLeft = DOOR_STATE_CLOSED;
            DoorControl_Data.rearRight = DOOR_STATE_CLOSED;
            Door_SM_State = DOOR_SM_IDLE;
            DoorControl_Data.cmd = DOOR_CMD_NONE;
            break;
            
        case DOOR_SM_UNLOCKING:
            /* 执行解锁动作 */
            (void)Rte_Write_DoorControl_LockActuator(FALSE);
            DoorControl_Data.frontLeft = DOOR_STATE_OPEN;
            DoorControl_Data.frontRight = DOOR_STATE_OPEN;
            DoorControl_Data.rearLeft = DOOR_STATE_OPEN;
            DoorControl_Data.rearRight = DOOR_STATE_OPEN;
            Door_SM_State = DOOR_SM_IDLE;
            DoorControl_Data.cmd = DOOR_CMD_NONE;
            break;
            
        case DOOR_SM_ERROR:
            /* 错误处理 - 保持门锁状态 */
            (void)Rte_Write_DoorControl_LockActuator(TRUE);
            Door_SM_State = DOOR_SM_IDLE;
            break;
            
        default:
            Door_SM_State = DOOR_SM_IDLE;
            break;
    }
}

/* ============================================
 * 防夹保护功能 (P0 - 安全关键)
 * ============================================ */
static boolean DoorControl_CheckPinchProtection(void)
{
    /* 读取防夹传感器 */
    boolean sensor_triggered = FALSE;
    
    (void)Dio_ReadChannel(DIO_CHANNEL_WINDOW_PINCH_SENSOR, &sensor_triggered);
    
    if (sensor_triggered == TRUE) {
        /* 检测到异物,停止车窗 */
        (void)Rte_Write_DoorControl_WindowActuator(WINDOW_CMD_STOP);
        /* 记录 DTC */
        Dcm_SetDTC(DTC_WINDOW_PINCH_PROTECTION, DTC_CONFIRMED);
    }
    
    return sensor_triggered;
}

/* ============================================
 * 运行nable (周期性任务)
 * ============================================ */

/* 10ms 任务 - 车门控制主函数 */
void DoorControl_Runnable_10ms(void)
{
    /* 读取输入 */
    (void)Rte_Read_DoorControl_Command(&DoorControl_Data.cmd);
    (void)Rte_Read_DoorControl_LockButton(&DoorControl_Data.lockButtonPressed);
    (void)Rte_Read_DoorControl_UnlockButton(&DoorControl_Data.unlockButtonPressed);
    
    /* 状态机处理 */
    DoorControl_StateMachine();
    
    /* 防夹检查 */
    (void)DoorControl_CheckPinchProtection();
    
    /* 超时计数 */
    if (DoorControl_TimeoutCounter > 0) {
        DoorControl_TimeoutCounter--;
    }
}

/* 100ms 任务 - 状态监控 */
void DoorControl_Runnable_100ms(void)
{
    /* 更新车门状态 */
    boolean fl_open, fr_open, rl_open, rr_open;
    
    (void)Dio_ReadChannel(DIO_CHANNEL_DOOR_FL, &fl_open);
    (void)Dio_ReadChannel(DIO_CHANNEL_DOOR_FR, &fr_open);
    (void)Dio_ReadChannel(DIO_CHANNEL_DOOR_RL, &rl_open);
    (void)Dio_ReadChannel(DIO_CHANNEL_DOOR_RR, &rr_open);
    
    DoorControl_Data.frontLeft = fl_open ? DOOR_STATE_OPEN : DOOR_STATE_CLOSED;
    DoorControl_Data.frontRight = fr_open ? DOOR_STATE_OPEN : DOOR_STATE_CLOSED;
    DoorControl_Data.rearLeft = rl_open ? DOOR_STATE_OPEN : DOOR_STATE_CLOSED;
    DoorControl_Data.rearRight = rr_open ? DOOR_STATE_OPEN : DOOR_STATE_CLOSED;
}

/* ============================================
 * 初始化函数
 * ============================================ */
void DoorControl_Init(void)
{
    /* 初始化内部变量 */
    DoorControl_Data.cmd = DOOR_CMD_NONE;
    DoorControl_Data.frontLeft = DOOR_STATE_UNDEFINED;
    DoorControl_Data.frontRight = DOOR_STATE_UNDEFINED;
    DoorControl_Data.rearLeft = DOOR_STATE_UNDEFINED;
    DoorControl_Data.rearRight = DOOR_STATE_UNDEFINED;
    DoorControl_Data.lockButtonPressed = FALSE;
    DoorControl_Data.unlockButtonPressed = FALSE;
    
    DoorControl_TimeoutCounter = 0;
    Door_SM_State = DOOR_SM_IDLE;
    DoorControl_InitFlag = TRUE;
}

/* ============================================
 * 故障处理
 * ============================================ */
void DoorControl_GetVersionInfo(Std_VersionInfoType* versioninfo)
{
    if (versioninfo != NULL_PTR) {
        versioninfo->moduleID = DOOR_CONTROL_MODULE_ID;
        versioninfo->vendorID = DOOR_CONTROL_VENDOR_ID;
        versioninfo->sw_major_version = DOOR_CONTROL_SW_MAJOR_VERSION;
        versioninfo->sw_minor_version = DOOR_CONTROL_SW_MINOR_VERSION;
        versioninfo->sw_patch_version = DOOR_CONTROL_SW_PATCH_VERSION;
    }
}

/* ============================================
 * 接口函数实现
 * ============================================ */

/* 解锁所有车门 */
Std_ReturnType BCM_UnlockAllDoors(void)
{
    if (Door_SM_State == DOOR_SM_IDLE) {
        DoorControl_Data.cmd = DOOR_CMD_UNLOCK;
        return E_OK;
    }
    return E_NOT_OK;
}

/* 锁止所有车门 */
Std_ReturnType BCM_LockAllDoors(void)
{
    if (Door_SM_State == DOOR_SM_IDLE) {
        DoorControl_Data.cmd = DOOR_CMD_LOCK;
        return E_OK;
    }
    return E_NOT_OK;
}

/* 获取车门状态 */
Std_ReturnType BCM_GetDoorStatus(DoorStateType* fl, DoorStateType* fr, 
                                  DoorStateType* rl, DoorStateType* rr)
{
    if ((fl == NULL_PTR) || (fr == NULL_PTR) || 
        (rl == NULL_PTR) || (rr == NULL_PTR)) {
        return E_NOT_OK;
    }
    
    *fl = DoorControl_Data.frontLeft;
    *fr = DoorControl_Data.frontRight;
    *rl = DoorControl_Data.rearLeft;
    *rr = DoorControl_Data.rearRight;
    
    return E_OK;
}

/*
 * 文件结束
 * ============================================ */
