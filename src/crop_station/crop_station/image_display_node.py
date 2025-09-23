import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import numpy as np
import cv2
import os

class ImageDisplayNode(Node):
    """
    ROS2 Node for displaying images on a Raspberry Pi screen using OpenCV.
    Subscribes to:
      - /show (std_msgs/String): expects a filename to display
      - /not_show (std_msgs/Bool): clears the display when True
    """

    def __init__(self):
        super().__init__('image_display_node')

        # Directory where images are stored (relative path didn't work)
        self.images_dir = "/home/screen/Desktop/rdj2025-crop-station/src/crop_station/images/"

        # Subscription to /show topic (expects filename as String) -> a.png
        self.sub_show = self.create_subscription(
            String,
            '/show',
            self.show_callback,
            10
        )

        # Subscription to /not_show topic (expects Bool message) -> true/false
        # If True, the display will be cleared
        self.sub_not_show = self.create_subscription(
            Bool,
            '/not_show',
            self.not_show_callback,
            10
        )

        # Variable to hold the currently displayed image
        self.current_image = None

        # OpenCV window name (used for identifying and controlling the window)
        self.window_name = 'Image Display'

        # Target screen resolution (we'll adjust this to our Raspberry Pi HDMI screen size)
        self.resolution = (1280, 720)

        # Create a fullscreen window using OpenCV
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Running flag (set to False when ESC is pressed)
        self.running = True

        # Show orange image to set window size and fullscreen immediately
        orange_bgr = (16, 117, 242)  # OpenCV uses BGR, so #f27510ff -> (16,117,242)
        blank = np.full((self.resolution[1], self.resolution[0], 3), orange_bgr, dtype=np.uint8)
        cv2.imshow(self.window_name, blank)
        cv2.waitKey(1)

        # Timer to update OpenCV display at 30Hz (refresh rate)
        self.timer = self.create_timer(1.0 / 30.0, self.update_display)

    def show_callback(self, msg):
        """
        Callback for /show topic.
        Loads and displays an image when a filename is received.
        """
        filename = msg.data
        image_path = os.path.join(self.images_dir, filename)

        if os.path.isfile(image_path):
            try:
                # Load the image from disk
                image = cv2.imread(image_path)

                if image is not None:
                    self.current_image = image
                    self.get_logger().info(f"Displayed image: {filename}")
                else:
                    # Handle case where cv2.imread fails
                    self.get_logger().error(f"Failed to load image {filename}: cv2.imread returned None")
            except Exception as e:
                self.get_logger().error(f"Failed to load image {filename}: {e}")
        else:
            # Log error if the file doesn’t exist
            self.get_logger().error(f"Image file not found: {os.getcwd()} >> {image_path} -> {filename}")

    def not_show_callback(self, msg):
        """
        Callback for /not_show topic.
        Clears the display when True is received.
        """
        if msg.data:
            self.current_image = None
            self.get_logger().info("Display cleared.")

    def update_display(self):
        """
        Timer callback that refreshes the display window at 30Hz.
        - Shows the current image if available
        - Otherwise shows a blank screen
        - Listens for ESC key press to exit
        """
        if self.current_image is not None:
            # Resize image to match target resolution
            image_resized = cv2.resize(self.current_image, self.resolution, interpolation=cv2.INTER_AREA)
            cv2.imshow(self.window_name, image_resized)
        else:
            # Show orange image if no image is set
            orange_bgr = (16, 117, 242)  # OpenCV uses BGR, so #f27510ff -> (16,117,242)
            blank = np.full((self.resolution[1], self.resolution[0], 3), orange_bgr, dtype=np.uint8)
            cv2.imshow(self.window_name, blank)

        # Handle window events
        key = cv2.waitKey(1)
        if key == 27:  # ESC key pressed
            self.running = False
            rclpy.shutdown()


def main(args=None):
    """
    Main function to initialize the ROS2 node and start spinning.
    """
    rclpy.init(args=args)
    node = ImageDisplayNode()
    try:
        # Keep the node alive and responsive
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Graceful shutdown when Ctrl+C is pressed
        pass
    finally:
        # Cleanup: destroy node and close OpenCV windows
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
