package br.ufal.ic.easy.minimal;

import org.junit.Assert;
import org.junit.Test;

public class MinimalTest {

    @Test
    public void method1T1() {
        Minimal minimal = new Minimal(0);
        Assert.assertEquals(0, minimal.method1(0));
    }

    @Test
    public void method1T2() {
        Minimal minimal = new Minimal(0);
        Assert.assertEquals(0, minimal.method1(-1));
    }

    @Test
    public void method1T3() {
        Minimal minimal = new Minimal(0);
        Assert.assertEquals(0, minimal.method1(1));
    }

    @Test
    public void method1T4() {
        Minimal minimal = new Minimal(-1);
        Assert.assertEquals(0, minimal.method1(1));
    }

    @Test
    public void method1T5() {
        Minimal minimal = new Minimal(1);
        Assert.assertEquals(1, minimal.method1(1));
    }

    @Test
    public void method1T6() {
        Minimal minimal = new Minimal(9);
        Assert.assertEquals(18, minimal.method1(2));
    }

    @Test
    public void method1T7() {
        Minimal minimal = new Minimal(9);
        Assert.assertEquals(0, minimal.method1(10));
    }
}
