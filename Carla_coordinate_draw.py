from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm
def create_grid_on_image(image_path, origin,grid_interval_x,grid_interval_y,add_x,add_y, output_path):
    try:
        # 加载图像
        img = Image.open(image_path)
    except IOError as e:
        print(f"Error opening image file: {e}")
        return

    draw = ImageDraw.Draw(img)

    # 获取图像尺寸
    width, height = img.size

    # 设置坐标轴的颜色
    axis_color = 'green'
    grid_color = 'gray'
    label_color = 'red'

    # 尝试加载字体
    try:
        # font = ImageFont.truetype("STKaiti", 20)
        fontsize = 15
        font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')),fontsize)
    except IOError:
        # 如果找不到字体文件，则使用默认字体
        print("Error loading font. Using default font.")
        font = ImageFont.load_default()

    # 计算中心位置作为原点 (0,0)
    center_x = origin[0]
    center_y = origin[1]

    # 绘制网格线
    for x in range(center_x, width, grid_interval_x):
        draw.line([(x, 0), (x, height)], fill=grid_color)
    for x in range(center_x, 0, -grid_interval_x):
        draw.line([(x, 0), (x, height)], fill=grid_color)
    for y in range(center_y, height, grid_interval_y):
        draw.line([(0, y), (width, y)], fill=grid_color)
    for y in range(center_y, 0, -grid_interval_y):
        draw.line([(0, y), (width, y)], fill=grid_color)

    # 绘制坐标轴
    draw.line([(0, center_y), (width, center_y)], fill=axis_color)
    draw.line([(center_x, 0), (center_x, height)], fill=axis_color)

    # 在坐标轴上放置坐标值标签
    x_label_ps,x_label_ng = 0,0
    for x in range(center_x , width, grid_interval_x):
        draw.text((x-10, center_y ), str(x_label_ps), fill=label_color, font=font)
        x_label_ps += add_x
    for x in range(center_x , 0, -grid_interval_x):
        draw.text((x-10, center_y ), str(x_label_ng), fill=label_color, font=font)
        x_label_ng -= add_x
    y_label_ps,y_label_ng = 0,0
    for y in range(center_y+grid_interval_y, height, grid_interval_y):
        y_label_ps += add_y
        draw.text((center_x , y-10), str(y_label_ps), fill=label_color, font=font)
        
    for y in range(center_y-grid_interval_y, 0, -grid_interval_y):
        y_label_ng -= add_y
        draw.text((center_x , y-10), str(y_label_ng), fill=label_color, font=font)

    # 保存带有网格的图像
    # img.save(output_path)
    img.show()

# 使用函数
if __name__ == "__main__":
    image_path = 'Coordinate_system/carla_town03_allmap.png'  # 图片路径
    output_path = 'Coordinate_system/output_with_coordinates.png'  # 输出路径
    origin = [348,524]
    add_x = 40
    add_y = 40
    grid_interval_x = 79 
    grid_interval_y = 78
    create_grid_on_image(image_path,origin, grid_interval_x,grid_interval_y,add_x,add_y, output_path)