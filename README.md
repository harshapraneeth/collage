<img src="D:\projects\collage_maker\killmonger_comparision.jpg" alt="killmonger_comparision" style="zoom:10%;" />

# Picture collage

**Introduction: ** Here we do something similar to what we do in [Image to Ascii](https://github.com/harshapraneeth/image_to_ascii) but instead of mapping each pixel to a character we map to smaller images, like in the above picture.

**Approach: **To make life easier for myself I chose python to do this. Opencv and Numpy make this so much easier than the *Image to Ascii*. The steps for achieving this are,

- Preparing the images:

  - First of all we need a target image. Something like this,

    <img src="D:\projects\collage_maker\killmonger.jpg" alt="killmonger" style="zoom:10%;" />

  - And a set of images which we use to create the collage. Let’s call these set of images the input images. Once we have all the images we have to resize the input images to something reasonable like 60X60. Let’s call this the cell size. So we map the 60X60 area of the target image to one of the input_images. We refer to this 60X60 or cell size X cell size area as a cell.

- Mapping: How do we go about picking an image from input images which fits a cell in the target image? We pic the image whose average RGB value is nearest to the average of the cell in the target image.

  <img src="D:\projects\collage_maker\square_killmonger_3600_100_0.jpg" alt="square_killmonger_3200_100_0" style="zoom:10%;" />

- Overlay: We can add an overlay of the original target image on to the output image for a better appearance. Here you can compare the images with increasing overlay opacity from 0 to 60%.

  ![killmonger_opacity](D:\projects\collage_maker\killmonger_opacity.jpg)

- Different cells: Instead of fixing the cells to be squares we can allow rectangular cells.

  ![killmonger_square_comparision](D:\projects\collage_maker\killmonger_square_comparision.jpg)

  You can compare them better if you zoom in,

  ![killmonger_zoomed](D:\projects\collage_maker\killmonger_zoomed.jpg)

  On the left you can see that all the cell are of the same size, whereas on the right we have all kinds of cells.

**Result:** At the end the image with varying cell size and an overlay opacity of 25% looks better. The output image is,

![killmonger_3600_60_25](D:\projects\collage_maker\killmonger_3600_60_25.jpg)

As I hate myself, I also implemented a crude version in Javascript without any optimizations so you can test this on you browser. [Demo.](https://collagemaker.glitch.me/) Also the code is in the Github [repo](https://github.com/harshapraneeth/collage_maker).
