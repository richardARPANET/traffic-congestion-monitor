import requests
import Image
import math
import StringIO
import time
import pygame
import datetime

point_width = 1
image_stream = 'http://www.bbc.co.uk/travelnews/motorways/trafficcameras/highwaysagency/50265/1370785351159/image'
pause_secs = 35  # amount of secs between each graph update, varies according to img stream


def process(r):
    output = StringIO.StringIO(r.content)
    img = Image.open(output)
    return entropy(img)


def entropy(img):
    # by calculating
    """
    By calculating entropy of the img stream
    density of traffic can be roughly measured
    """
    histogram = img.histogram()
    histogram_size = sum(histogram)
    histogram = [float(h) / histogram_size for h in histogram]

    return -sum([p * math.log(p, 2) for p in histogram if p != 0])


def main():
    # setup pygame window
    screen = pygame.display.set_mode((1200, 450))
    pygame.display.set_caption("graph")
    screen.fill((255, 255, 255))
    blue = (0, 0, 255)

    i = 0
    while True:
        i += point_width
        r = requests.get(image_stream)
        # increase visiblilty
        value = process(r) * 10
        print value
        print datetime.datetime.now()

        with open('log.txt', 'a') as f:
            f.write(str(value) + ',' + str(datetime.datetime.now()) + '\n')

        pygame.draw.rect(screen, blue, (i, 10, point_width, value), 0)
        pygame.display.flip()
        time.sleep(pause_secs)


if __name__ == '__main__':
    main()
    pygame.quit()