#include <cppunit/TestFixture.h>
#include <cppunit/TestAssert.h>
#include <cppunit/TestCaller.h>
#include <cppunit/TestSuite.h>
#include <cppunit/TestCase.h>

#include "../sniffing/parser.hpp"
#include "../persistance/measure_data.hpp"
//#include "../config.hpp"

using namespace std;

class TestParserMD : public CppUnit::TestFixture {

private:
  Parser * testParser;
  MeasureData * testMeasureData;

public:
  TestParserMD() : testParser(NULL), testMeasureData(NULL) {
  }
	virtual ~TestParserMD() {
		delete testParser;
    delete testMeasureData;
	}

  static CppUnit::Test *suite() {
  		CppUnit::TestSuite *suiteOfTests = new CppUnit::TestSuite("TestConfig");

  		suiteOfTests->addTest(new CppUnit::TestCaller<TestParserMD>("Test the parse function from Parser, writing the data to the buffer in the Measure Data and the get_list and append functions from Measure Data",
  				&TestParserMD::test_parsing_and_writing_to_buffer ));

  		return suiteOfTests;
  	}

  	void setUp() {
      md_struct_t md_struct;
      md_struct.MAX_SIZE = 5;
      md_struct.MAX_WORKERS = 2;
      md_struct.HOURS = 0;
      md_struct.MINUTES = 0;
      md_struct.SECONDS = 10;

      testMeasureData = new MeasureData(md_struct);
      testParser = new Parser(testMeasureData);

    }

  	void tearDown() {
    }

protected:
  void test_parsing_and_writing_to_buffer(){

  /* Packet with two MO and one MH */
  const unsigned char s[] = {
                0x00,0x04,0x00,0x00,0x00,0x13,0x00,0x04,0x00,0x00,0x00,
                0x23,0x08,0x00,0x45,0x00,0x00,0x74,0x00,0x01,0x00,0x00,
                0x3E,0x11,0x62,0x65,0x0A,0x00,0x05,0x0A,0x0A,0x00,0x01,
                0x0A,0x04,0x57,0x12,0xB6,0x00,0x60,0x00,0x00,0x04,0x00,
                0x00,0x0D,0x00,0x00,0x00,0x00,0x00,0x02,0x08,0x00,0x04,
                0xD2,0x04,0xD2,0x0A,0x00,0x05,0x0A,0x0A,0x00,0x01,0x0A,
                0x00,0x02,0x11,0x00,0x00,0x00,0x01,0x5A,0x45,0x51,0x79,
                0x6E,0x65,0xD8,0x00,0x00,0x00,0x00,0x1B,0x00,0x00,0x00,
                0x03,0x5A,0x45,0x51,0x79,0x6B,0x01,0x90,0x00,0x00,0x00,
                0x00,0x0E,0x45,0x00,0x00,0x1D,0x00,0x01,0x00,0x00,0x3F,
                0x11,0x60,0x0A,0x00,0x05,0x0A,0x0A,0x00,0x01,0x0A,0x04,
                0xD2,0x04,0xD2,0x00,0x09,0x14,0xA2,0x45,0x11,0x02,0xF4,
                0x6F};

    testParser->parse(s, 133);
    list<IHeader *> headers = testMeasureData->get_list();
    list<IHeader *>::iterator iter = headers.begin();

    int optionsNumber = 0;
    int mhNumber = 0;

    while(iter != headers.end()){
      if((*iter)->option==true){
        ++optionsNumber;
      } else {
        ++mhNumber;
        MeasureHeader * mh = dynamic_cast<MeasureHeader*>(*iter);
        CPPUNIT_ASSERT((*mh->fields).protocol == 17);
      }

      ++iter;
    }

    CPPUNIT_ASSERT(optionsNumber == 2);
    CPPUNIT_ASSERT(mhNumber == 1);

  }


};
