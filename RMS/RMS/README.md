MT3 Project: projet_cmt

Install Pierre Blazevic's image:  
- compile example:

  cd ~/catkin_ws
  
  catkin_make
  
To run:
-   launch camera, rosserial_python topic, projet_cmt and rqt image_view at one time:

    roslaunch projet_cmt Tata.launch 
    
-   use of services: ajust the picture's calibration to determine features of the screening for our subject, thanks to HSV parameters:

    rosservice call /Traitement_HSV Value1 Value2 Value3 Value4 Value5 Value6
    
-   It can be preferable to launch the command below to facilitate calibration:

    opencv3_V2_node
    
