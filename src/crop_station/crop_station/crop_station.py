#usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import pygame
import os


class ImageDisplayNode(Node):
    def __init__(self):
        super().__init__('image_display_node')
        self.get_logger().info("Image Display Node has started.")

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Set screen size
        pygame.display.set_caption("Image Display")

        # Subscriptions
        self.show_subscriber = self.create_subscription(
            String,
            '/show',
            self.show_callback,
            10
        )
        self.not_show_subscriber = self.create_subscription(
            Bool,
            '/not_show',
            self.not_show_callback,
            10
        )

        # Directory for images
        self.images_dir = os.path.join(os.getcwd(), 'images')

    def show_callback(self, msg):
        """Callback for /show topic."""
        image_filename = msg.data
        image_path = os.path.join(self.images_dir, image_filename)

        if os.path.exists(image_path):
            self.get_logger().info(f"Displaying image: {image_path}")
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (800, 600))  # Resize to fit screen
            self.screen.blit(image, (0, 0))
            pygame.display.flip()
        else:
            self.get_logger().error(f"Image file not found: {image_path}")

    def not_show_callback(self, msg):
        """Callback for /not_show topic."""
        if msg.data:
            self.get_logger().info("Clearing display.")
            self.screen.fill((0, 0, 0))  # Clear screen with black
            pygame.display.flip()


def main(args=None):
    rclpy.init(args=args)
    node = ImageDisplayNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Image Display Node.")
    finally:
        pygame.quit()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()