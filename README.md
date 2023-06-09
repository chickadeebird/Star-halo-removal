# Star Halo Removal
The main goal of Star Halo Removal is to use Python code to remove halos from large stars. Halos are often due to fog or haze during the aquisition stage.


## Sections
- [Usage](#Usage)
- [Images](#images)
- [Code](#code)


---

## Usage
This is meant to be used as a standalone file for now. The file source is specified by stars_filename and the output location is specified as save_path at the end of the code.

The centre of the star to be reduced is specified as x_centre, y_centre. The estimated radius to be reduced is radius.

The power_factor, default is 10, is how aggressive the remove of the halo is to be.


## Images

This is a sample pair of images. The first image is Polaris taken on a night with some haze. The second image is after the Remove mono halo.py is run.

Acquired
<img src="./figs/Polaris with halo.jpg" align=left />
Post halo removal
<img src="./figs/Polaris without halo.jpg" align=right />


## Code

Remove mono halo.py

---

## Additional Resources
