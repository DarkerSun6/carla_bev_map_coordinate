import carla
import random
import numpy as np
import os

# 连接到Carla服务器
client = carla.Client('127.0.0.1', 2000)
client.set_timeout(20.0)
world = client.get_world()
world = client.load_world('Town03_Opt')

def load_map():
    # world.unload_map_layer(carla.MapLayer.Buildings)
    # world.unload_map_layer(carla.MapLayer.ParkedVehicles)
    # world.unload_map_layer(carla.MapLayer.StreetLights)
    # world.unload_map_layer(carla.MapLayer.Decals)
    # world.unload_map_layer(carla.MapLayer.Foliage)
    # world.unload_map_layer(carla.MapLayer.Particles)
    # world.unload_map_layer(carla.MapLayer.Props)
    # world.unload_map_layer(carla.MapLayer.Walls)
    # world.unload_map_layer(carla.MapLayer.Ground)
    world.unload_map_layer(carla.MapLayer.All)


def set_spectator_transform():
    # world = client.get_world()#获取世界
    spectator = world.get_spectator()
    spectator_transform = carla.Transform(
        carla.Location(x=0.0, y=0.0, z=200.0),
        carla.Rotation(pitch=-90,yaw=-90)  # 设置俯视角度
    )
    spectator.set_transform(spectator_transform)

def get_spawn_points(num_points):
    map = world.get_map()                     
    # 获取所有可能的车辆生成点
    spawn_points = map.get_spawn_points() 

    # 随机选择生成点
    random.shuffle(spawn_points)
    vehicle_spawn_points = spawn_points[:num_points]
    #将第一个点的location设置为0，0，0
    vehicle_spawn_points[0].location = carla.Location(0,0,0)

    # 在地图上标记这10个点，并显示编号
    for index, spawn_point in enumerate(vehicle_spawn_points):
        # 在地面上绘制一个3D文本显示数字
        text = str(index)
        world.debug.draw_string(spawn_point.location, text, draw_shadow=False,
                                color=carla.Color(r=255, g=0, b=0), life_time=600.0,
                                persistent_lines=True)
    return vehicle_spawn_points

def save_spawn_points_to_file(locations, filename):
    with open(filename, 'w') as f:
        for location in locations:
            f.write(f"{location.location.x}, {location.location.y}, {location.location.z}\n")
    ab_filename = os.path.abspath(filename)
    print(ab_filename)

try:
    file_name = 'carla_points_2.txt'

    # load_map()
    set_spectator_transform()
    vehicle_spawn_points = get_spawn_points( num_points= 21)
    save_spawn_points_to_file(vehicle_spawn_points,file_name)
    

finally:
    # 清理资源
    print('finally')