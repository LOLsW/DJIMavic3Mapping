## 2023-04-05
- \[**ADDED**\] Option for waypoint filtering based on distance between **SUCCESSIVE** waypoints. It include several Earth models to calculate the most accurate distance based on geographic region
- \[**ADDED**\] When using "djiMappingConverter.py", once the processing is done, the script will wait for input before it closes (allowing you to view the output path if the script is run by double clicking)
- \[**FIXED**\] Height/Altitude mismatch is now completely fixed. (It works even when Altitude mode in QGroundControl is set to 'Calculated Above Terrain')
- \[**FIXED**\] The code now cleans the path/to/kml_file by removing quotes and the starting '&' (could cause problems on Windows)

I've also tried to clean and improve the 'Hover and take picture' part (to include a part of its workaround), but apparently now is even worse. BUT the workaround still works