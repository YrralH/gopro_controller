
import sys
import asyncio
from typing import Optional
import keyboard
import sys
import asyncio
from typing import Optional
import keyboard

from bleak import BleakClient

from lib_go_pro.connect import connect_ble
from lib_go_pro.logger import GOPRO_BASE_UUID, logger

from lib_go_pro.go_pro_ble import GoPro, try_connect_camera_once
from lib_go_pro.batch_options import batch_start_record, batch_stop_record, print_activate_camera_id, batch_set_60FPS, \
    batch_set_120FPS, batch_set_240FPS, batch_set_1080P, batch_set_2p7K, batch_set_4K, batch_sleep

from typing import List, Dict, Tuple

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


async def multi_controller(List_Camera_ID: List[int] = LIST_CAMERA_ID_AND_VERSION_9):
    """
    连接多个相机
    """
    print('List_Camera_ID', List_Camera_ID)

    logger.info("Press 'A' to start record")
    logger.info("Press 'S' to stop record")
    logger.info("Press 'Q' to set 60FPS")
    logger.info("Press 'W' to set 120FPS")
    logger.info("Press 'E' to set 240FPS")
    logger.info("Press 'R' to set 1080P")
    logger.info("Press 'T' to set 2.7K")
    logger.info("Press 'Y' to set 4K")
    logger.info("Press 'F' to sleep")

    List_Camera_Connected:List[GoPro] = []

    loop = asyncio.get_running_loop()  # 获取当前正在运行的事件循环

    #connect
    #for i in range(len(List_Camera_ID)):
    #    keyboard.add_hotkey(str(i), lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[i], List_Camera_Connected), loop))

    keyboard.add_hotkey('0', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[0], List_Camera_Connected), loop))
    keyboard.add_hotkey('1', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[1], List_Camera_Connected), loop))
    keyboard.add_hotkey('2', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[2], List_Camera_Connected), loop))
    keyboard.add_hotkey('3', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[3], List_Camera_Connected), loop))
    keyboard.add_hotkey('4', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[4], List_Camera_Connected), loop))
    keyboard.add_hotkey('5', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[5], List_Camera_Connected), loop))
    keyboard.add_hotkey('6', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[6], List_Camera_Connected), loop))
    keyboard.add_hotkey('7', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[7], List_Camera_Connected), loop))
    keyboard.add_hotkey('8', lambda: asyncio.run_coroutine_threadsafe(try_connect_camera_once(List_Camera_ID[8], List_Camera_Connected), loop))

    #options
    keyboard.add_hotkey('a', lambda: asyncio.run_coroutine_threadsafe(batch_start_record(List_Camera_Connected), loop))
    keyboard.add_hotkey('s', lambda: asyncio.run_coroutine_threadsafe(batch_stop_record(List_Camera_Connected), loop))
    keyboard.add_hotkey('f', lambda: asyncio.run_coroutine_threadsafe(batch_sleep(List_Camera_Connected), loop))

    keyboard.add_hotkey('q', lambda: asyncio.run_coroutine_threadsafe(batch_set_60FPS(List_Camera_Connected), loop))
    keyboard.add_hotkey('w', lambda: asyncio.run_coroutine_threadsafe(batch_set_120FPS(List_Camera_Connected), loop))
    keyboard.add_hotkey('e', lambda: asyncio.run_coroutine_threadsafe(batch_set_240FPS(List_Camera_Connected), loop))

    keyboard.add_hotkey('r', lambda: asyncio.run_coroutine_threadsafe(batch_set_1080P(List_Camera_Connected), loop))
    keyboard.add_hotkey('t', lambda: asyncio.run_coroutine_threadsafe(batch_set_2p7K(List_Camera_Connected), loop))
    keyboard.add_hotkey('y', lambda: asyncio.run_coroutine_threadsafe(batch_set_4K(List_Camera_Connected), loop))


    # 保持连接的循环
    while True:
        await print_activate_camera_id(List_Camera_Connected)
        await asyncio.sleep(5)  # 每秒钟检查一次