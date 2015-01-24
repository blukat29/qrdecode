
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;

import com.google.zxing.LuminanceSource;
import com.google.zxing.BufferedImageLuminanceSource;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.NotFoundException;
import com.google.zxing.FormatException;

import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.common.DetectorResult;
import com.google.zxing.common.BitMatrix;

import com.google.zxing.qrcode.detector.Detector;

public class SimpleQRDetector {

  private static void error(String msg, int code) {
    System.err.println(msg);
    System.exit(code);
  }

  public static void main (String[] args) {
    if (args.length == 0) {
      error("No filename provided", 1);
    }
    String name = args[0];

    BufferedImage image = null;
    try {
      image = ImageIO.read(new File(name));
    } catch(IOException e) {
      error("Cannot open file", 2);
    }

    LuminanceSource source = new BufferedImageLuminanceSource(image);
    BinaryBitmap bitmap = new BinaryBitmap(new HybridBinarizer(source));

    DetectorResult result = null;
    try {
      result = (new Detector(bitmap.getBlackMatrix())).detect();
    } catch(NotFoundException e) {
      error("QRCode not detected", 3);
    } catch(FormatException e) {
      error("QRCode shape is invalid", 4);
    }

    BitMatrix mat = result.getBits();
    System.out.print(mat.toString("X"," "));
  }
}
