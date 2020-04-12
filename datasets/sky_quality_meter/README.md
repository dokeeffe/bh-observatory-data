# SQM data

There are 2 directories containing data here from 2 different SQM devices.

## SQM_DL

The data in this directory is from an SQM datalogger which was borrowed from Cork Astronomy Club in 2019. 
The data logger was taking measurmentents every 5minutes at night in all conditions (clear, cloud, rain).
The format of this data is the standard unihedron format from the device.

## SQM_LU

The data in this directory is from a USB SQM permanently installed **inside** the observatory and only records when the observatory is open and the telescope is capturing images. This data is extracted from the FITS headers of images captured while the telscope is working.

The format of this data is a CSV file containing UTC timestamps and SQM readings
