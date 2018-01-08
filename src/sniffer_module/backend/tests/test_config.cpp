#include <iostream>
#include <cppunit/TestSuite.h>
#include <cppunit/ui/text/TestRunner.h>

#include "test_config.hpp"
#include "test_parser_md.hpp"

using namespace std;

int main() {
	CppUnit::TextUi::TestRunner runner;

	cout << "Creating Test Suites:" << endl;
	runner.addTest(TestConfig::suite());
	cout<< "Running the unit tests."<<endl;
	runner.run();

	cout << "Creating Test Suites:" << endl;
	runner.addTest(TestParserMD::suite());
	runner.run();

	return 0;
}
