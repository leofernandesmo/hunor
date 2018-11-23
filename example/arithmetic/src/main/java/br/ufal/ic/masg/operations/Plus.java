package br.ufal.ic.masg.operations;

import br.ufal.ic.masg.Operation;


public class Plus implements Operation {

    public double method(int var1, int var2) {
        return var1 + var2;
    }

    public String concat(String var1, String var2) {
        var1 = "AAAA" + "bbbb";
        return var1 + var2;
    }

}