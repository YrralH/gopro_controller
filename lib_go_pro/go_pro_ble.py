
import sys
import asyncio
from typing import Optional
import keyboard

from bleak import BleakClient

from lib_go_pro.connect import connect_ble
from lib_go_pro.logger import GOPRO_BASE_UUID, logger

from typing import List, Dict, Tuple




class GoPro():
    def __init__(self, GoProID: str, GoProVersion: str):
        self.event = asyncio.Event()
        self.COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
        self.COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
        self.SETTING_REQ_UUID = GOPRO_BASE_UUID.format("0074")
        self.SETTING_RSP_UUID = GOPRO_BASE_UUID.format("0075")
        self.command_response_uuid = self.COMMAND_RSP_UUID
        self.setting_response_uuid = self.SETTING_RSP_UUID
        self.Connected = False
        self.Recording = False
        self.id = GoProID
        self.ver = GoProVersion
        self.client = None

    async def connect(self, identifier: Optional[str]):
        """
        连接GoPro相机
        :param identifier: 相机编号后四位
        :return: 对应相机连接
        """

        client: BleakClient

        def notification_handler(handle: int, data: bytes) -> None:
            logger.info(f'Received response at {handle}: {data.hex(":")}')

            # If this is the correct handle and the status is success, the command was a success
            if client.services.characteristics[handle].uuid == self.command_response_uuid\
                    or client.services.characteristics[handle].uuid == self.setting_response_uuid and data[2] == 0x00:
                logger.info("Command sent successfully")
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")

            # Notify the writer
            self.event.set()

        client = await connect_ble(notification_handler, identifier)
        self.Connected = True
        if client is not None:
            self.client = client
            return True
        else:
            return False

    async def start_record(self):
        """
        开始录制
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the shutter on")
            self.event.clear()
            await self.client.write_gatt_char(self.COMMAND_REQ_UUID, bytearray([0x03, 0x01, 0x01, 0x01]), response=True)  # start
            await self.event.wait()  # Wait to receive the notification response
            self.Recording = True
        else:
            logger.info("Camera is now recording")

    async def stop_record(self):
        """
        停止录制
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        logger.info("Setting the shutter off")
        self.event.clear()
        await self.client.write_gatt_char(self.COMMAND_REQ_UUID, bytearray([0x03, 0x01, 0x01, 0x00]), response=True)  # stop
        await self.event.wait()  # Wait to receive the notification response
        self.Recording = False

    async def setting_60FPS(self):
        """
        设置相机参数为60FPS
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution to 60FPS")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x03, 0x01, 0x05]),
                                              response=True)  # fps 60
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_120FPS(self):
        """
        设置相机参数为120FPS
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution to 120FPS")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x03, 0x01, 0x01]),
                                              response=True)  # fps 120
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_240FPS(self):
        """
        设置相机参数为240FPS
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution to 240FPS")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x03, 0x01, 0x00]),
                                              response=True)  # fps 240
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_12_4K(self):
        """
        设置GoPro12相机参数为4K
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution of GoPro12 to 4K")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x02, 0x01, 0x66]),
                                              response=True)  # 4k 16:9
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_11_4K(self):
        """
        设置GoPro11相机参数为4K
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution of GoPro11 to 4K")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x02, 0x01, 0x01]),
                                              response=True)  # 4k
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_12_1080P(self):
        """
        设置GoPro12相机参数为1080P
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution of GoPro12 to 1080P")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x02, 0x01, 0x6A]),
                                              response=True)  # 1080P 16:9
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_11_1080P(self):
        """
        设置GoPro11相机参数为1080P
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution of GoPro11 to 1080P")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x02, 0x01, 0x09]),
                                              response=True)  # 1080P
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_12_2p7K(self):
        """
        设置GoPro12相机参数为2.7K
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution of GoPro12 to 2.7K")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x02, 0x01, 0x68]),
                                              response=True)  # 2.7K 16:9
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def setting_11_2p7K(self):
        """
        设置GoPro11相机参数为2.7K
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Setting the video resolution of GoPro11 to 2.7K")
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x02, 0x01, 0x04]),
                                              response=True)  # 2.7K
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x79, 0x01, 0x04]),
                                              response=True)  # linear
            await self.event.wait()  # Wait to receive the notification response
        else:
            logger.info("Camera is now recording")

    async def sleep(self):
        """
        相机睡眠
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        if not self.Recording:
            logger.info("Sleeping")
            self.event.clear()
            await self.client.write_gatt_char(self.COMMAND_REQ_UUID, bytearray([0x01, 0x05]), response=True)  # sleep
            await self.event.wait()  # Wait to receive the notification response
            self.Connected = False
            await self.client.disconnect()
            sys.exit(0)
        else:
            logger.info("Camera is now recording")

    async def keep_alive(self):
        """
        发送保持活跃的命令
        :param client: 相机连接
        """
        assert self.client is not None, 'connect first.'
        while True:
            self.event.clear()
            await self.client.write_gatt_char(self.SETTING_REQ_UUID, bytearray([0x03, 0x5b, 0x01, 0x42]), response=True)
            await self.event.wait()
            await asyncio.sleep(3)


async def try_connect_camera_once(id:str, List_Camera_Connected:List[GoPro]):
    SN = id[:4]
    VERSION = id[5:]
    camera = GoPro(SN, VERSION)
    print('try_connect_camera_once:', 'trying')
    print(SN, VERSION)
    flag_ret = await camera.connect(camera.id)
    if flag_ret:
        print('try_connect_camera_once:', 'connected')
        List_Camera_Connected.append(camera)
    return