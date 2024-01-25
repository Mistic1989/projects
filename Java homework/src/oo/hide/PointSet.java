package oo.hide;

import java.util.Objects;

public class PointSet {
    public static void main(String[] args) {
        PointSet pointset = new PointSet();
        pointset.add(new Point(1, 1));
        pointset.add(new Point(1, 2));
        pointset.add(new Point(1, 3));

        pointset.remove(new Point(1, 4));
        pointset.remove(new Point(1, 2));

        System.out.println(pointset);
    }

    private Point[] setArray;
    private int counter;

    public PointSet(int capacity) {
        this.setArray = new Point[capacity];
    }

    public PointSet() {
        this( 10);
    }

    @Override
    public String toString() {
        String result = "";

        for (int i = 0; i < setArray.length; i++) {
            if (counter - 1 == i) {
                if (setArray[i] == null) {
                    result += "null";
                    break;
                }
                result += setArray[i].toString();
                break;
            }
            if (setArray[i] == null && i < counter) {
                result += "null, ";
                continue;
            }
            if (setArray[i] != null) {
                result += setArray[i].toString() + ", ";
            }
        }
        return result;
    }

    public void add(Point point) {
        if (!contains(point) && counter == setArray.length) {
            PointSet setArray2 = new PointSet(setArray.length * 2);
            for (int j = 0; j < setArray.length; j++) {
                setArray2.setArray[j] = setArray[j];
            }
            setArray = setArray2.setArray;
        }
        for (int i = 0; i < setArray.length; i++) {
            if (point == null && setArray[i] == null) {
                setArray[i] = null;
                counter++;
                break;
            }
            if (setArray[i] == null && !contains(point) && i >= counter) {
                setArray[i] = point;
                counter++;
                break;
            }
        }
    }

    public int size() {
        int count = 0;
        for (Point point : setArray) {
            if (point != null) {
                count++;
            }
        }
        return count;
    }

    public boolean contains(Point point) {
        for (Object each : setArray) {
            if (each == null && point == null) {
                return true;
            }
            if (each != null && each.equals(point)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public boolean equals(Object obj) {

        if (!(obj instanceof PointSet)) {
            return false;
        }

        PointSet other = (PointSet) obj;

        for (Object each : this.setArray) {
            for (Object each2 : other.setArray) {
                if (each != null && each2 == null) {
                    return false;
                }
                if (each == null && each2 != null) {
                    return false;
                }
                if (Objects.equals(each, each2)) {
                    return true;
                }
            }
        }
        return false;
    }

    public PointSet subtract(PointSet other) {
        PointSet newPointset = new PointSet();
        for (Point each : this.setArray) {
            if (each == null) {
                continue;
            }
            for (Object each2 : other.setArray) {
                if (each2 == null) {
                    continue;
                }
                if (Objects.equals(each, each2)) {
                    break;
                }
                newPointset.add(each);
            }
        }
        return newPointset;
    }

    public PointSet intersect(PointSet other) {
        PointSet newPointset = new PointSet();
        for (Point each : this.setArray) {
            if (each == null) {
                continue;
            }
            for (Object each2 : other.setArray) {
                if (each2 == null) {
                    continue;
                }
                if (each.equals(each2)) {
                    newPointset.add(each);
                }
            }
        }
        return newPointset;
    }

    public void remove(Point point) {
        PointSet setArray2 = new PointSet(setArray.length);
        for (Point each : setArray) {
            if (each != null && Objects.equals(each, point)) {
                int count = 0;
                for (Point each2 : setArray) {
                    if (each2 == each) {
                        counter--;
                        continue;
                    }
                    setArray2.setArray[count] = each2;
                    count++;
                }
                setArray = setArray2.setArray;
                break;
            }
        }
    }
}
