/*
 * test_BCM_DoorControl.c
 * 车门控制模块 - 单元测试
 * 使用 Google Test 框架
 */

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "BCM_DoorControl.h"
#include "mock_Dio.h"
#include "mock_Dcm.h"

// 测试夹具
class DoorControlTest : public ::testing::Test {
protected:
    void SetUp() override {
        DoorControl_Init();
    }
};

// 测试用例: 初始化
TEST_F(DoorControlTest, Init_DefaultState) {
    DoorStateType fl, fr, rl, rr;
    
    BCM_GetDoorStatus(&fl, &fr, &rl, &rr);
    
    EXPECT_EQ(fl, DOOR_STATE_UNDEFINED);
    EXPECT_EQ(fr, DOOR_STATE_UNDEFINED);
    EXPECT_EQ(rl, DOOR_STATE_UNDEFINED);
    EXPECT_EQ(rr, DOOR_STATE_UNDEFINED);
}

// 测试用例: 解锁命令
TEST_F(DoorControlTest, UnlockCommand_SetsUnlockState) {
    Std_ReturnType ret = BCM_UnlockAllDoors();
    
    EXPECT_EQ(ret, E_OK);
    
    // 运行状态机
    DoorControl_Runnable_10ms();
    
    // 验证解锁状态
    DoorStateType fl, fr, rl, rr;
    BCM_GetDoorStatus(&fl, &fr, &rl, &rr);
    
    EXPECT_EQ(fl, DOOR_STATE_OPEN);
    EXPECT_EQ(fr, DOOR_STATE_OPEN);
}

// 测试用例: 锁止命令
TEST_F(DoorControlTest, LockCommand_SetsLockState) {
    Std_ReturnType ret = BCM_LockAllDoors();
    
    EXPECT_EQ(ret, E_OK);
    
    // 运行状态机
    DoorControl_Runnable_10ms();
    
    // 验证锁止状态
    DoorStateType fl, fr, rl, rr;
    BCM_GetDoorStatus(&fl, &fr, &rl, &rr);
    
    EXPECT_EQ(fl, DOOR_STATE_CLOSED);
    EXPECT_EQ(fr, DOOR_STATE_CLOSED);
}

// 测试用例: 防夹保护触发
TEST_F(DoorControlTest, PinchProtection_StopsWindow) {
    // 模拟防夹传感器触发
    EXPECT_CALL(mock_Dio, Dio_ReadChannel(DIO_CHANNEL_WINDOW_PINCH_SENSOR, ::testing::_))
        .WillOnce(::testing::DoAll(::testing::SetArgPointee<1>, TRUE));
    
    EXPECT_CALL(mock_Dio, Dio_WriteChannel(DIO_CHANNEL_WINDOW_UP, FALSE));
    EXPECT_CALL(mock_Dio, Dio_WriteChannel(DIO_CHANNEL_WINDOW_DOWN, FALSE));
    EXPECT_CALL(mock_Dcm, Dcm_SetDTC(DTC_WINDOW_PINCH_PROTECTION, DTC_CONFIRMED));
    
    boolean triggered = DoorControl_CheckPinchProtection();
    
    EXPECT_TRUE(triggered);
}

// 测试用例: 空指针检查
TEST_F(DoorControlTest, GetDoorStatus_NullPointer_ReturnsNotOK) {
    Std_ReturnType ret = BCM_GetDoorStatus(NULL, NULL, NULL, NULL);
    
    EXPECT_EQ(ret, E_NOT_OK);
}

// 测试用例: 版本信息
TEST_F(DoorControlTest, GetVersionInfo_ReturnsCorrectVersion) {
    Std_VersionInfoType version;
    DoorControl_GetVersionInfo(&version);
    
    EXPECT_EQ(version.sw_major_version, 1);
    EXPECT_EQ(version.sw_minor_version, 0);
    EXPECT_EQ(version.module_id, 0x01);
}

// 主函数
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
