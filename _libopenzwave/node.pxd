# -*- coding: utf-8 -*-
"""
This file is part of **libopenzwave** project

License : GPL(v3)

**libopenzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**libopenzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""
from libcpp cimport bool
from libcpp.list cimport list
from libc.stdint cimport uint32_t, uint8_t, uint16_t
from mylibc cimport string

cdef extern from "Node.h" namespace "OpenZWave::Node":

    cdef enum MetaDataFields:
        MetaData_OzwInfoPage_URL = 0
        MetaData_ZWProductPage_URL = 1
        MetaData_ProductPic = 2
        MetaData_Description = 3
        MetaData_ProductManual_URL = 4
        MetaData_ProductPage_URL = 5
        MetaData_InclusionHelp = 6
        MetaData_ExclusionHelp = 7
        MetaData_ResetHelp = 8
        MetaData_WakeupHelp = 9
        MetaData_ProductSupport_URL = 10
        MetaData_Frequency = 11
        MetaData_Name = 12
        MetaData_Identifier = 13
        MetaData_Invalid= 255

    cdef struct ChangeLogEntry:
        string  author
        string  date
        int revision
        string description

    cdef enum SecurityFlag:
        SecurityFlag_Security = 0x01
        SecurityFlag_Controller = 0x02
        SecurityFlag_SpecificDevice = 0x04
        SecurityFlag_RoutingSlave = 0x08
        SecurityFlag_BeamCapability = 0x10
        SecurityFlag_Sensor250ms = 0x20
        SecurityFlag_Sensor1000ms = 0x40
        SecurityFlag_OptionalFunctionality = 0x80

    cdef struct CommandClassData:
        # Num type of CommandClass id.
        uint8_t m_commandClassId
        # Number of messages sent from this CommandClass.
        uint32_t m_sentCnt
        # Number of messages received from this CommandClass.
        uint32_t m_receivedCnt

    cdef struct NodeData:
        # Number of messages sent from this node.
        uint32_t m_sentCnt
        # Number of sent messages failed
        uint32_t m_sentFailed
        # Number of message retries
        uint32_t m_retries
        # Number of messages received from this node.
        uint32_t m_receivedCnt
        # Number of duplicated messages received;
        uint32_t m_receivedDups
        # Number of messages received unsolicited
        uint32_t m_receivedUnsolicited
        # Last message request RTT
        uint32_t m_lastRequestRTT
        # Last message response RTT
        uint32_t m_lastResponseRTT
        # Last message sent time
        string m_sentTS
        # Last message received time
        string m_receivedTS
        # Average Request round trip time.
        uint32_t m_averageRequestRTT
        # Average Response round trip time.
        uint32_t m_averageResponseRTT
        # Node quality measure
        uint8_t m_quality
        # Place to hold last received message
        uint8_t m_lastReceivedMessage[254]
        list[CommandClassData] m_ccData
        # if Extended Status Reports are available
        bool m_txStatusReportSupported
        # Time Taken to Transmit the last frame
        uint16_t m_txTime
        # Hops taken in transmitting last frame
        uint8_t m_hops
        # RSSI Level of last transmission
        char m_rssi_1[8]
        # RSSI Level of last transmission
        char m_rssi_2[8]
        # RSSI Level of last transmission
        char m_rssi_3[8]
        # RSSI Level of last transmission
        char m_rssi_4[8]
        # RSSI Level of last transmission
        char m_rssi_5[8]
        # Channel we received the last ACK on
        uint8_t m_ackChannel
        # Channel we transmitted the last frame on
        uint8_t m_lastTxChannel
        # The Scheme used to route the last frame
        uint8_t m_routeScheme
        # The Route Taken in the last frame
        uint8_t m_routeUsed[4]
        # Baud Rate of the last frame
        uint8_t m_routeSpeed
        # The number of attempts to route the last frame
        uint8_t m_routeTries
        # The last failed link from
        uint8_t m_lastFailedLinkFrom
        # The last failed link to
        uint8_t m_lastFailedLinkTo


ctypedef NodeData NodeData_t

