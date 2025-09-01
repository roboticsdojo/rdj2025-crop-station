import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import cv2
import os

class ImageDisplayNode(Node):
    def __init__(self):
        super().__init__('image_display_node')
        # self.images_dir = os.path.join(os.path.dirname(__file__), 'images')
        self.images_dir = "/home/rdj2025-crop-station/src/crop_station/images/"
        self.sub_show = self.create_subscription(
            String,
            '/show',
            self.show_callback,
            10
        )
        self.sub_not_show = self.create_subscription(
            Bool,
            '/not_show',
            self.not_show_callback,
            10
        )
        self.current_image = None
        self.window_name = 'Image Display'
        self.running = True
        # Timer to update OpenCV display at 30Hz
        self.timer = self.create_timer(1.0/30.0, self.update_display)

    def show_callback(self, msg):
        filename = msg.data
        image_path = os.path.join(self.images_dir, filename)
        if os.path.isfile(image_path):
            try:
                image = cv2.imread(image_path)
                if image is not None:
                    self.current_image = image
                    self.get_logger().info(f"Displayed image: {filename}")
                else:
                    self.get_logger().error(f"Failed to load image {filename}: cv2.imread returned None")
            except Exception as e:
                self.get_logger().error(f"Failed to load image {filename}: {e}")
        else:
            self.get_logger().error(f"Image file not found: {os.getcwd()} >> {image_path} -> {filename}")

    def not_show_callback(self, msg):
        if msg.data:
            self.current_image = None
            cv2.destroyWindow(self.window_name)
            self.get_logger().info("Display cleared.")

    def update_display(self):
        if self.current_image is not None:
            cv2.imshow(self.window_name, self.current_image)
        else:
            # Show a blank image (black)
            blank = 255 * np.zeros((600, 800, 3), dtype=np.uint8)
            cv2.imshow(self.window_name, blank)
        # Handle window events
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            self.running = False
            rclpy.shutdown()


import numpy as np

def main(args=None):
    rclpy.init(args=args)
    node = ImageDisplayNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
