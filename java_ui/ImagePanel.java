package java_ui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.FileWriter;
import java.io.IOException;

public class ImagePanel extends JPanel {

    private BufferedImage image;
    private int x1, y1, x2, y2;
    private boolean dragging = false;

    public ImagePanel() {
        // Souris : début + glissé + relâchement
        addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                x1 = e.getX();
                y1 = e.getY();
                dragging = true;
            }

            public void mouseReleased(MouseEvent e) {
                x2 = e.getX();
                y2 = e.getY();
                dragging = false;
                repaint();
                try {
                    saveSelectionToFile("shared/zerosub.txt");
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });

        addMouseMotionListener(new MouseMotionAdapter() {
            public void mouseDragged(MouseEvent e) {
                x2 = e.getX();
                y2 = e.getY();
                repaint();
            }
        });
    }

    public void setImage(BufferedImage img) {
        this.image = img;
        repaint();
    }

    private void saveSelectionToFile(String path) throws IOException {
        FileWriter writer = new FileWriter(path);
        writer.write(x1 + " " + y1 + " " + x2 + " " + y2);
        writer.close();
        System.out.println("Rectangle enregistré : " + x1 + " " + y1 + " " + x2 + " " + y2);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (image != null) {
            int w = getWidth();
            int h = getHeight();
            g.drawImage(image, 0, 0, w, h, null);

            // Rectangle de sélection
            if (dragging || (x1 != x2 && y1 != y2)) {
                g.setColor(Color.RED);
                int x = Math.min(x1, x2);
                int y = Math.min(y1, y2);
                int width = Math.abs(x2 - x1);
                int height = Math.abs(y2 - y1);
                g.drawRect(x, y, width, height);
            }
        }
    }
}
