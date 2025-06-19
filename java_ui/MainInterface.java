package java_ui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;

public class MainInterface extends JFrame {

    private ImagePanel imagePanel;
    private JTextField deltaField;
    private JTextField levelField;
    private JLabel statusLabel;

    public MainInterface() {
        setTitle("Transformée en Ondelette");
        setSize(700, 700);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Zone d’affichage image
        imagePanel = new ImagePanel();
        add(imagePanel, BorderLayout.CENTER);

        // Boutons et champs
        JPanel controlPanel = new JPanel();
        JButton openButton = new JButton("Ouvrir une image");
        JButton processButton = new JButton("Lancer la transformée");

        deltaField = new JTextField("10", 5);
        levelField = new JTextField("2", 5);

        controlPanel.add(openButton);
        controlPanel.add(new JLabel("Delta:"));
        controlPanel.add(deltaField);
        controlPanel.add(new JLabel("Niv. Résol:"));
        controlPanel.add(levelField);
        controlPanel.add(processButton);

        add(controlPanel, BorderLayout.SOUTH);

        // Label de statut
        statusLabel = new JLabel("Statut : En attente");
        add(statusLabel, BorderLayout.NORTH);

        // Écouteurs
        openButton.addActionListener(e -> openImage());
        processButton.addActionListener(e -> runTransform());

        setVisible(true);
    }

    private void openImage() {
        JFileChooser chooser = new JFileChooser();
        int result = chooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selected = chooser.getSelectedFile();
            try {
                BufferedImage img = ImageUtils.loadGrayscaleImage(selected);
                ImageUtils.saveImage(img, "shared/input.png");
                imagePanel.setImage(img);
                statusLabel.setText("Image chargée : " + selected.getName());
            } catch (Exception ex) {
                ex.printStackTrace();
                JOptionPane.showMessageDialog(this, "Erreur : " + ex.getMessage());
            }
        }
    }

    private void runTransform() {
        try {
            String delta = deltaField.getText().trim();
            String levels = levelField.getText().trim();
            String cmd = "python python_core/process_image.py " + levels + " " + delta;

            statusLabel.setText("Traitement en cours…");

            Process process = Runtime.getRuntime().exec(cmd);
            process.waitFor();

            statusLabel.setText("Transformée terminée !");

            File outputFile = new File("shared/output.png");
            if (outputFile.exists()) {
                BufferedImage outputImg = ImageIO.read(outputFile);
                imagePanel.setImage(outputImg);
            } else {
                JOptionPane.showMessageDialog(this, "Erreur : output.png introuvable !");
            }
        } catch (Exception e) {
            e.printStackTrace();
            statusLabel.setText("Erreur lors du traitement");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MainInterface());
    }
}
