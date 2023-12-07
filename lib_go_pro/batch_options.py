

import sys
import asyncio
from typing import Optional
import keyboard

from go_pro_ble import GoPro

from typing import List, Dict, Tuple


async def batch_start_record(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        list_task.append(asyncio.create_task(camera.start_record()))
    await asyncio.gather(list_task)


async def batch_stop_record(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        list_task.append(asyncio.create_task(camera.stop_record()))
    await asyncio.gather(list_task)
    return


async def batch_set_60FPS(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        list_task.append(asyncio.create_task(camera.setting_60FPS()))
    await asyncio.gather(list_task)


async def batch_set_120FPS(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        list_task.append(asyncio.create_task(camera.setting_120FPS()))
    await asyncio.gather(list_task)


async def batch_set_240FPS(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        list_task.append(asyncio.create_task(camera.setting_240FPS()))
    await asyncio.gather(list_task)


async def batch_set_4K(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        if camera.ver == '12':
            list_task.append(asyncio.create_task(camera.setting_12_4K()))
        elif camera.ver == '11':
            list_task.append(asyncio.create_task(camera.setting_11_4K()))
        else:
            print("UnKnown GoPro Version")
    await asyncio.gather(list_task)


async def batch_set_1080P(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        if camera.ver == '12':
            list_task.append(asyncio.create_task(camera.setting_12_1080P()))
        elif camera.ver == '11':
            list_task.append(asyncio.create_task(camera.setting_11_1080P()))
        else:
            print("UnKnown GoPro Version")
    await asyncio.gather(list_task)


async def batch_set_2p7K(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        if camera.ver == '12':
            list_task.append(asyncio.create_task(camera.setting_12_2p7K()))
        elif camera.ver == '11':
            list_task.append(asyncio.create_task(camera.setting_11_2p7K()))
        else:
            print("UnKnown GoPro Version")
    await asyncio.gather(list_task)


async def batch_sleep(List_Camera_Connected:List[GoPro]):
    list_task = []
    for camera in List_Camera_Connected:
        list_task.append(asyncio.create_task(camera.sleep()))
    await asyncio.gather(list_task)


async def print_activate_camera_id(List_Camera_Connected:List[GoPro]):
    list_camera_id = []
    for camera in List_Camera_Connected:
        list_camera_id.append(camera.id)
    print(list_camera_id)
    return


