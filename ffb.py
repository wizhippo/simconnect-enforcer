import struct
from enum import Enum
import hid


class PACKET_TYPE(Enum):  # FFB Packet Type
    # Write
    PT_SET_EFFECT_REPORT = 1  # Usage Set Effect Report
    PT_SET_ENVELOPE_REPORT = 2  # Usage Set Envelope Report
    PT_SET_CONDITION_REPORT = 3  # Usage Set Condition Report
    PT_SET_PERIODIC_REPORT = 4  # Usage Set Periodic Report
    PT_SET_CONSTANT_FORCE_REPORT = 5  # Usage Set Constant Force Report
    PT_SET_RAMP_FORCE_REPORT = 6  # Usage Set Ramp Force Report
    PT_CUSTOM_FORCE_DATA_REPORT = 7  # Usage Custom Force Data Report
    PT_DOWNLOAD_FORCE_SAMPLE_REPORT = 8  # Usage Download Force Sample
    PT_EFFECT_OPERATION_REPORT = 10  # Usage Effect Operation Report
    PT_PID_BLOCK_FREE_REPORT = 11  # Usage PID Block Free Report
    PT_PID_DEVICE_CONTROL_REPORT = 12  # Usage PID Device Control
    PT_DEVICE_GAIN_REPORT = 13  # Usage Device Gain Report
    PT_SET_CUSTOM_FORCE_REPORT = 14  # Usage Set Custom Force Report

    # Feature
    PT_CREATE_NEW_EFFECT_REPORT = 5  # Usage Create New Effect Report
    PT_BLOCK_LOAD_REPORT = 6  # Usage Block Load Report
    PT_PID_POOL_REPORT = 7  # Usage PID Pool Report


class EFFECT_TYPE(Enum):
    ET_NONE = 0
    ET_CONSTANT = 1
    ET_RAMP = 2
    ET_SQUARE = 3
    ET_SINE = 4
    ET_TRIANGLE = 5
    ET_SAWTOOTH_UP = 6
    ET_SAWTOOTH_DOWN = 7
    ET_SPRING = 8
    ET_DAMPER = 9
    ET_INERTIA = 10
    ET_FRICTION = 11
    ET_CUSTOM = 12


class LOAD_STATUS(Enum):
    SUCCESS = 1
    FULL = 2
    ERROR = 3


