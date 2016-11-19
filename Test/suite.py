import sys
import unittest
import TestLoginUtp
import TestPautasTestUtp
import TestVercursoVergruposContactos1erMedioA
import TestVerCursoBonusMayor
import TestVerCursoBonusMenor
import TestVerCursoEditarNombre
import TestVerCursoEditarNotaMinima
import TestVerCursoEditarNotaMaxima
import TestVerCursoEditarNotaAprobacion
import TestVerCursoEditarFechaInicio
import TestVerCursoEditarFechaTermino
import HTMLTestRunner, time, os
 
class Test_Suite(unittest.TestCase):

    def test_main(self):
         
        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([            
            unittest.defaultTestLoader.loadTestsFromTestCase(TestLoginUtp.TestLoginUtp),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestPautasTestUtp.TestPautasTestUtp),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVercursoVergruposContactos1erMedioA.TestVercursoVergruposContactos1erMedioA),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoBonusMayor.TestVerCursoBonusMayor),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoBonusMenor.TestVerCursoBonusMenor), 
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoEditarNombre.TestVerCursoEditarNombre),       
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoEditarNotaMinima.TestVerCursoEditarNotaMinima),   
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoEditarNotaMaxima.TestVerCursoEditarNotaMaxima),  
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoEditarNotaAprobacion.TestVerCursoEditarNotaAprobacion),    
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoEditarFechaInicio.TestVerCursoEditarFechaInicio),  
            unittest.defaultTestLoader.loadTestsFromTestCase(TestVerCursoEditarFechaTermino.TestVerCursoEditarFechaTermino),                      
            ])
        dateTimeStamp = time.strftime('%Y%m%d_%H_%M_%S')
        if not os.path.exists("reports"): os.makedirs("reports")
        os.chdir("reports")
        buf = file("TestReport" + "_" + dateTimeStamp + ".html", 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
                stream=buf,
                title='Test the Report',
                description='Result of tests'
                )
        runner.run(self.suite)
#sdsa
import unittest
if __name__ == "__main__":
    unittest.main()