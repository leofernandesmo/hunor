package br.ufal.ic.easy.minimal;


public class Minimal {

    private int n;

    public Minimal(int n) {
        this.n = n;
    }

    public int method1(int x) {

        if (x <= 0 || x > this.n) {
            return 0;
        }

        return x * this.n;
    }

}