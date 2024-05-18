import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
import os

class PerformanceCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.browse_bmp_button = QPushButton('Browse BMP Image')
        self.browse_png_button = QPushButton('Browse PNG Image')
        self.bmp_label = QLabel('BMP Image')
        self.png_label = QLabel('PNG Image')

        self.bmp_filename_label = QLabel('')
        self.png_filename_label = QLabel('')

        self.calculate_psnr_button = QPushButton('Calculate PSNR and Compression Rate')
        self.result_label = QLabel('PSNR: N/A dB')
        self.compression_rate_label = QLabel('Compression Rate: N/A')

        self.bmp_image_path = None
        self.png_image_path = None

        # layout setup
        layout = QVBoxLayout()

        images_layout = QHBoxLayout()

        bmp_layout = QVBoxLayout()
        bmp_layout.addWidget(self.bmp_filename_label)
        bmp_layout.addWidget(self.browse_bmp_button)
        bmp_layout.addWidget(self.bmp_label)

        png_layout = QVBoxLayout()
        png_layout.addWidget(self.png_filename_label)
        png_layout.addWidget(self.browse_png_button)
        png_layout.addWidget(self.png_label)

        images_layout.addLayout(bmp_layout)
        images_layout.addLayout(png_layout)

        layout.addLayout(images_layout)
        layout.addWidget(self.calculate_psnr_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.compression_rate_label)

        self.browse_bmp_button.clicked.connect(self.load_bmp_image)
        self.browse_png_button.clicked.connect(self.load_png_image)
        self.calculate_psnr_button.clicked.connect(self.calculate_psnr_and_compression_rate)

        self.setLayout(layout)
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('Image Compare')
        self.show()

    def load_bmp_image(self):
        bmp_path, _ = QFileDialog.getOpenFileName(self, 'Open BMP Image', '', 'BMP Files (*.bmp);;All Files (*)')
        if bmp_path:
            self.bmp_image = cv2.imread(bmp_path)
            self.display_image(self.bmp_image, self.bmp_label)
            self.bmp_filename_label.setText(os.path.basename(bmp_path))
            self.bmp_image_path = bmp_path

    def load_png_image(self):
        png_path, _ = QFileDialog.getOpenFileName(self, 'Open PNG Image', '', 'PNG Files (*.png);;All Files (*)')
        if png_path:
            self.png_image = cv2.imread(png_path)
            self.display_image(self.png_image, self.png_label)
            self.png_filename_label.setText(os.path.basename(png_path))
            self.png_image_path = png_path

    def calculate_psnr_and_compression_rate(self):
        try:
            if self.bmp_image_path and self.png_image_path:
                bmp_image = cv2.imread(self.bmp_image_path).astype(np.float32)
                png_image = cv2.imread(self.png_image_path).astype(np.float32)

                if bmp_image.shape == png_image.shape:
                    psnr_value = self._calculate_psnr(bmp_image, png_image)
                    self.result_label.setText(f'PSNR: {psnr_value:.2f} dB')

                    # image path
                    bmp_size = os.path.getsize(self.bmp_image_path)
                    png_size = os.path.getsize(self.png_image_path)

                    # compression rate
                    compression_rate = bmp_size / png_size
                    self.compression_rate_label.setText(f'Compression Rate: {compression_rate:.2f}')
                else:
                    self.result_label.setText('Images must have the same dimensions.')
            else:
                self.result_label.setText('Please load both BMP and PNG images.')
        except Exception as e:
            self.result_label.setText(f'Error: {str(e)}')

    def _calculate_psnr(self, img1, img2):
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return float('inf')  # inf = infinite
        max_pixel_value = 255.0
        psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
        return psnr
      
    def display_image(self, image, label):
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # BGR to RGB
            q_img = q_img.rgbSwapped()

            pixmap = QPixmap(q_img)
            label.setPixmap(pixmap)

# start main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    psnr_calculator = PerformanceCalculator()
    sys.exit(app.exec_())
