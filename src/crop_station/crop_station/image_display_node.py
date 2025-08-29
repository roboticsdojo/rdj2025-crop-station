import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import pygame
import os

class ImageDisplayNode(Node):
    def __init__(self):
        super().__init__('image_display_node')
        self.images_dir = os.path.join(os.path.dirname(__file__), 'images')
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
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Image Display')
        self.clock = pygame.time.Clock()
        self.current_image = None
    self.running = True
    # Timer to update pygame display at 30Hz
    self.timer = self.create_timer(1.0/30.0, self.update_display)

    def show_callback(self, msg):
        filename = msg.data
        image_path = os.path.join(self.images_dir, filename)
        if os.path.isfile(image_path):
            try:
                self.current_image = pygame.image.load(image_path)
                self.get_logger().info(f"Displayed image: {filename}")
            except Exception as e:
                self.get_logger().error(f"Failed to load image {filename}: {e}")
        else:
            self.get_logger().error(f"Image file not found: {filename}")

    def not_show_callback(self, msg):
        if msg.data:
            self.current_image = None
            self.get_logger().info("Display cleared.")

    def update_display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                rclpy.shutdown()
        if self.current_image:
            self.screen.fill((128, 128, 128))
            self.screen.blit(self.current_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        pygame.display.flip()
        self.clock.tick(30)


def main(args=None):
    rclpy.init(args=args)
    node = ImageDisplayNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    pygame.quit()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
