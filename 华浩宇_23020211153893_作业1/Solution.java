import java.util.Arrays;
import java.util.LinkedList;

class Path {
    private int[] Node;
    private int pre;

    public Path(int[] node, int pre) {
        Node = node;
        this.pre = pre;
    }

    public int[] getNode() {
        return Node;
    }

    public int getPre() {
        return pre;
    }
}

public class Solution {
    private static final int[] cap = {10, 7, 3};
    private static Path start = new Path(new int[]{10, 0, 0}, -1);
    private static Path[] que = new Path[1000];
    private static boolean[][][] tag = new boolean[11][8][4];

    public static void main(String[] args) {
        Path end = bfs(start, que);
        Path temp;
        LinkedList<String> output = new LinkedList<>();
        if (end != null) {
            temp = end;
            while (temp.getPre() != -1) {
                output.add(temp.getNode()[0] + " " + temp.getNode()[1] + " " + temp.getNode()[2]);
                temp = que[temp.getPre()];
            }
            output.add(temp.getNode()[0] + " " + temp.getNode()[1] + " " + temp.getNode()[2]);
        }
        while (output.size() != 0) {
            System.out.println(output.removeLast());
        }
    }

    public static void pour(int i, int j, int[] node) {
        if (node[i] >= (cap[j] - node[j])) {
            node[i] -= cap[j] - node[j];
            node[j] = cap[j];
        } else {
            node[j] += node[i];
            node[i] = 0;
        }
    }

    public static Path bfs(Path start, Path[] que) {
        int front = 0;
        int tail = 0;
        que[tail] = start;
        tail += 1;
        int[] cur = start.getNode();
        tag[cur[0]][cur[1]][cur[2]] = true;

        while (front <= tail) {
            Path path = que[front];
            for (int i = 0; i < 3; i++) {
                if (path.getNode()[i] != 0) {
                    for (int j = 0; j < 3; j++) {
                        int[] temp = Arrays.copyOf(path.getNode(), 3);
                        pour(i, (i + j) % 3, temp);
                        if (temp[0] == 5 && temp[1] == 5) {
                            que[tail] = new Path(temp, front);
                            return que[tail];
                        }
                        if (tag[temp[0]][temp[1]][temp[2]]) {
                            continue;
                        }
                        tag[temp[0]][temp[1]][temp[2]] = true;
                        que[tail] = new Path(temp, front);
                        tail += 1;

                    }

                }
            }
            front += 1;
        }
        return null;
    }
}
