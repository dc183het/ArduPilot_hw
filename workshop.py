
import time
from future.utils import encode_filename
from dronekit import connect, VehicleMode,LocationGlobalRelative 

aLocation = LocationGlobalRelative(35.79196857,139.09689,0)
vehicle  = connect('127.0.0.1:14551', wait_ready=True, timeout=60)


while not vehicle.is_armable:
    print("初期化中です")
    time.sleep(1)

#while not vehicle1.is_armable:

while not vehicle.home_location:
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    if not vehicle.home_location:
        print("ホームロケーションを待っています…")



# ホームロケーションの取得完了
print("ホームロケーション: %s" % vehicle.home_location)


print("アームします")
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

while not vehicle.armed:
    print("アームを待ってます")
    time.sleep(1)

targetAltude = 100


print("離陸！")
vehicle.simple_takeoff(targetAltude)

while True:
    print("高度:",vehicle.location.global_relative_frame.alt)

    if vehicle.location.global_relative_frame.alt >= targetAltude * 0.95:
        print("目標高度に到達しました")
        break

    time.sleep(1)

time.sleep(1) 


vehicle.mode = VehicleMode("AUTO")
print("ミッション飛行開始")

while True:
    print("高度:",vehicle.location.global_relative_frame.alt)
    time.sleep(3)
    msg_distance = vehicle.message_factory.distance_sensor_encode(
    0,0,1000,120,5,1,2,0)

    print(msg_distance)
    vehicle.send_mavlink(msg_distance)
    time.sleep(0.2)

    for x in range(0, 100):
        vehicle.send_mavlink(msg_distance)

    if vehicle.location.global_relative_frame.alt >= 400*0.99:
        print("現場に到着しました")
        vehicle.mode = VehicleMode("CIRCLE")
        print("周囲を撮影します")
        time.sleep(60)
        break

       
vehicle.mode = VehicleMode("RTL")
print("帰還します")    

while True:
    print("高度:",vehicle.location.global_relative_frame.alt)
    time.sleep(3)
    msg_distance = vehicle.message_factory.distance_sensor_encode(
    0,0,1000,120,5,1,2,0)

    print(msg_distance)
    vehicle.send_mavlink(msg_distance)
    time.sleep(0.2)

    for x in range(0, 100):
        vehicle.send_mavlink(msg_distance)

    if vehicle.location.global_relative_frame.alt <= 0.01: 
     print("着陸しました")
     break 