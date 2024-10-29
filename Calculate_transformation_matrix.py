import numpy as np
from scipy.optimize import least_squares
import string
from PIL import Image
import os

def get_image_shape(img_path):
    image = Image.open(img_path)
    width, height = image.size
    return width, height

def read_img_points(file_name,width,height,num):
    img_points = []
    with open(file_name,'r') as A:
        for eachline in A:
            tmp = eachline.strip().split(',')
            x,y = float(tmp[0])-width/2,float(tmp[1])-height/2
            img_points.append([x,y])
    return img_points,img_points[:num]
def read_carla_points(file_name,num):
    carla_points = []
    with open(file_name,'r') as A:
        for eachline in A:
            tmp = eachline.strip().split(',')
            x,y = float(tmp[0]),float(tmp[1])
            carla_points.append([x,y])
    return carla_points,carla_points[:num]
def compute_transform_parameters(points_a, points_b):
    """
    计算缩放因子、旋转角度和平移量。
    """
    # 目标函数，最小化残差
    def residuals(params, points_a, points_b):
        sx, sy, theta, tx, ty = params
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([[c, -s], [s, c]])
        scale_matrix = np.array([[sx, 0], [0, sy]])
        transformation_matrix = rotation_matrix  @ scale_matrix
        transformed_points = np.dot(points_a, transformation_matrix.T) + [tx, ty]
        return (transformed_points - points_b).flatten()  # 展平为一维数组
    
    # 初始猜测值
    initial_guess = [1.0, 1.0, 0.0, 0.0, 0.0]  # 缩放因子sx, sy，旋转角，平移x，平移y
    
    # 使用最小二乘法优化
    result = least_squares(residuals, initial_guess, args=(points_a, points_b))
    
    return result.x[0], result.x[1], result.x[2], result.x[3], result.x[4]

def build_transformation_matrix(sx, sy, angle, translation):
    """
    根据给定的参数构建变换矩阵。
    """
    c, s = np.cos(angle), np.sin(angle)
    rotation_matrix = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    print("Rotation angle (radians):")
    print(rotation_matrix)

    scale_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
    print("Scale factor:")
    print( scale_matrix)

    translation_matrix = np.array([[1, 0, translation[0]], [0, 1, translation[1]], [0, 0, 1]])
    print("Translation vector:" )
    print(translation_matrix)

    # 计算最终的变换矩阵
    transform_matrix = translation_matrix @  scale_matrix @  rotation_matrix
    print("\nFinal Transformation Matrix:")
    print(transform_matrix)
    print("----------------------------------------")
    return rotation_matrix,scale_matrix,translation_matrix,transform_matrix # 只保留前两行，因为我们只关心二维变换

def save_points(file_name,data,data_name):
    with open(file_name, 'w') as f:
        for i in range(len(data)):
            # np.savetxt(f, data[i],delimiter=',')
            f.write(data_name[i]+"\n")
            f.write("["+"\n")
            for j in range(len(data[i])):
                f.write(str(data[i][j])+"\n")
            f.write("]"+"\n")
            f.write("\n")
        f.close()
    ab_filename = os.path.abspath(file_name)
    print(ab_filename)

def test_carla2img_list(id,transform_matrix,img_points,carla_points):
    test_carla_point = carla_points[id]
    test_img_point = img_points[id]
    print(f"test_carla_point : {test_carla_point}")
    print(f"test_img_point : {test_img_point}")

    transformed_validation_points = np.dot(test_carla_point, transform_matrix[:2, :2].T) 
    transformed_validation_points += transform_matrix[:2, 2]
    print(f"test_carla2img point: {transformed_validation_points}")
    print("----------------------------------------")

def test_carla2img(points,transform_matrix,width,height):
    all_carla2img_points = []
    for point in points:
        print(f"carla point : {point}")
        carla2img_point = np.dot(point, transform_matrix[:2, :2].T) 
        carla2img_point += transform_matrix[:2, 2]
        carla2img_point[0] += width/2
        carla2img_point[1] += height/2
        # 将carla2img_point四舍五入为整数
        carla2img_point = np.round(carla2img_point)
        # 化为整数
        carla2img_point = carla2img_point.astype(int)
        print(f"test_carla2img point: {carla2img_point}")
        print("----------------------------------------")
        all_carla2img_points.append(carla2img_point)
    gloal_interval_x,gloal_interval_y = 0,0
    num_x,num_y = 0,0
    for i in range(len(all_carla2img_points)-1):
        if all_carla2img_points[i][0] != all_carla2img_points[i+1][0]:
            gloal_interval_x += abs(all_carla2img_points[i][0]-all_carla2img_points[i+1][0])
            num_x += 1
        if all_carla2img_points[i][1] !=  all_carla2img_points[i+1][1]:
            gloal_interval_y += abs(all_carla2img_points[i][1]-all_carla2img_points[i+1][1])
            num_y += 1
    print(f"add: {add}")
    print(f"gloal_interval_x: {gloal_interval_x}")
    print(f"num_x: {num_x}")
    print(f"grid_interval_x: {gloal_interval_x/num_x}")
    print("----------------------------------------")
    print(f"add: {add}")
    print(f"grid_interval_y: {gloal_interval_y}")
    print(f"num_y: {num_y}")
    print(f"grid_interval_y: {gloal_interval_y/num_y}")

    return all_carla2img_points


if __name__ == "__main__":
    img_path = "Coordinate_system/carla_town03_allmap_points.png"
    img_points_file = "/home/sunbs/carla_0.9.14/Coordinate_system/img_label_2.txt"
    carla_points_file = "/home/sunbs/carla_0.9.14/Coordinate_system/carla_points_2.txt"
    output_file = "Coordinate_system/transformation_matrix.txt"
    try:

        width, height = get_image_shape(img_path)
        img_points,img_points_use = read_img_points(img_points_file,width=width,height=height,num=15)
        carla_points,carla_points_use = read_carla_points(carla_points_file,num=15)

        print (f"img_points_use: {img_points_use}")
        print (f"carla_points_use: {carla_points_use}")
        print("------------------------------------------")

        sx, sy, angle, tx, ty = compute_transform_parameters(carla_points_use,img_points_use)
        rotation_matrix,scale_matrix,translation_matrix,transform_matrix = build_transformation_matrix(sx, sy, angle, (tx, ty))

        data_name = ["rotation_matrix","scale_matrix","translation_matrix","transform_matrix"]
        data = np.array([rotation_matrix,scale_matrix,translation_matrix,transform_matrix])
        save_points(file_name=output_file,data=data,data_name=data_name)

        # 测试
        test_id = 5
        test_carla2img_list(test_id,transform_matrix,img_points,carla_points)

        add = 40
        
        points = [[0,0],[0,add],[add,0],[0,-add],[-add,0]]
        test_carla2img(points,transform_matrix,width,height)


    finally:
        print("Done")