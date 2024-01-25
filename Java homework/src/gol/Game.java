package gol;

import java.util.ArrayList;
import java.util.List;

public class Game {

    private boolean[][] board = new boolean[15][20];

    public void markAlive(int x, int y) {
        board[x][y] = true;
    }

    public boolean isAlive(int x, int y) {
        return board[x][y];
    }

    public void toggle(int x, int y) {
        if (isAlive(x, y)) {
            board[x][y] = false;
        } else {
            markAlive(x, y);
        }
    }

    public Integer getNeighbourCount(int x, int y) {

        List<Boolean> result = new ArrayList<>();
        for (int row = 0; row < 15; row++) {
            for (int col = 0; col < 20; col++) {

                List<Boolean> conditions = List.of(row != 0, col != 0, row != 14, col != 19,
                        row != 0 && col != 0, row != 14 && col != 19, row != 0 && col != 19, row != 14 && col != 0);

                if (col == y && row == x) {
                    addToResultIfTrue(-1, 0, result, conditions.get(0), row, col);
                    addToResultIfTrue(0, -1, result, conditions.get(1), row, col);
                    addToResultIfTrue(1, 0, result, conditions.get(2), row, col);
                    addToResultIfTrue(0, 1, result, conditions.get(3), row, col);
                    addToResultIfTrue(-1, -1, result, conditions.get(4), row, col);
                    addToResultIfTrue(1, 1, result, conditions.get(5), row, col);
                    addToResultIfTrue(-1, 1, result, conditions.get(6), row, col);
                    addToResultIfTrue(1, -1, result, conditions.get(7), row, col);

                    return result.size();
                }
            }
        }

        return 0;
    }

    public void addToResultIfTrue(Integer calcRow, Integer calcCol, List<Boolean> result,
                                  Boolean condition, Integer row, Integer col) {

        if (condition && board[row + calcRow][col + calcCol]) {
            result.add(true);
        }
    }

    public void nextFrame() {

        boolean[][] boardCopy = new boolean[15][];
        for (int i = 0; i < board.length; i++) {
            boardCopy[i] = board[i].clone();
        }

        for (int row = 0; row < 15; row++) {
            for (int col = 0; col < 20; col++) {
                if (nextState(isAlive(row, col), getNeighbourCount(row, col))) {
                    boardCopy[row][col] = true;
                } else {
                    boardCopy[row][col] = false;
                }

            }
        }

        board = boardCopy;
    }

    public void clear() {
        board = new boolean[15][20];
    }

    public boolean nextState(boolean isLiving, int neighborCount) {
        if (!isLiving && neighborCount == 3) {
            return true;
        }
        return isLiving && neighborCount >= 2 && neighborCount <= 3;
    }
}
