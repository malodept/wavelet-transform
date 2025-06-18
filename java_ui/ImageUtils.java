package java_ui;

import java.awt.image.BufferedImage;
import java.awt.Color;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class ImageUtils {

    public static BufferedImage loadGrayscaleImage(File file) throws IOException {
        BufferedImage img = ImageIO.read(file);
        BufferedImage gray = new BufferedImage(img.getWidth(), img.getHeight(), BufferedImage.TYPE_BYTE_GRAY);

        for (int y = 0; y < img.getHeight(); y++) {
            for (int x = 0; x < img.getWidth(); x++) {
                Color c = new Color(img.getRGB(x, y));
                int grayValue = (int)(0.299 * c.getRed() + 0.587 * c.getGreen() + 0.114 * c.getBlue());
                int grayRGB = new Color(grayValue, grayValue, grayValue).getRGB();
                gray.setRGB(x, y, grayRGB);
            }
        }

        return gray;
    }

    public static void saveImage(BufferedImage img, String path) throws IOException {
        File output = new File(path);
        output.getParentFile().mkdirs();
        ImageIO.write(img, "png", output);
    }
}
