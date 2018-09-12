// This is a mutant program.
// Author : ysma

package br.ufal.ic.masg.operations;


import br.ufal.ic.masg.Operation;


public class GreaterOrEqualThan implements br.ufal.ic.masg.Operation
{

    public  boolean function( int var1, int var2 )
    {
        return var1 < var2;
    }

}
