# Image Display Node — Usage Guide

This guide explains how to **use the Image Display Node** in a ROS 2 workspace on a Raspberry Pi 4 (Ubuntu 22.04).



## 1. Running the Node

Start the node:

```bash
ros2 run crop_station image_display_node
```


The display window will:

-   Run in **fullscreen** mode on the HDMI touchscreen.
    
-   Start with an **orange background**.
    

## 2. Topics

### `/show` (std_msgs/String)

-   Payload: **filename of an image** located in the package's `images/` directory.
    
-   Example:
    
    ```bash
    ros2 topic pub /show std_msgs/msg/String "data: 'a.png'"
    ```
    
-   If `a.png` exists in:
    
    ```
    ~/ros2_display_ws/src/crop_station/images/a.png
    ```
    
    it will be displayed fullscreen.
    


### `/not_show` (std_msgs/Bool)

-   Payload: `true` clears the display (switches back to orange).
    
-   Example:
    
    ```bash
    ros2 topic pub /not_show std_msgs/msg/Bool "data: true"

    ```
    

----------

## 3. Exiting the Node

-   Press **ESC** on the keyboard. (Currently not working - not too much of a bother either, so I will not fix this!)
    
-   Or stop the process with:
    
    ```bash
    Ctrl + C
    ```

## 4. Example Workflow

1.  Start the node:
    
    ```bash
    ros2 run crop_station image_display_node
    ```
    
2.  Show an image:
    
    ```bash
    ros2 topic pub /show std_msgs/msg/String "data: 'welcome.png'"
    ```
    
3.  Clear the screen (orange background):
    
    ```bash
    ros2 topic pub /not_show std_msgs/msg/Bool "data: true"
    ```
    

----------

## 6. Notes

-   Images must be placed in:
    
    ```
    ~/rdj2025-crop-station/src/crop_station/images/
    ```
    
-   The display automatically resizes images to `1280x720` (changeable in code).
    
-   Make sure your Raspberry Pi has OpenCV installed:
    
    ```bash
    sudo apt install python3-opencv    
    ```
    
