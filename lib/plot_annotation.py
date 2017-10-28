import os
import cv2
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET


class PlotAnnotation:
    def __init__(self, path_to_images, path_to_annotations, file_name, img_file_extension='jpg'):
        self.image = []
        self.img_path = path_to_images
        self.annotation_path = path_to_annotations
        self.file_name = file_name
        self.img_file_extension = img_file_extension
        self._validate_paths()

    def _validate_paths(self):
        # Can check whether the number of files in the annotations is the same as the number of images
        pass

    def display_annotated_image(self):
        # plt.axis('off')
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])
        plt.imshow(self.image)
        plt.show()

    def save_annotated_image(self, filename):
        cv2.imwrite(filename + ".png", self.image)

    def _assert_path(self, path, error_message):
        assert os.path.exists(path), error_message

    def _draw_on_img(self, x1, y1, x2, y2, label):
        color = {'Biker':(0, 255, 255), 'Pedestrian': (255, 0, 0), 'Cart': (0, 0, 255), 'Skater': (255, 255, 255),
                 'Car': (100, 100, 255), 'Bus': (255, 100, 100)}
        cv2.rectangle(self.image, (x1, y1), (x2, y2), color[label], 2)

        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = .3
        fontcolor = (255, 255, 255)
        cv2.putText(self.image, str(label), (x1, y1), fontface, fontscale, fontcolor)

    def plot_annotation(self):

        image_path = os.path.join(self.img_path, self.file_name + '.' + self.img_file_extension)
        self._assert_path(image_path, 'The corresponding image file for annotation not found at: ' + image_path)

        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Parse the xml annotation
        annotation_xml = open(os.path.join(self.annotation_path, self.file_name + '.xml'), 'r')
        tree = ET.parse(annotation_xml)
        root = tree.getroot()

        # For each bb-annotation in annotation:
        for annotation in root.findall('./object'):
            label = annotation.find('name').text
            xmin = int(annotation.find('./bndbox/xmin').text)
            ymin = int(annotation.find('./bndbox/ymin').text)
            xmax = int(annotation.find('./bndbox/xmax').text)
            ymax = int(annotation.find('./bndbox/ymax').text)
            self._draw_on_img(xmin, ymin, xmax, ymax, label)

if __name__ == '__main__':
    img_db_path = os.path.join('../data/images')
    annotation_path = os.path.join('../data/annotations')
    p = PlotAnnotation(img_db_path, annotation_path, 'bookstore_video0_5130')
    p.plot_annotation()
    p.display_annotated_image()
