import sys
import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import analyze_module.analyze_data as AnalyzeData

app = QApplication(sys.argv)

class AnalyzeDataTest(unittest.TestCase):
    def setUp(self):
        self.form = AnalyzeData.MainWindow()

    def test_defaults(self):
        '''Test GUI in its default state'''
        self.assertEqual(self.form.dbPortLineEdit.text(), '3306')

    def test_ipSrcLineEdit_groupA(self):
        QTest.keyClicks(self.form.ipSrcLineEdit, '10.0.1.10')
        QTest.keyClick(self.form.ipSrcLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskSrcLineEdit.text(), '8')


    def test_ipSrcLineEdit_groupB(self):
        QTest.keyClicks(self.form.ipSrcLineEdit, '128.168.12.12')
        QTest.keyClick(self.form.ipSrcLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskSrcLineEdit.text(), '16')


    def test_ipSrcLineEdit_groupC(self):
        QTest.keyClicks(self.form.ipSrcLineEdit, '192.168.12.12')
        QTest.keyClick(self.form.ipSrcLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskSrcLineEdit.text(), '24')


    def test_ipDstLineEdit_groupA(self):
        QTest.keyClicks(self.form.ipDstLineEdit, '10.0.1.10')
        QTest.keyClick(self.form.ipDstLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskDstLineEdit.text(), '8')


    def test_ipDstLineEdit_groupB(self):
        QTest.keyClicks(self.form.ipDstLineEdit, '128.168.12.12')
        QTest.keyClick(self.form.ipDstLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskDstLineEdit.text(), '16')


    def test_ipDstLineEdit_groupC(self):
        QTest.keyClicks(self.form.ipDstLineEdit, '192.168.12.12')
        QTest.keyClick(self.form.ipDstLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskDstLineEdit.text(), '24')


    def test_ipSrcLineEdit_regex(self):
        QTest.keyClicks(self.form.ipSrcLineEdit, '192.168.1.1.1')
        QTest.keyClick(self.form.ipSrcLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.ipSrcLineEdit.text(), '192.168.1.11')

    def test_ipDstLineEdit_regex(self):
        QTest.keyClicks(self.form.ipDstLineEdit, '3332.2.2.2')
        QTest.keyClick(self.form.ipDstLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.ipDstLineEdit.text(), '33.2.2.2')


    def test_maskDstLineEdit_regex(self):
        QTest.keyClicks(self.form.maskDstLineEdit, 'AAAb.91')
        QTest.keyClick(self.form.maskDstLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskDstLineEdit.text(), '9')

    def test_maskSrcLineEdit_regex(self):
        QTest.keyClicks(self.form.maskSrcLineEdit, 'AAAb.91')
        QTest.keyClick(self.form.maskSrcLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.maskSrcLineEdit.text(), '9')

    def test_portDstLineEdit_regex(self):
        QTest.keyClicks(self.form.portDstLineEdit, '11111111')
        QTest.keyClick(self.form.portDstLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.portDstLineEdit.text(), '11111')


    def test_portSrcLineEdit_regex(self):
        QTest.keyClicks(self.form.portSrcLineEdit, 'ABCDEFGHIJ123')
        QTest.keyClick(self.form.portSrcLineEdit, Qt.Key_Enter)
        self.assertEqual(self.form.portSrcLineEdit.text(), '123')

    def test_submit_button(self):
        self.assertFalse(self.form.button.isEnabled())
        QTest.keyClicks(self.form.ipSrcLineEdit, '192.168.1.1.1')
        self.assertFalse(self.form.button.isEnabled())
        QTest.keyClicks(self.form.ipDstLineEdit, '192.168.1.1.1')
        self.assertFalse(self.form.button.isEnabled())
        QTest.keyClicks(self.form.hostnameLineEdit, 'localhost')
        self.assertFalse(self.form.button.isEnabled())
        QTest.keyClicks(self.form.usernameLineEdit, 'user')
        self.assertFalse(self.form.button.isEnabled())

if __name__ == "__main__":
    unittest.main()