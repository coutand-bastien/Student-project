/*
 * 
 * Copyright (C) 2017 Emmanuel DESMONTILS
 * 
 * This library is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 2.1 of the
 * License, or (at your option) any later version.
 * 
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
 * USA
 * 
 * 
 * 
 * E-mail:
 * Emmanuel.Desmontils@univ-nantes.fr
 * 
 * 
 **/

/**
 * JFSM.java
 *
 * @Created: 2019-12-26
 * @author COUTAND Bastien, GARNIER Cyprien
 * @version 1.1
 * @what implementation of produit, mise en étoile et transposer
 */

import JFSM.*;
import Test.Test;

public class JFSM {
    public static void main(String[] argv) throws JFSMException {
        Test t = new Test();

        t.testOriginal();
        t.testLoad();
        t.testTP4();

        t.testAutomateNormal();
        t.testAutomateNonNormal1();
        t.testAutomateNonNormal2();

        t.testAutomateStandard();
        t.testAutomateNonStandard1();
        t.testAutomateNonStandard2();

        t.testAutomateProduit();
        
        t.testAutomateEtoile();
        t.testAutomateNonEtoile();
        t.testAutomateTranspose();
   }
}
