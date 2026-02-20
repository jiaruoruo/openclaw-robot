# BCM (Body Control Module) 需求文档

> 汽车车身控制模块 - 软件需求规范

---

## 1. 项目概述

### 1.1 项目名称
BCM (Body Control Module) 车身控制模块软件

### 1.2 项目目标
开发一款面向新能源汽车的车身控制模块软件，实现对车身电器设备的控制、监控和管理。

### 1.3 适用范围
- 纯电动汽车
- 混合动力汽车
- 乘用车 (A级-B级)

---

## 2. 功能需求

### 2.1 车门控制 (Door Control)

| 功能 | 描述 | 优先级 |
|------|------|--------|
| DOOR_UNLOCK | 车门解锁 | P0 |
| DOOR_LOCK | 车门闭锁 | P0 |
| DOOR_STATUS | 车门状态监测 | P0 |
| WINDOW_UP | 车窗上升 | P1 |
| WINDOW_DOWN | 车窗下降 | P1 |
| WINDOW_AUTO | 车窗一键升降 | P1 |
| WINDOW_PINCH | 车窗防夹 | P0 |

### 2.2 灯光控制 (Light Control)

| 功能 | 描述 | 优先级 |
|------|------|--------|
| LIGHT_LOW_BEAM | 近光灯控制 | P0 |
| LIGHT_HIGH_BEAM | 远光灯控制 | P0 |
| LIGHT_TURN_LEFT | 左转向灯 | P0 |
| LIGHT_TURN_RIGHT | 右转向灯 | P0 |
| LIGHT_HAZARD | 危险警告灯 | P0 |
| LIGHT_BRAKE | 制动灯 | P0 |
| LIGHT_REVERSE | 倒车灯 | P0 |
| LIGHT_FOG_FRONT | 前雾灯 | P1 |
| LIGHT_FOG_REAR | 后雾灯 | P1 |
| LIGHT_DOME | 室内灯控制 | P2 |
| LIGHT_DOME_AUTO | 室内灯自动控制 | P2 |

### 2.3 雨刮控制 (Wiper Control)

| 功能 | 描述 | 优先级 |
|------|------|--------|
| WIPER_LOW | 雨刮低速 | P0 |
| WIPER_HIGH | 雨刮高速 | P0 |
| WIPER_INT | 雨刮间歇 | P1 |
| WIPER_AUTO | 雨刮自动 | P1 |
| WIPER_WASH | 雨刮清洗 | P0 |
| WIPER_PARK | 雨刮归位 | P1 |

### 2.4 喇叭控制 (Horn Control)

| 功能 | 描述 | 优先级 |
|------|------|--------|
| HORN_LOW | 喇叭低音 | P0 |
| HORN_HIGH | 喇叭高音 | P0 |
| HORN_AUTOMATIC | 喇叭自动触发 | P2 |

### 2.5 防盗报警 (Theft Alarm)

| 功能 | 描述 | 优先级 |
|------|------|--------|
| ALARM_ARM | 防盗arming | P0 |
| ALARM_DISARM | 防盗disarm | P0 |
| ALARM_TRIGGER | 报警触发 | P0 |
| ALARM_STATUS | 报警状态 | P1 |
| ALARM_SIREN | 警笛控制 | P0 |
| ALARM_FLASH | 报警闪烁 | P1 |

---

## 3. 非功能需求

### 3.1 性能需求

| 指标 | 要求 |
|------|------|
| 启动时间 | < 200ms |
| 响应时间 (命令执行) | < 50ms |
| CAN 报文处理周期 | 10ms / 100ms |
| 任务调度周期 | 5ms / 10ms |

### 3.2 安全需求 (ISO 26262)

| 功能 | ASIL 等级 |
|------|-----------|
| 车门控制 | ASIL B |
| 制动灯控制 | ASIL B |
| 转向灯控制 | ASIL A |
| 喇叭控制 | ASIL A |
| 防盗报警 | ASIL B |

