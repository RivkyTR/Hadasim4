
//package project;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.scene.control.*;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.Pane;
import javafx.scene.shape.Rectangle;
import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import javafx.scene.shape.Polygon;

/**
 * @author Rivky Terebelo
 *
 */
public class ProjectController implements Initializable {
    @FXML
    private AnchorPane anchorPane;
    @FXML
    private Button exitButton;
    @FXML
    private TextField heightInput;
    @FXML
    private Label labelTowers;
    @FXML
    private Pane paneDeatails;
    @FXML
    private Rectangle rectangle;
    @FXML
    private Polygon triangle;
    @FXML
    private TextField widthInput;

    public void initialize(URL location, ResourceBundle resources) {

    }

    @FXML
    void exitClicked(ActionEvent event) {
        System.exit(0);
    }

    @FXML
    void rectangleClicked(MouseEvent event) {
        hideObjects();
        Button submit = new Button("Submit");
        submit.setLayoutX(340);
        submit.setLayoutY(400);
        anchorPane.getChildren().add(submit);

        submit.setOnAction(event1 -> {
            anchorPane.getChildren().remove(submit);
            double [] size = new double[2];
            if(!isValid(size))//checking if the size of the rectangle is OK
                return;
            double width = size[0], height = size[1];
            if (height == width || Math.abs(height - width) > 5)
                showAlert(Alert.AlertType.INFORMATION, "Area", "The area of the tower is " + height*width);
            else
                showAlert(Alert.AlertType.INFORMATION, "Perimeter", "The perimeter of the tower is " + (height+width)*2);
            backToMenu();
        });
    }

    @FXML
    void triangleClicked(MouseEvent event) {
        hideObjects();
        Button perimeter = new Button("Triangle perimeter");
        Button print = new Button("Triangle print");
        perimeter.setLayoutX(240);
        perimeter.setLayoutY(400);
        print.setLayoutX(352);
        print.setLayoutY(400);
        anchorPane.getChildren().addAll(perimeter,print);

        perimeter.setOnAction(event1 -> {
            anchorPane.getChildren().remove(print);
            anchorPane.getChildren().remove(perimeter);
            double [] size = new double[2];
            if(isValid(size)) {
                double width = size[0], height = size[1];
                double lengthOfSide = Math.sqrt(Math.pow(height, 2) + Math.pow((width / 2.0), 2));
                showAlert(Alert.AlertType.INFORMATION, "Perimeter", "The perimeter of the tower is " + (lengthOfSide * 2 + width));
                backToMenu();
            }
        });
        print.setOnAction(event1 -> {
            anchorPane.getChildren().remove(print);
            anchorPane.getChildren().remove(perimeter);
            double [] size = new double[2];
            if(isValid(size)) {
                double width = size[0], height = size[1];
                if (width%2 == 0 || width/height > 2 || width%1 !=0 || height%1 !=0)
                    //If the width is even or it is greater than 2 times the height or it is not a integer
                    showAlert(Alert.AlertType.ERROR, "Printing problem", "Can not print the triangle.");
                else if(height < 2)
                    showAlert(Alert.AlertType.ERROR, "Printing problem", "Can not print a triangle less than 2 floors.");
                else if ( width == 1)
                    showAlert(Alert.AlertType.ERROR, "Printing problem", "This is not a triangle, it is a rectangle.");
                else if (width == 3 && height != 2)
                    //Edge case where we can't get a tower
                    showAlert(Alert.AlertType.ERROR, "Printing problem", "Can not print the triangle.");
                else if(width == 3 && height == 2)
                    //Edge case of an edge case where we can get a tower
                    showAlert(Alert.AlertType.INFORMATION, "Printing rectangle", " *\n***");
                else{
                    int numberOfOddNumbers = (int)(width/2) + 1;
                    int numberOfOddInMiddle = numberOfOddNumbers - 2;
                    int numberOfMiddleLines = (int)height - 2;//number of lines beside the first and the last
                    int numberOfLinesforOdd = numberOfMiddleLines / numberOfOddInMiddle;
                    //numberOfLinesforOdd is number of lines foe each odd number
                    int divisionRemainder = numberOfMiddleLines % numberOfOddInMiddle;
                    String printTriangle ="";

                    for (int i = 0, numberOfSpaces = ((int)width / 2), numberOfStars = 1; i < numberOfOddNumbers; i++, numberOfSpaces--, numberOfStars+=2) {
                        int repeatLines = numberOfStars == 1 ? 1 : numberOfLinesforOdd;//if 1 star print it once
                        repeatLines = numberOfStars == 3? numberOfLinesforOdd + divisionRemainder : repeatLines;
                        //if 3 stars number prints include remainder
                        String stringToPrint = repeat(" ", numberOfSpaces) + repeat("*", numberOfStars)  + '\n';
                        for (int j = 0; j < repeatLines; j++) {
                            printTriangle += stringToPrint;
                            if (numberOfStars == width) {//the lest line should be printed once
                                break;
                            }
                        }
                    }
                    showAlert(Alert.AlertType.INFORMATION, "Printing rectangle", printTriangle);
                }
                backToMenu();
            }
        });
    }

    boolean isValid(double [] sizes){
        String widthStr = widthInput.getText();
        String heightStr = heightInput.getText();
        double width, height;
        try {
            width = Double.parseDouble(widthStr);
            height = Double.parseDouble(heightStr);
            if ( width < 1 || height < 1)
                throw new NumberFormatException("Width and height can not be smaller than 1");
        } catch (NumberFormatException e) {
            showAlert(Alert.AlertType.ERROR, "Invalid Input", "You entered non valid numeric values for width or height.");
            backToMenu();
            return false;
        } catch (Exception e){
            showAlert(Alert.AlertType.ERROR, "Invalid Input","Invalid Input");
            backToMenu();
            return false;
        }
        sizes[0] = width;
        sizes[1] = height;
        return true;
    }

    private void showAlert(Alert.AlertType alertType, String title, String content) {
        Alert alert = new Alert(alertType);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(content);
        alert.showAndWait();
    }
    private void hideObjects(){
        paneDeatails.setVisible(true);
        exitButton.setVisible(false);
        rectangle.setVisible(false);
        triangle.setVisible(false);
        labelTowers.setVisible(false);

    }
    private void backToMenu(){
        paneDeatails.setVisible(false);
        widthInput.setText("");
        heightInput.setText("");
        exitButton.setVisible(true);
        rectangle.setVisible(true);
        triangle.setVisible(true);
        labelTowers.setVisible(true);
    }
    private String repeat(String original, int times){
        String result = "";
        for (int i = 0; i < times; i++) {
            result += original;
        }
        return result;
    }
}