class USB_FFBReport_PIDState_Input_Data_t:
    def __init__(self, status=0, effectBlockIndex=0):
        self.reportId = 0x02
        self.status = status
        self.effectBlockIndex = effectBlockIndex

    def pack(self):
        return struct.pack('<3B', self.reportId, self.status, self.effectBlockIndex)

    @classmethod
    def unpack(cls, data):
        reportId, status, effectBlockIndex = struct.unpack('<3B', data)
        return cls(reportId, status, effectBlockIndex)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetEffect_Output_Data_t:
    def __init__(self, effectBlockIndex=0, effectType=0, duration=0, triggerRepeatInterval=0,
                 samplePeriod=0, gain=0, triggerButton=0, axisEnable=0, direction=None, startDelay=0):
        self.reportId = reportId = PACKET_TYPE.PT_SET_EFFECT_REPORT.value
        self.effectBlockIndex = effectBlockIndex
        self.effectType = effectType
        self.duration = duration
        self.triggerRepeatInterval = triggerRepeatInterval
        self.samplePeriod = samplePeriod
        self.gain = gain
        self.triggerButton = triggerButton
        self.axisEnable = axisEnable
        self.direction = direction if direction else [0, 0]
        self.startDelay = startDelay

    def pack(self):
        return struct.pack('<BBBHHHBBBBBH', self.reportId, self.effectBlockIndex, self.effectType, self.duration,
                           self.triggerRepeatInterval, self.samplePeriod, self.gain, self.triggerButton,
                           self.axisEnable, *self.direction, self.startDelay)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, effectType, duration, triggerRepeatInterval, samplePeriod, gain, triggerButton, axisEnable, direction0, direction1, startDelay = struct.unpack(
            '<BBBHHHBBBBBH', data)
        return cls(reportId, effectBlockIndex, effectType, duration, triggerRepeatInterval, samplePeriod, gain,
                   triggerButton, axisEnable, [direction0, direction1], startDelay)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetEnvelope_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, attackLevel=0, fadeLevel=0, attackTime=0, fadeTime=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.attackLevel = attackLevel
        self.fadeLevel = fadeLevel
        self.attackTime = attackTime
        self.fadeTime = fadeTime

    def pack(self):
        return struct.pack('<3B2H2H', self.reportId, self.effectBlockIndex, self.attackLevel, self.fadeLevel,
                           self.attackTime, self.fadeTime)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, attackLevel, fadeLevel, attackTime, fadeTime = struct.unpack(
            '<3B2H2H', data)
        return cls(reportId, effectBlockIndex, attackLevel, fadeLevel, attackTime, fadeTime)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetCondition_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, parameterBlockOffset=0, cpOffset=0, positiveCoefficient=0,
                 negativeCoefficient=0, positiveSaturation=0, negativeSaturation=0, deadBand=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.parameterBlockOffset = parameterBlockOffset
        self.cpOffset = cpOffset
        self.positiveCoefficient = positiveCoefficient
        self.negativeCoefficient = negativeCoefficient
        self.positiveSaturation = positiveSaturation
        self.negativeSaturation = negativeSaturation
        self.deadBand = deadBand

    def pack(self):
        return struct.pack('<3B3b2B2Bb', self.reportId, self.effectBlockIndex, self.parameterBlockOffset, self.cpOffset,
                           self.positiveCoefficient, self.negativeCoefficient, self.positiveSaturation,
                           self.negativeSaturation, self.deadBand)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, parameterBlockOffset, cpOffset, positiveCoefficient, negativeCoefficient, positiveSaturation, negativeSaturation, deadBand = struct.unpack(
            '<3B3b2B2Bb', data)
        return cls(reportId, effectBlockIndex, parameterBlockOffset, cpOffset, positiveCoefficient, negativeCoefficient,
                   positiveSaturation, negativeSaturation, deadBand)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetEnvelope_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, attackLevel=0, fadeLevel=0, attackTime=0, fadeTime=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.attackLevel = attackLevel
        self.fadeLevel = fadeLevel
        self.attackTime = attackTime
        self.fadeTime = fadeTime

    def pack(self):
        return struct.pack('<3B2H2H', self.reportId, self.effectBlockIndex, self.attackLevel, self.fadeLevel,
                           self.attackTime, self.fadeTime)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, attackLevel, fadeLevel, attackTime, fadeTime = struct.unpack(
            '<3B2H2H', data)
        return cls(reportId, effectBlockIndex, attackLevel, fadeLevel, attackTime, fadeTime)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetCondition_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, parameterBlockOffset=0, cpOffset=0, positiveCoefficient=0,
                 negativeCoefficient=0, positiveSaturation=0, negativeSaturation=0, deadBand=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.parameterBlockOffset = parameterBlockOffset
        self.cpOffset = cpOffset
        self.positiveCoefficient = positiveCoefficient
        self.negativeCoefficient = negativeCoefficient
        self.positiveSaturation = positiveSaturation
        self.negativeSaturation = negativeSaturation
        self.deadBand = deadBand

    def pack(self):
        return struct.pack('<3B3b2B2Bb', self.reportId, self.effectBlockIndex, self.parameterBlockOffset, self.cpOffset,
                           self.positiveCoefficient, self.negativeCoefficient, self.positiveSaturation,
                           self.negativeSaturation, self.deadBand)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, parameterBlockOffset, cpOffset, positiveCoefficient, negativeCoefficient, positiveSaturation, negativeSaturation, deadBand = struct.unpack(
            '<3B3b2B2Bb', data)
        return cls(reportId, effectBlockIndex, parameterBlockOffset, cpOffset, positiveCoefficient, negativeCoefficient,
                   positiveSaturation, negativeSaturation, deadBand)

    def __len__(self):
        return len(self.pack())


...


