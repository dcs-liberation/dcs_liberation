In this folder are icons for the different units in DCS / DCS Liberation. 

# How were these retrieved :
- I took screenshoot of the units from the encyclopedia in DCS. If you want to add more pictures, please do the same, so that the units have the same background.
- Then resized all the image so that have static size. Aspect ratio is not perfect, but it's hard to notice on such small image.

```python

import os
from PIL import Image

for img_name in os.listdir("."):
	if os.path.isfile(img_name) and img_name.endswith(".png"):
		print(img_name)
		img = Image.open(img_name)
		img = img.resize((64,24), Image.ANTIALIAS)
		img.save('./out/' + img_name[:-4] + "_24.jpg")

```

You need PIL to run the script : 

```
pip install PIL
```

If you want access to get my high res screenshoot, i still have them, but to reduce size and ram usage, i believe it's better to use super small jpg icons instead.

@Khopa