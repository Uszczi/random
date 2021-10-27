import urllib.request
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


response = urllib.request.urlopen(
    "https://helpx.adobe.com/content/dam/help/en/photoshop/using/convert-color-image-black-white/jcr_content/main-pars/before_and_after/image-before/Landscape-Color.jpg"
)
import numpy as np

i = mpimg.imread(response.fp, format="jpeg")

by = i.tobytes()

with open("dsaf.png", "wb") as f:
    f.write(by)

with open("dsaf2.png", "wb") as f:
    f.write(i)

plt.imshow(i)
# plt.imshow(by)

# plt.imsave(i)
i2 = mpimg.imread(by)


img
