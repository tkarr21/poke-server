from PIL import Image, ImageOps


def coloring_img(img, type):
    color = None
    black = "black"
    if type == 'normal':
        color = 'papayawhip'
    elif type == 'fire':
        color = '#ff9980'
    elif type == 'water':
        color = '#80bfff'
    elif type == 'grass':
        color = '#9fdf9f'
    elif type == 'electric':
        color = '#ffff99'
    elif type == 'ice':
        color = '#ccffff'
    elif type == 'fighting':
        color = '#c98383'
    elif type == 'poison':
        color = '#d580ff'
    elif type == 'ground':
        color = '#ffd699'
    elif type == 'flying':
        color = '#f2e6ff'
    elif type == 'psychic':
        color = '#ffccff'
    elif type == 'bug':
        color = '#ccff99'
    elif type == 'rock':
        color = '#e6ccb3'
    elif type == 'ghost':
        color = '#330033'
        black = 'white'
    elif type == 'dark':
        color = '#c7c7c7'
    elif type == 'dragon':
        color = '#9999ff'
    elif type == 'steel':
        color = '#d0d0e1'
    elif type == 'fairy':
        color = '#ffe6ff'

    # applying grayscale method
    gray_image = ImageOps.grayscale(img)
    colored = ImageOps.colorize(gray_image, black=black, white=color)

    #img.show()
    #colored.show()
    #gray_image.show()

    return img, gray_image, colored

def main():
    # creating an og_image object
    og_image = Image.open("./assets/pokemon/1.png")

    types = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison',
             'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dark', 'dragon', 'steel', 'fairy']

    coloring_img(og_image, types[13])


if __name__ == "__main__":
    main()
