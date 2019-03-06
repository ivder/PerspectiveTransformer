# PerspectiveTransformer
Python GUI program to do Perspective Transformation using Mouse Click to map the 4 points coordinates. 
Purpose : Pre-Processing for Object Detection dataset annotation.

# Requirements
 - Python3
 - TkInter
 - PIL
 - OpenCV 3.x

# Usage

1. Select image file<br>
![](https://github.com/gameon67/PerspectiveTransformer/blob/master/ss1.jpg)

2. Use <kbd>left-mouse-click</kbd> to save the coordinate and ret dot will be created. 
    - **Remember : You have to create point coordinates in the RIGHT ORDER**
    - **top-left, top-right, bottom-left, bottom-right**
![](https://github.com/gameon67/PerspectiveTransformer/blob/master/ss2.jpg)

3. To delete/remove last created coordinate press <kbd>right-mouse-click</kbd> and the ret dot will be deleted as well

4. After 4 points are created, the transformation result will be shown directly
![](https://github.com/gameon67/PerspectiveTransformer/blob/master/ss3.jpg)

5. Use `save` button to save the result image in result/..
