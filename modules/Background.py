from PIL import Image
from termcolor import colored
import random

class Background:
    color_scale = [
        "white", "yellow", "cyan", "red", "green",
        "blue", "magenta", "grey"
    ]
    chars = ["&","$","#","%","\\","/",":","-","."]
    def __init__(
            self, width=58, height=12, seed=0,
            orderness=50, brightness=50, noisiness=20,
            f = ""
    ):
        self.orderness = orderness
        self.brightness = brightness
        self.noisiness = noisiness
        self.brightness_map = int(
            (self.brightness / 100)*len(self.chars)
        )
        self.width = width
        self.height = height
        self.seed = seed
        self.f = f

    def get_background(self):
        if self.f == "":
            return self.make_background()
        else:
            return self.background_from_file()

    def make_background(self):
        random.seed(self.seed)

        usable_chars = [
            self.chars[(self.brightness_map-1) % len(self.chars)],
            self.chars[self.brightness_map % len(self.chars)],
            self.chars[(self.brightness_map+1) % len(self.chars)]
        ]
        
        color1 = self.color_scale[random.randint(0,7)]
        color2 = self.color_scale[random.randint(0,7)]
        color3 = self.color_scale[random.randint(0,7)]
        
        mapping = [
            [[char,color1] for char in usable_chars[2]*self.width]
            for h in range(self.height)
        ]

        for noise in range(self.noisiness):
            side = random.randint(1,4)
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            count = 0
            while (
                    x >= 0 and y >= 0 and
                    x < self.width and y<self.height and
                    count < self.noisiness
            ):
                count += 1
                mapping[y][x] = [usable_chars[1], color2]
                if side == 1:
                    x += 1
                elif side == 2:
                    y -= 1
                elif side == 3:
                    x -= 1
                elif side == 4:
                    y += 1
                if random.randint(0,100) > self.orderness:
                    side = ((side + random.randint(-1,1)) % 4) + 1
                
            top = random.randint(0,1)
            side = random.randint(0,1)
            if top:
                y = 0
            else:
                y = self.height-1
            if side:
                x = 0
            else:
                x = self.width-1

        for noise in range(self.noisiness):
            side = random.randint(1,4)
            if side == 1:
                x = 0
                y = random.randint(0, self.height-1)
            if side == 2:
                x = random.randint(0, self.width)
                y = 0
            if side == 3:
                x = self.width -1
                y = random.randint(0, self.height-1)
            if side == 4:
                x = random.randint(0, self.width)
                y = self.height-1
            count = 0
            while (
                    x >= 0 and y >= 0 and
                    x < self.width and y<self.height and
                    count < self.noisiness
            ):
                count += 1
                mapping[y][x] = [usable_chars[0], color2]
                if side == 1:
                    x += 1
                elif side == 2:
                    y -= 1
                elif side == 3:
                    x -= 1
                elif side == 4:
                    y += 1
                if random.randint(0,100) > self.orderness:
                    side = ((side + random.randint(-1,1)) % 4) + 1
                
            top = random.randint(0,1)
            side = random.randint(0,1)
            if top:
                y = 0
            else:
                y = self.height-1
            if side:
                x = 0
            else:
                x = self.width-1
        
        l = Text.Text("")
        l.add_listolists(mapping)
        return l

    def background_from_file(self):
        img = Image.open(self.f)

        w, h = img.size

        img = img.resize((self.width, self.height))
        pixels = img.getdata()
        img = img.convert('L')
        gpixels = img.getdata()

        new_pixels = [self.chars[pixel//28] for pixel in gpixels]
        colors = [pixel_to_color(pixel) for pixel in pixels]

        data = "".join(new_pixels)
        l = Text.Text("")
        for i, (char, col) in enumerate(zip(new_pixels, colors)):
            l.add_message(char, color=col, space="")
            if ((i+1) % self.width) == 0:
                l.add_message("\n")
        return l
            
def pixel_to_color(pixel):
    try:
        r, g, b = pixel
    except:
        r, g, b, _ = pixel
    if r > 150 and b > 150 and g > 150:
        return "grey"
    if r > 150 and b > 150:
        return "magenta"
    if r > 150 and g > 150:
        return "yellow"
    if r > 150:
        return "red"
    if g > 150:
        return "green"
    if b > 150:
        return "blue"
    return "white"

if __name__ == "__main__":
    import Text
    imgs = [
        "/home/harrison/Pictures/b2.png"
    ]
    Text.Text.use_term_color()
    for i in imgs:
        print(Background(f=i).get_background())

    print(Background().make_background())
    for seed, ordo, noise, bright in zip(
            ["Hallway","Kaleb", "Harrison", "Jacky Wong", "Franky Won"],
            [2, 60, 90, 20, 90],
            [5, 70, 70, 20, 20],
            [50, 0, 30, 99, 100]
    ):
        b = Background(
            seed=seed, orderness=ordo, noisiness=noise,
            brightness=bright
        )
        print(b.get_background())
    
    
else:
    from modules import Text
