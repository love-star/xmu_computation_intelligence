import java.util.HashSet;
import java.util.LinkedList;
import java.util.Set;
class State {
    int E;
    int S;

    public State(int e, int s) {
        E = e;
        S = s;
    }
}

public class Solution3 {
    static LinkedList<State> queue = new LinkedList<>();
    static Set<State> visited = new HashSet<>();
    private static boolean isVisited(State s) {
        for(State iterator : visited) {
            if (iterator.E == s.E && iterator.S == s.S) {
                return true;
            }
        }
        return false;
    }
    private static void move(State s) {
        if (!isVisited(s)) {
            visited.add(s);
            queue.addLast(s);
        }
    }
    public static void main(String[] args) {
        int R = 10, E = 0, S = 0;
        int fE = 5, fS = 0;
        queue.addLast(new State(E, S));
        while (!queue.isEmpty()) {
            State cur = queue.removeFirst();
            E = cur.E;
            S = cur.S;
            System.out.println(R - E - S + " " + E + " " + S);
            if (E == fE && S == fS) {
                System.out.println("success!");
                break;
            }
            if (E < 7) move(new State(7, S));
            if (S < 3) move(new State(E, 3));
            if (E > 0) move(new State(0, S));
            if (S > 0) move(new State(E, 0));
            if (E > 0 && E + S <= 3) move(new State(0, E + S));
            if (S > 0 && E + S <= 7) move(new State(E + S, 0));
            if (S < 3 && E + S >= 3) move(new State(E + S - 3, 3));
            if (E < 7 && E + S >= 7) move(new State(7, E + S - 7));
        }

    }
}