class USB_FFBReport_SetEnvelope_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, attackLevel=0, fadeLevel=0, attackTime=0, fadeTime=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.attackLevel = attackLevel
        self.fadeLevel = fadeLevel
        self.attackTime = attackTime
        self.fadeTime = fadeTime

    def pack(self):
        return struct.pack('<3B2H2H', self.reportId, self.effectBlockIndex, self.attackLevel, self.fadeLevel,
                           self.attackTime, self.fadeTime)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, attackLevel, fadeLevel, attackTime, fadeTime = struct.unpack(
            '<3B2H2H', data)
        return cls(reportId, effectBlockIndex, attackLevel, fadeLevel, attackTime, fadeTime)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetCondition_Output_Data_t:
    def __init__(self, reportId=PACKET_TYPE.PT_SET_CONDITION_REPORT.value, effectBlockIndex=0, parameterBlockOffset=0,
                 cpOffset=0, positiveCoefficient=0,
                 negativeCoefficient=0, positiveSaturation=0, negativeSaturation=0, deadBand=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.parameterBlockOffset = parameterBlockOffset
        self.cpOffset = cpOffset
        self.positiveCoefficient = positiveCoefficient
        self.negativeCoefficient = negativeCoefficient
        self.positiveSaturation = positiveSaturation
        self.negativeSaturation = negativeSaturation
        self.deadBand = deadBand

    def pack(self):
        return struct.pack('<BBBbbbBBb', self.reportId, self.effectBlockIndex, self.parameterBlockOffset, self.cpOffset,
                           self.positiveCoefficient, self.negativeCoefficient, self.positiveSaturation,
                           self.negativeSaturation, self.deadBand)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, parameterBlockOffset, cpOffset, positiveCoefficient, negativeCoefficient, positiveSaturation, negativeSaturation, deadBand = struct.unpack(
            '<BBBbbbBBb', data)
        return cls(reportId, effectBlockIndex, parameterBlockOffset, cpOffset, positiveCoefficient, negativeCoefficient,
                   positiveSaturation, negativeSaturation, deadBand)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetCustomForceData_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, dataOffset=0, data=None):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.dataOffset = dataOffset
        self.data = data if data else [0] * 255

    def pack(self):
        return struct.pack('<2BH255b', self.reportId, self.effectBlockIndex, self.dataOffset, *self.data)

    @classmethod
    def unpack(cls, data):
        unpacked = struct.unpack('<2BH255b', data)
        reportId = unpacked[0]
        effectBlockIndex = unpacked[1]
        dataOffset = unpacked[2]
        data = list(unpacked[3:])
        return cls(reportId, effectBlockIndex, dataOffset, data)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetDownloadForceSample_Output_Data_t:
    def __init__(self, reportId=0, x=0, y=0):
        self.reportId = reportId
        self.x = x
        self.y = y

    def pack(self):
        return struct.pack('<Bbb', self.reportId, self.x, self.y)

    @classmethod
    def unpack(cls, data):
        reportId, x, y = struct.unpack('<Bbb', data)
        return cls(reportId, x, y)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_EffectOperation_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, operation=0, loopCount=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.operation = operation
        self.loopCount = loopCount

    def pack(self):
        return struct.pack('<3Bb', self.reportId, self.effectBlockIndex, self.operation, self.loopCount)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, operation, loopCount = struct.unpack(
            '<3Bb', data)
        return cls(reportId, effectBlockIndex, operation, loopCount)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_BlockFree_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex

    def pack(self):
        return struct.pack('<2B', self.reportId, self.effectBlockIndex)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex = struct.unpack('<2B', data)
        return cls(reportId, effectBlockIndex)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_DeviceControl_Output_Data_t:
    def __init__(self, reportId=0, control=0):
        self.reportId = reportId
        self.control = control

    def pack(self):
        return struct.pack('<2B', self.reportId, self.control)

    @classmethod
    def unpack(cls, data):
        reportId, control = struct.unpack('<2B', data)
        return cls(reportId, control)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_DeviceGain_Output_Data_t:
    def __init__(self, reportId=0, gain=0):
        self.reportId = reportId
        self.gain = gain

    def pack(self):
        return struct.pack('<2B', self.reportId, self.gain)

    @classmethod
    def unpack(cls, data):
        reportId, gain = struct.unpack('<2B', data)
        return cls(reportId, gain)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_SetCustomForce_Output_Data_t:
    def __init__(self, reportId=0, effectBlockIndex=0, sampleCount=0, samplePeriod=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.sampleCount = sampleCount
        self.samplePeriod = samplePeriod

    def pack(self):
        return struct.pack('<3BH', self.reportId, self.effectBlockIndex, self.sampleCount, self.samplePeriod)

    @classmethod
    def unpack(cls, data):
        reportId, effectBlockIndex, sampleCount, samplePeriod = struct.unpack(
            '<3BH', data)
        return cls(reportId, effectBlockIndex, sampleCount, samplePeriod)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_CreateNewEffect_Feature_Data_t:
    def __init__(self, reportId=PACKET_TYPE.PT_CREATE_NEW_EFFECT_REPORT.value, effectType=0, byteCount=0):
        self.reportId = reportId
        self.effectType = effectType
        self.byteCount = byteCount

    def pack(self):
        return struct.pack('<2BH', self.reportId, self.effectType, self.byteCount)

    @classmethod
    def unpack(cls, data):
        reportId, effectType, byteCount = struct.unpack('<2BH', data)
        return cls(reportId, effectType, byteCount)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_PIDPool_Feature_Data_t:
    def __init__(self, reportId=PACKET_TYPE.PT_PID_POOL_REPORT, ramPoolSize=0, maxSimultaneousEffects=0,
                 memoryManagement=0):
        self.reportId = reportId
        self.ramPoolSize = ramPoolSize
        self.maxSimultaneousEffects = maxSimultaneousEffects
        self.memoryManagement = memoryManagement

    def pack(self):
        return struct.pack('<BH2B', self.reportId, self.ramPoolSize, self.maxSimultaneousEffects, self.memoryManagement)

    @classmethod
    def unpack(cls, data):
        unpacked = struct.unpack('<BH2B', data)
        return cls(*unpacked)

    def __len__(self):
        return len(self.pack())


class USB_FFBReport_PIDBlockLoad_Feature_Data_t:
    def __init__(self, reportId=PACKET_TYPE.PT_BLOCK_LOAD_REPORT.value, effectBlockIndex=0, loadStatus=0,
                 ramPoolAvailable=0):
        self.reportId = reportId
        self.effectBlockIndex = effectBlockIndex
        self.loadStatus = loadStatus
        self.ramPoolAvailable = ramPoolAvailable

    def pack(self):
        return struct.pack('<3BH', self.reportId, self.effectBlockIndex, self.loadStatus, self.ramPoolAvailable)

    @classmethod
    def unpack(cls, data):
        unpacked = struct.unpack('<3BH', data)
        return cls(*unpacked)

    def __len__(self):
        return len(self.pack())


def GetState(device):
    report = USB_FFBReport_PIDState_Input_Data_t()
    res = device.get_input_report(0x02, len(report))
    report = report.unpack(bytearray(res))
    # report.status # bits 7=Device Paused, 6=Actuators Enabled, 5=Safety Switch, 4=Actuator Override Switch, 3=Actuator Power
    return report


def SpringEffet(device):
    report = USB_FFBReport_PIDState_Input_Data_t()
    res = device.get_input_report(0x02, len(report))
    report = report.unpack(bytearray(res))
    # report.status # bits 7=Device Paused, 6=Actuators Enabled, 5=Safety Switch, 4=Actuator Override Switch, 3=Actuator Power

    report = USB_FFBReport_CreateNewEffect_Feature_Data_t()
    report.effectType = EFFECT_TYPE.ET_SPRING.value
    # the bytes count is not used see spec
    res = device.send_feature_report(
        bytearray([report.reportId, report.effectType]))
    if res > 1:
        report = USB_FFBReport_PIDBlockLoad_Feature_Data_t()
        res = device.get_feature_report(report.reportId, len(report))
        report = report.unpack(bytearray(res))

        if report.loadStatus == LOAD_STATUS.SUCCESS.value:
            effectBlockIndex = report.effectBlockIndex

            report = USB_FFBReport_SetEffect_Output_Data_t()
            report.effectBlockIndex = effectBlockIndex
            report.effectType = EFFECT_TYPE.ET_SPRING.value
            report.duration = 0xffff  # infinite
            report.triggerRepeatInterval = 0
            report.samplePeriod = 1
            report.gain = 255
            report.triggerButton = 255
            report.axisEnable = 0x02  # bits: 0=X, 1=Y, 2=DirectionEnable
            report.direction = [0, 0]  # north
            report.startDelay = 0

            res = device.write(report.pack())

            report = USB_FFBReport_SetCondition_Output_Data_t()
            report.effectBlockIndex = effectBlockIndex
            report.parameterBlockOffset = 0
            report.cpOffset = 0
            report.positiveCoefficient = 127
            report.negativeCoefficient = 127
            report.positiveSaturation = 255
            report.negativeSaturation = 255
            report.deadBand = 0

            res = device.write(report.pack())

            report.parameterBlockOffset = 1

            res = device.write(report.pack())


def ConstantForceEffect(device):
    report = USB_FFBReport_CreateNewEffect_Feature_Data_t()
    report.effectType = EFFECT_TYPE.ET_CONSTANT.value
    # the bytes count is not used see spec
    res = device.send_feature_report(
        bytearray([report.reportId, report.effectType]))
    if res > 1:
        report = USB_FFBReport_PIDBlockLoad_Feature_Data_t()
        res = device.get_feature_report(report.reportId, len(report))
        report = report.unpack(bytearray(res))

        if report.loadStatus == LOAD_STATUS.SUCCESS.value:
            effectBlockIndex = report.effectBlockIndex

            report = USB_FFBReport_SetEffect_Output_Data_t()
            report.effectBlockIndex = effectBlockIndex
            report.effectType = EFFECT_TYPE.ET_CONSTANT.value
            report.duration = 0xffff  # infinite
            report.triggerRepeatInterval = 0
            report.samplePeriod = 1
            report.gain = 255
            report.triggerButton = 255
            report.axisEnable = 0x02  # bits: 0=X, 1=Y, 2=DirectionEnable
            report.direction = [0, 0]  # north
            report.startDelay = 0

            res = device.write(report.pack())

            report = USB_FFBReport_SetCondition_Output_Data_t()
            report.effectBlockIndex = effectBlockIndex
            report.parameterBlockOffset = 0
            report.cpOffset = 0
            report.positiveCoefficient = 0
            report.negativeCoefficient = 0
            report.positiveSaturation = 255
            report.negativeSaturation = 255
            report.deadBand = 0

            res = device.write(report.pack())

            report.parameterBlockOffset = 1

            res = device.write(report.pack())
