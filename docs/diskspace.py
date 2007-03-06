import win32com.client
strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("Select * from Win32_DiskPartition")
for objItem in colItems:
    print "Access: ", objItem.Access
    print "Availability: ", objItem.Availability
    print "Block Size: ", objItem.BlockSize
    print "Bootable: ", objItem.Bootable
    print "Boot Partition: ", objItem.BootPartition
    print "Caption: ", objItem.Caption
    print "Config Manager Error Code: ", objItem.ConfigManagerErrorCode
    print "Config Manager User Config: ", objItem.ConfigManagerUserConfig
    print "Creation Class Name: ", objItem.CreationClassName
    print "Description: ", objItem.Description
    print "Device ID: ", objItem.DeviceID
    print "Disk Index: ", objItem.DiskIndex
    print "Error Cleared: ", objItem.ErrorCleared
    print "Error Description: ", objItem.ErrorDescription
    print "Error Methodology: ", objItem.ErrorMethodology
    print "Hidden Sectors: ", objItem.HiddenSectors
    print "Index: ", objItem.Index
    print "Install Date: ", objItem.InstallDate
    print "Last Error Code: ", objItem.LastErrorCode
    print "Name: ", objItem.Name
    print "Number Of Blocks: ", objItem.NumberOfBlocks
    print "PNP Device ID: ", objItem.PNPDeviceID
    z = objItem.PowerManagementCapabilities
    if z is None:
        a = 1
    else:
        for x in z:
            print "Power Management Capabilities: ", x
    print "Power Management Supported: ", objItem.PowerManagementSupported
    print "Primary Partition: ", objItem.PrimaryPartition
    print "Purpose: ", objItem.Purpose
    print "Rewrite Partition: ", objItem.RewritePartition
    print "Size: ", objItem.Size
    print "Starting Offset: ", objItem.StartingOffset
    print "Status: ", objItem.Status
    print "Status Info: ", objItem.StatusInfo
    print "System Creation Class Name: ", objItem.SystemCreationClassName
    print "System Name: ", objItem.SystemName
    print "Type: ", objItem.Type