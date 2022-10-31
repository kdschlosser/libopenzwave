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
from libcpp.vector cimport vector
from libc.stdint cimport uint32_t, int32_t, uint16_t, int16_t, uint8_t, int8_t
from mylibc cimport string
from node cimport NodeData, ChangeLogEntry, MetaDataFields
from driver cimport DriverData
from group cimport InstanceAssociation_t, InstanceAssociation
from driver cimport ControllerInterface
from notification cimport pfnOnNotification_t
from values cimport ValueID
from options cimport Options

ctypedef uint8_t** int_associations
ctypedef InstanceAssociation_t** struct_associations

cdef extern from "Manager.h" namespace "OpenZWave":

    # noinspection PyClassicStyleClass,PyMissingOrEmptyDocstring,PyPep8Naming
    cdef cppclass Manager:
        # // Destructor
        void Destroy() except +

        # // Configuration
        void WriteConfig(uint32_t homeid) except +
        Options* GetOptions() except +

        # // Drivers
        bool AddDriver(string serialport) except +
        bool RemoveDriver(string controllerPath) except +
        uint8_t GetControllerNodeId(uint32_t homeid) except +
        uint8_t GetSUCNodeId(uint32_t homeid) except +
        bool IsPrimaryController(uint32_t homeid) except +
        bool IsStaticUpdateController(uint32_t homeid) except +
        bool IsBridgeController(uint32_t homeid) except +
        string getVersionAsString() except +
        string getVersionLongAsString() except +
        string GetLibraryVersion(uint32_t homeid) except +
        string GetLibraryTypeName(uint32_t homeid) except +
        int32_t GetSendQueueCount(uint32_t homeId ) except +
        void LogDriverStatistics(uint32_t homeId ) except +
        void GetDriverStatistics(uint32_t homeId, DriverData* data) except +
        void GetNodeStatistics(uint32_t homeId, uint8_t nodeid, NodeData* data) except +
        ControllerInterface GetControllerInterfaceType(uint32_t homeId) except +
        string GetControllerPath(uint32_t homeId) except +

        # // Network
        void TestNetworkNode(uint32_t homeId, uint8_t nodeId, uint32_t count) except +
        void TestNetwork(uint32_t homeId, uint32_t count) except +
        void HealNetworkNode(uint32_t homeId, uint32_t nodeId, bool _doRR) except +
        void HealNetwork(uint32_t homeId, bool doRR) except +

        # // Polling
        uint32_t GetPollInterval() except +
        void SetPollInterval(uint32_t milliseconds, bIntervalBetweenPolls) except +
        bool EnablePoll(ValueID& valueId, uint8_t intensity) except +
        bool DisablePoll(ValueID& valueId) except +
        bool isPolled(ValueID& valueId) except +
        void SetPollIntensity(ValueID& valueId, uint8_t intensity) except +
        uint8_t GetPollIntensity(ValueID& valueId) except +

        # // Node Information
        bool RefreshNodeInfo(uint32_t homeid, uint8_t nodeid) except +
        bool RequestNodeState(uint32_t homeid, uint8_t nodeid) except +
        bool RequestNodeDynamic( uint32_t homeId, uint8_t nodeId ) except +
        bool IsNodeListeningDevice(uint32_t homeid, uint8_t nodeid) except +
        bool IsNodeFrequentListeningDevice(uint32_t homeId, uint8_t nodeId) except +
        bool IsNodeBeamingDevice(uint32_t homeId, uint8_t nodeId) except +
        bool IsNodeRoutingDevice(uint32_t homeid, uint8_t nodeid) except +
        bool IsNodeSecurityDevice(uint32_t homeId, uint8_t nodeId) except +
        bool IsNodeZWavePlus(uint32_t homeId, uint8_t nodeId) except +
        uint32_t GetNodeMaxBaudRate(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeVersion(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeSecurity(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeBasic(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeGeneric(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeSpecific(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeType(uint32_t homeid, uint8_t nodeid) except +
        uint16_t GetNodeDeviceType(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeDeviceTypeString(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeRole(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeRoleString(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodePlusType(uint32_t homeid, uint8_t nodeid) except +
        string GetNodePlusTypeString(uint32_t homeid, uint8_t nodeid) except +
        uint32_t GetNodeNeighbors(uint32_t homeid, uint8_t nodeid, uint8_t** nodeNeighbors) except +
        string GetNodeManufacturerName(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeProductName(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeName(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeLocation(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeManufacturerId(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeProductType(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeProductId(uint32_t homeid, uint8_t nodeid) except +
        void SetNodeManufacturerName(uint32_t homeid, uint8_t nodeid, string manufacturerName) except +
        void SetNodeProductName(uint32_t homeid, uint8_t nodeid, string productName) except +
        void SetNodeName(uint32_t homeid, uint8_t nodeid, string productName) except +
        void SetNodeLocation(uint32_t homeid, uint8_t nodeid, string location) except +
        void SetNodeOn(uint32_t homeid, uint8_t nodeid) except +
        void SetNodeOff(uint32_t homeid, uint8_t nodeid) except +
        void SetNodeLevel(uint32_t homeid, uint8_t nodeid, uint8_t level) except +
        bool IsNodeInfoReceived(uint32_t homeid, uint8_t nodeid) except +
        bool IsNodePlusInfoReceived(uint32_t homeid, uint8_t nodeid) except +
        bool GetNodeClassInformation(uint32_t homeId, uint8_t nodeId, uint8_t commandClassId, string *className, uint8_t *classVersion) except +
        bool IsNodeAwake(uint32_t homeid, uint8_t nodeid) except +
        bool IsNodeFailed(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeQueryStage(uint32_t homeid, uint8_t nodeid) except +
        uint8_t GetNodeIcon(uint32_t homeid, uint8_t nodeid) except +
        string GetNodeIconName(uint32_t homeid, uint8_t nodeid) except +

        # // Values
        string GetValueLabel(ValueID& valueid) except +
        void SetValueLabel(ValueID& valueid, string value) except +
        string GetValueUnits(ValueID& valueid) except +
        void SetValueUnits(ValueID& valueid, string value) except +
        string GetValueHelp(ValueID& valueid) except +
        void SetValueHelp(ValueID& valueid, string value) except +
        int32_t GetValueMin(ValueID& valueid) except +
        int32_t GetValueMax(ValueID& valueid) except +
        bool IsValueReadOnly(ValueID& valueid) except +
        bool IsValueWriteOnly(ValueID& valueid) except +
        bool IsValueSet(ValueID& valueid) except +
        bool IsValuePolled( ValueID& valueid ) except +
        bool GetValueAsBool(ValueID& valueid, bool* o_value) except +
        bool GetValueAsByte(ValueID& valueid, uint8_t* o_value) except +
        bool GetValueAsFloat(ValueID& valueid, float* o_value) except +
        bool GetValueAsInt(ValueID& valueid, int32_t* o_value) except +
        bool GetValueAsShort(ValueID& valueid, int16_t* o_value) except +
        bool GetValueAsBitSet(ValueID& valueid, uint8_t _pos, bool* o_value) except +
        bool GetValueAsRaw(ValueID& valueid, uint8_t** o_value, uint8_t* o_length) except +
        bool GetValueAsString(ValueID& valueid, string* o_value) except +
        bool GetValueListSelection(ValueID& valueid, string* o_value) except +
        bool GetValueListSelection(ValueID& valueid, int32_t* o_value) except +
        bool GetValueListItems(ValueID& valueid, vector[string]* o_value) except +
        bool GetValueListValues(ValueID& valueid, vector[int32_t]* o_value) except +
        bool SetValue(ValueID& valueid, bool value) except +
        bool SetValue(ValueID& valueid, uint8_t value) except +
        bool SetValue(ValueID& valueid, float value) except +
        bool SetValue(ValueID& valueid, int32_t value) except +
        bool SetValue(ValueID& valueid, int16_t value) except +
        bool SetValue(ValueID& valueid, uint8_t* value, uint8_t length) except +
        bool SetValue(ValueID& valueid, string value) except +
        bool SetValue(ValueID& valueid, uint8_t pos, bool value) except +
        bool SetValueListSelection(ValueID& valueid, string selecteditem) except +
        bool RefreshValue(ValueID& valueid) except +
        void SetChangeVerified(ValueID& valueid, bool verify) except +
        bool GetChangeVerified(ValueID& valueid) except +
        bool PressButton(ValueID& valueid) except +
        bool ReleaseButton(ValueID& valueid) except +
        bool GetValueFloatPrecision(ValueID& valueid, uint8_t* o_value) except +

        # // Climate Control
        uint8_t GetNumSwitchPoints(ValueID& valueid)
        bool SetSwitchPoint(ValueID& valueid, uint8_t hours, uint8_t minutes, uint8_t setback) except +
        bool RemoveSwitchPoint(ValueID& valueid, uint8_t hours, uint8_t minutes) except +
        bool ClearSwitchPoints(ValueID& valueid) except +
        bool GetSwitchPoint(ValueID& valueid, uint8_t idx, uint8_t* o_hours, uint8_t* o_minutes, int8_t* o_setback) except +

        # // SwitchAll
        void SwitchAllOn(uint32_t homeid) except +
        void SwitchAllOff(uint32_t homeid) except +

        # // Configuration Parameters
        bool SetConfigParam(uint32_t homeid, uint8_t nodeid, uint8_t param, uint32_t value, uint8_t size) except +
        void RequestConfigParam(uint32_t homeid, uint8_t nodeid, uint8_t aram) except +
        void RequestAllConfigParams(uint32_t homeid, uint8_t nodeid) except +
        # // Groups
        uint8_t GetNumGroups(uint32_t homeid, uint8_t nodeid) except +
        uint32_t GetAssociations(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, struct_associations o_associations) except +
        uint8_t GetMaxAssociations( uint32_t homeid, uint8_t nodeid, uint8_t groupidx) except +
        string GetGroupLabel(uint32_t homeid, uint8_t nodeid, uint8_t groupidx) except +
        bool IsMultiInstance(uint32_t homeid, uint8_t nodeid, uint8_t groupIdx) except +
        void AddAssociation(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, uint8_t targetnodeid, uint8_t instance) except +
        void RemoveAssociation(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, uint8_t targetnodeid, uint8_t instance) except +
        bool AddWatcher(pfnOnNotification_t notification, void* context) except +
        bool RemoveWatcher(pfnOnNotification_t notification, void* context) except +
        # void NotifyWatchers(Notification*)

        # // Controller Commands
        void ResetController(uint32_t homeid) except +
        void SoftReset(uint32_t homeid) except +

        bool CancelControllerCommand(uint32_t homeid) except +
        bool AddNode(uint32_t homeid, bool _doSecurity) except +
        bool RemoveNode(uint32_t homeid) except +
        bool RemoveFailedNode(uint32_t homeid, uint8_t nodeid) except +
        bool HasNodeFailed(uint32_t homeid, uint8_t nodeid) except +
        bool ReplaceFailedNode(uint32_t homeid, uint8_t nodeid) except +
        bool AssignReturnRoute(uint32_t homeid, uint8_t nodeid) except +
        bool RequestNodeNeighborUpdate(uint32_t homeid, uint8_t nodeid) except +
        bool RequestNetworkUpdate(uint32_t homeid, uint8_t nodeid) except +
        bool ReplicationSend(uint32_t homeid, uint8_t nodeid) except +
        bool DeleteAllReturnRoutes(uint32_t homeid, uint8_t nodeid) except +
        bool SendNodeInformation(uint32_t homeid, uint8_t nodeid) except +
        bool CreateNewPrimary(uint32_t homeid) except +
        bool TransferPrimaryRole(uint32_t homeid) except +
        bool ReceiveConfiguration(uint32_t homeid) except +
        bool CreateButton(uint32_t homeid, uint8_t nodeid, uint8_t buttonid) except +
        bool DeleteButton(uint32_t homeid, uint8_t nodeid, uint8_t buttonid) except +

        # Config file revision checks and downloads
        bool checkLatestConfigFileRevision(uint32_t _homeId, uint8_t _nodeId) except +
        bool checkLatestMFSRevision(uint32_t _homeId) except +
        bool downloadLatestConfigFileRevision(uint32_t _homeId, uint8_t _nodeId) except +
        bool downloadLatestMFSRevision(uint32_t _homeId) except +

        # node metadata
        ChangeLogEntry GetChangeLog(uint32_t _homeId, uint8_t _nodeId, uint32_t revision) except +
        string GetMetaData(uint32_t _homeId, uint8_t _nodeId, MetaDataFields _metadata) except +

        # value instance labels
        string GetInstanceLabel(ValueID& _id) except +
        string GetInstanceLabel(uint32_t _homeId, uint8_t _node, uint8_t _cc, uint8_t _instance) except +

        # raw data
        void SendRawData(uint32_t _homeId, uint8_t _nodeId, string& _logText, uint8_t _msgType, bool _sendSecure, uint8_t* _content, uint8_t _length) except +


cdef extern from "Manager.h" namespace "OpenZWave::Manager":
    # noinspection PyMissingOrEmptyDocstring,PyPep8Naming
    Manager* Create() except +
    # noinspection PyMissingOrEmptyDocstring,PyPep8Naming
    Manager* Get() except +
