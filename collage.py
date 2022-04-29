import json
from PIL import Image
from color_poke import coloring_img


def collage(body_img: str, body_anchors: dict, appendage_assets, appendage_anchors):
    size = 128
    shift = size // 4
    new = Image.new('RGBA', (size, size), 'white')

    # paste body
    body = Image.open(body_img)
    new.paste(body, (shift, shift), body)

    # paste members
    for k, v in body_anchors.items():
        img = Image.open(appendage_assets[k])

        if k == 'head':
            x = v['x'] - appendage_anchors[k]['x']
            y = v['y'] - appendage_anchors[k]['y']
        elif 'left' in k:
            if 'arm' in k:
                x = v['x'] - img.width
                y = v['y'] - img.height // 2
            else:
                x = v['x'] - img.width // 2
                y = v['y']
        elif 'right' in k:
            if 'arm' in k:
                x = v['x']
                y = v['y'] - img.height // 2
            else:
                x = v['x'] - img.width // 2
                y = v['y']
        elif 'tail' in k:
            x = v['x'] - img.width // 4
            y = v['y'] - (img.height * 4) // 5
        else:
            x = v['x']
            y = v['y']

        new.paste(img, (x + shift, y + shift), img)

    return new


def main():

    with open('body.json') as f:
        data = json.load(f)

        with open('attachment.json') as f1:
            anchors = json.load(f1)
            '''appendage_assets = {
                "head": "assets/head/274.png",
                "left-arm": "assets/arm/185-1.png",
                "right-arm": "assets/arm/185-2.png",
                "left-leg": "assets/leg/217-1.png",
                "right-leg": "assets/leg/217-2.png"
            }
            collage('assets/body/383.png',
                    data['upright']["383"], appendage_assets)

            appendage_assets = {
                "head": "assets/head/160.png",
                "left-arm": "assets/arm/253-1.png",
                "right-arm": "assets/arm/253-2.png",
                "left-leg": "assets/leg/348-1.png",
                "right-leg": "assets/leg/348-2.png"
            }
            collage('assets/body/383.png',
                    data['upright']["383"], appendage_assets)'''

            appendage_assets = {
                "head": "assets/head/350.png",
                "back-right-leg": "assets/leg/262-3.png",
                "front-left-leg": "assets/leg/262-1.png",
                "front-right-leg": "assets/leg/262-2.png",
                "tail": "assets/tail/259.png"
            }

            appendage_assets = {
                "left-leg": "assets/leg/9-1.png",
                "right-leg": "assets/leg/9-2.png",
                "left-arm": "assets/arm/36-1.png",
                "head": "assets/head/132.png",
                "right-arm": "assets/arm/36-2.png"
            }
            appendage_anchors = {'head': anchors['head']['132']}

            collage('assets/body/383.png',
                    data['upright']["383"], appendage_assets, appendage_anchors)
            coloring_img(collage('assets/body/383.png',
                                 data['upright']["383"], appendage_assets, appendage_anchors), 'normal')

    return


if __name__ == "__main__":
    main()
