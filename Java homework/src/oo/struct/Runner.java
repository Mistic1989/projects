package oo.struct;

import oo.struct.Point3D;
import org.junit.Test;

public class Runner {

    @Test
    public void coordinatesAsArrays() {

        int[][] trianglePoints = {{1, 1, 0}, {5, 1, 0}, {3, 7, 1}};

        for (int[] each : trianglePoints) {
            System.out.println(each[2]);
        }
    }

    @Test
    public void coordinatesAsObjects() {
        Point3D[] triangle = {new Point3D(1, 5, 3),
                              new Point3D(1, 1, 7),
                              new Point3D(0, 0, 1)};

        for (Point3D item : triangle) {
            System.out.println(item.z);
        }
    }
}