### 3.3 通信需求

| 接口 | 协议 | 速率 |
|------|------|------|
| CAN | CAN 2.0 | 500kbps |
| LIN | LIN 2.x | 19.2kbps |
| Ethernet | 100BASE-T1 | 100Mbps |

### 3.4 资源需求

| 资源 | 要求 |
|------|------|
| Flash | 512KB |
| RAM | 64KB |
| CPU | ARM Cortex-M4F @ 120MHz |

---

## 4. 输入输出定义

### 4.1 CAN 接收信号

| 信号名 | 周期 | 描述 |
|--------|------|------|
| BCM_Cmd_Unlock | 事件 | 解锁命令 |
| BCM_Cmd_Lock | 事件 | 闭锁命令 |
| BCM_Cmd_Wiper | 100ms | 雨刮命令 |
| BCM_Cmd_Light | 100ms | 灯光命令 |
| BCM_Cmd_Horn | 事件 | 喇叭命令 |
| BCM_Cmd_Alarm | 事件 | 报警命令 |

### 4.2 CAN 发送信号

| 信号名 | 周期 | 描述 |
|--------|------|------|
| BCM_Status_Door | 100ms | 车门状态 |
| BCM_Status_Light | 100ms | 灯光状态 |
| BCM_Status_Wiper | 100ms | 雨刮状态 |
| BCM_Status_Alarm | 100ms | 报警状态 |
| BCM_DIAG_Response | 事件 | 诊断响应 |

---

## 5. 诊断需求

### 5.1 DTC (Diagnostic Trouble Codes)

| DTC | 描述 | 类型 |
|-----|------|------|
| B1000 | CAN通信故障 | 故障 |
| B1001 | LIN通信故障 | 故障 |
| B2000 | 车门电机过流 | 故障 |
| B2001 | 车窗电机过流 | 故障 |
| B3000 | 灯光负载过流 | 故障 |
| B3001 | 喇叭负载过流 | 故障 |
| B4000 | 传感器故障 | 故障 |

### 5.2 服务

| SID | 服务 | 描述 |
|-----|------|------|
| 0x10 | DiagnosticSessionControl | 诊断会话 |
| 0x11 | ECUReset | ECU复位 |
| 0x19 | ReadDTCInformation | 读取DTC |
| 0x14 | ClearDTCInformation | 清除DTC |
| 0x22 | ReadDataByIdentifier | 读取数据 |
| 0x2E | WriteDataByIdentifier | 写入数据 |
| 0x31 | RoutineControl | 例程控制 |

---

## 6. 变体说明

### 6.1 车型变体

| 车型 | 配置差异 |
|------|----------|
| 入门型 | 无后雾灯、无自动雨刮 |
| 舒适型 | 完整配置 |
| 豪华型 | +后视镜加热、+大灯清洗 |

### 6.2 配置矩阵

| 功能 | 入门型 | 舒适型 | 豪华型 |
|------|--------|--------|--------|
| 车门控制 | ✅ | ✅ | ✅ |
| 车窗防夹 | ✅ | ✅ | ✅ |
| 雨刮自动 | ❌ | ✅ | ✅ |
| 前雾灯 | ❌ | ✅ | ✅ |
| 后雾灯 | ❌ | ❌ | ✅ |
| 室内灯自动 | ❌ | ✅ | ✅ |

---

## 7. 验收标准

### 7.1 功能验收
- [ ] 所有P0功能测试通过
- [ ] 所有P1功能测试通过
- [ ] 变体配置测试通过
- [ ] 诊断功能测试通过

### 7.2 安全验收
- [ ] ASIL B 功能通过安全测试
- [ ] 故障注入测试通过
- [ ] 背靠背测试通过

### 7.3 性能验收
- [ ] 启动时间 < 200ms
- [ ] 响应时间 < 50ms
- [ ] CPU负载 < 70%

---

*文档版本: 1.0*
*创建日期: 2026-02-20*
*状态: 草稿*
