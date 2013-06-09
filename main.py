import requests
import Image
import math
import StringIO
import time
import pygame
import datetime

point_width = 2
image_stream = 'http://streaming2.mdottraffic.com:1935/snapshots?application=rtplive&snap=020607.stream&num=1370817794327'
pause_secs = 10  # amount of secs between each graph update, varies according to img stream
time_step = 4 # move this amount on x axis between points


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
    red = (155, 155, 155)

    positions = []

    i = 1
    while True:
        r = requests.get(image_stream)
        x_pos = i
        # increase visiblilty
        y_pos = process(r) * 10

        with open('log.txt', 'a') as f:
            f.write(str(y_pos) + ',' + str(datetime.datetime.now()) + '\n')

        positions.append(y_pos)
        pygame.draw.rect(screen, blue, (i, y_pos, point_width, point_width), 0)

        prev_y_pos = positions[i/time_step - 1]
        prev_x_pos = i - time_step

        #surface, color, startpos, endpos
        if len(positions) == 1:
            pygame.draw.line(screen, red, (x_pos, y_pos), (x_pos, y_pos))
        else:
            pygame.draw.line(screen, red, (prev_x_pos, prev_y_pos), (x_pos, y_pos))

        pygame.transform.flip(screen, 0, 1)
        pygame.display.flip()
        time.sleep(pause_secs)

        i += time_step

if __name__ == '__main__':
    main()
    pygame.quit()