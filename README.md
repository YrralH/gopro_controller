# GoPro_Controller

#### 注意：此代码仅适配GoPro11与GoPro12相机，如需适配其他版本，请到官网查询对应命令。

### 使用说明：
#### 1.安装python包：
keyboard/bleak/asyncio
```
pip install keyboard
pip install bleak
pip install asyncio
```

#### 2.更改gopro_controller/lib_go_pro/cmd_controller.py  
更改22行LIST_CAMERA_ID_AND_VERSION_9中内容为：
相机序列号后四位-相机版本
```python
LIST_CAMERA_ID_AND_VERSION_9 = [
    '7222-12', #0
    '4406-12', #1
    '2789-12', #2 
    '3485-11', #3
    '2903-11', #4
    '0500-11', #5
    '0447-12', #6
    '5610-12', #7
    '0777-12'  #8
]
```
视连接相机需求按59-67行适当增减绑定按键
```python
keyboard.add_hotkey('0', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[0], List_Camera_Connected), loop))
keyboard.add_hotkey('1', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[1], List_Camera_Connected), loop))
keyboard.add_hotkey('2', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[2], List_Camera_Connected)loop))
keyboard.add_hotkey('3', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[3], List_Camera_Connected)loop))
keyboard.add_hotkey('4', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[4], List_Camera_Connected)loop))
keyboard.add_hotkey('5', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[5], List_Camera_Connected)loop))
keyboard.add_hotkey('6', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[6], List_Camera_Connected)loop))
keyboard.add_hotkey('7', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[7], List_Camera_Connected)loop))
keyboard.add_hotkey('8', lambda: asyncio.run_coroutine_threadsa(try_connect_camera_once(List_Camera_ID[8], List_Camera_Connected)loop))
```
#### 3.运行gopro_controller/cmd_multi.py

首次连接时，应将相机调至配对页面，并在电脑上按下对应绑定键进行配对，配对成功时应有提示：Pairing complete!

##### 若始终无法成功配对，请尝试重置相机或尝试使用其他电脑连接（我们也不知道为什么

相机全部连接成功后，按下对应按键进行设置，开始、停止录制或使相机睡眠

| 按键 | 功能         |
|------|--------------|
| A    | start record |
| S    | stop record  |
| Q    | set 60FPS    |
| W    | set 120FPS   |
| E    | set 240FPS   |
| R    | set 1080P    |
| T    | set 2.7K     |
| Y    | set 4K       |
| F    | sleep        |

-------------------------------------------------------------

### 其他信息：
#### 1.仓库意义：
提供对多个GoPro相机的连接，同时开始、停止录制，设置参数等功能
#### 2.创建动机：
某项目需要对多个GoPro相机实现同时控制，但是网上没找到，开源使大家免受折磨
#### 3.功能：
连接多个GoPro相机，控制开始、停止录制，设置参数，睡眠相机
#### 4.目标人群：
需要对多个GoPro相机进行控制，通过一台电脑控制多个相机的人群
#### 5.整体架构
cmd_multi.py：运行入口
lib_go_pro/batch_options.py：定义多个批处理函数，同步执行对多个相机的同一操作

lib_go_pro/cmd_controller.py：定义LIST_CAMERA_ID_AND_VERSION_9传入相机参数-版本
定义multi_controller实现操作快捷键，保持连接

lib_go_pro/connect.py：连接ble函数

lib_go_pro/go_pro_ble.py：定义GoPro类，实现连接相机与各指令实际功能

lib_go_pro/logger.py：初始化logger（异步程序需要专门的logger）
