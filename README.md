# Robotics Dojo 2025 Crop Station

## Image Display Node — Implementation Details

This document explains the **implementation** of the ROS 2 node that displays images on a Raspberry Pi 4 with an HDMI touchscreen. The node is written in Python using `rclpy` and `OpenCV`.

## Node Overview

- **Package name:** `crop_station`
- **Node name:** `image_display_node`
- **Subscriptions:**
  - `/show` (`std_msgs/String`) — expects a filename of an image to display.
  - `/not_show` (`std_msgs/Bool`) — when `true`, clears the display (reverts to orange background).
- **Display:**
  - Uses `OpenCV (cv2)` to render images in a fullscreen window.
  - When no image is set, an orange screen is shown instead of blank black.



## Key Features

-   Fullscreen OpenCV-based display.
    
-   Image file loading via topic.
    
-   Persistent orange background when cleared.
    
-   Keyboard interrupt and ESC handling for safe shutdown.
    
