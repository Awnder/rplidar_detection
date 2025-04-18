from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

try:
    info = lidar.get_info()
    print(info)

    health = lidar.get_health()
    print(health)

    
except Exception:
    print('exception')
    lidar.clear_input()

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()