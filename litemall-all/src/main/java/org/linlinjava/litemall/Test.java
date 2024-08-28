package org.linlinjava.litemall;

public class Test {
    public static void main(String[] args) {
        double lilv = 0.02301;
        double year = 10;
        double benjin = 50000;
        double benxi = 50000;
        for(int i = 1;i<=5;i++){
            double lixi = benjin*lilv;
            benxi = benjin+lixi;
            System.out.println("第"+i+"年末本息:"+benxi+",当年本金："+benjin+",当年利息："+lixi);

            benjin=benxi+50000;
        }

        benjin = benxi;
        lilv = 0.018;
        for(int i = 6;i<=20;i++){
            double lixi = benjin*lilv;
            benxi = benjin+lixi;
            System.out.println("第"+i+"年末本息:"+benxi+",当年本金："+benjin+",当年利息："+lixi);
            benjin = benxi;
        }


    }
}
