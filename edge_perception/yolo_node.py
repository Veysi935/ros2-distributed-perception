import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        # Kameradan gelen goruntulere abone oluyoruz
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.bridge = CvBridge()
        
        # YOLOv8 nano modelini yukluyoruz (hizli ve hafif)
        self.get_logger().info('YOLOv8 modeli yukleniyor...')
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info('YOLOv8 Dugumu Basariyla Baslatildi! Veri bekleniyor...')

    def listener_callback(self, msg):
        # 1. ROS2 Image mesajini OpenCV formatina cevir
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # 2. Resmi YOLO modeline sok ve nesneleri tespit et
        results = self.model(cv_image, verbose=False)
        
        # 3. Sonuclari (kutu ve etiketleri) resmin uzerine ciz
        annotated_frame = results[0].plot()
        
        # 4. Ekranda canli olarak goster
        cv2.imshow("TurtleBot3 - Yapay Zeka Gorus Ekrani", annotated_frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    yolo_node = YoloNode()
    rclpy.spin(yolo_node)
    yolo_node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
