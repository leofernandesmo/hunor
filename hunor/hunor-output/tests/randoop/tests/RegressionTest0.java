import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runners.MethodSorters;

@FixMethodOrder(MethodSorters.NAME_ASCENDING)
public class RegressionTest0 {

    public static boolean debug = false;

    @Test
    public void test01() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test01");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) (short) 100, 100);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
    }

    @Test
    public void test02() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test02");
        java.lang.Object obj0 = new java.lang.Object();
        java.lang.Class<?> wildcardClass1 = obj0.getClass();
        java.lang.Class<?> wildcardClass2 = obj0.getClass();
        java.lang.Class<?> wildcardClass3 = obj0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertNotNull(wildcardClass3);
    }

    @Test
    public void test03() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test03");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 0, (int) '4');
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 10, (int) (short) 10);
        boolean boolean9 = greaterOrEqualThan0.function(0, 0);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test04() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test04");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) ' ', (int) '#');
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function((int) (byte) 100, 100);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
    }

    @Test
    public void test05() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test05");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass3 = greaterOrEqualThan0.getClass();
        boolean boolean6 = greaterOrEqualThan0.function(100, (int) (short) 0);
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertNotNull(wildcardClass3);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
    }

    @Test
    public void test06() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test06");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 0, (int) '4');
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 10, (int) (short) 10);
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass8 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass9 = greaterOrEqualThan0.getClass();
        boolean boolean12 = greaterOrEqualThan0.function((int) (short) 1, (int) (byte) 1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertNotNull(wildcardClass8);
        org.junit.Assert.assertNotNull(wildcardClass9);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test07() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test07");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 0, (int) '4');
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (int) (byte) 10);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
    }

    @Test
    public void test08() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test08");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 0, (int) '4');
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 10, (int) (short) 10);
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass8 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass9 = greaterOrEqualThan0.getClass();
        boolean boolean12 = greaterOrEqualThan0.function((int) (byte) 100, (int) (byte) 100);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertNotNull(wildcardClass8);
        org.junit.Assert.assertNotNull(wildcardClass9);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test09() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test09");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', (int) '#');
        java.lang.Class<?> wildcardClass4 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass5 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertNotNull(wildcardClass4);
        org.junit.Assert.assertNotNull(wildcardClass5);
    }

    @Test
    public void test10() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test10");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        boolean boolean4 = greaterOrEqualThan0.function((int) (byte) -1, (int) (byte) 10);
        boolean boolean7 = greaterOrEqualThan0.function(100, (int) 'a');
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
    }

    @Test
    public void test11() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test11");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 1, (int) '#');
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
    }

    @Test
    public void test12() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test12");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        boolean boolean9 = greaterOrEqualThan0.function(1, 0);
        java.lang.Class<?> wildcardClass10 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass11 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass12 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNotNull(wildcardClass10);
        org.junit.Assert.assertNotNull(wildcardClass11);
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test13() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test13");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        boolean boolean4 = greaterOrEqualThan0.function((int) (byte) -1, (int) (byte) 10);
        boolean boolean7 = greaterOrEqualThan0.function((int) (byte) 1, (int) (short) -1);
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + true + "'", boolean7 == true);
    }

    @Test
    public void test14() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test14");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 0, (int) '4');
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 10, (int) (short) 10);
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass8 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass9 = greaterOrEqualThan0.getClass();
        boolean boolean12 = greaterOrEqualThan0.function((int) 'a', 10);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertNotNull(wildcardClass8);
        org.junit.Assert.assertNotNull(wildcardClass9);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test15() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test15");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function((int) ' ', (int) (byte) -1);
        java.lang.Class<?> wildcardClass11 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertNotNull(wildcardClass11);
    }

    @Test
    public void test16() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test16");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) ' ', (int) '#');
        boolean boolean9 = greaterOrEqualThan0.function((int) (byte) 1, (int) (byte) 100);
        java.lang.Class<?> wildcardClass10 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass11 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass12 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(wildcardClass10);
        org.junit.Assert.assertNotNull(wildcardClass11);
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test17() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test17");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) ' ', (int) '#');
        boolean boolean9 = greaterOrEqualThan0.function((int) (short) 1, 100);
        boolean boolean12 = greaterOrEqualThan0.function((-1), (int) (byte) -1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
    }

    @Test
    public void test18() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test18");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (short) 0, (int) '4');
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 10, (int) (short) 10);
        boolean boolean9 = greaterOrEqualThan0.function((int) 'a', (int) (short) 100);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test19() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test19");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        boolean boolean5 = greaterOrEqualThan0.function((-1), (int) (byte) -1);
        boolean boolean8 = greaterOrEqualThan0.function((int) (byte) -1, (int) ' ');
        boolean boolean11 = greaterOrEqualThan0.function((int) ' ', (int) (short) -1);
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + true + "'", boolean11 == true);
    }

    @Test
    public void test20() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test20");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 100, (int) 'a');
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
    }

    @Test
    public void test21() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test21");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        boolean boolean5 = greaterOrEqualThan0.function((-1), (int) (byte) -1);
        boolean boolean8 = greaterOrEqualThan0.function((int) (byte) -1, (int) ' ');
        boolean boolean11 = greaterOrEqualThan0.function(0, (int) ' ');
        java.lang.Class<?> wildcardClass12 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + false + "'", boolean8 == false);
        org.junit.Assert.assertTrue("'" + boolean11 + "' != '" + false + "'", boolean11 == false);
        org.junit.Assert.assertNotNull(wildcardClass12);
    }

    @Test
    public void test22() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test22");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', (int) '#');
        boolean boolean6 = greaterOrEqualThan0.function((int) (short) -1, (int) (byte) 10);
        boolean boolean9 = greaterOrEqualThan0.function(0, (int) (short) 10);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
    }

    @Test
    public void test23() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test23");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) (short) 10, (int) (byte) 100);
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertNotNull(wildcardClass7);
    }

    @Test
    public void test24() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test24");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function((int) ' ', (int) (byte) 1);
        boolean boolean13 = greaterOrEqualThan0.function((int) (byte) 10, 0);
        boolean boolean16 = greaterOrEqualThan0.function(100, 100);
        java.lang.Class<?> wildcardClass17 = greaterOrEqualThan0.getClass();
        boolean boolean20 = greaterOrEqualThan0.function((int) (short) 10, (int) (byte) 1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertNotNull(wildcardClass17);
        org.junit.Assert.assertTrue("'" + boolean20 + "' != '" + true + "'", boolean20 == true);
    }

    @Test
    public void test25() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test25");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) ' ', (int) '#');
        boolean boolean9 = greaterOrEqualThan0.function((int) (short) 1, 100);
        java.lang.Class<?> wildcardClass10 = greaterOrEqualThan0.getClass();
        boolean boolean13 = greaterOrEqualThan0.function((int) (byte) 100, (-1));
        java.lang.Class<?> wildcardClass14 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertNotNull(wildcardClass10);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertNotNull(wildcardClass14);
    }

    @Test
    public void test26() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test26");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) 1, 0);
        java.lang.Class<?> wildcardClass4 = greaterOrEqualThan0.getClass();
        boolean boolean7 = greaterOrEqualThan0.function(0, (int) (byte) 1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertNotNull(wildcardClass4);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
    }

    @Test
    public void test27() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test27");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass3 = greaterOrEqualThan0.getClass();
        boolean boolean6 = greaterOrEqualThan0.function((-1), (int) '4');
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertNotNull(wildcardClass3);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
    }

    @Test
    public void test28() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test28");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        boolean boolean9 = greaterOrEqualThan0.function(1, 0);
        java.lang.Class<?> wildcardClass10 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass11 = greaterOrEqualThan0.getClass();
        boolean boolean14 = greaterOrEqualThan0.function(10, (int) (byte) 100);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertNotNull(wildcardClass10);
        org.junit.Assert.assertNotNull(wildcardClass11);
        org.junit.Assert.assertTrue("'" + boolean14 + "' != '" + false + "'", boolean14 == false);
    }

    @Test
    public void test29() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test29");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        boolean boolean5 = greaterOrEqualThan0.function(100, 10);
        boolean boolean8 = greaterOrEqualThan0.function((int) '4', (int) '#');
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertTrue("'" + boolean8 + "' != '" + true + "'", boolean8 == true);
    }

    @Test
    public void test30() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test30");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass3 = greaterOrEqualThan0.getClass();
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 100, (int) (byte) 100);
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function((int) (byte) 10, (int) 'a');
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertNotNull(wildcardClass3);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
    }

    @Test
    public void test31() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test31");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) (byte) 100, 10);
        boolean boolean9 = greaterOrEqualThan0.function(1, 1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
    }

    @Test
    public void test32() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test32");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        boolean boolean5 = greaterOrEqualThan0.function((-1), (int) (byte) -1);
        java.lang.Class<?> wildcardClass6 = greaterOrEqualThan0.getClass();
        boolean boolean9 = greaterOrEqualThan0.function((int) '#', (int) (short) 10);
        boolean boolean12 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertNotNull(wildcardClass6);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
    }

    @Test
    public void test33() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test33");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function((int) ' ', (int) (byte) 1);
        boolean boolean13 = greaterOrEqualThan0.function((int) (byte) 10, 0);
        boolean boolean16 = greaterOrEqualThan0.function(100, 100);
        java.lang.Class<?> wildcardClass17 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass18 = greaterOrEqualThan0.getClass();
        boolean boolean21 = greaterOrEqualThan0.function((int) (short) 0, (int) (short) 10);
        java.lang.Class<?> wildcardClass22 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + true + "'", boolean10 == true);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + true + "'", boolean16 == true);
        org.junit.Assert.assertNotNull(wildcardClass17);
        org.junit.Assert.assertNotNull(wildcardClass18);
        org.junit.Assert.assertTrue("'" + boolean21 + "' != '" + false + "'", boolean21 == false);
        org.junit.Assert.assertNotNull(wildcardClass22);
    }

    @Test
    public void test34() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test34");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) ' ', (int) '#');
        boolean boolean9 = greaterOrEqualThan0.function((int) (byte) 1, (int) (byte) 100);
        boolean boolean12 = greaterOrEqualThan0.function((int) (short) -1, (int) (byte) -1);
        java.lang.Class<?> wildcardClass13 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + true + "'", boolean12 == true);
        org.junit.Assert.assertNotNull(wildcardClass13);
    }

    @Test
    public void test35() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test35");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass3 = greaterOrEqualThan0.getClass();
        boolean boolean6 = greaterOrEqualThan0.function((int) '#', (int) (byte) 10);
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertNotNull(wildcardClass3);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
    }

    @Test
    public void test36() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test36");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        boolean boolean4 = greaterOrEqualThan0.function(0, (int) (short) 10);
        boolean boolean7 = greaterOrEqualThan0.function(0, (int) '#');
        java.lang.Class<?> wildcardClass8 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertTrue("'" + boolean4 + "' != '" + false + "'", boolean4 == false);
        org.junit.Assert.assertTrue("'" + boolean7 + "' != '" + false + "'", boolean7 == false);
        org.junit.Assert.assertNotNull(wildcardClass8);
    }

    @Test
    public void test37() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test37");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function((int) (short) -1, 0);
        boolean boolean13 = greaterOrEqualThan0.function(0, (int) (short) 0);
        boolean boolean16 = greaterOrEqualThan0.function((-1), (int) '4');
        boolean boolean19 = greaterOrEqualThan0.function(0, (int) '#');
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertTrue("'" + boolean13 + "' != '" + true + "'", boolean13 == true);
        org.junit.Assert.assertTrue("'" + boolean16 + "' != '" + false + "'", boolean16 == false);
        org.junit.Assert.assertTrue("'" + boolean19 + "' != '" + false + "'", boolean19 == false);
    }

    @Test
    public void test38() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test38");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        java.lang.Class<?> wildcardClass1 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass2 = greaterOrEqualThan0.getClass();
        boolean boolean5 = greaterOrEqualThan0.function((-1), (int) (byte) -1);
        java.lang.Class<?> wildcardClass6 = greaterOrEqualThan0.getClass();
        java.lang.Class<?> wildcardClass7 = greaterOrEqualThan0.getClass();
        boolean boolean10 = greaterOrEqualThan0.function(1, (int) '4');
        java.lang.Class<?> wildcardClass11 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertNotNull(wildcardClass1);
        org.junit.Assert.assertNotNull(wildcardClass2);
        org.junit.Assert.assertTrue("'" + boolean5 + "' != '" + true + "'", boolean5 == true);
        org.junit.Assert.assertNotNull(wildcardClass6);
        org.junit.Assert.assertNotNull(wildcardClass7);
        org.junit.Assert.assertTrue("'" + boolean10 + "' != '" + false + "'", boolean10 == false);
        org.junit.Assert.assertNotNull(wildcardClass11);
    }

    @Test
    public void test39() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test39");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) '4', 0);
        boolean boolean6 = greaterOrEqualThan0.function((int) 'a', (-1));
        boolean boolean9 = greaterOrEqualThan0.function(1, 0);
        boolean boolean12 = greaterOrEqualThan0.function((int) ' ', (int) (short) 100);
        java.lang.Class<?> wildcardClass13 = greaterOrEqualThan0.getClass();
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + true + "'", boolean3 == true);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + true + "'", boolean6 == true);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + true + "'", boolean9 == true);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertNotNull(wildcardClass13);
    }

    @Test
    public void test40() throws Throwable {
        if (debug)
            System.out.format("%n%s%n", "RegressionTest0.test40");
        br.ufal.ic.masg.operations.GreaterOrEqualThan greaterOrEqualThan0 = new br.ufal.ic.masg.operations.GreaterOrEqualThan();
        boolean boolean3 = greaterOrEqualThan0.function((int) (byte) -1, (int) 'a');
        boolean boolean6 = greaterOrEqualThan0.function((int) ' ', (int) '#');
        boolean boolean9 = greaterOrEqualThan0.function((int) (byte) 1, (int) (byte) 100);
        boolean boolean12 = greaterOrEqualThan0.function((int) ' ', (int) 'a');
        boolean boolean15 = greaterOrEqualThan0.function(10, (int) (short) 1);
        org.junit.Assert.assertTrue("'" + boolean3 + "' != '" + false + "'", boolean3 == false);
        org.junit.Assert.assertTrue("'" + boolean6 + "' != '" + false + "'", boolean6 == false);
        org.junit.Assert.assertTrue("'" + boolean9 + "' != '" + false + "'", boolean9 == false);
        org.junit.Assert.assertTrue("'" + boolean12 + "' != '" + false + "'", boolean12 == false);
        org.junit.Assert.assertTrue("'" + boolean15 + "' != '" + true + "'", boolean15 == true);
    }
}

